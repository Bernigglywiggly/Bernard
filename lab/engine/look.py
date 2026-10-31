"""The channel look (decided on EP03): line art turned into characters, turquoise on black. Thin strokes light
their cells; clear outlines are drawn with | / - \\ along the shape (from the structure tensor), fills step through
a ramp; a faint drifting sea of characters is cleared around the subject so the eye has one place to go; a soft
light behind the subject and a tight glow. Small labels are drawn crisp on top, typed on with a block cursor.

Accents a scene can ask for (module-level lists in scenes.py, or none):
  TRAILS = [(t0, t1)]       a phosphor persistence: moving things leave a short tail of characters
  GLINTS = [(t0, dur)]      a diagonal band of bright characters sweeps across whatever is lit
"""
import numpy as np
from scipy.ndimage import distance_transform_edt, gaussian_filter, maximum_filter, sobel

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine import tl  # noqa: E402

W, H, FPS = tl.W, tl.H, tl.FPS
ease, seg, lerp = mg.ease, mg.seg, mg.lerp
RAMP = " .,:;-=+*o%#@"                        # fills, from sparse to dense
EDGE = "-\\|/"                                # outlines, by the stroke's angle on screen: 0, 45 (down-right), 90, 135
CPS = 24.0                                    # labels type at 24 characters a second


class Grid:
    def __init__(self, cw, ch, font=mg.MONO_M):
        self.cw, self.ch = cw, ch
        self.cols, self.rows = W // cw, H // ch
        f = mg.font(font, ch * 1.0)
        glyphs = RAMP + EDGE
        self.atlas = np.zeros((len(glyphs), ch, cw), np.float32)
        for i, g in enumerate(glyphs):
            sf = skia.Surface(cw, ch); c = sf.getCanvas(); c.clear(skia.ColorBLACK)
            c.drawString(g, (cw - f.measureText(g)) / 2, ch * 0.8, f, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
            self.atlas[i] = sf.makeImageSnapshot().toarray()[:, :, 1] / 255.0
        self.n_ramp = len(RAMP)


G = Grid(8, 12)                                                  # 240 x 90 characters
VIGNETTE = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), 1180,
                                                             [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 120)],
                                                             [0.0, 0.55, 1.0]))


def plus(a=1.0):
    p = skia.Paint(BlendMode=skia.BlendMode.kPlus)
    p.setAlphaf(a)
    return p


def cells_to_px(m):
    return np.repeat(np.repeat(m, G.ch, 0), G.cw, 1)[..., None]


def sea(t, cols, rows):
    yy, xx = np.mgrid[0:rows, 0:cols]
    u, v = xx / cols, yy / rows
    f = np.sin(u * 9.0 + t * 0.6) * np.cos(v * 7.0 - t * 0.4) + 0.5 * np.sin((u - v) * 13.0 + t * 0.9)
    return (f - f.min()) / (f.max() - f.min() + 1e-9)


def cells(arr):
    """A frame (BGRA array) -> (field, edge): how lit each character is, and the stroke direction where the cell sits
    on a clear outline (0-3, else -1)."""
    lum = (0.2126 * arr[..., 2] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 0]) / 255.0
    L2 = lum[: G.rows * G.ch, : G.cols * G.cw].reshape(G.rows, G.ch, G.cols, G.cw)
    mean, mx = L2.mean(axis=(1, 3)), L2.max(axis=(1, 3))
    fld = np.clip((np.maximum(mean * 2.4, mx * 0.95) - 0.10) / 0.9, 0, 1) ** 0.75
    sm = gaussian_filter(lum[::2, ::2], 1.0)
    gx, gy = sobel(sm, 1), sobel(sm, 0)
    h2, w2 = G.ch // 2, G.cw // 2
    cs = lambda v: v[: G.rows * h2, : G.cols * w2].reshape(G.rows, h2, G.cols, w2).sum(axis=(1, 3))
    jxx, jyy, jxy = cs(gx * gx), cs(gy * gy), cs(gx * gy)
    tr = jxx + jyy + 1e-9
    coh = np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / tr
    theta = 0.5 * np.degrees(np.arctan2(2 * jxy, jxx - jyy))
    b = np.round(((theta + 90) % 180) / 45).astype(int) % 4
    strong = (coh > 0.55) & (np.sqrt(tr / (h2 * w2)) > 0.05) & (mean < 0.5) & (mx > 0.55)
    return fld, np.where(strong, b, -1)


