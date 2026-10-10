"""Pictures h01-h05 for the sh_steve Short, drawn in code (skia): greys and white on black, no words.
Our own cast only: VOXEL (a cube-headed robot with a visor slit; deliberately not any game's character) and a generic
city made of monospaced type. Subjects sit in the middle 60% of the width: a Short crops the sides.

    ~/youtube/.venv/bin/python diagrams.py        -> src/ai/h01.png ... h05.png
"""
import math
import os
import random
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ch2", "ep06"))
from look_test import font  # noqa: E402

W, H = 1920, 1080
OUT = os.path.join(HERE, "src", "ai")
CX = W / 2


def g(v, a=1.0):
    k = int(round(max(0.0, min(1.0, v)) * 255))
    return skia.Color(k, k, k, int(255 * a))


def poly(c, pts, v, a=1.0, stroke=0.0):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    paint = skia.Paint(Color=g(v, a), AntiAlias=True)
    if stroke:
        paint.setStyle(skia.Paint.kStroke_Style)
        paint.setStrokeWidth(stroke)
    c.drawPath(p, paint)


def line(c, a, b, v, w=3.0, alpha=1.0, dash=None):
    p = skia.Paint(Color=g(v, alpha), AntiAlias=True, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap)
    if dash:
        p.setPathEffect(skia.DashPathEffect.Make(dash, 0))
    c.drawLine(*a, *b, p)


def cube(c, x, y, s, top=0.86, left=0.56, right=0.34, wire=False, alpha=1.0):
    """An isometric cube whose bottom corner sits at (x, y), edge s."""
    dx, dy = s * math.cos(math.radians(30)), s * 0.5
    A, B_, C, D = (x, y), (x - dx, y - dy), (x, y - 2 * dy), (x + dx, y - dy)
    A2, B2, C2, D2 = [(px, py - s) for px, py in (A, B_, C, D)]
    faces = [([B2, C2, D2, A2], top), ([B_, A, A2, B2], left), ([A, D, D2, A2], right)]
    for pts, v in faces:
        if wire:
            poly(c, pts, 0.9, 0.85 * alpha, stroke=3.0)
        else:
            poly(c, pts, v, alpha)
            poly(c, pts, 0.05, alpha, stroke=2.0)
    return A2, C2


def voxel(c, x, y, s=1.0):
    """VOXEL: big cube head with a bright visor slit and an antenna, a small body, block limbs. Feet at (x, y)."""
    u = 60 * s
    cube(c, x - 0.9 * u, y, 0.75 * u, 0.7, 0.45, 0.28)               # legs
    cube(c, x + 0.9 * u, y + 0.1 * u, 0.75 * u, 0.7, 0.45, 0.28)
    cube(c, x, y - 0.75 * u, 1.5 * u, 0.8, 0.52, 0.32)               # body
    cube(c, x - 1.75 * u, y - 1.4 * u, 0.62 * u, 0.75, 0.48, 0.3)     # arms
    cube(c, x + 1.75 * u, y - 1.2 * u, 0.62 * u, 0.75, 0.48, 0.3)
    hy = y - 2.25 * u
    cube(c, x, hy, 2.5 * u, 0.92, 0.62, 0.38)                          # the head
    dx, dy = 2.5 * u * math.cos(math.radians(30)), 2.5 * u * 0.5
    vy = hy - 2.5 * u * 0.55                                           # visor slit across the head's left face
    poly(c, [(x - dx * 0.85, vy - dy * 0.85), (x - dx * 0.12, vy - dy * 0.12), (x - dx * 0.12, vy - dy * 0.12 + 0.32 * u),
             (x - dx * 0.85, vy - dy * 0.85 + 0.32 * u)], 1.0)
    top = (x, hy - 2.5 * u - dy)                                       # antenna from the top face's centre
    line(c, top, (top[0] + 0.3 * u, top[1] - 1.3 * u), 0.85, 5 * s)
    c.drawCircle(top[0] + 0.3 * u, top[1] - 1.45 * u, 0.22 * u, skia.Paint(Color=g(1.0), AntiAlias=True))


