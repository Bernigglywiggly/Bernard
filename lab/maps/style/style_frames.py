#!/usr/bin/env python3
"""STYLE FRAMES for the maps channel (10 Oct 2026). One scene, the Strait of Hormuz narrows, rendered in six directions.

    P=~/youtube/.venv/bin/python
    $P style_frames.py                 # every still + sheet.jpg
    $P style_frames.py A B             # only those stills
    $P style_frames.py video C E       # C_neon.mp4, E_flow.mp4
    $P style_frames.py sheet

Geography: Natural Earth 10m land (lab/curvelf/data). Relief: NOAA NCEI ETOPO 2022, 15 arc-second (public domain),
subset 54-58.5E 24.5-28N fetched from the CoastWatch ERDDAP into data/etopo2022_15s_hormuz.npz. Lanes are the film's
schematic lanes (script.py Z_INBOUND / Z_OUTBOUND); attack pins are the film's approximate October positions.
"""
import json
import math
import os
import subprocess
import sys

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FONTDIR = os.path.join(REPO, "a01_v6", "fonts")
NE = os.path.join(REPO, "lab", "curvelf", "data", "ne_10m_land.geojson")
DEM = os.path.join(HERE, "data", "etopo2022_15s_hormuz.npz")
W, H = 1920, 1080

# ------------------------------------------------------------------ palette: highlighter inks on pure black
PAL = dict(
    cyan="#3DFFF2",      # water, navigation, the strait itself
    magenta="#FF2BD6",   # Iran
    yellow="#E6FF2E",    # oil: lanes, flows, the numbers that matter
    orange="#FF6A1A",    # danger: attacks, warnings
    violet="#A77BFF",    # data, sources, the quiet layer
    green="#39FF88",     # Oman
)
INK = "#F2F4F5"
DIM = "#8C949A"
UAE_COL = "#9AA3A9"


def rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)], np.float32) / 255.0


def col(h, a=1.0):
    r, g, b = (rgb(h) * 255).astype(int)
    return skia.Color(int(r), int(g), int(b), int(max(0, min(1, a)) * 255))


def mix(h1, h2, t):
    c = rgb(h1) * (1 - t) + rgb(h2) * t
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c)


_TF = {}


def font(name, size):
    if name not in _TF:
        _TF[name] = skia.Typeface.MakeFromFile(os.path.join(FONTDIR, name + ".ttf"))
    f = skia.Font(_TF[name], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def sans(s):
    return font("InterTight-600", s)


def light(s):
    return font("InterTight-300", s)


def medium(s):
    return font("InterTight-500", s)


def mono(s):
    return font("IBMPlexMono-500", s)


def halo(c, s, x, y, f, color, a=1.0, track=0.0, align="left", r=7, ha=0.9):
    text(c, s, x, y, f, "#000000", ha, track, align, paint=skia.Paint(Color=col("#000000", ha), AntiAlias=True,
         MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r)))
    text(c, s, x, y, f, "#000000", ha, track, align, paint=skia.Paint(Color=col("#000000", ha), AntiAlias=True,
         MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.4)))
    return text(c, s, x, y, f, color, a, track, align)


def tri(c, x, y, r, hx, up=True):
    p = skia.Path()
    k = -1 if up else 1
    p.addPoly([skia.Point(x, y + k * r), skia.Point(x - r * 0.9, y - k * r * 0.6), skia.Point(x + r * 0.9, y - k * r * 0.6)], True)
    c.drawPath(p, skia.Paint(Color=col(hx), AntiAlias=True))


def tw(s, f, track=0.0):
    return f.measureText(s) + track * max(0, len(s) - 1)


def text(c, s, x, y, f, color, a=1.0, track=0.0, align="left", paint=None):
    w = tw(s, f, track)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    p = paint or skia.Paint(Color=col(color, a), AntiAlias=True)
    if track == 0:
        c.drawString(s, x, y, f, p)
    else:
        for ch in s:
            c.drawString(ch, x, y, f, p)
            x += f.measureText(ch) + track
    return w


# ------------------------------------------------------------------ projection: the narrows, full bleed
LON_C, LAT_C, LAT_SPAN = 56.90, 26.45, 1.60
KY = H / LAT_SPAN
KX = KY * math.cos(math.radians(LAT_C))
LON0, LON1 = LON_C - W / 2 / KX, LON_C + W / 2 / KX
LAT0, LAT1 = LAT_C - LAT_SPAN / 2, LAT_C + LAT_SPAN / 2


def px(lon, lat):
    return W / 2 + (lon - LON_C) * KX, H / 2 - (lat - LAT_C) * KY


def PX(pts):
    return np.array([px(a, b) for a, b in pts], np.float64)


# ------------------------------------------------------------------ the film's scene (lab/maps/hormuz/script.py)
LARAK = (56.356, 26.853)
QUOIN = (56.529, 26.494)
HORMUZ_I = (56.460, 27.068)
QESHM = (55.773, 26.768)
BANDAR_ABBAS = (56.288, 27.196)
Z_INBOUND = [(56.088, 26.408), (56.23, 26.514), (56.416, 26.591), (56.581, 26.573), (56.688, 26.405), (56.728, 26.122),
             (56.765, 26.126), (56.724, 26.414), (56.604, 26.599), (56.409, 26.624), (56.21, 26.542), (56.064, 26.433)]
Z_OUTBOUND = [(56.112, 26.382), (56.25, 26.486), (56.424, 26.559), (56.559, 26.547), (56.652, 26.395), (56.692, 26.118),
              (56.655, 26.114), (56.616, 26.386), (56.536, 26.521), (56.431, 26.526), (56.27, 26.458), (56.136, 26.357)]
OCT_HITS = [(56.46, 26.40), (56.505, 26.26), (56.52, 26.42)]   # film's approximate positions; #2 nudged 0.025E so its ring clears Musandam


def centre(zone):
    n = len(zone) // 2
    return [((zone[k][0] + zone[-1 - k][0]) / 2, (zone[k][1] + zone[-1 - k][1]) / 2) for k in range(n)]


LANE_IN = centre(Z_INBOUND)        # listed west -> south; inbound traffic runs the other way
LANE_OUT = centre(Z_OUTBOUND)      # outbound: west -> east -> south


# ------------------------------------------------------------------ polylines
def chaikin(p, n=3):
    p = np.asarray(p, np.float64)
    for _ in range(n):
        q = np.empty((2 * (len(p) - 1) + 2, 2))
        q[0], q[-1] = p[0], p[-1]
        q[1:-1:2] = 0.75 * p[:-1] + 0.25 * p[1:]
        q[2:-1:2] = 0.25 * p[:-1] + 0.75 * p[1:]
        p = q
    return p


def resample(p, step):
    p = np.asarray(p, np.float64)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    n = max(2, int(d[-1] / step) + 1)
    s = np.linspace(0, d[-1], n)
    return np.c_[np.interp(s, d, p[:, 0]), np.interp(s, d, p[:, 1])], s


def normals(p):
    t = np.gradient(p, axis=0)
    t /= np.maximum(1e-9, np.hypot(t[:, 0], t[:, 1]))[:, None]
    return np.c_[-t[:, 1], t[:, 0]]


def skpath(p, close=False):
    path = skia.Path()
    path.addPoly([skia.Point(float(x), float(y)) for x, y in p], close)
    return path


# ------------------------------------------------------------------ geography, once
def land_rings():
    out = []
    mx, my = 0.3, 0.3
    for ft in json.load(open(NE))["features"]:
        for ring in ft["geometry"]["coordinates"]:
            a = np.asarray(ring, np.float64)
            if a[:, 0].max() < LON0 - mx or a[:, 0].min() > LON1 + mx or a[:, 1].max() < LAT0 - my or a[:, 1].min() > LAT1 + my:
                continue
            out.append(a)
    return out


