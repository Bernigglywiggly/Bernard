"""Thumbnails v2 (11 Oct 2026): one focal subject, 2-5 huge words, fluoro highlighter-on-black, one honest curiosity
device, a small channel mark. 1280x720 JPEGs, three variants per film for YouTube Test & Compare.

    ~/youtube/.venv/bin/python lab/tools/thumbs_v2.py                 # all films + feed sheet
    ~/youtube/.venv/bin/python lab/tools/thumbs_v2.py hormuz visa     # some films
    ~/youtube/.venv/bin/python lab/tools/thumbs_v2.py --feed          # just the feed-simulation sheet

Rules and picks: lab/tools/THUMBS.md. Every word on a thumbnail is a claim the film shows (CRAFT §9 rules 9-11);
the source line for each claim is in the RECIPES comments below.

Building blocks (reuse them for new films):
  subject(...)       a picture from the film, background crushed to black, graded to the channel's fluoro ramp,
                     rim light + outer glow in the channel colour (the "cut-out" look on black AI stills)
  photo_object(...)  an archive photo of a flat object (coupon, newspaper): cropped, inked, tilted, glowing edge
  hl_text(...)       black words on a streaky fluoro highlighter swipe
  glow_text(...)     solid words with neon bloom and a black keyline (reads on any picture)
  neon_text(...)     glass-tube outline words (events, danger)
  arrow / ring / xmark / strike   the drawn curiosity devices
  brand(...)         the channel's corner mark (repeat the mark, never the layout: CRAFT §9.14)
"""
import math
import os
import sys

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LAB = os.path.join(REPO, "lab")
CACHE = os.path.join(HERE, "cache_thumbs_v2")
W, H = 1280, 720
FONT_DIRS = [os.path.join(REPO, "a01_v6", "fonts"), os.path.join(LAB, "shorts", "fonts"), os.path.join(LAB, "ch2", "fonts"),
             os.path.expanduser("~/Library/Fonts/_brand"), "/Library/Fonts", "/System/Library/Fonts/Supplemental"]

# ------------------------------------------------------------------------------------------------ palettes
# One complementary fluoro pair per channel (+ one support ink). Hex values follow lab/maps/style/STYLE.md.
CHANNELS = {
    "curve": dict(name="THE CURVE", a="#3DFFF2", b="#FF2BD6", c="#E6FF2E", warn="#FF4A2A",
                  ramp=[(0.0, "#000000"), (0.22, "#14052E"), (0.45, "#7A1A9E"), (0.70, "#25C8E6"), (0.88, "#BFFFF8"), (1.0, "#FFFFFF")]),
    "curve_warm": dict(name="THE CURVE", a="#3DFFF2", b="#FF2BD6", c="#E6FF2E", warn="#FF4A2A",
                       ramp=[(0.0, "#050100"), (0.25, "#3A1406"), (0.5, "#B4501A"), (0.72, "#FFAA4A"), (0.88, "#FFF0C8"), (1.0, "#FFFFFF")]),
    "mc": dict(name="MONEY CRIMES", a="#FF2A2A", b="#FFFFFF", c="#FF7A1A", warn="#FF2A2A",
               ramp=[(0.0, "#000000"), (0.25, "#2A0303"), (0.5, "#9E1308"), (0.75, "#FF6A3A"), (0.92, "#FFE2D2"), (1.0, "#FFFFFF")]),
    "htp": dict(name="HOW THEY PROFIT", a="#C6FF1A", b="#FFE81A", c="#FFFFFF", warn="#FF3B2F",
                ramp=[(0.0, "#000000"), (0.3, "#0E1A02"), (0.6, "#5E8C00"), (0.85, "#D8FF5A"), (1.0, "#FFFFFF")]),
}


def rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)], np.float32)


def col(h, a=1.0):
    r, g, b = (int(v * 255) for v in rgb(h))
    return skia.Color(r, g, b, int(255 * a))


# ------------------------------------------------------------------------------------------------ fonts
_TF = {}


def _tag(s):
    return (ord(s[0]) << 24) | (ord(s[1]) << 16) | (ord(s[2]) << 8) | ord(s[3])