def chars(fe, t, boost=None, sea_amt=1.0):
    """The character layer (on black) and the subject's field."""
    fld, edge = fe
    fld = np.maximum(fld, maximum_filter(fld, size=3) * 0.28)
    if boost is not None:
        fld = np.maximum(fld, boost)
    subj = fld.copy()
    if sea_amt > 0:
        mask = fld > 0.14
        d = distance_transform_edt(~mask) if mask.any() else np.full(fld.shape, 99.0)
        fld = np.maximum(fld, sea(t, G.cols, G.rows) ** 1.6 * 0.13 * sea_amt * np.clip((d - 2) / 10, 0, 1))
    fld = np.where(subj < 0.2, np.minimum(fld, np.maximum(subj - 0.12, 0) + (fld - subj).clip(0)), fld)
    idx = np.clip((fld * (G.n_ramp - 1)).round().astype(int), 0, G.n_ramp - 1)
    stroke = (edge >= 0) & (subj > 0.12)
    idx = np.where(stroke, G.n_ramp + np.maximum(edge, 0), idx)
    fld = np.where(stroke, np.maximum(fld, 0.9), fld)
    tiles = G.atlas[idx]
    img = tiles.transpose(0, 2, 1, 3).reshape(G.rows * G.ch, G.cols * G.cw)
    lo, hi = np.array((16, 96, 90), np.float32), np.array((236, 246, 245), np.float32)
    k = cells_to_px(np.clip(fld * 1.15, 0, 1) ** 1.1)
    rgb = ((lo * (1 - k) + hi * k) * img[..., None]).clip(0, 255).astype(np.uint8)
    out = np.zeros((H, W, 4), np.uint8)
    out[: rgb.shape[0], : rgb.shape[1], :3] = rgb
    out[: rgb.shape[0], : rgb.shape[1], 3] = (img * 255).astype(np.uint8)
    return skia.Image.fromarray(out, colorType=skia.ColorType.kRGBA_8888_ColorType), subj


