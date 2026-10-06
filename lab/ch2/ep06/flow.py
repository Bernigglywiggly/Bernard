#!/usr/bin/env python3
"""HOW THEY PROFIT · EP06 (Visa) as ONE DRAWING AND ONE CAMERA: the look the user chose on 6 Oct (rend_test.py "B",
after the pollar.news references). No cuts and no fades between scenes: everything lives on one page at three
scales, and the camera travels between them on the narration's timings (script.py line ids, build*/lines.json).

  scale 1    the North Atlantic set in type, the crossing, and under it $17 trillion as a matrix of cells
  scale 12   inside the crossing: the four parties on the wire, interchange passing under the network
  (to come)  the three meters, the money handed back, the one lit cell, half of it profit, the weak point, the close

All seven chapters are drawn (6 Oct). keys2() and later() hold chapters 3-6.

    cd lab/ch2/ep06
    EP_BUILD=build_est ~/youtube/.venv/bin/python flow.py still 0.5 14 20 27 40 50 60 72 84 97 108 118 128 146
    EP_BUILD=build_est ~/youtube/.venv/bin/python flow.py clip 0 60            # 960x540 animatic, no sound
"""
import math
import os
import subprocess
import sys

import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import engine  # noqa: E402,F401  (paths)
from engine import tl  # noqa: E402

import rend_test as R  # noqa: E402
from look_test import W, H, col, font, glow, text  # noqa: E402

K = R.K
FPS = 30
P0, P1, arc, sm = R.P0, R.P1, R.arc, R.sm
MID = arc(0.5)                                       # where the wire is flat: the four parties live here, 12x smaller
NODE_W, NODE_H, STEP = 30.0, 13.0, 44.0
NODES = [("The café", "card tapped here"), ("The café's bank", "collects card payments"),
         ("The network", "carries the message"), ("The card's bank", "issued the card")]
NX = [MID[0] + (i - 1.5) * STEP for i in range(4)]   # west to east on screen; the message runs from the café
NY = MID[1]


def L(name):
    return tl.ls(name)


def E(name):
    return tl.le(name)


def mono(size):
    return font("IBMPlexMono-400", size)


def sans(size, weight=600):
    return font(f"InterTight-{weight}", size)


def hair(a=0.85, w=1.2):
    return skia.Paint(Color=col(K["light"], a), AntiAlias=True, StrokeWidth=w, Style=skia.Paint.kStroke_Style)


# ---------------------------------------------------------------- scale 1: the ocean and the figure
def ocean(c, t, z=1.0, far=1.0, near=0.0):
    """The map and the crossing fade as the camera enters the wire (far); the place labels and tags also step back
    whenever the camera is close after the opening, so no transit ever passes giant cropped words; the figure and its
    matrix always stay."""
    ev = dict(out=(L("ocean") + 0.6, L("ocean") + 4.8), back=(L("ocean") + 5.4, E("ocean") - 0.4),
              fig=L("scale") + 0.9, lit=L("never") + 3.0)
    R.MAP = R.MAP or R.map_picture()
    out, back = sm(t, *ev["out"]), sm(t, *ev["back"])
    lab = far * (1.0 if t < L("scale") - 0.3 else 1.0 - sm(z, 1.05, 1.35))
    if far > 0.004:
        c.saveLayerAlpha(None, int(255 * far))
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(0, 0, W, R.MY + R.MH + 60))       # the map's picture ends at its ruler
        c.drawPicture(R.MAP)
        c.restore()
        pulse = (t % 1.6) / 1.6
        c.drawCircle(P0[0], P0[1], 13 + 40 * pulse, skia.Paint(Color=col(K["acc"], 0.5 * (1 - pulse)), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4))
        if out > 0:
            p = skia.Path()
            for i in range(max(1, int(80 * out)) + 1):
                (p.moveTo if i == 0 else p.lineTo)(*arc(i / 80))
            g = glow(K["acc"], 0.45, 14)
            g.setStyle(skia.Paint.kStroke_Style)
            g.setStrokeWidth(6)
            c.drawPath(p, g)
            c.drawPath(p, skia.Paint(Color=col(K["acc"]), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8))
            if back < 1:
                px, py = arc(out if back <= 0 else 1 - back)
                c.drawCircle(px, py, 20, glow(K["acc"], 0.5, 14))
                c.drawRect(skia.Rect.MakeXYWH(px - 9, py - 9, 18, 18), skia.Paint(Color=col(K["acc"]), AntiAlias=True))
        c.restore()
    if lab > 0.004:
        c.saveLayerAlpha(None, int(255 * lab))
        R.place(c, P0, "A café, Lisbon", "38.72N  009.14W  ·  card tapped", -1, sm(t, 0.1, 0.9))
        R.place(c, P1, "A bank, Ohio", "39.96N  083.00W  ·  issued the card", 1, sm(t, ev["out"][1] - 0.3, ev["out"][1] + 0.5))
        if 0.05 < out < 1 and back <= 0:
            R.tag(c, *arc(out), f"message out  ·  {0.5 * out:0.2f} s", 1.0)
        elif 0 < back < 1:
            R.tag(c, *arc(1 - back), f"answer back  ·  {0.5 + 0.5 * back:0.2f} s", 1.0, -1)
        elif back >= 1:
            R.tag(c, P0[0], P0[1] - 30, "approved  ·  about 1 s", sm(t, ev["back"][1], ev["back"][1] + 0.5), -1)
        c.restore()
    # the figure and its matrix
    kf = sm(t, ev["fig"], ev["fig"] + 0.6)
    FIG, GX, GY, CELL, GAP = R.FIG, R.GX, R.GY, R.CELL, R.GAP
    if kf > 0:
        figa = kf * (1.0 - sm(z, 7.0, 10.0))
        grid_a = 1.0 - sm(z, 1.15, 1.9) * near                          # the matrix is not part of the dive into the wire
        figa *= grid_a
        text(c, "$17 trillion", FIG[0], FIG[1] + 14 * (1 - kf), font("InterTight-600", 150), K["light"], figa)
        text(c, "payments and cash volume on the network  ·  fiscal 2025  ·  Form 10-K", FIG[0] + 6, FIG[1] + 58, font("IBMPlexMono-400", 22), K["dim"], figa, 0.5)
        fill = sm(t, ev["fig"] + 0.3, ev["fig"] + 2.4) * 170
        pc = skia.Paint(Color=col(K["light"], 0.42 * grid_a), AntiAlias=True)
        for j in range(10):
            for i in range(17):
                if i * 10 + j < fill and not (i == 16 and j == 9):
                    c.drawRect(skia.Rect.MakeXYWH(GX + i * (CELL + GAP), GY + j * (CELL + GAP), CELL, CELL), pc)
        text(c, "each cell $100 billion moved", GX, GY + 10 * (CELL + GAP) + 22, font("IBMPlexMono-400", 19), K["dim"], figa, 0.5)
        lx, ly = R.LIT
        kl = sm(t, ev["lit"], ev["lit"] + 0.6)
        if fill >= 169:
            c.drawRect(skia.Rect.MakeXYWH(lx, ly, CELL, CELL), skia.Paint(Color=col(K["light"], 0.5), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.6))
        kl *= grid_a
        if kl > 0:
            c.drawCircle(lx + CELL / 2, ly + CELL * 0.8, 16 * kl, glow(K["acc"], 0.45, 8))
            c.drawRect(skia.Rect.MakeXYWH(lx, ly + CELL * (1 - 0.4 * kl), CELL, CELL * 0.4 * kl), skia.Paint(Color=col(K["acc"]), AntiAlias=True))
            kc = sm(t, W_("cents", "kept", -0.6), W_("cents", "kept", 0.2)) * (1.0 - sm(z, 8.0, 11.0)) if "cents" in tl.IDS else 0.0
            m6 = font("IBMPlexMono-400", 5.2)
            text(c, "$40.0 billion", lx + CELL + 6, ly + CELL * 0.82, m6, K["acc"], kc, 0.2)
            text(c, "what Visa kept", lx + CELL + 6, ly + CELL * 0.82 + 7, m6, K["dim"], kc, 0.2)
            text(c, "about 24¢ of every $100 moved", lx + CELL + 6, ly + CELL * 0.82 + 16, m6, K["light"], kc, 0.2)
    return ev


