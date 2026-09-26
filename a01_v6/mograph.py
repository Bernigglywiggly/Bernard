"""A01 v6 mockup: "Chrome & Marl". Calm, clean motion graphics (skia, 1080p30).

Principles: the camera barely moves; the *elements* move. Lines form things (Tron-style), then flow
into the next form (morphs) instead of cutting. Heathered marl ground, chrome hero type, turquoise
as the one accent, emerald only for gains. Every number gets several everyday perspectives.

    python3 mograph.py            # renders $A01V6_BUILD/mockup_silent.mp4 (+ events.json for the SFX)
    python3 mograph.py --still 20 # one frame at 20 s -> still_20.png
"""
import json
import math
import os
import random
import subprocess
import sys

import numpy as np
import skia

W, H, FPS = 1920, 1080, 30
DUR = 55.5
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get("A01V6_FONTS", os.path.join(HERE, "fonts"))
BUILD = os.environ.get("A01V6_BUILD", os.path.join(HERE, "build"))

# ---------------------------------------------------------------- tokens
def hexc(h, a=1.0):
    h = h.lstrip("#")
    return skia.Color4f(int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


DARK, SLATE = (20, 22, 26), (27, 30, 35)          # graphite for forming, slate (with a dot grid) for explaining
ON_DARK, ON_DARK_MID, ON_DARK_SOFT = "#E9EBEE", "#C9CED6", "#8A919C"
LINE_DIM, CELL = "#3B424C", "#9AA2AD"
PANEL = ("#2A2F36", "#1F2329")                     # dark glass cards and tiles, top to bottom
TURQ, TURQ_GLOW, EMERALD = "#12B8AC", "#3FE6D8", "#12A36E"
CHROME = ["#FFFFFF", "#E4E8EC", "#A7AFBA", "#1F242B", "#5E6772", "#9FE9E2", "#EEF2F5", "#FFFFFF"]
CHROME_POS = [0.0, 0.18, 0.44, 0.50, 0.58, 0.74, 0.9, 1.0]

_TF = {}


def font(name, size):
    if name not in _TF:
        _TF[name] = skia.Typeface.MakeFromFile(os.path.join(FONTS, name + ".ttf"))
    f = skia.Font(_TF[name], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


DISPLAY, BODY, BODY_M, MONO, MONO_M = "Michroma-400", "InterTight-400", "InterTight-500", "IBMPlexMono-400", "IBMPlexMono-500"

# ---------------------------------------------------------------- timing helpers
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def ease(x, k="io"):
    x = clamp(x)
    if k == "io":
        return x * x * x * (x * (x * 6 - 15) + 10)
    if k == "o":
        return 1 - (1 - x) ** 3
    if k == "i":
        return x ** 3
    if k == "back":
        c = 1.4
        return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
    return x


def lerp(a, b, t):
    return a + (b - a) * t


EVENTS = []          # (time, kind) for the sound design; collected on the first pass only
_EV_ON = [False]


def ev(t_evt, kind, now, x=None, fps=FPS):
    """Register a sound event once, on the frame where it happens; x (screen px) places it in stereo."""
    if _EV_ON[0] and t_evt <= now < t_evt + 1.0 / fps:     # the first frame at/after the event
        EVENTS.append((round(t_evt, 3), kind, None if x is None else round(clamp((x - W / 2) / (W / 2), -1.0, 1.0), 2)))


def scr_x(c, x, y=0.0):
    """Where a local point lands on screen (to pan sounds made inside transformed layers)."""
    return c.getTotalMatrix().mapXY(float(x), float(y)).x()


# scene-level sound cues (independent of what happens to be drawn on the exact frame)
CUES = [(0.2, "whoosh"), (3.4, "chime"), (4.2, "chime"), (6.2, "morph"), (11.5, "morph"), (12.6, "shimmer"),
        (14.3, "thum"), (23.2, "thock"), (29.0, "thock"), (33.4, "thock"), (42.5, "thock"), (42.6, "pierce"),
        (43.6, "decode"), (44.4, "shimmer"), (46.2, "whoosh"), (52.6, "zoom"), (52.6, "tunnel")] + [(6.9 + i / 12, "count") for i in range(11)]


# ---------------------------------------------------------------- paints
def stroke(col, w=2.0, a=1.0, glow=0.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                   StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    p.setColor4f(hexc(col, a))
    if glow:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, glow))
    return p


def fill(col, a=1.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style)
    p.setColor4f(hexc(col, a))
    return p


def chrome_paint(y0, y1, a=1.0, shift=0.0):
    cols = [hexc(c, a) for c in CHROME]
    pos = [clamp(p + shift * 0.0) for p in CHROME_POS]
    sh = skia.GradientShader.MakeLinear(points=[(0, y0), (0, y1)], colors=cols, positions=pos)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style)
    p.setShader(sh)
    return p


def panel_paint(y0, y1, a=1.0):
    sh = skia.GradientShader.MakeLinear(points=[(0, y0), (0, y1)], colors=[hexc(PANEL[0], a), hexc(PANEL[1], a)])
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style)
    p.setShader(sh)
    return p


def glass(c, x, y, w, h, r, a=1.0, shadow=True):
    """A dark glass panel: soft drop shadow, top-lit gradient, a hairline highlight along the top edge."""
    if shadow:
        sh = fill("#000000", 0.45 * a)
        sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y + 18, w, h), r, r), sh)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), panel_paint(y, y + h, 0.96 * a))
    c.drawLine(x + r, y + 1, x + w - r, y + 1, stroke("#FFFFFF", 1, 0.07 * a))


