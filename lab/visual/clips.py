"""Showcase clips for the v7 lab: four visual directions, each 8-10 s, rendered with holo.py.

  A  exploded   an AI accelerator comes apart layer by layer while the camera orbits it; HUD callouts
  B  rail       the camera glides low along a sentence of extruded line-work letters, then tilts up
  C  ascii      a torus knot shaded entirely in characters, decoding in, slowly turning
  D  ride       riding the exponential curve (1950 -> 2026) like a rollercoaster, then falling into
                the ring tunnel (the vortex)

    python3 clips.py still A 4.0      # one frame -> out/visual/A_4.0.png
    python3 clips.py render A         # out/visual/A_exploded.mp4 (silent) + A_events.json (for sound)
"""
import json
import math
import os
import sys

import numpy as np
import skia

sys.path.insert(0, os.path.dirname(__file__))
import holo as h  # noqa: E402
from holo import W, H, TURQ, GLOW, WHITE, MID, SOFT, EMERALD, ease, seg, clamp, lerp, smooth  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "out", "visual")
mg = h.mg
FOOTER = [True]          # the pilot hides the clips' footers (its captions live there)


# ================================================================ A: exploded accelerator
def chip_parts():
    """Parts in assembled position, each with the lift it gets when exploded (y units) and a label."""
    rng = np.random.default_rng(3)
    parts = []
    # substrate + BGA balls + traces
    sub = h.box(0, 0, 0, 8.0, 0.22, 8.0)
    traces = []
    for _ in range(46):
        x, z = rng.uniform(-3.6, 3.6), rng.uniform(-3.6, 3.6)
        pts = [(x, 0.115, z)]
        for _ in range(rng.integers(2, 5)):
            if rng.random() < 0.5:
                x = np.clip(x + rng.uniform(-1.4, 1.4), -3.8, 3.8)
            else:
                z = np.clip(z + rng.uniform(-1.4, 1.4), -3.8, 3.8)
            pts.append((x, 0.115, z))
        traces.append(np.array(pts))
    g = np.linspace(-3.6, 3.6, 18)
    balls = np.array([(x, -0.2, z) for x in g for z in g])
    parts.append(dict(name="SUBSTRATE", sub="18 × 18 BALL GRID", polys=sub, detail=traces, pts=balls, lift=0.0, col=MID, k0=0.0))
    # interposer
    parts.append(dict(name="INTERPOSER", sub="SILICON BRIDGE", polys=h.box(0, 0.42, 0, 7.2, 0.14, 4.6), detail=[], lift=1.0, col=SOFT, k0=0.1))
    # compute die with a core grid
    die = h.box(0, 0.58, -0.0, 2.6, 0.12, 2.6)
    cores = []
    for i in range(8):
        for j in range(8):
            cx, cz = -1.1 + i * 0.315, -1.1 + j * 0.315
            cores.append(h.rect_xz(cx, 0.645, cz, 0.24, 0.24))
    parts.append(dict(name="COMPUTE DIE", sub="64 CORE TILES", polys=die, detail=cores, lift=2.6, col=WHITE, k0=0.25, accent=True))
    # memory stacks: 8 slices each, which fan out when exploded
    for n, (x, z) in enumerate([(-2.9, -1.3), (-2.9, 0.0), (-2.9, 1.3), (2.9, -1.3), (2.9, 0.0), (2.9, 1.3)]):
        slices = []
        for s in range(8):
            slices.append(dict(y=0.52 + s * 0.075, polys=h.box(x, 0.0, z, 1.0, 0.05, 1.05)))
        parts.append(dict(name="MEMORY STACK" if n == 3 else None, sub="8 LAYERS" if n == 3 else None, stack=slices,
                          polys=[], detail=[], lift=1.7, col=MID, k0=0.35 + 0.03 * n))
    # lid and fins
    lid = h.box(0, 1.0, 0, 7.0, 0.28, 7.0) + [h.rect_xz(0, 1.145, 0, 5.2, 5.2)]
    parts.append(dict(name="HEAT SPREADER", sub="COPPER LID", polys=lid, detail=[], lift=4.1, col=MID, k0=0.55))
    fins = []
    for i in range(17):
        x = -3.2 + i * 0.4
        fins.append(np.array([[x, 1.3, -3.2], [x, 2.6, -3.2], [x, 2.6, 3.2], [x, 1.3, 3.2], [x, 1.3, -3.2]]))
    parts.append(dict(name="FIN ARRAY", sub="17 FINS", polys=fins, detail=[], lift=5.2, col=SOFT, k0=0.65))
    return parts


