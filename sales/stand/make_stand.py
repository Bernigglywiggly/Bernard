#!/usr/bin/env python3
"""Google review stand insert: a print-ready A6 card with the shop's own name, a tap target (the NFC sticker goes
behind it) and a QR code as the fallback for phones that don't tap. Slides into an A6 acrylic holder on the counter.

No Google logo or colours: the word only, so there is no trademark artwork on a card we sell.

    python3 sales/stand/make_stand.py "Stonefield Fish Bar" URL [--style ink|cream|green] [--out DIR]
    python3 sales/stand/make_stand.py --samples          # three colourways on one preview sheet (placeholder link)

URL is the shop's review link: `g.page/r/XXXX/review` from the owner's phone, or
`https://search.google.com/local/writereview?placeid=PLACE_ID`. Output: build/<slug>_<style>.png at 300 dpi with 3 mm
bleed (1311 x 1819 px; trim to 1240 x 1748). Needs skia and segno (~/youtube/.venv/bin/python has both).
"""
import math
import os
import re
import sys

import segno
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
FONT_DIRS = [os.path.join(REPO, d) for d in ("lab/shorts/fonts", "a01_v6/fonts", "lab/motion/public/fonts", "lab/ch2/fonts")]
DPI = 300
MM = DPI / 25.4
BLEED = round(3 * MM)
W, H = round(105 * MM), round(148 * MM)          # A6 trim size
M = 96                                           # safe margin inside the trim
STYLES = {
    "ink": dict(bg="#17181B", fg="#F4EFE4", soft="#A9A69E", acc="#E8B23A", panel="#F4EFE4", qr="#17181B"),
    "cream": dict(bg="#F4EFE4", fg="#1C1D20", soft="#6C6A64", acc="#C98A12", panel="#FFFFFF", qr="#1C1D20"),
    "green": dict(bg="#14402C", fg="#F4EFE4", soft="#A9C2B3", acc="#E8B23A", panel="#F4EFE4", qr="#14402C"),
}
STOP = {"OF", "THE", "AND", "&", "IN", "DI", "DE", "LA", "AT", "ON", "A"}
_TF = {}


def font(name, size):
    if name not in _TF:
        path = next(os.path.join(d, name + ".ttf") for d in FONT_DIRS if os.path.exists(os.path.join(d, name + ".ttf")))
        _TF[name] = skia.Typeface.MakeFromFile(path)
    f = skia.Font(_TF[name], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def col(hexs, a=1.0):
    h = hexs.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * a))


def fill(hexs, a=1.0):
    return skia.Paint(Color=col(hexs, a), AntiAlias=True)


def stroke(hexs, w, a=1.0):
    return skia.Paint(Color=col(hexs, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=skia.Paint.kRound_Cap)


def clean_name(n):
    n = re.sub(r"\s+(ltd\.?|limited)$", "", n.strip(), flags=re.I)
    return re.sub(r"\s+", " ", n).upper()


def fit_name(name, maxw, max_size, max_h):
    """Split the name over 1-3 lines and pick the biggest type; avoid lines that end on 'OF', 'THE', '&'."""
    f100 = font("Anton-Regular", 100)
    words = name.split()
    best = None
    for n in range(1, min(3, len(words)) + 1):
        cuts = [()]
        for _ in range(n - 1):
            cuts = [c + (k,) for c in cuts for k in range((c[-1] + 1 if c else 1), len(words))]
        for cut in cuts:
            idx = (0,) + cut + (len(words),)
            lines = [" ".join(words[idx[i]:idx[i + 1]]) for i in range(n)]
            size = min(max_size, maxw / (max(f100.measureText(ln) for ln in lines) / 100))
            block = n * 0.86 * size + (n - 1) * 0.14 * size
            if block > max_h:
                size *= max_h / block
            score = size * (1 - 0.06 * (n - 1))
            if any(ln.split()[-1] in STOP for ln in lines[:-1]):
                score *= 0.9
            if best is None or score > best[0] + 0.01:
                best = (score, size, lines)
    return best[1], best[2]


def centred(c, text, f, cx, y, paint, tracking=0.0):
    if not tracking:
        c.drawString(text, cx - f.measureText(text) / 2, y, f, paint)
        return
    widths = [f.measureText(ch) + tracking for ch in text]
    x = cx - (sum(widths) - tracking) / 2
    for ch, w in zip(text, widths):
        c.drawString(ch, x, y, f, paint)
        x += w


def star(cx, cy, r):
    p = skia.Path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.44
        (p.moveTo if i == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close()
    return p


def qr(c, url, x, y, size, s):
    """Dark modules on a light panel whatever the card colour: a QR reversed out of a dark card scans badly."""
    pad = size * 0.09
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, size, size), 28, 28, fill(s["panel"]))
    m = [list(r) for r in segno.make(url, error="m", micro=False).matrix]
    cell = (size - 2 * pad) / len(m)
    p = fill(s["qr"])
    for j, row in enumerate(m):
        for i, v in enumerate(row):
            if v:
                c.drawRect(skia.Rect.MakeXYWH(x + pad + i * cell, y + pad + j * cell, cell + 0.6, cell + 0.6), p)


