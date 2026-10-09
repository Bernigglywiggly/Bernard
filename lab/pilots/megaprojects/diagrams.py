"""Engineering diagrams g01-g22 for the Fehmarnbelt film, drawn in code (skia). White and greys on pure black, no text.

    python diagrams.py                 draw src/ai/g01.png ... g22.png
    python diagrams.py --sheets DIR    also write contact sheets (plain, down/up-scaled, engine-toned) into DIR
"""
import math
import os
import random
import sys

import cv2
import numpy as np
import skia

W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "src", "ai")

DK, MD, LT, WH = 0.32, 0.5, 0.68, 1.0     # seabed, mid tone, concrete, white
WATER = 0.13


def col(v):
    k = int(round(max(0.0, min(1.0, v)) * 255))
    return skia.Color(k, k, k)


def mkpath(pts, close=True):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p


def smooth(pts):
    """Closed Catmull-Rom curve through the points."""
    n = len(pts)
    p = skia.Path()
    p.moveTo(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    p.close()
    return p


class D:
    """One 1920x1080 black sheet and the few drawing verbs every picture shares."""

    def __init__(self):
        self.s = skia.Surface(W, H)
        self.c = self.s.getCanvas()
        self.c.clear(skia.ColorBLACK)
        self.post = None

    # --- paints
    def _f(self, v):
        return skia.Paint(AntiAlias=True, Color=col(v))

    def _s(self, v, sw, butt=False):
        return skia.Paint(AntiAlias=True, Color=col(v), Style=skia.Paint.kStroke_Style, StrokeWidth=sw,
                          StrokeCap=skia.Paint.kButt_Cap if butt else skia.Paint.kRound_Cap,
                          StrokeJoin=skia.Paint.kMiter_Join if butt else skia.Paint.kRound_Join)

    # --- shapes
    def path(self, p, fill=None, stroke=None, sw=10, butt=False):
        if fill is not None:
            self.c.drawPath(p, self._f(fill))
        if stroke is not None:
            self.c.drawPath(p, self._s(stroke, sw, butt))

    def poly(self, pts, fill=None, stroke=None, sw=10, close=True, butt=False):
        self.path(mkpath(pts, close), fill, stroke, sw, butt)

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=10, r=0):
        p = skia.Path()
        if r:
            p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
        else:
            p.addRect(skia.Rect.MakeXYWH(x, y, w, h))
        self.path(p, fill, stroke, sw, butt=not r)

    def line(self, x1, y1, x2, y2, v=1.0, sw=10, butt=False):
        self.c.drawLine(x1, y1, x2, y2, self._s(v, sw, butt))

    def oval(self, cx, cy, rx, ry, fill=None, stroke=None, sw=10):
        p = skia.Path()
        p.addOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry))
        self.path(p, fill, stroke, sw)

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=10):
        self.oval(cx, cy, r, r, fill, stroke, sw)

    def curve(self, pts, v=1.0, sw=10):
        """Open quadratic through three points (start, control, end)."""
        p = skia.Path()
        p.moveTo(*pts[0])
        p.quadTo(pts[1][0], pts[1][1], pts[2][0], pts[2][1])
        self.path(p, None, v, sw)

    def arrow(self, x1, y1, x2, y2, v=1.0, sw=16, head=46):
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - math.cos(a) * head * 0.9, y2 - math.sin(a) * head * 0.9
        self.line(x1, y1, bx, by, v, sw, butt=True)
        nx, ny = -math.sin(a), math.cos(a)
        self.poly([(x2, y2), (x2 - math.cos(a) * head + nx * head * 0.62, y2 - math.sin(a) * head + ny * head * 0.62),
                   (x2 - math.cos(a) * head - nx * head * 0.62, y2 - math.sin(a) * head - ny * head * 0.62)], fill=v)

    def bigarrow(self, x1, x2, y, v=1.0, t=44, head=92):
        """A fat block arrow along x (pressure)."""
        sgn = 1 if x2 > x1 else -1
        hx = x2 - sgn * head
        self.poly([(x1, y - t / 2), (hx, y - t / 2), (hx, y - t * 1.25), (x2, y), (hx, y + t * 1.25), (hx, y + t / 2), (x1, y + t / 2)], fill=v)

    # --- textures
    def clip(self, p):
        self.c.save()
        self.c.clipPath(p, skia.ClipOp.kIntersect, True)

    def unclip(self):
        self.c.restore()

    def hatch(self, p, v=0.5, sw=6, gap=30, ang=45):
        self.clip(p)
        t = math.tan(math.radians(ang))
        for k in range(int(-H * 2), W + H * 2, gap):
            self.line(k, H, k + H / t, 0, v, sw, butt=True)
        self.unclip()

    def dots(self, p, v=0.9, r=6, gap=22, seed=1):
        rnd = random.Random(seed)
        self.clip(p)
        b = p.getBounds()
        y = b.top()
        row = 0
        while y < b.bottom() + gap:
            x = b.left() + (gap / 2 if row % 2 else 0)
            while x < b.right() + gap:
                self.circle(x + rnd.uniform(-3, 3), y + rnd.uniform(-3, 3), r * rnd.uniform(0.7, 1.1), fill=v)
                x += gap
            y += gap * 0.8
            row += 1
        self.unclip()

    def waterline(self, x0, x1, y, v=0.85, sw=9, amp=7, wl=110, skip=()):
        """A gently waved surface line; skip = [(xa, xb)] spans left blank (where a hull sits)."""
        spans, a = [], x0
        for sa, sb in sorted(skip):
            spans.append((a, sa))
            a = sb
        spans.append((a, x1))
        for a, b in spans:
            if b - a < 12:
                continue
            p = skia.Path()
            x = a
            p.moveTo(x, y + amp * math.sin(2 * math.pi * x / wl))
            while x < b:
                x = min(b, x + 8)
                p.lineTo(x, y + amp * math.sin(2 * math.pi * x / wl))
            self.path(p, None, v, sw)

    def wavedashes(self, x0, y0, x1, y1, n, seed=1, v=0.34, sw=7, ln=54, dx=1.0, dy=0.0, avoid=()):
        rnd = random.Random(seed)
        placed = []
        tries = 0
        while len(placed) < n and tries < n * 40:
            tries += 1
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if any(a <= x <= c and b <= y <= e for a, b, c, e in avoid):
                continue
            if any(abs(x - px) < ln * 1.7 and abs(y - py) < 34 for px, py in placed):
                continue
            placed.append((x, y))
            l = ln * rnd.uniform(0.7, 1.2)
            self.line(x - dx * l / 2, y - dy * l / 2, x + dx * l / 2, y + dy * l / 2, v, sw)

    def water(self, x0, x1, y0, y1, v=WATER):
        self.rect(x0, y0, x1 - x0, y1 - y0, fill=v)

    def seabed(self, top, bottom=960, x0=134, x1=1786, fill=DK, hv=0.5, edge=0.9, sw=9):
        """top = the profile left to right; filled down to `bottom`, hatched, with a bright upper edge."""
        p = mkpath(list(top) + [(x1, bottom), (x0, bottom)])
        self.path(p, fill=fill)
        self.hatch(p, hv, 6, 34, 50)
        self.poly(top, stroke=edge, sw=sw, close=False)

    def array(self):
        a = self.s.makeImageSnapshot().toarray()[:, :, 1].astype(np.float32) / 255.0
        if self.post:
            a = self.post(a)
        return (np.clip(a, 0, 1) * 255).astype(np.uint8)


