#!/usr/bin/env python3
"""THE CURVE · LONG-FORM in one drawing with one camera (7 Oct 2026; the user, after the trial in flow_trial/: "go").
A film is the same folder kit.py uses (script.py with CHAPTERS of beats, src/ai/ pictures from assets_ai.json). Every
beat becomes a place in one black world, laid along a wandering line; one camera glides from place to place and never
cuts. Pictures and big numbers are characters (they live on the screen; the world slides beneath, so they shimmer as
the camera moves); quotes, lists and notes are crisp type on plates; a lit thread runs through every place.
Ether palette: cyan on black, white type, one red accent.

    P=~/youtube/.venv/bin/python
    $P flow.py <film> est                    # estimated timings -> <film>/flow/lines.json (until the voice exists)
    $P flow.py <film> lay                    # George's takes in <film>/flow/takes/NNN_<id>/*.mp3 -> lines.json, voice_dry.wav
    $P flow.py <film> still 3 41.5 ...       # -> <film>/flow/qc/sheet.jpg
    $P flow.py <film> seg 0 60               # 1080p part -> <film>/flow/seg_0000.mp4
    $P flow.py <film> lines                  # id, characters and text of every line (for voicing)
"""
import glob
import importlib.util
import json
import math
import os
import re
import subprocess
import sys

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ch2", "ep06"))
from look_test import col, font, glow, text  # noqa: E402

VERT = os.environ.get("FLOW_VERT") == "1"            # a Short: the same world, framed 9:16
W, H, FPS = (1080, 1920, 30) if VERT else (1920, 1080, 24)
CW, CH = 8, 12
COLS, ROWS = W // CW, H // CH
FW, FH = W // 4, H // 4
BG, INK, CYAN, RED, DIM = "#040506", "#F2F5F7", "#5FF0E4", "#FF6A4D", "#7B858C"
RAMP, EDGE = " .,:;-=+*o%#@", "-\\|/"
BEAT_GAP, CHAPTER_GAP, LEAD = 0.3, 3.0, 1.2
LONG_WORDS = 20
THREAD = False                                # the wandering line through every place (7 Oct, the user: not as the guide; a rail of numbered boxes instead, as in How They Profit 06)
LONG_NUM = 9
LONG_SPLIT = 6                                # a split's big words longer than this are set crisp
CAP_TOP = (H - 600) if VERT else (H - 165)   # where the caption band begins
RAISE = 40 if VERT else 20
SHIFT = 56 if VERT else 0                     # a Short sits left of centre: the app's buttons run down the right edge    #                                # screen pixels the world is lifted, so pictures clear the caption plate
WIDTH = dict(photo=2300, img=2300, clip=2500, num=2100, words=2300, quote=2300, list=2100, split=2500, tl=2700)

FILM = os.path.join(HERE, sys.argv[1]) if len(sys.argv) > 1 else None
BUILD = os.path.join(FILM, "flow") if FILM else None


def sm(x, a, b):
    u = min(1.0, max(0.0, (x - a) / (b - a))) if b != a else float(x >= a)
    return u * u * (3 - 2 * u)


