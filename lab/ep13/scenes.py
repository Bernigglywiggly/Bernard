"""EP13 · THE NINETY-MINUTE WAR, the scenes: line art keyed to the script's line ids and George's words (engine.tl.word),
which the engine turns into characters. One device runs through it: a price ruler on a log scale, a hundred dollars
per million tokens at the left, a cent at the right, and every cut moves a marker towards the cheap end.

  GROUND     22 SEP 2026: lab A's tag rolls $5 to $4 (-20%); a 90-minute arc to lab B's two chips at half the price;
             both tags drop: one afternoon
  MECHANISM  two dials, HOW GOOD (blurred: weeks to tell) and HOW MUCH (read in seconds); the price tag as a signal,
             hours not weeks; the ruler: $60 (2021) sliding to 6 cents (2024), 1,000x
  YOU        a million tokens, 750,000 words, eight novels on a shelf; a scan line reads them for under 10p; a reading
             list, a takeaway's reviews, a year of emails
  IDEA       the Red Queen and Alice running on a moving ground; Van Valen's two lines climbing with the gap fixed; two
             labs running in place while the price marker ticks cheaper with every step
  IMAGINE    the ruler running on past a cent in dashes; a tutor and a text message; coder, translator, second opinion;
             the question; an hourglass, an eye, someone at a door
  SURFACE    the job you've put off becomes pennies; the two cuts mirrored; both still running; the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         stroke_polys, bignum, chip, page, burst, keys, dotted_num, roll, figure, pose_mix)

TRAILS = []
GLINTS = []


def part(t, a, b, fin=0.3, fout=0.4):
    return win(t, a - 0.1, b + 0.2, fin, fout)


# ---------------------------------------------------------------- the price ruler (log $ per million tokens)
RX0, RX1, RY = 180, 1740, 600
TOP, LOW = 100.0, 0.01                                     # $100 at the left, 1 cent at the right


def px(usd):
    return RX0 + (RX1 - RX0) * (math.log10(TOP) - math.log10(max(usd, 1e-4))) / (math.log10(TOP) - math.log10(LOW))


TICKS = [(100, "$100"), (10, "$10"), (1, "$1"), (0.1, "10¢"), (0.01, "1¢")]


def ruler(c, t, t0, a, y=RY):
    k = ease(seg(t, t0, t0 + 0.9))
    if k <= 0:
        return
    x1 = lerp(RX0, RX1, k)
    c.drawLine(RX0, y, x1, y, mg.stroke(WHITE, 2.2, a))
    for usd, name in TICKS:
        x = px(usd)
        if x <= x1:
            c.drawLine(x, y - 14, x, y + 14, mg.stroke(WHITE, 1.6, a))
            label(c, name, x, y + 46, t, -1, 18, SOFT, a=a)
    label(c, "PRICE PER MILLION TOKENS · CHEAPER →", RX1, y - 40, t, t0 + 0.5, 18, SOFT, "right", a=a)
    ev(t0, "form", t, RX0)


def marker(c, x, t, t0, txt, sub, col=GLOW, a=1.0, up=True, y=RY):
    k = ease(seg(t, t0, t0 + 0.4))
    if k <= 0:
        return
    y0, y1 = (y - 20, y - 20 - 90 * k) if up else (y + 20, y + 20 + 90 * k)
    c.drawLine(x, y0, x, y1, mg.stroke(col, 2.4, a * k))
    c.drawCircle(x, y, 8, mg.fill(col, a * k))
    label(c, txt, x, y1 - 14 if up else y1 + 30, t, t0, 22, col, a=a)
    if sub:
        label(c, sub, x, y1 - 44 if up else y1 + 58, t, t0 + 0.1, 18, SOFT, a=a)
    ev(t0, "tick", t, x)


def dashes(c, x0, x1, y, a, col=GLOW, n=None):
    n = n or max(1, int((x1 - x0) / 26))
    for k in range(n):
        u0, u1 = k / n, (k + 0.5) / n
        c.drawLine(lerp(x0, x1, u0), y, lerp(x0, x1, u1), y, mg.stroke(col, 2.0, a))


# ---------------------------------------------------------------- shapes
def tag(cx, cy, w, h):
    """A price tag pointing left, with its hole and string."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    out = [P([(x0 + 0.22 * h, y0), (x1, y0), (x1, y1), (x0 + 0.22 * h, y1), (x0 - 0.18 * h, cy), (x0 + 0.22 * h, y0)]),
           ellipse(x0 + 0.12 * h, cy, 0.07 * h, 0.07 * h, 0, 360, 20)]
    out.append(P([(x0 + 0.12 * h, cy), (x0 - 0.35 * h, cy - 0.45 * h), (x0 - 0.5 * h, cy - 0.5 * h)]))
    return out


def arrow_down(cx, y0, y1, s=18):
    return [P([(cx, y0), (cx, y1)]), P([(cx - s, y1 - s), (cx, y1), (cx + s, y1 - s)])]


def dial(cx, cy, r):
    """A gauge: a half ring with ticks."""
    out = [np.column_stack([cx + r * np.cos(a), cy - r * np.sin(a)]) for a in [np.radians(np.linspace(0, 180, 60))]]
    for k in range(11):
        a = math.radians(180 - 18 * k)
        out.append(P([(cx + 0.86 * r * math.cos(a), cy - 0.86 * r * math.sin(a)), (cx + r * math.cos(a), cy - r * math.sin(a))]))
    out.append(P([(cx - r, cy), (cx + r, cy)]))
    return out