def screen(layer_img, subj=None):
    """Characters on the dark ground: a soft light behind the subject, the characters, a tight glow. The light and the
    glow are blurred small and scaled up (a quarter and half size): the same look as full-size blurs (PSNR 40-51 dB
    on EP04's frames) at about half the cost."""
    lin = skia.SamplingOptions(skia.FilterMode.kLinear)
    sf = skia.Surface(W, H); c = sf.getCanvas(); c.clear(skia.Color(8, 9, 11))
    if subj is not None and np.any(subj > 0.14):
        g = (np.clip(subj, 0, 1) ** 1.5 * 255).astype(np.uint8)
        rgba = np.stack([(g * 0.22).astype(np.uint8), (g * 0.78).astype(np.uint8), (g * 0.74).astype(np.uint8), g], -1)
        small = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.ColorType.kRGBA_8888_ColorType)
        q = skia.Surface(W // 4, H // 4); qc = q.getCanvas(); qc.clear(skia.ColorTRANSPARENT)
        p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(3, 3))
        qc.drawImageRect(small, skia.Rect.MakeWH(W // 4, H // 4), lin, p)
        c.drawImageRect(q.makeImageSnapshot(), skia.Rect.MakeWH(W, H), lin, plus(0.32))
    c.drawImage(layer_img, 0, 0)
    h2 = skia.Surface(W // 2, H // 2); hc = h2.getCanvas(); hc.clear(skia.ColorTRANSPARENT)
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(1.75, 1.75))
    hc.drawImageRect(layer_img, skia.Rect.MakeWH(W // 2, H // 2), lin, p)
    c.drawImageRect(h2.makeImageSnapshot(), skia.Rect.MakeWH(W, H), lin, plus(0.35))
    return sf.makeImageSnapshot()


def glint(k, fld, width=0.035):
    yy, xx = np.mgrid[0:G.rows, 0:G.cols]
    u = xx / G.cols + 0.35 * (yy / G.rows)
    return np.exp(-((u - lerp(-0.2, 1.4, k)) / width) ** 2) * 0.95 * (fld > 0.12)


# ---------------------------------------------------------------- labels, typed on crisp
def schedule(text, t0, cps=CPS):
    """When each character of a label appears (as EP03's typeon): a human rhythm, a touch uneven, a beat longer after
    a space and before punctuation, but fixed per text so every render agrees with itself."""
    import zlib
    r = np.random.default_rng(zlib.crc32(text.encode()))
    base = 1.0 / cps
    gaps = np.clip(r.normal(base, 0.22 * base, max(0, len(text) - 1)), 0.55 * base, 1.8 * base)
    for i in range(len(gaps)):
        if text[i] == " ":
            gaps[i] *= 1.25
        if text[i + 1] in "·,":
            gaps[i] *= 1.3
    return t0 + np.concatenate([[0.0], np.cumsum(gaps)])


def typed(c, s_, x, y, t, t0, size, col, align, a, cps=None):
    if a <= 0.01:
        return
    f = mg.font(mg.MONO_M, size)
    w = f.measureText(s_)
    x0 = x - w / 2 if align == "center" else x - w if align == "right" else x
    if t0 < 0:
        c.drawString(s_, x0, y, f, mg.fill(col, a))
        return
    sched = schedule(s_, t0, cps or CPS)
    n = int(np.searchsorted(sched, t, side="right"))
    if n == 0:
        return
    c.drawString(s_[:n], x0, y, f, mg.fill(col, a))
    if t < sched[-1] + 0.45 and (n < len(s_) or (t - sched[-1]) % 0.3 < 0.18):
        cx_ = x0 + f.measureText(s_[:n]) + 2
        c.drawRect(skia.Rect.MakeXYWH(cx_, y - size * 0.78, size * 0.56, size * 0.94), mg.fill(col, 0.75 * a))


def crisp_labels(c, t):
    seen = set()
    for item in tl.LABELS["queue"]:
        s_, x, y, tt, t0, size, col, align, a = item[:9]
        cps = item[9] if len(item) > 9 else None
        if abs(tt - t) > 1e-6 or (s_, x, y) in seen:
            continue
        seen.add((s_, x, y))
        typed(c, s_, x, y, t, t0, size, col, align, a, cps)
    tl.LABELS["queue"].clear()


def furniture(c):
    """The only furniture: a thin line and the episode's name, bottom left."""
    if tl.EP["title"]:
        c.drawString(tl.EP["title"], 120, H - 60, mg.font(mg.MONO, 16), mg.fill(mg.ON_DARK_SOFT, 0.8))
        c.drawLine(120, H - 84, 300, H - 84, mg.stroke(mg.ON_DARK_SOFT, 1, 0.6))


# ---------------------------------------------------------------- the frame
def lines_img(scenes, t, collect=True):
    """The scenes' line art at t on black (labels queued for the crisp pass)."""
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.ColorBLACK)
    tl.LABELS["mode"] = "collect" if collect else "draw"
    try:
        scenes.frame(c, t)
    finally:
        tl.LABELS["mode"] = "draw"
    return s.makeImageSnapshot()


TRAIL = {"f": None, "i": None, "w": None}


def _trail(scenes, t, cur, w):
    """Persistence, like a slow phosphor: each cell keeps the brighter of now and a fading memory, so motion leaves a
    short tail stepping down the ramp; tails are fills, strokes stay on the live shape. Stepped frame by frame from
    the window's start (a still or a render slice that starts inside the window replays the frames before it)."""
    t0, t1 = w
    kf = lambda tt: 0.8 * (ease(seg(tt, t0, t0 + 0.5)) if tt < t1 else 1 - ease(seg(tt, t1, t1 + 0.6)))
    i_t, i0 = int(round(t * FPS)), int(round(t0 * FPS))
    if TRAIL["w"] != w or TRAIL["i"] is None or TRAIL["i"] >= i_t or TRAIL["i"] < i0 - 1:
        TRAIL.update(f=None, i=i0 - 1, w=w)
    for i in range(TRAIL["i"] + 1, i_t + 1):
        tl.LABELS["queue"].clear()
        f = cur[0] if i == i_t else cells(lines_img(scenes, i / FPS).toarray())[0]
        k = kf(i / FPS)
        TRAIL["f"] = f if TRAIL["f"] is None or k < 0.002 else np.maximum(f, TRAIL["f"] * k)
        TRAIL["i"] = i
    f = TRAIL["f"]
    return f, np.where(cur[0] >= f - 1e-6, cur[1], -1)


def compose(scenes, t, captions=None):
    """One finished frame: the scenes' lines -> characters (+ any trail and glint), the light and glow, the vignette,
    the crisp labels, the furniture, and (optionally) the captions."""
    tl.LABELS["queue"].clear()
    img = lines_img(scenes, t)
    fe = cells(img.toarray())
    for w in getattr(scenes, "TRAILS", ()):
        if w[0] <= t < w[1] + 0.7:
            queue = list(tl.LABELS["queue"])
            fe = _trail(scenes, t, fe, tuple(w))
            tl.LABELS["queue"][:] = queue
    boost = None
    for g0, gd in getattr(scenes, "GLINTS", ()):
        if g0 <= t < g0 + gd:
            boost = glint(seg(t, g0, g0 + gd), fe[0])
    out = skia.Surface(W, H); cv = out.getCanvas()
    cv.drawImage(screen(*chars(fe, t, boost)), 0, 0)
    cv.drawRect(skia.Rect.MakeWH(W, H), VIGNETTE)
    crisp_labels(cv, t)
    furniture(cv)
    if captions:
        captions(cv, t)
    return out.makeImageSnapshot()
