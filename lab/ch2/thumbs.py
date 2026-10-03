"""THE MARGIN · thumbnails in the ledger look, two per film (A: the number, B: the mechanism), drawn as vectors so they
don't wait for a render. 1920x1080 JPEGs in ch2/build/thumbs/ plus a contact sheet.

    python3 ch2/thumbs.py
"""
import os
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine  # noqa: E402,F401  (paths)
from ch2 import look as L  # noqa: E402
from ch2 import ledger  # noqa: E402
from ch2 import kit  # noqa: E402

W, H = 1920, 1080
OUT = os.path.join(HERE, "build", "thumbs")
PAPER, BRASS, RED, MUTED, INK = L.PAPER, L.BRASS, L.RED, L.MUTED, L.INK


class _B:                                                  # a finished beat: every piece fully drawn
    t, t0 = 99.0, 0.0

    def k(self, a, d=0.5, curve="io"):
        return 1.0

    def w(self, *a, **k):
        return 0.0


B = _B()


def ground(c):
    L.ground(c, margin=False)
    L.text(c, ledger.BRAND, 80, 86, L.font(L.MONO_M, 30), L.fill(BRASS, 0.95), track=0.22)


def headline(c, lines, x=80, y0=330, size=150, cols=None, face=L.SERIF_B, gap=1.02):
    for i, ln in enumerate(lines):
        col = cols[i] if cols else PAPER
        f = L.font(face, size)
        while f.measureText(ln) > 1100 and f.getSize() > 60:
            f = L.font(face, f.getSize() - 4)
        o = L.stroke("#000000", 10, 0.6)
        L.text(c, ln, x, y0 + i * size * gap, f, o)
        L.text(c, ln, x, y0 + i * size * gap, f, L.fill(col))


def ep01_a(c):
    ground(c)
    headline(c, ["A CARD COMPANY", "PAID AN AIRLINE"], y0=300, size=96, cols=[PAPER, PAPER])
    headline(c, ["$8.2 BILLION"], y0=560, size=190, cols=[BRASS])
    kit.plane(c, 1540, 830, 190, 1.0, PAPER)
    kit.card(c, 1080, 860, 300, 1.0, BRASS, "")


def ep01_b(c):
    ground(c)
    headline(c, ["THE MILES", "WERE WORTH", "MORE THAN", "THE AIRLINE"], y0=290, size=130, cols=[PAPER, PAPER, BRASS, BRASS])
    kit.receipt(c, B, 1290, 150, 520, "UNITED · JUNE 2020", "MILEAGEPLUS",
                [("", ""), ("VALUED", "$21.9B"), ("WHOLE AIRLINE", "$10.5B"), ("", "")], circle=1)


def ep02_a(c):
    ground(c)
    headline(c, ["McDONALD'S"], y0=300, size=120, cols=[PAPER])
    headline(c, ["$10.4B", "IN RENT"], y0=480, size=170, cols=[BRASS, PAPER])
    kit.land(c, 1500, 820, 260, 1.0)
    kit.shop(c, 1500, 760, 150, 1.0, PAPER)


def ep02_b(c):
    ground(c)
    headline(c, ["IT'S NOT A", "BURGER", "COMPANY"], y0=300, size=150, cols=[PAPER, BRASS, PAPER])
    kit.stamp(c, B, "LANDLORD", 1450, 520, 0.0, RED, 84, -10)


def ep03_a(c):
    ground(c)
    kit.hotdog(c, 1450, 360, 210, 1.0)
    kit.cup(c, 1450, 660, 110, 1.0)
    headline(c, ["$1.50", "HOT DOG."], y0=330, size=170, cols=[BRASS, PAPER])
    headline(c, ["$9.2B PROFIT."], y0=720, size=120, cols=[PAPER])


def ep03_b(c):
    ground(c)
    kit.card(c, 1420, 520, 640, 1.0, BRASS, "MEMBER")
    headline(c, ["THE CARD", "IS THE", "PRODUCT"], y0=330, size=160, cols=[PAPER, PAPER, BRASS])


FILMS = [("ep01_a", ep01_a), ("ep01_b", ep01_b), ("ep02_a", ep02_a), ("ep02_b", ep02_b), ("ep03_a", ep03_a), ("ep03_b", ep03_b)]


def main():
    os.makedirs(OUT, exist_ok=True)
    paths = []
    for name, fn in FILMS:
        s = skia.Surface(W, H)
        fn(s.getCanvas())
        p = os.path.join(OUT, name + ".jpg")
        s.makeImageSnapshot().save(p, skia.kJPEG, 92)
        paths.append(p)
    sheet = skia.Surface(W, H * 3 // 2)
    sc = sheet.getCanvas()
    sc.clear(L.col("#000000"))
    for i, p in enumerate(paths):
        sc.drawImageRect(skia.Image.open(p), skia.Rect.MakeXYWH((i % 2) * W / 2, (i // 2) * H / 2, W / 2, H / 2),
                         skia.SamplingOptions(skia.FilterMode.kLinear))
    sp = os.path.join(OUT, "sheet.jpg")
    sheet.makeImageSnapshot().save(sp, skia.kJPEG, 90)
    print(sp)


if __name__ == "__main__":
    main()
