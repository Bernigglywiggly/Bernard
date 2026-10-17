"""EP04 · THE MAN IN THE MACHINE, the scenes: line art keyed to the script's line ids and George's words
(engine.tl.word), which the engine turns into characters. Robots are plated (dim fills, so they read solid in
characters); people are plain lines; the thread between a machine and the person steering it is a dashed signal with
pulses running down it.

  GROUND     the date; a cage forms; a man and a six-foot robot; three hits, with phosphor trails; the hand; stopped;
             the cage dissolves: the robot alone, then the pilot backstage in a VR headset, moving it like a puppet;
             2026 rolls back to 2021 and the robot becomes a person in a suit; how close?
  MECHANISM  Tesla AI Day: a stage, a spotlight, the dancer; robot boxing in a ring; four robots, four trainers; the
             split: what the machine does alone, what a person decides; $13,500 as a wall of 2,200 Big Macs
  NOW        the humanoid becomes a robot dog; the rifle; the operator; 50,000 ground robots; ~112,000 runs, a crate and
             a stretcher, the trip a soldier didn't make; the coin flips; a Patriot and its 680,000 Big Macs against a
             Shahed and its 3,000-8,000; cheap machines, expensive answers
  IDEA       four machines, four people above them; the machine's share grows along a bar; the bar becomes the loop and
             tightens around a person
  IMAGINE    a dotted 2030; the pilot dissolves; not a forecast; the rules, written far away; who is inside?
  SURFACE    2021: a person in a suit | 2026: a person inside the robot; the sources
"""
import math

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine import tl  # noqa: E402
from engine.tl import ls, le, ev, label  # noqa: E402
from engine.tl import word as wd  # noqa: E402
from engine.draw import (CX, GLOW, WHITE, MID, SOFT, GOLD, ease, seg, lerp, win, layer, P, ellipse, bezier, segs, big,  # noqa: E402
                         morph_flow, draw_segs, lines_in, points, sample_on, chrome_fill, closed_fill, stroke_polys, bignum,
                         mini_mac, coin, figure, pose_mix, STAND, GUARD, PUNCH, HIT, PILOT)

GROUND_Y = 800                                    # where feet stand in most scenes
HURT = dict(lean=18, head=16, ls=70, le=85, rs=58, re=100, lh=10, lk=-12, rh=-8, rk=-4)
TRAILS = []                                        # filled below, once the timeline is known
GLINTS = []


# ---------------------------------------------------------------- motion helpers
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


def hips_y(s):
    return GROUND_Y - 0.48 * s


# ---------------------------------------------------------------- things
def body(c, x, s, pose, face=1, t=0.0, t0=None, robot=False, mask=False, a=1.0, dur=0.8, y=None, col=None):
    """A figure standing on the ground (or with its hips at y), formed on from t0; robots get dim plate fills."""
    y = hips_y(s) if y is None else y
    polys, j = figure(x, y, s, pose, face, robot, mask)
    j["polys"] = polys
    if a <= 0.01 or (t0 is not None and t < t0):
        return j
    col = col or (WHITE if robot else GLOW)
    with layer(c, a):
        k = 1.0 if t0 is None else ease(seg(t, t0 + 0.55 * dur, t0 + dur))
        if robot and k > 0:
            closed_fill(c, j["closed"], 1.0, mg.fill(MID, 0.30 * k))
        if t0 is not None and t < t0 + dur:
            lines_in(c, polys, t, t0, dur, col, 1.8, seed_pt=(x, y + 0.5 * s))
        else:
            stroke_polys(c, polys, col, 1.8, 1.0)
    if t0 is not None:
        ev(t0, "hydraulic" if robot else "form", t, x)
    return j


def headset(j, s, face):
    hx, hy = j["head"]
    hr = 0.062 * s
    x0 = hx + 0.1 * hr if face > 0 else hx - 1.45 * hr
    return [mg.rrect_pts(x0, hy - 0.62 * hr, 1.35 * hr, 0.85 * hr, 0.25 * hr, 4), ellipse(hx, hy - 0.2 * hr, 1.08 * hr, 0.36 * hr, 0, 360, 32)]


def helmet(j, s, face):
    hx, hy = j["head"]
    hr = 0.062 * s
    return [ellipse(hx, hy - 0.15 * hr, 1.3 * hr, 1.05 * hr, 180, 360, 28), P([(hx - 1.45 * hr, hy - 0.12 * hr), (hx + 1.45 * hr, hy - 0.12 * hr)])]


def pad(j, s):
    """A controller held in both hands."""
    x = (j["lhand"][0] + j["rhand"][0]) / 2
    y = (j["lhand"][1] + j["rhand"][1]) / 2
    w = 0.16 * s
    return [mg.rrect_pts(x - w / 2, y - 0.22 * w, w, 0.44 * w, 0.2 * w, 4), ellipse(x - 0.22 * w, y, 0.08 * w, 0.08 * w, 0, 360, 12),
            ellipse(x + 0.22 * w, y, 0.08 * w, 0.08 * w, 0, 360, 12)]


def signal(c, p0, p1, t, a=1.0, bend=-150, n=64, frac=1.0):
    """The thread from a person to a machine: a dashed curve with pulses running from p0 to p1."""
    if a <= 0.01 or frac <= 0:
        return
    mid = ((p0[0] + p1[0]) / 2, min(p0[1], p1[1]) + bend)
    q = bezier(p0, mid, p1, n)[: max(2, int(n * frac))]
    path = skia.Path()
    for i in range(0, len(q) - 1, 2):
        path.moveTo(*q[i]); path.lineTo(*q[i + 1])
    c.drawPath(path, mg.stroke(GLOW, 1.7, 0.85 * a))
    if frac >= 1:
        for k in range(3):
            u = (t * 0.8 + k / 3) % 1.0
            x, y = q[int(u * (len(q) - 1))]
            c.drawCircle(float(x), float(y), 5.0, mg.fill(WHITE, a))


def burst(c, x, y, t, t0, r=60, a=1.0):
    """An impact: short lines flying out and fading."""
    k = seg(t, t0, t0 + 0.32)
    if k <= 0 or k >= 1:
        return
    p = mg.stroke(WHITE, 2.2, a * (1 - k))
    for i in range(9):
        ang = i * 2 * math.pi / 9 + 0.3
        r0, r1 = r * (0.3 + 0.9 * ease(k, "o")), r * (0.6 + 1.3 * ease(k, "o"))
        c.drawLine(x + r0 * math.cos(ang), y + r0 * math.sin(ang), x + r1 * math.cos(ang), y + r1 * math.sin(ang), p)


def morph_figs(c, pa, pb, k, col=WHITE):
    Sa, Sb = segs(pa, 720), segs(pb, 720)
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
    ev(t0, "form", t, cx)


def roll(c, a_txt, b_txt, size, cx, cy, t, t0, t_m, a=1.0):
    """A number that forms, then morphs into another (2026 -> 2021, 50,000 -> ~112,000), then fills with chrome."""
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
        ev(t_m, "morph", t, cx)
        ev(t_m + 0.75, "thock", t, cx)


# the cage: an octagon, the posts, the top rail, chain link on the back walls
CAGE_C, CAGE_RX, CAGE_RY, CAGE_H = (960.0, 790.0), 640.0, 110.0, 360.0


def cage():
    ang = np.radians(np.arange(8) * 45 + 22.5)
    fl = [(CAGE_C[0] + CAGE_RX * math.cos(a), CAGE_C[1] + CAGE_RY * math.sin(a)) for a in ang]
    top = [(x, y - CAGE_H) for x, y in fl]
    polys = [P(fl + [fl[0]]), P(top + [top[0]])] + [P([p, q]) for p, q in zip(fl, top)]
    mesh = []
    for i in range(8):
        a0, a1 = ang[i], ang[(i + 1) % 8]
        if math.sin(a0) + math.sin(a1) > -0.2:           # the front and side walls stay clear (the fighters)
            continue
        p0, p1 = np.array(fl[i]), np.array(fl[(i + 1) % 8])
        for u in np.linspace(-1, 1, 13):                 # diagonals both ways across the wall
            for sgn in (1, -1):
                pts = []
                for v in np.linspace(0, 1, 12):
                    uu = u + sgn * v
                    if 0 <= uu <= 1:
                        b = p0 + (p1 - p0) * uu
                        pts.append((b[0], b[1] - CAGE_H * v))
                if len(pts) > 1:
                    mesh.append(P(pts))
    return polys, mesh