def needle(c, cx, cy, r, frac, col, a, w=3.0):
    ang = math.radians(180 - 180 * frac)
    c.drawLine(cx, cy, cx + 0.8 * r * math.cos(ang), cy - 0.8 * r * math.sin(ang), mg.stroke(col, w, a))
    c.drawCircle(cx, cy, 7, mg.fill(col, a))


def rings(c, cx, cy, t, t0, a, col=GLOW, n=3, period=1.1, rmax=220):
    """A signal: rings spreading from a point."""
    if t < t0:
        return
    for k in range(n):
        u = ((t - t0) / period + k / n) % 1.0
        c.drawCircle(cx, cy, 30 + rmax * u, mg.stroke(col, 2.0, a * (1 - u) * 0.9))


def book(x, y, w, h):
    """A book spine standing on a shelf: (x, y) = its bottom-left corner."""
    return [rect(x, y - h, w, h), P([(x + 0.2 * w, y - 0.82 * h), (x + 0.8 * w, y - 0.82 * h)]),
            P([(x + 0.2 * w, y - 0.18 * h), (x + 0.8 * w, y - 0.18 * h)])]


def star(cx, cy, r):
    pts = []
    for k in range(11):
        rr = r if k % 2 == 0 else 0.45 * r
        a = math.radians(-90 + 36 * k)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return P(pts)


def envelope(cx, cy, w, h):
    x0, y0 = cx - w / 2, cy - h / 2
    return [rect(x0, y0, w, h), P([(x0, y0), (cx, cy + 0.1 * h), (x0 + w, y0)])]


def bubble(cx, cy, w, h):
    return [P([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 4, cy + h / 2),
               (cx - w / 3, cy + h / 2 + 0.3 * h), (cx - w / 3 - 0.02 * w, cy + h / 2), (cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2)])]


def hourglass(cx, cy, s):
    return [P([(cx - s, cy - s), (cx + s, cy - s), (cx + 0.12 * s, cy), (cx + s, cy + s), (cx - s, cy + s), (cx - 0.12 * s, cy),
               (cx - s, cy - s)]), P([(cx - 0.55 * s, cy + 0.75 * s), (cx + 0.55 * s, cy + 0.75 * s)])]


def eye(cx, cy, s):
    a = np.linspace(0, math.pi, 40)
    return [np.column_stack([cx - s * np.cos(a), cy - 0.45 * s * np.sin(a)]), np.column_stack([cx - s * np.cos(a), cy + 0.45 * s * np.sin(a)]),
            ellipse(cx, cy, 0.3 * s, 0.3 * s, 0, 360, 30), ellipse(cx, cy, 0.1 * s, 0.1 * s, 0, 360, 16)]


def door(x, y, w, h):
    return [P([(x, y), (x, y - h), (x + w, y - h), (x + w, y)]), ellipse(x + 0.82 * w, y - 0.48 * h, 6, 6, 0, 360, 12)]


def checkbox(x, y, s, ticked):
    out = [rect(x, y - s, s, s)]
    if ticked:
        out.append(P([(x + 0.2 * s, y - 0.5 * s), (x + 0.42 * s, y - 0.2 * s), (x + 0.85 * s, y - 0.85 * s)]))
    return out


RUN_A = dict(lean=14, head=6, ls=62, le=80, rs=-38, re=70, lh=38, lk=-18, rh=-30, rk=-72)
RUN_B = dict(lean=14, head=6, ls=-38, le=70, rs=62, re=80, lh=-30, lk=-72, rh=38, rk=-18)


def runner(c, x, y, s, t, a, col=WHITE, phase=0.0, crown=False, robot=False):
    """A figure running in place (a stride every ~0.55 s) over a ground that slides away under it."""
    k = 0.5 + 0.5 * math.sin(2 * math.pi * (t / 0.55 + phase))
    polys, j = figure(x, y, s, pose_mix(RUN_A, RUN_B, k), 1, robot=robot)
    stroke_polys(c, polys, col, 1.9, a)
    if crown:
        hx, hy = j["head"]
        r = 0.062 * s
        stroke_polys(c, [P([(hx - r, hy - 1.1 * r), (hx - r, hy - 1.9 * r), (hx - 0.5 * r, hy - 1.4 * r), (hx, hy - 2.1 * r),
                            (hx + 0.5 * r, hy - 1.4 * r), (hx + r, hy - 1.9 * r), (hx + r, hy - 1.1 * r)])], GOLD, 2.0, a)
    gy = y + 0.48 * s + 6
    for i in range(9):
        xx = x - 1.1 * s + ((i * 0.28 * s - t * 1.6 * s) % (2.5 * s))
        c.drawLine(xx, gy, xx + 0.12 * s, gy, mg.stroke(SOFT, 2.0, a))


