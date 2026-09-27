"""EP03 · THE SHOVEL SELLERS, seamless (16:9, 1920x1080), in the A01 v6.2 grammar the user rated best:
no gauge, no ruler, no furniture. Every fact becomes its own visual, and each one flows into the next:
line formations with bright tips, morphs (any shape's segments flow into any other's), particles that re-form,
chrome numerals, and push-throughs into the next part. Timings come from build/lines.json (voice_build.py), by
line id, so a new voice (ElevenLabs George) just re-times everything.

This file is the cold open (1848 -> the bottle -> the rush -> the shop -> $36,000 -> the street -> the shovel ->
through the handle -> the prize).

    python3 ep03s.py still 5 12 18 ...     # build/still_*.png
    python3 ep03s.py render                # build/ep03s_open_silent.mp4 + build/events.json
"""
import json
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(HERE, "..", "..", "a01_v6")
sys.path.insert(0, V6)
os.environ.setdefault("A01V6_FONTS", os.path.join(V6, "fonts"))
import mograph as mg  # noqa: E402
import skia  # noqa: E402

W, H, FPS = 1920, 1080, 30
BUILD = os.path.join(HERE, "build")
META = json.load(open(os.path.join(BUILD, "lines.json")))
L = META["lines"]
TURQ, GLOW, WHITE, MID, SOFT = mg.TURQ, mg.TURQ_GLOW, mg.ON_DARK, mg.ON_DARK_MID, mg.ON_DARK_SOFT
GOLD = "#F2D9A0"                                   # warm white for the dust: gold, in our palette
ease, seg, clamp, lerp = mg.ease, mg.seg, mg.clamp, mg.lerp
N = 720                                            # segments every shape is resampled to, so all shapes can morph
EVENTS = []


def I(name):
    return next(i for i, x in enumerate(L) if x.get("id") == name or x.get("slot") == name)


def ls(name):
    return L[I(name)]["start"]


def le(name):
    return L[I(name)]["end"]


def at(name, frac):
    """A time a fraction of the way through a line (words are roughly even at this pace)."""
    return ls(name) + frac * (le(name) - ls(name))


def ev(t_evt, kind, now, x=None):
    if now - 1 / FPS < t_evt <= now:
        EVENTS.append((round(t_evt, 3), kind, 0.0 if x is None else float(np.clip((x - W / 2) / (W / 2), -0.8, 0.8))))


# ---------------------------------------------------------------- shapes (polylines in screen space)
def P(pts):
    return np.asarray(pts, float)


def bottle(cx, cy, s):
    path = [(-0.2, -1.5), (-0.2, -1.05), (-0.25, -0.9), (-0.7, -0.65), (-0.72, 1.05), (-0.62, 1.25), (0.62, 1.25),
            (0.72, 1.05), (0.7, -0.65), (0.25, -0.9), (0.2, -1.05), (0.2, -1.5)]
    body = mg.resample(P([(cx + x * s, cy + y * s) for x, y in path]), 90)
    cork = mg.rrect_pts(cx - 0.26 * s, cy - 1.85 * s, 0.52 * s, 0.36 * s, 0.07 * s, 6)
    return [body, cork]


def ellipse(cx, cy, rx, ry, a0=0, a1=360, n=64):
    a = np.radians(np.linspace(a0, a1, n))
    return np.column_stack([cx + rx * np.cos(a), cy + ry * np.sin(a)])


def pan(cx, cy, s):
    """A gold pan, three-quarter view: the rim, the base, the sloped sides."""
    rim = ellipse(cx, cy, s, 0.3 * s)
    base = ellipse(cx, cy + 0.34 * s, 0.56 * s, 0.16 * s, 0, 180, 32)
    sides = [P([(cx - s, cy), (cx - 0.56 * s, cy + 0.34 * s)]), P([(cx + s, cy), (cx + 0.56 * s, cy + 0.34 * s)])]
    ridge = ellipse(cx, cy + 0.14 * s, 0.8 * s, 0.22 * s, 10, 170, 24)
    return [rim, base, ridge] + sides


