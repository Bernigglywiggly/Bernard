"""Flash-game art kit for the talking stickman: wobbly ink pen ("line boil"), the rig, mouths, faces,
the chrome hat (flat Flash version of the one in character.py), arena / flat backgrounds, a 5x7 bitmap font,
impact frames, speed lines, SFX bursts and the HUD. Pure skia, no project imports.

Conventions (same as character.py): angles in degrees measured from straight down, + = towards screen right.
"""
import math
import random

import numpy as np
import skia

INK = "#111111"
PAPER = "#FFFFFF"
MOUTH_IN = "#5A1020"
TONGUE = "#FF6B81"
TURQ = "#3FE6D8"
IMPACT_FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"


# ---------------------------------------------------------------- colour / paint helpers
def hexc(h, a=1.0):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return skia.ColorSetARGB(int(255 * max(0.0, min(1.0, a))), r, g, b)


def shade(h, k):
    """k<1 darker, k>1 lighter."""
    h = h.lstrip("#")
    rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    if k <= 1:
        rgb = [int(v * k) for v in rgb]
    else:
        rgb = [int(v + (255 - v) * (k - 1)) for v in rgb]
    return "#%02X%02X%02X" % tuple(max(0, min(255, v)) for v in rgb)


def fill(col, a=1.0):
    return skia.Paint(AntiAlias=True, Color=hexc(col, a), Style=skia.Paint.kFill_Style)


def stroke(col, w, a=1.0):
    return skia.Paint(AntiAlias=True, Color=hexc(col, a), Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


def _dir(deg):
    a = math.radians(deg)
    return np.array([math.sin(a), math.cos(a)])


# ---------------------------------------------------------------- the wobbly pen (line boil)
class Pen:
    """Every stroke is subdivided and nudged by a deterministic jitter keyed on (drawing seed, stroke number),
    so each new drawing (12 per second) boils slightly, like hand-inked Flash frames."""

    def __init__(self, c, seed, amp=2.0, step=26.0, ink=INK, paper=PAPER, invert=False):
        self.c, self.seed, self.amp, self.step, self.k = c, seed, amp, step, 0
        self.ink, self.paper = (paper, ink) if invert else (ink, paper)

    def _rng(self):
        self.k += 1
        return random.Random(self.seed * 7919 + self.k * 104729)

    def _jitter(self, pts, closed=False):
        rng = self._rng()
        out = []
        n = len(pts)
        segs = n if closed else n - 1
        for i in range(segs):
            p0, p1 = np.asarray(pts[i], float), np.asarray(pts[(i + 1) % n], float)
            d = p1 - p0
            L = float(np.hypot(*d)) + 1e-6
            m = max(1, int(L / self.step))
            nrm = np.array([-d[1], d[0]]) / L
            for j in range(m):
                t = j / m
                q = p0 + d * t + nrm * rng.uniform(-1, 1) * self.amp + np.array([rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)]) * self.amp * 0.6
                out.append(q)
        if not closed:
            out.append(np.asarray(pts[-1], float) + np.array([rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)]) * self.amp)
        return out

    @staticmethod
    def _smooth_path(q, closed):
        path = skia.Path()
        if len(q) < 3:
            path.moveTo(*q[0])
            for p in q[1:]:
                path.lineTo(*p)
            if closed:
                path.close()
            return path
        if closed:
            mids = [(q[i] + q[(i + 1) % len(q)]) / 2 for i in range(len(q))]
            path.moveTo(*mids[-1])
            for i in range(len(q)):
                path.quadTo(q[i][0], q[i][1], mids[i][0], mids[i][1])
            path.close()
        else:
            path.moveTo(*q[0])
            for i in range(1, len(q) - 1):
                m = (q[i] + q[i + 1]) / 2
                path.quadTo(q[i][0], q[i][1], m[0], m[1])
            path.lineTo(*q[-1])
        return path

    def line(self, pts, w, col=None, a=1.0, jitter=True):
        q = self._jitter(pts) if jitter else [np.asarray(p, float) for p in pts]
        self.c.drawPath(self._smooth_path(q, False), stroke(col or self.ink, w, a))

    def shape(self, pts, fill_col=None, line_w=0.0, line_col=None, a=1.0, jitter=True):
        q = self._jitter(pts, closed=True) if jitter else [np.asarray(p, float) for p in pts]
        path = self._smooth_path(q, True)
        if fill_col:
            self.c.drawPath(path, fill(fill_col, a))
        if line_w > 0:
            self.c.drawPath(path, stroke(line_col or self.ink, line_w, a))
        return path

    def ellipse(self, cx, cy, rx, ry, fill_col=None, line_w=0.0, line_col=None, rot=0.0, n=None, a=1.0):
        n = n or max(10, int(2 * math.pi * max(rx, ry) / self.step) + 6)
        cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts = []
        for i in range(n):
            th = 2 * math.pi * i / n
            x, y = rx * math.cos(th), ry * math.sin(th)
            pts.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
        return self.shape(pts, fill_col, line_w, line_col, a)