# ---------------------------------------------------------------- GROUND
T_C0, T_SEPT, T_LAB, T_CUT, T_FIFTH = ls("cut20"), wd("cut20", "september,"), wd("cut20", "lab"), wd("cut20", "cut"), wd("cut20", "fifth.")
T_R0, T_NINETY, T_RIVAL, T_TWO, T_HALF = ls("rival"), wd("rival", "ninety"), wd("rival", "rival"), wd("rival", "two"), wd("rival", "half")
T_B0, T_COMP, T_AFT, T_CHEAP = ls("both"), wd("both", "companies."), wd("both", "afternoon."), wd("both", "cheaper.")
T_ACT0 = ls("actually")
AX, BX = 560, 1360                                          # lab A's side, lab B's side


def ground(c, t):
    a = win(t, 0.8, T_ACT0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "22 SEPTEMBER 2026", CX, 80, t, T_SEPT - 0.3, 26, WHITE, a=a)
        lines_in(c, tag(AX, 330, 330, 150), t, T_C0 + 0.2, 0.6, WHITE, 2.0)
        roll(c, "$5", "$4", 100, AX + 30, 330, t, T_C0 + 0.4, T_CUT, a)
        label(c, "PER MILLION INPUT TOKENS", AX, 445, t, T_CUT + 0.2, 18, SOFT, a=a)
        label(c, "−20%", AX + 250, 290, t, T_FIFTH - 0.3, 34, GOLD, a=a, cps=20)
        lines_in(c, chip(AX, 640, 90), t, T_LAB - 0.3, 0.6, WHITE, 1.9, seed_pt=(AX, 640))
        label(c, "LAB A · ITS BEST MODEL", AX, 800, t, T_LAB, 20, GLOW, a=a)
        label(c, "ANTHROPIC · CLAUDE OPUS 5.5", AX, 832, t, T_FIFTH, 16, SOFT, a=a)
        if t >= T_R0 - 0.2:                                                 # ninety minutes later: lab B, two models, half
            k = ease(seg(t, T_NINETY - 0.3, T_RIVAL))
            arc = [(lerp(AX + 180, BX - 180, u), 230 - 90 * math.sin(math.pi * u)) for u in np.linspace(0, k, 40)]
            if k > 0:
                stroke_polys(c, [P(arc)], GLOW, 2.2, 1.0)
            label(c, "≈ 90 MINUTES LATER", CX, 126, t, T_NINETY, 22, GLOW, a=a)
            for i, (dx, name, price) in enumerate(((-130, "MODEL 1", "$2"), (130, "MODEL 2", "10¢"))):
                t_i = T_TWO - 0.2 + 0.3 * i
                lines_in(c, chip(BX + dx, 640, 70), t, t_i, 0.5, WHITE, 1.8, seed_pt=(BX + dx, 640))
                label(c, name, BX + dx, 770, t, t_i + 0.2, 18, SOFT, a=a)
                if t >= T_HALF - 0.4:
                    lines_in(c, tag(BX + dx, 360, 200, 100), t, T_HALF - 0.4 + 0.15 * i, 0.4, WHITE, 1.8)
                    bignum(c, t, price, 60, BX + dx + 18, 360, T_HALF - 0.3 + 0.15 * i)
            label(c, "LAB B · ITS BIGGEST RIVAL", BX, 800, t, T_RIVAL, 20, GLOW, a=a)
            label(c, "OPENAI · GPT-6 SOL AND LUNA", BX, 832, t, T_HALF + 0.2, 16, SOFT, a=a)
            label(c, "−50% A TOKEN", BX + 240, 470, t, T_HALF + 0.1, 30, GOLD, a=a, cps=24)
            ev(T_HALF - 0.3, "thock", t, BX)
        if t >= T_B0 - 0.2:                                                 # both went cheaper, one afternoon
            kb = ease(seg(t, T_CHEAP - 0.5, T_CHEAP + 0.2))
            for x in (AX, BX):
                if kb > 0:
                    stroke_polys(c, arrow_down(x - 230 if x == AX else x - 290, 280, 280 + 160 * kb), GOLD, 3.0, 1.0)
            label(c, "ONE AFTERNOON", CX, 520, t, T_AFT - 0.3, 26, WHITE, a=a)
            label(c, "BOTH WENT CHEAPER", CX, 560, t, T_CHEAP - 0.3, 26, GOLD, a=a)
            ev(T_CHEAP - 0.5, "whoosh", t, CX)


# ---------------------------------------------------------------- MECHANISM
T_BETTER, T_MONTHS, T_GOOD, T_MUCH = wd("compare", "better"), wd("compare", "months,"), wd("compare", "good."), wd("compare", "much.")
T_CMP0 = ls("compare")
T_SEE0, T_NOBODY, T_EVERYONE, T_PRICE = ls("see"), wd("see", "nobody"), wd("see", "everyone"), wd("see", "price.")
T_SIG0, T_SIGNAL, T_MOVES, T_HOURS, T_WEEKS = ls("signal"), wd("signal", "signal."), wd("signal", "moves,"), wd("signal", "hours,"), wd("signal", "weeks.")
T_K0, T_SIXTY, T_CENTS = ls("thousand"), wd("thousand", "sixty"), wd("thousand", "cents.")
T_NOV0 = ls("novels")
GX, MX, DY, DR = 640, 1280, 640, 190                        # the two dials


