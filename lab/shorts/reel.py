"""Reel: the vertical AI-short engine (2 Oct, the user: "go all in on best possible vids... impress me").

AI clips (Kling, Veo) and stills cut to a narration's word timings, then finished here: a film grade and grain, kinetic
captions with the spoken word lit, name cards, number stamps, a red pencil, a score ducked under the voice, sound effects.
1080x1920 at 30 fps, -14 LUFS, for TikTok, Shorts and Reels. A short is a spec (see lustig/make.py):

    SHOTS     [(start s, kind, source, options)]: kind "clip" (an mp4, slowed a little if short) or "still" (a png, pushed in)
    OVERLAYS  [dict(kind="name"|"stamp"|"redx"|"label", t0, t1, ...)]
    SFX       [(t, name in lab/out/sfx, gain dB)]
"""
import json
import os
import subprocess
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import audio_fx as fx  # noqa: E402

W, H, FPS = 1080, 1920, 30
FONT = {k: skia.Typeface.MakeFromFile(os.path.join(HERE, "fonts", f)) for k, f in
        (("cap", "Anton-Regular.ttf"), ("serif", "DMSerifDisplay-Regular.ttf"))}
FONT["mono"] = skia.Typeface.MakeFromFile(os.path.join(os.path.dirname(HERE), "ch2", "fonts", "IBMPlexMono-500.ttf")) \
    if os.path.exists(os.path.join(os.path.dirname(HERE), "ch2", "fonts", "IBMPlexMono-500.ttf")) else FONT["cap"]
GOLD, RED, WHITE = 0xFFFFC83D, 0xFFD62B1F, 0xFFFFFFFF
SFX_DIR = os.path.join(os.path.dirname(HERE), "out", "sfx")


def P(color, a=1.0, **kw):
    """A paint with the colour's own alpha scaled by a."""
    p = skia.Paint(AntiAlias=True, Color=color, **kw)
    p.setAlphaf(max(0.0, min(1.0, a * (((color >> 24) & 255) / 255.0))))
    return p


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- words and captions
def words(path, merge=(), fix=None):
    """Whisper words [(w, a, b)] with split numbers merged ("7" ",000") and spellings fixed."""
    ws = [list(w) for w in json.load(open(path))]
    out = []
    for w in ws:
        if out and w[0].startswith(",") and out[-1][0].replace(",", "").isdigit():
            out[-1][0] += w[0]
            out[-1][2] = w[2]
            continue
        out.append(w)
    for w in out:
        bare = w[0].strip(".,;:!?")
        if fix and bare in fix:
            w[0] = w[0].replace(bare, fix[bare])
    return [tuple(w) for w in out]


def chunks(ws, max_words=3, max_chars=15):
    """Caption groups: break after punctuation, at max_words or when the line would run long."""
    groups, cur = [], []
    for w in ws:
        if cur and (len(cur) >= max_words or len(" ".join(x[0] for x in cur + [w])) > max_chars):
            groups.append(cur)
            cur = []
        cur.append(w)
        if w[0][-1] in ".,?!:;":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for i, g in enumerate(groups):
        t1 = groups[i + 1][0][1] if i + 1 < len(groups) else g[-1][2] + 0.6
        out.append(dict(words=g, t0=g[0][1] - 0.04, t1=min(t1, g[-1][2] + 0.6)))
    return out


def shown(w):
    return w.strip(",.;:").upper()


