"""Illustrations e01-e33 for pilot 01 ("Why $87,000 Feels Like Less"), drawn in code (skia).
White and greys on pure black, no text, no numerals, no logos, no faces. Briefs: IMAGES.md.
Helpers copied from ../megaprojects/diagrams.py (same house finish), plus a few object helpers.

    python illustrations.py                 draw src/ai/e01.png ... e33.png
    python illustrations.py --sheets DIR    also write contact sheets (plain, phone-size, low-res, engine-toned) into DIR
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

DK, MD, LT, WH = 0.32, 0.5, 0.68, 1.0


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


def smooth(pts, close=True):
    """Catmull-Rom curve through the points (closed by default)."""
    n = len(pts)
    p = skia.Path()
    p.moveTo(*pts[0])
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (close or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (close or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if close:
        p.close()
    return p


def union(paths):
    out = paths[0]
    for q in paths[1:]:
        out = skia.Op(out, q, skia.PathOp.kUnion_PathOp)
    return out


def circ_path(cx, cy, r):
    p = skia.Path()
    p.addCircle(cx, cy, r)
    return p


def rrect_path(x, y, w, h, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    return p


def ribbon(centre, half):
    """Polygon of a band of half-width half(i) around an open polyline."""
    n = len(centre)
    left, right = [], []
    for i in range(n):
        a, b = centre[max(0, i - 1)], centre[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        h = half(i) if callable(half) else half
        left.append((centre[i][0] + nx * h, centre[i][1] + ny * h))
        right.append((centre[i][0] - nx * h, centre[i][1] - ny * h))
    return left, right


class D:
    """One 1920x1080 black sheet and the drawing verbs every picture shares."""

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
        p = rrect_path(x, y, w, h, r) if r else None
        if p is None:
            p = skia.Path()
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
        p = skia.Path()
        p.moveTo(*pts[0])
        p.quadTo(pts[1][0], pts[1][1], pts[2][0], pts[2][1])
        self.path(p, None, v, sw)

    def glow(self, p, v=1.0, sigma=40):
        paint = skia.Paint(AntiAlias=True, Color=col(v), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sigma))
        self.c.drawPath(p, paint)

    # --- transforms
    def push(self, cx=0, cy=0, ang=0, sc=1.0):
        self.c.save()
        self.c.translate(cx, cy)
        if ang:
            self.c.rotate(ang)
        if sc != 1.0:
            self.c.scale(sc, sc)

    def pop(self):
        self.c.restore()

    # --- textures
    def clip(self, p):
        self.c.save()
        self.c.clipPath(p, skia.ClipOp.kIntersect, True)

    def unclip(self):
        self.c.restore()

    def hatch(self, p, v=0.5, sw=6, gap=30, ang=45):
        self.clip(p)
        b = p.getBounds()
        cx, cy = b.centerX(), b.centerY()
        R = math.hypot(b.width(), b.height()) / 2 + 10
        a = math.radians(ang)
        ux, uy = math.cos(a), -math.sin(a)
        nx, ny = -uy, ux
        k = -R
        while k <= R:
            self.line(cx + nx * k - ux * R, cy + ny * k - uy * R, cx + nx * k + ux * R, cy + ny * k + uy * R, v, sw, butt=True)
            k += gap
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

    def array(self):
        a = self.s.makeImageSnapshot().toarray()[:, :, 1].astype(np.float32) / 255.0
        if self.post:
            a = self.post(a)
        return (np.clip(a, 0, 1) * 255).astype(np.uint8)


# ------------------------------------------------------------------ shared subjects

def coin_stack(d, cx, base, n, w=150, t=24, ry=30, face=0.86, side=0.5):
    """A cylinder of n coins standing on y=base; returns the top y."""
    top = base - n * t
    p = skia.Path()
    p.moveTo(cx - w / 2, top)
    p.lineTo(cx - w / 2, base)
    p.arcTo(skia.Rect.MakeLTRB(cx - w / 2, base - ry, cx + w / 2, base + ry), 180, -180, False)
    p.lineTo(cx + w / 2, top)
    p.close()
    d.path(p, fill=side, stroke=WH, sw=6)
    for i in range(1, n):
        y = base - i * t
        q = skia.Path()
        q.addArc(skia.Rect.MakeLTRB(cx - w / 2, y - ry, cx + w / 2, y + ry), 0, 180)
        d.path(q, None, 0.2, 4)
    d.line(cx - w * 0.36, top + 10, cx - w * 0.36, base + ry * 0.6, 0.72, 7)        # highlight
    d.oval(cx, top, w / 2, ry, fill=face, stroke=WH, sw=6)
    d.oval(cx, top, w / 2 * 0.76, ry * 0.76, stroke=0.55, sw=4)
    return top


def key_path(L=1000, R=170, hb=150, hole=62):
    """A plain house key lying along +x, bow centred at the origin. Returns (outline path, hole path)."""
    bow = circ_path(0, 0, R)
    neck = mkpath([(R * 0.6, -hb * 0.62), (R * 1.35, -hb * 0.62), (R * 1.35, hb * 0.62), (R * 0.6, hb * 0.62)])
    x0, x1 = R * 1.3, L
    ytop, ybot = -hb / 2, hb / 2
    pts = [(x0, ytop), (x0 + 60, ytop)]
    teeth = [0.0, 0.55, 0.15, 0.7, 0.3, 0.62, 0.1, 0.5, 0.2]
    span = (x1 - 110) - (x0 + 60)
    for i, dep in enumerate(teeth):
        xa = x0 + 60 + span * i / len(teeth)
        xb = x0 + 60 + span * (i + 0.5) / len(teeth)
        pts.append((xa, ytop))
        pts.append((xb, ytop + dep * hb * 0.55))
    pts += [(x1 - 110, ytop + 0.2 * hb), (x1, ytop + hb * 0.45), (x1, ybot), (x0, ybot)]
    blade = mkpath(pts)
    outline = union([bow, neck, blade])
    return outline, circ_path(-R * 0.25, 0, hole)


def house_front(d, x, base, w, h, body=0.42, roof=0.6, win=0.08, lit=False, chimney=True, door=True, sw=8):
    """Front elevation of a small gabled house; wall box from base-h*0.62 to base."""
    wall_h = h * 0.62
    wy = base - wall_h
    if chimney:
        d.rect(x + w * 0.66, base - h * 0.98, w * 0.11, h * 0.3, fill=roof * 0.85, stroke=WH, sw=sw * 0.8)
    d.rect(x, wy, w, wall_h, fill=body, stroke=WH, sw=sw)
    d.poly([(x - w * 0.08, wy), (x + w / 2, base - h), (x + w * 1.08, wy)], fill=roof, stroke=WH, sw=sw)
    d.hatch(mkpath([(x - w * 0.08, wy), (x + w / 2, base - h), (x + w * 1.08, wy)]), roof * 0.7, 5, 26, 0)
    d.poly([(x - w * 0.08, wy), (x + w / 2, base - h), (x + w * 1.08, wy)], stroke=WH, sw=sw)
    ww, wh = w * 0.22, wall_h * 0.28
    wins = [(x + w * 0.12, wy + wall_h * 0.16), (x + w * 0.66, wy + wall_h * 0.16)]
    if not door:
        wins += [(x + w * 0.12, wy + wall_h * 0.56), (x + w * 0.66, wy + wall_h * 0.56)]
    for wx, wyy in wins:
        if lit:
            d.glow(rrect_path(wx - 10, wyy - 10, ww + 20, wh + 20, 4), 0.9, 30)
        d.rect(wx, wyy, ww, wh, fill=WH if lit else win, stroke=WH, sw=sw * 0.7)
        d.line(wx + ww / 2, wyy, wx + ww / 2, wyy + wh, 0.0 if lit else 0.5, sw * 0.6, butt=True)
        d.line(wx, wyy + wh / 2, wx + ww, wyy + wh / 2, 0.0 if lit else 0.5, sw * 0.6, butt=True)
    if door:
        d.rect(x + w * 0.4, wy + wall_h * 0.48, w * 0.2, wall_h * 0.52, fill=WH if lit else 0.2, stroke=WH, sw=sw * 0.7)
        d.circle(x + w * 0.56, wy + wall_h * 0.76, sw * 0.6, fill=0.0 if lit else WH)


LEDGER = dict(x=200, y=110, w=1520, h=860)


def ledger(d, filled=False):
    """The open accounting ledger seen from above (e02 empty, e31 filled with tallies and double rules)."""
    x, y, w, h = LEDGER["x"], LEDGER["y"], LEDGER["w"], LEDGER["h"]
    cx = x + w / 2
    d.rect(x - 26, y - 22, w + 52, h + 52, fill=0.26, stroke=0.7, sw=8, r=22)          # cover board
    d.hatch(rrect_path(x - 26, y - 22, w + 52, h + 52, 22), 0.34, 5, 22, 60)
    d.rect(x - 26, y - 22, w + 52, h + 52, stroke=0.7, sw=8, r=22)
    for k in range(3, 0, -1):                                                           # page block edges
        d.rect(x + k * 4, y + k * 5, w - k * 8, h, fill=0.62 + 0.06 * (3 - k), stroke=0.35, sw=3)
    for side in (-1, 1):                                                                # two pages, curved at the spine
        ox = cx if side > 0 else x
        p = skia.Path()
        if side < 0:
            p.moveTo(x, y)
            p.quadTo(x + w * 0.25, y - 18, cx, y + 14)
            p.lineTo(cx, y + h + 6)
            p.quadTo(x + w * 0.25, y + h - 16, x, y + h)
        else:
            p.moveTo(cx, y + 14)
            p.quadTo(x + w * 0.75, y - 18, x + w, y)
            p.lineTo(x + w, y + h)
            p.quadTo(x + w * 0.75, y + h - 16, cx, y + h + 6)
        p.close()
        d.path(p, fill=0.9)
        d.clip(p)
        d.rect(cx - 70 if side < 0 else cx, y - 20, 70, h + 40, fill=0.72)              # gutter shade
        d.rect(cx - 30 if side < 0 else cx, y - 20, 30, h + 40, fill=0.56)
        px0 = (x + 70) if side < 0 else (cx + 70)
        px1 = (cx - 60) if side < 0 else (x + w - 70)
        rows = 16
        top = y + 120
        rh = (h - 190) / rows
        d.rect(px0, y + 58, px1 - px0, 40, fill=0.62)                                   # blank header band
        for r in range(rows + 1):
            ly = top + r * rh
            d.line(px0, ly, px1, ly, 0.6, 4, butt=True)
        colx = [px0 + (px1 - px0) * f for f in (0.0, 0.5, 1.0)]
        mid = colx[1]
        d.line(mid, y + 58, mid, top + rows * rh, 0.25, 9, butt=True)                   # the centre line
        for xx in (px0, px1):
            d.line(xx, y + 58, xx, top + rows * rh, 0.45, 5, butt=True)
        for xx in (mid - 90, px1 - 90):
            d.line(xx, top, xx, top + rows * rh, 0.62, 4, butt=True)                    # money columns
        if filled:
            rnd = random.Random(31 if side < 0 else 32)
            for half_i, (a, b) in enumerate(((px0, mid - 90), (mid, px1 - 90))):
                n_rows = rows - 2
                for r in range(n_rows):
                    ly0, ly1 = top + r * rh + rh * 0.18, top + (r + 1) * rh - rh * 0.18
                    groups = rnd.choice((1, 2, 2, 3, 3, 4))
                    gx = a + 26
                    for g in range(groups):
                        strokes = 5 if g < groups - 1 else rnd.choice((2, 3, 4, 5))
                        sp = 15
                        for s in range(min(strokes, 4)):
                            d.line(gx + s * sp, ly0, gx + s * sp + 3, ly1, 0.08, 6)
                        if strokes == 5:
                            d.line(gx - 8, ly1 - 3, gx + 3 * sp + 10, ly0 + 3, 0.08, 6)
                        gx += 4 * sp + 30
                        if gx > b - 60:
                            break
                    d.line(b + 18, (ly0 + ly1) / 2, b + 72, (ly0 + ly1) / 2, 0.2, 8)    # an amount bar in the money column
                yb = top + (rows - 1) * rh
                for xa, xb in ((a + 10, b - 10), (b + 8, b + 84)):
                    d.line(xa, yb - 9, xb, yb - 9, 0.0, 9, butt=True)                     # the heavy double rule
                    d.line(xa, yb + 9, xb, yb + 9, 0.0, 9, butt=True)
                d.rect(b + 14, yb + 26, 64, rh * 0.5, fill=0.1)                           # the total
        d.unclip()
        d.path(p, stroke=WH, sw=7)
    d.line(cx, y + 14, cx, y + h + 6, 0.2, 8)


def pen(d, x, y, ang, L=820, r=34):
    """Fountain pen, nib at (x, y), lying along angle ang (degrees)."""
    d.push(x, y, ang)
    d.poly([(0, 0), (120, -r * 0.62), (150, -r * 0.7), (150, r * 0.7), (120, r * 0.62)], fill=0.92, stroke=WH, sw=5)   # nib
    d.line(10, 0, 112, 0, 0.15, 5)
    d.circle(92, 0, 7, fill=0.15)
    d.rect(150, -r * 0.78, 70, r * 1.56, fill=0.55, stroke=WH, sw=5)                   # grip
    d.rect(220, -r, L - 220, 2 * r, fill=0.18, stroke=WH, sw=7, r=r)                   # barrel and cap
    d.rect(470, -r - 3, 26, 2 * r + 6, fill=0.85)                                      # cap band
    d.rect(530, -r - 16, 250, 20, fill=0.85, stroke=WH, sw=4, r=10)                    # clip
    d.line(250, -r * 0.45, L - 40, -r * 0.45, 0.5, 6)                                  # highlight
    d.pop()


def receipt_edge(x0, x1, y, n, amp, down=True):
    """Zigzag tear along y from x0 to x1."""
    pts = []
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        pts.append((xx, y + (amp if (i % 2) else 0) * (1 if down else -1)))
    return pts


# ------------------------------------------------------------------ pictures

def e01(d):
    """A tall antique mercury barometer, its column sunk almost to the bottom of the glass."""
    cx = 960
    bw = 400
    x0, x1 = cx - bw / 2, cx + bw / 2
    p = skia.Path()                                                       # the board: arched hood, long case, round cistern cover
    p.moveTo(x0, 250)
    p.cubicTo(x0, 70, x1, 70, x1, 250)
    p.lineTo(x1 - 40, 280)
    p.lineTo(x1 - 40, 840)
    p.cubicTo(x1 + 30, 880, x1 + 20, 1010, cx, 1010)
    p.cubicTo(x0 - 20, 1010, x0 - 30, 880, x0 + 40, 840)
    p.lineTo(x0 + 40, 280)
    p.close()
    d.path(p, fill=0.34)
    d.hatch(p, 0.42, 5, 16, 90)
    d.path(p, stroke=WH, sw=9)
    d.circle(cx, 52, 26, fill=0.8, stroke=WH, sw=6)                      # finial
    d.rect(cx - 8, 70, 16, 40, fill=0.8)
    d.rect(cx - 140, 170, 280, 330, fill=0.88, stroke=WH, sw=7, r=10)     # the scale plate
    for i in range(16):                                                   # tick marks, no numerals
        ty = 200 + i * 18.5
        ln = 70 if i % 5 == 0 else 40
        d.line(cx - 34 - ln, ty, cx - 34, ty, 0.15, 5, butt=True)
        d.line(cx + 34, ty, cx + 34 + ln, ty, 0.15, 5, butt=True)
    d.rect(cx - 26, 140, 52, 830, fill=0.05, stroke=WH, sw=7, r=26)      # the glass tube, empty
    d.line(cx - 12, 170, cx - 12, 780, 0.35, 5)                           # glass glint
    d.glow(rrect_path(cx - 18, 850, 36, 110, 14), 0.8, 18)
    d.rect(cx - 16, 852, 32, 120, fill=WH, r=14)                         # the mercury, sunk to the bottom
    d.circle(cx, 960, 62, fill=WH, stroke=0.0, sw=6)                      # the cistern bulb
    d.circle(cx - 20, 942, 14, fill=0.75)
    d.poly([(cx + 34, 852), (cx + 90, 832), (cx + 90, 872)], fill=WH)     # vernier pointer at the mercury top
    d.line(cx + 90, 852, cx + 150, 852, WH, 8)


def e02(d):
    """The open ledger, blank, a fountain pen resting on it."""
    ledger(d, filled=False)
    pen(d, 1080, 760, -32)


def e03(d):
    """A plain wooden kitchen table at three-quarters with one unopened envelope on it."""
    A, B, C, Dp = (180, 560), (820, 330), (1740, 450), (1100, 740)        # left, back, right, front corners of the top
    th = 46

    def Q(u, v):                                                          # bilinear map onto the top (u: A->B side, v: A->D side)
        top = (A[0] + (B[0] - A[0]) * u, A[1] + (B[1] - A[1]) * u)
        bot = (Dp[0] + (C[0] - Dp[0]) * u, Dp[1] + (C[1] - Dp[1]) * u)
        return (top[0] + (bot[0] - top[0]) * v, top[1] + (bot[1] - top[1]) * v)
    legw = 46
    d.poly([(B[0] - legw / 2, B[1] + th), (B[0] + legw / 2, B[1] + th), (B[0] + legw / 2, 720), (B[0] - legw / 2, 720)], fill=0.22, stroke=0.6, sw=5)
    for (lx, ly), bottom, tone in (((A[0] + 40, A[1]), 900, 0.5), ((C[0] - 40, C[1]), 860, 0.42), ((Dp[0], Dp[1] - 8), 1040, 0.6)):
        d.poly([(lx - legw / 2, ly + th), (lx + legw / 2, ly + th), (lx + legw / 2 - 6, bottom), (lx - legw / 2 + 6, bottom)], fill=tone, stroke=WH, sw=6)
    d.poly([A, Dp, (Dp[0], Dp[1] + th), (A[0], A[1] + th)], fill=0.5, stroke=WH, sw=7)          # front-left edge
    d.poly([Dp, C, (C[0], C[1] + th), (Dp[0], Dp[1] + th)], fill=0.36, stroke=WH, sw=7)         # front-right edge
    top = mkpath([A, B, C, Dp])
    d.path(top, fill=0.62)
    d.clip(top)
    rnd = random.Random(3)
    for k in range(1, 9):                                                 # planks and grain run A->B direction
        v = k / 9
        d.poly([Q(0, v), Q(1, v)], stroke=0.36, sw=6, close=False)
        for g in range(3):
            vv = v - 1 / 9 * (0.25 + 0.25 * g) + rnd.uniform(-0.01, 0.01)
            pts = [Q(u / 10, vv + 0.006 * math.sin(u * 1.3 + g)) for u in range(11)]
            d.poly(pts, stroke=0.54, sw=3, close=False)
    d.unclip()
    d.path(top, stroke=WH, sw=8)
    u0, u1, v0, v1 = 0.36, 0.68, 0.3, 0.7                               # the envelope, lying flat
    shadow = [Q(u0 + 0.012, v0 + 0.03), Q(u1 + 0.012, v0 + 0.03), Q(u1 + 0.012, v1 + 0.03), Q(u0 + 0.012, v1 + 0.03)]
    d.poly(shadow, fill=0.4)
    env = [Q(u0, v0), Q(u1, v0), Q(u1, v1), Q(u0, v1)]
    d.poly(env, fill=0.96, stroke=WH, sw=6)
    mid = Q((u0 + u1) / 2, (v0 + v1) / 2 + 0.03)
    d.poly([Q(u0, v0), mid, Q(u0, v1)], stroke=0.55, sw=6, close=False)
    d.poly([Q(u1, v0), mid, Q(u1, v1)], stroke=0.55, sw=6, close=False)
    d.poly([Q(u0, v1), Q((u0 + u1) / 2, v0 + (v1 - v0) * 0.38), Q(u1, v1)], stroke=0.7, sw=5, close=False)


def e04(d):
    """A pay envelope standing upright, a few blank banknotes fanning out of the top."""
    ex, ey, ew, eh = 560, 470, 800, 520
    d.poly([(ex, ey), (ex + ew / 2, ey - 200), (ex + ew, ey)], fill=0.4, stroke=WH, sw=7)          # open flap behind
    pivot = (960, 820)
    for ang, tone in ((-26, 0.62), (-13, 0.74), (0, 0.86), (13, 0.74), (26, 0.62)):
        d.push(pivot[0], pivot[1], ang)
        nw, nh = 330, 700
        d.rect(-nw / 2 - 6, -nh - 6, nw + 12, nh + 12, fill=0.0)
        d.rect(-nw / 2, -nh, nw, nh, fill=tone, stroke=WH, sw=6, r=6)
        d.rect(-nw / 2 + 26, -nh + 26, nw - 52, nh - 52, stroke=tone - 0.28, sw=5, r=4)
        d.oval(0, -nh + 170, 80, 100, fill=tone - 0.16, stroke=tone - 0.32, sw=5)               # blank portrait oval
        d.circle(0, -nh + 400, 42, stroke=tone - 0.32, sw=5)
        d.pop()
    body = mkpath([(ex, ey), (ex + ew, ey), (ex + ew, ey + eh), (ex, ey + eh)])
    d.path(body, fill=0.8, stroke=WH, sw=8)
    d.poly([(ex, ey + eh), (ex + ew / 2, ey + eh * 0.42), (ex + ew, ey + eh)], stroke=0.55, sw=7, close=False)
    d.line(ex, ey, ex + ew * 0.32, ey + eh * 0.62, 0.62, 5)
    d.line(ex + ew, ey, ex + ew * 0.68, ey + eh * 0.62, 0.62, 5)
    d.rect(ex + 70, ey + 70, 240, 110, fill=0.3, stroke=0.55, sw=5, r=6)                         # small window
    d.line(ex - 40, ey + eh + 6, ex + ew + 40, ey + eh + 6, 0.5, 6)


def e05(d):
    """A staircase of coin stacks rising left to right, the last clearly the tallest."""
    counts = [3, 6, 9, 12, 15, 18, 28]
    base = 960
    xs = [300 + i * 220 for i in range(len(counts))]
    for x, n in zip(xs, counts):
        coin_stack(d, x, base, n, w=176, t=26, ry=32)
    d.line(150, base + 40, 1770, base + 40, 0.4, 6)


def e06(d):
    """A small coin beside a very large house key."""
    outline, hole = key_path(L=1250, R=220, hb=200, hole=78)
    d.push(380, 470, 8)
    sh = skia.Path(outline)
    sh.offset(18, 26)
    d.path(sh, fill=0.16)
    d.path(outline, fill=0.72)
    d.hatch(outline, 0.62, 5, 20, 30)
    d.path(outline, stroke=WH, sw=9)
    d.path(hole, fill=0.0, stroke=WH, sw=8)
    d.circle(0, 0, 220 * 0.82, stroke=0.9, sw=5)
    d.line(220 * 1.4, 18, 1150, 18, 0.45, 9)                              # the blade groove
    d.line(220 * 1.4, 48, 1100, 48, 0.85, 5)
    d.pop()
    cx, cy, r = 1300, 905, 66                                              # the coin
    d.circle(cx + 8, cy + 10, r, fill=0.16)
    d.circle(cx, cy, r, fill=0.82, stroke=WH, sw=6)
    d.circle(cx, cy, r * 0.74, stroke=0.5, sw=5)
    for i in range(36):
        a = 2 * math.pi * i / 36
        d.line(cx + math.cos(a) * r * 0.86, cy + math.sin(a) * r * 0.86, cx + math.cos(a) * r * 0.98, cy + math.sin(a) * r * 0.98, 0.55, 3)


def e07(d):
    """A vintage rotary telephone, handset lifted off the cradle, cord trailing."""
    cx = 820
    body = skia.Path()
    body.moveTo(cx - 380, 930)
    body.cubicTo(cx - 360, 640, cx - 280, 470, cx - 170, 450)
    body.lineTo(cx + 170, 450)
    body.cubicTo(cx + 280, 470, cx + 360, 640, cx + 380, 930)
    body.close()
    d.oval(cx, 932, 400, 40, fill=0.25, stroke=0.7, sw=6)
    d.path(body, fill=0.3)
    d.hatch(body, 0.38, 5, 20, 100)
    d.path(body, stroke=WH, sw=9)
    for sx in (-1, 1):                                                     # cradle prongs, empty
        d.poly([(cx + sx * 120, 455), (cx + sx * 150, 360), (cx + sx * 210, 360), (cx + sx * 250, 455)], fill=0.55, stroke=WH, sw=7)
    d.rect(cx - 150, 430, 300, 34, fill=0.45, stroke=WH, sw=6, r=12)
    dc, dr = (cx, 700), 190                                                # the dial
    d.circle(*dc, dr + 18, fill=0.15, stroke=WH, sw=7)
    d.circle(*dc, dr, fill=0.85, stroke=WH, sw=6)
    for i in range(10):
        a = math.radians(-60 - i * 27)
        d.circle(dc[0] + math.cos(a) * dr * 0.7, dc[1] + math.sin(a) * dr * 0.7, 34, fill=0.12, stroke=0.4, sw=4)
    d.circle(*dc, dr * 0.36, fill=0.6, stroke=0.3, sw=5)
    a = math.radians(40)
    d.line(dc[0] + math.cos(a) * dr * 0.62, dc[1] + math.sin(a) * dr * 0.62, dc[0] + math.cos(a) * dr * 1.04, dc[1] + math.sin(a) * dr * 1.04, 0.2, 14)
    hx, hy, ha = 1450, 300, -14                                            # the handset, lifted up and right
    d.push(hx, hy, ha)
    for sx in (-1, 1):
        cup = skia.Path()
        cup.moveTo(sx * 190, -10)
        cup.lineTo(sx * 330, -10)
        cup.cubicTo(sx * 360, 60, sx * 380, 120, sx * 370, 160)
        cup.lineTo(sx * 160, 160)
        cup.cubicTo(sx * 150, 110, sx * 170, 50, sx * 190, -10)
        cup.close()
        d.path(cup, fill=0.6, stroke=WH, sw=8)
        d.oval(sx * 265, 160, 105, 28, fill=0.22, stroke=WH, sw=7)
    hp = skia.Path()
    hp.moveTo(-320, 40)
    hp.cubicTo(-250, -110, 250, -110, 320, 40)
    hp.lineTo(320, -40)
    hp.cubicTo(250, -190, -250, -190, -320, -40)
    hp.close()
    d.path(hp, fill=0.5, stroke=WH, sw=9)
    d.curve([(-230, -90), (0, -170), (230, -90)], 0.85, 9)
    d.pop()
    ca = math.radians(ha)
    end = (hx + (-265) * math.cos(ca) - 185 * math.sin(ca), hy + (-265) * math.sin(ca) + 185 * math.cos(ca))
    start = (cx + 370, 880)
    pts = []
    N = 600
    for i in range(N + 1):                                                 # the coiled cord, sagging between them
        t = i / N
        bx = (1 - t) ** 3 * end[0] + 3 * (1 - t) ** 2 * t * (end[0] + 40) + 3 * (1 - t) * t ** 2 * (start[0] + 330) + t ** 3 * start[0]
        by = (1 - t) ** 3 * end[1] + 3 * (1 - t) ** 2 * t * (end[1] + 330) + 3 * (1 - t) * t ** 2 * (start[1] + 120) + t ** 3 * start[1]
        ph = t * 2 * math.pi * 22
        pts.append((bx + 30 * math.cos(ph), by + 24 * math.sin(ph)))
    d.poly(pts, stroke=0.0, sw=18, close=False)
    d.poly(pts, stroke=0.9, sw=8, close=False)


def e08(d):
    """A magnifying glass over a long curling blank till receipt."""
    rnd = random.Random(8)
    cl = []
    for i in range(60):                                                    # centreline of the strip, lying diagonally
        t = i / 59
        cl.append((330 + 1350 * t, 300 + 520 * t + 70 * math.sin(t * math.pi * 1.4)))
    left, right = ribbon(cl, 150)
    zig_end = []
    a, b = left[-1], right[-1]
    for k in range(13):
        f = k / 12
        off = 18 if k % 2 else 0
        zig_end.append((a[0] + (b[0] - a[0]) * f + off * 0.7, a[1] + (b[1] - a[1]) * f + off * 0.7))
    strip = mkpath(left + zig_end + right[::-1])
    sh = skia.Path(strip)
    sh.offset(16, 24)
    d.path(sh, fill=0.14)
    d.path(strip, fill=0.88, stroke=WH, sw=6)
    for i in range(1, 59, 2):                                              # gentle shading where it bends
        sv = 0.88 - 0.12 * abs(math.cos(i / 59 * math.pi * 1.4))
        d.poly([left[i], left[i + 1], right[i + 1], right[i]], fill=sv)
        d.poly([left[i - 1], left[i], right[i], right[i - 1]], fill=sv + 0.02)
    d.path(strip, stroke=WH, sw=6)
    c0 = cl[0]                                                             # the rolled start of the strip
    d.push(c0[0], c0[1], math.degrees(math.atan2(cl[1][1] - c0[1], cl[1][0] - c0[0])) + 90)
    d.rect(-150, -40, 300, 80, fill=0.66, stroke=WH, sw=6)
    d.oval(0, -40, 150, 34, fill=0.82, stroke=WH, sw=6)
    d.oval(0, -40, 60, 14, fill=0.3)
    d.oval(0, 40, 150, 34, fill=0.66, stroke=WH, sw=6)
    d.rect(-150, -40, 300, 80, fill=0.66)
    d.oval(0, -40, 150, 34, fill=0.84, stroke=WH, sw=6)
    d.oval(0, -40, 74, 16, fill=0.2, stroke=0.55, sw=4)
    d.line(-150, -40, -150, 40, WH, 6)
    d.line(150, -40, 150, 40, WH, 6)
    d.pop()
    lx, ly, lr = 1040, 520, 250                                            # the magnifier
    d.push(lx, ly, 42)
    d.rect(lr + 10, -34, 120, 68, fill=0.5, stroke=WH, sw=7)
    d.rect(lr + 120, -46, 420, 92, fill=0.18, stroke=WH, sw=8, r=40)
    d.line(lr + 160, -20, lr + 500, -20, 0.5, 8)
    d.pop()
    d.circle(lx + 14, ly + 20, lr + 30, fill=0.08)
    lens = circ_path(lx, ly, lr)
    d.clip(lens)
    d.c.drawColor(col(0.12))
    d.push(lx, ly, 0, 1.45)                                                # the strip, magnified inside the lens
    d.c.translate(-lx, -ly)
    d.path(strip, fill=0.97, stroke=WH, sw=5)
    d.pop()
    d.unclip()
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(lx - lr * 0.78, ly - lr * 0.78, lx + lr * 0.78, ly + lr * 0.78), 200, 60)
    d.path(p, None, WH, 14)
    d.circle(lx, ly, lr, stroke=WH, sw=34)
    d.circle(lx, ly, lr + 17, stroke=0.0, sw=6)
    d.circle(lx, ly, lr - 17, stroke=0.6, sw=5)


def e09(d):
    """Two thin white ribbons rising side by side like finish-line tapes, nearly level, one a hair ahead."""
    def tape(off, ahead, tone, seed):
        pts = []
        N = 140
        for i in range(N + 1):
            t = i / N
            x = 120 + (1500 + ahead) * t
            y = 930 - 720 * t + off + 46 * math.sin(t * math.pi * 3 + seed)
            pts.append((x, y))
        hw = lambda i: 30 * abs(math.cos(i / N * math.pi * 4.2 + seed)) + 6
        left, right = ribbon(pts, hw)
        for i in range(N):                                                 # twist: the back of the tape is darker
            front = math.cos(i / N * math.pi * 4.2 + seed) > 0
            d.poly([left[i], left[i + 1], right[i + 1], right[i]], fill=tone if front else tone * 0.55)
        d.poly(left, stroke=WH, sw=4, close=False)
        d.poly(right, stroke=WH, sw=4, close=False)
        tip = pts[-1]
        a = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
        nx, ny = -math.sin(a), math.cos(a)
        d.poly([(left[-1][0] - nx * 6, left[-1][1] - ny * 6), (tip[0] + math.cos(a) * 70 + nx * 40, tip[1] + math.sin(a) * 70 + ny * 40),
                (tip[0] + math.cos(a) * 30, tip[1] + math.sin(a) * 30),
                (tip[0] + math.cos(a) * 70 - nx * 40, tip[1] + math.sin(a) * 70 - ny * 40), (right[-1][0] + nx * 6, right[-1][1] + ny * 6)],
               fill=tone, stroke=WH, sw=4)
        return tip
    for i in range(14):                                                    # the finish line, dashed
        d.line(1640, 70 + i * 70, 1640, 70 + i * 70 + 36, 0.4, 8, butt=True)
    tape(60, 0, 0.62, 0.9)
    tape(-60, 34, 0.95, 0.4)


def e10(d):
    """A classic two-pan balance scale tipped very slightly to one side."""
    cx, py = 960, 250
    d.poly([(cx - 330, 980), (cx + 330, 980), (cx + 250, 920), (cx - 250, 920)], fill=0.55, stroke=WH, sw=8)   # base
    d.rect(cx - 160, 880, 320, 44, fill=0.7, stroke=WH, sw=7)
    pillar = mkpath([(cx - 30, 880), (cx - 18, py + 20), (cx + 18, py + 20), (cx + 30, 880)])
    d.path(pillar, fill=0.62, stroke=WH, sw=7)
    ang = math.radians(4.0)
    L = 600
    ends = []
    for sx in (-1, 1):
        ends.append((cx + sx * L * math.cos(ang), py + sx * L * math.sin(ang)))
    d.push(cx, py, 4.0)
    beam = mkpath([(-L, -10), (-60, -26), (60, -26), (L, -10), (L, 10), (60, 26), (-60, 26), (-L, 10)])
    d.path(beam, fill=0.85, stroke=WH, sw=7)
    d.circle(-L, 0, 18, fill=WH)
    d.circle(L, 0, 18, fill=WH)
    d.pop()
    d.poly([(cx - 40, py - 50), (cx, py - 130), (cx + 40, py - 50)], fill=0.85, stroke=WH, sw=6)               # pointer
    d.circle(cx, py, 34, fill=WH, stroke=0.0, sw=6)
    for (ex, ey) in ends:                                                   # pans on three chains
        pan_y = ey + 430
        for dx in (-210, 0, 210):
            d.line(ex, ey, ex + dx, pan_y, 0.75, 5)
        pan = skia.Path()
        pan.moveTo(ex - 250, pan_y)
        pan.cubicTo(ex - 200, pan_y + 110, ex + 200, pan_y + 110, ex + 250, pan_y)
        pan.close()
        d.path(pan, fill=0.7, stroke=WH, sw=8)
        d.oval(ex, pan_y, 250, 34, fill=0.45, stroke=WH, sw=7)


def e11(d):
    """An overflowing wire shopping basket: bread, a milk bottle, eggs and a light bulb."""
    top_y, bot_y = 560, 960
    tl, tr, bl, br = 420, 1500, 520, 1400
    for sx, x0 in ((-1, 640), (1, 1280)):                                    # handles behind
        p = skia.Path()
        p.moveTo(x0 - 110, top_y + 10)
        p.cubicTo(x0 - 110, top_y - 300, x0 + 110, top_y - 300, x0 + 110, top_y + 10)
        d.path(p, None, 0.0, 30)
        d.path(p, None, 0.72, 16)
    d.push(1000, 420, -28)                                                  # the loaf, lying back across the basket
    loaf = rrect_path(-330, -95, 660, 190, 95)
    d.path(loaf, fill=0.64)
    d.hatch(loaf, 0.54, 4, 16, 0)
    d.path(loaf, stroke=WH, sw=8)
    for k in range(-2, 3):
        d.curve([(k * 110 - 34, -70), (k * 110, 0), (k * 110 - 34, 70)], 0.9, 9)
    d.pop()
    bx = 700                                                                # the milk bottle
    bottle = skia.Path()
    bottle.moveTo(bx - 90, top_y + 60)
    bottle.lineTo(bx - 90, 330)
    bottle.cubicTo(bx - 90, 260, bx - 44, 240, bx - 44, 190)
    bottle.lineTo(bx - 44, 130)
    bottle.lineTo(bx + 44, 130)
    bottle.lineTo(bx + 44, 190)
    bottle.cubicTo(bx + 44, 240, bx + 90, 260, bx + 90, 330)
    bottle.lineTo(bx + 90, top_y + 60)
    bottle.close()
    d.path(bottle, fill=0.95, stroke=WH, sw=8)
    d.rect(bx - 54, 100, 108, 46, fill=0.5, stroke=WH, sw=6, r=10)
    d.line(bx - 56, 320, bx - 56, top_y, 0.75, 10)
    lbx, lby = 1300, 360                                                    # the light bulb
    d.push(lbx, lby, 18)
    bulb = skia.Path()
    bulb.moveTo(-50, 110)
    bulb.cubicTo(-60, 60, -130, 20, -130, -60)
    bulb.cubicTo(-130, -150, -60, -200, 0, -200)
    bulb.cubicTo(60, -200, 130, -150, 130, -60)
    bulb.cubicTo(130, 20, 60, 60, 50, 110)
    bulb.close()
    d.glow(bulb, 0.5, 30)
    d.path(bulb, fill=0.82, stroke=WH, sw=8)
    d.poly([(-30, 90), (-20, -40), (0, -10), (20, -40), (30, 90)], stroke=0.3, sw=5, close=False)
    for k in range(4):
        d.rect(-52 + k * 2, 110 + k * 26, 104 - k * 4, 22, fill=0.5, stroke=WH, sw=4, r=6)
    d.pop()
    for ex, ey, a in ((900, 560, -10), (1040, 540, 8), (1150, 570, 22), (980, 600, 0)):   # eggs sitting at the rim
        d.push(ex, ey, a)
        d.oval(0, 0, 58, 76, fill=0.97, stroke=0.0, sw=6)
        d.oval(-16, -22, 14, 22, fill=WH)
        d.pop()
    face = mkpath([(tl, top_y), (tr, top_y), (br, bot_y), (bl, bot_y)])     # the wire front
    d.path(face, fill=0.1)
    d.clip(face)
    for k in range(-20, 40):
        x = tl + k * 44
        d.line(x, top_y, x - 30, bot_y, 0.72, 6)
    for k in range(9):
        y = top_y + 28 + k * 44
        d.line(tl, y, tr, y, 0.72, 6)
    d.unclip()
    d.path(face, stroke=WH, sw=12)
    d.line(tl - 20, top_y, tr + 20, top_y, WH, 20)


def e12(d):
    """A monthly wall calendar page, every square ticked, no numerals, one corner curling."""
    x, y, w, h = 400, 140, 1120, 840
    d.circle(960, 70, 22, stroke=0.7, sw=7)                                 # nail and hanging loop
    d.line(960, 92, x + 140, y + 4, 0.6, 5)
    d.line(960, 92, x + w - 140, y + 4, 0.6, 5)
    cut = 210
    page = mkpath([(x, y), (x + w, y), (x + w, y + h - cut), (x + w - cut, y + h), (x, y + h)])
    d.path(page, fill=0.9, stroke=WH, sw=8)
    d.rect(x, y, w, 120, fill=0.4)                                          # blank header band
    for i in range(9):                                                      # spiral binding
        rx = x + 80 + i * (w - 160) / 8
        d.rect(rx - 10, y - 30, 20, 60, fill=0.1, stroke=WH, sw=5, r=10)
    gx0, gy0 = x + 50, y + 160
    cw, ch = (w - 100) / 7, (h - 200) / 5
    d.clip(page)
    for r in range(5):
        for c in range(7):
            cx0, cy0 = gx0 + c * cw, gy0 + r * ch
            d.rect(cx0 + 6, cy0 + 6, cw - 12, ch - 12, fill=0.78, stroke=0.55, sw=4)
            if cx0 + cw > x + w - cut + 20 and cy0 + ch > y + h - cut + 20 and (cx0 + cw - (x + w - cut)) + (cy0 + ch - (y + h - cut)) > cut:
                continue
            mx, my = cx0 + cw / 2, cy0 + ch / 2
            d.poly([(mx - 38, my), (mx - 10, my + 28), (mx + 42, my - 34)], stroke=0.1, sw=13, close=False)
    d.unclip()
    d.path(page, stroke=WH, sw=8)
    fold = mkpath([(x + w, y + h - cut), (x + w - cut, y + h), (x + w - cut - 30, y + h - cut - 30)])
    d.path(fold, fill=0.62, stroke=WH, sw=7)                                 # the curling corner
    d.hatch(fold, 0.5, 4, 14, 45)
    d.path(fold, stroke=WH, sw=7)
    d.poly([(x + w - cut - 30, y + h - cut - 30), (x + w - cut, y + h), (x + w - cut - 10, y + h + 18)], fill=0.2)


def e13(d):
    """A car speedometer with no numerals, its needle dropping back toward the low end."""
    cx, cy, R = 960, 560, 460
    d.circle(cx, cy, R + 26, fill=0.2, stroke=WH, sw=14)
    d.circle(cx, cy, R, fill=0.06, stroke=0.6, sw=6)

    def ang(t):
        return math.radians(135 + 270 * t)
    band = skia.Path()                                                      # the high end, hatched
    band.addArc(skia.Rect.MakeLTRB(cx - R * 0.86, cy - R * 0.86, cx + R * 0.86, cy + R * 0.86), 135 + 270 * 0.78, 270 * 0.22)
    d.path(band, None, 0.42, 48)
    for i in range(51):
        t = i / 50
        a = ang(t)
        major = i % 5 == 0
        r0 = R * (0.78 if major else 0.85)
        d.line(cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * R * 0.94, cy + math.sin(a) * R * 0.94,
               WH if major else 0.7, 12 if major else 5, butt=True)
    for t, v in ((0.62, 0.12), (0.45, 0.2), (0.3, 0.32)):                   # where the needle was
        a = ang(t)
        d.line(cx, cy, cx + math.cos(a) * R * 0.8, cy + math.sin(a) * R * 0.8, v, 18)
    sweep = skia.Path()
    sweep.addArc(skia.Rect.MakeLTRB(cx - R * 0.55, cy - R * 0.55, cx + R * 0.55, cy + R * 0.55), 135 + 270 * 0.14, 270 * 0.44)
    d.path(sweep, None, 0.35, 10)
    a = ang(0.1)
    nx, ny = math.cos(a), math.sin(a)
    px, py = -ny, nx
    d.poly([(cx - nx * 70 + px * 16, cy - ny * 70 + py * 16), (cx + nx * R * 0.84, cy + ny * R * 0.84), (cx - nx * 70 - px * 16, cy - ny * 70 - py * 16)],
           fill=WH)
    d.circle(cx, cy, 58, fill=0.75, stroke=WH, sw=8)
    d.circle(cx, cy, 20, fill=0.2)


def e14(d):
    """A flight of stone steps from the side, still climbing but each step shallower than the last."""
    rises = [200, 140, 100, 72, 52, 38, 28, 20, 14]
    tread = 160
    x0, base = 230, 960
    x, y = x0, base
    prof = [(x0, base)]
    for r in rises:
        y -= r
        prof.append((x, y))
        x += tread
        prof.append((x, y))
    xe = x + 60
    solid = mkpath(prof + [(xe, y), (xe, base)])
    d.path(solid, fill=0.42)
    d.hatch(solid, 0.5, 5, 22, 60)
    xx, yy = x0, base                                                       # block joints
    for i, r in enumerate(rises):
        yy -= r
        d.line(xx, yy, xx, base, 0.15, 7, butt=True)
        d.line(xx, yy + r * 0.0, xx + tread, yy, 0.15, 4, butt=True)
        xx += tread
    d.path(solid, stroke=0.7, sw=8)
    d.poly(prof + [(xe, y)], stroke=WH, sw=12, close=False)
    d.line(120, base, 1800, base, 0.6, 8)


def e15(d):
    """A crumpled blank till receipt uncurling on a dark surface, lit from one side."""
    d.oval(960, 610, 860, 330, fill=0.07)                                   # the surface pool of light
    rnd = random.Random(15)
    nu, nv = 18, 4
    L, Wd = 1300, 340
    ang = math.radians(-14)
    cx, cy = 960, 560
    verts = {}
    for i in range(nu + 1):
        for j in range(nv + 1):
            u = L * i / nu
            v = Wd * j / nv
            if 0 < j < nv:
                u += rnd.uniform(-22, 22)
            if 0 < i < nu:
                v += rnd.uniform(-20, 20)
            crumple = max(0.0, 1.0 - i / nu * 1.3)                          # left end still crumpled, right end flattening out
            z = rnd.uniform(-1, 1) * 70 * crumple + 18 * math.sin(i * 1.1)
            if i in (0, nu):
                v += (12 if j % 2 else -6)
            v += 60 * crumple * math.sin(i * 1.7)
            verts[i, j] = (u - L / 2, v - Wd / 2, z)

    def S(p):
        x, y, _ = p
        return (cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang))
    light = np.array([-0.75, -0.35, 0.56])
    light /= np.linalg.norm(light)
    shadow = [S((p[0] + 40, p[1] + 50, 0)) for p in [verts[i, 0] for i in range(nu + 1)] + [verts[i, nv] for i in range(nu, -1, -1)]]
    d.poly(shadow, fill=0.0)
    for i in range(nu):
        for j in range(nv):
            a, b, c, e = verts[i, j], verts[i + 1, j], verts[i + 1, j + 1], verts[i, j + 1]
            for tri in ((a, b, c), (a, c, e)):
                p0, p1, p2 = (np.array(t) for t in tri)
                n = np.cross(p1 - p0, p2 - p0)
                n = n / (np.linalg.norm(n) or 1)
                if n[2] < 0:
                    n = -n
                tone = 0.3 + 0.68 * max(0.0, float(np.dot(n, light)))
                d.poly([S(t) for t in tri], fill=tone, stroke=tone, sw=1.5)
    edge = [S(verts[i, 0]) for i in range(nu + 1)]
    edge += [S(verts[nu, j]) for j in range(nv + 1)]
    edge += [S(verts[i, nv]) for i in range(nu, -1, -1)]
    edge += [S(verts[0, j]) for j in range(nv, -1, -1)]
    d.poly(edge, stroke=WH, sw=5)
    zig = []
    for j in range(13):                                                     # torn ends
        f = j / 12
        x = L / 2 + (14 if j % 2 else 0)
        zig.append(S((x, -Wd / 2 + Wd * f + (verts[nu, 0][1] + Wd / 2) * (1 - f) + (verts[nu, nv][1] - Wd / 2) * f, 0)))
    d.poly(zig, stroke=WH, sw=5, close=False)


def e16(d):
    """A clipboard holding a blank survey form of empty checkboxes, a pencil on a string."""
    x, y, w, h = 600, 110, 680, 900
    board = rrect_path(x, y, w, h, 30)
    d.path(board, fill=0.38)
    d.hatch(board, 0.44, 4, 14, 80)
    d.path(board, stroke=WH, sw=8)
    d.rect(x + 50, y + 110, w - 100, h - 160, fill=0.93, stroke=WH, sw=5)    # the form
    for r in range(7):
        ry = y + 220 + r * 92
        for c in range(5):
            d.rect(x + 100 + c * 100, ry, 52, 52, fill=0.98, stroke=0.15, sw=7)
    d.rect(x + 100, y + 150, 300, 26, fill=0.72)                             # a blank title band
    clip = mkpath([(x + 180, y + 140), (x + 220, y + 30), (x + w - 220, y + 30), (x + w - 180, y + 140)])
    d.path(clip, fill=0.7, stroke=WH, sw=8)                                  # the clip
    d.rect(x + 250, y - 20, w - 500, 70, fill=0.55, stroke=WH, sw=7, r=30)
    d.circle(x + w / 2, y + 15, 16, fill=0.0)
    sx, sy = x + w - 190, y + 60                                             # the string and pencil
    px, py = 1560, 760
    s = skia.Path()
    s.moveTo(sx, sy)
    s.cubicTo(sx + 340, sy + 60, px - 60, py - 460, px - 40, py - 260)
    d.path(s, None, 0.8, 5)
    d.push(px - 40, py - 260, 98)
    d.rect(0, -26, 470, 52, fill=0.72, stroke=WH, sw=6)
    d.line(0, -9, 470, -9, 0.86, 4)
    d.line(0, 9, 470, 9, 0.56, 4)
    d.rect(-50, -26, 50, 52, fill=0.5, stroke=WH, sw=6, r=6)
    d.rect(-80, -24, 34, 48, fill=0.85, stroke=WH, sw=5, r=12)
    d.poly([(470, -26), (580, 0), (470, 26)], fill=0.86, stroke=WH, sw=6)
    d.poly([(548, -7), (580, 0), (548, 7)], fill=0.1)
    d.pop()


def e17(d):
    """A trophy cup standing next to an open, empty wallet (a moth leaving it)."""
    tx = 640
    cup = skia.Path()                                                        # the trophy
    cup.moveTo(tx - 230, 150)
    cup.lineTo(tx + 230, 150)
    cup.cubicTo(tx + 230, 420, tx + 120, 520, tx + 40, 540)
    cup.lineTo(tx - 40, 540)
    cup.cubicTo(tx - 120, 520, tx - 230, 420, tx - 230, 150)
    cup.close()
    for sx in (-1, 1):
        hp = skia.Path()
        hp.moveTo(tx + sx * 215, 200)
        hp.cubicTo(tx + sx * 380, 190, tx + sx * 380, 420, tx + sx * 150, 440)
        d.path(hp, None, 0.0, 40)
        d.path(hp, None, 0.78, 26)
    d.path(cup, fill=0.8)
    d.line(tx - 140, 190, tx - 110, 450, WH, 22)
    d.line(tx + 120, 190, tx + 100, 420, 0.6, 10)
    d.path(cup, stroke=WH, sw=8)
    d.oval(tx, 150, 230, 34, fill=0.35, stroke=WH, sw=8)
    d.rect(tx - 30, 540, 60, 150, fill=0.7, stroke=WH, sw=6)
    d.oval(tx, 700, 110, 26, fill=0.75, stroke=WH, sw=6)
    d.rect(tx - 170, 730, 340, 110, fill=0.45, stroke=WH, sw=8)
    d.rect(tx - 210, 840, 420, 90, fill=0.6, stroke=WH, sw=8)
    d.rect(tx - 110, 760, 220, 50, fill=0.3)
    wx, wy, ww, wh = 1350, 690, 800, 470                                     # the wallet, opened flat, empty
    outer = rrect_path(wx - ww / 2, wy - wh / 2, ww, wh, 46)
    sh = skia.Path(outer)
    sh.offset(16, 22)
    d.path(sh, fill=0.12)
    d.path(outer, fill=0.4)
    d.hatch(outer, 0.46, 4, 14, 30)
    d.path(outer, stroke=WH, sw=9)
    inset = rrect_path(wx - ww / 2 + 22, wy - wh / 2 + 22, ww - 44, wh - 44, 30)
    stitch = skia.Paint(AntiAlias=True, Color=col(0.85), Style=skia.Paint.kStroke_Style, StrokeWidth=5,
                        PathEffect=skia.DashPathEffect.Make([22, 14], 0))
    d.c.drawPath(inset, stitch)
    d.line(wx, wy - wh / 2 + 8, wx, wy + wh / 2 - 8, 0.15, 12)               # the fold
    d.line(wx + 8, wy - wh / 2 + 8, wx + 8, wy + wh / 2 - 8, 0.6, 4)
    for k in range(3):                                                       # empty card slots, left half
        yy = wy - wh / 2 + 90 + k * 95
        slot = skia.Path()
        slot.moveTo(wx - ww / 2 + 50, yy)
        slot.quadTo(wx - ww / 4, yy - 26, wx - 40, yy)
        slot.lineTo(wx - 40, wy + wh / 2 - 50)
        slot.lineTo(wx - ww / 2 + 50, wy + wh / 2 - 50)
        slot.close()
        d.path(slot, fill=0.3 + 0.08 * k, stroke=0.9, sw=5)
    gap = rrect_path(wx + 40, wy - wh / 2 + 50, ww / 2 - 90, 70, 20)          # the note pocket gaping open, nothing inside
    d.path(gap, fill=0.0, stroke=0.9, sw=6)
    pocket = mkpath([(wx + 40, wy - wh / 2 + 95), (wx + ww / 2 - 50, wy - wh / 2 + 95), (wx + ww / 2 - 50, wy + wh / 2 - 50), (wx + 40, wy + wh / 2 - 50)])
    d.path(pocket, fill=0.5, stroke=0.9, sw=6)
    d.rect(wx + 90, wy - 20, ww / 2 - 190, 150, fill=0.04, stroke=0.9, sw=6, r=12)   # empty ID window
    mx, my = 1530, 290                                                        # the moth
    for sx in (-1, 1):
        wing = skia.Path()
        wing.moveTo(mx, my)
        wing.cubicTo(mx + sx * 60, my - 110, mx + sx * 170, my - 80, mx + sx * 150, my - 10)
        wing.cubicTo(mx + sx * 140, my + 30, mx + sx * 60, my + 30, mx, my + 10)
        d.path(wing, fill=0.75, stroke=WH, sw=5)
        wing2 = skia.Path()
        wing2.moveTo(mx, my + 10)
        wing2.cubicTo(mx + sx * 70, my + 30, mx + sx * 110, my + 80, mx + sx * 60, my + 100)
        wing2.cubicTo(mx + sx * 30, my + 100, mx, my + 60, mx, my + 20)
        d.path(wing2, fill=0.6, stroke=WH, sw=5)
    d.oval(mx, my + 30, 14, 60, fill=0.9)
    d.curve([(mx - 4, my - 20), (mx - 20, my - 70), (mx - 50, my - 90)], 0.9, 4)
    d.curve([(mx + 4, my - 20), (mx + 20, my - 70), (mx + 50, my - 90)], 0.9, 4)
    for k, (dx, dy) in enumerate(((-50, 140), (-90, 210), (-120, 290))):
        d.circle(mx + dx, my + dy, 9 - k * 2, fill=0.5)


def e18(d):
    """A blank supermarket price tag on a string, a second smaller tag hidden behind it."""
    def tag(cx, cy, ang, w, h, tone):
        d.push(cx, cy, ang)
        p = mkpath([(-w / 2 + h * 0.42, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2 + h * 0.42, h / 2), (-w / 2, 0)])
        sh = skia.Path(p)
        sh.offset(16, 22)
        d.path(sh, fill=0.0)
        d.path(p, fill=tone)
        d.rect(-w / 2 + h * 0.62, -h / 2 + 40, w - h * 0.62 - 50, h - 80, stroke=tone - 0.2, sw=6, r=14)
        d.path(p, stroke=WH, sw=8)
        hx = -w / 2 + h * 0.3
        d.circle(hx, 0, h * 0.12, fill=0.7, stroke=WH, sw=5)
        d.circle(hx, 0, h * 0.06, fill=0.0)
        d.pop()
        a = math.radians(ang)
        return (cx + math.cos(a) * hx, cy + math.sin(a) * hx)
    h2 = tag(1150, 420, -32, 640, 330, 0.48)
    s = skia.Path()
    s.moveTo(*h2)
    s.cubicTo(h2[0] - 200, h2[1] - 150, 600, 160, 420, 40)
    d.path(s, None, 0.55, 6)
    h1 = tag(1000, 620, -12, 1080, 520, 0.9)
    s = skia.Path()
    s.moveTo(*h1)
    s.cubicTo(h1[0] - 260, h1[1] - 40, 160, 480, 300, 260)
    s.cubicTo(380, 130, 260, 60, 160, 20)
    d.path(s, None, WH, 8)


def e19(d):
    """A stack of loose academic papers held by a bulldog clip, top sheet blank."""
    cx, cy = 960, 680
    sw_, sh_ = 700, 740
    for k in range(9, 0, -1):                                                # the stack's edges fanning out
        d.push(cx + k * 7, cy + k * 6, -4 + k * 1.1)
        d.rect(-sw_ / 2, -sh_ / 2, sw_, sh_, fill=0.42 + 0.03 * (9 - k), stroke=0.75, sw=4)
        d.pop()
    d.push(cx, cy, -4)
    d.rect(-sw_ / 2, -sh_ / 2, sw_, sh_, fill=0.94, stroke=WH, sw=7)         # top sheet, blank
    d.rect(-sw_ / 2 + 4, sh_ / 2 - 120, sw_ - 8, 116, fill=0.88)
    for sx in (-1, 1):                                                       # wire levers standing up in a V
        p = skia.Path()
        p.moveTo(sx * 150, -sh_ / 2 - 10)
        p.lineTo(sx * 240, -sh_ / 2 - 190)
        p.lineTo(sx * 120, -sh_ / 2 - 225)
        p.lineTo(sx * 70, -sh_ / 2 - 10)
        d.path(p, None, 0.0, 30)
        d.path(p, None, 0.9, 14)
    clip = skia.Path()                                                       # the black clip body gripping the top edge
    clip.moveTo(-210, -sh_ / 2 - 40)
    clip.lineTo(210, -sh_ / 2 - 40)
    clip.lineTo(230, -sh_ / 2 + 130)
    clip.quadTo(0, -sh_ / 2 + 150, -230, -sh_ / 2 + 130)
    clip.close()
    d.path(clip, fill=0.1, stroke=WH, sw=8)
    d.line(-190, -sh_ / 2 - 10, 190, -sh_ / 2 - 10, 0.55, 10)
    d.line(-180, -sh_ / 2 + 40, -160, -sh_ / 2 + 110, 0.35, 8)
    for sx in (-1, 1):
        d.circle(sx * 110, -sh_ / 2 - 10, 14, fill=0.85)
    d.pop()


def e20(d):
    """A row of five identical houses, one with every window lit, four dark."""
    w, h = 300, 520
    gap = 46
    x0 = (W - (5 * w + 4 * gap)) / 2
    base = 860
    for i in range(5):
        lit = i == 3
        house_front(d, x0 + i * (w + gap), base, w, h, body=0.3, roof=0.4, win=0.06, lit=lit, door=False, chimney=True)
    d.line(80, base + 6, 1840, base + 6, 0.55, 8)


def e21(d):
    """An umbrella open in falling rain, dry ground beneath it, wet ground all around."""
    cx, top, rim = 960, 210, 520
    gy = 900
    d.rect(0, gy, W, H - gy, fill=0.12)
    rnd = random.Random(21)                                                  # wet ground: puddles and ripples
    for _ in range(30):
        x = rnd.uniform(60, 1860)
        if abs(x - cx) < 480:
            continue
        y = rnd.uniform(gy + 30, 1050)
        rw = rnd.uniform(60, 160)
        d.oval(x, y, rw, rw * 0.18, stroke=0.45, sw=5)
        d.line(x - rw * 0.5, y, x + rw * 0.4, y, 0.7, 4)
    d.poly([(cx - 420, gy), (cx + 420, gy), (cx + 460, 1080), (cx - 460, 1080)], fill=0.34)    # the dry patch
    d.line(0, gy, W, gy, 0.6, 6)
    dry = (cx - 560, top - 40, cx + 560, gy)
    for _ in range(420):                                                     # rain, missing the umbrella's shadow
        x, y = rnd.uniform(0, W + 100), rnd.uniform(-40, gy)
        if dry[0] + (gy - y) * 0.0 < x < dry[2] and y > top - 20:
            continue
        L = rnd.uniform(40, 80)
        d.line(x, y, x - L * 0.3, y + L, 0.62, 4)
    for _ in range(26):
        x = rnd.uniform(40, 1880)
        if abs(x - cx) < 470:
            continue
        d.curve([(x - 18, gy + 2), (x, gy - 22), (x + 18, gy + 2)], 0.75, 4)
    canopy = skia.Path()                                                     # the canopy, scalloped rim
    canopy.moveTo(cx - 560, rim)
    canopy.cubicTo(cx - 540, top - 10, cx + 540, top - 10, cx + 560, rim)
    n = 6
    for i in range(n):
        xa = cx + 560 - 1120 * i / n
        xb = cx + 560 - 1120 * (i + 1) / n
        canopy.quadTo((xa + xb) / 2, rim - 60, xb, rim)
    canopy.close()
    d.path(canopy, fill=0.6)
    for i in range(n):
        if i % 2:
            xa = cx - 560 + 1120 * i / n
            xb = cx - 560 + 1120 * (i + 1) / n
            seg = mkpath([(cx, top + 8), (xa, rim), (xb, rim)])
            d.clip(canopy)
            d.path(seg, fill=0.82)
            d.unclip()
    for i in range(n + 1):
        xa = cx - 560 + 1120 * i / n
        d.curve([(cx, top + 8), ((cx + xa) / 2, top + 30 + abs(xa - cx) * 0.05), (xa, rim)], 0.25, 5)
    d.path(canopy, stroke=WH, sw=8)
    d.rect(cx - 8, top - 70, 16, 80, fill=WH)
    d.line(cx, rim - 120, cx, 790, WH, 14, butt=True)                       # shaft and crook handle
    h = skia.Path()
    h.moveTo(cx, 790)
    h.cubicTo(cx, 880, cx - 110, 880, cx - 110, 810)
    d.path(h, None, WH, 22)


def e22(d):
    """A wooden ruler with its markings worn away, lying diagonally."""
    d.push(960, 540, -18)
    L, Wd = 1720, 230
    rule = rrect_path(-L / 2, -Wd / 2, L, Wd, 18)
    sh = skia.Path(rule)
    sh.offset(18, 26)
    d.path(sh, fill=0.13)
    d.path(rule, fill=0.6)
    rnd = random.Random(22)
    d.clip(rule)
    for k in range(18):                                                      # grain
        y = -Wd / 2 + 8 + k * 13 + rnd.uniform(-3, 3)
        pts = [(-L / 2 + i * 60, y + 5 * math.sin(i * 0.7 + k)) for i in range(int(L / 60) + 2)]
        d.poly(pts, stroke=0.5 + rnd.uniform(-0.05, 0.05), sw=3, close=False)
    for i in range(1, 90):                                                   # markings, mostly worn away
        x = -L / 2 + 20 + i * 19
        major = i % 10 == 0
        mid = i % 5 == 0
        ln = 90 if major else (62 if mid else 36)
        wear = 0.5 + 0.5 * math.sin(i * 0.23) + rnd.uniform(-0.4, 0.3)
        if wear > 0.85:
            continue
        tone = max(0.08, 0.5 - 0.45 * (0.85 - wear))
        d.line(x, -Wd / 2 + 22, x, -Wd / 2 + 22 + ln * rnd.uniform(0.55, 1.0), tone, 7 if major else 5, butt=True)
    for _ in range(40):                                                      # scuffs
        x = rnd.uniform(-L / 2, L / 2)
        y = rnd.uniform(-Wd / 2, Wd / 2)
        d.line(x, y, x + rnd.uniform(20, 80), y + rnd.uniform(-6, 6), 0.68, 3)
    d.unclip()
    d.rect(-L / 2 + 4, -Wd / 2 + 4, L - 8, 18, fill=0.85)                       # metal edge strip
    d.path(rule, stroke=WH, sw=8)
    d.line(-L / 2 + 30, Wd / 2 - 18, L / 2 - 30, Wd / 2 - 18, 0.42, 6)     # bevelled lower edge
    d.circle(L / 2 - 70, 30, 24, fill=0.0, stroke=WH, sw=6)                  # hanging hole
    d.pop()


def e23(d):
    """Two identical small houses side by side on a plain street, straight on."""
    w, h = 560, 720
    base = 840
    house_front(d, 340, base, w, h, body=0.46, roof=0.6, win=0.1)
    house_front(d, 1020, base, w, h, body=0.46, roof=0.6, win=0.1)
    d.rect(0, base, W, 34, fill=0.62, stroke=WH, sw=6)                      # kerb
    d.rect(0, base + 34, W, 210, fill=0.18)
    for i in range(8):
        d.rect(40 + i * 250, base + 130, 140, 18, fill=0.55)


def e24(d):
    """A heavy padlock closed around a house key."""
    cx = 960
    by, bw, bh = 520, 600, 470
    sh_c = (cx, by)
    so, si = 250, 160                                                        # shackle outer/inner half-widths
    shackle = skia.Path()
    shackle.moveTo(cx - (so + si) / 2, by + 20)
    shackle.lineTo(cx - (so + si) / 2, by - 140)
    shackle.arcTo(skia.Rect.MakeLTRB(cx - (so + si) / 2, by - 140 - (so + si) / 2, cx + (so + si) / 2, by - 140 + (so + si) / 2), 180, 180, False)
    shackle.lineTo(cx + (so + si) / 2, by + 20)
    d.path(shackle, None, 0.0, so - si + 24)
    d.path(shackle, None, 0.7, so - si)
    d.path(shackle, None, 0.88, 18)
    outline, hole = key_path(L=820, R=150, hb=130, hole=70)                  # key hangs on the shackle's left leg
    kx, ky = cx - (so + si) / 2, by - 220
    ka = 152
    d.push(kx, ky, ka)
    d.c.translate(150 * 0.25, 0)
    dd = skia.Path(outline)
    d.path(dd, fill=0.0, stroke=0.0, sw=22)
    d.path(outline, fill=0.86)
    d.path(outline, stroke=WH, sw=8)
    d.path(hole, fill=0.0, stroke=WH, sw=6)
    d.line(150 * 1.4, 12, 780, 12, 0.5, 8)
    d.pop()
    seg = skia.Path()                                                        # the shackle passes over the bow's near side
    seg.moveTo(kx, ky - 140)
    seg.lineTo(kx, ky + 30)
    d.path(seg, None, 0.0, so - si + 24, butt=True)
    d.path(seg, None, 0.7, so - si, butt=True)
    d.path(seg, None, 0.88, 18, butt=True)
    body = rrect_path(cx - bw / 2, by, bw, bh, 60)                           # the body
    d.path(body, fill=0.5)
    d.hatch(body, 0.58, 5, 22, 0)
    d.path(body, stroke=WH, sw=10)
    d.rect(cx - bw / 2 + 20, by + 22, bw - 40, 26, fill=0.8, r=12)
    d.circle(cx, by + 230, 46, fill=0.0, stroke=WH, sw=6)                     # keyhole
    d.poly([(cx - 22, by + 250), (cx + 22, by + 250), (cx + 34, by + 360), (cx - 34, by + 360)], fill=0.0, stroke=WH, sw=6)
    d.circle(cx, by + 230, 40, fill=0.0)


def e25(d):
    """A glass jar with a thin layer of coins at the bottom and a long empty space above."""
    cx = 960
    x0, x1 = cx - 300, cx + 300
    jar = skia.Path()
    jar.moveTo(cx - 190, 170)
    jar.lineTo(cx - 190, 220)
    jar.cubicTo(cx - 190, 260, x0, 250, x0, 330)
    jar.lineTo(x0, 930)
    jar.cubicTo(x0, 990, x0 + 40, 1000, cx, 1000)
    jar.cubicTo(x1 - 40, 1000, x1, 990, x1, 930)
    jar.lineTo(x1, 330)
    jar.cubicTo(x1, 250, cx + 190, 260, cx + 190, 220)
    jar.lineTo(cx + 190, 170)
    jar.close()
    d.path(jar, fill=0.08)
    d.clip(jar)                                                              # a thin layer of coins
    rnd = random.Random(25)
    for layer in range(3):
        y = 975 - layer * 26
        n = 8 - layer
        for k in range(n):
            x = x0 + 40 + (k + 0.5 * (layer % 2)) * (600 - 80) / 7 + rnd.uniform(-14, 14)
            tilt = rnd.uniform(-10, 10)
            d.push(x, y + rnd.uniform(-6, 6), tilt)
            d.oval(0, 0, 66, 18, fill=0.6, stroke=WH, sw=4)
            d.oval(0, -5, 66, 16, fill=0.86, stroke=WH, sw=4)
            d.pop()
    d.unclip()
    d.line(x0 + 50, 360, x0 + 50, 880, 0.55, 18)                            # glass highlights
    d.line(x0 + 90, 400, x0 + 90, 640, 0.35, 8)
    d.line(x1 - 60, 380, x1 - 60, 900, 0.28, 10)
    d.path(jar, stroke=WH, sw=9)
    d.rect(cx - 220, 90, 440, 100, fill=0.62, stroke=WH, sw=8, r=14)          # the lid
    for k in range(1, 12):
        lx = cx - 220 + k * 440 / 12
        d.line(lx, 100, lx, 180, 0.4, 5, butt=True)
    d.rect(cx - 220, 90, 440, 100, stroke=WH, sw=8, r=14)


def e26(d):
    """A storm cloud with one bolt of lightning striking toward a small rooftop."""
    d.c.save()                                                               # whole scene scaled into the frame so the roof survives the engine's edge feather
    d.c.translate(960, 440)
    d.c.scale(0.8, 0.8)
    d.c.translate(-960, -480)
    e26_scene(d)
    d.c.restore()


def e26_scene(d):
    blobs = [(560, 380, 170), (760, 290, 210), (1000, 250, 240), (1240, 300, 200), (1420, 390, 150),
             (700, 450, 170), (960, 460, 190), (1220, 460, 170)]
    cloud = union([circ_path(x, y, r) for x, y, r in blobs] + [mkpath([(470, 470), (1500, 470), (1500, 560), (470, 560)])])
    d.path(cloud, fill=0.42)
    d.clip(cloud)
    for x, y, r in blobs:                                                    # lit tops
        d.circle(x - r * 0.15, y - r * 0.2, r * 0.8, fill=0.62)
    d.rect(400, 470, 1200, 200, fill=0.24)
    d.hatch(mkpath([(400, 470), (1600, 470), (1600, 680), (400, 680)]), 0.16, 6, 18, 0)
    d.unclip()
    d.path(cloud, stroke=WH, sw=8)
    bolt = mkpath([(1000, 540), (1090, 540), (1030, 680), (1100, 680), (990, 830), (1040, 830), (930, 960),
                   (960, 850), (900, 850), (960, 720), (900, 720)])
    d.glow(bolt, 0.9, 40)
    d.path(bolt, fill=WH)
    rx, ry = 930, 990                                                         # a small rooftop below
    d.rect(rx + 70, ry - 120, 34, 70, fill=0.4, stroke=WH, sw=5)
    d.rect(rx - 150, 1080, 300, 110, fill=0.3, stroke=WH, sw=7)                     # the wall under it
    d.rect(rx - 100, 1100, 60, 50, fill=0.06, stroke=0.7, sw=5)
    d.rect(rx + 40, 1100, 60, 50, fill=0.06, stroke=0.7, sw=5)
    d.poly([(rx - 190, 1080), (rx, ry - 30), (rx + 190, 1080)], fill=0.38, stroke=WH, sw=7)
    rnd = random.Random(26)
    for _ in range(70):                                                       # rain from the cloud
        x, y = rnd.uniform(520, 1440), rnd.uniform(600, 1060)
        if 840 < x < 1120:
            continue
        d.line(x, y, x - 10, y + 44, 0.45, 4)


def e27(d):
    """A generic oil tanker side-on passing through a narrow channel between two dark headlands."""
    wl = 690
    d.rect(0, wl, W, H - wl, fill=0.1)
    far = mkpath([(980, wl), (1150, 520), (1330, 430), (1520, 400), (1700, 450), (1920, 380), (1920, wl)])
    d.path(far, fill=0.2)
    d.hatch(far, 0.27, 4, 16, 30)
    d.poly([(980, wl), (1150, 520), (1330, 430), (1520, 400), (1700, 450), (1920, 380)], stroke=0.55, sw=6, close=False)
    x0, x1 = 360, 1580                                                        # the hull
    deck = 560
    hull = mkpath([(x0, deck - 10), (x1 - 40, deck - 10), (x1 + 60, deck - 30), (x1 + 20, wl + 10), (x1 - 60, wl + 50), (x0 + 30, wl + 50), (x0, wl)])
    d.path(hull, fill=0.46)
    d.rect(x0, wl - 30, x1 + 30 - x0, 30, fill=0.3)
    d.path(hull, stroke=WH, sw=8)
    d.line(x0 + 10, deck + 4, x1 + 40, deck - 16, 0.85, 6)
    for k in range(10):                                                       # deck pipes and manifold
        px = 560 + k * 92
        d.line(px, deck - 10, px, deck - 46, 0.7, 5)
    d.line(500, deck - 40, 1500, deck - 40, 0.75, 8)
    d.line(500, deck - 24, 1500, deck - 24, 0.55, 5)
    d.rect(1000, deck - 90, 30, 80, fill=0.7)
    d.rect(1480, deck - 70, 40, 60, fill=0.65)                                # forecastle
    sx = 380                                                                  # the accommodation block at the stern
    d.rect(sx, deck - 230, 230, 220, fill=0.8, stroke=WH, sw=7)
    d.rect(sx + 20, deck - 300, 190, 70, fill=0.86, stroke=WH, sw=6)
    d.rect(sx - 30, deck - 312, 290, 18, fill=0.86, stroke=WH, sw=4)
    for r in range(3):
        for c in range(5):
            d.rect(sx + 22 + c * 40, deck - 210 + r * 60, 24, 24, fill=0.15)
    for c in range(5):
        d.rect(sx + 32 + c * 34, deck - 285, 22, 28, fill=0.15)
    d.poly([(sx + 120, deck - 312), (sx + 200, deck - 312), (sx + 190, deck - 420), (sx + 130, deck - 420)], fill=0.55, stroke=WH, sw=6)   # funnel
    d.line(sx + 170, deck - 420, sx + 170, deck - 470, 0.7, 6)
    d.line(sx + 110, deck - 312, sx + 110, deck - 440, 0.8, 5)
    d.waterline(0, W, wl, 0.75, 7, 6, 120)
    d.wavedashes(40, wl + 40, 1880, 1050, 40, seed=27, v=0.32, sw=6, ln=60)
    near = smooth([(-60, 1100), (-60, 470), (120, 430), (300, 560), (430, 720), (560, 900), (720, 1100)])
    d.path(near, fill=0.05)
    d.hatch(near, 0.2, 5, 18, 60)
    d.path(near, stroke=0.7, sw=8)


def e28(d):
    """A long row of identical upright blank dominoes, only the one in the exact centre lit."""
    n = 9
    fw, fh, dep = 150, 430, 40
    gap = 36
    total = n * fw + (n - 1) * gap
    x0 = (W - total) / 2
    base = 800
    centre = n // 2
    d.line(80, base, 1840, base, 0.32, 5)
    for i in range(n):
        x = x0 + i * (fw + gap)
        lit = i == centre
        face_v = WH if lit else 0.24
        side_v = 0.7 if lit else 0.14
        if lit:
            d.glow(rrect_path(x - 30, base - fh - 30, fw + 60, fh + 60, 20), 0.75, 50)
        d.poly([(x + fw, base - fh), (x + fw + dep, base - fh - dep * 0.6), (x + fw + dep, base - dep * 0.6), (x + fw, base)], fill=side_v, stroke=0.6 if not lit else WH, sw=4)
        d.poly([(x, base - fh), (x + dep, base - fh - dep * 0.6), (x + fw + dep, base - fh - dep * 0.6), (x + fw, base - fh)], fill=side_v + 0.08, stroke=0.6 if not lit else WH, sw=4)
        d.rect(x, base - fh, fw, fh, fill=face_v, stroke=0.6 if not lit else WH, sw=6, r=8)
        d.line(x + 16, base - fh / 2, x + fw - 16, base - fh / 2, 0.5 if lit else 0.42, 6)
        rv = 0.22 if lit else 0.06                                            # reflection on a glossy floor
        d.rect(x, base + 10, fw, fh * 0.42, fill=rv, r=8)


def e29(d):
    """A stepladder, its top rung glowing and the lower rungs in shadow."""
    top_y, bot_y = 140, 1000
    fl0, fl1 = 760, 1000                                                      # front legs at top
    fb0, fb1 = 600, 1170                                                      # front legs at bottom
    d.line(1010, top_y + 30, 1330, bot_y, 0.22, 26)                            # rear legs
    d.line(780, top_y + 30, 1210, bot_y - 30, 0.18, 22)
    d.line(1120, 600, 1250, 640, 0.16, 10)
    d.line(fl0, top_y + 40, fb0, bot_y, 0.42, 30, butt=True)                   # front stiles
    d.line(fl1, top_y + 40, fb1, bot_y, 0.42, 30, butt=True)
    steps = 6
    for s in range(1, steps + 1):
        t = s / (steps + 1)
        y = top_y + 40 + (bot_y - top_y - 40) * t
        xa = fl0 + (fb0 - fl0) * t
        xb = fl1 + (fb1 - fl1) * t
        v = 0.12 + 0.04 * (steps - s)
        d.rect(xa + 10, y - 16, xb - xa - 20, 32, fill=v, stroke=v + 0.12, sw=4)
    d.glow(rrect_path(fl0 - 50, top_y - 30, fl1 - fl0 + 100, 110, 20), 1.0, 46)   # the top
    d.rect(fl0 - 40, top_y, fl1 - fl0 + 80, 60, fill=WH, r=8)
    d.rect(fl0 - 40, top_y + 60, fl1 - fl0 + 80, 16, fill=0.7)
    d.line(fl0 + 30, top_y + 100, fl1 - 30, top_y + 100, 0.6, 10)


def e30(d):
    """A crowd of small faceless standing silhouettes seen from behind, one row lit, the rest fading into black."""
    rnd = random.Random(30)
    rows = 8
    lit_row = 2
    for r in range(rows - 1, -1, -1):
        s = 0.8 ** r
        hr = 62 * s
        base = 1080 - 110 - (1 - 0.8 ** r) / (1 - 0.8) * 150
        if r == lit_row:
            tone = WH
        elif r < lit_row:
            tone = 0.2
        else:
            tone = max(0.04, 0.42 - 0.09 * (r - lit_row))
        sp = hr * 3.6
        x = -hr * 2 + rnd.uniform(0, sp) + (sp / 2 if r % 2 else 0)
        while x < W + hr * 2:
            hx = x + rnd.uniform(-hr * 0.3, hr * 0.3)
            hy = base - hr * 5.2 + rnd.uniform(-hr * 0.4, hr * 0.4)
            body = skia.Path()
            body.moveTo(hx - hr * 1.8, hy + hr * 7)
            body.lineTo(hx - hr * 1.8, hy + hr * 2.4)
            body.cubicTo(hx - hr * 1.8, hy + hr * 1.3, hx - hr * 0.9, hy + hr * 1.1, hx - hr * 0.45, hy + hr * 0.9)
            body.lineTo(hx + hr * 0.45, hy + hr * 0.9)
            body.cubicTo(hx + hr * 0.9, hy + hr * 1.1, hx + hr * 1.8, hy + hr * 1.3, hx + hr * 1.8, hy + hr * 2.4)
            body.lineTo(hx + hr * 1.8, hy + hr * 7)
            body.close()
            fig = union([body, circ_path(hx, hy, hr)])
            if r == lit_row:
                d.glow(fig, 0.4, 22 * s + 8)
            d.path(fig, fill=tone, stroke=0.0, sw=max(3, 7 * s))
            x += sp * rnd.uniform(0.9, 1.1)


def e31(d):
    """The ledger from e02, both columns now filled with tally strokes and a heavy double rule at the bottom."""
    ledger(d, filled=True)


def e32(d):
    """A folded newspaper with blank columns and a pair of reading glasses resting on top."""
    d.push(940, 560, -8)
    w, h = 1240, 760
    for k in range(4, 0, -1):                                                 # folded thickness
        d.rect(-w / 2 + k * 6, -h / 2 + k * 7, w, h, fill=0.4 + 0.05 * k, stroke=0.7, sw=3)
    d.rect(-w / 2, -h / 2, w, h, fill=0.84, stroke=WH, sw=7)
    d.rect(-w / 2, h / 2 - 16, w, 16, fill=0.6)                              # the fold edge
    d.rect(-w / 2 + 50, -h / 2 + 40, w - 100, 96, fill=0.3)                   # blank masthead band
    d.line(-w / 2 + 50, -h / 2 + 156, w / 2 - 50, -h / 2 + 156, 0.3, 6)
    d.line(-w / 2 + 50, -h / 2 + 168, w / 2 - 50, -h / 2 + 168, 0.3, 3)
    cols = 5
    cw = (w - 100 - (cols - 1) * 30) / cols
    for c in range(cols):
        cx0 = -w / 2 + 50 + c * (cw + 30)
        if c in (1, 2):
            if c == 1:
                d.rect(cx0, -h / 2 + 200, 2 * cw + 30, 250, fill=0.5, stroke=0.35, sw=4)   # a blank picture box
            d.rect(cx0, -h / 2 + 480, cw, h - 540, fill=0.7)
        else:
            d.rect(cx0, -h / 2 + 200, cw, h - 260, fill=0.7)
        if c < cols - 1:
            d.line(cx0 + cw + 15, -h / 2 + 200, cx0 + cw + 15, h / 2 - 60, 0.5, 3)
    d.pop()
    gx, gy = 1000, 560                                                        # reading glasses, temples folded
    d.push(gx, gy, 10)
    for sx in (-1, 1):
        d.oval(sx * 200 + 16, 26, 170, 128, stroke=0.25, sw=16)
    d.line(-360, -40, 320, -70, 0.0, 34)
    d.line(-360, -40, 320, -70, 0.75, 14)
    d.line(-340, -30, 330, 20, 0.0, 30)
    d.line(-340, -30, 330, 20, 0.65, 12)
    for sx in (-1, 1):
        lens = skia.Path()
        lens.addOval(skia.Rect.MakeLTRB(sx * 200 - 170, -128, sx * 200 + 170, 128))
        d.path(lens, fill=0.93)
        d.clip(lens)
        d.line(sx * 200 - 120, 60, sx * 200 + 40, -110, WH, 30)
        d.line(sx * 200 - 60, 100, sx * 200 + 90, -60, 0.98, 10)
        d.unclip()
        d.path(lens, stroke=WH, sw=20)
    br = skia.Path()
    br.moveTo(-34, -40)
    br.quadTo(0, -90, 34, -40)
    d.path(br, None, WH, 18)
    d.pop()


def e33(d):
    """A chain of paper clips linked end to end, trailing off frame."""
    def clip_path():
        """A gem clip's wire: three straight runs joined by three U-turns."""
        p = skia.Path()
        p.moveTo(60, -20)
        p.lineTo(-140, -20)
        p.arcTo(skia.Rect.MakeLTRB(-160, -20, -120, 20), 270, -180, False)
        p.lineTo(150, 20)
        p.arcTo(skia.Rect.MakeLTRB(110, -60, 190, 20), 90, -180, False)
        p.lineTo(-160, -60)
        p.arcTo(skia.Rect.MakeLTRB(-220, -60, -100, 60), 270, -180, False)
        p.lineTo(100, 60)
        return p
    pts = []
    N = 7
    for i in range(N):
        t = i / (N - 1)
        x = -100 + t * 2080
        y = 860 - 620 * t + 70 * math.sin(t * math.pi * 1.2)
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        nxt = pts[min(i + 1, N - 1)]
        prv = pts[max(i - 1, 0)]
        ang = math.degrees(math.atan2(nxt[1] - prv[1], nxt[0] - prv[0]))
        d.push(x, y, ang + (8 if i % 2 else -8), 1.25)
        p = clip_path()
        d.path(p, None, 0.0, 26)
        d.path(p, None, 0.62 if i % 2 else 0.95, 13)
        d.path(p, None, WH if i % 2 == 0 else 0.85, 4)
        d.pop()