def city(c, x0, x1, base, rng, size=22, hmin=260, hmax=760, v=0.75):
    """A skyline made of type: each building a column block of characters, windows brighter than walls."""
    f = font("IBMPlexMono-500", size)
    cw, lh = size * 0.6, size * 1.05
    x = x0
    while x < x1 - 4 * cw:
        bw = int(rng.uniform(5, 11)) * cw
        bh = rng.uniform(hmin, hmax)
        rows = int(bh / lh)
        cols = int(bw / cw)
        for r in range(rows):
            yy = base - r * lh
            for q in range(cols):
                edge = q in (0, cols - 1) or r == rows - 1
                ch = "|" if q in (0, cols - 1) else ("=" if r == rows - 1 else ("#" if (r % 3 and q % 2) else "."))
                lit = 0.95 if (ch == "#" and rng.random() < 0.35) else (v if edge else v * 0.55)
                c.drawString(ch, x + q * cw, yy, f, skia.Paint(Color=g(lit), AntiAlias=True))
        x += bw + rng.uniform(0.5, 2.5) * cw


def new():
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    return s, c


def save(s, name):
    os.makedirs(OUT, exist_ok=True)
    s.makeImageSnapshot().save(os.path.join(OUT, name + ".png"), skia.kPNG)
    print(name)


def h01():
    """The torn screen: VOXEL on the left half, the type city on the right, a jagged seam with data packets across it."""
    s, c = new()
    rng = random.Random(3)
    c.save()
    seam = [(CX + rng.uniform(-26, 26), y) for y in range(0, H + 60, 60)]
    right = skia.Path()
    right.moveTo(W, 0)
    for p in seam:
        right.lineTo(*p)
    right.lineTo(W, H)
    right.close()
    c.clipPath(right, doAntiAlias=True)
    city(c, CX - 20, CX + 470, 930, random.Random(5), size=24, hmin=300, hmax=720)
    c.restore()
    for y in range(0, H, 6):                                           # the block world's side: faint voxel ground
        pass
    for k in range(5):
        cube(c, CX - 420 + k * 90, 1010 - (k % 2) * 8, 56, 0.32, 0.2, 0.12)
    voxel(c, CX - 230, 930, 1.2)
    for a_, b_ in zip(seam, seam[1:]):                                # the seam itself
        line(c, a_, b_, 1.0, 5)
    for k in range(9):                                                 # packets crossing the gap
        y = 120 + k * 95 + rng.uniform(-20, 20)
        x = CX - 70 + rng.uniform(-30, 30)
        for j in range(3):
            c.drawRect(skia.Rect.MakeXYWH(x + j * 34, y, 22, 8), skia.Paint(Color=g(0.95, 0.9 - 0.25 * j)))
    save(s, "h01")


def h02():
    """The city reports its camera: a frustum over a perspective street, rays probing down onto the ground grid."""
    s, c = new()
    city(c, CX - 600, CX + 600, 520, random.Random(11), size=18, hmin=120, hmax=380, v=0.5)
    hz = 540
    for k in range(-12, 13):                                           # street grid in perspective
        line(c, (CX + k * 26, hz), (CX + k * 150, H), 0.35, 2)
    for r in range(1, 12):
        yy = hz + (H - hz) * (r / 11) ** 1.8
        line(c, (CX - 900, yy), (CX + 900, yy), 0.35, 2)
    cam = (CX - 330, 250)                                              # the camera, as a frustum pointing into the street
    for q in ((CX - 40, 470), (CX + 340, 470), (CX + 340, 760), (CX - 40, 760)):
        line(c, cam, q, 0.9, 3)
    poly(c, [(CX - 40, 470), (CX + 340, 470), (CX + 340, 760), (CX - 40, 760)], 0.9, 1.0, stroke=3)
    c.drawRect(skia.Rect.MakeXYWH(cam[0] - 60, cam[1] - 38, 90, 70), skia.Paint(Color=g(0.95), AntiAlias=True))
    rng = random.Random(2)
    for k in range(26):                                                # probes: rays hitting the ground, a dot at each hit
        x = CX - 420 + k * 34 + rng.uniform(-6, 6)
        yb = 690 + 260 * ((k % 6) / 6) + rng.uniform(-10, 10)
        line(c, (x, 120), (x, yb), 0.6, 2, 0.8, dash=[10, 10])
        c.drawCircle(x, yb, 9, skia.Paint(Color=g(1.0), AntiAlias=True))
    save(s, "h02")


