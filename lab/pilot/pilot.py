"""THE CURVE, pilot (v7 lab): the visual timeline, driven by build/lines.json from voice_build.py.

Scenes (each starts on a line and crossfades into the next, so every change reads as a transformation):
  chip    the accelerator forms, then comes apart while the camera orbits      (lines 0-3)
  curve   ride the exponential from 1950 to 2026, then the chase view up the wall (lines 4-10)
  vortex  peer over the top, the hang, the fall through the ring tunnel, the landing (line 11)
  gold    1848 in extruded line work, a stream of people, one point turning to the shovels (12-16)
  shop    the swarm digging for the same gold; the quiet takeaway; through its door (17-19)
  close   the type rail THE CURVE DOESN'T WAIT, then the sign-off (20-22)
Captions follow every line (active word in turquoise); number cards carry the sources.

    python3 pilot.py still 30.5 [..]      # frames -> build/still_*.png
    python3 pilot.py render               # build/pilot_silent.mp4 + build/events.json (sound cues)
"""
import functools
import json
import math
import os
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "visual"))
import holo as h  # noqa: E402
import clips as cl  # noqa: E402
from holo import W, H, TURQ, GLOW, WHITE, MID, SOFT, EMERALD, ease, seg, clamp, lerp, smooth  # noqa: E402

mg = h.mg
BUILD = os.path.join(HERE, "build")
META = json.load(open(os.path.join(BUILD, "lines.json")))
L = META["lines"]
DUR = META["total"]


def ls(i):
    return L[i]["start"]


def le(i):
    return L[i]["end"]


# scene windows: (name, start, end); a 0.6 s crossfade is centred on each boundary
B = {
    "chip": (0.0, ls(4) - 0.5),
    "curve": (ls(4) - 0.5, ls(11) - 0.4),
    "vortex": (ls(11) - 0.4, ls(12) - 0.35),
    "gold": (ls(12) - 0.35, ls(17) - 0.45),
    "shop": (ls(17) - 0.45, ls(20) - 0.55),
    "close": (ls(20) - 0.55, DUR),
}
XF = 0.6
FALL_T0 = le(11) + 1.0            # the Shepard fall starts here (the vortex sound is triggered 0.56 s earlier)
LAND = FALL_T0 + 3.24             # the impact

CUES = []                         # (time, sound, gain_db, pan) for the mixer


def cue(t, name, gain=0.0, pan=0.0):
    CUES.append((round(t, 3), name, gain, pan))


# ================================================================ chip (lines 0-3)
def sc_chip(c, t):
    # slow the showcase clip A to the lines: formation under line 0, explode through lines 1-3, callouts on 3
    t0, t1 = B["chip"]
    tl = lerp(0.0, 10.0, seg(t, t0, t1 + 0.6))
    cl.frame_A(c, tl, dur=10.0)


# ================================================================ curve (lines 4-10)
YEARS_KF = None


def year_at(t):
    kf = [(ls(4) - 0.6, 1950.0), (ls(5) + 0.4, 1956.0), (ls(6) + 0.2, 1972.0), (ls(7), 1990.0),
          (ls(7) + 1.2, 2000.0), (ls(7) + 2.4, 2012.0), (le(7), 2020.0), (le(8) - 0.8, 2026.0)]
    if t <= kf[0][0]:
        return kf[0][1]
    for (a, ya), (b, yb) in zip(kf[:-1], kf[1:]):
        if t <= b:
            return ya + (yb - ya) * smooth(seg(t, a, b)) if yb - ya < 20 else ya + (yb - ya) * seg(t, a, b)
    return 2026.0


