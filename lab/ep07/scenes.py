"""EP07 · THE THIRTY-YEAR DELAY, the scenes: line art keyed to the script's line ids and George's words
(engine.tl.word), which the engine turns into characters.

  GROUND     6,000 bosses as 200 figures (1 = 30), then nine in ten go dim: no change; a week of 168 hours with an
             hour and a half lit; "this has happened before"
  MECHANISM  1882: a light bulb and Pearl Street's power station; a flat productivity line for decades; 100 squares
             of factory power, 5 electric in 1900; the line-shaft factory (one steam engine, a flywheel, one long
             shaft, belts to every machine, all turning); the engine becomes one big electric motor and nothing else
             changes; then the shaft and belts go, a small motor in every machine, the machines lined up along the
             flow of the work; 50% by 1920 and the line bends up
  NOW        1987: Solow's sentence typed beside an old computer; the late-1990s upturn; 100 AI pilots, 95 dim; the
             line-shaft factory again, with an AI chip as the one big motor
  IDEA       a floor plan around a shaft becomes a floor plan along the work: the layout, not the tool
  IMAGINE    an office drawn in dashes; the status meeting, the inbox and the relay arrows fall away; 1890s vs 1920s
  SURFACE    1882: the power arrived | 2026: again; the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, MID, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         points, closed_fill, stroke_polys, bignum, chip, keys, bump, morph_polys, roll, draw_segs, segs)

GROUND_Y = 800
TRAILS = []
GLINTS = []


# ---------------------------------------------------------------- things
def person_head(cx, cy, s):
    return [ellipse(cx, cy - 0.15 * s, 0.28 * s, 0.3 * s, 0, 360, 16), ellipse(cx, cy + 0.55 * s, 0.45 * s, 0.3 * s, 180, 360, 16)]


def bulb(cx, cy, s):
    glass = np.vstack([ellipse(cx, cy, s, s, 140, 400, 48)[:, :], [(cx + 0.45 * s, cy + 1.25 * s), (cx - 0.45 * s, cy + 1.25 * s)]])
    glass = np.vstack([glass, glass[:1]])
    fil = P([(cx - 0.3 * s, cy + 0.9 * s), (cx - 0.3 * s, cy + 0.1 * s), (cx - 0.15 * s, cy - 0.15 * s), (cx, cy + 0.1 * s),
             (cx + 0.15 * s, cy - 0.15 * s), (cx + 0.3 * s, cy + 0.1 * s), (cx + 0.3 * s, cy + 0.9 * s)])
    base = [P([(cx - 0.45 * s, cy + (1.35 + 0.15 * k) * s), (cx + 0.45 * s, cy + (1.35 + 0.15 * k) * s)]) for k in range(4)]
    return [glass, fil] + base


def station(x, bot, w, h):
    out = [rect(x, bot - h, w, h), P([(x - 10, bot - h), (x + w / 2, bot - h - 0.22 * w), (x + w + 10, bot - h)]),
           rect(x + 0.78 * w, bot - h - 0.55 * w, 0.1 * w, 0.4 * w), rect(x + 0.42 * w, bot - 0.35 * h, 0.16 * w, 0.35 * h)]
    for r in range(2):
        for k in range(4):
            out.append(rect(x + (0.08 + 0.23 * k) * w, bot - h + (0.15 + 0.3 * r) * h, 0.12 * w, 0.18 * h))
    return out


def chart_polys(x0, y0, w, h, pts, k=1.0):
    """Axes plus a polyline through (u, v) points in 0..1, drawn to fraction k."""
    out = [P([(x0, y0 - h), (x0, y0), (x0 + w, y0)])]
    q = np.array([(x0 + u * w, y0 - v * h) for u, v in pts])
    if k < 1:
        L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(q, axis=0), axis=1))])
        d = k * L[-1]
        n = int(np.searchsorted(L, d))
        q = np.vstack([q[:n], q[n - 1] + (q[n] - q[n - 1]) * (d - L[n - 1]) / max(1e-6, L[n] - L[n - 1])]) if 0 < n < len(q) else q[:max(2, n)]
    if len(q) >= 2:
        out.append(q)
    return out


FLAT = [(u, 0.18 + 0.03 * math.sin(u * 23) + 0.02 * u) for u in np.linspace(0, 0.85, 30)]
SURGE = FLAT + [(0.85 + 0.15 * v, 0.2 + 0.7 * v ** 1.6) for v in np.linspace(0.05, 1, 12)]


def cells(c, x0, y0, n_col, n_row, cell, gap, lit, a=1.0, lit_col=WHITE):
    for k in range(n_col * n_row):
        x = x0 + (k % n_col) * (cell + gap)
        y = y0 + (k // n_col) * (cell + gap)
        c.drawRect(skia.Rect.MakeXYWH(x, y, cell, cell), mg.stroke(SOFT, 1.2, 0.55 * a))
        f = min(1.0, max(0.0, lit - k))
        if f > 0:
            c.drawRect(skia.Rect.MakeXYWH(x, y + cell * (1 - f), cell, cell * f), mg.fill(lit_col, 0.95 * a))


# the line-shaft factory, side on
SHAFT_Y, ENG_C = 300.0, (330.0, 480.0)
MACH_X = [640, 830, 1020, 1210, 1400, 1590]


def machine(x, bot):
    return [rect(x - 60, bot - 150, 120, 80), P([(x - 50, bot - 70), (x - 50, bot)]), P([(x + 50, bot - 70), (x + 50, bot)]),
            ellipse(x, bot - 176, 22, 22, 0, 360, 20), P([(x - 40, bot - 110), (x + 40, bot - 110)])]


def pulley(cx, cy, r, rot):
    out = [ellipse(cx, cy, r, r, 0, 360, 24)]
    for k in range(3):
        a = rot + k * math.pi / 3
        out.append(P([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx - r * math.cos(a), cy - r * math.sin(a))]))
    return out


def steam_engine(rot):
    cx, cy = ENG_C
    fly = [ellipse(cx, cy, 120, 120, 0, 360, 64), ellipse(cx, cy, 16, 16, 0, 360, 16)]
    for k in range(6):
        a = rot + k * math.pi / 3
        fly.append(P([(cx + 16 * math.cos(a), cy + 16 * math.sin(a)), (cx + 112 * math.cos(a), cy + 112 * math.sin(a))]))
    boiler = [mg.rrect_pts(150, 660, 300, 110, 50, 6), P([(390, 660), (390, 560), (420, 560), (420, 660)])]
    return fly + boiler


def big_motor(rot):
    cx, cy = ENG_C
    out = [mg.rrect_pts(cx - 150, cy - 70, 240, 140, 30, 5), P([(cx - 170, cy + 70), (cx + 110, cy + 70)]),
           P([(cx - 140, cy + 70), (cx - 160, GROUND_Y)]), P([(cx + 80, cy + 70), (cx + 100, GROUND_Y)])]
    for k in range(7):
        x = cx - 120 + 30 * k
        out.append(P([(x, cy - 70), (x, cy + 70)]))
    out += pulley(cx + 130, cy, 30, rot)
    return out


def ai_motor(rot):
    cx, cy = ENG_C
    return chip(cx, cy, 90) + pulley(cx + 150, cy, 30, rot)


def factory(engine_kind, rot):
    """The building, the shaft with its pulleys, the machines and the engine (all as polylines)."""
    bld = [P([(100, GROUND_Y), (100, 220), (CX, 120), (1820, 220), (1820, GROUND_Y)]), P([(80, GROUND_Y), (1840, GROUND_Y)])]
    shaft = [P([(ENG_C[0], SHAFT_Y - 6), (1680, SHAFT_Y - 6)]), P([(ENG_C[0], SHAFT_Y + 6), (1680, SHAFT_Y + 6)])]
    for x in [ENG_C[0]] + MACH_X:
        shaft += pulley(x, SHAFT_Y, 26, rot)
    mach = [q for x in MACH_X for q in machine(x, GROUND_Y)]
    eng = steam_engine(rot) if engine_kind == "steam" else big_motor(rot) if engine_kind == "motor" else ai_motor(rot)
    return bld, shaft, mach, eng


def belts(c, t, a=1.0, xs=None):
    """Belt loops from the shaft pulleys down to each machine, the dashes running."""
    for x in xs or ([ENG_C[0]] + MACH_X):
        y1 = ENG_C[1] if x == ENG_C[0] else GROUND_Y - 176
        for sgn, direction in ((-1, 1), (1, -1)):
            xx = x + sgn * (26 if x != ENG_C[0] else 24)
            n = 12
            for i in range(n):
                u0 = ((i / n) + direction * t * 0.9) % 1.0
                ya = SHAFT_Y + (y1 - SHAFT_Y) * u0
                yb = min(y1, ya + (y1 - SHAFT_Y) / n * 0.55)
                c.drawLine(xx, ya, xx, yb, mg.stroke(GLOW, 2.0, 0.9 * a))


def small_motor(cx, cy, s=28):
    return [ellipse(cx, cy, s, s, 0, 360, 24)] + [P([(cx - s + 0.5 * s * k, cy - s * 0.9), (cx - s + 0.5 * s * k, cy + s * 0.9)]) for k in range(1, 4)]


def computer(cx, bot, s):
    return [mg.rrect_pts(cx - 0.6 * s, bot - 1.3 * s, 1.2 * s, 0.85 * s, 0.05 * s, 3), mg.rrect_pts(cx - 0.5 * s, bot - 1.22 * s, 1.0 * s, 0.68 * s, 0.03 * s, 3),
            P([(cx - 0.1 * s, bot - 0.45 * s), (cx - 0.15 * s, bot - 0.3 * s), (cx + 0.15 * s, bot - 0.3 * s), (cx + 0.1 * s, bot - 0.45 * s)]),
            mg.rrect_pts(cx - 0.7 * s, bot - 0.22 * s, 1.4 * s, 0.2 * s, 0.03 * s, 3)]


def envelope(cx, cy, s):
    return [rect(cx - s, cy - 0.65 * s, 2 * s, 1.3 * s), P([(cx - s, cy - 0.65 * s), (cx, cy + 0.1 * s), (cx + s, cy - 0.65 * s)])]


def dashed(c, polys, col=WHITE, w=1.6, a=1.0, n=600):
    S = segs(polys, n)
    draw_segs(c, S[::2], col, w, a, glow=False)


# ---------------------------------------------------------------- GROUND
T_SIX, T_BOSS, T_NOTH, T_NINE, T_PROD, T_JOBS = wd("survey", "six"), wd("survey", "bosses"), wd("nothing", "nothing."), wd("nothing", "nine"), wd("nothing", "productivity."), wd("nothing", "jobs.")
T_HOURS, T_HOUR, T_WEEK = ls("hours"), wd("hours", "hour"), wd("hours", "week.")
T_BEFORE = ls("before")
T_EDI = ls("edison")
COUNTRIES = [("survey", "America,", "AMERICA"), ("survey", "Britain,", "BRITAIN"), ("survey", "Germany", "GERMANY"), ("survey", "Australia", "AUSTRALIA")]
HEADS = [(495 + (k % 20) * 49, 440 + (k // 20) * 34) for k in range(200)]
LIT = set(np.random.default_rng(12).permutation(200)[:20].tolist())


def ground(c, t):
    a = win(t, 1.2, T_EDI + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kh = 1 - ease(seg(t, T_HOURS - 0.2, T_HOURS + 0.3))
        if kh > 0:
            with layer(c, kh):
                if t < T_NINE:
                    bignum(c, t, "6,000", 120, CX, 230, T_SIX - 0.05)
                else:
                    roll(c, "6,000", "~90%", 120, CX, 230, t, T_SIX - 0.05, T_NINE)
                label(c, "BOSSES ASKED · NBER, FEB 2026", CX, 325, t, T_BOSS, 22, SOFT, a=a * kh * (1 - ease(seg(t, T_NINE - 0.2, T_NINE))))
                label(c, "SAID: NO CHANGE IN PRODUCTIVITY OR JOBS", CX, 325, t, T_PROD - 0.3, 22, GLOW, a=a * kh)
                dim = ease(seg(t, T_NOTH - 0.1, T_NOTH + 0.5))
                for k, (x, y) in enumerate(HEADS):
                    tk = T_BOSS - 0.3 + 0.004 * k
                    if t < tk:
                        continue
                    lit = k in LIT
                    stroke_polys(c, person_head(x, y, 26), WHITE if lit else GLOW, 1.4, 1.0 if lit else 1 - 0.75 * dim)
                ev(T_BOSS - 0.3, "grains", t, CX)
                ev(T_NOTH, "sub_drop", t, CX)
                for k, (i_d, w_, name) in enumerate(COUNTRIES):
                    label(c, name, 600 + 240 * k, 800, t, wd(i_d, w_), 20, SOFT, a=a * kh)
                label(c, "1 FIGURE = 30 BOSSES", CX, 850, t, T_BOSS + 0.6, 16, SOFT, a=a * kh)
        if t >= T_HOURS - 0.2:                                                # a week of 168 hours, 1.5 lit
            kw = ease(seg(t, T_HOURS - 0.2, T_HOURS + 0.3)) * (1 - ease(seg(t, T_BEFORE - 0.3, T_BEFORE)))
            with layer(c, kw):
                days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
                for d in range(7):
                    x0 = 700 + d * 76
                    label(c, days[d], x0 + 30, 320, t, T_HOURS + 0.1, 16, SOFT, a=a * kw)
                    lit = keys(t, [(T_HOUR - 0.1, 0.0), (T_WEEK, 1.5)]) if d == 0 else 0.0
                    for h in range(24):
                        y = 340 + h * 17
                        c.drawRect(skia.Rect.MakeXYWH(x0, y, 60, 13), mg.stroke(SOFT, 1.0, 0.5))
                        f = min(1.0, max(0.0, lit - h))
                        if f > 0:
                            c.drawRect(skia.Rect.MakeXYWH(x0, y, 60 * f, 13), mg.fill(WHITE, 0.95))
                ev(T_HOUR, "tick", t, 730)
                bignum(c, t, "1.5 HOURS", 100, CX, 230, T_HOUR - 0.3)
                label(c, "A WEEK, OUT OF 168", CX, 780, t, T_WEEK, 22, WHITE, a=a * kw)
        label(c, "THIS HAS HAPPENED BEFORE", CX, 540, t, wd("before", "happened"), 30, WHITE, a=a * (1 - ease(seg(t, T_EDI - 0.3, T_EDI))))


# ---------------------------------------------------------------- MECHANISM
T_1882, T_EDISON, T_POWER, T_STATION = wd("edison", "eighteen"), wd("edison", "Edison"), wd("edison", "power"), wd("edison", "station,")
T_DEC0, T_DECADES = ls("decades"), wd("decades", "decades,")
T_FIVE0, T_FIVE = ls("five"), wd("five", "five")
T_SHAFT0, T_OLD, T_STEAM, T_SHAFTW, T_BELTS, T_MACH = ls("shaft"), wd("shaft", "factories"), wd("shaft", "steam"), wd("shaft", "shaft,"), wd("shaft", "belts"), wd("shaft", "machine.")
T_SWAP, T_MOTOR = wd("swap", "swapped"), wd("swap", "motor.")
T_S1, T_S2, T_S3, T_S4 = wd("same", "shaft."), wd("same", "belts."), wd("same", "building."), wd("same", "Small")
T_RED, T_SMALLM, T_EVERY, T_LAID = ls("redesign"), wd("redesign", "small"), wd("redesign", "every"), wd("redesign", "laid")
T_50, T_HALF, T_SURGE0, T_SURGED = ls("fifty"), wd("fifty", "half"), wd("fifty", "productivity"), wd("fifty", "surged.")
T_SOLOW = ls("solow")
FLOW_X = [520, 700, 880, 1060, 1240, 1420]


def mechanism(c, t):
    a = win(t, T_EDI - 0.05, T_SHAFT0 + 0.2, 0.3, 0.5)
    if a > 0:
        with layer(c, a):
            k1 = 1 - ease(seg(t, T_DEC0 - 0.2, T_DEC0 + 0.4))
            if k1 > 0:
                with layer(c, k1):
                    bignum(c, t, "1882", 130, CX, 230, T_1882)
                    label(c, "EDISON'S PEARL STREET STATION · NEW YORK", CX, 330, t, T_EDISON, 22, SOFT, a=a * k1)
                    lines_in(c, bulb(700, 520, 90), t, T_POWER - 0.3, 0.6, WHITE, 1.8)
                    kg = ease(seg(t, T_POWER + 0.3, T_POWER + 0.8))
                    if kg > 0:
                        closed_fill(c, [ellipse(700, 520, 80, 80, 0, 360, 40)], 1.0, mg.fill(GOLD, 0.35 * kg))
                    ev(T_POWER - 0.3, "power_up", t, 700)
                    lines_in(c, station(1080, GROUND_Y, 380, 230), t, T_STATION - 0.2, 0.6, WHITE, 1.8)
                    if t >= T_STATION + 0.3:
                        n = 50
                        u = ((t - T_STATION) * 0.3 + np.arange(n) / n) % 1.0
                        points(c, np.column_stack([1428 + 30 * np.sin(u * 6) * u, GROUND_Y - 230 - 0.55 * 380 - u * 200]), 0.6, WHITE, 3.2)
            if t >= T_DEC0 - 0.2:                                           # decades of a flat line
                kc = ease(seg(t, T_DEC0 - 0.2, T_DEC0 + 0.3))
                with layer(c, kc):
                    stroke_polys(c, chart_polys(360, 760, 620, 380, FLAT, seg(t, T_DECADES - 0.2, T_DECADES + 1.8)), GLOW, 2.0, 1.0)
                    for yr, u in (("1880", 0.0), ("1900", 0.5), ("1915", 0.85)):
                        label(c, yr, 360 + 620 * u, 800, t, T_DEC0 + 0.2, 18, SOFT, a=a * kc)
                    label(c, "FACTORY PRODUCTIVITY", 360, 360, t, T_DECADES, 20, WHITE, "left", a=a * kc)
                    ev(T_DECADES, "scan", t, 600)
                if t >= T_FIVE0 - 0.2:
                    kf = ease(seg(t, T_FIVE0 - 0.2, T_FIVE0 + 0.3))
                    with layer(c, kf):
                        cells(c, 1150, 380, 10, 10, 34, 7, keys(t, [(T_FIVE - 0.1, 0.0), (T_FIVE + 0.5, 5.0)]))
                        bignum(c, t, "5%", 110, 1355, 250, T_FIVE - 0.1)
                        label(c, "OF US FACTORY POWER · ELECTRIC · 1900", 1355, 820, t, T_FIVE + 0.3, 18, GLOW, a=a * kf)
                        ev(T_FIVE, "tick", t, 1200)
    # the line-shaft factory
    af = win(t, T_SHAFT0 - 0.05, T_50 + 0.3, 0.2, 0.5)
    if af > 0:
        rot = t * 3.0
        kind = "steam" if t < T_SWAP else "motor"
        bld, shaft, mach, eng = factory(kind, rot)
        with layer(c, af):
            ks = 1 - ease(seg(t, T_RED + 0.1, T_RED + 0.6))                   # building, shaft, belts, engine go at the redesign
            with layer(c, ks):
                lines_in(c, bld, t, T_OLD - 0.2, 0.7, SOFT, 1.5, seed_pt=(CX, 900))
                if t < T_SWAP:
                    lines_in(c, eng, t, T_STEAM - 0.2, 0.6, WHITE, 1.8)
                elif t < T_SWAP + 0.9:
                    morph_polys(c, steam_engine(rot), big_motor(rot), seg(t, T_SWAP, T_SWAP + 0.9), WHITE)
                    ev(T_SWAP, "morph", t, ENG_C[0])
                else:
                    stroke_polys(c, eng, WHITE, 1.8)
                    closed_fill(c, [eng[0]], 1.0, mg.fill(MID, 0.3))
                lines_in(c, shaft, t, T_SHAFTW - 0.3, 0.6, GLOW, 1.8, seed_pt=(ENG_C[0], SHAFT_Y))
                if t >= T_BELTS - 0.2:
                    belts(c, t, ease(seg(t, T_BELTS - 0.2, T_BELTS + 0.3)))
                ev(T_STEAM - 0.2, "hydraulic", t, ENG_C[0])
                ev(T_BELTS, "servo", t, CX)
                label(c, "ONE BIG ELECTRIC MOTOR", ENG_C[0], 290 - 50, t, T_MOTOR, 20, GLOW, a=af * ks)
                for tt, txt, x, y in ((T_S1, "SAME SHAFT", 1000, SHAFT_Y - 40), (T_S2, "SAME BELTS", 925, 520), (T_S3, "SAME BUILDING", CX, 170),
                                      (T_S4, "SMALL SAVINGS", ENG_C[0] + 10, 850)):
                    label(c, txt, x, y, t, tt, 22, WHITE, a=af * ks)
                    ev(tt, "latch", t, x)
            km_out = 1 - ease(seg(t, T_50 - 0.1, T_50 + 0.3))                  # the machines make way for the 50%
            c.saveLayerAlpha(None, int(255 * km_out))
            # the machines: along the shaft, then each with its own motor, lined up along the work
            km = seg(t, T_LAID - 0.3, T_LAID + 0.9)
            for k, x0 in enumerate(MACH_X):
                x = lerp(x0, FLOW_X[k], ease(km))
                y = lerp(GROUND_Y, 700, ease(km))
                t_m = T_MACH - 0.4 + 0.06 * k
                if t >= t_m:
                    lines_in(c, machine(x, y), t, t_m, 0.4, WHITE, 1.8)
                if t >= T_SMALLM + 0.05 * k:
                    stroke_polys(c, small_motor(x + 78, y - 110, 26), GLOW, 1.8, ease(seg(t, T_SMALLM + 0.05 * k, T_SMALLM + 0.05 * k + 0.3)))
                    ev(T_SMALLM + 0.05 * k, "tick", t, x)
                if km > 0.6 and k < 5:
                    for p in [P([(x + 70, y - 190), (FLOW_X[k + 1] - 70, y - 190)])]:
                        stroke_polys(c, [p], GLOW, 1.8, ease(seg(km, 0.6, 1.0)))
            if t >= T_SMALLM:
                label(c, "A SMALL MOTOR IN EVERY MACHINE", CX, 240, t, T_SMALLM + 0.2, 22, WHITE, a=af * km_out)
            if km > 0:
                label(c, "LAID OUT ALONG THE FLOW OF THE WORK", CX, 290, t, T_LAID + 0.3, 22, GLOW, a=af * km_out)
                ev(T_LAID - 0.3, "whoosh", t, CX)
            c.restore()
    a5 = win(t, T_50 - 0.1, T_SOLOW + 0.2, 0.3, 0.5)                         # half electric, and the surge
    if a5 > 0:
        with layer(c, a5):
            bignum(c, t, "50%", 120, CX, 230, T_50 + 0.15)
            label(c, "OF US FACTORY POWER ELECTRIC · 1920", CX, 330, t, T_HALF + 0.3, 22, SOFT, a=a5)
            if t >= T_SURGE0 - 0.3:
                stroke_polys(c, chart_polys(560, 780, 800, 380, SURGE, seg(t, T_SURGE0 - 0.3, T_SURGED + 0.3)), WHITE, 2.4, 1.0)
                label(c, "1920", 560 + 800 * 0.85, 820, t, T_SURGE0, 18, SOFT, a=a5)
                label(c, "PRODUCTIVITY", 560, 390, t, T_SURGE0, 20, GLOW, "left", a=a5)
                ev(T_SURGED - 0.2, "riser", t, 1300)


# ---------------------------------------------------------------- NOW
T_1987, T_ROBERT, T_YOU, T_EVERYW, T_STATS = wd("solow", "nineteen"), wd("solow", "Robert"), wd("solow", "you"), wd("solow", "everywhere"), wd("solow", "productivity")
T_90S, T_LATE, T_REBUILT = ls("nineties"), wd("nineties", "late"), wd("nineties", "rebuilt")
T_PIL, T_95 = ls("pilots"), wd("pilots", "ninety-five")
T_BOLT, T_ONE, T_SAMESH = ls("bolted"), wd("bolted", "One"), wd("bolted", "same")
T_LAYOUT = ls("layout")
NINETIES = [(u, 0.25 + 0.02 * math.sin(u * 30)) for u in np.linspace(0, 0.45, 14)] + [(0.45 + 0.55 * v, 0.26 + 0.5 * v) for v in np.linspace(0.05, 1, 12)]


def now(c, t):
    a = win(t, T_SOLOW - 0.05, T_PIL + 0.2, 0.3, 0.5)
    if a > 0:
        with layer(c, a):
            kq = 1 - ease(seg(t, T_90S - 0.2, T_90S + 0.3))
            if kq > 0:
                with layer(c, kq):
                    bignum(c, t, "1987", 130, CX, 230, T_1987)
                    label(c, "ROBERT SOLOW · NEW YORK TIMES BOOK REVIEW", CX, 330, t, T_ROBERT, 22, SOFT, a=a * kq)
                    lines_in(c, computer(560, 760, 260), t, T_1987 + 0.3, 0.6, WHITE, 1.8)
                    for k, (tt, txt) in enumerate(((T_YOU, "\"YOU CAN SEE THE COMPUTER AGE"), (T_EVERYW, "EVERYWHERE BUT IN THE"), (T_STATS, "PRODUCTIVITY STATISTICS.\""))):
                        label(c, txt, 860, 500 + 50 * k, t, tt - 0.1, 26, WHITE, "left", a=a * kq, cps=30)
            if t >= T_90S - 0.2:
                kn = ease(seg(t, T_90S - 0.2, T_90S + 0.3))
                with layer(c, kn):
                    stroke_polys(c, chart_polys(460, 760, 1000, 380, NINETIES, seg(t, T_90S, T_REBUILT + 0.6)), WHITE, 2.4, 1.0)
                    for yr, u in (("1987", 0.0), ("1995", 0.45), ("2004", 1.0)):
                        label(c, yr, 460 + 1000 * u, 800, t, T_90S + 0.1, 18, SOFT, a=a * kn)
                    label(c, "US PRODUCTIVITY", 460, 360, t, T_90S + 0.2, 20, GLOW, "left", a=a * kn)
                    label(c, "THE GAINS: THE LATE 1990s", 460 + 1000 * 0.72, 330, t, T_LATE, 22, WHITE, a=a * kn)
                    ev(T_LATE, "riser", t, 1100)
    ap = win(t, T_PIL - 0.05, T_LAYOUT + 0.2, 0.3, 0.5)
    if ap > 0:
        with layer(c, ap):
            kp = 1 - ease(seg(t, T_BOLT - 0.1, T_BOLT + 0.4))
            if kp > 0:
                with layer(c, kp):
                    bignum(c, t, "95%", 120, CX, 230, T_95 - 0.1)
                    label(c, "OF COMPANY AI PILOTS: NO MEASURABLE RETURN · MIT, 2025", CX, 330, t, T_95 + 0.4, 22, SOFT, a=ap * kp)
                    k0 = T_PIL + 0.3
                    for k in range(100):
                        x = 560 + (k % 20) * 41
                        y = 420 + (k // 20) * 41
                        if t < k0 + 0.006 * k:
                            continue
                        good = k >= 95
                        dim = ease(seg(t, T_95, T_95 + 0.6)) if not good else 0.0
                        c.drawRect(skia.Rect.MakeXYWH(x, y, 32, 32), mg.fill(WHITE, 0.95 * (1 - 0.8 * dim)) if not good or t < T_95 else mg.fill(GLOW, 0.95))
                    ev(T_95, "sub_drop", t, CX)
            if t >= T_BOLT - 0.1:                                             # AI as the one big motor, same shaft
                rot = t * 3.0
                bld, shaft, mach, eng = factory("ai", rot)
                kb = ease(seg(t, T_BOLT - 0.1, T_BOLT + 0.5))
                with layer(c, kb):
                    stroke_polys(c, bld, SOFT, 1.5, 1.0)
                    stroke_polys(c, shaft + mach, GLOW, 1.7, 1.0)
                    belts(c, t, 1.0)
                    if t >= T_ONE - 0.2:
                        lines_in(c, eng, t, T_ONE - 0.2, 0.5, WHITE, 2.0)
                        c.drawRect(skia.Rect.MakeXYWH(ENG_C[0] - 45, ENG_C[1] - 45, 90, 90), mg.fill(GLOW, 0.85 * ease(seg(t, T_ONE, T_ONE + 0.3))))
                        label(c, "AI", ENG_C[0], ENG_C[1] + 12, t, T_ONE + 0.1, 34, "#0B0C0E", a=ap)
                        ev(T_ONE - 0.2, "form", t, ENG_C[0])
                    label(c, "BOLTED ONTO THE OLD ROUTINE", CX, 180, t, wd("bolted", "bolted"), 22, WHITE, a=ap)
                    label(c, "THE SAME SHAFT", 1000, SHAFT_Y - 40, t, T_SAMESH, 22, GLOW, a=ap)


# ---------------------------------------------------------------- IDEA
T_TOOL, T_LAYOUTW, T_SHAPES0, T_SHAPES = wd("layout", "tool"), wd("layout", "layout"), ls("shapes"), wd("shapes", "shapes.")
T_IMAGINE = ls("imagine")
PLAN_SHAFT = [(x, y) for x in (560, 720, 880, 1040, 1200, 1360) for y in (430, 650)]
PLAN_FLOW = [(560 + 160 * (k % 6) if (k // 6) % 2 == 0 else 1360 - 160 * (k % 6), 430 + 220 * (k // 6)) for k in range(12)]


def plan_polys(pts, shaft=False):
    out = [rect(x - 40, y - 40, 80, 80) for x, y in pts]
    if shaft:
        out.append(P([(480, 540), (1440, 540)]))
    else:
        for k in range(11):
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]
            if y0 == y1:
                out.append(P([(x0 + (45 if x1 > x0 else -45), y0), (x1 - (45 if x1 > x0 else -45), y1)]))
            else:
                out.append(P([(x0, y0 + 45), (x1, y1 - 45)]))
    return out


def idea(c, t):
    a = win(t, T_LAYOUT - 0.05, T_IMAGINE + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        km = seg(t, T_LAYOUTW - 0.3, T_LAYOUTW + 0.7)
        if km <= 0:
            lines_in(c, plan_polys(PLAN_SHAFT, True), t, T_LAYOUT, 0.6, WHITE, 1.8)
        elif km < 1:
            morph_polys(c, plan_polys(PLAN_SHAFT, True), plan_polys(PLAN_FLOW), km, WHITE)
            ev(T_LAYOUTW - 0.3, "morph", t, CX)
        else:
            stroke_polys(c, plan_polys(PLAN_FLOW), WHITE, 1.8)
        label(c, "THE TOOL", CX, 250, t, T_TOOL, 22, SOFT, a=a * (1 - ease(seg(t, T_LAYOUTW - 0.3, T_LAYOUTW))))
        label(c, "THE LAYOUT", CX, 250, t, T_LAYOUTW, 30, WHITE, a=a)
        label(c, "NEW POWER NEEDS NEW SHAPES", CX, 860 - 20, t, T_SHAPES0 + 0.2, 24, GLOW, a=a)


# ---------------------------------------------------------------- IMAGINE
T_ZERO, T_WHATIF = wd("imagine", "zero"), ls("whatif")
T_MEET, T_INBOX, T_JOBSI, T_INFO = wd("first", "meeting."), wd("first", "inbox."), wd("first", "jobs"), wd("first", "information")
T_LOOK, T_20S, T_90S_ = ls("look"), wd("look", "nineteen-twenties"), wd("look", "eighteen-nineties.")
T_THEN = ls("then")
DESKS = [(640 + 150 * (k % 5), 420 + 110 * (k // 5)) for k in range(10)]
RELAY = [((640 + 150 * k, 420), (640 + 150 * (k + 1), 530)) for k in range(4)]


def imagine(c, t):
    a = win(t, T_IMAGINE - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        ko = 1 - ease(seg(t, T_LOOK - 0.2, T_LOOK + 0.3))
        if ko > 0:
            with layer(c, ko):
                dashed(c, [rect(460, 300, 1000, 460)], SOFT, 1.8, 1.0)
                for x, y in DESKS:
                    dashed(c, [rect(x - 50, y - 26, 100, 52)], WHITE, 1.6, ease(seg(t, T_IMAGINE + 0.3, T_IMAGINE + 0.9)), 160)
                km = 1 - ease(seg(t, T_MEET - 0.1, T_MEET + 0.4))              # the status meeting goes
                with layer(c, km):
                    dashed(c, [ellipse(560, 680, 70, 40, 0, 360, 40)] + [ellipse(560 + 95 * math.cos(q), 680 + 60 * math.sin(q), 12, 12, 0, 360, 12)
                                                                         for q in np.linspace(0, 2 * math.pi, 7)[:-1]], GLOW, 1.6, 1.0, 300)
                ki = 1 - ease(seg(t, T_INBOX - 0.1, T_INBOX + 0.4))            # the inbox goes
                with layer(c, ki):
                    stroke_polys(c, envelope(1320, 670, 44), GLOW, 1.8, 1.0)
                    label(c, "99+", 1370, 640, t, -1, 18, WHITE, "left", a=a * ki * ko)
                kr = 1 - ease(seg(t, T_INFO - 0.1, T_INFO + 0.5))              # the relay jobs go
                with layer(c, kr):
                    for p0, p1 in RELAY:
                        stroke_polys(c, [P([p0, p1])], GLOW, 1.6, 1.0)
                label(c, "AN OFFICE DESIGNED FROM ZERO AROUND AI", CX, 250, t, T_ZERO, 22, WHITE, a=a * ko * (1 - ease(seg(t, T_WHATIF - 0.2, T_WHATIF))))
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 250, t, T_WHATIF + 0.05, 24, WHITE, a=a * ko)
                for tt, txt, x in ((T_MEET, "THE STATUS MEETING", 560), (T_INBOX, "THE INBOX", 1320), (T_INFO, "THE RELAY JOBS", 800)):
                    label(c, txt, x, 820, t, tt, 18, SOFT, a=a * ko)
                    ev(tt, "pop", t, x)
        if t >= T_LOOK - 0.2:                                                # 1890s against 1920s
            kl = ease(seg(t, T_LOOK - 0.2, T_LOOK + 0.3))
            with layer(c, kl):
                if t < T_20S - 0.2:
                    lines_in(c, plan_polys(PLAN_SHAFT, True), t, T_LOOK, 0.5, SOFT, 1.5)
                label(c, "1890s: ONE SHAFT", 960, 250, t, T_90S_ - 0.4, 22, SOFT, a=a * kl * (1 - ease(seg(t, T_20S - 0.2, T_20S + 0.2))))
                if t >= T_20S - 0.2:
                    morph_polys(c, plan_polys(PLAN_SHAFT, True), plan_polys(PLAN_FLOW), seg(t, T_20S - 0.2, T_20S + 0.6), WHITE)
                    label(c, "1920s: THE FLOW OF THE WORK", 960, 250, t, T_20S, 22, WHITE, a=a * kl)
                    ev(T_20S - 0.2, "morph", t, CX)


# ---------------------------------------------------------------- SURFACE
T_1882B, T_ARRIVED, T_DECW, T_CHANGED = wd("then", "eighteen"), wd("then", "arrived."), wd("then", "Decades"), wd("then", "changed.")
T_2026, T_AGAIN = wd("now2", "twenty"), wd("now2", "again.")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "NBER survey of ~6,000 executives (US, UK, Germany, Australia), Feb 2026: via Fortune, 17 Feb 2026",
           "Edison's Pearl Street Station, New York, September 1882",
           "Paul A. David, \"The Dynamo and the Computer\", American Economic Review, 1990",
           "Robert Solow, New York Times Book Review, 12 July 1987 · US productivity from the mid-1990s: BLS",
           "MIT NANDA, \"The GenAI Divide: State of AI in Business 2025\"",
           "The office section is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 820)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 820))
            bignum(c, t, "1882", 130, 560, 250, T_1882B)
            lines_in(c, bulb(560, 520, 80), t, T_1882B + 0.3, 0.5, WHITE, 1.8)
            if t >= T_ARRIVED:
                closed_fill(c, [ellipse(560, 520, 72, 72, 0, 360, 40)], 1.0, mg.fill(GOLD, 0.3 * ease(seg(t, T_ARRIVED, T_ARRIVED + 0.4))))
            label(c, "THE POWER ARRIVED", 560, 760, t, T_ARRIVED - 0.2, 20, GLOW, a=a)
            label(c, "DECADES LATER, THE FACTORY CHANGED", 560, 800, t, T_DECW, 18, SOFT, a=a)
            if t >= T_2026 - 0.05:
                bignum(c, t, "2026", 130, 1360, 250, T_2026 - 0.05)
                lines_in(c, chip(1360, 540, 90), t, T_2026 + 0.2, 0.5, WHITE, 1.8)
                c.drawRect(skia.Rect.MakeXYWH(1360 - 45, 540 - 45, 90, 90), mg.fill(GLOW, 0.85 * ease(seg(t, T_AGAIN - 0.3, T_AGAIN))))
                label(c, "THE POWER HAS ARRIVED AGAIN", 1360, 760, t, T_AGAIN - 0.4, 20, GLOW, a=a)
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