class Geo:
    def __init__(self):
        self.rings = land_rings()
        ss = 3
        img = np.zeros((H * ss, W * ss), np.uint8)
        polys = []
        for a in self.rings:
            g = np.c_[(W / 2 + (a[:, 0] - LON_C) * KX) * ss, (H / 2 - (a[:, 1] - LAT_C) * KY) * ss]
            g = np.clip(g, -2000, max(W, H) * ss + 2000)
            polys.append(np.round(g * 16).astype(np.int32).reshape(-1, 1, 2))
        cv2.fillPoly(img, polys, 255, lineType=cv2.LINE_AA, shift=4)
        self.land = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        self.country = self._countries()
        # nearest land's country, everywhere (tints any line near a coast)
        sea = (self.country == 0).astype(np.uint8)
        _, lab = cv2.distanceTransformWithLabels(sea, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys, xs = np.nonzero(sea == 0)
        lut = np.zeros(lab.max() + 1, np.uint8)
        lut[lab[ys, xs]] = self.country[ys, xs]
        self.near = lut[lab]
        self.dem = self._dem()
        self._grid()

    def _countries(self):
        """1 Iran, 2 Oman, 3 UAE, by connected land within the view (Iran and Arabia do not touch in it)."""
        m = (self.land > 0.5).astype(np.uint8)
        n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
        out = np.zeros((H, W), np.uint8)
        ix, iy = [int(v) for v in px(58.0, 27.0)]
        ax, ay = [int(v) for v in px(56.20, 25.95)]
        iran_id, arab_id = lab[iy, ix], lab[ay, ax]
        for k in range(1, n):
            lon = LON_C + (cen[k][0] - W / 2) / KX
            lat = LAT_C - (cen[k][1] - H / 2) / KY
            if k == iran_id:
                out[lab == k] = 1
            elif k == arab_id:
                out[lab == k] = 2
            elif lat < 26.6 and lon > 56.25:       # the Quoins and the Musandam islets
                out[lab == k] = 2
            elif lat < 25.9:                       # the UAE shore islets
                out[lab == k] = 3
            else:                                  # Qeshm, Hormuz, Larak, Hengam
                out[lab == k] = 1
        # Musandam (Oman) against the UAE: approximate border, Sha'm on the west coast to Dibba on the east
        x0, y0 = px(56.07, 26.05)
        x1, y1 = px(56.30, 25.62)
        yy, xx = np.mgrid[0:H, 0:W]
        side = (x1 - x0) * (yy - y0) - (y1 - y0) * (xx - x0)
        out[(out == 2) & (side > 0) & (yy > y0 - 5)] = 3
        return out

    def _dem(self):
        """ETOPO 2022 resampled onto the frame (metres; negative is depth)."""
        d = np.load(DEM)
        z, la, lo = d["z"], d["lat"], d["lon"]
        xs = (LON0 + (np.arange(W) + 0.5) / KX - lo[0]) / (lo[1] - lo[0])
        ys = (LAT1 - (np.arange(H) + 0.5) / KY - la[0]) / (la[1] - la[0])
        mx, my = np.meshgrid(xs.astype(np.float32), ys.astype(np.float32))
        return cv2.remap(z.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    def _grid(self, cw=12, ch=16):
        self.cw, self.ch = cw, ch
        cols, rows = W // cw, (H + ch - 1) // ch
        landp = np.zeros((rows * ch, cols * cw), np.float32)
        landp[:H] = self.land[:, :cols * cw]
        cov = landp.reshape(rows, ch, cols, cw).mean(axis=(1, 3))
        land = cov > 0.5
        pad = np.pad(land, 1, mode="edge")
        water_near = ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        coast = (land & water_near) | ((cov > 0.3) & ~land)
        dist = cv2.distanceTransform(np.pad(land, 1, mode="edge").astype(np.uint8), cv2.DIST_L1, 3)[1:-1, 1:-1]
        second = land & ~coast & (dist <= 2)
        inner = land & ~coast & ~second
        smc = cv2.GaussianBlur(cov.astype(np.float32), (0, 0), 0.9)
        gx = cv2.Sobel(smc, cv2.CV_32F, 1, 0, ksize=3) / cw
        gy = cv2.Sobel(smc, cv2.CV_32F, 0, 1, ksize=3) / ch
        ang = np.degrees(np.arctan2(gx, -gy)) % 180.0
        ori = np.select([(ang < 22.5) | (ang >= 157.5), ang < 67.5, ang < 112.5], ["-", "\\", "|"], "/")
        cy = np.clip((np.arange(rows) + 0.5) * ch, 0, H - 1).astype(int)
        cx = ((np.arange(cols) + 0.5) * cw).astype(int)
        self.cells = dict(cols=cols, rows=rows, cov=cov, coast=coast, second=second, inner=inner, ori=ori,
                          cty=self.near[np.ix_(cy, cx)], sea_d=cv2.distanceTransform(np.pad(cov < 0.05, 1, mode="edge").astype(np.uint8), cv2.DIST_L1, 3)[1:-1, 1:-1])

    def coast_runs(self, margin=60):
        """Coastline as pixel polylines, split where the country of the shore changes."""
        runs = []
        for a in self.rings:
            p = PX(a)
            ins = (p[:, 0] > -margin) & (p[:, 0] < W + margin) & (p[:, 1] > -margin) & (p[:, 1] < H + margin)
            d = np.diff(ins.astype(np.int8), prepend=0, append=0)
            for s0, s1 in zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]):
                q = p[s0:s1]
                if len(q) < 2:
                    continue
                qi = np.clip(q.astype(int), [0, 0], [W - 1, H - 1])
                cc = self.near[qi[:, 1], qi[:, 0]]
                br = np.nonzero(np.diff(cc))[0]
                st = 0
                for b in list(br) + [len(q) - 1]:
                    seg = q[st:b + 2]
                    if len(seg) >= 2:
                        runs.append((int(cc[min(st + 1, len(cc) - 1)]), seg))
                    st = b + 1
        return runs


_GEO = None


def geo():
    global _GEO
    if _GEO is None:
        _GEO = Geo()
    return _GEO


CTY_NAME = {1: "magenta", 2: "green", 3: None}


def cty_hex(k):
    return PAL[CTY_NAME[k]] if CTY_NAME.get(k) else UAE_COL


# ------------------------------------------------------------------ raster plumbing
def surface():
    return skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))


def snap(s):
    return s.makeImageSnapshot().toarray(alphaType=skia.kPremul_AlphaType)[..., :3].astype(np.float32) / 255.0


def alpha_of(s):
    return s.makeImageSnapshot().toarray()[..., 3].astype(np.float32) / 255.0


