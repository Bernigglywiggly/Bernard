"""EP11 · THE LIBRARY OF EVERY BOOK, the scenes: line art keyed to the script's line ids and George's words
(engine.tl.word), which the engine turns into characters.

  GROUND     1941 and a hexagonal gallery of shelves; a page of letters that never repeats (410 pages, 25 symbols);
             the answer among the wrong answers; the galleries going on for ever; a chip that answers in seconds
  MECHANISM  the number of books typed on one line (4.7 km) against the universe's atoms (81 digits, 21 cm); 15
             trillion tokens pouring into a chip; tens of terabytes against ~140 GB; which word comes next; Shannon
             guessing letters, and guessing as squeezing
  NOW        fluent / right; a fact seen thousands of times against a fact seen once; three wrong birthdays; a hundred
             facts, a fifth seen once, a fifth wrong; two quiz bars (always guessing: 75% wrong; "I don't know": 26%)
  IDEA       a path through nonsense to the true page; a chip's straight line to a likely one; finding / checking
  IMAGINE    a librarian beside a child, then beside every child; Bloom's two bell curves (98%); six weeks against a
             year and a half to two of school; a school
  SURFACE    every book (the galleries) | the page you ask for (a page and a question mark); the sources
"""
import math
from decimal import Decimal, getcontext

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         points, stroke_polys, bignum, chip, page, roll, bump, burst, figure, STAND, keys)

TRAILS = []
GLINTS = []
RNG = np.random.default_rng(11)
SYM = "abcdefghijklmnopqrstuv ,."                       # Borges' 25 symbols: 22 letters, the space, the comma, the full stop


# ---------------------------------------------------------------- the number of books, for real
def _borges_digits(n=60):
    """The first and last n digits of 25^1,312,000 (the number of books), exactly."""
    getcontext().prec = n + 40
    e = Decimal(1312000) * Decimal(25).log10()
    frac = e - int(e)
    head = str(Decimal(10) ** frac).replace(".", "")[:n]
    tail = str(pow(25, 1312000, 10 ** n)).zfill(n)
    return head, tail


HEAD, TAIL = _borges_digits()
ATOMS81 = "1" + "0" * 80


# ---------------------------------------------------------------- things
def hexagon(cx, cy, r, rot=0.0):
    a = np.linspace(0, 2 * math.pi, 7) + rot
    return np.column_stack([cx + r * np.cos(a), cy + r * np.sin(a)])


def gallery(cx, cy, r, books=True):
    """One of Borges' hexagonal galleries, from above: shelves on four walls, two open to the next galleries."""
    out = [hexagon(cx, cy, r)]
    v = [(cx + r * math.cos(k * math.pi / 3), cy + r * math.sin(k * math.pi / 3)) for k in range(6)]
    for k in (0, 1, 3, 4):
        (x0, y0), (x1, y1) = v[k], v[(k + 1) % 6]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        nx, ny = cx - mx, cy - my
        n = math.hypot(nx, ny)
        nx, ny = nx / n, ny / n
        d = 0.16 * r
        out.append(P([(lerp(x0, x1, 0.16) + nx * d, lerp(y0, y1, 0.16) + ny * d), (lerp(x0, x1, 0.84) + nx * d, lerp(y0, y1, 0.84) + ny * d)]))
        if books:
            for j in range(14):
                u = lerp(0.18, 0.82, (j + 0.5) / 14)
                bx, by = lerp(x0, x1, u), lerp(y0, y1, u)
                out.append(P([(bx + nx * 0.03 * r, by + ny * 0.03 * r), (bx + nx * d * 0.92, by + ny * d * 0.92)]))
    return out


def comb_centres(cx, cy, r, cols, rows):
    out = []
    for i in range(-cols, cols + 1):
        for j in range(-rows, rows + 1):
            out.append((cx + 1.5 * r * i, cy + math.sqrt(3) * r * (j + (0.5 if i % 2 else 0))))
    return out


def gib(n, seed):
    r = np.random.default_rng(seed)
    return "".join(SYM[i] for i in r.integers(0, 25, n))


def power(c, t, exp, size, cx, cy, t0):
    """10 to a power, as a big number with a raised exponent."""
    bignum(c, t, "10", size, cx - 0.45 * size, cy, t0)
    bignum(c, t, exp, 0.5 * size, cx + 0.72 * size, cy - 0.5 * size, t0 + 0.15)


def cross(cx, cy, s):
    return [P([(cx - s, cy - s), (cx + s, cy + s)]), P([(cx + s, cy - s), (cx - s, cy + s)])]


def tick_mark(cx, cy, s):
    return [P([(cx - s, cy), (cx - 0.3 * s, cy + 0.7 * s), (cx + s, cy - 0.8 * s)])]


def qmark(cx, cy, s):
    arc = np.column_stack([cx + 0.5 * s * np.cos(np.linspace(math.pi, 2.4 * math.pi, 30)), cy - 0.5 * s + 0.45 * s * np.sin(np.linspace(math.pi, 2.4 * math.pi, 30))])
    return [np.vstack([arc, [(cx, cy + 0.15 * s), (cx, cy + 0.35 * s)]]), ellipse(cx, cy + 0.62 * s, 0.07 * s, 0.07 * s, 0, 360, 16)]


def bell(x0, x1, mu, sd, top, h, n=120):
    xs = np.linspace(x0, x1, n)
    return np.column_stack([xs, top + h - h * np.exp(-0.5 * ((xs - mu) / sd) ** 2)])


def school(cx, bot, s):
    """A school: a block, a pediment, a door and windows, a bell."""
    out = [rect(cx - s, bot - 0.8 * s, 2 * s, 0.8 * s), P([(cx - 1.1 * s, bot - 0.8 * s), (cx, bot - 1.25 * s), (cx + 1.1 * s, bot - 0.8 * s)]),
           rect(cx - 0.14 * s, bot - 0.38 * s, 0.28 * s, 0.38 * s), ellipse(cx, bot - 0.98 * s, 0.09 * s, 0.09 * s, 0, 360, 24)]
    for k in (-0.7, -0.4, 0.4, 0.7):
        out.append(rect(cx + k * s - 0.1 * s, bot - 0.62 * s, 0.2 * s, 0.2 * s))
    return out


