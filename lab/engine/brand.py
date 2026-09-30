"""Channel art in the house look (30 Sep: "so far just making stuff no uploads, need to get on that asap"): a YouTube
banner (2560x1440; the words sit in the 1546x423 middle that phones show), a profile picture (800x800, reads inside a
circle), and the channel's About text and short bio. Line art turned into characters, turquoise glow on black, like
the films.

    python3 -m engine.brand        # -> lab/out/brand/banner.jpg, avatar.png, about.txt
"""
import os

import numpy as np

import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import look, tl  # noqa: E402
from engine.draw import CX, GLOW, WHITE, SOFT, GOLD, bignum, points, stroke_polys, ellipse  # noqa: E402

OUT = os.path.join(engine.LAB, "out", "brand")
T = 30.0                                                    # long after everything has formed
ABOUT = ("The Curve explains the hidden mechanisms behind the AI headlines: why cheaper AI means more data centres, why a "
         "robot can pass an exam but can't fold your shirt, who really gets rich in a gold rush. Every figure is sourced on "
         "screen and in the description, and every price comes in Big Macs. A new film every two days, shorts daily.")
BIO = "AI's hidden mechanisms, in numbers you can picture. A new film every 2 days."
SKY = np.random.default_rng(4).uniform((60, 80), (1860, 460), (700, 2))


def _curve(x0, x1, y0, y1, p=3.0, n=200):
    u = np.linspace(0, 1, n)
    return np.column_stack([x0 + (x1 - x0) * u, y0 + (y1 - y0) * u ** p])


class Banner:
    TRAILS, GLINTS = (), ()

    @staticmethod
    def frame(c, t):
        points(c, SKY, 0.35, SOFT, 2.0)
        stroke_polys(c, [_curve(40, 1880, 990, 150, 5.0)], GLOW, 3.2, 0.95)          # rises after the wordmark
        bignum(c, t, "THE CURVE", 150, CX, 560, 0.0)
        tl.label(c, "THE HIDDEN MECHANISM BEHIND THE AI HEADLINES", CX, 650, t, 0.0, 24, WHITE)
        tl.label(c, "A NEW FILM EVERY TWO DAYS · SHORTS DAILY", CX, 700, t, 0.0, 18, GLOW)


class Avatar:
    TRAILS, GLINTS = (), ()

    @staticmethod
    def frame(c, t):
        q = _curve(640, 1270, 800, 290, 2.4)
        for w, a in ((32, 0.9), (18, 1.0)):
            stroke_polys(c, [q], GLOW, w, a)
        c.drawCircle(1270, 290, 34, skia.Paint(AntiAlias=True, Color=skia.Color4f(1, 1, 1, 1)))
        stroke_polys(c, [ellipse(1270, 290, 60, 60, 0, 360, 48)], GOLD, 4, 0.9)


def render(scenes, size, crop=None):
    img = look.compose(scenes, T)
    s = skia.Surface(*size)
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    src = skia.Rect.MakeXYWH(*crop) if crop else skia.Rect.MakeWH(img.width(), img.height())
    c.drawImageRect(img, src, skia.Rect.MakeWH(*size), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    return s.makeImageSnapshot()


def main():
    os.makedirs(OUT, exist_ok=True)
    tl.EP["title"] = ""                                     # no film furniture on channel art
    render(Banner, (2560, 1440)).save(os.path.join(OUT, "banner.jpg"), skia.kJPEG, 92)
    render(Avatar, (800, 800), (420, 0, 1080, 1080)).save(os.path.join(OUT, "avatar.png"), skia.kPNG)
    open(os.path.join(OUT, "about.txt"), "w").write(f"ABOUT (YouTube)\n{ABOUT}\n\nBIO (TikTok, Instagram, Facebook)\n{BIO}\n")
    print(OUT)


if __name__ == "__main__":
    main()
