"""Thumbnails in the one-camera look (8 Oct 2026): the film's own picture, resolved and toned to the palette (never the
characters alone: at feed size they do not read), on the right; the claim in the display face on the left.
1280x720 JPEG, three per film for YouTube's Test & Compare.

    ~/youtube/.venv/bin/python thumb_flow.py            -> <film>/out/thumbflow_a.jpg, _b, _c and thumbflow_sheet.jpg
"""
import glob
import os

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, HERE)
import kit  # noqa: E402

TW, TH = 1280, 720
CY = np.float32([0.37, 0.94, 0.89])
TURQ, WHITE = "#5FF0E4", "#FFFFFF"


def toned(g):
    t = g[..., None]
    cy = CY * 0.62
    return np.where(t < 0.6, np.float32([0.02, 0.03, 0.035]) + (cy - 0.02) * (t / 0.6), cy + (1 - cy) * ((t - 0.6) / 0.4))


def picture(path, x_frac, zoom, gain, cy_frac=0.5):
    """The picture toned, its centre at x_frac of the frame, fading to black on the left where the type sits."""
    g = cv2.imread(path, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    if g.mean() > 0.45:                                             # a pale archive scan: stretch it so the subject carries
        lo, hi = np.percentile(g, 2), np.percentile(g, 99)
        g = np.clip((g - lo) / (hi - lo), 0, 1) ** 1.25
    h, w = g.shape
    sc = max(TH / h, TW * 0.62 / w) * zoom
    g = cv2.resize(g, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_AREA)
    g = np.clip(g * gain, 0, 1)
    out = np.zeros((TH, TW), np.float32)
    x0 = int(TW * x_frac - g.shape[1] / 2)
    y0 = int(TH * cy_frac - g.shape[0] / 2)
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    ww, hh = min(TW - dx0, g.shape[1] - sx0), min(TH - dy0, g.shape[0] - sy0)
    out[dy0:dy0 + hh, dx0:dx0 + ww] = g[sy0:sy0 + hh, sx0:sx0 + ww]
    ramp = np.clip((np.arange(TW) / TW - 0.36) / 0.24, 0.05, 1)[None, :] ** 1.3     # the type's side stays near black
    rgb = toned(out * ramp)
    return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)


def fitted(s, size, maxw):
    f = skia.Font(kit.mg.font(kit.mg.DISPLAY, size).getTypeface(), size)
    while f.measureText(s) > maxw and size > 30:
        size -= 2
        f = skia.Font(kit.mg.font(kit.mg.DISPLAY, size).getTypeface(), size)
    return f, size