def draw_caption(c, cap, t, y=1310):
    if not (cap["t0"] <= t < cap["t1"]):
        return
    size = 104.0
    font = skia.Font(FONT["cap"], size)
    texts = [shown(w[0]) for w in cap["words"]]
    space = font.measureText(" ") * 1.7 + 6
    widths = [font.measureText(s) for s in texts]
    total = sum(widths) + space * (len(texts) - 1)
    if total > 960:
        k = 960 / total
        font = skia.Font(FONT["cap"], size * k)
        widths = [x * k for x in widths]
        space *= k
        total = 960
    pop = 0.9 + 0.1 * ease((t - cap["t0"]) / 0.08)
    c.save()
    c.translate(W / 2, y)
    c.scale(pop, pop)
    x = -total / 2
    for s, wd, w in zip(texts, widths, cap["words"]):
        active = w[1] - 0.03 <= t < w[2] + 0.05
        st = skia.Paint(AntiAlias=True, Color=0xFF000000, Style=skia.Paint.kStroke_Style, StrokeWidth=14,
                        StrokeJoin=skia.Paint.kRound_Join)
        sh = skia.Paint(AntiAlias=True, Color=0x88000000, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
        fill = skia.Paint(AntiAlias=True, Color=GOLD if active else WHITE)
        c.drawString(s, x + 4, 8, font, sh)
        c.drawString(s, x, 0, font, st)
        c.drawString(s, x, 0, font, fill)
        x += wd + space
    c.restore()


# ---------------------------------------------------------------- overlays
def draw_overlay(c, o, t):
    if not (o["t0"] <= t < o["t1"]):
        return
    a = ease((t - o["t0"]) / 0.25) * (1 - ease((t - (o["t1"] - 0.25)) / 0.25))
    k = o["kind"]
    if k == "name":                                   # a name card at the top: gold serif, a rule, a mono line
        y = o.get("y", 330)
        f1, f2 = skia.Font(FONT["serif"], 104), skia.Font(FONT["mono"], 34)
        dy = 24 * (1 - ease((t - o["t0"]) / 0.35))
        p1 = P(GOLD, a)
        sh = P(0xCC000000, a, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
        w1 = f1.measureText(o["title"])
        c.drawString(o["title"], W / 2 - w1 / 2 + 4, y + dy + 6, f1, sh)
        c.drawString(o["title"], W / 2 - w1 / 2, y + dy, f1, p1)
        rule = P(GOLD, 0.8 * a, StrokeWidth=3)
        half = (w1 / 2) * ease((t - o["t0"]) / 0.45)
        c.drawLine(W / 2 - half, y + 34 + dy, W / 2 + half, y + 34 + dy, rule)
        w2 = f2.measureText(o["sub"])
        c.drawString(o["sub"], W / 2 - w2 / 2 + 2, y + 92 + dy + 3, f2, sh)
        c.drawString(o["sub"], W / 2 - w2 / 2, y + 92 + dy, f2, P(WHITE, a))
    elif k == "stamp":                                # a rubber stamp that slams in, a little crooked
        u = (t - o["t0"]) / 0.12
        s = 1.0 + 0.45 * (1 - ease(u))
        shake = 6 * np.exp(-(t - o["t0"]) * 18) * np.sin((t - o["t0"]) * 90)
        f = skia.Font(FONT["cap"], o.get("size", 150))
        tw = f.measureText(o["text"])
        col = o.get("color", RED)
        c.save()
        c.translate(W / 2 + shake + o.get("dx", 0), o.get("y", 640))
        c.rotate(o.get("rot", -6))
        c.scale(s, s)
        box = skia.Rect.MakeLTRB(-tw / 2 - 34, -o.get("size", 150) * 0.86, tw / 2 + 34, o.get("size", 150) * 0.22)
        c.drawRect(box, P(0x55000000, a))
        c.drawRect(box, P(col, 0.92 * a, Style=skia.Paint.kStroke_Style, StrokeWidth=12))
        c.drawString(o["text"], -tw / 2, 0, f, P(col, 0.95 * a))
        c.restore()
    elif k == "redx":                                 # a red pencil crossing something out, stroke by stroke
        pen = P(RED, 0.92, StrokeWidth=26, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
        for i, ((x0, y0), (x1, y1)) in enumerate(o["lines"]):
            u = ease((t - o["t0"] - 0.32 * i) / 0.28)
            if u > 0:
                c.drawLine(x0, y0, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, pen)
    elif k == "label":                                # small mono text (the AI-reenactment label, a place and date)
        f = skia.Font(FONT["mono"], o.get("size", 28))
        tw = f.measureText(o["text"])
        x = {"left": 60, "center": W / 2 - tw / 2}[o.get("align", "left")]
        c.drawString(o["text"], x + 2, o["y"] + 2, f, P(0xAA000000, a))
        c.drawString(o["text"], x, o["y"], f, P(o.get("color", 0xDDFFFFFF), a))


# ---------------------------------------------------------------- pictures
def conform(src, dur, out):
    """An AI clip to exactly dur seconds at 1080x1920/30: cover-cropped, slowed (never more than 1.6x) if it runs short,
    its last frame held if it's still short."""
    clip = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                capture_output=True, text=True).stdout or 0)
    k = min(1.6, max(1.0, dur / max(0.1, clip)))
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setpts={k:.4f}*PTS,fps={FPS},"
          f"tpad=stop_mode=clone:stop_duration=2,trim=duration={dur:.3f}")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast",
                    "-pix_fmt", "yuv420p", out], check=True)