# ---------------------------------------------------------------- ground (marl)
def marl(base, seed, amt):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (H, W)).astype(np.float32)
    streak = rng.normal(0, 1, (H // 2, W // 16)).astype(np.float32)          # heathered fibres
    streak = np.repeat(np.repeat(streak, 2, 0), 16, 1)[:H, :W]
    lum = n * amt + streak * amt * 0.6
    yy, xx = np.mgrid[0:H, 0:W]
    vig = 1 - 0.10 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    img = np.clip((np.array(base, np.float32)[None, None, :] + lum[..., None]) * vig[..., None], 0, 255).astype(np.uint8)
    rgba = np.dstack([img, np.full((H, W), 255, np.uint8)])
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


def slate_ground():
    """Slate marl with a faint dot grid: the explaining world (grid paper, in the dark)."""
    surf = skia.Surface(W, H)
    cc = surf.getCanvas()
    cc.drawImage(marl(SLATE, 1, 2.6), 0, 0)
    p = fill(ON_DARK, 0.07)
    for y in range(30, H, 48):
        for x in range(24, W, 48):
            cc.drawCircle(x, y, 1.3, p)
    return surf.makeImageSnapshot()


# ---------------------------------------------------------------- geometry helpers
def poly_len(pts):
    d = np.diff(pts, axis=0)
    return np.concatenate([[0], np.cumsum(np.hypot(d[:, 0], d[:, 1]))])


def draw_poly(c, pts, paint, frac=1.0):
    """Draw a polyline up to `frac` of its length (lines that draw themselves)."""
    pts = np.asarray(pts, float)
    if frac <= 0 or len(pts) < 2:
        return None
    L = poly_len(pts)
    target = L[-1] * clamp(frac)
    path = skia.Path()
    path.moveTo(*pts[0])
    tip = pts[0]
    for i in range(1, len(pts)):
        if L[i] <= target:
            path.lineTo(*pts[i])
            tip = pts[i]
        else:
            r = (target - L[i - 1]) / max(L[i] - L[i - 1], 1e-9)
            tip = pts[i - 1] + (pts[i] - pts[i - 1]) * r
            path.lineTo(*tip)
            break
    c.drawPath(path, paint)
    return tip


def arc(cx, cy, r, a0, a1, n=48):
    a = np.linspace(math.radians(a0), math.radians(a1), n)
    return np.column_stack([cx + r * np.cos(a), cy + r * np.sin(a)])


def rrect_pts(x, y, w, h, r, n=10):
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        pts.append(arc(cx, cy, r, a0, a0 + 90, n))
    p = np.vstack(pts)
    return np.vstack([p, p[:1]])


def resample(pts, n):
    """Resample a polyline to n points evenly by length (for morphs)."""
    pts = np.asarray(pts, float)
    L = poly_len(pts)
    s = np.linspace(0, L[-1], n)
    return np.column_stack([np.interp(s, L, pts[:, 0]), np.interp(s, L, pts[:, 1])])


def glyph_polys(text, fnt, x, y, samples=8):
    """Outline polylines of text (for line-drawing and morphing type)."""
    glyphs = fnt.textToGlyphs(text)
    xs = fnt.getXPos(glyphs)
    polys = []
    for g, gx in zip(glyphs, xs):
        p = fnt.getPath(g)
        if p is None:
            continue
        p.offset(x + gx, y)
        it = skia.Path.Iter(p, False)
        cur = []
        while True:
            verb, pts = it.next()
            if verb == skia.Path.Verb.kDone_Verb:
                break
            if verb == skia.Path.Verb.kMove_Verb:
                if len(cur) > 1:
                    polys.append(np.array(cur))
                cur = [(pts[0].x(), pts[0].y())]
            elif verb == skia.Path.Verb.kLine_Verb:
                cur.append((pts[1].x(), pts[1].y()))
            elif verb in (skia.Path.Verb.kQuad_Verb, skia.Path.Verb.kConic_Verb):
                p0, p1, p2 = pts[0], pts[1], pts[2]
                for tt in np.linspace(0, 1, samples)[1:]:
                    cur.append(((1 - tt) ** 2 * p0.x() + 2 * (1 - tt) * tt * p1.x() + tt * tt * p2.x(),
                                (1 - tt) ** 2 * p0.y() + 2 * (1 - tt) * tt * p1.y() + tt * tt * p2.y()))
            elif verb == skia.Path.Verb.kCubic_Verb:
                p0, p1, p2, p3 = pts
                for tt in np.linspace(0, 1, samples)[1:]:
                    mt = 1 - tt
                    cur.append((mt ** 3 * p0.x() + 3 * mt * mt * tt * p1.x() + 3 * mt * tt * tt * p2.x() + tt ** 3 * p3.x(),
                                mt ** 3 * p0.y() + 3 * mt * mt * tt * p1.y() + 3 * mt * tt * tt * p2.y() + tt ** 3 * p3.y()))
            elif verb == skia.Path.Verb.kClose_Verb:
                if cur:
                    cur.append(cur[0])
        if len(cur) > 1:
            polys.append(np.array(cur))
    return polys


def text_path(text, fnt, x, y):
    glyphs = fnt.textToGlyphs(text)
    xs = fnt.getXPos(glyphs)
    path = skia.Path()
    for g, gx in zip(glyphs, xs):
        p = fnt.getPath(g)
        if p is not None:
            p.offset(x + gx, y)
            path.addPath(p)
    return path


def text_w(text, fnt):
    return fnt.measureText(text)


# ---------------------------------------------------------------- building blocks
ASCII = "01#%&*+=-:.<>/\\|~^"


def decode(c, text, x, y, fnt, col, t, t0, dur=0.6, seed=0, align="left", a=1.0):
    """Mono text that resolves out of random characters, left to right (the ASCII decode)."""
    if t < t0:
        return
    rng = random.Random(seed + int(t * 24))
    n = len(text)
    tw = text_w(text, fnt)
    x -= tw / 2 if align == "center" else tw if align == "right" else 0
    shown = []
    for i, ch in enumerate(text):
        ti = t0 + dur * (i / max(n, 1))
        if ch == " ":
            shown.append(" ")
        elif t >= ti + 0.12:
            shown.append(ch)
        elif t >= ti - 0.18:
            shown.append(rng.choice(ASCII))
        else:
            shown.append(" ")
        ev(ti + 0.12, "tick", t, scr_x(c, x + tw * i / max(n, 1), y))
    c.drawString("".join(shown), x, y, fnt, fill(col, a))


def type_on(c, text, x, y, fnt, col, t, t0, cps=38, a=1.0):
    if t < t0:
        return
    n = int((t - t0) * cps)
    c.drawString(text[:n], x, y, fnt, fill(col, a))


def counter(c, v0, v1, x, y, fnt, col, t, t0, dur, fmt="{:.1f}", align="center", a=1.0):
    if t < t0:
        return
    v = lerp(v0, v1, ease(seg(t, t0, t0 + dur), "o"))
    s = fmt.format(v)
    ww = text_w(s, fnt)
    xx = x - ww / 2 if align == "center" else x
    c.drawString(s, xx, y, fnt, fill(col, a))


def dimension(c, x, y0, y1, col, t, t0, dur=0.7, label=None, fnt=None, lab_col=None, side=1):
    """Technical-drawing dimension line with ticks and a label."""
    k = ease(seg(t, t0, t0 + dur))
    if k <= 0:
        return
    p = stroke(col, 2)
    ym = (y0 + y1) / 2
    draw_poly(c, [(x, ym), (x, lerp(ym, y0, k))], p)
    draw_poly(c, [(x, ym), (x, lerp(ym, y1, k))], p)
    for yy in (y0, y1):
        c.drawLine(x - 14 * k, yy, x + 14 * k, yy, p)
    if label and k > 0.6:
        c.drawString(label, x + side * 26, ym + 10, fnt, fill(lab_col or col, clamp((k - 0.6) / 0.4)))


def grid100(c, x, y, size, t, n_base, n_extra, t_base, t_extra, col=CELL, extra_col=TURQ, remove=False, a=1.0):
    """The 'per hundred' motif: a 10x10 grid whose cells fill in (or empty out)."""
    cell = size / 10
    gap = cell * 0.18
    for i in range(100):
        r, q = divmod(i, 10)
        cx, cy = x + q * cell, y + r * cell
        rect = skia.Rect.MakeXYWH(cx + gap / 2, cy + gap / 2, cell - gap, cell - gap)
        c.drawRect(rect, stroke(ON_DARK_SOFT, 1, 0.35 * a))
        if not remove:
            if i < n_base:
                k = seg(t, t_base + i * 0.008, t_base + i * 0.008 + 0.12)
                if k > 0:
                    c.drawRect(rect, fill(col, 0.85 * k * a))
            elif i < n_base + n_extra:
                j = i - n_base
                k = seg(t, t_extra + j * 0.03, t_extra + j * 0.03 + 0.12)
                if k > 0:
                    c.drawRect(rect, fill(extra_col, k * a))
                    ev(t_extra + j * 0.03, "pip", t, scr_x(c, cx + cell / 2, cy))
        else:
            if i < n_base:
                keep = i < n_base - n_extra
                if keep:
                    k = seg(t, t_base + i * 0.008, t_base + i * 0.008 + 0.12)
                    c.drawRect(rect, fill(col, 0.85 * k * a))
                else:
                    j = i - (n_base - n_extra)
                    k_in = seg(t, t_base + i * 0.008, t_base + i * 0.008 + 0.12)
                    k_out = seg(t, t_extra + j * 0.03, t_extra + j * 0.03 + 0.15)
                    if k_out > 0:
                        ev(t_extra + j * 0.03, "pip", t, scr_x(c, cx + cell / 2, cy))
                    colr = extra_col if k_out > 0 else col
                    c.drawRect(rect, fill(colr, (0.85 * k_in) * (1 - k_out) * a))


# ---------------------------------------------------------------- icons (line art, 100x100 box)
def icon_polys(name):
    if name == "cap":
        return [np.array([(0, 38), (50, 18), (100, 38), (50, 58), (0, 38)]),
                np.vstack([[(24, 48)], arc(50, 62, 26, 180, 0)[::-1][::-1], [(76, 48)]]),
                np.array([(92, 42), (92, 70)]), arc(92, 74, 4, 0, 360, 16)]
    if name == "pad":
        body = np.vstack([arc(26, 58, 22, 90, 270), arc(74, 58, 22, -90, 90)])
        return [np.vstack([body, body[:1]]), np.array([(18, 58), (34, 58)]), np.array([(26, 50), (26, 66)]),
                arc(70, 54, 4, 0, 360, 14), arc(80, 62, 4, 0, 360, 14)]
    if name == "shop":
        aw = [(0, 34)] + [(x, 34 if i % 2 == 0 else 44) for i, x in enumerate(range(10, 101, 10))]
        return [np.array([(4, 34), (12, 12), (88, 12), (96, 34)]), np.array(aw),
                np.array([(8, 44), (8, 92), (92, 92), (92, 44)]), np.array([(40, 92), (40, 62), (60, 62), (60, 92)])]
    if name == "clock":
        return [arc(50, 52, 42, 0, 360, 64), np.array([(50, 52), (50, 24)]), np.array([(50, 52), (70, 62)])] + \
               [np.array([(50 + 36 * math.cos(a), 52 + 36 * math.sin(a)), (50 + 42 * math.cos(a), 52 + 42 * math.sin(a))])
                for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    if name == "bulb":
        return [np.vstack([arc(50, 40, 30, 140, 400, 60), [(38, 72), (38, 60)], arc(50, 40, 30, 140, 140, 2)[:1]]),
                np.array([(38, 72), (62, 72)]), np.array([(40, 80), (60, 80)]), np.array([(44, 88), (56, 88)]),
                np.array([(44, 58), (50, 44), (56, 58)])]
    if name == "tag":
        return [np.array([(10, 50), (42, 12), (90, 12), (90, 88), (42, 88), (10, 50)]), arc(70, 32, 6, 0, 360, 16)]
    if name == "chart":
        return [np.array([(8, 8), (8, 92), (96, 92)]), np.array([(18, 76), (38, 58), (54, 66), (86, 26)]),
                np.array([(70, 26), (86, 26), (86, 42)])]
    if name == "coins":
        return [arc(50, 26, 34, 0, 360, 40) * [1, 0.35] + [0, 17], np.array([(16, 26), (16, 44)]), np.array([(84, 26), (84, 44)]),
                arc(50, 44, 34, 0, 180, 30) * [1, 0.35] + [0, 28.6], np.array([(16, 44), (16, 62)]), np.array([(84, 44), (84, 62)]),
                arc(50, 62, 34, 0, 180, 30) * [1, 0.35] + [0, 40.3], np.array([(16, 62), (16, 80)]), np.array([(84, 62), (84, 80)]),
                arc(50, 80, 34, 0, 180, 30) * [1, 0.35] + [0, 52]]
    return []


def draw_icon(c, name, x, y, s, t, t0, col, dur=0.9, w=2.2):
    polys = icon_polys(name)
    for i, p in enumerate(polys):
        k = seg(t, t0 + i * dur * 0.12, t0 + i * dur * 0.12 + dur * 0.6)
        if k > 0:
            draw_poly(c, np.asarray(p, float) * s / 100 + [x, y], stroke(col, w), ease(k))
            ev(t0 + i * dur * 0.12 + dur * 0.6, "tick", t, scr_x(c, x + s / 2, y))


# ---------------------------------------------------------------- the Tron formation (3D line work)
def core_edges():
    """An intricate 'model core': an outer cube, an inner cube and the struts between them."""
    V = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
    E = [(i, j) for i in range(8) for j in range(i + 1, 8) if np.sum(np.abs(V[i] - V[j])) == 2]
    edges = [(V[i], V[j]) for i, j in E]
    edges += [(V[i] * 0.45, V[j] * 0.45) for i, j in E]
    edges += [(V[i] * 0.45, V[i]) for i in range(8)]
    ring = [(np.array([math.cos(a), 0, math.sin(a)]) * 1.55, np.array([math.cos(b), 0, math.sin(b)]) * 1.55)
            for a, b in zip(np.linspace(0, 2 * math.pi, 24, endpoint=False), np.linspace(0, 2 * math.pi, 24, endpoint=False) + 2 * math.pi / 24)]
    return edges + ring


CORE = core_edges()


def project(p, cx, cy, s, ry, rx=0.42):
    cr, sr, cxr, sxr = math.cos(ry), math.sin(ry), math.cos(rx), math.sin(rx)
    x, y, z = p
    x, z = x * cr + z * sr, -x * sr + z * cr
    y, z = y * cxr - z * sxr, y * sxr + z * cxr
    f = 6.0 / (6.0 + z)
    return np.array([cx + x * s * f, cy + y * s * f])


def core_segments(cx, cy, s, ry):
    return np.array([[project(a, cx, cy, s, ry), project(b, cx, cy, s, ry)] for a, b in CORE])


def draw_formation(c, segs, t, t0, dur, col=TURQ_GLOW, seed=0, glow=True):
    """Edges light up in order of distance from a seed point, each drawing from its near end."""
    seed_pt = segs[:, 0, :].mean(axis=0) + [0, 200]
    order = np.argsort(np.linalg.norm(segs.mean(axis=1) - seed_pt, axis=1))
    n = len(segs)
    for rank, i in enumerate(order):
        ts = t0 + dur * 0.8 * rank / n
        k = ease(seg(t, ts, ts + dur * 0.25), "o")
        if k <= 0:
            continue
        a, b = segs[i]
        if np.linalg.norm(a - seed_pt) > np.linalg.norm(b - seed_pt):
            a, b = b, a
        tip = a + (b - a) * k
        if glow:
            c.drawLine(*a, *tip, stroke(col, 5, 0.25, glow=6))
        c.drawLine(*a, *tip, stroke(col, 1.6, 0.95))
        if k < 1:
            c.drawCircle(*tip, 3.2, fill("#FFFFFF", 0.9))
        ev(ts, "form", t, scr_x(c, *segs[i].mean(axis=0)))


def draw_segments(c, segs, col, w=1.6, a=1.0, glow=True):
    for s0, s1 in segs:
        if glow:
            c.drawLine(*s0, *s1, stroke(col, 5, 0.22 * a, glow=6))
        c.drawLine(*s0, *s1, stroke(col, w, a))


def bar_segments(x, base, h, wdt, n):
    """A bar in technical-drawing style: outline plus hatch lines, as n segments."""
    segs = [((x, base), (x, base - h)), ((x, base - h), (x + wdt, base - h)), ((x + wdt, base - h), (x + wdt, base)), ((x + wdt, base), (x, base))]
    k = n - 4
    for i in range(k):
        yy = base - h * (i + 1) / (k + 1)
        segs.append(((x + 8, yy), (x + wdt - 8, yy)))
    return np.array(segs, float)


def polys_to_segments(polys, n):
    """Turn polylines into exactly n segments (evenly by length) so any shape can morph into any other."""
    lens = np.array([poly_len(p)[-1] for p in polys])
    counts = np.maximum(1, np.round(lens / lens.sum() * n).astype(int))
    while counts.sum() > n:
        counts[np.argmax(counts)] -= 1
    while counts.sum() < n:
        counts[np.argmax(lens / counts)] += 1
    out = []
    for p, k in zip(polys, counts):
        q = resample(p, k + 1)
        out += [(q[i], q[i + 1]) for i in range(k)]
    return np.array(out, float)


def morph(a, b, k):
    return a + (b - a) * ease(k)


# ---------------------------------------------------------------- CDE board motifs
def brackets(c, x, y, w, h, t, t0, col, a=1.0, L=22):
    """HUD corner brackets that slide into place (board: the goat / crystal posters)."""
    ev(t0, "blip", t, scr_x(c, x + w / 2, y))
    k = ease(seg(t, t0, t0 + 0.5))
    if k <= 0:
        return
    p = stroke(col, 1.4, a * k)
    off = (1 - k) * 18
    for cx, cy, sx, sy in ((x - off, y - off, 1, 1), (x + w + off, y - off, -1, 1), (x - off, y + h + off, 1, -1), (x + w + off, y + h + off, -1, -1)):
        c.drawLine(cx, cy, cx + sx * L, cy, p)
        c.drawLine(cx, cy, cx, cy + sy * L, p)


def crosshair(c, x, y, r, col, a=1.0):
    p = stroke(col, 1.1, a)
    c.drawLine(x - r, y, x + r, y, p)
    c.drawLine(x, y - r, x, y + r, p)


def callout(c, ax, ay, lx, ly, lines, t, t0, col, lab_col, fnt, a=1.0):
    """Anchor dot + elbow leader + decoding label (scientific annotation)."""
    ev(t0, "blip", t, scr_x(c, lx, ly))
    k = ease(seg(t, t0, t0 + 0.6))
    if k <= 0:
        return
    c.drawCircle(ax, ay, 3.5, fill(col, a * k))
    c.drawCircle(ax, ay, 8 * k, stroke(col, 1, 0.6 * a))
    ex = lx - 14 if lx > ax else lx + 14
    draw_poly(c, [(ax, ay), (ex, ly), (lx, ly)], stroke(col, 1, 0.8 * a), k)
    for i, ln in enumerate(lines):
        decode(c, ln, lx + (8 if lx > ax else -8), ly + 6 + i * 22, fnt, lab_col, t, t0 + 0.35 + i * 0.12, 0.45,
               seed=int(ax + i), align="left" if lx > ax else "right", a=a)


VP = (960, 300)


def ground_grid(c, t, t0, a=1.0):
    """A perspective grid with glowing nodes that draws out from the centre (board: The Planck Pixel)."""
    ev(t0, "scan", t)
    k = ease(seg(t, t0, t0 + 1.4))
    if k <= 0:
        return
    top, bot = 620, 1010
    for i in range(-9, 10):                      # rays to the vanishing point
        xb = 960 + i * 150
        kk = ease(seg(t, t0 + abs(i) * 0.05, t0 + abs(i) * 0.05 + 0.6))
        if kk <= 0:
            continue
        xt = VP[0] + (xb - VP[0]) * (top - VP[1]) / (bot - VP[1])
        c.drawLine(xt, top, lerp(xt, xb, kk), lerp(top, bot, kk), stroke(ON_DARK, 1, 0.13 * a))
    for j in range(9):                            # rungs, closer together towards the horizon
        y = top + (bot - top) * (j / 8) ** 1.8
        kk = ease(seg(t, t0 + 0.3 + j * 0.06, t0 + 0.9 + j * 0.06))
        if kk <= 0:
            continue
        half = (y - VP[1]) / (bot - VP[1]) * 1350 * kk
        c.drawLine(960 - half, y, 960 + half, y, stroke(ON_DARK, 1, 0.13 * a))
    rng = random.Random(3)
    for n in range(26):                           # glowing nodes on intersections
        i, j = rng.randint(-8, 8), rng.randint(1, 8)
        y = top + (bot - top) * (j / 8) ** 1.8
        xb = 960 + i * 150
        x = VP[0] + (xb - VP[0]) * (y - VP[1]) / (bot - VP[1])
        tw = 0.5 + 0.5 * math.sin(t * 2.2 + n * 1.7)
        kk = seg(t, t0 + 0.8 + n * 0.03, t0 + 1.0 + n * 0.03)
        if kk > 0:
            c.drawCircle(x, y, 5, fill(TURQ_GLOW, 0.18 * kk * tw * a))
            c.drawRect(skia.Rect.MakeXYWH(x - 2, y - 2, 4, 4), fill("#FFFFFF", 0.75 * kk * a))


# the ridgeline data landscape (board: the white line mountains, point-cloud terrain)
TER_X0, TER_X1, TER_N, TER_P = 300, 1620, 40, 180
PEAKS = ((780, 52.3), (1150, 66.4))
TER_SCALE, TER_BACK, TER_FRONT, TER_ROW = 5.0, 350, 850, 0.74
_TER = {}


def terrain_lines():
    if "lines" in _TER:
        return _TER["lines"]
    xs = np.linspace(TER_X0, TER_X1, TER_P)
    rng = np.random.default_rng(12)
    kern = np.exp(-np.linspace(-2, 2, 17) ** 2)
    kern /= kern.sum()
    lines = []
    for i in range(TER_N):
        d = i / (TER_N - 1)
        base = lerp(TER_BACK, TER_FRONT, d)
        noise = np.convolve(rng.normal(0, 1, TER_P), kern, mode="same")
        h = noise * 10 * lerp(0.4, 1.0, d) + 5 * np.sin(xs / 85 + i * 0.5) * lerp(0.4, 1, d)
        for px, score in PEAKS:
            ridge = math.exp(-((d - TER_ROW) / 0.2) ** 2)
            w = lerp(70, 140, d)
            h += score * TER_SCALE * ridge * np.exp(-((xs - px) / w) ** 2)
        h *= np.clip(1 - ((xs - (TER_X0 + TER_X1) / 2) / ((TER_X1 - TER_X0) / 2)) ** 8, 0, 1)   # quiet edges
        lines.append(np.column_stack([xs, base - h]))
    _TER["lines"] = lines
    i_pk = int(round(TER_ROW * (TER_N - 1)))
    apex = []
    for px, score in PEAKS:
        L = lines[i_pk]
        j = int(np.argmin(np.abs(L[:, 0] - px)))
        apex.append((L[j, 0], L[j, 1]))
    _TER["apex"] = apex
    return lines


def draw_terrain(c, t, t0, ground_col=DARK, a=1.0):
    lines = terrain_lines()
    bg = fill("#%02x%02x%02x" % ground_col)
    for i, L in enumerate(lines):
        d = i / (TER_N - 1)
        ts = t0 + (1 - d) * 0.9
        k = ease(seg(t, ts, ts + 0.9))
        if k <= 0:
            continue
        n = max(2, int(len(L) * k))
        pts = L[:n]
        path = skia.Path()
        path.moveTo(*pts[0])
        for p in pts[1:]:
            path.lineTo(*p)
        occl = skia.Path(path)
        occl.lineTo(pts[-1][0], H + 10)
        occl.lineTo(pts[0][0], H + 10)
        occl.close()
        c.drawPath(occl, bg)
        near_peak = abs(d - TER_ROW) < 0.013
        col, alpha, wdt = (TURQ_GLOW, 0.95, 1.8) if near_peak else (ON_DARK, lerp(0.22, 0.85, d), 1.1)
        if near_peak:
            c.drawPath(path, stroke(col, 5, 0.25 * a * k, glow=5))
        c.drawPath(path, stroke(col, wdt, alpha * a))
    ev(t0, "scan", t)


def pin(c, x, y, label, sub, t, t0, col, a=1.0, h=90):
    """A marker on the landscape with a label plate (board: 'have a nice day' terrain)."""
    ev(t0, "blip", t, scr_x(c, x, y))
    k = ease(seg(t, t0, t0 + 0.5))
    if k <= 0:
        return
    c.drawCircle(x, y, 6, stroke(col, 1.5, a * k))
    c.drawCircle(x, y, 2.5, fill(col, a * k))
    c.drawLine(x, y - 8, x, y - 8 - h * k, stroke(col, 1.2, 0.8 * a))
    if k > 0.7:
        kk = seg(k, 0.7, 1.0)
        fnt = font(DISPLAY, 38)
        w = text_w(label, fnt) + 40
        r = skia.Rect.MakeXYWH(x - w / 2, y - 8 - h - 74, w, 66)
        c.drawRRect(skia.RRect.MakeRectXY(r, 10, 10), fill("#0E1013", 0.85 * a * kk))
        c.drawRRect(skia.RRect.MakeRectXY(r, 10, 10), stroke(col, 1.2, a * kk))
        c.drawString(label, x - w / 2 + 20, y - 8 - h - 28, fnt, fill(ON_DARK, a * kk))
        c.drawString(sub, x - w / 2, y - 8 - h - 86, font(MONO, 16), fill(ON_DARK_SOFT, a * kk))


def particle_ring(c, t, t0, cx, cy, n=700, dur=1.6):
    """A turquoise particle ring bursting outward (board: 'Cosmos .09')."""
    ev(t0, "burst", t)
    k = seg(t, t0, t0 + dur)
    if k <= 0 or k >= 1:
        return
    rng = np.random.default_rng(9)
    th = rng.uniform(0, 2 * np.pi, n)
    spd = rng.uniform(0.55, 1.0, n)
    sz = rng.uniform(1.0, 3.2, n)
    e = ease(k, "o")
    r = 60 + 1150 * e * spd
    ang = th + 0.55 * e * (1.2 - spd)
    xs, ys = cx + r * np.cos(ang), cy + r * np.sin(ang) * 0.9
    for i in range(n):
        colr = TURQ_GLOW if i % 3 else "#FFFFFF"
        c.drawCircle(float(xs[i]), float(ys[i]), float(sz[i]), fill(colr, (1 - k) * 0.9))


_HT = {}


def halftone(name, size=110, step=5.2):
    """Dot-matrix version of a line icon (board: the engraved tiger, the dot-screen cat)."""
    if name in _HT:
        return _HT[name]
    S = 400
    surf = skia.Surface(S, S)
    cc = surf.getCanvas()
    cc.clear(skia.ColorBLACK)
    for p in icon_polys(name):
        pts = np.asarray(p, float) * S / 100
        path = skia.Path()
        path.moveTo(*pts[0])
        for q in pts[1:]:
            path.lineTo(*q)
        if np.linalg.norm(pts[0] - pts[-1]) < 1:
            cc.drawPath(path, fill("#FFFFFF", 0.35))
        cc.drawPath(path, stroke("#FFFFFF", 22))
    m = surf.makeImageSnapshot().toarray()[:, :, 1].astype(np.float32) / 255
    kern = np.ones(9) / 9
    m = np.apply_along_axis(lambda r: np.convolve(r, kern, "same"), 1, m)
    m = np.apply_along_axis(lambda r: np.convolve(r, kern, "same"), 0, m)
    dots = []
    st = step * S / size
    for yy in np.arange(st / 2, S, st):
        for xx in np.arange(st / 2, S, st):
            v = m[int(yy), int(xx)]
            if v > 0.06:
                dots.append((xx * size / S, yy * size / S, min(1.0, v) * step * 0.52))
    _HT[name] = np.array(dots)
    return _HT[name]


def draw_halftone(c, name, x, y, size, t, t0, col, dur=1.0, a=1.0):
    dots = halftone(name, size)
    if t < t0:
        return
    for dx, dy, r in dots:
        ts = t0 + dur * (dx + dy) / (2 * size)
        k = ease(seg(t, ts, ts + 0.18), "back")
        if k > 0:
            c.drawCircle(x + dx, y + dy, r * k, fill(col, a))
    ev(t0, "dots", t, scr_x(c, x + size / 2, y))


def iso_affine(cx, cy, s, z):
    """Card coords (card centred) -> isometric plane at height z."""
    a, b, d, e = 0.866 * s, -0.866 * s, 0.5 * s, 0.5 * s
    return (a, b, cx - a * CARD_W / 2 - b * CARD_H / 2, d, e, cy - z - d * CARD_W / 2 - e * CARD_H / 2)


def lerp_affine(A, B, k):
    return tuple(lerp(p, q, k) for p, q in zip(A, B))


def as_matrix(A):
    return skia.Matrix.MakeAll(A[0], A[1], A[2], A[3], A[4], A[5], 0, 0, 1)


def ring_tunnel(c, cx, cy, z, a=1.0):
    """Concentric rings the push travels through (board: the blue/orange op-art circles)."""
    for k in range(1, 70):
        r = k * 9 * z ** 0.85
        if r > 2400:
            break
        colr = TURQ if k % 2 else "#5E6772"
        c.drawCircle(cx, cy, r, stroke(colr, max(1.0, 0.6 * z ** 0.5), a * 0.55))


# ---------------------------------------------------------------- scenes
N_MORPH = 132
BAR_L = (700, 830, 52.3 * 7, 130)
BAR_R = (1090, 830, 66.4 * 7, 130)


def scene_dark_base(c, t, ground):
    c.drawImage(ground["dark"], 0, 0)


def sc1(c, t):
    """Two cores form over a glowing grid, ninety minutes apart (board: The Planck Pixel, HUD posters)."""
    ground_grid(c, t, 0.15)
    decode(c, "22 · 09 · 2026", 120, 150, font(MONO_M, 26), ON_DARK, t, 0.5, 0.8, seed=1)
    decode(c, "TWO RELEASES · ONE EVENING", 120, 188, font(MONO, 20), ON_DARK_SOFT, t, 0.9, 0.7, seed=2)
    for i, (cx, t0, lab) in enumerate(((680, 1.7, "MODEL A"), (1240, 2.5, "MODEL B"))):
        ry = 0.5 + 0.12 * t + i * 0.7
        segs = core_segments(cx, 470, 120, ry)
        for r_i, rr in enumerate((190, 214)):
            k = ease(seg(t, t0 - 0.4 + r_i * 0.15, t0 + 0.5 + r_i * 0.15))
            if k > 0:
                draw_poly(c, arc(cx, 470, rr, -90, -90 + 360 * k, 90), stroke(TURQ_GLOW, 1, 0.35))
        draw_formation(c, segs, t, t0, 1.6, seed=i)
        kp = ease(seg(t, t0 + 1.1, t0 + 1.7))
        if kp > 0:                                  # projection lines down to the grid
            for vx in (-1, 1):
                for vz in (-1, 1):
                    x, y = project((vx, 1, vz), cx, 470, 120, ry)
                    y2 = lerp(y, 690 + vz * 18, kp)
                    c.drawLine(x, y, x, y2, stroke(TURQ_GLOW, 1, 0.3))
                    c.drawCircle(x, y2, 2.2, fill(TURQ_GLOW, 0.8 * kp))
        brackets(c, cx - 222, 470 - 222, 444, 444, t, t0 + 1.4, ON_DARK_SOFT, 0.7)
        if i == 0:
            callout(c, cx - 150, 400, 330, 330, ["CORE / A", "RELEASED  T+0"], t, t0 + 1.6, TURQ_GLOW, ON_DARK, font(MONO, 18))
        else:
            callout(c, cx + 150, 400, 1590, 330, ["CORE / B", "RELEASED  T+90 MIN"], t, t0 + 1.6, TURQ_GLOW, ON_DARK, font(MONO, 18))
        decode(c, lab, cx, 780, font(MONO_M, 22), ON_DARK, t, t0 + 1.2, 0.5, seed=5 + i, align="center")
        if t >= t0 + 1.7:
            ev(t0 + 1.7, "chime", t, cx)
    k = ease(seg(t, 4.5, 5.3))
    if k > 0:
        y = 870
        c.drawLine(680, y, lerp(680, 1240, k), y, stroke(ON_DARK_SOFT, 1.5))
        for xx in (680, 1240):
            c.drawLine(xx, y - 12, xx, y + 12, stroke(ON_DARK_SOFT, 1.5, k))
        decode(c, "T+0", 680, y + 44, font(MONO, 20), ON_DARK_SOFT, t, 4.6, 0.3, seed=9, align="center")
        decode(c, "T+90 MIN", 1240, y + 44, font(MONO, 20), TURQ_GLOW, t, 5.0, 0.5, seed=10, align="center")
        decode(c, "90 MINUTES APART", 960, y - 22, font(MONO_M, 22), ON_DARK, t, 5.0, 0.7, seed=11, align="center")


def core_final(i, t):
    cx = (680, 1240)[i]
    return core_segments(cx, 470, 120, 0.5 + 0.12 * t + i * 0.7)


def bars(i):
    x, base, h, wd = (BAR_L, BAR_R)[i]
    return bar_segments(x, base, h, wd, N_MORPH // 2)


def sc2(c, t):
    """The cores flow into a ridgeline landscape; two pinned peaks, 52.3 and 66.4 (board: line mountains, terrain pins)."""
    ground_grid(c, t, -10, a=lerp(1, 0.0, ease(seg(t, 6.2, 7.0))))
    km = seg(t, 6.2, 7.3)
    src = np.vstack([np.vstack([core_final(i, 6.2)] * 3)[:N_MORPH // 2] for i in range(2)])
    lines = terrain_lines()
    tgt = polys_to_segments([lines[i] for i in range(0, TER_N, 4)], N_MORPH)
    if km < 1:
        draw_segments(c, morph(src, tgt, km), TURQ_GLOW, 1.4, 1.0 - 0.6 * km)
    ev(6.2, "morph", t)
    draw_terrain(c, t, 6.9)
    (ax, ay), (bx, by) = _TER["apex"]
    k = ease(seg(t, 7.6, 8.2))
    if k > 0:
        for (x, y) in ((ax, ay), (bx, by)):
            c.drawLine(x + 10, y, lerp(x + 10, 1360, k), y, stroke("#2BD48F", 1, 0.45))
    dimension(c, 1360, by, ay, "#2BD48F", t, 7.7, 0.7, "+14.1 POINTS", font(MONO_M, 24), "#2BD48F")
    if t >= 8.3:
        ev(8.3, "chime", t, 1360)
    pin(c, ax, ay, "52.3", "PREVIOUS MODEL", t, 7.2, ON_DARK_SOFT)
    pin(c, bx, by, "66.4", "NEW MODEL", t, 7.4, TURQ_GLOW)
    decode(c, "CODING TEST · SHARE OF TASKS PASSED", 960, 960, font(MONO_M, 20), ON_DARK, t, 8.7, 0.8, seed=21, align="center")


def fourteen_polys():
    fnt = font(DISPLAY, 300)
    w = text_w("+14", fnt)
    return glyph_polys("+14", fnt, W / 2 - w / 2, 640), text_path("+14", fnt, W / 2 - w / 2, 640)


F14_POLYS, F14_PATH = None, None


def spectral_line(c, y, a):
    sh = skia.GradientShader.MakeLinear(points=[(0, 0), (W, 0)],
                                        colors=[hexc("#FF3D7F", 0), hexc("#FF3D7F", a), hexc("#FFD23F", a), hexc("#3FE6D8", a),
                                                hexc("#7B61FF", a), hexc("#7B61FF", 0)])
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6)
    p.setShader(sh)
    c.drawLine(0, y, W, y, p)


def chrome_14(c, t, scale=1.0, cx=W / 2, cy=530, a=1.0, sweep_t=None, spectral=False):
    c.save()
    c.translate(cx, cy)
    c.scale(scale, scale)
    c.translate(-W / 2, -530)
    b = F14_PATH.getBounds()
    if spectral:                                   # a thin prismatic fringe (board: the crystal and glass pins)
        for dx, colr in ((-3.5, "#FF4F8B"), (3.5, "#3FE6D8")):
            p = fill(colr, 0.5 * a)
            p.setBlendMode(skia.BlendMode.kScreen)
            c.save()
            c.translate(dx, 0)
            c.drawPath(F14_PATH, p)
            c.restore()
    c.drawPath(F14_PATH, chrome_paint(b.top(), b.bottom(), a))
    c.drawPath(F14_PATH, stroke("#B8C0CA", 1.2, 0.5 * a))    # a rim, so the dark horizon never melts into the ground
    if sweep_t is not None and 0 < sweep_t < 1:        # a slow specular glint across the chrome
        c.save()
        c.clipPath(F14_PATH, skia.ClipOp.kIntersect, True)
        x = lerp(b.left() - 200, b.right() + 200, sweep_t)
        sh = skia.GradientShader.MakeLinear(points=[(x - 90, 0), (x + 90, 0)],
                                            colors=[hexc("#FFFFFF", 0), hexc("#FFFFFF", 0.85 * a), hexc("#FFFFFF", 0)])
        p = skia.Paint(AntiAlias=True)
        p.setShader(sh)
        c.drawRect(b, p)
        c.restore()
    c.restore()


def sc3(c, t, ground):
    """The landscape flows into '+14'; chrome fills with a spectral glint; 'It isn't' bursts a particle ring."""
    global F14_POLYS, F14_PATH
    lines = terrain_lines()
    kf = seg(t, 11.5, 12.0)
    if kf < 1:
        draw_terrain(c, t, -10, a=1 - kf)
    target = polys_to_segments(F14_POLYS, N_MORPH)
    src = polys_to_segments([lines[i] for i in range(0, TER_N, 4)], N_MORPH)
    km = seg(t, 11.5, 12.6)
    segs = morph(src, target, km)
    ev(11.5, "morph", t)
    k_fill = ease(seg(t, 12.6, 13.4))
    shrink = lerp(1.0, 0.82, ease(seg(t, 13.1, 13.8)))
    grow = lerp(0, 0.30, ease(seg(t, 14.3, 14.9), "back"))
    s = shrink + grow
    kw = ease(seg(t, 14.3, 15.2))
    if kw > 0:
        c.save()
        clip = skia.Path()
        clip.addCircle(W / 2, 530, 1300 * kw)
        c.clipPath(clip, skia.ClipOp.kIntersect, True)
        c.drawImage(ground["slate"], 0, 0)
        c.restore()
        c.drawCircle(W / 2, 530, 1300 * kw, stroke(TURQ, 2.5, 1 - kw))
        ev(14.3, "thum", t)
    if k_fill < 1:
        c.save()
        c.translate(W / 2, 530)
        c.scale(s, s)
        c.translate(-W / 2, -530)
        draw_segments(c, segs, TURQ_GLOW, 1.8, 1.0 - k_fill * 0.9)
        c.restore()
    if k_fill > 0:
        c.save()
        b = F14_PATH.getBounds()
        clip = skia.Rect.MakeLTRB(0, lerp(b.bottom(), b.top(), k_fill), W, H)
        c.translate(W / 2, 530)
        c.scale(s, s)
        c.translate(-W / 2, -530)
        c.clipRect(clip)
        c.translate(W / 2, 530)
        c.scale(1 / s, 1 / s)
        c.translate(-W / 2, -530)
        chrome_14(c, t, s, sweep_t=seg(t, 13.0, 14.2), spectral=t < 14.3)
        c.restore()
        ev(12.6, "shimmer", t)
    kg = seg(t, 12.8, 13.5)
    ev(12.8, "glint", t)
    if 0 < kg < 1:                                 # spectral glint lines sweep up through the reveal
        for j in range(3):
            y = lerp(700, 360, ease(kg)) + j * 22
            spectral_line(c, y, 0.45 * math.sin(math.pi * kg) * (1 - j * 0.25))
        ev(12.8, "glint", t)
    particle_ring(c, t, 14.3, W / 2, 530)


CARDS = [
    dict(tag="IF YOU'RE AT UNI", icon="cap", metric=("2:2", "2:1"), sub="DEGREE CLASS", cap="The line most graduate jobs draw.",
         t0=15.3, t_a=17.9, t_b=18.6, t_cap=19.7, grid=(52, 14), mode="fill"),
    dict(tag="IF YOU GAME", icon="pad", metric=("1 IN 2", "2 IN 3"), sub="WIN RATE", cap="A coin flip becomes two wins in three.",
         t0=22.4, t_a=23.7, t_b=26.0, t_cap=26.3, grid=(52, 14), mode="fill"),
    dict(tag="IF YOU RUN A BUSINESS", icon="shop", metric=("48", "34"), sub="MISTAKES PER 100 JOBS", cap="Almost a third fewer things to fix.",
         t0=28.2, t_a=29.6, t_b=30.3, t_cap=30.8, grid=(48, 14), mode="remove"),
    dict(tag="IF YOUR TIME IS MONEY", icon="clock", metric=("", "+7 HRS"), sub="14 FEWER DO-OVERS × 30 MIN", cap="A full working day, back.",
         t0=32.6, t_a=34.4, t_b=39.8, t_cap=40.2, grid=(52, 14), mode="fill"),
]
CARD_W, CARD_H = 820, 380
SHELF_S, SHELF_Y = 0.34, 846
SHELF_X0 = (W - (4 * CARD_W * SHELF_S + 3 * 34)) / 2


def card_rect(i, t):
    """Each card forms large in the centre, then docks onto a shelf when the next one arrives."""
    t_dock = CARDS[i + 1]["t0"] if i + 1 < len(CARDS) else 41.7
    big_s = 1.32
    bx, by = W / 2 - CARD_W * big_s / 2, 430 - CARD_H * big_s / 2
    sx, sy = SHELF_X0 + i * (CARD_W * SHELF_S + 34), SHELF_Y
    k = ease(seg(t, t_dock, t_dock + 0.8))
    if k > 0:
        ev(t_dock + 0.8, "thock", t, sx + CARD_W * SHELF_S / 2)
    return lerp(bx, sx, k), lerp(by, sy, k), lerp(big_s, SHELF_S, k)


def arrow(c, x, y, w, col, a=1.0, k=1.0):
    p = stroke(col, 3, a)
    x1 = x + w * k
    c.drawLine(x, y, x1, y, p)
    if k > 0.6:
        c.drawLine(x1 - 12, y - 10, x1, y, p)
        c.drawLine(x1 - 12, y + 10, x1, y, p)


GRID_X, GRID_Y, GRID_S = CARD_W - 270, 70, 230


def card_body(c, i, t, a, active, grid=True, shadow=True):
    """A perspective card in its own coordinates (0..CARD_W, 0..CARD_H)."""
    cd = CARDS[i]
    glass(c, 0, 0, CARD_W, CARD_H, 24, a, shadow)
    k_edge = ease(seg(t, cd["t0"], cd["t0"] + 0.8))
    if active:                                   # the live card carries a faint turquoise halo
        draw_poly(c, rrect_pts(0, 0, CARD_W, CARD_H, 24), stroke(TURQ, 4, 0.2 * a, glow=6), k_edge)
    draw_poly(c, rrect_pts(0, 0, CARD_W, CARD_H, 24), stroke(TURQ if active else LINE_DIM, 1.5, a), k_edge)
    decode(c, cd["tag"], 40, 58, font(MONO_M, 20), TURQ_GLOW, t, cd["t0"] + 0.2, 0.6, seed=30 + i, a=a)
    draw_halftone(c, cd["icon"], 40, 92, 108, t, cd["t0"] + 0.3, ON_DARK_MID, 1.0, a)
    mx, my = 176, 170
    m0, m1 = cd["metric"]
    u = (text_w(m0, font(DISPLAY, 44)) + text_w(m1, font(DISPLAY, 44))) / 44       # width per point of type
    f_big = font(DISPLAY, min(44.0, (GRID_X - 36 - mx - (102 if m0 else 0)) / u))    # always fits before the grid
    if cd["metric"][0] and t >= cd["t_a"]:
        c.drawString(cd["metric"][0], mx, my, f_big, fill(ON_DARK_SOFT, a * ease(seg(t, cd["t_a"], cd["t_a"] + 0.3))))
    if t >= cd["t_b"]:
        k = ease(seg(t, cd["t_b"], cd["t_b"] + 0.45))
        x2 = mx
        if cd["metric"][0]:
            w0 = text_w(cd["metric"][0], f_big) + 24
            arrow(c, mx + w0, my - f_big.getSize() * 0.36, 54, TURQ, a, k)
            x2 = mx + w0 + 78
        c.drawString(cd["metric"][1], x2, my + (1 - k) * 12, f_big, fill(ON_DARK, a * k))
        ev(cd["t_b"], "chime_soft", t, scr_x(c, x2, my))
    decode(c, cd["sub"], mx, my + 40, font(MONO, 17), ON_DARK_SOFT, t, cd["t_a"] - 0.2, 0.5, seed=40 + i, a=a)
    type_on(c, cd["cap"], 40, 318, font(BODY, 28), ON_DARK, t, cd["t_cap"], 42, a)
    if grid:
        n_base, n_extra = cd["grid"]
        grid100(c, GRID_X, GRID_Y, GRID_S, t, n_base, n_extra, cd["t0"] + 0.6, cd["t_b"] + 0.1, remove=(cd["mode"] == "remove"), a=a)


def draw_card(c, i, t, alpha=1.0, grid=True):
    cd = CARDS[i]
    if t < cd["t0"]:
        return
    x, y, s = card_rect(i, t)
    k_in = ease(seg(t, cd["t0"], cd["t0"] + 0.5))
    active = t < (CARDS[i + 1]["t0"] if i + 1 < 4 else 41.7)
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    card_body(c, i, t, alpha * k_in, active, grid)
    c.restore()


def sc4(c, t):
    for i in range(4):
        draw_card(c, i, t)


STACK_C, STACK_S, STACK_DZ = (960, 760), 0.6, 128
LAYER_LAB = ["UNI  ·  2:2 → 2:1", "GAME  ·  1 IN 2 → 2 IN 3", "BUSINESS  ·  48 → 34 MISTAKES", "TIME  ·  +7 HOURS"]


def sc5(c, t):
    """Same number: the four cards tilt into an exploded isometric stack, one turquoise line pierces
    them all, the stack collapses into one grid, the grid dissolves to ASCII, the ASCII becomes chrome
    (board: the exploded map layers, ASCII motion)."""
    k_col = ease(seg(t, 43.1, 43.6))
    pierce_pts = []
    if k_col < 1:
        for i in (3, 2, 1, 0):                          # bottom layer first
            k = ease(seg(t, 41.9 + (3 - i) * 0.08, 42.7 + (3 - i) * 0.08))
            x, y, s0 = card_rect(i, t)
            ev(41.9 + (3 - i) * 0.08, "lift", t, x + CARD_W * s0 / 2)
            A_shelf = (s0, 0, x, 0, s0, y)
            z = (3 - i) * STACK_DZ * (1 - k_col)
            A_iso = iso_affine(STACK_C[0], STACK_C[1], STACK_S, z)
            A = lerp_affine(A_shelf, A_iso, k)
            c.save()
            c.concat(as_matrix(A))
            card_body(c, i, 99, (1 - k_col), False, grid=True, shadow=k < 0.2)
            c.restore()
            gx, gy = GRID_X + GRID_S / 2, GRID_Y + GRID_S / 2
            pierce_pts.append((A[0] * gx + A[1] * gy + A[2], A[3] * gx + A[4] * gy + A[5], A, i))
            if k > 0.95:                                # layer labels on leader lines (the map-legend look)
                lx = A[0] * 0 + A[1] * CARD_H + A[2]
                ly = A[3] * 0 + A[4] * CARD_H + A[5]
                c.drawLine(lx, ly, lx - 60, ly, stroke(ON_DARK_SOFT, 1, 1 - k_col))
                decode(c, LAYER_LAB[i], lx - 70, ly + 6, font(MONO_M, 17), ON_DARK, t, 42.6 + (3 - i) * 0.08, 0.5, seed=60 + i,
                       align="right", a=1 - k_col)
    kp = ease(seg(t, 42.6, 43.1))
    if kp > 0 and pierce_pts and k_col < 1:
        xb, yb = pierce_pts[0][0], pierce_pts[0][1] + 70
        xt, yt = pierce_pts[-1][0], pierce_pts[-1][1] - 150
        y_tip = lerp(yb, yt, kp)
        c.drawLine(xb, yb, xt, y_tip, stroke(TURQ_GLOW, 7, 0.25 * (1 - k_col), glow=7))
        c.drawLine(xb, yb, xt, y_tip, stroke(TURQ, 2.2, 1 - k_col))
        for (px, py, A, i) in pierce_pts:
            if y_tip <= py:
                c.save()
                c.translate(px, py)
                c.scale(1.0, 0.5)
                c.drawCircle(0, 0, 26, stroke(TURQ, 1.6, 1 - k_col))
                c.restore()
                c.drawCircle(px, py, 3.5, fill(TURQ, 1 - k_col))
        if kp >= 1:
            decode(c, "+14  ·  SAME NUMBER", xt + 18, yt + 6, font(MONO_M, 20), TURQ, t, 43.0, 0.5, seed=70, a=1 - k_col)
        ev(42.6, "pierce", t)
    big = 440
    k_one = ease(seg(t, 43.3, 43.7))
    k_ascii = seg(t, 43.6, 44.4)
    if k_one > 0 and k_ascii < 1:
        grid100(c, W / 2 - big / 2, 150, big, 99, 52, 14, 0, 0, a=k_one * (1 - k_ascii))
        ev(43.3, "chime_soft", t)
    if k_ascii > 0:
        ascii_fourteen(c, t, k_ascii, seg(t, 44.4, 45.3))


ASCII_FIELD = None


def ascii_fourteen(c, t, k_in, k_out):
    """The grid's cells become characters and re-flow into '+14' drawn in ASCII, then chrome takes over."""
    global ASCII_FIELD
    fnt = font(MONO_M, 18)
    cw, ch = 11.0, 20.0
    if ASCII_FIELD is None:
        surf = skia.Surface(W, H)
        cc = surf.getCanvas()
        cc.clear(skia.ColorBLACK)
        cc.drawPath(F14_PATH, fill("#FFFFFF"))
        m = surf.makeImageSnapshot().toarray()[:, :, 0]
        cells = []
        for yy in np.arange(260, 760, ch):
            for xx in np.arange(420, 1500, cw):
                v = m[int(yy), int(xx)]
                if v > 128:
                    cells.append((xx, yy))
        rng = np.random.default_rng(4)
        big, cell = 440, 44
        filled = [(W / 2 - big / 2 + (i % 10 + 0.5) * cell, 150 + (i // 10 + 0.5) * cell) for i in range(66)]
        src = np.array([filled[j % 66] for j in rng.permutation(len(cells))]) + rng.normal(0, 6, (len(cells), 2))
        ASCII_FIELD = (np.array(cells), src)
    dst, src = ASCII_FIELD
    pos = src + (dst - src) * ease(k_in)
    rng = random.Random(int(t * 20))
    a = 1 - ease(k_out)
    for i, (x, y) in enumerate(pos):
        chr_ = "+14#*"[i % 5] if k_in >= 1 else rng.choice(ASCII)
        c.drawString(chr_, x, y, fnt, fill(TURQ_GLOW if i % 7 == 0 else ON_DARK_MID, a))
    if k_in > 0 and k_in < 0.05:
        ev(43.2, "decode", t)
    if k_out > 0:
        chrome_14(c, t, 1.0, a=ease(k_out), sweep_t=seg(t, 44.8, 45.8))
        ev(44.3, "shimmer", t)


TILES = [("01", "WHAT IT CAN\nDO FOR YOU", "bulb", 47.5), ("02", "WHAT IT\nCOSTS", "tag", 49.2), ("03", "HOW PEOPLE\nEARN WITH IT", "chart", 50.3)]


def sc6(c, t):
    """Three chapter tiles, then a slow push through the '0' of 02."""
    k_up = ease(seg(t, 45.6, 46.6))
    chrome_14(c, t, lerp(1.0, 0.38, k_up), W / 2, lerp(530, 150, k_up))
    kl = ease(seg(t, 46.2, 47.0))
    if kl > 0:
        c.drawLine(W / 2 - 700 * kl, 262, W / 2 + 700 * kl, 262, stroke(TURQ, 1.4))
        ev(46.2, "whoosh", t)
    for i, (num, title, icon, t0) in enumerate(TILES):
        if t < t0:
            continue
        x = 250 + i * 490
        y = 320
        k = ease(seg(t, t0, t0 + 0.6))
        c.save()
        c.translate(0, (1 - k) * 30)
        glass(c, x, y, 440, 560, 26, k)
        draw_poly(c, rrect_pts(x, y, 440, 560, 26), stroke(TURQ, 1.4, k), ease(seg(t, t0, t0 + 0.9)))
        c.drawString(num, x + 36, y + 110, font(DISPLAY, 64), fill(ON_DARK, k))
        for j, line in enumerate(title.split("\n")):
            type_on(c, line, x + 36, y + 420 + j * 44, font(BODY_M, 36), ON_DARK, t, t0 + 0.3 + j * 0.3, 34, k)
        draw_icon(c, icon, x + 250, y + 170, 140, t, t0 + 0.2, ON_DARK_MID, 1.0, 2.6)
        c.restore()
        ev(t0, "chime_soft", t, x + 220)


def zoom_through(t):
    """Scale about the counter of the '0' in tile 02 (the vortex people liked, kept gentle)."""
    k = ease(seg(t, 52.6, 53.8), "i")
    return 1 + k * 70, (740 + 36 + 26, 320 + 110 - 24)


def frame(c, t, ground):
    c.drawImage(ground["dark"] if t < 15.2 else ground["slate"], 0, 0)     # sc3 wipes graphite -> slate from 14.3
    z, (zx, zy) = zoom_through(t)
    c.save()
    if z > 1:
        c.translate(zx, zy)
        c.scale(z, z)
        c.translate(-zx, -zy)
        ev(52.6, "zoom", t)
    if t < 6.4:
        sc1(c, t)
    elif t < 11.5:
        sc2(c, t)
    elif t < 15.3:
        sc3(c, t, ground)
    elif t < 41.8:
        sc4(c, t)
    elif t < 45.6:
        sc5(c, t)
    else:
        sc6(c, t)
    c.restore()
    if z > 1.0:
        ring_tunnel(c, zx, zy, z, a=seg(t, 52.6, 52.9) * (1 - seg(t, 53.2, 53.5)))
    if t > 53.3:                                           # after the push: the ground and a mark
        k = seg(t, 53.3, 53.8)
        c.drawImage(ground["dark"], 0, 0, skia.SamplingOptions(), fill("#FFFFFF", k))
        decode(c, "A01", W / 2, H / 2 + 12, font(DISPLAY, 34), ON_DARK, t, 53.85, 0.4, seed=99, align="center")
        kl = ease(seg(t, 54.3, 55.0))
        if kl > 0:                                         # a turquoise signature line settles under the mark
            c.drawLine(W / 2 - 70 * kl, H / 2 + 44, W / 2 + 70 * kl, H / 2 + 44, stroke(TURQ, 1.4))
    # frame furniture: one thin line and a tiny label, always calm
    col = ON_DARK_SOFT
    c.drawString("A01  ·  FOURTEEN POINTS", 120, H - 60, font(MONO, 16), fill(col, 0.8))
    c.drawLine(120, H - 84, 300, H - 84, stroke(col, 1, 0.6))


def main():
    global F14_POLYS, F14_PATH
    os.makedirs(BUILD, exist_ok=True)
    F14_POLYS, F14_PATH = fourteen_polys()
    ground = {"slate": slate_ground(), "dark": marl(DARK, 2, 2.4)}
    surface = skia.Surface(W, H)
    c = surface.getCanvas()
    if "--still" in sys.argv:
        t = float(sys.argv[sys.argv.index("--still") + 1])
        c.clear(skia.ColorBLACK)
        frame(c, t, ground)
        surface.makeImageSnapshot().save(os.path.join(BUILD, f"still_{t:05.1f}.png"), skia.kPNG)
        return
    _EV_ON[0] = True
    out = os.path.join(BUILD, "mockup_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "15",
                           "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        t = i / FPS
        c.clear(skia.ColorBLACK)
        frame(c, t, ground)
        ff.stdin.write(surface.makeImageSnapshot().toarray().tobytes())
    ff.stdin.close()
    ff.wait()
    merged = {}
    for at, kind, pan in EVENTS + [(a, k, None) for a, k in CUES]:     # cues fill gaps; a placed event wins
        if merged.get((at, kind)) is None:
            merged[(at, kind)] = pan
    json.dump([[at, kind, pan] for (at, kind), pan in sorted(merged.items())], open(os.path.join(BUILD, "events.json"), "w"))
    print(out, len(EVENTS), "sound events")


if __name__ == "__main__":
    main()
