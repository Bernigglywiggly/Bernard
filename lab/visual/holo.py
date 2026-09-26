"""holo: a small 3D line/point/ASCII renderer for the Chrome & Marl look, on top of skia.

What it adds to the hook's 2D engine (a01_v6/mograph.py, reused here for fonts, paints and type):
  * a real camera (orbit, dolly, glide, roll) with perspective and near-plane clipping
  * 3D polylines that *form* (Tron-style reveal with a bright tip), fade with depth, and get
    softer when far (a cheap depth of field)
  * one glow pass per frame (half-res blur, added back), plus a wide bloom (quarter-res)
  * 3D type: any string becomes outline polylines placed on a plane, optionally extruded
  * ASCII shading of solid surfaces (donut.c-style z-buffer into a character grid, drawn from a
    glyph atlas with numpy so 14k characters a frame stay fast)
  * a chunked, multi-process mp4 writer (BGRA raw -> x264)

Palette: graphite marl ground, soft-white line work, one turquoise accent, emerald for gains only.
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(HERE, "..", "..", "a01_v6")
sys.path.insert(0, V6)
os.environ.setdefault("A01V6_FONTS", os.path.join(V6, "fonts"))
import mograph as mg  # noqa: E402  (fonts, paints, easing, type helpers, marl)

W, H, FPS = mg.W, mg.H, mg.FPS
TURQ, GLOW, WHITE, MID, SOFT, EMERALD = mg.TURQ, mg.TURQ_GLOW, mg.ON_DARK, mg.ON_DARK_MID, mg.ON_DARK_SOFT, mg.EMERALD
ease, seg, clamp, lerp = mg.ease, mg.seg, mg.clamp, mg.lerp


def smooth(x):
    return ease(x, "io")


# ---------------------------------------------------------------- camera
def _norm(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


class Cam:
    def __init__(self, eye, target, fov=38.0, roll=0.0, up=(0, 1, 0), near=0.15):
        self.eye = np.asarray(eye, float)
        f = _norm(np.asarray(target, float) - self.eye)
        r = _norm(np.cross(f, np.asarray(up, float)))
        u = np.cross(r, f)
        if roll:
            c, s = math.cos(roll), math.sin(roll)
            r, u = r * c + u * s, -r * s + u * c
        self.R = np.stack([r, u, f])
        self.focal = (H / 2) / math.tan(math.radians(fov) / 2)
        self.near = near

    def cam(self, P):
        return (np.asarray(P, float) - self.eye) @ self.R.T

    def screen(self, Pc):
        z = np.maximum(Pc[:, 2], 1e-6)
        return np.stack([W / 2 + self.focal * Pc[:, 0] / z, H / 2 - self.focal * Pc[:, 1] / z], 1)

    def project(self, P):
        Pc = self.cam(np.atleast_2d(P))
        return self.screen(Pc), Pc[:, 2]


def orbit(target, dist, az, el, fov=38.0, roll=0.0):
    """Camera on a sphere around target (az, el in degrees)."""
    a, e = math.radians(az), math.radians(el)
    t = np.asarray(target, float)
    eye = t + dist * np.array([math.cos(e) * math.sin(a), math.sin(e), math.cos(e) * math.cos(a)])
    return Cam(eye, t, fov, roll)


# ---------------------------------------------------------------- geometry helpers
def box(cx, cy, cz, sx, sy, sz):
    """12 edges of an axis-aligned box as 6 polylines (top loop, bottom loop, 4 verticals)."""
    x0, x1, y0, y1, z0, z1 = cx - sx / 2, cx + sx / 2, cy - sy / 2, cy + sy / 2, cz - sz / 2, cz + sz / 2
    top = np.array([[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1], [x0, y1, z0]])
    bot = top.copy(); bot[:, 1] = y0
    verts = [np.array([[x, y0, z], [x, y1, z]]) for x, z in ((x0, z0), (x1, z0), (x1, z1), (x0, z1))]
    return [top, bot] + verts


def rect_xz(cx, y, cz, sx, sz):
    x0, x1, z0, z1 = cx - sx / 2, cx + sx / 2, cz - sz / 2, cz + sz / 2
    return np.array([[x0, y, z0], [x1, y, z0], [x1, y, z1], [x0, y, z1], [x0, y, z0]])


def circle(center, radius, n=96, axis="y", a0=0.0, a1=2 * math.pi):
    a = np.linspace(a0, a1, n)
    c = np.asarray(center, float)
    if axis == "y":
        return c + np.stack([radius * np.cos(a), np.zeros_like(a), radius * np.sin(a)], 1)
    if axis == "z":
        return c + np.stack([radius * np.cos(a), radius * np.sin(a), np.zeros_like(a)], 1)
    return c + np.stack([np.zeros_like(a), radius * np.cos(a), radius * np.sin(a)], 1)


def densify(P, step=0.25):
    """Resample a polyline so reveals and clipping look smooth."""
    P = np.asarray(P, float)
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    return np.array(out)


def rot_y(P, ang):
    c, s = math.cos(ang), math.sin(ang)
    R = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.asarray(P) @ R.T


def rot_x(P, ang):
    c, s = math.cos(ang), math.sin(ang)
    R = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    return np.asarray(P) @ R.T


def text3d(text, size=1.0, font=mg.DISPLAY, origin=(0, 0, 0), plane="xy", samples=6, extrude=0.0, center=True):
    """String -> 3D outline polylines. plane 'xy' stands up facing +z; 'xz' lies flat (reads from +y, top towards -z).
    With extrude > 0 the outline is doubled and joined by short edges every few vertices (a wireframe slab)."""
    fnt = mg.font(font, 100)
    polys = mg.glyph_polys(text, fnt, 0, 0, samples)
    if not polys:
        return []
    allp = np.concatenate(polys)
    x0, x1 = allp[:, 0].min(), allp[:, 0].max()
    y0, y1 = allp[:, 1].min(), allp[:, 1].max()
    sc = size / 100.0
    ox = -(x0 + x1) / 2 if center else -x0
    oy = -(y0 + y1) / 2
    out = []
    o = np.asarray(origin, float)
    for p in polys:
        u = (p[:, 0] + ox) * sc
        v = -(p[:, 1] + oy) * sc          # skia y is down
        if plane == "xy":
            P = np.stack([u, v, np.zeros_like(u)], 1)
        else:                             # flat on the ground, reading forward along -z
            P = np.stack([u, np.zeros_like(u), -v], 1)
        out.append(P + o)
        if extrude:
            d = np.array([0, 0, -extrude]) if plane == "xy" else np.array([0, extrude, 0])
            out.append(P + o + d)
            for k in range(0, len(P) - 1, 3):
                out.append(np.stack([P[k] + o, P[k] + o + d]))
    return out


# ---------------------------------------------------------------- polyline ops
def reveal(P, k):
    """The first k (0..1) of a polyline by arc length; returns (points, tip) or (None, None)."""
    if k <= 0:
        return None, None
    if k >= 1:
        return P, None
    d = np.linalg.norm(np.diff(P, axis=0), axis=1)
    c = np.concatenate([[0], np.cumsum(d)])
    L = c[-1] * k
    i = np.searchsorted(c, L) - 1
    i = max(0, min(i, len(P) - 2))
    f = (L - c[i]) / (d[i] + 1e-12)
    tip = P[i] + (P[i + 1] - P[i]) * f
    return np.vstack([P[: i + 1], tip]), tip


def clip_near(Pc, near):
    """Split a camera-space polyline into runs in front of the near plane (clipping crossing segments)."""
    z = Pc[:, 2]
    ok = z >= near
    if ok.all():
        return [Pc]
    runs, cur = [], []
    for i in range(len(Pc)):
        if ok[i]:
            if not cur and i > 0 and not ok[i - 1]:
                a, b = Pc[i - 1], Pc[i]
                f = (near - a[2]) / (b[2] - a[2])
                cur.append(a + (b - a) * f)
            cur.append(Pc[i])
        elif cur:
            a, b = Pc[i - 1], Pc[i]
            f = (near - a[2]) / (b[2] - a[2])
            cur.append(a + (b - a) * f)
            runs.append(np.array(cur))
            cur = []
    if len(cur) > 1:
        runs.append(np.array(cur))
    return [r for r in runs if len(r) > 1]


# ---------------------------------------------------------------- the frame
_BG = {}


def ground(kind="graphite"):
    if kind not in _BG:
        _BG[kind] = mg.marl(mg.DARK if kind == "graphite" else mg.SLATE, 2 if kind == "graphite" else 3, 2.4)
    return _BG[kind]


class Frame:
    """Collects 3D line work, points and anchored labels for one camera, then draws them with glow."""

    def __init__(self, cam, fade=(8.0, 60.0), dof=(0.0, 0.0)):
        self.cam = cam
        self.fade = fade
        self.dof = dof                  # (focus distance, strength): lines far from focus get a wider, softer glow
        self.batches = {}               # key -> list of screen polylines
        self.tips = []                  # bright formation tips (x, y, r, a)
        self.pts = []                   # (xy array, color, size, alpha)
        self.labels = []                # callables drawn last (screen space)

    def _alpha_depth(self, z):
        n, f = self.fade
        return float(clamp(1 - (z - n) / (f - n), 0.08, 1.0)) if f > n else 1.0

    def lines(self, polys, color=WHITE, width=1.5, alpha=1.0, glow=0.6, k=1.0, stagger=0.0, tip=True, seed=0):
        """Add polylines. k = formation progress; with stagger > 0 each polyline starts a little later."""
        if alpha <= 0.003:
            return
        rng = np.random.default_rng(seed)
        n = len(polys)
        offs = rng.uniform(0, stagger, n) if stagger else np.zeros(n)
        for P, o in zip(polys, offs):
            kk = clamp((k - o) / max(1e-6, 1 - stagger)) if stagger else k
            if kk <= 0:
                continue
            Q, tp = reveal(P, kk) if kk < 1 else (P, None)
            if Q is None:
                continue
            Pc = self.cam.cam(Q)
            for run in clip_near(Pc, self.cam.near):
                zm = float(run[:, 2].mean())
                a = alpha * self._alpha_depth(zm)
                if a < 0.01:
                    continue
                aq = round(a * 12) / 12
                blur = 0
                if self.dof[1]:
                    blur = int(min(3, abs(zm - self.dof[0]) * self.dof[1]))
                key = (color, round(width * max(0.45, min(1.3, 14.0 / max(zm, 1.0))), 1), aq, round(glow, 2), blur)
                self.batches.setdefault(key, []).append(self.cam.screen(run))
            if tp is not None and tip:
                s, z = self.cam.project(tp)
                if z[0] > self.cam.near:
                    self.tips.append((s[0, 0], s[0, 1], max(1.5, 26.0 / z[0]), alpha * self._alpha_depth(z[0])))

    def points(self, P, color=WHITE, size=2.0, alpha=1.0):
        s, z = self.cam.project(P)
        ok = z > self.cam.near
        if not ok.any():
            return
        a = np.clip(1 - (z[ok] - self.fade[0]) / (self.fade[1] - self.fade[0]), 0.08, 1) * alpha
        r = np.clip(size * 30.0 / z[ok], 0.8, size * 3.0)
        self.pts.append((s[ok], color, r, a))

    def anchor(self, P):
        s, z = self.cam.project(P)
        return (float(s[0, 0]), float(s[0, 1])) if z[0] > self.cam.near else None

    def label(self, fn):
        self.labels.append(fn)

    def draw(self, c, glow_gain=1.0, bloom_gain=0.5):
        glow_s = skia.Surface(W // 2, H // 2)
        g = glow_s.getCanvas()
        g.clear(skia.ColorTRANSPARENT)
        g.scale(0.5, 0.5)
        for (col, w, a, gl, blur), runs in sorted(self.batches.items(), key=lambda kv: kv[0][2]):
            path = skia.Path()
            for s in runs:
                path.moveTo(*s[0])
                for x, y in s[1:]:
                    path.lineTo(x, y)
            p = mg.stroke(col, w, a)
            if blur:
                p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 0.6 * blur))
            c.drawPath(path, p)
            if gl > 0:
                gp = mg.stroke(GLOW if col == TURQ else col, w * 2.2 + blur, a * gl)
                g.drawPath(path, gp)
        for xy, col, r, a in self.pts:
            for (x, y), rr, aa in zip(xy, r, a):
                c.drawCircle(x, y, rr, mg.fill(col, aa))
                if col == TURQ:
                    g.drawCircle(x, y, rr * 1.6, mg.fill(GLOW, aa * 0.7))
        for x, y, r, a in self.tips:
            g.drawCircle(x, y, r * 1.5, mg.fill(GLOW, 0.8 * a))
            c.drawCircle(x, y, r * 0.6, mg.fill("#FFFFFF", a))
        img = glow_s.makeImageSnapshot()
        paint = skia.Paint(BlendMode=skia.BlendMode.kPlus)
        paint.setImageFilter(skia.ImageFilters.Blur(3.0, 3.0))
        paint.setAlphaf(clamp(glow_gain))
        c.save(); c.scale(2, 2); c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), paint); c.restore()
        if bloom_gain > 0:
            q = skia.Surface(W // 4, H // 4)
            qc = q.getCanvas(); qc.clear(skia.ColorTRANSPARENT)
            qc.drawImageRect(img, skia.Rect.MakeWH(W // 4, H // 4), skia.SamplingOptions(skia.FilterMode.kLinear))
            bp = skia.Paint(BlendMode=skia.BlendMode.kPlus)
            bp.setImageFilter(skia.ImageFilters.Blur(7.0, 7.0))
            bp.setAlphaf(clamp(bloom_gain))
            c.save(); c.scale(4, 4); c.drawImage(q.makeImageSnapshot(), 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), bp); c.restore()
        for fn in self.labels:
            fn(c)


# ---------------------------------------------------------------- ASCII shading
RAMP = " .·:-=+*oxX#%@"


class Ascii:
    """Characters from a glyph atlas composed with numpy: cols x rows cells, 1920x1080 out."""

    def __init__(self, cols=160, rows=90, ramp=RAMP, font=mg.MONO_M):
        self.cols, self.rows, self.ramp = cols, rows, ramp
        self.cw, self.ch = W // cols, H // rows
        f = mg.font(font, self.ch * 0.95)
        atlas = np.zeros((len(ramp), self.ch, self.cw), np.float32)
        for i, chr_ in enumerate(ramp):
            s = skia.Surface(self.cw, self.ch)
            cc = s.getCanvas(); cc.clear(skia.ColorBLACK)
            p = skia.Paint(AntiAlias=True, Color=skia.ColorWHITE)
            wdt = f.measureText(chr_)
            cc.drawString(chr_, (self.cw - wdt) / 2, self.ch * 0.8, f, p)
            atlas[i] = s.makeImageSnapshot().toarray()[:, :, 1] / 255.0
        self.atlas = atlas

    def compose(self, lum, tint_lo=(18, 184, 172), tint_hi=(233, 235, 238), chars=None):
        """lum: rows x cols in 0..1 -> RGBA uint8 image (premultiplied-friendly, black where empty)."""
        n = len(self.ramp)
        idx = np.clip((lum * (n - 1)).round().astype(int), 0, n - 1) if chars is None else chars
        tiles = self.atlas[idx]                                   # rows, cols, ch, cw
        img = tiles.transpose(0, 2, 1, 3).reshape(self.rows * self.ch, self.cols * self.cw)
        lo, hi = np.array(tint_lo, np.float32), np.array(tint_hi, np.float32)
        mix = np.repeat(np.repeat(np.clip(lum, 0, 1) ** 1.6, self.ch, 0), self.cw, 1)[..., None]
        col = lo * (1 - mix) + hi * mix
        rgb = (col * img[..., None]).clip(0, 255).astype(np.uint8)
        a = (img * 255).astype(np.uint8)
        out = np.zeros((H, W, 4), np.uint8)
        out[: rgb.shape[0], : rgb.shape[1], :3] = rgb
        out[: rgb.shape[0], : rgb.shape[1], 3] = a
        return out


def zbuffer_lum(cam, P, N, light, cols, rows, amb=0.08, rim=0.35):
    """Project dense surface samples into a cell grid; keep the nearest per cell; Lambert + rim light."""
    Pc = cam.cam(P)
    ok = Pc[:, 2] > cam.near
    Pc, Nn = Pc[ok], N[ok]
    s = cam.screen(Pc)
    cx = (s[:, 0] / W * cols).astype(int)
    cy = (s[:, 1] / H * rows).astype(int)
    inb = (cx >= 0) & (cx < cols) & (cy >= 0) & (cy < rows)
    cx, cy, z, Nn, Pw = cx[inb], cy[inb], Pc[inb, 2], Nn[inb], P[ok][inb]
    L = _norm(np.asarray(light, float))
    diff = np.clip(Nn @ L, 0, 1)
    V = _norm(cam.eye - Pw)
    rimv = (1 - np.clip(np.sum(Nn * V, 1), 0, 1)) ** 2.5 * rim
    lum = np.clip(amb + 0.85 * diff + rimv, 0, 1)
    order = np.argsort(-z)                                  # far first, near overwrites
    grid = np.zeros((rows, cols), np.float32)
    grid[cy[order], cx[order]] = lum[order]
    return grid


def torus_knot(p=2, q=3, R=3.0, r=1.1, tube=0.55, nu=900, nv=48):
    u = np.linspace(0, 2 * np.pi, nu, endpoint=False)
    rr = R + r * np.cos(q * u)
    C = np.stack([rr * np.cos(p * u), r * np.sin(q * u), rr * np.sin(p * u)], 1)
    Tn = _norm(np.gradient(C, axis=0))
    up = np.array([0, 1, 0])
    Nr = _norm(np.cross(Tn, up))
    Bn = np.cross(Tn, Nr)
    v = np.linspace(0, 2 * np.pi, nv, endpoint=False)
    cv, sv = np.cos(v)[None, :, None], np.sin(v)[None, :, None]
    Nsurf = Nr[:, None, :] * cv + Bn[:, None, :] * sv
    P = C[:, None, :] + tube * Nsurf
    return P.reshape(-1, 3), Nsurf.reshape(-1, 3)


# ---------------------------------------------------------------- overlays
GRAIN = [True]          # the pilot turns this off while scenes draw, then adds grain once per frame


def grain(c, t, amt=5.0, seed=0):
    """Fine film grain as a cached noise tile, shifted every frame (keeps 1080p compression-friendly)."""
    if not GRAIN[0]:
        return
    if "grain" not in _BG:
        rng = np.random.default_rng(99)
        n = rng.normal(0, 1, (512, 512)).astype(np.float32)
        a = np.clip(np.abs(n) * amt, 0, 255).astype(np.uint8)
        v = np.where(n > 0, 255, 0).astype(np.uint8)
        rgba = np.dstack([v, v, v, a])
        _BG["grain"] = skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)
    img = _BG["grain"]
    rng = np.random.default_rng(int(t * FPS) + seed)
    ox, oy = rng.integers(0, 512, 2)
    p = skia.Paint(); p.setAlphaf(0.35)
    c.save()
    c.translate(-float(ox), -float(oy))
    for x in range(0, W + 1024, 512):
        for y in range(0, H + 1024, 512):
            c.drawImage(img, x, y, skia.SamplingOptions(), p)
    c.restore()


def vignette(c, strength=0.55):
    sh = skia.GradientShader.MakeRadial((W / 2, H / 2), W * 0.62, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, strength)], [0.55, 1.0])
    p = skia.Paint(); p.setShader(sh)
    c.drawRect(skia.Rect.MakeWH(W, H), p)


def mono(c, text, x, y, size=18, col=SOFT, a=1.0, align="left", font=mg.MONO):
    f = mg.font(font, size)
    w = f.measureText(text)
    xx = x - w if align == "right" else x - w / 2 if align == "center" else x
    c.drawString(text, xx, y, f, mg.fill(col, a))
    return w


def callout(c, anchor, dx, dy, title, sub, t, t0, col=TURQ, a=1.0):
    """HUD callout: a dot on the part, an elbow leader, a decoding title and a quiet subline."""
    if anchor is None or a <= 0.01:
        return
    x, y = anchor
    k = ease(seg(t, t0, t0 + 0.45), "o")
    if k <= 0:
        return
    ex, ey = x + dx * k, y + dy * k
    c.drawCircle(x, y, 3.2, mg.fill(col, a))
    c.drawCircle(x, y, 7.5 * k, mg.stroke(col, 1.0, a * 0.6))
    mx = x + dx * 0.35 * k
    path = skia.Path(); path.moveTo(x, y); path.lineTo(mx, ey); path.lineTo(ex, ey)
    c.drawPath(path, mg.stroke(col, 1.2, a * 0.9))
    if k >= 0.99:
        side = "left" if dx > 0 else "right"
        tx = ex + (10 if dx > 0 else -10)
        mg.decode(c, title, tx, ey - 8, mg.font(mg.MONO_M, 19), WHITE, t, t0 + 0.45, dur=0.5, seed=hash(title) % 97, align=side, a=a)
        if sub:
            mg.decode(c, sub, tx, ey + 20, mg.font(mg.MONO, 15), SOFT, t, t0 + 0.6, dur=0.5, seed=hash(sub) % 89, align=side, a=a * 0.9)


def callout_column(c, items, t, colx=(430, 1490), gap=66, top=150, bottom=H - 150):
    """Editorial HUD labels: anchors on the right half feed a right column, the rest a left column;
    labels keep their anchor's height where they can and never overlap. items: (anchor, title, sub, t0, col)."""
    sides = {1: [], -1: []}
    for it in items:
        if it[0] is None:
            continue
        sides[1 if it[0][0] > W * 0.5 else -1].append(it)
    for side, its in sides.items():
        its.sort(key=lambda it: it[0][1])
        ys, prev = [], top - gap
        for it in its:
            y = max(it[0][1], prev + gap)
            ys.append(y)
            prev = y
        over = prev - bottom
        if over > 0:
            ys = [y - over for y in ys]
        x_col = colx[1] if side == 1 else colx[0]
        for (anchor, title, sub, t0, col), y in zip(its, ys):
            k = ease(seg(t, t0, t0 + 0.5), "o")
            if k <= 0:
                continue
            ax, ay = anchor
            elbow = x_col - side * 46
            c.drawCircle(ax, ay, 3.0, mg.fill(col, 1.0))
            c.drawCircle(ax, ay, 8.0 * k, mg.stroke(col, 1.0, 0.55))
            path = skia.Path(); path.moveTo(ax, ay)
            mx, my = lerp(ax, elbow, k), lerp(ay, y, k)
            path.lineTo(mx, my)
            if k > 0.6:
                path.lineTo(lerp(elbow, x_col - side * 8, (k - 0.6) / 0.4), y)
            c.drawPath(path, mg.stroke(col, 1.1, 0.85))
            if k >= 0.99:
                align = "left" if side == 1 else "right"
                mg.decode(c, title, x_col, y + 6, mg.font(mg.MONO_M, 19), WHITE, t, t0 + 0.5, dur=0.45, seed=len(title), align=align)
                if sub:
                    mg.decode(c, sub, x_col, y + 32, mg.font(mg.MONO, 15), SOFT, t, t0 + 0.62, dur=0.45, seed=len(sub) + 3, align=align, a=0.9)


