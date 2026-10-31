"""EP09 · THE LAUNDRY PROBLEM, the scenes: line art keyed to the script's line ids and George's words (engine.tl.word),
which the engine turns into characters.

  GROUND     a gold medal, 35 / 42; 630 contestants, 67 lit gold; a laundry-folding machine and $89M; it comes apart:
             bankrupt, never shipped; the exam (easy) against a T-shirt (hard)
  MECHANISM  1988 and Mind Children; the quote: a test paper for the adults, a one-year-old for seeing and moving; a line
             of age: an eye at 500 million years, a hand at 375 million, written numbers a sliver at the very end; one day
             on a clock, numbers in its last second; a hand filling with 17,000 points
  NOW        1997 and a chess king; a humanoid folding a towel, still news; the machine at $16,000; 2,600 Big Macs; a
             T-shirt it can't manage
  IDEA       two columns: new (numbers, chess, exams) against ancient (seeing, gripping, walking), and the swap
  IMAGINE    a small robot walking like a toddler; a care home, a kitchen, a building site; a person at work, the hands,
             the eyes and the room lit
  SURFACE    1997: the chess king | 2026: the laundry, still yours; the sources
"""
import math

import numpy as np
from matplotlib.path import Path as MPath

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, MID, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         points, stroke_polys, bignum, keys, morph_polys, mini_mac, figure, STAND, page, xform, roll, bump)

GROUND_Y = 800
TRAILS = []
GLINTS = []
RNG = np.random.default_rng(9)


# ---------------------------------------------------------------- things
def star(cx, cy, r, n=5):
    a = np.linspace(-math.pi / 2, 1.5 * math.pi, 2 * n + 1)
    rr = np.where(np.arange(2 * n + 1) % 2 == 0, r, 0.42 * r)
    return np.column_stack([cx + rr * np.cos(a), cy + rr * np.sin(a)])


def medal(cx, cy, r):
    """A medal on a ribbon, a star in the middle."""
    return [ellipse(cx, cy, r, r, 0, 360, 72), ellipse(cx, cy, 0.74 * r, 0.74 * r, 0, 360, 60), star(cx, cy, 0.45 * r),
            P([(cx - 0.4 * r, cy - 0.92 * r), (cx - 0.95 * r, cy - 2.3 * r), (cx - 0.45 * r, cy - 2.3 * r), (cx - 0.02 * r, cy - r)]),
            P([(cx + 0.4 * r, cy - 0.92 * r), (cx + 0.95 * r, cy - 2.3 * r), (cx + 0.45 * r, cy - 2.3 * r), (cx + 0.02 * r, cy - r)])]


SHIRT = [(-0.25, -0.62), (-0.55, -0.55), (-1.0, -0.2), (-0.8, 0.02), (-0.5, -0.18), (-0.5, 0.75), (0.5, 0.75), (0.5, -0.18),
         (0.8, 0.02), (1.0, -0.2), (0.55, -0.55), (0.25, -0.62)]


def tshirt(cx, cy, s):
    """A T-shirt laid flat (s = half its sleeve span)."""
    neck = [(cx + 0.25 * s * math.cos(a), cy - 0.62 * s + 0.16 * s * math.sin(a)) for a in np.linspace(0, math.pi, 14)]
    return [P([(cx + x * s, cy + y * s) for x, y in SHIRT] + neck[1:])]


def crumple(cx, cy, s, seed=0):
    """The same shirt half-folded and bunched up: the attempt that didn't work."""
    rng = np.random.default_rng(seed)
    base = [(-0.45, -0.5), (0.1, -0.62), (0.55, -0.4), (0.62, 0.1), (0.35, 0.5), (-0.2, 0.62), (-0.6, 0.35), (-0.7, -0.1)]
    pts = [(cx + (x + rng.uniform(-0.08, 0.08)) * s, cy + (y + rng.uniform(-0.08, 0.08)) * s) for x, y in base]
    inner = [(cx + x * s, cy + y * s) for x, y in ((-0.3, -0.2), (0.1, 0.05), (0.3, -0.25))]
    return [P(pts + pts[:1]), P(inner)]


def machine(cx, bot, s):
    """A laundry-folding machine: a tall cabinet, a drawer, a window with a shirt inside, a little screen."""
    w, h = 1.2 * s, 1.9 * s
    x0, y0 = cx - w / 2, bot - h
    return [mg.rrect_pts(x0, y0, w, h, 0.06 * s, 5), rect(x0 + 0.1 * w, bot - 0.25 * h, 0.8 * w, 0.18 * h),
            P([(cx - 0.12 * w, bot - 0.16 * h), (cx + 0.12 * w, bot - 0.16 * h)]),
            mg.rrect_pts(x0 + 0.1 * w, y0 + 0.12 * h, 0.8 * w, 0.5 * h, 0.03 * s, 4),
            rect(x0 + 0.62 * w, y0 + 0.035 * h, 0.26 * w, 0.05 * h)] + tshirt(cx, y0 + 0.37 * h, 0.28 * s)


def exam(cx, cy, s):
    """A marked exam paper: every answer ticked."""
    x, y, w, h = cx - 0.7 * s, cy - s, 1.4 * s, 2 * s
    out = page(x, y, w, h)
    for k in range(4):
        yy = y + (0.33 + 0.16 * k) * h
        out.append(P([(x + 0.74 * w, yy), (x + 0.8 * w, yy + 0.04 * h), (x + 0.92 * w, yy - 0.05 * h)]))
    return out


def book(cx, cy, w, h):
    return [rect(cx - w / 2, cy - h / 2, w, h), P([(cx - 0.4 * w, cy - h / 2), (cx - 0.4 * w, cy + h / 2)]),
            P([(cx - 0.25 * w, cy - 0.22 * h), (cx + 0.35 * w, cy - 0.22 * h)]), P([(cx - 0.25 * w, cy - 0.1 * h), (cx + 0.25 * w, cy - 0.1 * h)])]