def tap(c, cx, cy, r, s):
    c.drawCircle(cx, cy, r, stroke(s["acc"], 9))
    c.drawCircle(cx, cy, r - 26, stroke(s["fg"], 2.5, 0.35))
    for k, a in enumerate((0.95, 0.7, 0.45)):       # contactless waves, fanning to the right of a small dot
        rr = 44 + k * 38
        c.drawArc(skia.Rect.MakeLTRB(cx - 46 - rr, cy - rr, cx - 46 + rr, cy + rr), -42, 84, False, stroke(s["fg"], 15, a))
    c.drawCircle(cx - 46, cy, 13, fill(s["fg"]))


def draw(name, url, style="ink", lines=("ENJOYED IT?", "Leave us a Google review")):
    s = STYLES[style]
    surf = skia.Surface(W + 2 * BLEED, H + 2 * BLEED)
    c = surf.getCanvas()
    c.clear(col(s["bg"]))
    c.translate(BLEED, BLEED)
    cx = W / 2
    mono = "IBMPlexMono-500"

    centred(c, "THANK YOU FROM", font(mono, 30), cx, M + 34, fill(s["soft"]), 7)
    size, nl = fit_name(clean_name(name), W - 2 * M, 250, 430)
    block = len(nl) * 0.86 * size + (len(nl) - 1) * 0.14 * size
    y = M + 84 + (430 - block) / 2
    for ln in nl:
        y += 0.86 * size
        centred(c, ln, font("Anton-Regular", size), cx, y, fill(s["fg"]))
        y += 0.14 * size

    sy = M + 84 + 430 + 104
    for i in range(5):
        c.drawPath(star(cx + (i - 2) * 96, sy, 38), fill(s["acc"]))
    centred(c, lines[0], font(mono, 34), cx, sy + 118, fill(s["acc"]), 9)
    centred(c, lines[1], font("DMSerifDisplay-Regular", 84), cx, sy + 218, fill(s["fg"]))

    top = sy + 290
    c.drawLine(M, top, W - M, top, stroke(s["fg"], 2, 0.25))
    box = 400
    lx, rx, by = M + 20 + box / 2, W - M - 20 - box / 2, top + 64
    tap(c, lx, by + box / 2, box / 2 - 6, s)
    qr(c, url, rx - box / 2, by, box, s)
    centred(c, "TAP YOUR PHONE", font(mono, 34), lx, by + box + 66, fill(s["fg"]), 5)
    centred(c, "OR SCAN", font(mono, 34), rx, by + box + 66, fill(s["fg"]), 5)
    centred(c, "20 SECONDS  ·  IT MEANS A LOT TO US", font(mono, 26), cx, H - M + 14, fill(s["soft"]), 4)
    return surf.makeImageSnapshot()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:32]


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, skia.kPNG)
    return path


def samples(out):
    shops = [("Stonefield Fish Bar", "ink"), ("Little Seeds Bar & Kitchen", "cream"), ("The Ovilash Restaurant", "green")]
    imgs = [draw(n, "https://search.google.com/local/writereview?placeid=SAMPLE", st) for n, st in shops]
    k = 0.5
    cw, ch, gap = round((W + 2 * BLEED) * k), round((H + 2 * BLEED) * k), 40
    sheet = skia.Surface(3 * cw + 4 * gap, ch + 2 * gap)
    c = sheet.getCanvas()
    c.clear(col("#DAD6CE"))
    for i, im in enumerate(imgs):
        c.drawImageRect(im, skia.Rect.MakeXYWH(gap + i * (cw + gap), gap, cw, ch), skia.SamplingOptions(skia.CubicResampler.Mitchell()))
    return save(sheet.makeImageSnapshot(), os.path.join(out, "samples.png"))


def main(a):
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(HERE, "build")
    if "--samples" in a:
        print(samples(out))
        return
    style = a[a.index("--style") + 1] if "--style" in a else "ink"
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--style", "--out"))]
    if len(pos) != 2:
        sys.exit(__doc__)
    name, url = pos
    print(save(draw(name, url, style), os.path.join(out, f"{slug(name)}_{style}.png")))


if __name__ == "__main__":
    main(sys.argv[1:])