def staircase(x0, y0, w, h, n=6):
    pts = [(x0, y0)]
    for k in range(n):
        pts += [(x0 + w * (k + 1) / n, y0 - h * k / n), (x0 + w * (k + 1) / n, y0 - h * (k + 1) / n)]
    return P(pts)


def mechanism(c, t):
    a = win(t, T_ACT0 - 0.05, T_NOV0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "HERE'S WHAT'S ACTUALLY GOING ON", CX, 160, t, T_ACT0 + 0.1, 26, WHITE,
              a=a * (1 - ease(seg(t, T_CMP0 + 0.5, T_CMP0 + 0.9))))
        kc = part(t, T_CMP0, T_SIG0)
        if kc > 0:                                                          # better every few months; how good, how much
            with layer(c, kc):
                kst = 1 - ease(seg(t, T_GOOD - 0.6, T_GOOD - 0.1))
                if kst > 0:
                    lines_in(c, [staircase(560, 760, 800, 420, 7)], t, T_BETTER - 0.3, 0.8, GLOW, 2.4, a=kst)
                    label(c, "BETTER EVERY FEW MONTHS", CX, 300, t, T_MONTHS - 0.3, 22, GLOW, a=a * kc * kst)
                if t >= T_GOOD - 0.5:
                    lines_in(c, dial(GX, DY, DR), t, T_GOOD - 0.5, 0.5, WHITE, 2.0)
                    label(c, "HOW GOOD", GX, DY + 60, t, T_GOOD - 0.4, 26, WHITE, a=a * kc)
                    fog = ease(seg(t, T_NOBODY - 0.2, T_NOBODY + 0.4))
                    jit = 0.5 + 0.28 * math.sin(t * 9.0) * fog + 0.12 * math.sin(t * 23.0) * fog
                    needle(c, GX, DY, DR, jit, WHITE, a * kc)
                    if fog > 0:
                        label(c, "? TAKES WEEKS TO TELL", GX, DY - DR - 40, t, T_NOBODY, 20, SOFT, a=a * kc * fog)
                if t >= T_MUCH - 0.5:
                    lines_in(c, dial(MX, DY, DR), t, T_MUCH - 0.5, 0.5, WHITE, 2.0)
                    label(c, "HOW MUCH", MX, DY + 60, t, T_MUCH - 0.4, 26, GOLD, a=a * kc)
                    needle(c, MX, DY, DR, keys(t, [(T_MUCH - 0.3, 0.5), (T_PRICE, 0.82)]), GOLD, a * kc)
                    if t >= T_EVERYONE - 0.3:
                        bignum(c, t, "$4", 80, MX, DY - DR - 60, T_EVERYONE - 0.2)
                        label(c, "READ IN SECONDS", MX, DY + 100, t, T_PRICE - 0.3, 20, GOLD, a=a * kc)
                ev(T_GOOD - 0.5, "form", t, GX)
                ev(T_MUCH - 0.5, "form", t, MX)
        ks = part(t, T_SIG0, T_K0)
        if ks > 0:                                                          # the price as a signal: hours, not weeks
            with layer(c, ks):
                lines_in(c, tag(CX, 330, 300, 140), t, T_SIG0, 0.5, GOLD, 2.2)
                label(c, "PRICE", CX + 20, 342, t, T_SIG0 + 0.2, 34, GOLD, a=a * ks, cps=20)
                rings(c, CX, 330, t, T_SIGNAL - 0.3, a * ks, GOLD)
                label(c, "THE SIGNAL", CX, 160, t, T_SIGNAL - 0.3, 26, WHITE, a=a * ks)
                if t >= T_MOVES - 0.3:
                    kw = ease(seg(t, T_WEEKS - 0.5, T_WEEKS + 0.3))
                    c.drawRect(skia.Rect.MakeXYWH(360, 640, 1200, 44), mg.fill(SOFT, 0.35 * a * ks))
                    label(c, "WEEKS", 360, 620, t, T_WEEKS - 0.5, 20, SOFT, "left", a=a * ks)
                    if kw > 0:                                              # weeks: struck through
                        c.drawLine(340, 662, lerp(340, 1580, kw), 662, mg.stroke(WHITE, 3.0, a * ks))
                    kh = ease(seg(t, T_HOURS - 0.4, T_HOURS + 0.1))
                    c.drawRect(skia.Rect.MakeXYWH(360, 740, 60 * kh, 44), mg.fill(GLOW, 0.9 * a * ks))
                    label(c, "HOURS", 440, 772, t, T_HOURS - 0.3, 24, GLOW, "left", a=a * ks)
                    label(c, "ONCE ONE LAB MOVES, THE OTHER HAS", CX, 560, t, T_MOVES - 0.2, 20, WHITE, a=a * ks)
                    ev(T_HOURS - 0.4, "tick", t, 380)
        if t >= T_K0 - 0.2:                                                 # $60 (2021) to 6 cents (2024): 1,000x
            kk = ease(seg(t, T_K0 - 0.2, T_K0 + 0.3))
            with layer(c, kk):
                ruler(c, t, T_K0 - 0.1, a * kk)
                marker(c, px(60), t, T_SIXTY - 0.3, "$60", "2021", GOLD, a * kk)
                if t >= T_SIXTY:
                    x = keys(t, [(T_SIXTY + 0.2, px(60)), (T_CENTS - 0.1, px(0.06))])
                    c.drawLine(px(60), RY + 70, x, RY + 70, mg.stroke(GLOW, 2.4, a * kk))
                    c.drawCircle(x, RY + 70, 8, mg.fill(GLOW, a * kk))
                    ev(T_SIXTY + 0.2, "whoosh", t, CX)
                if t >= T_CENTS - 0.3:
                    marker(c, px(0.06), t, T_CENTS - 0.3, "6¢", "2024", GLOW, a * kk)
                    bignum(c, t, "1,000×", 110, CX, 300, T_CENTS - 0.1)
                    label(c, "THE SAME LEVEL OF AI · a16z", CX, 390, t, T_CENTS + 0.4, 20, SOFT, a=a * kk)


