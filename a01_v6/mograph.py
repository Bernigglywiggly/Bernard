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
DUR = 54.0
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get("A01V6_FONTS", os.path.join(HERE, "fonts"))
BUILD = os.environ.get("A01V6_BUILD", os.path.join(HERE, "build"))

# ---------------------------------------------------------------- tokens
def hexc(h, a=1.0):
    h = h.lstrip("#")
    return skia.Color4f(int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


LIGHT, DARK = (231, 232, 234), (20, 22, 26)
INK, INK_SOFT = "#1C1F24", "#6B717C"
ON_DARK, ON_DARK_SOFT = "#E9EBEE", "#8A919C"
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


def ev(t_evt, kind, now, fps=FPS):
    """Register a sound event once, on the frame where it happens."""
    if _EV_ON[0] and t_evt <= now < t_evt + 1.0 / fps:     # the first frame at/after the event
        EVENTS.append((round(t_evt, 3), kind))


# scene-level sound cues (independent of what happens to be drawn on the exact frame)
CUES = [(0.2, "whoosh"), (3.4, "chime"), (4.2, "chime"), (6.2, "morph"), (8.0, "chime"), (11.5, "morph"), (12.6, "shimmer"),
        (14.3, "thum"), (23.2, "thock"), (29.0, "thock"), (33.4, "thock"), (42.5, "thock"), (41.9, "whoosh"), (42.7, "chime_soft"),
        (43.3, "decode"), (44.4, "shimmer"), (46.2, "whoosh"), (52.6, "zoom")] + [(6.9 + i / 12, "count") for i in range(11)]


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
        ev(ti + 0.12, "tick", t)
    s = "".join(shown)
    if align == "center":
        x -= text_w(text, fnt) / 2
    elif align == "right":
        x -= text_w(text, fnt)
    c.drawString(s, x, y, fnt, fill(col, a))


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


def grid100(c, x, y, size, t, n_base, n_extra, t_base, t_extra, col=INK, extra_col=TURQ, remove=False, a=1.0):
    """The 'per hundred' motif: a 10x10 grid whose cells fill in (or empty out)."""
    cell = size / 10
    gap = cell * 0.18
    for i in range(100):
        r, q = divmod(i, 10)
        cx, cy = x + q * cell, y + r * cell
        rect = skia.Rect.MakeXYWH(cx + gap / 2, cy + gap / 2, cell - gap, cell - gap)
        c.drawRect(rect, stroke(INK_SOFT if col == INK else ON_DARK_SOFT, 1, 0.35 * a))
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
                    ev(t_extra + j * 0.03, "pip", t)
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
                        ev(t_extra + j * 0.03, "pip", t)
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
            ev(t0 + i * dur * 0.12 + dur * 0.6, "tick", t)


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
        ev(ts, "form", t)


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


# ---------------------------------------------------------------- scenes
N_MORPH = 132
BAR_L = (700, 830, 52.3 * 7, 130)
BAR_R = (1090, 830, 66.4 * 7, 130)


def scene_dark_base(c, t, ground):
    c.drawImage(ground["dark"], 0, 0)


def sc1(c, t):
    """Two cores form, ninety minutes apart."""
    k_line = ease(seg(t, 0.2, 1.2))
    if k_line > 0:
        c.drawLine(W / 2 - 800 * k_line, 700, W / 2 + 800 * k_line, 700, stroke(TURQ_GLOW, 1.2, 0.55))
        ev(0.2, "whoosh", t)
    decode(c, "22 · 09 · 2026", 120, 150, font(MONO_M, 26), ON_DARK, t, 0.5, 0.8, seed=1)
    decode(c, "TWO RELEASES", 120, 188, font(MONO, 20), ON_DARK_SOFT, t, 0.9, 0.6, seed=2)
    for i, (cx, t0, lab) in enumerate(((680, 1.7, "MODEL A"), (1240, 2.5, "MODEL B"))):
        ry = 0.5 + 0.12 * t + i * 0.7
        segs = core_segments(cx, 470, 120, ry)
        for r_i, rr in enumerate((190, 214)):
            k = ease(seg(t, t0 - 0.4 + r_i * 0.15, t0 + 0.5 + r_i * 0.15))
            if k > 0:
                draw_poly(c, arc(cx, 470, rr, -90, -90 + 360 * k, 90), stroke(TURQ_GLOW, 1, 0.35))
        draw_formation(c, segs, t, t0, 1.6, seed=i)
        decode(c, lab, cx, 740 + 40, font(MONO_M, 22), ON_DARK, t, t0 + 1.2, 0.5, seed=5 + i, align="center")
        if t > t0 + 1.7:
            ev(t0 + 1.7, "chime", t)
    k = ease(seg(t, 4.5, 5.3))
    if k > 0:
        y = 860
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
    """The cores flow into two bars; 52.3 -> 66.4 on a coding test."""
    km = seg(t, 6.2, 7.2)
    for i in range(2):
        a = core_final(i, 6.2)
        a = np.vstack([a] * 3)[:N_MORPH // 2]
        b = bars(i)
        segs = morph(a, b, km)
        col = TURQ_GLOW if i == 1 else ON_DARK_SOFT
        draw_segments(c, segs, col, 1.6, 0.95 if i == 1 else 0.8, glow=(i == 1))
    ev(6.2, "morph", t)
    fnt = font(DISPLAY, 58)
    counter(c, 0, 52.3, 765, 830 - 52.3 * 7 - 30, fnt, ON_DARK_SOFT, t, 6.9, 0.8)
    counter(c, 0, 66.4, 1155, 830 - 66.4 * 7 - 30, fnt, ON_DARK, t, 7.0, 0.8)
    if 6.9 <= t < 7.8:
        ev(round(t * 12) / 12, "count", t)
    c.drawLine(640, 830, 1300, 830, stroke(ON_DARK_SOFT, 1.2, ease(seg(t, 6.4, 7.0))))
    for v in (0, 20, 40, 60):
        yy = 830 - v * 7
        a = ease(seg(t, 6.6 + v * 0.004, 7.2))
        c.drawLine(630, yy, 642, yy, stroke(ON_DARK_SOFT, 1, a))
        c.drawString(str(v), 590 - (10 if v >= 10 else 0), yy + 6, font(MONO, 16), fill(ON_DARK_SOFT, a))
    top_l, top_r = 830 - 52.3 * 7, 830 - 66.4 * 7
    k = ease(seg(t, 7.4, 8.1))
    if k > 0:
        c.drawLine(835, top_l, lerp(835, 1235, k), top_l, stroke(EMERALD, 1, 0.5))
    dimension(c, 1260, top_r, top_l, "#2BD48F", t, 7.5, 0.7, "+14.1 POINTS", font(MONO_M, 24), "#2BD48F")
    if t > 8.0:
        ev(8.0, "chime", t)
    decode(c, "CODING TEST", 960, 900, font(MONO_M, 22), ON_DARK, t, 8.7, 0.6, seed=21, align="center")
    decode(c, "PREVIOUS", 765, 870, font(MONO, 18), ON_DARK_SOFT, t, 10.1, 0.4, seed=22, align="center")
    decode(c, "NEW", 1155, 870, font(MONO, 18), TURQ_GLOW, t, 10.3, 0.3, seed=23, align="center")


def fourteen_polys():
    fnt = font(DISPLAY, 300)
    w = text_w("+14", fnt)
    return glyph_polys("+14", fnt, W / 2 - w / 2, 640), text_path("+14", fnt, W / 2 - w / 2, 640)


F14_POLYS, F14_PATH = None, None


def chrome_14(c, t, scale=1.0, cx=W / 2, cy=530, a=1.0, sweep_t=None):
    c.save()
    c.translate(cx, cy)
    c.scale(scale, scale)
    c.translate(-W / 2, -530)
    b = F14_PATH.getBounds()
    c.drawPath(F14_PATH, chrome_paint(b.top(), b.bottom(), a))
    c.drawPath(F14_PATH, stroke("#2A2F37", 1.5, 0.6 * a))
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
    """The bars flow into '+14'; chrome fills in; 'It isn't' opens the light world."""
    global F14_POLYS, F14_PATH
    target = polys_to_segments(F14_POLYS, N_MORPH)
    src = np.vstack([bars(0), bars(1)])
    km = seg(t, 11.5, 12.6)
    segs = morph(src, target, km)
    ev(11.5, "morph", t)
    k_fill = ease(seg(t, 12.6, 13.4))
    shrink = lerp(1.0, 0.82, ease(seg(t, 13.1, 13.8)))
    grow = lerp(0, 0.30, ease(seg(t, 14.3, 14.9), "back"))
    s = shrink + grow
    # the light world opens from the centre on "It isn't"
    kw = ease(seg(t, 14.3, 15.2))
    if kw > 0:
        c.save()
        clip = skia.Path()
        clip.addCircle(W / 2, 530, 1300 * kw)
        c.clipPath(clip, skia.ClipOp.kIntersect, True)
        c.drawImage(ground["light"], 0, 0)
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
        chrome_14(c, t, s, sweep_t=seg(t, 13.0, 14.2))
        c.restore()
        ev(12.6, "shimmer", t)


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
        ev(t_dock + 0.8, "thock", t)
    return lerp(bx, sx, k), lerp(by, sy, k), lerp(big_s, SHELF_S, k)


def arrow(c, x, y, w, col, a=1.0, k=1.0):
    p = stroke(col, 3, a)
    x1 = x + w * k
    c.drawLine(x, y, x1, y, p)
    if k > 0.6:
        c.drawLine(x1 - 12, y - 10, x1, y, p)
        c.drawLine(x1 - 12, y + 10, x1, y, p)


GRID_X, GRID_Y, GRID_S = CARD_W - 270, 70, 230


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
    a = alpha * k_in
    shadow = fill("#000000", 0.08 * a)
    shadow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, 14, CARD_W, CARD_H), 24, 24), shadow)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeWH(CARD_W, CARD_H), 24, 24), fill("#F5F6F7", 0.94 * a))
    draw_poly(c, rrect_pts(0, 0, CARD_W, CARD_H, 24), stroke(TURQ if active else "#B9BEC6", 1.5, a), ease(seg(t, cd["t0"], cd["t0"] + 0.8)))
    decode(c, cd["tag"], 40, 58, font(MONO_M, 20), TURQ, t, cd["t0"] + 0.2, 0.6, seed=30 + i, a=a)
    draw_icon(c, cd["icon"], 40, 96, 104, t, cd["t0"] + 0.3, INK, 1.0, 2.4)
    f_big = font(DISPLAY, 44)
    mx, my = 176, 170
    if cd["metric"][0] and t >= cd["t_a"]:
        c.drawString(cd["metric"][0], mx, my, f_big, fill(INK_SOFT, a * ease(seg(t, cd["t_a"], cd["t_a"] + 0.3))))
    if t >= cd["t_b"]:
        k = ease(seg(t, cd["t_b"], cd["t_b"] + 0.45))
        x2 = mx
        if cd["metric"][0]:
            w0 = text_w(cd["metric"][0], f_big) + 24
            arrow(c, mx + w0, my - 16, 54, TURQ, a, k)
            x2 = mx + w0 + 78
        c.drawString(cd["metric"][1], x2, my + (1 - k) * 12, f_big, fill(INK, a * k))
        ev(cd["t_b"], "chime_soft", t)
    decode(c, cd["sub"], mx, my + 40, font(MONO, 17), INK_SOFT, t, cd["t_a"] - 0.2, 0.5, seed=40 + i, a=a)
    type_on(c, cd["cap"], 40, 318, font(BODY, 28), INK, t, cd["t_cap"], 42, a)
    if grid:
        n_base, n_extra = cd["grid"]
        grid100(c, GRID_X, GRID_Y, GRID_S, t, n_base, n_extra, cd["t0"] + 0.6, cd["t_b"] + 0.1, remove=(cd["mode"] == "remove"), a=a)
    c.restore()


