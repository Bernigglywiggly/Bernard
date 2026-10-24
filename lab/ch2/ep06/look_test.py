#!/usr/bin/env python3
"""Style frames for a new look (user, 6 Oct: "more ASCII art, a slight futuristic twinge, ethereal light like Tron
Legacy, parts of Titanfall 2, the Fallen colourways from Destiny"; not the serif). One scene, the Atlantic crossing
from the Visa film, drawn three ways so he can pick. Nothing here is wired into the film yet.

    ~/youtube/.venv/bin/python lab/ch2/ep06/look_test.py      # -> build_est/look_<name>.png and look_sheet.jpg
"""
import json
import math
import os

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONTS = [os.path.join(REPO, d) for d in ("a01_v6/fonts", "lab/shorts/fonts", "lab/ch2/fonts")]
W, H = 1920, 1080
LON0, LON1, LAT0, LAT1 = -104.0, 14.0, 20.0, 60.0
LISBON, OHIO = (-9.14, 38.72), (-83.00, 39.96)
LOOKS = {
    # After the pollar.news references: black, white hairlines, tiny mono notes, a grotesque sans, ONE accent. Ours
    # differs by the accent (their yellow is theirs), the map drawn in type, and one line of light.
    # name: background, land glyphs, coast glyphs, ink (lines and type), accent (the one colour), dim text
    "ether": dict(bg="#040506", land="#20262B", coast="#6E7A82", light="#F2F5F7", acc="#5FF0E4", dim="#7B858C"),
    "dusk": dict(bg="#050409", land="#231F33", coast="#76709A", light="#F3F1FA", acc="#A98BFF", dim="#837E9C"),
    "devils": dict(bg="#060404", land="#2B2020", coast="#8A7470", light="#F7F2F0", acc="#FF6A4D", dim="#94827E"),
}
_TF = {}


def font(name, size):
    if name not in _TF:
        _TF[name] = skia.Typeface.MakeFromFile(next(os.path.join(d, name + ".ttf") for d in FONTS if os.path.exists(os.path.join(d, name + ".ttf"))))
    f = skia.Font(_TF[name], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def col(h, a=1.0):
    h = h.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * a))


def glow(h, a, blur):
    return skia.Paint(Color=col(h, a), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))


def text(c, s, x, y, f, h, a=1.0, track=0.0, align="left", halo=0.0):
    w = sum(f.measureText(ch) + track for ch in s) - track
    x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
    for paint in ([glow(h, 0.55 * a, halo)] if halo else []) + [skia.Paint(Color=col(h, a), AntiAlias=True)]:
        xx = x0
        for ch in s:
            c.drawString(ch, xx, y, f, paint)
            xx += f.measureText(ch) + track
    return w


def land_path():
    p = skia.Path()
    for ft in json.load(open(os.path.join(HERE, "data", "ne_110m_land.geojson")))["features"]:
        for ring in ft["geometry"]["coordinates"]:
            p.moveTo(*ring[0])
            for pt in ring[1:]:
                p.lineTo(*pt)
            p.close()
    return p