# ---------------------------------------------------------------- 5x7 bitmap font
_G = {
    "A": "".join([".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"]), "B": "####.#...##...#####.#...##...#####.",
    "C": ".###.#...##....#....#....#...#.###.", "D": "####.#...##...##...##...##...#####.",
    "E": "######....#....####.#....#....#####", "F": "######....#....####.#....#....#....",
    "G": ".###.#...##....#.####...##...#.####", "H": "#...##...##...#######...##...##...#",
    "I": "#####..#....#....#....#....#..#####", "J": "..###...#....#....#....##..#..##...",
    "K": "#...##..#.#.#..##...#.#..#..#.#...#", "L": "#....#....#....#....#....#....#####",
    "M": "#...###.###.#.##.#.##...##...##...#", "N": "#...###..##.#.##..###...##...##...#",
    "O": ".###.#...##...##...##...##...#.###.", "P": "####.#...##...#####.#....#....#....",
    "Q": ".###.#...##...##...##.#.##..#..##.#", "R": "####.#...##...#####.#.#..#..#.#...#",
    "S": "".join([".####", "#....", "#....", ".###.", "....#", "....#", "####."]), "T": "#####..#....#....#....#....#....#..",
    "U": "#...##...##...##...##...##...#.###.", "V": "#...##...##...##...##...#.#.#...#..",
    "W": "#...##...##...##.#.##.#.##.#.#.#.#.", "X": "#...##...#.#.#...#...#.#.#...##...#",
    "Y": "#...##...#.#.#...#....#....#....#..", "Z": "#####....#...#...#...#...#....#####",
    "0": ".###.#...##..###.#.###..##...#.###.", "1": "..#...##....#....#....#....#...###.",
    "2": ".###.#...#....#...#...#...#...#####", "3": "".join(["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."]),
    "4": "...#...##..#.#.#..#.#####...#....#.", "5": "######....####.....#....##...#.###.",
    "6": "..##..#...#....####.#...##...#.###.", "7": "#####....#...#...#...#....#....#...",
    "8": ".###.#...##...#.###.#...##...#.###.", "9": ".###.#...##...#.####....#...#..##..",
    ".": "".join([".....", ".....", ".....", ".....", ".....", ".##..", ".##.."]), "!": "..#....#....#....#....#.........#..",
    "?": ".###.#...#....#...#...#.........#..", "%": "##...##..#...#...#...#...#..##...##",
    ":": "......##...##.........##...##......", "-": "...............#####...............",
    "'": "".join(["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."]), "/": "....#....#...#...#...#...#....#....",
    "+": ".......#....#..#####..#....#.......", " ": "." * 35,
}


def pixel_text(c, s, x, y, px, col="#FFFFFF", shadow="#000000", align="left", a=1.0):
    """Draws s in the 5x7 bitmap font. px = size of one font pixel. (x, y) = top-left (or centre/right)."""
    s = s.upper()
    adv = 6 * px
    width = len(s) * adv - px
    if align == "center":
        x -= width / 2
    elif align == "right":
        x -= width
    passes = [(shadow, px * 0.7, px * 0.7)] + [(shadow, ox, oy) for ox, oy in ((-px * 0.35, 0), (px * 0.35, 0), (0, -px * 0.35), (0, px * 0.35))] + [(col, 0, 0)]
    for colr, ox, oy in passes:
        if colr is None:
            continue
        p = fill(colr, a)
        for i, ch in enumerate(s):
            g = _G.get(ch, _G[" "])[:35].ljust(35, ".")
            for k, v in enumerate(g):
                if v == "#":
                    r, cc = divmod(k, 5)
                    c.drawRect(skia.Rect.MakeXYWH(x + i * adv + cc * px + ox, y + r * px + oy, px + 0.5, px + 0.5), p)
    return width


