"""THE MARGIN · the ledger look, v1 style frames (1 Oct 2026). Channel 2 must not look like The Curve re-skinned
(channel/CHANNELS.md, rule 2), so nothing here is ASCII: navy-black ground ruled like a ledger, paper-white ink,
brass for the money, accounting red used once a film at most. Type: IBM Plex Serif (headings, figures) with IBM Plex
Mono (labels, sources). Every figure carries its source line on screen.

    python3 ch2/look.py            # style frames -> ch2/build/look/*.jpg and a contact sheet
"""
import math
import os
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
OUT = os.path.join(HERE, "build", "look")
FONT_DIRS = [os.path.join(HERE, "fonts"), os.path.join(os.path.dirname(LAB), "a01_v6", "fonts")]
W, H = 1920, 1080

NAVY, PAPER, BRASS, RED, MUTED, INK = "#0A0F17", "#EFE7D6", "#C9A35B", "#B4553F", "#8C93A0", "#1B1A17"
_TF = {}


def font(name, size):
    if name not in _TF:
        path = next(os.path.join(d, name + ".ttf") for d in FONT_DIRS if os.path.exists(os.path.join(d, name + ".ttf")))
        _TF[name] = skia.Typeface.MakeFromFile(path)
    f = skia.Font(_TF[name], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


SERIF, SERIF_M, SERIF_B, SERIF_I = "IBMPlexSerif-400", "IBMPlexSerif-500", "IBMPlexSerif-600", "IBMPlexSerif-400i"
MONO, MONO_M = "IBMPlexMono-400", "IBMPlexMono-500"


def col(hexs, a=1.0):
    h = hexs.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * max(0.0, min(1.0, a))))


def fill(hexs, a=1.0):
    return skia.Paint(Color=col(hexs, a), AntiAlias=True)


