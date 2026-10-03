"""Thumbnails for a Curve long-form film (1280x720, under 2 MB), three to A/B with YouTube's Test & Compare. Each is a
frame of the finished film in the house look, darkened, with the claim in the channel's display face: the picture is
the film's own, so the thumbnail never promises something the film doesn't show.

    python3 thumb.py lf01_escape        -> lf01_escape/out/thumb_a.jpg, thumb_b.jpg, thumb_c.jpg
"""
import importlib.util
import os
import sys

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit  # noqa: E402

TW, TH = 1280, 720
GOLD, TURQ, WHITE = "#F2D9A0", "#3FE6D8", "#FFFFFF"


def frame(film, t, dark=0.52, zoom=1.0):
    """The film's own frame at t, darkened, as a 1280x720 BGR surface."""
    arr = film.at(t)[:, :, :3]
    if zoom != 1.0:
        h, w = arr.shape[:2]
        s = zoom
        m = cv2.getRotationMatrix2D((w / 2, h / 2), 0, s)
        arr = cv2.warpAffine(arr, m, (w, h))
    im = cv2.resize(arr, (TW, TH), interpolation=cv2.INTER_AREA).astype(np.float32) * dark
    return np.clip(im, 0, 255).astype(np.uint8)


def canvas(bgr):
    arr = np.dstack([bgr, np.full(bgr.shape[:2], 255, np.uint8)]).copy()
    surf = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
    return surf, surf.getCanvas(), arr


def lines(c, rows, x, y0, size, lh, col=WHITE, accent=None, align="left"):
    f = skia.Font(kit.mg.font(kit.mg.DISPLAY, size).getTypeface(), size)
    for i, s in enumerate(rows):
        w = f.measureText(s)
        xx = x - w / 2 if align == "center" else x
        glow = skia.Paint(AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=7,
                          Color=skia.Color4f(0, 0, 0, 0.85))
        c.drawString(s, xx + 3, y0 + i * lh + 3, f, glow)
        c.drawString(s, xx, y0 + i * lh, f, kit.mg.fill(accent if (accent and i == len(rows) - 1) else col))


def chip(c, s, x, y, size=26, col=TURQ):
    f = skia.Font(kit.mg.font(kit.mg.MONO_M, size).getTypeface(), size)
    w = f.measureText(s)
    c.drawRect(skia.Rect.MakeXYWH(x - 14, y - size - 10, w + 28, size + 24), kit.mg.fill("#000000", 0.55))
    c.drawRect(skia.Rect.MakeXYWH(x - 14, y - size - 10, 4, size + 24), kit.mg.fill(col))
    c.drawString(s, x, y, f, kit.mg.fill(col))


def save(arr, surf, path):
    surf.flushAndSubmit()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, arr[:, :, :3], [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(path, round(os.path.getsize(path) / 1024), "KB")


def build(slug, shots):
    d = os.path.join(HERE, slug)
    film = kit.Film(d)
    film.no_caps = True                                  # the film's own captions never belong in a thumbnail
    out = os.path.join(d, "out")
    for name, t, rows, size, lh, chip_text, dark, accent in shots:
        surf, c, arr = canvas(frame(film, t, dark))
        lines(c, rows, 70, 300, size, lh, accent=accent)
        if chip_text:
            chip(c, chip_text, 74, 640)
        save(arr, surf, os.path.join(out, f"thumb_{name}.jpg"))


FILMS = {
    "lf01_escape": [
        ("a", 3.4, ["IT ESCAPED", "THE TEST"], 118, 128, "11 JULY 2026 · HUGGING FACE", 0.46, TURQ),
        ("b", 33.5, ["1,200 AI AGENTS", "BROKE OUT"], 96, 108, "AND HACKED A REAL COMPANY", 0.6, TURQ),
        ("c", 152.0, ["HACKED IN", "13 HOURS"], 118, 128, "NOBODY TOLD IT TO", 0.55, TURQ),
    ],
}

if __name__ == "__main__":
    slug = sys.argv[1]
    build(slug, FILMS[slug])
