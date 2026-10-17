"""EP05 · FOLLOW THE SUN, the scenes: line art keyed to the script's line ids and George's words (engine.tl.word),
which the engine turns into characters.

  GROUND     Google's satellite forms, four chips on its body; 1 OCT 2026 and a Falcon 9 going up; the chips in a
             rain of particles (do they survive?); Starcloud's satellite beside a fridge, one H100, Shakespeare
             streaming out; the Earth turning, chips lifting off it: why leave the planet?
  MECHANISM  1771: a mill and its water wheel turning in a river; the mill becomes racks, the wheel a pylon; a grid of
             100 squares (all the world's electricity) with 1.5 lit, then 3 (about all of Japan); Three Mile Island's
             cooling towers steaming again; look up: the sun, the Earth, a satellite in a dawn-dusk orbit; the same
             panel on the ground and in orbit, one stream of energy against eight
  NOW        the filings; the Earth in a shell of dots (1 dot = 100 satellites): Starcloud's 88,000, SpaceX's million,
             then the ~16,500 working today; China's 12 of 2,800; a Falcon 9 and $7,000 a kilo; one Big Mac as
             payload, $1,500, a block of 250 Big Macs; $7,000 against $200, 35x; a chip that can't shed its heat and
             cracks
  IDEA       four ages side by side: water and a mill, coal and a chimney, a reactor and racks, the sun and a satellite
  IMAGINE    a dotted 2040; a ring of satellites around the Earth, in no country, in permanent daylight; the 1967
             treaty; who owns what catches the sunlight?
  SURFACE    1771: the wheel in the river | 2026: the satellite in the sun; the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, MID, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, segs,  # noqa: E402
                         draw_segs, formation, lines_in, points, closed_fill, stroke_polys, bignum, mac_icon, mini_mac,
                         chip, keys, bump, morph_polys, dotted_num, roll, page, burst, sun, globe, satellite)

GROUND_Y = 800
TRAILS = []
GLINTS = []
RNG = np.random.default_rng(5)


# ---------------------------------------------------------------- things
def rocket(cx, bot, h, w):
    """A two-stage rocket with a payload fairing, grid fins and landing legs."""
    top = bot - h
    fh = 0.17 * h
    fw = 0.62 * w
    out = [P([(cx - w / 2, top + fh), (cx - w / 2, bot), (cx + w / 2, bot), (cx + w / 2, top + fh)]),
           np.column_stack([cx - fw * np.cos(np.linspace(0, math.pi / 2, 20)), top + fh - fh * np.sin(np.linspace(0, math.pi / 2, 20))]),
           np.column_stack([cx + fw * np.cos(np.linspace(0, math.pi / 2, 20)), top + fh - fh * np.sin(np.linspace(0, math.pi / 2, 20))]),
           P([(cx - fw, top + fh), (cx + fw, top + fh)]), P([(cx - w / 2, top + 0.38 * h), (cx + w / 2, top + 0.38 * h)]),
           P([(cx - w / 2, bot - 0.1 * h), (cx - 1.5 * w, bot)]), P([(cx + w / 2, bot - 0.1 * h), (cx + 1.5 * w, bot)]),
           P([(cx - 0.35 * w, bot), (cx - 0.5 * w, bot + 0.03 * h), (cx + 0.5 * w, bot + 0.03 * h), (cx + 0.35 * w, bot)])]
    for sgn in (-1, 1):
        x0 = cx + sgn * w / 2
        out.append(P([(x0, top + 0.4 * h), (x0 + sgn * 0.45 * w, top + 0.4 * h), (x0 + sgn * 0.45 * w, top + 0.44 * h), (x0, top + 0.44 * h)]))
    return out


def fridge(cx, bot, w, h):
    x0, y0 = cx - w / 2, bot - h
    return [mg.rrect_pts(x0, y0, w, h, 0.06 * w, 4), P([(x0, y0 + 0.36 * h), (x0 + w, y0 + 0.36 * h)]),
            P([(x0 + 0.84 * w, y0 + 0.1 * h), (x0 + 0.84 * w, y0 + 0.26 * h)]), P([(x0 + 0.84 * w, y0 + 0.46 * h), (x0 + 0.84 * w, y0 + 0.7 * h)])]


def mill(x, bot, w, h):
    """A mill building: walls, a pitched roof, rows of windows."""
    out = [P([(x, bot), (x, bot - h), (x + w, bot - h), (x + w, bot), (x, bot)]),
           P([(x - 0.04 * w, bot - h), (x + w / 2, bot - h - 0.28 * w), (x + 1.04 * w, bot - h)])]
    for r in range(3):
        for k in range(5):
            wx, wy = x + (0.1 + 0.18 * k) * w, bot - h + (0.14 + 0.28 * r) * h
            out.append(rect(wx, wy, 0.09 * w, 0.14 * h))
    return out


def wheel(cx, cy, r, rot):
    out = [ellipse(cx, cy, r, r, 0, 360, 72), ellipse(cx, cy, 0.84 * r, 0.84 * r, 0, 360, 64), ellipse(cx, cy, 0.12 * r, 0.12 * r, 0, 360, 20)]
    for k in range(8):
        a = rot + k * math.pi / 4
        out.append(P([(cx + 0.12 * r * math.cos(a), cy + 0.12 * r * math.sin(a)), (cx + 0.84 * r * math.cos(a), cy + 0.84 * r * math.sin(a))]))
    for k in range(16):
        a = rot + k * math.pi / 8
        out.append(P([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx + 1.16 * r * math.cos(a), cy + 1.16 * r * math.sin(a))]))
    return out


def river(x0, x1, y, ph, n=3):
    xs = np.linspace(x0, x1, 80)
    return [np.column_stack([xs, y + 16 * k + 7 * np.sin(xs / 45.0 + ph + k)]) for k in range(n)]


def racks(x, bot, n, w=70, h=240, gap=22):
    out = []
    for k in range(n):
        x0 = x + k * (w + gap)
        out.append(mg.rrect_pts(x0, bot - h, w, h, 5, 3))
        for j in range(8):
            yy = bot - h + (0.1 + 0.1 * j) * h
            out.append(P([(x0 + 0.15 * w, yy), (x0 + 0.85 * w, yy)]))
    return out


def pylon(cx, bot, h):
    """A lattice power pylon with two cross arms."""
    top = bot - h
    wb, wt = 0.26 * h, 0.05 * h
    L = P([(cx - wb / 2, bot), (cx - wt / 2, top)])
    R = P([(cx + wb / 2, bot), (cx + wt / 2, top)])
    out = [L, R]
    zz = []
    for k in range(9):
        u = k / 8
        y = bot - u * h
        hw = lerp(wb, wt, u) / 2
        zz.append((cx + (hw if k % 2 else -hw), y))
    out.append(P(zz))
    for u, span in ((0.72, 0.36), (0.88, 0.28)):
        y = bot - u * h
        out.append(P([(cx - span * h, y), (cx + span * h, y)]))
        for sgn in (-1, 1):
            out.append(P([(cx + sgn * span * h, y), (cx + sgn * span * h, y + 0.05 * h)]))
    return out


def tower(cx, bot, h, w):
    """A cooling tower: the hyperbolic profile, the lip, the base."""
    t = np.linspace(0, 1, 40)
    t0 = 0.7
    hw = np.where(t < t0, 0.3 * w + 0.2 * w * ((t0 - t) / t0) ** 2, 0.3 * w + 0.08 * w * ((t - t0) / (1 - t0)) ** 2)
    ys = bot - t * h
    return [np.column_stack([cx - hw, ys]), np.column_stack([cx + hw, ys]), ellipse(cx, bot - h, hw[-1], 0.08 * w, 0, 360, 40),
            P([(cx - hw[0] - 20, bot), (cx + hw[0] + 20, bot)])]


def panel(cx, cy, w, h, legs=False):
    """A solar panel of 4x3 cells (on legs for the ground one)."""
    out = [rect(cx - w / 2, cy - h / 2, w, h)]
    for k in range(1, 4):
        out.append(P([(cx - w / 2 + k * w / 4, cy - h / 2), (cx - w / 2 + k * w / 4, cy + h / 2)]))
    for k in range(1, 3):
        out.append(P([(cx - w / 2, cy - h / 2 + k * h / 3), (cx + w / 2, cy - h / 2 + k * h / 3)]))
    if legs:
        out += [P([(cx - 0.3 * w, cy + h / 2), (cx - 0.3 * w, GROUND_Y)]), P([(cx + 0.3 * w, cy + h / 2), (cx + 0.3 * w, GROUND_Y)]),
                P([(cx - w, GROUND_Y), (cx + w, GROUND_Y)])]
    return out


def factory(cx, bot, s):
    return [P([(cx - 0.6 * s, bot), (cx - 0.6 * s, bot - 0.5 * s), (cx - 0.3 * s, bot - 0.7 * s), (cx - 0.3 * s, bot - 0.5 * s),
               (cx, bot - 0.7 * s), (cx, bot - 0.5 * s), (cx + 0.3 * s, bot - 0.7 * s), (cx + 0.3 * s, bot - 0.5 * s), (cx + 0.6 * s, bot - 0.5 * s),
               (cx + 0.6 * s, bot), (cx - 0.6 * s, bot)]),
            P([(cx + 0.36 * s, bot - 0.5 * s), (cx + 0.36 * s, bot - 1.3 * s), (cx + 0.5 * s, bot - 1.3 * s), (cx + 0.5 * s, bot - 0.5 * s)])]


def coal(cx, bot, s):
    out = [P([(cx - 0.7 * s, bot), (cx - 0.35 * s, bot - 0.35 * s), (cx, bot - 0.5 * s), (cx + 0.35 * s, bot - 0.33 * s), (cx + 0.7 * s, bot)])]
    rng = np.random.default_rng(9)
    for _ in range(9):
        x, y = cx + rng.uniform(-0.45, 0.45) * s, bot - rng.uniform(0.05, 0.3) * s
        out.append(ellipse(x, y, 0.07 * s, 0.05 * s, 0, 360, 10))
    return out


def unit_grid(x0, y0, n_col, n_row, cell, gap):
    return [(x0 + (k % n_col) * (cell + gap), y0 + (k // n_col) * (cell + gap)) for k in range(n_col * n_row)]


def draw_cells(c, cells_, cell, lit, a=1.0, lit_col=WHITE, off_col=SOFT, off_a=0.55):
    """Unit squares: the first `lit` (fractional) filled, the rest outlined."""
    if a <= 0:
        return
    po = mg.stroke(off_col, 1.2, off_a * a)
    for k, (x, y) in enumerate(cells_):
        r = skia.Rect.MakeXYWH(x, y, cell, cell)
        c.drawRect(r, po)
        f = min(1.0, max(0.0, lit - k))
        if f > 0:
            c.drawRect(skia.Rect.MakeXYWH(x, y + cell * (1 - f), cell, cell * f), mg.fill(lit_col, 0.95 * a))


def shell(n, r0, r1, seed):
    """n satellites as dots around a globe of radius 1: (x, y, visible-in-front-or-beside) on the unit scale."""
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(n, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    rad = rng.uniform(r0, r1, n)
    x, y, z = v[:, 0] * rad, v[:, 1] * rad, v[:, 2]
    vis = ~((z < 0) & (np.hypot(x, y) < 1.0))
    return np.column_stack([x, y])[vis]


SHELL = shell(12000, 1.1, 1.9, 7)                 # 1 dot = 100 satellites (SpaceX's million = 10,000 dots)


def dots(c, cx, cy, r, n, a=1.0, size=2.6, col=WHITE):
    if n <= 0 or a <= 0:
        return
    X = SHELL[: int(n)] * r + [cx, cy]
    p = mg.stroke(col, size, a)
    p.setStrokeCap(skia.Paint.kRound_Cap)
    c.drawPoints(skia.Canvas.kPoints_PointMode, [skia.Point(float(x), float(y)) for x, y in X], p)


def sat_at(c, cx, cy, s, a=1.0, ang=0.0, lit=0.0):
    polys = satellite(cx, cy, s, ang)
    if lit > 0:
        closed_fill(c, [polys[2], polys[8]] if len(polys) > 8 else polys[:1], 1.0, mg.fill(WHITE, 0.35 * lit * a))
    stroke_polys(c, polys, WHITE, 1.7, a)
    return polys


# ---------------------------------------------------------------- GROUND
T_SAT, T_FOUR, T_ORBIT, T_LDATE, T_OCT = wd("launch", "satellite"), wd("launch", "four"), wd("launch", "orbit."), wd("launch", "Launch"), wd("launch", "October.")
T_TEST, T_SURV = ls("test"), wd("test", "survive")
T_FR, T_FRIDGE, T_MODEL, T_SHAKES = ls("fridge"), wd("fridge", "fridge"), wd("fridge", "model"), wd("fridge", "Shakespeare.")
T_WHY = ls("why")
T_MILL0 = ls("mill")
CHIPS4 = [(CX - 30, 520), (CX + 30, 520), (CX - 30, 580), (CX + 30, 580)]


def cold_open(c, t):
    a = win(t, T_SAT - 0.6, T_FR + 0.3, 0.3, 0.5)
    if a > 0:
        with layer(c, a):
            ks = 1 - ease(seg(t, T_LDATE - 0.2, T_LDATE + 0.4)) * 0.0
            with layer(c, ks):
                lines_in(c, satellite(CX, 550, 330), t, T_SAT - 0.5, 0.9, WHITE, 1.8, seed_pt=(CX, 800))
                ev(T_SAT - 0.5, "form", t, CX)
                if t >= T_FOUR - 0.1:
                    for k, (x, y) in enumerate(CHIPS4):
                        t_k = T_FOUR - 0.1 + 0.12 * k
                        if t >= t_k:
                            stroke_polys(c, chip(x, y, 18), GLOW, 1.4, ease(seg(t, t_k, t_k + 0.2)))
                            c.drawRect(skia.Rect.MakeXYWH(x - 9, y - 9, 18, 18), mg.fill(GLOW, 0.8 * ease(seg(t, t_k, t_k + 0.2))))
                            ev(t_k, "tick", t, x)
                    label(c, "FOUR GOOGLE AI CHIPS (TPUs)", CX, 690, t, T_FOUR + 0.4, 22, GLOW, a=a)
            if t >= T_ORBIT - 0.2:                                         # an orbit sweeps round it
                k = ease(seg(t, T_ORBIT - 0.2, T_ORBIT + 0.8))
                q = ellipse(CX, 560, 560, 150, 180, 180 + 360 * k, 120)
                stroke_polys(c, [q], SOFT, 1.4, 0.8)
                ev(T_ORBIT - 0.2, "whoosh", t, CX)
            bignum(c, t, "1 OCT 2026", 110, CX, 230, T_LDATE)
            label(c, "PROJECT SUNCATCHER · ON A SPACEX FALCON 9", CX, 325, t, T_LDATE + 0.5, 22, SOFT, a=a)
        if t >= T_OCT - 0.3:                                               # a rocket goes up at the right
            y = keys(t, [(T_OCT - 0.3, 1480), (T_TEST + 0.2, 1140), (T_SURV, 300)])
            with layer(c, win(t, T_OCT - 0.3, T_FR, 0.3, 0.4)):
                lines_in(c, rocket(1600, y, 420, 34), t, T_OCT - 0.3, 0.4, WHITE, 1.7)
                n = 60
                ex = np.column_stack([1600 + RNG.normal(0, 10, n), y + 20 + np.abs(RNG.normal(0, 60, n))])
                points(c, ex, 0.9, GOLD, 3.2)
                ev(T_OCT - 0.1, "riser", t, 1600)
    # the test: a rain of particles on the chips
    kt = win(t, T_TEST - 0.1, T_FR + 0.4, 0.3, 0.4)
    if kt > 0:
        n = 90
        ph = (t * 1.3 + np.arange(n) / n) % 1.0
        xs = CX + 520 - ph * 900 + (np.arange(n) * 37 % 200) - 100
        ys = 180 + ph * 520 + (np.arange(n) * 53 % 140)
        points(c, np.column_stack([xs, ys]), 0.8 * kt, WHITE, 2.4)
        label(c, "RADIATION · HEAT · COLD", CX, 760, t, T_TEST + 0.3, 20, SOFT, a=kt)
        label(c, "DO THEY SURVIVE?", CX, 800, t, T_SURV, 26, WHITE, a=kt)
        for k, (x, y) in enumerate(CHIPS4):
            if int(t * 9 + k * 3) % 7 == 0:
                c.drawRect(skia.Rect.MakeXYWH(x - 12, y - 12, 24, 24), mg.stroke(WHITE, 2, kt))
    # Starcloud-1, the size of a small fridge
    af = win(t, T_FR - 0.05, T_WHY + 0.3, 0.3, 0.5)
    if af > 0:
        with layer(c, af):
            bignum(c, t, "DEC 2025", 110, CX, 230, T_FR)
            label(c, "STARCLOUD-1 · THE FIRST NVIDIA H100 IN ORBIT", CX, 325, t, T_FR + 0.6, 22, SOFT, a=af)
            lines_in(c, satellite(CX - 170, 580, 300), t, wd("fridge", "satellite") - 0.1, 0.7, WHITE, 1.8)
            ev(wd("fridge", "satellite") - 0.1, "form", t, CX - 170)
            if t >= T_FRIDGE - 0.1:
                lines_in(c, fridge(CX + 250, 760, 170, 330), t, T_FRIDGE - 0.1, 0.5, SOFT, 1.5)
                label(c, "A SMALL FRIDGE", CX + 250, 800, t, T_FRIDGE + 0.2, 20, SOFT, a=af)
            if t >= T_MODEL - 0.1:
                c.drawRect(skia.Rect.MakeXYWH(CX - 170 - 22, 558, 44, 44), mg.fill(GLOW, 0.85 * ease(seg(t, T_MODEL - 0.1, T_MODEL + 0.2))))
                ev(T_MODEL, "confirm", t, CX - 170)
            if t >= T_SHAKES - 0.2:                                            # text streaming out of it
                k = seg(t, T_SHAKES - 0.2, T_SHAKES + 1.6)
                for j in range(9):
                    y = 380 + j * 26 - 120 * k
                    w = 60 + (j * 71) % 150
                    c.drawLine(CX - 170 - w / 2, y, CX - 170 + w / 2, y, mg.stroke(GLOW, 3, max(0.0, 1 - abs(y - 350) / 180) * af))
                label(c, "TRAINED ON SHAKESPEARE, IN ORBIT", CX - 170, 800, t, T_SHAKES, 22, WHITE, a=af)
    # why leave the planet?
    aw = win(t, T_WHY - 0.1, T_MILL0 + 0.3, 0.3, 0.4)
    if aw > 0:
        with layer(c, aw):
            rot = t * 0.35
            lines_in(c, globe(CX, 600, 230, rot), t, T_WHY - 0.1, 0.7, GLOW, 1.6, seed_pt=(CX, 900))
            ev(T_WHY - 0.1, "form", t, CX)
            for k in range(7):
                u = seg(t, T_WHY + 0.5 + 0.18 * k, T_WHY + 2.2 + 0.18 * k)
                if u <= 0:
                    continue
                ang = -math.pi / 2 + (k - 3) * 0.35
                r = lerp(230, 520, ease(u, "o"))
                x, y = CX + r * math.cos(ang), 600 + r * math.sin(ang)
                c.drawRect(skia.Rect.MakeXYWH(x - 8, y - 8, 16, 16), mg.fill(WHITE, 0.9 * (1 - 0.5 * u)))
            label(c, "WHY LEAVE THE PLANET?", CX, 250, t, wd("why", "leave"), 26, WHITE, a=aw)


# ---------------------------------------------------------------- MECHANISM
T_1771, T_ARK, T_MILLW, T_WATER = wd("mill", "seventeen"), wd("mill", "Richard"), wd("mill", "mill"), wd("mill", "water")
T_FOLLOW, T_COMP = ls("follow"), wd("follow", "Computers")
T_TWH, T_HALF = ls("twh"), wd("twh", "one")
T_JAPAN0, T_DOUBLE, T_JAPAN = ls("japan"), wd("japan", "double,"), wd("japan", "Japan")
T_TMI, T_RESTART, T_THREE = ls("tmi"), wd("tmi", "restart"), wd("tmi", "Three")
T_LOOK, T_ORB = ls("look"), wd("look", "orbit,")
T_EIGHT0, T_EIGHT = ls("eight"), wd("eight", "eight")
T_FIL = ls("filings")
MILL = mill(470, GROUND_Y, 380, 260)
WHEEL_C = (1000.0, 690.0)
GRID_CELLS = unit_grid(1010, 300, 10, 10, 40, 10)


def ground_scene(c, t):
    a = win(t, T_MILL0 - 0.1, T_LOOK + 0.9, 0.3, 0.7)
    if a <= 0:
        return
    drop = 900 * ease(seg(t, T_LOOK + 0.2, T_LOOK + 1.0), "i")           # "now look up": the ground falls away
    c.save(); c.translate(0, drop)
    with layer(c, a):
        kd = 1 - ease(seg(t, T_FOLLOW - 0.3, T_FOLLOW + 0.2))
        if kd > 0:
            with layer(c, kd):
                bignum(c, t, "1771", 130, CX, 230, T_1771)
                label(c, "CROMFORD, ENGLAND · RICHARD ARKWRIGHT'S MILL", CX, 330, t, T_ARK, 22, SOFT, a=a * kd)
        rot = (t - T_MILL0) * (0.6 + 1.4 * ease(seg(t, T_WATER - 0.3, T_WATER + 0.5)))
        ph = t * 2.2
        km = seg(t, T_COMP - 0.1, T_COMP + 0.9)                            # mills -> racks, the wheel -> a pylon
        src = MILL + wheel(*WHEEL_C, 120, rot) + river(900, 1650, GROUND_Y + 10, ph)
        dst = racks(430, GROUND_Y, 6) + pylon(1000, GROUND_Y, 330) + [P([(1000 - 0.36 * 330, GROUND_Y - 0.72 * 330), (1650, GROUND_Y - 0.62 * 330)]),
                                                                       P([(1000 + 0.36 * 330, GROUND_Y - 0.72 * 330), (1650, GROUND_Y - 0.6 * 330)])]
        if km <= 0:
            lines_in(c, MILL, t, T_MILLW - 0.3, 0.8, WHITE, 1.8, seed_pt=(660, 900))
            lines_in(c, wheel(*WHEEL_C, 120, rot), t, T_MILLW - 0.1, 0.7, GLOW, 1.8)
            lines_in(c, river(900, 1650, GROUND_Y + 10, ph), t, T_MILLW, 0.5, GLOW, 1.6)
            ev(T_MILLW - 0.3, "form", t, 660)
            ev(T_WATER, "swell", t, 1000)
        elif km < 1:
            morph_polys(c, src, dst, km, WHITE)
            ev(T_COMP - 0.1, "morph", t, CX)
        else:
            kr = 1 - ease(seg(t, T_TMI - 0.3, T_TMI + 0.3)) * 0.0
            stroke_polys(c, racks(430, GROUND_Y, 6), WHITE, 1.8, kr)
            stroke_polys(c, dst[len(racks(430, GROUND_Y, 6)):], GLOW, 1.7, 1 - ease(seg(t, T_TWH - 0.4, T_TWH + 0.1)))
        label(c, "MILLS FOLLOWED RIVERS", CX, 250, t, T_FOLLOW, 24, WHITE, a=a * (1 - ease(seg(t, T_COMP - 0.2, T_COMP + 0.1))))
        label(c, "COMPUTERS FOLLOW ELECTRICITY", CX, 250, t, T_COMP + 0.3, 24, WHITE, a=a * (1 - ease(seg(t, T_TWH - 0.3, T_TWH))))
        # all the world's electricity as 100 squares; data centres light 1.5, then about 3
        kg = win(t, T_TWH - 0.1, T_TMI + 0.2, 0.3, 0.4)
        if kg > 0:
            lit = keys(t, [(T_HALF - 0.1, 0.0), (T_HALF + 0.5, 1.5), (T_DOUBLE - 0.1, 1.5), (T_DOUBLE + 0.5, 2.9)])
            draw_cells(c, GRID_CELLS, 40, lit, kg)
            label(c, "ALL THE WORLD'S ELECTRICITY · 1 SQUARE = 1%", 1255, 830, t, T_TWH + 0.2, 18, SOFT, a=kg)
            ev(T_HALF + 0.1, "tick", t, 1030)
            ev(T_DOUBLE, "tick", t, 1060)
            with layer(c, kg):
                roll(c, "1.5%", "~3%", 120, 700, 260, t, T_HALF, T_DOUBLE)
            label(c, "DATA CENTRES, 2024", 700, 355, t, T_HALF + 0.4, 22, GLOW, a=kg * (1 - ease(seg(t, T_DOUBLE - 0.2, T_DOUBLE))))
            label(c, "BY 2030: 945 TWh, ABOUT ALL OF JAPAN", 700, 355, t, T_JAPAN, 22, GLOW, a=kg)
        # Three Mile Island, steaming again
        if t >= T_TMI - 0.2:
            kt = ease(seg(t, T_TMI - 0.2, T_TMI + 0.4))
            for k, x in enumerate((1090, 1370)):
                lines_in(c, tower(x, GROUND_Y, 330, 260), t, T_TMI - 0.2 + 0.15 * k, 0.6, WHITE, 1.8)
                if t >= T_RESTART:
                    n = 70
                    u = ((t - T_RESTART) * 0.35 + np.arange(n) / n) % 1.0
                    X = np.column_stack([x + np.sin(u * 7 + k) * 40 * u + (np.arange(n) * 29 % 60) - 30, GROUND_Y - 340 - u * 260])
                    points(c, X, 0.7 * kt * ease(seg(t, T_RESTART, T_RESTART + 0.6)), WHITE, 3.5)
            ev(T_RESTART, "hydraulic", t, 1230)
            c.drawLine(730, GROUND_Y - 250, 1000, GROUND_Y - 300, mg.stroke(GLOW, 1.6, kt))
            label(c, "THREE MILE ISLAND · A REACTOR RESTARTING FOR MICROSOFT", CX, 250, t, T_THREE, 22, WHITE, a=a)
    c.restore()


def sky(c, t):
    """Look up: the sun, the Earth, a satellite in a dawn-dusk orbit; then the same panel on the ground and in orbit."""
    a = win(t, T_LOOK + 0.4, T_FIL + 0.3, 0.4, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kg = 1 - ease(seg(t, T_EIGHT0 - 0.2, T_EIGHT0 + 0.3))
        if kg > 0:
            with layer(c, kg):
                lines_in(c, sun(1500, 330, 80, t * 0.2), t, T_LOOK + 0.5, 0.7, WHITE, 2.0)
                closed_fill(c, [ellipse(1500, 330, 80, 80, 0, 360, 60)], 1.0, mg.fill(WHITE, 0.8))
                lines_in(c, globe(760, 600, 220, t * 0.3), t, T_LOOK + 0.6, 0.7, GLOW, 1.6)
                q = ellipse(760, 600, 330, 120, 0, 360, 120)
                stroke_polys(c, [q], SOFT, 1.3, 0.8 * ease(seg(t, T_ORB - 0.3, T_ORB + 0.4)))
                if t >= T_ORB - 0.2:
                    th = (t - T_ORB) * 1.1
                    x, y = 760 + 330 * math.cos(th), 600 + 120 * math.sin(th)
                    if not (math.sin(th) < 0 and abs(x - 760) < 220):
                        sat_at(c, x, y, 70, 1.0, 0.0, lit=1.0)
                    for k in range(5):                                      # sunlight reaching it
                        yy = y - 30 + 15 * k
                        c.drawLine(1400, 330 + (yy - 330) * 0.2, x + 40, yy, mg.stroke(GOLD, 1.2, 0.35))
                label(c, "A DAWN-DUSK ORBIT: ALWAYS OVER THE LINE BETWEEN DAY AND NIGHT", CX, 900 - 40, t, T_ORB + 0.3, 18, SOFT, a=a * kg)
                ev(T_ORB, "swell", t, 760)
        if t >= T_EIGHT0 - 0.2:                                           # the same panel, ground vs orbit
            ke = ease(seg(t, T_EIGHT0 - 0.2, T_EIGHT0 + 0.3))
            with layer(c, ke):
                lines_in(c, panel(560, 620, 220, 120, legs=True), t, T_EIGHT0 - 0.2, 0.5, WHITE, 1.8)
                lines_in(c, panel(1360, 560, 220, 120), t, T_EIGHT0, 0.5, WHITE, 1.8)
                label(c, "ON THE GROUND", 560, 860 - 30, t, T_EIGHT0 + 0.2, 20, SOFT, a=a * ke)
                label(c, "IN ORBIT", 1360, 700, t, T_EIGHT0 + 0.4, 20, SOFT, a=a * ke)
                for (x, y, n_st) in ((560, 620, 1), (1360, 560, 8)):         # streams of energy into each
                    n = 18 * n_st
                    u = ((t - T_EIGHT0) * 0.9 + np.arange(n) / n) % 1.0
                    lane = (np.arange(n) % n_st) - (n_st - 1) / 2
                    X = np.column_stack([x - 90 + 180 * u, y - 250 + 180 * u + 0 * lane]) + np.column_stack([lane * 22, np.zeros(n)])
                    points(c, X, 0.9, GOLD, 3.4)
                bignum(c, t, "UP TO 8×", 110, CX, 240, T_EIGHT - 0.1)


# ---------------------------------------------------------------- NOW
T_SC, T_88K = ls("starcloud"), wd("starcloud", "eighty-eight")
T_SX, T_MIL = ls("spacex"), wd("spacex", "million.")
T_TODAY, T_16 = ls("today"), wd("today", "sixteen")
T_CN, T_12, T_2800 = ls("china"), wd("china", "twelve"), wd("china", "two")
T_TICKET, T_7K = ls("ticket"), wd("ticket", "seven")
T_MAC, T_MACW, T_1500, T_250 = ls("mac"), wd("mac", "Big"), wd("mac", "fifteen"), wd("mac", "two")
T_BE, T_200, T_35 = ls("breakeven"), wd("breakeven", "two"), wd("breakeven", "thirty-five")
T_HARD, T_HEAT, T_BROKEN = ls("hard"), wd("hard", "heat"), wd("hard", "broken")
T_EVERY = ls("every")
GLINTS.append((T_MIL + 0.9, 0.9))
CN_CELLS = unit_grid(CX - 420, 360, 70, 40, 9, 3)
MAC_WALL = {}


def filings(c, t):
    a = win(t, T_FIL - 0.05, T_CN + 0.3, 0.2, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kp = 1 - ease(seg(t, T_SC - 0.2, T_SC + 0.2))
        if kp > 0:
            for k in range(3):
                lines_in(c, page(CX - 260 + 180 * k, 380 + 20 * (k % 2), 190, 250), t, T_FIL + 0.1 * k, 0.4, WHITE, 1.8, a=kp)
                ev(T_FIL + 0.1 * k, "paper", t, CX - 260 + 180 * k)
            label(c, "FILED WITH THE FCC", CX, 700, t, T_FIL + 0.4, 22, SOFT, a=a * kp)
        if t >= T_SC - 0.2:
            r = 190
            lines_in(c, globe(CX, 580, r, t * 0.25), t, T_SC - 0.2, 0.5, GLOW, 1.5)
            n = keys(t, [(T_88K - 0.1, 0), (T_88K + 0.5, 880), (T_MIL - 0.4, 880), (T_MIL + 0.3, 10000), (T_16 - 0.2, 10000), (T_16 + 0.5, 165)])
            dots(c, CX, 580, r, n, 0.9)
            if t < T_SX - 0.05:
                bignum(c, t, "88,000", 110, CX, 200, T_88K - 0.05)
            elif t < T_TODAY - 0.05:
                roll(c, "88,000", "1,000,000", 110, CX, 200, t, T_88K - 0.05, T_SX)
            else:
                roll(c, "1,000,000", "~16,500", 110, CX, 200, t, T_TODAY - 0.1, T_16 - 0.1)
            lab = "STARCLOUD'S FCC FILING" if t < T_SX else "SPACEX'S FCC FILING, JAN 2026" if t < T_TODAY else "WORKING TODAY · EVERY COUNTRY"
            t0 = T_88K + 0.3 if t < T_SX else T_SX + 0.3 if t < T_TODAY else T_16 + 0.4
            label(c, lab, CX, 290, t, t0, 22, GLOW, a=a)
            label(c, "1 DOT = 100 SATELLITES", CX, 880 - 40, t, T_88K + 0.8, 18, SOFT, a=a)
            ev(T_88K + 0.1, "grains", t, CX)
            ev(T_MIL - 0.3, "zoom", t, CX)
            ev(T_16, "sub_drop", t, CX)


def china(c, t):
    a = win(t, T_CN - 0.1, T_TICKET + 0.2, 0.3, 0.4)
    if a <= 0:
        return
    with layer(c, a):
        lit = keys(t, [(T_12 - 0.1, 0), (T_12 + 0.5, 12)])
        draw_cells(c, CN_CELLS, 9, 0, ease(seg(t, T_CN, T_CN + 0.5)), off_a=0.22)
        if lit > 0:                                                        # the first 12, big enough to see
            for k in range(int(math.ceil(lit))):
                x, y = CN_CELLS[k]
                c.drawRect(skia.Rect.MakeXYWH(x - 2, y - 2, 13, 13), mg.fill(WHITE, min(1.0, lit - k)))
            c.drawLine(CX - 420 + 75, 352, CX - 420 + 180, 320, mg.stroke(GLOW, 1.5, 1.0))
            label(c, "THE FIRST 12", CX - 420 + 190, 325, t, T_12 + 0.2, 20, WHITE, "left", a=a)
        label(c, "CHINA'S COMPUTING CONSTELLATION", CX, 240, t, T_CN + 0.4, 24, WHITE, a=a)
        label(c, "12 LAUNCHED IN MAY 2025, OF 2,800 PLANNED", CX, 290, t, T_12 + 0.1, 22, GLOW, a=a)
        ev(T_12, "tick", t, CX - 420)
        ev(T_2800, "grains", t, CX)


def ticket(c, t):
    a = win(t, T_TICKET - 0.05, T_HARD + 0.1, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kr = 1 - ease(seg(t, T_BE - 0.3, T_BE + 0.2))
        if kr > 0:
            with layer(c, kr):
                lines_in(c, rocket(520, GROUND_Y + 20, 620, 54), t, T_TICKET, 0.7, WHITE, 1.8, seed_pt=(520, 900))
                ev(T_TICKET, "form", t, 520)
                k7 = 1 - ease(seg(t, T_MAC - 0.2, T_MAC + 0.2))
                if k7 > 0:
                    with layer(c, k7):
                        bignum(c, t, "$7,000", 120, 1180, 380, T_7K - 0.1)
                        label(c, "A KILO TO ORBIT · SPACEX RIDESHARE, 2026", 1180, 480, t, T_7K + 0.4, 22, GLOW, a=a * k7)
                if t >= T_MACW - 0.2:                                          # one Big Mac as the payload
                    km = ease(seg(t, T_MACW - 0.2, T_MACW + 0.3))
                    mac_icon(c, 520, 150, 40, km)
                    label(c, "ONE BIG MAC · 219 G", 520, 110, t, T_MACW + 0.1, 20, GLOW, a=a * km)
                    ev(T_MACW - 0.1, "pop", t, 520)
                    bignum(c, t, "$1,500", 120, 1180, 300, T_1500 - 0.1)
                    if t >= T_250 - 0.2:
                        if "w" not in MAC_WALL:
                            MAC_WALL["w"] = wall_img(25, 10, 26, 22, 10.5)
                        draw_wall(c, MAC_WALL["w"], 1180 - 325, 700, seg(t, T_250 - 0.2, T_250 + 0.9))
                        label(c, "= 250 BIG MACS", 1180, 760, t, T_250 + 0.4, 26, WHITE, a=a)
                        for r in range(10):
                            ev(T_250 - 0.2 + 1.1 * r / 10, "tick", t, 1180)
        if t >= T_BE - 0.1:                                                # $7,000 against $200
            kb = ease(seg(t, T_BE - 0.1, T_BE + 0.4))
            with layer(c, kb * (1 - ease(seg(t, T_HARD - 0.3, T_HARD + 0.1)))):
                w1 = 1200 * ease(seg(t, T_BE, T_BE + 0.6))
                c.drawRect(skia.Rect.MakeXYWH(360, 440, w1, 56), mg.chrome_paint(440, 496, 0.9))
                label(c, "TODAY: $7,000 A KILO", 360, 420, t, T_BE + 0.2, 22, WHITE, "left", a=a)
                if t >= T_200 - 0.1:
                    c.drawRect(skia.Rect.MakeXYWH(360, 600, 1200 * 200 / 7000 * ease(seg(t, T_200 - 0.1, T_200 + 0.3)), 56), mg.fill(GLOW, 0.95))
                    label(c, "WHERE GOOGLE SAYS ORBIT STARTS TO COMPETE: UNDER $200", 360, 580, t, T_200, 22, GLOW, "left", a=a)
                    ev(T_200, "tick", t, 400)
                bignum(c, t, "35× CHEAPER", 100, CX, 250, T_35 - 0.1)


def wall_img(cols, rows, cw, ch, s):
    w, h = int(cols * cw), int(rows * ch + 2 * s)
    sf = skia.Surface(w, h)
    c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    for r in range(rows):
        for k in range(cols):
            mini_mac(c, (k + 0.5) * cw, h - (r + 1) * ch + 0.52 * s, s, 1.0)
    return sf.makeImageSnapshot(), w, h


def draw_wall(c, img, x0, ybot, frac, a=1.0):
    im, w, h = img
    if frac <= 0 or a <= 0:
        return
    hh = h * min(1.0, frac)
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, skia.Rect.MakeLTRB(0, h - hh, w, h), skia.Rect.MakeLTRB(x0, ybot - hh, x0 + w, ybot), skia.SamplingOptions(skia.FilterMode.kLinear), p)


def hard(c, t):
    a = win(t, T_HARD - 0.1, T_EVERY + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        lines_in(c, chip(CX, 560, 150), t, T_HARD - 0.05, 0.5, WHITE, 1.8)
        kh = ease(seg(t, T_HEAT - 0.3, T_HEAT + 0.3))
        c.drawRect(skia.Rect.MakeXYWH(CX - 75, 485, 150, 150), mg.fill(WHITE, 0.25 + 0.5 * kh * (0.7 + 0.3 * math.sin(t * 9))))
        if kh > 0:                                                         # heat with nowhere to go
            for k in range(5):
                xs = np.linspace(CX - 200, CX + 200, 60)
                y = 380 - 18 * k + 8 * np.sin(xs / 30 + t * 6 + k)
                c.drawPath(_path(np.column_stack([xs, y])), mg.stroke(GLOW, 1.6, 0.7 * kh))
            label(c, "NO AIR TO CARRY THE HEAT AWAY", CX, 250, t, T_HEAT, 22, WHITE, a=a)
        if t >= T_BROKEN - 0.05:
            kc = ease(seg(t, T_BROKEN - 0.05, T_BROKEN + 0.15))
            q = P([(CX - 80, 500), (CX - 30, 545), (CX - 50, 575), (CX + 10, 600), (CX - 5, 630), (CX + 80, 660)])
            stroke_polys(c, [q[: max(2, int(len(q) * kc))]], "#FFFFFF", 3.0, 1.0)
            burst(c, CX + 10, 600, t, T_BROKEN, 70)
            ev(T_BROKEN, "glitch", t, CX)
            label(c, "AND NO ONE TO FIX IT", CX, 820 - 20, t, T_BROKEN + 0.2, 22, WHITE, a=a)


def _path(q):
    p = skia.Path()
    p.moveTo(*q[0])
    for x, y in q[1:]:
        p.lineTo(float(x), float(y))
    return p


# ---------------------------------------------------------------- IDEA
T_RIVER, T_COAL, T_REACTOR = wd("list", "river."), wd("list", "coal"), wd("list", "reactor.")
T_SUNW = wd("sun", "sun.")
T_IMAGINE = ls("imagine")
AGES_X = [420, 780, 1140, 1500]


def ages(c, t):
    a = win(t, T_EVERY - 0.05, T_IMAGINE + 0.2, 0.3, 0.6)
    if a <= 0:
        return
    rot = t * 1.2
    sets = [wheel(AGES_X[0] + 60, 640, 70, rot) + river(AGES_X[0] - 130, AGES_X[0] + 150, GROUND_Y - 30, t * 2) + mill(AGES_X[0] - 150, GROUND_Y - 40, 130, 110),
            coal(AGES_X[1] - 70, GROUND_Y - 40, 110) + factory(AGES_X[1] + 60, GROUND_Y - 40, 110),
            tower(AGES_X[2] - 60, GROUND_Y - 40, 170, 130) + racks(AGES_X[2] + 20, GROUND_Y - 40, 2, 40, 140, 14),
            sun(AGES_X[3] - 50, 520, 40, t * 0.3) + satellite(AGES_X[3] + 40, 650, 120)]
    labs = ["1771 · WATER", "1800s · COAL", "TODAY · NUCLEAR", "NEXT · THE SUN?"]
    hits = [T_RIVER, T_COAL, T_REACTOR, T_SUNW]
    with layer(c, a):
        label(c, "EVERY AGE BUILDS NEXT TO ITS POWER", CX, 230, t, wd("every", "machines"), 24, WHITE, a=a)
        for k, (polys, lab, th) in enumerate(zip(sets, labs, hits)):
            t0 = T_EVERY + 0.15 * k
            hl = bump(t, th - 0.1, th + 0.15, th + 0.9)
            col = WHITE if hl > 0.2 or (k == 3 and t > T_SUNW) else GLOW
            lines_in(c, polys, t, t0, 0.6, col, 1.7 + 1.2 * hl)
            ev(t0, "form", t, AGES_X[k])
            label(c, lab, AGES_X[k], 860 - 40, t, th, 20, WHITE if k == 3 else GLOW, a=a)
            ev(th, "latch", t, AGES_X[k])


# ---------------------------------------------------------------- IMAGINE
T_2040, T_COMPUTERW, T_COUNTRY = wd("imagine", "twenty"), wd("imagine", "computer"), wd("imagine", "country.")
T_WHATIF, T_RING, T_DAY = ls("whatif"), ls("ring"), wd("ring", "daylight.")
T_LAWS, T_TREATY, T_OWN, T_ANSWERS = ls("laws"), wd("laws", "treaty"), wd("laws", "own"), wd("laws", "answers")
T_Q, T_CATCH = ls("question"), wd("question", "catches")
T_THEN = ls("then")
N_RING = 36


def ring_sats(t, cx, cy, rx, ry):
    out = []
    for k in range(N_RING):
        th = t * 0.25 + k * 2 * math.pi / N_RING
        x, y = cx + rx * math.cos(th), cy + ry * math.sin(th)
        out.append((x, y, math.sin(th)))
    return out


def imagine(c, t):
    a = win(t, T_IMAGINE - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        kd = 1 - ease(seg(t, T_LAWS - 0.3, T_LAWS + 0.2))
        if kd > 0:
            dotted_num(c, "2040", 140, CX, 220, t, T_2040, kd)
            label(c, "NOT A FORECAST · A WHAT-IF", CX, 320, t, T_WHATIF + 0.05, 24, WHITE, a=a * kd)
        gx = keys(t, [(T_LAWS, CX), (T_LAWS + 0.8, CX + 180), (T_Q - 0.2, CX + 180), (T_Q + 0.6, CX)])
        lines_in(c, globe(gx, 600, 200, t * 0.2), t, T_IMAGINE + 0.1, 0.7, GLOW, 1.6)
        if t >= T_COMPUTERW - 0.2:                                           # the ring
            kr = ease(seg(t, T_COMPUTERW - 0.2, T_COMPUTERW + 0.8))
            lit = ease(seg(t, T_DAY - 0.6, T_DAY + 0.2))
            for k, (x, y, depth) in enumerate(ring_sats(t, gx, 600, 390, 110)):
                if k / N_RING > kr:
                    continue
                if depth < 0 and abs(x - gx) < 200:
                    continue
                sat_at(c, x, y, 26 + 6 * max(0.0, depth), 0.9, 0.0, lit=lit)
            ev(T_COMPUTERW - 0.2, "zoom", t, gx)
            label(c, "IN NO COUNTRY", gx, 860 - 40, t, T_COUNTRY, 22, GLOW, a=a * (1 - ease(seg(t, T_RING - 0.2, T_RING + 0.2))))
            if t >= T_RING - 0.1:
                lines_in(c, sun(1640, 250, 60, t * 0.2), t, T_RING - 0.1, 0.5, WHITE, 1.8)
                label(c, "IN PERMANENT DAYLIGHT", gx, 860 - 40, t, T_DAY - 0.3, 22, GLOW, a=a * (1 - ease(seg(t, T_LAWS - 0.2, T_LAWS + 0.2))))
                ev(T_DAY - 0.3, "swell", t, 1640)
        kt = win(t, T_TREATY - 0.2, T_Q + 0.3, 0.3, 0.4)                     # the treaty
        if kt > 0:
            with layer(c, kt):
                lines_in(c, page(250, 300, 200, 270), t, T_TREATY - 0.2, 0.5, WHITE, 1.8)
                ev(T_TREATY - 0.2, "paper", t, 350)
                label(c, "OUTER SPACE TREATY · 1967", 350, 620, t, T_TREATY + 0.1, 20, GLOW, a=kt)
                label(c, "NO ONE CAN OWN SPACE", 540, 360, t, T_OWN, 22, WHITE, "left", a=kt)
                label(c, "EVERY COUNTRY ANSWERS", 540, 400, t, T_ANSWERS, 22, WHITE, "left", a=kt)
                label(c, "FOR WHAT IT LAUNCHES", 540, 432, t, T_ANSWERS + 0.35, 22, WHITE, "left", a=kt)
        if t >= T_Q:                                                        # who owns what catches it?
            label(c, "WHO OWNS WHAT CATCHES IT?", CX, 230, t, T_CATCH - 0.3, 26, WHITE, a=a)


# ---------------------------------------------------------------- SURFACE
T_1771B, T_RIVERW = wd("then", "seventeen"), wd("then", "river.")
T_NOW2, T_2026, T_SUNW2 = ls("now2"), wd("now2", "twenty"), wd("now2", "sun.")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "Project Suncatcher, set for 1 Oct 2026: SiliconANGLE; DCD · up to 8x, <$200/kg: Google Research, 2025",
           "Starcloud-1 (H100, Nov 2025; Shakespeare, Dec 2025): CNBC · 88,000-satellite filing: Quartz",
           "Cromford Mill, 1771: Derwent Valley Mills · data centres 415 TWh (2024), 945 TWh (2030): IEA",
           "Three Mile Island restart for Microsoft: Constellation, Sep 2024",
           "SpaceX FCC filing for up to 1,000,000 satellites, 30 Jan 2026: SpaceNews",
           "~16,500 active satellites, Sep 2026: CelesTrak counts · China's 12 of 2,800: SpaceNews",
           "SpaceX rideshare ~$7,000/kg (2026) · Big Mac 219 g (McDonald's), $6.22 (The Economist)",
           "Outer Space Treaty, 1967, Articles II and VI · the 2040 section is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 820)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 820))
            bignum(c, t, "1771", 130, 560, 250, T_1771B)
            lines_in(c, wheel(560, 600, 130, t * 1.1), t, T_1771B + 0.3, 0.6, GLOW, 1.8)
            lines_in(c, river(330, 800, GROUND_Y - 30, t * 2.2), t, T_RIVERW - 0.1, 0.5, GLOW, 1.6)
            label(c, "THE MILL WENT TO THE RIVER", 560, 845, t, T_RIVERW, 20, GLOW, a=a)
            if t >= T_2026 - 0.05:
                bignum(c, t, "2026", 130, 1360, 250, T_2026 - 0.05)
                lines_in(c, sun(1600, 420, 50, t * 0.2), t, T_2026 + 0.3, 0.5, WHITE, 1.8)
                sat_at(c, 1330, 620, 230, ease(seg(t, T_2026 + 0.2, T_2026 + 0.8)), 0.0, lit=ease(seg(t, T_SUNW2 - 0.3, T_SUNW2 + 0.2)))
                label(c, "THE COMPUTER IS GOING TO THE SUN", 1360, 845, t, T_SUNW2 - 0.2, 20, GLOW, a=a)
                ev(T_2026 + 0.2, "form", t, 1330)
    if t >= T_SRC:
        ks = 1 - ease(seg(t, T_SRC + 7.6, T_SRC + 8.4))
        for k, s_ in enumerate(SOURCES):
            label(c, s_, 250, 250 + k * 50, t, T_SRC + 0.2 + (0 if k == 0 else 0.6 + 0.45 * (k - 1)),
                  24 if k == 0 else 20, GLOW if k == 0 else SOFT, align="left", a=ks, cps=17 if k == 0 else 45)


def end_time():
    return T_SRC + 8.6


def frame(c, t):
    cold_open(c, t)
    ground_scene(c, t)
    sky(c, t)
    filings(c, t)
    china(c, t)
    ticket(c, t)
    hard(c, t)
    ages(c, t)
    imagine(c, t)
    mirror(c, t)