def script():
    s = importlib.util.spec_from_file_location("film_script", os.path.join(FILM, "script.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


SC = script()


def beats():
    """Every beat as a line: id, chapter index, the text shown in captions, the text said, and its visual."""
    out = []
    for ci, ch in enumerate(SC.CHAPTERS):
        for bi, b in enumerate(ch["beats"]):
            shown, said = b[0] if isinstance(b[0], tuple) else (b[0], b[0])
            out.append(dict(id=f"{ch['id']}_{bi:02d}", floor=ci, text=shown, said=said, vis=b[1], first=(bi == 0), title=ch["title"]))
    return out


B = beats()
CHANNEL = SC.TAG.split("·")[0].strip()        # the channel's name, from the film's tag


def est():
    t, lines = LEAD, []
    for i, b in enumerate(B):
        if i:
            t += CHAPTER_GAP if b["first"] else BEAT_GAP
        d = len(b["said"]) / 15.2
        lines.append(dict(i=i, id=b["id"], floor=b["floor"], text=b["text"], start=round(t, 3), end=round(t + d, 3), words=[]))
        t += d
    os.makedirs(BUILD, exist_ok=True)
    json.dump(dict(engine="estimate", total=round(t + 3.0, 3), lines=lines), open(os.path.join(BUILD, "lines.json"), "w"), indent=1)
    print("estimated", round(t + 3, 1), "s")


def lay():
    """One take per line (ElevenLabs connector) -> lines.json with Whisper word times, and voice_dry.wav."""
    import soundfile as sf
    from faster_whisper import WhisperModel
    SR = 48000
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    t, meta, clips = LEAD, [], []
    for i, b in enumerate(B):
        d = glob.glob(os.path.join(BUILD, "takes", f"{i:03d}_{b['id']}", "*.mp3"))
        if not d:
            raise SystemExit(f"no take for {i:03d}_{b['id']}")
        wav = os.path.join(os.path.dirname(d[-1]), "take.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", sorted(d)[-1], "-ac", "1", "-ar", str(SR), wav], check=True)
        y, _ = sf.read(wav)
        on = np.where(np.abs(y) > 10 ** (-45 / 20) * np.abs(y).max())[0]
        a0, b0 = max(0, on[0] - int(0.04 * SR)), min(len(y), on[-1] + int(0.12 * SR))
        y, off = y[a0:b0], a0 / SR
        segs, _ = model.transcribe(wav, word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
        if i:
            t += CHAPTER_GAP if b["first"] else BEAT_GAP
        words = [[w.word.strip(), round(t + w.start - off, 3), round(t + w.end - off, 3)] for s in segs for w in s.words]
        dur = len(y) / SR
        meta.append(dict(i=i, id=b["id"], floor=b["floor"], text=b["text"], start=round(t, 3), end=round(t + dur, 3), words=words))
        clips.append((t, y))
        t += dur
    buf = np.zeros(int((t + 11.0) * SR))
    for t0, y in clips:
        buf[int(t0 * SR):int(t0 * SR) + len(y)] += y
    sf.write(os.path.join(BUILD, "voice_dry.wav"), buf, SR)
    json.dump(dict(engine="eleven", voice="george", total=round(t + 11.0, 3), lines=meta), open(os.path.join(BUILD, "lines.json"), "w"), indent=1)
    print("total", round(t + 11, 2))


if len(sys.argv) > 2 and sys.argv[2] in ("est", "lay", "lines"):
    {"est": est, "lay": lay, "lines": lambda: [print(f"{i:03d}_{b['id']}\t{len(b['said'])}\t{b['said']}") for i, b in enumerate(B)]}[sys.argv[2]]()
    sys.exit(0)

TL = json.load(open(os.path.join(BUILD, "lines.json")))
LINES = TL["lines"]
TOTAL = TL["total"]
N = len(B)


def S(i):
    return LINES[i]["start"]


def E(i):
    return LINES[i]["end"]


def NXT(i):
    return LINES[i + 1]["start"] if i + 1 < N else TOTAL


# ------------------------------------------------------------------ the world: one place per beat
def layout():
    P, x = [], 0.0
    for i, b in enumerate(B):
        k = b["vis"][0]
        ww = WIDTH[k]
        if i:
            x += (P[-1]["ww"] + ww) / 2 + (2600 if b["first"] else 520)
        y = 820 * math.sin(i * 1.9) + 380 * math.sin(i * 0.37)
        lab = k in ("img", "clip") and len(b["vis"]) > 2
        P.append(dict(i=i, kind=k, x=x, y=y, ww=ww, off=(-0.13 if lab and not VERT else 0.0)))
    return P


PL = layout()


def grey(im):
    """A picture as a grey field for the character look: levels stretched, mean pulled down, edges lifted, borders feathered."""
    g = im.astype(np.float32) / 255.0
    lo, hi = np.percentile(g, 3), np.percentile(g, 99.6)
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1)
    m = float(g.mean())
    g = g ** float(np.clip(math.log(0.36) / math.log(max(1e-3, m)), 1.0, 2.6))
    g = np.clip(g + 0.7 * (g - cv2.GaussianBlur(g, (0, 0), 3)), 0, 1)
    return np.clip(g - 0.04, 0, 1) / 0.96


def feather(h, w):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum(np.minimum(xx, w - 1 - xx) / (w * 0.26), np.minimum(yy, h - 1 - yy) / (h * 0.3))
    d = np.clip(d, 0, 1)
    return d * d * (3 - 2 * d)


_PIC = {}


def type_field(lines, frac=0.86, y=0.5, sizes=None):
    """Big type as a grey field, so numbers and short lines are made of characters like the pictures."""
    s = skia.Surface(1280, 720)
    c = s.getCanvas()
    c.clear(skia.ColorBLACK)
    lh = 720 * (0.8 if len(lines) == 1 else 0.6) / max(1.6, len(lines))      # several lines stay clear of the caption band
    size = lh * 0.98                                                # one size for every line: the smallest that fits the longest
    while max(font("InterTight-600", size).measureText(ln) for ln in lines) > 1280 * frac and size > 20:
        size -= 4
    f = font("InterTight-600", size)
    lh = min(lh, size * 1.12)
    for j, ln in enumerate(lines):
        yy = 720 * y + (j - (len(lines) - 1) / 2) * lh + size * 0.36
        c.drawString(ln, 640 - f.measureText(ln) / 2, yy, f, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
    g = s.makeImageSnapshot().toarray()[:, :, 1].astype(np.float32) / 255.0
    k = 1 if size > 150 else 3           # small type gets fatter strokes, or its characters are too thin to read
    if k > 1:
        g = cv2.dilate(g, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    return cv2.GaussianBlur(g, (0, 0), 1.2) * 0.92


def split_lines(s, n=16):
    out, cur = [], ""
    for w_ in s.split():
        if cur and len(cur) + 1 + len(w_) > n:
            out.append(cur)
            cur = w_
        else:
            cur = (cur + " " + w_).strip()
    return out + [cur]


_PHOTO = {}


def photo(pid):
    """A real photograph: its grey field for the characters (fitted inside 16:9, never stretched) and the picture itself,
    toned to the palette, with the rectangle it occupies in the place (fractions of the place's width and height)."""
    if pid not in _PHOTO:
        path = glob.glob(os.path.join(FILM, "src", "photo", pid + ".*"))[0]
        im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        h, w = im.shape
        sc = min(1280 * 0.94 / w, 720 * 0.94 / h)
        r = cv2.resize(im, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        lo, hi = np.percentile(r, 1), np.percentile(r, 99.5)
        r = np.clip((r - lo) / max(1e-3, hi - lo), 0, 1)
        fld = np.zeros((720, 1280), np.float32)
        y0, x0 = (720 - r.shape[0]) // 2, (1280 - r.shape[1]) // 2
        g = r ** 1.5
        fld[y0:y0 + r.shape[0], x0:x0 + r.shape[1]] = np.clip(g + 0.6 * (g - cv2.GaussianBlur(g, (0, 0), 3)), 0, 1)
        t = r[..., None]                                            # toned: black, through the film's cyan, to white
        rgb = np.where(t < 0.6, np.float32([0.02, 0.03, 0.035]) + (np.float32([0.37, 0.94, 0.89]) * 0.62 - 0.02) * (t / 0.6),
                       np.float32([0.37, 0.94, 0.89]) * 0.62 + (1 - np.float32([0.37, 0.94, 0.89]) * 0.62) * ((t - 0.6) / 0.4))
        rgba = np.dstack([(np.clip(rgb, 0, 1) * 255).astype(np.uint8), np.full(r.shape, 255, np.uint8)])
        img = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)
        _PHOTO[pid] = (fld, (img, x0 / 1280, y0 / 720, r.shape[1] / 1280, r.shape[0] / 720))
    return _PHOTO[pid]


_STILL = {}
RESOLVE = 0.8                                 # how far an illustration resolves from characters into the picture itself (8 Oct, the user: the characters alone can make the picture hard to read)


def toned(g):
    """A grey picture (0..1) in the film's palette: black, through cyan, to white."""
    t = g[..., None]
    cy = np.float32([0.37, 0.94, 0.89]) * 0.62
    return np.where(t < 0.6, np.float32([0.02, 0.03, 0.035]) + (cy - 0.02) * (t / 0.6), cy + (1 - cy) * ((t - 0.6) / 0.4))


def still(i, frame=0):
    """An illustration as a toned picture with soft edges, to show through its own characters."""
    key = (i, frame)
    if key not in _STILL:
        fr = pic(i)
        g = fr[frame % len(fr)][0]                                  # the same grey field the characters are read from (feathered, levelled)
        a = np.clip(g * 3.0, 0, 1) ** 0.8                           # dark surroundings stay clear: only the subject is laid in
        rgba = np.dstack([(np.clip(toned(np.clip(g * 1.15, 0, 1)), 0, 1) * 255).astype(np.uint8), (a * 255).astype(np.uint8)])
        if len(_STILL) > 40:
            _STILL.clear()
        _STILL[key] = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType)
    return _STILL[key]


def pic(i):
    """A place's grey field as mip levels (a clip has one set per frame); None for places that are only crisp type."""
    if i in _PIC:
        return _PIC[i]
    v = B[i]["vis"]
    k, frames = v[0], []
    if k in ("img", "clip"):
        path = glob.glob(os.path.join(FILM, "src", "ai", v[1] + ".*"))[0]
        if path.endswith(".mp4"):
            cap = cv2.VideoCapture(path)
            while True:
                ok, f = cap.read()
                if not ok:
                    break
                frames.append(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (960, 540), interpolation=cv2.INTER_AREA))
        else:
            im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            frames.append(cv2.resize(im, (1280, 720), interpolation=cv2.INTER_AREA))
        fe = feather(*frames[0].shape)
        frames = [grey(f) * fe for f in frames]
    elif k == "photo":
        g, _ = photo(v[1])
        frames = [g * feather(*g.shape)]
    elif k == "num" and len(v[1]) <= LONG_NUM:                      # a long "number" is a phrase: too small as characters, so world_type sets it crisp
        frames = [type_field([v[1]], 0.74, 0.44)]
    elif k == "words" and len(v[1]) <= LONG_WORDS:                  # longer lines are too small to read as characters: world_type sets them crisp
        frames = [type_field(split_lines(v[1], 12), 0.8, 0.41)]
    elif k == "split" and max(len(v[1][0]), len(v[2][0])) <= LONG_SPLIT:
        s = skia.Surface(1280, 720)
        c = s.getCanvas()
        c.clear(skia.ColorBLACK)
        for j, (big, _) in enumerate(v[1:3]):
            size = 300
            f = font("InterTight-600", size)
            while f.measureText(big) > 520:
                size -= 6
                f = font("InterTight-600", size)
            c.drawString(big, 320 + j * 640 - f.measureText(big) / 2, 370, f, skia.Paint(AntiAlias=True, Color=skia.ColorWHITE))
        frames = [cv2.GaussianBlur(s.makeImageSnapshot().toarray()[:, :, 1].astype(np.float32) / 255.0, (0, 0), 1.2) * 0.92]
    out = []
    for g in frames:
        lv = [g]
        for _ in range(3):
            lv.append(cv2.pyrDown(lv[-1]))
        out.append(lv)
    _PIC[i] = out or None
    if len(_PIC) > 14:                                              # only the places near the camera stay in memory
        for old in [q for q in _PIC if abs(q - i) > 6]:
            del _PIC[old]
    return _PIC[i]


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
    for n, p in enumerate(PL):
        x, y, ww = p["x"] + p["ww"] * p["off"], p["y"], p["ww"]
        z = W / ww * ((1.6 if p["kind"] in ("img", "clip", "photo") else 0.84 if p["kind"] in ("split", "tl") else 0.94) if VERT else 0.72 if p["kind"] == "photo" else 0.92)
        leave = 2.9 if (n + 1 < N and B[n + 1]["first"]) else 0.9          # a chapter's crossing is long: its name rides on it
        a, b = S(n) + (0.0 if n == 0 else 0.45 if E(n) - S(n) > 2.6 else 0.22), (NXT(n) - leave if n + 1 < N else TOTAL)
        b = max(b, a + 0.4)
        dx = ww * 0.03 * (1 if n % 2 else -1)
        if n == 0:
            k.append((0.0, (x - 40, y + 20, z * 1.45)))
            k.append((a + 1.4, (x + dx * 0.2, y, z * 1.02)))
        else:
            far = math.hypot(x - k[-1][1][0], y - k[-1][1][1])
            k.append((a, (x - dx, y + dx * 0.25, z * (0.94 if n % 2 else 1.06)), 0.35 + 0.25 * min(1.0, far / 6000)))
        k.append((b, (x + dx, y - dx * 0.25, z * (1.1 if n % 2 else 0.95))))
    return k


KEYS = keys()
_KT = [k[0] for k in KEYS]


def camera(t):
    t = min(max(t, KEYS[0][0]), KEYS[-1][0])
    i = max(0, min(len(KEYS) - 2, int(np.searchsorted(_KT, t, side="right")) - 1))
    (t0, a), k1 = KEYS[i][0:2], KEYS[i + 1]
    t1, b = k1[0], k1[1]
    u = (t - t0) / max(1e-6, t1 - t0)
    if len(k1) > 2:                                                 # a hop: pull out, travel, close in
        up = sm(u, 0.1, 0.9)
        zz = math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * sm(u, 0, 1) - k1[2] * math.sin(math.pi * u) ** 1.3)
        return a[0] + (b[0] - a[0]) * up, a[1] + (b[1] - a[1]) * up, zz
    e = sm(u, 0, 1) * 0.5 + u * 0.5                                 # a drift: never quite still
    return a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e, math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * e)