def sc_curve(c, t, peer=0.0):
    """The ride; peer (0..1) tips the camera over the top to look down (used by the vortex scene)."""
    if cl.CURVE is None:
        cl.frame_D(c, 0.0)                   # builds geometry caches
    years, P, s = cl.CURVE
    wall, floor, dust = cl.CTX
    c.drawImage(h.ground("graphite"), 0, 0)
    yr = year_at(t)
    i = int(np.clip(np.searchsorted(years, yr), 1, len(P) - 2))
    j = min(i + 10, len(P) - 1)
    tang = h._norm(P[j] - P[max(i - 10, 0)])
    nrm = np.array([-tang[1], tang[0], 0.0])
    u = seg(yr, 1950, 2026)
    eye1 = P[i] + nrm * 1.5 + np.array([0, 0, 2.6])
    ahead = P[min(i + 60, len(P) - 1)] if i + 60 < len(P) else P[-1] + tang * 20
    tgt1 = ahead + nrm * 0.6
    eye2 = P[i] + np.array([-9.0, -6.0, 24.0])
    tgt2 = P[i] + np.array([2.0, 7.0, 0.0])
    wv = smooth(seg(yr, 2006, 2019))
    up = h._norm(nrm * (1 - wv) + np.array([0, 1.0, 0]) * wv)
    eye = eye1 * (1 - wv) + eye2 * wv
    tgt = tgt1 * (1 - wv) + tgt2 * wv
    if peer > 0:                              # swing round above the summit and look down the drop
        top = P[-1]
        eye3 = top + np.array([6.0, 10.0, 9.0])
        tgt3 = top + np.array([14.0, -30.0, 0.0])
        eye = eye * (1 - peer) + eye3 * peer
        tgt = tgt * (1 - peer) + tgt3 * peer
        up = h._norm(up * (1 - peer) + np.array([-1.0, 0.3, 0]) * peer)
    cam = h.Cam(eye, tgt, fov=lerp(55, 50, wv) + 12 * peer, up=tuple(up))
    fr = h.Frame(cam, fade=(6, 70))
    fr.lines(wall, MID, 0.9, 0.22, glow=0.0, tip=False)
    fr.lines(floor, MID, 0.9, 0.16, glow=0.0, tip=False)
    fr.points(dust, SOFT, 0.9, 0.55)
    kin = ease(seg(t, B["curve"][0], B["curve"][0] + 1.0))
    rail = [P + np.array([0, 0, dz]) for dz in (-0.8, 0.8)]
    fr.lines(rail, WHITE, 1.8, 0.95, glow=0.35, k=kin, tip=False)
    ties = [np.array([P[q] + [0, 0, -0.8], P[q] + [0, 0, 0.8]]) for q in range(0, len(P), 5)]
    fr.lines(ties, MID, 1.0, 0.5 * kin, glow=0, tip=False)
    fr.lines([P[: i + 1]], TURQ, 2.6, 1.0, glow=1.1, tip=False)
    if wv > 0.05:                                  # the rider marker only reads in the chase view
        ring = h.circle(P[i], 1.1 + 0.15 * math.sin(t * 9), 40, "z")
        fr.lines([ring], TURQ, 1.4, 0.9 * wv, glow=1.0, tip=False)
        fr.points(P[i:i + 1], "#FFFFFF", 1.2, wv)
    if peer > 0:                                   # the mouth of the vortex, waiting under the summit
        top = P[-1]
        mouth = []
        for n in range(14):
            yy = top[1] - 10 - n * 2.4
            segs = 6 + (n % 3) * 2
            rot = (n % 2 * 2 - 1) * t * 0.6 + n * 0.3
            for q in range(segs):
                a0 = rot + q * 2 * math.pi / segs
                mouth.append(h.circle((top[0] + 14, yy, 0), 6.0, 12, "y", a0, a0 + 2 * math.pi / segs * 0.7))
        fr.lines(mouth, TURQ, 1.5, 0.9 * peer, glow=0.9, tip=False)
    for dec in range(1960, 2021, 10):
        q = int(np.searchsorted(years, dec))
        tq = h._norm(P[min(q + 5, len(P) - 1)] - P[max(q - 5, 0)])
        n2 = np.array([-tq[1], tq[0], 0])
        gate = [np.array([P[q] + [0, 0, -2.2], P[q] + n2 * 2.4 + [0, 0, -2.2], P[q] + n2 * 2.4 + [0, 0, 2.2], P[q] + [0, 0, 2.2]])]
        fr.lines(gate, SOFT, 1.1, 0.7, glow=0.1, tip=False)
        a = fr.anchor(P[q] + n2 * 2.4 + [0, 0, -2.2])
        if a and not (a[0] > W - 460 and a[1] < 230):
            fr.label(lambda cc, a=a, dec=dec: h.mono(cc, str(dec), a[0] + 8, a[1] - 8, 15, SOFT, 0.8))
    for yr_m, lab in cl.MILESTONES:
        q = min(int(np.searchsorted(years, yr_m)), len(P) - 1)
        if q < i - 4 or s[q] - s[i] > 95:
            continue
        tq = h._norm(P[min(q + 5, len(P) - 1)] - P[max(q - 5, 0)])
        n2 = nrm if q > len(P) - 30 else np.array([-tq[1], tq[0], 0])
        post = np.array([P[q] + [0, 0, -3.2], P[q] + n2 * 3.6 + [0, 0, -3.2]])
        fr.lines([post], TURQ, 1.4, 0.95, glow=0.6, tip=False)
        a = fr.anchor(post[1])
        if a and not (a[0] > W - 460 and a[1] < 230):
            fade = clamp(1 - (s[q] - s[i]) / 95) ** 0.7 * (1 - peer)
            fr.label(lambda cc, a=a, yr_m=yr_m, lab=lab, fade=fade: (h.mono(cc, str(yr_m), a[0] + 12, a[1] - 4, 30, WHITE, fade, font=mg.DISPLAY),
                                                                     h.mono(cc, lab, a[0] + 12, a[1] + 22, 15, SOFT, fade)))
    fr.draw(c, 0.9, 0.4)
    hud = 1 - peer
    h.mono(c, f"{years[i]:0.1f}", W - 120, 110, 44, WHITE, hud, align="right", font=mg.DISPLAY)
    h.mono(c, "YEAR", W - 120, 140, 14, SOFT, 0.9 * hud, align="right")
    slope = float(np.degrees(np.arctan2(tang[1], tang[0])))
    h.mono(c, f"GRADIENT {slope:4.1f}°", W - 120, 172, 14, TURQ if slope > 60 else SOFT, 0.9 * hud, align="right")
    h.vignette(c, 0.55)