def baby(cx, bot, s):
    """A one-year-old sitting up: a big head, a round body, short arms reaching, short legs."""
    hy = bot - 0.95 * s
    return [ellipse(cx, hy, 0.26 * s, 0.28 * s, 0, 360, 40), ellipse(cx, bot - 0.42 * s, 0.24 * s, 0.3 * s, 0, 360, 40),
            P([(cx - 0.2 * s, bot - 0.55 * s), (cx - 0.48 * s, bot - 0.72 * s)]), P([(cx + 0.2 * s, bot - 0.55 * s), (cx + 0.5 * s, bot - 0.66 * s)]),
            P([(cx - 0.15 * s, bot - 0.15 * s), (cx - 0.42 * s, bot), (cx - 0.55 * s, bot)]),
            P([(cx + 0.15 * s, bot - 0.15 * s), (cx + 0.42 * s, bot), (cx + 0.55 * s, bot)]),
            ellipse(cx - 0.09 * s, hy - 0.02 * s, 0.025 * s, 0.025 * s, 0, 360, 10), ellipse(cx + 0.09 * s, hy - 0.02 * s, 0.025 * s, 0.025 * s, 0, 360, 10)]


def eye(cx, cy, s):
    u = np.linspace(-1, 1, 40)
    top = np.column_stack([cx + s * u, cy - 0.55 * s * np.cos(u * math.pi / 2)])
    bot = np.column_stack([cx - s * u, cy + 0.45 * s * np.cos(u * math.pi / 2)])
    return [np.vstack([top, bot, top[:1]]), ellipse(cx, cy, 0.36 * s, 0.36 * s, 0, 360, 40), ellipse(cx, cy, 0.14 * s, 0.14 * s, 0, 360, 24)]


def hand_outline(cx, cy, s):
    """An open right hand, palm towards us, as one closed outline (s = about its height; (cx, cy) the palm)."""
    fingers = [(-0.235, -0.2, -0.74, 0.075), (-0.07, -0.21, -0.84, 0.075), (0.095, -0.2, -0.78, 0.072), (0.25, -0.15, -0.6, 0.065)]
    pts = [(-0.32, 0.5), (-0.36, 0.12), (-0.5, -0.02), (-0.62, -0.16)]
    pts += [(-0.67 + 0.075 * math.cos(a), -0.2 + 0.075 * math.sin(a)) for a in np.linspace(0.8 * math.pi, 1.95 * math.pi, 9)]
    pts += [(-0.5, -0.19), (-0.33, -0.17)]
    for fx, fy0, fy1, r in fingers:
        pts += [(fx - r, fy0), (fx - r, fy1)]
        pts += [(fx + r * math.cos(a), fy1 + r * math.sin(a)) for a in np.linspace(math.pi, 2 * math.pi, 10)]
        pts += [(fx + r, fy0)]
    pts += [(0.33, 0.1), (0.32, 0.5), (-0.32, 0.5)]
    return P([(cx + x * s, cy + y * s) for x, y in pts])


def king(cx, bot, s):
    """A chess king: base, body, collar, crown and cross."""
    pts = [(-0.55, 0), (-0.55, -0.12), (-0.4, -0.18), (-0.3, -0.25), (-0.22, -0.75), (-0.35, -0.8), (-0.35, -0.88), (-0.25, -0.92),
           (-0.3, -1.1), (0.3, -1.1), (0.25, -0.92), (0.35, -0.88), (0.35, -0.8), (0.22, -0.75), (0.3, -0.25), (0.4, -0.18), (0.55, -0.12),
           (0.55, 0), (-0.55, 0)]
    return [P([(cx + x * s, bot + y * s) for x, y in pts]), P([(cx, bot - 1.1 * s), (cx, bot - 1.45 * s)]),
            P([(cx - 0.13 * s, bot - 1.3 * s), (cx + 0.13 * s, bot - 1.3 * s)])]


def clock(cx, cy, r):
    """A 24-hour dial: the rim and the hours."""
    out = [ellipse(cx, cy, r, r, 0, 360, 96)]
    for k in range(24):
        a = -math.pi / 2 + k * 2 * math.pi / 24
        r0 = r * (0.8 if k % 6 == 0 else 0.88)
        out.append(P([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))]))
    return out


def basket(cx, bot, s):
    out = [P([(cx - s, bot - 0.7 * s), (cx + s, bot - 0.7 * s), (cx + 0.8 * s, bot), (cx - 0.8 * s, bot), (cx - s, bot - 0.7 * s)])]
    for k in range(1, 4):
        f = lerp(1.0, 0.8, k / 4)
        out.append(P([(cx - f * s, bot - 0.7 * s + 0.175 * k * s), (cx + f * s, bot - 0.7 * s + 0.175 * k * s)]))
    return out


def bed(cx, bot, s):
    return [P([(cx - s, bot), (cx - s, bot - 0.75 * s)]), P([(cx + s, bot), (cx + s, bot - 0.5 * s)]),
            rect(cx - s, bot - 0.45 * s, 2 * s, 0.18 * s), mg.rrect_pts(cx - 0.92 * s, bot - 0.62 * s, 0.38 * s, 0.17 * s, 0.05 * s, 4),
            P([(cx - 0.5 * s, bot - 0.45 * s), (cx - 0.3 * s, bot - 0.62 * s), (cx + 0.9 * s, bot - 0.6 * s), (cx + 0.95 * s, bot - 0.45 * s)])]


