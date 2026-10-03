"""THE MARGIN · channel art in the ledger look, following ch2/ledger.py BRAND (rename there, run this again):
a 2560x1440 banner (the text kept inside YouTube's 1546x423 safe area), an 800x800 avatar, a 150x150 watermark.

    python3 ch2/brand.py      -> ch2/build/brand/*.png
"""
import os
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine  # noqa: E402,F401  (paths)
from ch2 import look as L  # noqa: E402
from ch2 import ledger  # noqa: E402

OUT = os.path.join(HERE, "build", "brand")
TAGLINE = "ONE COMPANY'S MONEY MACHINE, OPENED UP"


def ruled(c, w, h, step=42, margin_x=None):
    c.clear(L.col(L.NAVY))
    for y in range(step, h, step):
        c.drawLine(0, y, w, y, L.stroke(L.PAPER, 1, 0.05))
    if margin_x:
        for x in (margin_x, margin_x + 8):
            c.drawLine(x, 0, x, h, L.stroke(L.BRASS, 1.4, 0.3))
    vig = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(w / 2, h / 2), max(w, h) * 0.7,
                                                           [L.col(L.NAVY, 0), L.col("#04070B", 0.85)]))
    c.drawRect(skia.Rect.MakeWH(w, h), vig)


def banner():
    w, h = 2560, 1440
    s = skia.Surface(w, h)
    c = s.getCanvas()
    ruled(c, w, h, margin_x=520)
    cy = h / 2
    f = L.font(L.SERIF_B, 150)
    L.text(c, ledger.BRAND, w / 2, cy + 30, f, L.fill(L.PAPER), "center", track=0.08)
    tw = f.measureText(ledger.BRAND) + 0.08 * 150 * (len(ledger.BRAND) - 1)
    c.drawLine(w / 2 - tw / 2, cy + 70, w / 2 + tw / 2, cy + 70, L.stroke(L.BRASS, 2.4, 0.9))
    c.drawLine(w / 2 - tw / 2, cy + 79, w / 2 + tw / 2, cy + 79, L.stroke(L.BRASS, 1.2, 0.6))
    L.text(c, TAGLINE, w / 2, cy + 140, L.font(L.MONO_M, 34), L.fill(L.BRASS), "center", track=0.18)
    for i, x in enumerate((w / 2 - 640, w / 2 + 640)):                      # a coin and a ticket at the edges of the safe area
        (L.coin if i == 0 else L.ticket)(c, x, cy - 150, 34 if i == 0 else 26, 0.9)
    return s


def avatar(size=800, small=False):
    s = skia.Surface(size, size)
    c = s.getCanvas()
    ruled(c, size, size, step=size // 16)
    c.drawCircle(size / 2, size / 2, size * 0.38, L.stroke(L.BRASS, size * 0.012, 0.95))
    initials = "".join(wd[0] for wd in ledger.BRAND.split() if wd not in ("THE", "A", "OF"))[:2] or ledger.BRAND[:1]
    f = L.font(L.SERIF_B, size * (0.42 if len(initials) == 1 else 0.3))
    L.text(c, initials, size / 2, size / 2 + f.getSize() * 0.36, f, L.fill(L.PAPER), "center")
    if not small:
        c.drawLine(size * 0.3, size * 0.68, size * 0.7, size * 0.68, L.stroke(L.BRASS, size * 0.006, 0.8))
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, surf in (("banner_2560x1440", banner()), ("avatar_800", avatar()), ("watermark_150", avatar(150, True))):
        p = os.path.join(OUT, name + ".png")
        surf.makeImageSnapshot().save(p, skia.kPNG)
        print(p)


if __name__ == "__main__":
    main()