# ---------------------------------------------------------------- scale 12: the four parties on the wire
def lerp_(a, b, u):
    return a + (b - a) * u


def lod(z, a, b):
    """Detail that only exists once the camera is close enough to read it."""
    return sm(z, a, b)


def party(c, i, k, t, hot=False):
    if k <= 0:
        return
    x, y = NX[i], NY
    r = skia.Rect.MakeXYWH(x - NODE_W / 2, y - NODE_H / 2, NODE_W, NODE_H)
    c.drawRect(r, skia.Paint(Color=col(K["bg"], 0.96 * k)))
    c.drawRect(r, hair(0.9 * k, 0.16))
    if hot:                                                          # the network: the accent, and a slow breath
        b = 0.5 + 0.5 * math.sin(t * 1.3)
        c.drawRect(r, skia.Paint(Color=col(K["acc"], k), AntiAlias=True, StrokeWidth=0.22, Style=skia.Paint.kStroke_Style))
        g = glow(K["acc"], (0.25 + 0.2 * b) * k, 1.6)
        g.setStyle(skia.Paint.kStroke_Style)
        g.setStrokeWidth(0.5)
        c.drawRect(r, g)
    name, note = NODES[i]
    text(c, name, x, y + 0.6, sans(3.0), K["light"], k, align="center")
    n = int(len(note) * min(1.0, k * 1.5))
    text(c, note[:n], x, y + 3.9, mono(1.45), K["dim"], k, 0.05, "center")
    text(c, f"0{i + 1}", x - NODE_W / 2 + 1.2, y - NODE_H / 2 + 2.4, mono(1.3), K["acc"] if hot else K["dim"], k, 0.05)


def wire_packets(c, t, k):
    """The message, small, running the wire through all four parties and back."""
    if k <= 0:
        return
    span = NX[3] - NX[0] + NODE_W
    for j in range(3):
        u = ((t * 0.16 + j / 3) % 1.0)
        u = 1 - abs(2 * u - 1)                                       # there and back
        x = NX[0] - NODE_W / 2 + span * u
        if any(abs(x - nx) < NODE_W / 2 for nx in NX):
            continue
        c.drawCircle(x, NY, 1.5, glow(K["acc"], 0.5 * k, 1.0))
        c.drawRect(skia.Rect.MakeXYWH(x - 0.9, NY - 0.9, 1.8, 1.8), skia.Paint(Color=col(K["acc"], k), AntiAlias=True))