CHIP = None


def frame_A(c, t, dur=10.0):
    global CHIP
    if CHIP is None:
        CHIP = chip_parts()
    c.drawImage(h.ground("graphite"), 0, 0)
    # camera: slow orbit (-38 -> +70 deg), rising, pushing in a touch
    k = smooth(seg(t, 0.0, dur))
    az = lerp(-38, 70, k)
    el = lerp(16, 27, smooth(seg(t, 0.5, dur - 0.5)))
    dist = lerp(25, 21, k)
    kx = smooth(seg(t, 1.6, 6.0))
    cam = h.orbit((0, lerp(0.9, 3.6, kx), 0), lerp(21, 26, kx) + (dist - 25), az, el, fov=36)
    fr = h.Frame(cam, fade=(12, 45), dof=(dist, 0.10))
    # faint ground grid
    grid = [np.array([[x, -0.35, -9], [x, -0.35, 9]]) for x in np.arange(-9, 9.1, 1.5)] + \
           [np.array([[-9, -0.35, z], [9, -0.35, z]]) for z in np.arange(-9, 9.1, 1.5)]
    fr.lines([h.densify(p, 1.0) for p in grid], MID, 0.8, 0.12, glow=0, k=ease(seg(t, 0, 1.2)), tip=False)
    ex = lambda k0: smooth(seg(t, 1.6 + k0 * 2.4, 4.2 + k0 * 2.4))       # staggered explode, bottom first
    form = seg(t, 0.1, 1.8)
    anchors = []
    for i, p in enumerate(CHIP):
        e = ex(p["k0"])
        dy = p["lift"] * e
        shift = np.array([0, dy, 0])
        col = p["col"]
        if "stack" in p:
            for s_i, s in enumerate(p["stack"]):
                y = s["y"] + dy + s_i * 0.2 * e        # the accordion: slices fan apart
                polys = [q + np.array([0, y, 0]) for q in s["polys"]]
                fr.lines(polys, TURQ if s_i == 7 and e > 0.5 else col, 1.3, 0.85, glow=0.35, k=form, stagger=0.3, seed=i * 10 + s_i)
            if p["name"]:
                top = p["stack"][-1]["polys"][0][1] + np.array([0, p["stack"][-1]["y"] + dy + 7 * 0.2 * e, 0])
                anchors.append((p, top, e))
            continue
        polys = [q + shift for q in p["polys"]]
        fr.lines(polys, col, 1.6 if col == WHITE else 1.3, 0.95, glow=0.5, k=form, stagger=0.25, seed=i)
        if p["detail"]:
            det = [q + shift for q in p["detail"]]
            accent = p.get("accent")
            fr.lines(det, TURQ if accent else MID, 1.0, 0.8 if accent else 0.45, glow=0.8 if accent else 0.0,
                     k=seg(t, 1.2 + i * 0.1, 3.2 + i * 0.1), stagger=0.5, seed=i + 50)
        if "pts" in p:
            fr.points(p["pts"] + shift, SOFT, 0.9, 0.45 * ease(seg(t, 0.8, 2.0)))
        if p["name"]:
            anchors.append((p, polys[0][1], e))
    # the one turquoise line: a data path piercing every layer once exploded
    kpierce = ease(seg(t, 6.3, 7.6), "o")
    if kpierce > 0:
        path = np.array([[0.0, -1.0, 0.0], [0.0, 9.2, 0.0]])
        fr.lines([h.densify(path, 0.2)], TURQ, 2.2, 1.0, glow=1.2, k=kpierce)
    fr.draw(c, glow_gain=0.95, bloom_gain=0.45)
    # callouts after the explode settles
    items = [(fr.anchor(P), p["name"], p["sub"], 5.0 + 0.16 * j, TURQ if p.get("accent") else MID) for j, (p, P, e) in enumerate(anchors)]
    h.callout_column(c, items, t)
    title_a = ease(seg(t, 0.4, 1.2)) * (1 - ease(seg(t, 8.8, 9.6)))
    h.mono(c, "AI ACCELERATOR · EXPLODED VIEW · ILLUSTRATIVE", 120, 1010, 16, SOFT, title_a * FOOTER[0])
    h.vignette(c, 0.5)
    h.grain(c, t)


