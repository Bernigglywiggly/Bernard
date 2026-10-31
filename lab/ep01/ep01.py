"""EP01 · SIXTEEN HOURS: the visual timeline (9:16, 1080×1920), Six Floors format.

Persistent furniture (pollar's spine, upgraded):
  * the depth gauge (left edge): six floors, a marker that slides down as we go deeper and back up at the end
  * the time ruler (bottom): log scale from 1 second to 1 month; the horizon marker moves on every beat,
    year dots collect along it, and IMAGINE adds dotted "if" markers
  * fact cards (top) with sources; captions (lower third) with the active word in turquoise
Floors: GROUND (the task card, the flashback) · MECHANISM (228 task cards in 3D, the success curve, the 50% line,
the ladder) · YOU (two working days, three things) · IDEA (steps vs folds, the paper stack to the Moon) ·
IMAGINE (the drop through the ring tunnel into an ASCII dream, ghost cards, two questions) · SURFACE (tonight's
version, the mirrored close, sources).

    python3 ep01.py still 12 40 ...     # frames -> build/still_*.png
    python3 ep01.py render              # build/ep01_silent.mp4 + build/events.json
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(HERE, "..", "..", "a01_v6")
sys.path.insert(0, V6)
os.environ.setdefault("A01V6_FONTS", os.path.join(V6, "fonts"))
import mograph as mg  # noqa: E402

mg.W, mg.H = 1080, 1920                    # vertical: patch before holo reads the size
sys.path.insert(0, os.path.join(HERE, "..", "visual"))
import holo as h  # noqa: E402
import skia  # noqa: E402
from script import FLOORS, LADDER, SOURCES  # noqa: E402

W, H, FPS = h.W, h.H, h.FPS
_GROUNDS = {}


def _ground(kind="graphite"):
    """marl() assumes a width divisible by 16: build it 1088 wide and let the canvas crop it."""
    if kind not in _GROUNDS:
        mg.W = 1088
        try:
            _GROUNDS[kind] = mg.marl(mg.DARK if kind == "graphite" else mg.SLATE, 2 if kind == "graphite" else 3, 2.4)
        finally:
            mg.W = 1080
    return _GROUNDS[kind]


h.ground = _ground
TURQ, GLOW, WHITE, MID, SOFT = h.TURQ, h.GLOW, h.WHITE, h.MID, h.SOFT
ease, seg, clamp, lerp, smooth = h.ease, h.seg, h.clamp, h.lerp, h.smooth
BUILD = os.path.join(HERE, "build")
META = json.load(open(os.path.join(BUILD, "lines.json")))
L = META["lines"]
DUR = META["total"]


def ls(i):
    return L[i]["start"]


def le(i):
    return L[i]["end"]


def first_of_floor(f):
    return next(x for x in L if x["floor"] == f)


# floor windows (each floor begins a little before its first line)
F_START = [0.0] + [first_of_floor(f)["start"] - 0.9 for f in range(1, 6)]
DROP_LINE = next(i for i, x in enumerate(L) if x.get("drop"))
FALL_T0 = le(DROP_LINE - 1) + 1.0            # the Shepard fall starts here (vortex cue 0.56 s earlier)
LAND = FALL_T0 + 3.24
F_START[4] = ls(DROP_LINE - 1) - 0.9         # IMAGINE begins with "So imagine it keeps going."
CUES = []


def cue(t, name, gain=0.0, pan=0.0):
    CUES.append((round(t, 3), name, gain, pan))


def floor_at(t):
    f = 0
    for k in range(6):
        if t >= F_START[k]:
            f = k
    return f


# ================================================================ furniture
GX, GY0, GY1 = 58, 420, 1180                  # depth gauge


def gauge_y(k):
    """Floors 0-4 descend the gauge; SURFACE (5) sits above GROUND, so the last move is a climb."""
    return GY0 - 120 if k == 5 else lerp(GY0, GY1, k / 4)


def gauge(c, t):
    c.drawLine(GX, GY0 - 150, GX, GY1 + 30, mg.stroke(MID, 1.2, 0.35))
    y = gauge_y(0)
    for k in range(1, 6):
        y = lerp(y, gauge_y(k), smooth(seg(t, F_START[k] - 0.2, F_START[k] + (2.2 if k == 5 else 0.9))))
    f = floor_at(t)
    for k in range(6):
        yy = gauge_y(k)
        on = (k == f)
        c.drawLine(GX - 8, yy, GX + 8, yy, mg.stroke(TURQ if on else MID, 1.4, 0.95 if on else 0.4))
        h.mono(c, str(k), GX - 30, yy + 5, 13, TURQ if on else SOFT, 0.9 if on else 0.45)
    c.drawCircle(GX, y, 7, mg.fill(TURQ, 1.0))
    c.drawCircle(GX, y, 14, mg.stroke(GLOW, 1.2, 0.5))
    a = ease(seg(t, F_START[f], F_START[f] + 0.6))
    mg.decode(c, FLOORS[f], GX + 22, y + 6, mg.font(mg.MONO_M, 15), TURQ, t, F_START[f], dur=0.5, seed=f + 3, align="left", a=0.95 * max(a, 0.35))


RX0, RX1, RY = 96, 900, 1488                  # time ruler (log seconds)
R_MIN, R_MAX = 0.0, math.log10(30 * 86400)
TICKS = [(1, "1S"), (60, "1M"), (3600, "1H"), (86400, "1D"), (7 * 86400, "1W"), (30 * 86400, "1MO")]


def rx(seconds):
    return lerp(RX0, RX1, (math.log10(max(seconds, 1.0)) - R_MIN) / (R_MAX - R_MIN))


def horizon_at(t):
    """Where the horizon marker sits (seconds), from the lines' `mark` fields, gliding between them;
    during the ladder line it steps through the ladder rungs in time with the words."""
    lad = next((x for x in L if x.get("ladder")), None)
    if lad and lad["start"] <= t <= lad["end"] + 0.6:
        n = len(LADDER)
        prev = LADDER[0][1]
        val = prev
        for k, (yr, s_, lab) in enumerate(LADDER):
            tk = lad["start"] + (lad["end"] - lad["start"]) * k / n
            if t >= tk:
                kk = smooth(seg(t, tk, tk + 0.45))
                val = 10 ** lerp(math.log10(prev), math.log10(s_), kk)
                prev = s_
        return val
    val, t_prev = None, -1
    keys = [(x["start"] + 0.3, x["mark"]) for x in L if x.get("mark")]
    cur = 16 * 3600.0
    for tk, m in keys:
        m = abs(m) if m > 0 else cur
        if t >= tk:
            prev = cur
            cur = m
            k = smooth(seg(t, tk, tk + 1.2))
            val = 10 ** lerp(math.log10(prev), math.log10(cur), k)
    return val if val is not None else 16 * 3600.0


def ruler(c, t):
    a = ease(seg(t, ls(0) - 0.4, ls(0) + 0.6))
    if a <= 0:
        return
    c.drawLine(RX0, RY, RX1, RY, mg.stroke(MID, 1.3, 0.6 * a))
    for s, lab in TICKS:
        x = rx(s)
        c.drawLine(x, RY - 9, x, RY + 9, mg.stroke(MID, 1.2, 0.7 * a))
        h.mono(c, lab, x, RY + 34, 14, SOFT, 0.85 * a, align="center")
    h.mono(c, "TIME HORIZON · LOG SCALE", RX0, RY - 26, 12, SOFT, 0.7 * a)
    # ladder dots collected so far
    lad = next((x for x in L if x.get("ladder")), None)
    if lad:
        for k, (yr, s, lab) in enumerate(LADDER):
            tk = lad["start"] + (lad["end"] - lad["start"]) * k / len(LADDER)
            ka = ease(seg(t, tk, tk + 0.25), "o")
            if ka > 0:
                x = rx(s)
                c.drawCircle(x, RY, 5 * ka, mg.fill(WHITE if yr < 2026 else TURQ, a))
                h.mono(c, str(yr), x, RY - 46 - (k % 2) * 16, 12, WHITE if yr < 2026 else TURQ, 0.85 * a * ka, align="center")
    # IMAGINE: dotted "if" markers
    ki = ease(seg(t, ls(DROP_LINE + 1) + 0.4, ls(DROP_LINE + 1) + 1.4))
    if ki > 0 and t < F_START[5] + 1.5:
        ko = 1 - ease(seg(t, F_START[5], F_START[5] + 1.2))
        for s, lab in ((40 * 3600, "1 WORK WEEK · IF"), (160 * 3600, "1 WORK MONTH · IF")):
            x = rx(s)
            p = mg.stroke(GLOW, 1.4, ki * ko)
            p.setPathEffect(skia.DashPathEffect.Make([5, 6], 0))
            c.drawLine(x, RY - 60, x, RY + 10, p)
            h.mono(c, lab, x, RY - 70, 12, GLOW, ki * ko, align="center")
    # the horizon marker
    hv = horizon_at(t)
    x = rx(hv)
    path = skia.Path(); path.moveTo(x, RY - 4); path.lineTo(x - 9, RY - 20); path.lineTo(x + 9, RY - 20); path.close()
    c.drawPath(path, mg.fill(TURQ, a))
    c.drawLine(x, RY - 4, x, RY + 14, mg.stroke(TURQ, 2.0, a))
    lab = f"{hv:0.0f} S" if hv < 60 else (f"{hv / 60:0.0f} MIN" if hv < 3600 else f"{hv / 3600:0.0f} H")
    h.mono(c, lab, x, RY + 62, 16, TURQ, a, align="center", font=mg.MONO_M)


def card(c, t):
    for x in L:
        if not x.get("card"):
            continue
        a = ease(seg(t, x["start"] + 0.2, x["start"] + 0.55)) * (1 - ease(seg(t, x["end"] + 1.0, x["end"] + 1.4)))
        if a <= 0:
            continue
        big, sub = x["card"]
        fb = mg.font(mg.DISPLAY, 46 if len(big) < 11 else 36)
        fs = mg.font(mg.MONO, 15)
        wdt = max(fb.measureText(big), fs.measureText(sub)) + 60
        cx, cy = 118, 170
        slide = (1 - ease(seg(t, x["start"] + 0.2, x["start"] + 0.55), "o")) * 26
        mg.glass(c, cx - slide, cy, wdt, 124, 16, a)
        c.drawRect(skia.Rect.MakeXYWH(cx - slide, cy + 20, 3, 84), mg.fill(TURQ, a))
        c.drawString(big, cx + 30 - slide, cy + 66, fb, mg.fill(WHITE, a))
        c.drawString(sub, cx + 30 - slide, cy + 98, fs, mg.fill(SOFT, a))


def captions(c, t):
    for ln in L:
        if ln["start"] - 0.05 <= t <= ln["end"] + 0.3:
            words = ln["text"].split()
            f = mg.font(mg.BODY_M, 42)
            maxw = 840
            lines, cur = [], []
            for w in words:
                test = " ".join(cur + [w])
                if f.measureText(test) > maxw and cur:
                    lines.append(cur); cur = [w]
                else:
                    cur.append(w)
            lines.append(cur)
            wts = np.array([max(2, len(w.strip(".,?:'"))) + (3 if w.endswith((".", ",", "?", ":")) else 0) for w in words], float)
            cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum()
            dur = ln["end"] - ln["start"]
            a = ease(seg(t, ln["start"] - 0.05, ln["start"] + 0.15)) * (1 - ease(seg(t, ln["end"] + 0.08, ln["end"] + 0.3)))
            y0 = 1300 - (len(lines) - 1) * 26
            k = 0
            for li, lw in enumerate(lines):
                tw = f.measureText(" ".join(lw))
                x = 500 - tw / 2
                y = y0 + li * 54
                for w in lw:
                    ws = ln["start"] + cum[k] * dur
                    we = ln["start"] + cum[k + 1] * dur
                    on = t >= ws
                    col = TURQ if (on and t < we + 0.05) else (WHITE if on else SOFT)
                    c.drawString(w, x, y, f, mg.fill(col, a * (1.0 if on else 0.4)))
                    x += f.measureText(w + " ")
                    k += 1
            return


# ================================================================ floor 0 · GROUND
def task_card(c, t, cx, cy, scale, a, hours_on, label="TASK", sub="HUMAN EXPERT TIME"):
    """A document-like task card with a 4×4 grid of hour cells."""
    w, hh = 560 * scale, 420 * scale
    x, y = cx - w / 2, cy - hh / 2
    mg.glass(c, x, y, w, hh, 22 * scale, a)
    h.mono(c, label, x + 34 * scale, y + 56 * scale, 18 * scale, TURQ, a, font=mg.MONO_M)
    h.mono(c, sub, x + w - 34 * scale, y + 56 * scale, 14 * scale, SOFT, a, align="right")
    cell, gap = 62 * scale, 12 * scale
    gx = cx - (4 * cell + 3 * gap) / 2
    gy = y + 96 * scale
    for i in range(16):
        r, q = divmod(i, 4)
        rr = skia.Rect.MakeXYWH(gx + q * (cell + gap), gy + r * (cell + gap), cell, cell)
        k = clamp(hours_on - i)
        c.drawRoundRect(rr, 6 * scale, 6 * scale, mg.stroke(MID, 1.2, 0.5 * a))
        if k > 0:
            p = mg.fill(TURQ, a * (0.35 + 0.65 * k))
            c.drawRoundRect(rr.makeInset(3 * scale, 3 * scale) if hasattr(rr, "makeInset") else rr, 5 * scale, 5 * scale, p)
    big = f"{min(16, int(hours_on + 0.001))}"
    c.drawString(big, x + w - 150 * scale, y + hh - 40 * scale, mg.font(mg.DISPLAY, 64 * scale), mg.fill(WHITE, a))
    h.mono(c, "HOURS", x + w - 40 * scale, y + hh - 40 * scale, 14 * scale, SOFT, a, align="right")


def half_ring(c, cx, cy, r, k, a, label="50%", sub="SUCCESS RATE"):
    c.drawCircle(cx, cy, r, mg.stroke(MID, 2, 0.5 * a))
    rect = skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r)
    p = skia.Path(); p.addArc(rect, -90, 180 * k)
    c.drawPath(p, mg.stroke(TURQ, 12, a))
    h.mono(c, label, cx, cy + 14, 40, WHITE, a, align="center", font=mg.DISPLAY)
    h.mono(c, sub, cx, cy + r + 40, 14, SOFT, a, align="center")


def fl_ground(c, t):
    c.drawImage(h.ground("graphite"), 0, 0)
    a_in = ease(seg(t, 0.2, 1.2))
    hours = 16 * ease(seg(t, ls(0) + 0.3, le(0) - 0.2), "io")
    shrink = smooth(seg(t, ls(2) + 0.2, ls(2) + 1.8))
    cy = lerp(740, 640, smooth(seg(t, ls(1), ls(1) + 1.0)))
    task_card(c, t, lerp(540, 540, shrink), lerp(cy, 560, shrink), lerp(1.3, 0.55, shrink), a_in * (1 - 0.6 * shrink), hours * (1 - shrink) + 0.5 * shrink)
    kr = ease(seg(t, ls(1) + 1.2, ls(1) + 2.4))
    if kr > 0:
        half_ring(c, 540, 1080 - 60 * shrink, 110, kr, kr * (1 - shrink))
    # the flashback: 2019 · 2 SEC stamped big
    kf = ease(seg(t, ls(2) + 0.8, ls(2) + 1.6), "o")
    if kf > 0:
        mg.decode(c, "2019", 540, 900, mg.font(mg.DISPLAY, 120), WHITE, t, ls(2) + 0.8, dur=0.6, seed=19, align="center", a=kf)
        h.mono(c, "TWO SECONDS OF YOUR TIME", 540, 960, 18, TURQ, kf, align="center", font=mg.MONO_M)
    h.vignette(c, 0.5)


# ================================================================ floor 1 · MECHANISM
TASKS = None


def task_field():
    global TASKS
    if TASKS is None:
        rng = np.random.default_rng(228)
        n = 228
        logt = np.clip(rng.normal(3.0, 1.35, n), 0.2, 5.4)          # log10 seconds: seconds to ~3 days
        order = np.argsort(logt)
        cats = rng.integers(0, 3, n)
        # stack cards into columns by duration bucket (a 3D histogram)
        bucket = np.floor((logt - 0.2) / 0.25).astype(int)
        height = np.zeros(n)
        cnt = {}
        for i in order:
            b = bucket[i]
            height[i] = cnt.get(b, 0)
            cnt[b] = cnt.get(b, 0) + 1
        # success probability falls with length (logistic around the 16 h horizon for the 2026 model)
        p = 1 / (1 + np.exp((logt - math.log10(16 * 3600)) * 2.2))
        success = rng.random(n) < p
        TASKS = dict(logt=logt, bucket=bucket, height=height, cats=cats, success=success, n=n)
    return TASKS


def tx(logt):
    return (logt - 2.8) * 5.2                                          # 3D x for a log10-seconds value


def fl_mechanism(c, t):
    tf = task_field()
    c.drawImage(h.ground("slate"), 0, 0)
    t0 = F_START[1]
    k = smooth(seg(t, t0, ls(8)))
    cam = h.Cam((lerp(-9, 6, k), lerp(10, 14, k), lerp(27, 23, k)), (lerp(-2, 3, k), 0.2, 0), fov=54)
    fr = h.Frame(cam, fade=(12, 60))
    # axis on the floor, seconds -> days
    axis = h.densify(np.array([[tx(0), 0, 2.5], [tx(5.5), 0, 2.5]]), 0.5)
    fr.lines([axis], MID, 1.4, 0.8 * ease(seg(t, ls(4), ls(4) + 0.8)), glow=0, tip=False)
    for lt, lab in ((0, "1 SEC"), (math.log10(60), "1 MIN"), (math.log10(3600), "1 HOUR"), (math.log10(86400), "1 DAY")):
        p0 = np.array([tx(lt), 0, 2.5])
        fr.lines([np.array([p0, p0 + [0, 0, 0.6]])], MID, 1.2, 0.8, glow=0, tip=False)
        an = fr.anchor(p0 + [0, 0, 1.2])
        if an:
            fr.label(lambda cc, an=an, lab=lab: h.mono(cc, lab, an[0], an[1] + 10, 15, SOFT, 0.9, align="center"))
    # the cards: arrive (line 4), categories light (line 5), results flip (line 6)
    arrive = seg(t, ls(4) + 0.2, ls(4) + 3.2)
    flip = seg(t, ls(6) + 0.8, ls(6) + 4.5)
    catlab = seg(t, ls(5), le(5))
    polys_w, polys_t, polys_d = [], [], []
    for i in range(tf["n"]):
        ki = clamp(arrive * 1.6 - (tf["logt"][i] / 5.4) * 0.6)
        if ki <= 0:
            continue
        x = tx(tf["logt"][i]) + (tf["bucket"][i] % 2) * 0.12
        y = 0.25 + tf["height"][i] * 0.34
        z = -0.4 * tf["cats"][i]
        y = y + (1 - smooth(ki)) * 6.0
        rect = np.array([[x - 0.55, y, z], [x + 0.55, y, z], [x + 0.55, y + 0.26, z], [x - 0.55, y + 0.26, z], [x - 0.55, y, z]])
        fk = clamp(flip * 1.4 - (tf["logt"][i] / 5.4) * 0.4)
        if fk > 0.5:
            (polys_t if tf["success"][i] else polys_d).append(rect)
        else:
            polys_w.append(rect)
    fr.lines(polys_w, WHITE, 1.1, 0.75, glow=0.15, tip=False)
    fr.lines(polys_t, TURQ, 1.3, 0.95, glow=0.7, tip=False)
    fr.lines(polys_d, MID, 1.0, 0.35, glow=0, tip=False)
    # the success curve and the 50% line
    kc = ease(seg(t, ls(6) + 2.2, ls(6) + 5.0))
    if kc > 0:
        lt = np.linspace(0, 5.5, 120)
        pr = 1 / (1 + np.exp((lt - math.log10(16 * 3600)) * 2.2))
        curve = np.stack([tx(lt), 0.4 + pr * 7.0, np.full_like(lt, 0.6)], 1)
        fr.lines([curve], GLOW, 2.2, 1.0, glow=1.1, k=kc)
        half = np.array([[tx(0), 0.4 + 3.5, 0.6], [tx(5.5), 0.4 + 3.5, 0.6]])
        p50 = mg.stroke(MID, 1.2, 0.8)
        fr.lines([h.densify(half, 0.3)], SOFT, 1.1, 0.7 * kc, glow=0, tip=False)
        an = fr.anchor(half[0])
        if an:
            fr.label(lambda cc, an=an, kc=kc: h.mono(cc, "50% SUCCESS", an[0] - 6, an[1] - 12, 15, SOFT, kc))
    kh = ease(seg(t, ls(7) - 0.2, ls(7) + 0.8))
    if kh > 0:
        xh = tx(math.log10(16 * 3600))
        drop = np.array([[xh, 0.4 + 3.5, 0.6], [xh, 0.0, 0.6]])
        fr.lines([h.densify(drop, 0.2)], TURQ, 2.4, 1.0, glow=1.2, k=kh)
        an = fr.anchor(np.array([xh, 0.4 + 3.5, 0.6]))
        if an:
            fr.label(lambda cc, an=an: mg.decode(cc, "TIME HORIZON", an[0] + 18, an[1] - 18, mg.font(mg.MONO_M, 24), TURQ, t, ls(7), dur=0.5, seed=7, align="left"))
    fr.draw(c, 0.9, 0.4)
    # category labels (line 5)
    if catlab > 0:
        for j, lab in enumerate(["CODING", "RESEARCH", "FIXING SYSTEMS"]):
            kk = ease(seg(t, ls(5) + j * 0.7, ls(5) + j * 0.7 + 0.4))
            mg.decode(c, lab, 150, 390 + j * 40, mg.font(mg.MONO_M, 20), WHITE if j != 2 else TURQ, t, ls(5) + j * 0.7, dur=0.35, seed=j + 30, align="left", a=kk * (1 - ease(seg(t, ls(6) + 0.5, ls(6) + 1.2))))
    # the ladder (line 8): five cards stack on the right
    lad = next(i for i, x in enumerate(L) if x.get("ladder"))
    for k2, (yr, s, lab) in enumerate(LADDER):
        tk = ls(lad) + (le(lad) - ls(lad)) * k2 / len(LADDER)
        ka = ease(seg(t, tk, tk + 0.3), "o")
        if ka <= 0:
            continue
        y = 1120 - k2 * 118
        x = 600
        mg.glass(c, x + (1 - ka) * 40, y, 330, 96, 14, ka)
        h.mono(c, str(yr), x + 24 + (1 - ka) * 40, y + 40, 16, SOFT, ka)
        c.drawString(lab, x + 24 + (1 - ka) * 40, y + 78, mg.font(mg.DISPLAY, 30), mg.fill(TURQ if yr == 2026 else WHITE, ka))
    h.vignette(c, 0.5)


# ================================================================ floor 2 · YOU
def icon(c, name, cx, cy, s, a, col=WHITE):
    p = mg.stroke(col, 2.4, a)
    if name == "essay":
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - 34 * s, cy - 44 * s, 68 * s, 88 * s), 6, 6, p)
        for k in range(5):
            c.drawLine(cx - 22 * s, cy - 24 * s + k * 14 * s, cx + (22 - (k == 4) * 16) * s, cy - 24 * s + k * 14 * s, p)
    elif name == "shop":
        c.drawRect(skia.Rect.MakeXYWH(cx - 44 * s, cy - 16 * s, 88 * s, 56 * s), p)
        c.drawLine(cx - 52 * s, cy - 16 * s, cx + 52 * s, cy - 16 * s, p)
        for k in range(6):
            c.drawLine(cx - 50 * s + k * 20 * s, cy - 16 * s, cx - 44 * s + k * 20 * s, cy - 36 * s, p)
        c.drawRect(skia.Rect.MakeXYWH(cx - 12 * s, cy + 4 * s, 24 * s, 36 * s), p)
    elif name == "pad":
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - 56 * s, cy - 26 * s, 112 * s, 52 * s), 24 * s, 24 * s, p)
        c.drawLine(cx - 34 * s, cy, cx - 16 * s, cy, p); c.drawLine(cx - 25 * s, cy - 9 * s, cx - 25 * s, cy + 9 * s, p)
        c.drawCircle(cx + 24 * s, cy - 6 * s, 5 * s, p); c.drawCircle(cx + 34 * s, cy + 6 * s, 5 * s, p)


def fl_you(c, t):
    c.drawImage(h.ground("slate"), 0, 0)
    L9 = first_of_floor(2)["i"]
    kd = ease(seg(t, ls(L9) + 0.1, ls(L9) + 1.2))
    for d in range(2):                                   # two working days, eight hour-cells each
        y = 520 + d * 170
        h.mono(c, f"DAY {d + 1}", 150, y + 40, 16, SOFT, kd)
        for q in range(8):
            kk = clamp((kd * 16) - (d * 8 + q))
            r = skia.Rect.MakeXYWH(260 + q * 78, y, 66, 66)
            c.drawRoundRect(r, 8, 8, mg.stroke(MID, 1.2, 0.5 * kd))
            if kk > 0:
                c.drawRoundRect(r, 8, 8, mg.fill(TURQ, 0.4 + 0.6 * kk))
    for j, (nm, lab) in enumerate([("essay", "COURSEWORK ESSAY"), ("shop", "A TAKEAWAY'S WEBSITE"), ("pad", "THE MOD YOU NEVER FINISHED")]):
        tk = ls(L9 + 1) + j * 1.9
        ka = ease(seg(t, tk, tk + 0.45), "o")
        if ka <= 0:
            continue
        y = 900 + j * 132
        mg.glass(c, 150 + (1 - ka) * 50, y, 740, 112, 16, ka)
        icon(c, nm, 230 + (1 - ka) * 50, y + 56, 0.8, ka, TURQ)
        c.drawString(lab, 320 + (1 - ka) * 50, y + 66, mg.font(mg.BODY_M, 30), mg.fill(WHITE, ka))
    h.vignette(c, 0.5)


# ================================================================ floor 3 · IDEA
def fl_idea(c, t):
    L11 = first_of_floor(3)["i"]
    c.drawImage(h.ground("graphite"), 0, 0)
    # steps vs folds (line 12)
    ks = ease(seg(t, ls(L11 + 1), ls(L11 + 1) + 1.6))
    fade_sf = 1 - ease(seg(t, ls(L11 + 2) - 0.3, ls(L11 + 2) + 0.4))
    if ks > 0 and fade_sf > 0:
        a = ks * fade_sf
        h.mono(c, "STEPS", 280, 440, 18, SOFT, a, align="center", font=mg.MONO_M)
        h.mono(c, "FOLDS", 800, 440, 18, TURQ, a, align="center", font=mg.MONO_M)
        path = skia.Path(); path.moveTo(120, 1100)
        for k in range(8):
            path.lineTo(120 + (k + 1) * 45, 1100 - k * 60); path.lineTo(120 + (k + 1) * 45, 1100 - (k + 1) * 60)
        c.drawPath(path, mg.stroke(WHITE, 2.4, a))
        pts = skia.Path(); pts.moveTo(640, 1100)
        for q in range(60):
            x = 640 + q * 5.5
            y = 1100 - 1.45 ** (q / 6) * 12
            pts.lineTo(x, max(470, y))
        c.drawPath(pts, mg.stroke(TURQ, 3.0, a))
    # the paper stack to the Moon (line 13): a powers-of-ten zoom-out; the stack stays the same size on
    # screen while the world's landmarks slide down past it
    kp = seg(t, ls(L11 + 2) - 0.2, le(L11 + 2) + 1.0)
    if kp > 0:
        a = ease(seg(t, ls(L11 + 2) - 0.2, ls(L11 + 2) + 0.4)) * (1 - ease(seg(t, ls(L11 + 3) + 0.6, ls(L11 + 3) + 1.4)))
        nf = 42 * ease(kp, "io")
        folds = int(nf + 0.5)
        top_m = 1e-4 * 2 ** nf                                   # stack height in metres (continuous)
        gy, ty = 1180, 470                                        # ground and top of the stack on screen
        span = 4.0                                                # decades visible below the top
        lo = math.log10(top_m) - span
        def ymap(metres):
            return gy - (math.log10(metres) - lo) / span * (gy - ty)
        c.drawLine(540, gy, 540, ty, mg.stroke(TURQ, 3.0, a))
        glow = mg.stroke(GLOW, 9.0, 0.25 * a); glow.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
        c.drawLine(540, gy, 540, ty, glow)
        c.drawLine(470, ty, 610, ty, mg.stroke(WHITE, 2.0, a))
        for dec in range(-4, 10):                                 # decade ticks slide as we zoom out
            yy = ymap(10 ** dec)
            if ty <= yy <= gy:
                c.drawLine(520, yy, 560, yy, mg.stroke(MID, 1.0, 0.5 * a))
        for nfold, lab, metres in ((0, "A SHEET · 0.1 MM", 1e-4), (7, "A BOOK · 1.3 CM", 0.0128), (14, "A PERSON · 1.6 M", 1.64),
                                   (19, "A TOWER BLOCK · 52 M", 52.4), (27, "PAST EVEREST · 13 KM", 13400.0),
                                   (32, "THE SPACE STATION · 430 KM", 429000.0), (42, "THE MOON · 440,000 KM", 4.398e8)):
            if nf + 0.3 < nfold:
                continue
            yy = ymap(metres)
            if yy < ty - 2 or yy > gy + 4:
                continue
            la = a * clamp((nf + 0.3 - nfold) / 0.6)
            col = TURQ if nfold == 42 else WHITE
            c.drawLine(600, yy, 660, yy, mg.stroke(col, 1.4, la))
            h.mono(c, lab, 672, yy + 6, 17, col, la, font=mg.MONO_M)
            h.mono(c, f"FOLD {nfold}", 470, yy + 6, 14, SOFT, la, align="right")
        h.mono(c, f"FOLD {folds:02d}", 150, 460, 20, WHITE, a, font=mg.MONO_M)
        km = 1e-7 * 2 ** folds
        txt = f"{km:,.0f} KM" if km >= 1 else (f"{km * 1e6:,.1f} MM" if km < 0.001 else f"{km * 1000:,.1f} M")
        c.drawString(txt, 150, 540, mg.font(mg.DISPLAY, 52), mg.fill(TURQ if folds >= 42 else WHITE, a))
    # doubling (line 14)
    kd = ease(seg(t, ls(L11 + 3), ls(L11 + 3) + 1.0))
    if kd > 0:
        for j, (lab, mo) in enumerate([("2019 → 2024", "×2 EVERY ~7 MONTHS"), ("SINCE 2024", "×2 EVERY ~4 MONTHS")]):
            kk = ease(seg(t, ls(L11 + 3) + j * 2.6, ls(L11 + 3) + j * 2.6 + 0.5), "o")
            y = 760 + j * 170
            mg.glass(c, 150 + (1 - kk) * 40, y, 780, 130, 16, kk)
            h.mono(c, lab, 184 + (1 - kk) * 40, y + 44, 16, SOFT, kk)
            c.drawString(mo, 184 + (1 - kk) * 40, y + 96, mg.font(mg.DISPLAY, 30), mg.fill(TURQ if j else WHITE, kk))
    h.vignette(c, 0.5)


# ================================================================ floor 4 · IMAGINE
ASC = None


def dream_field(t, cols=90, rows=160):
    """A slow 3D noise field shaded into characters: the dream layer."""
    yy, xx = np.mgrid[0:rows, 0:cols]
    u, v = xx / cols, yy / rows
    f = (np.sin(u * 7.0 + t * 0.35) * np.cos(v * 5.0 - t * 0.22) + np.sin((u + v) * 11.0 - t * 0.5) * 0.5
         + np.sin(np.hypot(u - 0.5, v - 0.45) * 22.0 - t * 1.1) * 0.35)
    f = (f - f.min()) / (f.max() - f.min() + 1e-9)
    vign = np.clip(1.2 - 1.6 * np.hypot(u - 0.5, (v - 0.45) * 0.7), 0, 1)
    return (f ** 1.8) * vign


def fl_imagine(c, t):
    global ASC
    c.drawImage(h.ground("graphite"), 0, 0)
    if t < FALL_T0:
        # "So imagine it keeps going." The gauge has dropped; the world holds its breath (the hang).
        k = seg(t, F_START[4], FALL_T0)
        cam = h.Cam((0, 22, 0.001), (0, 0, 0), fov=64, up=(0, 0, -1))
        fr = h.Frame(cam, fade=(4, 60))
        rings = []
        for n in range(16):
            y = -n * 2.4
            segs = 6 + (n % 3) * 2
            rot = (n % 2 * 2 - 1) * t * 0.6 + n * 0.3
            for q in range(segs):
                a0 = rot + q * 2 * math.pi / segs
                rings.append(h.circle((0, y, 0), 6.0, 12, "y", a0, a0 + 2 * math.pi / segs * 0.7))
        fr.lines(rings, TURQ, 1.6, 0.9 * ease(seg(t, F_START[4], F_START[4] + 1.5)), glow=0.9, tip=False)
        fr.draw(c, 1.0, 0.5)
        hang = seg(t, le(DROP_LINE - 1) + 0.35, FALL_T0)
        if hang > 0:
            c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0B0C0E", 0.4 * hang))
        return
    if t < LAND + 0.1:                                            # the fall
        kf = seg(t, FALL_T0, LAND)
        depth = 210 * kf ** 1.7
        cam = h.Cam((0, -depth, 0), (0, -depth - 10, 0.0001), fov=lerp(78, 104, kf), roll=kf * 2.6, up=(0, 0, 1))
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
        fr.lines(rings, TURQ, 1.6, 1.0, glow=0.9, tip=False)
        fr.draw(c, 1.0, 0.6)
        return
    # the dream layer: characters drifting, the camera free
    if ASC is None:
        ASC = h.Ascii(cols=90, rows=160)
    kin = ease(seg(t, LAND, LAND + 1.4))
    kout = 1 - ease(seg(t, F_START[5] - 0.2, F_START[5] + 1.4))
    lum = dream_field(t) * kin * kout
    img = ASC.compose(lum * 0.85)
    sk = skia.Image.fromarray(img, colorType=skia.ColorType.kRGBA_8888_ColorType)
    c.drawImage(sk, 0, 0)
    gp = skia.Paint(BlendMode=skia.BlendMode.kPlus); gp.setImageFilter(skia.ImageFilters.Blur(8, 8)); gp.setAlphaf(0.45)
    c.drawImage(sk, 0, 0, skia.SamplingOptions(), gp)
    c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0B0C0E", 0.35))
    stamp = ease(seg(t, LAND + 0.4, LAND + 1.0)) * kout
    if stamp > 0:
        r = skia.Rect.MakeXYWH(300, 350, 480, 64)
        p = mg.stroke(GLOW, 1.6, stamp); p.setPathEffect(skia.DashPathEffect.Make([7, 6], 0))
        c.drawRoundRect(r, 10, 10, p)
        h.mono(c, "IMAGINE · NOT A FORECAST", 540, 392, 20, GLOW, stamp, align="center", font=mg.MONO_M)
    # ghost cards drift through (line: the book, the business, the cure)
    Lg = DROP_LINE + 3
    ghosts = [("THE FIRST DRAFT", "OF THE BOOK"), ("THE FIRST VERSION", "OF THE BUSINESS"), ("THE WHOLE SEARCH", "FOR THE CURE")]
    for j, (a1, a2) in enumerate(ghosts):
        tk = ls(Lg) + j * 2.1
        kk = seg(t, tk, tk + 5.5)
        if 0 < kk < 1:
            a = math.sin(math.pi * kk) * kout
            y = lerp(1180, 560, kk) + j * 20
            x = [300, 720, 460][j]
            p = mg.stroke(GLOW, 1.4, 0.8 * a); p.setPathEffect(skia.DashPathEffect.Make([4, 5], 0))
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 210, y - 70, 420, 140), 16, 16, p)
            h.mono(c, a1, x, y - 6, 22, WHITE, a, align="center", font=mg.MONO_M)
            h.mono(c, a2, x, y + 28, 18, GLOW, a, align="center")
    # 1 MONTH ghost (line: imagine handing over a month)
    km = ease(seg(t, ls(DROP_LINE + 2), ls(DROP_LINE + 2) + 0.8)) * (1 - ease(seg(t, ls(Lg) - 0.3, ls(Lg) + 0.5)))
    if km > 0:
        c.drawString("1 MONTH", 540 - mg.font(mg.DISPLAY, 96).measureText("1 MONTH") / 2, 820, mg.font(mg.DISPLAY, 96), mg.fill(WHITE, km * kout))
        h.mono(c, "HANDED OVER · IF THE TREND HELD", 540, 880, 18, GLOW, km * kout, align="center")
    # the two questions
    for j, (qq, col) in enumerate([("WHAT WOULD YOU GIVE IT?", WHITE), ("WHAT WOULD YOU KEEP?", TURQ)]):
        li = Lg + 1 + j
        kq = ease(seg(t, ls(li), ls(li) + 0.6)) * kout
        if kq > 0:
            f = mg.font(mg.DISPLAY, 44)
            c.drawString(qq, 540 - f.measureText(qq) / 2, 760 + j * 110, f, mg.fill(col, kq))
    h.vignette(c, 0.55)


# ================================================================ floor 5 · SURFACE
def fl_surface(c, t):
    c.drawImage(h.ground("graphite"), 0, 0)
    L21 = first_of_floor(5)["i"]
    ka = ease(seg(t, ls(L21) + 0.3, ls(L21) + 1.2)) * (1 - ease(seg(t, ls(L21 + 1) - 0.6, ls(L21 + 1))))
    if ka > 0:
        mg.glass(c, 150, 520, 780, 420, 20, ka)
        h.mono(c, "TONIGHT'S VERSION", 190, 580, 18, TURQ, ka, font=mg.MONO_M)
        for j, s in enumerate(["1 · PICK ONE TASK THAT EATS YOUR WEEK", "2 · CUT IT INTO PIECES", "3 · HAND THE PIECES OVER BEFORE BED"]):
            kk = ease(seg(t, ls(L21) + 1.2 + j * 1.8, ls(L21) + 1.7 + j * 1.8))
            c.drawString(s, 190, 670 + j * 90, mg.font(mg.BODY_M, 30), mg.fill(WHITE, ka * kk))
    # the mirrored close
    for j, (l1, l2, sub, col) in enumerate([("2 SEC", "1 HOUR", "6 YEARS", WHITE), ("1 HOUR", "16 HOURS", "1 YEAR", TURQ)]):
        li = L21 + 1 + j
        kk = ease(seg(t, ls(li) + 0.1, ls(li) + 0.7))
        if kk > 0:
            y = 640 + j * 230
            f = mg.font(mg.DISPLAY, 50)
            w1, w2, gap = f.measureText(l1), f.measureText(l2), 90
            x0 = 540 - (w1 + gap + w2) / 2
            c.drawString(l1, x0, y, f, mg.fill(col, kk))
            ax = x0 + w1 + 18
            c.drawLine(ax, y - 18, ax + gap - 36, y - 18, mg.stroke(col, 3.0, kk))
            hp = skia.Path(); hp.moveTo(ax + gap - 30, y - 18); hp.lineTo(ax + gap - 44, y - 27); hp.lineTo(ax + gap - 44, y - 9); hp.close()
            c.drawPath(hp, mg.fill(col, kk))
            c.drawString(l2, x0 + w1 + gap, y, f, mg.fill(col, kk))
            h.mono(c, sub, 540, y + 60, 22, SOFT if j == 0 else GLOW, kk, align="center", font=mg.MONO_M)
    ke = ease(seg(t, le(L21 + 2) + 0.4, le(L21 + 2) + 1.2))
    if ke > 0:
        h.mono(c, "EP01 · SIXTEEN HOURS", 540, 1110, 20, WHITE, ke, align="center", font=mg.MONO_M)
        for j, s in enumerate(SOURCES[:4]):
            h.mono(c, s[:86] + ("…" if len(s) > 86 else ""), 540, 1600 + j * 22, 11, SOFT, 0.8 * ke, align="center")
    h.vignette(c, 0.5)


FLOOR_FN = [fl_ground, fl_mechanism, fl_you, fl_idea, fl_imagine, fl_surface]
XF = 0.7


def frame(c, t):
    h.GRAIN[0] = False
    f = floor_at(t)
    FLOOR_FN[f](c, t)
    if f + 1 < 6 and t > F_START[f + 1] - XF:                  # crossfade into the next floor
        a = ease(seg(t, F_START[f + 1] - XF, F_START[f + 1]))
        c.saveLayerAlpha(None, int(255 * a))
        FLOOR_FN[f + 1](c, t)
        c.restore()
    if f == 4 and FALL_T0 - 0.2 < t < LAND + 0.2:
        pass                                                    # the fall owns the frame: no furniture
    else:
        ruler(c, t)
        card(c, t)
    gauge(c, t)
    captions(c, t)
    h.mono(c, "EP01 · SIXTEEN HOURS", 540, 100, 16, SOFT, 0.8, align="center", font=mg.MONO_M)
    h.GRAIN[0] = True
    h.grain(c, t)


def build_cues():
    CUES.clear()
    d = 0.012
    cue(0.25, "power_up", -10)
    for k in range(16):
        cue(ls(0) + 0.3 + (le(0) - 0.5 - ls(0)) * (k / 16) ** 1.2 + d, "tick_run" if k % 4 else "thock", -18 if k % 4 else -12, -0.3 + 0.04 * k)
    cue(ls(1) + 1.2 + d, "form", -12)
    cue(ls(2) - 0.05, "servo", -10, 0.2)                        # the ruler slides back to 2 seconds
    cue(ls(2) + 0.8 + d, "chatter", -14)
    for f in range(1, 6):
        cue(F_START[f] - 0.2, "hydraulic" if f < 4 else "servo", -12, -0.7)   # the gauge moves floor
    cue(ls(4) + 0.2, "chatter", -17)
    for k in range(10):
        cue(ls(4) + 0.3 + k * 0.28, "tick_run", -22, -0.4 + 0.08 * k)
    for j in range(3):
        cue(ls(5) + j * 0.7 + d, "confirm", -18, -0.5)
    cue(ls(6) + 0.8, "scan", -14)
    cue(ls(6) + 2.2, "form", -12)
    cue(ls(7) + d, "latch", -9)
    lad = next(i for i, x in enumerate(L) if x.get("ladder"))
    for k in range(5):
        cue(ls(lad) + (le(lad) - ls(lad)) * k / 5 + d, "dock", -12 + k, 0.3)
    L9 = first_of_floor(2)["i"]
    for k in range(16):
        cue(ls(L9) + 0.1 + k * 0.07, "tick_run", -22, 0.0)
    for j in range(3):
        cue(ls(L9 + 1) + j * 1.9 + d, "dock", -12, 0.3)
    L11 = first_of_floor(3)["i"]
    cue(ls(L11 + 1), "form", -14)
    cue(ls(L11 + 2) - 0.2, "riser", -16)
    cue(le(L11 + 2) + 0.8, "thum", -12)
    for j in range(2):
        cue(ls(L11 + 3) + j * 2.6 + d, "dock", -11)
    cue(FALL_T0 - 0.56, "vortex", -2)
    cue(LAND + 0.4, "swell", -10)
    cue(LAND + 0.5, "chatter", -16)
    Lg = DROP_LINE + 3
    for j in range(3):
        cue(ls(Lg) + j * 2.1, "whoosh", -18, [-0.4, 0.4, 0.0][j])
    cue(ls(DROP_LINE + 2), "form", -14)
    cue(F_START[5] - 0.3, "riser", -15)
    L21 = first_of_floor(5)["i"]
    for j in range(3):
        cue(ls(L21) + 1.2 + j * 1.8 + d, "thock", -10)
    for j in range(2):
        cue(ls(L21 + 1 + j) + 0.1 + d, "latch", -9, [-0.3, 0.3][j])
    cue(le(L21 + 2) + 0.4, "thum", -14)
    json.dump(dict(cues=CUES, floors=F_START, fall=FALL_T0, land=LAND, total=DUR,
                   cuts=[x["start"] for x in L if x.get("cut")]), open(os.path.join(BUILD, "events.json"), "w"), indent=1)
    return CUES


if __name__ == "__main__":
    if sys.argv[1] == "still":
        for tt in sys.argv[2:]:
            print(h.still(frame, float(tt), os.path.join(BUILD, f"still_{float(tt):05.1f}.png")))
    elif sys.argv[1] == "cues":
        print(len(build_cues()))
    else:
        build_cues()
        print(h.render(frame, DUR, os.path.join(BUILD, "ep01_silent.mp4")))
