"""MONEY CRIMES · channel art in the case-file look (35 mm warmth, gold serif, red rubber stamp): a 2560x1440 banner
(text inside YouTube's 1546x423 safe area) over the forger's-workshop still from film 01, an 800x800 avatar, a 150x150
watermark, then the X and Facebook covers.

    python3 brand/money_crimes.py      -> channel/money-crimes/brand/
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from covers import covers  # noqa: E402

OUT = os.path.join(os.path.dirname(LAB), "channel", "money-crimes", "brand")
FONTS = os.path.join(LAB, "shorts", "fonts")
SERIF, MONO = os.path.join(FONTS, "DMSerifDisplay-Regular.ttf"), os.path.join(FONTS, "IBMPlexMono-Medium.ttf")
GOLD, RED, INK, PAPER = (226, 186, 112), (196, 38, 32), (14, 10, 8), (236, 226, 206)
BG = os.path.join(LAB, "longform", "lustig", "src", "ai", "s01.png")   # the forger's back room, no people


def grade(im, dark=0.42):
    """Warm, dark 35 mm grade with grain and a vignette."""
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255
    lum = a @ [0.3, 0.59, 0.11]
    a = np.stack([lum * 1.08, lum * 0.92, lum * 0.72], -1) * 0.6 + a * 0.4
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1 - 0.75 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) ** 1.2
    a = a * dark * np.clip(vig, 0.15, 1)[..., None]
    a += np.random.default_rng(7).normal(0, 0.018, a.shape)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def stamp(text, size, angle=-8):
    """A red rubber stamp: a double box, letters slightly worn."""
    f = ImageFont.truetype(MONO, size)
    tw = f.getbbox(text)[2]
    pad = size * 0.5
    im = Image.new("RGBA", (int(tw + pad * 2), int(size * 2.1)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w, h = im.size
    d.rectangle((3, 3, w - 4, h - 4), outline=RED + (235,), width=max(3, size // 9))
    d.rectangle((size // 4, size // 4, w - size // 4, h - size // 4), outline=RED + (200,), width=max(1, size // 22))
    d.text((pad, h / 2), text, font=f, fill=RED + (240,), anchor="lm")
    a = np.asarray(im).copy()
    wear = np.random.default_rng(3).random(a.shape[:2]) < 0.16
    a[..., 3][wear] = (a[..., 3][wear] * 0.25).astype(np.uint8)
    return Image.fromarray(a).rotate(angle, expand=True, resample=Image.BICUBIC)


def banner():
    w, h = 2560, 1440
    bg = Image.open(BG).convert("RGB")
    s = max(w / bg.width, h / bg.height)
    bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - w) // 2, (bg.height - h) // 2, (bg.width + w) // 2, (bg.height + h) // 2))
    im = grade(bg.filter(ImageFilter.GaussianBlur(2)), 0.38).convert("RGBA")
    d = ImageDraw.Draw(im)
    cy = h // 2
    title = ImageFont.truetype(SERIF, 200)
    d.text((w / 2 + 4, cy - 2 + 4), "Money Crimes", font=title, fill=(0, 0, 0, 200), anchor="mm")
    d.text((w / 2, cy - 2), "Money Crimes", font=title, fill=GOLD, anchor="mm")
    tw = title.getbbox("Money Crimes")[2]
    d.line((w / 2 - tw / 2, cy + 92, w / 2 + tw / 2, cy + 92), fill=GOLD + (180,), width=3)
    sub = ImageFont.truetype(MONO, 36)
    d.text((w / 2, cy + 150), "THE GREATEST CONS, FRAUDS AND HEISTS, EXPLAINED", font=sub, fill=PAPER, anchor="mm")
    st = stamp("CASE FILE", 54, -9)
    im.alpha_composite(st, (int(w / 2 + tw / 2 - st.width * 0.6), int(cy - 150 - st.height / 2)))
    return im.convert("RGB")


def avatar(size=800):
    im = grade(Image.new("RGB", (size, size), (70, 52, 38)), 0.55).convert("RGBA")
    d = ImageDraw.Draw(im)
    c, r = size / 2, size * 0.41
    d.ellipse((c - r, c - r, c + r, c + r), outline=RED + (235,), width=int(size * 0.035))
    r2 = r * 0.86
    d.ellipse((c - r2, c - r2, c + r2, c + r2), outline=RED + (190,), width=int(size * 0.012))
    f = ImageFont.truetype(SERIF, int(size * 0.36))
    d.text((c + size * 0.008, c + size * 0.008), "MC", font=f, fill=(0, 0, 0, 200), anchor="mm")
    d.text((c, c), "MC", font=f, fill=GOLD, anchor="mm")
    a = np.asarray(im).copy()
    wear = (np.random.default_rng(5).random(a.shape[:2]) < 0.1) & (a[..., 0] > 150) & (a[..., 1] < 80)
    a[..., :3][wear] = (a[..., :3][wear] * 0.55).astype(np.uint8)
    return Image.fromarray(a).convert("RGB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner().save(os.path.join(OUT, "banner_2560x1440.jpg"), quality=92)
    av = avatar()
    av.save(os.path.join(OUT, "avatar_800.png"))
    av.resize((150, 150), Image.LANCZOS).save(os.path.join(OUT, "watermark_150.png"))
    covers(os.path.join(OUT, "banner_2560x1440.jpg"), OUT)
    print(sorted(os.listdir(OUT)))