def interchange(c, t, k, red=0.0):
    """Coins from the café's bank to the card's bank, passing UNDER the network without stopping."""
    if k <= 0:
        return
    xa, xb, y0, dip = NX[1], NX[3], NY + NODE_H / 2 + 0.8, 15.0
    p = skia.Path()
    n = 60
    for j in range(int(n * k) + 1):
        u = j / n
        (p.moveTo if j == 0 else p.lineTo)(xa + (xb - xa) * u, y0 + dip * math.sin(math.pi * u))
    c.drawPath(p, hair(0.9, 0.2))
    if k >= 1:
        for j in range(5):
            u = (t * 0.11 + j / 5) % 1.0
            x, y = xa + (xb - xa) * u, y0 + dip * math.sin(math.pi * u)
            c.drawCircle(x, y, 1.05, skia.Paint(Color=col(K["bg"]), AntiAlias=True))
            c.drawCircle(x, y, 1.05, hair(1.0, 0.2))
            text(c, "$", x, y + 0.55, mono(1.5), K["light"], 1.0, 0, "center")


def box_label(c, s, x, y, k, size=1.7, align="left"):
    """The accent as a highlight box behind dark type."""
    if k <= 0:
        return
    f = mono(size)
    s = s[:max(1, int(len(s) * min(1.0, k * 2)))]
    w = sum(f.measureText(ch) + 0.05 for ch in s)
    x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
    c.drawRect(skia.Rect.MakeXYWH(x0 - 0.7, y - size * 1.05, w + 1.4, size * 1.45), skia.Paint(Color=col(K["acc"]), AntiAlias=True))
    text(c, s, x0, y, f, K["bg"], 1.0, 0.05)


def route(c, t, z):
    k = lod(z, 1.6, 3.2)
    if k <= 0:
        return
    c6_ = sm(t, L("weak") + 1.5, L("weak") + 2.6) if "weak" in tl.IDS else 0.0
    c.drawLine(lerp_(NX[0] - 60, NX[1] - NODE_W / 2 - 6, c6_), NY, NX[3] + NODE_W / 2 + 10, NY, skia.Paint(Color=col(K["acc"], 0.9 * k), AntiAlias=True, StrokeWidth=0.18))
    text(c, "one card payment  ·  four parties", NX[0] - NODE_W / 2, NY - 17, mono(1.7), K["dim"], k * sm(t, L("four"), L("four") + 0.8) * (1 - c6_), 0.05)
    c.drawLine(lerp_(NX[0] - NODE_W / 2, NX[1] - NODE_W / 2, c6_), NY - 15, NX[3] + NODE_W / 2, NY - 15, hair(0.35 * k, 0.1))
    c6 = sm(t, L("weak") + 1.5, L("weak") + 2.6) if "weak" in tl.IDS else 0.0     # the last chapter frames the three right-hand parties
    for i in range(4):                                               # the four places, sketched before they are named
        r = skia.Rect.MakeXYWH(NX[i] - NODE_W / 2, NY - NODE_H / 2, NODE_W, NODE_H)
        c.drawRect(r, skia.Paint(Color=col(K["bg"], 0.9 * k)))
        c.drawRect(r, hair(0.2 * k * sm(t, L("four") + 0.6 + 0.2 * i, L("four") + 1.2 + 0.2 * i) * (1 - c6 if i == 0 else 1), 0.1))
    party(c, 0, k * sm(t, L("four") + 1.2, L("four") + 1.9) * (1 - c6), t)
    party(c, 1, k * sm(t, L("shopbank") + 0.2, L("shopbank") + 0.9), t)
    party(c, 3, k * sm(t, L("yourbank") + 0.2, L("yourbank") + 0.9), t)
    party(c, 2, k * sm(t, L("quote") + 0.2, L("quote") + 0.9), t, hot=True)
    wire_packets(c, t, k * sm(t, L("quote") + 1.0, L("quote") + 1.6) * (1 - c6))
    # the annual report, set above the network
    kq = sm(t, tl.word("quote", "plain") - 0.2, tl.word("quote", "plain") + 0.5)
    if kq > 0:
        qx, qy = NX[2], NY - 23
        c.drawLine(NX[2], NY - NODE_H / 2, NX[2], qy + 3.2, hair(0.6 * kq, 0.1))
        text(c, "“Visa is not a financial institution.”", qx, qy - 4.2, sans(3.4), K["light"], kq, align="center")
        text(c, "We do not issue cards, extend credit or set rates and fees for account holders.", qx, qy - 0.6, mono(1.5), K["dim"], kq, 0.05, "center")
        text(c, "Visa Form 10-K  ·  fiscal 2025", qx, qy + 1.8, mono(1.25), K["dim"], 0.8 * kq, 0.05, "center")
    # who carries the risk
    box_label(c, "carries the loss when a bill goes unpaid", NX[3], NY - NODE_H / 2 - 2.2, sm(t, tl.word("risk", "loss") - 0.3, tl.word("risk", "loss") + 0.4), 1.5, "center")
    # interchange
    ki = sm(t, L("fee") + 0.4, L("fee") + 2.2)
    interchange(c, t, ki)
    gone6 = 1.0 - (sm(t, L("meters") + 0.2, L("meters") + 1.0) if "meters" in tl.IDS else 0.0) + (sm(t, L("weak") + 2.5, L("weak") + 3.5) if "weak" in tl.IDS else 0.0)
    box_label(c, "interchange", (NX[1] + NX[3]) / 2, NY + NODE_H / 2 + 19.5, sm(t, L("interchange") + 0.3, L("interchange") + 0.9) * (1.0 if gone6 > 0.5 else 0.0), 2.0, "center")
    text(c, "paid by the shop's bank to the cardholder's bank", (NX[1] + NX[3]) / 2, NY + NODE_H / 2 + 22.6, mono(1.35), K["dim"],
         sm(t, L("interchange") + 1.2, L("interchange") + 1.9) * min(1.0, gone6), 0.05, "center")
    ks = sm(t, tl.word("sets", "writes") - 0.2, tl.word("sets", "writes") + 0.5)
    c.drawRect(skia.Rect.MakeXYWH(NX[2] - 13, NY + NODE_H / 2 + 1.2, 26, 5.2), skia.Paint(Color=col(K["bg"], 0.92 * ks)))
    text(c, "sets the default rates", NX[2], NY + NODE_H / 2 + 3.0, mono(1.45), K["acc"], ks * (1 - sm(t, L("fee") - 9, L("fee") - 8)), 0.05, "center")
    text(c, "collects none of it", NX[2], NY + NODE_H / 2 + 5.4, mono(1.45), K["light"], sm(t, tl.word("sets", "without") - 0.2, tl.word("sets", "without") + 0.5), 0.05, "center")
    gone = 1.0 - (sm(t, L("meters") + 0.3, L("meters") + 1.3) if "meters" in tl.IDS else 0.0)   # the why leaves with its chapter
    kw = sm(t, L("whyset") + 1.0, L("whyset") + 1.8) * gone
    text(c, "The fee pays banks to issue the cards.", NX[2], NY + 38, sans(3.0), K["light"], kw, align="center")
    text(c, "Every card sends more messages down the wire.", NX[2], NY + 42.4, sans(3.0), K["acc"],
         sm(t, tl.word("whyset", "every") - 0.2, tl.word("whyset", "every") + 0.6) * gone, align="center")


