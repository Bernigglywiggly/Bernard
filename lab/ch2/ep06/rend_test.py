#!/usr/bin/env python3
"""Two renditions of the Visa opening in the new look (look_test.py, "ether"), so the user can choose how the films
move: CUTS (three separate shots, hard cuts, a slow push in each) against FLOW (one drawing, one continuous camera:
close on Lisbon, ride the message to Ohio, pull back to the whole ocean, drop to the figure, push into the one lit
cell). Same content, same timings where possible, no sound. A study, not wired into the film engine.

    ~/youtube/.venv/bin/python lab/ch2/ep06/rend_test.py      # -> build_est/rend_cuts.mp4, rend_flow.mp4, rend_both.mp4
"""
import math
import os
import subprocess

import skia

import look_test as LT
from look_test import W, H, col, font, glow, text

K = LT.LOOKS["ether"]
FPS, DUR = 30, 15.0
MX, MY, MW, MH = 90, 150, 1740, 680
COLS, ROWS = 150, 44
CELL, GAP = 34, 10
GX, GY = 1082, 1010                                  # the dot matrix, lower right of the world
FIG = (90, 1330)                                     # the figure, lower left of the world
LIT = (GX + 16 * (CELL + GAP), GY + 9 * (CELL + GAP))
CAPS = [(0.2, 3.2, "A card touches a reader in a café in Lisbon,"), (3.2, 6.6, "and a message crosses the ocean to a bank in Ohio and back."),
        (6.9, 10.6, "Last year $17 trillion moved across the network like this."),
        (10.9, 14.8, "The company in the middle kept about 24 cents of every $100.")]


def sm(t, a, b):
    x = max(0.0, min(1.0, (t - a) / (b - a)))
    return x * x * (3 - 2 * x)


def xy(lon, lat):
    return MX + (lon - LT.LON0) / (LT.LON1 - LT.LON0) * MW, MY + (LT.LAT1 - lat) / (LT.LAT1 - LT.LAT0) * MH


P0, P1 = xy(*LT.LISBON), xy(*LT.OHIO)


def arc(u):
    return P0[0] + (P1[0] - P0[0]) * u, P0[1] + (P1[1] - P0[1]) * u - 200 * math.sin(math.pi * u)


