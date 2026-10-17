"""EP06 · WHO'S HUMAN HERE? the scenes: line art keyed to the script's line ids and George's words (engine.tl.word),
which the engine turns into characters.

  GROUND     two chat windows side by side, messages arriving, a five-minute clock; pick the human; a cursor picks
             B (the AI); 73% against 27%; a question mark
  MECHANISM  1950: the imitation game (a judge, a wall, a person and a machine behind it); a timeline with Turing's
             30% bar at 2000 and 73% at 2025; a persona card (young, introverted, internet culture) doubling 36% to
             73%; small-talk bubbles
  NOW        100 visits: 53 robot heads, 47 people; the checkbox "Verify you are human" and a cursor clicking it; the
             agent's own note, typed; a phone, a voice copied, a key: a secret word
  IDEA       machine -> person?, then the arrow turns round: person -> prove it; "the default" becomes "a claim"
  IMAGINE    a dotted 2030; a voice that could be synthetic; a key, a second channel, two people meeting; who can you
             trust?
  SURFACE    1950: the test was for the machine | 2026: it's for us; the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, MID, SOFT, ease, seg, lerp, win, layer, P, ellipse, rect, lines_in,  # noqa: E402
                         closed_fill, stroke_polys, bignum, figure, STAND, keys, morph_polys, dotted_num, roll, burst)

GROUND_Y = 800
TRAILS = []
GLINTS = []


# ---------------------------------------------------------------- things
def window(x, y, w, h, title_h=34):
    return [mg.rrect_pts(x, y, w, h, 14, 5), P([(x, y + title_h), (x + w, y + title_h)]),
            ellipse(x + 20, y + title_h / 2, 5, 5, 0, 360, 12), ellipse(x + 38, y + title_h / 2, 5, 5, 0, 360, 12)]


def bubble(x, y, w, h=34, right=False):
    q = mg.rrect_pts(x, y, w, h, 14, 4)
    tail = P([(x + (w - 18 if right else 18), y + h), (x + (w - 8 if right else 8), y + h + 12), (x + (w - 30 if right else 30), y + h)])
    return [q, tail]


def cursor(x, y, s=1.0):
    pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (27, 24), (0, 0)]
    return [P([(x + px * s, y + py * s) for px, py in pts])]


def checkbox(x, y, w=520, h=86):
    return [mg.rrect_pts(x, y, w, h, 8, 4), mg.rrect_pts(x + 26, y + h / 2 - 18, 36, 36, 5, 3)]


def check(x, y, k=1.0):
    pts = np.array([(x + 34, y + 44), (x + 42, y + 54), (x + 58, y + 30)])
    if k >= 1:
        return [P(pts)]
    L1 = np.linalg.norm(pts[1] - pts[0]); L2 = np.linalg.norm(pts[2] - pts[1])
    d = k * (L1 + L2)
    if d <= L1:
        return [P([pts[0], pts[0] + (pts[1] - pts[0]) * d / L1])]
    return [P([pts[0], pts[1], pts[1] + (pts[2] - pts[1]) * (d - L1) / L2])]


def robot_head(cx, cy, s):
    return [mg.rrect_pts(cx - s / 2, cy - s / 2, s, 0.9 * s, 0.15 * s, 3), P([(cx, cy - s / 2), (cx, cy - 0.75 * s)]),
            ellipse(cx, cy - 0.8 * s, 0.07 * s, 0.07 * s, 0, 360, 8), P([(cx - 0.25 * s, cy - 0.05 * s), (cx - 0.1 * s, cy - 0.05 * s)]),
            P([(cx + 0.1 * s, cy - 0.05 * s), (cx + 0.25 * s, cy - 0.05 * s)])]


def person_head(cx, cy, s):
    return [ellipse(cx, cy - 0.15 * s, 0.28 * s, 0.3 * s, 0, 360, 20), ellipse(cx, cy + 0.55 * s, 0.45 * s, 0.3 * s, 180, 360, 20)]


def computer(cx, bot, s):
    """A 1950s-ish machine: a cabinet with dials and a paper slot."""
    x0, y0 = cx - 0.5 * s, bot - s
    out = [rect(x0, y0, s, s), P([(x0 + 0.1 * s, y0 + 0.2 * s), (x0 + 0.9 * s, y0 + 0.2 * s)])]
    for k in range(3):
        out.append(ellipse(x0 + (0.22 + 0.28 * k) * s, y0 + 0.45 * s, 0.08 * s, 0.08 * s, 0, 360, 16))
    for k in range(4):
        out.append(P([(x0 + 0.15 * s, y0 + (0.66 + 0.07 * k) * s), (x0 + 0.85 * s, y0 + (0.66 + 0.07 * k) * s)]))
    return out


def desk(cx, bot, w):
    return [P([(cx - w / 2, bot - 0.35 * w), (cx + w / 2, bot - 0.35 * w)]), P([(cx - 0.42 * w, bot - 0.35 * w), (cx - 0.42 * w, bot)]),
            P([(cx + 0.42 * w, bot - 0.35 * w), (cx + 0.42 * w, bot)])]


def phone(cx, cy, s):
    return [mg.rrect_pts(cx - 0.5 * s, cy - s, s, 2 * s, 0.14 * s, 5), P([(cx - 0.12 * s, cy - 0.88 * s), (cx + 0.12 * s, cy - 0.88 * s)]),
            ellipse(cx, cy + 0.86 * s, 0.07 * s, 0.07 * s, 0, 360, 12)]


def wave(cx, cy, w, h, t, n=24, dotted=False):
    out = []
    for k in range(n):
        x = cx - w / 2 + (k + 0.5) * w / n
        a = h * (0.25 + 0.75 * abs(math.sin(k * 0.9 + t * 7) * math.sin(k * 0.37 + t * 3.1)))
        if dotted and k % 2:
            continue
        out.append(P([(x, cy - a / 2), (x, cy + a / 2)]))
    return out


def key(cx, cy, s):
    return [ellipse(cx - 0.55 * s, cy, 0.32 * s, 0.32 * s, 0, 360, 28), ellipse(cx - 0.55 * s, cy, 0.12 * s, 0.12 * s, 0, 360, 14),
            P([(cx - 0.23 * s, cy), (cx + 0.75 * s, cy)]), P([(cx + 0.45 * s, cy), (cx + 0.45 * s, cy + 0.22 * s)]),
            P([(cx + 0.65 * s, cy), (cx + 0.65 * s, cy + 0.3 * s)])]


def arrow(x0, y0, x1, y1, head=18):
    ang = math.atan2(y1 - y0, x1 - x0)
    return [P([(x0, y0), (x1, y1)]), P([(x1 - head * math.cos(ang - 0.45), y1 - head * math.sin(ang - 0.45)), (x1, y1),
                                        (x1 - head * math.cos(ang + 0.45), y1 - head * math.sin(ang + 0.45))])]


def bars(c, t, items, x0, y0, w, t0, a=1.0):
    """Horizontal bars (label, fraction, colour, when), growing in."""
    for k, (lab, f, col, tk) in enumerate(items):
        if t < tk:
            continue
        y = y0 + k * 110
        ww = w * f * ease(seg(t, tk, tk + 0.5))
        c.drawRect(skia.Rect.MakeXYWH(x0, y, ww, 50), mg.chrome_paint(y, y + 50, 0.9) if col == "chrome" else mg.fill(col, 0.95 * a))
        c.drawRect(skia.Rect.MakeXYWH(x0, y, w, 50), mg.stroke(SOFT, 1.2, 0.6 * a))
        label(c, lab, x0, y - 16, t, tk, 20, WHITE, "left", a=a)
        ev(tk, "tick", t, x0 + ww)


# ---------------------------------------------------------------- GROUND
T_284, T_CHAT, T_5, T_PERSON, T_AI = wd("setup", "two"), wd("setup", "chat"), wd("setup", "five"), wd("setup", "person."), wd("setup", "AI.")
T_JOB, T_PICK = ls("job"), wd("job", "pick")
T_RES, T_73 = ls("result"), wd("result", "seventy-three")
T_MORE = ls("more")
T_HOW, T_TELL = ls("how"), wd("how", "tell?")
T_TUR = ls("turing")
WA, WB = (430, 250, 480, 470), (1010, 250, 480, 470)
MSGS = [(0, 1.9, 300, False), (1, 2.4, 240, True), (0, 3.2, 200, True), (1, 3.9, 320, False), (0, 4.8, 260, False), (1, 5.5, 180, True),
        (0, 6.4, 330, True), (1, 7.0, 220, False)]


def chats(c, t):
    a = win(t, 1.2, T_TUR + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kh = 1 - ease(seg(t, T_MORE - 0.2, T_MORE + 0.2))
        with layer(c, kh):
            for k, (x, y, w, h) in enumerate((WA, WB)):
                lines_in(c, window(x, y, w, h), t, 1.3 + 0.15 * k, 0.6, WHITE, 1.8, seed_pt=(x + w / 2, y + h + 100))
                label(c, "A" if k == 0 else "B", x + w - 30, y + 24, t, 1.9, 20, GLOW, a=a * kh)
        ev(1.3, "form", t, CX)
        with layer(c, kh):
            rows = [0, 0]
            for w_i, t_i, bw, right in MSGS:
                if t < t_i:
                    continue
                x, y, w, h = (WA, WB)[w_i]
                r = rows[w_i]; rows[w_i] += 1
                bx = x + w - bw - 24 if right else x + 24
                by = y + 56 + r * 64
                if by > y + h - 60:
                    continue
                stroke_polys(c, bubble(bx, by, bw, 34, right), GLOW if right else WHITE, 1.6, ease(seg(t, t_i, t_i + 0.2)))
                ev(t_i, "pop", t, x + w / 2)
            label(c, "284 PEOPLE · FIVE MINUTES · TWO CHATS AT ONCE", CX, 190, t, T_284 + 0.2, 22, WHITE, a=a * kh * (1 - ease(seg(t, T_JOB - 0.2, T_JOB + 0.1))))
            if t >= T_5:                                                   # the five-minute clock
                rem = max(0.0, 300 - (t - T_5) * 40)
                label(c, f"{int(rem // 60)}:{int(rem % 60):02d}", CX, 790, t, -1, 30, GLOW, a=a * kh)
            label(c, "ONE IS A PERSON · ONE IS AN AI", CX, 845, t, T_PERSON - 0.3, 20, SOFT, a=a * kh)
            if t >= T_JOB - 0.1:                                           # pick the human: a cursor, then B
                cx_ = keys(t, [(T_JOB, CX), (T_PICK + 0.3, 700), (T_RES - 0.2, 1240), (T_73, 1250)])
                cy_ = keys(t, [(T_JOB, 820), (T_PICK + 0.3, 520), (T_RES - 0.2, 480), (T_73, 470)])
                stroke_polys(c, cursor(cx_, cy_), WHITE, 2.0, 1.0)
                closed_fill(c, cursor(cx_, cy_), 1.0, mg.fill(WHITE, 0.9))
                label(c, "PICK THE HUMAN", CX, 190, t, T_PICK, 24, WHITE, a=a * (1 - ease(seg(t, T_RES - 0.1, T_RES + 0.2))))
                if t >= T_73 - 0.1:
                    x, y, w, h = WB
                    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 8, y - 8, w + 16, h + 16), 18, 18), mg.stroke(GLOW, 3.0, ease(seg(t, T_73 - 0.1, T_73 + 0.2))))
                    burst(c, cx_, cy_, t, T_73, 40)
                    ev(T_73, "confirm", t, 1250)
        if t >= T_RES:
            with layer(c, kh):
                bignum(c, t, "73%", 130, CX, 180 - 30 + 30, T_73 - 0.1)
                label(c, "CHOSE B: THE AI (GPT-4.5)", CX, 280 - 20, t, T_73 + 0.4, 22, GLOW, a=a * kh)
        if t >= T_MORE - 0.1:                                              # more often than the real person
            km = win(t, T_MORE - 0.1, T_TUR + 0.1, 0.3, 0.4)
            with layer(c, km):
                bars(c, t, [("PICKED THE AI AS THE HUMAN · 73%", 0.73, "chrome", T_MORE), ("PICKED THE REAL PERSON · 27%", 0.27, GLOW, T_MORE + 0.5)],
                     460, 420, 1000, T_MORE, a)
                if t >= T_TELL - 0.25:
                    bignum(c, t, "?", 150, CX, 740, T_TELL - 0.25)


# ---------------------------------------------------------------- MECHANISM
T_1950, T_MACH, T_PERS, T_WHICH = wd("turing", "nineteen"), wd("turing", "machine"), wd("turing", "person,"), wd("turing", "which", 1)
T_PRED, T_2000, T_30 = ls("predict"), wd("predict", "two"), wd("predict", "thirty")
T_LATE, T_25, T_FURTHER = ls("late"), wd("late", "twenty-five"), wd("late", "further.")
T_PERSONA, T_TOLD, T_INTRO, T_INTERNET, T_DOUBLED = ls("persona"), wd("persona", "Told"), wd("persona", "introverted"), wd("persona", "internet"), wd("persona", "doubled.")
T_GUT, T_SMALL, T_GUTW = ls("gut"), wd("gut", "small"), wd("gut", "gut.")
T_BOTS = ls("bots")
AX0, AX1, AXY = 360, 1560, 640
yx = lambda yr: AX0 + (AX1 - AX0) * (yr - 1950) / (2026 - 1950)


def imitation(c, t):
    a = win(t, T_TUR - 0.05, T_BOTS + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kd = 1 - ease(seg(t, T_PRED - 0.2, T_PRED + 0.3))
        if kd > 0:                                                         # the imitation game
            with layer(c, kd):
                bignum(c, t, "1950", 130, CX, 210, T_1950)
                label(c, "ALAN TURING · THE IMITATION GAME", CX, 305, t, wd("turing", "Alan"), 22, SOFT, a=a * kd)
                body_polys, _ = figure(470, GROUND_Y - 0.48 * 300, 300, dict(STAND, ls=60, le=40, rs=50, re=45), 1)
                lines_in(c, body_polys + desk(560, GROUND_Y, 220), t, T_TUR + 0.5, 0.7, GLOW, 1.7)
                label(c, "THE JUDGE", 470, 850 - 20, t, T_TUR + 0.9, 20, SOFT, a=a * kd)
                lines_in(c, [P([(CX + 60, 360), (CX + 60, GROUND_Y)])], t, T_TUR + 0.8, 0.5, SOFT, 2.4)
                if t >= T_MACH - 0.1:
                    lines_in(c, computer(1300, GROUND_Y, 190), t, T_MACH - 0.1, 0.5, WHITE, 1.8)
                    ev(T_MACH - 0.1, "form", t, 1300)
                if t >= T_PERS - 0.1:
                    pp, _ = figure(1560, GROUND_Y - 0.48 * 300, 300, STAND, -1)
                    lines_in(c, pp, t, T_PERS - 0.1, 0.5, GLOW, 1.7)
                    ev(T_PERS - 0.1, "form", t, 1560)
                if t >= T_WHICH - 0.3:
                    bignum(c, t, "?", 120, CX + 60, 300 + 20, T_WHICH - 0.3, fill=False)
                for yy in (520, 600):
                    c.drawLine(640, yy, CX + 40, yy, mg.stroke(SOFT, 1.2, 0.6 * ease(seg(t, T_TUR + 1.2, T_TUR + 1.6))))
        kt = win(t, T_PRED - 0.1, T_PERSONA + 0.3, 0.3, 0.4)               # Turing's bar, and 2025
        if kt > 0:
            with layer(c, kt):
                lines_in(c, [P([(AX0, AXY), (AX1, AXY)])], t, T_PRED, 0.5, SOFT, 1.6, seed_pt=(AX0, AXY))
                for yr in (1950, 2000, 2025):
                    x = yx(yr)
                    c.drawLine(x, AXY - 12, x, AXY + 12, mg.stroke(SOFT, 1.6, kt))
                    label(c, str(yr), x, AXY + 44, t, T_PRED + 0.2, 20, SOFT, a=kt)
                if t >= T_2000 - 0.1:
                    h30 = 300 * 0.30 * ease(seg(t, T_30 - 0.2, T_30 + 0.4))
                    c.drawRect(skia.Rect.MakeXYWH(yx(2000) - 30, AXY - h30, 60, h30), mg.fill(GLOW, 0.95))
                    label(c, "TURING'S BAR: 30%", yx(2000), AXY - h30 - 22, t, T_30, 20, GLOW, a=kt)
                    ev(T_30, "tick", t, yx(2000))
                if t >= T_25 - 0.2:
                    for p in arrow(yx(2000) + 40, AXY - 150, yx(2025) - 40, AXY - 150, 16):
                        stroke_polys(c, [p], WHITE, 1.8, ease(seg(t, T_25 - 0.2, T_25 + 0.3)))
                    label(c, "25 YEARS LATER", (yx(2000) + yx(2025)) / 2, AXY - 172, t, T_25, 20, WHITE, a=kt)
                if t >= T_FURTHER - 0.3:
                    h73 = 300 * 0.73 * ease(seg(t, T_FURTHER - 0.3, T_FURTHER + 0.4))
                    c.drawRect(skia.Rect.MakeXYWH(yx(2025) - 30, AXY - h73, 60, h73), mg.chrome_paint(AXY - h73, AXY, 0.95))
                    label(c, "2025: 73%", yx(2025), AXY - h73 - 22, t, T_FURTHER, 22, WHITE, a=kt)
                    ev(T_FURTHER - 0.3, "zoom", t, yx(2025))
        kp = win(t, T_PERSONA - 0.1, T_BOTS + 0.2, 0.3, 0.5)              # the persona
        if kp > 0:
            with layer(c, kp):
                kcard = 1 - ease(seg(t, T_GUT - 0.3, T_GUT + 0.1))
                with layer(c, kcard):
                    lines_in(c, [mg.rrect_pts(400, 280, 420, 400, 16, 5)], t, T_TOLD - 0.2, 0.5, WHITE, 1.8)
                    ph, _ = figure(510, 470, 170, STAND, 1)
                    lines_in(c, ph, t, T_TOLD, 0.5, GLOW, 1.6)
                label(c, "THE PERSONA", 610, 320, t, T_TOLD, 20, GLOW, a=kp * kcard)
                for k, (tt, txt) in enumerate(((wd("persona", "young"), "YOUNG"), (T_INTRO, "INTROVERTED"), (T_INTERNET, "INTO INTERNET CULTURE"))):
                    label(c, txt, 610, 420 + 44 * k, t, tt, 20, WHITE, "left", a=kp * (1 - ease(seg(t, T_GUT - 0.2, T_GUT + 0.2))))
                    ev(tt, "latch", t, 610)
                bars(c, t, [("NO PERSONA · 36%", 0.36, GLOW, wd("persona", "AI's")), ("WITH THE PERSONA · 73%", 0.73, "chrome", T_DOUBLED - 0.3)],
                     930, 380, 600, T_DOUBLED, kp)
                if t >= T_DOUBLED - 0.1:
                    bignum(c, t, "×2", 110, 1230, 690, T_DOUBLED - 0.1)
        kg = win(t, T_GUT - 0.1, T_BOTS + 0.2, 0.3, 0.4)                   # small talk and gut feel
        if kg > 0 and t >= T_SMALL - 0.4:
            with layer(c, kg):
                for k, (bw, right) in enumerate(((280, False), (220, True), (330, False))):
                    tk = T_SMALL - 0.4 + 0.25 * k
                    if t >= tk:
                        stroke_polys(c, bubble(380 if not right else 640, 300 + 70 * k, bw, 36, right), GLOW if right else WHITE, 1.6, 1.0)
                        ev(tk, "pop", t, 600)
                label(c, "SMALL TALK IN 61% OF GAMES", 640, 580, t, T_SMALL + 0.2, 20, WHITE, a=kg)
                label(c, "AND THEN: A GUT FEELING", 640, 620, t, T_GUTW - 0.1, 20, GLOW, a=kg)


# ---------------------------------------------------------------- NOW
T_OUT, T_53, T_AUTO = wd("bots", "outnumbered."), wd("bots", "fifty-three"), wd("bots", "automated.")
T_HUN, T_WERENT = ls("hundred"), wd("hundred", "weren't")
T_CAP, T_CLICK, T_VERIFY = ls("captcha"), wd("captcha", "clicking"), wd("captcha", "verify")
T_NOTE, T_THIS = ls("note"), wd("note", "this")
T_FBI, T_COPIED, T_SECRET = ls("fbi"), wd("fbi", "copied,"), wd("fbi", "secret")
T_FLIP = ls("flip")
CELLS = [(560 + (k % 10) * 82, 250 + (k // 10) * 58) for k in range(100)]
BOT_IDX = set(np.random.default_rng(6).permutation(100)[:53].tolist())


def visits(c, t):
    a = win(t, T_BOTS - 0.1, T_CAP + 0.2, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        label(c, "EVERY 100 VISITS TO A WEBSITE, 2025", CX, 200, t, T_BOTS + 0.2, 22, SOFT, a=a)
        k_icons = ease(seg(t, T_HUN, T_HUN + 0.6))
        for k, (x, y) in enumerate(CELLS):
            tk = T_BOTS + 0.2 + 0.012 * k
            if t < tk:
                continue
            is_bot = k in BOT_IDX and t >= T_53 - 0.2
            if k_icons <= 0:
                c.drawRect(skia.Rect.MakeXYWH(x - 14, y - 14, 28, 28), mg.fill(WHITE, 0.95) if is_bot else mg.stroke(SOFT, 1.3, 0.7))
            else:
                stroke_polys(c, robot_head(x, y, 30) if is_bot else person_head(x, y, 30), WHITE if is_bot else GLOW, 1.5, 1.0)
        ev(T_53 - 0.2, "grains", t, CX)
        bignum(c, t, "53%", 120, 330, 420, T_53 - 0.1)
        label(c, "AUTOMATED", 330, 510, t, T_AUTO, 22, WHITE, a=a)
        label(c, "47 PEOPLE", 1590, 420, t, T_WERENT, 22, GLOW, a=a)
        label(c, "53 BOTS", 1590, 470, t, T_WERENT + 0.2, 22, WHITE, a=a)


def captcha(c, t):
    a = win(t, T_CAP - 0.1, T_FLIP + 0.1, 0.3, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kc = 1 - ease(seg(t, T_FBI - 0.2, T_FBI + 0.3))
        if kc > 0:
            with layer(c, kc):
                label(c, "AN AI AGENT · JULY 2025", CX, 220, t, T_CAP + 0.2, 22, SOFT, a=a * kc)
                x0, y0 = CX - 260, 360
                lines_in(c, checkbox(x0, y0), t, T_CAP + 0.1, 0.5, WHITE, 1.8)
                label(c, "Verify you are human", x0 + 90, y0 + 52, t, T_CAP + 0.5, 26, WHITE, "left", a=a * kc)
                cx_ = keys(t, [(T_CLICK - 0.6, 1500), (T_CLICK + 0.4, x0 + 50), (T_VERIFY, x0 + 46)])
                cy_ = keys(t, [(T_CLICK - 0.6, 760), (T_CLICK + 0.4, y0 + 58), (T_VERIFY, y0 + 56)])
                if t >= T_CLICK - 0.6:
                    closed_fill(c, cursor(cx_, cy_), 1.0, mg.fill(WHITE, 0.9))
                    stroke_polys(c, cursor(cx_, cy_), WHITE, 2.0, 1.0)
                    label(c, "AI AGENT", cx_ + 40, cy_ + 60, t, T_CLICK - 0.4, 18, GLOW, "left", a=a * kc)
                if t >= T_VERIFY:
                    stroke_polys(c, check(x0, y0 + 16, ease(seg(t, T_VERIFY, T_VERIFY + 0.25))), GLOW, 3.4, 1.0)
                    burst(c, x0 + 44, y0 + 43, t, T_VERIFY, 36)
                    ev(T_VERIFY, "confirm", t, x0)
                if t >= T_NOTE - 0.1:                                       # its own note
                    lines_in(c, [mg.rrect_pts(CX - 520, 560, 1040, 150, 12, 4)], t, T_NOTE - 0.1, 0.4, SOFT, 1.5)
                    label(c, "ITS OWN NOTE:", CX - 490, 600, t, T_NOTE + 0.1, 18, SOFT, "left", a=a * kc)
                    label(c, "\"This step is necessary to prove I'm not a bot.\"", CX - 490, 660, t, T_THIS - 0.1, 26, GLOW, "left", a=a * kc, cps=20)
        if t >= T_FBI - 0.1:                                               # the voice, copied; the secret word
            kf = ease(seg(t, T_FBI - 0.1, T_FBI + 0.4))
            with layer(c, kf):
                lines_in(c, phone(620, 520, 150), t, T_FBI - 0.1, 0.5, WHITE, 1.8)
                stroke_polys(c, wave(620, 520, 180, 150, t), GLOW, 2.2, 1.0)
                if t >= T_COPIED - 0.2:
                    k2 = ease(seg(t, T_COPIED - 0.2, T_COPIED + 0.4))
                    lines_in(c, phone(1000, 520, 150), t, T_COPIED - 0.2, 0.4, WHITE, 1.8)
                    stroke_polys(c, wave(1000, 520, 180, 150, t, dotted=True), GLOW, 2.2, k2)
                    label(c, "A COPIED VOICE", 1000, 740, t, T_COPIED, 20, SOFT, a=a)
                    ev(T_COPIED - 0.2, "glitch", t, 1000)
                if t >= T_SECRET - 0.2:
                    lines_in(c, key(1400, 520, 140), t, T_SECRET - 0.2, 0.5, WHITE, 2.0)
                    label(c, "A SECRET WORD", 1400, 640, t, T_SECRET + 0.2, 22, WHITE, a=a)
                    label(c, "THE FBI'S ADVICE, DEC 2024", 1400, 680, t, T_SECRET + 0.5, 18, GLOW, a=a)
                    ev(T_SECRET - 0.2, "latch", t, 1400)


# ---------------------------------------------------------------- IDEA
T_OTHER, T_PROVE = ls("other"), wd("other", "prove")
T_CLAIM0, T_DEFAULT, T_CLAIMW = ls("claim"), wd("claim", "default."), wd("claim", "claim.")
T_IMAGINE = ls("imagine")


def flip(c, t):
    a = win(t, T_FLIP - 0.05, T_IMAGINE + 0.2, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        lines_in(c, computer(560, 700, 220), t, T_FLIP, 0.5, WHITE, 1.8)
        pp, _ = figure(1360, 700 - 0.48 * 330, 330, STAND, -1)
        lines_in(c, pp, t, T_FLIP + 0.2, 0.5, GLOW, 1.7)
        k = ease(seg(t, T_OTHER, T_OTHER + 0.7))                            # the arrow turns round
        y = 520
        if k < 1:
            for p in arrow(700 + 0 * k, y, 1220, y):
                stroke_polys(c, [p], WHITE, 2.0, 1 - k)
        if k > 0:
            for p in arrow(1220, y, 700, y):
                stroke_polys(c, [p], GLOW, 2.2, k)
        ev(T_OTHER, "morph", t, CX)
        label(c, "CAN A MACHINE PASS AS A PERSON?", CX, 470, t, T_FLIP + 0.3, 22, WHITE, a=a * (1 - k))
        label(c, "CAN A PERSON PROVE THEY'RE A PERSON?", CX, 470, t, T_PROVE - 0.2, 22, GLOW, a=a * k)
        kd = win(t, T_CLAIM0 - 0.1, T_IMAGINE + 0.2, 0.3, 0.4)
        if kd > 0:
            label(c, "HUMAN: THE DEFAULT", CX, 250, t, T_DEFAULT - 0.4, 26, SOFT, a=kd)
            if t >= T_DEFAULT + 0.3:
                w = 330 * ease(seg(t, T_DEFAULT + 0.3, T_DEFAULT + 0.6))
                c.drawLine(CX - 165, 241, CX - 165 + w, 241, mg.stroke(WHITE, 3, kd))
                ev(T_DEFAULT + 0.3, "scan", t, CX)
            label(c, "HUMAN: A CLAIM", CX, 310, t, T_CLAIMW - 0.2, 30, WHITE, a=kd)


# ---------------------------------------------------------------- IMAGINE
T_2030, T_SYN = wd("imagine", "twenty"), wd("imagine", "synthetic.")
T_WHATIF, T_PROOF = ls("whatif"), ls("proof")
T_KEY, T_CHAN, T_MEET = wd("proof", "secret"), wd("proof", "second"), wd("proof", "Someone")
T_Q, T_TRUST = ls("question"), wd("question", "trust.")
T_THEN = ls("then")


def imagine(c, t):
    a = win(t, T_IMAGINE - 0.05, T_THEN + 0.1, 0.3, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        kd = 1 - ease(seg(t, T_PROOF - 0.2, T_PROOF + 0.2))
        if kd > 0:
            with layer(c, kd):
                dotted_num(c, "2030", 140, CX, 220, t, T_2030, kd)
                lines_in(c, phone(CX, 560, 170), t, T_IMAGINE + 0.3, 0.5, WHITE, 1.8)
                stroke_polys(c, wave(CX, 560, 220, 180, t, dotted=t >= T_SYN - 0.2), GLOW, 2.4, 1.0)
                label(c, "REAL, OR SYNTHETIC?", CX, 800, t, T_SYN - 0.3, 22, WHITE, a=a * kd)
                label(c, "NOT A FORECAST · A WHAT-IF", CX, 320, t, T_WHATIF + 0.05, 24, WHITE, a=a * kd)
        if t >= T_PROOF - 0.2:                                              # three ways to prove you're you
            kp = ease(seg(t, T_PROOF - 0.2, T_PROOF + 0.3))
            with layer(c, kp):
                label(c, "WAYS TO PROVE YOU'RE YOU", CX, 230, t, T_PROOF + 0.3, 24, WHITE, a=a)
                if t >= T_KEY - 0.2:
                    lines_in(c, key(520, 500, 150), t, T_KEY - 0.2, 0.4, WHITE, 2.0)
                    label(c, "A SECRET WORD", 520, 640, t, T_KEY + 0.1, 20, GLOW, a=a)
                    ev(T_KEY - 0.2, "latch", t, 520)
                if t >= T_CHAN - 0.2:
                    lines_in(c, phone(890, 500, 90) + phone(1030, 500, 90), t, T_CHAN - 0.2, 0.4, WHITE, 1.8)
                    c.drawLine(940, 470, 980, 470, mg.stroke(GLOW, 2, 1.0)); c.drawLine(940, 530, 980, 530, mg.stroke(GLOW, 2, 1.0))
                    label(c, "A SECOND CHANNEL", 960, 640, t, T_CHAN + 0.1, 20, GLOW, a=a)
                    ev(T_CHAN - 0.2, "link", t, 960)
                if t >= T_MEET - 0.2:
                    p1, _ = figure(1330, 520, 180, dict(STAND, rs=70, re=10), 1)
                    p2, _ = figure(1470, 520, 180, dict(STAND, rs=70, re=10), -1)
                    lines_in(c, p1 + p2, t, T_MEET - 0.2, 0.5, GLOW, 1.7)
                    label(c, "SOMEONE YOU CAN MEET", 1400, 640, t, T_MEET + 0.1, 20, GLOW, a=a)
                    ev(T_MEET - 0.2, "form", t, 1400)
                if t >= T_Q:
                    label(c, "WHO CAN YOU TRUST?", CX, 790, t, T_TRUST - 0.5, 30, WHITE, a=a)


# ---------------------------------------------------------------- SURFACE
T_1950B, T_MACHINE = wd("then", "nineteen"), wd("then", "machine.")
T_2026, T_US = wd("now2", "twenty"), wd("now2", "us.")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "Jones & Bergen, UC San Diego, 2025: 284 people; GPT-4.5 with a persona judged human 73%, 36% without",
           "Turing, Computing Machinery and Intelligence, Mind, 1950: \"not more than 70 per cent\" after five minutes",
           "Imperva Bad Bot Report 2026: automated traffic over 53% of the web in 2025",
           "ChatGPT Agent clicks \"Verify you are human\", July 2025: Ars Technica; Tom's Hardware",
           "FBI IC3 PSA241203, 3 Dec 2024: agree a secret word or phrase with your family",
           "The 2030 section is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 820)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 820))
            bignum(c, t, "1950", 130, 560, 250, T_1950B)
            lines_in(c, computer(560, 700, 220), t, T_1950B + 0.3, 0.5, WHITE, 1.8)
            label(c, "THE TEST WAS FOR THE MACHINE", 560, 780, t, T_MACHINE - 0.2, 20, GLOW, a=a)
            if t >= T_2026 - 0.05:
                bignum(c, t, "2026", 130, 1360, 250, T_2026 - 0.05)
                pp, _ = figure(1360, 700 - 0.48 * 330, 330, STAND, -1)
                lines_in(c, pp, t, T_2026 + 0.2, 0.5, GLOW, 1.7)
                label(c, "NOW IT'S FOR US", 1360, 780, t, T_US - 0.2, 20, GLOW, a=a)
                ev(T_2026 + 0.2, "form", t, 1360)
    if t >= T_SRC:
        ks = 1 - ease(seg(t, T_SRC + 7.0, T_SRC + 7.8))
        for k, s_ in enumerate(SOURCES):
            label(c, s_, 250, 280 + k * 54, t, T_SRC + 0.2 + (0 if k == 0 else 0.6 + 0.45 * (k - 1)),
                  24 if k == 0 else 20, GLOW if k == 0 else SOFT, align="left", a=ks, cps=17 if k == 0 else 45)


def end_time():
    return T_SRC + 8.0


def frame(c, t):
    chats(c, t)
    imitation(c, t)
    visits(c, t)
    captcha(c, t)
    flip(c, t)
    imagine(c, t)
    mirror(c, t)