def font(name, size, wght=None, wdth=None):
    """name: file stem (e.g. 'Archivo', 'Anton-Regular', 'IBMPlexMono-500'). wght/wdth pick a static instance of a
    variable font (skia-python ignores the wght axis on clones, so the instance is cut once with fontTools and cached)."""
    key = (name, wght, wdth)
    if key not in _TF:
        path = next(os.path.join(d, name + ext) for d in FONT_DIRS for ext in (".ttf", ".otf")
                    if os.path.exists(os.path.join(d, name + ext)))
        if wght or wdth:
            inst = os.path.join(CACHE, f"{name}-w{wght}-d{wdth}.ttf")
            if not os.path.exists(inst):
                from fontTools.ttLib import TTFont
                from fontTools.varLib import instancer
                os.makedirs(CACHE, exist_ok=True)
                vf = TTFont(path)
                loc = {"wght": wght or 400}
                if wdth:
                    loc["wdth"] = wdth
                instancer.instantiateVariableFont(vf, loc, inplace=True)
                vf.save(inst)
            path = inst
        _TF[key] = skia.Typeface.MakeFromFile(path)
    f = skia.Font(_TF[key], size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setSubpixel(True)
    return f


def heavy(size, wdth=100):
    """The display face: Archivo Black at a chosen width (62 condensed .. 125 expanded)."""
    return font("Archivo", size, 900, wdth)


def mono(size):
    return font("IBMPlexMono-500", size)


def tw(s, f, track=0.0):
    return sum(f.measureText(ch) for ch in s) + track * (len(s) - 1)


def cap_h(f):
    return f.getMetrics().fCapHeight


def fit(s, size, maxw, wdth=100, track=0.0):
    """Largest heavy() font <= size whose text fits maxw."""
    while size > 10 and tw(s, heavy(size, wdth), track) > maxw:
        size -= 2
    return heavy(size, wdth)


# ------------------------------------------------------------------------------------------------ raster helpers
def blur(a, s):
    return cv2.GaussianBlur(a, (0, 0), s) if s > 0 else a


def smooth(lo, hi, x):
    t = np.clip((x - lo) / max(hi - lo, 1e-6), 0, 1)
    return t * t * (3 - 2 * t)


def ramp_map(L, stops):
    xs = np.array([s[0] for s in stops], np.float32)
    cs = np.stack([rgb(s[1]) for s in stops])
    out = np.zeros(L.shape + (3,), np.float32)
    for k in range(3):
        out[..., k] = np.interp(L, xs, cs[:, k])
    return out


def screen(a, b):
    return 1 - (1 - a) * (1 - b)


def load(path):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None:
        raise FileNotFoundError(path)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0


def lum(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def warp_into(img, crop, dst, angle=0.0, flip=False):
    """Map crop (x,y,w,h in source px) onto dst (x,y,w,h on the 1280x720 canvas), rotated by angle (deg) about dst centre.
    Returns the warped image and a coverage mask."""
    sx, sy, sw, sh = crop
    dx, dy, dw, dh = dst
    k = np.float32([[dw / sw, 0, dx - sx * dw / sw], [0, dh / sh, dy - sy * dh / sh]])
    if flip:
        k = np.float32([[-dw / sw, 0, dx + dw + sx * dw / sw], [0, dh / sh, dy - sy * dh / sh]])
    if angle:
        R = cv2.getRotationMatrix2D((dx + dw / 2, dy + dh / 2), angle, 1.0)
        k = (np.vstack([R, [0, 0, 1]]) @ np.vstack([k, [0, 0, 1]]))[:2].astype(np.float32)
    out = cv2.warpAffine(img, k, (W, H), flags=cv2.INTER_AREA if dw < sw else cv2.INTER_CUBIC, borderValue=0)
    m = cv2.warpAffine(np.ones(img.shape[:2], np.float32), k, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
    return out, m


def subject(base, path, crop, dst, ch, lo=0.08, hi=0.35, gamma=1.0, rim=1.0, glow=1.0, glow_col=None, rim_col=None,
            angle=0.0, flip=False, fade=None, gain=1.0, solid=None, floor=None, ambient=0.0):
    """A bright B&W AI still on black -> isolated, graded, rim-lit subject composited onto base.
    lo/hi: luminance band that becomes the cut-out alpha (background below lo goes to pure black).
    fade: (x0, x1) horizontal alpha fade (0 at x0 -> 1 at x1; x1 < x0 fades the other way).
    solid: a luminance threshold; when set, the alpha is the filled silhouette of everything brighter than it (for
    objects with dark mid-tones, e.g. a burger or a box, which would otherwise go see-through)."""
    img, cov = warp_into(load(path), crop, dst, angle, flip)
    L = np.clip(lum(img) * gain, 0, 1) ** gamma
    if solid == "none":
        # no cut-out: grade the whole still (its background is already black); the glow comes from its highlights
        a = cov * np.ones_like(L)
        L = np.maximum(smooth(lo, hi, L) * 0.85 + L * 0.15, 0)
    elif solid:
        m = (blur(L, 6) > solid).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
        n, lab_, stats, _ = cv2.connectedComponentsWithStats(m)
        if n > 1:
            keep = 1 + np.argsort(stats[1:, cv2.CC_STAT_AREA])[::-1][:1]
            m = np.isin(lab_, keep).astype(np.uint8)
        inv = (1 - m).astype(np.uint8)
        n2, lab2 = cv2.connectedComponents(inv)
        border = set(np.unique(np.concatenate([lab2[0], lab2[-1], lab2[:, 0], lab2[:, -1]])))
        holes = ~np.isin(lab2, list(border)) & (inv > 0)
        m = np.maximum(m, holes.astype(np.uint8))
        a = blur(m.astype(np.float32), 2.5) * cov
        L = np.maximum(smooth(lo, hi, L) * 0.85 + L * 0.15, ambient)
    else:
        a = smooth(lo, hi, L) * cov
    if floor:
        a = a * (1 - smooth(floor - 40, floor, np.arange(H, dtype=np.float32)[:, None]))
    if fade:
        x = np.arange(W, dtype=np.float32)[None, :]
        a = a * smooth(min(fade), max(fade), x) if fade[1] > fade[0] else a * (1 - smooth(min(fade), max(fade), x))
    graded = ramp_map(L, ch["ramp"]) * a[..., None]
    gc = rgb(glow_col or ch["a"])
    rc = rgb(rim_col or ch["b"])
    # outer glow: soft light around the silhouette, outside it
    src = smooth(0.45, 0.9, L) * a if solid == "none" else a
    halo = np.clip(blur(src, 22) * 1.15 - (0 if solid == "none" else a * 0.6), 0, 1) * glow
    halo2 = blur(src, 60) * 0.55 * glow
    out = screen(base, halo[..., None] * gc * 0.85)
    out = screen(out, halo2[..., None] * gc * 0.5)
    # rim light: the inside edge of the silhouette catches the second ink
    edge = np.clip(src - blur(src, 5), 0, 1) * 2.2 * rim
    if solid == "none":
        out = screen(out, graded)
    else:
        out = out * (1 - a[..., None]) + graded * a[..., None]
    out = screen(out, (edge[..., None] * rc).clip(0, 1))
    return out, a


def photo_object(base, path, crop, dst, angle, ch, paper="#F4ECDC", ink="#120707", glow=1.0, glow_col=None, contrast=(0.25, 0.8)):
    """A flat archive object (coupon, note, newspaper) on black: inked/papered duotone, tilted, glowing edge."""
    img = load(path)
    L = lum(img)
    L = smooth(contrast[0], contrast[1], L)
    duo = rgb(ink)[None, None] * (1 - L[..., None]) + rgb(paper)[None, None] * L[..., None]
    out_img, m = warp_into(duo, crop, dst, angle)
    gc = rgb(glow_col or ch["a"])
    shadow = blur(m, 18)
    out = base * (1 - 0.85 * shadow[..., None])
    out = screen(out, (np.clip(blur(m, 16) * 1.3 - m, 0, 1) * glow)[..., None] * gc)
    out = screen(out, (blur(m, 50) * 0.5 * glow)[..., None] * gc)
    out = out * (1 - m[..., None]) + out_img * m[..., None]
    return out, m


def vignette(a, k=0.35):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return a * (1 - k * np.clip(r - 0.6, 0, 1)[..., None])


def grain(a, amt=0.012, seed=3):
    rng = np.random.default_rng(seed)
    return np.clip(a + rng.normal(0, amt, (H, W, 1)).astype(np.float32), 0, 1)


def to_surface(a):
    s = skia.Surface(W, H)
    c = s.getCanvas()
    rgba = np.dstack([np.clip(a, 0, 1) * 255, np.full((H, W), 255)]).astype(np.uint8)
    c.drawImage(skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType), 0, 0)
    return s, c


def from_surface(s):
    return s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(np.float32) / 255.0


# ------------------------------------------------------------------------------------------------ vector devices
def P(**kw):
    p = skia.Paint(AntiAlias=True)
    for k, v in kw.items():
        getattr(p, "set" + k)(v)
    return p


def glowp(h, a, sigma, stroke=None):
    p = skia.Paint(AntiAlias=True, Color=col(h, a), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sigma))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def strokep(h, w, a=1.0):
    return skia.Paint(AntiAlias=True, Color=col(h, a), Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


def text_path(s, x, y, f, track=0.0):
    path = skia.Path()
    xx = x
    for ch in s:
        g = f.textToGlyphs(ch)
        gp = f.getPath(g[0]) if len(g) else None
        if gp is not None:
            gp.offset(xx, y)
            path.addPath(gp)
        xx += f.measureText(ch) + track
    return path


def ax(s, x, f, align, track=0.0):
    w = tw(s, f, track)
    return x - (w if align == "right" else w / 2 if align == "center" else 0), w


def glow_text(c, s, x, y, f, fill, glow=None, glow_a=0.75, glow_s=18, keyline=8, key_col="#000000", align="left", track=0.0, skew=0.0):
    """Big solid word: black keyline (separates it from any picture), neon bloom, solid fill."""
    x0, w = ax(s, x, f, align, track)
    path = text_path(s, x0, y, f, track)
    if skew:
        m = skia.Matrix()
        m.setSkew(skew, 0, x0, y)
        path.transform(m)
    if keyline:
        c.drawPath(path, glowp(key_col, 0.85, keyline * 1.6, keyline * 2.2))
        c.drawPath(path, strokep(key_col, keyline))
    if glow:
        c.drawPath(path, glowp(glow, glow_a, glow_s))
        c.drawPath(path, glowp(glow, glow_a * 0.6, glow_s * 3))
    c.drawPath(path, P(Color=col(fill)))
    return x0, w


def neon_text(c, s, x, y, f, h, align="left", track=0.0, width=6, core="#FFFFFF"):
    """Glass-tube outline letters: wide coloured bloom, coloured tube, white-hot core."""
    x0, w = ax(s, x, f, align, track)
    path = text_path(s, x0, y, f, track)
    c.drawPath(path, glowp("#000000", 0.9, 10, width * 4))
    c.drawPath(path, glowp(h, 0.55, 40, width * 3))
    c.drawPath(path, glowp(h, 0.9, 12, width * 2))
    c.drawPath(path, strokep(h, width))
    c.drawPath(path, strokep(core, width * 0.35, 0.95))
    return x0, w


def swipe(c, x, y, w, h, hx, seed=0, slope=-0.012, alpha=1.0):
    """Streaky marker swipe: rough ends, slight tilt, ink streaks. (x, y) is the top-left."""
    rng = np.random.default_rng(seed)
    path = skia.Path()
    n = 10
    top = [(x + w * i / n, y + rng.uniform(-2, 2) + slope * w * i / n) for i in range(n + 1)]
    bot = [(x + w * i / n, y + h + rng.uniform(-2, 2) + slope * w * i / n) for i in range(n, -1, -1)]
    path.moveTo(x - rng.uniform(4, 12), y + h * 0.5)
    for px_, py_ in top:
        path.lineTo(px_, py_)
    path.lineTo(x + w + rng.uniform(6, 16), y + h * 0.45 + slope * w)
    for px_, py_ in bot:
        path.lineTo(px_, py_)
    path.close()
    c.drawPath(path, glowp(hx, 0.45 * alpha, 22))
    c.drawPath(path, P(Color=col(hx, alpha)))
    # streaks: thin darker and lighter lines along the stroke, like a felt tip
    c.save()
    c.clipPath(path, doAntiAlias=True)
    for _ in range(int(h / 3)):
        yy = y + rng.uniform(0, h)
        a = rng.uniform(0.04, 0.14)
        tone = "#000000" if rng.random() < 0.6 else "#FFFFFF"
        c.drawLine(x - 20, yy, x + w + 20, yy + slope * w, strokep(tone, rng.uniform(0.8, 2.4), a))
    c.restore()


def hl_text(c, s, x, y, f, block, ink="#060606", pad=(22, 16), seed=0, align="left", track=0.0, slope=-0.010):
    """Black words on a highlighter swipe. y is the text baseline."""
    x0, w = ax(s, x, f, align, track)
    ch = cap_h(f)
    swipe(c, x0 - pad[0], y - ch - pad[1], w + 2 * pad[0], ch + 2 * pad[1], block, seed, slope)
    path = text_path(s, x0, y, f, track)
    c.drawPath(path, P(Color=col(ink)))
    return x0, w


def arrow(c, p0, p1, p2, h, width=14, head=44, glow=True):
    """Marker arrow along a quadratic curve p0 -> (control p1) -> p2, head at p2."""
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(*p1, *p2)
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    ang = math.atan2(dy, dx)
    hd = skia.Path()
    for s in (-1, 1):
        a = ang + math.pi + s * 0.5
        hd.moveTo(*p2)
        hd.lineTo(p2[0] + head * math.cos(a), p2[1] + head * math.sin(a))
    c.drawPath(path, glowp("#000000", 0.8, 8, width * 2.4))
    c.drawPath(hd, glowp("#000000", 0.8, 8, width * 2.4))
    if glow:
        c.drawPath(path, glowp(h, 0.7, 16, width * 1.6))
        c.drawPath(hd, glowp(h, 0.7, 16, width * 1.6))
    c.drawPath(path, strokep(h, width))
    c.drawPath(hd, strokep(h, width))


def ring(c, cx, cy, rx, ry, h, width=12, seed=0, rot=-8):
    """Hand-drawn marker ellipse with an overshoot."""
    rng = np.random.default_rng(seed)
    path = skia.Path()
    a0 = math.radians(-120)
    n = 80
    drift = rng.uniform(0.03, 0.07)
    for i in range(n + 1):
        t = a0 + (2 * math.pi + 0.55) * i / n
        k = 1 + drift * i / n
        x = rx * k * math.cos(t)
        y = ry * k * math.sin(t)
        r = math.radians(rot)
        X, Y = cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)
        path.moveTo(X, Y) if i == 0 else path.lineTo(X, Y)
    c.drawPath(path, glowp("#000000", 0.8, 8, width * 2.4))
    c.drawPath(path, glowp(h, 0.75, 16, width * 1.8))
    c.drawPath(path, strokep(h, width))


def xmark(c, cx, cy, size, h, width=26):
    path = skia.Path()
    s = size / 2
    path.moveTo(cx - s, cy - s * 0.92)
    path.lineTo(cx + s, cy + s)
    path.moveTo(cx + s * 0.95, cy - s)
    path.lineTo(cx - s, cy + s * 0.95)
    c.drawPath(path, glowp("#000000", 0.85, 10, width * 2.2))
    c.drawPath(path, glowp(h, 0.8, 22, width * 1.6))
    c.drawPath(path, strokep(h, width))


def strike(c, x0, y0, x1, y1, h, width=18):
    path = skia.Path()
    path.moveTo(x0, y0)
    path.lineTo(x1, y1)
    c.drawPath(path, glowp("#000000", 0.85, 8, width * 2.2))
    c.drawPath(path, glowp(h, 0.8, 16, width * 1.6))
    c.drawPath(path, strokep(h, width))


def brand(c, ch_key, corner="tl"):
    """Small channel mark, top-left by default (bottom-right is under YouTube's duration badge)."""
    ch = CHANNELS[ch_key]
    x, y = (28, 26) if corner == "tl" else (28, H - 70)
    if ch_key == "curve":
        # the avatar's mark: a cyan rising curve ending in a white dot
        p = skia.Path()
        p.moveTo(x + 4, y + 38)
        p.cubicTo(x + 22, y + 40, x + 34, y + 24, x + 40, y + 4)
        c.drawPath(p, glowp("#000000", 0.8, 6, 16))
        c.drawPath(p, glowp(ch["a"], 0.7, 8, 10))
        c.drawPath(p, strokep(ch["a"], 6.5))
        c.drawCircle(x + 40, y + 4, 6.5, P(Color=col("#FFFFFF")))
        f = mono(19)
        c.drawString("THE CURVE", x + 54, y + 30, f, glowp("#000000", 0.9, 5))
        c.drawString("THE CURVE", x + 54, y + 30, f, P(Color=col("#FFFFFF", 0.92)))
    else:
        # the avatar's mark: serif initials in a ring (gold on red for MC, gold for HTP)
        ring_c = "#E02A20" if ch_key == "mc" else "#D9B45A"
        ini = "MC" if ch_key == "mc" else "HTP"
        cx, cy, r = x + 24, y + 22, 24
        c.drawCircle(cx, cy, r + 6, glowp("#000000", 0.9, 6))
        c.drawCircle(cx, cy, r, P(Color=col("#0B0B0B")))
        c.drawCircle(cx, cy, r, strokep(ring_c, 3.2))
        f = font("IBMPlexSerif-600", 19 if ini == "MC" else 15)
        c.drawString(ini, cx - tw(ini, f) / 2, cy + 7, f, P(Color=col("#E8C873")))
        f2 = mono(17)
        c.drawString(ch["name"], cx + r + 12, cy + 7, f2, glowp("#000000", 0.9, 5))
        c.drawString(ch["name"], cx + r + 12, cy + 7, f2, P(Color=col("#FFFFFF", 0.9)))


def small(c, s, x, y, h="#FFFFFF", size=22, a=0.9, align="left"):
    f = mono(size)
    x0, _ = ax(s, x, f, align, 1.0)
    c.drawString(s, x0, y, f, glowp("#000000", 0.95, 6))
    xx = x0
    for chh in s:
        c.drawString(chh, xx, y, f, P(Color=col(h, a)))
        xx += f.measureText(chh) + 1.0


def save(a, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = cv2.cvtColor((np.clip(a, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    q = 93
    while True:
        cv2.imwrite(out, img, [cv2.IMWRITE_JPEG_QUALITY, q, cv2.IMWRITE_JPEG_OPTIMIZE, 1])
        if os.path.getsize(out) < 1_900_000 or q < 60:
            break
        q -= 5
    print(f"wrote {os.path.relpath(out, REPO)}  {os.path.getsize(out) / 1e6:.2f} MB")


def finish(s, out, vig=0.3):
    a = from_surface(s)
    save(grain(vignette(a, vig), 0.010), out)


def black():
    return np.zeros((H, W, 3), np.float32)


# ------------------------------------------------------------------------------------------------ Hormuz map plate
def hormuz_plate():
    """The film's style-F map of the narrows (contours, country-ink coast, oil flow, attack pins) WITHOUT labels,
    rendered once at 1920x1080 through lab/maps/style/style_frames.py and cached."""
    path = os.path.join(CACHE, "hormuz_plate.png")
    if os.path.exists(path):
        return load(path)
    os.makedirs(CACHE, exist_ok=True)
    sys.path.insert(0, os.path.join(LAB, "maps", "style"))
    import style_frames as sf  # noqa: E402
    s = sf.surface()
    c = s.getCanvas()
    sf.topo_layer(c, alpha=0.30, wscale=1.1, labels=False, mono_hex="#9FB4BF")
    T = sf.snap(s)
    s = sf.surface()
    c = s.getCanvas()
    sf.draw_glyphs(c, sf.cty_hex, 0.95, 0.40, 0.16)
    sf.border_dash(c, 0.5)
    sf.coast_stroke(c, sf.cty_hex, 2.2, 0.85)
    M = sf.snap(s)
    routes = sf.flow_routes()
    FL = sf.flow_frame(3.0, routes, np.zeros((sf.H, sf.W, 3), np.float32), n_scale=1.25, stops=sf.OIL_STOPS, in_hex="#9C8C1C")
    base = sf.screen(sf.screen(T, M), FL)
    out = sf.screen(base, sf.bloom(M * 0.7, ((3, 0.5), (12, 0.3), (36, 0.15))))
    out = sf.screen(out, sf.bloom(FL * 0.9, ((4, 0.5), (16, 0.35), (50, 0.2))))
    cv2.imwrite(path, cv2.cvtColor((np.clip(out, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))
    hits = [sf.px(lo, la) for lo, la in sf.OCT_HITS]
    np.save(os.path.join(CACHE, "hormuz_hits.npy"), np.array(hits))
    return out.astype(np.float32)


def hormuz_on(base, crop, gain=1.0):
    """Place a crop (x, y, w, h in the 1920x1080 plate) full-bleed."""
    plate = hormuz_plate()
    img, _ = warp_into(plate, crop, (0, 0, W, H))
    return screen(base, np.clip(img * gain, 0, 1))


def plate_xy(pt, crop):
    """Plate pixel -> thumbnail pixel for a full-bleed crop."""
    x, y, w, h = crop
    return ((pt[0] - x) * W / w, (pt[1] - y) * H / h)


# ------------------------------------------------------------------------------------------------ Visa card (drawn, no logo)
def card(c, cx, cy, w, angle, sliver="#C6FF1A", glow=True):
    """A generic payment card drawn in code: no brand, no logo. The lit sliver on the right edge is the network's cut."""
    h = w * 0.63
    c.save()
    c.translate(cx, cy)
    c.rotate(angle)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.055, w * 0.055)
    c.drawRRect(r, glowp("#000000", 0.9, 30))
    if glow:
        c.drawRRect(r, glowp(sliver, 0.35, 60))
    c.drawRRect(r, P(Shader=skia.GradientShader.MakeLinear([(-w / 2, -h / 2), (w / 2, h / 2)], [col("#22262B"), col("#07090B")])))
    # chip
    cr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w * 0.36, -h * 0.16, w * 0.15, h * 0.2), 10, 10)
    c.drawRRect(cr, strokep("#E8EAEC", w * 0.008))
    # contactless arcs
    for k in range(3):
        rr = w * (0.035 + 0.028 * k)
        c.drawArc(skia.Rect.MakeXYWH(-w * 0.16 - rr, -h * 0.06 - rr, 2 * rr, 2 * rr), -50, 100, False, strokep("#E8EAEC", w * 0.008))
    # number dots
    for g in range(4):
        for d in range(4):
            c.drawCircle(-w * 0.38 + g * w * 0.17 + d * w * 0.032, h * 0.22, w * 0.009, P(Color=col("#D8DADC")))
    # the lit sliver
    c.save()
    c.clipRRect(r, doAntiAlias=True)
    sx = w / 2 - w * 0.09
    c.drawRect(skia.Rect.MakeXYWH(sx, -h / 2, w * 0.09, h), glowp(sliver, 0.9, 20))
    c.drawRect(skia.Rect.MakeXYWH(sx, -h / 2, w * 0.09, h), P(Color=col(sliver)))
    c.restore()
    c.drawRRect(r, strokep("#F2F4F5", w * 0.007, 0.95))
    c.restore()
    # return the sliver centre in canvas coordinates
    a = math.radians(angle)
    lx, ly = w / 2 - w * 0.045, 0
    return cx + lx * math.cos(a) - ly * math.sin(a), cy + lx * math.sin(a) + ly * math.cos(a), h


# ================================================================================================ RECIPES
AI = {k: os.path.join(LAB, p) for k, p in {
    "lf01": "curvelf/lf01_escape/src/ai", "lf02": "curvelf/lf02_price/src/ai", "lf03": "curvelf/lf03_held/src/ai",
    "mc02": "curvelf/mc02_ponzi/src/ai", "mc02p": "curvelf/mc02_ponzi/src/photo"}.items()}
OUT = {
    "hormuz": os.path.join(LAB, "maps/hormuz/out"), "lf01": os.path.join(LAB, "curvelf/lf01_escape/out"),
    "lf02": os.path.join(LAB, "curvelf/lf02_price/out"), "lf03": os.path.join(LAB, "curvelf/lf03_held/out"),
    "visa": os.path.join(LAB, "ch2/ep06/out"), "mc02": os.path.join(LAB, "curvelf/mc02_ponzi/out")}
OLD = {
    "hormuz": "maps/hormuz/out/thumb_8ships.jpg", "lf01": "curvelf/lf01_escape/out/thumbflow_a.jpg",
    "lf02": "curvelf/lf02_price/out/thumbflow_a.jpg", "lf03": "curvelf/lf03_held/out/thumbflow_a.jpg",
    "visa": "ch2/ep06/thumb_D.png", "mc02": "curvelf/mc02_ponzi/out/thumbflow_a.jpg"}
TITLES = {
    "hormuz": "Hormuz Is Closed. The Oil Isn't.", "lf01": "The AI That Escaped", "lf02": "The Price of Thinking",
    "lf03": "Too Dangerous to Release", "visa": "Visa Isn't a Credit Card Company", "mc02": "The Original Ponzi Scheme"}


def o(film, v):
    return os.path.join(OUT[film], f"thumbs_v2_{v}.jpg")


# ---------------------------------------------------------------- HORMUZ (The Curve)
# Claims: "8" = ships that crossed on 8 Oct 2026 (Windward), on screen 0:00; "125" = large ships a day before 28 Feb,
# on screen 0:11; "CLOSED TO SHIPS · OPEN TO OIL" on screen 0:17 (POST.md).
HZ_CROP = (330, 330, 1000, 562)   # the bend round Musandam, lanes + oil route


def dim_region(a, fn):
    """Multiply the picture by a per-pixel factor fn(x, y) (arrays) to clear room for words."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    return a * fn(x, y)[..., None]


def hormuz_a():
    ch = CHANNELS["curve"]
    crop = (230, 300, 1000, 562)
    base = hormuz_on(black(), crop, 1.3)
    base = dim_region(base, lambda x, y: 0.35 + 0.65 * (1 - smooth(820, 980, x) * (1 - smooth(520, 700, y) * 0)))
    s, c = to_surface(base)
    f8 = heavy(560, 100)
    glow_text(c, "8", 1240, 560, f8, ch["c"], glow=ch["c"], glow_a=0.9, glow_s=30, keyline=12, align="right")
    hl_text(c, "SHIPS", 1222, 670, heavy(96, 100), ch["b"], ink="#0A0008", seed=4, align="right")
    f125 = heavy(150, 100)
    x0, w = glow_text(c, "125", 50, 600, f125, "#FFFFFF", keyline=8)
    strike(c, x0 - 10, 600 - 8, x0 + w + 10, 600 - cap_h(f125) + 8, ch["warn"], 12)
    glow_text(c, "A DAY BEFORE", 56, 662, heavy(34, 100), "#FFFFFF", keyline=6)
    brand(c, "curve")
    finish(s, o("hormuz", "a"))


def hormuz_b():
    ch = CHANNELS["curve"]
    crop = (250, 200, 850, 478)
    base = hormuz_on(black(), crop, 1.3)
    base = dim_region(base, lambda x, y: 0.28 + 0.72 * smooth(250, 360, y))
    s, c = to_surface(base)
    orange = "#FF6A1A"
    neon_text(c, "CLOSED", W / 2, 200, heavy(190, 100), orange, align="center", width=7)
    hl_text(c, "TO SHIPS", W / 2, 312, heavy(70, 100), "#FFFFFF", seed=2, align="center")
    # the oil route still bends round Musandam: the arrow lands on it
    tx, ty = plate_xy((600, 487), crop)
    hl_text(c, "OIL?", 1010, 560, heavy(96, 100), ch["c"], ink="#0B0D00", seed=6)
    arrow(c, (1000, 520), (880, 420), (tx + 40, ty - 6), ch["c"], width=13, head=40)
    brand(c, "curve")
    finish(s, o("hormuz", "b"))


def hormuz_c():
    ch = CHANNELS["curve"]
    crop = (150, 230, 950, 534)
    base = hormuz_on(black(), crop, 1.35)
    base = dim_region(base, lambda x, y: 1 - 0.7 * (1 - smooth(560, 760, x)) * (1 - smooth(380, 520, y)))
    s, c = to_surface(base)
    hl_text(c, "OPEN", 60, 205, heavy(170, 100), ch["c"], ink="#0B0D00", seed=1)
    hl_text(c, "TO OIL", 60, 395, heavy(150, 100), ch["c"], ink="#0B0D00", seed=9)
    brand(c, "curve", corner="bl")
    finish(s, o("hormuz", "c"))



# ---------------------------------------------------------------- LF01 THE AI THAT ESCAPED (The Curve)
# Claims: "700" AI agents joined the attack (script 0:3x, split card "700 JOINED THE ATTACK"); "IT GOT OUT": "This is how
# they got out" + sandbox "That, at least, was the plan" (cold open); "NOT A PERSON": "It wasn't a person." (cold open).
def lf01_a():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf01"], "s28.png"), (900, 120, 1788, 1011), (330, 0, 1270, 720), ch,
                      lo=0.10, hi=0.42, gamma=0.9, rim=1.1, glow=1.0)
    s, c = to_surface(base)
    glow_text(c, "700", 48, 330, heavy(280, 100), ch["c"], glow=ch["c"], glow_a=0.8, glow_s=24, keyline=10)
    hl_text(c, "AI AGENTS", 62, 450, heavy(84, 100), "#FFFFFF", seed=3)
    hl_text(c, "ATTACKED", 62, 580, heavy(98, 100), ch["b"], ink="#0A0008", seed=5)
    brand(c, "curve")
    finish(s, o("lf01", "a"))


def lf01_b():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf01"], "s04.png"), (560, 200, 1600, 1250), (440, 40, 860, 672), ch,
                      lo=0.02, hi=0.8, gamma=0.9, rim=0.9, glow=1.3, glow_col=ch["a"], solid="none")
    s, c = to_surface(base)
    glow_text(c, "IT GOT", 50, 230, heavy(150, 100), "#FFFFFF", keyline=9)
    glow_text(c, "OUT", 50, 420, heavy(220, 108), ch["a"], glow=ch["a"], glow_a=0.85, glow_s=22, keyline=10)
    # arrow at the light leaking from the lid seam
    arrow(c, (770, 470), (680, 640), (420, 560), ch["c"], width=14, head=42)
    brand(c, "curve")
    finish(s, o("lf01", "b"))


def lf01_c():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf01"], "s23.png"), (640, 60, 1400, 1288), (460, 0, 820, 720), ch,
                      lo=0.08, hi=0.40, gamma=0.9, rim=1.0, glow=1.2)
    s, c = to_surface(base)
    xmark(c, 870, 400, 420, ch["warn"], 34)
    glow_text(c, "NOT A", 50, 250, heavy(130, 100), "#FFFFFF", keyline=9)
    hl_text(c, "PERSON", 62, 420, heavy(130, 100), ch["c"], ink="#0B0D00", seed=7)
    small(c, "HUGGING FACE · JULY 2026", 56, 520, ch["a"], 24, 0.95)
    brand(c, "curve")
    finish(s, o("lf01", "c"))


# ---------------------------------------------------------------- LF02 THE PRICE OF THINKING (The Curve)
# Claims: "≈500 novels read for one Big Mac" (chapter In Big Macs, 2:56); "$60 -> $0.06 per million tokens, 1,000×"
# (chapter A Thousand Times, 1:45); "$1 trillion+" data-centre spending 2026 (cold open).
def lf02_a():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf02"], "p06.png"), (290, 30, 1600, 1440), (560, 0, 800, 720),
                      CHANNELS["curve_warm"], lo=0.02, hi=0.75, gamma=0.9, rim=1.0, glow=1.2, glow_col=ch["a"], rim_col=ch["a"], solid="none", floor=700)
    s, c = to_surface(base)
    glow_text(c, "500", 44, 300, heavy(270, 100), "#FFFFFF", glow=ch["a"], glow_a=0.8, glow_s=24, keyline=10)
    hl_text(c, "NOVELS", 58, 440, heavy(112, 100), ch["c"], ink="#0B0D00", seed=2)
    hl_text(c, "= 1 BIG MAC", 58, 570, heavy(66, 100), ch["b"], ink="#0A0008", seed=5)
    arrow(c, (470, 640), (560, 700), (640, 610), ch["a"], width=12, head=36)
    brand(c, "curve")
    finish(s, o("lf02", "a"))


def lf02_b():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf02"], "p01.png"), (1000, 0, 900, 1520), (820, -40, 470, 794), ch,
                      lo=0.06, hi=0.38, gamma=0.9, rim=1.0, glow=1.2)
    s, c = to_surface(base)
    f = heavy(200, 100)
    x0, w = glow_text(c, "$60", 52, 260, f, "#FFFFFF", keyline=9)
    strike(c, x0 - 12, 260 - 12, x0 + w + 12, 260 - cap_h(f) + 12, ch["warn"], 14)
    glow_text(c, "6¢", 40, 560, heavy(330, 100), ch["c"], glow=ch["c"], glow_a=0.85, glow_s=26, keyline=10)
    hl_text(c, "1,000× CHEAPER", 490, 640, heavy(60, 100), ch["b"], ink="#0A0008", seed=3)
    small(c, "PER MILLION TOKENS · 2021 → 2024", 496, 698, "#FFFFFF", 20, 0.9)
    brand(c, "curve")
    finish(s, o("lf02", "b"))


def lf02_c():
    ch = CHANNELS["curve"]
    # before -> after split: left the chip (cheaper), right the data centre (the bill)
    base, _ = subject(black(), os.path.join(AI["lf02"], "p04.png"), (500, 100, 1500, 1300), (0, 0, 640, 720), ch,
                      lo=0.08, hi=0.45, gamma=1.0, rim=0.7, glow=0.6, glow_col=ch["a"], fade=(640, 560))
    base, _ = subject(base, os.path.join(AI["lf02"], "p12.png"), (700, 150, 1300, 1300), (640, 0, 640, 720), ch,
                      lo=0.06, hi=0.40, gamma=0.9, rim=0.7, glow=0.6, glow_col=ch["b"], fade=(640, 720))
    s, c = to_surface(base)
    c.drawLine(640, 0, 640, H, glowp("#FFFFFF", 0.8, 6, 6))
    c.drawLine(640, 0, 640, H, strokep("#FFFFFF", 3))
    hl_text(c, "1,000×", 320, 290, fit("1,000×", 150, 500), ch["a"], align="center", seed=1)
    glow_text(c, "CHEAPER", 320, 440, fit("CHEAPER", 110, 540), "#FFFFFF", align="center", keyline=9)
    hl_text(c, "$1 TRILLION", 960, 290, fit("$1 TRILLION", 110, 500, wdth=80), ch["b"], ink="#0A0008", align="center", seed=4)
    glow_text(c, "BILL?", 960, 470, heavy(170, 100), "#FFFFFF", align="center", keyline=10, glow=ch["b"], glow_a=0.5)
    brand(c, "curve")
    finish(s, o("lf02", "c"))


# ---------------------------------------------------------------- LF03 TOO DANGEROUS TO RELEASE (The Curve)
# Claims: OpenAI "cancelled the launch" of GPT-6.1 Astra (0:3x, card "CANCELLED."); "29%" of runs slipped malicious code
# into an open-source project, UK AISI simulated test (chapter The Test, 1:45); "acted without asking permission" (cold open).
def lf03_a():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf03"], "c01.png"), (380, 80, 1500, 1360), (120, 0, 800, 720), ch,
                      lo=0.05, hi=0.40, gamma=0.85, rim=0.9, glow=1.0)
    s, c = to_surface(base)
    # rubber-stamp CANCELLED across the vault
    c.save()
    c.rotate(-9, 640, 360)
    f = heavy(150, 96)
    wv = tw("CANCELLED", f)
    rx = 640 - wv / 2 - 34
    rr = skia.Rect.MakeXYWH(rx, 230, wv + 68, 210)
    c.drawRect(rr, glowp("#000000", 0.7, 20))
    c.drawRect(rr, glowp(ch["warn"], 0.6, 26, 14))
    c.drawRect(rr, strokep(ch["warn"], 12))
    glow_text(c, "CANCELLED", 640, 390, f, ch["warn"], align="center", keyline=8, glow=ch["warn"], glow_a=0.5)
    c.restore()
    hl_text(c, "GPT-6.1", 70, 610, heavy(96, 100), "#FFFFFF", seed=2)
    small(c, "OPENAI · 28 SEP 2026", 74, 668, ch["a"], 22, 0.95)
    brand(c, "curve")
    finish(s, o("lf03", "a"))


def lf03_b():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf03"], "h04.png"), (1100, 0, 1588, 1400), (600, 0, 740, 720), ch,
                      lo=0.08, hi=0.45, gamma=0.9, rim=1.0, glow=1.0, glow_col=ch["b"])
    s, c = to_surface(base)
    glow_text(c, "29%", 40, 330, heavy(290, 100), ch["c"], glow=ch["c"], glow_a=0.85, glow_s=26, keyline=10)
    hl_text(c, "PLANTED BAD CODE", 58, 450, fit("PLANTED BAD CODE", 84, 640), "#FFFFFF", seed=4)
    hl_text(c, "IN A TEST", 58, 580, heavy(96, 100), ch["b"], ink="#0A0008", seed=8)
    brand(c, "curve")
    finish(s, o("lf03", "b"))


def lf03_c():
    ch = CHANNELS["curve"]
    base, _ = subject(black(), os.path.join(AI["lf03"], "h02.png"), (200, 180, 2300, 1300), (0, 120, 1280, 600), ch,
                      lo=0.07, hi=0.40, gamma=0.9, rim=1.1, glow=1.1)
    s, c = to_surface(base)
    f = heavy(140, 100)
    x0, w = glow_text(c, "IT DIDN'T", 44, 170, f, "#FFFFFF", keyline=9)
    hl_text(c, "ASK", x0 + w + 60, 170, f, ch["c"], ink="#0B0D00", seed=3)
    ring(c, 790, 400, 190, 95, ch["b"], 12, seed=2, rot=-4)
    brand(c, "curve", corner="bl")
    finish(s, o("lf03", "c"))


# ---------------------------------------------------------------- VISA (How They Profit)
# Claims (FACTS.md, Visa FY2025 8-K/10-K): ≈24¢ of every $100 of volume is Visa's net revenue; net income $20.1B; Visa
# lends none of the money; $17 trillion total payments and cash volume. All on screen in the film (chapters 1:02-2:45).
def visa_a():
    ch = CHANNELS["htp"]
    s, c = to_surface(black())
    sx, sy, ch_h = card(c, 300, 420, 500, -9, ch["a"])
    ring(c, sx - 4, sy, 62, ch_h * 0.66, ch["warn"], 11, seed=1, rot=-9)
    glow_text(c, "24¢", 1250, 340, heavy(300, 100), ch["a"], glow=ch["a"], glow_a=0.8, glow_s=24, keyline=10, align="right", track=16)
    hl_text(c, "OF EVERY $100", 1225, 480, heavy(66, 100), ch["b"], seed=3, align="right")
    arrow(c, (760, 560), (660, 660), (sx + 74, sy + 90), ch["warn"], width=13, head=40)
    brand(c, "htp")
    finish(s, o("visa", "a"))


def visa_b():
    ch = CHANNELS["htp"]
    base = black()
    base[:, 640:] = rgb("#0B1200")
    s, c = to_surface(base)
    card(c, 330, 620, 360, -8, "#3A3F44", glow=False)
    sx, sy, _ = card(c, 960, 620, 360, 8, ch["a"])
    c.drawLine(640, 0, 640, H, strokep("#FFFFFF", 3, 0.8))
    glow_text(c, "LENDS", 320, 175, heavy(92, 100), "#FFFFFF", align="center", keyline=8)
    glow_text(c, "$0", 320, 395, heavy(230, 100), "#FFFFFF", align="center", keyline=10)
    glow_text(c, "KEEPS", 960, 175, heavy(92, 100), ch["a"], align="center", keyline=8)
    glow_text(c, "$20B", 960, 395, fit("$20B", 230, 600, 96), ch["a"], glow=ch["a"], glow_a=0.8, align="center", keyline=10)
    small(c, "NET INCOME · FY2025", 960, 440, ch["b"], 22, 0.95, align="center")
    brand(c, "htp")
    finish(s, o("visa", "b"))


def visa_c():
    ch = CHANNELS["htp"]
    s, c = to_surface(black())
    # streaks of money flowing through the card (the volume that isn't its money)
    rng = np.random.default_rng(5)
    for k in range(70):
        y = rng.uniform(300, 700)
        x0 = rng.uniform(-200, 600)
        ln = rng.uniform(200, 700)
        c.drawLine(x0, y, x0 + ln, y - ln * 0.16, glowp(ch["b"], rng.uniform(0.15, 0.5), 3, rng.uniform(1.5, 4)))
    card(c, 940, 450, 560, -10, ch["a"])
    glow_text(c, "$17", 40, 300, heavy(260, 100), ch["b"], glow=ch["b"], glow_a=0.7, keyline=10)
    glow_text(c, "TRILLION", 52, 410, heavy(104, 100), "#FFFFFF", keyline=8)
    hl_text(c, "NOT ITS MONEY", 640, 690, heavy(78, 100), ch["a"], seed=6, align="center", slope=-0.004)
    brand(c, "htp")
    finish(s, o("visa", "c"))


# ---------------------------------------------------------------- PONZI (Money Crimes)
# Claims: "+50% ON PAPER": the note shown at 5:0x promises $300 for $200 (50%), over the line "watch it grow. On paper."
# (NOT "double in 90 days": the film says it, but the note on screen says 50% at ninety days, so the two would clash);
# "where is the money coming from?" (cold open card); "The money didn't come from coupons. It came from the next
# investors." (4:1x). Pictures: the Securities Exchange Company note (film 7:xx), the reply coupon (2:58), the
# "PONZI ARRESTED" front page (film end). No faces.
def tab(size):
    """Money Crimes' own face: Anton, tall and condensed like a 1920s tabloid headline (brand mark by type, not layout)."""
    return font("Anton-Regular", size)


def fit_face(face, s, size, maxw):
    while size > 10 and tw(s, face(size)) > maxw:
        size -= 2
    return face(size)


def mc02_a():
    ch = CHANNELS["mc"]
    base, _ = photo_object(black(), os.path.join(AI["mc02p"], "ponzi_promissory_note_1920.jpg"), (40, 40, 2520, 1220),
                           (580, 150, 820, 397), -8, ch, glow=1.2)
    s, c = to_surface(base)
    glow_text(c, "+50%", 40, 350, tab(260), ch["a"], glow=ch["a"], glow_a=0.7, glow_s=24, keyline=10)
    hl_text(c, "ON PAPER", 58, 520, tab(150), "#FFFFFF", ink="#0A0A0A", seed=2)
    # the note's own promise: $200 in, $300 back
    ring(c, 890, 402, 138, 28, ch["c"], 8, seed=4, rot=8)
    brand(c, "mc", corner="bl")
    finish(s, o("mc02", "a"))


def mc02_b():
    ch = CHANNELS["mc"]
    base, m = photo_object(black(), os.path.join(AI["mc02p"], "boston_american_ponzi_arrested_1920.jpg"), (60, 60, 2500, 1500),
                           (590, 90, 720, 432), 6, ch, glow=1.1, contrast=(0.2, 0.75))
    s, c = to_surface(base)
    glow_text(c, "WHERE'S THE", 44, 250, fit_face(tab, "WHERE'S THE", 150, 520), "#FFFFFF", keyline=10)
    hl_text(c, "MONEY?", 62, 560, tab(290), ch["a"], ink="#FFFFFF", seed=5)
    brand(c, "mc")
    finish(s, o("mc02", "b"))


def mc02_c():
    ch = CHANNELS["mc"]
    base, _ = photo_object(black(), os.path.join(AI["mc02p"], "reply_coupon_rome_type.jpg"), (40, 40, 2480, 1780),
                           (660, 150, 580, 417), 7, ch, paper="#EAF0F4", ink="#0B1A2A", glow=1.0, contrast=(0.2, 0.85))
    s, c = to_surface(base)
    xmark(c, 950, 358, 360, ch["a"], 34)
    f = tab(170)
    x0, w = glow_text(c, "COUPONS", 44, 230, f, "#FFFFFF", keyline=9)
    strike(c, x0 - 14, 230 - cap_h(f) * 0.30, x0 + w + 16, 230 - cap_h(f) * 0.62, ch["a"], 13)
    hl_text(c, "NEW", 58, 460, tab(170), ch["a"], ink="#FFFFFF", seed=3)
    hl_text(c, "INVESTORS", 58, 660, tab(150), "#FFFFFF", ink="#0A0A0A", seed=8)
    brand(c, "mc")
    finish(s, o("mc02", "c"))



RECIPES = {
    "hormuz": [hormuz_a, hormuz_b, hormuz_c], "lf01": [lf01_a, lf01_b, lf01_c], "lf02": [lf02_a, lf02_b, lf02_c],
    "lf03": [lf03_a, lf03_b, lf03_c], "visa": [visa_a, visa_b, visa_c], "mc02": [mc02_a, mc02_b, mc02_c]}


# ================================================================================================ feed sheet
def neighbour(seed, bright):
    """A synthetic stand-in for a typical YouTube thumbnail: saturated, busy, mean luminance ~0.45-0.6 (no real
    thumbnails are copied). Used only to judge our contrast against the feed."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:94 * 4, 0:168 * 4].astype(np.float32)
    a = np.zeros(x.shape + (3,), np.float32)
    for _ in range(5):
        cx, cy, r = rng.uniform(0, 672), rng.uniform(0, 376), rng.uniform(80, 260)
        cc = rng.uniform(0.2, 1.0, 3)
        a += np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r))[..., None] * cc
    a = np.clip(0.12 + a * 0.5 * bright, 0, 1)
    img = (a * 255).astype(np.uint8)
    cv2.putText(img, "BIG TEXT", (30, 120), cv2.FONT_HERSHEY_DUPLEX, 3.2, (255, 255, 255), 14)
    cv2.putText(img, "BIG TEXT", (30, 120), cv2.FONT_HERSHEY_DUPLEX, 3.2, (255, 220, 0), 6)
    return img


def feed_sheet():
    """Every variant at real phone sizes on YouTube's white and dark UI, next to synthetic 'typical' neighbours."""
    from PIL import Image, ImageDraw, ImageFont
    films = list(RECIPES)
    tw_, th_ = 168, 94           # mobile search / suggested-list size
    hw, hh = 360, 202            # home feed card on a 390 pt phone (scaled for the sheet)
    fnt = ImageFont.truetype(os.path.join(REPO, "a01_v6", "fonts", "IBMPlexMono-500.ttf"), 13)
    fnb = ImageFont.truetype(os.path.join(REPO, "a01_v6", "fonts", "InterTight-600.ttf"), 22)
    pad = 16
    row_h = th_ + 44
    col_w = tw_ + 20
    ncols = 6                     # old, A, B, C, two neighbours
    panel_w = pad * 2 + 150 + ncols * col_w
    panel_h = 60 + len(films) * row_h + 20
    home_h = 60 + hh + 70
    sheet = Image.new("RGB", (panel_w * 2, panel_h + home_h), (0, 0, 0))
    for p, (bg, fg, sub) in enumerate([((255, 255, 255), (15, 15, 15), (96, 96, 96)), ((15, 15, 15), (241, 241, 241), (170, 170, 170))]):
        x0 = p * panel_w
        d = ImageDraw.Draw(sheet)
        d.rectangle([x0, 0, x0 + panel_w, panel_h + home_h], fill=bg)
        d.text((x0 + pad, 16), ("WHITE" if p == 0 else "DARK") + " YOUTUBE UI · thumbnails at 168x94 (phone search / up next)", font=fnb, fill=fg)
        heads = ["OLD", "A", "B", "C", "typical*", "typical*"]
        for k, hd in enumerate(heads):
            d.text((x0 + pad + 150 + k * col_w, 44), hd, font=fnt, fill=sub)
        for r, film in enumerate(films):
            y = 64 + r * row_h
            d.text((x0 + pad, y + 30), film.upper(), font=fnb, fill=fg)
            paths = [os.path.join(LAB, OLD[film])] + [o(film, v) for v in "abc"]
            for k, pth in enumerate(paths):
                im = Image.open(pth).convert("RGB").resize((tw_, th_), Image.LANCZOS)
                sheet.paste(im, (x0 + pad + 150 + k * col_w, y))
                if k:
                    d.text((x0 + pad + 150 + k * col_w, y + th_ + 4), TITLES[film][:22], font=fnt, fill=fg)
            for k in range(2):
                nb = Image.fromarray(neighbour(r * 7 + k + p * 50, 0.9 + 0.3 * k)).resize((tw_, th_), Image.LANCZOS)
                sheet.paste(nb, (x0 + pad + 150 + (4 + k) * col_w, y))
        # home-feed size: the recommended A variants in a row at 360 wide (scaled 0.5 to fit: still ~180 px each)
        y = panel_h
        d.text((x0 + pad, y + 10), "HOME FEED (A variants, 360 px wide card scaled to half)", font=fnb, fill=fg)
        for k, film in enumerate(films):
            im = Image.open(o(film, "a")).convert("RGB").resize((hw // 2 + 0, hh // 2), Image.LANCZOS)
            sheet.paste(im, (x0 + pad + k * (hw // 2 + 10), y + 50))
        d.text((x0 + pad, y + 50 + hh // 2 + 12), "*typical = synthetic stand-in at typical feed brightness/saturation (no real thumbnails copied)",
               font=fnt, fill=sub)
    out = os.path.join(HERE, "thumbs_v2_feed.jpg")
    sheet.save(out, quality=90)
    print("wrote", os.path.relpath(out, REPO), f"{os.path.getsize(out) / 1e6:.2f} MB")


def phone_check(film):
    """168 px preview of one film's three variants, upscaled 3x nearest, for eyeballing legibility."""
    from PIL import Image
    ims = [Image.open(o(film, v)).convert("RGB").resize((168, 94), Image.LANCZOS).resize((504, 282), Image.NEAREST) for v in "abc"]
    sheet = Image.new("RGB", (504 * 3 + 20, 282), (255, 255, 255))
    for k, im in enumerate(ims):
        sheet.paste(im, (k * 514, 0))
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"phone_{film}.png")
    sheet.save(out)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--feed" not in sys.argv or args:
        for film in (args or RECIPES):
            for fn in RECIPES[film]:
                fn()
            print("phone check:", os.path.relpath(phone_check(film), REPO))
    if "--feed" in sys.argv or not args:
        feed_sheet()