def now(t):
    """The index of the place the story is at."""
    return max(0, min(N - 1, int(np.searchsorted([ln["start"] for ln in LINES], t + 0.9, side="right")) - 1))


# ------------------------------------------------------------------ characters
def field(t, cx, cy, z):
    s = z * FW / W
    ls = s * LAT_WORLD / 512
    m = np.float32([[ls, 0, FW / 2 - SHIFT / 4 - cx * s], [0, ls, FH / 2 - RAISE / 4 - cy * s]])
    f = cv2.warpAffine(LAT, m, (FW, FH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP) * 0.16
    subj = np.zeros((FH, FW), np.float32)
    n = now(t)
    for i in range(max(0, n - 2), min(N, n + 3)):
        p = PL[i]
        x, y, ww = p["x"], p["y"], p["ww"]
        hh = ww * 9 / 16
        if abs(x - cx) > ww / 2 + W / z / 2 or abs(y - cy) > hh / 2 + H / z / 2:
            continue
        a = (sm(t, S(i) - 2.2, S(i) - 0.4) if i else 1.0) * (1 - sm(t, NXT(i) + 0.6, NXT(i) + 2.0))
        fr = pic(i)
        if not fr or a <= 0:
            continue
        lv = fr[0] if len(fr) == 1 else fr[_pingpong(int(t * 12), len(fr))]
        full = s * ww / lv[0].shape[1]
        g = lv[int(min(3, max(0, math.floor(-math.log2(max(full, 1e-6))))))]
        sc = s * ww / g.shape[1]
        m = np.float32([[sc, 0, FW / 2 - SHIFT / 4 + (x - ww / 2 - cx) * s], [0, sc, FH / 2 - RAISE / 4 + (y - hh / 2 - cy) * s]])
        subj = np.maximum(subj, cv2.warpAffine(g, m, (FW, FH), flags=cv2.INTER_LINEAR, borderValue=0) * a)
    return np.maximum(f * (1 - np.clip(subj * 6, 0, 1)), subj), subj


def _pingpong(i, n):
    i %= 2 * n - 2
    return i if i < n else 2 * n - 2 - i


def chars(t, cx, cy, z):
    f, subj = field(t, cx, cy, z)
    fld = cv2.resize(f, (COLS, ROWS), interpolation=cv2.INTER_AREA)
    fld = np.maximum(fld, cv2.dilate(fld, np.ones((3, 3), np.uint8)) * 0.32)   # a thin bright line lights the cells beside it
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
    k = np.clip(lum * 2.0, 0, 1)[..., None]
    c = np.where(k < 0.7, LO + (MID - LO) * (k / 0.7), MID + (HI - MID) * ((k - 0.7) / 0.3))
    c = cv2.resize(c.astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST)
    img = c * cov[..., None]
    back = cv2.resize(cv2.GaussianBlur(cv2.resize(subj, (FW // 2, FH // 2)), (0, 0), 9), (W, H), interpolation=cv2.INTER_LINEAR)
    out = np.float32([4, 5, 6]) / 255.0 + back[..., None] ** 1.4 * MID * 0.24 + img
    h = cv2.GaussianBlur(cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA), (0, 0), 2.2)
    out += 0.62 * cv2.resize(h, (W, H), interpolation=cv2.INTER_LINEAR)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    out *= (1 - 0.5 * np.clip((np.hypot(xx - W / 2, yy - H / 2) / 1100.0 - 0.55) / 0.45, 0, 1))[..., None]
    return np.clip(out, 0, 1)


# ------------------------------------------------------------------ type and lines, drawn crisp on top
def sans(sz):
    return font("InterTight-600", sz)


def mono(sz):
    return font("IBMPlexMono-500", sz)


def plate(c, x, y, w, h, a):
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Color=col(BG, 0.94 * a)))


def typed(s, t, t0, cps=30.0):
    n = int(max(0.0, t - t0) * cps)
    return s[:n] + ("█" if 0 < n < len(s) else "")


CAM = [0.0, 0.0, 1.0]                         # the frame's camera, for type that must know where it is on screen


def on_screen(x0, x1, y1):
    """1 when a block is wholly inside the frame and above the caption band, falling to 0 as it nears an edge."""
    cx, cy, z = CAM
    l, r, bot = (x0 - cx) * z + W / 2 - SHIFT, (x1 - cx) * z + W / 2 - SHIFT, (y1 - cy) * z + H / 2 - RAISE
    return sm(l, 14, 70) * (1 - sm(r, W - 70 - 2 * SHIFT, W - 14 - 2 * SHIFT)) * (1 - sm(bot, CAP_TOP - 40, CAP_TOP))


def held(i, t, t0=None):
    """A place's type: on once the camera has arrived, off as it leaves."""
    t0 = S(i) + 0.1 if t0 is None else max(t0, S(i) + 0.1)
    off = min(NXT(i) - 0.2, E(i) + 0.7) if i < N - 1 else TOTAL + 9     # the last line holds to the end
    return sm(t, t0, t0 + 0.35) * (1 - sm(t, off - 0.3, off)), t0


_SEG = {}


def seg_path(i):
    if i not in _SEG:
        (x0, y0), (x1, y1) = [(PL[j]["x"], PL[j]["y"] - PL[j]["ww"] * 0.3) for j in (i - 1, i)]   # over the top of each place, clear of its picture and type
        p = skia.Path()
        p.moveTo(x0, y0)
        p.cubicTo(x0 + (x1 - x0) * 0.5, y0, x0 + (x1 - x0) * 0.5, y1, x1, y1)
        _SEG[i] = p
    return _SEG[i]


def thread(c, t, z):
    """The story's path: one hairline through every place, lit as far as the story has gone, a pulse at its head."""
    n = now(t)
    faint = skia.Paint(Color=col(INK, 0.1), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5 / z)
    g = glow(CYAN, 0.55, 10 / z)
    g.setStyle(skia.Paint.kStroke_Style)
    g.setStrokeWidth(7 / z)
    line = skia.Paint(Color=col(CYAN), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6 / z)
    head = None
    for i in range(max(1, n - 3), min(N, n + 4)):
        p = seg_path(i)
        u = sm(t, S(i) - 1.6, S(i) + 0.5)
        c.drawPath(p, faint)
        if u > 0:
            m = skia.PathMeasure(p, False)
            lit = skia.Path()
            m.getSegment(0, m.getLength() * u, lit, True)
            c.drawPath(lit, g)
            c.drawPath(lit, line)
            if u < 1 or i == n:
                head = m.getPosTan(m.getLength() * u)[0]
    if head is not None:
        c.drawCircle(head.x(), head.y(), 16 / z, glow(INK, 0.9, 14 / z))
        c.drawCircle(head.x(), head.y(), 6 / z, skia.Paint(Color=col(INK), AntiAlias=True))


def fit_sans(s, size, maxw):
    maxw = min(maxw, (W - (300 if VERT else 200)) / max(CAM[2], 1e-6))      # never wider than the frame it is drawn in
    f = sans(size)
    while f.measureText(s) > maxw and size > 12:
        size -= 3
        f = sans(size)
    return f, size


def block(c, x0, top, w, h, a, pad=36):
    plate(c, x0 - pad, top - pad * 0.6, w + 2 * pad, h + pad * 1.2, a)


def world_type(c, t):
    n = now(t)
    for i in range(max(0, n - 1), min(N, n + 2)):
        p, v = PL[i], B[i]["vis"]
        k, x, y, u = p["kind"], p["x"], p["y"], p["ww"] / 2300.0
        a, t0 = held(i, t)
        if a <= 0:
            continue
        dur = max(1.0, E(i) - t0)
        if k in ("img", "clip") and RESOLVE > 0:                  # an illustration resolves most of the way into the picture; the characters stay as its grain
            fr = pic(i)
            rr = a * sm(t, S(i) + 0.8, S(i) + 2.0) * RESOLVE
            if fr and rr > 0:
                hh = p["ww"] * 9 / 16
                im = still(i, 0 if len(fr) == 1 else _pingpong(int(t * 12), len(fr)))
                c.drawImageRect(im, skia.Rect.MakeXYWH(x - p["ww"] / 2, y - hh / 2, p["ww"], hh), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(Color=col("#FFFFFF", rr)))
        if k == "photo":                                          # the characters resolve into the photograph itself
            _, (img, fx, fy, fw, fh) = photo(v[1])
            hh = p["ww"] * 9 / 16
            rr = a * sm(t, S(i) + 1.3, S(i) + 2.6)
            R = skia.Rect.MakeXYWH(x - p["ww"] / 2 + fx * p["ww"], y - hh / 2 + fy * hh, fw * p["ww"], fh * hh)
            if rr > 0:
                c.drawImageRect(img, R, skia.SamplingOptions(skia.CubicResampler.Mitchell()), skia.Paint(Color=col("#FFFFFF", 0.94 * rr)))
                c.drawRect(R, skia.Paint(Color=col(INK, 0.5 * rr), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2 * u))
            if len(v) > 3:
                text(c, typed("PHOTO  ·  " + v[3], t, t0 + 1.4, 40.0), R.left(), R.bottom() + 34 * u, mono(22 * u), DIM, a, 0.5 * u)
            if len(v) > 2:                                          # the label sits on the picture's lower left, on a plate
                f, size = fit_sans(v[2], 96 * u, R.width() - 90 * u)
                X, Y = R.left() + 44 * u, R.bottom() - 54 * u
                block(c, X, Y - size * 0.86, f.measureText(v[2]), size, a, 24 * u)
                text(c, v[2], X, Y, f, INK, a)
                c.drawRect(skia.Rect.MakeXYWH(X, Y + 18 * u, 80 * u, 6 * u), skia.Paint(Color=col(CYAN, a)))
        elif k in ("img", "clip") and len(v) > 2:
            f, size = fit_sans(v[2], 150 * u, 700 * u)
            X, Y = x - 1230 * u, y + 200 * u
            if VERT:                                                # above the picture, centred
                X, Y = x - f.measureText(v[2]) / 2, y - p["ww"] * 0.2 - 60 * u
            a *= on_screen(X - 36 * u, X + f.measureText(v[2]) + 36 * u, Y + 30 * u)
            if a > 0:
                block(c, X, Y - size * 0.86, f.measureText(v[2]), size, a, 30 * u)
                text(c, v[2], X, Y, f, INK, a)
                c.drawRect(skia.Rect.MakeXYWH(X, Y + 22 * u, 90 * u, 7 * u), skia.Paint(Color=col(CYAN, a)))
        elif k == "words" and len(v[1]) > LONG_WORDS:
            lines = split_lines(v[1], 17 if len(v[1]) < 40 else 24)
            f, size = fit_sans(max(lines, key=len), min(230.0, 640.0 / (len(lines) * 1.04)) * u, 1750 * u)
            lh = size * 1.04
            wd = max(f.measureText(s_) for s_ in lines)
            top = y - len(lines) * lh / 2 - 70 * u
            a *= on_screen(x - wd / 2 - 40 * u, x + wd / 2 + 40 * u, top + len(lines) * lh + 30 * u)
            if a > 0:
                c.drawRect(skia.Rect.MakeXYWH(x - wd / 2, top - 26 * u, 110 * u, 9 * u), skia.Paint(Color=col(CYAN, a)))
                for j, s_ in enumerate(lines):
                    aj = a * sm(t, t0 + 0.18 * j, t0 + 0.18 * j + 0.25)
                    text(c, s_, x - wd / 2, top + (j + 0.86) * lh, f, CYAN if j == len(lines) - 1 else INK, aj, halo=(16 * u if j == len(lines) - 1 else 0))
        elif k == "num":
            if len(v[1]) > LONG_NUM:
                f, size = fit_sans(v[1], 300 * u, 1800 * u)
                wd0 = f.measureText(v[1])
                a0 = a * on_screen(x - wd0 / 2 - 30 * u, x + wd0 / 2 + 30 * u, y + 120 * u)
                text(c, v[1], x - wd0 / 2, y + 60 * u, f, INK, a0)
            fm = mono(34 * u)
            s_ = v[2]
            while fm.measureText(s_) > 1900 * u:
                fm = mono(fm.getSize() - 1)
            wd = fm.measureText(s_)
            Y = y + 330 * u
            a *= on_screen(x - wd / 2 - 30 * u, x + wd / 2 + 30 * u, Y + 20 * u)
            if a > 0:
                block(c, x - wd / 2, Y - 34 * u, wd, 44 * u, a, 24 * u)
                text(c, typed(s_, t, t0 + 0.2), x - wd / 2, Y, fm, CYAN, a)
        elif k == "split":
            if max(len(v[1][0]), len(v[2][0])) > LONG_SPLIT:
                for j, (big, _) in enumerate(v[1:3]):
                    f, size = fit_sans(big, 170 * u, p["ww"] * 0.34)
                    bx = x + (-0.21 + 0.42 * j) * p["ww"] - f.measureText(big) / 2
                    text(c, big, bx, y + 90 * u, f, INK if j == 0 else CYAN, a * on_screen(bx - 20 * u, bx + f.measureText(big) + 20 * u, y + 120 * u), halo=(14 * u if j else 0))
            for j, (_, small) in enumerate(v[1:3]):
                fm = mono(30 * u)
                wd = fm.measureText(small)
                Y = y + 250 * u
                X = x + (-0.25 + 0.5 * j) * p["ww"] - wd / 2
                aa = a * on_screen(X - 30 * u, X + wd + 30 * u, Y + 20 * u)
                if aa > 0:
                    block(c, X, Y - 30 * u, wd, 40 * u, aa, 20 * u)
                    text(c, typed(small, t, t0 + 0.2 + 0.5 * j), X, Y, fm, CYAN if j == 0 else RED, aa)
        elif k == "quote":
            f = sans(80 * u)
            qw = min(1560 * u, (W - (330 if VERT else 200)) / max(CAM[2], 1e-6))
            lines = wrap(v[1], f, qw)
            lh = 100 * u
            while len(lines) > (9 if VERT else 6):
                f = sans(f.getSize() * 0.9)
                lh *= 0.9
                lines = wrap(v[1], f, qw)
            wd = max(f.measureText(s_) for s_ in lines)
            hgt = len(lines) * lh + 70 * u
            X, top = x - wd / 2, y - hgt / 2 - 80 * u
            a *= on_screen(X - 150 * u, X + wd + 40 * u, top + hgt + 30 * u)
            if a > 0:
                block(c, X - 110 * u, top - 40 * u, wd + 110 * u, hgt + 60 * u, a, 40 * u)
                text(c, "“", X - 120 * u, top + 150 * u, sans(260 * u), CYAN, a, halo=14 * u)
                shown = int(len(v[1]) * min(1.0, (t - t0 + 0.25) / min(len(v[1]) / 48.0 + 0.3, dur * 0.34, 2.2)))
                done = 0
                for j, s_ in enumerate(lines):
                    part = s_[:max(0, shown - done)]
                    done += len(s_) + 1
                    text(c, part, X, top + (j + 0.8) * lh, f, INK, a)
                c.drawRect(skia.Rect.MakeXYWH(X, top + len(lines) * lh + 18 * u, 90 * u, 6 * u), skia.Paint(Color=col(CYAN, a)))
                text(c, typed(v[2], t, t0 + 0.3, 60.0), X, top + len(lines) * lh + 66 * u, mono(30 * u), CYAN, a, 0.5 * u)
        elif k == "list":
            items, title = v[1], (v[2] if len(v) > 2 else None)
            f, size = fit_sans(max(items, key=len), 96 * u, 1700 * u)
            lh = size * 1.55
            wd = max(f.measureText(s_) for s_ in items)
            hgt = len(items) * lh + (70 * u if title else 0)
            X, top = x - wd / 2, y - hgt / 2 - 80 * u
            a *= on_screen(X - 80 * u, X + wd + 40 * u, top + hgt + 20 * u)
            if a > 0:
                block(c, X - 50 * u, top, wd + 50 * u, hgt, a, 40 * u)
                if title:
                    text(c, title, X, top + 30 * u, mono(32 * u), CYAN, a, 1.0 * u)
                for j, s_ in enumerate(items):
                    aj = a * sm(t, t0 + dur * 0.45 * j / len(items) - 0.1, t0 + dur * 0.45 * j / len(items) + 0.2)
                    Y = top + (70 * u if title else 0) + (j + 0.75) * lh
                    c.drawRect(skia.Rect.MakeXYWH(X - 40 * u, Y - size * 0.74, 10 * u, size * 0.78), skia.Paint(Color=col(CYAN, aj)))
                    text(c, s_, X, Y, f, INK, aj)
        elif k == "tl":
            marks = v[1]
            span = 1740 * u
            X0, Y = x - span / 2, y - 40 * u
            a *= on_screen(X0 - 60 * u, X0 + span + 60 * u, Y + 260 * u)
            if a > 0:
                block(c, X0, Y - 190 * u, span, 420 * u, a, 50 * u)
                c.drawLine(X0, Y, X0 + span * sm(t, t0, t0 + dur * 0.6), Y, skia.Paint(Color=col(CYAN, a), AntiAlias=True, StrokeWidth=4 * u))
                for j, (date, what) in enumerate(marks):
                    aj = a * sm(t, t0 + dur * 0.6 * j / len(marks), t0 + dur * 0.6 * j / len(marks) + 0.3)
                    mx = X0 + span * (j + 0.08) / len(marks)
                    c.drawCircle(mx, Y, 12 * u, skia.Paint(Color=col(INK, aj), AntiAlias=True))
                    fd, _ = fit_sans(max((d_ for d_, _w in marks), key=len), 92 * u, span / len(marks) * 0.84)
                    text(c, date, mx - 10 * u, Y - 50 * u, fd, INK, aj)
                    fm = mono(26 * u)
                    for q, s_ in enumerate(wrap(what, fm, span / len(marks) * 0.86)):
                        text(c, s_, mx - 10 * u, Y + (70 + q * 38) * u, fm, CYAN, aj)


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
    n = now(t - 0.9)
    if VERT:
        return short_screen(c, t, n)
    NC = len(SC.CHAPTERS)
    firsts = [i for i, b in enumerate(B) if b["first"]] + [N]
    cur = B[now(t + 1.4)]["floor"]                                  # it turns over as the chapter's name comes up
    c0, c1 = S(firsts[cur]) - (0 if cur == 0 else 2.3), (S(firsts[cur + 1]) - 2.3 if cur + 1 < NC else E(N - 1))
    prog = cur + min(1.0, max(0.0, (t - c0) / max(1.0, c1 - c0)))   # how far along the film, in chapters

    def rail(x0, x1, y, bw, bh, a, fs, big):
        """Numbered boxes on a hairline, one per chapter: done ones dim, the current one lit, the line filled as far as the film has run."""
        step = (x1 - x0 - bw) / max(1, NC - 1)
        c.drawLine(x0, y, x1, y, skia.Paint(Color=col(INK, 0.22 * a), AntiAlias=True, StrokeWidth=1.5))
        c.drawLine(x0, y, x0 + bw / 2 + step * min(prog, NC - 1), y, skia.Paint(Color=col(CYAN, a), AntiAlias=True, StrokeWidth=2.5 if big else 2))
        for k in range(NC):
            r = skia.Rect.MakeXYWH(x0 + k * step, y - bh / 2, bw, bh)
            on = k == cur
            c.drawRect(r, skia.Paint(Color=col(BG, a)))
            if on:
                c.drawRect(r, glow(CYAN, 0.5 * a, 8))
                c.drawRect(r, skia.Paint(Color=col("#0B2A2B", a)))
            c.drawRect(r, skia.Paint(Color=col(CYAN if on else INK, (1.0 if on else 0.75 if k < cur else 0.32) * a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2 if on else 1.3))
            text(c, f"{k + 1:02d}", r.centerX(), y + fs * 0.36, mono(fs), CYAN if on else INK, (1.0 if on else 0.8 if k < cur else 0.4) * a, align="center")

    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 104), skia.Paint(Color=col(BG, 0.78)))
    text(c, SC.TAG.split("·")[0].strip(), 70, 62, mono(20), DIM, 1.0, 1.0)
    rail(300, W - 70, 56, 46, 26, 1.0, 14, False)
    step = (W - 70 - 300 - 46) / max(1, NC - 1)
    name = SC.CHAPTERS[cur]["title"] or "COLD OPEN"
    nw = mono(17).measureText(name) + 0.6 * (len(name) - 1)
    text(c, name, min(max(300 + cur * step, 300), W - 70 - nw), 94, mono(17), CYAN, 1.0, 0.6)
    for i, b in enumerate(B):                                          # the chapter's name, while the camera crosses to it
        if b["first"] and b["title"] and abs(t - S(i)) < 4:
            a = sm(t, S(i) - CHAPTER_GAP + 1.0, S(i) - CHAPTER_GAP + 1.35) * (1 - sm(t, S(i) - 0.55, S(i) - 0.15))
            if a > 0:
                f, size = fit_sans(b["title"], 150, W - 360)
                wd = f.measureText(b["title"])
                c.drawRect(skia.Rect.MakeXYWH(0, H / 2 - 190, W, 400), skia.Paint(Color=col(BG, 0.97 * min(1.0, a * 2.5))))        # a band, up before the name: nothing behind reads through a chapter's name
                for yy in (H / 2 - 190, H / 2 + 210):
                    c.drawLine(0, yy, W, yy, skia.Paint(Color=col(INK, 0.14 * a), AntiAlias=True, StrokeWidth=1))
                text(c, f"CHAPTER {b['floor'] + 1:02d}", W / 2 - wd / 2, H / 2 - 116, mono(28), CYAN, a, 2.0)
                text(c, b["title"], W / 2 - wd / 2, H / 2 + 24, f, INK, a)
                rail(200, W - 200, H / 2 + 132, 96, 54, a, 24, True)
    a = sm(t, E(N - 1) + 1.2, E(N - 1) + 2.0)
    if a > 0:                                                       # the sign-off, with room left for end-screen elements above it
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - 430, H - 226, 860, 150), skia.Paint(Color=col(BG, 0.9 * a)))
        text(c, CHANNEL, W / 2, H - 150, sans(64), INK, a, 6.0, align="center")
        text(c, ("AI, EXPLAINED  ·  " if CHANNEL == "THE CURVE" else "") + "SOURCES IN THE DESCRIPTION", W / 2, H - 100, mono(24), CYAN, a, 1.0, align="center")
    captions(c, t, n)


