#!/usr/bin/env python3
"""THE CURVE, one drawing and one camera: a trial of the How They Profit 06 look (ch2/ep06/flow.py) on the Curve's own
material. The Curve's detailed AI pictures stay as characters, but they are now places in one black world that a
single camera glides between and never cuts. The characters live on the screen and the pictures slide beneath them,
so everything shimmers while the camera moves. Ether palette: cyan on black, white type, one red accent.

    ~/youtube/.venv/bin/python curve_flow.py still 3 12 21 ...   # -> build/qc/*.jpg and build/qc/sheet.jpg
    ~/youtube/.venv/bin/python curve_flow.py clip 0 20           # 1280x720 -> build/clip_000_020.mp4
    ~/youtube/.venv/bin/python curve_flow.py master              # 1920x1080 -> build/picture.mp4
"""
import json
import math
import os
import subprocess
import sys

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ch2", "ep06"))
import look_test as LT  # noqa: E402
from look_test import col, font, glow, text  # noqa: E402

W, H, FPS = 1920, 1080, 24
CW, CH = 8, 12
COLS, ROWS = W // CW, H // CH
FW, FH = W // 4, H // 4                       # the grey field the characters are read from
BG, INK, CYAN, RED, DIM = "#040506", "#F2F5F7", "#5FF0E4", "#FF6A4D", "#7B858C"
RAMP, EDGE = " .,:;-=+*o%#@", "-\\|/"
BUILD = os.path.join(HERE, "build")
TL = json.load(open(os.path.join(BUILD, "lines.json")))
LN = {ln["id"]: ln for ln in TL["lines"]}
TOTAL = TL["total"] + 1.5


def sm(x, a, b):
    u = min(1.0, max(0.0, (x - a) / (b - a))) if b != a else float(x >= a)
    return u * u * (3 - 2 * u)


def S(i):
    return LN[i]["start"]


def E(i):
    return LN[i]["end"]


def word(i, w, d=0.0):
    """When a word is spoken in line i (falls back to the line's start)."""
    for x in LN[i]["words"]:
        if x[0].lower().strip(".,:;") == w:
            return x[1] + d
    return S(i) + d


# ------------------------------------------------------------------ the places: (picture, world x, y, world width)
PLACES = dict(
    k01=("k01.mp4", 0, 0, 2500),
    s02=("s02.png", 3300, -760, 2300),
    s20=("s20.png", 5900, 420, 1900),
    s03=("s03.png", 8000, -900, 2700),
    s06=("s06.png", 10150, 500, 1250),
    s23=("s23.png", 12300, -520, 2100),
    s10=("s10.png", 14900, 520, 2700),
    s04=("s04.png", 17300, -380, 1700),
)
ORDER = ["k01", "s02", "s20", "s03", "s06", "s23", "s10", "s04"]
CAM_OFF = dict(s06=0.2)                       # the camera sits this far right of a place (in its widths) to leave room for type
LINE_OF = dict(k01="date", s02="site", s20="thirteen", s03="expert", s06="wanted", s23="person", s10="agents", s04="box")


def grey(im):
    """A picture as a grey field for the character look: levels stretched, mean pulled down, edges lifted, borders feathered."""
    g = im.astype(np.float32) / 255.0
    lo, hi = np.percentile(g, 3), np.percentile(g, 99.6)
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1)
    m = float(g.mean())
    g = g ** float(np.clip(math.log(0.3) / math.log(max(1e-3, m)), 1.0, 2.6))
    g = np.clip(g + 0.7 * (g - cv2.GaussianBlur(g, (0, 0), 3)), 0, 1)
    return np.clip(g - 0.04, 0, 1) / 0.96


def feather(h, w):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum(np.minimum(xx, w - 1 - xx) / (w * 0.26), np.minimum(yy, h - 1 - yy) / (h * 0.3))
    d = np.clip(d, 0, 1)
    return d * d * (3 - 2 * d)


