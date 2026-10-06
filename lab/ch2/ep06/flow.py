#!/usr/bin/env python3
"""HOW THEY PROFIT · EP06 (Visa) as ONE DRAWING AND ONE CAMERA: the look the user chose on 6 Oct (rend_test.py "B",
after the pollar.news references). No cuts and no fades between scenes: everything lives on one page at three
scales, and the camera travels between them on the narration's timings (script.py line ids, build*/lines.json).

  scale 1    the North Atlantic set in type, the crossing, and under it $17 trillion as a matrix of cells
  scale 12   inside the crossing: the four parties on the wire, interchange passing under the network
  (to come)  the three meters, the money handed back, the one lit cell, half of it profit, the weak point, the close

Stage 1 (this file, 6 Oct): chapters 0-2, to the end of "whyset". Later chapters are not drawn yet.

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
def ocean(c, t):
    ev = dict(out=(L("ocean") + 0.6, L("ocean") + 4.8), back=(L("ocean") + 5.4, E("ocean") - 0.4),
              fig=L("scale") - 0.2, lit=L("never") + 3.0)
    R.MAP = R.MAP or R.map_picture()
    R.world(c, t, ev)
    return ev


# ---------------------------------------------------------------- scale 12: the four parties on the wire
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
    k = lod(z, 3.5, 7.0)
    if k <= 0:
        return
    c.drawLine(NX[0] - 60, NY, NX[3] + 60, NY, skia.Paint(Color=col(K["acc"], 0.9 * k), AntiAlias=True, StrokeWidth=0.18))
    text(c, "one card payment  ·  four parties", NX[0] - NODE_W / 2, NY - 17, mono(1.7), K["dim"], k * sm(t, L("four"), L("four") + 0.8), 0.05)
    c.drawLine(NX[0] - NODE_W / 2, NY - 15, NX[3] + NODE_W / 2, NY - 15, hair(0.35 * k, 0.1))
    party(c, 0, k * sm(t, L("four") + 1.2, L("four") + 1.9), t)
    party(c, 1, k * sm(t, L("shopbank") + 0.2, L("shopbank") + 0.9), t)
    party(c, 3, k * sm(t, L("yourbank") + 0.2, L("yourbank") + 0.9), t)
    party(c, 2, k * sm(t, L("quote") + 0.2, L("quote") + 0.9), t, hot=True)
    wire_packets(c, t, k * sm(t, L("quote") + 1.0, L("quote") + 1.6))
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
    box_label(c, "interchange", (NX[1] + NX[3]) / 2, NY + NODE_H / 2 + 19.5, sm(t, L("interchange") + 0.3, L("interchange") + 0.9), 2.0, "center")
    text(c, "paid by the shop's bank to the cardholder's bank", (NX[1] + NX[3]) / 2, NY + NODE_H / 2 + 22.6, mono(1.35), K["dim"],
         sm(t, L("interchange") + 1.2, L("interchange") + 1.9), 0.05, "center")
    ks = sm(t, tl.word("sets", "writes") - 0.2, tl.word("sets", "writes") + 0.5)
    c.drawRect(skia.Rect.MakeXYWH(NX[2] - 13, NY + NODE_H / 2 + 1.2, 26, 5.2), skia.Paint(Color=col(K["bg"], 0.92 * ks)))
    text(c, "sets the default rates", NX[2], NY + NODE_H / 2 + 3.0, mono(1.45), K["acc"], ks * (1 - sm(t, L("fee") - 9, L("fee") - 8)), 0.05, "center")
    text(c, "collects none of it", NX[2], NY + NODE_H / 2 + 5.4, mono(1.45), K["light"], sm(t, tl.word("sets", "without") - 0.2, tl.word("sets", "without") + 0.5), 0.05, "center")
    kw = sm(t, L("whyset") + 1.0, L("whyset") + 1.8)
    text(c, "The fee pays banks to issue the cards.", NX[2], NY + 38, sans(3.0), K["light"], kw, align="center")
    text(c, "Every card sends more messages down the wire.", NX[2], NY + 42.4, sans(3.0), K["acc"],
         sm(t, tl.word("whyset", "every") - 0.2, tl.word("whyset", "every") + 0.6), align="center")


# ---------------------------------------------------------------- the camera: one move, keyed to the narration
def camera(t):
    o0, o1 = L("ocean") + 0.6, L("ocean") + 4.8
    px, py = arc(sm(t, o0, o1))
    ride = (px + 110, py + 30, 2.3)
    lis = (P0[0] - 150, P0[1] + 30)
    rc = ((NX[1] + NX[2]) / 2, NY + 2)                               # the route, all four parties in frame
    keys = [(0.0, (lis[0], lis[1], 2.75)), (L("ocean") + 0.4, (lis[0], lis[1], 2.45)), (o0 + 1.0, ride), (o1, ride),
            (E("ocean"), (960, 520, 1.0)), (L("scale") - 0.3, (960, 560, 1.0)), (L("scale") + 1.6, (960, 1300, 1.02)),
            (L("never") - 0.5, (960, 1305, 1.06)), (L("never") + 5.5, (R.LITC[0] - 60, R.LITC[1] - 20, 4.6)),
            (E("never") - 0.2, (R.LITC[0] - 30, R.LITC[1] - 10, 5.2)),
            (L("four") + 1.6, (960, 620, 1.0)),                      # back out over the ocean on the way to the wire
            (L("four") + 4.4, (NX[0] + 12, NY + 2, 11.0)), (L("shopbank") + 1.0, (NX[0] + 22, NY + 2, 11.5)),
            (L("yourbank") + 1.5, (rc[0] + 10, rc[1], 9.6)), (L("quote") - 0.3, (rc[0], rc[1], 9.4)),
            (L("quote") + 2.2, (NX[2], NY - 12, 11.5)), (E("quote"), (NX[2], NY - 13, 12.2)),
            (L("risk") + 2.2, (NX[3] - 4, NY + 3, 15.0)), (E("risk"), (NX[3] - 5, NY + 4, 15.8)),
            (L("fee") + 2.4, ((NX[1] + NX[3]) / 2, NY + 11, 10.6)), (E("interchange"), ((NX[1] + NX[3]) / 2, NY + 13, 11.4)),
            (L("sets") + 2.0, (NX[2], NY + 9, 14.5)), (E("sets"), (NX[2], NY + 10, 15.2)),
            (L("whyset") + 2.6, (NX[2], NY + 30, 9.4)), (E("whyset"), (NX[2], NY + 32, 10.0))]
    for (ta, a), (tb, b) in zip(keys, keys[1:]):
        if t <= tb:
            u = sm(t, ta, tb)
            return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u,
                    math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * u))
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


def screen(c, t, z):
    a = 1.0 - sm(z, 1.15, 1.6)
    text(c, "How They Profit  ·  06", 90, 86, mono(19), K["dim"], a, 0.5)
    text(c, "illustration  ·  one card payment across a border  ·  not a real transaction", 90, 112, mono(19), K["dim"], a, 0.5)
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
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - wmax / 2 - 22, y0 - 40, wmax + 44, len(lines) * 44 + 16), skia.Paint(Color=col(K["bg"], 0.82 * k)))
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
    far = 1.0 - sm(z, 3.0, 6.5)                                      # the ocean gives way as the camera enters the wire
    if far > 0.999:
        ocean(c, t)
    elif far > 0.004:
        c.saveLayerAlpha(None, int(255 * far))
        ocean(c, t)
        c.restore()
    route(c, t, z)
    c.restore()
    screen(c, t, z)
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