# ------------------------------------------------------------------ shared subjects

TUBES = (("road", 10.8), ("road", 10.8), ("svc", 2.6), ("rail", 6.35), ("rail", 6.35))   # metres, wall 0.85 m between, total 42


def element_face(d, x, y, w, h, fill=LT, edge=WH, sw=9, inner=0.0):
    """Tunnel element end-on: wide flat box, two road tubes, a narrow service tube, two rail tubes. Returns the tube rects."""
    d.rect(x, y, w, h, fill=fill, stroke=edge, sw=sw)
    u = w / 42.0
    wall = 0.85 * u
    ty, th = y + h * 0.115, h * 0.76
    out, cx = [], x + wall
    for kind, m in TUBES:
        tw = m * u
        d.rect(cx, ty, tw, th, fill=inner, stroke=edge, sw=max(4, sw * 0.6))
        out.append((kind, cx, ty, tw, th))
        cx += tw + wall
    return out


def car_front(d, cx, base, w):
    h = w * 0.36
    d.poly([(cx - w * 0.36, base - h), (cx - w * 0.27, base - h * 1.95), (cx + w * 0.27, base - h * 1.95), (cx + w * 0.36, base - h)], fill=0.62)
    d.rect(cx - w * 0.42, base - h * 0.2, w * 0.2, h * 0.2 + 2, fill=0.45)
    d.rect(cx + w * 0.22, base - h * 0.2, w * 0.2, h * 0.2 + 2, fill=0.45)
    d.rect(cx - w / 2, base - h * 1.05, w, h * 0.9, fill=0.95, r=w * 0.08)
    d.circle(cx - w * 0.33, base - h * 0.62, w * 0.075, fill=0.0)
    d.circle(cx + w * 0.33, base - h * 0.62, w * 0.075, fill=0.0)


def train_front(d, cx, base, w, h):
    d.rect(cx - w * 0.36, base - 10, w * 0.14, 10, fill=0.6)
    d.rect(cx + w * 0.22, base - 10, w * 0.14, 10, fill=0.6)
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, base - h - 8, w, h), w * 0.24, w * 0.24))
    d.path(p, fill=0.95)
    d.rect(cx - w * 0.36, base - h * 0.86, w * 0.72, h * 0.34, fill=0.0, r=w * 0.1)
    d.circle(cx - w * 0.28, base - h * 0.2, w * 0.08, fill=0.0)
    d.circle(cx + w * 0.28, base - h * 0.2, w * 0.08, fill=0.0)


# ------------------------------------------------------------------ pictures

def g01(d):
    """Element afloat between two pontoons, five tugs leading; seen from above at an angle."""
    s = 4.3
    ox, oy = 330, 700
    ex, ey = (0.93 * s, -0.30 * s), (0.40 * s, 0.46 * s)

    def P(x, y, z=0):
        return (ox + x * ex[0] + y * ey[0], oy + x * ex[1] + y * ey[1] - z * s)

    def box(x0, x1, y0, y1, z0, z1, top=0.8, side=0.42, end=0.58, sw=7):
        d.poly([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], fill=side, stroke=WH, sw=sw)
        d.poly([P(x0, y0, z0), P(x0, y1, z0), P(x0, y1, z1), P(x0, y0, z1)], fill=end, stroke=WH, sw=sw)
        d.poly([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], fill=top, stroke=WH, sw=sw)

    d.wavedashes(170, 200, 1750, 930, 46, seed=4, v=0.3, sw=7, ln=60, dx=0.95, dy=-0.31)
    tugs = [(304, 21), (290, -10), (290, 52), (268, -36), (268, 78)]
    for tx, ty in tugs:                                              # tow lines first, under everything
        a, b = P(217, 21 + (ty - 21) * 0.25, 3), P(tx - 14, ty, 3)
        d.line(a[0], a[1], b[0], b[1], 0.85, 6)
    for x0 in (20, 163):                                             # far hulls of the two pontoons
        box(x0, x0 + 34, -22, -5, 0, 8, top=0.9, side=0.5, end=0.62)
    box(0, 217, 0, 42, 0, 3.2, top=0.62, side=0.36, end=0.46, sw=8)  # the element: barely any freeboard
    for k in range(1, 9):                                            # nine cast segments
        a, b = P(217 * k / 9, 0, 3.2), P(217 * k / 9, 42, 3.2)
        d.line(a[0], a[1], b[0], b[1], 0.9, 4)
    for x0 in (20, 163):
        box(x0, x0 + 34, 47, 64, 0, 8, top=0.9, side=0.5, end=0.62)  # near hull
        box(x0 + 3, x0 + 31, -22, 64, 8, 11, top=0.95, side=0.55, end=0.7)   # deck bridging over the element
        box(x0 + 11, x0 + 23, 12, 30, 11, 19, top=1.0, side=0.6, end=0.75, sw=5)   # winch house
    for tx, ty in tugs:
        k = 1.75
        hull = [(-8, -3.6), (5, -3.6), (9.5, 0), (5, 3.6), (-8, 3.6)]
        d.poly([P(tx + a * k, ty + b * k, 0) for a, b in hull], fill=0.4, stroke=WH, sw=5)
        d.poly([P(tx + a * k, ty + b * k, 3) for a, b in hull], fill=0.92, stroke=WH, sw=5)
        box(tx - 4 * k, tx + 1.5 * k, ty - 2 * k, ty + 2 * k, 3, 8, top=1.0, side=0.5, end=0.65, sw=4)