def to_image(a):
    u8 = np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8)
    rgba = np.dstack([u8, np.full(u8.shape[:2], 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)


def blur(a, sigma):
    d = max(1, int(sigma / 3))
    if d == 1:
        return cv2.GaussianBlur(a, (0, 0), sigma)
    h, w = a.shape[:2]
    sm = cv2.resize(a, (w // d, h // d), interpolation=cv2.INTER_AREA)
    sm = cv2.GaussianBlur(sm, (0, 0), sigma / d)
    return cv2.resize(sm, (w, h), interpolation=cv2.INTER_LINEAR)


def bloom(a, spec=((3, 0.55), (10, 0.45), (32, 0.32), (90, 0.16))):
    out = np.zeros_like(a)
    for s, wgt in spec:
        out += wgt * blur(a, s)
    return out


def screen(a, b):
    return 1 - (1 - np.clip(a, 0, 1)) * (1 - np.clip(b, 0, 1))


def tint(mask, colour_field):
    return mask[..., None] * colour_field


def country_field(near=True, alpha=None):
    g = geo()
    lut = np.zeros((4, 3), np.float32)
    for k in (1, 2, 3):
        lut[k] = rgb(cty_hex(k))
    return lut[g.near if near else g.country]


def grain(a, amt=0.018, seed=1):
    r = np.random.default_rng(seed)
    n = r.normal(0, 1, (H, W)).astype(np.float32)
    return np.clip(a + amt * n[..., None] * (0.35 + a), 0, 1)


def vignette(a, k=0.22):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
    return a * (1 - k * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]


def save(a, name, crisp=None):
    """a: float RGB. crisp(c): type drawn over the finished picture, never bloomed."""
    s = surface()
    c = s.getCanvas()
    c.drawImage(to_image(a), 0, 0)
    if crisp:
        crisp(c)
    out = s.makeImageSnapshot().toarray()[..., :3]
    cv2.imwrite(os.path.join(HERE, name), cv2.cvtColor(out, cv2.COLOR_RGB2BGR))
    print("wrote", name)
    return out


# ------------------------------------------------------------------ the typographic map (the engine's look)
def draw_glyphs(c, colour_of, a_coast=1.0, a_second=0.5, a_inner=0.28, only=None):
    """Coast cells as oriented strokes (- | / \\), then a ':' rim, then a quiet '·' field. colour_of(country) -> hex|None."""
    g = geo()
    k = g.cells
    f = mono(g.ch * 0.95)
    gw = f.measureText("#")
    for j in range(k["rows"]):
        y = (j + 0.78) * g.ch
        for mask, glyph, a in ((k["inner"][j], "·", a_inner), (k["second"][j], ":", a_second), (k["coast"][j], None, a_coast)):
            if a <= 0:
                continue
            ii = np.nonzero(mask)[0]
            if not len(ii):
                continue
            byc = {}
            for q in ii:
                byc.setdefault(int(k["cty"][j, q]), []).append(q)
            for cty, qs in byc.items():
                if only and cty not in only:
                    continue
                hx = colour_of(cty)
                if hx is None:
                    continue
                s_ = "".join(k["ori"][j, q] for q in qs) if glyph is None else glyph * len(qs)
                xs = [q * g.cw + (g.cw - gw) / 2 for q in qs]
                c.drawTextBlob(skia.TextBlob.MakeFromPosTextH(s_, xs, y, f), 0, 0, skia.Paint(Color=col(hx, a), AntiAlias=True))


def coast_stroke(c, colour_of, width=1.6, a=0.9, simplify=0.0):
    for cty, seg in geo().coast_runs():
        hx = colour_of(cty)
        if hx is None:
            continue
        if simplify > 0 and len(seg) > 3:
            seg = cv2.approxPolyDP(seg.astype(np.float32).reshape(-1, 1, 2), simplify, False).reshape(-1, 2)
        c.drawPath(skpath(seg), skia.Paint(Color=col(hx, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=width,
                                           StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap))


def land_fill(c, colour_of, a=0.08):
    g = geo()
    for k in (1, 2, 3):
        hx = colour_of(k)
        if hx is None:
            continue
        m = (g.country == k).astype(np.float32) * g.land
        rgba = np.zeros((H, W, 4), np.uint8)
        rgba[..., :3] = (rgb(hx) * 255).astype(np.uint8)
        rgba[..., 3] = (m * 255 * a).astype(np.uint8)
        c.drawImage(skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType), 0, 0)


# ------------------------------------------------------------------ highlighter marks
def marker(c, pts, width, hx, a=0.9, seed=0, streaks=True, taper=True):
    """A highlighter pen swiped along pts: parallel nib streaks, ragged ends, slight pressure wobble."""
    r = np.random.default_rng(seed)
    p, s = resample(chaikin(pts, 2) if len(pts) > 2 else pts, 2.0)
    n = normals(p)
    L = s[-1]
    K = max(4, int(width / 2.2)) if streaks else 1
    lay = skia.Paint(BlendMode=skia.BlendMode.kSrcOver)
    c.saveLayer(None, skia.Paint(Color=col("#FFFFFF", a)))
    for k in range(K):
        off = (-0.5 + (k + 0.5) / K) * width
        wob = np.sin(s / (60 + 40 * r.random()) + r.random() * 6) * 0.6
        q = p + n * (off + wob)[:, None]
        t0 = r.uniform(0, 0.012 * L + 5) if taper else 0
        t1 = L - (r.uniform(0, 0.012 * L + 5) if taper else 0)
        keep = (s >= t0) & (s <= t1)
        if keep.sum() < 2:
            continue
        aa = (0.55 + 0.45 * r.random()) if streaks else 1.0
        c.drawPath(skpath(q[keep]), skia.Paint(Color=col(hx, aa), AntiAlias=True, Style=skia.Paint.kStroke_Style,
                                               StrokeWidth=width / K * 1.25 if streaks else width, StrokeCap=skia.Paint.kButt_Cap,
                                               StrokeJoin=skia.Paint.kRound_Join))
    c.restore()


def swipe_rect(x, y_base, w, cap, pad=14, slope=-0.012, seed=0):
    """Points for a swipe behind a word set at baseline y_base with cap height cap."""
    r = np.random.default_rng(seed)
    yc = y_base - cap * 0.5
    x0, x1 = x - pad - r.uniform(0, 6), x + w + pad + r.uniform(0, 8)
    return [(x0, yc + r.uniform(-1.5, 1.5)), ((x0 + x1) / 2, yc + slope * (x1 - x0) / 2 + r.uniform(-1, 1)), (x1, yc + slope * (x1 - x0) + r.uniform(-1.5, 1.5))]


def hl_label(c_glow, s, x, y, size, hx, seed=0, f=None, track=0.0, pad=None):
    """The swipe (glows) for a highlighted word; returns what the crisp pass needs to set the word on it."""
    f = f or sans(size)
    w = tw(s, f, track)
    cap = size * 0.73
    pts = swipe_rect(x, y, w, cap, pad=pad if pad is not None else size * 0.28, seed=seed)
    marker(c_glow, pts, cap * 1.62, hx, a=0.92, seed=seed)
    return (s, x, y, f, track)


def ink_word(c, item, hx="#060606"):
    s, x, y, f, track = item
    text(c, s, x, y, f, hx, 1.0, track)


# ------------------------------------------------------------------ chrome: the channel's header and the meta line
def scrim(c):
    for y0, y1, up in ((0, 96, True), (H - 96, H, False)):
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)],
                                            [col("#000000", 0.82), col("#000000", 0.0)] if up else [col("#000000", 0.0), col("#000000", 0.95)])
        c.drawRect(skia.Rect.MakeLTRB(0, y0, W, y1), skia.Paint(Shader=sh))


def chrome(c, tag, chapter, hero, foot):
    scrim(c)
    m = mono(17)
    c.drawRect(skia.Rect.MakeXYWH(44, 34, 12, 12), skia.Paint(Color=col(hero)))
    text(c, "MAPS & POWER", 66, 46, m, INK, 0.92, 1.2)
    text(c, chapter, W - 330, 46, m, hero, 1.0, 1.2, "right")
    text(c, "26.45°N  056.90°E", W - 44, 46, m, INK, 0.75, 1.2, "right")
    c.drawRect(skia.Rect.MakeXYWH(44, 62, 210, 2), skia.Paint(Color=col(hero, 0.9)))
    text(c, tag, 44, H - 38, mono(15), DIM, 0.95, 1.4)
    text(c, foot, W - 44, H - 38, mono(15), DIM, 0.8, 1.2, "right")


def corner_frame(c, r, hx, a=0.9, tick=18, wdt=2):
    p = skia.Paint(Color=col(hx, a), AntiAlias=True, StrokeWidth=wdt)
    x0, y0, x1, y1 = r
    for (x, y, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        c.drawLine(x, y, x + dx * tick, y, p)
        c.drawLine(x, y, x, y + dy * tick, p)


TAILS = [[(55.40, 26.29), (55.80, 26.31), LANE_OUT[0]], [LANE_OUT[-1], (56.84, 25.80), (56.98, 25.66)],
         [(55.40, 26.47), (55.80, 26.46), LANE_IN[0]], [LANE_IN[-1], (56.90, 25.82), (57.04, 25.66)]]


def lane_tails(c, hx, a=0.75, wdt=1.6):
    """The lanes' approaches as dashed hairlines (schematic), so the lanes don't stop in open water."""
    if a <= 0:
        return
    p = skia.Paint(Color=col(hx, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=wdt,
                   PathEffect=skia.DashPathEffect.Make([7, 7], 0))
    for t in TAILS:
        c.drawPath(skpath(chaikin(PX(t), 3)), p)


def border_dash(c, a=0.6):
    """Musandam (Oman) / UAE, approximate, drawn where it crosses land."""
    p = skia.Paint(Color=col(UAE_COL, a), AntiAlias=True, StrokeWidth=1.4, PathEffect=skia.DashPathEffect.Make([4, 5], 0))
    x0, y0 = px(56.07, 26.05)
    x1, y1 = px(56.30, 25.62)
    g = geo()
    pts = [(x0 + (x1 - x0) * k / 200, y0 + (y1 - y0) * k / 200) for k in range(201)]
    on = [g.land[int(min(H - 1, y)), int(min(W - 1, x))] > 0.5 for x, y in pts]
    for k in range(200):
        if on[k] and on[k + 1]:
            c.drawLine(*pts[k], *pts[k + 1], p)


# ======================================================================= A · HIGHLIGHTER
CARD = (1372, 610, 1852, 948)          # the number card, on Iran's shore east of the strait
CX = CARD[0] + 222                     # the card's text column
ATK = (96, 700)                        # the attacks label, in open Gulf water west of Musandam (leader to the pins)


def atk_leader(c, hx, a=0.9):
    ax, ay = px(*OCT_HITS[0])
    c.drawLine(ATK[0] + 300, ATK[1] - 12, ax - 16, ay + 6, skia.Paint(Color=col(hx, a), AntiAlias=True, StrokeWidth=1.4))


def frame_A():
    g = geo()
    hexof = cty_hex
    glow = surface()
    c = glow.getCanvas()
    # land: a whisper of its colour, the typographic coast in full ink
    land_fill(c, lambda k: hexof(k) if k != 3 else None, 0.10)
    draw_glyphs(c, hexof, 1.0, 0.55, 0.30)
    lane_tails(c, PAL["yellow"], 0.8)
    coast_stroke(c, hexof, 1.8, 0.95)
    # sea furniture, cyan: graticule crosses every half degree
    gp = skia.Paint(Color=col(PAL["cyan"], 0.35), AntiAlias=True, StrokeWidth=1.3)
    for lo in np.arange(55.5, 58.6, 0.5):
        for la in np.arange(25.5, 27.4, 0.5):
            x, y = px(lo, la)
            if 0 < x < W and 0 < y < H and g.land[int(min(H - 1, y)), int(min(W - 1, x))] < 0.1:
                c.drawLine(x - 7, y, x + 7, y, gp)
                c.drawLine(x, y - 7, x, y + 7, gp)
    # the lanes: oil, so yellow; a fat highlighter swipe down each
    for k, lane in enumerate((LANE_OUT, LANE_IN)):
        marker(c, PX(lane), 21, PAL["yellow"], 0.88, seed=11 + k)
    # attacks: orange, hot centres
    for k, (lo, la) in enumerate(OCT_HITS):
        x, y = px(lo, la)
        c.drawCircle(x, y, 17, skia.Paint(Color=col(PAL["orange"], 0.95), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3))
        c.drawCircle(x, y, 7, skia.Paint(Color=col(PAL["orange"], 1.0), AntiAlias=True))
    # highlighted words
    words = []
    words.append((hl_label(c, "STRAIT OF HORMUZ", 600, 395, 50, PAL["cyan"], seed=3), "#050505"))
    words.append((hl_label(c, "IRAN", 1540, 168, 62, PAL["magenta"], seed=5, track=6), "#050505"))
    words.append((hl_label(c, "OMAN", 476, 812, 46, PAL["green"], seed=7, track=5), "#050505"))
    words.append((hl_label(c, "QESHM", 206, 268, 30, PAL["magenta"], seed=8, track=3), "#050505"))
    words.append((hl_label(c, "ATTACKS 1–8 OCT", ATK[0], ATK[1], 28, PAL["orange"], seed=9, track=1), "#050505"))
    words.append((hl_label(c, "SHIPS CROSSED", CX, CARD[1] + 150, 30, PAL["yellow"], seed=12, track=1), "#050505"))
    # the card's big number glows with everything else
    x0, y0, x1, y1 = CARD
    text(c, "8", x0 + 40, y0 + 262, sans(270), PAL["yellow"])
    G = snap(glow)
    # plate under the card (drawn under the glow pass so the bloom wraps it)
    base = G.copy()
    pl = np.zeros((H, W), np.float32)
    pl[y0:y1, x0:x1] = 1
    pl = cv2.GaussianBlur(pl, (0, 0), 6)
    base = base * (1 - 0.86 * pl[..., None])
    # redraw the card content on top of the plate
    s2 = surface()
    c2 = s2.getCanvas()
    text(c2, "8", x0 + 40, y0 + 262, sans(270), PAL["yellow"])
    marker(c2, swipe_rect(CX, y0 + 150, tw("SHIPS CROSSED", sans(30), 1), 30 * 0.73, pad=8, seed=12), 30 * 0.73 * 1.62, PAL["yellow"], 0.92, seed=12)
    C2 = snap(s2)
    m2 = alpha_of(s2)
    base = base * (1 - m2[..., None]) + C2
    out = screen(base, bloom(G * 0.9))
    out = grain(vignette(out), 0.014)

    def crisp(c):
        for item, ink in words:
            ink_word(c, item, ink)
        # labels' second lines
        text(c, "26.6N 56.4E · LANES ON THE OMANI SIDE", 600, 432, mono(17), PAL["cyan"], 0.95, 1.2)
        text(c, "QESHM · HORMUZ · LARAK", 1540, 204, mono(16), PAL["magenta"], 0.9, 1.2)
        text(c, "MUSANDAM", 478, 846, mono(17), PAL["green"], 0.95, 1.6)
        border_dash(c)
        text(c, "UAE", 436, 962, mono(15), UAE_COL, 0.9, 3)
        text(c, "POSITIONS APPROX.", ATK[0], ATK[1] + 32, mono(15), PAL["orange"], 0.95, 1.0)
        text(c, "UKMTO · WINDWARD", ATK[0], ATK[1] + 52, mono(15), PAL["orange"], 0.95, 1.0)
        text(c, "↑ IN", *px(56.80, 26.50), mono(15), PAL["yellow"], 0.95, 1)
        text(c, "OUT ↓", *px(56.645, 26.10), mono(15), PAL["yellow"], 0.95, 1, "right")
        lp = skia.Paint(Color=col(PAL["orange"], 0.9), AntiAlias=True, StrokeWidth=1.4)
        atk_leader(c, PAL["orange"])
        corner_frame(c, CARD, PAL["violet"], 0.95)
        text(c, "CMP 04.03 · 8 OCT 2026", x0 + 26, y0 + 34, mono(14), PAL["violet"], 0.95, 1.2)
        text(c, "8 OCT 2026 · 5 IN · 3 OUT", CX, y0 + 196, mono(15), PAL["yellow"], 0.95, 1.0)
        text(c, "WAS ≈125 A DAY", CX, y0 + 238, sans(30), INK, 1.0)
        text(c, "BEFORE 28 FEB", CX, y0 + 272, sans(30), INK, 0.55)
        text(c, "WINDWARD · AL JAZEERA / AFP", x0 + 26, y1 - 22, mono(13), PAL["violet"], 0.9, 1.2)
        chrome(c, "A · HIGHLIGHTER — FLAT INK, SOFT BLOOM, MARKER SWIPES", "04  THE CLOSING", PAL["orange"],
               "COAST: NATURAL EARTH 10M · LANES SCHEMATIC · BORDERS APPROX.")
    return save(out, "A_highlighter.png", crisp)


# ======================================================================= B · TOPOGRAPHIC (real relief)
def contour_paths(z, levels):
    import contourpy
    gen = contourpy.contour_generator(z=z, line_type=contourpy.LineType.Separate)
    return {lv: [np.asarray(l, np.float64) for l in gen.lines(lv)] for lv in levels}


def topo_colour(lv):
    if lv < 0:
        d = -lv
        t = min(1, math.log(d / 20.0) / math.log(270 / 20.0))
        stops = [(0, "#5FFFF4"), (0.35, "#3DB8FF"), (0.65, "#5A6BFF"), (1.0, "#9B4BFF")]
    else:
        t = min(1, (lv - 200) / 1900.0)
        stops = [(0, "#39FF88"), (0.4, "#E6FF2E"), (0.75, "#FF9A1A"), (1.0, "#FF4A3A")]
    for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
        if t <= t1:
            return mix(c0, c1, (t - t0) / max(1e-6, t1 - t0))
    return stops[-1][1]


SEA_LV = [-20 * k for k in range(1, 14)]          # every 20 m (the deepest water in view is 265 m)
LAND_LV = [200 * k for k in range(1, 11)]         # every 200 m (the highest ground in view is 2,087 m)


def topo_layer(c, alpha=1.0, wscale=1.0, labels=True, mono_hex=None):
    g = geo()
    z = cv2.GaussianBlur(g.dem, (0, 0), 2.2)
    sea_ok = g.land < 0.5
    paths = contour_paths(z, SEA_LV + LAND_LV)
    lbls = []
    for lv, ls in paths.items():
        idx = (lv < 0 and lv % 100 == 0) or (lv > 0 and lv % 1000 == 0)
        hx = mono_hex or topo_colour(lv)
        p = skia.Paint(Color=col(hx, alpha * (0.95 if idx else 0.72)), AntiAlias=True, Style=skia.Paint.kStroke_Style,
                       StrokeWidth=(2.1 if idx else 1.05) * wscale, StrokeJoin=skia.Paint.kRound_Join)
        for l in ls:
            if len(l) < 6:
                continue
            # sea contours stay in the sea, land contours on land (ETOPO's shoreline and Natural Earth's differ a little)
            li = np.clip(l.astype(int), [0, 0], [W - 1, H - 1])
            ok = sea_ok[li[:, 1], li[:, 0]] if lv < 0 else ~sea_ok[li[:, 1], li[:, 0]]
            d = np.diff(ok.astype(np.int8), prepend=0, append=0)
            for s0, s1 in zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]):
                if s1 - s0 < 5:
                    continue
                seg = l[s0:s1]
                c.drawPath(skpath(seg), p)
                if idx and labels and s1 - s0 > 160:
                    q = seg[len(seg) // 2]
                    if 60 < q[0] < W - 60 and 90 < q[1] < H - 90:
                        a = seg[min(len(seg) - 1, len(seg) // 2 + 6)] - seg[max(0, len(seg) // 2 - 6)]
                        lbls.append((lv, q, math.degrees(math.atan2(a[1], a[0])), hx))
    return lbls


def frame_B():
    g = geo()
    s = surface()
    c = s.getCanvas()
    lbls = topo_layer(c)
    # the typographic coast, white, over the relief
    draw_glyphs(c, lambda k: INK, 0.95, 0.0, 0.0)
    coast_stroke(c, lambda k: INK, 1.3, 0.75)
    # lanes as survey hairlines, attacks as small crosses
    lane_tails(c, PAL["yellow"], 0.7, 1.2)
    for z_ in (Z_INBOUND, Z_OUTBOUND):
        c.drawPath(skpath(chaikin(PX(z_ + z_[:2]), 3)[4:-4], True), skia.Paint(Color=col(PAL["yellow"], 0.95), AntiAlias=True,
                   Style=skia.Paint.kStroke_Style, StrokeWidth=1.6))
    for lo, la in OCT_HITS:
        x, y = px(lo, la)
        pp = skia.Paint(Color=col(PAL["orange"], 1.0), AntiAlias=True, StrokeWidth=2.4, Style=skia.Paint.kStroke_Style)
        c.drawLine(x - 9, y - 9, x + 9, y + 9, pp)
        c.drawLine(x - 9, y + 9, x + 9, y - 9, pp)
        c.drawCircle(x, y, 15, pp)
    A = snap(s)
    out = screen(A, bloom(A, ((2.5, 0.5), (9, 0.3), (30, 0.16))))
    # spot heights from the data
    zz = g.dem.copy()
    zz[:110] = 0
    zz[H - 110:] = 0
    hi = np.unravel_index(np.argmax(np.where(g.land > 0.5, zz, -9e9)), zz.shape)
    dd = np.load(DEM)                        # the label quotes the raw 15" grid, not the resampled frame
    m_ = (dd["lon"][None, :] >= LON0) & (dd["lon"][None, :] <= LON1) & (dd["lat"][:, None] >= LAT0) & (dd["lat"][:, None] <= LAT1)
    zmax, zmin = float(dd["z"][m_].max()), float(dd["z"][m_].min())
    lo_ = np.unravel_index(np.argmin(np.where(g.land < 0.5, zz, 9e9)), zz.shape)
    lane_d = [g.dem[int(y), int(x)] for x, y in resample(PX(LANE_OUT), 3)[0]]
    out = grain(vignette(out, 0.18), 0.012)
    x0, y0, x1, y1 = CARD

    def crisp(c):
        for lv, q, ang, hx in lbls:
            c.save()
            c.translate(q[0], q[1])
            a = ang if -90 <= ang <= 90 else ang + 180
            c.rotate(a)
            s_ = f"{abs(lv):,}"
            f = mono(13)
            w = f.measureText(s_)
            c.drawRect(skia.Rect.MakeXYWH(-w / 2 - 4, -9, w + 8, 14), skia.Paint(Color=col("#000000", 1.0)))
            text(c, s_, 0, 4, f, hx, 1.0, 0, "center")
            c.restore()
        for (yy, xx), lab, hx, up in ((hi, f"{int(round(zmax)):,} M · HIGHEST IN VIEW", PAL["orange"], True),
                                      (lo_, f"{int(round(-zmin)):,} M · DEEPEST IN VIEW", "#B07BFF", False)):
            tri(c, xx, yy, 7, hx, up)
            right = xx > W - 420
            lx_ = xx - 14 if right else xx + 60
            ly_ = yy + 5 if right else yy - 28
            if not right:
                c.drawLine(xx + 6, yy - 6, lx_ - 4, ly_ + 4, skia.Paint(Color=col(hx, 0.9), AntiAlias=True, StrokeWidth=1.2))
            halo(c, lab, lx_, ly_, mono(15), INK, 1.0, 1, "right" if right else "left", r=8, ha=1.0)
        halo(c, "I R A N", 1530, 168, medium(58), INK, 1.0, 10, r=12, ha=1.0)
        halo(c, "O M A N", 470, 812, medium(42), INK, 1.0, 7, r=12, ha=1.0)
        halo(c, "MUSANDAM", 472, 842, mono(15), INK, 0.9, 2, r=8, ha=1.0)
        halo(c, "QESHM", 210, 268, medium(30), INK, 1.0, 5)
        halo(c, "STRAIT  OF  HORMUZ", 590, 380, medium(44), INK, 1.0, 4, r=10)
        halo(c, f"OUTBOUND LANE: {int(round(-max(lane_d)))}–{int(round(-min(lane_d)))} M OF WATER (ETOPO)", 592, 412, mono(15), PAL["cyan"], 1.0, 1)
        halo(c, "ATTACKS 1–8 OCT", ATK[0], ATK[1], mono(16), PAL["orange"], 1.0, 1)
        halo(c, "POSITIONS APPROX.", ATK[0], ATK[1] + 22, mono(14), PAL["orange"], 0.9, 1)
        c.drawLine(ATK[0] + 200, ATK[1] - 6, px(*OCT_HITS[0])[0] - 18, px(*OCT_HITS[0])[1] + 6, skia.Paint(Color=col(PAL["orange"], 0.8), AntiAlias=True, StrokeWidth=1.2))
        # card
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Color=col("#000000", 0.95)))
        c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Color=col(INK, 0.5), Style=skia.Paint.kStroke_Style, StrokeWidth=1))
        text(c, "8", x0 + 34, y0 + 262, light(270), INK, 1.0)
        text(c, "SHIPS CROSSED", CX, y0 + 140, sans(30), INK, 1.0)
        text(c, "8 OCT 2026 · 5 IN · 3 OUT", CX, y0 + 176, mono(15), PAL["yellow"], 1.0, 1)
        text(c, "WAS ≈125 A DAY", CX, y0 + 236, sans(28), INK, 0.65)
        text(c, "BEFORE 28 FEB", CX, y0 + 268, sans(28), INK, 0.4)
        text(c, "WINDWARD · AL JAZEERA / AFP", x0 + 22, y1 - 20, mono(13), DIM, 1.0, 1.2)
        # legend: the ramp, sea to summit
        lx, ly, lw = 44, H - 124, 520
        c.drawRect(skia.Rect.MakeXYWH(lx - 16, ly - 36, lw + 52, 80), skia.Paint(Color=col("#000000", 0.8)))
        for k in range(lw):
            t = k / (lw - 1)
            lv = min(-20, -270 * (1 - t / 0.45)) if t < 0.45 else 200 + (t - 0.45) / 0.55 * 1900
            c.drawRect(skia.Rect.MakeXYWH(lx + k, ly, 1.2, 8), skia.Paint(Color=col(topo_colour(lv))))
        f = mono(13)
        for t, s_ in ((0, "−270"), (0.45 * (1 - 100 / 270), "−100"), (0.45, "0"), (0.45 + 0.55 * 800 / 1900, "1,000"), (1.0, f"{int(math.ceil(zmax / 100) * 100):,} M")):
            text(c, s_, lx + t * lw, ly + 28, f, DIM, 1.0, 1, "left" if t == 0 else ("right" if t == 1 else "center"))
        text(c, "CONTOURS · SEA EVERY 20 M · LAND EVERY 200 M", lx, ly - 12, f, INK, 0.85, 1)
        chrome(c, "B · TOPOGRAPHIC — REAL RELIEF: NOAA NCEI ETOPO 2022 15″, PUBLIC DOMAIN", "02  THE GAP", PAL["cyan"],
               "COAST: NATURAL EARTH 10M · LANES SCHEMATIC")
    return save(out, "B_topographic.png", crisp)


