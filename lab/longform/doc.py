"""Doc: the 16:9 long-form documentary engine (2 Oct, the user: "target long form yt for money, shorts is bonus and
discovery"). A film is a folder with a film.py that defines

    SHOTS     [dict(t=start s, kind="clip"|"still"|"arch"|"gfx", ...)] in time order; each runs until the next starts.
              x = seconds of dissolve from the shot before (0 = a cut).
              clip  src (an mp4; slowed up to 1.6x if it runs short, then held)
              still src (a png/jpg), cam=((cx, cy, zoom), (cx, cy, zoom)) from start to end (centre in 0..1 of the
                    picture, zoom 1 = fills the frame), grade="bw"|"sepia"|"dim"|None
              arch  an archival photograph: as still, plus mode="print" (a framed print on a blurred bed of itself,
                    for pictures that don't fill 16:9), credit="..." (printed small, bottom right)
              gfx   fn=name in GFX (title cards, maps, documents, counters...), opt={...}
    OVERLAYS  [dict(kind=..., t0, t1, ...)]: label, name, stamp, redx, counter, lines, quote, box, ai, credit
    SFX       [(t, name in lab/out/sfx, gain dB)]
    MUSIC     [(t0, t1, wav)] beds, crossfaded, ducked under the voice
    VOICE, WORDS (build/voice.wav, build/words.json), END

and the engine renders it in segments (in parallel), joins them, mixes the sound and makes two files: a high-quality
master (CRF 17) and a delivery cut sized to fit a downloads page (two-pass, about 2.2 Mbit/s).

    python3 doc.py lustig frames 12.5 40 300      # QC stills at those seconds -> build/qc/
    python3 doc.py lustig render                    # everything -> out/
"""
import importlib.util
import json
import math
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
sys.path.insert(0, LAB)
import audio_fx as fx  # noqa: E402

W, H, FPS = 1920, 1080, 30
FONTS = os.path.join(LAB, "shorts", "fonts")
FONT = {"cap": skia.Typeface.MakeFromFile(os.path.join(FONTS, "Anton-Regular.ttf")),
        "serif": skia.Typeface.MakeFromFile(os.path.join(FONTS, "DMSerifDisplay-Regular.ttf")),
        "mono": skia.Typeface.MakeFromFile(os.path.join(FONTS, "IBMPlexMono-Medium.ttf")),
        "type": skia.Typeface.MakeFromFile(os.path.join(FONTS, "CourierPrime-Regular.ttf"))}
GOLD, CREAM, RED, INK, PAPER = 0xFFE2B866, 0xFFF1E6CF, 0xFFC8321F, 0xFF120F0B, 0xFFE9DCC0
SFX_DIR = os.path.join(LAB, "out", "sfx")


def P(color, a=1.0, **kw):
    p = skia.Paint(AntiAlias=True, Color=color, **kw)
    p.setAlphaf(max(0.0, min(1.0, a * (((color >> 24) & 255) / 255.0))))
    return p


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def fade(t, t0, t1, d=0.35):
    return ease((t - t0) / d) * (1 - ease((t - (t1 - d)) / d))


def text(c, s, x, y, font, paint, align="left", track=0.0):
    """Draw s with optional letter spacing; align left/center/right on x."""
    if track:
        widths = [font.measureText(ch) for ch in s]
        total = sum(widths) + track * (len(s) - 1)
        x0 = {"left": x, "center": x - total / 2, "right": x - total}[align]
        for ch, wd in zip(s, widths):
            c.drawString(ch, x0, y, font, paint)
            x0 += wd + track
        return total
    wd = font.measureText(s)
    c.drawString(s, {"left": x, "center": x - wd / 2, "right": x - wd}[align], y, font, paint)
    return wd


def shadow(a=0.8, blur=10):
    return P(0xFF000000, a, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))


# ---------------------------------------------------------------- pictures
_img = {}


def image(path):
    if path not in _img:
        if os.path.exists(path):
            _img[path] = skia.Image.open(path)
        else:                                   # not made yet: a labelled grey card, so a draft still renders
            surf = skia.Surface(1600, 900)
            cc = surf.getCanvas()
            cc.clear(0xFF2A2A2A)
            text(cc, "MISSING: " + os.path.basename(path), 800, 470, skia.Font(FONT["mono"], 40), P(0xFFBBBBBB), align="center")
            _img[path] = surf.makeImageSnapshot()
    return _img[path]


def grade_filter(g):
    if g == "bw":            # archival black and white, a touch warm and contrasty
        r = [0.33 * 1.12, 0.62 * 1.12, 0.12 * 1.12, 0, -0.05]       # skia's offsets are 0..1
        gg = [0.31 * 1.09, 0.60 * 1.09, 0.11 * 1.09, 0, -0.05]
        b = [0.28 * 1.02, 0.55 * 1.02, 0.10 * 1.02, 0, -0.05]
        return skia.ColorFilters.Matrix(r + gg + b + [0, 0, 0, 1, 0])
    if g == "sepia":
        return skia.ColorFilters.Matrix([0.393 * .85, 0.769 * .85, 0.189 * .85, 0, 0, 0.349 * .85, 0.686 * .85, 0.168 * .85, 0, 0,
                                         0.272 * .85, 0.534 * .85, 0.131 * .85, 0, 0, 0, 0, 0, 1, 0])
    if g == "dim":
        return skia.ColorFilters.Matrix([0.42, 0, 0, 0, 0, 0, 0.42, 0, 0, 0, 0, 0, 0.42, 0, 0, 0, 0, 0, 1, 0])
    return None


def cam_at(cam, u):
    (x0, y0, z0), (x1, y1, z1) = cam
    e = ease(u)
    return x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, z0 * (z1 / z0) ** e


def draw_cover(c, img, cx, cy, z, paint=None, box=(0, 0, W, H)):
    """Draw img to fill box, zoomed by z around the picture point (cx, cy) (clamped inside the picture)."""
    bx, by, bw, bh = box
    iw, ih = img.width(), img.height()
    s = max(bw / iw, bh / ih) * z
    ww, wh = bw / s, bh / s
    px = min(max(cx * iw, ww / 2), iw - ww / 2)
    py = min(max(cy * ih, wh / 2), ih - wh / 2)
    src = skia.Rect.MakeXYWH(px - ww / 2, py - wh / 2, ww, wh)
    c.drawImageRect(img, src, skia.Rect.MakeXYWH(bx, by, bw, bh), skia.SamplingOptions(skia.FilterMode.kLinear,
                    skia.MipmapMode.kLinear), paint or skia.Paint(AntiAlias=True))


