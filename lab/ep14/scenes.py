"""EP14 · THE YES MACHINE, the scenes: line art keyed to the script's line ids and George's words (engine.tl.word), which
the engine turns into characters. One device runs through it: a thumbs-up, the button that taught a machine to flatter,
set against a pair of scales, AGREES WITH YOU on one pan and CORRECT on the other.

  GROUND     25 to 29 April 2025 filling day by day, the update and the rollback; a column of replies all ticked; a gift
             box, $30,000 and a praising tick; the question
  MECHANISM  two answers and the one picked; a field of pairs multiplying; the scales tipping to AGREES WITH YOU
             (Anthropic, 2023); the thumbs; the signal that held sycophancy in check, weakening
  NOW        500,000,000 a week as a field of points; health, money, plans, and a mirror; the rollback arrow and the pull
  IDEA       the emperor in a suit drawn in dashes, three courtiers bowing; a child pointing; a chip that bows
  IMAGINE    DID YOU LIKE IT? struck through, WERE YOU RIGHT A MONTH LATER? ticked; a NO in a bubble; thumbs up or down?
  SURFACE    three questions to ask; the thumbs-up, April 2025; still there; the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         stroke_polys, bignum, chip, page, burst, keys, dotted_num, figure)

TRAILS = []
GLINTS = []
RNG = np.random.default_rng(14)


def part(t, a, b, fin=0.3, fout=0.4):
    return win(t, a - 0.1, b + 0.2, fin, fout)


# ---------------------------------------------------------------- shapes
def thumb(cx, cy, s, down=False):
    """A thumbs-up (or down): the fist, three finger lines, the thumb, the cuff."""
    k = -1 if down else 1
    def q(x, y):
        return (cx + x * s, cy + k * y * s)
    out = [P([q(-0.45, -0.05), q(0.32, -0.05), q(0.38, 0.05), q(0.38, 0.55), q(0.3, 0.62), q(-0.45, 0.62), q(-0.45, -0.05)])]
    for y in (0.13, 0.29, 0.45):
        out.append(P([q(0.0, y), q(0.38, y)]))
    out.append(P([q(-0.45, -0.05), q(-0.36, -0.55), q(-0.28, -0.72), q(-0.14, -0.72), q(-0.1, -0.5), q(-0.12, -0.05)]))
    out.append(P([q(-0.72, -0.08), q(-0.5, -0.08), q(-0.5, 0.65), q(-0.72, 0.65), q(-0.72, -0.08)]))
    return out


def bubble(cx, cy, w, h):
    return [P([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 4, cy + h / 2),
               (cx - w / 3, cy + h / 2 + 0.3 * h), (cx - w / 3 - 0.02 * w, cy + h / 2), (cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2)])]


def tick(cx, cy, s):
    return [P([(cx - s, cy), (cx - 0.3 * s, cy + 0.7 * s), (cx + s, cy - 0.8 * s)])]


def cross(cx, cy, s):
    return [P([(cx - s, cy - s), (cx + s, cy + s)]), P([(cx + s, cy - s), (cx - s, cy + s)])]


def gift(cx, cy, s):
    """A gift box with its ribbon and bow."""
    return [rect(cx - s, cy - 0.6 * s, 2 * s, 1.4 * s), rect(cx - 1.1 * s, cy - 0.9 * s, 2.2 * s, 0.3 * s),
            P([(cx, cy - 0.9 * s), (cx, cy + 0.8 * s)]),
            P([(cx, cy - 0.9 * s), (cx - 0.5 * s, cy - 1.35 * s), (cx - 0.6 * s, cy - 1.0 * s), (cx, cy - 0.9 * s)]),
            P([(cx, cy - 0.9 * s), (cx + 0.5 * s, cy - 1.35 * s), (cx + 0.6 * s, cy - 1.0 * s), (cx, cy - 0.9 * s)])]


def scales(cx, cy, w, tilt):
    """A pair of scales: the post, the beam tilted by `tilt` (radians, + = left pan down) and two hanging pans."""
    out = [P([(cx, cy), (cx, cy + 300)]), P([(cx - 70, cy + 300), (cx + 70, cy + 300)])]
    dx, dy = w * math.cos(tilt), w * math.sin(tilt)
    lx, ly, rx_, ry = cx - dx, cy + dy, cx + dx, cy - dy
    out.append(P([(lx, ly), (rx_, ry)]))
    pans = []
    for (x, y) in ((lx, ly), (rx_, ry)):
        out += [P([(x, y), (x - 70, y + 120)]), P([(x, y), (x + 70, y + 120)])]
        arc = np.column_stack([x + 90 * np.cos(np.linspace(0, math.pi, 24)), y + 120 + 30 * np.sin(np.linspace(0, math.pi, 24))])
        out.append(np.vstack([[x - 90, y + 120], arc[::-1], [x + 90, y + 120]]))
        pans.append((x, y + 120))
    return out, pans


def mirror_shape(cx, cy, rx, ry):
    return [ellipse(cx, cy, rx, ry, 0, 360, 80), ellipse(cx, cy, rx * 0.86, ry * 0.9, 0, 360, 80),
            P([(cx - 0.4 * rx, cy - 0.5 * ry), (cx - 0.1 * rx, cy - 0.75 * ry)]), P([(cx - 0.45 * rx, cy - 0.2 * ry), (cx + 0.05 * rx, cy - 0.65 * ry)])]


def rollback(cx, cy, r):
    a = np.radians(np.linspace(-30, 210, 50))
    arc = np.column_stack([cx + r * np.cos(a), cy - r * np.sin(a)])
    x1, y1 = arc[-1]
    return [arc, P([(x1 - 22, y1 - 26), (x1, y1), (x1 + 28, y1 - 14)])]


BOW = dict(lean=55, head=20, ls=20, le=10, rs=10, re=10, lh=4, lk=0, rh=-4, rk=0)
STAND = dict(lean=0, head=0, ls=8, le=10, rs=-8, re=10, lh=4, lk=0, rh=-4, rk=0)
POINT = dict(lean=-4, head=-6, ls=8, le=10, rs=130, re=-10, lh=4, lk=0, rh=-4, rk=0)


def crown(c, j, s, a, col=GOLD):
    hx, hy = j["head"]
    r = 0.062 * s
    stroke_polys(c, [P([(hx - r, hy - 1.1 * r), (hx - r, hy - 1.9 * r), (hx - 0.5 * r, hy - 1.4 * r), (hx, hy - 2.1 * r),
                        (hx + 0.5 * r, hy - 1.4 * r), (hx + r, hy - 1.9 * r), (hx + r, hy - 1.1 * r)])], col, 2.2, a)


def dashed(c, polys, col, w, a, on=14, off=10):
    p = mg.stroke(col, w, a)
    p.setPathEffect(skia.DashPathEffect.Make([on, off], 0))
    for q in polys:
        path = skia.Path()
        path.moveTo(*q[0])
        for x, y in q[1:]:
            path.lineTo(x, y)
        c.drawPath(path, p)


# ---------------------------------------------------------------- GROUND
T_A0, T_UPD, T_FOUR, T_BACK = ls("april"), wd("april", "updated"), wd("april", "four"), wd("april", "back.")
T_AG0, T_AGREED = ls("agreed"), wd("agreed", "agreed")
T_G0, T_JOKE, T_PRAISED, T_THIRTY = ls("gag"), wd("gag", "joke"), wd("gag", "praised"), wd("gag", "thirty")
T_HOW0 = ls("how")
T_PICK0 = ls("pick")


def ground(c, t):
    a = win(t, 0.8, T_PICK0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kd = part(t, T_A0, T_AG0)
        if kd > 0:                                                          # 25 to 29 April: the update, then the rollback
            with layer(c, kd):
                label(c, "APRIL 2025", CX, 200, t, T_A0 + 0.2, 26, WHITE, a=a * kd)
                for i, d in enumerate(range(25, 30)):
                    x = 460 + i * 250
                    td = T_UPD - 0.3 + (T_BACK - T_UPD) * i / 4
                    lines_in(c, [rect(x - 100, 380, 200, 200, 0.0)], t, T_A0 + 0.3 + 0.08 * i, 0.4, WHITE, 1.8)
                    label(c, str(d), x, 430, t, T_A0 + 0.4 + 0.08 * i, 28, WHITE, a=a * kd)
                    if t >= td:
                        c.drawRect(skia.Rect.MakeXYWH(x - 92, 460, 184, 112), mg.fill(GOLD if i == 4 else GLOW, 0.55 * a * kd))
                        ev(td, "tick", t, x)
                label(c, "THE UPDATE", 460, 640, t, T_UPD, 22, GLOW, a=a * kd)
                label(c, "ROLLED BACK", 1460, 640, t, T_BACK - 0.4, 22, GOLD, a=a * kd)
                bignum(c, t, "4 DAYS", 100, CX, 820, T_FOUR - 0.2)
        kg = part(t, T_AG0, T_HOW0)
        if kg > 0:                                                          # agreed with everything; the joke gift
            with layer(c, kg):
                for i in range(5):
                    ti = T_AG0 + 0.12 * i
                    y = 260 + i * 120
                    lines_in(c, bubble(420, y, 380, 80), t, ti, 0.3, SOFT, 1.6)
                    if t >= T_AGREED - 0.2 + 0.1 * i:
                        stroke_polys(c, tick(560, y, 22), GLOW, 3.0, a * kg)
                        ev(T_AGREED - 0.2 + 0.1 * i, "tick", t, 560)
                label(c, "AGREED WITH ALMOST EVERYTHING", 420, 900, t, T_AGREED, 20, GLOW, a=a * kg)
                if t >= T_G0 - 0.2:
                    lines_in(c, gift(1260, 520, 150), t, T_JOKE - 0.5, 0.6, WHITE, 2.0)
                    label(c, "A JOKE GAG GIFT", 1260, 760, t, T_JOKE - 0.2, 22, SOFT, a=a * kg)
                    if t >= T_PRAISED - 0.3:
                        lines_in(c, bubble(1560, 300, 220, 110), t, T_PRAISED - 0.3, 0.4, GLOW, 2.0)
                        stroke_polys(c, tick(1560, 300, 30), GLOW, 3.2, a * kg)
                        label(c, "PRAISED IT", 1560, 400, t, T_PRAISED, 20, GLOW, a=a * kg)
                    bignum(c, t, "$30,000", 90, 1260, 230, T_THIRTY - 0.3)
        if t >= T_HOW0 - 0.1:
            kh = ease(seg(t, T_HOW0 - 0.1, T_HOW0 + 0.3))
            label(c, "HOW DOES A MACHINE LEARN TO FLATTER?", CX, 540, t, T_HOW0 + 0.1, 30, WHITE, a=a * kh, cps=30)


# ---------------------------------------------------------------- MECHANISM
T_TWO, T_LIKE = wd("pick", "two"), wd("pick", "like")
T_MIL0, T_MILLIONS, T_LEARNS = ls("millions"), wd("millions", "millions"), wd("millions", "learns")
T_ST0, T_AGREE, T_WRONG = ls("study"), wd("study", "agree"), wd("study", "wrong")
T_TH0, T_UP, T_DOWN = ls("thumbs"), wd("thumbs", "up"), wd("thumbs", "down")
T_W0, T_WEAK, T_CHECK = ls("weakened"), wd("weakened", "weakened"), wd("weakened", "check.")
T_SC0 = ls("scale")
PAIRS = RNG.uniform([180, 220], [1740, 820], (900, 2))


def mechanism(c, t):
    a = win(t, T_PICK0 - 0.05, T_SC0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kp = part(t, T_PICK0, T_MIL0)
        if kp > 0:                                                          # two answers, one picked
            with layer(c, kp):
                label(c, "SHAPED BY WHAT PEOPLE PREFER", CX, 180, t, T_PICK0 + 0.2, 24, WHITE, a=a * kp)
                for i, x in enumerate((640, 1280)):
                    lines_in(c, page(x - 150, 300, 300, 380), t, min(T_TWO - 0.4, T_PICK0 + 0.6) + 0.2 * i, 0.5, WHITE, 1.8)
                    label(c, ("ANSWER A", "ANSWER B")[i], x, 270, t, T_TWO - 0.2 + 0.2 * i, 22, SOFT, a=a * kp)
                if t >= T_LIKE - 0.4:
                    kk = ease(seg(t, T_LIKE - 0.4, T_LIKE))
                    c.drawRect(skia.Rect.MakeXYWH(1110, 280, 340, 420), mg.stroke(GOLD, 3.0, a * kp * kk))
                    stroke_polys(c, thumb(1280, 790, 60), GOLD, 2.4, a * kp * kk)
                    label(c, "THE ONE THEY LIKE MORE", 1280, 900, t, T_LIKE - 0.2, 20, GOLD, a=a * kp)
                    ev(T_LIKE - 0.4, "confirm", t, 1280)
        km = part(t, T_MIL0, T_ST0)
        if km > 0:                                                          # millions of times
            with layer(c, km):
                n = int(len(PAIRS) * ease(seg(t, T_MIL0, T_MILLIONS + 0.6)))
                for i in range(n):
                    x, y = PAIRS[i]
                    c.drawRect(skia.Rect.MakeXYWH(x, y, 7, 9), mg.fill(SOFT, 0.5 * a * km))
                    c.drawRect(skia.Rect.MakeXYWH(x + 10, y, 7, 9), mg.fill(GOLD if i % 3 else GLOW, 0.8 * a * km))
                bignum(c, t, "× MILLIONS", 90, CX, 520, T_MILLIONS - 0.2)
                label(c, "THE MODEL LEARNS WHAT PEOPLE LIKE", CX, 900, t, T_LEARNS - 0.3, 22, WHITE, a=a * km)
                ev(T_MIL0, "grains", t, CX)
        ks = part(t, T_ST0, T_TH0)
        if ks > 0:                                                          # the scales tip to AGREES WITH YOU
            with layer(c, ks):
                tilt = 0.22 * ease(seg(t, T_AGREE - 0.3, T_AGREE + 0.6))
                polys, pans = scales(CX, 300, 380, tilt)
                lines_in(c, polys, t, T_ST0, 0.6, WHITE, 2.0)
                label(c, "AGREES WITH YOU", pans[0][0], pans[0][1] + 90, t, T_AGREE - 0.3, 22, GOLD, a=a * ks)
                label(c, "CORRECT", pans[1][0], pans[1][1] + 90, t, T_AGREE, 22, GLOW, a=a * ks)
                label(c, "ANTHROPIC · 2023 · TOWARDS UNDERSTANDING SYCOPHANCY", CX, 200, t, T_ST0 + 0.4, 20, SOFT, a=a * ks)
                label(c, "SOMETIMES: A CONVINCING WRONG ANSWER", CX, 880, t, T_WRONG - 0.4, 22, WHITE, a=a * ks)
                ev(T_AGREE - 0.3, "whoosh", t, CX)
        if t >= T_TH0 - 0.2:                                                # the thumbs; the signal weakening
            kt = ease(seg(t, T_TH0 - 0.2, T_TH0 + 0.3))
            with layer(c, kt):
                lines_in(c, thumb(760, 470, 170), t, T_UP - 0.5, 0.6, GOLD, 2.6)
                lines_in(c, thumb(1160, 470, 170, down=True), t, T_DOWN - 0.5, 0.6, SOFT, 2.2)
                label(c, "A NEW REWARD SIGNAL · APRIL 2025", CX, 200, t, T_TH0 + 0.2, 22, WHITE, a=a * kt)
                if t >= T_W0 - 0.3:
                    kw = ease(seg(t, T_WEAK - 0.2, T_CHECK))
                    w = lerp(900, 260, kw)
                    c.drawRect(skia.Rect.MakeXYWH(510, 780, 900, 40), mg.stroke(SOFT, 1.8, a * kt))
                    c.drawRect(skia.Rect.MakeXYWH(510, 780, w, 40), mg.fill(GLOW, 0.85 * a * kt))
                    label(c, "THE SIGNAL HOLDING SYCOPHANCY IN CHECK", CX, 760, t, T_W0, 20, GLOW, a=a * kt)
                    label(c, "WEAKENED", 510 + w + 20, 810, t, T_WEAK, 22, GOLD, "left", a=a * kt)
                    ev(T_WEAK - 0.2, "whoosh", t, CX)


# ---------------------------------------------------------------- NOW
T_FIVE, T_WEEK = wd("scale", "five"), wd("scale", "week")
T_MI0, T_HEALTH, T_MONEY, T_PLANS, T_MIRROR = ls("mirror"), wd("mirror", "health,"), wd("mirror", "money,"), wd("mirror", "plans."), wd("mirror", "mirror.")
T_PU0, T_ROLLED, T_PULL = ls("pull"), wd("pull", "rolled"), wd("pull", "pull")
T_STO0 = ls("story")
CROWD = RNG.uniform([160, 260], [1760, 820], (2400, 2))


def now(c, t):
    a = win(t, T_SC0 - 0.05, T_STO0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kc = part(t, T_SC0, T_MI0)
        if kc > 0:                                                          # 500 million a week
            with layer(c, kc):
                n = int(len(CROWD) * ease(seg(t, T_SC0, T_FIVE + 0.8)))
                for i in range(n):
                    x, y = CROWD[i]
                    c.drawCircle(x, y, 2.6, mg.fill(GLOW if i % 7 else WHITE, 0.6 * a * kc))
                bignum(c, t, "500,000,000", 100, CX, 540, T_FIVE - 0.2)
                label(c, "PEOPLE A WEEK · CHATGPT · APRIL 2025", CX, 640, t, T_WEEK - 0.3, 22, WHITE, a=a * kc)
        km = part(t, T_MI0, T_PU0)
        if km > 0:                                                          # health, money, plans; a mirror
            with layer(c, km):
                for i, (word_t, name) in enumerate(((T_HEALTH, "HEALTH"), (T_MONEY, "MONEY"), (T_PLANS, "PLANS"))):
                    y = 330 + i * 170
                    lines_in(c, bubble(560, y, 340, 100), t, word_t - 0.4, 0.4, WHITE, 1.8)
                    label(c, name + "?", 560, y + 10, t, word_t - 0.3, 26, WHITE, a=a * km)
                lines_in(c, mirror_shape(1300, 500, 210, 280), t, T_MIRROR - 0.7, 0.6, GLOW, 2.4)
                label(c, "AND GETTING A MIRROR", 1300, 860, t, T_MIRROR - 0.4, 24, GLOW, a=a * km)
                ev(T_MIRROR - 0.7, "swell", t, 1300)
        if t >= T_PU0 - 0.2:                                                # rolled back; the pull is still there
            kp = ease(seg(t, T_PU0 - 0.2, T_PU0 + 0.3))
            with layer(c, kp):
                lines_in(c, rollback(620, 520, 150), t, T_ROLLED - 0.4, 0.6, WHITE, 2.4)
                label(c, "ROLLED BACK · TESTS CHANGED", 620, 760, t, T_ROLLED, 20, WHITE, a=a * kp)
                polys, pans = scales(1300, 330, 260, 0.14)
                lines_in(c, polys, t, T_PULL - 0.6, 0.5, SOFT, 1.8)
                label(c, "AGREES", pans[0][0], pans[0][1] + 80, t, T_PULL - 0.3, 20, GOLD, a=a * kp)
                label(c, "THE PULL IS STILL THERE", 1300, 860, t, T_PULL - 0.2, 22, GOLD, a=a * kp)


# ---------------------------------------------------------------- IDEA
T_EM0, T_COURT, T_SUIT, T_DISAGREE = ls("emperor"), wd("emperor", "court"), wd("emperor", "suit"), wd("emperor", "disagrees.")
T_CH0, T_CHILD = ls("child"), wd("child", "child")
T_CO0, T_COURTIER, T_HEAR = ls("courtier"), wd("courtier", "courtier."), wd("courtier", "hear.")
T_IMAG0 = ls("imagine")
EX, EY, ES = 760, 560, 380                                       # the emperor: hips, height


def idea(c, t):
    a = win(t, T_STO0 - 0.05, T_IMAG0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "THERE'S AN OLD STORY ABOUT THIS", CX, 200, t, T_STO0 + 0.1, 26, WHITE,
              a=a * (1 - ease(seg(t, T_EM0 + 0.3, T_EM0 + 0.7))))
        ke = part(t, T_EM0, T_CO0)
        if ke > 0:                                                          # the emperor, the suit in dashes, the court
            with layer(c, ke):
                polys, j = figure(EX, EY, ES, STAND, 1)
                lines_in(c, polys, t, T_EM0 + 0.1, 0.6, WHITE, 2.0)
                crown(c, j, ES, a * ke * ease(seg(t, T_EM0 + 0.5, T_EM0 + 0.9)))
                label(c, "THE EMPEROR'S NEW CLOTHES · HANS CHRISTIAN ANDERSEN · 1837", CX, 180, t, T_EM0 + 0.2, 22, GOLD, a=a * ke)
                if t >= T_SUIT - 0.3:
                    ks = ease(seg(t, T_SUIT - 0.3, T_SUIT + 0.3))
                    dashed(c, [rect(EX - 95, EY - 0.33 * ES, 190, 0.62 * ES, 0.0)], GOLD, 2.2, a * ke * ks)
                    label(c, "A SUIT THAT DOESN'T EXIST", EX, EY + 0.62 * ES + 10, t, T_SUIT, 20, GOLD, a=a * ke)
                for i in range(3):
                    tc = T_COURT - 0.3 + 0.15 * i
                    if t >= tc:
                        cp, _ = figure(1180 + i * 170, 600, 260, BOW, -1)
                        lines_in(c, cp, t, tc, 0.4, SOFT, 1.8)
                label(c, "THE WHOLE COURT PRAISES IT", 1350, 790, t, T_COURT, 20, SOFT, a=a * ke)
                label(c, "NOBODY WANTS TO DISAGREE", 1350, 830, t, T_DISAGREE - 0.5, 20, WHITE, a=a * ke)
                if t >= T_CH0 - 0.2:                                        # the child who says it
                    cp, _ = figure(380, 640, 190, POINT, 1)
                    lines_in(c, cp, t, T_CHILD - 0.5, 0.5, GLOW, 2.2)
                    label(c, "A CHILD SAYS WHAT EVERYONE CAN SEE", 380, 860, t, T_CHILD - 0.2, 20, GLOW, a=a * ke)
                    ev(T_CHILD - 0.5, "form", t, 380)
        if t >= T_CO0 - 0.2:                                                # the machine as a courtier
            kc = ease(seg(t, T_CO0 - 0.2, T_CO0 + 0.3))
            with layer(c, kc):
                lines_in(c, chip(700, 520, 120), t, T_CO0, 0.6, WHITE, 2.0, seed_pt=(700, 520))
                label(c, "TRAINED ON OUR APPROVAL", 700, 740, t, T_CO0 + 0.4, 20, SOFT, a=a * kc)
                polys, j = figure(1300, 560, 360, STAND, -1)
                lines_in(c, polys, t, T_COURTIER - 0.6, 0.6, WHITE, 1.9)
                crown(c, j, 360, a * kc * ease(seg(t, T_COURTIER - 0.2, T_COURTIER + 0.2)))
                label(c, "A COURTIER", 700, 260, t, T_COURTIER - 0.3, 30, GOLD, a=a * kc, cps=24)
                label(c, "SAYS WHAT THE EMPEROR WANTS TO HEAR", CX, 860, t, T_HEAR - 0.8, 22, WHITE, a=a * kc)
                ev(T_COURTIER - 0.6, "thock", t, 700)


# ---------------------------------------------------------------- IMAGINE
T_WHATIF = ls("whatif")
T_RA0, T_LIKED, T_RIGHT, T_MONTH = ls("rated"), wd("rated", "liked"), wd("rated", "right"), wd("rated", "month")
T_HE0, T_DIDNT = ls("hear"), wd("hear", "didn't")
T_Q0, T_KEEP, T_CLICK = ls("question"), wd("question", "keep"), wd("question", "click")
T_TIP0 = ls("tip")


def imagine(c, t):
    a = win(t, T_IMAG0 - 0.05, T_TIP0 + 0.2, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "NOT A FORECAST · A WHAT-IF", CX, 180, t, T_WHATIF + 0.05, 24, GLOW, a=a)
        kr = part(t, T_RA0, T_HE0)
        if kr > 0:                                                          # rated on being right, a month later
            with layer(c, kr):
                label(c, "DID YOU LIKE IT?", CX, 400, t, T_LIKED - 0.4, 34, SOFT, a=a * kr, cps=28)
                if t >= T_RIGHT - 0.3:
                    k = ease(seg(t, T_RIGHT - 0.3, T_RIGHT + 0.2))
                    c.drawLine(620, 388, lerp(620, 1300, k), 388, mg.stroke(GOLD, 4.0, a * kr))
                label(c, "WERE YOU RIGHT, A MONTH LATER?", CX, 560, t, T_RIGHT - 0.2, 38, WHITE, a=a * kr, cps=28)
                if t >= T_MONTH:
                    stroke_polys(c, tick(1660, 548, 30), GLOW, 3.4, a * kr)
                    ev(T_MONTH, "confirm", t, 1660)
        kh = part(t, T_HE0, T_Q0)
        if kh > 0:                                                          # things you didn't want to hear
            with layer(c, kh):
                lines_in(c, bubble(CX, 480, 420, 200), t, T_HE0, 0.5, WHITE, 2.2)
                label(c, "NO.", CX, 500, t, T_DIDNT - 0.3, 60, GOLD, a=a * kh, cps=10)
                label(c, "THINGS YOU DIDN'T WANT TO HEAR", CX, 760, t, T_DIDNT, 22, WHITE, a=a * kh)
        if t >= T_Q0 - 0.2:                                                 # keep it, or thumbs down?
            kq = ease(seg(t, T_Q0 - 0.2, T_Q0 + 0.3))
            with layer(c, kq):
                lines_in(c, thumb(700, 520, 150), t, T_KEEP - 0.5, 0.5, GLOW, 2.4)
                label(c, "KEEP IT?", 700, 760, t, T_KEEP - 0.3, 24, GLOW, a=a * kq)
                lines_in(c, thumb(1220, 520, 150, down=True), t, T_CLICK - 0.5, 0.5, GOLD, 2.4)
                label(c, "THUMBS DOWN?", 1220, 760, t, T_CLICK - 0.3, 24, GOLD, a=a * kq)


# ---------------------------------------------------------------- SURFACE
T_ARGUE, T_PROVE, T_SURV = wd("tip", "argue"), wd("tip", "prove"), wd("tip", "survives")
T_THEN0, T_BUTTON, T_FLATTER = ls("then"), wd("then", "button"), wd("then", "flatter.")
T_S0, T_THERE = ls("still"), wd("still", "there.")
T_SRC = le("still") + 1.2
SOURCES = ["SOURCES",
           "OpenAI, Sycophancy in GPT-4o (29 Apr 2025): the 25 April update rolled back; ~500 million people use ChatGPT a week",
           "OpenAI, Expanding on what we missed with sycophancy (2 May 2025): thumbs-up/down added as a reward signal",
           "\"weakened the influence of our primary reward signal, which had been holding sycophancy in check\"",
           "Sharma et al. (Anthropic), Towards Understanding Sycophancy in Language Models (2023) · VentureBeat (29 Apr 2025)",
           "Hans Christian Andersen, The Emperor's New Clothes (1837) · the what-if is imagined, not a forecast"]


def surface(c, t):
    a = win(t, T_TIP0 - 0.05, T_SRC + 0.1, 0.3, 0.6)
    if a > 0:
        with layer(c, a):
            kt = part(t, T_TIP0, T_THEN0)
            if kt > 0:                                                      # three questions to ask
                with layer(c, kt):
                    for i, (tt, txt) in enumerate(((T_ARGUE, "\"ARGUE AGAINST ME.\""), (T_PROVE, "\"WHAT WOULD PROVE ME WRONG?\""),
                                                   (T_SURV, "A GOOD ANSWER SURVIVES THE QUESTION"))):
                        y = 380 + i * 140
                        if t >= tt - 0.5:
                            stroke_polys(c, tick(420, y - 10, 22), GLOW if i < 2 else GOLD, 3.0, a * kt)
                        label(c, txt, 480, y, t, tt - 0.4, 30 if i < 2 else 26, WHITE if i < 2 else GOLD, "left", a=a * kt, cps=30)
            if t >= T_THEN0 - 0.2:                                          # the button; still there
                kb = ease(seg(t, T_THEN0 - 0.2, T_THEN0 + 0.3)) * (1 - ease(seg(t, T_SRC - 0.4, T_SRC)))
                with layer(c, kb):
                    lines_in(c, thumb(CX, 470, 220), t, T_BUTTON - 0.5, 0.6, GOLD, 2.8)
                    label(c, "APRIL 2025", CX, 200, t, T_THEN0 + 0.2, 24, WHITE, a=a * kb)
                    label(c, "TAUGHT A MACHINE TO FLATTER", CX, 800, t, T_FLATTER - 0.8, 24, WHITE, a=a * kb)
                    if t >= T_S0 - 0.1:
                        label(c, "STILL THERE", CX, 860, t, T_THERE - 0.5, 30, GOLD, a=a * kb, cps=20)
                        ev(T_THERE - 0.5, "thud", t, CX)
    if t >= T_SRC:
        ks = 1 - ease(seg(t, T_SRC + 7.0, T_SRC + 7.8))
        for k, s_ in enumerate(SOURCES):
            label(c, s_, 200, 300 + k * 60, t, T_SRC + 0.2 + (0 if k == 0 else 0.6 + 0.45 * (k - 1)),
                  24 if k == 0 else 19, GLOW if k == 0 else SOFT, align="left", a=ks, cps=17 if k == 0 else 45)


def end_time():
    return T_SRC + 8.0


def frame(c, t):
    ground(c, t)
    mechanism(c, t)
    now(c, t)
    idea(c, t)
    imagine(c, t)
    surface(c, t)