# ================================================================ vortex (line 11 + the fall)
def sc_vortex(c, t):
    if t < FALL_T0:
        peer = smooth(seg(t, B["vortex"][0], le(11)))
        sc_curve(c, t, peer=peer)
        hang = seg(t, le(11) + 0.35, FALL_T0)
        if hang > 0:                              # the hang: everything holds its breath
            c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0B0C0E", 0.35 * hang))
        return
    kf = seg(t, FALL_T0, LAND)
    c.drawImage(h.ground("graphite"), 0, 0)
    depth = 200 * kf ** 1.7
    cam = h.Cam((0, -depth, 0), (0, -depth - 10, 0.0001), fov=lerp(72, 98, kf), roll=kf * 2.6, up=(0, 0, 1))
    fr = h.Frame(cam, fade=(2, 60))
    rings = []
    for n in range(100):
        y = -n * 2.2
        if y > -depth + 1:
            continue
        segs = 6 + (n % 3) * 2
        rot = (n % 2 * 2 - 1) * t * 0.6 + n * 0.3
        for q in range(segs):
            a0 = rot + q * 2 * math.pi / segs
            rings.append(h.circle((0, y, 0), 6.0, 12, "y", a0, a0 + 2 * math.pi / segs * 0.7))
    c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0B0C0E", 0.6))
    fr.lines(rings, TURQ, 1.6, ease(seg(t, FALL_T0, FALL_T0 + 0.3)), glow=0.9, tip=False)
    fr.draw(c, 1.0, 0.6)
    fl = seg(t, LAND - 0.06, LAND + 0.5)          # the landing: a soft turquoise flash that settles to graphite
    if fl > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill(GLOW, 0.22 * (1 - fl) * (fl < 1)))
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0E1013", ease(fl)))
    h.vignette(c, 0.6)


# ================================================================ gold (lines 12-16)
GOLD = {}