CAGE, MESH = cage()


def ring(cx, fy, w, d, h):
    """A boxing ring in perspective: the floor, the apron, four posts, three ropes."""
    bl, br, fl, fr = (cx - 0.78 * w, fy - d), (cx + 0.78 * w, fy - d), (cx - w, fy), (cx + w, fy)
    out = [P([bl, br, fr, fl, bl]), P([fl, (fl[0], fl[1] + 36), (fr[0], fr[1] + 36), fr])]
    for p, hh in ((bl, 0.8 * h), (br, 0.8 * h), (fl, h), (fr, h)):
        out.append(P([p, (p[0], p[1] - hh)]))
    for k in (0.42, 0.66, 0.9):
        out.append(P([(bl[0], bl[1] - 0.8 * h * k), (br[0], br[1] - 0.8 * h * k), (fr[0], fr[1] - h * k), (fl[0], fl[1] - h * k),
                      (bl[0], bl[1] - 0.8 * h * k)]))
    return out


RING = ring(960, 800, 540, 170, 250)


def dog(x, y, s, ph=0.0, amp=0.0):
    """A robot dog side on, facing right: (x, y) = the middle of its body, s = body length; ph/amp = the walk.
    Returns (lines, closed)."""
    body_ = mg.rrect_pts(x - 0.5 * s, y - 0.14 * s, s, 0.28 * s, 0.1 * s, 5)
    head = mg.rrect_pts(x + 0.47 * s, y - 0.33 * s, 0.3 * s, 0.2 * s, 0.06 * s, 4)
    out = [body_, head, P([(x + 0.63 * s, y - 0.25 * s), (x + 0.74 * s, y - 0.25 * s)]),
           P([(x + 0.42 * s, y - 0.1 * s), (x + 0.52 * s, y - 0.16 * s)]), P([(x - 0.3 * s, y - 0.02 * s), (x + 0.3 * s, y - 0.02 * s)])]
    closed = [body_, head]
    w = 0.036 * s
    for hx_, off, far in ((x + 0.36 * s, 0.0, False), (x + 0.3 * s, math.pi, True), (x - 0.36 * s, math.pi, False), (x - 0.42 * s, 0.0, True)):
        th = math.radians(amp * math.sin(ph + off))
        lift = max(0.0, math.sin(ph + off + math.pi / 2)) * amp / 30 * 0.06 * s
        hip = np.array([hx_, y + 0.1 * s])
        knee = hip + 0.3 * s * np.array([math.sin(th - 0.42), math.cos(th - 0.42)])
        foot = knee + 0.3 * s * np.array([math.sin(th * 0.6 + 0.42), math.cos(th * 0.6 + 0.42)]) - np.array([0, lift])
        for a_, b_ in ((hip, knee), (knee, foot)):
            v = b_ - a_
            n2 = np.array([-v[1], v[0]]) / (np.linalg.norm(v) + 1e-9) * w * (0.8 if far else 1.0)
            limb = P([a_ + n2, b_ + n2 * 0.8, b_ - n2 * 0.8, a_ - n2, a_ + n2])
            out.append(limb)
            if not far:
                closed.append(limb)
        out.append(ellipse(*knee, w * 1.2, w * 1.2, 0, 360, 14))
        out.append(ellipse(foot[0], foot[1], w * 1.1, w * 0.8, 0, 360, 14))
    return out, closed


def rifle(x, y, s):
    """A rifle on a mount, pointing right: (x, y) = where the mount meets the back, s = length."""
    top = y - 0.16 * s
    return [mg.rrect_pts(x - 0.05 * s, top - 0.025 * s, 0.62 * s, 0.05 * s, 0.02 * s, 3),
            mg.rrect_pts(x - 0.3 * s, top - 0.06 * s, 0.34 * s, 0.11 * s, 0.02 * s, 3),
            P([(x - 0.3 * s, top - 0.04 * s), (x - 0.5 * s, top - 0.02 * s), (x - 0.52 * s, top + 0.07 * s), (x - 0.3 * s, top + 0.05 * s)]),
            P([(x - 0.12 * s, top + 0.05 * s), (x - 0.1 * s, top + 0.16 * s), (x - 0.03 * s, top + 0.15 * s), (x - 0.05 * s, top + 0.05 * s)]),
            mg.rrect_pts(x - 0.2 * s, top - 0.12 * s, 0.2 * s, 0.05 * s, 0.02 * s, 3),
            P([(x - 0.12 * s, y), (x - 0.12 * s, top + 0.05 * s)]), P([(x + 0.05 * s, y), (x + 0.05 * s, top + 0.02 * s)])]


def ugv(x, y, s, ph=0.0):
    """A tracked ground robot side on: (x, y) = the ground under its middle, s = length. Returns (lines, closed)."""
    track = mg.rrect_pts(x - 0.5 * s, y - 0.24 * s, s, 0.24 * s, 0.12 * s, 8)
    body_ = mg.rrect_pts(x - 0.42 * s, y - 0.44 * s, 0.84 * s, 0.2 * s, 0.03 * s, 3)
    out = [track, body_, P([(x - 0.34 * s, y - 0.44 * s), (x - 0.37 * s, y - 0.7 * s)]),
           mg.rrect_pts(x + 0.3 * s, y - 0.55 * s, 0.1 * s, 0.11 * s, 0.02 * s, 2)]
    for k in (-0.375, -0.125, 0.125, 0.375):
        cx_, cy_ = x + k * s, y - 0.12 * s
        r = 0.08 * s
        out.append(ellipse(cx_, cy_, r, r, 0, 360, 16))
        out.append(P([(cx_ + r * 0.8 * math.cos(ph), cy_ + r * 0.8 * math.sin(ph)), (cx_ - r * 0.8 * math.cos(ph), cy_ - r * 0.8 * math.sin(ph))]))
    return out, [body_]


def crate(x, y, s):
    x0, y0, w, h = x - 0.22 * s, y - 0.72 * s, 0.4 * s, 0.28 * s
    return [P([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)]), P([(x0, y0), (x0 + w, y0 + h)]),
            P([(x0 + w, y0), (x0, y0 + h)])]


def stretcher(x, y, s):
    y0 = y - 0.5 * s
    return [mg.rrect_pts(x - 0.5 * s, y0, s, 0.06 * s, 0.03 * s, 3), P([(x - 0.56 * s, y0 + 0.03 * s), (x - 0.5 * s, y0 + 0.03 * s)]),
            P([(x + 0.5 * s, y0 + 0.03 * s), (x + 0.56 * s, y0 + 0.03 * s)]),
            P([(x - 0.06 * s, y0 - 0.16 * s), (x - 0.06 * s, y0 - 0.02 * s)]), P([(x - 0.13 * s, y0 - 0.09 * s), (x + 0.01 * s, y0 - 0.09 * s)])]


def patriot(x, top, bot, r):
    """An interceptor, nose up."""
    nose = 3.2 * r
    return [P([(x - r, top + nose), (x - r, bot), (x + r, bot), (x + r, top + nose)]),
            bezier((x - r, top + nose), (x - r, top + 0.3 * nose), (x, top), 30), bezier((x + r, top + nose), (x + r, top + 0.3 * nose), (x, top), 30),
            P([(x - r, bot - 3.6 * r), (x - 2.5 * r, bot + 0.2 * r), (x - r, bot)]), P([(x + r, bot - 3.6 * r), (x + 2.5 * r, bot + 0.2 * r), (x + r, bot)]),
            P([(x - r, top + nose + 0.5 * r), (x + r, top + nose + 0.5 * r)]), P([(x - r, bot - 5.5 * r), (x + r, bot - 5.5 * r)]),
            P([(x - r, top + 0.45 * (bot - top)), (x - 1.8 * r, top + 0.45 * (bot - top) + 1.2 * r), (x - r, top + 0.45 * (bot - top) + 2.2 * r)]),
            P([(x + r, top + 0.45 * (bot - top)), (x + 1.8 * r, top + 0.45 * (bot - top) + 1.2 * r), (x + r, top + 0.45 * (bot - top) + 2.2 * r)])]


