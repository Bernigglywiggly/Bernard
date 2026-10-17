"""EP12 · SIXTEEN HOURS, the scenes: line art keyed to the script's line ids and George's words (engine.tl.word),
which the engine turns into characters. One device runs through it: a ruler of time on a log scale (a second at the
left, weeks at the right) that the time horizon climbs, and that runs out just past sixteen hours.

  GROUND     16 H and two working days filling hour by hour; a half-filled ring (50%, on its own); the ruler: 2019 at
             two seconds, 2026 at sixteen hours, and the ruler ending there
  MECHANISM  228 tasks as bars from seconds to days; the success curve and its 50% point; the ladder, year by year;
             the tasks along the ruler, only five past sixteen hours
  NOW        half is not every time: the 80% mark at about three hours; a checked terminal against a speech and a talk
  IDEA       steps against folds; a fold count from the Earth past the Moon; the doubling times
  IMAGINE    the ruler extended in dashes to 256 hours; six working weeks filling; a business and a book; two questions
  SURFACE    two seconds to an hour (six years) | an hour to sixteen (about one); the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         points, stroke_polys, bignum, chip, page, burst, globe, keys, dotted_num)

TRAILS = []
GLINTS = []
RNG = np.random.default_rng(12)
H = 3600.0


# ---------------------------------------------------------------- the ruler (log time)
RX0, RX1, RY = 160, 1760, 560
LMAX = 6.0                                                  # 10^6 s at the right end (about 11.6 days)


def rx(sec):
    return RX0 + (RX1 - RX0) * math.log10(max(sec, 1.0)) / LMAX


END = rx(20 * H)                                            # where the ruler runs out
TICKS = [(1, "1 S"), (10, "10 S"), (60, "1 MIN"), (600, "10 MIN"), (H, "1 H"), (8 * H, "8 H"), (16 * H, "16 H")]
LADDER = [("2019", 2.0, "2 SEC", ("ladder", "two", 0)), ("2022", 30.0, "30 SEC", ("ladder", "thirty", 0)),
          ("2023", 240.0, "4 MIN", ("ladder", "four", 0)), ("2025", H, "1 HOUR", ("ladder", "hour", 0)),
          ("2026", 16 * H, "16 HOURS", ("ladder", "sixteen", 0))]


def ruler(c, t, t0, a, end=END, ticks=TICKS, col=WHITE):
    """The ruler forming from the left: the line, its ticks and their labels."""
    k = ease(seg(t, t0, t0 + 0.9))
    if k <= 0:
        return
    x1 = lerp(RX0, end, k)
    c.drawLine(RX0, RY, x1, RY, mg.stroke(col, 2.2, a))
    for s, name in ticks:
        x = rx(s)
        if x <= x1:
            c.drawLine(x, RY - 14, x, RY + 14, mg.stroke(col, 1.6, a))
            label(c, name, x, RY + 46, t, -1, 18, SOFT, a=a)
    ev(t0, "form", t, RX0)


def marker(c, x, t, t0, txt, sub, col=GLOW, a=1.0, up=True):
    k = ease(seg(t, t0, t0 + 0.4))
    if k <= 0:
        return
    y0, y1 = (RY - 20, RY - 20 - 90 * k) if up else (RY + 20, RY + 20 + 90 * k)
    c.drawLine(x, y0, x, y1, mg.stroke(col, 2.4, a * k))
    c.drawCircle(x, RY, 8, mg.fill(col, a * k))
    label(c, txt, x, y1 - 14 if up else y1 + 30, t, t0, 22, col, a=a)
    if sub:
        label(c, sub, x, y1 - 44 if up else y1 + 58, t, t0 + 0.1, 18, SOFT, a=a)
    ev(t0, "tick", t, x)


def dashes(c, x0, x1, y, a, col=GLOW, n=None):
    n = n or max(1, int((x1 - x0) / 26))
    for k in range(n):
        u0, u1 = k / n, (k + 0.5) / n
        c.drawLine(lerp(x0, x1, u0), y, lerp(x0, x1, u1), y, mg.stroke(col, 2.0, a))


def ring(c, cx, cy, r, frac, a):
    c.drawCircle(cx, cy, r, mg.stroke(SOFT, 2.0, 0.6 * a))
    path = skia.Path()
    path.addArc(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), -90, 360 * frac)
    c.drawPath(path, mg.stroke(GLOW, 10.0, a))


def staircase(x0, y0, w, h, n=6):
    pts = [(x0, y0)]
    for k in range(n):
        pts += [(x0 + w * (k + 1) / n, y0 - h * k / n), (x0 + w * (k + 1) / n, y0 - h * (k + 1) / n)]
    return P(pts)


def expo(x0, y0, w, h, n=60):
    u = np.linspace(0, 1, n)
    return np.column_stack([x0 + w * u, y0 - h * (2 ** (6 * u) - 1) / 63])


def shop(cx, bot, s):
    out = [rect(cx - s, bot - 0.8 * s, 2 * s, 0.8 * s), rect(cx - 0.25 * s, bot - 0.5 * s, 0.5 * s, 0.5 * s),
           P([(cx - 1.1 * s, bot - 0.8 * s), (cx - s, bot - 1.05 * s), (cx + s, bot - 1.05 * s), (cx + 1.1 * s, bot - 0.8 * s)])]
    for k in range(5):
        x = cx - s + k * 0.4 * s
        out.append(P([(x, bot - 1.05 * s), (x + 0.2 * s, bot - 0.8 * s), (x + 0.4 * s, bot - 1.05 * s)]))
    return out


def bubble(cx, cy, w, h):
    return [P([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 4, cy + h / 2),
               (cx - w / 3, cy + h / 2 + 0.3 * h), (cx - w / 3 - 0.02 * w, cy + h / 2), (cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2)])]


def tick_mark(cx, cy, s):
    return [P([(cx - s, cy), (cx - 0.3 * s, cy + 0.7 * s), (cx + s, cy - 0.8 * s)])]


def cross(cx, cy, s):
    return [P([(cx - s, cy - s), (cx + s, cy + s)]), P([(cx + s, cy - s), (cx - s, cy + s)])]


def part(t, a, b, fin=0.3, fout=0.4):
    return win(t, a - 0.1, b + 0.2, fin, fout)


# 228 task lengths, from seconds to two working days (log-uniform-ish), five of them 16 h or more
_L = np.sort(10 ** RNG.uniform(0.3, math.log10(15 * H), 223))
TASKS = np.concatenate([_L, [16.5 * H, 18 * H, 21 * H, 25 * H, 30 * H]])


# ---------------------------------------------------------------- GROUND
T_TASK0, T_16, T_TWO, T_DAYS = ls("task"), wd("task", "sixteen"), wd("task", "two"), wd("task", "days.")
T_SPR0, T_MEASURED, T_HALF, T_OWN = ls("spring"), wd("spring", "measured"), wd("spring", "half"), wd("spring", "own.")
T_BEF0, T_SEVEN, T_TWOSEC = ls("before"), wd("before", "seven"), wd("before", "seconds.")
T_RUL0, T_RULER = ls("ruler"), wd("ruler", "ruler.")
T_WHY0 = ls("why")
T_HOW0 = ls("how")


def ground(c, t):
    a = win(t, 1.0, T_HOW0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kt = part(t, T_TASK0, T_SPR0)
        if kt > 0:                                                          # 16 hours: two working days, hour by hour
            with layer(c, kt):
                bignum(c, t, "16 H", 130, CX, 280, T_16 - 0.2)
                label(c, "HUMAN EXPERT TIME", CX, 370, t, T_16 + 0.3, 22, SOFT, a=a * kt)
                for d in range(2):
                    x0 = 330 + d * 660
                    lines_in(c, [rect(x0, 520, 600, 90)], t, T_TWO - 0.3 + 0.2 * d, 0.4, WHITE, 1.8)
                    for h in range(8):
                        th = T_TWO + 0.12 * (8 * d + h)
                        if t >= th:
                            c.drawRect(skia.Rect.MakeXYWH(x0 + 6 + h * 74.2, 526, 68, 78), mg.chrome_paint(526, 604, 0.9 * ease(seg(t, th, th + 0.2))))
                            ev(th, "tick", t, x0 + h * 74)
                    label(c, f"DAY {d + 1} · 8 HOURS", x0 + 300, 660, t, T_TWO + 0.1 + 0.2 * d, 20, GLOW, a=a * kt)
        ks = part(t, T_SPR0, T_BEF0)
        if ks > 0:                                                          # about half the time, on its own
            with layer(c, ks):
                lines_in(c, chip(620, 520, 130), t, T_SPR0 + 0.1, 0.5, WHITE, 1.9, seed_pt=(620, 520))
                label(c, "MARCH 2026 · METR", 620, 760, t, T_MEASURED - 0.2, 20, SOFT, a=a * ks)
                ring(c, 1300, 520, 150, 0.5 * ease(seg(t, T_HALF - 0.3, T_HALF + 0.4)), a * ks)
                bignum(c, t, "50%", 90, 1300, 555, T_HALF - 0.2)
                label(c, "OF 16-HOUR TASKS", 1300, 760, t, T_HALF + 0.2, 20, GLOW, a=a * ks)
                label(c, "ON ITS OWN", CX, 220, t, T_OWN - 0.2, 26, WHITE, a=a * ks)
                ev(T_HALF - 0.3, "swell", t, 1300)
        if t >= T_BEF0 - 0.2:                                               # the ruler: 2 s in 2019, 16 h now; and its end
            kb = ease(seg(t, T_BEF0 - 0.2, T_BEF0 + 0.3)) * (1 - ease(seg(t, T_HOW0 - 0.3, T_HOW0 + 0.1)))
            with layer(c, kb):
                ruler(c, t, T_BEF0, a * kb)
                marker(c, rx(16 * H), t, T_BEF0 + 0.6, "2026 · 16 H", "", GLOW, a * kb)
                marker(c, rx(2.0), t, T_TWOSEC - 0.4, "2019 · 2 SEC", "", GOLD, a * kb)
                if t >= T_SEVEN:
                    k = ease(seg(t, T_SEVEN, T_TWOSEC))
                    c.drawLine(rx(2.0), RY + 90, lerp(rx(2.0), rx(16 * H), k), RY + 90, mg.stroke(SOFT, 1.6, a * kb))
                    label(c, "SEVEN YEARS", (rx(2.0) + rx(16 * H)) / 2, RY + 130, t, T_SEVEN + 0.2, 20, SOFT, a=a * kb)
                if t >= T_RUL0 - 0.2:
                    kr = ease(seg(t, T_RUL0 - 0.2, T_RULER))
                    dashes(c, END, lerp(END, RX1 + 60, kr), RY, 0.5 * a * kb, SOFT)
                    c.drawLine(END, RY - 40, END, RY + 40, mg.stroke(GOLD, 3.0, a * kb * kr))
                    label(c, "END OF THE RULER", END, RY - 210, t, T_RULER - 0.3, 22, GOLD, a=a * kb)
                    ev(T_RULER - 0.3, "thud", t, END)
                label(c, "HOW DO YOU MEASURE SOMETHING THAT OUTGROWS THE TEST?", CX, 820, t, T_WHY0 + 0.1, 26, WHITE, a=a * kb)


# ---------------------------------------------------------------- MECHANISM
T_METR, T_228, T_CODING, T_SECONDS, T_DAYS2 = wd("how", "meter"), wd("how", "two"), wd("how", "coding"), wd("how", "seconds"), wd("how", "days.")
T_SAME0, T_AGENTS, T_LENGTH, T_HALFT = ls("same"), wd("same", "agents"), wd("same", "length"), wd("same", "half")
T_NAME0 = ls("name")
T_LAD0 = ls("ladder")
T_FIVE0, T_FIVE, T_RELIABLE = ls("five"), wd("five", "five"), wd("five", "reliable.")
T_HALF20 = ls("half")


def ladder_times():
    out = []
    for yr, s, txt, (ln, w, k) in LADDER:
        try:
            out.append(wd(ln, w, k) - 0.2)
        except KeyError:
            out.append(None)
    return out


def mechanism(c, t):
    a = win(t, T_HOW0 - 0.05, T_HALF20 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kh = part(t, T_HOW0, T_SAME0)
        if kh > 0:                                                          # 228 tasks, seconds to two working days
            with layer(c, kh):
                bignum(c, t, "228 TASKS", 100, CX, 230, T_228 - 0.2)
                label(c, "METR · TIMED ON SKILLED PEOPLE", CX, 320, t, T_METR - 0.1, 22, SOFT, a=a * kh)
                n = int(len(TASKS) * ease(seg(t, T_228, T_SECONDS)))
                for i in range(n):                                          # one bar a task, shortest to longest
                    x = 200 + i * 1520 / len(TASKS)
                    hgt = 16 + 330 * math.log10(TASKS[i]) / math.log10(30 * H)
                    c.drawRect(skia.Rect.MakeXYWH(x, 770 - hgt, 4.2, hgt), mg.fill(GOLD if TASKS[i] >= 16 * H else GLOW, 0.85 * a * kh))
                label(c, "SECONDS", 200, 800, t, T_SECONDS - 0.3, 18, SOFT, "left", a=a * kh)
                label(c, "TWO WORKING DAYS", 1720, 800, t, T_DAYS2 - 0.3, 18, GOLD, "right", a=a * kh)
                ev(T_228, "grains", t, CX)
                label(c, "CODING · RESEARCH · FIXING BROKEN SYSTEMS", CX, 360, t, T_CODING - 0.2, 20, WHITE, a=a * kh)
        kc = part(t, T_SAME0, T_LAD0)
        if kc > 0:                                                          # the success curve and its 50% point
            with layer(c, kc):
                x0, y0, w, h = 300, 760, 1320, 440
                c.drawLine(x0, y0 - h, x0, y0, mg.stroke(SOFT, 1.6, a * kc))
                c.drawLine(x0, y0, x0 + w, y0, mg.stroke(SOFT, 1.6, a * kc))
                xs = np.linspace(0, 1, 120)
                ys = 1 / (1 + np.exp((xs - 0.62) * 9))
                k = seg(t, T_AGENTS - 0.3, T_LENGTH)
                nn = max(2, int(120 * k))
                stroke_polys(c, [np.column_stack([x0 + w * xs[:nn], y0 - h * ys[:nn]])], GLOW, 2.6, 1.0)
                label(c, "SUCCESS", x0 - 20, y0 - h - 20, t, T_AGENTS - 0.3, 18, SOFT, "left", a=a * kc)
                label(c, "TASK LENGTH (FOR A PERSON) →", x0 + w, y0 + 40, t, T_AGENTS, 18, SOFT, "right", a=a * kc)
                if t >= T_HALFT - 0.4:
                    kx = ease(seg(t, T_HALFT - 0.4, T_HALFT + 0.2))
                    xm = x0 + w * 0.62
                    c.drawLine(x0, y0 - h / 2, lerp(x0, xm, kx), y0 - h / 2, mg.stroke(WHITE, 1.4, a * kc))
                    c.drawLine(xm, y0 - h / 2, xm, lerp(y0 - h / 2, y0, kx), mg.stroke(WHITE, 1.4, a * kc))
                    c.drawCircle(xm, y0 - h / 2, 10, mg.fill(GOLD, a * kc * kx))
                    label(c, "50%", x0 - 20, y0 - h / 2 + 8, t, T_HALFT - 0.2, 20, GOLD, "right", a=a * kc)
                    ev(T_HALFT - 0.2, "confirm", t, xm)
                label(c, "THE TIME HORIZON", x0 + w * 0.62, y0 + 80, t, T_NAME0, 30, GOLD, a=a * kc, cps=30)
        kl = part(t, T_LAD0, T_HALF20)
        if kl > 0:                                                          # the ladder, then the five long tasks
            with layer(c, kl):
                ruler(c, t, T_LAD0 - 0.1, a * kl)
                for (yr, s, txt, _), tk in zip(LADDER, ladder_times()):
                    marker(c, rx(s), t, tk if tk is not None else T_LAD0, txt, yr, GLOW if yr != "2026" else GOLD, a * kl)
                if t >= T_FIVE0 - 0.3:                                      # the tasks along the ruler; five past 16 h
                    kf = ease(seg(t, T_FIVE0 - 0.3, T_FIVE0 + 0.6))
                    for i, s in enumerate(TASKS):
                        x = rx(s)
                        y = RY + 80 + (i % 9) * 12
                        long_ = s >= 16 * H
                        c.drawCircle(x, y, 5 if long_ else 3, mg.fill(GOLD if long_ else SOFT, (1.0 if long_ else 0.5) * a * kl * kf))
                    bignum(c, t, "5 OF 228", 70, rx(24 * H) - 120, 230, T_FIVE - 0.2)
                    label(c, "TAKE A PERSON 16 HOURS OR MORE", rx(24 * H) - 120, 300, t, T_FIVE + 0.3, 20, GOLD, a=a * kl)
                    dashes(c, END, RX1 + 60, RY, 0.6 * a * kl, SOFT)
                    label(c, "ABOVE 16 H: NOT RELIABLE YET", CX, 830, t, T_RELIABLE - 0.6, 22, WHITE, a=a * kl)
                    ev(T_FIVE - 0.2, "pop", t, rx(20 * H))


# ---------------------------------------------------------------- NOW
T_EVERY = wd("half", "every")
T_80A, T_80, T_THREE = ls("eighty"), wd("eighty", "eighty"), wd("eighty", "three")
T_KIND0, T_SOFTWARE, T_CHECK, T_SPEECH, T_CONVO = ls("kind"), wd("kind", "software,"), wd("kind", "check"), wd("kind", "speech."), wd("kind", "conversation.")
T_BRAINS0 = ls("brains")


def now(c, t):
    a = win(t, T_HALF20 - 0.05, T_BRAINS0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        ke = part(t, T_HALF20, T_KIND0)
        if ke > 0:                                                          # 50% at 16 h; 80% at about 3 h
            with layer(c, ke):
                label(c, "HALF THE TIME ≠ EVERY TIME", CX, 220, t, T_EVERY - 0.3, 30, WHITE, a=a * ke, cps=30)
                ruler(c, t, T_HALF20 - 0.2, a * ke)
                marker(c, rx(16 * H), t, T_HALF20 + 0.2, "50% · ≥ 16 H", "", GLOW, a * ke)
                if t >= T_80 - 0.3:
                    x = keys(t, [(T_80 - 0.2, rx(16 * H)), (T_THREE + 0.2, rx(3.1 * H))])
                    marker(c, x, t, T_80 - 0.2, "80% · ~3 H", "THE SAME MODEL", GOLD, a * ke, up=False)
                    ev(T_80 - 0.2, "whoosh", t, x)
        if t >= T_KIND0 - 0.2:                                              # checkable software, not a speech or a talk
            kk = ease(seg(t, T_KIND0 - 0.2, T_KIND0 + 0.3))
            with layer(c, kk):
                lines_in(c, [rect(260, 330, 560, 330)], t, T_KIND0, 0.5, WHITE, 1.8)
                label(c, "$ run tests", 300, 400, t, T_SOFTWARE - 0.2, 24, WHITE, "left", a=a * kk, cps=24)
                label(c, "228 passed", 300, 450, t, T_CHECK - 0.4, 24, GLOW, "left", a=a * kk, cps=24)
                lines_in(c, tick_mark(700, 560, 50), t, T_CHECK - 0.2, 0.4, GLOW, 3.0)
                label(c, "A CLEAR GOAL · A WAY TO CHECK", 540, 720, t, T_CHECK - 0.2, 20, GLOW, a=a * kk)
                lines_in(c, bubble(1200, 450, 300, 180), t, T_SPEECH - 0.7, 0.5, SOFT, 1.8)
                label(c, "A WEDDING SPEECH", 1200, 460, t, T_SPEECH - 0.5, 20, SOFT, a=a * kk)
                lines_in(c, bubble(1500, 620, 300, 160), t, T_CONVO - 0.8, 0.5, SOFT, 1.8)
                label(c, "A HARD CONVERSATION", 1500, 630, t, T_CONVO - 0.6, 20, SOFT, a=a * kk)
                label(c, "NOT IN THE TEST", 1350, 820, t, T_CONVO - 0.3, 22, WHITE, a=a * kk)
                ev(T_CHECK - 0.2, "confirm", t, 700)


# ---------------------------------------------------------------- IDEA
T_WRONG = wd("brains", "wrong.")
T_FOLDS0, T_STEPS, T_FOLDSW = ls("folds"), wd("folds", "steps."), wd("folds", "folds.")
T_PAPER0, T_FORTY, T_MOON = ls("paper"), wd("paper", "fortytwo"), wd("paper", "moon.")
T_DBL0, T_SEVENM, T_FOUR = ls("doubling"), wd("doubling", "seven"), wd("doubling", "four.")
T_IMAG0 = ls("imagine")
MOON_KM = 384400.0


def idea(c, t):
    a = win(t, T_BRAINS0 - 0.05, T_IMAG0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "HERE'S WHAT OUR BRAINS GET WRONG", CX, 200, t, T_BRAINS0 + 0.1, 26, WHITE, a=a * (1 - ease(seg(t, T_PAPER0 - 0.3, T_PAPER0))))
        kf = part(t, T_FOLDS0, T_PAPER0)
        if kf > 0:                                                          # steps against folds
            with layer(c, kf):
                lines_in(c, [staircase(300, 760, 560, 440)], t, T_STEPS - 0.6, 0.6, WHITE, 2.2)
                label(c, "STEPS", 580, 820, t, T_STEPS - 0.3, 24, WHITE, a=a * kf)
                lines_in(c, [expo(1060, 760, 560, 440)], t, T_FOLDSW - 0.6, 0.6, GLOW, 2.6)
                label(c, "FOLDS", 1340, 820, t, T_FOLDSW - 0.3, 24, GLOW, a=a * kf)
                ev(T_FOLDSW - 0.6, "riser", t, 1340)
        kp = part(t, T_PAPER0, T_DBL0)
        if kp > 0:                                                          # 42 folds: from the Earth past the Moon
            with layer(c, kp):
                lines_in(c, globe(260, 540, 110, t * 0.2), t, T_PAPER0, 0.5, WHITE, 1.6)
                mx = 1600
                lines_in(c, [ellipse(mx, 540, 46, 46, 0, 360, 48)], t, T_PAPER0 + 0.3, 0.5, WHITE, 1.8)
                label(c, "THE MOON · 384,400 KM", mx, 640, t, T_PAPER0 + 0.5, 18, SOFT, a=a * kp)
                n = int(42 * ease(seg(t, T_PAPER0 + 0.4, T_FORTY + 0.4)))
                km = 0.1e-6 * 2 ** n                                         # 0.1 mm doubled n times, in km
                x1 = 370 + (mx - 370) * min(1.15, km / MOON_KM)
                if km > 5e-3:
                    c.drawLine(370, 540, x1, 540, mg.stroke(GLOW, 3.0, a * kp))
                label(c, f"FOLD {n} · {km:,.0f} KM" if km >= 1 else f"FOLD {n} · {km * 1e6:,.1f} MM" if km < 1e-3 else f"FOLD {n} · {km * 1e3:,.0f} M",
                      CX, 420, t, T_PAPER0 + 0.4, 26, WHITE, a=a * kp)
                if n >= 42:
                    burst(c, mx, 540, t, T_FORTY + 0.4, 90)
                    label(c, "PAST THE MOON", CX, 720, t, T_MOON - 0.4, 26, GLOW, a=a * kp)
                    ev(T_FORTY + 0.4, "thud", t, mx)
                ev(T_PAPER0 + 0.4, "paper", t, 370)
        if t >= T_DBL0 - 0.2:                                               # the doubling times
            kd = ease(seg(t, T_DBL0 - 0.2, T_DBL0 + 0.3))
            with layer(c, kd):
                ruler(c, t, T_DBL0 - 0.2, a * kd)
                for i, (yr, s, txt, _) in enumerate(LADDER):
                    marker(c, rx(s), t, T_DBL0 + 0.2 + 0.25 * i, txt, yr, GOLD if yr == "2026" else GLOW, a * kd)
                bignum(c, t, "× 2", 90, 560, 230, T_SEVENM - 0.4)
                label(c, "EVERY ~7 MONTHS SINCE 2019", 560, 310, t, T_SEVENM - 0.2, 20, WHITE, a=a * kd)
                bignum(c, t, "× 2", 90, 1360, 230, T_FOUR - 0.6)
                label(c, "EVERY ~4 MONTHS SINCE 2023", 1360, 310, t, T_FOUR - 0.4, 20, GLOW, a=a * kd)
                label(c, "METR · TIME HORIZON 1.1", CX, 830, t, T_SEVENM, 18, SOFT, a=a * kd)


# ---------------------------------------------------------------- IMAGINE
T_KEEP = wd("imagine", "coming.")
T_WHATIF = ls("whatif")
T_SIX0, T_DOUBLINGS, T_256, T_WEEKS = ls("six"), wd("six", "doublings,"), wd("six", "two", 0), wd("six", "weeks.")
T_PROJ0, T_PROJECT, T_BUSINESS, T_BOOK = ls("project"), wd("project", "project."), wd("project", "business."), wd("project", "book.")
T_Q0, T_HAND, T_KEEPQ = ls("question"), wd("question", "hand"), wd("question", "keep?")
T_THEN = ls("then")


def imagine(c, t):
    a = win(t, T_IMAG0 - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        ki = part(t, T_IMAG0, T_PROJ0)
        if ki > 0:                                                          # the ruler extended in dashes: 32, 64, 128, 256 h
            with layer(c, ki):
                ruler(c, t, T_IMAG0, a * ki)
                marker(c, rx(16 * H), t, T_IMAG0 + 0.3, "16 H", "MARCH 2026", GOLD, a * ki)
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 200, t, T_WHATIF + 0.05, 24, GLOW, a=a * ki)
                for i, hh in enumerate((32, 64, 128, 256)):
                    tk = T_DOUBLINGS - 0.3 + 0.35 * i
                    if t >= tk:
                        x = rx(hh * H)
                        dashes(c, rx(hh / 2 * H), x, RY, 0.8 * a * ki)
                        c.drawCircle(x, RY, 7, mg.stroke(GLOW, 2.0, a * ki))
                        label(c, f"{hh} H", x, RY - 40, t, tk, 20, GLOW, a=a * ki)
                        ev(tk, "tick", t, x)
                if t >= T_256 - 0.4:
                    dotted_num(c, "256 H", 110, CX, 330, t, T_256 - 0.4, a * ki)
                if t >= T_WEEKS - 1.0:                                      # six working weeks, day by day
                    for d in range(30):
                        td = T_WEEKS - 1.0 + 0.04 * d
                        if t >= td:
                            x = 420 + (d % 5) * 70 + (d // 5) * 200 - 190
                            x = 300 + (d // 5) * 230 + (d % 5) * 40
                            c.drawRect(skia.Rect.MakeXYWH(x, 700, 32, 60), mg.fill(GLOW, 0.8 * a * ki))
                    label(c, "SIX WORKING WEEKS", CX, 820, t, T_WEEKS - 0.3, 24, WHITE, a=a * ki)
        if t >= T_PROJ0 - 0.2:                                              # a project: a business, a book; two questions
            kp = ease(seg(t, T_PROJ0 - 0.2, T_PROJ0 + 0.3))
            with layer(c, kp):
                label(c, "NOT A CHORE. A PROJECT.", CX, 220, t, T_PROJECT - 0.5, 30, WHITE, a=a * kp, cps=28)
                lines_in(c, shop(620, 640, 170), t, T_BUSINESS - 0.8, 0.6, WHITE, 1.9)
                label(c, "THE FIRST VERSION OF THE BUSINESS", 620, 720, t, T_BUSINESS - 0.6, 20, GLOW, a=a * kp)
                lines_in(c, page(1220, 380, 200, 260), t, T_BOOK - 0.8, 0.6, WHITE, 1.9)
                label(c, "THE FIRST DRAFT OF THE BOOK", 1320, 720, t, T_BOOK - 0.6, 20, GLOW, a=a * kp)
                if t >= T_Q0 - 0.2:
                    label(c, "WHAT WOULD YOU HAND OVER?", 620, 820, t, T_HAND - 0.2, 24, WHITE, a=a * kp)
                    label(c, "WHAT WOULD YOU KEEP?", 1320, 820, t, T_KEEPQ - 0.4, 24, GLOW, a=a * kp)
                ev(T_BUSINESS - 0.8, "form", t, 620)
                ev(T_BOOK - 0.8, "paper", t, 1320)


# ---------------------------------------------------------------- SURFACE
T_SIXY, T_HOUR = wd("then", "six"), wd("then", "hour.")
T_NOW0, T_ONE, T_SIXTEEN = ls("now2"), wd("now2", "one"), wd("now2", "sixteen.")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "METR, Measuring AI Ability to Complete Long Tasks (Mar 2025): ~2 s (2019), ~30 s (2022), ~4 min (2023), ~1 h (early 2025)",
           "METR, Time Horizon 1.1 (Jan 2026): 228 tasks; doubling ~7 months since 2019, ~130.8 days since 2023",
           "METR on an early Claude Mythos Preview (evaluated Mar 2026): 50% horizon ≥ 16 h (95% CI 8.5-55 h); 80% ~3 h 6 min",
           "Only 5 of 228 tasks take people 16 h+; METR: measurements above 16 h are unreliable with the current suite",
           "Paper: 0.1 mm × 2^42 ≈ 439,805 km; Moon 384,400 km · 256 h = 16 h × 2^4 (a what-if, not a forecast)"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            ruler(c, t, T_THEN - 0.1, a)
            marker(c, rx(2.0), t, T_THEN + 0.1, "2 SEC", "2019", GLOW, a)
            marker(c, rx(H), t, T_HOUR - 0.3, "1 HOUR", "EARLY 2025", GLOW, a)
            k1 = ease(seg(t, T_SIXY - 0.2, T_HOUR))
            if k1 > 0:
                arc = [(lerp(rx(2.0), rx(H), u), RY + 90 + 60 * math.sin(math.pi * u)) for u in np.linspace(0, k1, 40)]
                stroke_polys(c, [P(arc)], WHITE, 2.0, 1.0)
                label(c, "SIX YEARS", (rx(2.0) + rx(H)) / 2, RY + 200, t, T_SIXY, 24, WHITE, a=a)
            if t >= T_NOW0 - 0.05:
                marker(c, rx(16 * H), t, T_SIXTEEN - 0.4, "16 HOURS", "MARCH 2026", GOLD, a)
                k2 = ease(seg(t, T_ONE - 0.3, T_SIXTEEN))
                if k2 > 0:
                    arc = [(lerp(rx(H), rx(16 * H), u), RY + 90 + 30 * math.sin(math.pi * u)) for u in np.linspace(0, k2, 30)]
                    stroke_polys(c, [P(arc)], GOLD, 2.6, 1.0)
                    label(c, "ABOUT ONE", (rx(H) + rx(16 * H)) / 2, RY + 170, t, T_ONE, 24, GOLD, a=a)
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
    mirror(c, t)
