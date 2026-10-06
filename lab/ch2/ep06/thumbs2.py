#!/usr/bin/env python3
"""A second round of thumbnails for HTP 06 (user, 7 Oct: "more thumbnails, the main goal is eye-catching and a
curiosity trigger"). Six ideas, each one question or contradiction the title does not answer, each true to FACTS.md.
Red is used here as the attention colour against the film's cyan (a complementary pair). No logo.

    ~/youtube/.venv/bin/python thumbs2.py      # -> thumb_D..I.png and thumbs2_sheet.png
"""
import math
import os

import skia

import look_test as LT
import thumbs as T
from look_test import col, font, glow

W, H = T.W, T.H
BG, INK, CYAN, RED = T.BG, T.INK, T.CYAN, T.RED
SANS = "InterTight-600"


def fit(c, s, x, y, maxw, size, colr, halo=0.0, align="left"):
    """Type that is guaranteed to fit its width (nothing may be clipped by the frame)."""
    f = font(SANS, size)
    while f.measureText(s) > maxw and size > 20:
        size -= 2
        f = font(SANS, size)
    w = f.measureText(s)
    x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
    if halo:
        c.drawString(s, x0, y, f, glow(colr, 0.55, halo))
    c.drawString(s, x0, y, f, skia.Paint(Color=col(colr), AntiAlias=True))
    return w, size


def arrow(c, pts, colr=RED, w=16):
    """A fat curved arrow through three points, ending in a head."""
    (x0, y0), (x1, y1), (x2, y2) = pts
    p = skia.Path()
    p.moveTo(x0, y0)
    p.quadTo(x1, y1, x2, y2)
    c.drawPath(p, skia.Paint(Color=col(colr), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap))
    a = math.atan2(y2 - y1, x2 - x1)
    h = skia.Path()
    for i, d in enumerate((0.0, 2.5, -2.5)):
        r = 0 if i == 0 else w * 3.2
        (h.moveTo if i == 0 else h.lineTo)(x2 + (w * 1.6) * math.cos(a) * (1 if i == 0 else 0) - r * math.cos(a + (d and (math.pi - d) or 0)) * (1 if i else 0),
                                           y2 + (w * 1.6) * math.sin(a) * (1 if i == 0 else 0) - r * math.sin(a + (d and (math.pi - d) or 0)) * (1 if i else 0))
    tip = (x2 + w * 1.8 * math.cos(a), y2 + w * 1.8 * math.sin(a))
    h = skia.Path()
    h.moveTo(*tip)
    h.lineTo(x2 + w * 2.6 * math.cos(a + 2.45), y2 + w * 2.6 * math.sin(a + 2.45))
    h.lineTo(x2 + w * 2.6 * math.cos(a - 2.45), y2 + w * 2.6 * math.sin(a - 2.45))
    h.close()
    c.drawPath(h, skia.Paint(Color=col(colr), AntiAlias=True))


def thumb_d():
    """A question with the answer visibly tiny: the sliver at the card's edge."""
    s, c = T.base()
    T.card(c, 400, 372, 640, -7, sliver=0.03)
    c.drawCircle(727, 330, 88, skia.Paint(Color=col(RED), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=12))
    arrow(c, [(1060, 300), (940, 250), (838, 300)])
    fit(c, "WHO GETS", 1240, 170, 470, 120, INK, align="right")
    fit(c, "THIS?", 1240, 600, 430, 200, RED, halo=16, align="right")
    return s.makeImageSnapshot()


def thumb_e():
    """The belief, stamped out."""
    s, c = T.base()
    T.card(c, 640, 372, 880, -6)
    c.save()
    c.translate(640, 372)
    c.rotate(-13)
    f = font(SANS, 190)
    wd = f.measureText("NOT A BANK")
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-wd / 2 - 44, -118, wd + 88, 236), 22, 22)
    c.drawRRect(r, skia.Paint(Color=col(BG, 0.82), AntiAlias=True))
    c.drawRRect(r, glow(RED, 0.5, 20))
    c.drawRRect(r, skia.Paint(Color=col(RED), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=16))
    c.drawString("NOT A BANK", -wd / 2, 68, f, skia.Paint(Color=col(RED), AntiAlias=True))
    c.restore()
    return s.makeImageSnapshot()