# ================================================================ chapters 3-6 (added 6 Oct, same page, same camera)
RED = "#FF6A4D"                                      # the one second colour, kept for the weak point
X0 = NX[0] - NODE_W / 2
MT = NY + 58.0                                       # the meters, under the route
HT = MT + 72.0                                       # the money handed back, under the meters
RX = NX[3] + NODE_W / 2 + 16.0                       # the last chapter's column, right of the route
METERS = [("service", "01  service  ·  for being on the network at all", 17.5, "$17.5B", "service", "brought"),
          ("processing", "02  data processing  ·  a charge on every message", 20.0, "$20.0B", "processing", "earned"),
          ("border", "03  international  ·  only when card and shop are in different countries", 14.2, "$14.2B", "border", "earned"),
          ("other", "04  other  ·  licences and extra services", 4.1, "$4.1B", "other", "added")]


def W_(line, word, d=0.0):
    try:
        return tl.word(line, word) + d
    except (KeyError, ValueError):
        return tl.ls(line) + d


def cells(c, x, y, n, k, size=2.0, gap=0.5, h=4.4, colr=None, a=0.5):
    """A bar made of small cells, filling left to right."""
    m = int(n * k + 0.999) if k > 0 else 0
    p = skia.Paint(Color=col(colr or K["light"], a), AntiAlias=True)
    for i in range(m):
        c.drawRect(skia.Rect.MakeXYWH(x + i * (size + gap), y, size, h), p)
    return x + m * (size + gap)


def meters(c, t, z):
    k0 = sm(t, L("meters") + 0.3, L("meters") + 1.0)
    if k0 <= 0 or z < 2.5 or t > L("weak"):
        return
    m_out = 1.0 - sm(t, L("back") + 0.2, L("back") + 1.4)                # the meters leave as the money handed back arrives
    h_out = 1.0 - sm(t, L("cents") + 0.4, L("cents") + 1.6)
    if m_out > 0.004:
        c.saveLayerAlpha(None, int(255 * m_out))
        _meters(c, t, k0)
        c.restore()
    if h_out > 0.004:
        c.saveLayerAlpha(None, int(255 * h_out))
        _handed(c, t)
        c.restore()