def sc4(c, t):
    for i in range(4):
        draw_card(c, i, t)


def sc5(c, t):
    """Same number: each card's grid lifts off the shelf and they converge into one, then ASCII, then chrome."""
    k = ease(seg(t, 41.9, 43.0))
    for i in range(4):
        draw_card(c, i, t, alpha=lerp(1.0, 0.25, k), grid=(k <= 0))
    if k > 0:
        ev(41.9, "whoosh", t)
        k_ascii = seg(t, 43.3, 44.3)
        big = 440
        for i in range(4):
            x, y, s = card_rect(i, 41.9)
            gx0, gy0, gs0 = x + GRID_X * s, y + GRID_Y * s, GRID_S * s
            kk = ease(seg(t, 41.9 + i * 0.08, 43.0 + i * 0.08))
            gx, gy, gs = lerp(gx0, W / 2 - big / 2, kk), lerp(gy0, 150, kk), lerp(gs0, big, kk)
            cd = CARDS[i]
            grid100(c, gx, gy, gs, 99, 52, 14, 0, 0, a=(1 - k_ascii) * 0.35 * (1 - ease(seg(t, 42.6, 43.1))))
        k_one = ease(seg(t, 42.7, 43.1))
        if k_one > 0:
            grid100(c, W / 2 - big / 2, 150, big, 99, 52, 14, 0, 0, a=k_one * (1 - k_ascii))
            ev(42.7, "chime_soft", t)
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
        c.drawString(chr_, x, y, fnt, fill(TURQ if i % 7 == 0 else INK, a))
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
        rect = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, 440, 560), 26, 26)
        sh = fill("#000000", 0.07 * k)
        sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y + 14, 440, 560), 26, 26), sh)
        c.drawRRect(rect, fill("#F4F5F6", 0.95 * k))
        draw_poly(c, rrect_pts(x, y, 440, 560, 26), stroke(TURQ, 1.4, k), ease(seg(t, t0, t0 + 0.9)))
        c.drawString(num, x + 36, y + 110, font(DISPLAY, 64), fill(INK, k))
        for j, line in enumerate(title.split("\n")):
            type_on(c, line, x + 36, y + 420 + j * 44, font(BODY_M, 36), INK, t, t0 + 0.3 + j * 0.3, 34, k)
        draw_icon(c, icon, x + 250, y + 170, 140, t, t0 + 0.2, INK, 1.0, 2.6)
        c.restore()
        ev(t0, "chime_soft", t)