def stove(cx, bot, s):
    out = [rect(cx - 0.7 * s, bot - 0.9 * s, 1.4 * s, 0.9 * s), rect(cx - 0.5 * s, bot - 0.6 * s, s, 0.45 * s)]
    out += [ellipse(cx + dx * s, bot - 0.93 * s, 0.2 * s, 0.05 * s, 0, 360, 24) for dx in (-0.33, 0.33)]
    out += [rect(cx - 0.55 * s, bot - 1.22 * s, 0.44 * s, 0.26 * s), P([(cx - 0.11 * s, bot - 1.15 * s), (cx + 0.3 * s, bot - 1.25 * s)])]
    return out


def crane(cx, bot, s):
    out = [P([(cx - 0.1 * s, bot), (cx - 0.1 * s, bot - 1.6 * s)]), P([(cx + 0.1 * s, bot), (cx + 0.1 * s, bot - 1.6 * s)])]
    for k in range(8):
        out.append(P([(cx - 0.1 * s, bot - k * 0.2 * s), (cx + 0.1 * s, bot - (k + 1) * 0.2 * s)]))
    out += [P([(cx - 0.5 * s, bot - 1.6 * s), (cx + 1.1 * s, bot - 1.6 * s)]), P([(cx - 0.5 * s, bot - 1.6 * s), (cx, bot - 1.85 * s), (cx + 1.1 * s, bot - 1.6 * s)]),
            P([(cx + 0.9 * s, bot - 1.6 * s), (cx + 0.9 * s, bot - 1.05 * s)]), rect(cx + 0.78 * s, bot - 1.05 * s, 0.24 * s, 0.16 * s)]
    return out


def walk(t, t0, sway=1.0):
    """A toddler's walk: short steps, arms out for balance, a wobble."""
    ph = 2 * math.pi * 1.4 * (t - t0)
    return dict(lean=5 * sway * math.sin(ph / 2), head=4 * math.sin(ph / 2 + 1), ls=55, le=-25, rs=-55 + 5 * math.sin(ph), re=25,
                lh=18 * math.sin(ph), lk=-12 * max(0, math.sin(ph)), rh=-18 * math.sin(ph), rk=-12 * max(0, -math.sin(ph)))