# ======================================================================= C · NEON
def glyph_outline(s, x, y, f, track=0.0):
    """Each letter's outline as its own path, placed (for letter-by-letter ignition)."""
    gl = f.textToGlyphs(s)
    xs = f.getXPos(gl)
    out = []
    for k, (gid, gx) in enumerate(zip(gl, xs)):
        p = f.getPath(gid)
        if p is None or p.countPoints() == 0:
            out.append(None)
            continue
        p.offset(x + gx + k * track, y)
        out.append(p)
    return out


class Neon:
    """Glass tubes: a pale core, the coloured gas, the coloured halo. Each element is rendered once, lit; a frame is a
    weighted sum (bloom is linear), so flicker costs nothing."""

    def __init__(self):
        self.els = {}
        self.glass = np.zeros((H, W, 3), np.float32)

    def add(self, name, paths, hx, wdt=4.0, halo=1.0):
        s = surface()
        c = s.getCanvas()
        gas = skia.Paint(Color=col(hx, 1.0), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=wdt,
                         StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        for p in paths:
            c.drawPath(p, gas)
        G = snap(s)
        s2 = surface()
        c2 = s2.getCanvas()
        core = skia.Paint(Color=col(mix(hx, "#FFFFFF", 0.8), 1.0), AntiAlias=True, Style=skia.Paint.kStroke_Style,
                          StrokeWidth=max(1.0, wdt * 0.38), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        for p in paths:
            c2.drawPath(p, core)
        Cc = snap(s2)
        lit = np.maximum(G * 0.95, Cc) + bloom(G, ((2.5, 0.85), (8, 0.7), (24, 0.5), (70, 0.30), (160, 0.12))) * halo
        ys, xs = np.nonzero(lit.max(axis=2) > 0.002)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        self.els[name] = ((y0, y1, x0, x1), lit[y0:y1, x0:x1].astype(np.float16))
        # unlit glass: a dim grey tube with a faint highlight
        s3 = surface()
        c3 = s3.getCanvas()
        for p in paths:
            c3.drawPath(p, skia.Paint(Color=col("#FFFFFF", 0.07), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=wdt + 1.5,
                                      StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join))
            c3.drawPath(p, skia.Paint(Color=col(hx, 0.10), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1, wdt * 0.3)))
        self.glass += snap(s3)

    def compose(self, I):
        out = self.glass.copy()
        for name, v in I.items():
            if v <= 0 or name not in self.els:
                continue
            (y0, y1, x0, x1), a = self.els[name]
            out[y0:y1, x0:x1] += a.astype(np.float32) * v
        return out


def stutter(t, t_on, seed, dur=0.55):
    """A tube striking: dark, a few failed blinks, a warm-up, then steady."""
    if t < t_on:
        return 0.0
    r = np.random.default_rng(seed)
    x = t - t_on
    if x >= dur:
        return 1.0
    ev = np.cumsum(r.uniform(0.025, 0.11, 10))
    on = (np.searchsorted(ev, x) % 2) == 0
    lvl = r.uniform(0.35, 1.1)
    return float(lvl * on * (0.4 + 0.6 * x / dur))


def hum(t, seed):
    r = np.random.default_rng(seed)
    ph = r.uniform(0, 6.28, 3)
    return 0.955 + 0.025 * math.sin(2 * math.pi * 1.7 * t + ph[0]) + 0.015 * math.sin(2 * math.pi * 9.3 * t + ph[1]) + 0.012 * math.sin(2 * math.pi * 23.1 * t + ph[2])


NEON_LABEL = [("STRAIT OF", 64, 872, 84), ("HORMUZ", 60, 974, 108)]


def build_neon():
    g = geo()
    N = Neon()
    # coast: bent glass along a simplified shoreline, per country
    groups = {1: [], 2: [], 3: []}
    for cty, seg in g.coast_runs(margin=-4):
        if len(seg) < 2:
            continue
        L = np.hypot(*np.diff(seg, axis=0).T).sum()
        if L < 40:
            continue
        q = cv2.approxPolyDP(seg.astype(np.float32).reshape(-1, 1, 2), 2.2, False).reshape(-1, 2)
        groups[cty].append(skpath(chaikin(q, 2)))
    N.add("iran", groups[1], PAL["magenta"], 3.2, 0.8)
    N.add("oman", groups[2], PAL["green"], 3.2, 0.8)
    N.add("uae", groups[3], "#B8C2C8", 2.4, 0.5)          # never lit: just glass
    for k, lane in enumerate((LANE_OUT, LANE_IN)):
        N.add(f"lane{k}", [skpath(chaikin(PX(lane), 3))], PAL["yellow"], 6.0, 1.1)
    k = 0
    for s, x, y, size in NEON_LABEL:
        for p in glyph_outline(s, x, y, light(size), 5):
            if p is not None:
                N.add(f"L{k}", [p], PAL["cyan"], 3.0, 1.0)
                k += 1
    # attack pins: an orange ring and a hot point
    for k, (lo, la) in enumerate(OCT_HITS):
        x_, y_ = px(lo, la)
        ring = skia.Path()
        ring.addCircle(x_, y_, 15)
        dot = skia.Path()
        dot.addCircle(x_, y_, 3.0)
        N.add(f"pin{k}", [ring, dot], PAL["orange"], 4.0, 1.25)
    # the number, in tube
    x0, y0, x1, y1 = CARD
    N.add("num", [p for p in glyph_outline("8", x0 + 40, y0 + 262, light(270)) if p], PAL["orange"], 4.0, 1.1)
    # underline tube under the card caption
    N.add("rule", [skpath([(CX, y0 + 168), (x0 + 452, y0 + 168)])], PAL["violet"], 3.0, 0.9)
    return N


def neon_levels(t, N):
    I = {}
    I["iran"] = stutter(t, 0.35, 1) * hum(t, 1)
    I["oman"] = stutter(t, 0.70, 2) * hum(t, 2)
    I["lane0"] = stutter(t, 1.35, 4) * hum(t, 4)
    I["lane1"] = stutter(t, 1.55, 5) * hum(t, 5)
    order = np.random.default_rng(9).permutation(14)
    for k in range(14):
        tk = 2.15 + 0.07 * order[k]
        v = stutter(t, tk, 20 + k, 0.45) * hum(t, 20 + k)
        if k == 13:                                     # the faulty 'Z': it buzzes and drops out
            for tb, d in ((4.05, 0.12), (5.62, 0.07), (5.78, 0.16), (6.55, 0.09)):
                if tb <= t < tb + d:
                    v *= 0.15 + 0.2 * ((int(t * 60) % 2))
        I[f"L{k}"] = v
    I["num"] = stutter(t, 3.45, 40, 0.9) * hum(t, 40)
    I["rule"] = stutter(t, 3.9, 41) * hum(t, 41)
    for k, ts in enumerate((4.6, 4.95, 5.2)):
        v = 0.0
        if t >= ts:
            x = t - ts
            v = 1.0 + 2.2 * math.exp(-x * 7) + 0.18 * math.sin(2 * math.pi * 1.1 * (t - ts))
        I[f"pin{k}"] = v * (stutter(t, ts - 0.12, 50 + k, 0.12) if t < ts else 1)
    return I


def sparks(t):
    """Particles off the first pin as it strikes: streaks that arc and die, plus a shock ring."""
    s = surface()
    c = s.getCanvas()
    for k, ts in enumerate((4.6, 4.95, 5.2)):
        x = t - ts
        if x < 0 or x > 1.6:
            continue
        cx, cy = px(*OCT_HITS[k])
        r = np.random.default_rng(70 + k)
        n = (70, 30, 30)[k]
        ang = r.uniform(0, 2 * math.pi, n)
        spd = r.uniform(140, 620, n) * (1.0 if k == 0 else 0.7)
        life = r.uniform(0.25, 0.95, n)
        for a, v, lf in zip(ang, spd, life):
            if x > lf:
                continue
            def pos(tt):
                return cx + math.cos(a) * v * tt, cy + math.sin(a) * v * tt + 520 * tt * tt
            p0, p1 = pos(max(0, x - 0.045)), pos(x)
            fade = 1 - x / lf
            c.drawLine(p0[0], p0[1], p1[0], p1[1], skia.Paint(Color=col(mix(PAL["orange"], "#FFF6D0", fade), fade), AntiAlias=True,
                                                               StrokeWidth=1.2 + 1.6 * fade, StrokeCap=skia.Paint.kRound_Cap))
        if x < 0.7:
            rr = 15 + 170 * (1 - math.exp(-x * 5))
            c.drawCircle(cx, cy, rr, skia.Paint(Color=col(PAL["orange"], 0.7 * (1 - x / 0.7) ** 1.5), AntiAlias=True,
                                                 Style=skia.Paint.kStroke_Style, StrokeWidth=2.5))
        if x < 0.08:
            c.drawCircle(cx, cy, 22, skia.Paint(Color=col("#FFF1C8", 1 - x / 0.08), AntiAlias=True,
                                                 MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9)))
    A = snap(s)
    return A + bloom(A, ((3, 0.8), (12, 0.6), (40, 0.35)))