def zoom_through(t):
    """Scale about the counter of the '0' in tile 02 (the vortex people liked, kept gentle)."""
    k = ease(seg(t, 52.6, 53.8), "i")
    return 1 + k * 70, (740 + 36 + 26, 320 + 110 - 24)


def frame(c, t, ground):
    if t < 14.3:
        c.drawImage(ground["dark"], 0, 0)
    else:
        c.drawImage(ground["light"], 0, 0)
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
    if t > 53.3:                                           # after the push: the ground and a mark
        k = seg(t, 53.3, 53.8)
        c.drawImage(ground["light"], 0, 0, skia.SamplingOptions(), fill("#FFFFFF", k))
        decode(c, "A01", W / 2, H / 2 + 12, font(DISPLAY, 34), INK, t, 53.4, 0.4, seed=99, align="center")
    # frame furniture: one thin line and a tiny label, always calm
    col = ON_DARK_SOFT if t < 14.3 else INK_SOFT
    c.drawString("A01  ·  FOURTEEN POINTS", 120, H - 60, font(MONO, 16), fill(col, 0.8))
    c.drawLine(120, H - 84, 300, H - 84, stroke(col, 1, 0.6))


def main():
    global F14_POLYS, F14_PATH
    os.makedirs(BUILD, exist_ok=True)
    F14_POLYS, F14_PATH = fourteen_polys()
    ground = {"light": marl(LIGHT, 1, 3.2), "dark": marl(DARK, 2, 2.4)}
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
    json.dump(sorted(set(EVENTS) | set(CUES)), open(os.path.join(BUILD, "events.json"), "w"))
    print(out, len(EVENTS), "sound events")


if __name__ == "__main__":
    main()