# ---------------------------------------------------------------- rig
POSES = {
    #            lean head  arms[(sh, el), (sh, el)]        legs[(hip, knee), (hip, knee)]  shoulder lift
    "idle":    dict(lean=0, head=0, arms=[(-16, -10), (16, 10)], legs=[(-10, 3), (10, -3)], lift=0),
    "talk":    dict(lean=2, head=-3, arms=[(-22, -35), (40, 70)], legs=[(-10, 3), (12, -4)], lift=0),
    "hips":    dict(lean=-2, head=4, arms=[(-52, 100), (52, -100)], legs=[(-13, 2), (13, -2)], lift=0),
    "point":   dict(lean=6, head=-4, arms=[(-50, 100), (98, -6)], legs=[(-14, 4), (16, -2)], lift=0),
    "shrug":   dict(lean=0, head=12, arms=[(-58, -105), (58, 105)], legs=[(-9, 2), (9, -2)], lift=0.35),
    "pump":    dict(lean=-4, head=-8, arms=[(-30, -40), (168, 12)], legs=[(-20, 6), (20, -6)], lift=0.1),
    "explain": dict(lean=3, head=-5, arms=[(-62, -62), (62, 62)], legs=[(-12, 3), (12, -3)], lift=0.1),
    "wide":    dict(lean=0, head=0, arms=[(-138, -12), (138, 12)], legs=[(-22, 5), (22, -5)], lift=0.15),
    "cross":   dict(lean=-3, head=8, arms=[(-14, 112), (14, -112)], legs=[(-6, 0), (16, -6)], lift=0),
    "think":   dict(lean=2, head=10, arms=[(-14, 100), (24, 152)], legs=[(-8, 2), (12, -4)], lift=0),
    "crouch":  dict(lean=4, head=4, arms=[(-30, -30), (30, 30)], legs=[(-18, 40), (18, -40)], lift=-0.1),
}


def blend_pose(a, b, k):
    out = {}
    for key in ("lean", "head", "lift"):
        out[key] = a[key] + (b[key] - a[key]) * k
    for key in ("arms", "legs"):
        out[key] = [tuple(a[key][i][j] + (b[key][i][j] - a[key][i][j]) * k for j in range(2)) for i in range(2)]
    return out


def joints(p, R, HR):
    hip = np.zeros(2)
    up = -_dir(p["lean"])
    shoulder = hip + up * 2.6 * R
    sh_l = shoulder + up * p.get("lift", 0) * R
    neck = shoulder + up * 0.35 * R
    head = neck + _dir(180 + p["lean"] + p["head"]) * HR * 0.92
    J = dict(hip=hip, shoulder=shoulder, neck=neck, head=head)
    for side, (s, e) in zip(("l", "r"), p["arms"]):
        elbow = sh_l + _dir(p["lean"] + s) * 1.45 * R
        hand = elbow + _dir(p["lean"] + s + e) * 1.35 * R
        J["elbow_" + side], J["hand_" + side] = elbow, hand
    for side, (h, k) in zip(("l", "r"), p["legs"]):
        knee = hip + _dir(h) * 1.8 * R
        foot = knee + _dir(h + k) * 1.8 * R
        J["knee_" + side], J["foot_" + side] = knee, foot
    J["sh_l"] = sh_l
    return J


def hat(pen, cx, cy, HR, tilt, ink_w):
    """Flat Flash chrome cone: silver with hard highlight bands, ink outline, turquoise rim."""
    c = pen.c
    c.save()
    c.translate(cx, cy)
    c.rotate(tilt)
    w, h = 3.1 * HR, 1.15 * HR
    cone = [(0, -h), (w * 0.25, -h * 0.5), (w / 2, 0), (w * 0.25, 0.13 * HR), (0, 0.17 * HR), (-w * 0.25, 0.13 * HR), (-w / 2, 0), (-w * 0.25, -h * 0.5)]
    path = pen.shape(cone, "#C9D1DA", 0)
    c.save()
    c.clipPath(path, doAntiAlias=True)
    c.drawPath(_poly([(-0.05 * HR, -h * 1.1), (0.25 * HR, -h * 1.1), (-w * 0.18, 0.4 * HR), (-w * 0.38, 0.4 * HR)]), fill("#FFFFFF"))
    c.drawPath(_poly([(0.45 * HR, -h * 1.1), (0.6 * HR, -h * 1.1), (-w * 0.02, 0.4 * HR), (-w * 0.1, 0.4 * HR)]), fill("#F2F6F9"))
    c.drawPath(_poly([(0.3 * HR, -h), (w * 0.6, 0.0), (w * 0.6, 0.4 * HR), (w * 0.12, 0.4 * HR)]), fill("#8C96A3"))
    c.restore()
    pen.shape(cone, None, ink_w)
    rim = [(-w / 2 + 0.05 * HR, 0.02 * HR), (-w * 0.25, 0.15 * HR), (0, 0.19 * HR), (w * 0.25, 0.15 * HR), (w / 2 - 0.05 * HR, 0.02 * HR)]
    pen.line(rim, ink_w * 0.55, TURQ)
    c.restore()


def _poly(pts):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