def neon_crisp(c, a):
    x0, y0, x1, y1 = CARD
    if a <= 0:
        return
    text(c, "SHIPS CROSSED", CX, y0 + 150, sans(30), INK, a)
    text(c, "8 OCT 2026 · 5 IN · 3 OUT", CX, y0 + 200, mono(15), PAL["orange"], a, 1)
    text(c, "WAS ≈125 A DAY", CX, y0 + 240, sans(28), INK, 0.75 * a)
    text(c, "BEFORE 28 FEB", CX, y0 + 272, sans(28), INK, 0.45 * a)
    text(c, "WINDWARD · AL JAZEERA / AFP", x0 + 26, y1 - 22, mono(13), DIM, a, 1.2)


def neon_names(c, a):
    if a > 0:
        text(c, "IRAN", 1540, 168, mono(20), PAL["magenta"], 0.9 * a, 8)
        text(c, "OMAN · MUSANDAM", 476, 622, mono(16), PAL["green"], 0.9 * a, 2, "right")


def neon_frame(N, t):
    I = neon_levels(t, N)
    A = N.compose(I) + sparks(t)
    A = np.clip(A, 0, None)
    A = A / (1 + np.maximum(0, A.max(axis=2, keepdims=True) - 1) * 0.35)   # keep hot cores from flattening to white blocks
    return np.clip(A, 0, 1)


def frame_C(N=None):
    N = N or build_neon()
    out = grain(neon_frame(N, 5.31), 0.012, 3)

    def crisp(c):
        neon_crisp(c, 1)
        text(c, "ATTACKS 1–8 OCT", ATK[0], ATK[1], sans(30), PAL["orange"], 1.0, 1)
        text(c, "POSITIONS APPROX. · UKMTO", ATK[0], ATK[1] + 28, mono(14), PAL["orange"], 0.9, 1)
        atk_leader(c, PAL["orange"], 0.6)
        neon_names(c, 1)
        chrome(c, "C · NEON — GLASS TUBES, FLICKER-ON, HUM, SPARK ON IMPACT", "07  OCTOBER", PAL["orange"],
               "COAST: NATURAL EARTH 10M, SIMPLIFIED · LANES SCHEMATIC")
    return save(out, "C_neon.png", crisp)


# ======================================================================= D · FLUORESCENT RISO
RISO = dict(pink="#FF48B0", blue="#3D8BFF", yellow="#FFE800")