def draw(name):
    k = LOOKS[name]
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(col(k["bg"]))
    mx, my, mw, mh = 90, 150, 1740, 680
    cols, rows = 150, 44
    cw, ch = mw / cols, mh / rows
    land = land_path()
    grid = [[land.contains(LON0 + (i + 0.5) / cols * (LON1 - LON0), LAT1 - (j + 0.5) / rows * (LAT1 - LAT0)) for i in range(cols)] for j in range(rows)]
    f = font("IBMPlexMono-500", ch * 0.95)
    for j in range(rows):                                           # the map as type: sea is empty, land is glyphs
        for i in range(cols):
            if not grid[j][i]:
                continue
            edge = any(0 <= j + dj < rows and 0 <= i + di < cols and not grid[j + dj][i + di] for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            x, y = mx + i * cw, my + (j + 0.8) * ch
            if edge:
                c.drawString("#+%*"[(i * 7 + j * 3) % 4], x, y, f, skia.Paint(Color=col(k["coast"], 0.9), AntiAlias=True))
            else:
                c.drawString(".:·"[(i + j * 2) % 3], x, y, f, skia.Paint(Color=col(k["land"]), AntiAlias=True))

    def xy(lon, lat):
        return mx + (lon - LON0) / (LON1 - LON0) * mw, my + (LAT1 - lat) / (LAT1 - LAT0) * mh

    (x0, y0), (x1, y1) = xy(*LISBON), xy(*OHIO)
    p = skia.Path()
    for i in range(81):                                             # the crossing: the one line of light in the frame
        u = i / 80
        (p.moveTo if i == 0 else p.lineTo)(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - 200 * math.sin(math.pi * u))
    pt = glow(k["acc"], 0.45, 14)
    pt.setStyle(skia.Paint.kStroke_Style)
    pt.setStrokeWidth(6)
    c.drawPath(p, pt)
    c.drawPath(p, skia.Paint(Color=col(k["acc"]), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8))
    u = 0.62                                                        # the message, mid-ocean
    px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u - 200 * math.sin(math.pi * u)
    c.drawCircle(px, py, 20, glow(k["acc"], 0.5, 14))
    c.drawRect(skia.Rect.MakeXYWH(px - 9, py - 9, 18, 18), skia.Paint(Color=col(k["acc"]), AntiAlias=True))
    m = font("IBMPlexMono-400", 19)
    sans = font("InterTight-600", 30)
    ink = skia.Paint(Color=col(k["light"], 0.85), AntiAlias=True, StrokeWidth=1.2)
    for (x, y), a, b_, c_, sd in (((x0, y0), "A café, Lisbon", "38.72N  009.14W", "card tapped", -1),
                                  ((x1, y1), "A bank, Ohio", "39.96N  083.00W", "issued the card", 1)):
        c.drawCircle(x, y, 5, skia.Paint(Color=col(k["light"]), AntiAlias=True))
        c.drawCircle(x, y, 13, skia.Paint(Color=col(k["light"], 0.6), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2))
        c.drawLine(x, y + 13, x, y + 100, ink)
        note = b_ + "  ·  " + c_
        bw = max(sans.measureText(a), sum(m.measureText(ch) + 0.5 for ch in note)) + 28
        c.drawRect(skia.Rect.MakeXYWH(x + 1 if sd > 0 else x - bw - 1, y + 36, bw, 66), skia.Paint(Color=col(k["bg"], 0.92)))
        al = "left" if sd > 0 else "right"
        text(c, a, x + 14 * sd, y + 66, sans, k["light"], align=al)
        text(c, note, x + 14 * sd, y + 94, m, k["dim"], 1.0, 0.5, al)
    lab = "message out  ·  0.41 s"                                   # the accent as a highlight box, their one trick
    lw = sum(m.measureText(ch) + 0.5 for ch in lab)
    c.drawRect(skia.Rect.MakeXYWH(px + 22, py - 30, lw + 16, 28), skia.Paint(Color=col(k["acc"]), AntiAlias=True))
    text(c, lab, px + 30, py - 10, m, k["bg"], 1.0, 0.5)
    # the page: small notes top left, the figure bottom left, the caption centred low, hairlines only where they measure
    text(c, "How They Profit  ·  06", 90, 86, m, k["dim"], 1.0, 0.5)
    text(c, "illustration  ·  one card payment across a border  ·  not a real transaction", 90, 112, m, k["dim"], 1.0, 0.5)
    for j, lon in enumerate(range(-100, 0, 20)):                   # a longitude scale under the map, like a ruler
        x, _ = xy(lon, 0)
        c.drawLine(x, my + mh + 8, x, my + mh + 20, ink)
        text(c, f"{abs(lon):03d}{'W' if lon < 0 else 'E'}", x, my + mh + 44, m, k["dim"], 1.0, 0.5, "center")
    c.drawLine(mx, my + mh + 8, mx + mw, my + mh + 8, skia.Paint(Color=col(k["light"], 0.35), AntiAlias=True, StrokeWidth=1))
    text(c, "$17 trillion", 90, 1000, font("InterTight-600", 92), k["light"])
    text(c, "payments and cash volume on the network  ·  fiscal 2025  ·  Visa Form 10-K", 94, 1040, m, k["dim"], 1.0, 0.5)
    cell, gap = 15, 5                                                # $17 trillion as 170 cells of $100 billion
    gx, gy = W - 90 - 17 * (cell + gap) + gap, 1040 - 10 * (cell + gap) + gap
    for j in range(10):
        for i in range(17):
            c.drawRect(skia.Rect.MakeXYWH(gx + i * (cell + gap), gy + j * (cell + gap), cell, cell),
                       skia.Paint(Color=col(k["light"], 0.42), AntiAlias=True))
    lx, ly = gx + 16 * (cell + gap), gy + 9 * (cell + gap)          # Visa's $40 billion: four tenths of one cell
    c.drawRect(skia.Rect.MakeXYWH(lx, ly, cell, cell), skia.Paint(Color=col(k["bg"])))
    c.drawRect(skia.Rect.MakeXYWH(lx, ly + cell * 0.6, cell, cell * 0.4), skia.Paint(Color=col(k["acc"]), AntiAlias=True))
    c.drawCircle(lx + cell / 2, ly + cell * 0.8, 12, glow(k["acc"], 0.5, 10))
    text(c, "each cell $100 billion moved  ·  lit: what Visa keeps, to scale", W - 90, 1066, font("IBMPlexMono-400", 15), k["dim"], 1.0, 0.5, "right")
    return s.makeImageSnapshot()


def main():
    out = os.path.join(HERE, "build_est")
    os.makedirs(out, exist_ok=True)
    imgs = []
    for name in LOOKS:
        im = draw(name)
        im.save(os.path.join(out, f"look_{name}.png"), skia.kPNG)
        imgs.append((name, im))
    sh = skia.Surface(W, (H // 2 + 20) * len(imgs) // 1 + 20) if False else skia.Surface(W // 2 + 40, (H // 2 + 20) * len(imgs) + 20)
    c = sh.getCanvas()
    c.clear(col("#000000"))
    for i, (name, im) in enumerate(imgs):
        c.drawImageRect(im, skia.Rect.MakeXYWH(20, 20 + i * (H // 2 + 20), W // 2, H // 2), skia.SamplingOptions(skia.CubicResampler.Mitchell()))
    p = os.path.join(HERE, "look_sheet.png")
    sh.makeImageSnapshot().save(p, skia.kPNG)
    print(p)


if __name__ == "__main__":
    main()