# fixed crowds and fills
GRID = np.array([(460 + 1000 * (i % 35) / 34, 360 + 380 * (i // 35) / 17) for i in range(630)])
GOLDS = np.sort(RNG.choice(630, 67, replace=False))
HAND_C, HAND_S = (700.0, 520.0), 470.0
HAND = hand_outline(*HAND_C, HAND_S)


def _fill_hand(n=17000):
    """17,000 points in the hand, denser towards the fingertips (as the nerve fibres are)."""
    path = MPath(HAND)
    x0, y0 = HAND.min(0)
    x1, y1 = HAND.max(0)
    out = []
    rng = np.random.default_rng(17)
    while len(out) < n:
        q = np.column_stack([rng.uniform(x0, x1, 40000), rng.uniform(y0, y1, 40000)])
        q = q[path.contains_points(q)]
        w = np.where(q[:, 1] < HAND_C[1] - 0.45 * HAND_S, 1.0, 0.45)
        q = q[rng.random(len(q)) < w]
        out.extend(q.tolist())
    pts = np.array(out[:n])
    return pts[np.argsort(-pts[:, 1] + rng.normal(0, 40, n))]           # they light from the wrist upwards


HAND_PTS = _fill_hand()


# ---------------------------------------------------------------- GROUND
T_GOLD, T_OLY = wd("gold", "gold"), wd("gold", "olympiad")
T_FEW0, T_67, T_SAME = ls("few"), wd("few", "sixtyseven"), wd("few", "same")
T_LAU0, T_89, T_MACH = ls("laundry"), wd("laundry", "eightynine"), wd("laundry", "machine")
T_BUST0, T_BANK, T_NEVER = ls("bust"), wd("bust", "bankrupt"), wd("bust", "never")
T_WHY0, T_EXAM, T_EASY, T_LAUW, T_HARD = ls("why"), wd("why", "exam"), wd("why", "easy"), wd("why", "laundry"), wd("why", "hard")
T_MOR = ls("moravec")


def ground(c, t):
    a = win(t, 1.0, T_MOR + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kg = win(t, 1.0, T_LAU0 + 0.2, 0.3, 0.5)
        if kg > 0:                                                          # gold, then 67 of 630
            with layer(c, kg):
                km = 1 - ease(seg(t, T_FEW0 - 0.2, T_FEW0 + 0.3))
                if km > 0:
                    with layer(c, km):
                        lines_in(c, medal(CX, 600, 120), t, T_GOLD - 0.6, 0.7, GOLD, 2.0)
                        ev(T_GOLD - 0.6, "form", t, CX)
                        bignum(c, t, "35 / 42", 120, CX, 250, wd("gold", "scored") - 0.2)
                        label(c, "GOLD · INTERNATIONAL MATHEMATICAL OLYMPIAD · JULY 2025", CX, 830, t, T_OLY - 0.4, 22, SOFT, a=a * kg * km)
                if t >= T_FEW0 - 0.2:
                    kf = ease(seg(t, T_FEW0 - 0.2, T_FEW0 + 0.4))
                    points(c, GRID, 0.35 * kf, SOFT, 5.0)
                    n = int(67 * ease(seg(t, T_67 - 0.1, T_67 + 1.1)))
                    if n:
                        points(c, GRID[GOLDS[:n]], kf, GOLD, 9.0)
                        ev(T_67 - 0.1, "grains", t, CX)
                    label(c, "630 CONTESTANTS", CX, 300, t, T_FEW0 + 0.3, 22, SOFT, a=a * kg)
                    label(c, "67 WON GOLD", CX, 820, t, T_SAME - 0.4, 26, GOLD, a=a * kg)
        kl = win(t, T_LAU0 - 0.2, T_WHY0 + 0.2, 0.3, 0.4)
        if kl > 0:                                                          # the machine, the money, the collapse
            with layer(c, kl):
                bignum(c, t, "$89M", 120, CX, 230, T_89 - 0.1)
                label(c, "RAISED FOR A LAUNDRY-FOLDING MACHINE", CX, 330, t, T_89 + 0.5, 22, SOFT, a=a * kl)
                parts = machine(CX, GROUND_Y, 220)
                kb = ease(seg(t, T_BANK - 0.1, T_BANK + 1.3), "i")
                if kb > 0:                                                  # it comes apart and falls
                    rng = np.random.default_rng(3)
                    parts = [xform([q], rng.uniform(-160, 160) * kb, 380 * kb ** 2 * rng.uniform(0.4, 1.0), 1.0, rng.uniform(-0.6, 0.6) * kb,
                                   tuple(q.mean(0)))[0] for q in parts]
                    ev(T_BANK - 0.1, "glitch", t, CX)
                lines_in(c, parts, t, T_MACH - 0.4, 0.7, WHITE, 1.8)
                ev(T_MACH - 0.4, "form", t, CX)
                label(c, "BANKRUPT · 2019", 1440, 520, t, T_BANK, 30, WHITE, a=a * kl)
                label(c, "NEVER SHIPPED", 1440, 580, t, T_NEVER, 24, GLOW, a=a * kl)
                ev(T_NEVER, "thud", t, CX)
        if t >= T_WHY0 - 0.2:                                               # the exam against the shirt
            kw = ease(seg(t, T_WHY0 - 0.2, T_WHY0 + 0.3))
            with layer(c, kw):
                lines_in(c, exam(620, 520, 150), t, T_EXAM - 0.3, 0.5, WHITE, 1.8)
                label(c, "THE EXAM", 620, 250, t, T_EXAM, 22, SOFT, a=a * kw)
                label(c, "EASY", 620, 790, t, T_EASY, 30, GLOW, a=a * kw)
                lines_in(c, tshirt(1300, 520, 190), t, T_LAUW - 0.3, 0.5, WHITE, 1.9)
                label(c, "THE LAUNDRY", 1300, 250, t, T_LAUW, 22, SOFT, a=a * kw)
                label(c, "HARD", 1300, 790, t, T_HARD, 30, WHITE, a=a * kw)
                ev(T_EXAM - 0.3, "paper", t, 620)
                ev(T_LAUW - 0.3, "whoosh", t, 1300)


# ---------------------------------------------------------------- MECHANISM
T_1988, T_HANS = wd("moravec", "nineteen"), wd("moravec", "hans")
T_Q0, T_QEASY, T_ADULT, T_DIFF, T_ONE, T_SEE = (ls("quote"), wd("quote", "easy"), wd("quote", "adults"), wd("quote", "difficult"),
                                                 wd("quote", "oneyearold"), wd("quote", "seeing"))
T_AGE0, T_AGE = ls("age"), wd("age", "age.")
T_EYES0, T_EYESEE, T_500 = ls("eyes"), wd("eyes", "seeing"), wd("eyes", "five")
T_LIMBS0, T_375 = ls("limbs"), wd("limbs", "three")
T_NUM0, T_5K = ls("numbers"), wd("numbers", "five")
T_DAY0, T_DAYW, T_LAST, T_SEC = ls("day"), wd("day", "day,"), wd("day", "last"), wd("day", "second.")
T_HAND0, T_PALM, T_17K, T_FOLD = ls("hand"), wd("hand", "palm"), wd("hand", "seventeen"), wd("hand", "fold")
T_CHESS0 = ls("chess")
AX_Y, AX0, AX1 = 640, 200, 1720


def ax_x(years_ago):
    return AX1 - (AX1 - AX0) * years_ago / 500e6


def mechanism(c, t):
    a = win(t, T_MOR - 0.05, T_CHESS0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kq = win(t, T_MOR - 0.05, T_AGE0 + 0.1, 0.3, 0.4)
        if kq > 0:                                                          # 1988; the quote: easy against impossible
            with layer(c, kq):
                kmv = 1 - ease(seg(t, T_Q0 - 0.2, T_Q0 + 0.3))
                if kmv > 0:
                    with layer(c, kmv):
                        bignum(c, t, "1988", 130, CX, 250, T_1988)
                        lines_in(c, book(CX, 580, 240, 320), t, T_MOR + 0.4, 0.6, WHITE, 1.8)
                        label(c, "MIND CHILDREN", CX + 12, 540, t, T_HANS + 0.3, 20, GLOW, a=a * kq * kmv)
                        label(c, "HANS MORAVEC · ROBOTICIST", CX, 800, t, T_HANS, 22, SOFT, a=a * kq * kmv)
                if t >= T_Q0 - 0.2:
                    kk = ease(seg(t, T_Q0 - 0.2, T_Q0 + 0.3))
                    with layer(c, kk):
                        lines_in(c, exam(560, 500, 150), t, T_QEASY - 0.3, 0.5, WHITE, 1.8)
                        label(c, "ADULT-LEVEL TEST SCORES", 560, 250, t, T_ADULT - 0.2, 22, SOFT, a=a * kq)
                        label(c, "COMPARATIVELY EASY", 560, 780, t, T_QEASY, 24, GLOW, a=a * kq)
                        lines_in(c, baby(1360, 700, 300), t, T_ONE - 0.4, 0.6, WHITE, 1.9)
                        label(c, "THE SKILLS OF A ONE-YEAR-OLD", 1360, 250, t, T_ONE, 22, SOFT, a=a * kq)
                        label(c, "DIFFICULT OR IMPOSSIBLE", 1360, 780, t, T_DIFF, 24, WHITE, a=a * kq)
                        label(c, "SEEING · MOVING", 1360, 830, t, T_SEE, 20, GLOW, a=a * kq)
                        ev(T_ONE - 0.4, "form", t, 1360)
        kt = win(t, T_AGE0 - 0.1, T_DAY0 + 0.4, 0.3, 0.5)
        if kt > 0:                                                          # the line of age
            with layer(c, kt):
                lines_in(c, [P([(AX0, AX_Y), (AX1, AX_Y)])] + [P([(ax_x(y), AX_Y - 10), (ax_x(y), AX_Y + 10)]) for y in (500e6, 400e6, 300e6, 200e6, 100e6)],
                         t, T_AGE0, 0.8, SOFT, 1.6, seed_pt=(AX0, AX_Y))
                label(c, "500 MILLION YEARS AGO", AX0, AX_Y + 50, t, T_AGE0 + 0.3, 20, SOFT, "left", a=a * kt)
                label(c, "NOW", AX1, AX_Y + 50, t, T_AGE0 + 0.5, 20, SOFT, "right", a=a * kt)
                label(c, "AGE", CX, 250, t, T_AGE - 0.1, 30, WHITE, a=a * kt * (1 - ease(seg(t, T_EYES0 - 0.2, T_EYES0))))
                ev(T_AGE0, "scan", t, CX)
                if t >= T_EYESEE - 0.3:                                     # eyes, 500 million years
                    lines_in(c, eye(ax_x(500e6) + 70, AX_Y - 110, 70), t, T_EYESEE - 0.3, 0.5, WHITE, 1.9)
                    c.drawCircle(ax_x(500e6), AX_Y, 8, mg.fill(GLOW, 0.95 * a * kt))
                    label(c, "SEEING", ax_x(500e6) + 70, AX_Y - 200, t, T_EYESEE, 20, GLOW, a=a * kt)
                    ev(T_EYESEE - 0.3, "latch", t, ax_x(500e6))
                if t < T_5K - 0.05:
                    bignum(c, t, "500,000,000", 100, CX, 250, T_500 - 0.1)
                    label(c, "YEARS OF SEEING", CX, 330, t, T_500 + 0.6, 22, SOFT, a=a * kt)
                else:
                    roll(c, "500,000,000", "5,000", 100, CX, 250, t, T_500 - 0.1, T_5K - 0.1)
                    label(c, "YEARS OF WRITTEN NUMBERS", CX, 330, t, T_5K + 0.5, 22, GLOW, a=a * kt)
                if t >= T_LIMBS0 - 0.1:                                     # limbs, 375 million
                    x = ax_x(375e6)
                    lines_in(c, [hand_outline(x, AX_Y - 120, 150)], t, T_LIMBS0 - 0.1, 0.5, WHITE, 1.9)
                    c.drawCircle(x, AX_Y, 8, mg.fill(GLOW, 0.95 * a * kt))
                    label(c, "GRIPPING · WALKING", x, AX_Y - 230, t, T_LIMBS0 + 0.2, 20, GLOW, a=a * kt)
                    label(c, "375 MILLION", x, AX_Y + 50, t, T_375, 20, WHITE, a=a * kt)
                    ev(T_LIMBS0 - 0.1, "latch", t, x)
                if t >= T_NUM0 - 0.1:                                       # written numbers: a sliver at the end
                    kn = ease(seg(t, T_NUM0 - 0.1, T_NUM0 + 0.4))
                    stroke_polys(c, [ellipse(1600, 460, 90, 90, 0, 360, 60), P([(1664, 524), (AX1 - 4, AX_Y - 6)])], GLOW, 1.8, kn)
                    c.drawCircle(AX1 - 1, AX_Y, 6, mg.fill(WHITE, a * kt * kn))
                    label(c, "1 2 3", 1600, 470, t, T_NUM0 + 0.2, 26, WHITE, a=a * kt)
                    label(c, "WRITTEN NUMBERS", 1600, 330 + 60, t, T_5K + 0.2, 18, GLOW, a=a * kt * 0)
                    ev(T_NUM0 - 0.1, "pop", t, 1600)
        if t >= T_DAY0 - 0.2:                                               # one day: numbers in its last second
            kd = win(t, T_DAY0 - 0.2, T_HAND0 + 0.2, 0.4, 0.4)
            with layer(c, kd):
                lines_in(c, clock(CX, 520, 250), t, T_DAY0, 0.6, WHITE, 1.8)
                sweep = ease(seg(t, T_DAYW - 0.2, T_LAST + 0.2), "io")
                ang = -math.pi / 2 + 2 * math.pi * sweep
                c.drawLine(CX, 520, CX + 215 * math.cos(ang), 520 + 215 * math.sin(ang), mg.stroke(GLOW, 3.0, a * kd))
                c.drawCircle(CX, 520, 8, mg.fill(GLOW, a * kd))
                label(c, "FIRST EYES · 00:00", CX, 230, t, T_DAY0 + 0.4, 20, SOFT, a=a * kd)
                fl = bump(t, T_LAST - 0.1, T_SEC, T_SEC + 1.2)
                if fl > 0:
                    c.drawCircle(CX, 520 - 250, 16, mg.fill(WHITE, fl * a * kd))
                label(c, "WRITTEN NUMBERS: THE LAST SECOND", CX, 830, t, T_SEC - 0.3, 24, WHITE, a=a * kd)
                ev(T_SEC - 0.1, "tick", t, CX)
        if t >= T_HAND0 - 0.2:                                              # 17,000 points in a hand
            kh = ease(seg(t, T_HAND0 - 0.2, T_HAND0 + 0.3))
            with layer(c, kh):
                lines_in(c, [HAND], t, T_PALM - 0.4, 0.7, WHITE, 1.9)
                n = int(len(HAND_PTS) * ease(seg(t, T_17K - 0.2, T_17K + 1.8), "io"))
                glow = 0.55 + 0.4 * bump(t, T_FOLD - 0.2, T_FOLD + 0.2, T_FOLD + 1.0)
                points(c, HAND_PTS[:n], glow, GLOW, 1.8)
                bignum(c, t, "17,000", 120, 1420, 400, T_17K - 0.1)
                label(c, "TOUCH NERVE FIBRES", 1420, 500, t, T_17K + 0.6, 22, SOFT, a=a * kh)
                label(c, "THE PALM SIDE OF ONE HAND", 1420, 540, t, T_17K + 0.9, 20, SOFT, a=a * kh)
                label(c, "EVERY FOLD OF THE FABRIC", 1420, 640, t, T_FOLD, 22, GLOW, a=a * kh)
                ev(T_17K - 0.2, "grains", t, 700)


# ---------------------------------------------------------------- NOW
T_1997, T_BEAT = wd("chess", "nineteen"), wd("chess", "beat")
T_TOW0, T_AUG, T_FOLDING, T_NEWS = ls("towels"), wd("towels", "august"), wd("towels", "folding"), wd("towels", "news.")
T_PRICE0, T_16K = ls("price"), wd("price", "sixteen")
T_MACS0, T_2600, T_BIG, T_STRUG = ls("macs"), wd("macs", "two"), wd("macs", "big"), wd("macs", "struggled")
T_IDEA = ls("idea")
TOWEL_POSE = dict(lean=6, head=8, ls=78, le=18, rs=62, re=30, lh=4, lk=0, rh=-4, rk=0)


def now(c, t):
    a = win(t, T_CHESS0 - 0.05, T_IDEA + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kc = win(t, T_CHESS0 - 0.05, T_TOW0 + 0.2, 0.3, 0.4)
        if kc > 0:                                                          # 1997 and a chess king
            with layer(c, kc):
                bignum(c, t, "1997", 130, CX, 250, T_1997)
                lines_in(c, king(CX, 780, 270), t, T_CHESS0 + 0.3, 0.7, WHITE, 2.0)
                label(c, "DEEP BLUE BEATS KASPAROV", CX, 840, t, T_BEAT, 22, GLOW, a=a * kc)
                ev(T_CHESS0 + 0.3, "form", t, CX)
                ev(T_BEAT, "thock", t, CX)
        kt = win(t, T_TOW0 - 0.1, T_PRICE0 + 0.2, 0.3, 0.4)
        if kt > 0:                                                          # a humanoid folds a towel: still news
            with layer(c, kt):
                bignum(c, t, "AUG 2025", 110, CX, 230, T_AUG)
                body, j = figure(760, 660, 440, TOWEL_POSE, 1, robot=True)
                lines_in(c, body, t, T_TOW0 + 0.2, 0.7, WHITE, 1.8)
                hx = (j["lhand"][0] + j["rhand"][0]) / 2 + 40
                hy = (j["lhand"][1] + j["rhand"][1]) / 2
                f1 = ease(seg(t, T_FOLDING - 0.1, T_FOLDING + 0.7))
                f2 = ease(seg(t, T_FOLDING + 0.9, T_FOLDING + 1.6))
                w = lerp(lerp(360, 180, f1), 90, f2)
                h = lerp(220, 120, f2)
                stroke_polys(c, [rect(hx - 20, hy - 30, w, h), P([(hx - 20 + w * 0.5, hy - 30), (hx - 20 + w * 0.5, hy - 30 + h)])], GLOW, 2.0,
                             ease(seg(t, T_FOLDING - 0.6, T_FOLDING - 0.2)))
                label(c, "A HUMANOID FOLDS TOWELS ON ITS OWN", 1400, 720, t, T_FOLDING, 20, SOFT, a=a * kt)
                label(c, "STILL NEWS", 1400, 790, t, T_NEWS - 0.1, 30, WHITE, a=a * kt)
                ev(T_TOW0 + 0.2, "servo", t, 760)
                ev(T_FOLDING + 0.1, "paper", t, 1100)
        if t >= T_PRICE0 - 0.1:                                             # $16,000, then 2,600 Big Macs
            kp = ease(seg(t, T_PRICE0 - 0.1, T_PRICE0 + 0.4))
            with layer(c, kp):
                km = 1 - ease(seg(t, T_STRUG - 0.3, T_STRUG + 0.2))
                if t < T_2600 - 0.05:
                    bignum(c, t, "$16,000", 120, CX, 230, T_16K - 0.1)
                    label(c, "THE LAUNDRY MACHINE'S PLANNED PRICE", CX, 320, t, T_16K + 0.5, 22, SOFT, a=a * kp)
                else:
                    roll(c, "$16,000", "2,600", 120, CX, 230, t, T_16K - 0.1, T_2600 - 0.1)
                    label(c, "BIG MACS", CX, 320, t, T_BIG, 24, GLOW, a=a * kp)
                with layer(c, 1 - ease(seg(t, T_2600 - 0.3, T_2600 + 0.1))):
                    lines_in(c, machine(CX, GROUND_Y, 190), t, T_PRICE0, 0.6, WHITE, 1.8)
                if t >= T_2600 - 0.3:                                       # a grid of Big Macs, 100 each
                    for k in range(26):
                        tk = T_2600 - 0.2 + 0.035 * k
                        if t >= tk:
                            mini_mac(c, 520 + 70 * (k % 13), 440 + 90 * (k // 13), 24, km * ease(seg(t, tk, tk + 0.2)))
                            ev(tk, "tick", t, 520 + 70 * (k % 13))
                    label(c, "EACH = 100", CX, 650, t, T_BIG + 0.3, 18, SOFT, a=a * kp * km)
                if t >= T_STRUG - 0.3:                                      # and a T-shirt it can't manage
                    ks = ease(seg(t, T_STRUG - 0.3, T_STRUG + 0.1))
                    wob = 0.5 - 0.5 * math.cos(2 * math.pi * seg(t, T_STRUG, T_STRUG + 3.0) * 2)
                    with layer(c, ks):
                        morph_polys(c, tshirt(CX, 600, 170), crumple(CX, 600, 200, int(t * 3) % 4), 0.85 * wob, WHITE)
                        label(c, "IT STRUGGLED WITH AN ORDINARY T-SHIRT", CX, 830, t, T_STRUG + 0.1, 22, GLOW, a=a * kp * ks)
                        ev(T_STRUG, "glitch", t, CX)


# ---------------------------------------------------------------- IDEA
T_CLEVER, T_RECENT = wd("idea", "clever"), wd("idea", "recently")
T_FLIP0, T_NEW, T_EFF, T_ANC, T_COPY = ls("flip"), wd("flip", "new."), wd("flip", "effortless"), wd("flip", "ancient,"), wd("flip", "copy.")
T_IMAGINE = ls("imagine")


def idea(c, t):
    a = win(t, T_IDEA - 0.05, T_IMAGINE + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "DIFFICULTY = HOW RECENTLY WE LEARNED IT", CX, 200, t, T_RECENT - 0.3, 26, WHITE, a=a)
        lines_in(c, [P([(CX, 260), (CX, 820)])], t, T_IDEA + 0.2, 0.5, SOFT, 1.4, seed_pt=(CX, 260))
        lnew = 1.0 if t < T_NEW - 0.2 else 0.6 + 0.4 * bump(t, T_NEW - 0.2, T_NEW + 0.2, T_EFF)
        lold = 0.6 + 0.4 * ease(seg(t, T_ANC - 0.2, T_ANC + 0.3))
        with layer(c, lnew):
            label(c, "NEW", 560, 300, t, T_IDEA + 0.3, 30, GLOW, a=a)
            lines_in(c, exam(430, 500, 90), t, T_IDEA + 0.5, 0.5, WHITE, 1.8)
            lines_in(c, king(690, 610, 170), t, T_IDEA + 0.7, 0.5, WHITE, 1.8)
            label(c, "NUMBERS · CHESS · EXAMS", 560, 700, t, T_IDEA + 0.9, 20, SOFT, a=a)
            label(c, "HARD FOR US · EASY FOR MACHINES", 560, 780, t, T_CLEVER, 20, WHITE, a=a)
        with layer(c, lold):
            label(c, "ANCIENT", 1360, 300, t, T_IDEA + 0.6, 30, GLOW, a=a)
            lines_in(c, eye(1190, 480, 80), t, T_IDEA + 0.8, 0.5, WHITE, 1.8)
            lines_in(c, [hand_outline(1370, 520, 170)], t, T_IDEA + 1.0, 0.5, WHITE, 1.8)
            body, _ = figure(1540, 560, 200, STAND, -1)
            lines_in(c, body, t, T_IDEA + 1.2, 0.5, WHITE, 1.8)
            label(c, "SEEING · GRIPPING · WALKING", 1360, 700, t, T_IDEA + 1.4, 20, SOFT, a=a)
            label(c, "EASY FOR US · HARD FOR MACHINES", 1360, 780, t, T_CLEVER + 0.3, 20, WHITE, a=a)
        label(c, "ANCIENT IS THE HARDEST THING TO COPY", CX, 870 - 30, t, T_COPY - 0.4, 22, GLOW, a=a * ease(seg(t, T_COPY - 0.4, T_COPY)))
        ev(T_IDEA + 0.2, "scan", t, CX)
        ev(T_ANC - 0.1, "confirm", t, 1360)


# ---------------------------------------------------------------- IMAGINE
T_TODD, T_WHATIF = wd("imagine", "toddler."), ls("whatif")
T_WHERE0, T_ANY, T_CARE, T_KIT, T_BUILD = ls("where"), wd("where", "anything."), wd("where", "care"), wd("where", "kitchen?"), wd("where", "building")
T_YOU0, T_HANDS, T_EYESW, T_ROOM, T_OLD, T_LASTW = (ls("you"), wd("you", "hands,"), wd("you", "eyes"), wd("you", "room"), wd("you", "oldest"),
                                                     wd("you", "last"))
T_THEN = ls("then")
REACH = dict(lean=38, head=20, ls=80, le=10, rs=70, re=15, lh=10, lk=-20, rh=-10, rk=-15)


def imagine(c, t):
    a = win(t, T_IMAGINE - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        kr = win(t, T_IMAGINE - 0.05, T_YOU0 + 0.2, 0.3, 0.4)
        if kr > 0:                                                          # a robot that walks like a toddler
            with layer(c, kr):
                x = keys(t, [(T_IMAGINE, 820), (T_WHERE0, 1020), (T_ANY, 1060)])
                s = keys(t, [(T_WHERE0, 360), (T_CARE - 0.3, 240)])
                y = keys(t, [(T_WHERE0, 660), (T_CARE - 0.3, 668)])                 # feet on the icons' ground
                pose = walk(t, T_IMAGINE)
                kb = bump(t, T_ANY - 0.9, T_ANY - 0.2, T_ANY + 0.6)
                if kb > 0:                                                  # it bends to pick something up
                    pose = {k_: lerp(v, REACH[k_], kb) for k_, v in pose.items()}
                body, j = figure(x, y, s, pose, 1, robot=True)
                lines_in(c, body, t, T_IMAGINE + 0.2, 0.7, WHITE, 1.8)
                ball = (j["rhand"][0] + 6, j["rhand"][1] + 10) if kb > 0.6 or t > T_ANY else (x + 0.45 * s, y + 0.46 * s)
                stroke_polys(c, [ellipse(ball[0], ball[1], 0.04 * s, 0.04 * s, 0, 360, 20)], GLOW, 1.8, ease(seg(t, T_WHERE0, T_WHERE0 + 0.4)))
                label(c, "THE FIRST ROBOT THAT MOVES LIKE A TODDLER", CX, 230, t, T_TODD - 0.3, 22, WHITE,
                      a=a * kr * (1 - ease(seg(t, T_WHERE0 - 0.2, T_WHERE0 + 0.2))))
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 290, t, T_WHATIF + 0.05, 22, GLOW,
                      a=a * kr * (1 - ease(seg(t, T_WHERE0 - 0.2, T_WHERE0 + 0.2))))
                ev(T_IMAGINE + 0.2, "servo", t, x)
                if t >= T_CARE - 0.4:                                       # where it would change things
                    for tt, shape, xx, txt in ((T_CARE, bed(420, 780, 150), 420, "A CARE HOME"), (T_KIT, stove(CX - 140, 780, 150), CX - 140, "A KITCHEN"),
                                               (T_BUILD, crane(1380, 780, 170), 1470, "A BUILDING SITE")):
                        if t >= tt - 0.3:
                            lines_in(c, shape, t, tt - 0.3, 0.5, WHITE, 1.8)
                            label(c, txt, xx, 840, t, tt, 20, GLOW, a=a * kr)
                            ev(tt - 0.3, "latch", t, xx)
        if t >= T_YOU0 - 0.2:                                               # your oldest skills
            ky = ease(seg(t, T_YOU0 - 0.2, T_YOU0 + 0.3))
            with layer(c, ky):
                pose = dict(lean=4, head=6, ls=60, le=40, rs=48, re=50, lh=4, lk=0, rh=-4, rk=0)
                body, j = figure(860, 640, 440, pose, 1)
                lines_in(c, body + [rect(930, 560, 360, 18), P([(960, 578), (960, 800)]), P([(1260, 578), (1260, 800)])], t, T_YOU0, 0.7, WHITE, 1.8)
                for tt, (px, py), r, txt, lx, ly in ((T_HANDS, j["rhand"], 46, "HANDS", 1180, 520), (T_EYESW, j["head"], 50, "EYES", 1000, 250),
                                                    (T_ROOM, (900, 520), 330, "READING A ROOM", 1400, 330)):
                    if t >= tt - 0.2:
                        k = ease(seg(t, tt - 0.2, tt + 0.3))
                        stroke_polys(c, [ellipse(px, py, r * (0.8 + 0.2 * k), r * (0.8 + 0.2 * k), 0, 360, 48)], GLOW, 2.0, k)
                        label(c, txt, lx, ly, t, tt, 22, GLOW, a=a * ky)
                        ev(tt - 0.2, "confirm", t, px)
                label(c, "THE OLDEST SKILLS YOU HAVE", 1440, 640, t, T_OLD, 22, WHITE, a=a * ky)
                label(c, "MAY BE THE LAST TO GO", 1440, 690, t, T_LASTW, 22, SOFT, a=a * ky)


# ---------------------------------------------------------------- SURFACE
T_1997B, T_CHESSB = wd("then", "nineteen"), wd("then", "chess")
T_2026, T_LAUB, T_YOURS = wd("now2", "twenty"), wd("now2", "laundry"), wd("now2", "yours.")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "Google DeepMind, Gemini Deep Think at IMO 2025: 35 of 42; 67 of 630 contestants won gold",
           "Seven Dreamers (Laundroid): ~$89M raised, bankrupt April 2019, planned ~$16,000 (Engadget, Digital Trends)",
           "H. Moravec, Mind Children, 1988 · R. S. Johansson & Å. B. Vallbo, J. Physiol. 286, 1979: ~17,000 fibres",
           "Eyes: Cambrian, 500M+ years; limbs: ~375M years (Daeschler et al., Nature 2006); written numbers ~5,000 years",
           "Deep Blue beat Kasparov, May 1997 · Figure AI, Helix folding towels, 13 Aug 2025 · Big Mac $6.22, July 2026",
           "The section on a robot that moves like a toddler is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 820)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 820))
            bignum(c, t, "1997", 130, 560, 250, T_1997B)
            lines_in(c, king(560, 700, 190), t, T_1997B + 0.3, 0.6, WHITE, 1.8)
            label(c, "A MACHINE BEAT THE BEST CHESS PLAYER", 560, 790, t, T_CHESSB - 0.3, 20, GLOW, a=a)
            if t >= T_2026 - 0.05:
                bignum(c, t, "2026", 130, 1360, 250, T_2026 - 0.05)
                lines_in(c, basket(1360, 700, 150) + tshirt(1360, 500, 120), t, T_2026 + 0.2, 0.6, WHITE, 1.8)
                label(c, "THE LAUNDRY IS STILL YOURS", 1360, 790, t, T_YOURS - 0.5, 20, GLOW, a=a)
                ev(T_2026 + 0.2, "form", t, 1360)
    if t >= T_SRC:
        ks = 1 - ease(seg(t, T_SRC + 7.0, T_SRC + 7.8))
        for k, s_ in enumerate(SOURCES):
            label(c, s_, 250, 280 + k * 54, t, T_SRC + 0.2 + (0 if k == 0 else 0.6 + 0.45 * (k - 1)),
                  24 if k == 0 else 20, GLOW if k == 0 else SOFT, align="left", a=ks, cps=17 if k == 0 else 45)


def end_time():
    return T_SRC + 8.0


def frame(c, t):
    ground(c, t)
    mechanism(c, t)
    now(c, t)
    idea(c, t)
    imagine(c, t)
    mirror(c, t)