def shahed(cx, cy, s):
    """A delta-wing one-way drone, seen from above, nose up."""
    wing = P([(cx - 0.06 * s, cy - 0.22 * s), (cx - 0.5 * s, cy + 0.3 * s), (cx - 0.5 * s, cy + 0.4 * s), (cx + 0.5 * s, cy + 0.4 * s),
              (cx + 0.5 * s, cy + 0.3 * s), (cx + 0.06 * s, cy - 0.22 * s)])
    fus = mg.rrect_pts(cx - 0.065 * s, cy - 0.58 * s, 0.13 * s, 1.0 * s, 0.06 * s, 5)
    return [wing, fus, P([(cx - 0.5 * s, cy + 0.12 * s), (cx - 0.5 * s, cy + 0.44 * s)]), P([(cx + 0.5 * s, cy + 0.12 * s), (cx + 0.5 * s, cy + 0.44 * s)]),
            P([(cx - 0.13 * s, cy + 0.47 * s), (cx + 0.13 * s, cy + 0.47 * s)])], [wing, fus]


def page(x, y, w, h):
    out = [P([(x, y), (x + 0.82 * w, y), (x + w, y + 0.18 * w), (x + w, y + h), (x, y + h), (x, y)]),
           P([(x + 0.82 * w, y), (x + 0.82 * w, y + 0.18 * w), (x + w, y + 0.18 * w)])]
    for k in range(7):
        yy = y + (0.28 + 0.1 * k) * h
        out.append(P([(x + 0.12 * w, yy), (x + (0.45 + 0.4 * ((k * 37) % 7) / 7) * w, yy)]))
    return out


def stage():
    floor = [P([(420, 812), (1500, 812)]), P([(360, 850), (1560, 850)]), P([(420, 812), (360, 850)]), P([(1500, 812), (1560, 850)])]
    cone = P([(935, 100), (985, 100), (1130, 812), (790, 812), (935, 100)])
    return floor, cone


_IMG = {}


def mac_wall(key, cols, rows, cw, ch, s):
    """A block of small Big Macs, drawn once and reused: (image, width, height)."""
    if key not in _IMG:
        w, h = int(cols * cw), int(rows * ch + 2 * s)
        sf = skia.Surface(w, h)
        c = sf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
        for r in range(rows):
            for k in range(cols):
                mini_mac(c, (k + 0.5) * cw, h - (r + 1) * ch + 0.62 * s - 0.1 * s, s, 1.0)
        _IMG[key] = (sf.makeImageSnapshot(), w, h)
    return _IMG[key]


def draw_wall(c, img, x0, ybot, frac, a=1.0):
    """Show the bottom `frac` of a Big Mac block (it builds up row by row)."""
    im, w, h = img
    if frac <= 0 or a <= 0:
        return
    hh = h * min(1.0, frac)
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, skia.Rect.MakeLTRB(0, h - hh, w, h), skia.Rect.MakeLTRB(x0, ybot - hh, x0 + w, ybot),
                    skia.SamplingOptions(skia.FilterMode.kLinear), p)


# ---------------------------------------------------------------- GROUND: the fight
T_DATE = wd("cage", "eighteenth") - 0.08
T_SF, T_MAN, T_CAGE, T_SIX = wd("cage", "San"), wd("cage", "man"), wd("cage", "cage"), wd("cage", "six-foot")
T_KG = wd("lost", "80")
HITS = [wd("lost", "knocks"), wd("lost", "again"), wd("lost", "again", 1)]
T_HAND, T_STOP = wd("lost", "hand"), wd("lost", "stopped")
T_CLIPS = ls("pilot")
S_MAN, S_BOT = 400, 430
TRAILS.append((HITS[0] - 0.2, HITS[-1] + 0.5))


def man_x(t):
    return keys(t, [(T_MAN - 0.1, 470), (T_MAN + 0.9, 680), (HITS[0] + 0.03, 680), (HITS[0] + 0.33, 560), (HITS[1] + 0.03, 560),
                    (HITS[1] + 0.3, 470), (HITS[2] + 0.03, 470), (HITS[2] + 0.28, 420)])


def bot_x(t):
    return keys(t, [(HITS[0] - 0.45, 1260), (HITS[0] - 0.06, 890), (HITS[1] - 0.4, 890), (HITS[1] - 0.06, 770), (HITS[2] - 0.3, 770),
                    (HITS[2] - 0.05, 690), (HITS[2] + 0.5, 690), (HITS[2] + 1.1, 800)])


def bot_pose(t):
    k = max(bump(t, h - 0.14, h, h + 0.3) for h in HITS)
    p = pose_mix(GUARD, PUNCH, k)
    return pose_mix(p, STAND, ease(seg(t, HITS[-1] + 0.6, HITS[-1] + 1.2)))


def fight(c, t):
    a = win(t, T_DATE - 0.1, T_CLIPS + 0.8, 0.2, 0.7)
    if a <= 0:
        return
    kd = 1 - ease(seg(t, T_MAN - 0.2, T_MAN + 0.4))                  # the date card, then the cage
    if kd > 0:
        with layer(c, kd):
            bignum(c, t, "18 SEP 2026", 110, CX, 300, T_DATE)
            label(c, "SAN FRANCISCO · HUMAN VS HUMANOID", CX, 400, t, T_SF, 22, SOFT, a=kd)
    if t < T_CAGE - 0.4:
        return
    with layer(c, a):
        lines_in(c, CAGE, t, T_CAGE - 0.35, 0.9, SOFT, 1.5, seed_pt=(CX, 900))
        stroke_polys(c, MESH, SOFT, 1.0, 0.4 * ease(seg(t, T_CAGE + 0.3, T_CAGE + 1.2)))
        ev(T_CAGE - 0.35, "form", t, CX)
        hurt = ease(seg(t, T_HAND - 0.2, T_HAND + 0.3))
        kh = max(bump(t, h + 0.02, h + 0.14, h + 0.55) for h in HITS)
        mp = pose_mix(STAND, GUARD, ease(seg(t, T_SIX - 0.3, T_SIX + 0.2)))
        mp = pose_mix(pose_mix(mp, HIT, kh), HURT, hurt)
        jm = body(c, man_x(t), S_MAN, mp, 1, t, T_MAN - 0.1, a=1.0)
        if t >= T_SIX - 0.05:
            jb = body(c, bot_x(t), S_BOT, bot_pose(t), -1, t, T_SIX - 0.05, robot=True)
            for h in HITS:
                burst(c, jb["lhand"][0] - 10, jb["lhand"][1], t, h, 55)
                ev(h, "thud", t, jb["lhand"][0])
                ev(h - 0.4, "servo", t, bot_x(t))
            kb = win(t, T_SIX + 0.15, T_KG + 0.9)                       # six feet
            if kb > 0:
                x = bot_x(t) + 150
                top = jb["head"][1] - 0.075 * S_BOT
                c.drawLine(x, GROUND_Y, x, top, mg.stroke(SOFT, 1.5, kb))
                for yy in (GROUND_Y, top):
                    c.drawLine(x - 12, yy, x + 12, yy, mg.stroke(SOFT, 1.5, kb))
                label(c, "6 FT", x + 22, (GROUND_Y + top) / 2 + 8, t, T_SIX + 0.25, 22, GLOW, "left", a=a * kb)
            label(c, "ABOUT 80 KG OF METAL", bot_x(t), jb["head"][1] - 90, t, T_KG, 22, GLOW, a=a * win(t, T_KG, HITS[0] - 0.1))
        if t >= T_HAND - 0.1:
            hx, hy = jm["rhand"]
            kk = win(t, T_HAND - 0.1, T_CLIPS + 0.4)
            c.drawCircle(hx, hy, 34, mg.stroke(GLOW, 2.0, kk))
            label(c, "HAND INJURY", hx, hy - 52, t, T_HAND, 20, GLOW, a=a * kk)
            ev(T_HAND, "pop", t, hx)
        label(c, "FIGHT STOPPED", CX, 250, t, T_STOP, 26, WHITE, a=a)
        ev(T_STOP, "confirm", t, CX)


