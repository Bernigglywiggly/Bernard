"""Covers and thumbnails: two 9:16 covers for EP01 (TikTok / Shorts), a 16:9 thumbnail for EP01 and one for
THE CURVE pilot. Same system as the videos: graphite marl, one turquoise, Michroma numbers, the log ruler.

    python3 covers.py        # build/covers/*.png (+ .jpg)
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(HERE, "..", "..", "a01_v6")
sys.path.insert(0, V6)
os.environ.setdefault("A01V6_FONTS", os.path.join(V6, "fonts"))
import mograph as mg  # noqa: E402
import skia  # noqa: E402

OUT = os.path.join(HERE, "build", "covers")
TURQ, GLOW, WHITE, MID, SOFT = mg.TURQ, mg.TURQ_GLOW, mg.ON_DARK, mg.ON_DARK_MID, mg.ON_DARK_SOFT


def ground(w, h, base=mg.DARK, seed=2):
    ww = (w + 15) // 16 * 16
    W0, H0 = mg.W, mg.H
    mg.W, mg.H = ww, h
    try:
        img = mg.marl(base, seed, 2.4)
    finally:
        mg.W, mg.H = W0, H0
    return img


def text(c, s, x, y, size, col, font=mg.DISPLAY, align="left", a=1.0, paint=None):
    f = mg.font(font, size)
    w = f.measureText(s)
    xx = x - w if align == "right" else x - w / 2 if align == "center" else x
    c.drawString(s, xx, y, f, paint or mg.fill(col, a))
    return w


def glow_line(c, x0, y0, x1, y1, col, w=3.0, g=10.0, a=1.0):
    p = mg.stroke(col, w * 3.2, 0.35 * a)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, g))
    c.drawLine(x0, y0, x1, y1, p)
    c.drawLine(x0, y0, x1, y1, mg.stroke(col, w, a))


def arrow(c, x, y, length, col, size=1.0):
    c.drawLine(x, y, x + length - 16 * size, y, mg.stroke(col, 4.0 * size, 1.0))
    p = skia.Path(); p.moveTo(x + length, y); p.lineTo(x + length - 20 * size, y - 12 * size); p.lineTo(x + length - 20 * size, y + 12 * size); p.close()
    c.drawPath(p, mg.fill(col, 1.0))


def log_ruler(c, x0, x1, y, marks, size=1.0, highlight=None):
    """1 s .. 1 month log ruler with tick labels; marks = [(seconds, label, col)]."""
    lo, hi = 0.0, math.log10(30 * 86400)
    X = lambda s: x0 + (math.log10(max(1, s)) - lo) / (hi - lo) * (x1 - x0)
    c.drawLine(x0, y, x1, y, mg.stroke(MID, 2 * size, 0.7))
    for s, lab in ((1, "1S"), (60, "1M"), (3600, "1H"), (86400, "1D"), (7 * 86400, "1W"), (30 * 86400, "1MO")):
        c.drawLine(X(s), y - 12 * size, X(s), y + 12 * size, mg.stroke(MID, 1.6 * size, 0.8))
        text(c, lab, X(s), y + 44 * size, 18 * size, SOFT, font=mg.MONO, align="center")
    if highlight:
        a, b = X(highlight[0]), X(highlight[1])
        glow_line(c, a, y, b, y, TURQ, 5 * size, 12 * size)
    for s, lab, col in marks:
        c.drawCircle(X(s), y, 9 * size, mg.fill(col, 1.0))
        if lab:
            text(c, lab, X(s), y - 26 * size, 20 * size, col, font=mg.MONO_M, align="center")
    return X


def vignette(c, w, h, s=0.6):
    sh = skia.GradientShader.MakeRadial((w / 2, h / 2), max(w, h) * 0.62, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, s)], [0.5, 1.0])
    p = skia.Paint(); p.setShader(sh)
    c.drawRect(skia.Rect.MakeWH(w, h), p)


def save(surf, name):
    os.makedirs(OUT, exist_ok=True)
    img = surf.makeImageSnapshot()
    img.save(os.path.join(OUT, name + ".png"), skia.kPNG)
    img.save(os.path.join(OUT, name + ".jpg"), skia.kJPEG)
    print("wrote", name)


def cover_a():
    """9:16 · the number journey: 2 SEC → 16 HOURS on the ruler, 7 YEARS."""
    w, h = 1080, 1920
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    text(c, "AN AI WORKED ALONE FOR", w / 2, 640, 40, SOFT, font=mg.MONO_M, align="center")
    text(c, "16", w / 2, 1010, 360, WHITE, align="center", paint=mg.chrome_paint(690, 1010))
    text(c, "HOURS", w / 2, 1150, 120, TURQ, align="center")
    log_ruler(c, 110, 970, 1420, [(2, "2019", WHITE), (16 * 3600, "2026", TURQ)], 1.25, highlight=(2, 16 * 3600))
    text(c, "7 YEARS AGO IT WAS 2 SECONDS", w / 2, 1590, 34, WHITE, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.55)
    save(s, "ep01_cover_a")


def cover_b():
    """9:16 · the question: WHAT WOULD YOU HAND OVER?"""
    w, h = 1080, 1920
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    rng = np.random.default_rng(5)
    f = mg.font(mg.MONO_M, 22)
    ramp = " .·:-=+*oxX#"
    for yy in range(180, 1700, 30):                       # an ASCII haze: the dream layer
        for xx in range(40, 1060, 18):
            u, v = xx / w, yy / h
            val = 0.5 + 0.5 * math.sin(u * 9 + v * 5) * math.cos(v * 7 - u * 3)
            val *= max(0.0, 1.1 - 1.8 * math.hypot(u - 0.5, (v - 0.47) * 0.8))
            ch = ramp[min(len(ramp) - 1, int(val * (len(ramp) - 1)))]
            if ch != " ":
                c.drawString(ch, xx, yy, f, mg.fill(TURQ, 0.18 + 0.4 * val))
    c.drawRect(skia.Rect.MakeWH(w, h), mg.fill("#0B0C0E", 0.25))
    text(c, "IF AN AI COULD WORK", w / 2, 760, 56, WHITE, align="center")
    text(c, "A WHOLE MONTH", w / 2, 890, 80, TURQ, align="center")
    text(c, "FOR YOU…", w / 2, 1000, 56, WHITE, align="center")
    r = skia.Rect.MakeXYWH(150, 1110, 780, 110)
    p = mg.stroke(GLOW, 2.4, 1.0); p.setPathEffect(skia.DashPathEffect.Make([10, 9], 0))
    c.drawRoundRect(r, 16, 16, p)
    text(c, "WHAT WOULD YOU KEEP?", w / 2, 1180, 38, GLOW, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.5)
    save(s, "ep01_cover_b")


def thumb_ep01():
    """16:9 · YouTube: 2 SEC → 16 HOURS."""
    w, h = 1280, 720
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    f = mg.font(mg.DISPLAY, 104)
    w1, w2, gap = f.measureText("2 SEC"), f.measureText("16 HRS"), 170
    x0 = (w - (w1 + gap + w2)) / 2
    text(c, "2 SEC", x0, 330, 104, SOFT)
    arrow(c, x0 + w1 + 26, 292, gap - 52, TURQ, 1.5)
    text(c, "16 HRS", x0 + w1 + gap, 330, 104, WHITE, paint=mg.chrome_paint(225, 335))
    log_ruler(c, 110, 1170, 520, [(2, "2019", WHITE), (16 * 3600, "2026", TURQ)], 1.0, highlight=(2, 16 * 3600))
    text(c, "HOW LONG AN AI CAN WORK ALONE", w / 2, 650, 28, TURQ, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.5)
    save(s, "ep01_thumb_16x9")


def thumb_pilot():
    """16:9 · THE CURVE: the exponential rail with 1956 and the 90-minute summit."""
    w, h = 1280, 720
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    pts = []
    for k in range(400):
        yr = 1950 + 76 * k / 399
        y = 0.026 * (math.exp((yr - 1950) / 9.0) - 1)
        pts.append((110 + (yr - 1950) / 76 * 1000, 640 - y / 120 * 520))
    path = skia.Path(); path.moveTo(*pts[0])
    for x, y in pts[1:]:
        path.lineTo(x, y)
    p = mg.stroke(TURQ, 16, 0.25); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
    c.drawPath(path, p)
    c.drawPath(path, mg.stroke(TURQ, 5, 1.0))
    c.drawCircle(pts[-1][0], pts[-1][1], 12, mg.fill(WHITE, 1.0))
    text(c, "1956", 110, 690, 26, SOFT, font=mg.MONO_M)
    text(c, "2026", 1110, 690, 26, TURQ, font=mg.MONO_M, align="right")
    text(c, "90 MINUTES", 110, 200, 84, WHITE, paint=mg.chrome_paint(120, 205))
    text(c, "APART", 110, 290, 84, TURQ)
    text(c, "THE CURVE ISN'T A TREND LINE", 110, 350, 24, SOFT, font=mg.MONO_M)
    vignette(c, w, h, 0.5)
    save(s, "pilot_thumb_16x9")


if __name__ == "__main__":
    cover_a(); cover_b(); thumb_ep01(); thumb_pilot()