def map_picture():
    rec = skia.PictureRecorder()
    c = rec.beginRecording(skia.Rect.MakeWH(W, 1600))
    land = LT.land_path()
    cw, ch = MW / COLS, MH / ROWS
    g = [[land.contains(LT.LON0 + (i + 0.5) / COLS * (LT.LON1 - LT.LON0), LT.LAT1 - (j + 0.5) / ROWS * (LT.LAT1 - LT.LAT0))
          for i in range(COLS)] for j in range(ROWS)]
    f = font("IBMPlexMono-500", ch * 0.95)
    for j in range(ROWS):
        for i in range(COLS):
            if not g[j][i]:
                continue
            edge = any(0 <= j + dj < ROWS and 0 <= i + di < COLS and not g[j + dj][i + di] for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            x, y = MX + i * cw, MY + (j + 0.8) * ch
            if edge:
                c.drawString("#+%*"[(i * 7 + j * 3) % 4], x, y, f, skia.Paint(Color=col(K["coast"], 0.9), AntiAlias=True))
            else:
                c.drawString(".:·"[(i + j * 2) % 3], x, y, f, skia.Paint(Color=col(K["land"]), AntiAlias=True))
    m = font("IBMPlexMono-400", 19)
    ink = skia.Paint(Color=col(K["light"], 0.85), AntiAlias=True, StrokeWidth=1.2)
    for lon in range(-100, 20, 20):
        x, _ = xy(lon, 0)
        c.drawLine(x, MY + MH + 8, x, MY + MH + 20, ink)
        text(c, f"{abs(lon):03d}{'W' if lon < 0 else 'E'}", x, MY + MH + 44, m, K["dim"], 1.0, 0.5, "center")
    c.drawLine(MX, MY + MH + 8, MX + MW, MY + MH + 8, skia.Paint(Color=col(K["light"], 0.35), AntiAlias=True, StrokeWidth=1))
    return rec.finishRecordingAsPicture()


MAP = None


def place(c, pt, a, note, sd, k):
    if k <= 0:
        return
    x, y = pt
    m, sans = font("IBMPlexMono-400", 19), font("InterTight-600", 30)
    c.drawCircle(x, y, 5, skia.Paint(Color=col(K["light"], k), AntiAlias=True))
    c.drawCircle(x, y, 13, skia.Paint(Color=col(K["light"], 0.6 * k), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2))
    c.drawLine(x, y + 13, x, y + 13 + 87 * k, skia.Paint(Color=col(K["light"], 0.85), AntiAlias=True, StrokeWidth=1.2))
    bw = max(sans.measureText(a), sum(m.measureText(ch) + 0.5 for ch in note)) + 28
    c.drawRect(skia.Rect.MakeXYWH(x + 1 if sd > 0 else x - bw - 1, y + 36, bw, 66), skia.Paint(Color=col(K["bg"], 0.92 * k)))
    al = "left" if sd > 0 else "right"
    text(c, a, x + 14 * sd, y + 66, sans, K["light"], k, align=al)
    n = int(len(note) * min(1.0, k * 1.6))                           # the note types on
    text(c, note[:n] + " " * (len(note) - n), x + 14 * sd, y + 94, m, K["dim"], 1.0, 0.5, al)


def tag(c, x, y, s, k, sd=1):
    if k <= 0:
        return
    m = font("IBMPlexMono-400", 19)
    s = s[:max(1, int(len(s) * min(1.0, k * 2)))]
    lw = sum(m.measureText(ch) + 0.5 for ch in s)
    x0 = x + 22 if sd > 0 else x - 22 - lw - 16
    c.drawRect(skia.Rect.MakeXYWH(x0, y - 30, lw + 16, 28), skia.Paint(Color=col(K["acc"]), AntiAlias=True))
    text(c, s, x0 + 8, y - 10, m, K["bg"], 1.0, 0.5)


def world(c, t, ev):
    """Everything that lives in the drawing, at time t. ev = the variant's event times."""
    c.drawPicture(MAP)
    out, back = sm(t, *ev["out"]), sm(t, *ev["back"])
    place(c, P0, "A café, Lisbon", "38.72N  009.14W  ·  card tapped", -1, sm(t, 0.1, 0.9))
    place(c, P1, "A bank, Ohio", "39.96N  083.00W  ·  issued the card", 1, sm(t, ev["out"][1] - 0.3, ev["out"][1] + 0.5))
    pulse = (t % 1.6) / 1.6                                            # the reader, never quite still
    c.drawCircle(P0[0], P0[1], 13 + 40 * pulse, skia.Paint(Color=col(K["acc"], 0.5 * (1 - pulse)), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4))
    if out > 0:
        p = skia.Path()
        n = max(1, int(80 * out))
        for i in range(n + 1):
            (p.moveTo if i == 0 else p.lineTo)(*arc(i / 80))
        g = glow(K["acc"], 0.45, 14)
        g.setStyle(skia.Paint.kStroke_Style)
        g.setStrokeWidth(6)
        c.drawPath(p, g)
        c.drawPath(p, skia.Paint(Color=col(K["acc"]), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8))
        u = out if back <= 0 else 1 - back
        px, py = arc(u)
        if back < 1:
            c.drawCircle(px, py, 20, glow(K["acc"], 0.5, 14))
            c.drawRect(skia.Rect.MakeXYWH(px - 9, py - 9, 18, 18), skia.Paint(Color=col(K["acc"]), AntiAlias=True))
            if 0.05 < out < 1:
                tag(c, px, py, f"message out  ·  {0.5 * out:0.2f} s", 1.0)
            elif 0 < back < 1:
                tag(c, px, py, f"answer back  ·  {0.5 + 0.5 * back:0.2f} s", 1.0, -1)
        else:
            tag(c, P0[0], P0[1] - 30, "approved  ·  about 1 s", sm(t, ev["back"][1], ev["back"][1] + 0.5), -1)
    # the figure and its matrix, below the ocean
    kf = sm(t, ev["fig"], ev["fig"] + 0.6)
    if kf > 0:
        text(c, "$17 trillion", FIG[0], FIG[1] + 14 * (1 - kf), font("InterTight-600", 150), K["light"], kf)
        text(c, "payments and cash volume on the network  ·  fiscal 2025  ·  Visa Form 10-K", FIG[0] + 6, FIG[1] + 58, font("IBMPlexMono-400", 22), K["dim"], kf, 0.5)
        fill = sm(t, ev["fig"] + 0.3, ev["fig"] + 2.4) * 170
        for j in range(10):
            for i in range(17):
                if i * 10 + j < fill:
                    c.drawRect(skia.Rect.MakeXYWH(GX + i * (CELL + GAP), GY + j * (CELL + GAP), CELL, CELL), skia.Paint(Color=col(K["light"], 0.42), AntiAlias=True))
        text(c, "each cell $100 billion moved", GX, GY + 10 * (CELL + GAP) + 22, font("IBMPlexMono-400", 19), K["dim"], kf, 0.5)
    kl = sm(t, ev["lit"], ev["lit"] + 0.6)
    if kl > 0:
        lx, ly = LIT
        c.drawRect(skia.Rect.MakeXYWH(lx, ly, CELL, CELL), skia.Paint(Color=col(K["bg"])))
        c.drawRect(skia.Rect.MakeXYWH(lx, ly, CELL, CELL), skia.Paint(Color=col(K["light"], 0.5), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.6))
        c.drawCircle(lx + CELL / 2, ly + CELL * 0.8, 16 * kl, glow(K["acc"], 0.5, 9))
        c.drawRect(skia.Rect.MakeXYWH(lx, ly + CELL * (1 - 0.4 * kl), CELL, CELL * 0.4 * kl), skia.Paint(Color=col(K["acc"]), AntiAlias=True))
        m6 = font("IBMPlexMono-400", 5.2)
        text(c, "$40.0 billion", lx + CELL + 6, ly + CELL * 0.82, m6, K["acc"], kl, 0.2)
        text(c, "what Visa kept", lx + CELL + 6, ly + CELL * 0.82 + 7, m6, K["dim"], kl, 0.2)


def screen(c, t, z=1.0):
    m = font("IBMPlexMono-400", 19)
    a = 1.0 - sm(z, 1.15, 1.6)                                       # the page notes give way when the camera is close
    c.drawRect(skia.Rect.MakeXYWH(70, 56, 1010, 70), skia.Paint(Color=col(K["bg"], 0.85 * a)))
    text(c, "How They Profit  ·  06", 90, 86, m, K["dim"], a, 0.5)
    text(c, "illustration  ·  one card payment across a border  ·  not a real transaction", 90, 112, m, K["dim"], a, 0.5)
    for a, b, s in CAPS:
        k = sm(t, a, a + 0.25) * (1 - sm(t, b - 0.25, b))
        if k > 0:
            f = font("InterTight-500", 34)
            w = f.measureText(s)
            c.drawRect(skia.Rect.MakeXYWH(W / 2 - w / 2 - 18, H - 104, w + 36, 54), skia.Paint(Color=col(K["bg"], 0.8 * k)))
            text(c, s, W / 2, H - 66, f, K["light"], k, align="center")


EV_CUTS = dict(out=(1.2, 3.4), back=(3.9, 6.0), fig=6.9, lit=11.2)
EV_FLOW = dict(out=(1.4, 4.6), back=(5.0, 7.6), fig=8.4, lit=11.4)
LITC = (LIT[0] + CELL / 2 + 6, LIT[1] + CELL / 2)


def cam_cuts(t):
    if t < 6.7:
        return 960, 520, 1.0 + 0.04 * t / 6.7
    if t < 10.8:
        return 960, 1300, 1.0 + 0.04 * (t - 6.7) / 4.1
    return LITC[0], LITC[1], 7.0 + 0.6 * (t - 10.8) / 4.2


def cam_flow(t):
    """One move. Keys: close on Lisbon; ride the message; hold on Ohio; pull back; drop to the figure; into the cell."""
    out = sm(t, *EV_FLOW["out"])
    px, py = arc(out)
    ride = (px + 120, py + 30, 2.3)
    keys = [(0.0, (P0[0] - 150, P0[1] + 30, 2.7)), (1.4, (P0[0] - 150, P0[1] + 30, 2.5)), (2.2, ride), (4.6, ride),
            (7.6, (960, 520, 1.0)), (8.2, (960, 540, 1.0)), (10.0, (960, 1300, 1.02)), (11.2, (960, 1305, 1.05)),
            (13.6, (LITC[0], LITC[1], 7.4)), (15.0, (LITC[0], LITC[1], 7.8))]
    for (ta, a), (tb, b) in zip(keys, keys[1:]):
        if t <= tb:
            u = sm(t, ta, tb)
            z = math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * u)     # zoom eases in log space
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, z
    return keys[-1][1]


