"""EP03 · THE SHOVEL SELLERS, the body (everything after the cold open), in the same system: line art keyed to the
script's line ids (build/lines.json), which ascii_open.py turns into characters with one focal point and the small
labels typed on top. Every analogy is drawn as the thing itself (the plan: FULL_PLAN.md).

  MECHANISM  a census ledger read by a scan line; miners' bar against everyone else's; one prize split across a
             crowd; every one of them gets a pan, and the supplier is paid
  NOW        1848 turns into 2026; the four companies, $725 billion, data-centre racks; a million dollars a day from
             AD 43 to 2026; the shovel becomes a chip; Big Macs pour out of it; four coins, one makes the chips;
             OpenAI's money in and out; the balance tips to $1.65; a trickle of Big Macs; some diggers strike gold
  IDEA       1846; 272 Acts stacking up; the railway map, a third never built, the bubble pops; 6,000 miles, London
             to Tokyo; the speculation dissolves and the rails stay
  IMAGINE    a dotted 2030; not a forecast; a tap running; electricity, chips, land, water; one answer to trust;
             where the gold is against what everyone will need
  SURFACE    the gold rush again, then a supply chain; the sources

ep03s.frame calls frame(c, t) once the cold open's question has been asked.
"""
import math

import numpy as np

import ep03s as S
from ep03s import mg, skia, W, CX, GLOW, WHITE, MID, SOFT, TURQ, GOLD, ease, seg, clamp, lerp, P, ellipse, glyphs, segs, \
    morph_flow, draw_segs, formation, chrome_fill, points, label, ev, ls, at

IDS = [x.get("id") for x in S.L]
DIM = "#0B0C0E"


def nxt(i_d):
    """The start of the line after this one (or its end + 3 s)."""
    i = IDS.index(i_d)
    return S.L[i + 1]["start"] if i + 1 < len(S.L) else S.L[i]["end"] + 3.0


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


_G = {}


def big(text, size, cx, cy, n=420):
    k = (text, size, cx, cy, n)
    if k not in _G:
        polys, path = glyphs(text, size, cx, cy)
        _G[k] = (segs(polys, n), path)
    return _G[k]


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
    ev(t0, "form", t, cx)
    if fill:
        ev(t0 + 0.75, "thock", t, cx)


def fill_rrect(c, x, y, w, h, r, paint):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), paint)


def poly_path(q, close=False):
    p = skia.Path()
    p.moveTo(*q[0])
    for x, y in q[1:]:
        p.lineTo(float(x), float(y))
    if close:
        p.close()
    return p


def stroke_polys(c, polys, col=GLOW, w=1.7, a=1.0):
    if a <= 0:
        return
    path = skia.Path()
    for q in polys:
        path.addPoly([skia.Point(float(x), float(y)) for x, y in q], False)
    g = mg.stroke(col, 6, 0.22 * a)
    g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5))
    c.drawPath(path, g)
    c.drawPath(path, mg.stroke(col, w, a))


def mini_mac(c, x, y, s, a=1.0):
    """A small Big Mac, as solid shapes (so it reads as a stack in characters)."""
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


RATE_MAC = 4.0


def mac_icon(c, x, y, s, a=1.0):
    """The hero Big Mac, small: chrome buns, dark patties, seeds, outlines (so it still reads in characters)."""
    if a <= 0.01:
        return
    outl, buns, patties, seeds = S.bigmac(x, y, s)
    with layer(c, a):
        S.closed_fill(c, buns, 1.0, mg.chrome_paint(y - 0.62 * s, y + 1.02 * s))
        S.closed_fill(c, patties, 1.0, mg.fill(MID, 0.55))
        S.closed_fill(c, seeds, 1.0, mg.fill(DIM, 0.9))
        stroke_polys(c, outl, WHITE, 1.3, 0.9)


def coin(c, x, y, r, a=1.0, lit=1.0):
    c.drawCircle(x, y, r, mg.stroke(GLOW, 2.0, a))
    c.drawCircle(x, y, r * 0.8, mg.stroke(GLOW, 1.2, 0.6 * a))
    if lit > 0:
        p = mg.chrome_paint(y - r, y + r, a * lit)
        c.drawCircle(x, y, r * 0.78, p)
    f = mg.font(mg.DISPLAY, r * 0.9)
    c.drawString("$", x - f.measureText("$") / 2, y + r * 0.32, f, mg.fill(DIM if lit > 0.5 else GLOW, a))


def chip(cx, cy, s):
    """A GPU package: the substrate, the die, the pins on every side."""
    out = [mg.rrect_pts(cx - s, cy - s, 2 * s, 2 * s, 0.08 * s, 4), mg.rrect_pts(cx - 0.5 * s, cy - 0.5 * s, s, s, 0.04 * s, 3)]
    for k in range(9):
        o = -0.8 * s + k * 0.2 * s
        out += [P([(cx + o, cy - s), (cx + o, cy - 1.18 * s)]), P([(cx + o, cy + s), (cx + o, cy + 1.18 * s)]),
                P([(cx - s, cy + o), (cx - 1.18 * s, cy + o)]), P([(cx + s, cy + o), (cx + 1.18 * s, cy + o)])]
    return out


def bezier(p0, p1, p2, n=40):
    u = np.linspace(0, 1, n)[:, None]
    return (1 - u) ** 2 * np.array(p0) + 2 * (1 - u) * u * np.array(p1) + u ** 2 * np.array(p2)


RNG = np.random.default_rng(31)

# ---------------------------------------------------------------- scene data
# the ledger (two census pages) and the verdict bars
PAGES = [(CX - 590, 260), (CX + 60, 260)]
LEDGER = []
for px, py in PAGES:
    LEDGER.append(mg.rrect_pts(px, py, 530, 470, 10, 3))
    LEDGER.append(P([(px, py + 50), (px + 530, py + 50)]))
    for k in (170, 260, 420):
        LEDGER.append(P([(px + k, py + 50), (px + k, py + 470)]))
ROWS = []                                        # handwriting: short strokes in each row and column
for pi, (px, py) in enumerate(PAGES):
    for r in range(13):
        y = py + 78 + r * 30
        for x0, x1 in ((12, 160), (182, 250), (272, 410), (432, 518)):
            L = RNG.uniform(0.35, 0.9) * (x1 - x0)
            ROWS.append((pi, r, P([(px + x0, y), (px + x0 + L, y)])))
MINER_ROWS = {(pi, r) for pi in (0, 1) for r in range(13) if RNG.random() < 0.34}
BAR_X = CX - 560
BARS = [mg.rrect_pts(BAR_X, 360, 64, 74, 8, 3), mg.rrect_pts(BAR_X, 540, 1120, 74, 8, 3)]