# ================================================================ B: type rail
RAIL = None


def keys(t, kf):
    """Smoothstep between keyframes [(t, value), ...]; values may be numbers or arrays."""
    if t <= kf[0][0]:
        return np.asarray(kf[0][1], float)
    for (t0, v0), (t1, v1) in zip(kf[:-1], kf[1:]):
        if t <= t1:
            return np.asarray(v0, float) + (np.asarray(v1, float) - np.asarray(v0, float)) * smooth(seg(t, t0, t1))
    return np.asarray(kf[-1][1], float)


def rail_geo():
    words = [("THE CURVE", 0.0), ("DOESN'T", -30.0), ("WAIT", -58.0)]
    polys, owner = [], []
    for wi, (w, z) in enumerate(words):
        ps = h.text3d(w, size=4.2, plane="xz", extrude=1.3, samples=5)
        polys += [q + np.array([0, 0, z]) for q in ps]
        owner += [wi] * len(ps)
    ruler = []
    for side in (-24.0, 24.0):
        ruler.append(h.densify(np.array([[side, 0, 14], [side, 0, -84]]), 1.0))
        for z in range(14, -85, -2):
            L = 1.6 if z % 10 == 0 else 0.6
            ruler.append(np.array([[side, 0, z], [side - np.sign(side) * L, 0, z]]))
    return polys, owner, ruler


def frame_B(c, t, dur=10.0):
    global RAIL
    if RAIL is None:
        RAIL = rail_geo()
    polys, owner, ruler = RAIL
    c.drawImage(h.ground("graphite"), 0, 0)
    eye = keys(t, [(0.0, (-7.0, 19.0, 30.0)), (3.2, (-2.0, 12.0, 2.0)), (6.2, (1.5, 7.0, -26.0)), (9.6, (0.0, 12.5, -45.5))])
    tgt = keys(t, [(0.0, (0.0, 0.0, 4.0)), (3.2, (0.0, 0.0, -22.0)), (6.2, (0.0, 1.0, -48.0)), (9.6, (0.0, 0.0, -58.5))])
    roll = math.radians(3.0 * math.sin(t / dur * math.pi * 2))
    cam = h.Cam(eye, tgt, fov=float(keys(t, [(0, 50), (6.2, 56), (9.6, 44)])), roll=roll)
    fr = h.Frame(cam, fade=(10, 80))
    fr.lines(ruler, MID, 1.0, 0.5, glow=0.0, k=ease(seg(t, 0, 1.4)), tip=False)
    t_word = [0.2, 2.6, 5.4]                                   # each word forms as it comes into view
    for i, (p, wi) in enumerate(zip(polys, owner)):
        col = TURQ if wi == 2 else WHITE
        fr.lines([p], col, 1.7, 0.95, glow=0.7 if col == TURQ else 0.35, k=ease(seg(t, t_word[wi], t_word[wi] + 1.6), "o"), seed=i)
    fr.draw(c, 0.9, 0.35)
    for zz in range(10, -81, -10):
        a = fr.anchor((24.0, 0, zz))
        if a and 0 < a[0] < W - 60 and 0 < a[1] < H:
            h.mono(c, f"{2026 - (10 - zz) // 10 * 7:d}", a[0] + 14, a[1] + 5, 14, SOFT, 0.75)
    h.vignette(c, 0.55)
    h.grain(c, t)