class Frames:
    """Sequential BGRA frames of a conformed clip."""
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "bgra", "-"],
                                  stdout=subprocess.PIPE)
        self.last = np.zeros((H, W, 4), np.uint8)

    def next(self):
        buf = self.p.stdout.read(W * H * 4)
        if len(buf) == W * H * 4:
            self.last = np.frombuffer(buf, np.uint8).reshape(H, W, 4).copy()
        return self.last.copy()

    def close(self):
        self.p.stdout.close()
        self.p.wait()


SEPIA = [0.393 * 0.8, 0.769 * 0.8, 0.189 * 0.8, 0, 0, 0.349 * 0.8, 0.686 * 0.8, 0.168 * 0.8, 0, 0,
         0.272 * 0.8, 0.534 * 0.8, 0.131 * 0.8, 0, 0, 0, 0, 0, 1, 0]


def draw_still(c, img, u, opt):
    """A still pushed in (scale s0 -> s1 over the shot, u in 0..1), optionally drifting and graded sepia."""
    s = opt.get("s0", 1.0) + (opt.get("s1", 1.12) - opt.get("s0", 1.0)) * ease(u) if opt.get("ease", True) else \
        opt.get("s0", 1.0) + (opt.get("s1", 1.12) - opt.get("s0", 1.0)) * u
    iw, ih = img.width(), img.height()
    base = max(W / iw, H / ih) * s
    dw, dh = iw * base, ih * base
    cx = W / 2 + opt.get("dx", 0) * u
    cy = H / 2 + opt.get("dy", 0) * u
    paint = skia.Paint(AntiAlias=True)
    if opt.get("sepia"):
        paint.setColorFilter(skia.ColorFilters.Matrix(SEPIA))
    c.drawImageRect(img, skia.Rect.MakeXYWH(cx - dw / 2, cy - dh / 2, dw, dh), skia.SamplingOptions(skia.FilterMode.kLinear), paint)


