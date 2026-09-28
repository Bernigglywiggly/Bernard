"""The EP03 cold open in the decided look: ASCII all the way, a little Blender realism, other looks as rare accents.

  1848          Blender's chrome numerals, shaded in characters (tonal ASCII), with the line trace drawn in over them
                and a glint of bright characters sweeping across
  1848 → bottle the lines flow into the bottle in characters; the gold pours in
  the bottle    the characters re-form as Blender's glass bottle, then DEVELOP into the real image from the bottle out
  the burst     the photo breaks back into characters and, once, the gold leaves a trail: a phosphor persistence in
                the grid, so the stream draws its own path in characters stepping down the ramp (no zoom, no colour split)
  the store     the trail fades into clean characters; $36,000 in dense blocks with a glint; the street sells out
  the shovel    the characters re-form as the Blender dunes and develop into the image again, for the one lonely shot
  the grip      the push into the grip breaks back into characters, and the prize is a character too

Scored with Mainframe (lab/music/beds.py): dark synth-orchestral, an original in the spirit of The Son of Flynn,
re-cut so the pulse arrives on "Within weeks the town empties", the brass with the Big Mac, and the pulse drops out on
"He never panned".

    python3 ascii_open.py still 2 9.6 13 ...   # build/ascii_still_*.png + build/ascii_sheet.jpg
    python3 ascii_open.py render               # build/style_S_ascii.mp4
    python3 ascii_open.py mix                  # the same picture, a fresh score and mix
    EP03_FULL=1 python3 ascii_open.py full 4   # the whole episode: 4 parallel slices, then events, score, mix
    EP03_FULL=1 python3 ascii_open.py sound_full   # just the sound again, onto build/ep03_full_silent.mp4
"""
import math
import os
import subprocess
import sys

import numpy as np
from scipy.ndimage import maximum_filter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "music"))
import relay as R  # noqa: E402
from relay import S, ST, mg, skia, W, H, FPS, surface, plus, a_img, d_img, blend  # noqa: E402
import typeon as TO  # noqa: E402

BUILD = S.BUILD
FULL = os.environ.get("EP03_FULL") == "1"                        # the whole episode, not just the cold open
NO_CAPTIONS = os.environ.get("NO_CAPTIONS") == "1"               # the clean feed, for shorts (they caption themselves)
T_BODY = S.ls("census") if "census" in S.IDS else 1e9
if FULL:
    import ep03_body
    DUR = ep03_body.end_time()
    ST.DUR = DUR                                                  # captions run to the end
else:
    DUR = S.ls("rule") + 2.4
ease, seg, lerp = mg.ease, mg.seg, mg.lerp

TB, TM, TSH, TN, TR = S.ls("bottle"), S.ls("mind"), S.ls("shop"), S.ls("never"), S.ls("rule")
T_MORPH = S.at("bottle", 0.55)                                   # A's 1848 → bottle morph, and D's cut to the bottle
X1A, X1B = T_MORPH - 0.6, T_MORPH + 0.2                          # D's chrome characters hand over to the line ones
P1A, P1B = T_MORPH + 0.1, T_MORPH + 1.2                          # ...and the framing eases back to A's own
X2A = S.at("bottle", 0.95); X2B = X2A + 0.45                     # once the pour has settled, the line bottle re-forms as
DV2A, DV2B = X2A + 0.2, X2A + 0.8                                # the glass one (in characters), then develops into the image
UD3A, UD3B = TM + 1.2, TM + 1.75                                 # the cork pops, the gold streams out, then back to characters
X3A, X3B = TM + 1.5, TM + 2.3                                    # the characters' source: the Blender stream → the line one
FB_ON, FB_OFF = UD3A, TSH - 0.2                                  # the feedback loop on the characters
SW36 = S.at("36k", 0.55) + 1.25                                  # the $36,000 glint
SW1848 = TB + 1.5                                                # the 1848 glint
X6A = TN + 0.95; DV6A, DV6B = X6A + 0.4, X6A + 1.3               # the dunes: re-form, then develop
UD7A, UD7B = TR - 0.6, TR - 0.12                                 # into the grip: back to characters
X7A, X7B = TR - 0.3, TR + 0.15                                   # ...and on to A's ring and prize