# ---------------------------------------------------------------- GROUND: the pilot, the suit, how close
T_ROBOT_ALONE = wd("pilot", "robot")
T_DEC = wd("pilot", "deciding")
T_PERSON, T_VR = wd("pilot", "person"), wd("pilot", "VR")
T_SUIT = ls("suit")
T_EARLIER, T_MOST, T_TOO = wd("suit", "earlier"), wd("suit", "most"), wd("suit", "person")
T_CLOSE0, T_CLOSE = ls("close"), wd("close", "close")
T_TESLA = ls("tesla")
PX = 1390                                              # the pilot, backstage right


def puppet(t):
    """The pilot's arms, which the robot copies a beat later."""
    w = 2.3
    return dict(PILOT, lean=4 + 3 * math.sin(w * t), ls=55 + 28 * math.sin(w * t), le=70 + 25 * math.sin(w * t + 0.8),
                rs=45 + 26 * math.sin(w * t + 1.3), re=80 + 20 * math.sin(w * t + 2.0))


def robot_x2(t):
    return keys(t, [(T_CLIPS, 800), (T_CLIPS + 0.9, 760)])


def pilot(c, t):
    if not (T_CLIPS - 0.05 <= t < T_TESLA + 0.9):
        return
    # the robot: alone, then the puppet, then (2026 -> 2021) a person in a suit
    k_pup = ease(seg(t, T_PERSON + 0.4, T_PERSON + 1.0)) * (1 - ease(seg(t, T_SUIT, T_SUIT + 0.5)))
    rp = pose_mix(STAND, puppet(t - 0.18), k_pup)
    x_r = robot_x2(t)
    if t < T_TOO - 0.05:
        jr = body(c, x_r, S_BOT, rp, -1, t, None, robot=True)
        label(c, "NOT DECIDING ANYTHING", x_r, jr["head"][1] - 90, t, T_DEC, 22, GLOW, a=win(t, T_DEC, T_PERSON + 0.2))
    else:                                                               # the robot becomes a person in a suit
        pa, _ = figure(x_r, hips_y(S_BOT), S_BOT, STAND, -1, robot=True)
        pb, _ = figure(x_r, hips_y(S_MAN), S_MAN, STAND, 1, mask=True)
        k = seg(t, T_TOO - 0.05, T_TOO + 0.75)
        if k < 1:
            morph_figs(c, pa, pb, k)
            ev(T_TOO - 0.05, "morph", t, x_r)
    # the pilot backstage, in a VR headset, and the thread
    ap = win(t, T_PERSON - 0.1, T_SUIT + 0.6, 0.2, 0.5)
    if ap > 0:
        jp = body(c, PX, 380, puppet(t) if t > T_PERSON + 0.4 else pose_mix(STAND, puppet(t), ease(seg(t, T_PERSON, T_PERSON + 0.4))),
                  -1, t, T_PERSON - 0.1, a=ap)
        if t >= T_VR - 0.1:
            lines_in(c, headset(jp, 380, -1), t, T_VR - 0.1, 0.4, WHITE, 2.0, a=ap)
            ev(T_VR - 0.1, "latch", t, PX)
        label(c, "BACKSTAGE · A VR HEADSET", PX, jp["head"][1] - 90, t, T_VR + 0.1, 22, GLOW, a=ap)
        jr_ = figure(x_r, hips_y(S_BOT), S_BOT, rp, -1, robot=True)[1]
        signal(c, (PX - 40, jp["head"][1]), (x_r + 30, jr_["head"][1]), t, ap * ease(seg(t, T_PERSON + 0.5, T_PERSON + 1.0)),
               frac=ease(seg(t, T_PERSON + 0.5, T_PERSON + 1.1)))
        ev(T_PERSON + 0.5, "link", t, CX)
    # 2026 rolls back to 2021
    ay = win(t, T_SUIT, T_CLOSE0 - 0.1, 0.2, 0.5)
    if ay > 0:
        roll(c, "2026", "2021", 150, CX, 250, t, T_SUIT, T_EARLIER, ay)
        label(c, "THE MOST FAMOUS ROBOT IN THE WORLD", CX, 360, t, T_MOST, 22, SOFT, a=ay)
    ac = win(t, T_CLOSE0 - 0.05, T_TESLA + 0.3, 0.3, 0.5)
    if ac > 0:
        body(c, 1180, S_BOT, STAND, -1, t, T_CLOSE0 - 0.05, robot=True, a=ac)
        y = 520
        c.drawLine(900, y, 1100, y, mg.stroke(GLOW, 1.8, ac))
        for x, d in ((900, 1), (1100, -1)):
            c.drawLine(x, y, x + d * 16, y - 10, mg.stroke(GLOW, 1.8, ac)); c.drawLine(x, y, x + d * 16, y + 10, mg.stroke(GLOW, 1.8, ac))
        label(c, "HOW CLOSE?", CX, 360, t, T_CLOSE, 26, WHITE, a=ac)


def dancer(c, t):
    """The person in the suit: from the morph, through "how close?", onto the Tesla stage, dancing."""
    if not (T_TOO + 0.75 <= t < T_BOX + 0.35):
        return
    a = 1 - ease(seg(t, T_BOX - 0.15, T_BOX + 0.35))
    x_h = keys(t, [(T_TESLA - 0.2, robot_x2(t)), (T_TESLA + 2.4, 960)])
    k = ease(seg(t, wd("tesla", "stage") - 0.3, wd("tesla", "stage") + 0.3))
    body(c, x_h, S_MAN, pose_mix(STAND, dance(t), k), 1, t, None, mask=True, a=a,
         y=hips_y(S_MAN) - 8 * abs(math.sin(2 * math.pi * 0.8 * t)) * k)


def dance(t):
    w = 2 * math.pi * 0.8
    s1, s2 = math.sin(w * t), math.sin(2 * w * t)
    return dict(lean=-4 + 6 * s1, head=-6 + 6 * s1, ls=150 + 20 * s1, le=25 + 15 * s2, rs=-95 + 70 * math.sin(w * t + math.pi),
                re=-20 + 40 * s2, lh=18 + 14 * s1, lk=-28 - 14 * s1, rh=-10 + 10 * math.sin(w * t + math.pi), rk=-4)


# ---------------------------------------------------------------- MECHANISM
T_AUG, T_TESLA_W, T_STAGE, T_BODYSUIT = ls("tesla"), wd("tesla", "Tesla"), wd("tesla", "stage"), wd("tesla", "person")
T_BOX = ls("boxing")


def tesla(c, t):
    a = win(t, T_AUG - 0.05, T_BOX + 0.3, 0.2, 0.5)
    if a <= 0:
        return
    kd = 1 - ease(seg(t, T_STAGE - 0.5, T_STAGE))
    if kd > 0:
        with layer(c, kd * a):
            bignum(c, t, "19 AUG 2021", 110, CX, 250, T_AUG + 0.04)
            label(c, "TESLA AI DAY · THE TESLA BOT ANNOUNCED", CX, 345, t, T_TESLA_W, 22, SOFT, a=kd * a)
    if t >= T_STAGE - 0.1:
        floor, cone = stage()
        with layer(c, a):
            k = ease(seg(t, T_STAGE, T_STAGE + 0.6))
            closed_fill(c, [cone], 1.0, mg.fill(GLOW, 0.10 * k))
            lines_in(c, floor, t, T_STAGE - 0.1, 0.6, SOFT, 1.5, seed_pt=(CX, 830))
            ev(T_STAGE, "swell", t, CX)
            label(c, "A PERSON IN A WHITE BODYSUIT", CX, 250, t, T_BODYSUIT, 24, WHITE, a=a)


T_CN, T_BOXW, T_FOUR, T_STEER, T_HUMAN = wd("boxing", "Chinese"), wd("boxing", "boxing"), wd("boxing", "Four"), wd("boxing", "steered"), wd("boxing", "human")
T_SPLIT = ls("split")
EX = [T_BOXW - 0.3 + 0.62 * k for k in range(4)]                  # the exchange: who punches when
TRAILS.append((EX[0] - 0.2, EX[-1] + 0.5))
ROW_X = [510, 810, 1110, 1410]