def _meters(c, t, k0):
    text(c, "What Visa charges the banks", X0, MT, sans(3.6), K["light"], k0)
    text(c, "three meters  ·  fiscal 2025  ·  Visa results, 28 Oct 2025", X0, MT + 3.4, mono(1.4), K["dim"], k0, 0.05)
    c.drawLine(X0, MT + 5.2, X0 + 150 * k0, MT + 5.2, hair(0.3, 0.1))
    for i, (lid, lab, v, disp, wl, ww) in enumerate(METERS):
        y = MT + 12 + i * 13.0
        ka = sm(t, L("meters") + 0.7 + 0.25 * i, L("meters") + 1.3 + 0.25 * i)
        if ka <= 0:
            continue
        on = sm(t, L(lid) + 0.2, L(lid) + 0.8) if lid != "processing" else sm(t, L("count") + 0.2, L("count") + 0.8)
        text(c, lab, X0, y - 1.4, mono(1.5), K["light"] if on > 0.5 else K["dim"], ka, 0.05)
        c.drawRect(skia.Rect.MakeXYWH(X0, y, 100, 4.4), hair(0.22 * ka, 0.1))            # the empty track
        tv = W_(wl, ww, -0.5)
        kb = sm(t, tv, tv + 1.2)
        hot = lid == "processing"
        xe = cells(c, X0, y, int(v * 2 + 0.5), kb, colr=K["acc"] if hot else None, a=0.9 if hot else 0.5)
        text(c, disp, xe + 2.0, y + 4.0, sans(4.6), K["acc"] if hot else K["light"], sm(t, tv + 0.9, tv + 1.4))
    # the second meter counts messages: a stream of them along its row
    yc = MT + 12 + 13.0
    kc = sm(t, W_("count", "processed", -0.3), W_("count", "processed", 0.3))
    text(c, "257.5 billion transactions processed", X0 + 122, yc + 1.6, mono(1.7), K["light"], kc, 0.05)
    box_label(c, "about 700 million a day", X0 + 122.7, yc + 5.6, sm(t, L("daily") + 0.4, L("daily") + 1.0), 1.7)
    if kc > 0:
        for j in range(7):
            u = (t * 0.22 + j / 7) % 1.0
            c.drawRect(skia.Rect.MakeXYWH(X0 + 100 * u, yc + 5.6, 1.1, 0.7), skia.Paint(Color=col(K["acc"], kc * (1 - abs(2 * u - 1)) ** 0.5), AntiAlias=True))


def _handed(c, t):
    kh = sm(t, L("back") + 0.9, L("back") + 1.6)
    if kh > 0:
        y, sc, hh = HT + 10, 1.8, 8.0
        wi, wn = 15.8 * sc, 40.0 * sc
        text(c, "Before any of it counts as revenue", X0, HT, sans(3.6), K["light"], kh)
        text(c, "charged to banks and partners  ·  $55.8 billion", X0, HT + 3.4, mono(1.4), K["dim"], kh, 0.05)
        ki = sm(t, W_("incentives", "paid", -0.2), W_("incentives", "paid", 0.8))
        kn = sm(t, L("net") + 0.1, L("net") + 0.9)
        drop = 12.0 * sm(t, W_("incentives", "incentives", 0.0), W_("incentives", "incentives", 1.0))
        c.drawRect(skia.Rect.MakeXYWH(X0, y, wn * kh, hh), hair(0.8, 0.14))
        c.drawRect(skia.Rect.MakeXYWH(X0 + wn, y + drop, wi * kh, hh), skia.Paint(Color=col(K["light"], 0.16 + 0.2 * ki), AntiAlias=True))
        c.drawRect(skia.Rect.MakeXYWH(X0 + wn, y + drop, wi * kh, hh), hair(0.6, 0.12))
        text(c, "$15.8B", X0 + wn + 2, y + drop + 5.6, sans(4.2), K["light"], ki)
        text(c, "handed back as incentives", X0 + wn + wi + 2, y + drop + 3.0, mono(1.5), K["dim"], ki, 0.05)
        text(c, "the price of keeping cards on this network", X0 + wn + wi + 2, y + drop + 5.6, mono(1.5), K["dim"],
             sm(t, W_("incentives", "price", -0.2), W_("incentives", "price", 0.5)), 0.05)
        if kn > 0:
            c.drawRect(skia.Rect.MakeXYWH(X0, y, wn * kn, hh), skia.Paint(Color=col(K["acc"]), AntiAlias=True))
            text(c, "$40.0 billion", X0 + 2.5, y + 5.9, sans(5.2), K["bg"], kn)
            text(c, "net revenue  ·  fiscal 2025", X0 + 40, y + 5.2, mono(1.6), K["bg"], kn, 0.05)