# ---------------------------------------------------------------- YOU
T_MILLION, T_WORDS, T_EIGHT = wd("novels", "million"), wd("novels", "words."), wd("novels", "eight")
T_P0, T_CHEAPEST, T_READ, T_PENCE = ls("tenp"), wd("tenp", "cheapest"), wd("tenp", "read"), wd("tenp", "pence.")
T_L0, T_LIST, T_REVIEW, T_EMAILS = ls("list"), wd("list", "list."), wd("list", "review"), wd("list", "emails.")
T_NAME0 = ls("name")
SHELF_Y, BOOK_X0 = 700, 560


def you(c, t):
    a = win(t, T_NOV0 - 0.05, T_NAME0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kn = part(t, T_NOV0, T_L0)
        if kn > 0:                                                          # a million tokens: eight novels, under 10p
            with layer(c, kn):
                bignum(c, t, "1,000,000", 90, CX, 230, T_MILLION - 0.3)
                label(c, "TOKENS", CX, 310, t, T_MILLION + 0.2, 22, SOFT, a=a * kn)
                label(c, "≈ 750,000 WORDS", CX, 360, t, T_WORDS - 0.4, 26, WHITE, a=a * kn)
                c.drawLine(BOOK_X0 - 40, SHELF_Y, BOOK_X0 + 840, SHELF_Y, mg.stroke(WHITE, 2.0, a * kn * ease(seg(t, T_EIGHT - 0.8, T_EIGHT - 0.4))))
                for i in range(8):
                    tb = T_EIGHT - 0.3 + 0.12 * i
                    h = 200 + 40 * ((i * 5) % 3)
                    lines_in(c, book(BOOK_X0 + i * 100, SHELF_Y, 80, h), t, tb, 0.35, WHITE, 1.8)
                    ev(tb, "tick", t, BOOK_X0 + i * 100)
                label(c, "≈ 8 NOVELS", CX, 770, t, T_EIGHT + 0.6, 26, GLOW, a=a * kn)
                if t >= T_READ - 0.3:                                       # read for under ten pence
                    u = seg(t, T_READ - 0.3, T_PENCE - 0.4)
                    xs = lerp(BOOK_X0 - 30, BOOK_X0 + 830, u)
                    if 0 < u < 1:
                        c.drawLine(xs, SHELF_Y - 300, xs, SHELF_Y + 10, mg.stroke(GLOW, 3.0, a * kn))
                    label(c, "THE NEW CHEAPEST PRICE: $0.10 PER MILLION", CX, 820, t, T_CHEAPEST, 18, SOFT, a=a * kn)
                    if t >= T_PENCE - 0.5:
                        lines_in(c, [ellipse(1580, 360, 90, 90, 0, 360, 60), ellipse(1580, 360, 72, 72, 0, 360, 60)], t, T_PENCE - 0.5, 0.4, GOLD, 2.2)
                        label(c, "10P", 1580, 372, t, T_PENCE - 0.3, 34, GOLD, a=a * kn)
                        label(c, "LESS THAN", 1580, 230, t, T_PENCE - 0.3, 20, GOLD, a=a * kn)
                        ev(T_PENCE - 0.5, "coin", t, 1580)
        if t >= T_L0 - 0.2:                                                 # a reading list, every review, a year of email
            kl = ease(seg(t, T_L0 - 0.2, T_L0 + 0.3))
            with layer(c, kl):
                lines_in(c, page(380, 330, 200, 270), t, T_LIST - 0.6, 0.5, WHITE, 1.9)
                label(c, "YOUR WHOLE READING LIST", 480, 700, t, T_LIST - 0.4, 20, GLOW, a=a * kl)
                for i in range(5):
                    lines_in(c, [star(800 + i * 80, 470, 34)], t, T_REVIEW - 0.4 + 0.08 * i, 0.3, GOLD, 2.0)
                label(c, "EVERY REVIEW A TAKEAWAY HAS EVER HAD", 960, 700, t, T_REVIEW - 0.2, 20, GLOW, a=a * kl)
                for i in range(3):
                    lines_in(c, envelope(1440 + 18 * i, 440 + 26 * i, 220, 140), t, T_EMAILS - 0.6 + 0.1 * i, 0.4, WHITE, 1.8)
                label(c, "A YEAR OF YOUR EMAILS", 1460, 700, t, T_EMAILS - 0.4, 20, GLOW, a=a * kl)
                ev(T_LIST - 0.6, "paper", t, 480)
                ev(T_EMAILS - 0.6, "paper", t, 1460)


# ---------------------------------------------------------------- IDEA
T_Q0, T_QUEEN, T_ALICE, T_RUNNING, T_PLACE = ls("queen"), wd("queen", "queen"), wd("queen", "alice:"), wd("queen", "running"), wd("queen", "place.")
T_V0, T_1973, T_SPECIES, T_AHEAD, T_EVOLV = ls("vanvalen"), wd("vanvalen", "nineteen"), wd("vanvalen", "species"), wd("vanvalen", "ahead."), wd("vanvalen", "evolving")
T_RU0, T_LABS, T_STAY, T_STEP, T_CHEAPER = ls("running"), wd("running", "labs,"), wd("running", "stay"), wd("running", "step"), wd("running", "cheaper.")
T_IMAG0 = ls("imagine")


def idea(c, t):
    a = win(t, T_NAME0 - 0.05, T_IMAG0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "BIOLOGISTS HAVE A NAME FOR THIS", CX, 160, t, T_NAME0 + 0.1, 26, WHITE,
              a=a * (1 - ease(seg(t, T_Q0 + 0.4, T_Q0 + 0.8))))
        kq = part(t, T_Q0, T_V0)
        if kq > 0:                                                          # the Red Queen and Alice, running in place
            with layer(c, kq):
                if t >= T_Q0 + 0.1:
                    runner(c, 760, 560, 330, t, a * kq * ease(seg(t, T_Q0 + 0.1, T_Q0 + 0.6)), GOLD, 0.0, crown=True)
                    label(c, "THE RED QUEEN · LEWIS CARROLL · 1871", CX, 200, t, T_QUEEN - 0.3, 24, GOLD, a=a * kq)
                if t >= T_ALICE - 0.4:
                    runner(c, 1160, 570, 300, t, a * kq, WHITE, 0.35)
                    label(c, "ALICE", 1160, 330, t, T_ALICE - 0.2, 20, SOFT, a=a * kq)
                label(c, "ALL THE RUNNING YOU CAN DO", CX, 800, t, T_RUNNING - 0.2, 24, WHITE, a=a * kq)
                label(c, "TO KEEP IN THE SAME PLACE", CX, 840, t, T_PLACE - 0.5, 24, GLOW, a=a * kq)
                ev(T_Q0 + 0.1, "form", t, 760)
        kv = part(t, T_V0, T_RU0)
        if kv > 0:                                                          # Van Valen: two lines climbing, the gap fixed
            with layer(c, kv):
                label(c, "LEIGH VAN VALEN · 1973", CX, 180, t, T_1973 - 0.3, 26, WHITE, a=a * kv)
                label(c, "\"A NEW EVOLUTIONARY LAW\"", CX, 220, t, T_1973 + 0.4, 20, SOFT, a=a * kv)
                k = ease(seg(t, T_SPECIES - 0.4, T_EVOLV + 0.6))
                n = max(2, int(80 * k))
                xs = np.linspace(360, 1560, 80)[:n]
                y1 = 760 - 360 * (xs - 360) / 1200 - 18 * np.sin((xs - 360) / 70)
                stroke_polys(c, [np.column_stack([xs, y1])], GLOW, 2.6, 1.0)
                stroke_polys(c, [np.column_stack([xs, y1 - 110])], GOLD, 2.6, 1.0)
                if n > 4:
                    label(c, "A SPECIES", xs[-1] + 20, y1[-1] + 8, t, T_SPECIES - 0.2, 20, GLOW, "left", a=a * kv)
                    label(c, "ITS RIVALS", xs[-1] + 20, y1[-1] - 102, t, T_EVOLV - 0.3, 20, GOLD, "left", a=a * kv)
                if t >= T_AHEAD - 0.4:
                    xm, ym = 960, 760 - 360 * 600 / 1200 - 18 * math.sin(600 / 70)
                    stroke_polys(c, [P([(xm, ym - 14), (xm, ym - 96)]), P([(xm - 12, ym - 84), (xm, ym - 96), (xm + 12, ym - 84)]),
                                     P([(xm - 12, ym - 26), (xm, ym - 14), (xm + 12, ym - 26)])], WHITE, 2.0, a * kv)
                    label(c, "THE GAP NEVER CLOSES", xm, ym + 70, t, T_AHEAD - 0.3, 22, WHITE, a=a * kv)
                ev(T_SPECIES - 0.4, "riser", t, CX)
        if t >= T_RU0 - 0.2:                                                # two labs running; every step, cheaper
            kr = ease(seg(t, T_RU0 - 0.2, T_RU0 + 0.3))
            with layer(c, kr):
                runner(c, 700, 420, 280, t, a * kr, WHITE, 0.0, robot=True)
                runner(c, 1220, 420, 280, t, a * kr, GLOW, 0.4, robot=True)
                label(c, "LAB A", 700, 200, t, T_LABS - 0.3, 22, WHITE, a=a * kr)
                label(c, "LAB B", 1220, 200, t, T_LABS - 0.1, 22, GLOW, a=a * kr)
                label(c, "EXACTLY WHERE THEY ARE", CX, 260, t, T_STAY - 0.2, 22, SOFT, a=a * kr)
                if t >= T_STEP - 0.6:
                    ruler(c, t, T_STEP - 0.6, a * kr, y=760)
                    steps = int(max(0.0, t - T_STEP + 0.2) / 0.55)
                    x = px(5.0 / (1.6 ** min(steps, 12)))
                    c.drawCircle(x, 760, 10, mg.fill(GOLD, a * kr))
                    label(c, "EVERY STEP: CHEAPER FOR YOU", CX, 840, t, T_CHEAPER - 0.5, 22, GOLD, a=a * kr)
                    if steps:
                        ev(T_STEP - 0.2 + 0.55 * steps, "tick", t, x)


# ---------------------------------------------------------------- IMAGINE
T_WHATIF = ls("whatif")
T_TU0, T_TUTOR, T_TEXT = ls("tutor"), wd("tutor", "tutor"), wd("tutor", "text")
T_CO0, T_CODER, T_TRANS, T_OPIN = ls("coder"), wd("coder", "coder."), wd("coder", "translator."), wd("coder", "opinion.")
T_EX0, T_FREE, T_EXP = ls("expensive"), wd("expensive", "free,"), wd("expensive", "expensive?")
T_MB0, T_SEND, T_TIME, T_ATTN, T_UP = ls("maybe"), wd("maybe", "send"), wd("maybe", "time."), wd("maybe", "attention."), wd("maybe", "up.")
T_TN0 = ls("tonight")


def imagine(c, t):
    a = win(t, T_IMAG0 - 0.05, T_TN0 + 0.2, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        ki = part(t, T_IMAG0, T_TU0)
        if ki > 0:                                                          # the ruler runs on past a cent, in dashes
            with layer(c, ki):
                ruler(c, t, T_IMAG0, a * ki)
                k = ease(seg(t, T_IMAG0 + 0.6, T_WHATIF))
                dashes(c, RX1, lerp(RX1, RX1 + 150, k), RY, 0.8 * a * ki)
                x = keys(t, [(T_IMAG0 + 0.4, px(0.1)), (T_WHATIF + 0.6, RX1 + 140)])
                c.drawCircle(x, RY, 9, mg.fill(GOLD, a * ki))
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 220, t, T_WHATIF + 0.05, 26, GLOW, a=a * ki)
        kt = part(t, T_TU0, T_EX0)
        if kt > 0:                                                          # a tutor for less than a text; then the rest
            with layer(c, kt):
                ktu = 1 - ease(seg(t, T_CO0 - 0.2, T_CO0 + 0.2))
                if ktu > 0:
                    polys, _ = figure(620, 520, 300, dict(lean=0, head=4, ls=8, le=10, rs=120, re=-40, lh=4, lk=0, rh=-4, rk=0), 1)
                    lines_in(c, polys, t, T_TUTOR - 0.6, 0.6, WHITE, 1.9, a=ktu)
                    label(c, "THE BEST TUTOR ON EARTH", 620, 790, t, T_TUTOR - 0.3, 22, WHITE, a=a * kt * ktu)
                    lines_in(c, bubble(1300, 470, 340, 160), t, T_TEXT - 0.6, 0.5, GLOW, 2.0, a=ktu)
                    label(c, "ONE TEXT MESSAGE", 1300, 480, t, T_TEXT - 0.4, 22, GLOW, a=a * kt * ktu)
                    label(c, "<", 960, 500, t, T_TEXT - 0.2, 60, GOLD, a=a * kt * ktu)
                for i, (tt, name) in enumerate(((T_CODER, "THE BEST CODER"), (T_TRANS, "THE BEST TRANSLATOR"), (T_OPIN, "THE BEST SECOND OPINION"))):
                    if t >= tt - 0.6:
                        x = 420 + i * 540
                        lines_in(c, [rect(x - 200, 380, 400, 240, 0.0)], t, tt - 0.6, 0.4, WHITE, 1.9)
                        glyph = ("</>", "HOLA → HELLO", "?")[i]
                        label(c, glyph, x, 520, t, tt - 0.4, 50 if i != 1 else 34, GLOW, a=a * kt)
                        label(c, name, x, 680, t, tt - 0.3, 20, WHITE, a=a * kt)
                        ev(tt - 0.6, "form", t, x)
        ke = part(t, T_EX0, T_MB0)
        if ke > 0:                                                          # the question
            with layer(c, ke):
                label(c, "WHEN THINKING IS ALMOST FREE,", CX, 440, t, T_FREE - 0.6, 34, WHITE, a=a * ke, cps=30)
                label(c, "WHAT GETS EXPENSIVE?", CX, 520, t, T_EXP - 0.6, 44, GOLD, a=a * ke, cps=26)
                ev(T_EXP - 0.6, "swell", t, CX)
        if t >= T_MB0 - 0.2:                                                # time, attention, someone who turns up
            km = ease(seg(t, T_MB0 - 0.2, T_MB0 + 0.3))
            with layer(c, km):
                label(c, "THINGS A MACHINE CAN'T SEND YOU", CX, 200, t, T_SEND - 0.3, 24, WHITE, a=a * km)
                lines_in(c, hourglass(480, 500, 110), t, T_TIME - 0.6, 0.5, GOLD, 2.2)
                label(c, "YOUR TIME", 480, 700, t, T_TIME - 0.4, 22, GOLD, a=a * km)
                lines_in(c, eye(960, 500, 150), t, T_ATTN - 0.7, 0.5, GOLD, 2.2)
                label(c, "YOUR ATTENTION", 960, 700, t, T_ATTN - 0.5, 22, GOLD, a=a * km)
                lines_in(c, door(1360, 640, 170, 340), t, T_UP - 1.0, 0.5, WHITE, 2.0)
                polys, _ = figure(1445, 470, 260, dict(lean=0, head=4, ls=8, le=10, rs=150, re=-20, lh=4, lk=0, rh=-4, rk=0), -1)
                lines_in(c, polys, t, T_UP - 0.8, 0.5, GOLD, 2.0)
                label(c, "SOMEONE WHO TURNS UP", 1445, 700, t, T_UP - 0.6, 22, GOLD, a=a * km)
                ev(T_UP - 0.8, "form", t, 1445)


# ---------------------------------------------------------------- SURFACE
T_JOB, T_READING, T_PENNIES = wd("tonight", "job"), wd("tonight", "reading,"), wd("tonight", "pennies.")
T_F0, T_FIFTH2, T_HALF2 = ls("fifth"), wd("fifth", "fifth."), wd("fifth", "half.")
T_S0, T_STILL = ls("still"), wd("still", "running.")
T_SRC = le("still") + 1.2
SOURCES = ["SOURCES",
           "22 Sep 2026: Anthropic Claude Opus 5.5 $4 / $20 per million tokens (Opus 5: $5 / $25); The Neuron, AIOS Guide",
           "About 90 min later: OpenAI GPT-6 Sol ($2 / $10) and Luna ($0.10 / $0.50), about half their predecessors' prices",
           "a16z, Welcome to LLMflation (Nov 2024): GPT-3-level AI $60 → $0.06 per million tokens, 2021 → 2024",
           "~0.75 words a token; a novel ~90,000 words · Carroll, Through the Looking-Glass (1871)",
           "Leigh Van Valen, A New Evolutionary Law (1973) · the what-if is imagined, not a forecast"]


def surface(c, t):
    a = win(t, T_TN0 - 0.05, T_SRC + 0.1, 0.3, 0.6)
    if a > 0:
        with layer(c, a):
            kn = part(t, T_TN0, T_F0)
            if kn > 0:                                                      # the job you've been putting off
                with layer(c, kn):
                    lines_in(c, [rect(560, 260, 800, 420, 0.0)], t, T_TN0 + 0.1, 0.5, WHITE, 1.9)
                    label(c, "TONIGHT", 600, 310, t, T_TN0 + 0.2, 22, GLOW, "left", a=a * kn)
                    for i, (txt, tk) in enumerate((("Reply to the landlord", True), ("Book the dentist", True),
                                                   ("Read the 200-page contract", False))):
                        y = 400 + i * 90
                        stroke_polys(c, checkbox(600, y, 40, tk), WHITE if tk else GOLD, 2.0, a * kn)
                        label(c, txt, 670, y - 8, t, T_TN0 + 0.4 + 0.2 * i, 26, SOFT if tk else WHITE, "left", a=a * kn)
                    if t >= T_JOB - 0.3:
                        c.drawRect(skia.Rect.MakeXYWH(586, 526, 740, 68), mg.stroke(GOLD, 2.2, a * kn))
                        label(c, "HOURS OF READING", 960, 740, t, T_READING - 0.5, 22, GOLD, a=a * kn)
                    if t >= T_PENNIES - 0.6:
                        lines_in(c, [ellipse(1500, 583, 50, 50, 0, 360, 40)], t, T_PENNIES - 0.6, 0.3, GOLD, 2.2)
                        label(c, "1P", 1500, 593, t, T_PENNIES - 0.5, 26, GOLD, a=a * kn)
                        label(c, "FOR PENNIES", 1500, 680, t, T_PENNIES - 0.4, 22, GOLD, a=a * kn)
                        stroke_polys(c, [P([(1330, 583), (1440, 583)]), P([(1425, 571), (1440, 583), (1425, 595)])], GOLD, 2.2, a * kn)
                        ev(T_PENNIES - 0.6, "coin", t, 1500)
            kf = part(t, T_F0, T_SRC - 0.4)
            if kf > 0:                                                      # the two cuts mirrored; both still running
                with layer(c, kf):
                    lines_in(c, tag(AX, 330, 380, 150), t, T_F0, 0.5, WHITE, 2.0)
                    bignum(c, t, "-20%", 62, AX + 30, 330, T_FIFTH2 - 0.6)
                    lines_in(c, tag(BX, 330, 380, 150), t, T_FIFTH2 + 0.1, 0.5, WHITE, 2.0)
                    bignum(c, t, "-50%", 62, BX + 30, 330, T_HALF2 - 0.6)
                    if t >= T_S0 - 0.2:
                        runner(c, AX, 650, 240, t, a * kf, WHITE, 0.0, robot=True)
                        runner(c, BX, 650, 240, t, a * kf, GLOW, 0.4, robot=True)
                        label(c, "STILL RUNNING", CX, 560, t, T_STILL - 0.6, 26, GOLD, a=a * kf)
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
    you(c, t)
    idea(c, t)
    imagine(c, t)
    surface(c, t)