def boxing(c, t):
    a = win(t, T_BOX - 0.05, T_SPLIT + 0.2, 0.2, 0.5)
    if a <= 0:
        return
    k1 = 1 - ease(seg(t, T_FOUR - 0.2, T_FOUR + 0.25))
    if k1 > 0:
        with layer(c, a * k1):
            bignum(c, t, "MAY 2025", 110, CX, 250, T_BOX + 0.05)
            label(c, "CHINA'S FIRST HUMANOID ROBOT BOXING · STATE TV", CX, 345, t, T_CN, 22, SOFT, a=a * k1)
            if t >= T_CN - 0.1:
                lines_in(c, RING, t, T_CN - 0.1, 0.8, SOFT, 1.5, seed_pt=(CX, 900))
                ev(T_CN - 0.1, "form", t, CX)
            t_b = wd("boxing", "humanoid") - 0.1
            if t >= t_b:
                pl, pr = GUARD, GUARD
                for k, h in enumerate(EX):
                    if k % 2 == 0:
                        pl = pose_mix(pl, PUNCH, bump(t, h - 0.12, h, h + 0.28))
                        pr = pose_mix(pr, HIT, 0.5 * bump(t, h + 0.02, h + 0.12, h + 0.45))
                    else:
                        pr = pose_mix(pr, PUNCH, bump(t, h - 0.12, h, h + 0.28))
                        pl = pose_mix(pl, HIT, 0.5 * bump(t, h + 0.02, h + 0.12, h + 0.45))
                    ev(h, "clack", t, CX)
                bob = 6 * math.sin(2 * math.pi * 1.6 * t)
                body(c, 830, 300, pl, 1, t, t_b, robot=True, y=hips_y(300) - 16 + bob)
                body(c, 1090, 300, pr, -1, t, t_b + 0.1, robot=True, y=hips_y(300) - 16 - bob)
    if t >= T_FOUR - 0.1:                                             # four robots, four trainers
        k2 = ease(seg(t, T_FOUR - 0.1, T_FOUR + 0.3))
        with layer(c, a * k2):
            label(c, "UNITREE G1 · 132 CM · 35 KG", CX, 235, t, T_FOUR + 0.2, 22, GLOW, a=a * k2)
            label(c, "EACH ONE STEERED BY A HUMAN TRAINER", CX, 280, t, T_HUMAN - 0.1, 22, SOFT, a=a * k2)
            for k, x in enumerate(ROW_X):
                pb = pose_mix(GUARD, PUNCH, bump((t + 0.37 * k) % 1.4, 0.2, 0.34, 0.62))
                jb = body(c, x, 220, pb, 1 if k < 2 else -1, t, T_FOUR - 0.05 + 0.1 * k, robot=True, y=440)
                jt = body(c, x, 190, dict(PILOT, ls=50, le=75, rs=40, re=85), 1 if k < 2 else -1, t, T_STEER - 0.15 + 0.08 * k, y=GROUND_Y - 0.48 * 190)
                if t >= T_STEER + 0.2:
                    stroke_polys(c, pad(jt, 190), WHITE, 1.6, ease(seg(t, T_STEER + 0.2, T_STEER + 0.5)))
                    signal(c, (jt["head"][0], jt["head"][1] - 20), (jb["hip"][0], jb["hip"][1] + 70), t + 0.2 * k,
                           ease(seg(t, T_HUMAN, T_HUMAN + 0.4)), bend=-10, n=24, frac=ease(seg(t, T_HUMAN, T_HUMAN + 0.4)))
                ev(T_STEER + 0.2 + 0.08 * k, "tick", t, x)


T_UP, T_HITW, T_BACK, T_OWN = wd("split", "upright"), wd("split", "hit"), wd("split", "back"), wd("split", "own")
T_DECIDE, T_PUNCH, T_WHO = ls("decide"), wd("decide", "punch"), wd("decide", "who")
T_PRICE = ls("price")


def check(c, x, y, a):
    c.drawLine(x, y - 8, x + 6, y, mg.stroke(GLOW, 2.2, a)); c.drawLine(x + 6, y, x + 18, y - 16, mg.stroke(GLOW, 2.2, a))


def split(c, t):
    a = win(t, T_SPLIT - 0.05, T_PRICE + 0.3, 0.2, 0.4)
    if a <= 0:
        return
    with layer(c, a):
        lines_in(c, [P([(CX, 140), (CX, 830)])], t, T_SPLIT, 0.5, SOFT, 1.4, seed_pt=(CX, 140))
        ev(T_SPLIT, "scan", t, CX)
        label(c, "THE MACHINE, ON ITS OWN", 600, 190, t, T_SPLIT + 0.35, 24, WHITE, a=a)
        label(c, "A PERSON", 1320, 190, t, T_SPLIT + 0.35, 24, WHITE, a=a)
        for k, (tt, txt) in enumerate(((T_UP, "STAYING UPRIGHT"), (T_HITW, "TAKING A HIT"), (T_BACK, "GETTING BACK UP"))):
            label(c, txt, 610, 250 + 38 * k, t, tt, 20, GLOW, "left", a=a)
            if t >= tt + 0.3:
                check(c, 575, 250 + 38 * k, a * ease(seg(t, tt + 0.3, tt + 0.45)))
            ev(tt + 0.3, "tick", t, 600)
        kh = bump(t, T_HITW - 0.02, T_HITW + 0.15, T_BACK + 0.4)
        jr = body(c, 600, 380, pose_mix(STAND, HIT, 0.75 * kh), 1, t, T_SPLIT + 0.2, robot=True)
        burst(c, jr["neck"][0] + 40, jr["neck"][1] + 30, t, T_HITW, 50)
        ev(T_HITW, "thud", t, 600)
        ev(T_BACK, "servo", t, 600)
        if t >= T_DECIDE - 0.1:
            jp = body(c, 1320, 380, dict(PILOT, ls=50, le=75, rs=40, re=85), -1, t, T_DECIDE - 0.1)
            if t >= T_DECIDE + 0.4:
                stroke_polys(c, pad(jp, 380), WHITE, 1.8, ease(seg(t, T_DECIDE + 0.4, T_DECIDE + 0.7)))
            for k, (tt, txt) in enumerate(((T_PUNCH, "WHEN TO PUNCH"), (T_WHO, "AND WHO"))):
                label(c, txt, 1330, 250 + 38 * k, t, tt, 20, GLOW, "left", a=a)
                ev(tt, "tick", t, 1320)


T_13K, T_MACS0, T_MACS = wd("price", "thirteen"), wd("price", "About"), wd("price", "Big")
T_DOGS = ls("dogs")
GLINTS.append((T_13K + 1.3, 0.9))
WALL = None


def price(c, t):
    global WALL
    a = win(t, T_PRICE - 0.3, T_DOGS + 0.7, 0.01, 0.6)
    if a <= 0:
        return
    if t < T_DOGS + 0.1:                                               # the robot (it becomes the dog next)
        x = keys(t, [(T_PRICE - 0.3, 600), (T_PRICE + 0.5, 520)])
        jr = body(c, x, 380, STAND, 1, t, None, robot=True)
        label(c, "UNITREE G1", x, jr["head"][1] - 80, t, wd("price", "robots"), 22, GLOW, a=win(t, T_PRICE, T_DOGS))
    ka = win(t, T_13K - 0.1, T_DOGS + 0.6, 0.2, 0.6)
    if ka > 0:
        with layer(c, ka):
            bignum(c, t, "$13,500", 120, 1190, 290, T_13K)
            if WALL is None:
                WALL = mac_wall("g1", 50, 44, 14.8, 9.1, 6.2)
            draw_wall(c, WALL, 820, 842, seg(t, T_MACS0 + 0.1, T_MACS + 0.3))
            for r in range(0, 44, 4):
                ev(T_MACS0 + 0.1 + (T_MACS + 0.2 - T_MACS0) * r / 44, "tick", t, 1190)
            label(c, "= 2,200 BIG MACS", 1190, 395, t, T_MACS, 26, WHITE, a=ka)


