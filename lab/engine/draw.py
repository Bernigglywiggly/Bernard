"""Line-art primitives for the ASCII look (from EP03's cold open and body, freed from its timeline). Everything is
drawn as bright lines on black; the look turns it into characters. Shapes are polylines in screen space (1920x1080)
so any shape can form from a seed point, morph into any other, fill with chrome, and read as a clear outline.

  timing   win, layer
  shapes   P, ellipse, rect, bezier, segs, glyphs, big (cached numerals)
  motion   formation (edges light up from a seed), morph_flow (segments sweep across), draw_segs, points
  fills    chrome_fill (numbers), closed_fill (solid shapes that read dense in characters)
  things   bignum (a number that forms, fills and glints), bigmac, mac_icon, mini_mac, coin, chip, figure
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine import tl  # noqa: E402

W, H = tl.W, tl.H
CX, CY = W / 2, 500
TURQ, GLOW, WHITE, MID, SOFT = mg.TURQ, mg.TURQ_GLOW, mg.ON_DARK, mg.ON_DARK_MID, mg.ON_DARK_SOFT
GOLD = "#F2D9A0"
DIM = "#0B0C0E"
ease, seg, clamp, lerp = mg.ease, mg.seg, mg.clamp, mg.lerp
N = 720                                              # segments every shape is resampled to, so all shapes can morph


def win(t, a, b, fin=0.35, fout=0.4):
    """0..1: fades in over fin from a, out over fout ending at b."""
    return ease(seg(t, a, a + fin)) * (1 - ease(seg(t, b - fout, b)))


class layer:
    """Draw a group at an alpha (and nothing at all when it's invisible)."""

    def __init__(self, c, a):
        self.c, self.a = c, float(np.clip(a, 0, 1))

    def __enter__(self):
        if self.a < 0.999:
            self.c.saveLayerAlpha(None, int(255 * self.a))
        else:
            self.c.save()
        return self.a

    def __exit__(self, *e):
        self.c.restore()


# ---------------------------------------------------------------- shapes
def P(pts):
    return np.asarray(pts, float)


def ellipse(cx, cy, rx, ry, a0=0, a1=360, n=64):
    a = np.radians(np.linspace(a0, a1, n))
    return np.column_stack([cx + rx * np.cos(a), cy + ry * np.sin(a)])


def rect(x, y, w, h, r=0.0, n=4):
    return mg.rrect_pts(x, y, w, h, r, n) if r > 0 else P([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)])


def bezier(p0, p1, p2, n=40):
    u = np.linspace(0, 1, n)[:, None]
    return (1 - u) ** 2 * np.array(p0) + 2 * (1 - u) * u * np.array(p1) + u ** 2 * np.array(p2)


