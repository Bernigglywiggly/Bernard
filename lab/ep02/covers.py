"""EP02 covers: 9:16 (the price war, the question) and a 16:9 thumbnail. Reuses the EP01 cover kit."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ep01"))
import covers as cv  # noqa: E402
from covers import mg, skia, text, ground, vignette, TURQ, GLOW, WHITE, MID, SOFT  # noqa: E402

cv.OUT = os.path.join(HERE, "build", "covers")


def pct(c, num, x, y, size, col, paint=None, unit_col=None):
    """A big number with a small raised % in the mono face (Michroma's own % reads as o/o). Centred on x."""
    f = mg.font(mg.DISPLAY, size)
    fu = mg.font(mg.MONO_M, size * 0.42)
    wn, wu, gap = f.measureText(num), fu.measureText("%"), size * 0.06
    x0 = x - (wn + gap + wu) / 2
    c.drawString(num, x0, y, f, paint or mg.fill(col, 1.0))
    c.drawString("%", x0 + wn + gap, y - size * 0.40, fu, mg.fill(unit_col or col, 1.0))
    return wn + gap + wu


def fit(s, size, max_w, font=None):
    w = mg.font(font or mg.DISPLAY, size).measureText(s)
    return size if w <= max_w else size * max_w / w


def queen(c, cx, cy, s, col, a=1.0):
    p = mg.stroke(col, 3.0 * s, a)
    crown = skia.Path()
    pts = [(-30, -40), (-24, -78), (-12, -48), (0, -86), (12, -48), (24, -78), (30, -40)]
    crown.moveTo(cx + pts[0][0] * s, cy + pts[0][1] * s)
    for px, py in pts[1:]:
        crown.lineTo(cx + px * s, cy + py * s)
    c.drawPath(crown, p)
    for px, py in ((-24, -82), (0, -90), (24, -82)):
        c.drawCircle(cx + px * s, cy + py * s, 4.5 * s, p)
    body = skia.Path()
    body.moveTo(cx - 30 * s, cy - 40 * s); body.lineTo(cx - 18 * s, cy + 20 * s); body.lineTo(cx + 18 * s, cy + 20 * s); body.lineTo(cx + 30 * s, cy - 40 * s)
    c.drawPath(body, p)
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 38 * s, cy + 20 * s, 76 * s, 16 * s), 4, 4, p)
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 46 * s, cy + 36 * s, 92 * s, 14 * s), 4, 4, p)


def cover_a():
    w, h = 1080, 1920
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    text(c, "TWO AI LABS · ONE AFTERNOON", w / 2, 560, 34, SOFT, font=mg.MONO_M, align="center")
    big = fit("−50", 230, 640)
    pct(c, "−20", w / 2, 800, big, WHITE, paint=mg.chrome_paint(800 - big, 805), unit_col=MID)
    pct(c, "−50", w / 2, 1060, big, TURQ, unit_col=GLOW)
    text(c, "90 MINUTES APART", w / 2, 1190, 60, WHITE, align="center")
    queen(c, 430, 1450, 1.8, WHITE)
    queen(c, 650, 1450, 1.8, TURQ)
    text(c, "BOTH STILL RUNNING", w / 2, 1600, 30, TURQ, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.55)
    cv.save(s, "ep02_cover_a")


def cover_b():
    w, h = 1080, 1920
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    text(c, "WHEN THINKING", w / 2, 760, 70, WHITE, align="center")
    text(c, "IS FREE,", w / 2, 860, 70, WHITE, align="center")
    text(c, "WHAT GETS", w / 2, 1010, 70, TURQ, align="center")
    text(c, "EXPENSIVE?", w / 2, 1110, 70, TURQ, align="center")
    r = skia.Rect.MakeXYWH(210, 1220, 660, 96)
    p = mg.stroke(GLOW, 2.4, 1.0); p.setPathEffect(skia.DashPathEffect.Make([10, 9], 0))
    c.drawRoundRect(r, 16, 16, p)
    text(c, "THE PRICE OF A GENIUS → 0", w / 2, 1280, 30, GLOW, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.55)
    cv.save(s, "ep02_cover_b")


def thumb():
    w, h = 1280, 720
    s = skia.Surface(w, h); c = s.getCanvas()
    c.drawImage(ground(w, h), 0, 0)
    big = fit("−50", 190, 430)
    pct(c, "−20", 330, 330, big, WHITE, paint=mg.chrome_paint(330 - big, 335), unit_col=MID)
    pct(c, "−50", 950, 330, big, TURQ, unit_col=GLOW)
    text(c, "90 MINUTES APART", w / 2, 480, 64, WHITE, align="center")
    text(c, "THE AI PRICE WAR · WHO WINS? YOU.", w / 2, 600, 26, TURQ, font=mg.MONO_M, align="center")
    vignette(c, w, h, 0.5)
    cv.save(s, "ep02_thumb_16x9")


if __name__ == "__main__":
    cover_a(); cover_b(); thumb()