def draw_still(c, sh, u):
    img = image(sh["src"])
    cx, cy, z = cam_at(sh.get("cam", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.08))), u)
    p = skia.Paint(AntiAlias=True)
    f = grade_filter(sh.get("grade"))
    if f:
        p.setColorFilter(f)
    draw_cover(c, img, cx, cy, z, p)


_beds = {}


def print_bed(path, grade):
    """A blurred, darkened copy of a picture that fills the frame (the bed a framed print sits on)."""
    key = (path, grade)
    if key not in _beds:
        img = image(path)
        surf = skia.Surface(W // 4, H // 4)
        cc = surf.getCanvas()
        p = skia.Paint(AntiAlias=True)
        p.setColorFilter(skia.ColorFilters.Compose(grade_filter("dim"), grade_filter(grade) or grade_filter("dim")))
        draw_cover(cc, img, 0.5, 0.5, 1.3, p, (0, 0, W // 4, H // 4))
        a = surf.makeImageSnapshot().toarray()
        a = cv2.GaussianBlur(a, (0, 0), 9)
        _beds[key] = skia.Image.fromarray(np.ascontiguousarray(a))
    return _beds[key]


def draw_arch(c, sh, u):
    if sh.get("mode") != "print":
        sh2 = dict(sh, grade=sh.get("grade", "bw"))
        draw_still(c, sh2, u)
        return
    img = image(sh["src"])
    bed = print_bed(sh["src"], sh.get("grade", "bw"))
    c.drawImageRect(bed, skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear))
    cx, cy, z = cam_at(sh.get("cam", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.07))), u)
    iw, ih = img.width(), img.height()
    fit = sh.get("fit", 0.8)
    s = min(W * 0.86 / iw, H * fit / ih)
    pw, ph = iw * s, ih * s
    border = max(10, pw * 0.025)
    c.save()
    c.translate(W / 2 + (0.5 - cx) * 300 * (z - 1) * 4, H / 2 + (0.5 - cy) * 200 * (z - 1) * 4)
    c.scale(z, z)
    c.rotate(sh.get("rot", -1.2))
    r = skia.Rect.MakeXYWH(-pw / 2 - border, -ph / 2 - border, pw + 2 * border, ph + 2 * border)
    c.drawRect(r.makeOffset(10, 16), shadow(0.7, 24))
    c.drawRect(r, P(0xFFEFE6D2))
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(grade_filter(sh.get("grade", "bw")))
    c.drawImageRect(img, skia.Rect.MakeXYWH(-pw / 2, -ph / 2, pw, ph), skia.SamplingOptions(skia.FilterMode.kLinear,
                    skia.MipmapMode.kLinear), p)
    c.restore()


# ---------------------------------------------------------------- clips
def conform(src, dur, out):
    clip = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                capture_output=True, text=True).stdout or 0)
    k = min(1.6, max(1.0, dur / max(0.1, clip)))
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setpts={k:.4f}*PTS,fps={FPS},"
          f"tpad=stop_mode=clone:stop_duration=4,trim=duration={dur + 0.2:.3f}")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-crf", "12",
                    "-preset", "fast", "-pix_fmt", "yuv420p", out], check=True)


class Frames:
    def __init__(self, path, start=0.0):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", path, "-f", "rawvideo",
                                   "-pix_fmt", "bgra", "-"], stdout=subprocess.PIPE)
        self.last = np.zeros((H, W, 4), np.uint8)

    def next(self):
        buf = self.p.stdout.read(W * H * 4)
        if len(buf) == W * H * 4:
            self.last = np.frombuffer(buf, np.uint8).reshape(H, W, 4).copy()
        return self.last.copy()

    def close(self):
        self.p.stdout.close()
        self.p.kill()
        self.p.wait()