def g02(d):
    """Blank wall calendar, one day torn out."""
    px, py, pw, ph = 500, 170, 920, 760
    d.rect(px, py, pw, ph, fill=0.26, stroke=WH, sw=10)
    d.rect(px, py, pw, 120, fill=0.9)
    for i in range(8):
        cx = px + 80 + i * (pw - 160) / 7
        d.circle(cx, py + 44, 17, fill=0.0)
        d.line(cx, py + 44, cx, py - 34, WH, 12)
    gx, gy, gw, gh = px + 40, py + 160, pw - 80, ph - 200
    cw, ch = gw / 7, gh / 5
    hole = (4, 2)
    for r in range(5):
        for c in range(7):
            if (c, r) == hole:
                continue
            d.rect(gx + c * cw + 9, gy + r * ch + 9, cw - 18, ch - 18, fill=0.6)
    rnd = random.Random(7)

    def ragged(x, y, w, h, j=11, n=7):
        pts = []
        for i in range(n):
            pts.append((x + w * i / n, y + rnd.uniform(-j, j)))
        for i in range(n):
            pts.append((x + w + rnd.uniform(-j, j), y + h * i / n))
        for i in range(n):
            pts.append((x + w - w * i / n, y + h + rnd.uniform(-j, j)))
        for i in range(n):
            pts.append((x + rnd.uniform(-j, j), y + h - h * i / n))
        return pts

    hx, hy = gx + hole[0] * cw, gy + hole[1] * ch
    d.poly(ragged(hx - 4, hy - 4, cw + 8, ch + 8), fill=0.0, stroke=WH, sw=9)
    d.c.save()                                                       # the torn square, fallen to one side
    d.c.translate(1540, 840)
    d.c.rotate(19)
    d.poly(ragged(-cw / 2, -ch / 2, cw, ch, 9), fill=0.95)
    d.c.restore()

    def lit(a):
        ramp = np.linspace(1.0, 0.62, W, dtype=np.float32)[None, :]
        return a * ramp
    d.post = lit


def g03(d):
    """Two islands across a strait, one line between them."""
    north = [(300, 262), (500, 178), (800, 205), (1090, 160), (1400, 185), (1630, 262), (1600, 352), (1390, 404), (1170, 380),
             (1030, 432), (860, 398), (650, 428), (430, 386)]
    south = [(690, 742), (870, 690), (1080, 706), (1236, 790), (1206, 900), (1020, 952), (820, 934), (676, 858)]
    d.wavedashes(240, 440, 1680, 960, 34, seed=11, v=0.3, sw=7, ln=58,
                 avoid=[(640, 660, 1280, 980), (880, 420, 1040, 700)])
    for pts in (north, south):
        cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        d.path(smooth(pts), fill=0.3, stroke=WH, sw=10)
        d.path(smooth([(cx + (x - cx) * 0.7, cy + (y - cy) * 0.62) for x, y in pts]), fill=0.46)
        d.path(smooth([(cx + (x - cx) * 0.4, cy + (y - cy) * 0.3) for x, y in pts]), fill=0.62)
    a, b = (1000, 428), (905, 694)
    d.line(a[0], a[1], b[0], b[1], 0.0, 30)
    d.line(a[0], a[1], b[0], b[1], WH, 14)
    for q in (a, b):
        d.circle(q[0], q[1], 24, fill=WH, stroke=0.0, sw=8)


def g04(d):
    """TBM cutterhead face-on, the right half being erased."""
    cx, cy, R = 960, 540, 410
    d.circle(cx, cy, R, fill=0.26, stroke=WH, sw=18)
    d.circle(cx, cy, R * 0.72, stroke=0.6, sw=8)
    for k in range(6):                                               # muck openings between the arms
        a = math.radians(k * 60 + 30)
        pts = []
        for t in np.linspace(-0.2, 0.2, 9):
            pts.append((cx + math.cos(a + t) * R * 0.86, cy + math.sin(a + t) * R * 0.86))
        for t in np.linspace(0.13, -0.13, 9):
            pts.append((cx + math.cos(a + t) * R * 0.36, cy + math.sin(a + t) * R * 0.36))
        d.poly(pts, fill=0.0, stroke=0.75, sw=6)
    for k in range(6):                                               # arms with disc cutters
        a = math.radians(k * 60)
        ca, sa = math.cos(a), math.sin(a)
        wd = 44
        d.poly([(cx - sa * wd, cy + ca * wd), (cx + ca * R * 0.95 - sa * wd, cy + sa * R * 0.95 + ca * wd),
                (cx + ca * R * 0.95 + sa * wd, cy + sa * R * 0.95 - ca * wd), (cx + sa * wd, cy - ca * wd)], fill=0.7, stroke=WH, sw=8)
        for r in (0.34, 0.5, 0.66, 0.82):
            d.circle(cx + ca * R * r, cy + sa * R * r, 21, fill=0.0, stroke=WH, sw=7)
    d.circle(cx, cy, 96, fill=0.85, stroke=WH, sw=10)
    d.circle(cx, cy, 36, fill=0.0)

    def erase(a):
        rnd = random.Random(3)
        xs = np.arange(W, dtype=np.float32)[None, :]
        m = np.ones((H, W), np.float32)
        y, band = 0, 30
        while y < H:
            cut = cx + rnd.uniform(-110, 250)
            fade = np.clip(1 - (xs - cut) / 200.0, 0, 1) * 0.55
            m[y:y + band] = np.where(xs < cut, 1.0, fade)
            y += band
        return a * cv2.GaussianBlur(m, (0, 0), 3)
    d.post = erase


def g05(d):
    """The method: a trench in the seabed, sections end to end, one still hanging in the water."""
    wl, sb, tb = 235, 700, 850
    d.water(134, 1786, wl, 960)
    top = [(134, sb), (250, sb), (310, tb), (1620, tb), (1680, sb), (1786, sb)]
    d.seabed(top)
    ew, eh = 248, 92
    x = 330
    for i in range(4):
        d.rect(x + i * (ew + 6), tb - eh, ew, eh, fill=LT, stroke=WH, sw=9)
    hx, hy = x + 4 * (ew + 6), 430
    for px in (hx + 44, hx + ew - 44):                               # two pontoons at the surface, cables down
        d.line(px, wl + 20, px, hy, WH, 8)
        d.rect(px - 52, wl - 34, 104, 62, fill=0.9, stroke=WH, sw=6)
    d.rect(hx, hy, ew, eh, fill=0.85, stroke=WH, sw=10)
    d.arrow(hx + ew / 2, hy + eh + 34, hx + ew / 2, tb - eh - 26, WH, 18, 54)
    d.waterline(170, 1750, wl, skip=[(hx - 16, hx + 104), (hx + ew - 104, hx + ew + 16)])