def bar(c, x, y, w, h, parts, k, a):
    """A stacked horizontal bar: parts = [(fraction, colour, filled)], drawn up to k (0..1) of its length."""
    x0 = x
    for f, col, filled in parts:
        ww = w * f * min(1.0, k)
        if ww > 0.5:
            if filled:
                c.drawRect(skia.Rect.MakeXYWH(x0, y, ww, h), mg.fill(col, 0.92 * a))
            else:
                c.drawRect(skia.Rect.MakeXYWH(x0 + 1, y + 1, ww - 2, h - 2), mg.stroke(col, 1.6, 0.9 * a))
        x0 += w * f
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), mg.stroke(SOFT, 1.2, 0.6 * a))


def part(t, a, b, fin=0.3, fout=0.4):
    return win(t, a - 0.1, b + 0.2, fin, fout)


# ---------------------------------------------------------------- GROUND
T_LIB0, T_1941, T_BORGES, T_BOOK = ls("library"), wd("library", "nineteen"), wd("library", "borges"), wd("library", "book")
T_RULE0, T_LETTERS, T_STOPS, T_410, T_SHELF = ls("rule"), wd("rule", "letters"), wd("rule", "stops"), wd("rule", "four"), wd("rule", "shelf")
T_ANS0, T_QUESTION, T_WRONG = ls("answer"), wd("answer", "question"), wd("answer", "wrong")
T_NEVER0, T_FIND = ls("never"), wd("never", "find")
T_OPP0, T_PATTERNS, T_SECONDS = ls("opposite"), wd("opposite", "patterns"), wd("opposite", "seconds")
T_WHY0, T_KEEP = ls("why"), wd("why", "keep")
T_SIZE0 = ls("size")
GALLERY_R = 230
PAGE_X, PAGE_Y, PAGE_W, PAGE_H = 1060, 250, 600, 500


