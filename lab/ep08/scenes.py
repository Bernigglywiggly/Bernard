"""EP08 · CHEAPER MAKES MORE, the scenes: line art keyed to the script's line ids and George's words
(engine.tl.word), which the engine turns into characters.

  GROUND     1865 and a steam engine by its coal; the same work from a smaller pile; Britain's coal line goes up, not
             down; the line hands over to AI
  MECHANISM  a price falling, new uses appearing; a candle, then 3,000x cheaper light; 40,000x more light as a night
             city of dots filling the frame; a streetlight, a shop window, a screen
  NOW        price down, use up: two lines crossing; eight novels, $60 -> $0.06; ten Big Macs down to a hundredth of
             one; 3.2 quadrillion tokens bursting out; a 300x bar; the post: "Jevons paradox strikes again!"
  IDEA       a padlock opening; racks, a pylon, a chip: more, not fewer
  IMAGINE    a bulb with a chip for a filament; a tutor, a second look at a scan, a letter explained
  SURFACE    1865: better engines, more coal | 2026: cheaper thinking, more thinking; the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, MID, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         points, closed_fill, stroke_polys, bignum, chip, keys, morph_polys, roll, dotted_num, mac_icon, figure, STAND)

GROUND_Y = 800
TRAILS = []
GLINTS = []
RNG = np.random.default_rng(8)


# ---------------------------------------------------------------- things
def engine_shape(cx, cy, s, rot):
    """A steam engine: a boiler, a chimney, a flywheel."""
    out = [mg.rrect_pts(cx - 1.4 * s, cy + 0.2 * s, 1.8 * s, 0.7 * s, 0.3 * s, 6), rect(cx - 1.2 * s, cy - 0.7 * s, 0.25 * s, 0.9 * s),
           ellipse(cx + 0.9 * s, cy + 0.1 * s, 0.8 * s, 0.8 * s, 0, 360, 48)]
    for k in range(6):
        a = rot + k * math.pi / 3
        out.append(P([(cx + 0.9 * s, cy + 0.1 * s), (cx + 0.9 * s + 0.75 * s * math.cos(a), cy + 0.1 * s + 0.75 * s * math.sin(a))]))
    out.append(P([(cx + 0.4 * s, cy + 0.55 * s), (cx + 0.9 * s, cy + 0.1 * s)]))
    return out


def coal(cx, bot, s, seed=9):
    rng = np.random.default_rng(seed)
    out = [P([(cx - 0.8 * s, bot), (cx - 0.4 * s, bot - 0.4 * s), (cx, bot - 0.55 * s), (cx + 0.4 * s, bot - 0.38 * s), (cx + 0.8 * s, bot)])]
    for _ in range(int(10 * s / 100)):
        x, y = cx + rng.uniform(-0.5, 0.5) * s, bot - rng.uniform(0.05, 0.32) * s
        out.append(ellipse(x, y, 0.08 * s, 0.055 * s, 0, 360, 10))
    return out


def candle(cx, bot, s):
    return [rect(cx - 0.18 * s, bot - s, 0.36 * s, s), P([(cx, bot - s), (cx, bot - 1.1 * s)]),
            np.column_stack([cx + 0.1 * s * np.sin(np.linspace(0, math.pi, 20)) * np.sign(np.linspace(-1, 1, 20)),
                             bot - 1.12 * s - 0.28 * s * np.sin(np.linspace(0, math.pi, 20))])]


def bulb(cx, cy, s):
    glass = np.vstack([ellipse(cx, cy, s, s, 140, 400, 48), [(cx + 0.45 * s, cy + 1.25 * s), (cx - 0.45 * s, cy + 1.25 * s)]])
    glass = np.vstack([glass, glass[:1]])
    base = [P([(cx - 0.45 * s, cy + (1.35 + 0.15 * k) * s), (cx + 0.45 * s, cy + (1.35 + 0.15 * k) * s)]) for k in range(4)]
    return [glass] + base


def streetlight(cx, bot, h):
    return [P([(cx, bot), (cx, bot - h), (cx + 0.25 * h, bot - h)]), P([(cx + 0.18 * h, bot - h), (cx + 0.32 * h, bot - h), (cx + 0.29 * h, bot - 0.94 * h),
                                                                       (cx + 0.21 * h, bot - 0.94 * h), (cx + 0.18 * h, bot - h)])]


def shop(cx, bot, w):
    return [rect(cx - w / 2, bot - 0.8 * w, w, 0.8 * w), rect(cx - 0.4 * w, bot - 0.55 * w, 0.8 * w, 0.4 * w),
            P([(cx - 0.55 * w, bot - 0.8 * w), (cx + 0.55 * w, bot - 0.8 * w), (cx + 0.45 * w, bot - 0.95 * w), (cx - 0.45 * w, bot - 0.95 * w),
               (cx - 0.55 * w, bot - 0.8 * w)])]


def screen(cx, bot, s):
    return [mg.rrect_pts(cx - 0.6 * s, bot - 1.2 * s, 1.2 * s, 0.8 * s, 0.05 * s, 3), P([(cx, bot - 0.4 * s), (cx, bot - 0.15 * s)]),
            P([(cx - 0.3 * s, bot - 0.15 * s), (cx + 0.3 * s, bot - 0.15 * s)])]


def book(x, y, w, h):
    return [rect(x, y, w, h), P([(x + 0.15 * w, y), (x + 0.15 * w, y + h)])]


def racks(x, bot, n, w=60, h=200, gap=18):
    out = []
    for k in range(n):
        x0 = x + k * (w + gap)
        out.append(mg.rrect_pts(x0, bot - h, w, h, 5, 3))
        for j in range(7):
            out.append(P([(x0 + 0.15 * w, bot - h + (0.12 + 0.11 * j) * h), (x0 + 0.85 * w, bot - h + (0.12 + 0.11 * j) * h)]))
    return out


def bolt(cx, cy, s):
    return [P([(cx + 0.2 * s, cy - s), (cx - 0.35 * s, cy + 0.08 * s), (cx + 0.02 * s, cy + 0.08 * s), (cx - 0.22 * s, cy + s),
               (cx + 0.38 * s, cy - 0.12 * s), (cx + 0.02 * s, cy - 0.12 * s), (cx + 0.2 * s, cy - s)])]


def padlock(cx, cy, s, k):
    body = mg.rrect_pts(cx - s, cy, 2 * s, 1.5 * s, 0.2 * s, 4)
    lift = 0.6 * s * k
    shackle = np.column_stack([cx - 0.6 * s + 1.2 * s * (0.5 - 0.5 * np.cos(np.linspace(0, math.pi, 30))),
                               cy - lift - 0.9 * s * np.sin(np.linspace(0, math.pi, 30))])
    legs = [P([(cx - 0.6 * s, cy - lift), (cx - 0.6 * s, cy)]) if k < 0.5 else P([(cx - 0.6 * s, cy - lift), (cx - 0.6 * s, cy - lift + 0.2 * s)]),
            P([(cx + 0.6 * s, cy - lift), (cx + 0.6 * s, cy)])]
    return [body, shackle, ellipse(cx, cy + 0.6 * s, 0.15 * s, 0.15 * s, 0, 360, 12)] + legs


def scan(cx, cy, s):
    return [mg.rrect_pts(cx - 0.8 * s, cy - s, 1.6 * s, 2 * s, 0.08 * s, 4), ellipse(cx, cy - 0.45 * s, 0.25 * s, 0.3 * s, 0, 360, 24),
            P([(cx, cy - 0.15 * s), (cx, cy + 0.6 * s)])] + [P([(cx - 0.35 * s, cy + k * 0.18 * s), (cx + 0.35 * s, cy + k * 0.18 * s)]) for k in range(4)]


def letter(cx, cy, s):
    return [P([(cx - 0.7 * s, cy - s), (cx + 0.5 * s, cy - s), (cx + 0.7 * s, cy - 0.8 * s), (cx + 0.7 * s, cy + s), (cx - 0.7 * s, cy + s), (cx - 0.7 * s, cy - s)])] + \
           [P([(cx - 0.5 * s, cy - 0.6 * s + k * 0.3 * s), (cx + (0.2 + 0.3 * ((k * 37) % 5) / 5) * s, cy - 0.6 * s + k * 0.3 * s)]) for k in range(6)]


def chart(x0, y0, w, h, pts, k=1.0):
    out = [P([(x0, y0 - h), (x0, y0), (x0 + w, y0)])]
    q = np.array([(x0 + u * w, y0 - v * h) for u, v in pts])
    n = max(2, int(len(q) * k))
    return out + [q[:n]]


CITY = np.column_stack([RNG.uniform(120, 1800, 9000), 150 + 700 * RNG.beta(2.2, 1.3, 9000)])


# ---------------------------------------------------------------- GROUND
T_1865, T_ECON, T_COAL = wd("coal", "eighteen"), wd("coal", "economist"), wd("coal", "coal.")
T_ENG, T_EFF, T_LESS = ls("engines"), wd("engines", "efficient."), wd("engines", "less")
T_MORE0, T_BURNED = ls("more"), wd("more", "burned", 1)
T_AI, T_AIW = ls("ai"), wd("ai", "AI.")
T_MECH = ls("mech")
COAL_UP = [(u, 0.15 + 0.7 * u ** 1.5 + 0.02 * math.sin(u * 20)) for u in np.linspace(0, 1, 30)]


def ground(c, t):
    a = win(t, 1.2, T_MECH + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    rot = t * 2.5
    with layer(c, a):
        k1 = 1 - ease(seg(t, T_MORE0 - 0.2, T_MORE0 + 0.3))
        if k1 > 0:
            with layer(c, k1):
                bignum(c, t, "1865", 130, CX, 230, T_1865)
                label(c, "WILLIAM STANLEY JEVONS · THE COAL QUESTION", CX, 330, t, T_ECON, 22, SOFT, a=a * k1)
                lines_in(c, engine_shape(700, 560, 150, rot), t, T_COAL - 0.6, 0.7, WHITE, 1.8)
                pile = keys(t, [(T_LESS - 0.2, 200.0), (T_LESS + 0.6, 90.0)])
                lines_in(c, coal(1180, GROUND_Y, pile), t, T_COAL - 0.2, 0.5, GLOW, 1.7)
                ev(T_COAL - 0.6, "hydraulic", t, 700)
                label(c, "FAR MORE EFFICIENT", 700, 820, t, T_EFF, 22, WHITE, a=a * k1)
                label(c, "LESS COAL FOR THE SAME WORK", 1180, 860 - 30, t, T_LESS, 20, GLOW, a=a * k1)
        if t >= T_MORE0 - 0.2:                                              # the coal line goes up
            kc = ease(seg(t, T_MORE0 - 0.2, T_MORE0 + 0.3)) * (1 - ease(seg(t, T_AI - 0.1, T_AI + 0.4)))
            with layer(c, kc):
                stroke_polys(c, chart(460, 760, 1000, 420, COAL_UP, seg(t, T_MORE0, T_BURNED + 0.5)), WHITE, 2.4, 1.0)
                label(c, "BRITAIN'S COAL USE", 460, 320, t, T_MORE0 + 0.2, 20, GLOW, "left", a=a * kc)
                label(c, "IT BURNED MORE", 1300, 300, t, T_BURNED, 26, WHITE, a=a * kc)
                ev(T_BURNED, "riser", t, 1300)
        if t >= T_AI - 0.1:
            lines_in(c, chip(CX, 520, 140), t, T_AI - 0.1, 0.6, WHITE, 1.8)
            c.drawRect(skia.Rect.MakeXYWH(CX - 70, 450, 140, 140), mg.fill(GLOW, 0.85 * ease(seg(t, T_AIW - 0.2, T_AIW + 0.2))))
            label(c, "AI", CX, 540, t, T_AIW, 40, "#0B0C0E", a=a)
            ev(T_AI - 0.1, "form", t, CX)


# ---------------------------------------------------------------- MECHANISM
T_CHEAPER, T_SAVE, T_NEW = wd("mech", "cheaper,"), wd("mech", "save"), wd("mech", "new")
T_LIGHT0, T_3K = ls("light"), wd("light", "three")
T_USED0, T_40K = ls("used"), wd("used", "forty")
T_LIT0, T_STREET, T_SHOP, T_SCREEN = ls("lit"), wd("lit", "Streetlights."), wd("lit", "Shop"), wd("lit", "Screens.")
T_CURVE = ls("curve")


def mechanism(c, t):
    a = win(t, T_MECH - 0.05, T_CURVE + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        km = 1 - ease(seg(t, T_LIGHT0 - 0.2, T_LIGHT0 + 0.3))
        if km > 0:                                                          # cheaper, then new uses
            with layer(c, km):
                y = keys(t, [(T_CHEAPER - 0.2, 300), (T_CHEAPER + 0.6, 620)])
                stroke_polys(c, [mg.rrect_pts(760, y - 50, 260, 100, 14, 4), ellipse(795, y, 12, 12, 0, 360, 12)], WHITE, 2.0, 1.0)
                label(c, "PRICE", 905, y + 10, t, T_MECH + 0.3, 26, WHITE, a=a * km)
                label(c, "CHEAPER", 890, y + 90, t, T_CHEAPER, 22, GLOW, a=a * km)
                ev(T_CHEAPER, "whoosh", t, 890)
                for k, (x, shape) in enumerate(((1250, screen(1250, 560, 120)), (1450, bulb(1450, 380, 60)), (1650, streetlight(1620, 560, 260)))):
                    tk = T_NEW + 0.2 * k
                    if t >= tk:
                        lines_in(c, shape, t, tk, 0.4, GLOW, 1.8)
                        ev(tk, "pop", t, x)
                label(c, "NEW USES", 1450, 640, t, T_NEW + 0.1, 22, WHITE, a=a * km)
        if t >= T_LIGHT0 - 0.2:
            kl = ease(seg(t, T_LIGHT0 - 0.2, T_LIGHT0 + 0.3)) * (1 - ease(seg(t, T_LIT0 - 0.2, T_LIT0 + 0.3)))
            with layer(c, kl):
                lines_in(c, candle(520, 700, 160), t, T_LIGHT0 + 0.1, 0.5, WHITE, 1.8)
                label(c, "1800", 520, 760, t, T_LIGHT0 + 0.4, 20, SOFT, a=a * kl)
                if t < T_USED0 - 0.05:
                    bignum(c, t, "3,000×", 120, CX + 150, 330, T_3K - 0.1)
                    label(c, "CHEAPER LIGHT · BRITAIN, 1800–2000", CX + 150, 430, t, T_3K + 0.5, 22, SOFT, a=a * kl)
                else:
                    roll(c, "3,000×", "40,000×", 120, CX + 150, 330, t, T_3K - 0.1, T_40K - 0.1)
                    label(c, "MORE LIGHT USED", CX + 150, 430, t, T_40K + 0.4, 22, GLOW, a=a * kl)
                if t >= T_USED0:                                            # a night city of dots
                    n = int(9000 * ease(seg(t, T_40K - 0.3, T_40K + 1.2), "i"))
                    points(c, CITY[:n], 0.8, GOLD, 2.4)
                    ev(T_40K - 0.3, "grains", t, CX)
        if t >= T_LIT0 - 0.2:                                               # things nobody would have lit
            kt = ease(seg(t, T_LIT0 - 0.2, T_LIT0 + 0.3))
            with layer(c, kt):
                for tt, shape, x, txt in ((T_STREET, streetlight(520, GROUND_Y, 380), 560, "STREETLIGHTS"), (T_SHOP, shop(CX, GROUND_Y, 300), CX, "SHOP WINDOWS"),
                                          (T_SCREEN, screen(1400, GROUND_Y, 280), 1400, "SCREENS")):
                    if t >= tt - 0.2:
                        lines_in(c, shape, t, tt - 0.2, 0.4, WHITE, 1.9)
                        label(c, txt, x, 850 - 20, t, tt, 20, GLOW, a=a * kt)
                        ev(tt, "latch", t, x)
                if t >= wd("lit", "fortune.") - 0.3:
                    label(c, "WHEN LIGHT COST A FORTUNE, NOBODY LIT THESE", CX, 250, t, wd("lit", "Things"), 22, SOFT, a=a * kt)


# ---------------------------------------------------------------- NOW
T_SAMEC = wd("curve", "curve.")
T_TOK0, T_NOVELS, T_60, T_6C = ls("tokens"), wd("tokens", "novels"), wd("tokens", "sixty"), wd("tokens", "six")
T_MACS0, T_TEN, T_HUND = ls("macs"), wd("macs", "ten,"), wd("macs", "hundredth")
T_GOO0, T_EXPL, T_QUAD = ls("google"), wd("google", "exploded."), wd("google", "quadrillion")
T_TIMES0, T_300 = ls("times"), wd("times", "three")
T_NAD0, T_POSTED, T_JEVONS = ls("nadella"), wd("nadella", "posted:"), wd("nadella", "Jevons")
T_UNLOCK = ls("unlock")
PRICE_DOWN = [(u, 0.9 * math.exp(-4 * u) + 0.05) for u in np.linspace(0, 1, 30)]
USE_UP = [(u, 0.05 + 0.85 * u ** 2.4) for u in np.linspace(0, 1, 30)]


def now(c, t):
    a = win(t, T_CURVE - 0.05, T_UNLOCK + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kc = 1 - ease(seg(t, T_TOK0 - 0.2, T_TOK0 + 0.3))
        if kc > 0:                                                          # the same curve
            with layer(c, kc):
                stroke_polys(c, chart(460, 780, 1000, 440, PRICE_DOWN, seg(t, T_CURVE, T_CURVE + 0.9)), GLOW, 2.4, 1.0)
                stroke_polys(c, chart(460, 780, 1000, 440, USE_UP, seg(t, T_CURVE + 0.3, T_CURVE + 1.2))[1:], WHITE, 2.4, 1.0)
                label(c, "PRICE", 560, 360, t, T_CURVE + 0.2, 22, GLOW, a=a * kc)
                label(c, "USE", 1380, 380, t, T_SAMEC, 22, WHITE, a=a * kc)
        kt = win(t, T_TOK0 - 0.1, T_GOO0 + 0.2, 0.3, 0.4)
        if kt > 0:                                                          # eight novels; $60 -> $0.06; Big Macs
            with layer(c, kt):
                label(c, "A MILLION TOKENS ≈ 8 NOVELS", CX, 180, t, T_NOVELS - 0.2, 22, SOFT, a=a * kt)
                kb = 1 - ease(seg(t, T_MACS0 - 0.2, T_MACS0 + 0.2))
                for k in range(8):
                    tk = T_NOVELS - 0.1 + 0.06 * k
                    if t >= tk:
                        stroke_polys(c, book(640 + 82 * k, 230, 60, 90), WHITE, 1.6, kb)
                if t < T_6C - 0.05:
                    bignum(c, t, "$60", 130, CX, 480, T_60 - 0.1)
                    label(c, "2021", CX, 580, t, T_60 + 0.3, 20, SOFT, a=a * kt * kb)
                else:
                    with layer(c, kb):
                        roll(c, "$60", "$0.06", 130, CX, 480, t, T_60 - 0.1, T_6C - 0.1)
                        label(c, "2024", CX, 580, t, T_6C + 0.2, 20, SOFT, a=a * kt)
                if t >= T_MACS0 - 0.2:                                      # ten Big Macs, then a hundredth of one
                    kmac = ease(seg(t, T_MACS0 - 0.2, T_MACS0 + 0.3))
                    shrink = ease(seg(t, T_HUND - 0.1, T_HUND + 0.6))
                    for k in range(10):
                        tk = T_TEN - 0.5 + 0.05 * k
                        if t < tk:
                            continue
                        x = 370 + 131 * k
                        aa = kmac * (1 - shrink) if k else kmac
                        if k == 0 and shrink > 0:
                            c.save()
                            w = lerp(120, 1.5, shrink)
                            c.clipRect(skia.Rect.MakeXYWH(x - 60, 400, w, 200))
                            mac_icon(c, x, 500, 58, kmac)
                            c.restore()
                        else:
                            mac_icon(c, x, 500, 58, aa)
                        ev(tk, "tick", t, x)
                    label(c, "ABOUT 10 BIG MACS", CX, 660, t, T_TEN, 24, WHITE, a=a * kt * (1 - shrink))
                    label(c, "A HUNDREDTH OF ONE", 430, 660, t, T_HUND + 0.2, 24, GLOW, "left", a=a * kt * shrink)
        kg = win(t, T_GOO0 - 0.1, T_NAD0 + 0.2, 0.3, 0.4)
        if kg > 0:                                                          # use exploded
            with layer(c, kg):
                n = int(6000 * ease(seg(t, T_EXPL - 0.2, T_EXPL + 1.4), "o"))
                ang = RNG.uniform(0, 2 * math.pi, 6000) if "ang" not in _S else _S["ang"]
                _S.setdefault("ang", ang)
                rad = _S.setdefault("rad", RNG.gamma(2.0, 170, 6000))
                sp = ease(seg(t, T_EXPL - 0.2, T_EXPL + 1.6), "o")
                X = np.column_stack([CX + np.cos(_S["ang"][:n]) * _S["rad"][:n] * sp * 1.6, 520 + np.sin(_S["ang"][:n]) * _S["rad"][:n] * sp * 0.9])
                points(c, X, 0.75 * (1 - ease(seg(t, T_TIMES0 - 0.2, T_TIMES0 + 0.3))), WHITE, 2.2)
                ev(T_EXPL - 0.2, "zoom", t, CX)
                kq = 1 - ease(seg(t, T_TIMES0 - 0.2, T_TIMES0 + 0.2))
                with layer(c, kq):
                    bignum(c, t, "3.2 QUADRILLION", 100, CX, 240, T_QUAD - 0.3)
                    label(c, "TOKENS A MONTH · GOOGLE, MAY 2026", CX, 330, t, T_QUAD + 0.4, 22, SOFT, a=a * kg * kq)
                if t >= T_TIMES0 - 0.2:                                     # 300x in two years
                    k3 = ease(seg(t, T_TIMES0 - 0.2, T_TIMES0 + 0.2))
                    with layer(c, k3):
                        c.drawRect(skia.Rect.MakeXYWH(360, 470, 4, 60), mg.fill(GLOW, 0.95))
                        label(c, "MAY 2024", 360, 450, t, T_TIMES0, 20, SOFT, "left", a=a * k3)
                        c.drawRect(skia.Rect.MakeXYWH(360, 600, 1200 * ease(seg(t, T_300 - 0.2, T_300 + 0.8)), 60), mg.chrome_paint(600, 660, 0.95))
                        label(c, "MAY 2026: MORE THAN 300×", 360, 580, t, T_300, 22, WHITE, "left", a=a * k3)
                        ev(T_300 - 0.2, "riser", t, 900)
        kn = win(t, T_NAD0 - 0.1, T_UNLOCK + 0.2, 0.3, 0.4)
        if kn > 0:                                                          # the post
            with layer(c, kn):
                bignum(c, t, "27 JAN 2025", 100, CX, 230, T_NAD0 + 0.1)
                lines_in(c, [mg.rrect_pts(CX - 460, 400, 920, 260, 18, 5), ellipse(CX - 380, 470, 34, 34, 0, 360, 24)], t, T_NAD0 + 0.6, 0.5, WHITE, 1.8)
                label(c, "SATYA NADELLA · MICROSOFT", CX - 330, 478, t, wd("nadella", "Microsoft's"), 20, SOFT, "left", a=a * kn)
                label(c, "Jevons paradox strikes again!", CX - 400, 580, t, T_JEVONS - 0.15, 34, WHITE, "left", a=a * kn, cps=20)
                ev(T_POSTED, "paper", t, CX)


_S = {}


# ---------------------------------------------------------------- IDEA
T_UNLOCKS, T_DC, T_POWER, T_CHIPS, T_FEWER = wd("unlock", "unlocks"), wd("why", "data"), wd("why", "power"), wd("why", "chips."), wd("why", "fewer.")
T_IMAGINE = ls("imagine")


def idea(c, t):
    a = win(t, T_UNLOCK - 0.05, T_IMAGINE + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kl = 1 - ease(seg(t, ls("why") - 0.2, ls("why") + 0.3))
        if kl > 0:
            with layer(c, kl):
                stroke_polys(c, padlock(CX, 470, 90, ease(seg(t, T_UNLOCKS - 0.1, T_UNLOCKS + 0.4))), WHITE, 2.2, 1.0)
                label(c, "EFFICIENCY DOESN'T SHRINK DEMAND", CX, 250, t, T_UNLOCK + 0.2, 22, SOFT, a=a * kl)
                label(c, "IT UNLOCKS IT", CX, 740, t, T_UNLOCKS, 28, WHITE, a=a * kl)
                ev(T_UNLOCKS, "latch", t, CX)
        if t >= ls("why") - 0.2:
            kw = ease(seg(t, ls("why") - 0.2, ls("why") + 0.3))
            with layer(c, kw):
                for tt, shape, x, txt in ((T_DC, racks(420, 700, 4), 570, "MORE DATA CENTRES"), (T_POWER, bolt(CX, 560, 130), CX, "MORE POWER"),
                                          (T_CHIPS, chip(1380, 560, 110), 1380, "MORE CHIPS")):
                    if t >= tt - 0.2:
                        lines_in(c, shape, t, tt - 0.2, 0.4, WHITE, 1.9)
                        label(c, txt, x, 790, t, tt, 22, GLOW, a=a * kw)
                        ev(tt, "latch", t, x)
                label(c, "NOT FEWER", CX, 250, t, T_FEWER - 0.1, 30, WHITE, a=a * kw)


# ---------------------------------------------------------------- IMAGINE
T_LIGHTW, T_WHATIF = wd("imagine", "light."), ls("whatif")
T_TUTOR, T_SCAN, T_LETTER = wd("uses", "tutor"), wd("uses", "scan."), wd("uses", "letter")
T_Q, T_MOREDO = ls("question"), wd("question", "more")
T_THEN = ls("then")


def imagine(c, t):
    a = win(t, T_IMAGINE - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        kb = 1 - ease(seg(t, ls("uses") - 0.2, ls("uses") + 0.3))
        if kb > 0:
            with layer(c, kb):
                lines_in(c, bulb(CX, 430, 120), t, T_IMAGINE + 0.1, 0.6, WHITE, 1.8)
                stroke_polys(c, chip(CX, 440, 40), GLOW, 1.6, ease(seg(t, T_LIGHTW - 0.3, T_LIGHTW + 0.2)))
                label(c, "THINKING, AS CHEAP AS LIGHT", CX, 780, t, T_LIGHTW - 0.2, 24, WHITE, a=a * kb)
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 230, t, T_WHATIF + 0.05, 24, WHITE, a=a * kb)
        if t >= ls("uses") - 0.2:
            ku = ease(seg(t, ls("uses") - 0.2, ls("uses") + 0.3))
            with layer(c, ku):
                label(c, "WHAT NOBODY BOTHERS WITH TODAY", CX, 230, t, ls("uses") + 0.2, 22, SOFT, a=a * ku)
                if t >= T_TUTOR - 0.2:
                    p1, _ = figure(500, 560, 240, dict(STAND, rs=40, re=40), 1)
                    p2, _ = figure(620, 600, 150, STAND, -1)
                    lines_in(c, p1 + p2 + [rect(535, 520, 60, 40)], t, T_TUTOR - 0.2, 0.5, WHITE, 1.8)
                    label(c, "A TUTOR FOR EVERY CHILD", 560, 780, t, T_TUTOR + 0.1, 20, GLOW, a=a * ku)
                    ev(T_TUTOR - 0.2, "form", t, 560)
                if t >= T_SCAN - 0.3:
                    lines_in(c, scan(CX, 540, 130), t, T_SCAN - 0.3, 0.5, WHITE, 1.8)
                    label(c, "A SECOND LOOK AT EVERY SCAN", CX, 780, t, T_SCAN, 20, GLOW, a=a * ku)
                    ev(T_SCAN - 0.3, "scan", t, CX)
                if t >= T_LETTER - 0.3:
                    lines_in(c, letter(1400, 540, 130), t, T_LETTER - 0.3, 0.5, WHITE, 1.8)
                    label(c, "EVERY LETTER EXPLAINED", 1400, 780, t, T_LETTER, 20, GLOW, a=a * ku)
                    ev(T_LETTER - 0.3, "paper", t, 1400)
                if t >= T_Q:
                    label(c, "NOT HOW MUCH WE SAVE · HOW MUCH MORE WE DO", CX, 850 - 20, t, T_MOREDO - 0.3, 22, WHITE, a=a)


# ---------------------------------------------------------------- SURFACE
T_1865B, T_COALB = wd("then", "eighteen"), wd("then", "coal.")
T_2026, T_THINK = wd("now2", "twenty"), wd("now2", "thinking.")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "W. S. Jevons, The Coal Question, 1865",
           "Fouquet & Pearson, The Energy Journal 27(1), 2006: light in Britain, 1800-2000",
           "a16z, \"Welcome to LLMflation\", Nov 2024: a million tokens, ~$60 to ~$0.06",
           "Google I/O, May 2026: ~3,200 trillion tokens a month (9.7 trillion two years earlier)",
           "Satya Nadella, LinkedIn and X, 27 Jan 2025 · Big Mac $6.22: The Economist, July 2026",
           "The section on thinking as cheap as light is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 820)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 820))
            bignum(c, t, "1865", 130, 560, 250, T_1865B)
            lines_in(c, engine_shape(520, 540, 100, t * 2.5) + coal(760, 700, 90), t, T_1865B + 0.3, 0.6, WHITE, 1.8)
            label(c, "BETTER ENGINES, MORE COAL", 560, 790, t, T_COALB - 0.3, 20, GLOW, a=a)
            if t >= T_2026 - 0.05:
                bignum(c, t, "2026", 130, 1360, 250, T_2026 - 0.05)
                lines_in(c, chip(1360, 540, 100), t, T_2026 + 0.2, 0.5, WHITE, 1.8)
                c.drawRect(skia.Rect.MakeXYWH(1360 - 50, 540 - 50, 100, 100), mg.fill(GLOW, 0.85 * ease(seg(t, T_THINK - 0.4, T_THINK))))
                label(c, "CHEAPER THINKING, MORE THINKING", 1360, 790, t, T_THINK - 0.5, 20, GLOW, a=a)
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