PICS = [e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20,
        e21, e22, e23, e24, e25, e26, e27, e28, e29, e30, e31, e32, e33]


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


def sheet(tiles, path, names, cols=4, tw=480):
    """Contact sheet; ids are printed in the grey margin above each tile, never inside the picture."""
    th = tw * 9 // 16
    lab = 30
    rows = -(-len(tiles) // cols)
    out = np.full((rows * (th + lab + 8) + 8, cols * (tw + 8) + 8), 60, np.uint8)
    for i, t in enumerate(tiles):
        r, c = divmod(i, cols)
        y0 = 8 + r * (th + lab + 8)
        x0 = 8 + c * (tw + 8)
        cv2.putText(out, names[i], (x0 + 4, y0 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 230, 2, cv2.LINE_AA)
        out[y0 + lab: y0 + lab + th, x0: x0 + tw] = cv2.resize(t, (tw, th), interpolation=cv2.INTER_AREA)
    cv2.imwrite(path, out)


def main():
    os.makedirs(OUT, exist_ok=True)
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    imgs, names = [], []
    for fn in PICS:
        if only and fn.__name__ not in only:
            continue
        d = D()
        fn(d)
        a = d.array()
        cv2.imwrite(os.path.join(OUT, fn.__name__ + ".png"), a)
        imgs.append(a)
        names.append(fn.__name__)
    if "--sheets" in sys.argv:
        out = sys.argv[sys.argv.index("--sheets") + 1]
        os.makedirs(out, exist_ok=True)
        sheet(imgs, os.path.join(out, "sheet_plain.png"), names, cols=4, tw=480)
        sheet(imgs, os.path.join(out, "sheet_phone.png"), names, cols=6, tw=320)
        sheet([cv2.resize(cv2.resize(a, (240, 135), interpolation=cv2.INTER_AREA), (W, H), interpolation=cv2.INTER_NEAREST) for a in imgs],
              os.path.join(out, "sheet_lowres.png"), names)
        sheet([(np.clip(engine_grey(a) * 1.15, 0, 1) * 255).astype(np.uint8) for a in imgs], os.path.join(out, "sheet_engine.png"), names)
    print("drew", len(imgs), "pictures into", OUT)


if __name__ == "__main__":
    main()