def h03():
    """The invisible floor: VOXEL standing on a stepped layer of ghost cubes that follow a kerb he can't see."""
    s, c = new()
    s_ = 70
    dx, dy = s_ * math.cos(math.radians(30)), s_ * 0.5
    for r in range(5, -1, -1):                                         # back rows first
        for q in range(-5, 6):
            x = CX + (q - r) * dx
            y = 900 + (q + r) * dy * 0.5 - r * 40 - (s_ if q > 1 else 0)
            cube(c, x, y, s_, wire=True, alpha=0.9 - 0.1 * r)
    for q in range(-6, 7):                                             # the real street, a faint line of type under the ghosts
        c.drawString("_ . _ . _", CX + q * 140 - 70, 1040, font("IBMPlexMono-500", 22), skia.Paint(Color=g(0.4), AntiAlias=True))
    voxel(c, CX - 40, 820, 1.25)
    save(s, "h03")


def h04():
    """Depth decides who's in front: three stacked layers (city, block world, the blend), a lamp post in front of VOXEL."""
    s, c = new()

    def plate(y, v):
        pts = [(CX - 560, y), (CX + 400, y), (CX + 560, y - 230), (CX - 400, y - 230)]
        poly(c, pts, 0.03)
        poly(c, pts, v, 1.0, stroke=4)
        return pts

    plate(560, 0.55)                                                   # above: the block world on its own
    voxel(c, CX, 520, 0.7)
    plate(1010, 0.95)                                                  # below: the blend, a lamp post in front of him
    city(c, CX - 380, CX + 380, 960, random.Random(8), size=16, hmin=100, hmax=230, v=0.45)
    voxel(c, CX + 30, 960, 0.7)
    line(c, (CX - 60, 975), (CX - 60, 700), 1.0, 16)
    line(c, (CX - 60, 703), (CX + 30, 703), 1.0, 14)
    line(c, (CX + 620, 590), (CX + 620, 760), 0.8, 5)                  # arrow down
    poly(c, [(CX + 600, 760), (CX + 640, 760), (CX + 620, 792)], 0.8)
    save(s, "h04")


def h05():
    """Glue, not fusion: two separate windows, a cube world and a tower of type, joined only by a thin bridge of lines."""
    s, c = new()
    for x0, kind in ((CX - 560, "vox"), (CX + 90, "city")):
        c.drawRect(skia.Rect.MakeXYWH(x0, 290, 470, 520), skia.Paint(Color=g(0.06)))
        c.drawRect(skia.Rect.MakeXYWH(x0, 290, 470, 520), skia.Paint(Color=g(0.85), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4))
        c.drawRect(skia.Rect.MakeXYWH(x0, 290, 470, 34), skia.Paint(Color=g(0.5)))
        if kind == "vox":
            voxel(c, x0 + 235, 720, 0.85)
        else:
            city(c, x0 + 40, x0 + 440, 770, random.Random(4), size=20, hmin=180, hmax=400, v=0.7)
    for k in range(5):                                                 # the bridge: a few thin lines, packets on them
        y = 470 + k * 36
        line(c, (CX - 90, y), (CX + 90, y), 0.9, 3)
        c.drawRect(skia.Rect.MakeXYWH(CX - 40 + (k * 23) % 60, y - 7, 26, 14), skia.Paint(Color=g(1.0)))
    save(s, "h05")


if __name__ == "__main__":
    for fn in (h01, h02, h03, h04, h05):
        fn()