def xform(polys, dx=0.0, dy=0.0, s=1.0, ang=0.0, pivot=(0.0, 0.0)):
    """Move, scale and rotate polylines about a pivot."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    px, py = pivot
    out = []
    for q in polys:
        x, y = (q[:, 0] - px) * s, (q[:, 1] - py) * s
        out.append(np.column_stack([px + dx + x * ca - y * sa, py + dy + x * sa + y * ca]))
    return out


def glyphs(text, size, cx, cy, font=None):
    f = mg.font(font or mg.DISPLAY, size)
    w = f.measureText(text)
    return mg.glyph_polys(text, f, cx - w / 2, cy + size * 0.36), mg.text_path(text, f, cx - w / 2, cy + size * 0.36)


def segs(polys, n=N):
    return mg.polys_to_segments(polys, n)


_G = {}


def big(text, size, cx, cy, n=420):
    k = (text, size, cx, cy, n)
    if k not in _G:
        polys, path = glyphs(text, size, cx, cy)
        _G[k] = (segs(polys, n), path)
    return _G[k]


# ---------------------------------------------------------------- motion
def morph_flow(a, b, k, spread=0.35):
    """Segments leave in a sweep (left to right) instead of all at once, and travel on a slight arc."""
    order = np.argsort(np.argsort(a.mean(axis=1)[:, 0]))
    r = order / max(1, len(order) - 1)
    kk = np.clip((k * (1 + spread) - spread * r), 0, 1)
    kk = kk * kk * (3 - 2 * kk)
    out = a + (b - a) * kk[:, None, None]
    lift = np.sin(np.pi * kk)[:, None, None] * np.array([0, -60.0])[None, None, :]
    return out + lift, kk


def draw_segs(c, S, col=GLOW, w=1.7, a=1.0, glow=True, tips=None):
    if a <= 0 or len(S) == 0:
        return
    path = skia.Path()
    for p0, p1 in S:
        path.moveTo(*p0); path.lineTo(*p1)
    if glow:
        g = mg.stroke(col, 6, 0.22 * a)
        g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5))
        c.drawPath(path, g)
    c.drawPath(path, mg.stroke(col, w, a))
    if tips is not None:
        moving = S[(tips > 0.02) & (tips < 0.98)]
        if len(moving):
            pts = [skia.Point(float(x), float(y)) for x, y in moving[::3, 1]]
            p = mg.stroke("#FFFFFF", 4.0, 0.9 * a); p.setStrokeCap(skia.Paint.kRound_Cap)
            c.drawPoints(skia.Canvas.kPoints_PointMode, pts, p)


def formation(c, S, t, t0, dur, col=GLOW, w=1.7, seed_pt=None, a=1.0):
    """Edges light up in order of distance from a seed point, each drawing from its near end with a bright tip."""
    if t < t0:
        return None
    if t >= t0 + dur:
        draw_segs(c, S, col, w, a)
        return np.ones(len(S))
    sp = np.array(seed_pt if seed_pt is not None else S[:, 0, :].mean(axis=0) + [0, 260])
    order = np.argsort(np.linalg.norm(S.mean(axis=1) - sp, axis=1))
    n = len(S)
    ts = t0 + dur * 0.75 * np.arange(n) / n
    k = np.clip((t - ts[np.argsort(order)]) / (dur * 0.25), 0, 1)
    p0, p1 = S[:, 0, :], S[:, 1, :]
    flip = np.linalg.norm(p0 - sp, axis=1) > np.linalg.norm(p1 - sp, axis=1)
    a2, b2 = np.where(flip[:, None], p1, p0), np.where(flip[:, None], p0, p1)
    tip = a2 + (b2 - a2) * k[:, None]
    on = k > 0
    draw_segs(c, np.stack([a2[on], tip[on]], 1), col, w, a)
    live = on & (k < 1)
    if live.any():
        pts = [skia.Point(float(x), float(y)) for x, y in tip[live][::2]]
        p = mg.stroke("#FFFFFF", 4.5, 0.9 * a); p.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPoints(skia.Canvas.kPoints_PointMode, pts, p)
    return k


def lines_in(c, polys, t, t0, dur=0.7, col=GLOW, w=1.7, a=1.0, seed_pt=None, n=None):
    """Polylines that form on at t0 (from a seed point) and then stay: the everyday way a thing appears."""
    if t < t0 or a <= 0:
        return
    S = segs(polys, n or max(120, min(900, int(sum(mg.poly_len(q)[-1] for q in polys) / 6))))
    formation(c, S, t, t0, dur, col, w, seed_pt, a)


def points(c, X, a=1.0, col=GOLD, size=3.2):
    if a <= 0 or len(X) == 0:
        return
    for q in range(3):
        sel = X[q::3]
        pts = [skia.Point(float(x), float(y)) for x, y in sel]
        p = mg.stroke(col if q else "#FFFFFF", size + q * 0.6, a * (0.55 + 0.2 * q))
        p.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPoints(skia.Canvas.kPoints_PointMode, pts, p)


def sample_on(polys, n, rng):
    """n points spread along polylines, proportional to length."""
    lens = np.array([mg.poly_len(p)[-1] for p in polys])
    idx = rng.choice(len(polys), n, p=lens / lens.sum())
    out = []
    for i in idx:
        q = polys[i]
        Lq = mg.poly_len(q)
        s = rng.uniform(0, Lq[-1])
        out.append((np.interp(s, Lq, q[:, 0]), np.interp(s, Lq, q[:, 1])))
    return np.array(out)


# ---------------------------------------------------------------- fills and strokes
def chrome_fill(c, path, k, sweep=None):
    """Fill a glyph path with chrome, rising from the bottom (k 0..1)."""
    if k <= 0:
        return
    b = path.getBounds()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(b.left() - 10, lerp(b.bottom(), b.top(), k), b.right() + 10, b.bottom() + 10))
    c.drawPath(path, mg.chrome_paint(b.top(), b.bottom()))
    c.restore()
    if sweep is not None and 0 < sweep < 1:
        x = lerp(b.left() - 200, b.right() + 200, sweep)
        sh = skia.GradientShader.MakeLinear([(x - 120, 0), (x + 120, 0)], [skia.Color4f(1, 1, 1, 0), skia.Color4f(1, 1, 1, 0.55), skia.Color4f(1, 1, 1, 0)])
        p = skia.Paint(AntiAlias=True); p.setShader(sh)
        c.save(); c.clipPath(path, skia.ClipOp.kIntersect, True); c.drawRect(b, p); c.restore()


def closed_fill(c, polys, k, paint):
    """Fill closed polylines, rising from the bottom (k 0..1)."""
    if k <= 0:
        return
    path = skia.Path()
    for q in polys:
        path.addPoly([skia.Point(float(x), float(y)) for x, y in q], True)
    b = path.getBounds()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(b.left() - 10, lerp(b.bottom(), b.top(), k), b.right() + 10, b.bottom() + 10))
    c.drawPath(path, paint)
    c.restore()


def fill_rrect(c, x, y, w, h, r, paint):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), paint)


def stroke_polys(c, polys, col=GLOW, w=1.7, a=1.0, closed=False):
    if a <= 0:
        return
    path = skia.Path()
    for q in polys:
        path.addPoly([skia.Point(float(x), float(y)) for x, y in q], closed)
    g = mg.stroke(col, 6, 0.22 * a)
    g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5))
    c.drawPath(path, g)
    c.drawPath(path, mg.stroke(col, w, a))


def bignum(c, t, text, size, cx, cy, t0, col=GLOW, seed=None, fill=True):
    """A number that forms line by line, then fills with chrome and catches a glint."""
    if t < t0:
        return
    sg, path = big(text, size, cx, cy)
    kf = ease(seg(t, t0 + 0.7, t0 + 1.2)) if fill else 0.0
    if t < t0 + 0.85:
        formation(c, sg, t, t0, 0.8, col, seed_pt=seed or (cx, cy + 320))
    else:
        draw_segs(c, sg, col, 1.7, 1 - 0.8 * kf)
    if fill:
        chrome_fill(c, path, kf, sweep=seg(t, t0 + 1.0, t0 + 1.9))
    tl.ev(t0, "form", t, cx)
    if fill:
        tl.ev(t0 + 0.75, "thock", t, cx)


# ---------------------------------------------------------------- things
def bigmac(cx, cy, s):
    """A Big Mac side on, the house unit for money: (cx, cy) = the middle of the top bun's base, s = half its width.
    Returns (outlines, buns, patties, seeds)."""
    def rr(x0, y0, x1, y1, r):
        return mg.rrect_pts(cx + x0 * s, cy + y0 * s, (x1 - x0) * s, (y1 - y0) * s, r * s, 6)
    dome = np.vstack([ellipse(cx, cy, s, 0.62 * s, 180, 360, 64), ellipse(cx, cy, s, 0.07 * s, 0, 180, 32)])
    xs = np.linspace(-1.04, 1.04, 70)
    lettuce = [np.column_stack([cx + xs * s, cy + (y0 + a * np.sin(xs * f + ph)) * s]) for y0, a, f, ph in ((0.12, 0.035, 14, 0), (0.575, 0.03, 16, 1))]
    cheese = P([(cx + x * s, cy + y * s) for x, y in ((-0.97, 0.17), (0.28, 0.17), (0.4, 0.3), (0.52, 0.17), (0.97, 0.17))])
    patties = [rr(-1.0, 0.2, 1.0, 0.37, 0.08), rr(-1.0, 0.61, 1.0, 0.78, 0.08)]
    buns = [dome, rr(-0.97, 0.41, 0.97, 0.53, 0.05), rr(-0.97, 0.82, 0.97, 1.02, 0.1)]
    seeds = [ellipse(cx + x * s, cy + y * s, 0.05 * s, 0.022 * s, 0, 360, 12) for x, y in
             ((-0.62, -0.22), (-0.34, -0.42), (-0.02, -0.5), (0.3, -0.44), (0.6, -0.26), (-0.18, -0.2), (0.16, -0.18), (0.42, -0.08), (-0.46, -0.04))]
    return buns + patties + lettuce + [cheese], buns, patties, seeds


def mac_icon(c, x, y, s, a=1.0):
    """The hero Big Mac, small: chrome buns, dark patties, seeds, outlines (so it still reads in characters)."""
    if a <= 0.01:
        return
    outl, buns, patties, seeds = bigmac(x, y, s)
    with layer(c, a):
        closed_fill(c, buns, 1.0, mg.chrome_paint(y - 0.62 * s, y + 1.02 * s))
        closed_fill(c, patties, 1.0, mg.fill(MID, 0.55))
        closed_fill(c, seeds, 1.0, mg.fill(DIM, 0.9))
        stroke_polys(c, outl, WHITE, 1.3, 0.9)


def mini_mac(c, x, y, s, a=1.0):
    """A small Big Mac as solid bands (reads as a stack in characters, cheap to draw by the thousand)."""
    if a <= 0:
        return
    top = skia.Path()
    top.addArc(skia.Rect.MakeLTRB(x - s, y - 0.62 * s, x + s, y + 0.62 * s), 180, 180)
    top.close()
    c.drawPath(top, mg.fill(WHITE, 0.95 * a))
    fill_rrect(c, x - s, y + 0.14 * s, 2 * s, 0.22 * s, 0.08 * s, mg.fill(MID, 0.75 * a))
    fill_rrect(c, x - 0.96 * s, y + 0.44 * s, 1.92 * s, 0.14 * s, 0.05 * s, mg.fill(WHITE, 0.8 * a))
    fill_rrect(c, x - s, y + 0.64 * s, 2 * s, 0.22 * s, 0.08 * s, mg.fill(MID, 0.75 * a))
    fill_rrect(c, x - 0.96 * s, y + 0.92 * s, 1.92 * s, 0.24 * s, 0.1 * s, mg.fill(WHITE, 0.95 * a))


def coin(c, x, y, r, a=1.0, lit=1.0):
    c.drawCircle(x, y, r, mg.stroke(GLOW, 2.0, a))
    c.drawCircle(x, y, r * 0.8, mg.stroke(GLOW, 1.2, 0.6 * a))
    if lit > 0:
        c.drawCircle(x, y, r * 0.78, mg.chrome_paint(y - r, y + r, a * lit))
    f = mg.font(mg.DISPLAY, r * 0.9)
    c.drawString("$", x - f.measureText("$") / 2, y + r * 0.32, f, mg.fill(DIM if lit > 0.5 else GLOW, a))


def chip(cx, cy, s):
    """A chip package: the substrate, the die, the pins on every side."""
    out = [mg.rrect_pts(cx - s, cy - s, 2 * s, 2 * s, 0.08 * s, 4), mg.rrect_pts(cx - 0.5 * s, cy - 0.5 * s, s, s, 0.04 * s, 3)]
    for k in range(9):
        o = -0.8 * s + k * 0.2 * s
        out += [P([(cx + o, cy - s), (cx + o, cy - 1.18 * s)]), P([(cx + o, cy + s), (cx + o, cy + 1.18 * s)]),
                P([(cx - s, cy + o), (cx - 1.18 * s, cy + o)]), P([(cx + s, cy + o), (cx + 1.18 * s, cy + o)])]
    return out


# ---------------------------------------------------------------- figures (people and humanoid robots)
# A pose is joint angles in degrees: 0 = straight down, 90 = forward (the way the figure faces), 180 = straight up,
# -90 = backward. Arms are relative to the torso (lean), legs to the vertical; the elbow and knee values bend the
# lower limb from the upper one (a knee bends with a negative value).
STAND = dict(lean=0, head=0, ls=8, le=10, rs=-8, re=10, lh=4, lk=0, rh=-4, rk=0)
GUARD = dict(lean=8, head=6, ls=40, le=110, rs=18, re=132, lh=18, lk=-12, rh=-18, rk=-6)
PUNCH = dict(lean=16, head=8, ls=88, le=-4, rs=18, re=132, lh=22, lk=-10, rh=-24, rk=-4)
HOOK = dict(lean=12, head=6, ls=40, le=110, rs=95, re=40, lh=16, lk=-14, rh=-20, rk=-6)
HIT = dict(lean=-24, head=-20, ls=-40, le=70, rs=110, re=30, lh=26, lk=-34, rh=-22, rk=-10)
DANCE = dict(lean=-6, head=-10, ls=150, le=25, rs=-95, re=-20, lh=28, lk=-40, rh=-10, rk=0)
WAVE = dict(lean=0, head=4, ls=8, le=10, rs=160, re=-30, lh=4, lk=0, rh=-4, rk=0)
PILOT = dict(lean=4, head=2, ls=55, le=70, rs=45, re=80, lh=4, lk=0, rh=-4, rk=0)      # arms up at chest height, VR


def pose_mix(a, b, k):
    return {j: lerp(a[j], b[j], k) for j in a}


def skeleton(x, y, s, pose, face=1):
    """Joint positions of a figure: (x, y) = the hips, s = its height, face = +1 (right) or -1 (left)."""
    def d(ang, length, p):
        r = math.radians(ang)
        return (p[0] + face * length * math.sin(r), p[1] + length * math.cos(r))
    lean = math.radians(pose["lean"])
    hip = (x, y)
    neck = (x + face * 0.30 * s * math.sin(lean), y - 0.30 * s * math.cos(lean))
    head = (neck[0] + face * 0.075 * s * math.sin(lean + math.radians(pose["head"])), neck[1] - 0.075 * s * math.cos(lean + math.radians(pose["head"])))
    sh = (neck[0], neck[1] + 0.02 * s)
    j = {"hip": hip, "neck": neck, "head": head}
    for side in "lr":
        a = pose[side + "s"] + pose["lean"]
        j[side + "elb"] = d(a, 0.17 * s, sh)
        j[side + "hand"] = d(a + pose[side + "e"], 0.16 * s, j[side + "elb"])
        k = d(pose[side + "h"], 0.24 * s, hip)
        j[side + "knee"] = k
        j[side + "foot"] = d(pose[side + "h"] + pose[side + "k"], 0.24 * s, k)
    j["sh"] = sh
    return j


def figure(x, y, s, pose, face=1, robot=False, mask=False):
    """A person (or a humanoid robot) as polylines. Robots get plated limbs, a visor and joint rings; people get a
    plain head (mask: a visor band, the Tesla dancer) and slimmer limbs. (x, y) = hips, s = height. Returns (polys,
    joints); joints["closed"] are the closed shapes (head, torso, limbs) for fills."""
    j = skeleton(x, y, s, pose, face)
    out, closed = [], []
    hr = 0.062 * s
    hx, hy = j["head"]
    if robot:
        head = mg.rrect_pts(hx - hr, hy - hr * 1.15, 2 * hr, 2.1 * hr, 0.5 * hr, 5)
        out += [head, P([(hx - face * 0.1 * hr, hy - 0.2 * hr), (hx + face * 0.95 * hr, hy - 0.2 * hr)])]
    else:
        head = ellipse(hx, hy, hr, hr * 1.12, 0, 360, 40)
        out.append(head)
        if mask:
            out.append(P([(hx - face * 0.2 * hr, hy - 0.15 * hr), (hx + face * 0.98 * hr, hy - 0.15 * hr)]))
    closed.append(head)
    nk, hp = np.array(j["neck"]), np.array(j["hip"])
    ax = hp - nk
    ln = np.linalg.norm(ax) + 1e-9
    nrm = np.array([-ax[1], ax[0]]) / ln
    wt, wb = (0.1 if robot else 0.078) * s, (0.07 if robot else 0.06) * s
    torso = P([nk + nrm * wt, hp + nrm * wb, hp - nrm * wb, nk - nrm * wt, nk + nrm * wt])
    out.append(torso); closed.append(torso)
    if robot:
        out.append(P([nk + nrm * wt * 0.7 + ax * 0.25, nk - nrm * wt * 0.7 + ax * 0.25]))
        out.append(P([nk + nrm * wt * 0.55 + ax * 0.55, nk - nrm * wt * 0.55 + ax * 0.55]))
        out.append(P([j["neck"], (hx, hy + hr * 1.0)]))
    else:
        out.append(P([j["neck"], (hx, hy + hr * 1.0)]))
    width = (0.044 if robot else 0.032) * s
    for side in "lr":
        for a_, b_ in ((j["sh"], j[side + "elb"]), (j[side + "elb"], j[side + "hand"]), (j["hip"], j[side + "knee"]),
                       (j[side + "knee"], j[side + "foot"])):
            a2, b2 = np.array(a_), np.array(b_)
            v = b2 - a2
            n2 = np.array([-v[1], v[0]]) / (np.linalg.norm(v) + 1e-9) * width
            limb = P([a2 + n2, b2 + n2 * 0.8, b2 - n2 * 0.8, a2 - n2, a2 + n2])
            out.append(limb); closed.append(limb)
        if robot:
            for jn in (side + "elb", side + "knee"):
                out.append(ellipse(*j[jn], width * 1.25, width * 1.25, 0, 360, 20))
        out.append(ellipse(*j[side + "hand"], width * 1.2, width * 1.2, 0, 360, 16))
        fx_, fy_ = j[side + "foot"]
        out.append(P([(fx_ - face * 0.02 * s, fy_), (fx_ + face * 0.07 * s, fy_)]))
    j["closed"] = closed
    return out, j


# ---------------------------------------------------------------- motion and set pieces shared by episodes
def keys(t, ks):
    """Eased motion through keyframes [(time, value), ...]."""
    if t <= ks[0][0]:
        return ks[0][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t < t1:
            return lerp(v0, v1, ease(seg(t, t0, t1)))
    return ks[-1][1]


def bump(t, a, peak, b):
    """0 -> 1 -> 0: up from a to peak, down to b."""
    if t <= a or t >= b:
        return 0.0
    return ease(seg(t, a, peak)) if t < peak else 1 - ease(seg(t, peak, b))


def morph_polys(c, pa, pb, k, col=WHITE, n=720):
    """Any line art into any other: segments sweep across on a slight arc, bright tips while they travel."""
    Sa, Sb = segs(pa, n), segs(pb, n)
    Sg, kk = morph_flow(Sa, Sb, k)
    draw_segs(c, Sg, col, 1.8, 1.0, tips=kk if k < 1 else None)


def dotted_num(c, text, size, cx, cy, t, t0, a=1.0):
    """A number drawn in dashes (a what-if, not a fact)."""
    if t < t0 or a <= 0:
        return
    sg, _ = big(text, size, cx, cy, 520)
    sel = sg[::2]
    n = int(len(sel) * ease(seg(t, t0, t0 + 0.8)))
    draw_segs(c, sel[:n], GLOW, 2.2, a)
    tl.ev(t0, "form", t, cx)


def roll(c, a_txt, b_txt, size, cx, cy, t, t0, t_m, a=1.0):
    """A number that forms, then morphs into another, then fills with chrome."""
    if t < t0 or a <= 0:
        return
    with layer(c, a):
        if t < t_m:
            bignum(c, t, a_txt, size, cx, cy, t0, fill=False)
            return
        sa, _ = big(a_txt, size, cx, cy)
        sb, pb = big(b_txt, size, cx, cy)
        k = seg(t, t_m, t_m + 0.8)
        Sg, kk = morph_flow(sa, sb, k)
        kf = ease(seg(t, t_m + 0.7, t_m + 1.2))
        draw_segs(c, Sg, GLOW, 1.7, 1 - 0.8 * kf, tips=kk if k < 1 else None)
        chrome_fill(c, pb, kf, sweep=seg(t, t_m + 1.0, t_m + 1.9))
        tl.ev(t_m, "morph", t, cx)
        tl.ev(t_m + 0.75, "thock", t, cx)


def page(x, y, w, h):
    """A document: the outline, a folded corner, lines of text."""
    out = [P([(x, y), (x + 0.82 * w, y), (x + w, y + 0.18 * w), (x + w, y + h), (x, y + h), (x, y)]),
           P([(x + 0.82 * w, y), (x + 0.82 * w, y + 0.18 * w), (x + w, y + 0.18 * w)])]
    for k in range(7):
        yy = y + (0.28 + 0.1 * k) * h
        out.append(P([(x + 0.12 * w, yy), (x + (0.45 + 0.4 * ((k * 37) % 7) / 7) * w, yy)]))
    return out


def burst(c, x, y, t, t0, r=60, a=1.0, n=9):
    """An impact or a spark: short lines flying out and fading."""
    k = seg(t, t0, t0 + 0.32)
    if k <= 0 or k >= 1:
        return
    p = mg.stroke(WHITE, 2.2, a * (1 - k))
    for i in range(n):
        ang = i * 2 * math.pi / n + 0.3
        r0, r1 = r * (0.3 + 0.9 * ease(k, "o")), r * (0.6 + 1.3 * ease(k, "o"))
        c.drawLine(x + r0 * math.cos(ang), y + r0 * math.sin(ang), x + r1 * math.cos(ang), y + r1 * math.sin(ang), p)


def sun(cx, cy, r, rot=0.0, n=16):
    """The sun: a disc and rays."""
    out = [ellipse(cx, cy, r, r, 0, 360, 72)]
    for k in range(n):
        a = rot + k * 2 * math.pi / n
        r0, r1 = r * 1.25, r * (1.6 if k % 2 == 0 else 1.45)
        out.append(P([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))]))
    return out


def globe(cx, cy, r, rot=0.0, n_mer=10, lats=(-60, -30, 0, 30, 60)):
    """The Earth seen from the equator (orthographic): the rim, the visible halves of the meridians (turning with
    rot, in radians), and the parallels."""
    out = [ellipse(cx, cy, r, r, 0, 360, 120)]
    lat = np.radians(np.linspace(-90, 90, 40))
    for k in range(n_mer):
        lon = (rot + k * math.pi / n_mer * 2) % (2 * math.pi)
        if math.cos(lon) <= 0.02:
            continue
        out.append(np.column_stack([cx + r * np.cos(lat) * math.sin(lon), cy - r * np.sin(lat)]))
    for d in lats:
        f = math.sin(math.radians(d))
        w = r * math.cos(math.radians(d))
        out.append(P([(cx - w, cy - f * r), (cx + w, cy - f * r)]))
    return out


def satellite(cx, cy, s, ang=0.0):
    """A satellite: a body with a dish and two solar wings of cells."""
    out = [P([(-0.18, -0.16), (0.18, -0.16), (0.18, 0.16), (-0.18, 0.16), (-0.18, -0.16)])]
    for sgn in (-1, 1):
        x0, x1 = sgn * 0.24, sgn * 0.95
        out.append(P([(sgn * 0.18, 0.0), (x0, 0.0)]))
        out.append(P([(x0, -0.14), (x1, -0.14), (x1, 0.14), (x0, 0.14), (x0, -0.14)]))
        for k in range(1, 5):
            xx = x0 + (x1 - x0) * k / 5
            out.append(P([(xx, -0.14), (xx, 0.14)]))
        out.append(P([(x0, 0.0), (x1, 0.0)]))
    out.append(P([(0.0, -0.16), (0.0, -0.28)]))
    out.append(np.column_stack([0.12 * np.cos(np.linspace(0.2, math.pi - 0.2, 12)), -0.3 - 0.06 * np.sin(np.linspace(0.2, math.pi - 0.2, 12))]))
    ca, sa = math.cos(ang), math.sin(ang)
    return [np.column_stack([cx + s * (q[:, 0] * ca - q[:, 1] * sa), cy + s * (q[:, 0] * sa + q[:, 1] * ca)]) for q in out]