VISEMES = ("rest", "MBP", "small", "open", "wide", "O", "U", "FV")


def mouth(pen, vis, HR, open_k=1.0):
    """Mouth shapes in head-local coords (unit HR, origin = head centre). open_k scales jaw drop (0.6..1.2)."""
    u = HR
    lw = 0.075 * u
    ink, paper = pen.ink, pen.paper
    mi = MOUTH_IN if ink == INK else "#FFFFFF"
    y0 = 0.40

    def P(pts):
        return [(x * u, y * u) for x, y in pts]

    c0 = pen.c
    c0.save()
    c0.translate(0, 0.35 * u)
    c0.scale(1.28, 1.28)
    c0.translate(0, -0.40 * u)
    _mouth_shape(pen, vis, u, lw, ink, paper, mi, y0, P, open_k)
    c0.restore()


def _mouth_shape(pen, vis, u, lw, ink, paper, mi, y0, P, open_k):
    if vis == "rest":
        pen.line(P([(-0.22, 0.41), (-0.08, 0.47), (0.08, 0.47), (0.22, 0.41)]), lw)
    elif vis == "MBP":
        pen.line(P([(-0.26, 0.45), (0.26, 0.45)]), lw * 1.35)
        pen.line(P([(-0.28, 0.40), (-0.25, 0.50)]), lw * 0.8)
        pen.line(P([(0.28, 0.40), (0.25, 0.50)]), lw * 0.8)
    elif vis in ("small", "open", "wide"):
        hw, dep = {"small": (0.17, 0.17), "open": (0.25, 0.36), "wide": (0.32, 0.22)}[vis]
        dep *= open_k
        top = 0.38 if vis != "wide" else 0.37
        pts = P([(-hw, top), (-hw * 0.5, top - 0.02), (0, top - 0.025), (hw * 0.5, top - 0.02), (hw, top),
                 (hw * 0.75, top + dep * 0.65), (0, top + dep), (-hw * 0.75, top + dep * 0.65)])
        path = pen.shape(pts, mi, 0)
        c = pen.c
        c.save()
        c.clipPath(path, doAntiAlias=True)
        tb = (0.07 if vis != "small" else 0.05) * u
        c.drawRect(skia.Rect.MakeXYWH(-hw * u, (top - 0.05) * u, 2 * hw * u, tb + 0.05 * u), fill(paper))
        if vis == "wide":
            c.drawRect(skia.Rect.MakeXYWH(-hw * u, (top + dep - 0.075) * u, 2 * hw * u, 0.2 * u), fill(paper))
        if vis == "open":
            c.drawOval(skia.Rect.MakeXYWH(-0.17 * u, (top + dep - 0.14) * u, 0.34 * u, 0.24 * u), fill(TONGUE if ink == INK else "#BBBBBB"))
        c.restore()
        pen.shape(pts, None, lw)
    elif vis == "O":
        rx, ry = 0.15, 0.17 * open_k + 0.02
        pen.ellipse(0, (y0 + ry) * u, rx * u, ry * u, mi, lw)
        pen.c.drawOval(skia.Rect.MakeXYWH(-0.08 * u, (y0 + ry * 1.2) * u, 0.16 * u, 0.1 * u), fill(TONGUE if ink == INK else "#BBBBBB"))
        pen.ellipse(0, (y0 + ry) * u, rx * u, ry * u, None, lw)
    elif vis == "U":
        pen.ellipse(0, (y0 + 0.09) * u, 0.075 * u, 0.085 * u, mi, lw * 1.2)
        pen.line(P([(-0.13, 0.46), (-0.09, 0.49)]), lw * 0.7)
        pen.line(P([(0.13, 0.46), (0.09, 0.49)]), lw * 0.7)
    elif vis == "FV":
        pts = P([(-0.21, 0.40), (0, 0.38), (0.21, 0.40), (0.15, 0.52), (0, 0.55), (-0.15, 0.52)])
        path = pen.shape(pts, mi, 0)
        pen.c.save()
        pen.c.clipPath(path, doAntiAlias=True)
        pen.c.drawRect(skia.Rect.MakeXYWH(-0.25 * u, 0.33 * u, 0.5 * u, 0.15 * u), fill(paper))
        pen.c.restore()
        pen.shape(pts, None, lw)
        pen.line(P([(-0.19, 0.49), (0, 0.475), (0.19, 0.49)]), lw * 1.1)          # lower lip tucked under the teeth