def build(film, name, src, rows, chip, x_frac=0.70, zoom=1.0, gain=1.25, maxw=760, cy_frac=0.5):
    path = glob.glob(os.path.join(HERE, film, "src", src + ".*"))[0]
    rgb = picture(path, x_frac, zoom, gain, cy_frac)
    arr = np.ascontiguousarray(np.dstack([rgb, np.full((TH, TW), 255, np.uint8)]))
    surf = skia.Surface(arr, colorType=skia.kRGBA_8888_ColorType)
    c = surf.getCanvas()
    fits = [fitted(s, 170, maxw)[1] for s in rows]
    sizes = [min(v, int(min(fits) * 1.4)) for v in fits]               # a short row may be larger, never wildly
    tot = sum(v * 1.1 for v in sizes)
    y = TH / 2 - tot / 2 - (30 if chip else 0)
    for i, s in enumerate(rows):
        size = sizes[i]
        y += size * 1.1
        f = skia.Font(kit.mg.font(kit.mg.DISPLAY, size).getTypeface(), size)
        edge = skia.Paint(AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=12, Color=skia.Color4f(0, 0, 0, 0.9),
                          StrokeJoin=skia.Paint.kRound_Join)
        c.drawString(s, 52, y - size * 0.22, f, edge)
        c.drawString(s, 52, y - size * 0.22, f, kit.mg.fill(TURQ if i == len(rows) - 1 else WHITE))
    if chip:
        f = skia.Font(kit.mg.font(kit.mg.MONO_M, 30).getTypeface(), 30)
        yy = y + 62
        w = f.measureText(chip)
        c.drawRect(skia.Rect.MakeXYWH(56, yy - 38, w + 36, 56), kit.mg.fill("#000000", 0.72))
        c.drawRect(skia.Rect.MakeXYWH(56, yy - 38, 5, 56), kit.mg.fill(TURQ))
        c.drawString(chip, 74, yy, f, kit.mg.fill(WHITE))
    surf.flushAndSubmit()
    out = os.path.join(HERE, film, "out", f"thumbflow_{name}.jpg")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cv2.imwrite(out, cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    return out


FILMS = {
    "lf01_escape": [
        ("a", "ai/s28", ["IT ESCAPED", "THE TEST"], "11 JULY 2026", dict(x_frac=0.80, zoom=1.1)),
        ("b", "ai/s04", ["THE BOX", "HAD HOLES"], "SOMETHING INSIDE FOUND THEM", dict(x_frac=0.82, zoom=1.15)),
        ("c", "ai/s16", ["NOBODY", "TOLD IT TO"], "700 AI AGENTS · ONE REAL COMPANY", dict(x_frac=0.74)),
    ],
    "lf02_price": [
        ("a", "ai/p06", ["500 NOVELS", "1 BIG MAC"], "WHAT AI COSTS NOW", dict(x_frac=0.83, gain=1.4)),
        ("b", "ai/p14", ["1,000×", "CHEAPER"], "SO WHY IS THE BILL $1 TRILLION?", dict(x_frac=0.80, gain=1.5, maxw=600)),
        ("c", "ai/p13", ["CHEAPER AI", "BIGGER BILL"], "A PARADOX FROM 1865", dict(x_frac=0.78, gain=1.5)),
    ],
    "lf03_held": [
        ("a", "ai/c01", ["TOO", "DANGEROUS", "TO RELEASE"], "THE LAUNCH THAT WAS CANCELLED", dict(x_frac=0.86, gain=1.4)),
        ("b", "ai/h02", ["IT INVENTED", "FAKE PEOPLE"], "UK GOVERNMENT TEST · SEPT 2026", dict(x_frac=0.80, gain=1.4)),
        ("c", "ai/h21", ["LAUNCH", "CANCELLED"], "28 SEPTEMBER 2026", dict(x_frac=0.78, gain=1.6)),
    ],
    "mc02_ponzi": [
        ("a", "photo/ponzi_portrait_bain_1920", ["DOUBLE IN", "90 DAYS"], "BOSTON · 1920", dict(x_frac=0.80, zoom=1.9, gain=1.1, cy_frac=1.05, maxw=640)),
        ("b", "photo/school_street_run_1920", ["THE DAY", "IT BROKE"], "THE RUN ON CHARLES PONZI · 1920", dict(x_frac=0.74, zoom=1.25, gain=1.15, maxw=640)),
        ("c", "photo/ponzi_straw_hat_1920", ["HE NEVER", "BOUGHT IN"], "THE MAN BEHIND THE WORD", dict(x_frac=0.84, zoom=1.5, gain=1.1, cy_frac=0.9, maxw=640)),
    ],
}

if __name__ == "__main__":
    sheet = []
    for film, shots in FILMS.items():
        row = []
        for name, src, rows, chip, o in shots:
            p = build(film, name, src, rows, chip, **o)
            im = cv2.imread(p)
            big = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
            small = np.zeros((110, 640, 3), np.uint8) + 28
            small[8:102, 8:176] = cv2.resize(im, (168, 94), interpolation=cv2.INTER_AREA)
            cv2.putText(small, f"{film} {name}  <- phone feed size", (190, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 205, 210), 1, cv2.LINE_AA)
            row.append(np.vstack([big, small]))
        sheet.append(np.hstack(row))
        cv2.imwrite(os.path.join(HERE, film, "out", "thumbflow_sheet.jpg"), sheet[-1])
    cv2.imwrite(os.path.join(HERE, "thumbflow_all.jpg"), np.vstack(sheet))
    print("ok")