EXTRA_SFX = [(SW1848, "scan", -18), (X2A + 0.3, "swell", -15), (UD3A - 0.05, "form", -16), (FB_OFF + 0.1, "thum", -15),
             (SW36, "scan", -17), (X6A + 0.35, "swell", -16), (UD7A + 0.1, "glitch", -19), (TR - 0.12, "sub_drop", -13)]


# ---------------------------------------------------------------- characters (v3: finer, true strokes, one clear focus)
RAMP = " .,:;-=+*o%#@"                        # fills, from sparse to dense
EDGE = "-\\|/"                                # outlines, by the stroke's angle on screen: 0, 45 (down-right), 90, 135


class Grid:
    """A character grid with its glyph atlas: a luminance ramp for fills plus four stroke glyphs for outlines."""

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


G = Grid(8, 12)                                                  # 240 x 90 characters (was 192 x 72)
NOISE2 = np.random.default_rng(4).random((G.rows, G.cols))
S.E2.update(s=0.8, up=-275.0, label_y=345)                      # the $36,000 stays big over the street


def cells_to_px(m):
    return np.repeat(np.repeat(m, G.ch, 0), G.cw, 1)[..., None]


def cells(arr, photo=0.0):
    """A frame (BGRA array) → (field, edge): the field is how lit each character is (the line mapping, where thin
    strokes light a cell, or the tonal one for photographs, blended by `photo`); edge is the stroke direction where
    the cell sits on a clear outline (0-3, else -1), from the structure tensor of the smoothed luminance, so
    outlines are drawn with | / - \\ that follow the shape instead of blobs."""
    from scipy.ndimage import gaussian_filter, sobel
    lum = (0.2126 * arr[..., 2] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 0]) / 255.0
    L2 = lum[: G.rows * G.ch, : G.cols * G.cw].reshape(G.rows, G.ch, G.cols, G.cw)
    mean, mx = L2.mean(axis=(1, 3)), L2.max(axis=(1, 3))
    fld = np.clip((np.maximum(mean * 2.4, mx * 0.95) - 0.10) / 0.9, 0, 1) ** 0.75
    if photo > 0:
        tonal = np.clip((0.75 * mean + 0.25 * mx - 0.04) * 1.6, 0, 1) ** 0.9
        fld = fld * (1 - photo) + tonal * photo
    sm = gaussian_filter(lum[::2, ::2], 1.0)
    gx, gy = sobel(sm, 1), sobel(sm, 0)
    h2, w2 = G.ch // 2, G.cw // 2
    cs = lambda v: v[: G.rows * h2, : G.cols * w2].reshape(G.rows, h2, G.cols, w2).sum(axis=(1, 3))
    jxx, jyy, jxy = cs(gx * gx), cs(gy * gy), cs(gx * gy)
    tr = jxx + jyy + 1e-9
    coh = np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / tr
    theta = 0.5 * np.degrees(np.arctan2(2 * jxy, jxx - jyy))       # the gradient's angle (y down)
    b = np.round(((theta + 90) % 180) / 45).astype(int) % 4          # the stroke runs across it
    strong = (coh > 0.55) & (np.sqrt(tr / (h2 * w2)) > 0.05) & (mean < 0.5) & (mx > 0.55)   # the line's core, not its glow
    return fld, np.where(strong, b, -1)


def mix(a, b, u):
    """Blend two (field, edge) pairs; each cell keeps the stroke of whichever source is brighter there."""
    fa, fb = a[0] * (1 - u), b[0] * u
    return fa + fb, np.where(fa >= fb, a[1], b[1])


def brighter(a, b, ka=1.0):
    fa = a[0] * ka
    return np.maximum(fa, b[0]), np.where(fa >= b[0], a[1], b[1])


