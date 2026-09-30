"""Channel art in the house look (30 Sep: "so far just making stuff no uploads, need to get on that asap"): a YouTube
banner (2560x1440; the words sit in the 1546x423 middle that phones show), a profile picture (800x800, reads inside a
circle), and the channel's About text and short bio. Line art turned into characters, turquoise glow on black, like
the films.

    python3 -m engine.brand        # -> lab/out/brand/: banner.jpg, avatar.png, watermark.png, facebook_cover.jpg,
                                   #    x_header.jpg, highlight_*.png, channel_setup.md (every name, bio and setting)
"""
import os

import numpy as np

import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import look, tl  # noqa: E402
from engine.draw import CX, GLOW, WHITE, SOFT, GOLD, bignum, points, stroke_polys, ellipse, chip, satellite, figure, mac_icon  # noqa: E402

OUT = os.path.join(engine.LAB, "out", "brand")
T = 30.0                                                    # long after everything has formed
ABOUT = ("The Curve explains the hidden mechanisms behind the AI headlines: why cheaper AI means more data centres, why a "
         "robot can pass an exam but can't fold your shirt, who really gets rich in a gold rush. Every figure is sourced on "
         "screen and in the description, and every price comes in Big Macs. A new film every two days, shorts daily.")
BIO = "AI's hidden mechanisms, in numbers you can picture. A new film every 2 days."
IG_BIO = "The hidden mechanism behind the AI headlines. Every number sourced, every price in Big Macs. New film every 2 days."
KEYWORDS = ("AI, artificial intelligence, AI explained, technology explained, economics explained, AI news, robots, data "
            "centres, Big Mac index, explainer, documentary, science, The Curve")
PINNED = {
    "ep05": "Would you trust a data centre in orbit? Every number in this film is sourced in the description.",
    "ep08": "What would you use thinking for if it cost as little as light? Sources are in the description.",
    "ep04": "Should a robot ever decide on its own? Every figure is sourced in the description.",
    "ep06": "Does your family have a secret word yet? Sources are in the description.",
    "ep07": "What would disappear first in an office built from zero around AI? Sources are in the description.",
    "ep03": "Who are the shovel sellers of the AI rush? Every number is sourced in the description.",
    "ep09": "Which part of your job is the oldest skill you have? Sources are in the description.",
    "ep10": "Who should set the line: a number, or a test? Sources are in the description.",
}
SETUP = f"""# The Curve: channel set-up (every name, bio and setting)

All the art is in the kit page's "Set up the channel once" card (and in the chat). Same look everywhere: black,
turquoise (#35D6C6), white. Channel name everywhere: **The Curve**. Handles to try, in order: @thecurve, @thecurveai,
@thecurve.explained, @curveexplains (keep the same one on every platform).

## YouTube (YouTube Studio > Customisation, on a computer or the Studio app)
- Profile picture: avatar.png. Banner: banner.jpg. Video watermark (Branding > Video watermark): watermark.png, "entire video".
- Description: {ABOUT}
- Keywords (Settings > Channel > Basic info): {KEYWORDS}
- Links: your TikTok, Instagram and Facebook pages once they exist.
- Upload defaults (Settings > Upload defaults): category Education; language English; tags: ai, the curve, explained,
  economics, technology; comments: hold potentially inappropriate ones for review.
- Playlists: "Every film" (all of them, newest first); "AI and money" (EP03, EP08, EP10); "AI and the physical world"
  (EP04, EP05, EP09); "AI and people" (EP06, EP07).
- Each upload: title, description and thumbnail from the kit; not made for kids; altered or synthetic content: Yes (the
  narrator is an AI voice); add it to its playlists; pin the comment below as the first comment.
- Pinned comments: {"; ".join(f"{k.upper()}: {v}" for k, v in PINNED.items())}
- Custom thumbnails and videos over 15 minutes need the channel verified once (Settings > Channel > Feature eligibility).

## TikTok
- Name: The Curve. Photo: avatar.png. Bio: {BIO}
- Every post: switch on "AI-generated content" (More options). Post one short a day in the kit's order; pin each Part 1.

## Instagram
- Name field: The Curve · AI explained (the name field is searchable). Photo: avatar.png.
- Bio: {IG_BIO}
- Highlights: FILMS, SPACE, ROBOTS, MONEY with the four highlight covers. Post the same shorts as Reels.

## Facebook Page
- Name: The Curve. Category: Education website (or Media/news company). Photo: avatar.png. Cover: facebook_cover.jpg.
- Intro: {BIO}
- Post the same shorts as Reels; Meta Business Suite can schedule Instagram and Facebook together.

## X (optional)
- Photo: avatar.png. Header: x_header.jpg. Bio: {IG_BIO}
"""
SKY =np.random.default_rng(4).uniform((60, 80), (1860, 460), (700, 2))


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