def g06(d):
    """Casting hall in one-point perspective, an element on its line running away from us."""
    vx, vy = 960, 470
    prof = [(200, 950), (200, 270), (960, 120), (1720, 270), (1720, 950)]

    def pt(s, p):
        return (vx + s * (p[0] - vx), vy + s * (p[1] - vy))
    near, far = 1.0, 0.17
    d.poly([pt(near, prof[0]), pt(near, prof[4]), pt(far, prof[4]), pt(far, prof[0])], fill=0.13)
    d.poly([pt(far, p) for p in prof], fill=0.07)
    d.rect(vx - 44, pt(far, prof[0])[1] - 62, 88, 62, fill=0.95)     # daylight at the far door
    for p in prof:
        a, b = pt(near, p), pt(far, p)
        d.line(a[0], a[1], b[0], b[1], 0.55, 7)
    for s in (0.17, 0.23, 0.31, 0.42, 0.56, 0.75, 1.0):
        d.poly([pt(s, p) for p in prof], stroke=0.4 + 0.6 * s, sw=5 + 9 * s, close=False)
        a, b = pt(s, prof[1]), pt(s, prof[3])
        d.line(a[0], a[1], b[0], b[1], 0.3 + 0.5 * s, 4 + 5 * s)     # truss tie
    for rx in (640, 1280):                                           # rails
        a, b = pt(1.0, (rx, 950)), pt(0.6, (rx, 950))
        d.line(a[0], a[1], b[0], b[1], WH, 10)
    sb, sf = 0.6, 0.2                                                # the element: front face near, body receding
    x0, x1, y0, y1 = 410, 1510, 716, 950
    d.poly([pt(sb, (x0, y0)), pt(sb, (x1, y0)), pt(sf, (x1, y0)), pt(sf, (x0, y0))], fill=0.42, stroke=WH, sw=7)
    for k in range(1, 9):
        s = 1 / (1 / sb + (1 / sf - 1 / sb) * k / 9)                 # equal segments in depth
        a, b = pt(s, (x0, y0)), pt(s, (x1, y0))
        d.line(a[0], a[1], b[0], b[1], 0.85, 4)
    fa, fb = pt(sb, (x0, y0)), pt(sb, (x1, y1))
    element_face(d, fa[0], fa[1], fb[0] - fa[0], fb[1] - fa[1], fill=0.78, sw=9)


def g07(d):
    """Cross-section: five tubes. Road, road, narrow service gallery, rail, rail. Sitting in its trench under the sea."""
    x, y, w, h = 290, 440, 1340, 300
    d.water(134, 1786, 180, 400)
    top = [(134, 372), (200, 372), (x - 14, y + h + 34), (x + w + 14, y + h + 34), (1720, 372), (1786, 372)]
    d.seabed(top, bottom=900)
    back = mkpath([(200, 372), (x - 14, y + h + 34), (x + w + 14, y + h + 34), (1720, 372)])
    d.path(back, fill=0.16)
    d.dots(back, v=0.42, r=6, gap=30, seed=5)
    d.poly([(200, 372), (1720, 372)], stroke=0.9, sw=9, close=False)
    tubes = element_face(d, x, y, w, h, fill=0.7, sw=11)
    for i, (kind, tx, ty, tw, th) in enumerate(tubes):
        base = ty + th
        if kind == "road":
            d.rect(tx, base - 16, tw, 16, fill=0.45)
            for f in (0.27, 0.73):
                car_front(d, tx + tw * f, base - 16, 132)
        elif kind == "rail":
            d.rect(tx, base - 16, tw, 16, fill=0.45)
            train_front(d, tx + tw / 2, base - 16, 132, 176)
        else:
            for k in range(4):
                d.circle(tx + tw / 2, ty + 34 + k * 46, 13, fill=0.9)
    d.waterline(170, 1750, 180)