def captions(c, t, n):
    for ln in LINES[max(0, n - 1):n + 3]:
        k = sm(t, ln["start"], ln["start"] + 0.15) * (1 - sm(t, ln["end"] + 0.02, ln["end"] + 0.14))   # two lines are never up together
        if k <= 0:
            continue
        f = sans(56 if VERT else 34)
        CL, CB = (68, H - 440) if VERT else (44, H - 66)
        cap = re.sub(r"GPT (\d)", r"GPT-\1", ln["text"])
        mw = (W - 290) if VERT else 1180
        CX = W / 2 - SHIFT
        lines = wrap(cap, f, mw)
        while len(lines) > 3 and mw < (W - 250 if VERT else 1560):
            mw += 60
            lines = wrap(cap, f, mw)
        full = len(lines)
        while len(lines[-1].split()) < 2 and mw > 700 and len(lines) == full and full > 1:     # no word alone on the last line
            mw -= 40
            lines = wrap(cap, f, mw)
        if len(lines) != full:
            lines = wrap(cap, f, mw + 40)
        ws = ln.get("words") or []
        nw = len(cap.split())
        said = sum(1 for w_ in ws if w_[1] <= t) if ws else int(nw * sm(t, ln["start"], ln["end"]) + 0.999)
        y0 = CB - (len(lines) - 1) * CL
        wmax = max(f.measureText(x) for x in lines)
        pl = skia.Rect.MakeXYWH(CX - wmax / 2 - 34, y0 - CL - 2, wmax + 68, len(lines) * CL + 28)
        c.drawRect(pl, skia.Paint(Color=col(BG, 0.985 * k)))
        c.drawLine(pl.left(), pl.top(), pl.right(), pl.top(), skia.Paint(Color=col(INK, 0.22 * k), AntiAlias=True, StrokeWidth=1))
        m = 0
        for i, s in enumerate(lines):
            x = CX - f.measureText(s) / 2
            for w_ in s.split():
                text(c, w_, x, y0 + i * CL, f, INK, k * (1.0 if m < said else 0.42))
                x += f.measureText(w_ + " ")
                m += 1