def gold_geo():
    if GOLD:
        return GOLD
    GOLD["digits"] = h.text3d("1848", size=5.0, plane="xy", extrude=0.8, samples=6, origin=(0, 2.6, 0))
    x = np.linspace(-26, 26, 200)
    GOLD["river"] = [np.stack([x, np.full_like(x, -0.2), -6 + 1.6 * np.sin(x / 4.0) + dz], 1) for dz in (-0.9, 0.9)]
    rng = np.random.default_rng(12)
    n = 520
    GOLD["p0"] = np.stack([rng.uniform(-24, 24, n), np.zeros(n), rng.uniform(6, 22, n)], 1)
    GOLD["pdest"] = np.stack([GOLD["p0"][:, 0] * 0.7, np.zeros(n), -6 + 1.6 * np.sin(GOLD["p0"][:, 0] * 0.7 / 4.0) + rng.uniform(-0.7, 0.7, n)], 1)
    GOLD["delay"] = rng.uniform(0, 1.2, n)
    sh = [np.array([[0, 0, 0], [0, 3.0, 0]]),                                            # handle
          np.array([[-0.45, 3.0, 0], [0.45, 3.0, 0]]),                                  # grip
          np.array([[0, 0, 0], [-0.7, -0.2, 0], [-0.75, -1.3, 0], [0, -1.8, 0], [0.75, -1.3, 0], [0.7, -0.2, 0], [0, 0, 0]])]
    GOLD["shovel"] = [q * 1.6 + np.array([14.0, 2.6, 4.0]) for q in sh]
    return GOLD


def sc_gold(c, t):
    g = gold_geo()
    t0 = B["gold"][0]
    c.drawImage(h.ground("graphite"), 0, 0)
    az = lerp(-12, 14, seg(t, t0, B["gold"][1]))
    cam = h.orbit((2.0, 1.6, 0), 34, az, lerp(14, 22, seg(t, t0, B["gold"][1])), fov=40)
    fr = h.Frame(cam, fade=(14, 70))
    grid = [h.densify(np.array([[x, -0.3, -20], [x, -0.3, 24]]), 2.0) for x in range(-30, 31, 3)] + \
           [h.densify(np.array([[-30, -0.3, z], [30, -0.3, z]]), 2.0) for z in range(-20, 25, 3)]
    fr.lines(grid, MID, 0.8, 0.10, glow=0, tip=False)
    # 1848 forms on line 12, then lifts and thins as the people start running (line 13)
    kd = ease(seg(t, ls(12) - 0.2, ls(12) + 1.4), "o")
    lift = ease(seg(t, ls(13) - 0.2, ls(14)))
    digits = [q + np.array([0, 6.0 * lift, -8 * lift]) for q in g["digits"]]
    fr.lines(digits, WHITE, 1.8, 0.95 * (1 - lift), glow=0.45, k=kd, stagger=0.3, seed=4)
    kr = ease(seg(t, ls(13) - 0.4, ls(13) + 0.8))
    fr.lines(g["river"], TURQ if kr >= 1 else MID, 1.4, 0.8 * kr, glow=0.5, k=kr, tip=False)
    # the crowd running for the river
    kp = seg(t, ls(13) - 0.1, ls(14) + 1.5)
    if kp > 0:
        k = np.clip((kp * 2.2 - g["delay"]) / 1.0, 0, 1)
        k = k * k * (3 - 2 * k)
        pts = g["p0"] * (1 - k[:, None]) + g["pdest"] * k[:, None]
        fr.points(pts, SOFT, 1.6, 0.85 * ease(seg(t, ls(13) - 0.3, ls(13) + 0.3)))
    # one point turns the other way: Brannan, to the shovels
    kb = ease(seg(t, ls(14) + 0.3, ls(14) + 2.0))
    if kb > 0:
        a0 = np.array([4.0, 0.0, 9.0])
        a1 = np.array([14.0, 0.0, 4.0])
        path = np.array([a0 + (a1 - a0) * q for q in np.linspace(0, kb, 30)])
        fr.lines([path], TURQ, 2.0, 1.0, glow=1.0, k=1.0, tip=False)
        fr.points(path[-1:], "#FFFFFF", 2.4, 1.0)
        fr.lines(g["shovel"], TURQ, 1.8, 1.0, glow=0.8, k=ease(seg(t, ls(14) + 1.2, ls(14) + 2.4), "o"), seed=9)
        an = fr.anchor(np.array([14.0, 7.8, 4.0]))
        if an:
            fr.label(lambda cc, an=an: (mg.decode(cc, "SAM BRANNAN", an[0], an[1] - 30, mg.font(mg.MONO_M, 19), WHITE, t, ls(14) + 1.0, dur=0.5, seed=5, align="center"),
                                        mg.decode(cc, "STOREKEEPER · 1848", an[0], an[1] - 6, mg.font(mg.MONO, 15), SOFT, t, ls(14) + 1.2, dur=0.5, seed=6, align="center")))
    fr.draw(c, 0.9, 0.4)
    # $36,000 counter (line 15)
    kc = seg(t, ls(15) + 0.1, ls(15) + 1.8)
    if kc > 0:
        a = ease(seg(t, ls(15), ls(15) + 0.4)) * (1 - ease(seg(t, ls(16) - 0.3, ls(16) + 0.2)))
        v = 36000 * ease(kc, "o")
        txt = f"${v:,.0f}"
        f = mg.font(mg.DISPLAY, 118)
        w = f.measureText(txt)
        c.drawString(txt, W / 2 - w / 2, 300, f, mg.chrome_paint(200, 310, a))
        h.mono(c, "IN NINE WEEKS · WITHOUT SWINGING A PICK", W / 2, 350, 18, SOFT, a, align="center")
    # the chiasmus (line 16): two columns
    kx = ease(seg(t, ls(16) - 0.1, ls(16) + 0.5))
    if kx > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0E1013", 0.72 * kx))
        for side, (top, big, col, tt) in enumerate([("THEY SAW", "A GOLD RUSH", WHITE, ls(16)), ("HE SAW", "A SUPPLY CHAIN", TURQ, ls(16) + 1.3)]):
            x = W * (0.3 if side == 0 else 0.7)
            mg.decode(c, top, x, 420, mg.font(mg.MONO_M, 22), SOFT, t, tt, dur=0.4, seed=11 + side, align="center")
            mg.decode(c, big, x, 500, mg.font(mg.DISPLAY, 50), col, t, tt + 0.15, dur=0.5, seed=13 + side, align="center")
        c.drawLine(W / 2, 380, W / 2, 380 + 170 * kx, mg.stroke(MID, 1.2, 0.7))
    h.vignette(c, 0.55)