def shovel(cx, cy, s, ang=0.0):
    """Upright shovel; (cx, cy) = the tip of the blade; s = height scale."""
    blade = [(-0.16, -0.36), (0.16, -0.36), (0.155, -0.14), (0.1, -0.03), (0.0, 0.03), (-0.1, -0.03), (-0.155, -0.14), (-0.16, -0.36)]
    shaft_l = [(-0.018, -0.4), (-0.018, -1.02)]
    shaft_r = [(0.018, -0.4), (0.018, -1.02)]
    socket = [(-0.045, -0.36), (-0.018, -0.46)], [(0.045, -0.36), (0.018, -0.46)]
    grip = mg.arc(0, -1.1, 0.085, 0, 360, 36)
    polys = [P(blade), P(shaft_l), P(shaft_r), P(socket[0]), P(socket[1]), np.asarray(grip)]
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    out = []
    for q in polys:
        x, y = q[:, 0] * s, q[:, 1] * s
        out.append(np.column_stack([cx + x * ca - y * sa, cy + x * sa + y * ca]))
    return out


def house(x, y, w, h):
    return [P([(x, y), (x, y - h), (x + w / 2, y - h - 0.55 * w), (x + w, y - h), (x + w, y), (x, y)]),
            mg.rrect_pts(x + w * 0.38, y - h * 0.55, w * 0.24, h * 0.55, 3, 3)]


def river(x0, x1, y, amp=18, n=90):
    xs = np.linspace(x0, x1, n)
    return [np.column_stack([xs, y + amp * np.sin(xs / 60.0)]), np.column_stack([xs, y + 30 + amp * np.sin(xs / 60.0 + 1.2)])]


def glyphs(text, size, cx, cy):
    f = mg.font(mg.DISPLAY, size)
    w = f.measureText(text)
    return mg.glyph_polys(text, f, cx - w / 2, cy + size * 0.36), mg.text_path(text, f, cx - w / 2, cy + size * 0.36)


def segs(polys, n=N):
    return mg.polys_to_segments(polys, n)


def morph_flow(a, b, k, spread=0.35):
    """Segments leave in a sweep (left to right) instead of all at once, and travel on a slight arc."""
    order = np.argsort(np.argsort(a.mean(axis=1)[:, 0]))
    r = order / max(1, len(order) - 1)
    kk = np.clip((k * (1 + spread) - spread * r), 0, 1)
    kk = kk * kk * (3 - 2 * kk)
    out = a + (b - a) * kk[:, None, None]
    lift = np.sin(np.pi * kk)[:, None, None] * np.array([0, -60.0])[None, None, :]
    return out + lift, kk


def draw_segs(c, S, col=GLOW, w=1.7, a=1.0, glow=True, tips=None):
    if a <= 0:
        return
    path = skia.Path()
    for p0, p1 in S:
        path.moveTo(*p0); path.lineTo(*p1)
    if glow:
        g = mg.stroke(col, 6, 0.22 * a)
        g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5))
        c.drawPath(path, g)
    c.drawPath(path, mg.stroke(col, w, a))
    if tips is not None:
        moving = S[(tips > 0.02) & (tips < 0.98)]
        if len(moving):
            pts = [skia.Point(float(x), float(y)) for x, y in moving[::3, 1]]
            p = mg.stroke("#FFFFFF", 4.0, 0.9 * a); p.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawPoints(skia.Canvas.kPoints_PointMode, pts, p)


def formation(c, S, t, t0, dur, col=GLOW, w=1.7, seed_pt=None):
    """Edges light up in order of distance from a seed point, each drawing from its near end with a bright tip."""
    sp = np.array(seed_pt if seed_pt is not None else S[:, 0, :].mean(axis=0) + [0, 260])
    order = np.argsort(np.linalg.norm(S.mean(axis=1) - sp, axis=1))
    n = len(S)
    ts = t0 + dur * 0.75 * np.arange(n) / n
    k = np.clip((t - ts[np.argsort(order)]) / (dur * 0.25), 0, 1)
    a, b = S[:, 0, :], S[:, 1, :]
    flip = np.linalg.norm(a - sp, axis=1) > np.linalg.norm(b - sp, axis=1)
    a2, b2 = np.where(flip[:, None], b, a), np.where(flip[:, None], a, b)
    tip = a2 + (b2 - a2) * k[:, None]
    on = k > 0
    draw_segs(c, np.stack([a2[on], tip[on]], 1), col, w)
    live = on & (k < 1)
    if live.any():
        pts = [skia.Point(float(x), float(y)) for x, y in tip[live][::2]]
        p = mg.stroke("#FFFFFF", 4.5, 0.9); p.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPoints(skia.Canvas.kPoints_PointMode, pts, p)
    return k