def g08(d):
    """Trailing suction dredger above the trench it is cutting."""
    wl, sb, tb = 350, 760, 866
    d.water(134, 1786, wl, 960)
    top = [(134, sb), (210, sb), (270, tb), (1250, tb), (1310, sb), (1786, sb)]
    d.seabed(top)
    hull = [(430, 268), (1300, 268), (1420, 248), (1352, 410), (474, 410), (430, 340)]
    d.poly(hull, fill=0.72, stroke=WH, sw=9)
    d.clip(mkpath(hull))
    d.rect(300, wl, 1300, 100, fill=0.42)
    d.unclip()
    d.poly(hull, stroke=WH, sw=9)
    d.rect(1150, 150, 160, 118, fill=0.9, stroke=WH, sw=7)           # bridge
    d.rect(1172, 172, 116, 26, fill=0.0)
    d.rect(1200, 96, 16, 54, fill=0.9)
    d.rect(500, 180, 64, 88, fill=0.8, stroke=WH, sw=6)              # funnel
    heap = mkpath([(640, 268), (760, 214), (900, 232), (1010, 206), (1100, 268)])
    d.path(heap, fill=0.5, stroke=WH, sw=7)                          # the hopper, heaped with spoil
    d.dots(heap, v=0.95, r=5, gap=24, seed=2)
    for gx in (760, 980):                                            # gantries that carry the pipe
        d.line(gx, 268, gx + 20, 330, WH, 9)
    a, b = (720, 320), (1218, 838)
    d.line(a[0], a[1], b[0], b[1], 0.0, 44)
    d.line(a[0], a[1], b[0], b[1], WH, 26)
    d.circle(a[0], a[1], 26, fill=WH)
    d.circle((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 25, fill=WH, stroke=0.0, sw=7)
    d.poly([(1186, 822), (1290, 800), (1300, 862), (1200, 866)], fill=WH)          # draghead at the cut face
    rnd = random.Random(9)
    for _ in range(16):
        d.circle(rnd.uniform(1150, 1330), rnd.uniform(730, 800), rnd.uniform(5, 9), fill=0.7)
    d.waterline(170, 1750, wl, skip=[(440, 1372)])


def g09(d):
    """Why IVY is needed: the element floats with only its roof above the water."""
    x, w, h = 330, 1260, 270
    wl = 372
    top = wl - 34
    d.water(134, 1786, wl, 900)
    d.wavedashes(180, wl + 60, 1740, 880, 22, seed=6, v=0.3, sw=7, avoid=[(x - 40, wl, x + w + 40, top + h + 190)])
    element_face(d, x, top, w, h, fill=0.74, sw=12)
    d.waterline(170, 1750, wl, skip=[(x - 6, x + w + 6)], sw=11, v=1.0)
    for ax in (x + w * 0.2, x + w * 0.5, x + w * 0.8):               # buoyancy
        d.arrow(ax, top + h + 170, ax, top + h + 34, WH, 20, 56)


def g10(d):
    """From directly above: two catamaran pontoons astride the two ends of one element."""
    x, y, w, h = 310, 414, 1300, 252
    d.wavedashes(190, 170, 1730, 930, 34, seed=8, v=0.28, sw=7, avoid=[(x - 40, 250, x + w + 40, 830)])
    d.rect(x, y, w, h, fill=0.42, stroke=WH, sw=10)
    for k in range(1, 9):
        d.line(x + w * k / 9, y + 8, x + w * k / 9, y + h - 8, 0.75, 4, butt=True)
    for px in (x + 96, x + w - 96 - 300):
        for by in (px + 34, px + 131, px + 228):                     # cross-beams over the element
            d.rect(by, y - 60, 38, h + 120, fill=0.0)
            d.rect(by + 4, y - 60, 30, h + 120, fill=0.95)
        for hy in (y - 150, y + h + 46):                             # the two hulls, one each side
            d.rect(px, hy, 300, 104, fill=0.86, stroke=WH, sw=9, r=30)
            for cxx in (px + 62, px + 238):
                d.circle(cxx, hy + 52, 20, fill=0.0)


def g11(d):
    """The pontoon alone at an empty quay: nothing between its hulls, cables hanging slack."""
    wl = 716
    d.water(134, 1786, wl, 930)
    d.rect(134, 606, 1652, wl - 606 + 30, fill=0.2)                  # the long quay wall behind
    d.line(134, 606, 1786, 606, 0.7, 9, butt=True)
    for bx in (330, 1590):                                           # bollards
        d.rect(bx - 16, 566, 32, 40, fill=0.9)
        d.rect(bx - 26, 556, 52, 16, fill=0.9, r=6)
    d.curve([(330, 580), (450, 760), (600, 640)], 0.9, 7)            # slack mooring lines
    d.curve([(1590, 580), (1470, 760), (1320, 640)], 0.9, 7)
    for hx in (590, 1140):                                           # two hulls, end-on
        d.rect(hx - 8, 578, 206, 232, fill=0.0)
        d.rect(hx, 586, 190, 216, fill=0.8, stroke=WH, sw=9)
        d.rect(hx + 5, wl, 180, 802 - wl - 5, fill=0.4)
    d.rect(540, 468, 840, 118, fill=0.0)
    d.rect(550, 478, 820, 108, fill=0.92, stroke=WH, sw=9)           # the deck that bridges them
    for tx in (650, 1200):                                           # winch towers
        d.poly([(tx, 478), (tx + 16, 330), (tx + 54, 330), (tx + 70, 478)], fill=0.7, stroke=WH, sw=8)
        d.circle(tx + 35, 322, 26, fill=0.0, stroke=WH, sw=9)
    for a, b in ((800, 890), (940, 1030), (1070, 1120)):             # lifting cables, limp, holding nothing
        if b > 1100:
            continue
        d.curve([(a, 586), ((a + b) / 2, 586 + 190), (b, 586)], WH, 8)
    d.line(985, 586, 985, 668, WH, 8)
    d.poly([(965, 668), (1005, 668), (1005, 700), (985, 712), (965, 700)], fill=WH)
    d.waterline(170, 1750, wl, skip=[(584, 786), (1134, 1336)])


def g12(d):
    """Seen from astern: the element between its pontoons, five tugs fanned ahead, heading for the harbour mouth."""
    cx = 960
    d.wavedashes(230, 420, 1690, 950, 30, seed=13, v=0.28, sw=7, avoid=[(560, 380, 1360, 960)])
    for x0, x1 in ((230, 716), (1204, 1690)):                        # the two breakwaters and their lights
        d.poly([(x0, 372), (x1, 372), (x1 - 8, 328), (x0 + 8, 328)] if x0 < cx else [(x0, 372), (x1, 372), (x1 - 8, 328), (x0 + 8, 328)],
               fill=0.4, stroke=0.9, sw=8)
        bx = x1 - 34 if x0 < cx else x0 + 34
        d.rect(bx - 15, 236, 30, 92, fill=0.85)
        d.circle(bx, 222, 22, fill=WH)
    tugs = [(960, 430, 0.82), (800, 452, 0.88), (1120, 452, 0.88), (650, 492, 0.96), (1270, 492, 0.96)]
    for tx, ty, k in tugs:                                           # tow lines
        d.line(cx + (tx - cx) * 0.12, 606, tx, ty + 20 * k, 0.85, 6)
    for tx, ty, k in tugs:
        d.poly([(tx - 46 * k, ty), (tx + 46 * k, ty), (tx + 36 * k, ty + 32 * k), (tx - 36 * k, ty + 32 * k)], fill=0.6, stroke=WH, sw=6)
        d.rect(tx - 24 * k, ty - 40 * k, 48 * k, 40 * k, fill=0.95)
        d.rect(tx - 5 * k, ty - 66 * k, 10 * k, 28 * k, fill=0.95)
    yn, yf, hn, hf = 900, 606, 215, 128
    d.poly([(cx - hn, yn), (cx + hn, yn), (cx + hf, yf), (cx - hf, yf)], fill=0.66, stroke=WH, sw=9)   # element roof, receding
    d.rect(cx - hn, yn, 2 * hn, 40, fill=0.4, stroke=WH, sw=9)                                          # its low stern face

    def slab(yn_, yf_, hwn, hwf, ht):
        d.poly([(cx - hwn, yn_ - ht), (cx + hwn, yn_ - ht), (cx + hwf, yf_ - ht), (cx - hwf, yf_ - ht)], fill=0.95, stroke=WH, sw=7)
        d.rect(cx - hwn, yn_ - ht, 2 * hwn, ht, fill=0.5, stroke=WH, sw=7)
        d.rect(cx - hwn * 0.62, yn_ - ht + 8, 2 * hwn * 0.62, ht, fill=0.0)                             # the tunnel between the hulls
        d.rect(cx - hwn * 0.2, yn_ - ht - 64, hwn * 0.4, 46, fill=0.8, stroke=WH, sw=5)
    slab(690, 640, 262, 240, 34)
    slab(868, 792, 344, 314, 48)


def g13(d):
    """Lowering: two pontoons, steel wires, the element going down onto the gravel bed in the trench."""
    wl, bed, floor = 250, 862, 892
    d.water(134, 1786, wl, 960)
    d.rect(134, 770, 1652, floor - 770, fill=0.22)                   # the far wall of the trench
    d.line(134, 770, 1786, 770, 0.6, 7, butt=True)
    d.seabed([(134, floor), (1786, floor)], sw=7)
    g = mkpath([(134, bed), (1786, bed), (1786, floor), (134, floor)])
    d.path(g, fill=0.3)
    d.dots(g, v=WH, r=7, gap=22, seed=3)                             # gravel
    d.rect(160, bed - 112, 268, 112, fill=0.55, stroke=0.9, sw=8)    # the piece already down
    ex, ey, ew, eh = 452, 470, 1010, 112
    for px in (ex + 90, ex + ew - 90 - 250):
        d.poly([(px + 70, wl - 50), (px + 96, wl - 150), (px + 154, wl - 150), (px + 180, wl - 50)], fill=0.7, stroke=WH, sw=8)
        for cxx in (px + 40, px + 210):
            d.line(cxx, wl + 30, cxx, ey, WH, 8)
        d.rect(px, wl - 50, 250, 88, fill=0.92, stroke=WH, sw=9)
    d.rect(ex, ey, ew, eh, fill=LT, stroke=WH, sw=10)
    for i in range(4):                                               # ballast tanks, part filled
        tx = ex + 60 + i * 235
        d.rect(tx, ey + 22, 180, eh - 44, fill=0.0)
        d.rect(tx, ey + 22 + (eh - 44) * 0.45, 180, (eh - 44) * 0.55, fill=0.95)
    for ax in (ex + ew * 0.27, ex + ew * 0.73):
        d.arrow(ax, ey + eh + 36, ax, bed - 150 + 104, WH, 20, 56)
    d.waterline(170, 1750, wl, skip=[(ex + 80, ex + 350), (ex + ew - 350, ex + ew - 80)])


def g14(d):
    """Close-up: two hydraulic arms on one element end reach over the gap and grip the next."""
    y0, y1 = 240, 840
    lx, rx = 850, 1070
    d.rect(180, y0, lx - 180, y1 - y0, fill=0.44)
    d.rect(rx, y0, 1740 - rx, y1 - y0, fill=0.44)
    d.poly([(180, y0), (lx, y0), (lx, y1), (180, y1)], stroke=WH, sw=11, close=False)
    d.poly([(1740, y0), (rx, y0), (rx, y1), (1740, y1)], stroke=WH, sw=11, close=False)
    for gy in (y0 + 48, y1 - 48):                                    # the rubber gasket waiting on the end face
        d.oval(lx + 16, gy, 30, 38, fill=WH)
    for ay in (420, 660):
        d.rect(470, ay - 62, 330, 124, fill=0.0)
        d.rect(480, ay - 52, 310, 104, fill=0.86, stroke=WH, sw=9, r=14)       # cylinder
        d.rect(430, ay - 34, 60, 68, fill=0.86, stroke=WH, sw=7)
        d.line(790, ay, 1100, ay, 0.0, 52, butt=True)
        d.line(790, ay, 1100, ay, WH, 32, butt=True)                           # rod, across the gap
        d.rect(rx + 86, ay - 76, 150, 152, fill=0.0)
        d.rect(rx + 110, ay - 60, 120, 120, fill=0.8, stroke=WH, sw=8)         # catch block on the next element
        d.poly([(1090, ay - 44), (1220, ay - 44), (1220, ay - 16), (1132, ay - 16), (1132, ay + 16), (1220, ay + 16), (1220, ay + 44), (1090, ay + 44)],
               fill=WH, stroke=0.0, sw=5)                                      # the jaw
        d.circle(1178, ay, 13, fill=WH)
    d.arrow(1640, 540, 1380, 540, WH, 26, 70)


def g15(d):
    """The joint: two end walls, the chamber between them drained, the sea pressing the gasket shut."""
    d.water(134, 1786, 170, 910, v=0.15)
    d.wavedashes(200, 200, 1720, 880, 26, seed=21, v=0.36, sw=7, avoid=[(150, 290, 1770, 790)])
    y0, y1, roof, flr = 330, 750, 72, 84
    for sgn, xa, xb in ((1, 430, 938), (-1, 982, 1490)):
        d.rect(xa, y0, xb - xa, y1 - y0, fill=0.7)
        d.rect(xa, y0 + roof, xb - xa, y1 - y0 - roof - flr, fill=0.0)          # the tube
        far = xa if sgn > 0 else xb - 44
        near = xb - 96 if sgn > 0 else xa + 52
        d.rect(far, y0, 44, y1 - y0, fill=0.7)                                  # outer end wall
        d.rect(near, y0, 44, y1 - y0, fill=WH)                                  # end wall at the joint
        d.rect(xa, y0, xb - xa, y1 - y0, stroke=WH, sw=10)
    for gy in (y0 + roof / 2, y1 - flr / 2):                                    # gasket, squeezed
        d.rect(924, gy - 30, 72, 60, fill=0.0, r=20)
        d.rect(930, gy - 24, 60, 48, fill=WH, r=18)
    d.rect(938, y0 + roof - 5, 44, y1 - y0 - roof - flr + 10, fill=0.0)         # drained gap between the faces
    d.rect(886, y1 - flr - 26, 148, 26, fill=0.4)                               # the last of the water
    d.arrow(960, y1 - flr - 150, 960, y1 - flr - 34, 0.8, 14, 40)
    d.bigarrow(215, 412, 540)
    d.bigarrow(1705, 1508, 540)


def g16(d):
    """Three stacks of blank coins, nearly but not quite the same height."""
    rx, ry, t, base = 172, 50, 46, 900
    for cx, n in ((470, 9), (960, 11), (1450, 10)):
        for i in range(n):
            y = base - i * t
            d.oval(cx, y, rx, ry, fill=0.4)
            d.rect(cx - rx, y - t, 2 * rx, t, fill=0.4)
            d.oval(cx, y - t, rx, ry, fill=0.0)
            d.oval(cx, y - t + 5, rx, ry, fill=0.62 if i < n - 1 else 0.0)
            if i == n - 1:
                d.oval(cx, y - t, rx, ry, fill=WH)
                d.oval(cx, y - t, rx - 30, ry - 11, stroke=0.6, sw=7)
        d.line(cx - rx, base, cx - rx, base - n * t, WH, 7)
        d.line(cx + rx, base, cx + rx, base - n * t, WH, 7)


def g17(d):
    """A toll barrier across the one lane into the tunnel."""
    d.poly([(330, 300), (1590, 300), (1590, 640), (330, 640)], fill=0.36, stroke=0.9, sw=9)
    d.hatch(mkpath([(330, 300), (1590, 300), (1590, 640), (330, 640)]), 0.5, 5, 40, 60)
    d.rect(690, 366, 540, 274, fill=0.0, stroke=WH, sw=14)            # the mouth
    d.poly([(690, 640), (1230, 640), (1560, 980), (360, 980)], fill=0.2)
    d.line(690, 640, 360, 980, WH, 12)
    d.line(1230, 640, 1560, 980, WH, 12)
    for ya, yb in ((660, 700), (740, 800), (860, 950)):               # centre dashes running in
        wa, wb = 5 + (ya - 640) * 0.035, 5 + (yb - 640) * 0.035
        d.poly([(960 - wa, ya), (960 + wa, ya), (960 + wb, yb), (960 - wb, yb)], fill=0.8)
    by = 800
    d.rect(1470, by - 60, 96, 200, fill=0.0)
    d.rect(1480, by - 50, 76, 190, fill=0.75, stroke=WH, sw=9)        # the post
    d.rect(372, by - 36, 1130, 64, fill=0.0)
    n = 9
    seg = 1100 / n
    for i in range(n):                                                # striped arm
        d.rect(390 + i * seg, by - 22, seg + 1, 44, fill=WH if i % 2 == 0 else 0.42)
    d.rect(390, by - 22, 1100, 44, stroke=WH, sw=7)
    d.circle(1518, by, 30, fill=0.0, stroke=WH, sw=10)


def g18(d):
    """Tunnel mouth on the shore; the railway out of it simply stops in the grass."""
    d.line(250, 252, 1670, 252, 0.6, 8)
    d.wavedashes(280, 268, 1640, 318, 12, seed=17, v=0.4, sw=7, ln=70, avoid=[(760, 240, 1160, 340)])
    d.line(250, 336, 770, 336, 0.9, 9)
    d.line(1150, 336, 1670, 336, 0.9, 9)
    d.poly([(790, 300), (560, 660), (850, 484)], fill=0.34, stroke=0.9, sw=8)      # cutting walls
    d.poly([(1130, 300), (1360, 660), (1070, 484)], fill=0.34, stroke=0.9, sw=8)
    d.rect(790, 290, 340, 194, fill=0.6, stroke=WH, sw=10)
    d.rect(838, 334, 244, 150, fill=0.0, stroke=WH, sw=8)
    ya, yb = 484, 770
    ha, hb = 44, 170                                                 # half gauge near the portal and at the track's end
    d.poly([(960 - ha - 34, ya), (960 + ha + 34, ya), (960 + hb + 110, yb + 14), (960 - hb - 110, yb + 14)], fill=0.17)
    t = 0.0
    k = 0
    while t < 1.0:                                                   # sleepers, spreading as they come toward us
        y = ya + (yb - ya) * t
        hw = (ha + (hb - ha) * t) * 1.42
        d.line(960 - hw, y, 960 + hw, y, 0.62, 6 + 14 * t, butt=True)
        k += 1
        t += 0.05 + 0.028 * k
    for sgn in (-1, 1):
        d.line(960 + sgn * ha, ya, 960 + sgn * hb, yb, WH, 13, butt=True)
    rnd = random.Random(5)
    tufts = []
    for _ in range(400):
        x, y = rnd.uniform(330, 1590), rnd.uniform(690, 960)
        if y < yb + 40 and abs(x - 960) < hb + 190:
            continue
        if any(abs(x - a) < 96 and abs(y - b) < 54 for a, b in tufts):
            continue
        tufts.append((x, y))
    for x, y in tufts:
        s = 0.8 + (y - 690) / 400
        for dx in (-26, -9, 9, 26):
            d.line(x + dx * 0.35 * s, y, x + dx * s, y - 44 * s * (1.0 if abs(dx) < 12 else 0.74), 0.8, 7)


def g19(d):
    """Fehmarnsund: the arched bridge over the sound, and a short immersed tunnel in the seabed beside it."""
    wl, sb, land = 540, 690, 452
    d.water(420, 1500, wl, sb + 10)
    top = [(134, land), (400, land), (590, sb), (1330, sb), (1520, land), (1786, land)]
    d.seabed(top, bottom=950)
    deck = 330
    for px in (330, 520, 780, 1140, 1400, 1590):                     # piers
        gy = land if (px < 400 or px > 1520) else (sb if 590 <= px <= 1330 else land + (sb - land) * ((px - 400) / 190 if px < 600 else (1520 - px) / 190))
        d.line(px, deck, px, gy, 0.8, 16, butt=True)
    p = skia.Path()                                                  # the arch over the middle span
    p.moveTo(780, deck)
    p.quadTo(960, deck - 380, 1140, deck)
    d.path(p, None, WH, 16)
    for i in range(1, 8):
        hx = 780 + 360 * i / 8
        tt = i / 8
        hy = deck - 380 * 2 * tt * (1 - tt)
        d.line(hx, deck, hx, hy, 0.9, 5)
    d.line(230, deck, 1690, deck, WH, 22, butt=True)
    ty, th = 772, 84                                                 # the tunnel: a short row of boxes under the bed
    d.poly([(350, land + 4), (600, ty + th / 2)], stroke=0.0, sw=62, close=False, butt=True)
    d.poly([(1570, land + 4), (1320, ty + th / 2)], stroke=0.0, sw=62, close=False, butt=True)
    d.poly([(350, land + 4), (600, ty + th / 2)], stroke=0.62, sw=40, close=False, butt=True)
    d.poly([(1570, land + 4), (1320, ty + th / 2)], stroke=0.62, sw=40, close=False, butt=True)
    d.rect(576, ty - 14, 768, th + 28, fill=0.0)
    n = 5
    bw = 740 / n
    for i in range(n):
        d.rect(590 + i * bw + 3, ty, bw - 6, th, fill=0.92, stroke=WH, sw=7)
    d.waterline(452, 1468, wl, skip=[(508, 532), (768, 792), (1128, 1152), (1388, 1412)])


def g20(d):
    """Eighty-nine elements; the first four are down."""
    rows = (23, 22, 22, 22)
    pitch, bw, bh, rp = 62, 44, 128, 176
    x0 = (W - (23 * pitch - (pitch - bw))) / 2
    y0 = (H - (3 * rp + bh)) / 2
    n = 0
    for r, cnt in enumerate(rows):
        for c in range(cnt):
            x, y = x0 + c * pitch, y0 + r * rp
            if n < 4:
                d.rect(x - 3, y - 3, bw + 6, bh + 6, fill=WH)
            else:
                d.rect(x + 3.5, y + 3.5, bw - 7, bh - 7, stroke=0.6, sw=7)
            n += 1
    assert n == 89


def g21(d):
    """Two paces from the same start: the one we have, and the far steeper one a 2031 date would need."""
    ox, oy = 400, 880
    for i in range(1, 6):
        d.line(ox + i * 200, oy - 16, ox + i * 200, oy + 16, 0.8, 9, butt=True)
    for i in range(1, 4):
        d.line(ox - 16, oy - i * 180, ox + 16, oy - i * 180, 0.8, 9, butt=True)
    d.poly([(ox, 190), (ox, oy), (1540, oy)], stroke=0.8, sw=13, close=False)
    a, b = (1500, 726), (1040, 220)
    d.line(ox, oy, a[0], a[1], 0.62, 18)
    d.circle(a[0], a[1], 28, fill=0.62)
    d.line(ox, oy, b[0], b[1], WH, 22)
    d.circle(b[0], b[1], 32, fill=WH)
    d.circle(ox, oy, 30, fill=WH, stroke=0.0, sw=8)


def g22(d):
    """Sources: plain papers and photographs fanned on a table."""
    def sheet(cx, cy, w, h, ang, kind, tone):
        d.c.save()
        d.c.translate(cx, cy)
        d.c.rotate(ang)
        d.rect(-w / 2 - 9, -h / 2 - 9, w + 18, h + 18, fill=0.0)
        d.rect(-w / 2, -h / 2, w, h, fill=tone, stroke=WH, sw=8)
        if kind == "doc":
            for i in range(7):
                ly = -h / 2 + 70 + i * (h - 120) / 7
                d.line(-w / 2 + 44, ly, w / 2 - (44 if i % 3 else 130), ly, 0.0 if tone > 0.5 else 0.8, 11, butt=True)
        else:
            d.rect(-w / 2 + 24, -h / 2 + 24, w - 48, h - 48, fill=0.0)
            d.clip(mkpath([(-w / 2 + 24, -h / 2 + 24), (w / 2 - 24, -h / 2 + 24), (w / 2 - 24, h / 2 - 24), (-w / 2 + 24, h / 2 - 24)]))
            d.poly([(-w / 2, h / 2), (-w * 0.2, -h * 0.05), (0, h * 0.2), (w * 0.2, -h * 0.18), (w / 2, h / 2)], fill=0.5)
            d.circle(-w * 0.22, -h * 0.22, 26, fill=WH)
            d.unclip()
        d.c.restore()
    sheet(640, 560, 430, 580, -24, "doc", 0.4)
    sheet(820, 520, 430, 580, -9, "doc", 0.55)
    sheet(1030, 520, 430, 580, 6, "doc", 0.72)
    sheet(1260, 570, 430, 580, 21, "doc", 0.9)
    sheet(760, 760, 400, 290, -13, "photo", 0.95)
    sheet(1190, 780, 400, 290, 10, "photo", 0.95)


PICS = [g01, g02, g03, g04, g05, g06, g07, g08, g09, g10, g11, g12, g13, g14, g15, g16, g17, g18, g19, g20, g21, g22]


# ------------------------------------------------------------------ checking

def engine_grey(im):
    """The film engine's treatment (flow.py grey + feather), copied so the check sees what the film will."""
    im = cv2.resize(im, (1280, 720), interpolation=cv2.INTER_AREA)
    g = im.astype(np.float32) / 255.0
    lo, hi = np.percentile(g, 3), np.percentile(g, 99.6)
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1)
    m = float(g.mean())
    g = g ** float(np.clip(math.log(0.36) / math.log(max(1e-3, m)), 1.0, 2.6))
    g = np.clip(g + 0.7 * (g - cv2.GaussianBlur(g, (0, 0), 3)), 0, 1)
    g = np.clip(g - 0.04, 0, 1) / 0.96
    h, w = g.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    f = np.clip(np.minimum(np.minimum(xx, w - 1 - xx) / (w * 0.26), np.minimum(yy, h - 1 - yy) / (h * 0.3)), 0, 1)
    return g * (f * f * (3 - 2 * f))