SHORT = dict(t0=0.0, t1=1e9, headline="", film="")


def short_screen(c, t, n):
    """A Short's furniture: the headline up top, captions above the app's own buttons, an end card to the full film."""
    f = sans(60)
    lines = wrap(SHORT["headline"], f, W - 260)
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 190 + len(lines) * 70), skia.Paint(Color=col(BG, 0.9)))
    text(c, CHANNEL, 75, 150, mono(26), CYAN, 1.0, 3.0)
    for i, s_ in enumerate(lines):
        text(c, s_, 75, 230 + i * 70, f, INK)
    e = sm(t, SHORT["t1"] - 3.4, SHORT["t1"] - 3.1)
    if e > 0:
        c.drawRect(skia.Rect.MakeXYWH(0, 190 + len(lines) * 70, W, H), skia.Paint(Color=col(BG, e)))
        text(c, "WATCH THE FULL FILM", W / 2, H / 2 - 150, mono(30), CYAN, e, 3.0, align="center")
        ff, _ = fit_sans(SHORT["film"].upper(), 92, W - 140)
        text(c, SHORT["film"].upper(), W / 2, H / 2 - 30, ff, INK, e, align="center")
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - 60, H / 2 + 20, 120, 7), skia.Paint(Color=col(CYAN, e)))
        text(c, "ON " + CHANNEL + "  ·  LINK ON THIS SHORT", W / 2, H / 2 + 110, mono(26), INK, e, 1.0, align="center")
    else:
        captions(c, t, n)