def stroke(hexs, w=2.0, a=1.0):
    return skia.Paint(Color=col(hexs, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


def text(c, s, x, y, f, p, align="left", track=0.0):
    """Draw a string; track adds letter spacing in ems (for the small capitals labels)."""
    if track:
        widths = [f.measureText(ch) + track * f.getSize() for ch in s]
        total = sum(widths) - track * f.getSize()
        x0 = x - (total if align == "right" else total / 2 if align == "center" else 0)
        for ch, w in zip(s, widths):
            c.drawString(ch, x0, y, f, p)
            x0 += w
        return total
    w = f.measureText(s)
    x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
    c.drawString(s, x0, y, f, p)
    return w


_GRAIN = None


def grain():
    global _GRAIN
    if _GRAIN is None:
        rng = np.random.default_rng(7)
        g = rng.normal(0, 1, (H // 2, W // 2))
        a = np.clip(np.abs(g) * 9, 0, 22).astype(np.uint8)
        img = np.zeros((H // 2, W // 2, 4), np.uint8)
        img[..., 0] = img[..., 1] = img[..., 2] = 255
        img[..., 3] = a
        _GRAIN = skia.Image.fromarray(img, colorType=skia.ColorType.kRGBA_8888_ColorType)
    return _GRAIN


def ground(c, margin=True):
    """Navy-black paper ruled like a ledger: faint rules, a brass double margin, grain, a soft vignette."""
    c.clear(col(NAVY))
    for y in range(84, H, 42):
        c.drawLine(0, y, W, y, stroke(PAPER, 1, 0.045))
    if margin:
        for x in (150, 157):
            c.drawLine(x, 0, x, H, stroke(BRASS, 1.2, 0.28))
    c.drawImageRect(grain(), skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(Alphaf=0.35))
    vig = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), 1250, [col(NAVY, 0), col("#04070B", 0.85)]))
    c.drawRect(skia.Rect.MakeWH(W, H), vig)


def furniture(c, film="THE MARGIN", floor=None):
    text(c, film, 190, 70, font(MONO_M, 20), fill(BRASS, 0.9), track=0.22)
    if floor:
        text(c, floor, W - 80, 70, font(MONO, 20), fill(MUTED, 0.9), "right", track=0.22)


def source(c, s):
    text(c, "SOURCE · " + s, 190, H - 56, font(MONO, 19), fill(MUTED, 0.85), track=0.06)


def coin(c, x, y, r=18, a=1.0):
    c.drawCircle(x, y, r, fill(BRASS, 0.9 * a))
    c.drawCircle(x, y, r * 0.72, stroke("#7A5F2C", 2, 0.8 * a))
    c.drawCircle(x - r * 0.3, y - r * 0.35, r * 0.18, fill("#F4DFA8", 0.6 * a))


# ---------------------------------------------------------------- style frames
def f_title(c):
    ground(c, margin=False)
    text(c, "THE MARGIN", W / 2, 560, font(SERIF_B, 150), fill(PAPER), "center", track=0.08)
    c.drawLine(W / 2 - 330, 620, W / 2 + 330, 620, stroke(BRASS, 2, 0.9))
    c.drawLine(W / 2 - 330, 628, W / 2 + 330, 628, stroke(BRASS, 1, 0.6))
    text(c, "ONE COMPANY'S MONEY MACHINE, OPENED UP", W / 2, 690, font(MONO_M, 26), fill(BRASS), "center", track=0.18)


def f_floor(c):
    ground(c)
    furniture(c, floor="BANKS WITH WINGS")
    text(c, "II", 190, 470, font(SERIF_I, 120), fill(BRASS))
    text(c, "The Machine", 190, 610, font(SERIF_M, 120), fill(PAPER))
    text(c, "HOW A MILE IS MADE", 194, 680, font(MONO_M, 26), fill(MUTED), track=0.18)


def f_number(c):
    ground(c)
    furniture(c, floor="I · THE PRICE")
    text(c, "$8.2 billion", W / 2 + 40, 560, font(SERIF_M, 200), fill(PAPER), "center")
    text(c, "AMERICAN EXPRESS → DELTA · 2025", W / 2 + 40, 650, font(MONO_M, 30), fill(BRASS), "center", track=0.14)
    source(c, "DELTA AIR LINES, FULL-YEAR 2025 RESULTS (13 JAN 2026)")


def node(c, x, y, w, h, title, sub):
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 6, 6)
    c.drawRRect(r, fill("#0F1622", 0.95))
    c.drawRRect(r, stroke(PAPER, 2, 0.85))
    text(c, title, x, y + 4, font(SERIF_M, 40), fill(PAPER), "center")
    text(c, sub, x, y + 44, font(MONO, 18), fill(MUTED), "center", track=0.12)


def ticket(c, x, y, r=11, a=1.0):
    """A mile: a small paper ticket (coins are cash; miles never look like cash)."""
    c.save(); c.translate(x, y); c.rotate(45)
    c.drawRect(skia.Rect.MakeXYWH(-r, -r, 2 * r, 2 * r), fill(PAPER, 0.9 * a))
    c.drawRect(skia.Rect.MakeXYWH(-r * 0.55, -r * 0.55, 1.1 * r, 1.1 * r), stroke(NAVY, 1.5, 0.7 * a))
    c.restore()


def arrow(c, pts, label, hexs=PAPER, t=0.62, lab_dy=-18, token=None):
    path = skia.Path()
    path.moveTo(*pts[0])
    path.cubicTo(*pts[1], *pts[2], *pts[3])
    c.drawPath(path, stroke(hexs, 2.4, 0.9))
    (x2, y2), (x3, y3) = pts[2], pts[3]
    ang = math.atan2(y3 - y2, x3 - x2)
    for d in (-0.45, 0.45):
        c.drawLine(x3, y3, x3 - 22 * math.cos(ang + d), y3 - 22 * math.sin(ang + d), stroke(hexs, 2.4, 0.9))
    def at(u):
        p0, p1, p2, p3 = [np.array(p, float) for p in pts]
        return (1 - u) ** 3 * p0 + 3 * (1 - u) ** 2 * u * p1 + 3 * (1 - u) * u * u * p2 + u ** 3 * p3
    mx, my = at(0.5)
    text(c, label, mx, my + lab_dy, font(MONO_M, 22), fill(BRASS), "center", track=0.1)
    for k in range(3):
        u = (t + k * 0.12) % 1.0
        x, y = at(u)
        (token or coin)(c, x, y, 13, 0.95 - 0.25 * k)


def f_machine(c):
    ground(c)
    furniture(c, floor="II · THE MACHINE")
    node(c, 520, 430, 420, 150, "Delta", "PRINTS THE MILES")
    node(c, 1400, 430, 420, 150, "American Express", "BUYS THEM IN BULK")
    node(c, 960, 840, 420, 150, "You", "EARN THEM ON EVERYTHING")
    arrow(c, [(1190, 380), (1050, 300), (870, 300), (730, 380)], "$8.2B CASH · 2025", t=0.2)
    arrow(c, [(730, 480), (870, 560), (1050, 560), (1190, 480)], "MILES", hexs=MUTED, t=0.55, lab_dy=40, token=ticket)
    arrow(c, [(1400, 505), (1400, 700), (1300, 840), (1170, 840)], "", hexs=MUTED, t=0.4, token=ticket)
    text(c, "A FEW MILES", 1430, 690, font(MONO_M, 22), fill(PAPER, 0.85), "left", track=0.1)
    text(c, "PER PURCHASE", 1430, 722, font(MONO_M, 22), fill(PAPER, 0.85), "left", track=0.1)
    source(c, "DELTA AIR LINES 2025 RESULTS; DELTA INVESTOR DAY")


def f_receipt(c):
    ground(c)
    furniture(c, floor="III · THE PROOF")
    x0, y0, w = 1060, 150, 560
    rows = [("MILEAGEPLUS", ""), ("", ""), ("MILES SOLD, 2019", "$5.3B"), ("SOLD TO PARTNERS", "71%"),
            ("VALUED FOR THE LOAN", "$21.9B"), ("BORROWED AGAINST IT", "$6.8B"), ("", ""),
            ("ALL OF UNITED", "$10.5B"), ("ON THE STOCK MARKET", "")]
    h = 110 + 56 * len(rows) + 60
    path = skia.Path()
    path.moveTo(x0, y0)
    path.lineTo(x0 + w, y0)
    path.lineTo(x0 + w, y0 + h)
    n = 14
    for i in range(n):
        xa = x0 + w - (i + 0.5) * w / n
        xb = x0 + w - (i + 1) * w / n
        path.lineTo(xa, y0 + h + 16)
        path.lineTo(xb, y0 + h)
    path.close()
    sh = skia.Paint(Color=col("#000000", 0.55), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.save(); c.translate(10, 16); c.drawPath(path, sh); c.restore()
    c.drawPath(path, fill(PAPER))
    text(c, "UNITED AIRLINES · JUNE 2020", x0 + w / 2, y0 + 62, font(MONO_M, 22), fill(INK), "center", track=0.12)
    c.drawLine(x0 + 30, y0 + 90, x0 + w - 30, y0 + 90, skia.Paint(Color=col(INK, 0.6), StrokeWidth=1.5,
               PathEffect=skia.DashPathEffect.Make([8, 6], 0)))
    y = y0 + 150
    for i, (a, b) in enumerate(rows):
        if a:
            big = i == 0
            text(c, a, x0 + 34, y, font(SERIF_B if big else MONO_M, 34 if big else 23), fill(INK))
        if b:
            bw = text(c, b, x0 + w - 34, y, font(SERIF_B, 34), fill(INK), "right")
            if b == "$21.9B":                                  # the figure that matters, circled in brass ink
                ring = skia.Path()
                cx, cy, rx, ry = x0 + w - 34 - bw / 2, y - 12, bw / 2 + 26, 30
                ring.addOval(skia.Rect.MakeXYWH(cx - rx, cy - ry, 2 * rx, 2 * ry))
                c.save(); c.rotate(-4, cx, cy); c.drawPath(ring, stroke("#A57B2C", 3, 0.95)); c.restore()
        y += 56
    c.drawLine(x0 + 30, y0 + h - 40, x0 + w - 30, y0 + h - 40, skia.Paint(Color=col(INK, 0.6), StrokeWidth=1.5,
               PathEffect=skia.DashPathEffect.Make([8, 6], 0)))
    text(c, "The miles were worth", 190, 470, font(SERIF, 70), fill(PAPER))
    text(c, "twice the airline.", 190, 560, font(SERIF_I, 70), fill(BRASS))
    source(c, "UNITED INVESTOR PRESENTATION, 15 JUN 2020; SKIFT; THE HUSTLE")


def f_split(c):
    ground(c)
    furniture(c, floor="IV · THE MONEY")
    text(c, "Of every $10 spent at a franchised McDonald's", 190, 300, font(SERIF, 54), fill(PAPER))
    x0, y0, w, h = 190, 420, 1540, 210
    parts = [("THE RESTAURANT KEEPS", 8.72, "#2A3442", PAPER), ("RENT", 0.80, BRASS, INK), ("ROYALTY", 0.46, "#8A6F3C", PAPER)]
    x = x0
    for name, v, bg, fg in parts:
        ww = w * v / 10
        c.drawRect(skia.Rect.MakeXYWH(x, y0, ww, h), fill(bg))
        c.drawRect(skia.Rect.MakeXYWH(x, y0, ww, h), stroke(PAPER, 1.5, 0.7))
        if ww > 300:
            text(c, f"${v:.2f}", x + 40, y0 + 120, font(SERIF_M, 76), fill(fg))
            text(c, name, x + 44, y0 + 170, font(MONO_M, 22), fill(fg, 0.85), track=0.12)
        x += ww
    rx = x0 + w * 8.72 / 10
    for i, (label, v) in enumerate([("RENT", "80¢"), ("ROYALTY", "46¢")]):
        cx = rx + (w * 0.80 / 10) / 2 if i == 0 else rx + w * 0.80 / 10 + (w * 0.46 / 10) / 2
        y1 = y0 + h + 40 + i * 110
        c.drawLine(cx, y0 + h, cx, y1, stroke(BRASS, 2, 0.9))
        text(c, v, cx - 20, y1 + 60, font(SERIF_M, 64), fill(BRASS), "right")
        text(c, label, cx + 10, y1 + 52, font(MONO_M, 22), fill(BRASS), "left", track=0.12)
    text(c, "≈ $1.28 GOES TO McDONALD'S", 190, y0 + h + 120, font(MONO_M, 30), fill(PAPER), track=0.12)
    source(c, "McDONALD'S FORM 10-K 2025; FULL-YEAR 2025 RESULTS · AVERAGE ACROSS FRANCHISED SALES")


FRAMES = [("01_title", f_title), ("02_floor", f_floor), ("03_number", f_number), ("04_machine", f_machine),
          ("05_receipt", f_receipt), ("06_split", f_split)]


def stills():
    os.makedirs(OUT, exist_ok=True)
    paths = []
    for name, fn in FRAMES:
        s = skia.Surface(W, H)
        fn(s.getCanvas())
        p = os.path.join(OUT, name + ".jpg")
        s.makeImageSnapshot().save(p, skia.kJPEG, 92)
        paths.append(p)
    sheet = skia.Surface(W, H * 3 // 2)
    sc = sheet.getCanvas()
    sc.clear(col("#000000"))
    for i, p in enumerate(paths):
        img = skia.Image.open(p)
        sc.drawImageRect(img, skia.Rect.MakeXYWH((i % 2) * W / 2, (i // 2) * H / 2, W / 2, H / 2),
                         skia.SamplingOptions(skia.FilterMode.kLinear))
    sp = os.path.join(OUT, "sheet.jpg")
    sheet.makeImageSnapshot().save(sp, skia.kJPEG, 90)
    print(sp)


if __name__ == "__main__":
    stills() if len(sys.argv) < 2 or sys.argv[1] == "stills" else None