def render(name, cam, ev, out_dir):
    global MAP
    MAP = MAP or map_picture()
    path = os.path.join(out_dir, f"rend_{name}.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", path], stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    for i in range(int(DUR * FPS)):
        t = i / FPS
        c = surf.getCanvas()
        c.clear(col(K["bg"]))
        cx, cy, z = cam(t)
        c.save()
        c.translate(W / 2, H / 2 - 20)
        c.scale(z, z)
        c.translate(-cx, -cy)
        world(c, t, ev)
        c.restore()
        screen(c, t, z)
        ff.stdin.write(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    ff.stdin.close()
    ff.wait()
    return path


def main():
    out = os.path.join(LT.HERE, "build_est")
    os.makedirs(out, exist_ok=True)
    a = render("cuts", cam_cuts, EV_CUTS, out)
    b = render("flow", cam_flow, EV_FLOW, out)
    both = os.path.join(LT.HERE, "rend_both.mp4")
    lab = "drawtext=text='%s':fontcolor=white:fontsize=30:x=30:y=h-50"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-i", b, "-filter_complex",
                    f"[0:v]scale=1280:720,{lab % 'A  CUTS'}[l];[1:v]scale=1280:720,{lab % 'B  ONE CAMERA'}[r];[l][r]vstack", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "20", both], check=False)
    print(a, b, both)


if __name__ == "__main__":
    main()