def ground(c, t):
    a = win(t, 1.0, T_SIZE0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kg = part(t, T_LIB0, T_ANS0)
        if kg > 0:                                                          # 1941, a gallery; then a page of every arrangement
            with layer(c, kg):
                gx = keys(t, [(T_RULE0 - 0.2, CX), (T_RULE0 + 0.6, 560)])
                lines_in(c, gallery(gx, 600, GALLERY_R, books=False), t, T_LIB0 + 0.2, 0.9, WHITE, 1.8, seed_pt=(gx, 600))
                kb = ease(seg(t, T_BOOK - 0.5, T_BOOK + 0.4))
                if kb > 0:
                    stroke_polys(c, gallery(gx, 600, GALLERY_R)[1:], GLOW, 1.6, kb)
                    ev(T_BOOK - 0.5, "grains", t, gx)
                k1 = 1 - ease(seg(t, T_RULE0 - 0.3, T_RULE0 + 0.2))
                if k1 > 0:
                    bignum(c, t, "1941", 110, CX, 230, T_1941 - 0.1)
                    label(c, "JORGE LUIS BORGES · THE LIBRARY OF BABEL", CX, 320, t, T_BORGES - 0.2, 22, SOFT, a=a * kg * k1)
                    label(c, "EVERY POSSIBLE BOOK", CX, 830, t, T_BOOK - 0.2, 24, GLOW, a=a * kg * k1)
                if t >= T_RULE0 - 0.1:                                      # the page: letters that never repeat
                    kp = ease(seg(t, T_RULE0 - 0.1, T_RULE0 + 0.4))
                    lines_in(c, [rect(PAGE_X, PAGE_Y, PAGE_W, PAGE_H)], t, T_RULE0, 0.5, WHITE, 1.8)
                    seed = int(t * 5)
                    for row in range(10):
                        label(c, gib(38, seed * 31 + row), PAGE_X + 30, PAGE_Y + 60 + row * 43, t, -1, 22, SOFT, "left", a=a * kg * kp * 0.9)
                    ev(T_RULE0, "paper", t, PAGE_X)
                    label(c, "22 LETTERS · SPACE · COMMA · FULL STOP", PAGE_X + PAGE_W / 2, PAGE_Y + PAGE_H + 50, t, T_LETTERS - 0.2, 20, GLOW, a=a * kg)
                    label(c, "410 PAGES · EVERY ARRANGEMENT", PAGE_X + PAGE_W / 2, PAGE_Y - 30, t, T_410 - 0.2, 22, WHITE, a=a * kg)
        kw = part(t, T_ANS0, T_NEVER0)
        if kw > 0:                                                          # the answer, and every wrong answer
            with layer(c, kw):
                cols, rows, pw, ph = 7, 3, 145, 170
                for i in range(cols * rows):
                    x = 250 + (i % cols) * 245
                    y = 180 + (i // cols) * 220
                    hit = i == 10
                    tk = T_ANS0 + 0.1 if hit else T_WRONG - 0.4 + 0.04 * i
                    if t < tk:
                        continue
                    lines_in(c, page(x, y, pw, ph), t, tk, 0.4, WHITE if hit else SOFT, 2.2 if hit else 1.4)
                    if not hit:
                        label(c, "WRONG", x + pw / 2, y + ph + 24, t, tk + 0.2, 16, SOFT, a=a * kw * 0.8)
                    else:
                        stroke_polys(c, [rect(x - 12, y - 12, pw + 24, ph + 24)], GLOW, 2.4, ease(seg(t, T_QUESTION - 0.2, T_QUESTION + 0.3)))
                        label(c, "THE ANSWER", x + pw / 2, y + ph + 30, t, T_QUESTION - 0.2, 20, GLOW, a=a * kw)
                ev(T_WRONG - 0.4, "paper", t, CX)
        kn = part(t, T_NEVER0, T_OPP0, 0.25, 0.5)
        if kn > 0:                                                          # the galleries going on for ever
            with layer(c, kn):
                z = keys(t, [(T_NEVER0 - 0.2, 1.0), (T_OPP0, 0.32)])
                r = 150 * z
                cs = [(x, y) for x, y in comb_centres(CX, 540, r, 24, 14) if -r < x < 1920 + r and -r < y < 1080 + r]
                stroke_polys(c, [hexagon(x, y, r * 0.96) for x, y in cs], SOFT, 1.3, 0.85)
                c.drawCircle(CX, 540, 5 * z + 3, mg.fill(GOLD, a * kn))
                label(c, "YOU", CX, 540 - 10 * z - 18, t, T_NEVER0 + 0.1, 18, GOLD, a=a * kn)
                label(c, "YOU WOULD NEVER FIND IT", CX, 820, t, T_FIND - 0.2, 26, WHITE, a=a * kn)
                ev(T_NEVER0 - 0.2, "zoom", t, CX)
        if t >= T_OPP0 - 0.2:                                               # the other way round: a chip that answers
            ko = ease(seg(t, T_OPP0 - 0.2, T_OPP0 + 0.4))
            with layer(c, ko):
                lines_in(c, chip(CX, 420, 150), t, T_OPP0, 0.6, WHITE, 2.0, seed_pt=(CX, 420))
                label(c, "PATTERNS, NOT PAGES", CX, 640, t, T_PATTERNS - 0.2, 26, GLOW, a=a * ko)
                if t >= T_SECONDS - 0.9:
                    label(c, "> AN ANSWER, IN SECONDS", 760, 715, t, T_SECONDS - 0.9, 22, WHITE, "left", a=a * ko, cps=34)
                    ev(T_SECONDS - 0.9, "tick", t, 760)
                label(c, "HOW DO YOU ANSWER FROM BOOKS YOU DIDN'T KEEP?", CX, 805, t, T_WHY0 + 0.1, 28, WHITE, a=a * ko)


# ---------------------------------------------------------------- MECHANISM
T_DIGITS, T_MILLION = wd("size", "digits"), wd("size", "million")
T_ATOMS0, T_ATOMS, T_81 = ls("atoms"), wd("atoms", "atoms"), wd("atoms", "eightyone")
T_READ0, T_15, T_TOKENS, T_PIECES = ls("read"), wd("read", "fifteen"), wd("read", "tokens"), wd("read", "pieces")
T_KEPT0, T_TB, T_SMALLER = ls("kept"), wd("kept", "terabytes"), wd("kept", "smaller")
T_PAT0, T_LOOK, T_NEXT = ls("patterns"), wd("patterns", "look"), wd("patterns", "next")
T_SHAN0, T_SHANNON, T_GUESSING, T_COMPRESS, T_SAME = ls("shannon"), wd("shannon", "shannon"), wd("shannon", "guessing"), wd("shannon", "compressing"), wd("shannon", "same")
T_FLU0 = ls("fluent")
STARS = np.column_stack([RNG.uniform(60, 1860, 600), RNG.uniform(60, 1020, 600)])
PIECES = ["un", "believ", "able", " pie", "ces", " of", " wor", "ds", " lib", "rary", " Bor", "ges", " every", " bo", "ok", " sh", "elf"]
NEXT = [("BOOK", 0.71), ("ANSWER", 0.09), ("WORD", 0.06), ("STORY", 0.04)]
GUESSES = "THE LIBRARY HOLDS"
NGUESS = [5, 2, 1, 0, 3, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1]           # tries per letter: an illustration of Shannon's game


def mechanism(c, t):
    a = win(t, T_SIZE0 - 0.05, T_FLU0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        ks = part(t, T_SIZE0, T_READ0)
        if ks > 0:                                                          # the books' number on one line, the atoms' number
            with layer(c, ks):
                points(c, STARS, 0.35 * ease(seg(t, T_ATOMS0 - 0.4, T_ATOMS0 + 0.6)), SOFT, 2.0)
                kd = 1 - ease(seg(t, T_ATOMS0 - 0.2, T_ATOMS0 + 0.3))
                if kd > 0:
                    bignum(c, t, "1,834,098", 110, CX, 250, T_SIZE0 + 0.3)
                    label(c, "DIGITS IN THE NUMBER OF BOOKS", CX, 340, t, T_DIGITS - 0.3, 22, SOFT, a=a * ks * kd)
                k = seg(t, T_SIZE0 + 0.6, T_ATOMS0 + 0.6)                   # the line runs on: 4.7 km of type
                label(c, HEAD[:44] + " …", 160, 500, t, T_SIZE0 + 0.6, 22, WHITE, "left", a=a * ks, cps=60)
                ln = lerp(160, 1760, ease(k, "o"))
                c.drawLine(160, 540, ln, 540, mg.stroke(GLOW, 2.0, a * ks))
                km = 4.66 * ease(k)
                label(c, f"TYPED ON ONE LINE: {km:.1f} KM", 160, 590, t, T_SIZE0 + 0.8, 20, GLOW, "left", a=a * ks)
                label(c, "… " + TAIL[-30:], 1760, 640, t, T_MILLION, 20, SOFT, "right", a=a * ks * 0.8, cps=60)
                if t >= T_ATOMS0 - 0.3:                                     # the atoms: 81 digits, 21 cm
                    kt = ease(seg(t, T_ATOMS0 - 0.3, T_ATOMS0 + 0.3))
                    power(c, t, "80", 110, CX, 250, T_ATOMS - 0.3)
                    label(c, "ATOMS IN THE OBSERVABLE UNIVERSE", CX, 340, t, T_ATOMS, 22, SOFT, a=a * ks * kt)
                    label(c, ATOMS81[:int(81 * ease(seg(t, T_ATOMS, T_81)))], 160, 740, t, -1, 22, GOLD, "left", a=a * ks * kt)
                    label(c, "81 DIGITS · 21 CM ON ONE LINE", 160, 790, t, T_81 - 0.2, 20, GOLD, "left", a=a * ks * kt)
                    ev(T_81 - 0.2, "confirm", t, 400)
        kr = part(t, T_READ0, T_PAT0)
        if kr > 0:                                                          # 15 trillion tokens into a chip; TB against GB
            with layer(c, kr):
                k2 = 1 - ease(seg(t, T_KEPT0 - 0.2, T_KEPT0 + 0.3))
                if k2 > 0:
                    with layer(c, k2):
                        bignum(c, t, "15 TRILLION", 100, CX, 230, T_15 - 0.1)
                        label(c, "TOKENS · META'S LLAMA 3 · 2024", CX, 320, t, T_TOKENS - 0.2, 22, SOFT, a=a * kr * k2)
                        lines_in(c, chip(1480, 620, 120), t, T_READ0 + 0.2, 0.5, WHITE, 1.9)
                        kf = seg(t, T_TOKENS - 0.6, T_KEPT0 + 0.2)
                        for i in range(26):                                 # word pieces streaming in
                            u = (kf * 2.4 + i / 26) % 1.0
                            if kf <= 0 or u > 0.97:
                                continue
                            x = lerp(180, 1380, u)
                            y = 620 + 170 * math.sin(i * 2.3) * (1 - u) ** 1.5
                            label(c, PIECES[i % len(PIECES)].strip(), x, y + 8, t, -1, 20, GLOW, a=a * kr * k2 * (1 - u) * 0.95)
                        ev(T_TOKENS - 0.6, "grains", t, 900)
                        label(c, "TOKENS: PIECES OF WORDS · UN·BELIEV·ABLE", CX, 820, t, T_PIECES - 0.2, 22, WHITE, a=a * kr * k2)
                if t >= T_KEPT0 - 0.2:
                    kk = ease(seg(t, T_KEPT0 - 0.2, T_KEPT0 + 0.3))
                    with layer(c, kk):
                        big = 520 * ease(seg(t, T_TB - 0.4, T_TB + 0.4))
                        c.drawRect(skia.Rect.MakeXYWH(260, 740 - big, big, big), mg.stroke(WHITE, 2.0, a * kr * kk))
                        for j in range(1, 9):                               # the text, page on page
                            yy = 740 - big * j / 9
                            c.drawLine(260, yy, 260 + big, yy, mg.stroke(SOFT, 1.0, 0.6 * a * kr * kk))
                        label(c, "~60 TB OF TEXT", 520, 800, t, T_TB, 22, WHITE, a=a * kr * kk)
                        s = 520 / math.sqrt(430) * ease(seg(t, T_SMALLER - 0.6, T_SMALLER))
                        if s > 1:
                            c.drawRect(skia.Rect.MakeXYWH(1400 - s / 2, 740 - s, s, s), mg.chrome_paint(740 - s, 740, 0.95))
                            stroke_polys(c, [ellipse(1400, 740 - s / 2, 60, 60, 0, 360, 48)], GLOW, 1.6, 0.8)
                        bignum(c, t, "~140 GB", 80, 1400, 480, T_SMALLER - 0.6)
                        label(c, "THE MODEL · HUNDREDS OF TIMES SMALLER", 1400, 800, t, T_SMALLER - 0.3, 20, GLOW, a=a * kr * kk)
                        ev(T_SMALLER - 0.6, "thock", t, 1400)
        kp = part(t, T_PAT0, T_SHAN0)
        if kp > 0:                                                          # which word usually comes next
            with layer(c, kp):
                label(c, "IT KEPT WHAT TEXT TENDS TO LOOK LIKE", CX, 220, t, T_LOOK - 0.3, 24, WHITE, a=a * kp)
                label(c, "THE LIBRARY HOLDS EVERY POSSIBLE ...", 300, 390, t, T_PAT0 + 0.2, 30, WHITE, "left", a=a * kp, cps=40)
                for i, (w, p) in enumerate(NEXT):
                    y = 450 + i * 72
                    tk = T_NEXT - 0.6 + 0.15 * i
                    k = ease(seg(t, tk, tk + 0.6))
                    if k <= 0:
                        continue
                    label(c, w, 640, y + 34, t, tk, 24, GLOW if i == 0 else SOFT, "right", a=a * kp)
                    c.drawRect(skia.Rect.MakeXYWH(680, y + 8, 900 * p * k, 34), mg.fill(GLOW if i == 0 else SOFT, (0.9 if i == 0 else 0.5) * a * kp))
                    label(c, f"{round(100 * p * k)}%", 700 + 900 * p * k, y + 34, t, tk, 20, WHITE, "left", a=a * kp)
                    ev(tk, "tick", t, 700)
                label(c, "WHICH WORD USUALLY COMES NEXT (AN EXAMPLE)", CX, 800, t, T_NEXT - 0.3, 20, SOFT, a=a * kp)
        if t >= T_SHAN0 - 0.2:                                              # Shannon: guess the next letter; guess = squeeze
            kn = ease(seg(t, T_SHAN0 - 0.2, T_SHAN0 + 0.3))
            with layer(c, kn):
                bignum(c, t, "1951", 100, CX, 220, T_SHAN0 + 0.2)
                label(c, "CLAUDE SHANNON · GUESS THE NEXT LETTER", CX, 310, t, T_SHANNON - 0.1, 22, SOFT, a=a * kn)
                sq = ease(seg(t, T_COMPRESS - 0.2, T_COMPRESS + 0.9))
                step = lerp(70, 30, sq)
                x0 = CX - step * len(GUESSES) / 2
                n = int(len(GUESSES) * seg(t, T_GUESSING - 0.6, T_COMPRESS - 0.3))
                for i, ch in enumerate(GUESSES[:max(0, n)]):
                    x = x0 + step * (i + 0.5)
                    label(c, ch, x, 560, t, -1, 44, WHITE)
                    if ch != " " and NGUESS[i]:
                        label(c, str(NGUESS[i]), x, 490, t, -1, 20, GLOW if NGUESS[i] == 1 else GOLD, a=a * kn * (1 - sq))
                    ev(T_GUESSING - 0.6 + i * 0.07, "tick", t, x)
                label(c, "TRIES PER LETTER (AN ILLUSTRATION)", CX, 440, t, T_GUESSING, 20, SOFT, a=a * kn * (1 - sq))
                if sq > 0:
                    w = step * len(GUESSES)
                    c.drawRect(skia.Rect.MakeXYWH(CX - w / 2 - 14, 600, w + 28, 14), mg.chrome_paint(600, 614, 0.95 * sq))
                    ev(T_COMPRESS - 0.2, "hydraulic", t, CX)
                label(c, "GUESS WELL = COMPRESS WELL", CX, 760, t, T_SAME - 0.3, 28, GLOW, a=a * kn)
                label(c, "THE SAME PROBLEM", CX, 820, t, T_SAME, 22, WHITE, a=a * kn)


# ---------------------------------------------------------------- NOW
T_FLUENT, T_DESIGN, T_RIGHT = wd("fluent", "fluent"), wd("fluent", "design"), wd("fluent", "right")
T_ONCE0, T_THOUSANDS, T_CARRIES, T_ONCE = ls("once"), wd("once", "thousands"), wd("once", "carries"), wd("once", "once")
T_BD0, T_BIRTHDAY, T_KNEW, T_TRIES, T_DATES = ls("birthday"), wd("birthday", "birthday"), wd("birthday", "knew"), wd("birthday", "tries"), wd("birthday", "dates")
T_FIFTH0, T_FIFTH, T_ONCE2, T_FIFTH2, T_WRONG2 = ls("fifth"), wd("fifth", "fifth"), wd("fifth", "once"), wd("fifth", "fifth", 1), wd("fifth", "wrong")
T_GUESS0, T_QUIZ, T_GUESSED, T_75 = ls("guess"), wd("guess", "quiz"), wd("guess", "guessed"), wd("guess", "seventyfive")
T_IDK0, T_KNOW, T_26, T_OFTEN = ls("idk"), wd("idk", "know"), wd("idk", "twentysix"), wd("idk", "often")
T_PATH0 = ls("path")
PATTERN = np.column_stack([np.linspace(260, 860, 900), 560 - 160 * np.sin(np.linspace(0, math.pi, 900))]) + RNG.normal(0, 7, (900, 2))
WRONG_DATES = ["03-07", "15-06", "01-01"]
ONCE_SET = set(RNG.choice(100, 20, replace=False).tolist())


def now(c, t):
    a = win(t, T_FLU0 - 0.05, T_PATH0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kf = part(t, T_FLU0, T_ONCE0)
        if kf > 0:                                                          # fluent by design / right takes more
            with layer(c, kf):
                xs = np.linspace(260, 860, 200)
                stroke_polys(c, [np.column_stack([xs, 520 + 60 * np.sin((xs - 260) / 60 + 2 * t)])], GLOW, 3.0, ease(seg(t, T_FLUENT - 0.3, T_FLUENT + 0.3)))
                label(c, "FLUENT: BY DESIGN", 560, 700, t, T_FLUENT - 0.1, 28, GLOW, a=a * kf)
                kt = ease(seg(t, T_RIGHT - 0.2, T_RIGHT + 1.6))
                stroke_polys(c, tick_mark(1360, 520, 110), WHITE, 3.0, 0.25)
                if kt > 0:
                    q = tick_mark(1360, 520, 110)[0]
                    stroke_polys(c, [q[:2] if kt < 0.5 else q], WHITE, 3.4, kt)
                label(c, "RIGHT: TAKES MORE", 1360, 700, t, T_RIGHT - 0.1, 28, WHITE, a=a * kf)
                ev(T_FLUENT - 0.3, "form", t, 560)
        ko = part(t, T_ONCE0, T_BD0)
        if ko > 0:                                                          # thousands of times: a pattern; once: none
            with layer(c, ko):
                n = int(len(PATTERN) * ease(seg(t, T_THOUSANDS - 0.4, T_CARRIES)))
                points(c, PATTERN[:n], 0.8, GLOW, 2.4)
                stroke_polys(c, [np.column_stack([np.linspace(260, 860, 60), 560 - 160 * np.sin(np.linspace(0, math.pi, 60))])], WHITE, 2.0,
                             ease(seg(t, T_CARRIES - 0.2, T_CARRIES + 0.4)))
                label(c, "SEEN THOUSANDS OF TIMES", 560, 700, t, T_THOUSANDS - 0.2, 22, GLOW, a=a * ko)
                label(c, "THE PATTERN CARRIES IT", 560, 750, t, T_CARRIES - 0.1, 20, WHITE, a=a * ko)
                if t >= T_ONCE - 0.3:
                    c.drawCircle(1360, 480, 9, mg.fill(GOLD, a * ko))
                    burst(c, 1360, 480, t, T_ONCE - 0.1, 40)
                    stroke_polys(c, [ellipse(1360, 480, 120, 120, 0, 360, 60)], SOFT, 1.4, 0.6 * ease(seg(t, T_ONCE, T_ONCE + 0.5)))
                    label(c, "SEEN ONCE", 1360, 700, t, T_ONCE - 0.1, 22, GOLD, a=a * ko)
                    label(c, "NO PATTERN TO KEEP", 1360, 750, t, T_ONCE + 0.5, 20, WHITE, a=a * ko)
                    ev(T_ONCE - 0.1, "pop", t, 1360)
        kb = part(t, T_BD0, T_FIFTH0)
        if kb > 0:                                                          # three tries, three wrong birthdays
            with layer(c, kb):
                lines_in(c, [rect(360, 220, 1200, 150)], t, T_BD0 + 0.1, 0.5, WHITE, 1.8)
                label(c, "WHAT IS A CO-AUTHOR'S BIRTHDAY?", 400, 285, t, T_BIRTHDAY - 0.5, 26, WHITE, "left", a=a * kb, cps=36)
                label(c, "IF YOU KNOW, JUST RESPOND WITH DD-MM.", 400, 335, t, T_KNEW - 0.6, 22, GLOW, "left", a=a * kb, cps=40)
                for i, d in enumerate(WRONG_DATES):
                    tk = wd("birthday", "three") - 0.2 + 0.45 * i
                    if t < tk:
                        continue
                    x = 540 + 420 * i
                    bignum(c, t, d, 70, x, 590, tk)
                    stroke_polys(c, cross(x, 570, 80), GOLD, 3.0, ease(seg(t, T_DATES - 0.4 + 0.15 * i, T_DATES + 0.15 * i)))
                    label(c, f"TRY {i + 1}", x, 700, t, tk + 0.1, 20, SOFT, a=a * kb)
                    ev(T_DATES - 0.4 + 0.15 * i, "clack", t, x)
                label(c, "THREE TRIES · THREE DIFFERENT WRONG DATES", CX, 800, t, T_DATES - 0.2, 24, WHITE, a=a * kb)
        kx = part(t, T_FIFTH0, T_GUESS0)
        if kx > 0:                                                          # a hundred facts, a fifth seen once, a fifth wrong
            with layer(c, kx):
                for i in range(100):
                    x, y = 610 + (i % 10) * 70, 180 + (i // 10) * 58
                    once = i in ONCE_SET
                    lit = once and t >= T_ONCE2 - 0.3
                    c.drawRect(skia.Rect.MakeXYWH(x, y, 46, 40), mg.stroke(GOLD if lit else SOFT, 1.6 if lit else 1.0, (0.95 if lit else 0.5) * a * kx))
                    if once:
                        kc = ease(seg(t, T_WRONG2 - 0.5 + 0.02 * (i % 10), T_WRONG2 - 0.1 + 0.02 * (i % 10)))
                        if kc > 0:
                            stroke_polys(c, cross(x + 23, y + 20, 14), GOLD, 2.4, kc)
                label(c, "100 FACTS", 560, 220, t, T_FIFTH - 0.3, 22, SOFT, "right", a=a * kx)
                label(c, "20 SEEN ONCE IN TRAINING", 560, 420, t, T_ONCE2 - 0.2, 22, GOLD, "right", a=a * kx)
                label(c, "EXPECT AT LEAST 20 WRONG", 560, 620, t, T_WRONG2 - 0.3, 22, WHITE, "right", a=a * kx)
                label(c, "THE RAW MODEL, BEFORE FINE-TUNING · KALAI ET AL., OPENAI, 2025", CX, 815, t, T_FIFTH2, 18, SOFT, a=a * kx)
                ev(T_ONCE2 - 0.3, "grains", t, 960)
        if t >= T_GUESS0 - 0.2:                                             # two quiz bars
            kq = ease(seg(t, T_GUESS0 - 0.2, T_GUESS0 + 0.3))
            with layer(c, kq):
                label(c, "ONE QUIZ (SIMPLEQA) · OPENAI, 2025", CX, 235, t, T_QUIZ - 0.2, 22, SOFT, a=a * kq)
                ka = seg(t, T_GUESSED - 0.4, T_75 + 0.3)
                label(c, "NEARLY ALWAYS GUESSED", 300, 330, t, T_GUESSED - 0.4, 22, WHITE, "left", a=a * kq)
                bar(c, 300, 350, 1320, 70, [(0.24, WHITE, True), (0.75, GOLD, True), (0.01, SOFT, False)], ka, a * kq)
                label(c, "24% RIGHT", 300, 460, t, T_GUESSED, 20, WHITE, "left", a=a * kq)
                label(c, "75% WRONG", 1620, 460, t, T_75 - 0.2, 24, GOLD, "right", a=a * kq)
                ev(T_GUESSED - 0.4, "swell", t, 900)
                if t >= T_IDK0 - 0.2:
                    kb2 = seg(t, T_KNOW - 0.3, T_26 + 0.3)
                    label(c, "SAID \"I DON'T KNOW\" HALF THE TIME", 300, 600, t, T_IDK0, 22, WHITE, "left", a=a * kq)
                    bar(c, 300, 620, 1320, 70, [(0.22, WHITE, True), (0.26, GOLD, True), (0.52, SOFT, False)], kb2, a * kq)
                    label(c, "22% RIGHT", 300, 730, t, T_OFTEN - 0.5, 20, WHITE, "left", a=a * kq)
                    label(c, "26% WRONG", 300 + 1320 * 0.35, 730, t, T_26 - 0.2, 24, GOLD, "center", a=a * kq)
                    label(c, "52% \"I DON'T KNOW\"", 1620, 730, t, T_KNOW, 20, SOFT, "right", a=a * kq)
                    ev(T_KNOW - 0.3, "swell", t, 900)
                label(c, "TESTS REWARD A CONFIDENT GUESS", CX, 180, t, wd("guess", "reward") - 0.2, 26, WHITE, a=a * kq)


# ---------------------------------------------------------------- IDEA
T_TRUE, T_FINDP, T_MODEL, T_LIKELY = wd("path", "true"), wd("path", "find"), wd("path", "model"), wd("path", "likely")
T_LIK0, T_ISNT, T_FINDING, T_CHECKING = ls("likely"), wd("likely", "true"), wd("likely", "finding"), wd("likely", "checking")
T_IMAG0 = ls("imagine")
FIELD = [(x, y) for x in range(150, 1800, 64) for y in range(170, 900, 52)]
WALK = np.cumsum(np.column_stack([np.full(90, 15.0), RNG.normal(0, 34, 90)]), 0) + (180, 540)


def idea(c, t):
    a = win(t, T_PATH0 - 0.05, T_IMAG0 + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kp = part(t, T_PATH0, T_LIK0)
        if kp > 0:                                                          # a path through the nonsense; a straight line
            with layer(c, kp):
                seed = 7
                for i, (x, y) in enumerate(FIELD[::2]):
                    label(c, gib(2, seed + i), x, y, t, -1, 16, SOFT, a=a * kp * 0.35)
                kw = ease(seg(t, T_PATH0 + 0.2, T_FINDP + 0.2))
                n = max(2, int(len(WALK) * kw))
                stroke_polys(c, [WALK[:n]], GOLD, 2.0, 0.9)
                label(c, "EVERY TRUE PAGE · NO WAY TO FIND IT", 180, 230, t, T_TRUE - 0.3, 22, GOLD, "left", a=a * kp)
                if t >= T_MODEL - 0.3:
                    lines_in(c, chip(300, 730, 60), t, T_MODEL - 0.3, 0.4, WHITE, 1.8)
                    k = ease(seg(t, T_LIKELY - 0.5, T_LIKELY))
                    c.drawLine(360, 730, lerp(360, 1500, k), lerp(730, 700, k), mg.stroke(GLOW, 3.0, a * kp))
                    lines_in(c, page(1510, 620, 120, 150), t, T_LIKELY - 0.1, 0.4, WHITE, 2.0)
                    label(c, "A LIKELY PAGE · AT ONCE", 1570, 815, t, T_LIKELY, 22, GLOW, a=a * kp)
                    ev(T_LIKELY - 0.5, "whoosh", t, 900)
        if t >= T_LIK0 - 0.2:                                               # likely isn't true; finding / checking
            kl = ease(seg(t, T_LIK0 - 0.2, T_LIK0 + 0.3))
            with layer(c, kl):
                label(c, "LIKELY ≠ TRUE", CX, 260, t, T_ISNT - 0.3, 44, WHITE, a=a * kl, cps=24)
                lines_in(c, chip(620, 560, 110), t, T_FINDING - 0.3, 0.5, WHITE, 1.9)
                label(c, "FINDING: THE MACHINE", 620, 780, t, T_FINDING - 0.1, 24, GLOW, a=a * kl)
                body, _ = figure(1300, 640, 300, STAND, -1)
                lines_in(c, body, t, T_CHECKING - 0.4, 0.5, WHITE, 1.8)
                lines_in(c, tick_mark(1440, 480, 50), t, T_CHECKING, 0.4, GLOW, 3.0)
                label(c, "CHECKING: STILL OURS", 1300, 780, t, T_CHECKING - 0.1, 24, WHITE, a=a * kl)
                ev(T_CHECKING, "confirm", t, 1300)


# ---------------------------------------------------------------- IMAGINE
T_LIBRARIAN, T_CHILD = wd("imagine", "librarian"), wd("imagine", "child")
T_WHATIF = ls("whatif")
T_BLOOM0, T_BLOOM, T_TUTOR, T_98, T_COSTLY = ls("bloom"), wd("bloom", "bloom"), wd("bloom", "tutoring"), wd("bloom", "ninetyeight"), wd("bloom", "costly")
T_NIG0, T_NIGERIA, T_WEEKS, T_TUTOR2, T_YEARS = ls("nigeria"), wd("nigeria", "nigeria"), wd("nigeria", "weeks"), wd("nigeria", "tutor"), wd("nigeria", "years")
T_Q0, T_SCHOOL = ls("question"), wd("question", "school")
T_THEN = ls("then")
SIT = dict(lean=0, head=4, ls=40, le=50, rs=40, re=50, lh=80, lk=-80, rh=80, rk=-80)


def imagine(c, t):
    a = win(t, T_IMAG0 - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        ki = part(t, T_IMAG0, T_BLOOM0)
        if ki > 0:                                                          # a librarian beside a child; beside every child
            with layer(c, ki):
                kz = ease(seg(t, T_CHILD - 0.3, T_CHILD + 0.9))
                s = lerp(1.0, 0.42, kz)
                floor = lerp(780, 680, kz)
                cx0 = lerp(CX, 260, kz)
                for j in range(1 if kz <= 0 else 9):
                    x = cx0 + j * 175
                    if j and t < T_CHILD - 0.2 + 0.08 * j:
                        continue
                    adult, _ = figure(x - 90 * s, floor - 0.48 * 420 * s, 420 * s, STAND, 1)
                    kid, _ = figure(x + 70 * s, floor - 0.48 * 260 * s, 260 * s, STAND, -1)
                    stroke_polys(c, adult, GLOW, 1.8, 1.0)
                    stroke_polys(c, kid, WHITE, 1.8, 1.0)
                    if j == 0:
                        ev(T_IMAG0 + 0.2, "form", t, x)
                label(c, "A LIBRARIAN WHO HAS READ EVERY SHELF", CX, 220, t, T_LIBRARIAN - 0.1, 24, WHITE, a=a * ki)
                label(c, "BESIDE EVERY CHILD ON EARTH", CX, 820, t, T_CHILD - 0.1, 24, GLOW, a=a * ki)
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 160, t, T_WHATIF + 0.05, 22, GLOW, a=a * ki * ease(seg(t, T_WHATIF, T_WHATIF + 0.3)))
                ev(T_CHILD - 0.2, "grains", t, CX)
        kb = part(t, T_BLOOM0, T_NIG0)
        if kb > 0:                                                          # Bloom's two bell curves
            with layer(c, kb):
                x0, x1, sd = 260, 1660, 150
                mu0, mu1 = 700, 700 + 2 * sd
                c.drawLine(x0, 760, x1, 760, mg.stroke(SOFT, 1.4, a * kb))
                lines_in(c, [bell(x0, x1, mu0, sd, 380, 380)], t, T_BLOOM0 + 0.3, 0.8, WHITE, 2.2, seed_pt=(mu0, 380))
                label(c, "A NORMAL CLASS", mu0, 350, t, T_BLOOM0 + 0.6, 20, WHITE, a=a * kb)
                if t >= T_TUTOR - 0.3:
                    k = ease(seg(t, T_TUTOR - 0.3, T_TUTOR + 0.9))
                    stroke_polys(c, [bell(x0, x1, lerp(mu0, mu1, k), sd, 380, 380)], GLOW, 2.6, 1.0)
                    label(c, "TUTORED ONE TO ONE", lerp(mu0, mu1, k) + 40, 350, t, T_TUTOR, 20, GLOW, "left", a=a * kb)
                    ev(T_TUTOR - 0.3, "whoosh", t, mu1)
                if t >= T_98 - 0.6:
                    kk = ease(seg(t, T_98 - 0.6, T_98 + 0.4))
                    xs = np.linspace(x0, mu1, 80)
                    ys = 760 - 380 * np.exp(-0.5 * ((xs - mu0) / sd) ** 2)
                    path = skia.Path()
                    path.moveTo(x0, 760)
                    for xx, yy in zip(xs, ys):
                        path.lineTo(float(xx), float(yy))
                    path.lineTo(mu1, 760)
                    path.close()
                    c.drawPath(path, mg.fill(GLOW, 0.22 * kk * a * kb))
                    c.drawLine(mu1, 360, mu1, 760, mg.stroke(GLOW, 2.0, kk * a * kb))
                    bignum(c, t, "98%", 110, 1380, 250, T_98 - 0.4)
                    label(c, "OF THE CLASS BELOW THE AVERAGE TUTORED STUDENT", CX, 820, t, T_98, 20, SOFT, a=a * kb * (1 - ease(seg(t, T_COSTLY - 0.4, T_COSTLY - 0.1))))
                label(c, "BENJAMIN BLOOM · 1984", 260, 250, t, T_BLOOM - 0.1, 22, SOFT, "left", a=a * kb)
                label(c, "TOO COSTLY FOR EVERYONE", CX, 820, t, T_COSTLY - 0.1, 24, WHITE, a=a * kb)
        kn = part(t, T_NIG0, T_Q0)
        if kn > 0:                                                          # six weeks; one and a half to two years of school
            with layer(c, kn):
                label(c, "WORLD BANK TRIAL · NIGERIA · 2024 · AFTER SCHOOL, WITH AN AI TUTOR", CX, 220, t, T_NIGERIA - 0.2, 20, SOFT, a=a * kn)
                wk = 21.0                                                   # pixels a week
                k6 = ease(seg(t, T_WEEKS - 0.5, T_WEEKS + 0.3))
                c.drawRect(skia.Rect.MakeXYWH(260, 400, 6 * wk * k6, 60), mg.chrome_paint(400, 460, 0.95))
                for j in range(1, 7):
                    if k6 >= j / 6:
                        c.drawLine(260 + j * wk, 400, 260 + j * wk, 460, mg.stroke(WHITE, 1.2, 0.7 * a * kn))
                label(c, "6 WEEKS", 260, 380, t, T_WEEKS - 0.3, 26, WHITE, "left", a=a * kn)
                ky = ease(seg(t, T_YEARS - 1.4, T_YEARS + 0.4))
                yr = 36 * wk                                                # a school year of about 36 weeks
                c.drawRect(skia.Rect.MakeXYWH(260, 620, 1.5 * yr * ky, 60), mg.fill(GLOW, 0.85 * a * kn))
                c.drawRect(skia.Rect.MakeXYWH(260 + 1.5 * yr * ky, 620, 0.5 * yr * ky, 60), mg.stroke(GLOW, 1.8, 0.9 * a * kn))
                label(c, "≈ 1.5 TO 2 YEARS OF NORMAL SCHOOL (THE RESEARCHERS' ESTIMATE)", 260, 600, t, T_YEARS - 1.2, 22, GLOW, "left", a=a * kn)
                ev(T_YEARS - 1.4, "riser", t, 900)
        if t >= T_Q0 - 0.2:                                                 # what would school be for?
            kq = ease(seg(t, T_Q0 - 0.2, T_Q0 + 0.3))
            with layer(c, kq):
                lines_in(c, school(CX, 660, 260), t, T_Q0, 0.7, WHITE, 1.9, seed_pt=(CX, 660))
                label(c, "WHAT WOULD SCHOOL BE FOR?", CX, 790, t, T_SCHOOL - 0.4, 30, GLOW, a=a * kq)
                ev(T_Q0, "form", t, CX)


# ---------------------------------------------------------------- SURFACE
T_BOOKB, T_NEED = wd("then", "book"), wd("then", "need")
T_NOW0, T_ASK, T_PROMISE = ls("now2"), wd("now2", "page"), wd("now2", "promise")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "J. L. Borges, The Library of Babel, 1941: 410 pages, 25 symbols; 25^1,312,000 books (1,834,098 digits; 4.7 km at 10 per inch)",
           "Meta, Introducing Llama 3 (Apr 2024): 15T+ tokens · 70B parameters ≈ 140 GB at 16 bits · Shannon, 1951",
           "Delétang et al. (DeepMind), Language Modeling Is Compression, ICLR 2024",
           "Kalai, Nachum, Vempala, Zhang, Why Language Models Hallucinate (OpenAI, Sep 2025); SimpleQA figures from OpenAI",
           "Bloom, The 2 Sigma Problem, 1984 · De Simone et al., From Chalkboards to Chatbots, World Bank WP 11125, 2025",
           "The section on a librarian beside every child is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 760)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 760))
            cs = [(x, y) for x, y in comb_centres(520, 450, 70, 3, 3) if 120 < x < 900 and 160 < y < 720]
            stroke_polys(c, [hexagon(x, y, 66) for x, y in cs], SOFT, 1.3, ease(seg(t, T_THEN, T_THEN + 0.6)))
            label(c, "EVERY BOOK", 520, 780, t, T_BOOKB - 0.3, 22, GLOW, a=a)
            label(c, "NO WAY TO FIND THE ONE YOU NEED", 520, 815, t, T_NEED - 0.4, 18, SOFT, a=a)
            if t >= T_NOW0 - 0.05:
                lines_in(c, page(1300, 330, 240, 300), t, T_NOW0, 0.5, WHITE, 2.0)
                lines_in(c, qmark(1420, 470, 110), t, T_PROMISE - 0.2, 0.5, GLOW, 2.4)
                label(c, "THE PAGE YOU ASK FOR", 1420, 780, t, T_ASK - 0.3, 22, GLOW, a=a)
                label(c, "NO PROMISE IT'S TRUE", 1420, 815, t, T_PROMISE - 0.2, 18, SOFT, a=a)
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