# ---------------------------------------------------------------- NOW
T_DONT, T_CHINA, T_RIFLE = wd("dogs", "don't"), wd("dogs", "China's"), wd("dogs", "rifle")
T_WALK, T_REMOTE = ls("remote"), wd("remote", "remote")
T_UKR = ls("ukraine")
DOG_S = 420


def dog_x(t):
    return keys(t, [(T_WALK, 960), (T_UKR + 0.3, 1170)])


def dog_ph(t):
    return 2 * math.pi * 1.1 * max(0.0, t - T_WALK)


def dogs(c, t):
    a = win(t, T_DOGS, T_UKR + 0.4, 0.01, 0.5)
    if a <= 0:
        return
    yd = 610
    with layer(c, a):
        k = seg(t, T_DOGS + 0.1, T_DONT + 0.2)
        dl, dc = dog(dog_x(t), yd, DOG_S, dog_ph(t), 14 * ease(seg(t, T_WALK, T_WALK + 0.4)))
        if k < 1:                                                      # the humanoid becomes the dog
            pa, _ = figure(520, hips_y(380), 380, STAND, 1, robot=True)
            morph_figs(c, pa, dl, k)
            ev(T_DOGS + 0.1, "morph", t, 700)
        else:
            closed_fill(c, dc, 1.0, mg.fill(MID, 0.3))
            stroke_polys(c, dl, WHITE, 1.8)
        label(c, "GOLDEN DRAGON 2024 · CHINA AND CAMBODIA", CX, 230, t, T_CHINA, 22, SOFT, a=a)
        if t >= T_RIFLE - 0.1:
            lines_in(c, rifle(dog_x(t) - 0.05 * DOG_S, yd - 0.14 * DOG_S, 0.75 * DOG_S), t, T_RIFLE - 0.1, 0.45, WHITE, 1.8)
            ev(T_RIFLE, "latch", t, dog_x(t))
            label(c, "A RIFLE ON A ROBOT DOG", CX, 275, t, T_RIFLE + 0.2, 24, WHITE, a=a)
        if t >= T_REMOTE - 0.45:
            jo = body(c, 420, 330, dict(PILOT, ls=50, le=75, rs=40, re=85), 1, t, T_REMOTE - 0.45)
            if t >= T_REMOTE:
                stroke_polys(c, pad(jo, 330), WHITE, 1.8, ease(seg(t, T_REMOTE, T_REMOTE + 0.3)))
            signal(c, (450, jo["head"][1]), (dog_x(t) + 0.55 * DOG_S, yd - 0.34 * DOG_S), t, ease(seg(t, T_REMOTE + 0.1, T_REMOTE + 0.4)),
                   bend=-120, frac=ease(seg(t, T_REMOTE + 0.1, T_REMOTE + 0.5)))
            label(c, "A REMOTE OPERATOR", 420, jo["head"][1] - 80, t, T_REMOTE + 0.2, 22, GLOW, a=a)
            ev(T_REMOTE + 0.1, "link", t, 700)
        ev(T_WALK + 0.1, "servo", t, dog_x(t))


T_APRIL, T_50K, T_GROUND = ls("ukraine"), wd("ukraine", "fifty"), wd("ukraine", "ground")
T_MIS, T_112, T_SUP, T_EVAC = ls("missions"), wd("missions", "hundred"), wd("missions", "supply"), wd("missions", "evacuation")
T_EACH, T_TRIP = wd("missions", "Each"), wd("missions", "trip")
T_COST = ls("cost")


def ugv_x(t):
    return keys(t, [(T_EACH, 960), (T_COST + 0.3, 1330)])


def ukraine(c, t):
    a = win(t, T_APRIL, T_COST + 0.4, 0.2, 0.5)
    if a <= 0:
        return
    with layer(c, a):
        kn = 1 - ease(seg(t, T_EACH - 0.3, T_EACH + 0.2))
        if kn > 0:
            with layer(c, kn):
                roll(c, "50,000", "~112,000", 120, CX, 270, t, T_50K, T_112)
                label(c, "APRIL 2026 · UKRAINE", CX, 180, t, T_APRIL + 0.05, 22, SOFT, a=a * kn)
                label(c, "GROUND ROBOTS ORDERED FOR 2026", CX, 370, t, T_GROUND, 22, GLOW, a=a * kn * (1 - ease(seg(t, T_MIS, T_MIS + 0.3))))
                label(c, "SUPPLY AND EVACUATION RUNS BY SEPTEMBER", CX, 370, t, T_SUP - 0.1, 22, GLOW, a=a * kn)
        kc = win(t, T_GROUND - 0.1, T_EACH + 0.2, 0.3, 0.5)                    # a convoy of them, behind
        if kc > 0:
            for k in range(14):
                x = (170 * k + 240 * (t - T_GROUND)) % 2300 - 200
                ul, uc = ugv(x, 470, 90, ph=(t - T_GROUND) * 6)
                stroke_polys(c, ul, SOFT, 1.3, kc * 0.8)
        x = ugv_x(t)
        ph = (t - T_EACH) * 5 if t > T_EACH else 0.0
        ul, uc = ugv(x, GROUND_Y - 20, 400, ph)
        closed_fill(c, uc, 1.0, mg.fill(MID, 0.3 * ease(seg(t, T_APRIL + 0.6, T_APRIL + 1.0))))
        lines_in(c, ul, t, T_APRIL + 0.1, 0.8, WHITE, 1.8, seed_pt=(x, GROUND_Y + 60))
        ev(T_APRIL + 0.1, "hydraulic", t, x)
        kx = ease(seg(t, T_SUP - 0.1, T_SUP + 0.2)) * (1 - ease(seg(t, T_EVAC - 0.1, T_EVAC + 0.2)))
        if kx > 0:
            stroke_polys(c, crate(x, GROUND_Y - 20, 400), GLOW, 1.8, kx)
            ev(T_SUP - 0.1, "dock", t, x)
        ks = ease(seg(t, T_EVAC - 0.1, T_EVAC + 0.2))
        if ks > 0:
            stroke_polys(c, stretcher(x, GROUND_Y - 20, 400), GLOW, 1.8, ks)
            ev(T_EVAC, "dock", t, x)
        if t >= T_EACH - 0.1:                                               # the trip a soldier didn't make
            js = body(c, 430, 340, STAND, 1, t, T_EACH - 0.1)
            stroke_polys(c, helmet(js, 340, 1), GLOW, 1.8, ease(seg(t, T_EACH + 0.3, T_EACH + 0.6)))
            kp = ease(seg(t, T_TRIP - 0.2, T_TRIP + 0.6))
            n = int(22 * kp)
            for i in range(n):
                fx_ = 540 + i * 40
                fy_ = GROUND_Y + 22 + (8 if i % 2 else -2)
                c.drawOval(skia.Rect.MakeXYWH(fx_, fy_ - 5, 16, 8), mg.stroke(SOFT, 1.3, 0.8 * (1 - 0.6 * i / 22)))
            label(c, "A TRIP A SOLDIER DIDN'T MAKE", CX, 280, t, T_TRIP, 24, WHITE, a=a)


T_FLIP, T_PAT, T_42, T_680_0, T_680 = wd("cost", "flipped"), wd("cost", "Patriot"), wd("cost", "four"), wd("cost", "About"), wd("cost", "Big")
T_DRONE, T_3K, T_8K = wd("drone", "drone"), wd("drone", "three"), wd("drone", "eight")
T_CHEAP, T_EXP, T_MATHS = wd("cheap", "Cheap"), wd("cheap", "Expensive"), wd("cheap", "maths")
T_LINE = ls("line")
COL_X0, COL_X1, COL_BOT, COL_H = 560, 800, 842, 640
PAT_WALL = None
GLINTS.append((T_680 + 0.2, 0.9))