# the crowd around one prize
N_CROWD = 64
_ang = np.linspace(0, 2 * np.pi, N_CROWD, endpoint=False) + RNG.uniform(-0.04, 0.04, N_CROWD)
CROWD = np.column_stack([CX + 430 * np.cos(_ang), 470 + 255 * np.sin(_ang)])
CROWD_FROM = np.column_stack([CX + 1400 * np.cos(_ang), 470 + 900 * np.sin(_ang)])
ORB = np.array([CX, 470.0])
PANS_SMALL = [(i, q) for i, (x, y) in enumerate(CROWD) for q in S.pan(x, y - 34, 15)]
STORE = S.house(CX - 70, 540, 140, 90)

# 2026, the racks
G1848 = big("1848", 250, CX, 500)
G2026 = big("2026", 250, CX, 500)
RACKS = [mg.rrect_pts(CX - 660 + k * 112, 640, 72, 170, 6, 3) for k in range(12)]

# Rome to 2026
AX0, AX1, AXY = 300.0, 1620.0, 600.0
YEARS = [(43, "AD 43"), (500, "500"), (1000, "1000"), (1500, "1500"), (2026, "2026")]
yx = lambda yr: AX0 + (AX1 - AX0) * (yr - 43) / (2026 - 43)


def helmet(cx, cy, s):
    """A Roman helmet in profile: the bowl, the neck guard, a cheek piece, and the crest with its bristles."""
    bowl = ellipse(cx, cy, s, 0.85 * s, 180, 360, 40)
    neck = P([(cx + s, cy), (cx + 1.35 * s, cy + 0.28 * s), (cx + 1.45 * s, cy + 0.36 * s)])
    brow = P([(cx - s, cy), (cx - 1.12 * s, cy + 0.06 * s)])
    cheek = P([(cx - 0.55 * s, cy), (cx - 0.62 * s, cy + 0.7 * s), (cx - 0.25 * s, cy + 0.82 * s), (cx - 0.12 * s, cy + 0.1 * s)])
    crest_o = ellipse(cx, cy - 0.85 * s, 0.95 * s, 0.55 * s, 190, 350, 30)
    crest_i = ellipse(cx, cy - 0.8 * s, 0.8 * s, 0.4 * s, 195, 345, 30)
    bristles = [P([crest_i[k], crest_o[k]]) for k in range(2, 29, 3)]
    return [bowl, neck, brow, cheek, crest_o, crest_i] + bristles


HELMET = helmet(AX0 + 30, AXY - 190, 100)

# the chip, the Big Mac pile
CHIP_C = (CX - 420, 470.0)
SHOVEL_SRC = S.shovel(CHIP_C[0], 690, 430)
CHIP = chip(CHIP_C[0], CHIP_C[1], 150)
COINS_X = [CX - 390, CX - 130, CX + 130, CX + 390]

# the balance
BEAM_C = (CX, 330.0)

# the railway map (a stylised Britain) and the globe
TOWN = {"EDINBURGH": (560, 230), "GLASGOW": (470, 255), "NEWCASTLE": (620, 330), "YORK": (610, 450), "LEEDS": (575, 480),
        "MANCHESTER": (520, 520), "LIVERPOOL": (455, 525), "BIRMINGHAM": (545, 640), "NORWICH": (730, 650),
        "LONDON": (640, 755), "BRISTOL": (450, 745), "CARDIFF": (385, 740), "EXETER": (360, 820), "DOVER": (760, 790),
        "SOUTHAMPTON": (560, 815), "CARLISLE": (505, 335), "HULL": (705, 470), "SHEFFIELD": (585, 560),
        "NOTTINGHAM": (625, 600), "OXFORD": (565, 715), "CAMBRIDGE": (690, 680), "PLYMOUTH": (290, 850)}
LINKS = [("LONDON", "BIRMINGHAM"), ("BIRMINGHAM", "MANCHESTER"), ("BIRMINGHAM", "LIVERPOOL"), ("MANCHESTER", "LEEDS"),
         ("LEEDS", "YORK"), ("YORK", "NEWCASTLE"), ("NEWCASTLE", "EDINBURGH"), ("EDINBURGH", "GLASGOW"),
         ("LONDON", "BRISTOL"), ("BRISTOL", "CARDIFF"), ("BRISTOL", "EXETER"), ("LONDON", "SOUTHAMPTON"),
         ("LONDON", "DOVER"), ("LONDON", "NORWICH"), ("LEEDS", "LIVERPOOL"), ("MANCHESTER", "GLASGOW"),
         ("NEWCASTLE", "CARLISLE"), ("CARLISLE", "GLASGOW"), ("YORK", "HULL"), ("LEEDS", "SHEFFIELD"),
         ("SHEFFIELD", "NOTTINGHAM"), ("NOTTINGHAM", "BIRMINGHAM"), ("BIRMINGHAM", "BRISTOL"), ("LONDON", "OXFORD"),
         ("OXFORD", "BIRMINGHAM"), ("LONDON", "CAMBRIDGE"), ("CAMBRIDGE", "NORWICH"), ("MANCHESTER", "SHEFFIELD"),
         ("EXETER", "PLYMOUTH")]
NEVER = {("BRISTOL", "EXETER"), ("LONDON", "NORWICH"), ("LEEDS", "LIVERPOOL"), ("MANCHESTER", "GLASGOW"), ("LONDON", "DOVER"),
         ("CAMBRIDGE", "NORWICH"), ("YORK", "HULL"), ("OXFORD", "BIRMINGHAM"), ("EXETER", "PLYMOUTH")}


def rail(a, b):
    (x0, y0), (x1, y1) = TOWN[a], TOWN[b]
    mid = ((x0 + x1) / 2 + (y1 - y0) * 0.08, (y0 + y1) / 2 - (x1 - x0) * 0.08)
    return bezier((x0, y0), mid, (x1, y1), 30)


RAILS = {(a, b): rail(a, b) for a, b in LINKS}
GLOBE_C, GLOBE_R = (CX + 330, 560.0), 220.0
LONDON_G = (GLOBE_C[0] - 0.62 * GLOBE_R, GLOBE_C[1] - 0.55 * GLOBE_R)
TOKYO_G = (GLOBE_C[0] + 0.72 * GLOBE_R, GLOBE_C[1] - 0.3 * GLOBE_R)
ROUTE = bezier(LONDON_G, (GLOBE_C[0] + 0.1 * GLOBE_R, GLOBE_C[1] - 1.2 * GLOBE_R), TOKYO_G, 80)


def globe():
    cx, cy = GLOBE_C
    r = GLOBE_R
    out = [ellipse(cx, cy, r, r, 0, 360, 96)]
    for k in (0.35, 0.72):
        out.append(ellipse(cx, cy, r * k, r, 0, 360, 64))
    for f in (-0.5, 0.0, 0.5):
        w = r * math.sqrt(1 - f * f)
        out.append(ellipse(cx, cy + f * r, w, 0.12 * w, 0, 360, 48))
    return out


GLOBE = globe()