_PIC = {}


def pic(k):
    """The picture's mip levels (a film clip has one set per frame)."""
    if k not in _PIC:
        path = os.path.join(HERE, "src", PLACES[k][0])
        frames = []
        if path.endswith(".mp4"):
            cap = cv2.VideoCapture(path)
            while True:
                ok, f = cap.read()
                if not ok:
                    break
                frames.append(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (960, 540), interpolation=cv2.INTER_AREA))
        else:
            im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            frames.append(cv2.resize(im, (1280, int(1280 * im.shape[0] / im.shape[1])), interpolation=cv2.INTER_AREA))
        fe = feather(*frames[0].shape)
        out = []
        for f in frames:
            g = grey(f) * fe
            lv = [g]
            for _ in range(3):
                lv.append(cv2.pyrDown(lv[-1]))
            out.append(lv)
        _PIC[k] = out
    return _PIC[k]


def lattice():
    """A faint world-anchored field of marks, so the camera's travel is felt in the dark between places."""
    r = np.random.default_rng(7)
    t = np.zeros((512, 512), np.float32)
    for _ in range(420):
        x, y = r.integers(0, 512, 2)
        t[y, x] = r.uniform(0.25, 0.7)
    for _ in range(26):
        x, y = r.integers(8, 500, 2)
        t[y, x - 3:x + 4] = 0.55
        t[y - 3:y + 4, x] = 0.55
    return cv2.GaussianBlur(t, (0, 0), 0.8) * 2.2


LAT = lattice()
LAT_WORLD = 3200.0                            # world width of one tile


def atlas():
    f = font("IBMPlexMono-500", CH * 1.0)
    gl = RAMP + EDGE
    a = np.zeros((len(gl), CH, CW), np.float32)
    for i, g in enumerate(gl):
        s = skia.Surface(CW, CH)
        c = s.getCanvas()
        c.clear(skia.ColorBLACK)
        c.drawString(g, (CW - f.measureText(g)) / 2, CH * 0.8, f, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
        a[i] = s.makeImageSnapshot().toarray()[:, :, 1] / 255.0
    return a


ATLAS = atlas()
_R = np.random.default_rng(3)
PH, SP = _R.uniform(0, 6.28, (ROWS, COLS)).astype(np.float32), _R.uniform(0.6, 2.2, (ROWS, COLS)).astype(np.float32)
LO, MID, HI = np.float32([0.03, 0.2, 0.22]), np.float32([0.37, 0.94, 0.89]), np.float32([0.95, 1.0, 1.0])   # RGB


# ------------------------------------------------------------------ the camera: one move, start to finish
def keys():
    k = []
    for n, p in enumerate(ORDER):
        _, x, y, ww = PLACES[p]
        x += ww * CAM_OFF.get(p, 0.0)
        ln = LINE_OF[p]
        z = W / ww * 0.92
        a, b = S(ln) + (0.0 if n == 0 else 0.4), (S(LINE_OF[ORDER[n + 1]]) - 0.5 if n + 1 < len(ORDER) else TOTAL)
        dx = ww * 0.05 * (1 if n % 2 else -1)
        if n == 0:
            k.append((0.0, (x - 40, y + 20, z * 2.3)))
            k.append((a + 2.6, (x + dx * 0.2, y, z * 1.05)))
        else:
            k.append((a, (x - dx, y + dx * 0.25, z * (0.94 if n % 2 else 1.06)), 0.5))
        k.append((b, (x + dx, y - dx * 0.25, z * (1.1 if n % 2 else 0.95) * 1.0)))
    return k


KEYS = keys()


def camera(t):
    t = min(max(t, KEYS[0][0]), KEYS[-1][0])
    for i in range(len(KEYS) - 1):
        (t0, a), k1 = KEYS[i][0:2], KEYS[i + 1]
        t1, b = k1[0], k1[1]
        if t <= t1:
            u = (t - t0) / max(1e-6, t1 - t0)
            if len(k1) > 2:                                             # a hop: pull out, travel, close in
                up = sm(u, 0.1, 0.9)
                zz = math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * sm(u, 0, 1) - k1[2] * math.sin(math.pi * u) ** 1.3)
                return a[0] + (b[0] - a[0]) * up, a[1] + (b[1] - a[1]) * up, zz
            e = sm(u, 0, 1) * 0.5 + u * 0.5                             # a drift: never quite still
            return a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e, math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * e)
    return KEYS[-1][1]