def cell_story(c, t, z):
    """Back at the one lit cell: 24 cents, then half of it profit, and why."""
    lx, ly = R.LIT
    CELL = R.CELL
    if z < 4 or t < L("thin"):
        return
    sy, shh = ly + CELL * 0.6, CELL * 0.4                               # the lit sliver: $40.0B
    text(c, "net revenue  $40.0B", lx + CELL - 1.2, sy - 1.6, mono(1.5), K["dim"], sm(t, L("thin") + 0.5, L("thin") + 1.2), 0.05, "right")
    ko = sm(t, W_("costs", "cost", -0.3), W_("costs", "cost", 0.5))
    kp = sm(t, W_("profit", "profit", -0.3), W_("profit", "profit", 0.6))
    kf = sm(t, W_("half", "fifty", -0.3), W_("half", "fifty", 0.5))
    if ko > 0:                                                          # the right half dims: what it costs to run, and tax
        c.drawRect(skia.Rect.MakeXYWH(lx + CELL / 2, sy, CELL / 2, shh), skia.Paint(Color=col(K["bg"], 0.62 * ko)))
        text(c, "$16.0B to run", lx + CELL / 2 + 1.0, sy + 4.0, mono(1.35), K["light"], ko, 0.03)
        text(c, "then tax", lx + CELL / 2 + 1.0, sy + 6.4, mono(1.35), K["light"], ko * kp, 0.03)
    if kp > 0:
        c.drawLine(lx + CELL / 2, sy, lx + CELL / 2, sy + shh * kp, skia.Paint(Color=col(K["bg"]), AntiAlias=True, StrokeWidth=0.3))
        text(c, "$20.1B", lx + 1.0, sy + 6.0, sans(4.0), K["bg"], kp)
        text(c, "profit after tax", lx + 1.0, sy + 9.0, mono(1.3), K["bg"], kp, 0.03)
    text(c, "50¢ per dollar", lx + 1.0, sy + 12.4, mono(1.35), K["bg"], kf, 0.03)
    # why: what a bank carries and the network doesn't
    wx, wy = lx + CELL + 10, ly - 2.0
    kw = sm(t, L("why") + 0.4, L("why") + 1.1)
    text(c, "A bank needs", wx, wy, mono(1.6), K["dim"], kw, 0.05)
    for i, (s_, wd) in enumerate((("branches", "branches"), ("loan books", "loan"), ("reserves for unpaid debts", "reserves"))):
        text(c, s_, wx, wy + 4.2 + i * 3.6, sans(2.8), K["light"], sm(t, W_("why", wd, -0.2), W_("why", wd, 0.4)))
    kv = sm(t, W_("why", "data", -0.5), W_("why", "data", 0.2))
    text(c, "The network needs", wx + 44, wy, mono(1.6), K["acc"], kv, 0.05)
    for i, (s_, wd) in enumerate((("data centres", "data"), ("a rulebook", "rulebook"))):
        text(c, s_, wx + 44, wy + 4.2 + i * 3.6, sans(2.8), K["acc"], sm(t, W_("why", wd, -0.2), W_("why", wd, 0.4)))
    text(c, "one more message costs it almost nothing", wx + 44, wy + 13.0, mono(1.4), K["dim"], sm(t, W_("why", "almost", -0.4), W_("why", "almost", 0.3)), 0.05)
    kr = sm(t, W_("returned", "sent", -0.3), W_("returned", "sent", 0.6))
    if kr > 0:
        c.drawLine(lx + 1.6, sy, lx + 1.6, sy - 15 * kr, skia.Paint(Color=col(K["acc"], kr), AntiAlias=True, StrokeWidth=0.25))
        box_label(c, "$22.8B back to shareholders", lx + 3.6, sy - 13.2, kr, 1.5)
        text(c, "buybacks and dividends, fiscal 2025", lx + 3.0, sy - 10.4, mono(1.2), K["dim"], kr, 0.03)


def rulebook(c, t, z):
    if t < L("weak") - 0.5 or z < 2.5:
        return
    kr = sm(t, L("weak") + 0.4, L("weak") + 1.6)
    xa, xb, y0, dip = NX[1], NX[3], NY + NODE_H / 2 + 0.8, 15.0
    p = skia.Path()
    for j in range(int(60 * kr) + 1):
        u = j / 60
        (p.moveTo if j == 0 else p.lineTo)(xa + (xb - xa) * u, y0 + dip * math.sin(math.pi * u))
    g = glow(RED, 0.5 * kr, 1.4)
    g.setStyle(skia.Paint.kStroke_Style)
    g.setStrokeWidth(0.9)
    c.drawPath(p, g)
    c.drawPath(p, skia.Paint(Color=col(RED, kr), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.32))
    ksu = sm(t, L("sued") + 0.2, L("sued") + 0.9)
    text(c, "Shops have taken Visa to court", RX, NY - 16, sans(3.9), K["light"], ksu)
    text(c, "over this fee for years.", RX, NY - 11.2, sans(3.9), K["light"], ksu)
    ks = sm(t, W_("suits", "set", -0.3), W_("suits", "set", 0.5))
    text(c, "$2.5 billion", RX, NY + 3.5, sans(12.0), K["light"], ks)
    text(c, "set aside for the interchange litigation", RX, NY + 8.6, mono(2.0), K["dim"], ks, 0.05)
    text(c, "and other legal matters  ·  fiscal 2025", RX, NY + 11.6, mono(2.0), K["dim"], ks, 0.05)
    kg = sm(t, L("regulators") + 0.6, L("regulators") + 1.4)
    for i, ln in enumerate(("“Regulatory authorities and central banks", "in a number of jurisdictions have reviewed",
                            "or are reviewing these fees, rules and practices.”")):
        text(c, ln, RX, NY + 21 + i * 4.5, sans(3.3), K["light"], kg)
    text(c, "Visa Form 10-K  ·  fiscal 2025", RX, NY + 34.0, mono(1.9), K["dim"], kg, 0.05)
    kv = sm(t, W_("verdict", "product", -0.4), W_("verdict", "product", 0.4))
    kv2 = sm(t, W_("verdict", "lets", -0.3), W_("verdict", "lets", 0.5))
    text(c, "Visa's real product is the rulebook", RX, NY + 46, sans(5.6), K["light"], kv)
    text(c, "that lets a café in Lisbon", RX, NY + 53, sans(5.6), K["acc"], kv2)
    text(c, "trust a bank in Ohio.", RX, NY + 60, sans(5.6), K["acc"], kv2)
    text(c, "The wires only deliver it.", RX, NY + 65.2, mono(2.2), K["dim"], sm(t, W_("verdict", "wires", -0.3), W_("verdict", "wires", 0.5)), 0.05)
    ksh = sm(t, L("shop") + 0.3, L("shop") + 1.0)
    text(c, "If you run a shop: interchange goes", RX, NY + 75, sans(3.6), K["light"], ksh)
    text(c, "to the banks, not to Visa.", RX, NY + 79.6, sans(3.6), K["light"], ksh)
    box_label(c, "the rate your bank quotes is the part to negotiate", RX + 0.9, NY + 85.4, sm(t, W_("shop", "rate", -0.4), W_("shop", "rate", 0.4)), 2.3)