def cost(c, t):
    global PAT_WALL
    a = win(t, T_COST - 0.1, T_LINE + 0.2, 0.2, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        kc = 1 - ease(seg(t, T_PAT - 0.5, T_PAT))                           # the money has flipped: a coin
        if kc > 0:
            ph = max(0.0, t - T_COST) * 2 * math.pi * 1.6
            sx = max(0.06, abs(math.cos(ph)))
            c.save(); c.translate(CX, 480); c.scale(sx, 1.0)
            coin(c, 0, 0, 110, kc, lit=1.0 if math.cos(ph) > 0 else 0.0)
            c.restore()
            ev(T_FLIP, "coin", t, CX)
        if t >= T_PAT - 0.1:
            lines_in(c, patriot(380, 190, 690, 30), t, T_PAT - 0.1, 0.7, WHITE, 1.8, seed_pt=(380, 760))
            ev(T_PAT - 0.1, "form", t, 380)
            label(c, "PATRIOT INTERCEPTOR", 380, 765, t, T_PAT + 0.3, 20, GLOW, a=a)
            label(c, "ABOUT $4.2 MILLION", 380, 797, t, T_42, 20, GLOW, a=a)
        if t >= T_680_0:
            if PAT_WALL is None:
                PAT_WALL = mac_wall("patriot", 11, 34, 23.6, 18.8, 9.5)
            draw_wall(c, PAT_WALL, COL_X0, COL_BOT, ease(seg(t, T_680_0, T_680 + 0.2), "o"))
            ev(T_680_0, "zoom", t, 680)
            label(c, "680,000 BIG MACS", 680, 160, t, T_680, 24, WHITE, a=a)
        if t >= T_DRONE - 0.1:
            dl, dc = shahed(1380, 430, 250)
            closed_fill(c, dc, 1.0, mg.fill(MID, 0.3 * ease(seg(t, T_DRONE + 0.3, T_DRONE + 0.6))))
            lines_in(c, dl, t, T_DRONE - 0.1, 0.6, WHITE, 1.8, seed_pt=(1380, 600))
            ev(T_DRONE - 0.1, "form", t, 1380)
            label(c, "SHAHED DRONE · $20,000–$50,000", 1380, 590, t, T_DRONE + 0.5, 22, GLOW, a=a)
        if t >= T_3K - 0.05:
            n = keys(t, [(T_3K - 0.05, 0.0), (T_3K + 0.3, 3000.0), (T_8K, 3000.0), (T_8K + 0.3, 8000.0)])
            hh = COL_H * n / 680000
            c.drawRect(skia.Rect.MakeLTRB(1250, COL_BOT - hh, 1510, COL_BOT), mg.fill(WHITE, 0.95))
            c.drawLine(1380, 760, 1380, COL_BOT - 14, mg.stroke(GLOW, 1.6, 1.0))
            c.drawLine(1380, COL_BOT - 14, 1370, COL_BOT - 28, mg.stroke(GLOW, 1.6, 1.0)); c.drawLine(1380, COL_BOT - 14, 1390, COL_BOT - 28, mg.stroke(GLOW, 1.6, 1.0))
            label(c, "3,000–8,000 BIG MACS", 1380, 740, t, T_3K, 22, WHITE, a=a)
            ev(T_3K, "tick", t, 1380)
            ev(T_8K, "tick", t, 1380)
        label(c, "CHEAP MACHINE", 1380, 130, t, T_CHEAP, 26, WHITE, a=a)
        label(c, "EXPENSIVE ANSWER", 560, 110, t, T_EXP, 26, WHITE, a=a)
        label(c, "THE ANSWER COSTS 84–210× THE DRONE", 1380, 660, t, T_MATHS, 20, SOFT, a=a)
        ev(T_CHEAP, "tick", t, 1380)
        ev(T_EXP, "tick", t, 590)


# ---------------------------------------------------------------- IDEA
T_PERSON_L = wd("line", "person")
T_EDGE, T_SHARE, T_BAL, T_WALKW, T_FIND = ls("edge"), wd("edge", "share"), wd("edge", "balance"), wd("edge", "walking"), wd("edge", "finding")
T_LOOP, T_LOOPW, T_SMALLER = ls("loop"), wd("loop", "loop"), wd("loop", "smaller")
T_IMAGINE = ls("imagine")
ICON_X = [540, 820, 1100, 1380]
BAR = (360.0, 500.0, 1200.0, 70.0)


def machine_icon(c, k, x, t, t0, a):
    y = 700
    if k == 0:
        return body(c, x, 200, STAND, 1, t, t0, robot=True, a=a, y=y - 0.48 * 200 + 50)
    if k == 1:
        return body(c, x, 200, GUARD, 1, t, t0, robot=True, a=a, y=y - 0.48 * 200 + 50)
    if k == 2:
        dl, dc = dog(x, y - 30, 190)
        with layer(c, a):
            closed_fill(c, dc, 1.0, mg.fill(MID, 0.3)); lines_in(c, dl, t, t0, 0.6, WHITE, 1.7)
        return None
    ul, uc = ugv(x, y + 50, 200)
    with layer(c, a):
        closed_fill(c, uc, 1.0, mg.fill(MID, 0.3)); lines_in(c, ul, t, t0, 0.6, WHITE, 1.7)
    return None


def share(t):
    return keys(t, [(T_SHARE, 0.0), (T_SHARE + 0.6, 0.14), (T_BAL, 0.14), (T_BAL + 0.4, 0.32), (T_WALKW, 0.32), (T_WALKW + 0.4, 0.5),
                    (T_FIND, 0.5), (T_FIND + 0.5, 0.7)])


def circle_polys(r):
    return [ellipse(CX, 520, r, r, 0, 360, 120)]


def idea(c, t):
    a = win(t, T_LINE - 0.05, T_IMAGINE + 0.2, 0.2, 0.7)
    if a <= 0:
        return
    with layer(c, a):
        ki = 1 - ease(seg(t, T_EDGE - 0.1, T_EDGE + 0.4))                   # four machines, four people deciding
        if ki > 0:
            for k, x in enumerate(ICON_X):
                machine_icon(c, k, x, t, T_LINE + 0.12 * k, ki)
                ev(T_LINE + 0.12 * k, "tick", t, x)
                t_p = T_PERSON_L - 0.2 + 0.1 * k
                if t >= t_p:
                    jp = body(c, x, 150, dict(PILOT, ls=50, le=75, rs=40, re=85), 1, t, t_p, a=ki, y=330)
                    signal(c, (x, jp["lfoot"][1] + 10), (x, 560), t + 0.3 * k, ki * ease(seg(t, t_p + 0.3, t_p + 0.6)), bend=0, n=20,
                           frac=ease(seg(t, t_p + 0.3, t_p + 0.6)))
            label(c, "A PERSON, DECIDING", CX, 170, t, T_PERSON_L + 0.3, 24, WHITE, a=a * ki)
        x0, y0, w, h = BAR
        if T_EDGE - 0.1 <= t < T_LOOP + 0.8:                                   # the machine's share grows
            bar = [P([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)])]
            if t < T_LOOP:
                lines_in(c, bar, t, T_EDGE, 0.6, WHITE, 1.8, seed_pt=(x0, y0))
                sh = share(t)
                if sh > 0:
                    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w * sh, h), mg.chrome_paint(y0, y0 + h, 0.9))
                label(c, "THE MACHINE", x0, y0 - 30, t, T_SHARE, 22, GLOW, "left", a=a)
                label(c, "THE PERSON", x0 + w, y0 - 30, t, T_SHARE + 0.2, 22, GLOW, "right", a=a)
                for tt, txt, u in ((T_BAL, "BALANCE", 0.32), (T_WALKW, "WALKING", 0.5), (T_FIND, "FINDING ITS OWN WAY", 0.7)):
                    if t >= tt:
                        c.drawLine(x0 + w * u, y0 + h, x0 + w * u, y0 + h + 30, mg.stroke(GLOW, 1.5, a))
                    label(c, txt, x0 + w * u, y0 + h + 60, t, tt + 0.15, 20, WHITE, a=a)
                    ev(tt + 0.1, "latch", t, x0 + w * u)
            else:                                                              # ...and becomes the loop
                k = seg(t, T_LOOP, T_LOOP + 0.8)
                morph_figs(c, bar, circle_polys(300), k, WHITE)
                ev(T_LOOP, "morph", t, CX)
        if t >= T_LOOP + 0.8:
            r = keys(t, [(T_LOOPW + 0.6, 300), (T_SMALLER + 0.3, 165)])
            stroke_polys(c, circle_polys(r), WHITE, 2.4, 1.0)
            ev(T_LOOPW + 0.7, "hydraulic", t, CX)
        if t >= wd("loop", "person") - 0.1:
            body(c, CX, 250, STAND, 1, t, wd("loop", "person") - 0.1, y=560)
            label(c, "IN THE LOOP", CX, 170, t, T_LOOPW, 26, WHITE, a=a)