# imagine: a tap, the scarce things, the answers
TAP = [P([(CX - 260, 250), (CX - 20, 250), (CX + 20, 262), (CX + 40, 300), (CX + 40, 330)]),
       P([(CX - 260, 290), (CX - 30, 290), (CX - 12, 300), (CX - 4, 330)]),
       P([(CX - 4, 330), (CX + 40, 330)]),
       P([(CX - 120, 250), (CX - 120, 214)]), P([(CX - 170, 205), (CX - 70, 205)])]


def bolt(cx, cy, s):
    return [P([(cx + 0.2 * s, cy - s), (cx - 0.35 * s, cy + 0.08 * s), (cx + 0.02 * s, cy + 0.08 * s),
               (cx - 0.22 * s, cy + s), (cx + 0.38 * s, cy - 0.12 * s), (cx + 0.02 * s, cy - 0.12 * s), (cx + 0.2 * s, cy - s)])]


def land(cx, cy, s):
    out = [P([(cx - s, cy + 0.5 * s), (cx - 0.55 * s, cy - 0.5 * s), (cx + s, cy - 0.5 * s), (cx + 0.55 * s, cy + 0.5 * s), (cx - s, cy + 0.5 * s)])]
    for k in (0.33, 0.66):
        out.append(P([(cx - s + 0.45 * s * k * 2, cy + 0.5 * s - s * k), (cx + 0.55 * s + 0.45 * s * k * 2, cy + 0.5 * s - s * k)]))
    return out


def water(cx, cy, s):
    xs = np.linspace(cx - s, cx + s, 40)
    return [np.column_stack([xs, cy + dy * s + 0.12 * s * np.sin((xs - cx) / s * 9 + dy * 5)]) for dy in (-0.35, 0.0, 0.35)]