def last_crossing(c, t):
    """The close: the same crossing again, so the film ends where it began."""
    t0 = L("close") + 1.6
    out, back = sm(t, t0, t0 + 2.2), sm(t, t0 + 2.5, t0 + 4.6)
    if out <= 0 or back >= 1:
        return
    px, py = arc(out if back <= 0 else 1 - back)
    c.drawCircle(px, py, 20, glow(K["acc"], 0.5, 14))
    c.drawRect(skia.Rect.MakeXYWH(px - 9, py - 9, 18, 18), skia.Paint(Color=col(K["acc"]), AntiAlias=True))


def later(c, t, z):
    if "meters" not in tl.IDS:
        return
    meters(c, t, z)
    cell_story(c, t, z)
    rulebook(c, t, z)


def keys2():
    if "meters" not in tl.IDS:
        return []
    lx, ly = R.LIT
    CELL = R.CELL
    rc = ((NX[1] + NX[3]) / 2, NY + 11)
    wk = (X0 + 163, NY + 8)                                             # the last chapter: the route and its column in one frame
    return [(L("meters") + 2.2, (X0 + 80, MT + 34, 8.4)), (E("service"), (X0 + 80, MT + 34, 8.8)),
            (L("count") + 2.0, (X0 + 86, MT + 34, 8.9)), (E("processing"), (X0 + 88, MT + 35, 9.2)),
            (L("border") + 2.4, (X0 + 80, MT + 36, 9.0)), (E("other"), (X0 + 78, MT + 38, 9.3)),
            (L("back") + 2.2, (X0 + 70, HT + 12, 9.2)), (E("incentives"), (X0 + 74, HT + 15, 9.6)),
            (E("net"), (X0 + 58, HT + 13, 10.6)),
            (L("cents") + 2.6, (960, 880, 0.60)), (W_("cents", "kept", 0.4), (R.LITC[0] + 40, R.LITC[1] + 26, 6.4)),
            (E("cents"), (R.LITC[0] + 44, R.LITC[1] + 26, 6.9)),
            (L("thin") + 2.6, (lx + CELL / 2 + 6, ly + CELL * 0.72, 17.0)), (E("costs"), (lx + CELL / 2 + 4, ly + CELL * 0.76, 19.0)),
            (E("half"), (lx + CELL / 2, ly + CELL * 0.8, 21.0)),
            (L("why") + 2.6, (lx + CELL + 34, ly + 8, 11.0)), (E("why"), (lx + CELL + 36, ly + 9, 11.3)),
            (L("returned") + 2.2, (lx + CELL / 2 + 36, ly + 10, 11.4)), (E("returned"), (lx + CELL / 2 + 36, ly + 9, 11.8)),
            (L("weak") + 1.5, (960, 880, 0.60)),
            (L("weak") + 3.8, (wk[0], wk[1], 7.7)), (E("suits"), (wk[0], wk[1] + 2, 7.8)),
            (E("regulators"), (wk[0], wk[1] + 10, 7.8)),
            (L("verdict") + 2.6, (wk[0], wk[1] + 30, 7.7)), (E("verdict"), (wk[0], wk[1] + 33, 7.8)),
            (L("shop") + 2.0, (wk[0], wk[1] + 46, 7.7)), (E("shop"), (wk[0], wk[1] + 47, 7.8)),
            (L("close") + 1.6, (960, 440, 1.0)), (E("close") + 3.0, (960, 436, 1.04))]


# ---------------------------------------------------------------- the camera: one move, keyed to the narration
def camera(t):
    o0, o1 = L("ocean") + 0.6, L("ocean") + 4.8
    px, py = arc(sm(t, o0, o1))
    ride = (px + 110, py + 30, 2.3)
    lis = (P0[0] - 150, P0[1] + 30)
    rc = ((NX[1] + NX[2]) / 2, NY + 2)                               # the route, all four parties in frame
    keys = [(0.0, (lis[0], lis[1], 2.75)), (L("ocean") + 0.4, (lis[0], lis[1], 2.45)), (o0 + 1.0, ride), (o1, ride),
            (E("ocean"), (960, 520, 1.0)), (L("scale") - 0.3, (960, 560, 1.0)), (L("scale") + 1.6, (960, 1400, 1.02)),
            (L("never") - 0.5, (960, 1404, 1.06)), (L("never") + 5.5, (R.LITC[0] - 60, R.LITC[1] + 20, 4.6)),
            (E("never") - 0.2, (R.LITC[0] - 30, R.LITC[1] + 24, 5.2)),
            (L("four") + 1.5, (960, 880, 0.60)),                        # the whole page, on the way to the wire
            (L("four") + 4.4, (NX[0] + 34, NY + 2, 8.6)), (L("shopbank") + 1.0, (NX[0] + 40, NY + 2, 9.0)),
            (L("yourbank") + 1.5, (rc[0] + 10, rc[1], 9.6)), (L("quote") - 0.3, (rc[0], rc[1], 9.4)),
            (L("quote") + 2.2, (NX[2], NY - 12, 11.5)), (E("quote"), (NX[2], NY - 13, 12.2)),
            (L("risk") + 2.2, ((NX[2] + NX[3]) / 2 + 2, NY - 9, 10.4)), (E("risk"), ((NX[2] + NX[3]) / 2 + 3, NY - 8, 10.9)),
            (L("fee") + 2.4, ((NX[1] + NX[3]) / 2, NY + 9, 9.4)), (E("interchange"), ((NX[1] + NX[3]) / 2, NY + 10, 9.9)),
            (L("sets") + 2.0, (NX[2], NY + 6, 11.4)), (E("sets"), (NX[2], NY + 7, 11.9)),
            (L("whyset") + 2.6, (NX[2], NY + 22, 8.8)), (E("whyset"), (NX[2], NY + 24, 9.2))]
    keys = keys + keys2()
    for (ta, a), (tb, b) in zip(keys, keys[1:]):
        if t <= tb:
            u = sm(t, ta, tb)
            up = uz = u
            if b[2] > a[2] * 1.6:                                    # zooming in: get over the target, then close in
                up, uz = 1 - (1 - u) ** 3.2, u ** 1.7
            elif b[2] < a[2] / 1.6:                                  # zooming out: open up, then travel
                up, uz = u ** 2.4, 1 - (1 - u) ** 2.6
            return (a[0] + (b[0] - a[0]) * up, a[1] + (b[1] - a[1]) * up,
                    math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * uz))
    return keys[-1][1]