# ---------------------------------------------------------------- output
def _render_chunk(args):
    frame_fn, i0, i1, out, fps = args
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out],
                          stdin=subprocess.PIPE)
    for i in range(i0, i1):
        c.clear(skia.ColorBLACK)
        frame_fn(c, i / fps)
        ff.stdin.write(surf.makeImageSnapshot().toarray().tobytes())
    ff.stdin.close()
    ff.wait()
    return out


def render(frame_fn, dur, out, procs=4, fps=FPS):
    """Render frame_fn(canvas, t) for dur seconds to out (mp4) using procs worker processes."""
    n = int(round(dur * fps))
    bounds = np.linspace(0, n, procs + 1).astype(int)
    tmp = [f"{out}.part{k}.mp4" for k in range(procs)]
    jobs = [(frame_fn, bounds[k], bounds[k + 1], tmp[k], fps) for k in range(procs) if bounds[k + 1] > bounds[k]]
    with Pool(len(jobs)) as pool:
        pool.map(_render_chunk, jobs)
    lst = out + ".txt"
    with open(lst, "w") as f:
        for j in jobs:
            f.write(f"file '{os.path.abspath(j[3])}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    for j in jobs:
        os.remove(j[3])
    os.remove(lst)
    return out


def still(frame_fn, t, out):
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.ColorBLACK)
    frame_fn(c, t)
    surf.makeImageSnapshot().save(out, skia.kPNG)
    return out