def chars(fe, t, boost=None, sea=1.0):
    """The character layer (on black) and the subject's field. The subject is drawn in bright white-cyan with true
    strokes; the drifting sea is faint and cleared around the subject, so the eye has one place to go."""
    from scipy.ndimage import distance_transform_edt
    fld, edge = fe
    fld = np.maximum(fld, maximum_filter(fld, size=3) * 0.28)
    if boost is not None:
        fld = np.maximum(fld, boost)
    subj = fld.copy()
    if sea > 0:
        mask = fld > 0.14
        d = distance_transform_edt(~mask) if mask.any() else np.full(fld.shape, 99.0)
        fld = np.maximum(fld, ST.sea(t, G.cols, G.rows) ** 1.6 * 0.13 * sea * np.clip((d - 2) / 10, 0, 1))
    fld = np.where(subj < 0.2, np.minimum(fld, np.maximum(subj - 0.12, 0) + (fld - subj).clip(0)), fld)   # halo → quiet
    idx = np.clip((fld * (G.n_ramp - 1)).round().astype(int), 0, G.n_ramp - 1)
    stroke = (edge >= 0) & (subj > 0.12)
    idx = np.where(stroke, G.n_ramp + np.maximum(edge, 0), idx)
    fld = np.where(stroke, np.maximum(fld, 0.9), fld)                                          # strokes at full light
    tiles = G.atlas[idx]
    img = tiles.transpose(0, 2, 1, 3).reshape(G.rows * G.ch, G.cols * G.cw)
    lo, hi = np.array((16, 96, 90), np.float32), np.array((236, 246, 245), np.float32)
    k = cells_to_px(np.clip(fld * 1.15, 0, 1) ** 1.1)
    rgb = ((lo * (1 - k) + hi * k) * img[..., None]).clip(0, 255).astype(np.uint8)
    out = np.zeros((H, W, 4), np.uint8)
    out[: rgb.shape[0], : rgb.shape[1], :3] = rgb
    out[: rgb.shape[0], : rgb.shape[1], 3] = (img * 255).astype(np.uint8)
    return skia.Image.fromarray(out, colorType=skia.ColorType.kRGBA_8888_ColorType), subj