def eyes(pen, HR, mood, blink, look=0.0, shock=False):
    u = HR
    lw = 0.075 * u
    ex, ey = 0.30, 0.02
    ink = pen.ink
    for s in (-1, 1):
        x = s * ex * u + look * 0.06 * u
        if blink:
            pen.line([(x - 0.11 * u, ey * u + 0.02 * u), (x, ey * u + 0.05 * u), (x + 0.11 * u, ey * u + 0.02 * u)], lw)
        elif shock:
            pen.ellipse(s * ex * u, ey * u, 0.17 * u, 0.19 * u, pen.paper, lw * 0.8)
            pen.c.drawCircle(x, ey * u, 0.05 * u, fill(ink))
        else:
            ry = 0.16 if mood != "smug" else 0.12
            pen.ellipse(x, ey * u, 0.085 * u, ry * u, ink, 0)
            pen.c.drawCircle(x + 0.03 * u, ey * u - 0.06 * u, 0.028 * u, fill(pen.paper))
            if mood == "smug":                                              # heavy lids
                pen.c.drawRect(skia.Rect.MakeXYWH(x - 0.12 * u, (ey - 0.2) * u, 0.24 * u, 0.15 * u), fill(pen.paper))
                pen.line([(x - 0.12 * u, (ey - 0.05) * u), (x + 0.12 * u, (ey - 0.05) * u)], lw)
    # brows
    bw = 0.085 * u
    if mood == "raised":
        for s in (-1, 1):
            pen.line([(s * 0.16 * u, -0.27 * u), (s * 0.30 * u, -0.33 * u), (s * 0.44 * u, -0.29 * u)], bw)
    elif mood == "angry":
        for s in (-1, 1):
            pen.line([(s * 0.12 * u, -0.13 * u), (s * 0.44 * u, -0.25 * u)], bw)
    elif mood == "smug":
        pen.line([(-0.44 * u, -0.17 * u), (-0.16 * u, -0.17 * u)], bw)
        pen.line([(0.16 * u, -0.27 * u), (0.30 * u, -0.34 * u), (0.44 * u, -0.30 * u)], bw)
    elif mood == "shock":
        for s in (-1, 1):
            pen.line([(s * 0.14 * u, -0.33 * u), (s * 0.30 * u, -0.40 * u), (s * 0.45 * u, -0.35 * u)], bw)
    else:
        for s in (-1, 1):
            pen.line([(s * 0.16 * u, -0.21 * u), (s * 0.44 * u, -0.22 * u)], bw)


def character(pen, pose, x, floor, R, HR, st):
    """st: dict(vis, open_k, mood, blink, look, shock, sy (squash/stretch), nod, hat_lift, hat_tilt, talk)."""
    c = pen.c
    J = joints(pose, R, HR)
    lowest = max(J["foot_l"][1], J["foot_r"][1])
    off = np.array([x, floor - lowest])
    J = {k: v + off for k, v in J.items()}
    sy = st.get("sy", 1.0)
    sx = 1.0 / math.sqrt(max(0.5, sy))
    c.save()
    c.translate(x, floor)
    c.scale(sx, sy)
    c.translate(-x, -floor)
    w = 0.30 * R
    if pen.paper == PAPER:                                   # paper underlay: the ink reads on any background
        under = [[J["hip"], J["knee_l"], J["foot_l"]], [J["hip"], J["knee_r"], J["foot_r"]], [J["hip"], J["shoulder"], J["neck"]],
                 [J["sh_l"], J["elbow_l"], J["hand_l"]], [J["sh_l"], J["elbow_r"], J["hand_r"]]]
        for seg in under:
            path = skia.Path()
            path.moveTo(*seg[0])
            for q in seg[1:]:
                path.lineTo(*q)
            c.drawPath(path, stroke(PAPER, w * 1.9, 0.9))
    for side in ("l", "r"):
        pen.line([J["hip"], J["knee_" + side], J["foot_" + side]], w)
    pen.line([J["hip"], J["shoulder"], J["neck"]], w)
    for side in ("l", "r"):
        pen.line([J["sh_l"], J["elbow_" + side], J["hand_" + side]], w)
        pen.c.drawCircle(*J["hand_" + side], 0.19 * R, fill(pen.ink))
    # head
    hx, hy = J["head"]
    nod = st.get("nod", 0.0)
    hy += nod * 0.12 * HR
    tilt = pose["lean"] + pose["head"] + nod * 6
    c.save()
    c.translate(hx, hy)
    c.rotate(tilt)
    hsq = 1.0 - 0.06 * nod
    c.scale(1.0 / hsq ** 0.5, hsq)
    pen.ellipse(0, 0, HR, HR, pen.paper, 0.13 * HR, n=22)
    shock = st.get("shock", False)
    eyes(pen, HR, "shock" if shock else st.get("mood", "neutral"), st.get("blink", False), st.get("look", 0.0), shock)
    mouth(pen, st.get("vis", "rest"), HR, st.get("open_k", 1.0))
    hat(pen, 0 + st.get("hat_dx", 0) * HR, -0.52 * HR - st.get("hat_lift", 0.0) * HR, HR, st.get("hat_tilt", 0.0), 0.11 * HR)
    c.restore()
    c.restore()
    return J


