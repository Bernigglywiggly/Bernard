"""Hormuz thumbnail (10 Oct): the film's opening map (frame 0, style F) on the right, "8 SHIPS" as an acid-yellow
highlighter swipe on the left, a small "WAS 125 A DAY" line. 1280x720 JPEG.
    ~/youtube/.venv/bin/python thumb.py <frame0.png> <out.jpg>"""
import os
import sys

import numpy as np
import skia

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "ch2", "ep06"))
from look_test import font  # noqa: E402

W, H = 1280, 720
src, out = sys.argv[1], sys.argv[2]
img = skia.Image.open(src)
s = skia.Surface(W, H)
c = s.getCanvas()
c.clear(skia.Color(0, 0, 0))
# the map: crop around the strait from the 1920x1080 frame, placed right, faded into black on its left edge
c.drawImageRect(img, skia.Rect.MakeXYWH(560, 150, 1000, 562), skia.Rect.MakeXYWH(330, 40, 1150, 646),
                skia.SamplingOptions(skia.CubicResampler.Mitchell()))
fade = skia.Paint(Shader=skia.GradientShader.MakeLinear([(330, 0), (720, 0)], [skia.Color(0, 0, 0, 255), skia.Color(0, 0, 0, 0)]))
c.drawRect(skia.Rect.MakeXYWH(330, 0, 390, H), fade)
YEL = skia.Color(0xE6, 0xFF, 0x2E)
big = font("InterTight-600", 330)
# highlighter swipe behind "8"
c.drawString("8", 56, 452, big, skia.Paint(Color=YEL, AntiAlias=True,
             ImageFilter=skia.ImageFilters.DropShadow(0, 0, 18, 18, skia.Color(0xE6, 0xFF, 0x2E, 150))))
f2 = font("InterTight-600", 120)
c.drawRect(skia.Rect.MakeXYWH(40, 478, 520, 132), skia.Paint(Color=YEL, AntiAlias=True))
c.drawString("SHIPS", 60, 588, f2, skia.Paint(Color=skia.Color(10, 12, 4), AntiAlias=True))
f3 = font("IBMPlexMono-500", 34)
c.drawString("WAS 125 A DAY", 62, 668, f3, skia.Paint(Color=skia.Color(0xF2, 0xF5, 0xF7), AntiAlias=True))
s.makeImageSnapshot().save(out, skia.kJPEG)
print(out)