def screen(layer, subj=None):
    """Characters on the dark ground: a soft light behind the subject (from its field, so shapes read at a glance),
    the characters, and a tight glow."""
    sf = skia.Surface(W, H); c = sf.getCanvas(); c.clear(skia.Color(8, 9, 11))
    if subj is not None and np.any(subj > 0.14):
        g = (np.clip(subj, 0, 1) ** 1.5 * 255).astype(np.uint8)
        rgba = np.stack([(g * 0.22).astype(np.uint8), (g * 0.78).astype(np.uint8), (g * 0.74).astype(np.uint8), g], -1)
        small = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.ColorType.kRGBA_8888_ColorType)
        p = plus(0.32); p.setImageFilter(skia.ImageFilters.Blur(12, 12))
        c.drawImageRect(small, skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.drawImage(layer, 0, 0)
    gp = plus(0.35); gp.setImageFilter(skia.ImageFilters.Blur(3.5, 3.5))
    c.drawImage(layer, 0, 0, skia.SamplingOptions(), gp)
    return sf.makeImageSnapshot()


def glint(k, fld, width=0.035):
    """A diagonal band of bright characters sweeping left to right, only where there's something to light."""
    yy, xx = np.mgrid[0:G.rows, 0:G.cols]
    u = xx / G.cols + 0.35 * (yy / G.rows)
    return np.exp(-((u - lerp(-0.2, 1.4, k)) / width) ** 2) * 0.95 * (fld > 0.12)


def develop(k, cx, cy):
    """Per-cell photo mask, spreading out from (cx, cy), each cell fading over a few frames."""
    yy, xx = np.mgrid[0:G.rows, 0:G.cols]
    dist = np.hypot((xx + 0.5) * G.cw - cx, ((yy + 0.5) * G.ch - cy) * 1.4) / 1150
    return np.clip((k * 1.35 - dist - 0.2 * NOISE2) / 0.12, 0, 1).astype(np.float32)


# ---------------------------------------------------------------- the one accent: a phosphor trail on the characters
TRAIL = {"f": None, "i": None}


def trail_k(t):
    """How much of the last frame survives into this one: eases in as the gold streams out, out as the store forms."""
    if t < FB_OFF:
        return 0.82 * ease(seg(t, FB_ON, FB_ON + 0.6))
    return 0.82 * (1 - ease(seg(t, FB_OFF, FB_OFF + 0.7)))


def trail(t, cur):
    """Persistence, like a slow phosphor: each cell keeps the brighter of what it shows now and a fading memory of
    what it showed, so moving gold leaves a short tail stepping down the ramp (@ # % o * + = - ; : , .) and anything
    still doesn't change at all. No zoom, no rotation, no colour split: the motion draws its own path. Stepped one
    frame at a time from FB_ON (a still far into the window replays the frames before it)."""
    i_t, i0 = int(round(t * FPS)), int(round(FB_ON * FPS))
    if TRAIL["i"] is None or TRAIL["i"] >= i_t or TRAIL["i"] < i0 - 1:
        TRAIL["f"], TRAIL["i"] = None, i0 - 1
    for i in range(TRAIL["i"] + 1, i_t + 1):
        f = cur[0] if i == i_t else field(i / FPS)[0][0]
        k = trail_k(i / FPS)
        TRAIL["f"] = f if TRAIL["f"] is None or k < 0.002 else np.maximum(f, TRAIL["f"] * k)
        TRAIL["i"] = i
    f = TRAIL["f"]
    return f, np.where(cur[0] >= f - 1e-6, cur[1], -1)                # tails are fills; strokes stay on the live shape


# ---------------------------------------------------------------- sources (small labels stay crisp, on top)
def a_src(t, xf=None, lines_only=True):
    """The line layer for the characters, without its small monospace labels (they'd turn to mush as characters):
    untransformed frames queue them to be drawn crisp over the characters; transformed ones drop them."""
    S.LABELS["mode"] = "collect" if xf is None else "skip"
    try:
        return a_img(t, xf, lines_only=lines_only)
    finally:
        S.LABELS["mode"] = "draw"


def crisp_labels(c, t):
    seen = set()
    for item in S.LABELS["queue"]:
        s_, x, y, tt, t0, size, col, align, a = item[:9]
        cps = item[9] if len(item) > 9 else None
        if abs(tt - t) > 1e-6 or (s_, x, y) in seen:
            continue
        seen.add((s_, x, y))
        typed(c, s_, x, y, t, t0, size, col, align, a, cps)
    S.LABELS["queue"].clear()


def typed(c, s_, x, y, t, t0, size, col, align, a, cps=None):
    """A label typed on, one character per keystroke (typeon.schedule, which the mix plays a key for), with a block
    cursor while it types and a moment after. t0 < 0: shown whole (a live counter)."""
    if a <= 0.01:
        return
    f = mg.font(mg.MONO_M, size)
    w = f.measureText(s_)
    x0 = x - w / 2 if align == "center" else x - w if align == "right" else x
    if t0 < 0:
        c.drawString(s_, x0, y, f, mg.fill(col, a))
        return
    sched = TO.schedule(s_, t0, cps or TO.CPS)
    n = int(np.searchsorted(sched, t, side="right"))
    if n == 0:
        return
    c.drawString(s_[:n], x0, y, f, mg.fill(col, a))
    if t < sched[-1] + 0.45 and (n < len(s_) or (t - sched[-1]) % 0.3 < 0.18):
        cx_ = x0 + f.measureText(s_[:n]) + 2
        c.drawRect(skia.Rect.MakeXYWH(cx_, y - size * 0.78, size * 0.56, size * 0.94), mg.fill(col, 0.75 * a))


# ---------------------------------------------------------------- the field at time t
def field(t):
    """The character field for the ASCII parts, from whichever sources are live at t."""
    if t < X1B:                                                    # D's chrome 1848 in tonal characters + the traced lines
        cd = cells(d_img(t).toarray(), 1.0)
        cl = cells(a_src(t, R.xf_1848(0.0)).toarray(), 0.0)
        c = brighter(cd, cl, 0.9)
        if t >= X1A:                                               # hand over to the line characters (same framing)
            c = mix(c, cl, ease(seg(t, X1A, X1B)))
        g = glint(seg(t, SW1848, SW1848 + 0.9), c[0]) if SW1848 <= t < SW1848 + 0.9 else None
        return c, g
    if t < X2A:                                                    # lines: the morph, the pour
        return cells(a_src(t, R.xf_1848(ease(seg(t, P1A, P1B))) if t < P1B else None).toarray(), 0.0), None
    if t < X3A:                                                    # line bottle → the glass bottle, in characters
        w = ease(seg(t, X2A, X2B), "i")
        u = ease(seg(t, X2A + 0.1, X2B))
        cd = cells(d_img(t, R.xf_d_bottle(t)).toarray(), 1.0)
        if u >= 1:
            return cd, None
        ca = cells(a_src(t, R.xf_bottle(w) if w > 0 else None).toarray(), 0.0)
        return mix(ca, cd, u), None
    if t < X3B:                                                    # the burst → the dust stream
        u = ease(seg(t, X3A, X3B))
        cd = cells(d_img(t).toarray(), 1.0)
        return mix(cd, cells(a_src(t).toarray(), 0.0), u), None
    if t < X6A:                                                    # clean characters: store, $36,000, the street
        c = cells(a_src(t).toarray(), 0.0)
        g = glint(seg(t, SW36, SW36 + 0.9), c[0]) if SW36 <= t < SW36 + 0.9 else None
        return c, g
    if t < X7A:                                                    # the dunes, in characters (tonal), matched grip to grip
        u = ease(seg(t, X6A, X6A + 0.5))
        cd = cells(d_img(t, R.xf_shovel(t)).toarray(), 1.0)
        if u >= 1:
            return cd, None
        return mix(cells(a_src(t).toarray(), 0.0), cd, u), None
    if t >= X7B + 0.3:                                             # past the grip: line art only (the body too)
        return cells(a_src(t).toarray(), 0.0), (tunnel_and_prize(t) if t < T_BODY + 0.7 else None)
    u = ease(seg(t, X7A, X7B))                                     # into the grip, out into the prize
    cd = cells(d_img(t).toarray(), 1.0)
    return mix(cd, cells(a_src(t).toarray(), 0.0), u), tunnel_and_prize(t)


def tunnel_and_prize(t):
    """ASCII-native ending: rings of bright characters rushing outward as we pass through the grip, then the prize
    as a glowing, pulsing orb of characters."""
    yy, xx = np.mgrid[0:G.rows, 0:G.cols]
    d = np.hypot((xx + 0.5) * G.cw - 960, ((yy + 0.5) * G.ch - 520) * 1.15)
    b = np.zeros((G.rows, G.cols))
    for k in (0.0, 0.11, 0.22):
        a0 = TR - 0.4 + k
        if a0 <= t < a0 + 0.5:
            r = lerp(30, 1400, ease(seg(t, a0, a0 + 0.5), "i"))
            b = np.maximum(b, np.exp(-((d - r) / (14 + 0.05 * r)) ** 2) * 0.9 * (1 - 0.6 * seg(t, a0, a0 + 0.5)))
    if t >= TR - 0.05:
        r = 14 + 60 * ease(seg(t, TR, TR + 0.6), "o") + 5 * math.sin((t - TR) * 5)
        k = 1 - ease(seg(t, T_BODY - 0.1, T_BODY + 0.6))            # the prize hands over to the body
        b = np.maximum(b, (np.exp(-2 * (d / r) ** 2) * 0.95 + np.exp(-(d / (r * 2.6)) ** 2) * 0.35) * k)
    return b


def photo_mask(t):
    """How much of the real (Blender) image shows, per cell: the bottle and the dunes only."""
    if DV2A <= t < UD3B:
        k = ease(seg(t, DV2A, DV2B)) if t < UD3A else 1 - ease(seg(t, UD3A, UD3B))
        return develop(k, 960, 620) if k > 0 else None, R.xf_d_bottle(t)
    if DV6A <= t < UD7B:
        k = ease(seg(t, DV6A, DV6B)) if t < UD7A else 1 - ease(seg(t, UD7A, UD7B))
        return develop(k, 960, 430) if k > 0 else None, R.xf_shovel(t)
    return None, None


def compose(t):
    S.LABELS["queue"].clear()
    c, g = field(t)
    if FB_ON <= t < FB_OFF + 0.8:                                  # the one accent: the gold leaves a trail
        c = trail(t, c)
    img = screen(*chars(c, t, g))
    m, xf = photo_mask(t)
    if m is not None:
        img = blend(img.toarray(), d_img(t, xf).toarray(), cells_to_px(m))
    s = skia.Surface(W, H); cv = s.getCanvas()
    cv.drawImage(img, 0, 0)
    cv.drawRect(skia.Rect.MakeWH(W, H), R.VIGNETTE)
    crisp_labels(cv, t)
    S.furniture(cv)
    if not NO_CAPTIONS:
        ST.captions(cv, t)
    return s.makeImageSnapshot()


# ---------------------------------------------------------------- the score
def score():
    """Mainframe (lab/music/beds.py; the user asked for something closer to The Son of Flynn), re-cut so its bar lines
    fall on the picture: strings and a filtered ostinato under 1848 and the bottle; a boom, the low pulse and the open
    ostinato on "Within weeks the town empties"; brass and violins from the Big Mac; the pulse out on "He never panned
    for gold"; then dipped for the question."""
    import beds
    import audio_fx as fx
    n = max(4, round((TN - TM) / (240.0 / 104)))                  # bars from "mind" to "never", near 104 BPM
    bar = (TN - TM) / n
    bpm = 240.0 / bar
    n_intro = int(TM // bar)                                      # the strings are there almost from the first frame
    lead = TM - n_intro * bar
    n_break = max(1, math.ceil((TR - TN) / bar))
    t_big = S.ls("markup") if "markup" in S.IDS else S.ls("36k")   # the brass arrives with the Big Mac
    a = min(max(2, round((t_big - TM) / bar)), n - 2)
    x = beds.mainframe(bpm, [("intro", n_intro), ("a", a), ("b", n - a), ("break", n_break), ("out", 2)], lead)
    t = np.arange(len(x)) / fx.SR
    dip = 1 - 0.8 * np.clip((t - (TR - 0.05)) / 0.12, 0, 1) * np.clip(1 - (t - (TR + 1.2)) / 1.0, 0.35, 1)
    x = (x * dip[:, None]).astype(np.float32)
    path = os.path.join(BUILD, "ascii_bed.wav")
    fx.save(path, x, mp3=False)
    print(f"score: Mainframe at {bpm:.2f} BPM, lead {lead:.2f}s, b from {TM + a * bar:.2f}s")
    return path


def score_full():
    """Mainframe for the whole episode, on one bar grid (the cold open's, near 104 BPM), its sections following the
    floors: the cold open as before; MECHANISM a; NOW b (brass for the money); a break for "It has happened before";
    IDEA a; IMAGINE a long break (strings, cello and sub only, the ostinato gone); SURFACE b; the sources out."""
    import beds
    import audio_fx as fx
    n = max(4, round((TN - TM) / (240.0 / 104)))
    bar = (TN - TM) / n
    bpm = 240.0 / bar
    n_intro = int(TM // bar)
    lead = TM - n_intro * bar
    t_big = S.ls("markup") if "markup" in S.IDS else S.ls("36k")
    edges_ = [(TM, "intro"), (TM + round((t_big - TM) / bar) * bar - 0.01, "a"), (TN - 0.01, "b"), (S.ls("census") - 0.4, "break"),
              (S.ls("now") - 0.4, "a"), (S.ls("before") - 0.4, "b"), (S.ls("acts") - 0.4, "break"), (S.ls("imagine") - 0.4, "a"),
              (S.ls("rush") - 0.4, "break"), (S.L[-1]["end"] + 1.0, "b"), (1e9, "out")]
    total = int(math.ceil((DUR - lead) / bar)) + 1
    names = []
    for b in range(total):
        tb = lead + (b + 0.25) * bar
        names.append(next(nm for te, nm in edges_ if tb < te))
    plan = []
    for nm in names:
        if plan and plan[-1][0] == nm:
            plan[-1][1] += 1
        else:
            plan.append([nm, 1])
    x = beds.mainframe(bpm, [tuple(p) for p in plan], lead)
    path = os.path.join(BUILD, "full_bed.wav")
    fx.save(path, x.astype(np.float32), mp3=False)
    print(f"score: Mainframe at {bpm:.2f} BPM, lead {lead:.2f}s, plan {[tuple(p) for p in plan]}")
    return path


def collect_events():
    """The picture's sound cues (forms, morphs, ticks, latches...) on the current timeline, at 30 fps as ep03s
    records them, and every label that types on (with its keystroke times, from typeon), into build/events.json."""
    import json
    S.EVENTS.clear()
    surf = skia.Surface(W, H)
    typed_, seen = [], {}
    S.LABELS["mode"] = "collect"
    try:
        for i in range(int(DUR * S.FPS)):
            t = i / S.FPS
            S.LABELS["queue"].clear()
            c = surf.getCanvas(); c.clear(skia.ColorBLACK)
            S.frame(c, t)
            for item in S.LABELS["queue"]:
                s_, x, y, tt, t0, size, col, align, a = item[:9]
                cps = item[9] if len(item) > 9 else None
                if t0 < 0 or a < 0.05:
                    continue
                k = (s_, round(t0, 3))
                if k not in seen:
                    seen[k] = len(typed_)
                    typed_.append(dict(text=s_, t0=round(t0, 3), cps=cps or TO.CPS, x=float(x), size=size))
    finally:
        S.LABELS["mode"] = "draw"
        S.LABELS["queue"].clear()
    json.dump(dict(events=S.EVENTS, typing=typed_, dur=DUR), open(os.path.join(BUILD, "events.json"), "w"))
    print(len(S.EVENTS), "events,", len(typed_), "typed labels")


def main():
    S.setup()
    if sys.argv[1] == "still":
        paths = []
        for tt in sorted(map(float, sys.argv[2:])):
            p = os.path.join(BUILD, f"ascii_still_{tt:05.2f}.png")
            compose(tt).save(p, skia.kPNG)
            paths.append(p)
            print(p, flush=True)
        cols, n = 4, len(paths)
        rows = (n + cols - 1) // cols
        ins = sum((["-i", p] for p in paths), [])
        pad = "".join(f"[{i}]scale=480:-1[s{i}];" for i in range(n))
        blanks = "".join(f"color=c=black:s=480x270:d=1[b{i}];" for i in range(rows * cols - n))
        grid = "".join(f"[s{i}]" for i in range(n)) + "".join(f"[b{i}]" for i in range(rows * cols - n))
        sheet = os.path.join(BUILD, "ascii_sheet.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", pad + blanks + grid + f"xstack=inputs={rows * cols}:grid={cols}x{rows}",
                        "-frames:v", "1", sheet], check=True)
        print(sheet)
        return
    if sys.argv[1] == "chunk":                                    # one slice of the film (render_full runs several)
        i0, i1, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                               "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for i in range(i0, i1):
            ff.stdin.write(compose(i / FPS).tobytes())
            if (i - i0) % 240 == 0:
                print(f"chunk {i0}-{i1}: {i / FPS:6.1f}s", flush=True)
        ff.stdin.close(); ff.wait()
        return
    if sys.argv[1] in ("render_full", "full"):                    # the whole episode, in parallel slices
        assert FULL, "set EP03_FULL=1"
        jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        n = int(DUR * FPS)
        w = np.where(np.arange(n) / FPS < X7B + 0.3, 4.0, 1.0)   # the cold open's frames cost about 4x (Blender, chrome)
        cw = np.cumsum(w)
        cuts = [0] + [int(np.searchsorted(cw, cw[-1] * k / jobs)) for k in range(1, jobs)] + [n]
        parts, procs = [], []
        for k in range(jobs):
            part = os.path.join(BUILD, f"full_{'clean_' if NO_CAPTIONS else ''}part{k}.mp4")
            parts.append(part)
            procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), "chunk", str(cuts[k]), str(cuts[k + 1]), part]))
        codes = [p.wait() for p in procs]
        assert all(c == 0 for c in codes), codes
        lst = os.path.join(BUILD, "full_clean_parts.txt" if NO_CAPTIONS else "full_parts.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        silent_full = os.path.join(BUILD, "ep03_full_clean_silent.mp4" if NO_CAPTIONS else "ep03_full_silent.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent_full], check=True)
        print(silent_full, flush=True)
        if sys.argv[1] == "render_full" or NO_CAPTIONS:
            return
    if sys.argv[1] in ("sound_full", "full"):                     # events, score, mix, then onto the picture
        import mix_full
        import mix_open
        collect_events()
        score_full()
        audio = mix_full.main()
        mix_open.mux(os.path.join(BUILD, "ep03_full_silent.mp4"), audio, os.path.join(BUILD, "ep03_full.mp4"), crf=20,
                     maxrate="5000k", abr="192k")
        return
    silent = os.path.join(BUILD, "style_S_ascii_silent.mp4")
    if sys.argv[1] == "mix":                                      # a new score on the picture already rendered
        import mix_open
        collect_events()
        audio = mix_open.build_mix(extra=EXTRA_SFX, out_name="ascii_mix.wav", bed_path=score(), bed_lufs=-17.0)
        mix_open.mux(silent, audio, os.path.join(BUILD, "style_S_ascii.mp4"), crf=21, maxrate="3600k", abr="192k")
        return
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        ff.stdin.write(compose(i / FPS).tobytes())
        if i % 120 == 0:
            print(f"{i / FPS:5.1f}s / {DUR:.1f}s", flush=True)
    ff.stdin.close(); ff.wait()
    import mix_open
    collect_events()
    audio = mix_open.build_mix(extra=EXTRA_SFX, out_name="ascii_mix.wav", bed_path=score(), bed_lufs=-17.0)
    mix_open.mux(silent, audio, os.path.join(BUILD, "style_S_ascii.mp4"), crf=21, maxrate="3600k", abr="192k")


if __name__ == "__main__":
    main()