# ------------------------------------------------------------------ characters
def field(t, cx, cy, z):
    s = z * FW / W
    f = np.zeros((FH, FW), np.float32)
    ls = s * LAT_WORLD / 512
    m = np.float32([[ls, 0, FW / 2 - cx * s], [0, ls, FH / 2 - cy * s]])
    f = cv2.warpAffine(LAT, m, (FW, FH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP) * 0.16
    subj = np.zeros((FH, FW), np.float32)
    for k, (_, x, y, ww) in PLACES.items():
        hh = ww * 9 / 16
        if abs(x - cx) > ww / 2 + W / z / 2 or abs(y - cy) > hh / 2 + H / z / 2:
            continue
        fr = pic(k)
        lv = fr[int(t * FPS) % len(fr)] if len(fr) == 1 else fr[_pingpong(int(t * 12), len(fr))]
        full = s * ww / lv[0].shape[1]
        n = int(min(3, max(0, math.floor(-math.log2(max(full, 1e-6))))))
        g = lv[n]
        sc = s * ww / g.shape[1]
        m = np.float32([[sc, 0, FW / 2 + (x - ww / 2 - cx) * s], [0, sc, FH / 2 + (y - hh / 2 - cy) * s]])
        a = sm(t, S(LINE_OF[k]) - 2.2, S(LINE_OF[k]) - 0.4) if k != "k01" else 1.0
        subj = np.maximum(subj, cv2.warpAffine(g, m, (FW, FH), flags=cv2.INTER_LINEAR, borderValue=0) * a)
    return np.maximum(f * (1 - np.clip(subj * 6, 0, 1)), subj), subj


def _pingpong(i, n):
    i %= 2 * n - 2
    return i if i < n else 2 * n - 2 - i


def chars(t, cx, cy, z):
    f, subj = field(t, cx, cy, z)
    fld = cv2.resize(f, (COLS, ROWS), interpolation=cv2.INTER_AREA)
    fld = fld * (1 + 0.1 * np.sin(t * SP + PH))                              # the characters breathe
    gx, gy = cv2.Sobel(fld, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(fld, cv2.CV_32F, 0, 1, ksize=3) * (CW / CH)
    mag = np.hypot(gx, gy)
    ang = (np.degrees(np.arctan2(gy, gx)) + 90.0) % 180.0                     # the stroke runs across the gradient
    eidx = (((ang + 22.5) // 45).astype(int)) % 4
    idx = np.clip((np.clip(fld, 0, 1) ** 0.85 * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)
    stroke = (mag > 0.42) & (fld > 0.16)
    idx = np.where(stroke, len(RAMP) + eidx, idx)
    lum = np.where(stroke, np.maximum(fld, 0.72), fld)
    cov = ATLAS[idx].transpose(0, 2, 1, 3).reshape(ROWS * CH, COLS * CW)
    k = np.clip(lum * 1.5, 0, 1)[..., None]
    c = np.where(k < 0.7, LO + (MID - LO) * (k / 0.7), MID + (HI - MID) * ((k - 0.7) / 0.3))
    c = cv2.resize(c.astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST)
    img = c * cov[..., None]
    back = cv2.resize(cv2.GaussianBlur(cv2.resize(subj, (FW // 2, FH // 2)), (0, 0), 9), (W, H), interpolation=cv2.INTER_LINEAR)
    out = np.float32([4, 5, 6]) / 255.0 + back[..., None] ** 1.4 * MID * 0.17 + img
    h = cv2.GaussianBlur(cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA), (0, 0), 2.2)
    out += 0.5 * cv2.resize(h, (W, H), interpolation=cv2.INTER_LINEAR)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    out *= (1 - 0.5 * np.clip((np.hypot(xx - W / 2, yy - H / 2) / 1100.0 - 0.55) / 0.45, 0, 1))[..., None]
    return np.clip(out, 0, 1)


# ------------------------------------------------------------------ type and lines, drawn crisp on top
def sans(sz):
    return font("InterTight-600", sz)


def mono(sz):
    return font("IBMPlexMono-500", sz)


def plate(c, x, y, w, h, a):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Color=col(BG, 0.9 * a)))


def typed(s, t, t0, cps=30.0):
    n = int(max(0.0, t - t0) * cps)
    return s[:n] + ("█" if 0 < n < len(s) else "")


def thread(c, t, z):
    """The attacker's path: one hairline through every place, lit as far as the story has gone, a pulse at its head."""
    pts = [(PLACES[p][1] + PLACES[p][3] * 0.36, PLACES[p][2] - PLACES[p][3] * 0.2) for p in ORDER]   # the top right of each place, clear of its subject and its type
    p = skia.Path()
    p.moveTo(*pts[0])
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        p.cubicTo(x0 + (x1 - x0) * 0.5, y0, x0 + (x1 - x0) * 0.5, y1, x1, y1)
    meas = skia.PathMeasure(p, False)
    total = meas.getLength()
    prog = 0.0
    for i in range(1, len(ORDER)):
        a = S(LINE_OF[ORDER[i]])
        prog = max(prog, (i - 1 + sm(t, a - 1.6, a + 0.5)) / (len(ORDER) - 1)) if t > a - 1.6 else prog
    c.drawPath(p, skia.Paint(Color=col(INK, 0.1), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5 / z))
    if prog > 0:
        lit = skia.Path()
        meas.getSegment(0, total * prog, lit, True)
        g = glow(CYAN, 0.55, 10 / z)
        g.setStyle(skia.Paint.kStroke_Style)
        g.setStrokeWidth(7 / z)
        c.drawPath(lit, g)
        c.drawPath(lit, skia.Paint(Color=col(CYAN), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6 / z))
        pos, _ = meas.getPosTan(total * prog)
        c.drawCircle(pos.x(), pos.y(), 16 / z, glow(INK, 0.9, 14 / z))
        c.drawCircle(pos.x(), pos.y(), 6 / z, skia.Paint(Color=col(INK), AntiAlias=True))
    for i, (x, y) in enumerate(pts):
        f = mono(15 / z)
        c.drawString(f"{i + 1:02d}", x + 12 / z, y - 12 / z, f, skia.Paint(Color=col(DIM, 0.8), AntiAlias=True))


def label(c, k, t, big, note, dx, dy, size, t0=None, colr=INK, align="left", t1=None):
    """Big type and a typed note anchored to a place, on a plate so the characters never run under the words."""
    _, x, y, ww = PLACES[k]
    ln = LINE_OF[k]
    t0 = S(ln) + 0.5 if t0 is None else t0
    t0 = max(t0, S(ln) + 0.45)                                        # never before the camera has arrived
    a = sm(t, t0, t0 + 0.35) * (1 - sm(t, (t1 or E(ln)) - 0.4, (t1 or E(ln)) - 0.08))   # and gone before it leaves
    if a <= 0:
        return
    s = ww / 2300.0
    X, Y = x + dx * s, y + dy * s
    f, fm = sans(size * s), mono(30 * s)
    wb = max([f.measureText(b) for b in big.split("\n")] + [fm.measureText(note)])
    nb = len(big.split("\n"))
    x0 = X - (wb if align == "right" else 0)
    plate(c, x0 - 36 * s, Y - size * s * 0.98, wb + 72 * s, size * s * (nb * 1.02) + 86 * s, a)
    for i, b in enumerate(big.split("\n")):
        text(c, b, x0, Y + i * size * s * 1.02, f, colr, a, halo=(14 * s if colr != INK else 0))
    text(c, typed(note, t, t0 + 0.25), x0 + 4 * s, Y + (nb - 1) * size * s * 1.02 + 52 * s, fm, CYAN if colr == INK else INK, a, 0.5 * s)


def world_type(c, t):
    # every block ends above the caption band (the bottom fifth of the screen) at every point of the camera's drift
    label(c, "k01", t, "11 JULY 2026", "HUGGING FACE  ·  BREACH DETECTED", -1060, 270, 150, t0=S("date") + 0.4)
    label(c, "s02", t, "1,000,000+", "MODELS SHARED  ·  AND THE DATA THEY LEARN FROM", -1040, 270, 170, t0=word("site", "over", -0.1))
    label(c, "s20", t, "< 13 HOURS", "ONE DATASET MACHINE  →  ADMIN OF SEVERAL CLUSTERS", -1060, 280, 190, t0=word("thirteen", "under", -0.1))
    label(c, "s03", t, "LIKE NO ATTACKER\nTHEY HAD SEEN", "EXPERT MOVES  ·  STRANGE GOALS", -1040, 150, 120, t0=word("expert", "but", -0.1))
    _, x, y, ww = PLACES["s06"]
    u = ww / 2300.0
    for i, (s_, w_) in enumerate((("NO CUSTOMER DATA TAKEN", "take"), ("NO RANSOM NOTE", "ask"), ("IT WANTED TEST DATA", "looking"))):
        t0 = word("wanted", w_, -0.15)
        a = sm(t, t0, t0 + 0.3) * (1 - sm(t, E("wanted") - 0.4, E("wanted") - 0.08))
        if a > 0:
            f = sans(76 * u)
            X, Y = x + 450 * u, y + (-250 + i * 170) * u
            plate(c, X - 60 * u, Y - 84 * u, f.measureText(s_) + 90 * u, 118 * u, a)
            text(c, s_, X, Y, f, RED if i == 2 else INK, a, halo=(12 * u if i == 2 else 0))
            c.drawRect(skia.Rect.MakeXYWH(X - 44 * u, Y - 62 * u, 10 * u, 64 * u), skia.Paint(Color=col(RED if i == 2 else CYAN, a)))
    label(c, "s23", t, "IT WASN'T\nA PERSON.", "IDENTIFIED ONE WEEK LATER", -930, 20, 185, t0=word("person", "it", -0.05), colr=RED)
    label(c, "s10", t, "1,200", "AI AGENTS  ·  ONE TEST  ·  STILL RUNNING", -1120, 280, 300, t0=word("agents", "twelve", -0.1))
    label(c, "s04", t, "CAN THEY KEEP\nTHEM IN THE BOX?", "THE CURVE  ·  THE AI THAT ESCAPED", -1060, 130, 84, t0=word("box", "whether", -0.1), t1=TOTAL + 9)


def wrap(s, f, maxw):
    out, cur = [], ""
    for w_ in s.split():
        if cur and f.measureText(cur + " " + w_) > maxw:
            out.append(cur)
            cur = w_
        else:
            cur = (cur + " " + w_).strip()
    return out + [cur]


def screen(c, t, cx, cy, z):
    c.drawRect(skia.Rect.MakeXYWH(52, 48, 560, 46), skia.Paint(Color=col(BG, 0.85)))
    c.drawRect(skia.Rect.MakeXYWH(W - 470, 48, 420, 46), skia.Paint(Color=col(BG, 0.85)))
    text(c, "THE CURVE  ·  THE AI THAT ESCAPED", 70, 78, mono(22), DIM, 1.0, 0.5)
    text(c, f"CAM {cx:+07.0f} {cy:+06.0f}  x{z:4.2f}", W - 70, 78, mono(22), DIM, 1.0, 0.5, align="right")
    for ln in TL["lines"]:
        k = sm(t, ln["start"], ln["start"] + 0.15) * (1 - sm(t, ln["end"] + 0.02, ln["end"] + 0.14))   # two lines are never up together
        if k <= 0:
            continue
        f = sans(34)
        lines = wrap(ln["text"], f, 1180)
        ws = ln.get("words") or []
        said = sum(1 for w_ in ws if w_[1] <= t) if ws else 999
        y0 = H - 66 - (len(lines) - 1) * 44
        wmax = max(f.measureText(x) for x in lines)
        pl = skia.Rect.MakeXYWH(W / 2 - wmax / 2 - 34, y0 - 46, wmax + 68, len(lines) * 44 + 28)
        c.drawRect(pl, skia.Paint(Color=col(BG, 0.985 * k)))
        c.drawLine(pl.left(), pl.top(), pl.right(), pl.top(), skia.Paint(Color=col(INK, 0.22 * k), AntiAlias=True, StrokeWidth=1))
        n = 0
        for i, s in enumerate(lines):
            x = W / 2 - f.measureText(s) / 2
            for w_ in s.split():
                text(c, w_, x, y0 + i * 44, f, INK, k * (1.0 if n < said else 0.42))
                x += f.measureText(w_ + " ")
                n += 1


def frame(t):
    cx, cy, z = camera(t)
    px = (chars(t, cx, cy, z) * 255).astype(np.uint8)
    rgba = np.dstack([px, np.full((H, W), 255, np.uint8)])
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    c.drawImage(skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType), 0, 0)
    c.save()
    c.translate(W / 2, H / 2)
    c.scale(z, z)
    c.translate(-cx, -cy)
    thread(c, t, z)
    world_type(c, t)
    c.restore()
    screen(c, t, cx, cy, z)
    a = sm(t, 0, 0.8) * (1 - sm(t, TL['total'] - 1.3, TL['total'] - 0.1))
    if a < 1:
        c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=col(BG, 1 - a)))
    return surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)


def encode(a, b, out, size):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", f"scale={size}:flags=lanczos", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out],
                         stdin=subprocess.PIPE)
    for i in range(int(a * FPS), int(b * FPS)):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    p.wait()
    print(out)


def main():
    cmd = sys.argv[1]
    if cmd == "still":
        os.makedirs(os.path.join(BUILD, "qc"), exist_ok=True)
        ts = [float(x) for x in sys.argv[2:]]
        ims = []
        for t in ts:
            im = cv2.cvtColor(frame(t), cv2.COLOR_RGBA2BGR)
            cv2.imwrite(os.path.join(BUILD, "qc", f"f_{t:06.2f}.jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
            sm_ = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
            cv2.putText(sm_, f"{t:.1f}s", (16, 524), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            ims.append(sm_)
        while len(ims) % 2:
            ims.append(np.zeros_like(ims[0]))
        rows = [np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)]
        cv2.imwrite(os.path.join(BUILD, "qc", "sheet.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(os.path.join(BUILD, "qc", "sheet.jpg"))
    elif cmd == "clip":
        a, b = float(sys.argv[2]), float(sys.argv[3])
        encode(a, b, os.path.join(BUILD, f"clip_{int(a):03d}_{int(b):03d}.mp4"), "1280:720")
    elif cmd == "seg":
        a, b = float(sys.argv[2]), float(sys.argv[3])
        encode(a, min(b, TOTAL), os.path.join(BUILD, f"seg_{int(a):03d}.mp4"), "1920:1080")
    elif cmd == "master":
        encode(0, TOTAL, os.path.join(BUILD, "picture.mp4"), "1920:1080")


if __name__ == "__main__":
    main()
