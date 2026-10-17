#!/usr/bin/env python3
"""Thumbnail candidates for HTP 06 (Visa), in the film's look, built from the 6 Oct title and thumbnail research
(RESEARCH_TITLE_THUMB.md). Rules applied: one focal object, three words or fewer of big type, the text complements
the title and never repeats it, contrast first, readable at phone size (each is also written at 168x94 to check).
No logo: the card is a plain wireframe.

    ~/youtube/.venv/bin/python thumbs.py      # -> thumb_A.png, thumb_B.png, thumb_C.png, thumbs_sheet.png
"""
import math
import os

import skia

import look_test as LT
from look_test import col, font, glow, text

W, H = 1280, 720
BG, INK, CYAN, RED, DIM = "#040506", "#F2F5F7", "#5FF0E4", "#FF6A4D", "#7B858C"
HERE = LT.HERE


def card(c, cx, cy, w, rot=-8.0, split=None, sliver=None):
    """A plain payment card, wireframe. split = fraction filled cyan from the left; sliver = fraction lit at the right."""
    h = w * 0.63
    c.save()
    c.translate(cx, cy)
    c.rotate(rot)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.06, w * 0.06)
    c.drawRRect(r, skia.Paint(Color=col("#0B0E11"), AntiAlias=True))
    if split:
        c.save()
        c.clipRRect(r, True)
        c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w * split, h), skia.Paint(Color=col(CYAN), AntiAlias=True))
        c.restore()
    if sliver:
        c.save()
        c.clipRRect(r, True)
        sw = max(10.0, w * sliver)
        c.drawRect(skia.Rect.MakeXYWH(w / 2 - sw, -h / 2, sw, h), glow(CYAN, 0.9, 26))
        c.drawRect(skia.Rect.MakeXYWH(w / 2 - sw, -h / 2, sw, h), skia.Paint(Color=col(CYAN), AntiAlias=True))
        c.restore()
    line = skia.Paint(Color=col(INK), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5)
    c.drawRRect(r, line)
    chip = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w * 0.36, -h * 0.16, w * 0.15, h * 0.2), 8, 8)
    on = BG if split and split > 0.2 else INK
    c.drawRRect(chip, skia.Paint(Color=col(on), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    for k in range(3):                                               # contactless waves
        rr = w * (0.035 + 0.03 * k)
        c.drawArc(skia.Rect.MakeLTRB(-w * 0.16 - rr, -h * 0.06 - rr, -w * 0.16 + rr, -h * 0.06 + rr), -45, 90, False,
                  skia.Paint(Color=col(on), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, StrokeCap=skia.Paint.kRound_Cap))
    for g in range(4):                                               # the number, as dots
        for d in range(4):
            x = -w * 0.36 + g * w * 0.19 + d * w * 0.035
            c.drawCircle(x, h * 0.2, w * 0.011, skia.Paint(Color=col(on if x < -w / 2 + w * (split or 0) else INK, 0.9), AntiAlias=True))
    c.restore()


def base():
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(col(BG))
    return s, c


def thumb_a():
    """The number nobody expects: what Visa keeps. Title supplies 'Visa'; the picture supplies the stake."""
    s, c = base()
    card(c, 330, 380, 520, -9, sliver=0.035)
    text(c, "24¢", 640, 400, font("InterTight-600", 310), CYAN, halo=22)
    text(c, "OF EVERY $100", 652, 508, font("InterTight-600", 80), INK)
    return s.makeImageSnapshot()


def thumb_b():
    """Belief against fact: it lends nothing, and half of what it takes is profit."""
    s, c = base()
    card(c, 300, 372, 480, -9, split=0.5)
    text(c, "LENDS $0", 580, 330, font("InterTight-600", 114), INK)
    text(c, "KEEPS HALF", 580, 466, font("InterTight-600", 114), CYAN, halo=18)
    return s.makeImageSnapshot()


def thumb_c():
    """The look as the hook: the crossing on the typed map, one huge figure."""
    s, c = base()
    land = LT.land_path()
    cols, rows = 96, 40
    mx, my, mw, mh = 30, 20, 1220, 500
    lon0, lon1, lat0, lat1 = -104.0, 14.0, 22.0, 60.0
    g = [[land.contains(lon0 + (i + 0.5) / cols * (lon1 - lon0), lat1 - (j + 0.5) / rows * (lat1 - lat0)) for i in range(cols)] for j in range(rows)]
    f = font("IBMPlexMono-500", mh / rows * 0.95)
    for j in range(rows):
        for i in range(cols):
            if g[j][i]:
                edge = any(0 <= j + dj < rows and 0 <= i + di < cols and not g[j + dj][i + di] for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)))
                c.drawString("#+%*"[(i * 7 + j * 3) % 4] if edge else ".", mx + i * mw / cols, my + (j + 0.8) * mh / rows, f,
                             skia.Paint(Color=col("#8E9AA2" if edge else "#2A3238"), AntiAlias=True))

    def xy(lon, lat):
        return mx + (lon - lon0) / (lon1 - lon0) * mw, my + (lat1 - lat) / (lat1 - lat0) * mh

    (x0, y0), (x1, y1) = xy(-9.14, 38.72), xy(-83.0, 39.96)
    p = skia.Path()
    for i in range(81):
        u = i / 80
        (p.moveTo if i == 0 else p.lineTo)(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - 170 * math.sin(math.pi * u))
    for blur, a, wd in ((30, 0.5, 16), (10, 0.7, 9)):
        pt = glow(CYAN, a, blur)
        pt.setStyle(skia.Paint.kStroke_Style)
        pt.setStrokeWidth(wd)
        c.drawPath(p, pt)
    c.drawPath(p, skia.Paint(Color=col(CYAN), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5))
    for x, y in ((x0, y0), (x1, y1)):
        c.drawCircle(x, y, 13, skia.Paint(Color=col(INK), AntiAlias=True))
    c.drawRect(skia.Rect.MakeXYWH(0, 470, W, 250), skia.Paint(Color=col(BG, 0.92)))
    text(c, "$17 TRILLION", 50, 612, font("InterTight-600", 160), INK)
    text(c, "NOT ITS MONEY", 56, 696, font("InterTight-600", 78), CYAN)
    return s.makeImageSnapshot()


def main():
    imgs = [("A", thumb_a()), ("B", thumb_b()), ("C", thumb_c())]
    for n, im in imgs:
        im.save(os.path.join(HERE, f"thumb_{n}.png"), skia.kPNG)
    # the sheet: each at full size (scaled) and at the size a phone shows it in a feed
    sh = skia.Surface(3 * 660, 372 + 150)
    c = sh.getCanvas()
    c.clear(col("#1B1E22"))
    samp = skia.SamplingOptions(skia.CubicResampler.Mitchell())
    for i, (n, im) in enumerate(imgs):
        c.drawImageRect(im, skia.Rect.MakeXYWH(10 + i * 660, 10, 640, 360), samp)
        c.drawImageRect(im, skia.Rect.MakeXYWH(10 + i * 660, 384, 168, 94), samp)
        text(c, f"{n}   phone feed size ->", 200 + i * 660, 440, font("IBMPlexMono-400", 22), "#C9CED3")
    sh.makeImageSnapshot().save(os.path.join(HERE, "thumbs_sheet.png"), skia.kPNG)
    print(os.path.join(HERE, "thumbs_sheet.png"))


if __name__ == "__main__":
    main()