def sheet(tiles, path, cols=4, tw=480):
    th = tw * 9 // 16
    rows = -(-len(tiles) // cols)
    out = np.full((rows * (th + 8) + 8, cols * (tw + 8) + 8), 60, np.uint8)
    for i, t in enumerate(tiles):
        r, c = divmod(i, cols)
        out[8 + r * (th + 8): 8 + r * (th + 8) + th, 8 + c * (tw + 8): 8 + c * (tw + 8) + tw] = cv2.resize(t, (tw, th), interpolation=cv2.INTER_AREA)
    cv2.imwrite(path, out)


def main():
    os.makedirs(OUT, exist_ok=True)
    imgs = []
    for fn in PICS:
        d = D()
        fn(d)
        a = d.array()
        cv2.imwrite(os.path.join(OUT, fn.__name__ + ".png"), a)
        imgs.append(a)
    if "--sheets" in sys.argv:
        out = sys.argv[sys.argv.index("--sheets") + 1]
        os.makedirs(out, exist_ok=True)
        sheet(imgs, os.path.join(out, "sheet_plain.png"))
        sheet([cv2.resize(cv2.resize(a, (240, 135), interpolation=cv2.INTER_AREA), (W, H), interpolation=cv2.INTER_NEAREST) for a in imgs],
              os.path.join(out, "sheet_lowres.png"))
        sheet([(np.clip(engine_grey(a) * 1.15, 0, 1) * 255).astype(np.uint8) for a in imgs], os.path.join(out, "sheet_engine.png"))
    print("drew", len(imgs), "pictures into", OUT)


if __name__ == "__main__":
    main()