def halftone(d, angle, cell, seed, edge=0.35):
    """AM screen: round dots on a rotated grid, area proportional to density, with ragged ink edges."""
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = math.radians(angle)
    u = (xx * math.cos(a) + yy * math.sin(a)) / cell
    v = (-xx * math.sin(a) + yy * math.cos(a)) / cell
    fu, fv = u - np.floor(u) - 0.5, v - np.floor(v) - 0.5
    dist = np.sqrt(fu * fu + fv * fv) * cell
    dd = cv2.GaussianBlur(d.astype(np.float32), (0, 0), cell * 0.35)
    rad = cell * np.sqrt(np.clip(dd, 0, 1) / math.pi) * 1.08
    noise = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.8) * edge
    dot = np.clip((rad - dist + noise) / 1.1 + 0.5, 0, 1)
    dot[dd < 0.015] = 0
    return dot


def solid(mask, seed, rough=0.5):
    r = np.random.default_rng(seed)
    n = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.7) * rough
    m = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 0.6)
    return np.clip((m - 0.5 + 0.18 * n) * 3 + 0.5, 0, 1)


def ink_coverage(seed, lo=0.82, hi=1.04):
    r = np.random.default_rng(seed)
    n = cv2.GaussianBlur(r.normal(0, 1, (H // 8, W // 8)).astype(np.float32), (0, 0), 6)
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    n = cv2.resize(n, (W, H), interpolation=cv2.INTER_CUBIC)
    speck = (r.random((H, W)) > 0.012).astype(np.float32)
    return (lo + (hi - lo) * n) * speck


def shift(a, dx, dy, rot=0.0):
    M = cv2.getRotationMatrix2D((W / 2, H / 2), rot, 1.0)
    M[0, 2] += dx
    M[1, 2] += dy
    return cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)


def mask_from(draw):
    s = surface()
    c = s.getCanvas()
    draw(c)
    return alpha_of(s)


def pins_mask(c):
    for lo, la in OCT_HITS:
        c.drawCircle(*px(lo, la), 8, skia.Paint(Color=col("#FFFFFF"), AntiAlias=True))


def frame_D():
    g = geo()
    land = g.land
    dem = cv2.GaussianBlur(g.dem, (0, 0), 3)
    x0, y0, x1, y1 = CARD
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # BLUE: water, denser with depth (ETOPO); the shallow Gulf stays almost black
    depth = np.clip(-dem, 0, None)
    tdep = np.clip(np.log1p(depth / 25) / np.log1p(2600 / 25), 0, 1)
    d_blue = (1 - land) * np.clip(tdep ** 1.6 * 0.62 - 0.02, 0, 1)
    # PINK: land, denser with height (ETOPO): coastal plains sparse, the Zagros foothills dense
    elev = np.clip(dem, 0, None)
    d_pink = land * (0.04 + 0.52 * np.clip(elev / 2000, 0, 1) ** 0.8)
    arabia = ((g.country == 2) | (g.country == 3)).astype(np.float32) * land
    d_blue = np.maximum(d_blue, arabia * (0.10 + 0.5 * np.clip(elev / 1500, 0, 1) ** 0.8))     # Arabia overprints blue on pink: lavender
    d_pink = d_pink * (1 - 0.35 * arabia)
    heat = np.zeros((H, W), np.float32)
    for lo, la in OCT_HITS:
        x, y = px(lo, la)
        heat = np.maximum(heat, np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * 30 ** 2)))
    d_pink = np.maximum(d_pink, heat * 0.6)
    # YELLOW: the oil lanes, a solid core with a halftone falloff
    def lanes_mask(wd):
        return mask_from(lambda c: [c.drawPath(skpath(chaikin(PX(l), 3)), skia.Paint(Color=col("#FFFFFF"), AntiAlias=True,
                         Style=skia.Paint.kStroke_Style, StrokeWidth=wd, StrokeCap=skia.Paint.kRound_Cap)) for l in (LANE_IN, LANE_OUT)])
    d_yel = cv2.GaussianBlur(lanes_mask(30), (0, 0), 10) * 0.85
    yel_core = lanes_mask(7)
    # solids: type and marks, one plate each
    T = {}

    def put(key, c_draw):
        T[key] = mask_from(c_draw)
    put("pink", lambda c: (
        text(c, "IRAN", 1520, 170, sans(84), "#FFFFFF", 1, 8),
        text(c, "QESHM", 206, 268, sans(30), "#FFFFFF", 1, 3),
        pins_mask(c),
        text(c, "ATTACKS 1–8 OCT", ATK[0], ATK[1], sans(30), "#FFFFFF", 1, 1),
        text(c, "POSITIONS APPROX.", ATK[0], ATK[1] + 30, mono(15), "#FFFFFF", 1, 1),
        atk_leader(c, "#FFFFFF", 1.0),
        coast_stroke(c, lambda k: "#FFFFFF" if k == 1 else None, 1.5, 1.0),
    ))
    put("blue", lambda c: (
        text(c, "OMAN", 470, 812, sans(54), "#FFFFFF", 1, 6),
        text(c, "MUSANDAM", 472, 844, mono(17), "#FFFFFF", 1, 2),
        text(c, "STRAIT OF HORMUZ", 600, 395, sans(54), "#FFFFFF", 1, 0),
        text(c, "26.6N 56.4E · LANES ON THE OMANI SIDE", 602, 430, mono(17), "#FFFFFF", 1, 1),
        coast_stroke(c, lambda k: "#FFFFFF" if k != 1 else None, 1.5, 1.0),
        text(c, "WAS ≈125 A DAY", CX, y0 + 240, sans(28), "#FFFFFF", 1),
        text(c, "BEFORE 28 FEB", CX, y0 + 272, mono(17), "#FFFFFF", 1, 1),
        text(c, "WINDWARD · AL JAZEERA / AFP", x0 + 26, y1 - 22, mono(13), "#FFFFFF", 1, 1),
    ))
    put("yel", lambda c: (
        text(c, "8", x0 + 40, y0 + 262, sans(270), "#FFFFFF", 1),
        pins_mask(c),
        lane_tails(c, "#FFFFFF", 1.0, 2.2),
        text(c, "SHIPS CROSSED", CX, y0 + 150, sans(30), "#FFFFFF", 1),
        text(c, "8 OCT 2026 · 5 IN · 3 OUT", CX, y0 + 196, mono(15), "#FFFFFF", 1, 1),
    ))
    # knock-outs: every plate clears a margin around every word, so type sits on black
    words = np.maximum.reduce([T["pink"], T["blue"], T["yel"]])
    words[land > -1] = words[land > -1]
    ko = cv2.dilate((words > 0.2).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))).astype(np.float32)
    ko = cv2.GaussianBlur(ko, (0, 0), 2)
    # the card: knocked out of blue and pink, with a pink halftone shadow behind the yellow 8
    plate = np.zeros((H, W), np.float32)
    plate[y0:y1, x0:x1] = 1
    plate = cv2.GaussianBlur(plate, (0, 0), 3)
    num = mask_from(lambda c: text(c, "8", x0 + 40, y0 + 262, sans(270), "#FFFFFF", 1))
    num_shadow = shift(num, 14, 12)
    grad = np.clip((yy - (y0 + 50)) / 230.0, 0, 1)
    keep = 1 - np.maximum(ko, plate)
    d_pink = d_pink * keep + num_shadow * (0.85 - 0.55 * grad) * plate
    d_blue = d_blue * keep
    d_yel = d_yel * (1 - ko)
    P = np.maximum(halftone(d_pink, 75, 7.0, 1), solid(T["pink"], 11))
    Bl = np.maximum(halftone(d_blue, 15, 6.0, 2), solid(T["blue"], 12))
    Y = np.maximum.reduce([halftone(d_yel, 0, 8.0, 3), solid(T["yel"], 13), solid(yel_core * (1 - ko), 14)])
    P = shift(P, 3, -2) * ink_coverage(21)
    Bl = shift(Bl, -2, 1, 0.04) * ink_coverage(22)
    Y = shift(Y, 1, 3) * ink_coverage(23)
    out = np.zeros((H, W, 3), np.float32)
    for m, hx in ((Bl, RISO["blue"]), (P, RISO["pink"]), (Y, RISO["yellow"])):
        out = screen(out, m[..., None] * rgb(hx)[None, None] * 0.97)
    out = screen(out, bloom(out, ((2, 0.22), (10, 0.12), (40, 0.06))))
    r = np.random.default_rng(5)
    fib = cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 1.2)
    out = np.clip(out + (0.010 + 0.008 * fib)[..., None], 0, 1)
    marks = [(70, 120), (W - 70, 120), (70, H - 130), (W - 70, H - 130)]

    def crisp(c):
        for hx, (dx, dy) in ((RISO["blue"], (-2, 1)), (RISO["pink"], (3, -2)), (RISO["yellow"], (1, 3))):
            p = skia.Paint(Color=col(hx, 0.8), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2,
                           BlendMode=skia.BlendMode.kScreen)
            for mx, my in marks:
                c.drawCircle(mx + dx, my + dy, 9, p)
                c.drawLine(mx - 16 + dx, my + dy, mx + 16 + dx, my + dy, p)
                c.drawLine(mx + dx, my - 16 + dy, mx + dx, my + 16 + dy, p)
        chrome(c, "D · FLUORESCENT RISO — 3 INKS, HALFTONE, MISREGISTERED, ON BLACK", "06  THE WAY AROUND", RISO["pink"],
               "DOT DENSITY = REAL ETOPO 2022 DEPTH (BLUE) AND HEIGHT (PINK)")
        bx, by = W - 120 - 6 * 50, H - 116
        sw = [("P", RISO["pink"]), ("B", RISO["blue"]), ("Y", RISO["yellow"]), ("P+B", "#C9A6FF"), ("P+Y", "#FFC6B0"), ("B+Y", "#E8F6FF")]
        for k, (lab, hx) in enumerate(sw):
            c.drawRect(skia.Rect.MakeXYWH(bx + k * 50, by, 46, 12), skia.Paint(Color=col(hx, 0.95)))
            text(c, lab, bx + k * 50 + 23, by + 32, mono(14), INK, 0.85, 0.5, "center")
    return save(out, "D_riso.png", crisp)


# ======================================================================= E · PARTICLE FLOW
FLOW_STOPS = [(0.0, "#2B3BFF"), (0.18, "#7A4BFF"), (0.38, "#FF2BD6"), (0.6, "#FF6A1A"), (0.8, "#E6FF2E"), (1.0, "#FFFDF0")]
OIL_STOPS = [(0.0, "#3A2A00"), (0.35, "#B8A000"), (0.7, "#E6FF2E"), (1.0, "#FFFFF2")]