# ================================================================ shop (lines 17-19)
SHOP = {}


def shop_geo():
    if SHOP:
        return SHOP
    rng = np.random.default_rng(21)
    n = 900
    ph = rng.uniform(0, 2 * np.pi, n)
    r = rng.uniform(8, 22, n)
    SHOP["swarm0"] = np.stack([np.cos(ph) * r, rng.uniform(-2, 10, n), np.sin(ph) * r], 1) + np.array([-18, 0, -6])
    core = rng.normal(0, 1, (n, 3))
    core = core / np.linalg.norm(core, axis=1, keepdims=True) * rng.uniform(0.3, 1.6, (n, 1))
    SHOP["swarm1"] = core + np.array([-18, 4, -6])
    # a small takeaway, in line work, at the edge of town
    x0, z0 = 14.0, 6.0
    polys = h.box(x0, 2.2, z0, 7.0, 4.4, 4.0)
    polys += [np.array([[x0 - 1.0, 0, z0 + 2.001], [x0 - 1.0, 2.8, z0 + 2.001], [x0 + 0.6, 2.8, z0 + 2.001], [x0 + 0.6, 0, z0 + 2.001]])]  # door
    polys += [np.array([[x0 + 1.2, 1.0, z0 + 2.001], [x0 + 3.1, 1.0, z0 + 2.001], [x0 + 3.1, 2.8, z0 + 2.001], [x0 + 1.2, 2.8, z0 + 2.001], [x0 + 1.2, 1.0, z0 + 2.001]])]  # window
    for k in range(9):                                                           # striped awning
        xa = x0 - 3.5 + k * 7.0 / 8
        polys.append(np.array([[xa, 3.4, z0 + 2.0], [xa, 3.0, z0 + 3.0]]))
    polys.append(np.array([[x0 - 3.5, 3.0, z0 + 3.0], [x0 + 3.5, 3.0, z0 + 3.0]]))
    SHOP["shop"] = polys
    SHOP["sign"] = h.text3d("TAKEAWAY", size=0.9, plane="xy", origin=(x0, 3.9, z0 + 2.02))
    SHOP["lamp"] = [np.array([[x0 - 6, 0, z0 + 3.5], [x0 - 6, 6.2, z0 + 3.5], [x0 - 5.0, 6.2, z0 + 3.5]])]
    SHOP["door"] = np.array([x0 - 0.2, 1.4, z0 + 2.0])
    return SHOP