def chrome_fill(c, path, k, sweep=None):
    """Fill a glyph path with chrome, rising from the bottom (k 0..1)."""
    if k <= 0:
        return
    b = path.getBounds()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(b.left() - 10, lerp(b.bottom(), b.top(), k), b.right() + 10, b.bottom() + 10))
    c.drawPath(path, mg.chrome_paint(b.top(), b.bottom()))
    c.restore()
    if sweep is not None and 0 < sweep < 1:
        x = lerp(b.left() - 200, b.right() + 200, sweep)
        sh = skia.GradientShader.MakeLinear([(x - 120, 0), (x + 120, 0)], [skia.Color4f(1, 1, 1, 0), skia.Color4f(1, 1, 1, 0.55), skia.Color4f(1, 1, 1, 0)])
        p = skia.Paint(AntiAlias=True); p.setShader(sh)
        c.save(); c.clipPath(path, skia.ClipOp.kIntersect, True); c.drawRect(b, p); c.restore()


def points(c, X, a=1.0, col=GOLD, size=3.2):
    if a <= 0 or len(X) == 0:
        return
    for q in range(3):
        sel = X[q::3]
        pts = [skia.Point(float(x), float(y)) for x, y in sel]
        p = mg.stroke(col if q else "#FFFFFF", size + q * 0.6, a * (0.55 + 0.2 * q))
        p.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPoints(skia.Canvas.kPoints_PointMode, pts, p)


def sample_on(polys, n, rng):
    """n points spread along polylines, proportional to length."""
    lens = np.array([mg.poly_len(p)[-1] for p in polys])
    idx = rng.choice(len(polys), n, p=lens / lens.sum())
    out = []
    for i in idx:
        q = polys[i]
        Lq = mg.poly_len(q)
        s = rng.uniform(0, Lq[-1])
        out.append((np.interp(s, Lq, q[:, 0]), np.interp(s, Lq, q[:, 1])))
    return np.array(out)


def label(c, s, x, y, t, t0, size=20, col=SOFT, align="center", a=1.0):
    mg.decode(c, s, x, y, mg.font(mg.MONO_M, size), col, t, t0, 0.5, seed=hash(s) % 97, align=align, a=a)


# ---------------------------------------------------------------- the scene data (built once)
CX, CY = W / 2, 500
RNG = np.random.default_rng(7)
G1848, P1848 = glyphs("1848", 250, CX, CY)
G36K, P36K = glyphs("$36,000", 210, CX, CY - 30)
BOTTLE = bottle(CX, CY + 20, 190)
PANS = [q for x in (-560, -290, -20) for q in pan(CX + x, 610, 118)]
SHOVELS = [q for j, x in enumerate((330, 500, 670)) for q in shovel(CX + x, 770, 440, ang=(-7, 0, 7)[j])]
SHOP = PANS + SHOVELS
SHELF = [P([(CX - 700, 668), (CX + 640, 668)]), P([(CX - 700, 776), (CX + 640, 776)])]
WEEKS = [mg.rrect_pts(CX - 560 + j * 128, 840, 100, 26, 6, 3) for j in range(9)]
STREET = [q for j in range(7) for q in house(CX - 700 + j * 205, 820, 150, 120)]
BIG_SHOVEL = shovel(CX, 930, 820)
N_DUST = 900
DUST_IN = None


def dust_home():
    """Where the gold settles inside the bottle: the lower third, heaped."""
    x = RNG.uniform(-0.62, 0.62, N_DUST)
    y = 1.2 - RNG.power(2.0, N_DUST) * 0.75 * (1 - 0.4 * np.abs(x))
    return np.column_stack([CX + x * 190, CY + 20 + y * 190])


DUST_HOME = dust_home()
DUST_SKY = np.column_stack([CX + RNG.normal(0, 18, N_DUST), np.full(N_DUST, CY - 520.0) - RNG.uniform(0, 300, N_DUST)])
DUST_SHOP = sample_on(SHOP + SHELF, N_DUST, RNG)
_rx = RNG.uniform(90, 460, N_DUST)
RUN_TARGET = np.column_stack([_rx, 790 + (_rx - 90) * 0.12 + RNG.normal(0, 22, N_DUST)])
RUN_DELAY = RNG.uniform(0, 0.45, N_DUST)