SCARCE_X = [CX - 540, CX - 180, CX + 180, CX + 540]
SCARCE = [bolt(SCARCE_X[0], 470, 110), chip(SCARCE_X[1], 470, 78), land(SCARCE_X[2], 470, 110), water(SCARCE_X[3], 470, 110)]
SCARCE_LAB = ["ELECTRICITY", "CHIPS", "LAND", "WATER"]
CARDS = [(CX - 560 + (k % 4) * 290, 250 + (k // 4) * 170) for k in range(12)]
TRUSTED = 6

# the end: a chain
LINKS_N = 9
CHAIN = [ellipse(300 + k * 165, 500, 100, 46 if k % 2 == 0 else 15, 0, 360, 48) for k in range(LINKS_N)]
SOURCES = ["SOURCES",
           "Sam Brannan, 1848: Wikipedia; Britannica; FoundSF",
           "The Californian, 29 May 1848: Library of Congress",
           "Clay & Jones, Journal of Economic History 68(4), 2008",
           "Big-tech 2026 capex ~$725B: company guidance via CNBC",
           "Nvidia Q2 FY2027, 26 Aug 2026 8-K: $96.2B, 75% margin",
           "OpenAI Jan-Mar 2026: The Information",
           "Big Mac $6.22: The Economist, July 2026",
           "Railway Mania: 272 Acts in 1846; ~6,000 miles by 1850",
           "The 2030 section is a what-if, not a forecast"]


# ---------------------------------------------------------------- MECHANISM
def ledger(c, t):
    t_c, t_v, t_s = ls("census"), ls("verdict"), ls("split")
    a = win(t, t_c - 0.1, t_s + 0.45)
    if a <= 0:
        return
    with layer(c, a):
        S_L = segs(LEDGER, 640)
        S_B = segs(BARS, 640)
        if t < t_v:
            formation(c, S_L, t, t_c + 0.05, 1.1, WHITE, seed_pt=(CX, 470))
            ev(t_c + 0.05, "form", t)
            ks = seg(t, t_c + 2.0, at("census", 0.95))            # the scan reads the rows, top to bottom
            if ks > 0:
                yscan = lerp(330, 760, ks)
                for pi, (px, py) in enumerate(PAGES):
                    c.drawLine(px - 10, yscan, px + 540, yscan, mg.stroke("#FFFFFF", 2.2, 0.7 * (1 - ks ** 8)))
                ev(t_c + 2.0, "scan", t)
                shown = [q for pi, r, q in ROWS if q[0, 1] < yscan]
                stroke_polys(c, shown, WHITE, 1.3, 0.8)
                mark = [(pi, r) for pi, r in MINER_ROWS if PAGES[pi][1] + 78 + r * 30 < yscan]
                for pi, r in mark:                                  # the miners, marked as the scan passes
                    px, py = PAGES[pi]
                    c.drawCircle(px + 520, py + 78 + r * 30, 4.5, mg.fill(GLOW, 0.9))
        ky = 1 - ease(seg(t, t_v - 0.1, t_v + 0.4))
        if ky > 0:
            with layer(c, ky):
                bignum(c, t, "1850", 84, PAGES[0][0] + 265, 205, t_c + 0.5, fill=True)
                bignum(c, t, "1852", 84, PAGES[1][0] + 265, 205, t_c + 0.7, fill=True)
        if t >= t_v:
            km = seg(t, t_v, t_v + 0.9)
            Sg, kk = morph_flow(S_L, S_B, km)
            draw_segs(c, Sg, WHITE, 1.7, 1.0, tips=kk if km < 1 else None)
            ev(t_v, "morph", t)
            k1 = ease(seg(t, at("verdict", 0.18), at("verdict", 0.32)))
            k2 = ease(seg(t, at("verdict", 0.55), at("verdict", 0.85)))
            if k1 > 0:
                fill_rrect(c, BAR_X, 360, 64 * k1, 74, 8, mg.fill(MID, 0.8))
            if k2 > 0:
                c.save(); c.clipRect(skia.Rect.MakeXYWH(BAR_X, 540, 1120 * k2, 74))
                fill_rrect(c, BAR_X, 540, 1120, 74, 8, mg.chrome_paint(540, 614))
                c.restore()
                ev(at("verdict", 0.55), "tick", t)
                ev(at("verdict", 0.85), "thock", t, BAR_X + 1120)
        label(c, "CENSUS RECORDS · CLAY & JONES, 2008", CX, 812, t, t_c + 1.3, 20, SOFT, a=a * (1 - ease(seg(t, t_v - 0.3, t_v + 0.2))))
        if t >= t_v:
            label(c, "MINERS", BAR_X, 342, t, at("verdict", 0.08), 22, WHITE, align="left", a=a)
            label(c, "SMALL, OR EVEN ZERO", BAR_X + 96, 405, t, at("verdict", 0.3), 20, SOFT, align="left", a=a)
            label(c, "EVERYONE ELSE", BAR_X, 522, t, at("verdict", 0.5), 22, WHITE, align="left", a=a)
            label(c, "POSITIVE AND LARGE", BAR_X + 1120, 650, t, at("verdict", 0.86), 20, GLOW, align="right", a=a)


def crowd(c, t):
    t_s, t_p, t_n = ls("split"), ls("pan"), ls("now")
    a = win(t, t_s - 0.35, t_n + 0.35)
    if a <= 0:
        return
    with layer(c, a):
        kin = ease(seg(t, t_s - 0.3, t_s + 1.0))
        pts = CROWD_FROM + (CROWD - CROWD_FROM) * kin
        ksplit = ease(seg(t, at("split", 0.5), at("split", 0.9)))
        r_orb = 44 * (1 - ksplit)
        if r_orb > 1:
            g = mg.fill(GLOW, 0.35); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 24))
            c.drawCircle(*ORB, r_orb * 2.2, g)
            c.drawCircle(*ORB, r_orb, mg.fill(TURQ, 1.0))
            c.drawCircle(*ORB, r_orb + 14, mg.stroke(GLOW, 1.4, 0.6))
        if 0 < ksplit < 1:                                          # the prize, in slivers, to every one of them
            sl = ORB + (CROWD - ORB) * ksplit
            points(c, sl, 1.0, GOLD, 3.0)
        ev(at("split", 0.5), "morph", t)
        got = ksplit >= 1
        points(c, pts, 1.0, GOLD if got else WHITE, 6.0)
        label(c, "ONE PRIZE · EVERYONE CHASING IT", CX, 800, t, t_s + 0.4, 20, SOFT, a=a * (1 - ease(seg(t, t_p - 0.2, t_p + 0.3))))
        if t >= t_p:                                                # a pan for every one of them
            order = np.argsort(np.arctan2(CROWD[:, 1] - 470, CROWD[:, 0] - CX))
            rank = np.empty(N_CROWD, int); rank[order] = np.arange(N_CROWD)
            kp = seg(t, t_p + 0.1, at("pan", 0.42))
            polys = [q for i, q in PANS_SMALL if rank[i] < kp * N_CROWD]
            stroke_polys(c, polys, WHITE, 1.3, 0.9)
            for j in range(0, N_CROWD, 8):
                ev(t_p + 0.1 + (at("pan", 0.42) - t_p - 0.1) * j / N_CROWD, "tick", t)
            ks = ease(seg(t, at("pan", 0.55), at("pan", 0.7)))
            if ks > 0:                                              # the supplier in the middle, paid by all of them
                stroke_polys(c, STORE, GLOW, 1.8, ks)
                label(c, "THE SUPPLIER", CX, 668, t, at("pan", 0.58), 20, GLOW, a=a)
                kc = seg(t, at("pan", 0.66), at("pan", 0.94))
                if 0 < kc < 1:
                    u = np.clip(kc * 1.6 - rank / N_CROWD * 0.6, 0, 1)[:, None]
                    fly = CROWD + (np.array([CX, 500.0]) - CROWD) * (u * u * (3 - 2 * u))
                    points(c, fly[(u[:, 0] > 0) & (u[:, 0] < 1)], 1.0, GOLD, 4.0)
                for j in range(5):
                    ev(at("pan", 0.7) + j * 0.12, "coin", t, CX)
                label(c, "PAID EITHER WAY", CX, 812, t, at("pan", 0.72), 20, WHITE, a=a)


# ---------------------------------------------------------------- NOW
def year2026(c, t):
    t_n, t_x, t_r = ls("now"), ls("capex"), ls("rome")
    a = win(t, t_n - 0.2, t_r + 0.4)
    if a <= 0:
        return
    with layer(c, a):
        up = ease(seg(t, t_x, t_x + 0.7))
        c.save()
        c.translate(CX, 500); c.scale(lerp(1, 0.42, up), lerp(1, 0.42, up)); c.translate(-CX, -500 + lerp(0, -700, up))
        km = seg(t, at("now", 0.3), at("now", 0.3) + 0.8)
        if t < at("now", 0.3):
            formation(c, G1848[0], t, t_n - 0.15, 0.5, GLOW, seed_pt=(CX, 800))
        else:
            Sg, kk = morph_flow(G1848[0], G2026[0], km)
            kf = ease(seg(t, at("now", 0.3) + 0.8, at("now", 0.3) + 1.3))
            draw_segs(c, Sg, GLOW, 1.8, 1 - 0.8 * kf, tips=kk if km < 1 else None)
            chrome_fill(c, G2026[1], kf, sweep=seg(t, at("now", 0.3) + 1.0, at("now", 0.3) + 1.9))
        ev(at("now", 0.3), "morph", t)
        ev(at("now", 0.3) + 0.8, "thock", t)
        c.restore()
        if t >= t_x:
            names = [("AMAZON", 0.1), ("MICROSOFT", 0.17), ("ALPHABET", 0.25), ("META", 0.32)]
            for k, (nm, f) in enumerate(names):
                label(c, nm, CX - 450 + k * 300, 318, t, at("capex", f), 24, WHITE, a=a)
            kt = 1 - ease(seg(t, t_r - 0.2, t_r + 0.5))
            bignum(c, t, "$725 BILLION", 132, CX, 470, at("capex", 0.46))
            label(c, "2026 PLANS · MOSTLY AI DATA CENTRES", CX, 575, t, at("capex", 0.72), 20, SOFT, a=a * kt)
            kr = seg(t, at("capex", 0.74), at("capex", 0.95))
            if kr > 0:
                formation(c, segs(RACKS, 480), t, at("capex", 0.74), 1.0, WHITE, seed_pt=(CX, 900))
                ev(at("capex", 0.74), "form", t)
                if t > at("capex", 0.9):
                    leds = []
                    for k in range(12):
                        for j in range(10):
                            if (math.sin(t * 3.1 + k * 1.7 + j * 2.3) + math.sin(t * 1.3 + j)) > 0.2:
                                leds.append((CX - 660 + k * 112 + 22 + (j % 2) * 28, 662 + (j // 2) * 30))
                    points(c, np.array(leds), 0.9, GLOW, 5.0)


def rome(c, t):
    t_r, t_nv = ls("rome"), ls("nvidia")
    a = win(t, t_r - 0.1, t_nv + 0.4)
    if a <= 0:
        return
    with layer(c, a):
        formation(c, segs(HELMET, 360), t, t_r + 0.05, 0.9, WHITE, seed_pt=(AX0, AXY))
        ev(t_r + 0.05, "form", t, AX0)
        k_ax = ease(seg(t, t_r + 0.2, t_r + 0.9))
        c.drawLine(AX0, AXY, lerp(AX0, AX1, k_ax), AXY, mg.stroke(WHITE, 1.8, 0.8))
        for yr, lab in YEARS:
            x = yx(yr)
            if x <= lerp(AX0, AX1, k_ax):
                c.drawLine(x, AXY - 12, x, AXY + 12, mg.stroke(WHITE, 1.6, 0.8))
                label(c, lab, x, AXY + 48, t, t_r + 0.3 + 0.12 * YEARS.index((yr, lab)), 20, SOFT, a=a)
        label(c, "THE ROMANS INVADE BRITAIN", AX0 + 30, AXY - 360, t, t_r + 0.8, 20, SOFT, a=a)
        t0, t1 = at("rome", 0.3), at("rome", 0.9)
        kr = ease(seg(t, t0, t1), "io")
        if t >= t0:                                                 # a million dollars a day, all the way to today
            x = lerp(AX0, AX1, kr)
            c.drawLine(AX0, AXY, x, AXY, mg.stroke(GLOW, 5.0, 0.95))
            g = mg.fill(GLOW, 0.4); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
            c.drawCircle(x, AXY, 22, g)
            c.drawCircle(x, AXY, 9, mg.fill("#FFFFFF", 1.0))
            spent = 725e9 * kr
            label(c, f"${spent:,.0f}", CX, 450, t, -1, 44, WHITE, a=a)
            label(c, "$1,000,000 A DAY", CX, 372, t, t0 - 0.1, 22, GLOW, a=a)
            for yr in (500, 1000, 1500):
                ev(t0 + (t1 - t0) * ((yr - 43) / 1983) ** 0.9, "tick", t, yx(yr))
            ev(t1, "thock", t, AX1)
            if t > t1:
                label(c, "ONLY JUST SPENT", AX1, AXY - 60, t, t1 + 0.1, 20, GLOW, align="right", a=a)


def chip_scene(c, t):
    t_nv, t_nm, t_mg, t_o = ls("nvidia"), ls("nvidia_mac"), ls("margin"), ls("openai")
    a = win(t, t_nv - 0.1, t_o + 0.4)
    if a <= 0:
        return
    with layer(c, a):
        S_sh, S_ch = segs(SHOVEL_SRC, 560), segs(CHIP, 560)
        a_chip = 1 - ease(seg(t, t_mg - 0.3, t_mg + 0.3))
        if a_chip > 0:
            with layer(c, a_chip):
                t_m = at("nvidia", 0.28)
                if t < t_m:
                    formation(c, S_sh, t, t_nv + 0.02, 0.7, WHITE, seed_pt=(CHIP_C[0], 900))
                else:
                    km = seg(t, t_m, t_m + 1.0)
                    Sg, kk = morph_flow(S_sh, S_ch, km)
                    draw_segs(c, Sg, GLOW, 1.8, 1.0, tips=kk if km < 1 else None)
                    if km >= 1:
                        c.drawRect(skia.Rect.MakeXYWH(CHIP_C[0] - 75, CHIP_C[1] - 75, 150, 150), mg.chrome_paint(CHIP_C[1] - 75, CHIP_C[1] + 75, 0.9))
                ev(t_nv + 0.02, "form", t, CHIP_C[0])
                ev(t_m, "morph", t, CHIP_C[0])
                label(c, "THE SHOVEL, NOW", CHIP_C[0], CHIP_C[1] + 232, t, t_m + 0.5, 20, SOFT)
                ka = 1 - ease(seg(t, t_nm - 0.2, t_nm + 0.3))
                if ka > 0:
                    with layer(c, ka):
                        bignum(c, t, "$96.2 BILLION", 104, CX + 300, 440, at("nvidia", 0.55))
                        label(c, "NVIDIA · ONE QUARTER, TO 26 JULY 2026", CX + 300, 540, t, at("nvidia", 0.72), 20, SOFT, a=a * ka)
                if t >= t_nm - 0.1:                                   # Big Macs roll off it, one after another
                    kp = win(t, t_nm - 0.1, t_mg + 0.2, 0.3, 0.5)
                    belt_y = CHIP_C[1] + 118
                    c.drawLine(CHIP_C[0] + 190, belt_y, 1880, belt_y, mg.stroke(WHITE, 1.6, 0.7 * kp))
                    for x in range(int(CHIP_C[0]) + 230, 1880, 70):
                        c.drawCircle(x, belt_y + 14, 9, mg.stroke(WHITE, 1.2, 0.5 * kp))
                    t0 = t_nm - 0.1
                    for i in range(int((t - t0) * RATE_MAC) + 1):
                        x = CHIP_C[0] + 230 + (t - t0 - i / RATE_MAC) * 520
                        if x < 1960:
                            mac_icon(c, x, belt_y - 72, 42, kp * clamp((x - CHIP_C[0] - 190) / 60))
                        ev(t0 + i / RATE_MAC, "tick", t, CHIP_C[0] + 230)
                    bignum(c, t, "2,000", 120, CX + 360, 250, t_nm + 0.15, fill=True)
                    label(c, "BIG MACS · EVERY SECOND · ROUGHLY", CX + 360, 335, t, t_nm + 0.5, 22, GLOW, a=a * kp)
        if t >= t_mg - 0.1:                                           # four coins; one makes the chips
            for k, x in enumerate(COINS_X):
                t_k = t_mg + 0.08 + 0.14 * k
                if t < t_k:
                    continue
                kin = ease(seg(t, t_k, t_k + 0.3), "o")
                y = lerp(300, 430, kin)
                drop = ease(seg(t, at("margin", 0.55), at("margin", 0.75))) if k == 0 else 0.0
                y += 290 * drop
                coin(c, x, y, 62, 1.0, lit=0.0 if k == 0 else ease(seg(t, at("margin", 0.72), at("margin", 0.85))))
                ev(t_k + 0.28, "coin", t, x)
            if t > at("margin", 0.5):
                c.drawRect(skia.Rect.MakeXYWH(COINS_X[0] - 110, 660, 220, 130), mg.stroke(WHITE, 1.6, 0.8))
                label(c, "MAKING THE CHIPS", COINS_X[0], 830, t, at("margin", 0.55), 20, SOFT, a=a)
                ev(at("margin", 0.75), "coin", t, COINS_X[0])
            label(c, "75% GROSS MARGIN", CX + 130, 560, t, at("margin", 0.8), 22, GLOW, a=a)


def dig(c, t):
    t_o, t_om, t_f, t_b = ls("openai"), ls("openai_mac"), ls("fair"), ls("before")
    a = win(t, t_o - 0.1, t_b + 0.2)
    if a <= 0:
        return
    with layer(c, a):
        a1 = 1 - ease(seg(t, t_om - 0.2, t_om + 0.3))
        if a1 > 0:
            with layer(c, a1):
                formation(c, segs(S.pan(CX, 470, 170), 360), t, t_o + 0.05, 0.9, WHITE, seed_pt=(CX, 800))
                ev(t_o + 0.05, "form", t)
                label(c, "OPENAI · JAN–MAR 2026", CX, 640, t, t_o + 0.6, 22, WHITE, a=a * a1)
                k_in = seg(t, at("openai", 0.42), at("openai", 0.62))
                if k_in > 0:
                    n = 60
                    u = np.clip(k_in * 1.6 - np.arange(n) / n * 0.6, 0, 1)
                    xs = lerp(160, CX - 150, u); ys = 470 + 30 * np.sin(np.arange(n) * 1.7)
                    points(c, np.column_stack([xs, ys])[(u > 0) & (u < 1)], 1.0, GOLD, 5.0)
                    label(c, "$5.7B IN", 260, 400, t, at("openai", 0.45), 26, WHITE, align="left", a=a * a1)
                    ev(at("openai", 0.42), "grains", t, 400)
                k_out = seg(t, at("openai", 0.78), at("openai", 0.98))
                if k_out > 0:
                    n = 60
                    u = np.clip(k_out * 1.6 - np.arange(n) / n * 0.6, 0, 1)
                    xs = lerp(CX + 150, 1720, u); ys = 500 + 260 * u ** 2 + 20 * np.sin(np.arange(n) * 2.3)
                    live = (u > 0) & (u < 1)
                    points(c, np.column_stack([xs, ys])[live], 0.9, WHITE, 5.0)
                    label(c, "$3.7B OUT", 1660, 400, t, at("openai", 0.8), 26, GLOW, align="right", a=a * a1)
                    ev(at("openai", 0.78), "grains", t, 1500)
        a2 = win(t, t_om - 0.1, t_f + 0.3)
        if a2 > 0 and t >= t_om - 0.1:                                # the balance tips: $1 in, $1.65 out
            with layer(c, a2):
                tilt = 9 * ease(seg(t, at("openai_mac", 0.18), at("openai_mac", 0.4)), "o")
                ang = math.radians(tilt)
                bx, by = BEAM_C
                L_ = 380
                lx, ly = bx - L_ * math.cos(ang), by - L_ * math.sin(ang)
                rx, ry = bx + L_ * math.cos(ang), by + L_ * math.sin(ang)
                beam = [P([(lx, ly), (rx, ry)]), P([(bx, by), (bx, 700)]), P([(bx - 120, 700), (bx + 120, 700)])]
                dishes = []
                for (x, y) in ((lx, ly), (rx, ry)):
                    dishes += [P([(x, y), (x - 90, y + 150)]), P([(x, y), (x + 90, y + 150)]), ellipse(x, y + 150, 110, 26, 0, 180, 30)]
                stroke_polys(c, beam + dishes, WHITE, 1.8, 1.0)
                c.drawCircle(bx, by, 9, mg.fill(GLOW, 1.0))
                ev(t_om, "form", t)
                ev(at("openai_mac", 0.4), "thock", t, rx)
                label(c, "$1 IN", lx, ly + 230, t, t_om + 0.3, 26, WHITE, a=a * a2)
                label(c, "$1.65 OUT", rx, ry + 230, t, at("openai_mac", 0.2), 26, GLOW, a=a * a2)
                if t > at("openai_mac", 0.58):                          # a trickle of Big Macs, next to Nvidia's torrent
                    rate = 2.5
                    t0 = at("openai_mac", 0.58)
                    n0 = int((t - t0) * rate) + 1
                    for i in range(max(0, n0 - 6), n0):
                        age = t - (t0 + i / rate)
                        y = ry + 290 + 380 * min(1.0, age / 1.3) ** 2
                        if y < 890:
                            mac_icon(c, rx, y, 30, 1.0)
                        ev(t0 + i / rate, "tick", t, rx)
                    label(c, "≈75 BIG MACS · EVERY SECOND", rx, 208, t, at("openai_mac", 0.62), 22, GLOW, a=a * a2)
                    ev(t0, "tick", t, rx)
        a3 = win(t, t_f - 0.1, t_b + 0.2)
        if a3 > 0 and t >= t_f - 0.1:                                  # the diggers again; some strike gold
            with layer(c, a3):
                strike = [i for i in range(N_CROWD) if (i * 7) % 11 == 0]
                ks = seg(t, at("fair", 0.3), at("fair", 0.5))
                cols = np.array([GOLD if (i in strike and ks * len(strike) > strike.index(i)) else WHITE for i in range(N_CROWD)])
                points(c, CROWD[cols == WHITE], 1.0, WHITE, 6.0)
                gold = CROWD[cols == GOLD]
                if len(gold):
                    g = mg.fill(GOLD, 0.5); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
                    for x, y in gold:
                        c.drawCircle(x, y, 16, g)
                    points(c, gold, 1.0, GOLD, 9.0)
                for j, i in enumerate(strike):
                    ev(at("fair", 0.3) + 0.2 * (at("fair", 0.5) - at("fair", 0.3)) * j, "pop", t, CROWD[i][0])
                stroke_polys(c, [q for _, q in PANS_SMALL], WHITE, 1.2, 0.7)
                kst = ease(seg(t, at("fair", 0.62), at("fair", 0.75)))
                stroke_polys(c, STORE, GLOW, 2.0, 0.4 + 0.6 * kst)
                if kst > 0:
                    g = mg.fill(GLOW, 0.3 * kst); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
                    c.drawCircle(CX, 500, 110, g)
                label(c, "SOME FIND GOLD", CX, 800, t, at("fair", 0.35), 20, SOFT, a=a * a3 * (1 - kst))
                label(c, "THE SUPPLIER · PAID FIRST", CX, 668, t, at("fair", 0.66), 22, GLOW, a=a * a3)
                ev(at("fair", 0.66), "confirm", t)


# ---------------------------------------------------------------- IDEA
def railway(c, t):
    t_b, t_a, t_t, t_m, t_l, t_i = ls("before"), ls("acts"), ls("third"), ls("miles"), ls("layers"), ls("imagine")
    a = win(t, t_b + 0.1, t_i + 0.3)
    if a <= 0:
        return
    with layer(c, a):
        a_acts = 1 - ease(seg(t, t_t - 0.3, t_t + 0.3))
        if a_acts > 0:
            with layer(c, a_acts):
                label(c, "1846 · BRITAIN'S RAILWAY MANIA", CX, 250, t, t_a + 0.05, 22, WHITE, a=a * a_acts)
                bignum(c, t, "272 ACTS", 150, CX, 410, at("acts", 0.42))
                n = int(272 * ease(seg(t, at("acts", 0.42), at("acts", 0.8))))
                for k in range(n // 5):                                    # the paperwork piling up
                    y = 850 - k * 2.6
                    c.drawRect(skia.Rect.MakeXYWH(CX - 150 + ((k * 13) % 9) - 4, y, 300, 2.4), mg.fill(WHITE, 0.55))
                for j in range(8):
                    ev(at("acts", 0.42) + j * (at("acts", 0.8) - at("acts", 0.42)) / 8, "paper", t, CX)
                if n:
                    label(c, f"{n} IN ONE YEAR", CX, 525, t, -1, 22, SOFT, a=a * a_acts)
                label(c, "MORE THAN FIVE A WEEK", CX, 570, t, at("acts", 0.86), 22, GLOW, a=a * a_acts)
        a_map = win(t, t_t - 0.2, t_l + 0.3)
        if a_map > 0 and t >= t_t - 0.2:
            with layer(c, a_map):
                kf = seg(t, t_t, t_t + 1.0)
                gone = ease(seg(t, at("third", 0.18), at("third", 0.5)))
                lit = ease(seg(t, t_m + 0.1, t_m + 0.8))
                for (a_, b_), q in RAILS.items():
                    n = max(2, int(len(q) * kf))
                    if (a_, b_) in NEVER:
                        if gone < 1:
                            stroke_polys(c, [q[:n]], WHITE, 1.6, 1 - gone)
                        for k in range(0, n - 1, 3):
                            c.drawLine(*q[k], *q[k + 1], mg.stroke(SOFT, 1.2, 0.5 * gone * (1 - lit * 0.6)))
                    else:
                        stroke_polys(c, [q[:n]], GLOW if lit > 0 else WHITE, 1.8 + 1.2 * lit, 1.0)
                for nm, (x, y) in TOWN.items():
                    c.drawCircle(x, y, 5, mg.fill(WHITE, 0.9))
                ev(t_t, "form", t, 560)
                label(c, "A THIRD NEVER BUILT", 560, 880, t, at("third", 0.25), 20, SOFT, a=a * a_map * (1 - lit))
                kb = seg(t, at("third", 0.62), at("third", 0.84))            # the bubble around it all, then the pop
                if 0 < kb < 1:
                    r = 360 + 40 * ease(kb, "i")
                    c.drawCircle(565, 530, r, mg.stroke(WHITE, 1.4, 0.6 * (1 - kb ** 6)))
                    c.drawCircle(565 - r * 0.35, 530 - r * 0.45, r * 0.12, mg.stroke(WHITE, 1.2, 0.4 * (1 - kb ** 6)))
                if seg(t, at("third", 0.84), at("third", 0.84) + 0.5) > 0 and t < at("third", 0.84) + 0.5:
                    kk = seg(t, at("third", 0.84), at("third", 0.84) + 0.5)
                    ang = np.linspace(0, 2 * np.pi, 48, endpoint=False)
                    rr = 400 + 180 * ease(kk, "o")
                    points(c, np.column_stack([565 + rr * np.cos(ang), 530 + rr * np.sin(ang)]), 1 - kk, WHITE, 4.0)
                ev(at("third", 0.84), "pop", t, 565)
                if t >= t_m:
                    bignum(c, t, "6,000 MILES", 96, CX + 330, 250, t_m + 0.9)
                    label(c, "ABOUT · BY 1850", CX + 330, 322, t, t_m + 1.4, 20, SOFT, a=a * a_map)
                    kg = seg(t, at("miles", 0.62), at("miles", 0.95))
                    if kg > 0:
                        formation(c, segs(GLOBE, 420), t, at("miles", 0.62), 0.8, WHITE, seed_pt=GLOBE_C)
                        n = max(2, int(len(ROUTE) * ease(seg(t, at("miles", 0.72), at("miles", 0.95)))))
                        for k in range(0, n - 1, 2):
                            c.drawLine(*ROUTE[k], *ROUTE[k + 1], mg.stroke(GLOW, 3.0, 1.0))
                        for (x, y) in (LONDON_G, TOKYO_G):
                            c.drawCircle(x, y, 7, mg.fill("#FFFFFF", 1.0))
                        label(c, "LONDON", LONDON_G[0] - 20, LONDON_G[1] - 24, t, at("miles", 0.7), 20, WHITE, align="right", a=a * a_map)
                        label(c, "TOKYO", TOKYO_G[0] + 20, TOKYO_G[1] - 24, t, at("miles", 0.9), 20, WHITE, align="left", a=a * a_map)
                        ev(at("miles", 0.62), "form", t, GLOBE_C[0])
                        ev(at("miles", 0.72), "scan", t, GLOBE_C[0])
        if t >= t_l - 0.2:                                              # the speculation goes; the rails stay
            kd = ease(seg(t, at("layers", 0.05), at("layers", 0.45)))
            specs = np.column_stack([np.linspace(180, 1740, 90), 250 + 60 * np.sin(np.arange(90) * 1.3)])
            specs[:, 1] -= 220 * kd * (np.arange(90) % 5) / 4
            points(c, specs, (1 - kd), WHITE, 6.0)
            label(c, "SPECULATION", CX, 190, t, t_l, 22, SOFT, a=a * (1 - kd))
            kr = ease(seg(t, at("layers", 0.5), at("layers", 0.75)))
            c.drawLine(180, 640, 1740, 640, mg.stroke(GLOW, 2.5 + 2 * kr, 0.6 + 0.4 * kr))
            c.drawLine(180, 700, 1740, 700, mg.stroke(GLOW, 2.5 + 2 * kr, 0.6 + 0.4 * kr))
            for x in range(200, 1740, 60):
                c.drawLine(x, 628, x, 712, mg.stroke(WHITE, 2.0, 0.5 + 0.4 * kr))
            label(c, "INFRASTRUCTURE", CX, 790, t, at("layers", 0.5), 22, GLOW, a=a)
            ev(at("layers", 0.5), "latch", t)


# ---------------------------------------------------------------- IMAGINE
def imagine(c, t):
    t_i, t_w, t_c, t_s, t_tr, t_q, t_r = (ls(x) for x in ("imagine", "whatif", "cheap", "scarce", "trust", "question", "rush"))
    a = win(t, t_i - 0.4, t_r + 0.2)
    if a <= 0:
        return
    with layer(c, a):
        a1 = win(t, t_i - 0.4, t_c + 0.3)
        if a1 > 0:
            with layer(c, a1):
                sg, _ = big("2030", 230, CX, 470)
                k = seg(t, t_i + 0.1, t_i + 1.2)
                n = int(len(sg) * ease(k))
                draw_segs(c, sg[:n][::2], GLOW, 2.2, 1.0)            # dotted: every other segment, a what-if
                ev(t_i + 0.1, "form", t)
                label(c, "IMAGINE", CX, 250, t, t_i + 0.2, 22, GLOW, a=a * a1)
                label(c, "NOT A FORECAST", CX - 220, 690, t, t_w + 0.05, 22, SOFT, a=a * a1)
                if t > t_w + 0.9:
                    f = mg.font(mg.MONO_M, 22)
                    wdt = f.measureText("NOT A FORECAST")
                    c.drawLine(CX - 220 - wdt / 2, 682, CX - 220 - wdt / 2 + wdt * ease(seg(t, t_w + 0.9, t_w + 1.2)), 682, mg.stroke(WHITE, 2, 0.9))
                label(c, "A WHAT-IF", CX + 220, 690, t, at("whatif", 0.55), 22, WHITE, a=a * a1)
        a2 = win(t, t_c - 0.2, t_s + 0.3)
        if a2 > 0:
            with layer(c, a2):
                formation(c, segs(TAP, 300), t, t_c, 0.8, WHITE, seed_pt=(CX - 260, 270))
                ev(t_c, "form", t)
                if t > t_c + 0.6:
                    drops = []
                    for i in range(40):
                        ph = ((t - t_c) * 1.4 + i / 40) % 1.0
                        drops.append((CX + 18 + 6 * math.sin(i * 2.1), 345 + ph * 470))
                    points(c, np.array(drops), 0.95, GLOW, 5.0)
                    c.drawOval(skia.Rect.MakeXYWH(CX - 150, 815, 336, 30), mg.stroke(GLOW, 1.6, 0.6))
                label(c, "INTELLIGENCE · LIKE TAP WATER", CX, 880, t, at("cheap", 0.55), 22, GLOW, a=a * a2)
        a3 = win(t, t_s - 0.1, t_tr + 0.3)
        if a3 > 0:
            with layer(c, a3):
                label(c, "WHAT BECOMES SCARCE?", CX, 250, t, t_s + 0.05, 22, WHITE, a=a * a3)
                for k, (polys, lab) in enumerate(zip(SCARCE, SCARCE_LAB)):
                    t_k = at("scarce", (0.34, 0.5, 0.68, 0.8)[k])
                    if t < t_k:
                        continue
                    formation(c, segs(polys, 200), t, t_k, 0.5, GLOW if k == 0 else WHITE, seed_pt=(SCARCE_X[k], 640))
                    label(c, lab, SCARCE_X[k], 660, t, t_k + 0.1, 22, WHITE, a=a * a3)
                    ev(t_k, "latch", t, SCARCE_X[k])
        a4 = win(t, t_tr - 0.1, t_q + 0.3)
        if a4 > 0:
            with layer(c, a4):
                for k, (x, y) in enumerate(CARDS):
                    t_k = t_tr + 0.05 + 0.05 * k
                    if t < t_k:
                        continue
                    lit = k == TRUSTED and t > at("trust", 0.72)
                    rr = mg.rrect_pts(x, y, 250, 130, 12, 3)
                    stroke_polys(c, [rr], GLOW if lit else WHITE, 1.6, 1.0 if lit else 0.45)
                    for j in range(3):
                        c.drawLine(x + 22, y + 34 + j * 30, x + 22 + (200 - 50 * ((k + j) % 3)), y + 34 + j * 30, mg.stroke(WHITE, 2.2, 0.8 if lit else 0.3))
                    if lit:
                        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, 250, 130), 12, 12), mg.chrome_paint(y, y + 130, 0.35))
                        tick_ = P([(x + 190, y + 70), (x + 208, y + 92), (x + 236, y + 44)])
                        stroke_polys(c, [tick_], "#FFFFFF", 4.0, 1.0)
                    if k % 3 == 0:
                        ev(t_k, "tick", t, x)
                ev(at("trust", 0.72), "confirm", t, CARDS[TRUSTED][0])
                label(c, "WHICH ANSWER TO TRUST", CX, 830, t, at("trust", 0.6), 22, GLOW, a=a * a4)
        a5 = win(t, t_q - 0.1, t_r + 0.2)
        if a5 > 0:
            with layer(c, a5):
                dimq = ease(seg(t, at("question", 0.45), at("question", 0.6)))
                r = 40
                g = mg.fill(GLOW, 0.35 * (1 - 0.8 * dimq)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
                c.drawCircle(CX - 420, 470, r * 2.2, g)
                c.drawCircle(CX - 420, 470, r, mg.fill(TURQ, 1 - 0.75 * dimq))
                label(c, "WHERE THE GOLD IS", CX - 420, 640, t, t_q + 0.3, 22, SOFT, a=a * a5 * (1 - 0.6 * dimq))
                kn = ease(seg(t, at("question", 0.55), at("question", 0.7)))
                if kn > 0:
                    tools = S.pan(CX + 300, 520, 90) + S.shovel(CX + 470, 610, 250) + chip(CX + 620, 470, 55)
                    formation(c, segs(tools, 420), t, at("question", 0.55), 0.8, GLOW, seed_pt=(CX + 420, 700))
                    label(c, "WHAT EVERYONE WILL NEED", CX + 420, 700, t, at("question", 0.62), 22, GLOW, a=a * a5)
                    ev(at("question", 0.55), "form", t, CX + 420)


# ---------------------------------------------------------------- SURFACE
def ending(c, t):
    t_r, t_c = ls("rush"), ls("chain")
    t_src = S.L[IDS.index("chain")]["end"] + 1.2
    a = win(t, t_r - 0.2, t_src + 0.4)
    if a > 0:
        with layer(c, a):
            n = 160
            u = np.arange(n) / n
            ph = (u + (t - t_r) * 0.35) % 1.0
            kc = ease(seg(t, t_c, t_c + 1.0))
            xs = lerp(120, 1800, ph)
            ys = 470 - 160 * np.sin(np.pi * ph) + 30 * np.sin(u * 40)
            tgt = np.array([CHAIN[int(k * LINKS_N / n) % LINKS_N][int(k * 7) % 48] for k in range(n)])
            X = np.column_stack([xs, ys]) * (1 - kc) + tgt * kc
            points(c, X, 1.0 - 0.5 * kc, GOLD, 4.0)
            ev(t_r, "grains", t, CX)
            label(c, "A GOLD RUSH", CX, 760, t, t_r + 0.2, 22, SOFT, a=a * (1 - kc))
            if t >= t_c:
                for k, q in enumerate(CHAIN):
                    t_k = t_c + 0.12 + 0.09 * k
                    if t >= t_k:
                        stroke_polys(c, [q], GLOW if k % 2 == 0 else WHITE, 3.0, ease(seg(t, t_k, t_k + 0.25)))
                        ev(t_k, "link", t, q[0][0])
                label(c, "A SUPPLY CHAIN", CX, 760, t, t_c + 0.5, 22, GLOW, a=a)
    if t >= t_src:                                                   # the sources, typed
        ks = 1 - ease(seg(t, t_src + 7.5, t_src + 8.3))
        for k, s_ in enumerate(SOURCES):
            label(c, s_, 250, 250 + k * 50, t, t_src + 0.2 + (0 if k == 0 else 0.6 + 0.45 * (k - 1)),
                  24 if k == 0 else 20, GLOW if k == 0 else SOFT, align="left", a=ks, cps=17 if k == 0 else 45)


def end_time():
    return S.L[IDS.index("chain")]["end"] + 1.2 + 8.6


def frame(c, t):
    ledger(c, t)
    crowd(c, t)
    year2026(c, t)
    rome(c, t)
    chip_scene(c, t)
    dig(c, t)
    railway(c, t)
    imagine(c, t)
    ending(c, t)