class Highlight:
    """An Instagram highlight cover: one icon in the middle of a circle, a word under it."""
    TRAILS, GLINTS = (), ()
    icon, word = "chip", ""

    @classmethod
    def frame(cls, c, t):
        stroke_polys(c, [ellipse(CX, 520, 330, 330, 0, 360, 120)], GLOW, 3.0, 0.8)
        if cls.icon == "chip":
            stroke_polys(c, chip(CX, 500, 130), WHITE, 3.0, 1.0)
        elif cls.icon == "satellite":
            stroke_polys(c, satellite(CX, 500, 260, -0.3), WHITE, 3.0, 1.0)
        elif cls.icon == "robot":
            body, _ = figure(CX, 560, 380, dict(lean=0, head=0, ls=30, le=20, rs=-30, re=20, lh=6, lk=0, rh=-6, rk=0), 1, robot=True)
            stroke_polys(c, body, WHITE, 2.6, 1.0)
        elif cls.icon == "mac":
            mac_icon(c, CX, 470, 150, 1.0)
        tl.label(c, cls.word, CX, 710, t, 0.0, 44, GLOW)


def highlight(icon, word):
    return type("H_" + icon, (Highlight,), dict(icon=icon, word=word))


def render(scenes, size, crop=None):
    img = look.compose(scenes, T)
    s = skia.Surface(*size)
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    src = skia.Rect.MakeXYWH(*crop) if crop else skia.Rect.MakeWH(img.width(), img.height())
    c.drawImageRect(img, src, skia.Rect.MakeWH(*size), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    return s.makeImageSnapshot()


def watermark(path, px=150):
    """The YouTube video watermark (150x150 PNG, transparent): the curve mark drawn solid, not in characters, so it
    stays readable at the size YouTube shows it."""
    s = skia.Surface(px, px)
    c = s.getCanvas()
    c.clear(skia.Color4f(0, 0, 0, 0))
    q = _curve(0.14 * px, 0.8 * px, 0.8 * px, 0.22 * px, 2.4, 80)
    curve = skia.Path()
    curve.addPoly([skia.Point(float(x), float(y)) for x, y in q], False)
    for w, col in ((0.13 * px, skia.Color4f(0.02, 0.05, 0.05, 0.55)), (0.075 * px, skia.Color4f(0.21, 0.84, 0.78, 1.0))):
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=col)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPath(curve, p)
    c.drawCircle(0.8 * px, 0.22 * px, 0.085 * px, skia.Paint(AntiAlias=True, Color=skia.Color4f(0.02, 0.05, 0.05, 0.55)))
    c.drawCircle(0.8 * px, 0.22 * px, 0.06 * px, skia.Paint(AntiAlias=True, Color=skia.Color4f(1, 1, 1, 1)))
    s.makeImageSnapshot().save(path, skia.kPNG)


def main():
    os.makedirs(OUT, exist_ok=True)
    tl.EP["title"] = ""                                     # no film furniture on channel art
    render(Banner, (2560, 1440)).save(os.path.join(OUT, "banner.jpg"), skia.kJPEG, 92)
    render(Avatar, (800, 800), (420, 0, 1080, 1080)).save(os.path.join(OUT, "avatar.png"), skia.kPNG)
    watermark(os.path.join(OUT, "watermark.png"))
    render(Banner, (1640, 624), (0, 175, 1920, 730)).save(os.path.join(OUT, "facebook_cover.jpg"), skia.kJPEG, 92)
    render(Banner, (1500, 500), (0, 220, 1920, 640)).save(os.path.join(OUT, "x_header.jpg"), skia.kJPEG, 92)
    for icon, word in (("chip", "FILMS"), ("satellite", "SPACE"), ("robot", "ROBOTS"), ("mac", "MONEY")):
        sq = render(highlight(icon, word), (1080, 1080), (420, 0, 1080, 1080))
        a = np.array(sq.toarray(), dtype=np.float32)
        yy, xx = np.mgrid[0:1080, 0:1080]
        m = np.clip((520 - np.hypot(xx - 540, yy - 540)) / 60, 0, 1)[..., None]   # a soft round edge, no square band
        a[..., :3] *= m
        full = np.zeros((1920, 1080, 4), np.float32)
        full[..., 3] = 255
        full[420:1500] = a
        full[420:1500, :, 3] = 255
        skia.Image.fromarray(full.astype(np.uint8), colorType=sq.imageInfo().colorType()).save(
            os.path.join(OUT, f"highlight_{word.lower()}.png"), skia.kPNG)
    open(os.path.join(OUT, "about.txt"), "w").write(f"ABOUT (YouTube)\n{ABOUT}\n\nBIO (TikTok, Instagram, Facebook)\n{BIO}\n")
    open(os.path.join(OUT, "channel_setup.md"), "w").write(SETUP)
    print(OUT)


if __name__ == "__main__":
    main()