def ramp(v, stops=FLOW_STOPS):
    for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
        if v <= t1:
            return mix(c0, c1, (v - t0) / max(1e-6, t1 - t0))
    return stops[-1][1]


def flow_col(v):
    return ramp(v)


def lut(stops, n=256):
    return np.array([rgb(ramp(k / (n - 1), stops)) for k in range(n)], np.float32)


def flow_routes():
    """Outbound: feeders from the Gulf join a trunk through the outbound lane and leave for the Arabian Sea. Inbound:
    a thin cool return up the inbound lane. Trunk ~20 million b/d (EIA 2024 average); the feeder split is illustrative.
    Every path is checked clear of Natural Earth land."""
    trunk = [(56.05, 26.355)] + LANE_OUT + [(56.70, 25.95), (56.86, 25.75), (57.0, 25.55)]
    feeders = [([(55.20, 26.28), (55.55, 26.30), (55.85, 26.33)], 8.5),
               ([(55.20, 26.05), (55.55, 26.10), (55.85, 26.24)], 6.0),
               ([(55.20, 26.44), (55.50, 26.44), (55.80, 26.40)], 4.5)]
    inbound = [(57.05, 25.55), (56.92, 25.75), (56.76, 25.98)] + LANE_IN[::-1] + [(55.85, 26.47), (55.55, 26.49), (55.20, 26.48)]
    out = []
    for fp, v in feeders:
        p, s = resample(chaikin(PX(fp + trunk), 3), 2.0)
        jx = np.argmin(np.hypot(*(p - PX(trunk[:1])[0]).T))
        out.append(dict(p=p, s=s, n=normals(p), v=v, join=s[jx]))
    p, s = resample(chaikin(PX(inbound), 3), 2.0)
    out.append(dict(p=p, s=s, n=normals(p), v=1.6, join=1e9, inbound=True))
    return out


NARROW = px(56.43, 26.555)


def flow_density(t, routes, n_scale=1.0):
    """Particles advected along the routes; their trails splatted into a density field (one for each direction)."""
    acc = np.zeros((H + 2, W + 2), np.float32)
    acc_in = np.zeros_like(acc)
    heads = np.zeros_like(acc)
    nx, ny = NARROW
    for k, R in enumerate(routes):
        r = np.random.default_rng(100 + k)
        L = R["s"][-1]
        n = int(R["v"] * 260 * n_scale) + 60
        s0 = r.uniform(0, L, n)
        spd = r.uniform(0.85, 1.15, n) * (80 if R.get("inbound") else 120)
        lat = np.clip(r.normal(0, 1, n), -2.6, 2.6)
        trail = r.uniform(12, 30, n)
        pos = (s0 + spd * t) % L
        fade = np.clip(np.minimum(pos, L - pos) / 80, 0, 1)
        for q in range(10):
            sv = np.clip(pos - trail * q / 9, 0, L)
            x = np.interp(sv, R["s"], R["p"][:, 0])
            y = np.interp(sv, R["s"], R["p"][:, 1])
            ax = np.interp(sv, R["s"], R["n"][:, 0])
            ay = np.interp(sv, R["s"], R["n"][:, 1])
            dn = np.hypot(x - nx, y - ny)
            squeeze = 1 - 0.5 * np.exp(-(dn / 190) ** 2)
            joined = sv > R["join"]
            wd = (2.6 if R.get("inbound") else np.where(joined, 8.0, 1.6 + 0.9 * math.sqrt(R["v"]))) * squeeze
            xx, yy = x + ax * lat * wd, y + ay * lat * wd
            wgt = fade * (1 - q / 10) ** 1.3
            ok = (xx >= 0) & (xx < W) & (yy >= 0) & (yy < H)
            np.add.at(acc_in if R.get("inbound") else acc, (yy[ok].astype(int) + 1, xx[ok].astype(int) + 1), wgt[ok])
            if q == 0:
                sel = ok & (r.random(n) < 0.35)                      # a third of the particles show a hot head
                np.add.at(heads, (yy[sel].astype(int) + 1, xx[sel].astype(int) + 1), fade[sel])
    flow_density.heads = cv2.GaussianBlur(heads[1:-1, 1:-1], (0, 0), 0.7)
    return cv2.GaussianBlur(acc[1:-1, 1:-1], (0, 0), 0.9), cv2.GaussianBlur(acc_in[1:-1, 1:-1], (0, 0), 0.9)


FLOW_V0 = 0.82


def flow_rgb(D, Din, stops=FLOW_STOPS, in_hex="#4B7BFF"):
    V = cv2.GaussianBlur(D, (0, 0), 7)                       # volume: how much shares this water -> colour
    vc = np.clip(V / FLOW_V0, 0, 1)
    br = np.clip(1 - np.exp(-D / 0.45), 0, 1) * (0.55 + 0.45 * vc)   # the particles themselves -> light
    L = lut(stops)
    c = L[np.clip((vc * 255).astype(int), 0, 255)] * br[..., None]
    vi = 1 - np.exp(-Din / 0.8)
    c = c + vi[..., None] * rgb(in_hex)[None, None] * 0.9
    return c


def flow_frame(t, routes, base, n_scale=1.0, stops=FLOW_STOPS, in_hex="#4B7BFF"):
    D, Din = flow_density(t, routes, n_scale)
    P = flow_rgb(D, Din, stops, in_hex)
    G = bloom(P, ((2, 0.5), (7, 0.45), (22, 0.32), (70, 0.18)))
    hd = np.clip(flow_density.heads * 2.2, 0, 1)[..., None]
    P = P * (1 - 0.35 * hd) + hd * (0.55 * P / np.maximum(1e-3, P.max(axis=2, keepdims=True)) + 0.45)   # pale hot heads
    return np.clip(screen(base, P + G), 0, 1)


def flow_base():
    s = surface()
    c = s.getCanvas()
    land_fill(c, lambda k: "#FFFFFF", 0.035)
    draw_glyphs(c, lambda k: "#C9D2D8", 0.55, 0.20, 0.09)
    coast_stroke(c, lambda k: "#C9D2D8", 1.2, 0.55)
    return snap(s)


def fit(s, f_fn, size, maxw, track=0.0):
    while tw(s, f_fn(size), track) > maxw and size > 8:
        size -= 2
    return f_fn(size)


def flow_crisp(c):
    x0, y0, x1, y1 = CARD
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.Paint(Color=col("#000000", 0.86)))
    corner_frame(c, CARD, PAL["yellow"], 0.9)
    text(c, "US EIA · 2024 AVERAGE", x0 + 26, y0 + 34, mono(14), PAL["yellow"], 0.95, 1.2)
    f = fit("≈20M", sans, 220, x1 - x0 - 52)
    text(c, "≈20M", x0 + 24, y0 + 222, f, PAL["yellow"])
    text(c, "BARRELS OF OIL A DAY", x0 + 26, y0 + 268, sans(30), INK)
    text(c, "THROUGH THE STRAIT", x0 + 26, y0 + 300, sans(30), INK, 0.55)
    text(c, "FLOW PATHS SCHEMATIC", x1 - 22, y0 + 34, mono(13), DIM, 1.0, 1.2, "right")
    # legend
    lx, ly, lw = 44, H - 116, 420
    c.drawRect(skia.Rect.MakeXYWH(lx - 14, ly - 34, lw + 28, 76), skia.Paint(Color=col("#000000", 0.7)))
    for k in range(lw):
        c.drawRect(skia.Rect.MakeXYWH(lx + k, ly, 1.2, 8), skia.Paint(Color=col(flow_col(k / (lw - 1)))))
    text(c, "QUIET", lx, ly + 28, mono(13), DIM, 1.0, 1)
    text(c, "CROWDED", lx + lw, ly + 28, mono(13), DIM, 1.0, 1, "right")
    text(c, "COLOUR = HOW MUCH OIL SHARES THE WATER · FEEDER SPLIT ILLUSTRATIVE", lx, ly - 14, mono(12), INK, 0.85, 0.8)
    text(c, "THE PINCH", NARROW[0] + 70, NARROW[1] - 118, sans(34), INK, 1.0)
    text(c, "ALL OUTBOUND OIL IN ONE LANE, 2 NAUTICAL MILES WIDE", NARROW[0] + 70, NARROW[1] - 90, mono(15), PAL["yellow"], 1.0, 1)
    c.drawLine(NARROW[0] + 64, NARROW[1] - 112, NARROW[0] + 22, NARROW[1] - 2, skia.Paint(Color=col(INK, 0.6), AntiAlias=True, StrokeWidth=1.3))
    text(c, "INBOUND · IN BALLAST", 40, px(0, 26.48)[1] - 12, mono(14), "#7F9CFF", 1.0, 1)
    text(c, "↓ TO THE ARABIAN SEA", *px(57.02, 25.86), mono(14), PAL["yellow"], 0.95, 1)
    text(c, "IRAN", 1540, 168, light(56), INK, 0.8, 8)
    halo(c, "OMAN", 470, 812, light(40), INK, 0.9, 6)
    chrome(c, "E · THERMAL FLOW — PARTICLES ALONG THE ROUTES, HOT WHERE THEY CROWD", "03  WHAT FLOWS", PAL["yellow"],
           "COAST: NATURAL EARTH 10M · LANES SCHEMATIC")


def frame_E():
    routes = flow_routes()
    out = grain(flow_frame(3.0, routes, flow_base()), 0.01, 4)
    return save(out, "E_flow.png", flow_crisp)


# ======================================================================= F · THE SYSTEM
ATKF = (96, 884)


