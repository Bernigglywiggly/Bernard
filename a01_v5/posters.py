"""Print textures (W1 PRESS), phone screens (W4 SIGNAL), floor grid and the brand
overlays for A01 v5. Pillow only. Writes PNGs + layout.json into $A01_BUILD/tex."""
import json
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from shots import DURATION, FONTS, OUTRO, SHOTS, TEX

BONE, CARD, INK = (236, 230, 218), (205, 200, 190), (12, 12, 13)
AMBER, STEEL, WHITE = (255, 178, 63), (138, 144, 160), (236, 237, 239)
PHOS, GROUND = (92, 255, 157), (7, 8, 11)
WORLD_SWATCH = {"STAIR": (86, 82, 76), "LOBBY": (11, 42, 107), "VOID": (7, 8, 11), "PRESS": BONE,
                "CLOUD": (245, 245, 245), "CHROME": (190, 198, 210), "SIGNAL": PHOS}
LAYOUT = {}


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name + ".ttf"), size)


def fit(text, name, size, width, d):
    """Largest size <= size at which text fits width."""
    while d.textlength(text, font=F(name, size)) > width and size > 8:
        size -= 4
    return size


def paper(w, h, col=BONE, seed=1, amt=5.0):
    a = np.full((h, w, 3), col, np.float32)
    a += np.random.default_rng(seed).normal(0, amt, (h, w, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def crops(d, w, h, m=46, l=40, c=INK, wd=3):
    for x, y, sx, sy in ((m, m, 1, 1), (w - m, m, -1, 1), (m, h - m, 1, -1), (w - m, h - m, -1, -1)):
        d.line([(x, y), (x + sx * l, y)], fill=c, width=wd)
        d.line([(x, y), (x, y + sy * l)], fill=c, width=wd)


def barcode(d, x, y, w, h, seed=7, c=INK):
    r, cx = random.Random(seed), x
    while cx < x + w:
        bw = r.choice((3, 3, 5, 8, 11))
        if r.random() > 0.3:
            d.rectangle([cx, y, cx + bw - 1, y + h], fill=c)
        cx += bw + r.choice((3, 4, 6))


def reg_mark(d, cx, cy, r=22, c=INK, wd=3):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=wd)
    d.line([(cx - r - 10, cy), (cx + r + 10, cy)], fill=c, width=wd)
    d.line([(cx, cy - r - 10), (cx, cy + r + 10)], fill=c, width=wd)


def header(d, w, items, y=86, c=INK):
    m = F("PlexMono-600", 34)
    d.text((80, y), items[0], font=m, fill=c)
    if items[1]:
        d.text((w // 2, y), items[1], font=m, fill=c, anchor="ma")
    d.text((w - 80, y), items[2], font=m, fill=c, anchor="ra")
    d.line([(80, y + 62), (w - 80, y + 62)], fill=c, width=3)


def plane_xy(px, py, w, h, ppu):
    """Pixel -> plane coords (plane centred on the origin, +y up)."""
    return round(px / ppu - w / ppu / 2, 4), round(h / ppu / 2 - py / ppu, 4)


def poster_90():
    W, H, ppu = 2400, 1600, 400
    im = paper(W, H, seed=11)
    d = ImageDraw.Draw(im)
    header(d, W, ["RELEASE LOG — 22.09.2026", "TWO MODELS / ONE NIGHT", "A01—W1"])
    x0, base = 110, 1150
    size = 860
    while True:  # "90" is a 3D object in Blender; the page only reserves its room
        w90 = d.textlength("90", font=F("Unbounded-900", size))
        s_min = int(size * 0.3)
        right = x0 + w90 + 60 + d.textlength("APART", font=F("Unbounded-800", int(size * 0.19)))
        if right < W - 90 and x0 + w90 + 60 + d.textlength("MIN", font=F("Unbounded-800", s_min)) < W - 90:
            break
        size -= 20
    xr = x0 + w90 + 60
    cap = size * 0.72
    d.text((xr, base - cap + s_min * 0.73), "MIN", font=F("Unbounded-800", s_min), fill=INK, anchor="ls")
    d.text((xr, base), "APART", font=F("Unbounded-800", int(size * 0.19)), fill=INK, anchor="ls")
    # the timeline: two drops, ninety minutes apart
    ty = 1335
    d.line([(110, ty), (W - 110, ty)], fill=INK, width=4)
    d.rectangle([700, ty - 9, 1500, ty + 9], fill=AMBER)
    mono = F("PlexMono-600", 32)
    for x, lab in ((700, "DROP 01"), (1500, "DROP 02")):
        d.line([(x, ty - 44), (x, ty + 44)], fill=INK, width=5)
        d.text((x, ty + 62), lab, font=mono, fill=INK, anchor="ma")
    d.text((1100, ty - 70), "GAP · 90:00", font=F("PlexMono-600", 44), fill=INK, anchor="ms")
    barcode(d, 1900, 1440, 400, 70, seed=3)
    reg_mark(d, 150, 1480)
    crops(d, W, H)
    im.save(os.path.join(TEX, "P90.png"))
    x, y = plane_xy(x0, base, W, H, ppu)
    LAYOUT["p90"] = dict(x=x, base=y, size=round(size / ppu, 4), w=round(w90 / ppu, 4),
                         tl_y=plane_xy(0, ty, W, H, ppu)[1])


def poster_update():
    W, H, ppu = 2400, 1600, 400
    im = paper(W, H, seed=12)
    d = ImageDraw.Draw(im)
    header(d, W, ["SETTINGS › GENERAL › SOFTWARE UPDATE", "", "A01—W1"])
    s = fit("+14", "Unbounded-900", 760, 1180, d)
    d.text((100, 1130), "+14", font=F("Unbounded-900", s), fill=INK, anchor="ls")
    x = 1420
    d.text((x, 470), "VERSION +14", font=F("Unbounded-800", fit("VERSION +14", "Unbounded-800", 96, 880, d)), fill=INK, anchor="ls")
    body = F("PlexMono-500", 46)
    for i, ln in enumerate(("Includes performance", "improvements and", "bug fixes.")):
        d.text((x, 580 + i * 64), ln, font=body, fill=INK)
    d.rectangle([x, 850, x + 860, 890], outline=INK, width=4)
    d.rectangle([x + 8, 858, x + 852, 882], fill=AMBER)
    d.text((x, 950), "100% · INSTALLED", font=F("PlexMono-600", 40), fill=INK)
    d.rounded_rectangle([x, 1030, x + 520, 1130], radius=50, outline=INK, width=5)
    d.text((x + 260, 1080), "RESTART LATER", font=F("PlexMono-600", 36), fill=INK, anchor="mm")
    d.text((100, 1330), "HOW MOST PEOPLE READ A BENCHMARK.", font=F("PlexMono-600", 40), fill=INK)
    barcode(d, 1900, 1440, 400, 70, seed=5)
    reg_mark(d, 2250, 1330)
    crops(d, W, H)
    im.save(os.path.join(TEX, "P_UPDATE.png"))


def poster_cool():
    W, H, ppu = 2400, 1600, 400
    im = paper(W, H, seed=13)
    d = ImageDraw.Draw(im)
    header(d, W, ["WHAT PEOPLE HEAR", "", "A01—W1"])
    s = fit("14%", "Unbounded-900", 900, 1500, d)
    d.text((100, 960), "14%", font=F("Unbounded-900", s), fill=INK, anchor="ls")
    s2 = fit("FASTER", "Unbounded-800", 260, 1500, d)
    d.text((100, 1270), "FASTER", font=F("Unbounded-800", s2), fill=INK, anchor="ls")
    d.text((100, 1420), "*RESULTS MAY VARY. THEY WILL.", font=F("PlexMono-600", 38), fill=INK)
    # the sticker
    cx, cy, r = 1940, 1030, 250
    st = Image.new("RGBA", (2 * r + 20, 2 * r + 20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.ellipse([10, 10, 2 * r + 10, 2 * r + 10], fill=AMBER + (255,))
    sd.text((r + 10, r + 10), "cool.", font=F("Unbounded-800", 128), fill=INK, anchor="mm")
    st = st.rotate(14, resample=Image.BICUBIC)
    im.paste(st, (cx - r - 10, cy - r - 10), st)
    barcode(d, 1900, 1440, 400, 70, seed=9)
    crops(d, W, H)
    im.save(os.path.join(TEX, "P_COOL.png"))
    x, y = plane_xy(cx, cy, W, H, ppu)
    LAYOUT["cool"] = dict(x=x, y=y)


def cards():
    W, H, ppu = 1200, 1600, 500
    for key, col, lines, done in (("CARD_A", CARD, ("THE ONE", "WHO STARTS", "THE GROUP", "PROJECT"), False),
                                  ("CARD_B", BONE, ("THE ONE", "WHO HANDS", "IT IN."), True)):
        im = paper(W, H, col=col, seed=21 if done else 22)
        d = ImageDraw.Draw(im)
        if done:
            d.rectangle([0, 0, W, 170], fill=AMBER)
        m = F("PlexMono-600", 34)
        d.text((80, 64), "CASE B" if done else "CASE A", font=m, fill=INK)
        d.text((W - 80, 44), "+14", font=F("Unbounded-900", 80), fill=INK, anchor="ra")
        s = min(fit(t, "Unbounded-800", 150, W - 160, d) for t in lines)
        for i, t in enumerate(lines):
            d.text((80, 470 + i * (s * 1.12)), t, font=F("Unbounded-800", s), fill=INK, anchor="ls")
        bx, by, b = 80, 1250, 120
        d.rectangle([bx, by, bx + b, by + b], outline=INK, width=8)
        if done:
            d.rectangle([bx + 14, by + 14, bx + b - 14, by + b - 14], fill=AMBER)
            d.line([(bx + 26, by + 64), (bx + 52, by + 92), (bx + 98, by + 30)], fill=INK, width=12)
        d.text((bx + b + 40, by + b // 2), "HANDED IN", font=F("PlexMono-600", 48), fill=INK, anchor="lm")
        barcode(d, 760, 1480, 360, 50, seed=11 if done else 12)
        crops(d, W, H, m=30, l=30)
        im.save(os.path.join(TEX, key + ".png"))
        LAYOUT[key] = dict(zip(("x", "y"), plane_xy(bx + b / 2, by + b / 2, W, H, ppu)))


def sparkle(d, cx, cy, r, c):
    pts = []
    for i in range(8):
        a = i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.22
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=c)


def screens():
    W, H = 600, 1200
    for key, big, small, seed in (("SCREEN_A", "GLOW\nUP", "MODEL A · NEW", 1), ("SCREEN_B", "GLOW\nUP", "MODEL B · NEW", 2),
                                  ("SCREEN_DONE", "UPDATED.", "NOTHING FEELS DIFFERENT", 3)):
        im = Image.new("RGB", (W, H), (6, 7, 9))
        d = ImageDraw.Draw(im)
        d.text((40, 40), "9:41", font=F("PlexMono-600", 34), fill=WHITE)
        d.ellipse([200, 210, 400, 410], outline=WHITE, width=10)
        spots = [(90, 480, 40), (505, 505, 56), (120, 930, 30), (470, 960, 48), (300, 1010, 26)]
        for i, (sx, sy, sr) in enumerate(spots):
            if (i + seed) % 5:
                sparkle(d, sx, sy - (60 if sy > 900 else 0), sr, WHITE)
        d.multiline_text((W // 2, 700), big, font=F("Unbounded-900", fit("GLOW", "Unbounded-900", 150, 520, d) if "\n" in big
                                                      else fit(big, "Unbounded-900", 150, 520, d)),
                         fill=WHITE, anchor="mm", align="center", spacing=10)
        d.text((W // 2, 1110), small, font=F("PlexMono-600", fit(small, "PlexMono-600", 34, 540, d)), fill=WHITE, anchor="mm")
        im.save(os.path.join(TEX, key + ".png"))


def grid():
    n, step = 2048, 256
    im = Image.new("RGB", (n, n), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(0, n, step):
        d.line([(i, 0), (i, n)], fill=(88, 108, 170), width=4)
        d.line([(0, i), (n, i)], fill=(88, 108, 170), width=4)
    im.save(os.path.join(TEX, "GRID.png"))


def signal_palette():
    """16x16 palette for ffmpeg paletteuse: ground, phosphor, and the brand amber."""
    cols = [GROUND, PHOS, AMBER]
    im = Image.new("RGB", (16, 16))
    im.putdata([cols[min(i // 86, 2)] for i in range(256)])
    im.save(os.path.join(TEX, "signal_palette.png"))


def hud(s):
    """Brand furniture on every shot: crop marks, chapter, world code, the mini drift line
    (where we are in the video) and the palette swatch whose last square is always amber."""
    W, H = 1920, 1080
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fg = INK if s.get("hud") == "ink" else WHITE          # same layout, adapted to bright worlds
    crops(d, W, H, m=44, l=26, c=fg + (150,), wd=2)
    m6, m5 = F("PlexMono-600", 22), F("PlexMono-500", 22)
    d.text((80, 60), "A01", font=m6, fill=fg + (225,))
    d.text((80 + d.textlength("A01  ", font=m6), 60), "FOURTEEN POINTS", font=m5, fill=fg + (130,))
    tw = d.textlength(s["world"], font=m6)
    d.text((W - 80, 60), s["world"], font=m6, fill=fg + (225,), anchor="ra")
    d.rectangle([W - 80 - tw - 26, 66, W - 80 - tw - 14, 78], fill=AMBER + (255,))
    # mini drift line + position
    x0, x1, y = 80, 330, 1012
    pts = [(x0 + i, y + 7 * math.sin(i / 28.0)) for i in range(0, x1 - x0 + 1, 2)]
    d.line(pts, fill=(fg if s.get("hud") == "ink" else STEEL) + (170,), width=2)
    frac = (s["t0"] + s["t1"]) / 2 / DURATION
    px = x0 + frac * (x1 - x0)
    py = y + 7 * math.sin((px - x0) / 28.0)
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=AMBER + (255,))
    # swatch: ground · world colour(s) · amber (the constant)
    names = [k for k in WORLD_SWATCH if k in s["world"]] or list(WORLD_SWATCH)
    sw = [GROUND] + [WORLD_SWATCH[k] for k in names] + [AMBER]
    for i, c in enumerate(reversed(sw)):
        xx = W - 80 - 16 - i * 22
        d.rectangle([xx, 1004, xx + 16, 1020], fill=c + (255,), outline=fg + (110,), width=1)
    im.save(os.path.join(TEX, f"HUD_{s['id']}.png"))


def caption(name, text, font, size, col, y, spacing=0):
    W, H = 1920, 1080
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = F(font, size)
    if spacing:
        text = (" " * spacing).join(text)
    d.text((W // 2 + 3, y + 4), text, font=f, fill=(0, 0, 0, 170), anchor="mm")
    d.text((W // 2, y), text, font=f, fill=col + (255,), anchor="mm")
    im.save(os.path.join(TEX, name))


def flatten_fonts():
    """Blender fills overlapping glyph contours as holes; write overlap-free copies (*-flat.ttf)."""
    try:
        from fontTools.ttLib import TTFont
        from fontTools.ttLib.removeOverlaps import removeOverlaps
    except ImportError:
        print("pip install fonttools skia-pathops  (else 3D text shows holes)")
        return
    for n in ("Unbounded-800", "Unbounded-900", "PlexMono-600"):
        out = os.path.join(FONTS, n + "-flat.ttf")
        if not os.path.exists(out):
            f = TTFont(os.path.join(FONTS, n + ".ttf"))
            removeOverlaps(f)
            f.save(out)


if __name__ == "__main__":
    os.makedirs(TEX, exist_ok=True)
    flatten_fonts()
    poster_90(); poster_update(); poster_cool(); cards(); screens(); grid(); signal_palette()
    for s in SHOTS + [OUTRO]:
        hud(s)
    caption("TXT_SAME.png", "SAME NUMBER.", "Unbounded-800", 92, WHITE, 800)
    caption("TXT_ANIMAL.png", "WHOLE DIFFERENT ANIMAL.", "Unbounded-800", 92, AMBER, 910)
    caption("TXT_HOME.png", "see you on the line.", "PlexMono-600", 40, AMBER, 880, spacing=1)
    caption("TXT_COMPLETELY.png", "COMPLETELY", "PlexMono-600", 46, AMBER, 930, spacing=1)
    caption("TXT_EMBARRASSINGLY.png", "EMBARRASSINGLY", "PlexMono-600", 46, AMBER, 930, spacing=1)
    json.dump(LAYOUT, open(os.path.join(TEX, "layout.json"), "w"), indent=1)
    print("textures ->", TEX)