# ---------------------------------------------------------------- IMAGINE
T_2030, T_PILOT_GONE = wd("imagine", "twenty"), wd("imagine", "pilot")
T_WHATIF, T_WHO, T_STRIKE, T_RULES, T_MONTHS = ls("whatif"), ls("who"), wd("who", "strikes?"), wd("who", "wrote"), wd("who", "months")
T_Q, T_INSIDE = ls("question"), wd("question", "inside")
T_THEN = ls("then")
_DUST = {}


def imagine(c, t):
    a = win(t, T_IMAGINE - 0.05, T_THEN + 0.1, 0.2, 0.6)
    if a <= 0:
        return
    with layer(c, a):
        k2 = 1 - ease(seg(t, T_WHO - 0.2, T_WHO + 0.3))
        if k2 > 0:
            dotted_num(c, "2030", 150, CX, 250, t, T_2030, k2)
            label(c, "NOT A FORECAST · A WHAT-IF", CX, 370, t, T_WHATIF + 0.05, 24, WHITE, a=a * k2)
        xr = keys(t, [(T_WHO, 720), (T_WHO + 0.9, 1340), (T_Q, 1340), (T_Q + 0.8, CX)])
        sr = keys(t, [(T_Q, 380), (T_Q + 0.8, 470)])
        rp = pose_mix(STAND, PUNCH, bump(t, T_STRIKE - 0.1, T_STRIKE + 0.05, T_STRIKE + 0.45))
        jr = body(c, xr, sr, rp, 1 if t < T_Q else -1, t, T_IMAGINE + 0.05, robot=True)
        ev(T_WHO + 0.05, "servo", t, xr)
        ev(T_STRIKE, "thud", t, xr)
        if t < T_PILOT_GONE + 1.2:                                            # the pilot, then not needed
            jp = figure(1260, hips_y(380), 380, STAND, -1)
            kg = seg(t, T_PILOT_GONE, T_PILOT_GONE + 1.1)
            if kg <= 0:
                body(c, 1260, 380, STAND, -1, t, T_IMAGINE + 0.15)
                stroke_polys(c, headset(jp[1], 380, -1), WHITE, 2.0, ease(seg(t, T_IMAGINE + 0.5, T_IMAGINE + 0.8)))
                signal(c, (1220, jp[1]["head"][1]), (xr + 30, jr["head"][1]), t, ease(seg(t, T_IMAGINE + 0.6, T_IMAGINE + 1.0)))
            else:
                if "p" not in _DUST:
                    _DUST["p"] = sample_on(jp[0] + headset(jp[1], 380, -1), 700, np.random.default_rng(3))
                    _DUST["v"] = np.random.default_rng(4).normal(0, 1, (700, 2)) * [70, 50] + [60, -90]
                X = _DUST["p"] + _DUST["v"] * ease(kg, "o")
                points(c, X, 1 - kg, GOLD, 3.0)
                ev(T_PILOT_GONE, "grains", t, 1260)
        if T_WHO <= t < T_Q + 0.4:                                             # the rules, written far away
            kr = win(t, T_RULES - 0.2, T_Q + 0.4, 0.3, 0.4)
            with layer(c, kr):
                lines_in(c, page(330, 380, 190, 250), t, T_RULES - 0.2, 0.5, WHITE, 1.8)
                ev(T_RULES - 0.2, "paper", t, 420)
                label(c, "THE RULES", 425, 680, t, T_RULES + 0.1, 22, GLOW, a=kr)
                if t >= T_MONTHS - 0.3:
                    q = bezier((530, 470), (930, 300), (xr - 60, jr["head"][1]), 60)
                    n = int(len(q) * ease(seg(t, T_MONTHS - 0.3, T_MONTHS + 0.4)))
                    path = skia.Path()
                    for i in range(0, max(0, n - 1), 2):
                        path.moveTo(*q[i]); path.lineTo(*q[i + 1])
                    c.drawPath(path, mg.stroke(GLOW, 1.7, kr))
                    label(c, "MONTHS EARLIER · FAR AWAY", CX, 250, t, T_MONTHS, 24, WHITE, a=kr)
        if t >= T_INSIDE - 0.15:                                               # who is inside?
            cx_, cy_ = (jr["neck"][0] + jr["hip"][0]) / 2, (jr["neck"][1] + jr["hip"][1]) / 2
            bignum(c, t, "?", 110, cx_, cy_, T_INSIDE - 0.15)
            label(c, "WHO IS INSIDE?", CX, 170, t, T_INSIDE, 26, WHITE, a=a)


# ---------------------------------------------------------------- SURFACE: the mirrored close, then the sources
T_2021, T_SUITW = wd("then", "twenty"), wd("then", "robot")
T_NOW2, T_2026, T_STILL, T_INSIDE2 = ls("now2"), wd("now2", "twenty"), wd("now2", "twenty-six,"), wd("now2", "person")
T_SRC = le("now2") + 1.2
SOURCES = ["SOURCES",
           "Human vs humanoid, San Francisco, 18 Sep 2026: Yahoo Tech; IBTimes UK",
           "Tesla AI Day, 19 Aug 2021: Fortune; Gizmodo",
           "Robot boxing, Hangzhou, May 2025 (Unitree G1): Live Science; Global Times",
           "Unitree G1 $13,500: The Robot Report · Big Mac $6.22: The Economist, July 2026",
           "PLA robot dog with a rifle, Golden Dragon 2024: CNN",
           "Ukraine's ground robots, 2026: Defense News; United24 Media",
           "Patriot PAC-3 MSE ~$4.2M: US Army FY2025 · Shahed $20k-$50k: CSIS",
           "The 2030 section is a what-if, not a forecast"]


def mirror(c, t):
    a = win(t, T_THEN - 0.05, T_SRC + 0.1, 0.2, 0.6)
    if a > 0:
        with layer(c, a):
            lines_in(c, [P([(CX, 180), (CX, 820)])], t, T_THEN, 0.5, SOFT, 1.4, seed_pt=(CX, 820))
            bignum(c, t, "2021", 130, 560, 250, T_2021)
            body(c, 560, 360, STAND, 1, t, T_SUITW - 0.1, mask=True)
            label(c, "A PERSON IN A SUIT", 560, 845, t, wd("then", "person"), 22, GLOW, a=a)
            if t >= T_2026 - 0.05:
                bignum(c, t, "2026", 130, 1360, 250, T_2026 - 0.05)
                jr = body(c, 1360, 380, STAND, -1, t, T_STILL + 0.2, robot=True)
                if t >= T_INSIDE2 - 0.1:
                    cx_, cy_ = (jr["neck"][0] + jr["hip"][0]) / 2, (jr["neck"][1] + jr["hip"][1]) / 2
                    body(c, cx_, 105, STAND, -1, t, T_INSIDE2 - 0.1, y=cy_ - 5, col=GLOW)
                label(c, "A PERSON INSIDE THE ROBOT", 1360, 845, t, T_INSIDE2 + 0.1, 22, GLOW, a=a)
    if t >= T_SRC:
        ks = 1 - ease(seg(t, T_SRC + 7.6, T_SRC + 8.4))
        for k, s_ in enumerate(SOURCES):
            label(c, s_, 250, 250 + k * 50, t, T_SRC + 0.2 + (0 if k == 0 else 0.6 + 0.45 * (k - 1)),
                  24 if k == 0 else 20, GLOW if k == 0 else SOFT, align="left", a=ks, cps=17 if k == 0 else 45)


def end_time():
    return T_SRC + 8.6


def frame(c, t):
    fight(c, t)
    pilot(c, t)
    dancer(c, t)
    tesla(c, t)
    boxing(c, t)
    split(c, t)
    price(c, t)
    dogs(c, t)
    ukraine(c, t)
    cost(c, t)
    idea(c, t)
    imagine(c, t)
    mirror(c, t)