# ================================================================ C: ASCII torus knot
KNOT = None
ASC = None


def frame_C(c, t, dur=9.0):
    global KNOT, ASC
    if KNOT is None:
        KNOT = h.torus_knot(nu=1600, nv=60)
        ASC = h.Ascii(cols=160, rows=90)
    P, N = KNOT
    ang = 0.55 * t
    Pr = h.rot_x(h.rot_y(P, ang), 0.35 * math.sin(0.3 * t))
    Nr = h.rot_x(h.rot_y(N, ang), 0.35 * math.sin(0.3 * t))
    cam = h.Cam((0, 0.5, 11.0), (0, 0, 0), fov=40)
    light = (math.cos(0.7 * t) * 0.8, 0.9, 0.6)
    lum = h.zbuffer_lum(cam, Pr, Nr, light, ASC.cols, ASC.rows)
    # decode in: cells flicker through random characters before settling
    rng = np.random.default_rng(int(t * 30))
    k_in = seg(t, 0.2, 2.2)
    settle = rng.random(lum.shape) < k_in
    chars = np.clip((lum * (len(ASC.ramp) - 1)).round().astype(int), 0, len(ASC.ramp) - 1)
    noise_chars = rng.integers(1, len(ASC.ramp), lum.shape)
    chars = np.where(settle | (lum <= 0), chars, np.where(lum > 0, noise_chars, 0))
    fade_out = 1 - ease(seg(t, dur - 0.8, dur))
    img = ASC.compose(lum * fade_out, chars=chars)
    c.drawImage(h.ground("graphite"), 0, 0)
    sk = skia.Image.fromarray(img, colorType=skia.ColorType.kRGBA_8888_ColorType)
    c.drawImage(sk, 0, 0)
    # a soft glow of the same characters
    p = skia.Paint(BlendMode=skia.BlendMode.kPlus)
    p.setImageFilter(skia.ImageFilters.Blur(6, 6))
    p.setAlphaf(0.55)
    c.drawImage(sk, 0, 0, skia.SamplingOptions(), p)
    h.mono(c, "COMPOUNDING  ·  f(t) = a·2^(t/T)", 120, 1010, 16, SOFT, ease(seg(t, 1.0, 2.0)) * fade_out)
    h.vignette(c, 0.5)
    h.grain(c, t)


# ================================================================ D: ride the curve into the vortex
CURVE = None
MILESTONES = [(1956, "DARTMOUTH · THE WORD 'AI'"), (1997, "DEEP BLUE BEATS KASPAROV"), (2012, "ALEXNET"),
              (2017, "THE TRANSFORMER"), (2022, "CHATGPT"), (2026, "TWO LABS · 90 MINUTES APART")]


def curve_geo():
    years = np.linspace(1950, 2026.0, 1400)
    x = (years - 1950) * 1.0
    y = 0.026 * (np.exp((years - 1950) / 9.0) - 1)            # flat for decades, then nearly vertical
    P = np.stack([x, y, np.zeros_like(x)], 1)
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    return years, P, s


CTX = None