# ---------------------------------------------------------------- backgrounds
def _sky(c, W, H, top, bot, bands=7):
    """Posterised (hard-banded) gradient, the cheap Flash look."""
    tc = [int(top[1 + 2 * j:3 + 2 * j], 16) for j in range(3)]
    bc = [int(bot[1 + 2 * j:3 + 2 * j], 16) for j in range(3)]
    for i in range(bands):
        k = i / (bands - 1)
        col = "#%02X%02X%02X" % tuple(int(tc[j] * (1 - k) + bc[j] * k) for j in range(3))
        y0 = -H if i == 0 else H * 0.8 * i / bands
        y1 = 3 * H if i == bands - 1 else H * 0.8 * (i + 1) / bands + 1
        c.drawRect(skia.Rect.MakeLTRB(-W, y0, 2 * W, y1), fill(col))


class Arena:
    """A Flash-game arena: banded sky, outlined clouds, two skyline layers, a grass-topped ground and floating
    platforms. Laid out from (W, H, floor) so the same code serves 16:9 and 9:16."""

    def __init__(self, W, H, floor, seed=3):
        self.W, self.H, self.floor = W, H, floor
        rng = random.Random(seed)
        self.far, self.near = [], []
        x = -W * 0.6
        while x < W * 1.6:
            bw = rng.uniform(0.05, 0.11) * max(W, H * 0.9)
            self.far.append((x, bw, rng.uniform(0.14, 0.32) * H))
            x += bw * rng.uniform(0.75, 1.05)
        x = -W * 0.6
        while x < W * 1.6:
            bw = rng.uniform(0.06, 0.13) * max(W, H * 0.9)
            hgt = rng.uniform(0.08, 0.20) * H
            wins = [(i, j, rng.random() < 0.55) for i in range(int(bw // 34)) for j in range(int(hgt // 46))]
            self.near.append((x, bw, hgt, wins, rng.choice(["#7C93D6", "#8E85D2", "#6FA3D8"])))
            x += bw * rng.uniform(1.0, 1.3)
        self.clouds = [(rng.uniform(-0.2, 1.2) * W, rng.uniform(0.05, 0.15) * H, rng.uniform(0.6, 1.0)) for _ in range(4)]
        vert = H > W
        self.plats = ([(0.12 * W, floor - 0.30 * H, 0.26 * W), (0.86 * W, floor - 0.22 * H, 0.24 * W)] if not vert else
                      [(0.08 * W, floor - 0.42 * H, 0.36 * W), (0.95 * W, floor - 0.30 * H, 0.32 * W)])

    def draw(self, c, pen, cam, t):
        W, H, floor = self.W, self.H, self.floor
        c.save()
        _sky(c, W, H, "#3FA9F5", "#BDEBFF")
        c.restore()
        with cam.apply(0.15, c):
            for (cx0, cy, s) in self.clouds:
                cx = (cx0 + t * 14 * s) % (W * 1.4) - W * 0.2
                blobs = [(-60, 8, 42), (-20, -14, 55), (30, -6, 48), (68, 10, 36), (5, 14, 50)]
                path = skia.Path()
                for bx, by, br in blobs:
                    path.addCircle(cx + bx * s, cy + by * s, br * s)
                c.drawPath(path, stroke(INK, 9 * s))
                c.drawPath(path, fill("#FFFFFF"))
        with cam.apply(0.35, c):
            for (x, bw, hgt) in self.far:
                c.drawRect(skia.Rect.MakeXYWH(x, floor - hgt - 0.02 * H, bw + 1, hgt + H), fill("#8FB8E8"))
        with cam.apply(0.6, c):
            for (x, bw, hgt, wins, col) in self.near:
                top = floor - hgt
                pen.shape([(x, top), (x + bw, top), (x + bw, floor + 40), (x, floor + 40)], col, 6)
                for i, j, on in wins:
                    if on:
                        c.drawRect(skia.Rect.MakeXYWH(x + 14 + i * 34, top + 18 + j * 46, 16, 22), fill("#FFF3B0"))
        with cam.apply(1.0, c):
            # ground
            gpts = [(-W, floor), (2 * W, floor), (2 * W, floor + H), (-W, floor + H)]
            pen.shape(gpts, "#9C6B3E", 0)
            rng = random.Random(11)
            for i in range(40):
                bx = -W * 0.5 + i * 0.07 * W
                by = floor + 60 + (i % 3) * 70
                c.drawRoundRect(skia.Rect.MakeXYWH(bx, by, 0.045 * W, 34), 10, 10, fill("#7E5330"))
            grass = []
            n = 60
            for i in range(n + 1):
                gx = -W + 3 * W * i / n
                grass.append((gx, floor + (18 if i % 2 else 30)))
            pen.shape([(-W, floor - 10)] + [(2 * W, floor - 10)] + grass[::-1], "#5BD35B", 0)
            pen.line([(-W, floor - 10), (2 * W, floor - 10)], 8)
            for (px, py, pw) in self.plats:
                body = [(px - pw / 2, py), (px + pw / 2, py), (px + pw / 2 - 18, py + 46), (px - pw / 2 + 18, py + 46)]
                pen.shape(body, "#9C6B3E", 7)
                pen.shape([(px - pw / 2 - 6, py - 14), (px + pw / 2 + 6, py - 14), (px + pw / 2 + 6, py + 8), (px - pw / 2 - 6, py + 8)], "#5BD35B", 7)
            # a crate, for flavour
            cx_, cs = (0.72 * W if W > H else 0.80 * W), 0.075 * max(W, H) * (0.9 if W > H else 0.75)
            pen.shape([(cx_, floor - cs), (cx_ + cs, floor - cs), (cx_ + cs, floor), (cx_, floor)], "#D9A15B", 7)
            pen.line([(cx_ + 8, floor - cs + 8), (cx_ + cs - 8, floor - 8)], 6)
            pen.line([(cx_ + cs - 8, floor - cs + 8), (cx_ + 8, floor - 8)], 6)


class Flat:
    """Flat bright colour with slow Newgrounds title-screen rays."""

    def __init__(self, W, H, floor, col="#FFD23F"):
        self.W, self.H, self.floor, self.col = W, H, floor, col

    def draw(self, c, pen, cam, t):
        W, H = self.W, self.H
        c.drawRect(skia.Rect.MakeXYWH(-10, -10, W + 20, H + 20), fill(self.col))
        cx, cy = W / 2, self.floor - 0.3 * H
        n = 16
        rot = t * 6
        L = 2 * max(W, H)
        ray = fill(shade(self.col, 1.12))
        for i in range(n):
            a0 = math.radians(rot + i * 360 / n)
            a1 = math.radians(rot + i * 360 / n + 360 / n / 2)
            c.drawPath(_poly([(cx, cy), (cx + L * math.cos(a0), cy + L * math.sin(a0)), (cx + L * math.cos(a1), cy + L * math.sin(a1))]), ray)


# ---------------------------------------------------------------- camera
class Cam:
    """screen = (world - focus) * zoom + anchor, with parallax p blending towards identity."""

    def __init__(self, W, H):
        self.W, self.H = W, H
        self.anchor = np.array([W / 2, H * 0.5])
        self.focus = self.anchor.copy()
        self.zoom = 1.0
        self.shake = np.zeros(2)

    def set(self, focus, zoom, shake=(0, 0)):
        self.focus, self.zoom, self.shake = np.asarray(focus, float), zoom, np.asarray(shake, float)

    class _Ctx:
        def __init__(self, cam, p, c):
            self.cam, self.p, self.c = cam, p, c

        def __enter__(self):
            cam, p, c = self.cam, self.p, self.c
            z = 1 + (cam.zoom - 1) * p
            f = cam.anchor + (cam.focus - cam.anchor) * p
            c.save()
            c.translate(*(cam.anchor + cam.shake * (0.3 + 0.7 * p)))
            c.scale(z, z)
            c.translate(*(-f))

        def __exit__(self, *a):
            self.c.restore()

    def apply(self, p, c):
        return Cam._Ctx(self, p, c)


# ---------------------------------------------------------------- effects
def speed_lines(c, W, H, cx, cy, seed, col=INK, a=0.85, inner=0.32):
    rng = random.Random(seed)
    L = math.hypot(W, H)
    for i in range(70):
        th = rng.uniform(0, 2 * math.pi)
        r0 = rng.uniform(inner, inner + 0.25) * min(W, H)
        w = rng.uniform(4, 16)
        dx, dy = math.cos(th), math.sin(th)
        nx, ny = -dy, dx
        p = _poly([(cx + dx * r0, cy + dy * r0), (cx + dx * L + nx * w * 3, cy + dy * L + ny * w * 3), (cx + dx * L - nx * w * 3, cy + dy * L - ny * w * 3)])
        c.drawPath(p, fill(col, a))


def burst(pen, cx, cy, r, seed, text=None, font_size=120, rot=-8):
    """Comic SFX star with Impact text, e.g. BOOM!"""
    rng = random.Random(seed)
    n = 14
    pts = []
    for i in range(2 * n):
        rr = r * (1.0 if i % 2 == 0 else rng.uniform(0.55, 0.68))
        th = math.pi * i / n + rng.uniform(-0.05, 0.05)
        pts.append((cx + rr * math.cos(th) * 1.35, cy + rr * math.sin(th)))
    pen.shape(pts, "#FF7A1A", r * 0.07)
    pts2 = [(cx + (x - cx) * 0.72, cy + (y - cy) * 0.72) for x, y in pts]
    pen.shape(pts2, "#FFE14D", 0)
    if text:
        f = skia.Font(skia.Typeface.MakeFromFile(IMPACT_FONT), font_size)
        tw = f.measureText(text)
        c = pen.c
        c.save()
        c.translate(cx, cy)
        c.rotate(rot)
        blob = skia.TextBlob.MakeFromString(text, f)
        c.drawTextBlob(blob, -tw / 2, font_size * 0.36, stroke(INK, font_size * 0.16))
        c.drawTextBlob(blob, -tw / 2, font_size * 0.36, fill("#FFFFFF"))
        c.restore()


def caption(c, words, active, W, y, size, pop=1.0):
    """words: list[str]; active: index of the word being spoken (-1 none)."""
    f = skia.Font(skia.Typeface.MakeFromFile(IMPACT_FONT), size)
    gap = size * 0.28
    widths = [f.measureText(w) for w in words]
    total = sum(widths) + gap * (len(words) - 1)
    c.save()
    c.translate(W / 2, y)
    c.scale(pop, pop)
    x = -total / 2
    for i, (w_, ww) in enumerate(zip(words, widths)):
        blob = skia.TextBlob.MakeFromString(w_, f)
        c.drawTextBlob(blob, x, 0, stroke(INK, size * 0.2))
        c.drawTextBlob(blob, x, 0, fill("#FFE14D" if i == active else "#FFFFFF"))
        x += ww + gap
    c.restore()


def hud(c, W, H, hp, score, pop_text=None, pop_k=0.0, name="STICKMAN"):
    s = min(W, H) / 1080
    px = 7 * s
    m = 40 * s
    pixel_text(c, "P1 " + name, m, m, px, "#FFFFFF")
    bw, bh = 520 * s if W > H else 600 * s, 38 * s
    by = m + 9 * px
    c.drawRect(skia.Rect.MakeXYWH(m - 6 * s, by - 6 * s, bw + 12 * s, bh + 12 * s), fill(INK))
    c.drawRect(skia.Rect.MakeXYWH(m, by, bw, bh), fill("#B3122E"))
    col = "#45E04A" if hp > 0.5 else ("#FFD23F" if hp > 0.25 else "#FF4D2E")
    c.drawRect(skia.Rect.MakeXYWH(m, by, bw * hp, bh), fill(col))
    c.drawRect(skia.Rect.MakeXYWH(m, by, bw * hp, bh * 0.3), fill("#FFFFFF", 0.35))
    for k in range(1, 10):
        c.drawRect(skia.Rect.MakeXYWH(m + bw * k / 10 - 2 * s, by, 4 * s, bh), fill(INK, 0.6))
    pixel_text(c, "SCORE", W - m, m, px, "#FFFFFF", align="right")
    pixel_text(c, "%07d" % score, W - m, m + 9 * px, px, "#FFE14D", align="right")
    if pop_text and pop_k < 1:
        pixel_text(c, pop_text, W - m, m + 19 * px - pop_k * 30 * s, px * 0.8, "#FFFFFF", align="right", a=1 - pop_k ** 3)


def loading(c, W, H, k, done):
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), fill("#000000"))
    s = min(W, H) / 1080
    px = 10 * s
    pct = min(100, int(k * 100))
    pixel_text(c, "LOADING..." if not done else "READY!", W / 2, H / 2 - 120 * s, px, "#FFFFFF", None, align="center")
    bw, bh = 700 * s, 60 * s
    x0, y0 = W / 2 - bw / 2, H / 2
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, bw, bh), stroke("#FFFFFF", 6 * s))
    segs = 14
    for i in range(int(segs * min(1, k))):
        c.drawRect(skia.Rect.MakeXYWH(x0 + 12 * s + i * (bw - 24 * s) / segs, y0 + 12 * s, (bw - 24 * s) / segs - 8 * s, bh - 24 * s), fill(TURQ))
    pixel_text(c, "%d%%" % pct, W / 2, y0 + bh + 40 * s, px * 0.8, "#FFE14D", None, align="center")