def sc_shop(c, t):
    g = shop_geo()
    c.drawImage(h.ground("graphite"), 0, 0)
    # camera: on the swarm (line 17) -> pans to the shop (line 18) -> dollies through the door (line 19)
    pan = smooth(seg(t, ls(18) - 0.4, ls(18) + 1.8))
    push = seg(t, ls(19) + 1.2, le(19) + 0.5) ** 2.2
    tgt_a, eye_a = np.array([-18.0, 4.0, -6.0]), np.array([-4.0, 9.0, 24.0])
    tgt_b, eye_b = np.array([14.0, 2.2, 6.0]), np.array([4.0, 6.0, 26.0])
    tgt = tgt_a * (1 - pan) + tgt_b * pan
    eye = eye_a * (1 - pan) + eye_b * pan
    door = g["door"]
    if push > 0:
        eye = eye * (1 - push) + (door + np.array([0, 0.0, 0.4])) * push
        tgt = tgt * (1 - push) + (door + np.array([0, 0, -8])) * push
    cam = h.Cam(eye, tgt, fov=46, near=0.05)
    fr = h.Frame(cam, fade=(10, 70))
    grid = [h.densify(np.array([[x, 0, -30], [x, 0, 30]]), 2.0) for x in range(-40, 31, 4)] + \
           [h.densify(np.array([[-40, 0, z], [30, 0, z]]), 2.0) for z in range(-30, 31, 4)]
    fr.lines(grid, MID, 0.8, 0.1, glow=0, tip=False)
    ks = ease(seg(t, ls(17) - 0.5, ls(17) + 2.8))
    pts = g["swarm0"] * (1 - ks) + g["swarm1"] * ks
    wob = 0.15 * np.sin(t * 3 + np.arange(len(pts)))[:, None]
    fr.points(pts + wob, SOFT, 1.5, 0.85)
    fr.points(g["swarm1"][:80] + wob[:80], TURQ, 1.8, 0.85 * ks)
    for k, (lab, off) in enumerate([("APPS", (-6, 8, 0)), ("AGENTS", (5, 10, -2)), ("STARTUPS", (-3, -1, 3))]):
        a = fr.anchor(np.array([-18, 4, -6]) + np.array(off))
        if a:
            tt = ls(17) + 2.4 + 0.45 * k
            fr.label(lambda cc, a=a, lab=lab, tt=tt: mg.decode(cc, lab, a[0], a[1], mg.font(mg.MONO_M, 18), SOFT, t, tt, dur=0.4, seed=len(lab), align="center"))
    ksh = ease(seg(t, ls(18) - 0.2, ls(18) + 1.6), "o")
    fr.lines(g["shop"], WHITE, 1.5, 0.95, glow=0.35, k=ksh, stagger=0.3, seed=2)
    fr.lines(g["sign"], TURQ, 1.4, 1.0, glow=0.9, k=ease(seg(t, ls(18) + 0.8, ls(18) + 2.0)), seed=3)
    fr.lines(g["lamp"], MID, 1.2, 0.7, glow=0.2, k=ksh, tip=False)
    fr.draw(c, 0.9, 0.4)
    # the 30% slice beside the shop (line 18)
    kp = ease(seg(t, ls(18) + 2.2, ls(18) + 3.2))
    a = fr.anchor(np.array([23.0, 2.4, 6.0]))
    if kp > 0 and a and push < 0.3:
        r = 58
        c.drawCircle(a[0], a[1], r, mg.stroke(MID, 1.2, 0.6 * kp))
        rect = skia.Rect.MakeXYWH(a[0] - r, a[1] - r, 2 * r, 2 * r)
        path = skia.Path(); path.addArc(rect, -90, 108 * kp)
        c.drawPath(path, mg.stroke(TURQ, 9, 0.95))
        h.mono(c, "30%", a[0], a[1] + 8, 22, WHITE, kp, align="center", font=mg.DISPLAY)
        h.mono(c, "TO THE APP", a[0], a[1] + r + 26, 13, SOFT, kp, align="center")
    fade = seg(t, le(19) + 0.1, le(19) + 0.6)
    if fade > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0E1013", fade))
    h.vignette(c, 0.55)