# ---------------------------------------------------------------- the screen: notes and captions, not in the world
def wrap(s, n=54):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + [cur]


def screen(c, t, z, cy=0.0):
    a = (1.0 if t < L("scale") - 0.5 else 1.0 - sm(z, 1.15, 1.6)) * (1.0 - sm(cy, 620, 820)) * sm(z, 0.8, 0.98)
    if a > 0:
        c.drawRect(skia.Rect.MakeXYWH(70, 52, 1420, 84), skia.Paint(Color=col(K["bg"], 0.94 * a)))
        text(c, "How They Profit  ·  06", 90, 84, mono(22), K["dim"], a, 0.5)
        text(c, "illustration  ·  one card payment across a border  ·  not a real transaction", 90, 118, mono(27), K["light"], a, 0.5)
    for ln in tl.L:
        k = sm(t, ln["start"] - 0.1, ln["start"] + 0.2) * (1 - sm(t, ln["end"] + 0.1, ln["end"] + 0.35))
        if k <= 0:
            continue
        lines = wrap(ln["text"])
        words = ln["text"].split()
        said = int(len(words) * sm(t, ln["start"], ln["end"]) + 0.999)            # words not yet spoken sit back
        f = sans(34, 500)
        y0 = H - 70 - (len(lines) - 1) * 44
        wmax = max(f.measureText(x) for x in lines)
        plate = skia.Rect.MakeXYWH(W / 2 - wmax / 2 - 34, y0 - 46, wmax + 68, len(lines) * 44 + 30)
        c.drawRect(plate, skia.Paint(Color=col(K["bg"], 0.985 * k)))             # solid: nothing in the drawing shows through the words
        c.drawLine(plate.left(), plate.top(), plate.right(), plate.top(), skia.Paint(Color=col(K["light"], 0.22 * k), AntiAlias=True, StrokeWidth=1))
        n = 0
        for i, s in enumerate(lines):
            x = W / 2 - f.measureText(s) / 2
            for w_ in s.split():
                text(c, w_, x, y0 + i * 44, f, K["light"], k * (1.0 if n < said else 0.42))
                x += f.measureText(w_ + " ")
                n += 1


def frame(surf, t):
    c = surf.getCanvas()
    c.clear(col(K["bg"]))
    cx, cy, z = camera(t)
    c.save()
    c.translate(W / 2, H / 2 - 30)
    c.scale(z, z)
    c.translate(-cx, -cy)
    near = 1.0 - sm(math.hypot(cx - MID[0], cy - MID[1]), 430, 720)  # only the wire has an inside
    ocean(c, t, z, 1.0 - sm(z, 2.0, 3.8) * near, near)
    route(c, t, z)
    later(c, t, z)
    if "close" in tl.IDS:
        last_crossing(c, t)
    c.restore()
    screen(c, t, z, cy)
    return surf.makeImageSnapshot()


def main(a):
    tl.load(HERE, "HOW THEY PROFIT")
    out = tl.EP["build"]
    surf = skia.Surface(W, H)
    if a and a[0] == "still":
        paths = []
        for tt in map(float, a[1:]):
            p = os.path.join(out, f"flow_{tt:06.2f}.png")
            frame(surf, tt).save(p, skia.kPNG)
            paths.append(p)
        cols = 4
        rows = math.ceil(len(paths) / cols)
        sh = skia.Surface(cols * 480, rows * 270)
        cc = sh.getCanvas()
        for i, p in enumerate(paths):
            cc.drawImageRect(skia.Image.open(p), skia.Rect.MakeXYWH((i % cols) * 480, (i // cols) * 270, 480, 270), skia.SamplingOptions(skia.CubicResampler.Mitchell()))
        sp = os.path.join(HERE, "flow_sheet.png")
        sh.makeImageSnapshot().save(sp, skia.kPNG)
        print(sp)
    elif a and a[0] == "clip":
        t0, t1 = float(a[1]), float(a[2])
        p = os.path.join(HERE, f"flow_{int(t0):03d}_{int(t1):03d}.mp4")
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                               "-vf", "scale=1280:720", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", p], stdin=subprocess.PIPE)
        for i in range(int((t1 - t0) * FPS)):
            ff.stdin.write(frame(surf, t0 + i / FPS).toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        ff.stdin.close()
        ff.wait()
        print(p)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