def frame_F():
    g = geo()
    hero = PAL["orange"]
    # 1 terrain: contours, quiet
    s = surface()
    c = s.getCanvas()
    topo_layer(c, alpha=0.26, wscale=0.9, labels=False, mono_hex="#9FB4BF")   # terrain is texture, not colour
    T = snap(s)
    # 2 the typographic coast in the country inks, held back so the hero can lead
    s = surface()
    c = s.getCanvas()
    draw_glyphs(c, cty_hex, 0.75, 0.30, 0.12)
    border_dash(c, 0.45)
    coast_stroke(c, cty_hex, 1.4, 0.6)
    words = []
    words.append(hl_label(c, "IRAN", 1540, 168, 56, PAL["magenta"], seed=5, track=6))
    words.append(hl_label(c, "OMAN", 476, 812, 42, PAL["green"], seed=7, track=5))
    words.append(hl_label(c, "STRAIT OF HORMUZ", 600, 395, 46, PAL["cyan"], seed=3))
    M = snap(s)
    # 3 flows: oil particles, yellow-hot (one frame of E)
    routes = flow_routes()
    FL = flow_frame(3.0, routes, np.zeros((H, W, 3), np.float32), n_scale=0.8, stops=OIL_STOPS, in_hex="#9C8C1C")
    # 4 events: the attack pins in neon, mid-strike
    N = Neon()
    for k, (lo, la) in enumerate(OCT_HITS):
        x_, y_ = px(lo, la)
        ring = skia.Path()
        ring.addCircle(x_, y_, 15)
        dot = skia.Path()
        dot.addCircle(x_, y_, 3.0)
        N.add(f"pin{k}", [ring, dot], hero, 4.0, 1.3)
    s_, x, y, size = ("ATTACKS 1–8 OCT", ATKF[0], ATKF[1], 34)
    for k, p in enumerate(glyph_outline(s_, x, y, light(size), 2)):
        if p is not None:
            N.add(f"a{k}", [p], hero, 1.8, 0.8)
    E = N.compose({**{f"pin{k}": 1.6 for k in range(3)}, **{f"a{k}": 1.0 for k in range(20)}}) - N.glass + sparks(5.42) * 0.7
    base = screen(screen(T, M), FL)
    out = screen(base, bloom(M * 0.6, ((3, 0.5), (12, 0.3), (36, 0.15))))
    out = np.clip(out + E, 0, 1)
    # 5 data card: halftone (the riso dot, one ink: oil yellow)
    x0, y0, x1, y1 = CARD
    plate = np.zeros((H, W), np.float32)
    plate[y0:y1, x0:x1] = 1
    out = out * (1 - 0.9 * cv2.GaussianBlur(plate, (0, 0), 4)[..., None])
    num = mask_from(lambda c: text(c, "8", x0 + 40, y0 + 262, sans(270), "#FFFFFF", 1))
    grad = np.clip((np.mgrid[0:H, 0:W][0] - (y0 + 40)) / 260.0, 0, 1).astype(np.float32)
    dots = halftone(num * (0.95 - 0.55 * grad), 45, 7.0, 7, 0.25) * num.clip(0, 1)
    dots = np.maximum(dots, shift(num, 0, 0) * 0)
    vio = rgb("#B48CFF")[None, None]
    out = screen(out, dots[..., None] * vio)
    out = screen(out, bloom(dots[..., None] * vio, ((3, 0.5), (14, 0.3), (40, 0.12))))
    out = grain(vignette(out), 0.012, 9)

    def crisp(c):
        for item in words:
            ink_word(c, item)
        text(c, "26.6N 56.4E · LANES ON THE OMANI SIDE", 600, 430, mono(16), PAL["cyan"], 0.95, 1.2)
        text(c, "POSITIONS APPROX. · UKMTO", ATKF[0], ATKF[1] + 30, mono(14), hero, 1.0, 1)
        ax, ay = px(*OCT_HITS[1])
        c.drawLine(ATKF[0] + 290, ATKF[1] - 14, ax - 16, ay + 8, skia.Paint(Color=col(hero, 0.8), AntiAlias=True, StrokeWidth=1.4))
        lane_tails(c, PAL["yellow"], 0.0)
        corner_frame(c, CARD, PAL["violet"], 0.95)
        text(c, "DATA · 8 OCT 2026", x0 + 26, y0 + 34, mono(14), PAL["violet"], 0.95, 1.2)
        text(c, "SHIPS CROSSED", CX, y0 + 150, sans(30), INK, 1.0)
        text(c, "8 OCT 2026 · 5 IN · 3 OUT", CX, y0 + 186, mono(15), PAL["violet"], 1.0, 1)
        text(c, "WAS ≈125 A DAY", CX, y0 + 238, sans(30), INK, 0.6)
        text(c, "BEFORE 28 FEB", CX, y0 + 272, sans(30), INK, 0.35)
        text(c, "WINDWARD · AL JAZEERA / AFP", x0 + 26, y1 - 22, mono(13), PAL["violet"], 0.9, 1.2)
        # the key: texture = meaning
        ky = H - 92
        c.drawRect(skia.Rect.MakeXYWH(30, ky - 30, 760, 56), skia.Paint(Color=col("#000000", 0.75)))
        items = [("TERRAIN", "CONTOURS", "#9FB4BF"), ("PLACES", "HIGHLIGHTER", PAL["magenta"]), ("FLOWS", "PARTICLES", PAL["yellow"]),
                 ("EVENTS", "NEON", hero), ("DATA", "HALFTONE", PAL["violet"])]
        kx = 44
        for a, b, hx in items:
            c.drawRect(skia.Rect.MakeXYWH(kx, ky - 11, 22, 4), skia.Paint(Color=col(hx)))
            text(c, a, kx + 32, ky - 4, mono(13), INK, 0.95, 1.2)
            text(c, b, kx + 32, ky + 14, mono(12), DIM, 1.0, 1.2)
            kx += 150
        chrome(c, "F · THE SYSTEM — BLACK BASE · HIGHLIGHTER INKS · TEXTURE BY MEANING · HERO COLOUR: ORANGE", "07  OCTOBER", hero,
               "COAST: NATURAL EARTH 10M · RELIEF: ETOPO 2022 · LANES SCHEMATIC")
    return save(out, "F_system.png", crisp)


# ======================================================================= video
def encode(frames_fn, n, out, fps=30, audio=None):
    path = os.path.join(HERE, out)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    if audio:
        cmd += ["-i", audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "medium", "-movflags", "+faststart", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        pr.stdin.write(np.ascontiguousarray(frames_fn(k)).tobytes())
        if k % 30 == 0:
            print(out, k, "/", n, flush=True)
    pr.stdin.close()
    pr.wait()
    print("wrote", out)


def render_crisp(a, crisp):
    s = surface()
    c = s.getCanvas()
    c.drawImage(to_image(a), 0, 0)
    if crisp:
        crisp(c)
    return s.makeImageSnapshot().toarray()[..., :3]


def neon_audio(T, path, sr=48000):
    """Mains hum that swells as tubes strike, crackle on each strike, a crack and fizz on each impact."""
    import wave
    t = np.arange(int(T * sr)) / sr
    lvl = np.array([sum(neon_levels(x, None).values()) for x in np.arange(0, T, 1 / 30)])
    lvl = np.interp(t, np.arange(len(lvl)) / 30, lvl / max(1e-6, lvl.max()))
    humw = (np.sin(2 * np.pi * 100 * t) * 0.5 + np.sin(2 * np.pi * 200 * t) * 0.25 + np.sin(2 * np.pi * 300 * t) * 0.12) * 0.16 * lvl
    r = np.random.default_rng(3)
    noise = r.normal(0, 1, len(t))
    dl = np.abs(np.diff(lvl, prepend=0)) * 400
    crack = noise * np.clip(dl, 0, 1) * 0.35
    imp = np.zeros_like(t)
    for ts, g in ((4.6, 1.0), (4.95, 0.6), (5.2, 0.6)):
        x = t - ts
        m = x >= 0
        imp[m] += g * (noise[m] * np.exp(-x[m] * 9) * 0.6 + np.sin(2 * np.pi * 55 * x[m]) * np.exp(-x[m] * 5) * 0.5)
    y = np.tanh((humw + crack + imp) * 1.2) * 0.8
    st = np.c_[y, np.roll(y, 37)]
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def video_C():
    N = build_neon()
    T, fps = 7.0, 30
    wav = os.path.join(HERE, "data", "neon_hum.wav")
    neon_audio(T, wav)

    def fr(k):
        t = k / fps
        a = grain(neon_frame(N, t), 0.012, 3 + k)

        def crisp(c):
            ca = max(0.0, min(1.0, (t - 3.6) / 0.4))
            neon_crisp(c, ca * (0.85 + 0.15 * min(1, neon_levels(t, N)["num"])))
            if t > 4.7:
                aa = min(1, (t - 4.7) / 0.3)
                text(c, "ATTACKS 1–8 OCT", ATK[0], ATK[1], sans(30), PAL["orange"], aa, 1)
                text(c, "POSITIONS APPROX. · UKMTO", ATK[0], ATK[1] + 28, mono(14), PAL["orange"], 0.9 * aa, 1)
                atk_leader(c, PAL["orange"], 0.6 * aa)
            neon_names(c, max(0.0, min(1.0, (t - 1.0) / 0.5)))
            chrome(c, "C · NEON", "07  OCTOBER", PAL["orange"], "COAST: NATURAL EARTH 10M, SIMPLIFIED · LANES SCHEMATIC")
        return render_crisp(a, crisp)
    encode(fr, int(T * fps), "C_neon.mp4", fps, wav)


def video_E():
    routes = flow_routes()
    base = flow_base()
    T, fps = 7.0, 30

    def fr(k):
        t = k / fps
        a = grain(flow_frame(t + 3.0, routes, base), 0.01, 4 + k)
        return render_crisp(a, flow_crisp)
    encode(fr, int(T * fps), "E_flow.mp4", fps)


# ======================================================================= sheet
TILES = [("A_highlighter.png", "A · HIGHLIGHTER (BRIEF)"), ("B_topographic.png", "B · TOPOGRAPHIC · REAL ETOPO 2022"),
         ("C_neon.png", "C · NEON · EVENTS"), ("D_riso.png", "D · FLUORO RISO · MY PICK 1"),
         ("E_flow.png", "E · THERMAL FLOW · MY PICK 2"), ("F_system.png", "F · THE SYSTEM · RECOMMENDED")]


def sheet():
    tw_, th_ = 960, 540
    m, lab = 24, 40
    S = np.full((m + 3 * (th_ + lab + m), m + 2 * (tw_ + m), 3), 10, np.uint8)
    s = skia.Surface.MakeRaster(skia.ImageInfo.Make(S.shape[1], S.shape[0], skia.kRGBA_8888_ColorType, skia.kPremul_AlphaType))
    c = s.getCanvas()
    c.clear(col("#0A0A0A"))
    for k, (fn, label) in enumerate(TILES):
        im = cv2.imread(os.path.join(HERE, fn))
        if im is None:
            continue
        im = cv2.cvtColor(cv2.resize(im, (tw_, th_), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)
        x = m + (k % 2) * (tw_ + m)
        y = m + (k // 2) * (th_ + lab + m)
        rgba = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
        c.drawImage(skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType), x, y + lab)
        text(c, label, x, y + 26, mono(17), INK, 0.9, 1.4)
    out = s.makeImageSnapshot().toarray()[..., :3]
    cv2.imwrite(os.path.join(HERE, "sheet.jpg"), cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print("wrote sheet.jpg")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "video":
        for k in args[1:] or ["C", "E"]:
            {"C": video_C, "E": video_E}[k]()
    elif args and args[0] == "sheet":
        sheet()
    else:
        for k in args or list("ABCDEF"):
            globals()[f"frame_{k}"]()
        sheet()