def thumb_f():
    """The film's own image: a wall of grey cells and the one that is lit."""
    s, c = T.base()
    cell, gap, cols, rows = 64, 16, 16, 9
    for j in range(rows):
        for i in range(cols):
            lit = (i == 11 and j == 5)
            x, y = 8 + i * (cell + gap), 6 + j * (cell + gap)
            if lit:
                c.drawRect(skia.Rect.MakeXYWH(x - 8, y - 8, cell + 16, cell + 16), glow(CYAN, 0.9, 30))
                c.drawRect(skia.Rect.MakeXYWH(x - 8, y - 8, cell + 16, cell + 16), skia.Paint(Color=col(CYAN), AntiAlias=True))
            else:
                c.drawRect(skia.Rect.MakeXYWH(x, y, cell, cell), skia.Paint(Color=col(INK, 0.2), AntiAlias=True))
    c.drawRect(skia.Rect.MakeXYWH(0, 150, 700, 330), skia.Paint(Color=col(BG, 0.93)))
    fit(c, "VISA'S", 44, 290, 610, 170, INK)
    fit(c, "CUT", 44, 452, 420, 190, CYAN, halo=18)
    arrow(c, [(480, 400), (700, 330), (850, 420)])
    return s.makeImageSnapshot()


def thumb_g():
    """One startling number: half of what it takes in is profit."""
    s, c = T.base()
    T.card(c, 980, 400, 520, 9, split=0.5)
    fit(c, "50%", 40, 400, 660, 400, CYAN, halo=26)
    fit(c, "IS PROFIT", 52, 560, 640, 150, INK)
    return s.makeImageSnapshot()


def thumb_h():
    """The contradiction, stacked: nothing lent, twenty billion made."""
    s, c = T.base()
    for k in range(7):                                               # a tap, radiating
        rr = 120 + k * 110
        c.drawArc(skia.Rect.MakeLTRB(1280 - rr, 360 - rr, 1280 + rr, 360 + rr), 120, 120, False,
                  skia.Paint(Color=col(CYAN, 0.75 - k * 0.09), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=14 - k, StrokeCap=skia.Paint.kRound_Cap))
    fit(c, "LENDS $0", 44, 300, 820, 230, INK)
    fit(c, "MAKES $20B", 44, 560, 900, 230, CYAN, halo=22)
    return s.makeImageSnapshot()


def thumb_i():
    """A question the film answers in its last minute (a rulebook)."""
    s, c = T.base()
    T.card(c, 350, 380, 560, -9)
    f = font(SANS, 300)
    c.drawString("?", 300, 470, f, glow(RED, 0.6, 22))
    c.drawString("?", 300, 470, f, skia.Paint(Color=col(RED), AntiAlias=True))
    fit(c, "WHAT DOES", 1236, 250, 560, 118, INK, align="right")
    fit(c, "VISA SELL?", 1236, 410, 560, 130, INK, align="right")
    fit(c, "NOT MONEY", 1236, 556, 560, 108, CYAN, halo=16, align="right")
    return s.makeImageSnapshot()


def main():
    imgs = [(n, fn()) for n, fn in (("D", thumb_d), ("E", thumb_e), ("F", thumb_f), ("G", thumb_g), ("H", thumb_h), ("I", thumb_i))]
    for n, im in imgs:
        im.save(os.path.join(LT.HERE, f"thumb_{n}.png"), skia.kPNG)
    sh = skia.Surface(3 * 660, 2 * (372 + 130) + 10)
    c = sh.getCanvas()
    c.clear(col("#1B1E22"))
    samp = skia.SamplingOptions(skia.CubicResampler.Mitchell())
    for k, (n, im) in enumerate(imgs):
        x, y = 10 + (k % 3) * 660, 10 + (k // 3) * 502
        c.drawImageRect(im, skia.Rect.MakeXYWH(x, y, 640, 360), samp)
        c.drawImageRect(im, skia.Rect.MakeXYWH(x, y + 372, 168, 94), samp)
        c.drawString(f"{n}   <- phone feed size", x + 190, y + 430, font("IBMPlexMono-400", 22), skia.Paint(Color=col("#C9CED3"), AntiAlias=True))
    p = os.path.join(LT.HERE, "thumbs2_sheet.png")
    sh.makeImageSnapshot().save(p, skia.kPNG)
    print(p)


if __name__ == "__main__":
    main()
