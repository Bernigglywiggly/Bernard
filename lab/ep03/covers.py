"""EP03 covers: 9:16 (the number, the mirrored line) and a 16:9 thumbnail. Reuses the EP01 cover kit."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ep01"))
import covers as cv  # noqa: E402
from covers import mg, skia, text, ground, vignette, TURQ, GLOW, WHITE, MID, SOFT  # noqa: E402

cv.OUT = os.path.join(HERE, "build", "covers")


def fit(s, size, max_w, font=None):
    w = mg.font(font or mg.DISPLAY, size).measureText(s)
    return size if w <= max_w else size * max_w / w


def shovel(c, cx, cy, s, col, a=1.0, glow=True):
    """A line-art shovel standing upright; (cx, cy) is the tip of the blade."""
    p = mg.stroke(col, 3.0 * s, a)
    blade = skia.Path()
    pts = [(-46, -95), (46, -95), (44, -35), (30, -8), (0, 12), (-30, -8), (-44, -35), (-46, -95)]
    blade.moveTo(cx + pts[0][0] * s, cy + pts[0][1] * s)
    for px, py in pts[1:]:
        blade.lineTo(cx + px * s, cy + py * s)
    if glow:
        g = mg.stroke(GLOW, 12 * s, 0.3 * a)
        g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14 * s))
        c.drawPath(blade, g)
    c.drawPath(blade, p)
    c.drawLine(cx, cy - 90 * s, cx, cy + 2 * s, mg.stroke(col, 1.6 * s, 0.7 * a))
    for sx in (-1, 1):
        c.drawLine(cx + sx * 12 * s, cy - 95 * s, cx + sx * 5 * s, cy - 125 * s, p)
    for dx in (-4.5, 4.5):
        c.drawLine(cx + dx * s, cy - 122 * s, cx + dx * s, cy - 300 * s, p)
    c.drawCircle(cx, cy - 322 * s, 22 * s, p)
    c.drawLine(cx - 22 * s, cy - 322 * s, cx + 22 * s, cy - 322 * s, p)


def cover_a():
    w, h = 1080, 1920
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    text(c, "1848 · SAN FRANCISCO", w / 2, 560, 34, SOFT, font=mg.MONO_M, align="center")
    big = fit("$36,000", 190, 900)
    text(c, "$36,000", w / 2, 780, big, WHITE, align="center", paint=mg.chrome_paint(780 - big, 785))
    text(c, "IN NINE WEEKS", w / 2, 880, 56, TURQ, align="center")
    shovel(c, w / 2, 1440, 1.25, WHITE)
    text(c, "HE NEVER DUG FOR GOLD", w / 2, 1560, 32, TURQ, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.55)
    cv.save(s, "ep03_cover_a")


def cover_b():
    w, h = 1080, 1920
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    text(c, "THEY SAW", w / 2, 700, 40, SOFT, font=mg.MONO_M, align="center")
    text(c, "A GOLD RUSH.", w / 2, 800, fit("A GOLD RUSH.", 84, 900), WHITE, align="center")
    text(c, "HE SAW", w / 2, 1000, 40, GLOW, font=mg.MONO_M, align="center")
    text(c, "A SUPPLY CHAIN.", w / 2, 1100, fit("A SUPPLY CHAIN.", 84, 900), TURQ, align="center")
    r = skia.Rect.MakeXYWH(250, 1230, 580, 90)
    p = mg.stroke(GLOW, 2.4, 1.0); p.setPathEffect(skia.DashPathEffect.Make([10, 9], 0))
    c.drawRoundRect(r, 16, 16, p)
    text(c, "THE SHOVELS OF 2026", w / 2, 1287, 30, GLOW, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.55)
    cv.save(s, "ep03_cover_b")


def thumb():
    w, h = 1280, 720
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    big = fit("$36,000", 150, 760)
    text(c, "$36,000", 470, 340, big, WHITE, align="center", paint=mg.chrome_paint(340 - big, 345))
    text(c, "SELLING SHOVELS", 470, 450, 50, TURQ, align="center")
    text(c, "1848 → 2026 · THE SHOVELS OF THE AI RUSH", 470, 560, 24, SOFT, font=mg.MONO_M, align="center")
    shovel(c, 1070, 600, 1.35, WHITE)
    vignette(c, w, h, 0.5)
    cv.save(s, "ep03_thumb_16x9")


if __name__ == "__main__":
    cover_a(); cover_b(); thumb()