# ================================================================ close (lines 20-22)
def sc_close(c, t):
    t0 = B["close"][0]
    end_rail = le(21) + 0.4
    if t < end_rail + 0.6:
        tl = lerp(0.9, 9.7, seg(t, t0, end_rail))
        cl.frame_B(c, tl, dur=10.0)
    k = ease(seg(t, end_rail, end_rail + 0.8))
    if k > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0E1013", k))
        c.save()
        cam = h.orbit((0, 2.6, 0), 30, 30 + 10 * seg(t, end_rail, DUR), 22, fov=34)
        fr = h.Frame(cam, fade=(14, 60))
        if cl.CHIP is None:
            cl.CHIP = cl.chip_parts()
        for p in cl.CHIP:
            if "stack" in p:
                for s_ in p["stack"]:
                    fr.lines([q + np.array([0, s_["y"], 0]) for q in s_["polys"]], MID, 1.0, 0.6 * k, glow=0.2, tip=False)
            else:
                fr.lines(p["polys"], WHITE if p.get("accent") else MID, 1.2, 0.8 * k, glow=0.3, tip=False)
        c.translate(0, -120)
        fr.draw(c, 0.8, 0.3)
        c.restore()
        mg.decode(c, "SEE YOU ON THE CURVE", W / 2, 830, mg.font(mg.DISPLAY, 40), WHITE, t, ls(22) - 0.1, dur=0.6, seed=22, align="center")
        h.mono(c, "THE CURVE · PILOT · v7 LAB", W / 2, 880, 15, SOFT, k * 0.9, align="center")
        h.vignette(c, 0.55)


# ================================================================ overlays
def captions(c, t):
    for ln in L:
        if ln["start"] - 0.05 <= t <= ln["end"] + 0.35:
            words = ln["text"].split()
            wts = np.array([max(2, len(w.strip(".,?'")) ) + (3 if w.endswith((".", ",", "?")) else 0) for w in words], float)
            cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum()
            dur = ln["end"] - ln["start"]
            f = mg.font(mg.BODY_M, 34)
            total_w = sum(f.measureText(w + " ") for w in words)
            x = W / 2 - total_w / 2
            a = ease(seg(t, ln["start"] - 0.05, ln["start"] + 0.15)) * (1 - ease(seg(t, ln["end"] + 0.1, ln["end"] + 0.35)))
            bg = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 22, 968, total_w + 44, 56), 12, 12)
            c.drawRRect(bg, mg.fill("#0B0C0E", 0.55 * a))
            for k, w in enumerate(words):
                ws = ln["start"] + cum[k] * dur
                on = t >= ws
                col = TURQ if (on and t < ln["start"] + cum[k + 1] * dur + 0.05) else (WHITE if on else SOFT)
                c.drawString(w, x, 1006, f, mg.fill(col, a * (1.0 if on else 0.45)))
                x += f.measureText(w + " ")
            return


def cards(c, t):
    for ln in L:
        if not ln.get("card"):
            continue
        a = ease(seg(t, ln["start"] + 0.25, ln["start"] + 0.6)) * (1 - ease(seg(t, ln["end"] + 0.6, ln["end"] + 1.0)))
        if a <= 0:
            continue
        big, sub = ln["card"]
        if ln["scene"] in ("gold",) and big.startswith("$"):
            continue                                   # the gold scene draws its own counter
        fb = mg.font(mg.DISPLAY, 38 if len(big) < 12 else 28)
        fs = mg.font(mg.MONO, 14)
        wdt = max(fb.measureText(big), fs.measureText(sub)) + 56
        x, y = 96, 84
        slide = (1 - ease(seg(t, ln["start"] + 0.25, ln["start"] + 0.6), "o")) * 24
        mg.glass(c, x - slide, y, wdt, 110, 14, a)
        c.drawRect(skia.Rect.MakeXYWH(x - slide, y + 18, 3, 74), mg.fill(TURQ, a))
        c.drawString(big, x + 28 - slide, y + 58, fb, mg.fill(WHITE, a))
        c.drawString(sub, x + 28 - slide, y + 86, fs, mg.fill(SOFT, a))


SCENES = {"chip": sc_chip, "curve": sc_curve, "vortex": sc_vortex, "gold": sc_gold, "shop": sc_shop, "close": sc_close}
ORDER = ["chip", "curve", "vortex", "gold", "shop", "close"]


cl.FOOTER[0] = False