# ---------------------------------------------------------------- the finish
class Finish:
    """Vignette and moving grain, the same over every shot, so Kling, GPT stills, archive and graphics cut together."""
    def __init__(self, seed=7, grain=2.6):
        yy, xx = np.mgrid[0:H, 0:W]
        v = (1 - 0.34 * (((xx - W / 2) / (W * 0.6)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)).clip(0.5, 1)
        self.vig = (v * 256).astype(np.uint16)[:, :, None]
        rng = np.random.default_rng(seed)
        small = rng.normal(0, grain, (12, H // 3, W // 3)).astype(np.float32)
        self.bank = [cv2.resize(s, (W, H), interpolation=cv2.INTER_NEAREST).astype(np.int16) for s in small]
        self.rng = rng

    def __call__(self, arr, f):
        rgb = (arr[:, :, :3].astype(np.uint16) * self.vig) >> 8
        n = self.bank[(f * 7 + int(self.rng.integers(0, 12))) % 12]
        rgb = rgb.astype(np.int16) + n[:, :, None]
        arr[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
        return arr


# ---------------------------------------------------------------- overlays
def draw_overlay(c, o, t):
    if not (o["t0"] <= t < o["t1"]):
        return
    a = fade(t, o["t0"], o["t1"], o.get("fd", 0.35))
    dt = t - o["t0"]
    k = o["kind"]
    if k == "label":                                   # a place and a date, top left
        f = skia.Font(FONT["mono"], o.get("size", 30))
        x, y = o.get("x", 96), o.get("y", 110)
        rule = 60 * ease(dt / 0.5)
        c.drawLine(x, y - 44, x + rule, y - 44, P(GOLD, a, StrokeWidth=3))
        text(c, o["text"], x + 2, y + 2, f, P(0xFF000000, 0.7 * a), track=4)
        text(c, o["text"], x, y, f, P(o.get("color", CREAM), a), track=4)
        if o.get("sub"):
            f2 = skia.Font(FONT["mono"], 22)
            text(c, o["sub"], x, y + 38, f2, P(GOLD, 0.9 * a), track=3)
    elif k == "ai":                                    # the reconstruction tag, small, top right
        f = skia.Font(FONT["mono"], 19)
        text(c, o.get("text", "AI RECONSTRUCTION"), W - 70, 66, f, P(CREAM, 0.55 * a), align="right", track=3)
    elif k == "credit":
        f = skia.Font(FONT["mono"], 18)
        text(c, o["text"], W - 70, H - 52, f, P(CREAM, 0.6 * a), align="right", track=1)
    elif k == "name":                                  # a lower third: gold bar, serif name, mono line
        x, y = o.get("x", 120), o.get("y", 860)
        sl = 40 * (1 - ease(dt / 0.5))
        f1, f2 = skia.Font(FONT["serif"], o.get("size", 72)), skia.Font(FONT["mono"], 26)
        c.drawRect(skia.Rect.MakeXYWH(x - 28, y - 64, 6, 110 * ease(dt / 0.4)), P(GOLD, a))
        text(c, o["title"], x + 4 - sl, y + 5, f1, shadow(0.8 * a, 12))
        text(c, o["title"], x - sl, y, f1, P(CREAM, a))
        text(c, o["sub"], x - sl, y + 46, f2, P(0xFF000000, 0.6 * a), track=4)
        text(c, o["sub"], x - sl, y + 44, f2, P(GOLD, a), track=4)
    elif k == "stamp":                                 # a rubber stamp that slams in, a little crooked
        u = dt / 0.12
        s = 1.0 + 0.4 * (1 - ease(u))
        shake = 7 * math.exp(-dt * 18) * math.sin(dt * 90)
        size = o.get("size", 120)
        f = skia.Font(FONT["cap"], size)
        tw = f.measureText(o["text"])
        col = o.get("color", RED)
        c.save()
        c.translate(o.get("x", W / 2) + shake, o.get("y", H / 2))
        c.rotate(o.get("rot", -6))
        c.scale(s, s)
        box = skia.Rect.MakeLTRB(-tw / 2 - 30, -size * 0.86, tw / 2 + 30, size * 0.22)
        c.drawRect(box, P(0x44000000, a))
        c.drawRect(box, P(col, 0.92 * a, Style=skia.Paint.kStroke_Style, StrokeWidth=10))
        c.drawString(o["text"], -tw / 2, 0, f, P(col, 0.95 * a))
        c.restore()
    elif k == "redx":
        pen = P(RED, 0.9 * a, StrokeWidth=o.get("w", 22), Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
        for i, ((x0, y0), (x1, y1)) in enumerate(o["lines"]):
            u = ease((dt - 0.3 * i) / 0.28)
            if u > 0:
                c.drawLine(x0, y0, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, pen)
    elif k == "counter":                               # a number that counts up: 0 -> value
        u = ease(dt / o.get("count", 1.4))
        v = o["value"] * u
        s = o.get("fmt", "{:,.0f}").format(v)
        s = o.get("pre", "") + s + o.get("post", "")
        size = o.get("size", 170)
        f = skia.Font(FONT["cap"], size)
        x, y = o.get("x", W / 2), o.get("y", H / 2 + size * 0.35)
        text(c, s, x + 6, y + 8, f, shadow(0.85 * a, 18), align="center")
        text(c, s, x, y, f, P(o.get("color", CREAM), a), align="center")
        if o.get("sub"):
            f2 = skia.Font(FONT["mono"], 34)
            text(c, o["sub"], x, y + 70, f2, P(0xFF000000, 0.7 * a), align="center", track=6)
            text(c, o["sub"], x, y + 68, f2, P(GOLD, a), align="center", track=6)
    elif k == "lines":                                 # lines of text that appear one after another
        f = skia.Font(FONT[o.get("font", "serif")], o.get("size", 60))
        x, y, gap = o.get("x", 160), o.get("y", 300), o.get("gap", 86)
        for i, (ti, s) in enumerate(o["items"]):
            if t < ti:
                continue
            b = a * ease((t - ti) / 0.35)
            dx = 24 * (1 - ease((t - ti) / 0.4))
            yy = y + i * gap
            if o.get("tick"):
                text(c, "—", x - 70 + dx, yy, f, P(GOLD, b))
            text(c, s, x + dx + 3, yy + 4, f, shadow(0.8 * b, 10), align=o.get("align", "left"))
            text(c, s, x + dx, yy, f, P(o.get("color", CREAM) if i != o.get("hi") else GOLD, b), align=o.get("align", "left"))
    elif k == "quote":                                 # a centred line or two of serif
        f = skia.Font(FONT["serif"], o.get("size", 76))
        y = o.get("y", H / 2)
        for i, s in enumerate(o["text"].split("\n")):
            yy = y + i * o.get("size", 76) * 1.25
            text(c, s, W / 2 + 3, yy + 5, f, shadow(0.85 * a, 14), align="center")
            text(c, s, W / 2, yy, f, P(o.get("color", CREAM), a), align="center")
        if o.get("sub"):
            f2 = skia.Font(FONT["mono"], 28)
            text(c, o["sub"], W / 2, y + 90 + (len(o["text"].split("\n")) - 1) * o.get("size", 76) * 1.25, f2,
                 P(GOLD, a), align="center", track=5)
    elif k == "box":                                   # a gold rectangle drawn round something (x, y, w, h)
        x, y, w, h = o["rect"]
        u = ease(dt / 0.6)
        pen = P(o.get("color", GOLD), a, StrokeWidth=6, Style=skia.Paint.kStroke_Style)
        per = 2 * (w + h) * u
        pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            seg = math.hypot(bx - ax, by - ay)
            if per <= 0:
                break
            k2 = min(1, per / seg)
            c.drawLine(ax, ay, ax + (bx - ax) * k2, ay + (by - ay) * k2, pen)
            per -= seg


# ---------------------------------------------------------------- graphics
GFX = {}


def gfx(fn):
    GFX[fn.__name__] = fn
    return fn


def paper_bg(c, tone=0xFF16120D):
    c.drawRect(skia.Rect.MakeWH(W, H), P(tone))
    g = skia.GradientShader.MakeRadial((W / 2, H * 0.45), W * 0.7, [0x22F1E6CF, 0x00000000])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=g))


@gfx
def card(c, dt, dur, opt):
    """A chapter card: the number in mono, the title in serif, a rule that draws, over a dark bed or a dimmed picture."""
    if opt.get("bg"):
        p = skia.Paint(AntiAlias=True)
        p.setColorFilter(grade_filter("dim"))
        draw_cover(c, image(opt["bg"]), 0.5, 0.5, 1.05 + 0.03 * dt / dur, p)
        c.drawRect(skia.Rect.MakeWH(W, H), P(0xAA000000))
    else:
        paper_bg(c)
    a = fade(dt, 0, dur, 0.45)
    f1, f2 = skia.Font(FONT["mono"], 30), skia.Font(FONT["serif"], opt.get("size", 112))
    text(c, opt.get("kicker", ""), W / 2, H / 2 - 92, f1, P(GOLD, a), align="center", track=10)
    rule = 260 * ease((dt - 0.15) / 0.8)
    c.drawLine(W / 2 - rule, H / 2 - 56, W / 2 + rule, H / 2 - 56, P(GOLD, 0.8 * a, StrokeWidth=2))
    sc = 1.0 + 0.03 * dt / dur
    c.save()
    c.translate(W / 2, H / 2 + 60)
    c.scale(sc, sc)
    text(c, opt["title"], 4, 6, f2, shadow(0.8 * a, 16), align="center")
    text(c, opt["title"], 0, 0, f2, P(CREAM, a), align="center")
    c.restore()


@gfx
def title(c, dt, dur, opt):
    """The film's title over a picture."""
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(grade_filter("dim"))
    draw_cover(c, image(opt["bg"]), 0.5, 0.5, 1.0 + 0.06 * dt / dur, p)
    a = fade(dt, 0, dur + 1, 0.8)
    f0, f1, f2 = skia.Font(FONT["mono"], 30), skia.Font(FONT["serif"], 128), skia.Font(FONT["mono"], 28)
    text(c, opt.get("kicker", ""), W / 2, H / 2 - 150, f0, P(GOLD, a), align="center", track=12)
    for i, line in enumerate(opt["lines"]):
        b = a * ease((dt - 0.25 - 0.3 * i) / 0.6)
        text(c, line, W / 2 + 5, H / 2 - 20 + i * 140 + 6, f1, shadow(0.8 * b, 18), align="center")
        text(c, line, W / 2, H / 2 - 20 + i * 140, f1, P(CREAM, b), align="center")
    if opt.get("sub"):
        text(c, opt["sub"], W / 2, H / 2 + 120 + (len(opt["lines"]) - 1) * 140, f2, P(GOLD, a * ease((dt - 1.0) / 0.6)),
             align="center", track=8)


@gfx
def plate(c, dt, dur, opt):
    """A dark plate for overlays to sit on (lists, quotes, counters), with an optional dimmed picture behind."""
    if opt.get("bg"):
        p = skia.Paint(AntiAlias=True)
        p.setColorFilter(grade_filter(opt.get("grade", "dim")))
        cam = opt.get("cam", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.06)))
        cx, cy, z = cam_at(cam, dt / dur)
        draw_cover(c, image(opt["bg"]), cx, cy, z, p)
        c.drawRect(skia.Rect.MakeWH(W, H), P(0xFF000000, opt.get("shade", 0.45)))
    else:
        paper_bg(c)


# ---- maps
_geo = {}


def geo(name):
    if name not in _geo:
        d = json.load(open(os.path.join(HERE, "data", name + ".geojson")))
        polys = []
        for ft in d["features"]:
            g = ft["geometry"]
            if g is None:
                continue
            rings = g["coordinates"] if g["type"] == "Polygon" else [r for p in g["coordinates"] for r in p]
            for r in rings:
                polys.append((np.array(r, np.float64), ft.get("properties", {})))
        _geo[name] = polys
    return _geo[name]


def lerp_view(v0, v1, u):
    e = ease(u)
    return tuple(a + (b - a) * e for a, b in zip(v0, v1))


def gmap(c, dt, dur, opt):
    """A dark period map: land, coasts (and US state lines if us=True), gold pins with labels, and routes drawn as
    arcs. view=(lon, lat, degrees of longitude across the frame) from v0 to v1. pins: [(lon, lat, label, t)];
    routes: [((lon, lat), (lon, lat), t0, t1)]."""
    c.drawRect(skia.Rect.MakeWH(W, H), P(0xFF0A0D11))
    v = lerp_view(opt["v0"], opt.get("v1", opt["v0"]), dt / max(0.1, opt.get("move", dur)))
    lon0, lat0, span = v
    kx = W / span
    ky = kx / math.cos(math.radians(lat0)) * math.cos(math.radians(lat0)) * 1.0
    clat = math.cos(math.radians(lat0))

    def proj(lon, lat):
        return W / 2 + (lon - lon0) * kx * clat, H / 2 - (lat - lat0) * kx

    land = skia.Path()
    for ring, _ in geo("ne_50m_land"):
        xs = W / 2 + (ring[:, 0] - lon0) * kx * clat
        ys = H / 2 - (ring[:, 1] - lat0) * kx
        if xs.max() < -50 or xs.min() > W + 50 or ys.max() < -50 or ys.min() > H + 50:
            continue
        land.moveTo(xs[0], ys[0])
        for x, y in zip(xs[1:], ys[1:]):
            land.lineTo(x, y)
        land.close()
    c.drawPath(land, P(0xFF332B20))
    c.drawPath(land, P(0xFFB39466, 0.75, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0))
    if opt.get("borders"):
        bl = skia.Path()
        for ring, props in geo(opt["borders"]):
            xs = W / 2 + (ring[:, 0] - lon0) * kx * clat
            ys = H / 2 - (ring[:, 1] - lat0) * kx
            if xs.max() < -50 or xs.min() > W + 50 or ys.max() < -50 or ys.min() > H + 50:
                continue
            bl.moveTo(xs[0], ys[0])
            for x, y in zip(xs[1:], ys[1:]):
                bl.lineTo(x, y)
        c.drawPath(bl, P(0xFF8C7650, 0.35, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0))
    # graticule
    gp = P(0xFF8C7650, 0.12, Style=skia.Paint.kStroke_Style, StrokeWidth=1)
    for lo in range(-180, 181, 10):
        x, _ = proj(lo, 0)
        c.drawLine(x, 0, x, H, gp)
    for la in range(-80, 81, 10):
        _, y = proj(0, la)
        c.drawLine(0, y, W, y, gp)
    for (a, b, t0, t1) in opt.get("routes", []):
        u = ease((dt - t0) / max(0.1, t1 - t0))
        if u <= 0:
            continue
        (x0, y0), (x1, y1) = proj(*a), proj(*b)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 0.18 * math.hypot(x1 - x0, y1 - y0)
        path = skia.Path()
        n = 60
        pts = [((1 - s) ** 2 * x0 + 2 * (1 - s) * s * mx + s * s * x1, (1 - s) ** 2 * y0 + 2 * (1 - s) * s * my + s * s * y1)
               for s in np.linspace(0, u, n)]
        path.moveTo(*pts[0])
        for p_ in pts[1:]:
            path.lineTo(*p_)
        dash = skia.Paint(AntiAlias=True, Color=GOLD, Style=skia.Paint.kStroke_Style, StrokeWidth=4,
                          PathEffect=skia.DashPathEffect.Make([16, 10], 0))
        c.drawPath(path, dash)
        c.drawCircle(*pts[-1], 8, P(GOLD))
    fl, fs = skia.Font(FONT["mono"], 30), skia.Font(FONT["mono"], 22)
    ft = skia.Font(FONT["mono"], 20)
    for lon, lat, name in opt.get("towns", []):                 # reference towns: small, grey, no pulse
        x, y = proj(lon, lat)
        c.drawCircle(x, y, 5, P(0xFFB39466, 0.7))
        text(c, name, x + 12, y + 7, ft, P(0xFFB39466, 0.75), track=2)
    for pin in opt.get("pins", []):
        lon, lat, label, t0 = pin[:4]
        sub = pin[4] if len(pin) > 4 else None
        u = ease((dt - t0) / 0.4)
        if u <= 0:
            continue
        x, y = proj(lon, lat)
        ring = (dt - t0) % 1.6 / 1.6
        c.drawCircle(x, y, 10 + 30 * ring, P(GOLD, 0.6 * (1 - ring) * u, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        c.drawCircle(x, y, 9 * u, P(GOLD))
        side = pin[5] if len(pin) > 5 else "right"
        tx = x + 26 if side == "right" else x - 26
        al = "left" if side == "right" else "right"
        text(c, label, tx + 2, y + 12, fl, P(0xFF000000, 0.8 * u), align=al, track=3)
        text(c, label, tx, y + 10, fl, P(CREAM, u), align=al, track=3)
        if sub:
            text(c, sub, tx, y + 44, fs, P(GOLD, u), align=al, track=2)
    if opt.get("caption"):
        f = skia.Font(FONT["mono"], 26)
        text(c, opt["caption"], 96, H - 90, f, P(GOLD, fade(dt, 0, dur)), track=5)


GFX["map"] = gmap


# ---- documents
@gfx
def letter(c, dt, dur, opt):
    """The forged letterhead on cream paper, lit from one side, the camera drifting over it."""
    c.drawRect(skia.Rect.MakeWH(W, H), P(0xFF1A140E))
    z = 1.0 + 0.08 * ease(dt / dur)
    c.save()
    c.translate(W / 2, H / 2 + 40)
    c.scale(z, z)
    c.rotate(-2.5)
    pw, ph = 1100, 1420
    r = skia.Rect.MakeXYWH(-pw / 2, -ph * 0.36, pw, ph)
    c.drawRect(r.makeOffset(16, 22), shadow(0.8, 30))
    c.drawRect(r, P(0xFFEDE3CB))
    g = skia.GradientShader.MakeLinear([(-pw / 2, 0), (pw / 2, 0)], [0x00000000, 0x30000000])
    c.drawRect(r, skia.Paint(Shader=g))
    ink = 0xFF1E2A3C
    y = -ph * 0.36 + 120
    f1, f2, f3, f4 = (skia.Font(FONT["serif"], 46), skia.Font(FONT["mono"], 24), skia.Font(FONT["serif"], 34),
                      skia.Font(FONT["mono"], 22))
    text(c, "RÉPUBLIQUE FRANÇAISE", 0, y - 40, f2, P(ink, 0.8), align="center", track=6)
    text(c, "MINISTÈRE DES POSTES", 0, y + 30, f1, P(ink), align="center")
    text(c, "ET TÉLÉGRAPHES", 0, y + 86, f1, P(ink), align="center")
    c.drawLine(-360, y + 122, 360, y + 122, P(ink, 0.8, StrokeWidth=2))
    text(c, "LE DIRECTEUR GÉNÉRAL ADJOINT", 0, y + 166, f2, P(ink, 0.85), align="center", track=4)
    text(c, "Paris, le ...  1925", pw / 2 - 90, y + 250, f3, P(ink, 0.75), align="right")
    for i in range(7):
        ww = [700, 820, 760, 800, 540, 780, 420][i]
        c.drawLine(-pw / 2 + 110, y + 330 + i * 58, -pw / 2 + 110 + ww, y + 330 + i * 58, P(ink, 0.18, StrokeWidth=12))
    if opt.get("stamp_t") is not None and dt > opt["stamp_t"]:
        u = (dt - opt["stamp_t"]) / 0.12
        s = 1 + 0.4 * (1 - ease(u))
        c.save()
        c.translate(220, y + 760)
        c.rotate(-8)
        c.scale(s, s)
        fs = skia.Font(FONT["cap"], 96)
        tw = fs.measureText("CONFIDENTIEL")
        c.drawRect(skia.Rect.MakeLTRB(-tw / 2 - 26, -84, tw / 2 + 26, 22), P(RED, 0.85, Style=skia.Paint.kStroke_Style, StrokeWidth=9))
        c.drawString("CONFIDENTIEL", -tw / 2, 0, fs, P(RED, 0.85))
        c.restore()
    c.restore()
    if opt.get("english"):
        a = fade(dt, opt.get("en_t", 1.2), dur, 0.4)
        f = skia.Font(FONT["mono"], 28)
        y0 = H - 150
        c.drawRect(skia.Rect.MakeXYWH(0, y0 - 60, W, 120), P(0xCC000000, a))
        text(c, opt["english"], W / 2, y0 + 10, f, P(GOLD, a), align="center", track=4)


@gfx
def record(c, dt, dur, opt):
    """A typed transcription of a document's key fields on a card, labelled as a transcription (used when the scan
    itself isn't available): opt.head, opt.fields [(label, value, t)], opt.hi [(field, t)] (boxed in red from t), opt.note."""
    c.drawRect(skia.Rect.MakeWH(W, H), P(0xFF15110C))
    z = 1.0 + 0.05 * ease(dt / dur)
    c.save()
    c.translate(W / 2, H / 2 + 20)
    c.scale(z, z)
    c.rotate(-1.2)
    pw, ph = 1240, 820
    r = skia.Rect.MakeXYWH(-pw / 2, -ph / 2, pw, ph)
    c.drawRect(r.makeOffset(14, 20), shadow(0.8, 28))
    c.drawRect(r, P(0xFFE9E0C8))
    ink = 0xFF22262E
    ft, fl, fv = skia.Font(FONT["mono"], 26), skia.Font(FONT["mono"], 22), skia.Font(FONT["type"], 44)
    text(c, opt.get("head", "CERTIFICATE OF DEATH"), 0, -ph / 2 + 90, ft, P(ink), align="center", track=8)
    c.drawLine(-pw / 2 + 80, -ph / 2 + 120, pw / 2 - 80, -ph / 2 + 120, P(ink, 0.6, StrokeWidth=2))
    y = -ph / 2 + 210
    for i, (label, value, t0) in enumerate(opt["fields"]):
        a = ease((dt - t0) / 0.35)
        text(c, label, -pw / 2 + 90, y, fl, P(ink, 0.7 * a), track=3)
        text(c, value, -pw / 2 + 90, y + 52, fv, P(0xFF1A2E5A, a))
        hit = [t for k, t in opt.get("hi", []) if k == i and dt > t]
        if hit:
            u = ease((dt - hit[0]) / 0.5)
            wv = fv.measureText(value)
            c.drawRect(skia.Rect.MakeXYWH(-pw / 2 + 74, y + 8, (wv + 32) * u, 64), P(RED, 0.9, Style=skia.Paint.kStroke_Style, StrokeWidth=5))
        y += 132
    c.restore()
    f = skia.Font(FONT["mono"], 20)
    text(c, opt.get("note", "TRANSCRIBED FROM THE RECORD"), W - 70, H - 52, f, P(CREAM, 0.6), align="right", track=2)


@gfx
def boxdiagram(c, dt, dur, opt):
    """How the Rumanian Box 'worked' (opt.reveal=False) and how it really worked (reveal=True)."""
    paper_bg(c)
    ink, gold = CREAM, GOLD
    fs, fm = skia.Font(FONT["mono"], 28), skia.Font(FONT["serif"], 52)

    def note(x, y, a, label="$100", col=0xFF6E8A5A, blank=False):
        r = skia.Rect.MakeXYWH(x - 120, y - 52, 240, 104)
        c.drawRect(r.makeOffset(6, 8), shadow(0.6 * a, 10))
        c.drawRect(r, P(0xFFEDE3CB if blank else col, a))
        if not blank:
            c.drawRect(r.makeInset(10, 10), P(0xFF2B3A24, 0.8 * a, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            c.drawCircle(x, y, 26, P(0xFF2B3A24, 0.6 * a, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
            text(c, label, x - 100, y - 18, skia.Font(FONT["mono"], 22), P(0xFF1A2414, a))
    a = fade(dt, 0, dur, 0.3)
    bx, by = W / 2, H / 2 + 30
    box = skia.Rect.MakeXYWH(bx - 260, by - 150, 520, 300)
    c.drawRect(box.makeOffset(10, 14), shadow(0.7 * a, 20))
    c.drawRect(box, P(0xFF5A2E1A, a))
    c.drawRect(box.makeInset(14, 14), P(0xFF7A4226, a, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    for i in range(5):
        c.drawCircle(bx - 160 + i * 80, by + 80, 20, P(0xFFC9A45C, a))
    c.drawRect(skia.Rect.MakeXYWH(bx - 150, by - 160, 120, 14), P(0xFF111111, a))
    c.drawRect(skia.Rect.MakeXYWH(bx + 30, by - 160, 120, 14), P(0xFF111111, a))
    text(c, opt.get("head", "HOW THE BOX 'WORKED'"), W / 2, 150, fs, P(gold, a), align="center", track=8)
    if not opt.get("reveal"):
        tc, to = opt.get("t_clock", 3.0), opt.get("t_out", 6.2)
        u1 = ease((dt - 0.6) / 1.2)
        gone = 1 - ease((dt - (tc - 1.0)) / 0.5)
        note(bx - 90 - 420 * (1 - u1), by - 260 - 60 * (1 - u1), a * gone)
        note(bx + 90 + 420 * (1 - u1), by - 260 - 60 * (1 - u1), a * gone, blank=True)
        text(c, "a real note  +  blank paper", W / 2, 250, fm, P(ink, a * ease((dt - 0.4) / 0.5) * (1 - ease((dt - tc) / 0.4))), align="center")
        cl = ease((dt - tc) / 0.4) * (1 - ease((dt - to - 0.2) / 0.4))          # the clock
        if cl > 0:
            cx, cy = W - 330, by - 40
            c.drawCircle(cx, cy, 90, P(0xFF000000, 0.5 * cl * a))
            c.drawCircle(cx, cy, 90, P(gold, cl * a, Style=skia.Paint.kStroke_Style, StrokeWidth=5))
            ang = (dt - tc) * 2.2
            c.drawLine(cx, cy, cx + 70 * math.sin(ang), cy - 70 * math.cos(ang), P(gold, cl * a, StrokeWidth=5))
            text(c, "6 HOURS", cx, cy + 150, fs, P(gold, cl * a), align="center", track=6)
        o = ease((dt - to) / 1.0)
        if o > 0:
            note(bx - 140 - 120 * o, by + 260, a * o)
            note(bx + 140 + 120 * o, by + 260, a * o)
            text(c, "two identical notes", W / 2, 250, fm, P(ink, a * ease((dt - to - 0.4) / 0.5)), align="center")
    else:
        # a cutaway: the real note hidden inside
        cut = ease((dt - 0.4) / 0.8)
        c.drawRect(box.makeInset(40, 40), P(0xFF140C08, a * cut))
        note(bx, by + 10, a * cut)
        hi = ease((dt - 1.4) / 0.5)
        c.drawRect(skia.Rect.MakeXYWH(bx - 140, by - 62, 280, 144), P(gold, hi * a, Style=skia.Paint.kStroke_Style, StrokeWidth=5))
        text(c, "THE SECRET: A REAL NOTE, HIDDEN INSIDE", W / 2, H - 120, fs, P(gold, a * hi), align="center", track=6)


@gfx
def phone(c, dt, dur, opt):
    """A modern phone with scam messages arriving."""
    if opt.get("bg"):
        p = skia.Paint(AntiAlias=True)
        p.setColorFilter(grade_filter("dim"))
        draw_cover(c, image(opt["bg"]), 0.5, 0.5, 1.05, p)
        c.drawRect(skia.Rect.MakeWH(W, H), P(0x99000000))
    else:
        paper_bg(c, 0xFF0D0F12)
    pw, ph = 560, 1000
    x0, y0 = W / 2 - pw / 2, H / 2 - ph / 2 + 40 - 30 * ease(dt / dur)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0, pw, ph), 70, 70)
    c.drawRRect(r, shadow(0.8, 30))
    c.drawRRect(r, P(0xFF0B0B0D))
    sr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + 18, y0 + 18, pw - 36, ph - 36), 56, 56)
    c.drawRRect(sr, P(0xFF17191D))
    fsm = skia.Font(FONT["mono"], 22)
    text(c, "Messages", W / 2, y0 + 92, skia.Font(FONT["mono"], 26), P(0xFFB9BEC6), align="center")
    y = y0 + 150
    for i, (ti, who, msg) in enumerate(opt["msgs"]):
        if dt < ti:
            continue
        u = ease((dt - ti) / 0.3)
        lines = msg.split("\n")
        bh = 40 + 34 * len(lines)
        br = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + 44, y + 30 * (1 - u), pw - 120, bh), 26, 26)
        c.drawRRect(br, P(0xFF2B2F36, u))
        text(c, who, x0 + 70, y + 30 * (1 - u) - 10, fsm, P(0xFF8D939C, u))
        for k2, ln in enumerate(lines):
            text(c, ln, x0 + 70, y + 30 * (1 - u) + 46 + k2 * 34, fsm, P(0xFFE8EAED, u))
        y += bh + 64


@gfx
def timeline(c, dt, dur, opt):
    """A horizontal line of years with marks that light up in turn: marks [(year, label, t)]."""
    paper_bg(c) if not opt.get("bg") else plate(c, dt, dur, opt)
    y0, y1 = opt["span"]
    xl, xr, yy = 220, W - 220, H / 2 + 40
    a = fade(dt, 0, dur, 0.3)
    c.drawLine(xl, yy, xl + (xr - xl) * ease(dt / 0.8), yy, P(GOLD, a, StrokeWidth=4))
    fy, fl = skia.Font(FONT["cap"], 92), skia.Font(FONT["mono"], 28)
    for yr, label, t0 in opt["marks"]:
        u = ease((dt - t0) / 0.4)
        if u <= 0:
            continue
        x = xl + (xr - xl) * (yr - y0) / (y1 - y0)
        c.drawCircle(x, yy, 14 * u, P(GOLD, a))
        text(c, str(yr), x, yy - 50, fy, P(CREAM, a * u), align="center")
        for k2, ln in enumerate(label.split("\n")):
            text(c, ln, x, yy + 70 + k2 * 36, fl, P(GOLD, a * u), align="center", track=3)


@gfx
def endcard(c, dt, dur, opt):
    """The end screen: a dimmed picture, the channel line and space for YouTube's two end-screen elements."""
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(grade_filter("dim"))
    draw_cover(c, image(opt["bg"]), 0.5, 0.5, 1.04 + 0.04 * dt / dur, p)
    c.drawRect(skia.Rect.MakeWH(W, H), P(0xB0000000))
    a = fade(dt, 0, dur + 2, 0.8)
    f1, f2 = skia.Font(FONT["serif"], 84), skia.Font(FONT["mono"], 28)
    text(c, opt.get("line", "MONEY CRIMES"), W / 2, 210, f1, P(CREAM, a), align="center")
    text(c, opt.get("sub", ""), W / 2, 270, f2, P(GOLD, a), align="center", track=8)    # YouTube's end screen sits below


# ---------------------------------------------------------------- the film
def load(film_dir):
    spec = importlib.util.spec_from_file_location("film", os.path.join(film_dir, "film.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def spans(shots, end):
    out = []
    for i, s in enumerate(shots):
        nxt = shots[i + 1] if i + 1 < len(shots) else None
        out.append((s["t"], (nxt["t"] + nxt.get("x", 0.0)) if nxt else end))
    return out


def prepare(film, build):
    """Conform every clip to its span (once; cached by span)."""
    os.makedirs(os.path.join(build, "shots"), exist_ok=True)
    for i, (sh, (a, b)) in enumerate(zip(film.SHOTS, spans(film.SHOTS, film.END))):
        if sh["kind"] == "clip" and not os.path.exists(sh["src"]) and sh.get("still"):
            sh.update(kind="still", src=sh["still"], cam=((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)))   # no clip yet: its still
        if sh["kind"] == "clip":
            out = os.path.join(build, "shots", f"{i:03d}_{os.path.basename(sh['src'])[:-4]}_{b - a:.2f}.mp4")
            if not os.path.exists(out):
                conform(sh["src"], b - a, out)
            sh["_conf"] = out


def draw_shot(c, sh, t, a, b, readers, i):
    if sh["kind"] == "clip":
        if i not in readers:
            readers[i] = Frames(sh["_conf"], max(0.0, t - a))
        return readers[i].next()
    arr = np.zeros((H, W, 4), np.uint8)
    s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
    cc = s.getCanvas()
    u = (t - a) / max(0.01, b - a)
    if sh["kind"] == "still":
        draw_still(cc, sh, u)
    elif sh["kind"] == "arch":
        draw_arch(cc, sh, u)
    else:
        GFX[sh["fn"]](cc, t - a, b - a, sh.get("opt", {}))
    s.flushAndSubmit()
    return arr


def frame_at(film, sp, t, readers, fin, f):
    """One frame at time t. fin=None leaves the grain and vignette to the delivery encode (LOOK)."""
    shots = film.SHOTS
    i = max(k for k, (a, _) in enumerate(sp) if a <= t + 1e-6)
    live = {i}
    arr = draw_shot(None, shots[i], t, *sp[i], readers, i)
    x = shots[i].get("x", 0.0)
    if i > 0 and x > 0 and t < shots[i]["t"] + x:
        prev = draw_shot(None, shots[i - 1], t, *sp[i - 1], readers, i - 1)
        live.add(i - 1)
        k = ease((t - shots[i]["t"]) / x)
        arr = cv2.addWeighted(arr, k, prev, 1 - k, 0)
    for j in list(readers):
        if j not in live:
            readers.pop(j).close()
    if fin:
        arr = fin(arr, f)
    s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
    c = s.getCanvas()
    for o in film.OVERLAYS:
        draw_overlay(c, o, t)
    s.flushAndSubmit()
    return arr


def render_segment(film_dir, t0, t1, out):
    film = load(film_dir)
    build = os.path.join(film_dir, "build")
    prepare(film, build)
    sp = spans(film.SHOTS, film.END)
    fin = None                                     # grain and vignette: once, in deliver() (LOOK)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r",
                            str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "superfast", "-crf", "16", "-pix_fmt", "yuv420p",
                            out], stdin=subprocess.PIPE)
    readers = {}
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    for f in range(f0, f1):
        enc.stdin.write(frame_at(film, sp, f / FPS, readers, fin, f).tobytes())
    for r in readers.values():
        r.close()
    enc.stdin.close()
    enc.wait()
    return out


def qc_frames(film_dir, times):
    film = load(film_dir)
    build = os.path.join(film_dir, "build")
    prepare(film, build)
    sp = spans(film.SHOTS, film.END)
    os.makedirs(os.path.join(build, "qc"), exist_ok=True)
    fin = Finish()
    paths = []
    for t in times:
        readers = {}
        arr = frame_at(film, sp, t, readers, fin, int(t * FPS))
        for r in readers.values():
            r.close()
        p = os.path.join(build, "qc", f"t{t:07.2f}.jpg")
        cv2.imwrite(p, arr[:, :, :3], [cv2.IMWRITE_JPEG_QUALITY, 88])
        paths.append(p)
    return paths


# ---------------------------------------------------------------- sound
def mix(film, out_wav, voice_db=-16.0, bed_db=-25.0, duck_db=-9.0):
    n = int(film.END * fx.SR)
    v = fx.load(film.VOICE, mono=True)
    v = v if v.ndim == 1 else v.mean(1)
    room = fx.cinema_ir(rt60=0.9, predelay=0.012, seed=5, dark=0.6)
    v = fx.chain_voice(v, room=room, room_wet=-22.0, target=voice_db)
    v = fx.bq(fx.bq(v, "peak", 6800, q=2.0, gain_db=-3.0), "hshelf", 9500, gain_db=-2.0)
    v = v if v.ndim == 2 else np.stack([v, v], 1)
    voice = np.zeros((n, 2), np.float32)
    voice[: min(n, len(v))] = v[: min(n, len(v))]
    talk = np.zeros(n, np.float32)
    for w in json.load(open(film.WORDS)):
        talk[int(max(0, w[1] - 0.12) * fx.SR): int((w[2] + 0.3) * fx.SR)] = 1.0
    k = int(0.25 * fx.SR)
    talk = np.convolve(talk, np.ones(k) / k, mode="same").astype(np.float32)
    bed = np.zeros((n, 2), np.float32)
    for t0, t1, path, gain in film.MUSIC:
        x = fx.load(path)
        x = x if x.ndim == 2 else np.stack([x, x], 1)
        x = x * fx.db(bed_db + gain - fx.lufs(x))
        i0 = int(t0 * fx.SR)
        m = min(len(x), int((t1 - t0) * fx.SR), n - i0)
        x = x[:m].copy()
        fi, fo = int(0.4 * fx.SR), int(1.6 * fx.SR)
        x[:fi] *= np.linspace(0, 1, fi)[:, None]
        x[-fo:] *= np.linspace(1, 0, fo)[:, None]
        bed[i0: i0 + m] += x
    lo = fx.bq(bed, "lp", 160)
    hi = bed - lo
    bed = lo * fx.db(duck_db * 0.5 * talk)[:, None] + hi * fx.db(duck_db * talk)[:, None]
    fxs = np.zeros((n, 2), np.float32)
    for t, name, g in film.SFX:
        x = fx.load(os.path.join(SFX_DIR, name + ".wav"))
        x = x if x.ndim == 2 else np.stack([x, x], 1)
        i = int(t * fx.SR)
        j = min(n, i + len(x))
        if j > i:
            fxs[i:j] += x[: j - i] * fx.db(g - 20.0)
    end = np.clip((film.END - np.arange(n) / fx.SR) / 2.0, 0, 1)[:, None]
    out = fx.master((voice + bed + fxs) * end, target=-14.0, ceiling_db=-1.5)   # -1.5 dBTP: AAC adds ~0.8 dB (finals were -0.2)
    fx.save(out_wav, out, mp3=False)
    return out_wav


# ---------------------------------------------------------------- the whole thing
def segments(film, build):
    cuts = [0.0] + [c for c in getattr(film, "SEGMENTS", []) if 0 < c < film.END] + [film.END]
    return [(a, b, os.path.join(build, f"seg_{i:02d}.mp4")) for i, (a, b) in enumerate(zip(cuts, cuts[1:]))]


def render(film_dir, only=None, workers=3):
    """Render segments (the ones listed, else every one not yet made) three at a time; once all exist, mix, join and
    deliver. A segment is one chapter, so a fix re-renders only its chapter: `doc.py <film> segs 7 10`."""
    film = load(film_dir)
    name = getattr(film, "NAME", "film")
    build, out = os.path.join(film_dir, "build"), os.path.join(film_dir, "out")
    os.makedirs(out, exist_ok=True)
    prepare(film, build)
    segs = segments(film, build)
    todo = [segs[i] for i in only] if only is not None else [x for x in segs if not os.path.exists(x[2])]
    with ProcessPoolExecutor(workers) as ex:
        futs = [ex.submit(render_segment, film_dir, a, b, p + ".part.mp4") for a, b, p in todo]
        for (a, b, p), fu in zip(todo, futs):
            os.replace(fu.result(), p)
            print("segment", os.path.basename(p), f"{a:.1f}-{b:.1f}", flush=True)
    if only is not None or not all(os.path.exists(p) for _, _, p in segs):
        return None
    wav = os.path.join(build, "mix.wav")
    if not os.path.exists(wav):
        mix(film, wav)
    lst = os.path.join(build, "segs.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for _, _, p in segs))
    hq = os.path.join(build, f"{name}_hq.mkv")          # the joined segments + the mix, no re-encode (CRF 15)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav, "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "flac", hq], check=True)
    deliver(hq, os.path.join(out, f"{name}_1080p.mp4"), film.END)
    return hq


LOOK = "vignette=angle=PI/6,noise=c0s=4:c0f=t"      # the film look over every shot: a soft vignette, moving luma grain


def deliver(src, dst, dur, mib=246, look=LOOK):
    """Two-pass to a size: the whole file inside mib MiB (a downloads page holds 256 MiB a version), with LOOK (or
    another filter, or none: The Curve's films bring their own look)."""
    total = mib * 8 * 1024 * 1024 / dur
    v = int(total - 160_000)
    log = dst + ".2pass"
    vf = ["-vf", look] if look else []
    base = ["ffmpeg", "-y", "-v", "error", "-i", src, *vf, "-c:v", "libx264", "-preset", "slow", "-tune", "film", "-b:v", str(v),
            "-maxrate", str(int(v * 1.8)), "-bufsize", str(int(v * 3)), "-pix_fmt", "yuv420p", "-passlogfile", log]
    subprocess.run(base + ["-pass", "1", "-an", "-f", "mp4", os.devnull], check=True)
    subprocess.run(base + ["-pass", "2", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", dst], check=True)
    for f in os.listdir(os.path.dirname(dst)):
        if f.startswith(os.path.basename(log)):
            os.remove(os.path.join(os.path.dirname(dst), f))
    print(dst, round(os.path.getsize(dst) / 2 ** 20, 1), "MiB")


if __name__ == "__main__":
    d = os.path.join(HERE, sys.argv[1])
    if sys.argv[2] == "frames":
        for p in qc_frames(d, [float(x) for x in sys.argv[3:]]):
            print(p)
    elif sys.argv[2] == "mix":
        print(mix(load(d), os.path.join(d, "build", "mix.wav")))
    elif sys.argv[2] == "segs":
        render(d, only=[int(x) for x in sys.argv[3:]])
    elif sys.argv[2] == "render":
        render(d)
