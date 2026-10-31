"""EP10 · COUNTING SUMS, the scenes: line art keyed to the script's line ids and George's words (engine.tl.word), which
the engine turns into characters.

  GROUND     Europe's ring of stars and 10^25; not a test score (the paper crossed out) but sums pouring into a chip;
             the line across the screen, the models above it ringed; "why count sums?"
  MECHANISM  a model that doesn't exist yet (a dashed box and a question mark) against effort (a meter filling); the
             scaling line (more compute, more capable); the Earth and everyone on it: 39,000,000 years of sums
  NOW        California's line ten times higher; 390,000,000 years and a dinosaur; the compute for the same result
             halving bar by bar; a model growing under the line; Europe's line moving
  IDEA       1975, Goodhart: a target hit by an arrow; the target becomes the line, builders counting under it
  IMAGINE    a ration strip of sums; three labs with allowances trading, a price line like fuel's; two questions
  SURFACE    the danger (a question mark) | the sums (10^25); the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         points, stroke_polys, bignum, keys, chip, page, roll, bump, globe, burst)

TRAILS = []
GLINTS = []
RNG = np.random.default_rng(10)


# ---------------------------------------------------------------- things
def star(cx, cy, r, n=5):
    a = np.linspace(-math.pi / 2, 1.5 * math.pi, 2 * n + 1)
    rr = np.where(np.arange(2 * n + 1) % 2 == 0, r, 0.42 * r)
    return np.column_stack([cx + rr * np.cos(a), cy + rr * np.sin(a)])


def eu_ring(cx, cy, r, s=16):
    return [star(cx + r * math.cos(-math.pi / 2 + k * math.pi / 6), cy + r * math.sin(-math.pi / 2 + k * math.pi / 6), s) for k in range(12)]


def power(c, t, exp, size, cx, cy, t0):
    """10 to a power, as a big number with a raised exponent."""
    bignum(c, t, "10", size, cx - 0.45 * size, cy, t0)
    bignum(c, t, exp, 0.5 * size, cx + 0.72 * size, cy - 0.5 * size, t0 + 0.15)


def exam(cx, cy, s):
    x, y, w, h = cx - 0.7 * s, cy - s, 1.4 * s, 2 * s
    return page(x, y, w, h)


def cross(cx, cy, s):
    return [P([(cx - s, cy - s), (cx + s, cy + s)]), P([(cx + s, cy - s), (cx - s, cy + s)])]


def dashed_box(x, y, w, h, n=10):
    out = []
    for (x0, y0), (x1, y1) in (((x, y), (x + w, y)), ((x + w, y), (x + w, y + h)), ((x + w, y + h), (x, y + h)), ((x, y + h), (x, y))):
        for k in range(n):
            a0, a1 = k / n, (k + 0.55) / n
            out.append(P([(lerp(x0, x1, a0), lerp(y0, y1, a0)), (lerp(x0, x1, a1), lerp(y0, y1, a1))]))
    return out


def qmark(cx, cy, s):
    arc = np.column_stack([cx + 0.5 * s * np.cos(np.linspace(math.pi, 2.4 * math.pi, 30)), cy - 0.5 * s + 0.45 * s * np.sin(np.linspace(math.pi, 2.4 * math.pi, 30))])
    return [np.vstack([arc, [(cx, cy + 0.15 * s), (cx, cy + 0.35 * s)]]), ellipse(cx, cy + 0.62 * s, 0.07 * s, 0.07 * s, 0, 360, 16)]


def dino(cx, bot, s):
    """A long-necked dinosaur, side on, facing right."""
    pts = [(-1.0, -0.12), (-0.4, -0.4), (0.0, -0.46), (0.3, -0.36), (0.55, -0.9), (0.68, -1.0), (0.8, -0.96), (0.78, -0.9), (0.66, -0.88),
           (0.45, -0.3), (0.36, -0.05), (0.33, 0.3), (0.22, 0.3), (0.2, 0.02), (-0.2, 0.02), (-0.24, 0.3), (-0.36, 0.3), (-0.4, -0.02),
           (-0.7, -0.06), (-1.0, -0.12)]
    return [P([(cx + x * s, bot - 0.3 * s + y * s) for x, y in pts])]


def target(cx, cy, r):
    return [ellipse(cx, cy, r * k, r * k, 0, 360, 64) for k in (1.0, 0.7, 0.4, 0.12)]


def arrow(x0, y0, x1, y1):
    ang = math.atan2(y1 - y0, x1 - x0)
    head = [(x1 - 30 * math.cos(ang - 0.4), y1 - 30 * math.sin(ang - 0.4)), (x1, y1), (x1 - 30 * math.cos(ang + 0.4), y1 - 30 * math.sin(ang + 0.4))]
    tail = [(x0 + 26 * math.cos(ang + a), y0 + 26 * math.sin(ang + a)) for a in (2.6, math.pi, -2.6)]
    return [P([(x0, y0), (x1, y1)]), P(head), P([tail[0], (x0, y0), tail[2]])]


def lab(cx, bot, s):
    """A lab: a block with a sawtooth roof and a chip on the door."""
    out = [rect(cx - s, bot - 0.9 * s, 2 * s, 0.9 * s),
           P([(cx - s, bot - 0.9 * s)] + [(cx - s + (k + 1) * 0.5 * s, bot - (1.25 if k % 2 == 0 else 0.9) * s) for k in range(4)])]
    return out + chip(cx, bot - 0.42 * s, 0.22 * s)


def ration(cx, cy, w, h, n=6):
    """A ration strip: tickets divided by perforations."""
    out = [rect(cx - w / 2, cy - h / 2, w, h)]
    for k in range(1, n):
        x = cx - w / 2 + k * w / n
        out += [P([(x, cy - h / 2 + j * h / 10), (x, cy - h / 2 + (j + 0.5) * h / 10)]) for j in range(10)]
    return out


def chart(x0, y0, w, h, pts, k=1.0):
    q = np.array([(x0 + u * w, y0 - v * h) for u, v in pts])
    n = max(2, int(len(q) * k))
    return [P([(x0, y0 - h), (x0, y0), (x0 + w, y0)]), q[:n]]


SCALING = [(u, 0.08 + 0.84 * u ** 1.15 + 0.015 * math.sin(u * 9)) for u in np.linspace(0, 1, 30)]
MODELS = [(0.12, 0.2), (0.3, 0.33), (0.47, 0.5), (0.63, 0.62), (0.8, 0.78), (0.93, 0.9)]
PRICE = [(u, 0.45 + 0.25 * math.sin(u * 13) + 0.12 * math.sin(u * 31 + 1)) for u in np.linspace(0, 1, 80)]
_ANG = RNG.uniform(0, 2 * math.pi, 1400)
PEOPLE = np.column_stack([np.cos(_ANG), np.sin(_ANG)]) * RNG.uniform(1.05, 1.5, (1400, 1))     # everyone, around the Earth


# ---------------------------------------------------------------- GROUND
T_LINE0, T_WATCH, T_TEN, T_25 = ls("line"), wd("line", "watch:"), wd("line", "ten"), wd("line", "twentyfive.")
T_WHAT0, T_SCORE, T_CALC = ls("what"), wd("what", "score."), wd("what", "calculations")
T_ABOVE0, T_RISK = ls("above"), wd("above", "systemic")
T_WHY0 = ls("why")
T_CANT0 = ls("cant")
LINE_Y = 470


def ground(c, t):
    a = win(t, 1.0, T_CANT0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        k1 = 1 - ease(seg(t, T_WHAT0 - 0.2, T_WHAT0 + 0.3))
        if k1 > 0:                                                          # Europe and 10^25
            with layer(c, k1):
                lines_in(c, eu_ring(CX, 560, 170), t, T_LINE0 + 0.1, 0.8, GOLD, 1.8, seed_pt=(CX, 560))
                label(c, "EUROPE", CX, 570, t, T_LINE0 + 0.5, 24, GOLD, a=a * k1)
                power(c, t, "25", 130, CX, 250, T_TEN - 0.2)
                label(c, "THE CLOSEST WATCH", CX, 830, t, T_WATCH - 0.3, 22, SOFT, a=a * k1)
                ev(T_LINE0 + 0.1, "form", t, CX)
        kw = win(t, T_WHAT0 - 0.2, T_ABOVE0 + 0.2, 0.3, 0.4)
        if kw > 0:                                                          # not a score: sums into a chip
            with layer(c, kw):
                lines_in(c, exam(560, 500, 150), t, T_WHAT0, 0.5, WHITE, 1.8)
                stroke_polys(c, cross(560, 500, 130), GLOW, 3.0, ease(seg(t, T_SCORE - 0.3, T_SCORE)))
                label(c, "NOT A TEST SCORE", 560, 790, t, T_SCORE - 0.2, 22, SOFT, a=a * kw)
                lines_in(c, chip(1360, 500, 130), t, T_CALC - 0.4, 0.5, WHITE, 1.9)
                k = seg(t, T_CALC - 0.2, T_ABOVE0 + 0.2)
                for i in range(22):                                         # the sums pour in
                    u = (k * 2.2 + i / 22) % 1.0
                    if k <= 0 or u > 0.98:
                        continue
                    x = lerp(900, 1330, u)
                    y = 500 + 150 * math.sin(i * 1.7) * (1 - u)
                    label(c, "+×−÷"[i % 4], x, y + 8, t, -1, 22, GLOW, a=a * kw * (1 - u) * 0.9)
                label(c, "CALCULATIONS TO TRAIN IT", 1360, 790, t, T_CALC, 22, WHITE, a=a * kw)
                ev(T_CALC - 0.4, "grains", t, 1360)
        if t >= T_ABOVE0 - 0.2:                                             # the line and the models above it
            ka = ease(seg(t, T_ABOVE0 - 0.2, T_ABOVE0 + 0.3)) * (1 - ease(seg(t, T_CANT0 - 0.3, T_CANT0 + 0.1)))
            with layer(c, ka):
                lines_in(c, [P([(200, LINE_Y), (1720, LINE_Y)])], t, T_ABOVE0, 0.6, GLOW, 2.2, seed_pt=(200, LINE_Y))
                power(c, t, "25", 60, 330, LINE_Y - 60, T_ABOVE0 + 0.3)
                for i, (x, y, s) in enumerate(((560, 680, 44), (820, 650, 52), (1080, 690, 40), (700, 330, 58), (1180, 300, 62), (1480, 340, 54))):
                    lines_in(c, chip(x, y, s), t, T_ABOVE0 + 0.2 + 0.08 * i, 0.4, WHITE, 1.6)
                    if y < LINE_Y:
                        kr = ease(seg(t, T_RISK - 0.2, T_RISK + 0.3))
                        stroke_polys(c, [ellipse(x, y, 1.8 * s, 1.8 * s, 0, 360, 48)], GLOW, 2.0, kr)
                label(c, "PRESUMED SYSTEMIC RISK", CX, 200, t, T_RISK - 0.1, 24, WHITE, a=a * ka)
                ev(T_RISK - 0.2, "confirm", t, CX)
        if t >= T_WHY0 - 0.2:
            label(c, "WHY COUNT SUMS?", CX, 870 - 40, t, T_WHY0 + 0.2, 30, WHITE, a=a * (1 - ease(seg(t, T_CANT0 - 0.3, T_CANT0 + 0.1))))


# ---------------------------------------------------------------- MECHANISM
T_DANGER, T_EXISTS, T_EFFORT = wd("cant", "dangerous"), wd("cant", "exists."), wd("cant", "effort")
T_MORE0, T_COMPUTE, T_CAP, T_STANDS = ls("more"), wd("more", "compute"), wd("more", "capable"), wd("more", "stands")
T_SIZE0, T_EVERY0, T_ONE, T_39 = ls("size"), ls("everyone"), wd("everyone", "one"), wd("everyone", "thirtynine")
T_CAL0 = ls("cal")


def mechanism(c, t):
    a = win(t, T_CANT0 - 0.05, T_CAL0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kc = win(t, T_CANT0 - 0.05, T_MORE0 + 0.2, 0.3, 0.4)
        if kc > 0:                                                          # the danger can't be measured; the effort can
            with layer(c, kc):
                stroke_polys(c, dashed_box(400, 330, 320, 340), SOFT, 1.8, ease(seg(t, T_CANT0, T_CANT0 + 0.4)))
                lines_in(c, qmark(560, 480, 150), t, T_DANGER - 0.2, 0.5, WHITE, 2.2)
                label(c, "HOW DANGEROUS?", 560, 290, t, T_DANGER, 22, SOFT, a=a * kc)
                label(c, "IT DOESN'T EXIST YET", 560, 730, t, T_EXISTS - 0.3, 20, GLOW, a=a * kc)
                if t >= T_EFFORT - 0.4:
                    lines_in(c, [rect(1300, 330, 120, 340)], t, T_EFFORT - 0.4, 0.4, WHITE, 1.8)
                    h = 330 * ease(seg(t, T_EFFORT - 0.2, T_EFFORT + 1.2))
                    c.drawRect(skia.Rect.MakeXYWH(1305, 665 - h, 110, h), mg.chrome_paint(335, 665, 0.9))
                    label(c, "THE EFFORT THAT BUILT IT", 1360, 730, t, T_EFFORT, 20, GLOW, a=a * kc)
                    ev(T_EFFORT - 0.2, "riser", t, 1360)
        km = win(t, T_MORE0 - 0.1, T_SIZE0 + 0.3, 0.3, 0.4)
        if km > 0:                                                          # more compute, more capable
            with layer(c, km):
                stroke_polys(c, chart(460, 760, 1000, 460, SCALING, seg(t, T_MORE0, T_CAP + 0.3)), GLOW, 2.4, 1.0)
                for i, (u, v) in enumerate(MODELS):
                    tk = T_MORE0 + 0.4 + 0.25 * i
                    if t >= tk:
                        c.drawCircle(460 + 1000 * u, 760 - 460 * v, 10, mg.fill(WHITE, 0.95 * a * km))
                        ev(tk, "tick", t, 460 + 1000 * u)
                label(c, "TRAINING COMPUTE →", 1460, 810, t, T_COMPUTE, 20, SOFT, "right", a=a * km)
                label(c, "CAPABILITY", 460, 270, t, T_CAP - 0.2, 20, SOFT, "left", a=a * km)
                label(c, "EFFORT STANDS IN FOR DANGER", CX, 200, t, T_STANDS - 0.2, 24, WHITE, a=a * km)
        if t >= T_SIZE0 - 0.1:                                              # the Earth and everyone on it
            ke = ease(seg(t, T_SIZE0 - 0.1, T_SIZE0 + 0.4))
            with layer(c, ke):
                lines_in(c, globe(700, 520, 200, t * 0.15), t, T_SIZE0, 0.6, WHITE, 1.6)
                n = int(len(PEOPLE) * ease(seg(t, T_ONE - 0.3, T_ONE + 1.0)))
                points(c, np.column_stack([700 + 200 * PEOPLE[:n, 0], 520 + 200 * PEOPLE[:n, 1]]), 0.8, GOLD, 2.6)
                label(c, "HOW BIG IS THE NUMBER?", CX, 180, t, T_SIZE0 + 0.2, 22, SOFT, a=a * ke * (1 - ease(seg(t, T_EVERY0, T_EVERY0 + 0.3))))
                label(c, "EVERYONE ON EARTH · ONE SUM A SECOND", 700, 800, t, T_ONE - 0.2, 20, GOLD, a=a * ke)
                if t < T_CAL0 + 1.0:
                    bignum(c, t, "39,000,000", 100, 1380, 470, T_39 - 0.1)
                    label(c, "YEARS", 1380, 560, t, T_39 + 0.6, 26, WHITE, a=a * ke)
                ev(T_ONE - 0.3, "grains", t, 700)


# ---------------------------------------------------------------- NOW
T_CALW, T_SIGNED = wd("cal", "california"), wd("cal", "signed")
T_LAND0, T_390, T_DINO = ls("land"), wd("land", "three"), wd("land", "dinosaur.")
T_HALF0, T_FALL, T_EIGHT = ls("halves"), wd("halves", "falling."), wd("halves", "eight")
T_UNDER0, T_STAY = ls("under"), wd("under", "under")
T_MOVE0, T_COMM, T_MOVES = ls("move"), wd("move", "commission"), wd("move", "moves.")
T_GOOD0 = ls("goodhart")


def now(c, t):
    a = win(t, T_CAL0 - 0.05, T_GOOD0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kl = win(t, T_CAL0 - 0.05, T_HALF0 + 0.2, 0.3, 0.4)
        if kl > 0:                                                          # two lines; 390,000,000 years
            with layer(c, kl):
                lines_in(c, [P([(200, 700), (1000, 700)])], t, T_CAL0 + 0.1, 0.5, GLOW, 2.0, seed_pt=(200, 700))
                label(c, "EUROPE · 10^25", 220, 680, t, T_CAL0 + 0.3, 20, GLOW, "left", a=a * kl)
                y2 = keys(t, [(T_CALW - 0.2, 700), (T_CALW + 0.8, 380)])
                c.drawLine(200, y2, 1000, y2, mg.stroke(WHITE, 2.4, a * kl * ease(seg(t, T_CALW - 0.3, T_CALW))))
                label(c, "CALIFORNIA · 10^26 · TEN TIMES HIGHER", 220, y2 - 20, t, T_CALW + 0.4, 20, WHITE, "left", a=a * kl)
                label(c, "SB 53 · SIGNED 29 SEPTEMBER 2025", 220, y2 + 40, t, T_SIGNED, 18, SOFT, "left", a=a * kl)
                ev(T_CALW - 0.2, "whoosh", t, 600)
                if t >= T_LAND0 - 0.2:
                    roll(c, "39,000,000", "390,000,000", 90, 1400, 300, t, T_LAND0 - 0.2, T_390 - 0.1)
                    label(c, "YEARS OF SUMS", 1400, 380, t, T_390 + 0.6, 22, SOFT, a=a * kl)
                    lines_in(c, dino(1400, 760, 220), t, T_DINO - 0.9, 0.7, WHITE, 1.9)
                    label(c, "LONG BEFORE THE FIRST DINOSAUR", 1400, 820, t, T_DINO - 0.3, 20, GLOW, a=a * kl)
                    ev(T_DINO - 0.9, "form", t, 1400)
        kh = win(t, T_HALF0 - 0.1, T_UNDER0 + 0.2, 0.3, 0.4)
        if kh > 0:                                                          # the same result, half the compute, again and again
            with layer(c, kh):
                bignum(c, t, "8 MONTHS", 100, CX, 230, T_EIGHT - 0.2)
                label(c, "TO HALVE THE COMPUTE FOR THE SAME RESULT", CX, 320, t, T_EIGHT + 0.6, 22, SOFT, a=a * kh)
                for k in range(7):
                    tk = T_FALL - 0.2 + 0.45 * k
                    if t >= tk:
                        w = 900 / 2 ** k
                        c.drawRect(skia.Rect.MakeXYWH(510, 420 + 58 * k, w * ease(seg(t, tk, tk + 0.3)), 40), mg.chrome_paint(420 + 58 * k, 460 + 58 * k, 0.9))
                        ev(tk, "tick", t, 510 + w)
                label(c, "LANGUAGE MODELS · 2012–2023", CX, 870 - 30, t, T_FALL + 0.4, 20, SOFT, a=a * kh)
        if t >= T_UNDER0 - 0.2:                                             # more ability, still under the line; the line moves
            ku = ease(seg(t, T_UNDER0 - 0.2, T_UNDER0 + 0.3))
            with layer(c, ku):
                ly = keys(t, [(T_COMM - 0.2, 400), (T_MOVES + 0.2, 520)])
                c.drawLine(200, ly, 1720, ly, mg.stroke(GLOW, 2.4, a * ku))
                label(c, "THE LINE", 220, ly - 20, t, T_UNDER0, 20, GLOW, "left", a=a * ku)
                g = 0.6 + 0.9 * ease(seg(t, T_UNDER0, T_STAY + 0.6))
                stroke_polys(c, chip(CX, 640, 60 * g), WHITE, 1.8, 1.0)
                stroke_polys(c, [ellipse(CX, 640, 95 * g, 95 * g, 0, 360, 48)], GLOW, 1.6, 0.6 * ease(seg(t, T_UNDER0, T_STAY)))
                label(c, "MORE ABILITY · STILL UNDER THE LINE", CX, 830, t, T_STAY - 0.2, 22, WHITE, a=a * ku * (1 - ease(seg(t, T_MOVE0 - 0.2, T_MOVE0 + 0.2))))
                label(c, "EUROPE CAN MOVE THE NUMBER", CX, 830, t, T_COMM - 0.2, 22, GLOW, a=a * ku * ease(seg(t, T_MOVE0 - 0.2, T_MOVE0 + 0.2)))
                ev(T_COMM - 0.2, "hydraulic", t, CX)


# ---------------------------------------------------------------- IDEA
T_TRAP, T_TARGET, T_STOPS = wd("goodhart", "trap."), wd("goodhart", "target,"), wd("goodhart", "stops")
T_COUNT0, T_WORKS, T_COUNTING = ls("count"), wd("count", "works"), wd("count", "counting")
T_IMAGINE = ls("imagine")


def idea(c, t):
    a = win(t, T_GOOD0 - 0.05, T_IMAGINE + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kg = 1 - ease(seg(t, T_COUNT0 - 0.2, T_COUNT0 + 0.3))
        if kg > 0:
            with layer(c, kg):
                bignum(c, t, "1975", 110, 560, 240, T_GOOD0 + 0.2)
                label(c, "CHARLES GOODHART", 560, 330, t, T_GOOD0 + 0.9, 22, SOFT, a=a * kg)
                lines_in(c, target(1340, 520, 180), t, T_TARGET - 0.5, 0.6, WHITE, 1.9)
                k = ease(seg(t, T_TARGET - 0.1, T_TARGET + 0.3), "i")
                if k > 0:
                    stroke_polys(c, arrow(lerp(700, 1150, k) - 260, lerp(700, 540, k) + 60, lerp(700, 1340, k), lerp(700, 520, k)), GLOW, 2.4, 1.0)
                    burst(c, 1340, 520, t, T_TARGET + 0.3, 70)
                    ev(T_TARGET + 0.3, "thud", t, 1340)
                label(c, "WHEN A MEASURE BECOMES A TARGET,", 560, 560, t, T_TARGET - 0.3, 22, WHITE, a=a * kg, cps=30)
                label(c, "IT STOPS BEING A GOOD MEASURE", 560, 610, t, T_STOPS, 22, GLOW, a=a * kg, cps=30)
        if t >= T_COUNT0 - 0.2:
            kc = ease(seg(t, T_COUNT0 - 0.2, T_COUNT0 + 0.3))
            with layer(c, kc):
                c.drawLine(200, 420, 1720, 420, mg.stroke(GLOW, 2.4, a * kc))
                label(c, "10^25", 220, 400, t, T_COUNT0, 20, GLOW, "left", a=a * kc)
                for i, x in enumerate((620, 960, 1300)):
                    lines_in(c, chip(x, 560, 60), t, T_COUNT0 + 0.2 + 0.15 * i, 0.4, WHITE, 1.8)
                    n = int(99 * ease(seg(t, T_COUNTING - 0.2, T_COUNTING + 1.4)))
                    label(c, f"SUMS: {n:02d}%", x, 690, t, T_COUNTING - 0.2, 20, SOFT, a=a * kc)
                label(c, "BUILDERS COUNT THE SUMS TOO", CX, 830, t, T_COUNTING, 22, WHITE, a=a * kc)
                ev(T_COUNTING - 0.2, "tick", t, CX)


# ---------------------------------------------------------------- IMAGINE
T_CARBON, T_WHATIF = wd("imagine", "carbon."), ls("whatif")
T_ALLOW0, T_ALLOWW, T_TRADED, T_PRICE = ls("allow"), wd("allow", "allowance"), wd("allow", "traded."), wd("allow", "price")
T_Q0, T_WHO, T_CHOOSE = ls("question"), wd("question", "who"), wd("question", "choose")
T_THEN = ls("then")


def imagine(c, t):
    a = win(t, T_IMAGINE - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        kr = 1 - ease(seg(t, T_ALLOW0 - 0.2, T_ALLOW0 + 0.3))
        if kr > 0:                                                          # a ration strip of sums
            with layer(c, kr):
                lines_in(c, ration(CX, 520, 900, 200), t, T_IMAGINE + 0.2, 0.7, WHITE, 1.8)
                for k in range(6):
                    label(c, "SUMS", CX - 450 + 75 + k * 150, 530, t, T_IMAGINE + 0.6 + 0.1 * k, 20, GLOW, a=a * kr)
                label(c, "THINKING, RATIONED LIKE CARBON", CX, 780, t, T_CARBON - 0.3, 24, WHITE, a=a * kr)
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 280, t, T_WHATIF + 0.05, 22, GLOW, a=a * kr)
                ev(T_IMAGINE + 0.2, "paper", t, CX)
        if t >= T_ALLOW0 - 0.2:                                             # labs, allowances, trading, a price
            ka = ease(seg(t, T_ALLOW0 - 0.2, T_ALLOW0 + 0.3))
            with layer(c, ka):
                for i, x in enumerate((420, 760, 1100)):
                    lines_in(c, lab(x, 560, 110), t, T_ALLOW0 + 0.1 * i, 0.5, WHITE, 1.7)
                    fill = (0.9, 0.35, 0.65)[i] + 0.25 * math.sin(3 * (t - T_TRADED) + i) * ease(seg(t, T_TRADED - 0.4, T_TRADED))
                    c.drawRect(skia.Rect.MakeXYWH(x - 100, 620, 200 * fill, 22), mg.chrome_paint(620, 642, 0.9))
                    c.drawRect(skia.Rect.MakeXYWH(x - 100, 620, 200, 22), mg.stroke(SOFT, 1.2, a * ka))
                label(c, "AN ALLOWANCE OF SUMS", 760, 700, t, T_ALLOWW, 20, GLOW, a=a * ka)
                k = seg(t, T_TRADED - 0.4, T_TRADED + 2.0)
                if 0 < k < 1:                                               # spare sums crossing between labs
                    for j in range(6):
                        u = (k * 3 + j / 6) % 1.0
                        x = lerp(420, 1100, u) if j % 2 else lerp(1100, 420, u)
                        c.drawCircle(x, 470 - 70 * math.sin(math.pi * u), 7, mg.fill(GOLD, 0.9 * a * ka))
                    ev(T_TRADED - 0.4, "coin", t, 760)
                label(c, "SPARE ONES TRADED", 760, 740, t, T_TRADED - 0.2, 20, SOFT, a=a * ka)
                if t >= T_PRICE - 0.3:
                    stroke_polys(c, chart(1300, 620, 440, 260, PRICE, seg(t, T_PRICE - 0.3, T_PRICE + 1.6)), GLOW, 2.2, 1.0)
                    label(c, "THE PRICE OF A THOUGHT", 1520, 670, t, T_PRICE, 20, WHITE, a=a * ka)
                label(c, "WHO SETS THE ALLOWANCE?", CX, 200, t, T_WHO, 24, WHITE, a=a * ka)
                label(c, "WHAT WOULD WE CHOOSE NOT TO THINK?", CX, 820, t, T_CHOOSE - 0.2, 24, GLOW, a=a * ka)


# ---------------------------------------------------------------- SURFACE
T_DANGERB = wd("then", "danger.")
T_SUMSB = wd("now2", "sums.")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "EU AI Act, Art. 51: systemic risk presumed above 10^25 operations; 51(3): the Commission can amend it",
           "California SB 53 (Transparency in Frontier AI Act), signed 29 Sep 2025: frontier models above 10^26",
           "Ho, Besiroglu et al., Algorithmic progress in language models, NeurIPS 2024: halving ~8 months (2012-2023)",
           "Kaplan et al. 2020; Hoffmann et al. 2022: performance scales with training compute",
           "Goodhart 1975; Strathern 1997 · sums: 10^25 / 8.2bn people / 31.6M s a year ≈ 39M years",
           "The section on thinking rationed like carbon is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 820)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 820))
            stroke_polys(c, dashed_box(400, 330, 320, 340), SOFT, 1.8, ease(seg(t, T_THEN, T_THEN + 0.4)))
            lines_in(c, qmark(560, 480, 150), t, T_THEN + 0.2, 0.5, WHITE, 2.2)
            label(c, "THE DANGER", 560, 790, t, T_DANGERB - 0.3, 22, GLOW, a=a)
            if t >= ls("now2") - 0.05:
                power(c, t, "25", 130, 1360, 520, ls("now2") - 0.05)
                label(c, "THE SUMS", 1360, 790, t, T_SUMSB - 0.3, 22, GLOW, a=a)
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