def frame(c, t):
    h.GRAIN[0] = False
    active = []
    for name in ORDER:
        a, b = B[name]
        if a - XF / 2 <= t <= b + XF / 2:
            active.append(name)
    for k, name in enumerate(active):
        a, b = B[name]
        if k == 0:
            SCENES[name](c, t)
        else:
            alpha = ease(seg(t, a - XF / 2, a + XF / 2))
            c.saveLayerAlpha(None, int(255 * alpha))
            SCENES[name](c, t)
            c.restore()
    cards(c, t)
    captions(c, t)
    h.GRAIN[0] = True
    h.grain(c, t)


def build_cues():
    """Sound cues tied to the picture (the mixer reads events.json). Sounds land 0-20 ms after motion."""
    CUES.clear()
    d = 0.012
    cue(0.2, "power_up", -8)
    for k in range(6):
        cue(0.35 + k * 0.28, "chatter", -16, -0.3 + 0.12 * k)
    t0, t1 = B["chip"]
    sc = (t1 + 0.6 - t0) / 10.0                      # clip A time -> pilot time
    for j, k0 in enumerate([0.0, 0.1, 0.25, 0.35, 0.55, 0.65]):
        cue(t0 + (1.6 + k0 * 2.4) * sc + d, "servo" if j % 2 else "hydraulic", -12, -0.2 + 0.08 * j)
        cue(t0 + (4.2 + k0 * 2.4) * sc + d, "latch", -11, 0.1)
    cue(t0 + 6.3 * sc + d, "form", -8)
    for j in range(7):
        cue(t0 + (5.0 + 0.16 * j) * sc + d, "tick_run", -20, 0.5)
    cue(B["curve"][0] - 0.2, "whoosh", -10)
    for dec in range(1960, 2021, 10):                # a gate whooshes past on every decade
        tt = None
        for q in np.linspace(B["curve"][0], B["curve"][1], 3000):
            if year_at(q) >= dec:
                tt = q
                break
        if tt:
            cue(tt + d, "whoosh", -17, 0.35)
    for ln in L:
        if ln.get("card") and not ln["card"][0].startswith("$"):
            cue(ln["start"] + 0.25 + d, "dock", -10, -0.6)
    cue(le(10) + 0.2, "riser", -14)
    cue(FALL_T0 - 0.56, "vortex", -3)                # inhale + hang + Shepard fall + landing thum
    cue(ls(12) - 0.2, "swell", -10)
    cue(ls(12) + 0.1, "form", -12)
    cue(ls(13), "chatter", -18)
    cue(ls(14) + 1.2, "latch", -9, 0.5)
    for k in range(9):
        cue(ls(15) + 0.1 + k * 0.18, "tick_run", -21, 0.0)
    cue(ls(15) + 1.8 + d, "thum", -12)
    cue(ls(16) + d, "dock", -9, -0.5)
    cue(ls(16) + 1.3 + d, "dock", -9, 0.5)
    cue(ls(17) - 0.4, "whoosh", -12)
    cue(ls(17) + 2.4, "chatter", -17, -0.4)
    cue(ls(18) + 0.1, "scan", -14, 0.4)
    cue(ls(18) + 0.8, "form", -12, 0.5)
    cue(ls(18) + 2.2, "servo", -13, 0.6)
    cue(ls(19) + 1.2, "riser", -17)
    cue(le(19) + 0.1, "sub_drop", -9)
    cue(B["close"][0], "whoosh", -12)
    for k, tt in enumerate([0.2, 2.6, 5.4]):         # each word of the rail forms
        cue(B["close"][0] + tt * (le(21) + 0.4 - B["close"][0]) / 9.7, "form", -12, [-0.4, 0.0, 0.4][k])
    cue(le(21) + 0.45, "latch", -8)
    cue(ls(22) - 0.1, "chatter", -15)
    cue(ls(22) + 0.5, "thum", -14)
    json.dump(dict(cues=CUES, sections=B, fall=FALL_T0, land=LAND, total=DUR), open(os.path.join(BUILD, "events.json"), "w"), indent=1)
    return CUES


if __name__ == "__main__":
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]:
            print(h.still(frame, float(tt), os.path.join(BUILD, f"still_{float(tt):05.1f}.png")))
    elif sys.argv[1] == "cues":
        print(len(build_cues()), "cues")
    else:
        build_cues()
        print(h.render(frame, DUR, os.path.join(BUILD, "pilot_silent.mp4")))