def dust_at(t):
    """The one set of dust that pours in, bursts out, runs for the river, and re-forms as the shop."""
    t_pour0, t_pour1 = at("bottle", 0.66), at("bottle", 0.95)
    t_burst = ls("mind") + 0.1
    t_run1 = at("mind", 0.95)
    t_shop0, t_shop1 = ls("shop") + 0.05, at("shop", 0.55)
    if t < t_pour0:
        return None, 0
    if t < t_burst:                                   # falling into the bottle, heaping at the bottom
        k = np.clip((t - t_pour0 - RUN_DELAY * (t_pour1 - t_pour0)) / (0.55 * (t_pour1 - t_pour0)), 0, 1)
        k = k * k
        return DUST_SKY + (DUST_HOME - DUST_SKY) * k[:, None], 1
    if t < t_shop0:                                    # out of the neck, then streaming left for the river
        u = (t - t_burst) / (t_run1 - t_burst)
        k = np.clip((u - RUN_DELAY) / 0.55, 0, 1)
        k = k * k * (3 - 2 * k)
        neck = np.array([CX, CY - 260.0])
        up = np.clip(u * 3, 0, 1)
        mid = DUST_HOME + (neck + RNG.normal(0, 1, (N_DUST, 2)) * [120, 60] - DUST_HOME) * up
        pos = mid + (RUN_TARGET - mid) * k[:, None]
        pos[:, 1] += np.sin(np.pi * k) * -120
        return pos, 1
    k = np.clip((t - t_shop0 - RUN_DELAY * 0.5) / (t_shop1 - t_shop0), 0, 1)
    k = k * k * (3 - 2 * k)
    return RUN_TARGET + (DUST_SHOP - RUN_TARGET) * k[:, None], 1 - clamp((t - t_shop1) / 0.8)


# ---------------------------------------------------------------- the frame
GROUND = {}