def finish(arr, rng, vig):
    """The shared film look: a gentle vignette and moving grain over every shot, so Kling, Veo and stills cut together."""
    rgb = arr[:, :, :3].astype(np.float32)
    rgb *= vig
    rgb += rng.normal(0, 3.2, (H // 3, W // 3, 1)).repeat(3, 0).repeat(3, 1).astype(np.float32)   # fine, light grain
    arr[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return arr


# ---------------------------------------------------------------- sound
def mix(voice_path, bed_path, words_, sfx, dur, out_wav, voice_db=-16.0, bed_db=-21.0, duck_db=-10.0):
    n = int(dur * fx.SR)
    v = fx.load(voice_path, mono=True)
    v = v if v.ndim == 1 else v.mean(1)
    room = fx.cinema_ir(rt60=1.1, predelay=0.015, seed=5, dark=0.6)
    v = fx.chain_voice(v, room=room, room_wet=-20.0, target=voice_db)
    v = fx.bq(fx.bq(v, "peak", 6800, q=2.0, gain_db=-3.5), "hshelf", 9000, gain_db=-2.5)   # softer esses, a darker top
    v = v if v.ndim == 2 else np.stack([v, v], 1)
    voice = np.zeros((n, 2), np.float32)
    voice[: min(n, len(v))] = v[: min(n, len(v))]
    talk = np.zeros(n, np.float32)
    for _, a, b in words_:
        talk[int(max(0, a - 0.1) * fx.SR): int((b + 0.22) * fx.SR)] = 1.0
    k = int(0.18 * fx.SR)
    talk = np.convolve(talk, np.ones(k) / k, mode="same").astype(np.float32)
    bed = fx.load(bed_path)
    bed = np.pad(bed, ((0, max(0, n - len(bed))), (0, 0)))[:n]
    bed = bed * fx.db(bed_db - fx.lufs(bed))
    lo = fx.bq(bed, "lp", 160)
    hi = bed - lo
    bed = lo * fx.db(duck_db * 0.5 * talk)[:, None] + hi * fx.db(duck_db * talk)[:, None]
    fxs = np.zeros((n, 2), np.float32)
    for t, name, g in sfx:
        x = fx.load(os.path.join(SFX_DIR, name + ".wav"))
        x = x if x.ndim == 2 else np.stack([x, x], 1)
        i = int(t * fx.SR)
        j = min(n, i + len(x))
        if j > i:
            fxs[i:j] += x[: j - i] * fx.db(g - 20.0)
    fade = np.clip((dur - np.arange(n) / fx.SR) / 0.6, 0, 1)[:, None]
    out = fx.master((voice + bed + fxs) * fade, target=-14.0, ceiling_db=-1.5)   # -1.5 dBTP: room for the AAC encode
    fx.save(out_wav, out, mp3=False)
    return out_wav


# ---------------------------------------------------------------- the render
def remix(spec, build, mp4):
    """New sound on a finished short (3 Oct, the jazz re-score): re-mix, then swap the audio track, picture untouched."""
    ws = words(spec["WORDS"], fix=spec.get("FIX"))
    wav = mix(spec["VOICE"], spec["BED"], ws, spec.get("SFX", []), spec["END"], os.path.join(build, "mix.wav"),
              bed_db=spec.get("BED_DB", -21.0), duck_db=spec.get("DUCK_DB", -10.0))
    tmp = mp4[:-4] + ".remix.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, mp4)
    print(mp4, round(os.path.getsize(mp4) / 1e6, 1), "MB (new sound)")
    return mp4


def render(spec, build, out_mp4):
    os.makedirs(build, exist_ok=True)
    shots, end = spec["SHOTS"], spec["END"]
    spans = [(s[0], shots[i + 1][0] if i + 1 < len(shots) else end) for i, s in enumerate(shots)]
    srcs = []
    for i, ((t0, t1), s) in enumerate(zip(spans, shots)):
        if s[1] == "clip":
            p = os.path.join(build, f"shot{i:02d}.mp4")
            conform(s[2], t1 - t0, p)
            srcs.append(p)
        else:
            srcs.append(skia.Image.open(s[2]))
    ws = words(spec["WORDS"], fix=spec.get("FIX"))
    caps = chunks(ws)
    wav = mix(spec["VOICE"], spec["BED"], ws, spec.get("SFX", []), end, os.path.join(build, "mix.wav"),
              bed_db=spec.get("BED_DB", -21.0), duck_db=spec.get("DUCK_DB", -10.0))
    yy, xx = np.mgrid[0:H, 0:W]
    vig = (1 - 0.38 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)).clip(0.45, 1)[:, :, None].astype(np.float32)
    rng = np.random.default_rng(7)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "19",
                            "-maxrate", "16M", "-bufsize", "32M",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_mp4],
                           stdin=subprocess.PIPE)
    cur, reader = -1, None
    for f in range(int(end * FPS)):
        t = f / FPS
        i = max(k for k, (a, _) in enumerate(spans) if a <= t + 1e-6)
        if i != cur:
            if reader:
                reader.close()
            reader = Frames(srcs[i]) if isinstance(srcs[i], str) else None
            cur = i
        if reader:
            arr = reader.next()
        else:
            arr = np.zeros((H, W, 4), np.uint8)
            s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
            a, b = spans[i]
            draw_still(s.getCanvas(), srcs[i], (t - a) / (b - a), shots[i][3] if len(shots[i]) > 3 else {})
            s.flushAndSubmit()
        arr = finish(arr, rng, vig)
        s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
        c = s.getCanvas()
        for o in spec.get("OVERLAYS", []):
            draw_overlay(c, o, t)
        for cap in caps:
            draw_caption(c, cap, t)
        s.flushAndSubmit()
        enc.stdin.write(arr.tobytes())
    if reader:
        reader.close()
    enc.stdin.close()
    enc.wait()
    print(out_mp4, round(os.path.getsize(out_mp4) / 1e6, 1), "MB")
    return out_mp4
