"""THE MARGIN · the storyboard kit: a film's scenes are a list of beats, each starting on a line id and drawn with these
pieces (the ledger look's objects, now animated). A beat runs until the next beat starts, cross-fading over ~0.35 s.

    from ch2.kit import Board, Beat, number, statement, receipt, split, flow, stamp, floor_card, source
    BOARD = Board([Beat("paid", lambda c, b: number(c, b, "$8.2 billion", "AMERICAN EXPRESS → DELTA · 2025",
                                                    src="DELTA AIR LINES, FULL-YEAR 2025 RESULTS")), ...])
    def frame(c, t): BOARD.frame(c, t)
    def end_time(): return BOARD.end()

Each piece takes the beat (b): b.t (now), b.t0 (beat start), b.w(id, word) (when the narrator says a word), so
anything can land on a word. Times are the engine's (engine.tl), so a new voice re-times the whole film.
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402

W, H = tl.W, tl.H
CX, CY = W / 2, 470                                   # the page's centre, above the captions
ease, seg, lerp, clamp = mg.ease, mg.seg, mg.lerp, mg.clamp
PAPER, BRASS, RED, MUTED, INK, NAVY = L.PAPER, L.BRASS, L.RED, L.MUTED, L.INK, L.NAVY


# ---------------------------------------------------------------- beats
class Beat:
    def __init__(self, at, draw, until=None, lead=0.15):
        self.at, self.draw_fn, self.until, self.lead = at, draw, until, lead
        self.t0 = self.t1 = 0.0
        self.t = 0.0

    def w(self, line, word, k=0, end=False):
        try:
            return tl.word(line, word, k, end)
        except (KeyError, ValueError):
            return tl.ls(line)

    def k(self, a, d=0.5, curve="io"):
        """0 -> 1 over d seconds from time a."""
        return ease(seg(self.t, a, a + d), curve)


class Board:
    def __init__(self, beats, tail=1.0):
        self.beats, self.tail, self._ready = beats, tail, False

    def _resolve(self):
        for i, b in enumerate(self.beats):
            if isinstance(b.at, tuple):                                   # (line, word[, k]): the beat lands on a word
                b.t0 = b.w(*b.at) - b.lead
            else:
                b.t0 = (tl.ls(b.at) if isinstance(b.at, str) else float(b.at)) - b.lead
        for i, b in enumerate(self.beats):
            nxt = self.beats[i + 1].t0 if i + 1 < len(self.beats) else tl.L[-1]["end"] + self.tail
            b.t1 = tl.le(b.until) if b.until else nxt
        self._ready = True

    def frame(self, c, t):
        if not self._ready:
            self._resolve()
        for b in self.beats:
            if b.t0 - 0.05 <= t <= b.t1 + 0.4:
                a = ease(seg(t, b.t0 - 0.05, b.t0 + 0.3)) * (1 - ease(seg(t, b.t1 - 0.05, b.t1 + 0.35)))
                if a <= 0.001:
                    continue
                b.t = t
                if a < 0.999:
                    c.saveLayerAlpha(None, int(255 * a))
                else:
                    c.save()
                b.draw_fn(c, b)
                c.restore()

    def end(self):
        if not self._ready:
            self._resolve()
        return self.beats[-1].t1 + 0.5


# ---------------------------------------------------------------- type
def typed(c, b, s, x, y, t0, size=24, col=BRASS, align="center", track=0.12, face=None, cps=40.0, a=1.0):
    """Mono capitals typed on at cps characters a second, with a brief block cursor."""
    if b.t < t0 or not s:
        return
    n = min(len(s), int((b.t - t0) * cps) + 1)
    f = L.font(face or L.MONO_M, size)
    full = sum(f.measureText(ch) + track * size for ch in s) - track * size
    x0 = x - (full if align == "right" else full / 2 if align == "center" else 0)
    p = L.fill(col, a)
    xx = x0
    for ch in s[:n]:
        c.drawString(ch, xx, y, f, p)
        xx += f.measureText(ch) + track * size
    if n < len(s):
        c.drawRect(skia.Rect.MakeXYWH(xx + 2, y - size * 0.8, size * 0.55, size * 0.95), L.fill(col, 0.8 * a))


def serif(c, b, s, x, y, t0, size=64, col=PAPER, align="center", face=None, rise=18, d=0.5):
    """A serif line that rises into place and inks in."""
    k = b.k(t0, d)
    if k <= 0:
        return 0
    f = L.font(face or L.SERIF_M, size)
    return L.text(c, s, x, y + rise * (1 - k), f, L.fill(col, k), align)


def source(c, b, s, t0=None):
    if s:
        typed(c, b, "SOURCE · " + s, 190, H - 236, b.t0 + 0.6 if t0 is None else t0, 18, MUTED, "left", 0.06, L.MONO, 70)


# ---------------------------------------------------------------- pieces
def number(c, b, big, small="", src="", at=None, y=CY, size=170, col=PAPER, small_col=BRASS):
    """A figure: the big number rises and inks in, a brass rule draws under it, the small line types, the source
    types at the foot of the page."""
    t0 = b.t0 + 0.15 if at is None else at
    wbig = serif(c, b, big, CX, y, t0, size, col)
    k = b.k(t0 + 0.25, 0.6)
    if k > 0 and wbig:
        c.drawLine(CX - wbig / 2 * k, y + 40, CX + wbig / 2 * k, y + 40, L.stroke(BRASS, 2.2, 0.9))
    typed(c, b, small, CX, y + 100, t0 + 0.45, 28, small_col)
    source(c, b, src, t0 + 0.9)
    tl.ev(t0, "thock", b.t, CX)


def statement(c, b, lines, at=None, y=None, size=64, gap=1.25, cols=None, dt=0.45, face=None):
    """Lines of serif set in turn: each line (text, time or None) inks in at its time or after the one before."""
    t = b.t0 + 0.15 if at is None else at
    yy = (CY - (len(lines) - 1) * size * gap / 2 + size * 0.3) if y is None else y
    for i, ln in enumerate(lines):
        txt, ti = (ln if isinstance(ln, tuple) else (ln, None))
        t = ti if ti is not None else (t if i == 0 else t + dt)
        col = (cols[i] if cols else (BRASS if i == len(lines) - 1 and len(lines) > 1 else PAPER))
        serif(c, b, txt, CX, yy + i * size * gap, t, size, col, face=face)


def floor_card(c, b, roman, name, sub=""):
    serif(c, b, roman, 190, 430, b.t0 + 0.1, 120, BRASS, "left", L.SERIF_I)
    serif(c, b, name, 190, 570, b.t0 + 0.3, 120, PAPER, "left")
    typed(c, b, sub, 194, 640, b.t0 + 0.7, 26, MUTED, "left", 0.18)
    k = b.k(b.t0 + 0.4, 0.7)
    c.drawLine(190, 600, 190 + 900 * k, 600, L.stroke(BRASS, 1.5, 0.7))


def stamp(c, b, txt, x, y, at, col=RED, size=54, rot=-8):
    """A rubber stamp landing: it drops in large and settles, ink slightly uneven."""
    if b.t < at:
        return
    k = ease(seg(b.t, at, at + 0.22), "o")
    sc = lerp(1.6, 1.0, k)
    f = L.font(L.MONO_M, size)
    w = f.measureText(txt) + 0.12 * size * (len(txt) - 1)
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(sc, sc)
    a = clamp(k * 1.4)
    r = skia.Rect.MakeXYWH(-w / 2 - 22, -size * 0.95, w + 44, size * 1.35)
    c.drawRoundRect(r, 8, 8, L.stroke(col, 4.0, 0.9 * a))
    c.drawRoundRect(r.makeInset(7, 7), 5, 5, L.stroke(col, 1.5, 0.6 * a))
    L.text(c, txt, -w / 2, size * 0.18, f, L.fill(col, 0.92 * a), "left", track=0.12)
    c.restore()
    tl.ev(at, "thud", b.t, x)


def receipt(c, b, x0, y0, w, head, title, rows, at=None, dt=0.4, circle=None, times=None):
    """A till receipt: header, title, rows typed in turn (times: a time per row, else dt apart), one row's figure
    circled in brass ink."""
    t0 = b.t0 + 0.1 if at is None else at
    h = 110 + 56 * len(rows) + 60
    k = b.k(t0, 0.5, "o")
    if k <= 0:
        return
    hh = h * k
    path = skia.Path()
    path.moveTo(x0, y0)
    path.lineTo(x0 + w, y0)
    path.lineTo(x0 + w, y0 + hh)
    n = 14
    for i in range(n):
        path.lineTo(x0 + w - (i + 0.5) * w / n, y0 + hh + 16)
        path.lineTo(x0 + w - (i + 1) * w / n, y0 + hh)
    path.close()
    sh = skia.Paint(Color=L.col("#000000", 0.55), AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.save(); c.translate(10, 16); c.drawPath(path, sh); c.restore()
    c.drawPath(path, L.fill(PAPER))
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(x0, y0, w, hh + 20))
    typed(c, b, head, x0 + w / 2, y0 + 62, t0 + 0.2, 22, INK, "center", 0.12)
    dash = skia.Paint(Color=L.col(INK, 0.6), StrokeWidth=1.5, PathEffect=skia.DashPathEffect.Make([8, 6], 0))
    c.drawLine(x0 + 30, y0 + 90, x0 + w - 30, y0 + 90, dash)
    y = y0 + 150
    serif(c, b, title, x0 + 34, y, t0 + 0.3, 34, INK, "left", L.SERIF_B, rise=0)
    y += 56
    for i, (lab, val) in enumerate(rows):
        ti = times[i] if times and i < len(times) and times[i] is not None else t0 + 0.6 + dt * i
        if lab:
            typed(c, b, lab, x0 + 34, y, ti, 23, INK, "left", 0.04, L.MONO_M, 60)
        if val:
            bw = serif(c, b, val, x0 + w - 34, y, ti + 0.2, 34, INK, "right", L.SERIF_B, rise=0)
            if circle == i and bw:
                kc = b.k(ti + 0.5, 0.5)
                if kc > 0:
                    ring = skia.Path()
                    cx, cy, rx, ry = x0 + w - 34 - bw / 2, y - 12, bw / 2 + 26, 30
                    ring.addArc(skia.Rect.MakeXYWH(cx - rx, cy - ry, 2 * rx, 2 * ry), -100, 360 * kc)
                    c.save(); c.rotate(-4, cx, cy); c.drawPath(ring, L.stroke("#A57B2C", 3, 0.95)); c.restore()
        y += 56
    c.drawLine(x0 + 30, y0 + h - 40, x0 + w - 30, y0 + h - 40, dash)
    c.restore()


def split(c, b, title, parts, at=None, x0=190, y0=420, w=1540, h=210, total=10.0, callouts=(), src=""):
    """One amount cut into who gets what: parts = [(label, value, fill, ink)], growing left to right."""
    t0 = b.t0 + 0.15 if at is None else at
    serif(c, b, title, x0, 300, t0, 54, PAPER, "left", L.SERIF)
    x = x0
    for i, (name, v, bg, fg) in enumerate(parts):
        ti = t0 + 0.4 + 0.5 * i
        k = b.k(ti, 0.6)
        ww = w * v / total
        if k > 0:
            c.drawRect(skia.Rect.MakeXYWH(x, y0, ww * k, h), L.fill(bg))
            c.drawRect(skia.Rect.MakeXYWH(x, y0, ww * k, h), L.stroke(PAPER, 1.5, 0.7))
            if ww > 300 and total == 10.0:                                # money: the amount, then who gets it
                serif(c, b, f"${v:.2f}", x + 40, y0 + 120, ti + 0.3, 76, fg, "left", rise=0)
                typed(c, b, name, x + 44, y0 + 170, ti + 0.4, 22, fg, "left", 0.12)
            elif ww > 200:                                                # shares: the name, set to fit
                f = L.font(L.SERIF_M, 40)
                while f.getSize() > 18 and f.measureText(name) > ww - 60:
                    f = L.font(L.SERIF_M, f.getSize() - 2)
                L.text(c, name, x + 30, y0 + h / 2 + 14, f, L.fill(fg, b.k(ti + 0.3, 0.4)), "left")
        x += ww
    for (txt, cx, cy, ti) in callouts:
        typed(c, b, txt, cx, cy, ti, 28, BRASS, "center", 0.1)
    source(c, b, src, t0 + 1.2)


def node(c, b, x, y, w, h, title, sub, at):
    k = b.k(at, 0.45)
    if k <= 0:
        return
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2 + 12 * (1 - k), w, h), 6, 6)
    c.drawRRect(r, L.fill("#0F1622", 0.95 * k))
    c.drawRRect(r, L.stroke(PAPER, 2, 0.85 * k))
    L.text(c, title, x, y + 4, L.font(L.SERIF_M, 40), L.fill(PAPER, k), "center")
    typed(c, b, sub, x, y + 44, at + 0.2, 18, MUTED, "center", 0.12, L.MONO)


def _bez(pts, u):
    p0, p1, p2, p3 = [np.array(p, float) for p in pts]
    return (1 - u) ** 3 * p0 + 3 * (1 - u) ** 2 * u * p1 + 3 * (1 - u) * u * u * p2 + u ** 3 * p3


def arrow(c, b, pts, at, label="", col=PAPER, token="coin", lab_dy=-18, speed=0.45):
    """An arrow drawing itself along a curve, then tokens (coin = cash, ticket = miles/points) flowing along it."""
    k = b.k(at, 0.6)
    if k <= 0:
        return
    us = np.linspace(0, k, 40)
    poly = [_bez(pts, u) for u in us]
    path = skia.Path()
    path.moveTo(*poly[0])
    for p in poly[1:]:
        path.lineTo(*p)
    c.drawPath(path, L.stroke(col, 2.4, 0.9))
    if k >= 1:
        (x2, y2), (x3, y3) = pts[2], pts[3]
        ang = math.atan2(y3 - y2, x3 - x2)
        for d in (-0.45, 0.45):
            c.drawLine(x3, y3, x3 - 22 * math.cos(ang + d), y3 - 22 * math.sin(ang + d), L.stroke(col, 2.4, 0.9))
        if label:
            mx, my = _bez(pts, 0.5)
            typed(c, b, label, mx, my + lab_dy, at + 0.5, 22, BRASS, "center", 0.1)
        if token:
            for j in range(3):
                u = ((b.t - at) * speed + j / 3) % 1.0
                x, y = _bez(pts, u)
                (L.coin if token == "coin" else L.ticket)(c, x, y, 13 if token == "coin" else 11, 0.95)


# ---------------------------------------------------------------- icons (line work in paper ink)
def plane(c, cx, cy, s, a=1.0, col=PAPER):
    p = skia.Path()
    pts = [(-1.0, 0.0), (-0.75, -0.08), (0.1, -0.08), (0.45, -0.55), (0.6, -0.55), (0.42, -0.08), (0.85, -0.08), (1.0, -0.28),
           (1.1, -0.28), (1.0, 0.0), (1.1, 0.28), (1.0, 0.28), (0.85, 0.08), (0.42, 0.08), (0.6, 0.55), (0.45, 0.55), (0.1, 0.08),
           (-0.75, 0.08), (-1.0, 0.0)]
    p.moveTo(cx + pts[0][0] * s, cy + pts[0][1] * s)
    for x, y in pts[1:]:
        p.lineTo(cx + x * s, cy + y * s)
    c.drawPath(p, L.stroke(col, 2.2, a))


def card(c, cx, cy, w, a=1.0, col=PAPER, label=""):
    h = w * 0.63
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), w * 0.06, w * 0.06)
    c.drawRRect(r, L.fill("#121A27", 0.95 * a))
    c.drawRRect(r, L.stroke(col, 2.0, a))
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - w * 0.38, cy - h * 0.12, w * 0.16, h * 0.22), 4, 4, L.fill(BRASS, 0.9 * a))
    for i in range(4):
        c.drawLine(cx - w * 0.38 + i * w * 0.2, cy + h * 0.25, cx - w * 0.24 + i * w * 0.2, cy + h * 0.25, L.stroke(col, 2.0, 0.6 * a))
    if label:
        L.text(c, label, cx + w * 0.4, cy - h * 0.3, L.font(L.MONO_M, max(12, int(w * 0.07))), L.fill(BRASS, a), "right", track=0.1)


def bank(c, cx, cy, s, a=1.0, col=PAPER):
    p = L.stroke(col, 2.2, a)
    c.drawLine(cx - s, cy - 0.55 * s, cx, cy - s, p)
    c.drawLine(cx, cy - s, cx + s, cy - 0.55 * s, p)
    c.drawLine(cx - s, cy - 0.55 * s, cx + s, cy - 0.55 * s, p)
    for i in range(5):
        x = cx - 0.8 * s + i * 0.4 * s
        c.drawLine(x, cy - 0.45 * s, x, cy + 0.55 * s, p)
    c.drawLine(cx - 1.05 * s, cy + 0.6 * s, cx + 1.05 * s, cy + 0.6 * s, p)
    c.drawLine(cx - 1.15 * s, cy + 0.72 * s, cx + 1.15 * s, cy + 0.72 * s, p)


def coins(c, cx, cy, n, a=1.0, r=22, cols=10):
    """A pile of coins, n of them, stacked in columns from the left."""
    for i in range(n):
        col_i, row = i % cols, i // cols
        L.coin(c, cx + (col_i - (cols - 1) / 2) * r * 2.2, cy - row * r * 0.55, r, a)


def shop(c, cx, cy, s, a=1.0, col=PAPER, sign=""):
    """A roadside restaurant: a box, a door, a window band, a tall sign on a pole (generic, no logo)."""
    p = L.stroke(col, 2.2, a)
    c.drawRect(skia.Rect.MakeXYWH(cx - s, cy - 0.7 * s, 2 * s, 0.7 * s), p)
    c.drawRect(skia.Rect.MakeXYWH(cx - 0.18 * s, cy - 0.45 * s, 0.36 * s, 0.45 * s), p)
    c.drawLine(cx - s, cy - 0.55 * s, cx - 0.3 * s, cy - 0.55 * s, p)
    c.drawLine(cx + 0.3 * s, cy - 0.55 * s, cx + s, cy - 0.55 * s, p)
    c.drawLine(cx - 1.1 * s, cy - 0.7 * s, cx + 1.1 * s, cy - 0.7 * s, p)
    c.drawLine(cx + 1.35 * s, cy, cx + 1.35 * s, cy - 1.3 * s, p)
    c.drawRect(skia.Rect.MakeXYWH(cx + 1.05 * s, cy - 1.65 * s, 0.6 * s, 0.35 * s), p)
    if sign:
        L.text(c, sign, cx + 1.35 * s, cy - 1.42 * s, L.font(L.MONO_M, max(12, int(s * 0.14))), L.fill(BRASS, a), "center")
    c.drawLine(cx - 1.6 * s, cy, cx + 1.8 * s, cy, L.stroke(col, 1.5, 0.6 * a))


def land(c, cx, cy, s, a=1.0, col=BRASS):
    """A plot of land: a hatched parallelogram with corner pegs."""
    pts = [(cx - s, cy), (cx - 0.6 * s, cy - 0.45 * s), (cx + s, cy - 0.45 * s), (cx + 0.6 * s, cy)]
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.drawPath(p, L.fill(col, 0.12 * a))
    c.drawPath(p, L.stroke(col, 2.0, 0.9 * a))
    for q in pts:
        c.drawCircle(q[0], q[1], 5, L.fill(col, a))


def warehouse(c, cx, cy, s, a=1.0, col=PAPER):
    p = L.stroke(col, 2.2, a)
    c.drawLine(cx - s, cy, cx - s, cy - 0.55 * s, p)
    c.drawLine(cx - s, cy - 0.55 * s, cx, cy - 0.8 * s, p)
    c.drawLine(cx, cy - 0.8 * s, cx + s, cy - 0.55 * s, p)
    c.drawLine(cx + s, cy - 0.55 * s, cx + s, cy, p)
    c.drawRect(skia.Rect.MakeXYWH(cx - 0.35 * s, cy - 0.38 * s, 0.7 * s, 0.38 * s), p)
    for i in range(1, 4):
        c.drawLine(cx - 0.35 * s, cy - 0.38 * s + i * 0.095 * s, cx + 0.35 * s, cy - 0.38 * s + i * 0.095 * s, L.stroke(col, 1.2, 0.6 * a))
    c.drawLine(cx - 1.3 * s, cy, cx + 1.3 * s, cy, L.stroke(col, 1.5, 0.6 * a))


def hotdog(c, cx, cy, s, a=1.0):
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - s, cy - 0.22 * s, 2 * s, 0.44 * s), 0.22 * s, 0.22 * s, L.stroke(PAPER, 2.2, a))
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 1.1 * s, cy - 0.1 * s, 2.2 * s, 0.2 * s), 0.1 * s, 0.1 * s, L.stroke(BRASS, 2.2, a))
    pts = [(cx - 0.8 * s + i * 0.2 * s, cy - 0.12 * s + (0.06 * s if i % 2 else -0.04 * s)) for i in range(9)]
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, L.stroke(BRASS, 1.6, 0.8 * a))


def cup(c, cx, cy, s, a=1.0):
    p = skia.Path()
    p.moveTo(cx - 0.4 * s, cy - 0.6 * s); p.lineTo(cx + 0.4 * s, cy - 0.6 * s); p.lineTo(cx + 0.3 * s, cy + 0.6 * s)
    p.lineTo(cx - 0.3 * s, cy + 0.6 * s); p.close()
    c.drawPath(p, L.stroke(PAPER, 2.2, a))
    c.drawLine(cx - 0.45 * s, cy - 0.6 * s, cx + 0.45 * s, cy - 0.6 * s, L.stroke(PAPER, 3, a))
    c.drawLine(cx + 0.1 * s, cy - 0.6 * s, cx + 0.25 * s, cy - 1.0 * s, L.stroke(BRASS, 2.2, a))


def chicken(c, cx, cy, s, a=1.0):
    """A roast chicken in its dome tray."""
    c.drawOval(skia.Rect.MakeXYWH(cx - 0.8 * s, cy - 0.5 * s, 1.6 * s, 0.9 * s), L.stroke(BRASS, 2.2, a))
    c.drawOval(skia.Rect.MakeXYWH(cx + 0.55 * s, cy - 0.3 * s, 0.45 * s, 0.25 * s), L.stroke(BRASS, 2.0, a))
    c.drawOval(skia.Rect.MakeXYWH(cx - 1.0 * s, cy - 0.3 * s, 0.45 * s, 0.25 * s), L.stroke(BRASS, 2.0, a))
    c.drawLine(cx - 1.2 * s, cy + 0.42 * s, cx + 1.2 * s, cy + 0.42 * s, L.stroke(PAPER, 2.2, a))
    arc = skia.Path()
    arc.addArc(skia.Rect.MakeXYWH(cx - 1.15 * s, cy - 1.0 * s, 2.3 * s, 2.8 * s), 180, 180)
    c.drawPath(arc, L.stroke(PAPER, 1.6, 0.6 * a))


def person(c, cx, cy, s, a=1.0, col=PAPER):
    """A simple standing person: head and shoulders, for 'you' and per-person shares."""
    c.drawCircle(cx, cy - 0.55 * s, 0.22 * s, L.stroke(col, 2.2, a))
    p = skia.Path()
    p.moveTo(cx - 0.45 * s, cy + 0.35 * s)
    p.cubicTo(cx - 0.45 * s, cy - 0.25 * s, cx + 0.45 * s, cy - 0.25 * s, cx + 0.45 * s, cy + 0.35 * s)
    c.drawPath(p, L.stroke(col, 2.2, a))