def frame(c, t):
    c.drawImage(GROUND["dark"], 0, 0)
    # 1848, drawn in light, then chrome
    t0 = ls("bottle")
    t_to_bottle = at("bottle", 0.55)
    S1848 = segs(G1848)
    SB = segs(BOTTLE)
    if t < t_to_bottle:
        k = formation(c, S1848, t, t0 + 0.1, 1.3, GLOW, seed_pt=(CX, CY + 400))
        ev(t0 + 0.1, "form", t)
        kf = ease(seg(t, t0 + 1.2, t0 + 1.9))
        chrome_fill(c, P1848, kf, sweep=seg(t, t0 + 1.6, t0 + 2.6))
        ev(t0 + 1.2, "glint", t)
        label(c, "SAN FRANCISCO · CALIFORNIA", CX, CY + 190, t, t0 + 1.4, 22, SOFT)
    # 1848 -> the bottle
    t_shop = ls("shop")
    if t_to_bottle <= t < t_shop + 0.8:
        km = seg(t, t_to_bottle, t_to_bottle + 1.0)
        S, kk = morph_flow(S1848, SB, km)
        a = 1 - 0.55 * ease(seg(t, t_shop - 0.2, t_shop + 0.8))
        shake = 0.0
        tb = ls("mind")
        if tb <= t < tb + 0.6:                          # the bottle jolts as the town hears
            shake = math.sin((t - tb) * 60) * 6 * (1 - (t - tb) / 0.6)
        draw_segs(c, S + np.array([shake, 0]), GLOW, 1.8, a, tips=kk if km < 1 else None)
        ev(t_to_bottle, "morph", t)
        if km >= 1:
            label(c, "A BOTTLE OF GOLD", CX + 330, CY - 120, t, t_to_bottle + 1.1, 20, GLOW, align="left")
            c.drawLine(CX + 150, CY - 60, CX + 318, CY - 128, mg.stroke(GLOW, 1.2, 0.6 * clamp((t - t_to_bottle - 1.1) / 0.4)))
    # the dust
    X, a = dust_at(t)
    if X is not None and a > 0:
        points(c, X, a)
        ev(at("bottle", 0.66), "scan", t)
        ev(ls("mind") + 0.1, "whoosh", t)
    # the river they run for
    tm = ls("mind")
    if tm <= t < t_shop + 1.0:
        kr = ease(seg(t, tm + 0.8, tm + 1.8)) * (1 - ease(seg(t, t_shop, t_shop + 0.8)))
        for q in river(60, 500, 860):
            mg.draw_poly(c, q, mg.stroke(GLOW, 1.4, 0.7 * kr), frac=kr)
        label(c, "THE RIVER", 280, 940, t, tm + 1.4, 18, SOFT, a=kr)
    # the shop: pans, then shovels, form where the dust lands
    t_36 = ls("36k")
    S_SHOP = segs(SHOP + SHELF)
    if t_shop <= t < t_36 + 1.4:
        k_pans = formation(c, segs(SHELF + PANS, 320), t, at("shop", 0.3), 1.1, WHITE, seed_pt=(CX - 900, 700)) if t < t_36 else None
        k_sh = formation(c, segs(SHOVELS, 300), t, at("shop", 0.72), 0.9, GLOW, seed_pt=(CX + 900, 700)) if t < t_36 else None
        ev(at("shop", 0.3), "form", t)
        ev(at("shop", 0.72), "latch", t, CX + 400)
        if t < t_36:
            label(c, "SAM BRANNAN'S STORE · STOCKED FIRST", CX, 900, t, at("shop", 0.5), 20, SOFT)
    # nine weeks, then the shop flows into $36,000
    S36 = segs(G36K)
    t_m36 = at("36k", 0.55)
    if t_36 <= t < ls("e2"):
        kw = seg(t, ls("36k") + 0.1, at("36k", 0.5))
        for j, r in enumerate(WEEKS):
            kk = clamp(kw * 9 - j)
            if kk > 0:
                c.drawPath(_poly_path(r), mg.stroke(MID, 1.4, 0.8))
                c.drawRect(skia.Rect.MakeXYWH(r[:, 0].min(), r[:, 1].min(), (r[:, 0].max() - r[:, 0].min()) * kk, 26), mg.fill(TURQ, 0.85))
                ev(ls("36k") + 0.1 + j * (at("36k", 0.5) - ls("36k") - 0.1) / 9, "tick", t, r[:, 0].mean())
        if kw > 0:
            label(c, "NINE WEEKS", CX, 912, t, ls("36k") + 0.2, 20, SOFT)
        km = seg(t, t_m36, t_m36 + 1.0)
        if t < t_m36:
            draw_segs(c, S_SHOP, WHITE, 1.6, 0.9)
        else:
            S, kk = morph_flow(S_SHOP, S36, km)
            kf = ease(seg(t, t_m36 + 1.0, t_m36 + 1.6))
            draw_segs(c, S, GLOW, 1.7, 1 - 0.85 * kf, tips=kk if km < 1 else None)
            chrome_fill(c, P36K, kf, sweep=seg(t, t_m36 + 1.3, t_m36 + 2.3))
            ev(t_m36, "morph", t)
            ev(t_m36 + 1.0, "thock", t)
    # buy-the-street rich: the weeks become a street, and it all sells
    te2 = ls("e2")
    t_never = ls("never")
    if te2 <= t < t_never + 1.2:
        up = ease(seg(t, te2 + 0.1, te2 + 0.8))
        c.save()
        c.translate(CX, CY - 30); c.scale(lerp(1, 0.55, up), lerp(1, 0.55, up)); c.translate(-CX, -(CY - 30) + lerp(0, -420, up))
        kfade = 1 - ease(seg(t, t_never, t_never + 0.5))
        c.saveLayerAlpha(None, int(255 * kfade))
        chrome_fill(c, P36K, 1.0)
        c.restore()
        c.restore()
        label(c, "IN 1848 MONEY", CX, 330, t, te2 + 0.9, 20, SOFT, a=kfade)
        SW = segs(sum(([w] for w in WEEKS), []), 360)
        SS = segs(STREET, 360)
        ks = seg(t, te2 + 0.6, te2 + 1.6)
        S, kk = morph_flow(SW, SS, ks)
        draw_segs(c, S, WHITE, 1.6, kfade, tips=kk if ks < 1 else None)
        ev(te2 + 0.6, "morph", t)
        for j in range(7):
            tk = at("e2", 0.62) + j * 0.14
            ka = ease(seg(t, tk, tk + 0.18), "o") * kfade
            if ka > 0:
                x = CX - 700 + j * 205 + 75
                r = skia.Rect.MakeXYWH(x - 44, 830, 88, 30)
                c.drawRoundRect(r, 6, 6, mg.fill(TURQ, ka))
                f = mg.font(mg.MONO_M, 17)
                c.drawString("SOLD", x - f.measureText("SOLD") / 2, 851, f, mg.fill("#071413", ka))
                ev(tk, "latch", t, x)
    # he never dug: everything becomes one shovel, which starts to scoop and stops dead
    if t_never <= t:
        k_in = seg(t, t_never, t_never + 1.0)
        src = segs(STREET + [q for q in G36K], N)
        dst = segs(BIG_SHOVEL, N)
        S, kk = morph_flow(src, dst, k_in)
        ev(t_never, "morph", t)
        # the scoop: a tilt that starts on "one fucking" and freezes on "scoop"
        tilt = 0.0
        t_sc = at("never", 0.72)
        if t > t_sc:
            tilt = -28 * ease(seg(t, t_sc, t_sc + 0.35), "o")
        if tilt:
            ang = math.radians(tilt)
            ca, sa = math.cos(ang), math.sin(ang)
            pivot = np.array([CX, 930.0])
            d = S - pivot
            S = pivot + np.stack([d[..., 0] * ca - d[..., 1] * sa, d[..., 0] * sa + d[..., 1] * ca], -1)
        kz = seg(t, le("never") + 0.15, ls("rule") - 0.05)      # push through the D-grip into the next part
        z = 1 + 80 * ease(kz, "i") ** 2
        grip = np.array([CX, 930 - 1.1 * 820])
        if tilt:
            d = grip - np.array([CX, 930.0])
            grip = np.array([CX, 930.0]) + np.array([d[0] * math.cos(math.radians(tilt)) - d[1] * math.sin(math.radians(tilt)),
                                                    d[0] * math.sin(math.radians(tilt)) + d[1] * math.cos(math.radians(tilt))])
        c.save()
        c.translate(*grip); c.scale(z, z); c.translate(*(-grip))
        draw_segs(c, S, GLOW, 1.9, 1.0 - 0.9 * kz, tips=kk if k_in < 1 else None)
        c.restore()
        if kz <= 0:
            label(c, "NEVER DUG", CX + 250, 520, t, t_never + 1.2, 24, GLOW, align="left")
        ev(t_sc + 0.35, "thock", t)
        ev(le("never") + 0.15, "zoom", t)
        if kz > 0.6:
            mg.ring_tunnel(c, CX, 540, lerp(1, 40, (kz - 0.6) / 0.4), a=0.8 * (1 - kz))
    # the prize, waiting on the other side
    tr = ls("rule")
    if t >= tr - 0.05:
        k = ease(seg(t, tr, tr + 0.5), "o")
        r = 16 + 3 * math.sin((t - tr) * 5)
        g = mg.fill(GLOW, 0.35 * k); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
        c.drawCircle(CX, 520, r * 2.2, g)
        c.drawCircle(CX, 520, r * k, mg.fill(TURQ, k))
        c.drawCircle(CX, 520, (r + 14) * k, mg.stroke(GLOW, 1.4, 0.6 * k))
        label(c, "THE PRIZE", CX, 470, t, tr + 0.3, 20, SOFT)
        ev(tr, "confirm", t)
    # the only furniture: one thin line and a tiny label, as in A01
    c.drawString("EP03  ·  THE SHOVEL SELLERS", 120, H - 60, mg.font(mg.MONO, 16), mg.fill(SOFT, 0.8))
    c.drawLine(120, H - 84, 300, H - 84, mg.stroke(SOFT, 1, 0.6))


def _poly_path(q):
    p = skia.Path()
    p.moveTo(*q[0])
    for x, y in q[1:]:
        p.lineTo(x, y)
    return p


def setup():
    GROUND["dark"] = mg.marl(mg.DARK, 2, 2.4)


if __name__ == "__main__":
    setup()
    os.makedirs(BUILD, exist_ok=True)
    surf = skia.Surface(W, H)
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]:
            c = surf.getCanvas(); c.clear(skia.ColorBLACK)
            frame(c, float(tt))
            p = os.path.join(BUILD, f"still_{float(tt):05.1f}.png")
            surf.makeImageSnapshot().save(p, skia.kPNG)
            print(p)
    else:
        dur = ls("rule") + 2.4
        out = os.path.join(BUILD, "ep03s_open_silent.mp4")
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                               "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            c = surf.getCanvas(); c.clear(skia.ColorBLACK)
            frame(c, i / FPS)
            ff.stdin.write(surf.makeImageSnapshot().tobytes())
        ff.stdin.close(); ff.wait()
        json.dump(dict(events=EVENTS, dur=dur), open(os.path.join(BUILD, "events.json"), "w"))
        print(out, len(EVENTS), "events")
