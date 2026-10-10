#!/usr/bin/env python3
"""The chosen title and thumbnail pairing for HTP 06, shown the way a feed shows it (dark mode), with the two
thumbnails that go into Test & Compare beside it.

    ~/youtube/.venv/bin/python combo.py      # -> combo_pick.png
"""
import os

import skia

import look_test as LT
from look_test import col, font

TITLE = "Visa Isn't a Credit Card Company"
PICK, TESTS = "D", ("H", "A")


def img(n):
    return skia.Image.open(os.path.join(LT.HERE, f"thumb_{n}.png"))


def tile(c, n, x, y, w, big):
    samp = skia.SamplingOptions(skia.CubicResampler.Mitchell())
    h = w * 9 / 16
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), w * 0.025, w * 0.025), True)
    c.drawImageRect(img(n), skia.Rect.MakeXYWH(x, y, w, h), samp)
    c.restore()
    s = w / 640
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + w - 62 * s, y + h - 34 * s, 52 * s, 24 * s), 5 * s, 5 * s), skia.Paint(Color=col("#000000", 0.85), AntiAlias=True))
    c.drawString("4:19", x + w - 56 * s, y + h - 16 * s, font("InterTight-600", 17 * s), skia.Paint(Color=col("#FFFFFF"), AntiAlias=True))
    c.drawCircle(x + 22 * s, y + h + 40 * s, 20 * s, skia.Paint(Color=col("#5FF0E4"), AntiAlias=True))
    c.drawString(TITLE, x + 56 * s, y + h + 36 * s, font("InterTight-600", 25 * s), skia.Paint(Color=col("#F1F1F1"), AntiAlias=True))
    c.drawString("How They Profit  ·  2 hours ago", x + 56 * s, y + h + 64 * s, font("InterTight-600", 17 * s), skia.Paint(Color=col("#AAAAAA"), AntiAlias=True))
    if big:
        c.drawString(big, x, y - 16, font("IBMPlexMono-400", 22), skia.Paint(Color=col("#C9CED3"), AntiAlias=True))


def main():
    s = skia.Surface(1500, 720)
    c = s.getCanvas()
    c.clear(col("#0F0F0F"))
    tile(c, PICK, 40, 60, 860, f"THE PICK: thumbnail {PICK} + this title")
    for k, n in enumerate(TESTS):
        tile(c, n, 960, 60 + k * 330, 400, f"test against it: {n}")
    p = os.path.join(LT.HERE, "combo_pick.png")
    s.makeImageSnapshot().save(p, skia.kPNG)
    print(p)


if __name__ == "__main__":
    main()