def frame_D(c, t, dur=12.0):
    global CURVE, CTX
    if CURVE is None:
        CURVE = curve_geo()
        wall = [h.densify(np.array([[x, -2, -16], [x, 130, -16]]), 4.0) for x in range(-10, 101, 5)] + \
               [h.densify(np.array([[-10, y, -16], [100, y, -16]]), 4.0) for y in range(0, 131, 5)]
        floor = [h.densify(np.array([[x, -2, -40], [x, -2, 30]]), 4.0) for x in range(-10, 101, 5)] + \
                [h.densify(np.array([[-10, -2, z], [100, -2, z]]), 4.0) for z in range(-40, 31, 5)]
        rng = np.random.default_rng(8)
        dust = np.stack([rng.uniform(-5, 95, 1800), rng.uniform(-2, 130, 1800), rng.uniform(-14, 14, 1800)], 1)
        CTX = (wall, floor, dust)
    years, P, s = CURVE
    c.drawImage(h.ground("graphite"), 0, 0)
    fall_t0 = 8.4
    if t < fall_t0 + 0.05:
        u = seg(t, 0.2, fall_t0)
        pos = s[-1] * (0.015 + 0.985 * u ** 2.4)
        i = int(np.clip(np.searchsorted(s, pos), 1, len(P) - 2))
        j = min(i + 10, len(P) - 1)
        tang = h._norm(P[j] - P[max(i - 10, 0)])
        nrm = np.array([-tang[1], tang[0], 0.0])
        eye1 = P[i] + nrm * 1.5 + np.array([0, 0, 2.6])                     # POV on the track
        ahead = P[min(i + 60, len(P) - 1)] if i + 60 < len(P) else P[-1] + tang * 20
        tgt1 = ahead + nrm * 0.6
        eye2 = P[i] + np.array([-9.0, -6.0, 24.0])                            # chase camera beside the climb
        tgt2 = P[i] + np.array([2.0, 7.0, 0.0])
        wv = smooth(seg(u, 0.5, 0.72))
        up = h._norm(nrm * (1 - wv) + np.array([0, 1.0, 0]) * wv)
        cam = h.Cam(eye1 * (1 - wv) + eye2 * wv, tgt1 * (1 - wv) + tgt2 * wv, fov=lerp(55, 50, wv), up=tuple(up))
        fr = h.Frame(cam, fade=(6, 70))
        fr.lines(CTX[0], MID, 0.9, 0.22, glow=0.0, tip=False)            # the grid wall behind the track
        fr.lines(CTX[1], MID, 0.9, 0.16, glow=0.0, tip=False)            # the floor
        fr.points(CTX[2], SOFT, 0.9, 0.55)                                # dust, for parallax
        rail = [P + np.array([0, 0, dz]) for dz in (-0.8, 0.8)]
        fr.lines(rail, WHITE, 1.8, 0.95, glow=0.35, k=ease(seg(t, 0, 0.9)), tip=False)
        ties = [np.array([P[q] + [0, 0, -0.8], P[q] + [0, 0, 0.8]]) for q in range(0, len(P), 5)]
        fr.lines(ties, MID, 1.0, 0.5, glow=0, tip=False)
        fr.lines([P[: i + 1]], TURQ, 2.6, 1.0, glow=1.1, tip=False)
        if wv > 0.05:                                                                  # the rider, in the chase view
            ring = h.circle(P[i], 1.1 + 0.15 * math.sin(t * 9), 40, "z")
            fr.lines([ring], TURQ, 1.4, 0.9 * wv, glow=1.0, tip=False)
            fr.points(P[i:i + 1], "#FFFFFF", 1.2, wv)
        for yr in range(1960, 2021, 10):                     # decade gates for speed and parallax
            q = int(np.searchsorted(years, yr))
            n2 = np.array([-h._norm(P[min(q + 5, len(P) - 1)] - P[max(q - 5, 0)])[1], h._norm(P[min(q + 5, len(P) - 1)] - P[max(q - 5, 0)])[0], 0])
            gate = [np.array([P[q] + [0, 0, -2.2], P[q] + n2 * 2.4 + [0, 0, -2.2], P[q] + n2 * 2.4 + [0, 0, 2.2], P[q] + [0, 0, 2.2]])]
            fr.lines(gate, SOFT, 1.1, 0.7, glow=0.1, tip=False)
            a = fr.anchor(P[q] + n2 * 2.4 + [0, 0, -2.2])
            if a:
                fr.label(lambda cc, a=a, yr=yr: h.mono(cc, str(yr), a[0] + 8, a[1] - 8, 15, SOFT, 0.8))
        for yr, lab in MILESTONES:
            q = int(np.searchsorted(years, yr))
            if q >= len(P):
                q = len(P) - 1
            if q < i - 4 or s[q] - s[i] > 95:              # only milestones just ahead are labelled
                continue
            n2 = nrm if q > len(P) - 30 else np.array([-h._norm(P[min(q + 5, len(P) - 1)] - P[q - 5])[1], h._norm(P[min(q + 5, len(P) - 1)] - P[q - 5])[0], 0])
            post = np.array([P[q] + [0, 0, -3.2], P[q] + n2 * 3.6 + [0, 0, -3.2]])
            fr.lines([post], TURQ, 1.4, 0.95, glow=0.6, tip=False)
            a = fr.anchor(post[1])
            if a and not (a[0] > W - 460 and a[1] < 230):
                fade = clamp(1 - (s[q] - s[i]) / 95) ** 0.7
                fr.label(lambda cc, a=a, yr=yr, lab=lab, fade=fade: (h.mono(cc, str(yr), a[0] + 12, a[1] - 4, 30, WHITE, fade, font=mg.DISPLAY),
                                                                     h.mono(cc, lab, a[0] + 12, a[1] + 22, 15, SOFT, fade)))
        fr.draw(c, 0.9, 0.4)
        h.mono(c, f"{years[i]:0.1f}", W - 120, 110, 44, WHITE, 1.0, align="right", font=mg.DISPLAY)
        h.mono(c, "YEAR", W - 120, 140, 14, SOFT, 0.9, align="right")
        slope = float(np.degrees(np.arctan2(tang[1], tang[0])))
        h.mono(c, f"GRADIENT {slope:4.1f}°", W - 120, 172, 14, TURQ if slope > 60 else SOFT, 0.9, align="right")
    kf = seg(t, fall_t0, dur)
    if kf > 0:
        a_in = ease(seg(t, fall_t0, fall_t0 + 0.4))
        depth = 190 * kf ** 1.8
        cam = h.Cam((0, -depth, 0), (0, -depth - 10, 0.0001), fov=lerp(70, 96, kf), roll=kf * 2.4, up=(0, 0, 1))
        fr = h.Frame(cam, fade=(2, 60))
        rings = []
        for n in range(96):
            y = -n * 2.2
            if y > -depth + 1:
                continue
            segs = 6 + (n % 3) * 2
            rot = (n % 2 * 2 - 1) * t * 0.6 + n * 0.3
            for q in range(segs):
                a0 = rot + q * 2 * math.pi / segs
                rings.append(h.circle((0, y, 0), 6.0, 12, "y", a0, a0 + 2 * math.pi / segs * 0.7))
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0B0C0E", a_in))
        fr.lines(rings, TURQ, 1.6, a_in, glow=0.9, tip=False)
        fr.draw(c, 1.0, 0.6)
        end = ease(seg(t, dur - 0.35, dur))
        if end > 0:
            c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0B0C0E", end))
    h.vignette(c, 0.55)
    h.grain(c, t)


CLIPS = {"A": ("A_exploded", frame_A, 10.0), "B": ("B_rail", frame_B, 10.0), "C": ("C_ascii", frame_C, 9.0), "D": ("D_ride", frame_D, 12.0)}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mode, key = sys.argv[1], sys.argv[2]
    name, fn, dur = CLIPS[key]
    if mode == "still":
        for tt in sys.argv[3:]:
            print(h.still(lambda cc, t: fn(cc, t, dur), float(tt), os.path.join(OUT, f"{key}_{float(tt):04.1f}.png")))
    else:
        import functools
        print(h.render(functools.partial(fn, dur=dur), dur, os.path.join(OUT, name + ".mp4")))