def frame(t):
    cx, cy, z = camera(t)
    CAM[:] = [cx, cy, z]
    px = (chars(t, cx, cy, z) * 255).astype(np.uint8)
    rgba = np.dstack([px, np.full((H, W), 255, np.uint8)])
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    c.drawImage(skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType), 0, 0)
    c.save()
    c.translate(W / 2 - SHIFT, H / 2 - RAISE)
    c.scale(z, z)
    c.translate(-cx, -cy)
    if THREAD:
        thread(c, t, z)
    world_type(c, t)
    c.restore()
    screen(c, t, cx, cy, z)
    a = sm(t, -0.2, 0.35) * (1 - sm(t, TOTAL - 1.4, TOTAL - 0.1))
    if VERT:
        a = 1 - sm(t, SHORT["t1"] - 0.35, SHORT["t1"])
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
    cmd = sys.argv[2]
    if cmd == "still":
        os.makedirs(os.path.join(BUILD, "qc"), exist_ok=True)
        ims = []
        for t in [float(x) for x in sys.argv[3:]]:
            im = cv2.cvtColor(frame(t), cv2.COLOR_RGBA2BGR)
            cv2.imwrite(os.path.join(BUILD, "qc", f"f_{t:07.2f}.jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
            sm_ = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
            cv2.putText(sm_, f"{t:.1f}s  {B[now(t - 0.9)]['id']}", (16, 524), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            ims.append(sm_)
        while len(ims) % 2:
            ims.append(np.zeros_like(ims[0]))
        cv2.imwrite(os.path.join(BUILD, "qc", "sheet.jpg"), np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(os.path.join(BUILD, "qc", "sheet.jpg"))
    elif cmd == "seg":
        a, b = float(sys.argv[3]), float(sys.argv[4])
        encode(a, min(b, TOTAL), os.path.join(BUILD, f"seg_{int(a):04d}.mp4"), "1920:1080")
    elif cmd == "short":                                            # FLOW_VERT=1 flow.py <film> short <name> <first id> <last id> <film mp4> "<headline>" "<film title>"
        name, a_id, b_id, mp4, head, film = sys.argv[3:9]
        ids = [b["id"] for b in B]
        t0, t1 = max(0.0, S(ids.index(a_id)) - 0.15), E(ids.index(b_id)) + 0.5 + 3.4
        SHORT.update(t0=t0, t1=t1, headline=head, film=film)
        os.makedirs(os.path.join(FILM, "shorts"), exist_ok=True)
        pic_, out = os.path.join(BUILD, f"short_{name}_pic.mp4"), os.path.join(FILM, "shorts", f"short_{name}.mp4")
        encode(t0, t1, pic_, "1080:1920")
        d = t1 - t0
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pic_, "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", mp4, "-map", "0:v", "-map", "1:a",
                        "-af", f"afade=t=in:d=0.25,afade=t=out:st={d - 2.4:.2f}:d=2.3", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
        print(out, round(d, 1), "s")
    elif cmd == "times":
        for ln in LINES:
            print(f"{ln['start']:7.2f} {ln['end']:7.2f}  {ln['id']:10s} {B[ln['i']]['vis'][0]}")


if __name__ == "__main__":
    main()
