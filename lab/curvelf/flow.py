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
LONG_WORDS = 14
THREAD = False                                # the wandering line through every place (7 Oct, the user: not as the guide; a rail of numbered boxes instead, as in How They Profit 06)
LONG_NUM = 0                                  # 8 Oct, final critic: figures as characters read dim; every figure is set crisp
LONG_SPLIT = 0                                # a split's big words longer than this are set crisp
CAP_TOP = (H - 600) if VERT else (H - 165)   # where the caption band begins
RAISE = 40 if VERT else 20
SHIFT = 56 if VERT else 0                     # a Short sits left of centre: the app's buttons run down the right edge    #                                # screen pixels the world is lifted, so pictures clear the caption plate
WIDTH = dict(photo=2300, img=2300, clip=2500, num=2100, words=2300, quote=2300, list=2100, split=2500, tl=2700, map=2300)

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
LANG = getattr(SC, "LANG", "en")               # the narration's language (a translated film sets LANG in its script)
HOLD = getattr(SC, "HOLD", {})                  # {beat id: seconds of silence after it}
UI = {"en": dict(open="COLD OPEN", chapter="CHAPTER", sources="SOURCES IN THE DESCRIPTION", tagline="AI, EXPLAINED  ·  ", photo="PHOTO  ·  ",
                 illus="ILLUSTRATION  ·  AI-GENERATED", watch="WATCH THE FULL FILM", on="ON ", link="  ·  LINK ON THIS SHORT"),
      "es": dict(open="INICIO", chapter="CAPÍTULO", sources="FUENTES EN LA DESCRIPCIÓN", tagline="LA IA, EXPLICADA  ·  ", photo="FOTO  ·  ",
                 illus="ILUSTRACIÓN  ·  GENERADA CON IA", watch="MIRA LA PELÍCULA COMPLETA", on="EN ", link="  ·  ENLACE EN ESTE SHORT")}
UI = UI.get(LANG, UI["en"])                   # the engine's own on-screen words, in the film's language
ILLUS = getattr(SC, "ILLUS", "")                # a film whose pictures are drawn, not generated, says so on every one (9 Oct critic: "AI-GENERATED" on code-drawn diagrams was false)
if ILLUS:
    UI["illus"] = ILLUS
LEAD = getattr(SC, "LEAD", LEAD)                # seconds of picture before the first word
OPEN_RESOLVED = getattr(SC, "OPEN_RESOLVED", False)     # frame 0 shows the first picture already resolved (it is the Short hook and the fallback thumbnail)
CHROME = getattr(SC, "CHROME", "curve")         # "chart" (9 Oct, maps channel): a nav-instrument header, plain captions, cards in ruled frames
CHART = CHROME == "chart"


def beats():
    """Every beat as a line: id, chapter index, the text shown in captions, the text said, and its visual."""
    out = []
    for ci, ch in enumerate(SC.CHAPTERS):
        for bi, b in enumerate(ch["beats"]):
            shown, said = b[0] if isinstance(b[0], tuple) else (b[0], b[0])
            out.append(dict(id=f"{ch['id']}_{bi:02d}", floor=ci, text=shown, said=said, vis=b[1], first=(bi == 0), title=ch["title"]))
    return out


B = beats()
HAS_PHOTO = any(b["vis"][0] == "photo" for b in B)
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
    model = WhisperModel("small.en" if LANG == "en" else "small", device="cpu", compute_type="int8")     # another language: the multilingual model
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
        segs, _ = model.transcribe(wav, word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False, language=LANG)
        if i:
            t += CHAPTER_GAP if b["first"] else BEAT_GAP
        words = [[w.word.strip(), round(t + w.start - off, 3), round(t + w.end - off, 3)] for s in segs for w in s.words]
        dur = len(y) / SR
        meta.append(dict(i=i, id=b["id"], floor=b["floor"], text=b["text"], start=round(t, 3), end=round(t + dur, 3), words=words))
        clips.append((t, y))
        t += dur + HOLD.get(b["id"], 0.0)                         # a short line's card may be held past its words
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
        if i and k == "map" and P[-1]["kind"] == "map":           # map after map: the same plate, the geography zooms (handover)
            P.append(dict(i=i, kind=k, x=x, y=P[-1]["y"], ww=ww, off=0.0))
            continue
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


# ------------------------------------------------------------------ maps: the world set in type (the How They Profit 06 opening)
# ("map", dict(view=(lon0, lat0, lon1, lat1), labels=[(lon, lat, title, sub)], routes=[[(lon, lat), ...]], pins=[(lon, lat)],
#              zones=[[(lon, lat), ...]], caption="...")). Land is Natural Earth (public domain): 1:110m for wide views,
# 1:10m for regional ones. Equirectangular, longitudes scaled by cos(mid latitude). The view is the least that is shown:
# it is widened to fill the map's box. Coast cells are #+%*, land .:·, sea empty; routes, pins and zones are the one accent.
DATA = os.path.join(HERE, "data")
MAP_LAND, MAP_COAST = "#56636B", "#A9B4BB"      # brighter (9 Oct: the land read as faint next to the Visa map)
_LAND, _MAPF, _MAPP = {}, {}, {}


def land_rings(res):
    """Every land ring of a Natural Earth file as an (n, 2) array with its bounding box."""
    if res not in _LAND:
        out = []
        for ft in json.load(open(os.path.join(DATA, f"ne_{res}_land.geojson")))["features"]:
            for ring in ft["geometry"]["coordinates"]:
                a = np.asarray(ring, np.float64)
                out.append((a, a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()))
        _LAND[res] = out
    return _LAND[res]


def map_frame(i):
    """A map's geometry in the world: the box it fills, the widened view, the grid, and lon/lat -> world."""
    if i in _MAPF:
        return _MAPF[i]
    v, p = B[i]["vis"][1], PL[i]
    lon0, lat0, lon1, lat1 = v["view"]
    ov = [q[:2] for q in list(v.get("pins", [])) + list(v.get("labels", []))] + [q for r in v.get("routes", []) for q in r] + [q for z in v.get("zones", []) for q in z]
    if ov:                                                          # the view grows to hold every overlay, with a margin (9 Oct critic H3)
        mx_, my_ = 0.07 * (lon1 - lon0), 0.09 * (lat1 - lat0)
        lon0, lon1 = min(lon0, min(q[0] for q in ov) - mx_), max(lon1, max(q[0] for q in ov) + mx_)
        lat0, lat1 = min(lat0, min(q[1] for q in ov) - my_), max(lat1, max(q[1] for q in ov) + my_)
    u = p["ww"] / 2300.0
    BW, BH = (1700.0, 1250.0) if VERT else (2060.0, 760.0)
    BW, BH = BW * u, BH * u
    k = math.cos(math.radians((lat0 + lat1) / 2))
    sc = min(BW / ((lon1 - lon0) * k), BH / (lat1 - lat0))         # world units per degree of latitude
    lw, lh = min(360.0, BW / sc / k), min(170.0, BH / sc)           # the view, widened to the box (never past the whole earth)
    cx_, cy_ = (lon0 + lon1) / 2, min(85 - lh / 2, max(-85 + lh / 2, (lat0 + lat1) / 2))
    cw = ((29.0 if VERT else 18.0) * (0.66 if lw < 6.5 else 1.0)) * u    # one character cell; finer for a close view, so islands separate
    chh = cw * 4 / 3
    cols, rows = int(lw * sc * k / cw), int(lh * sc / chh)
    w, h = cols * cw, rows * chh
    L0, L1, A0, A1 = cx_ - lw / 2, cx_ + lw / 2, cy_ - lh / 2, cy_ + lh / 2
    bx, by = p["x"] - w / 2, p["y"] - h / 2 - (55 if not VERT else 120) * u     # lifted: the ruler and the source line sit under it

    def proj(lon, lat):
        return bx + (lon - L0) / (L1 - L0) * w, by + (A1 - lat) / (A1 - A0) * h

    pts = [proj(q[0], q[1]) for q in list(v.get("pins", [])) + [lb[:2] for lb in v.get("labels", [])]]
    focus = ((sum(q[0] for q in pts) / len(pts) - p["x"], sum(q[1] for q in pts) / len(pts) - p["y"]) if pts else (0.0, 0.0))
    _MAPF[i] = dict(v=v, u=u, bx=bx, by=by, w=w, h=h, cols=cols, rows=rows, cw=cw, ch=chh, view=(L0, A0, L1, A1), proj=proj,
                    focus=(max(-400.0, min(400.0, focus[0])), max(-200.0, min(200.0, focus[1]))))
    return _MAPF[i]


def map_res(m):
    L0, A0, L1, A1 = m["view"]
    return "110m" if L1 - L0 > 40 else "10m"


def map_mask(m, ss=4):
    """Land coverage of every cell (0..1): the rings that touch the view, clipped to it, filled at ss x ss per cell; and the fine fill."""
    L0, A0, L1, A1 = m["view"]
    cols, rows = m["cols"], m["rows"]
    gw, gh = cols * ss, rows * ss
    mx, my = 0.08 * (L1 - L0), 0.08 * (A1 - A0)
    polys = []
    for a, x0, y0, x1, y1 in land_rings(map_res(m)):
        if x1 < L0 - mx or x0 > L1 + mx or y1 < A0 - my or y0 > A1 + my:
            continue
        g = np.empty_like(a)
        g[:, 0] = (a[:, 0] - L0) / (L1 - L0) * gw
        g[:, 1] = (A1 - a[:, 1]) / (A1 - A0) * gh
        g[:, 0] = np.clip(g[:, 0], -0.08 * gw, 1.08 * gw)                   # clamped just outside the view: exact inside it
        g[:, 1] = np.clip(g[:, 1], -0.08 * gh, 1.08 * gh)
        q = np.round(g * 16).astype(np.int32)
        keep = np.r_[True, np.any(q[1:] != q[:-1], axis=1)]
        q = q[keep]
        if len(q) >= 3:
            polys.append(q.reshape(-1, 1, 2))
    img = np.zeros((gh, gw), np.uint8)
    if polys:
        cv2.fillPoly(img, polys, 255, lineType=cv2.LINE_AA, shift=4)          # even-odd over all rings: holes stay holes
    return img.reshape(rows, ss, cols, ss).mean(axis=(1, 3)) / 255.0, img


def coast_path(m):
    """The coastline itself, as vector runs in the world (the Natural Earth rings, kept to the view)."""
    L0, A0, L1, A1 = m["view"]
    mx, my = 0.04 * (L1 - L0), 0.04 * (A1 - A0)
    path = skia.Path()
    step = 0.5 * m["cw"] / 18.0
    for a, x0, y0, x1, y1 in land_rings(map_res(m)):
        if x1 < L0 - mx or x0 > L1 + mx or y1 < A0 - my or y0 > A1 + my:
            continue
        inside = (a[:, 0] > L0 - mx) & (a[:, 0] < L1 + mx) & (a[:, 1] > A0 - my) & (a[:, 1] < A1 + my)
        X = m["bx"] + (a[:, 0] - L0) / (L1 - L0) * m["w"]
        Y = m["by"] + (A1 - a[:, 1]) / (A1 - A0) * m["h"]
        d = np.diff(inside.astype(np.int8), prepend=0, append=0)
        for s0, s1 in zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]):
            xs, ys = X[s0:s1], Y[s0:s1]
            if len(xs) < 2:
                continue
            keep = [0]
            for q in range(1, len(xs)):                               # drop points closer than half a world unit
                if abs(xs[q] - xs[keep[-1]]) + abs(ys[q] - ys[keep[-1]]) > step or q == len(xs) - 1:
                    keep.append(q)
            path.addPoly([skia.Point(float(xs[q]), float(ys[q])) for q in keep], False)
    return path


def nice_step(span, n=6):
    for s_ in (0.25, 0.5, 1, 2, 5, 10, 15, 20, 30, 45, 60, 90):
        if span / s_ <= n:
            return s_
    return 90


def deg(x, pos, neg, frac):
    return (f"{abs(x):.1f}" if frac else f"{abs(x):.0f}") + (pos if x >= 0 else neg)


SEA, LANDF = "#06141B", "#1A2226"                 # the sea has a colour (blue-black); the land a faint warm-grey mass under its glyphs


def map_pics(i):
    """A map's type as two recorded pictures (every frame replays them): the map itself, and its coast lit in the accent.
    The coast is a vector stroke from the real rings; its glyphs follow its direction (- | / \\); land inside is a quiet
    dot field; the sea is tinted with a sparse ~ swell (9 Oct critic H2)."""
    if i in _MAPP:
        return _MAPP[i]
    m = map_frame(i)
    cov, fine = map_mask(m, 6)
    land = cov > 0.5
    pad = np.pad(land, 1, mode="edge")                                      # the box's edge is not a coast
    water_near = ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    coast = (land & water_near) | ((cov > 0.3) & ~land)     # 0.3: a sliver of land too small to fill a cell is still drawn
    dist = cv2.distanceTransform(np.pad(land, 1, mode="edge").astype(np.uint8), cv2.DIST_L1, 3)[1:-1, 1:-1]
    second = land & ~coast & (dist <= 2)
    inner = land & ~coast & ~second
    sea_d = cv2.distanceTransform(np.pad(cov < 0.05, 1, mode="edge").astype(np.uint8), cv2.DIST_L1, 3)[1:-1, 1:-1]
    sm_ = cv2.GaussianBlur(cov.astype(np.float32), (0, 0), 0.9)
    gx = cv2.Sobel(sm_, cv2.CV_32F, 1, 0, ksize=3) / m["cw"]
    gy = cv2.Sobel(sm_, cv2.CV_32F, 0, 1, ksize=3) / m["ch"]
    ang = np.degrees(np.arctan2(gx, -gy)) % 180.0                  # the coast's own direction (across the gradient), y down
    ori = np.select([(ang < 22.5) | (ang >= 157.5), ang < 67.5, ang < 112.5], ["-", "\\", "|"], "/")
    f = mono(m["ch"] * 0.95)
    gwid = f.measureText("#")
    cpath = coast_path(m)
    rgba = np.zeros(fine.shape + (4,), np.uint8)
    rgba[..., :3] = [int(LANDF[1:3], 16), int(LANDF[3:5], 16), int(LANDF[5:7], 16)]
    rgba[..., 3] = fine
    fimg = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType)
    box = skia.Rect.MakeXYWH(m["bx"], m["by"], m["w"], m["h"])
    L0, A0, L1, A1 = m["view"]
    st = nice_step(max(L1 - L0, (A1 - A0) * 1.6), 8)

    def rec_(draw):
        rec = skia.PictureRecorder()
        c = rec.beginRecording(skia.Rect.MakeXYWH(m["bx"] - 400, m["by"] - 400, m["w"] + 800, m["h"] + 800))
        c.save()
        c.clipRect(box)
        draw(c)
        c.restore()
        return rec.finishRecordingAsPicture()

    def stroke(c, lit):
        c.drawPath(cpath, skia.Paint(Color=col(CYAN if lit else MAP_COAST, 0.9 if lit else 0.55), AntiAlias=True, Style=skia.Paint.kStroke_Style,
                                     StrokeWidth=(2.2 if lit else 1.5) * m["u"], StrokeJoin=skia.Paint.kRound_Join))

    def vector(c):                                                  # land mass, the sea's swell, the coast stroke, the graticule
        c.drawImageRect(fimg, box, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(Color=col("#FFFFFF", 0.9)))
        stroke(c, False)
        pg = skia.Paint(Color=col(INK, 0.16), AntiAlias=True, StrokeWidth=1.4 * m["u"])
        r_ = 5 * m["u"]
        for lo in np.arange(math.ceil(L0 / st) * st, L1, st):
            for la in np.arange(math.ceil(A0 / st) * st, A1, st):
                x, y = m["proj"](lo, la)
                jj, ii = int((y - m["by"]) / m["ch"]), int((x - m["bx"]) / m["cw"])
                if 0 <= jj < m["rows"] and 0 <= ii < m["cols"] and cov[jj, ii] < 0.05:
                    c.drawLine(x - r_, y, x + r_, y, pg)
                    c.drawLine(x, y - r_, x, y + r_, pg)

    def glyphs(c, lit):
        if not lit:
            sw = skia.Paint(Color=col("#3F8C93", 0.30), AntiAlias=True)        # the sea: a sparse swell of ~, clear of the shore
            for j in range(1, m["rows"], 3):
                ii = [q for q in range((j // 3) % 2 * 3 + 1, m["cols"], 6) if sea_d[j, q] > 2]
                if ii:
                    xs = [m["bx"] + q * m["cw"] + (m["cw"] - gwid) / 2 for q in ii]
                    c.drawTextBlob(skia.TextBlob.MakeFromPosTextH("~" * len(ii), xs, m["by"] + (j + 0.8) * m["ch"], f), 0, 0, sw)
        pc = skia.Paint(Color=col(CYAN if lit else MAP_COAST, 1.0 if lit else 0.95), AntiAlias=True)
        p2 = skia.Paint(Color=col(CYAN if lit else MAP_LAND, 0.45 if lit else 1.0), AntiAlias=True)
        pl = skia.Paint(Color=col(CYAN if lit else MAP_LAND, 0.3 if lit else 0.75), AntiAlias=True)
        for j in range(m["rows"]):
            y = m["by"] + (j + 0.8) * m["ch"]
            for mask, glyph, paint in ((inner[j], "·", pl), (second[j], ":", p2), (coast[j], None, pc)):
                ii = np.nonzero(mask)[0]
                if len(ii):
                    s_ = "".join(ori[j, q] for q in ii) if glyph is None else glyph * len(ii)
                    xs = [m["bx"] + q * m["cw"] + (m["cw"] - gwid) / 2 for q in ii]
                    c.drawTextBlob(skia.TextBlob.MakeFromPosTextH(s_, xs, y, f), 0, 0, paint)

    out = [rec_(vector), rec_(lambda c: glyphs(c, False)), rec_(lambda c: (stroke(c, True), glyphs(c, True)))]
    _MAPP[i] = out
    if len(_MAPP) > 6:
        for old in [q for q in _MAPP if abs(q - i) > 3]:
            del _MAPP[old]
    return out


# ---- map after map: one plate, the geography zooms from one view into the next (9 Oct critic M1: no dip to black)
def handover_in(i):
    """True when beat i is a map that takes over from the map just before it (same plate)."""
    return 0 < i < N and B[i]["vis"][0] == "map" and B[i - 1]["vis"][0] == "map" and PL[i]["x"] == PL[i - 1]["x"]


def ho_window(j):
    """The seconds over which map j takes over from map j-1."""
    return (S(j) - 2.4, S(j) + 0.5) if B[j]["first"] else (S(j) - 0.6, S(j) + 1.0)


def ho_geo(j):
    """Per axis (scale, offset) taking map j's world coords onto map j-1's, so the same lon/lat lands on the same point."""
    a, b = map_frame(j - 1), map_frame(j)
    (L0i, A0i, L1i, A1i), (L0j, A0j, L1j, A1j) = a["view"], b["view"]
    sx = ((L1j - L0j) / b["w"]) / ((L1i - L0i) / a["w"])
    sy = ((A1j - A0j) / b["h"]) / ((A1i - A0i) / a["h"])
    ox = a["bx"] + (L0j - L0i) * a["w"] / (L1i - L0i) - sx * b["bx"]
    oy = a["by"] + (A1i - A1j) * a["h"] / (A1i - A0i) - sy * b["by"]
    return (sx, ox), (sy, oy)


def ho_D(j, e):
    """The display transform at progress e: identity for map j-1 at e=0, and the inverse of ho_geo at e=1."""
    out = []
    for s, o in ho_geo(j):
        se = s ** -e
        if abs(s - 1) < 1e-6:
            out.append((1.0, -e * o / s))
        else:
            f_ = -o / (s - 1)
            out.append((se, f_ * (1 - se)))
    return out


def ho_progress(j, t):
    a, b = ho_window(j)
    return sm(t, a, b)


def map_xform(i, t):
    """(sx, ox, sy, oy, role, e): how map i is displayed now; role 'in' while it takes over, 'out' while it hands over."""
    if handover_in(i):
        e = ho_progress(i, t)
        if e < 1:
            (dx, dox), (dy, doy) = ho_D(i, e)
            (gx, gox), (gy, goy) = ho_geo(i)
            return dx * gx, dx * gox + dox, dy * gy, dy * goy + doy, "in", e
    if i + 1 < N and handover_in(i + 1):
        e = ho_progress(i + 1, t)
        if e > 0:
            (dx, dox), (dy, doy) = ho_D(i + 1, e)
            return dx, dox, dy, doy, "out", e
    return 1.0, 0.0, 1.0, 0.0, None, 0.0


def map_geo_at(i, t, wx, wy):
    """The lon/lat under a world point, as map i shows it now."""
    m = map_frame(i)
    sx, ox, sy, oy, _, _ = map_xform(i, t)
    x, y = (wx - ox) / sx, (wy - oy) / sy
    L0, A0, L1, A1 = m["view"]
    return L0 + (x - m["bx"]) / m["w"] * (L1 - L0), A1 - (y - m["by"]) / m["h"] * (A1 - A0)


def spring(x):
    """A critically damped spring from 0 to 1: quick out, long settle."""
    x = min(1.0, max(0.0, x))
    return (1 - (1 + 8 * x) * math.exp(-8 * x)) / (1 - 9 * math.exp(-8))


def route_path(m, pts):
    """A route through its points as a smooth curve (Catmull-Rom) in the world."""
    P = [m["proj"](lo, la) for lo, la in pts]
    p = skia.Path()
    p.moveTo(*P[0])
    for j in range(len(P) - 1):
        a0, a1, a2, a3 = P[max(0, j - 1)], P[j], P[j + 1], P[min(len(P) - 1, j + 2)]
        for s_ in range(1, 13):
            q = s_ / 12
            p.lineTo(*[0.5 * (2 * a1[d] + (-a0[d] + a2[d]) * q + (2 * a0[d] - 5 * a1[d] + 4 * a2[d] - a3[d]) * q * q
                              + (-a0[d] + 3 * a1[d] - 3 * a2[d] + a3[d]) * q ** 3) for d in (0, 1)])
    return p


def map_labels(i):
    """Where each label's plate goes: beside its point, on the side with room, clear of the other plates and points."""
    m = map_frame(i)
    if "plates" in m:
        return m["plates"]
    u = m["u"] * (1.7 if VERT else 1.0)
    ft, fs = sans(50 * u), mono(31 * u)
    taken = [skia.Rect.MakeLTRB(x - 14 * u, y - 14 * u, x + 14 * u, y + 14 * u) for x, y in
             [m["proj"](*q) for q in list(m["v"].get("pins", [])) + [lb[:2] for lb in m["v"].get("labels", [])]]]
    out = []
    cxm, cym = m["bx"] + m["w"] / 2, m["by"] + m["h"] / 2
    for lon, lat, title, sub in m["v"].get("labels", []):
        x, y = m["proj"](lon, lat)
        pw = max(ft.measureText(title), fs.measureText(sub) + 0.5 * u * len(sub)) + 36 * u
        ph = 112 * u if sub else 72 * u
        cands = []
        for L in (64 * u, 150 * u, 250 * u):
            for sy in ((1, -1) if y < cym else (-1, 1)):
                for sx in ((1, -1) if x < cxm else (-1, 1)):
                    cands.append((sx, sy, skia.Rect.MakeXYWH(x + 2 if sx > 0 else x - pw - 2, y + L if sy > 0 else y - L - ph, pw, ph)))
            for sx in ((1, -1) if x < cxm else (-1, 1)):            # beside the point, the leader running sideways
                cands.append((sx, 0, skia.Rect.MakeXYWH(x + L if sx > 0 else x - L - pw, y - ph / 2, pw, ph)))
        best, bs = None, 1e18
        for n_, (sx, sy, r) in enumerate(cands):
            inside = r.left() > m["bx"] + 6 * u and r.right() < m["bx"] + m["w"] - 6 * u and r.top() > m["by"] + 6 * u and r.bottom() < m["by"] + m["h"] - 6 * u
            hit = 0.0
            for q in taken + [o[2] for o in out]:
                ix = skia.Rect(r.left(), r.top(), r.right(), r.bottom())
                if ix.intersect(q):
                    hit += ix.width() * ix.height() + 1e4
            sc_ = hit * 10 + (0 if inside else 1e7) + n_ * 50
            if sc_ < bs:
                best, bs = (sx, sy, r), sc_
        out.append(best)
    m["plates"] = out
    return out


def draw_map(c, i, t):
    """A map beat: the type map wipes on, then its zones, pins, routes and labels arrive one after another. A map that
    follows a map takes over its plate: the geography zooms from one view to the next, with no fade to black."""
    m = map_frame(i)
    v, u0 = m["v"], m["u"]
    u = u0 * (1.7 if VERT else 1.0)
    vecp, glyp, lit = map_pics(i)
    gs = 1 - sm(abs(math.log(max(1e-6, math.sqrt(abs(map_xform(i, t)[0] * map_xform(i, t)[2]))))), math.log(1.3), math.log(2.0))   # glyphs give way while the view is magnified or shrunk
    first = i == 0 and OPEN_RESOLVED and not VERT
    sx, ox, sy, oy, role, e = map_xform(i, t)
    nxt_map = i + 1 < N and handover_in(i + 1)
    leave = 1 - sm(t, NXT(i) + 0.4, NXT(i) + 1.0) if (i < N - 1 and not nxt_map) else 1.0     # the map stays up while the camera leaves it
    if role == "in":
        am = sm(e, 0.05, 0.4)
    elif first:
        am = 1.0
    else:
        am = sm(t, S(i) - 1.6, S(i) - 0.6) * leave
    back = am
    fin = 1.0
    if role == "out":
        fin = 1 - sm(e, 0.1, 0.4)                                  # inside the incoming map's box the old one gives way; outside it stays
    if am <= 0:
        return
    bx, by, w, h = m["bx"], m["by"], m["w"], m["h"]
    box = skia.Rect.MakeXYWH(bx, by, w, h)
    rv = 1.0 if (first or role == "in" or handover_in(i)) else sm(t, S(i) - 1.2, S(i) + 0.6)    # the map is typed on, left to right, behind a lit edge
    if role != "in":                                               # the plate: the sea's colour, which also keeps the lattice out
        c.drawRect(skia.Rect.MakeXYWH(bx - 40 * u0, by - 30 * u0, w + 80 * u0, h + 60 * u0), skia.Paint(Color=col(BG, 0.72 * back)))
        c.drawRect(box, skia.Paint(Color=col(SEA, 0.95 * back)))
    mat = skia.Matrix.MakeAll(sx, 0, ox, 0, sy, oy, 0, 0, 1)
    c.saveLayerAlpha(skia.Rect.MakeXYWH(bx - 600, by - 400, w + 1200, h + 800), int(255 * am))
    ex = bx + (w + 240 * u0) * rv - 120 * u0
    ph = ((t - S(i)) % 7.0) / 7.0                                      # then a slow sweep of light crosses the coast every 7 s
    band = ([(ex - 140 * u0, ex)] if rv < 1 else []) + [(bx - 300 * u0 + ph * (w + 600 * u0), bx - 300 * u0 + ph * (w + 600 * u0) + 220 * u0)]
    passes = [(None, 1.0)]
    if role == "out":
        jm = map_frame(i + 1)
        jx, jox, jy, joy, _, _ = map_xform(i + 1, t)
        jr = skia.Rect.MakeXYWH(jx * jm["bx"] + jox, jy * jm["by"] + joy, jx * jm["w"], jy * jm["h"])
        passes = [((jr, skia.ClipOp.kDifference), 1.0), ((jr, skia.ClipOp.kIntersect), fin)]
    for clip_, pa_ in passes:
        if pa_ <= 0:
            continue
        c.save()
        c.clipRect(box)
        if clip_:
            c.clipRect(clip_[0], clip_[1])
        c.concat(mat)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(bx - 50, by - 50, ex, by + h + 50))
        c.drawPicture(vecp, None, skia.Paint(Color=col("#FFFFFF", pa_)))
        if gs > 0:
            c.drawPicture(glyp, None, skia.Paint(Color=col("#FFFFFF", pa_ * gs)))
        c.restore()
        for x0, x1 in band:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(max(bx - 50, x0), by - 50, min(ex, x1), by + h + 50))
            c.drawPicture(lit, None, skia.Paint(Color=col("#FFFFFF", (0.55 if x1 == ex else 0.32) * pa_ * max(gs, 0.3))))
            c.restore()
        c.restore()
    # the ruler: longitudes under the map, latitudes down its left side, and the source line beneath (on the plate, not the geography)
    rk = sm(e, 0.6, 1.0) if role == "in" else (1 - sm(e, 0.0, 0.4)) if role == "out" else 1.0
    if rk > 0:
        L0, A0, L1, A1 = m["view"]
        fr = mono(29 * u)                                              # readable on a phone (9 Oct)
        ink = skia.Paint(Color=col(INK, 0.5 * rk), AntiAlias=True, StrokeWidth=1.3 * u0)
        ra = sm(t, S(i) - 0.4, S(i) + 0.6) if not (first or handover_in(i)) else 1.0
        yb = by + h + 12 * u0
        c.drawLine(bx, yb, bx + w * ra, yb, skia.Paint(Color=col(INK, 0.3 * rk), AntiAlias=True, StrokeWidth=1.2 * u0))
        st = nice_step(L1 - L0, 7 if not VERT else 4)
        for lo in np.arange(math.ceil(L0 / st) * st, L1 + 1e-9, st):
            x, _ = m["proj"](lo, 0)
            if x > bx + w * ra:
                break
            c.drawLine(x, yb, x, yb + 12 * u0, ink)
            text(c, deg(((lo + 180) % 360) - 180, "E", "W", st < 1), x, yb + 40 * u, fr, DIM, ra * rk, 0.5 * u, "center")
        st = nice_step(A1 - A0, 4 if not VERT else 6)
        for la in np.arange(math.ceil(A0 / st) * st, A1 + 1e-9, st):
            _, y = m["proj"](0, la)
            c.drawLine(bx - 22 * u0, y, bx - 8 * u0, y, ink)
            text(c, deg(la, "N", "S", st < 1), bx - 30 * u0, y + 7 * u, fr, DIM, ra * rk, 0.5 * u, "right")
        if v.get("caption"):
            cap = typed(v["caption"], t, S(i) + 0.3, 45.0) if not (first or handover_in(i)) else v["caption"]
            c.drawRect(skia.Rect.MakeXYWH(bx, yb + 62 * u, 6 * u, 24 * u), skia.Paint(Color=col(CYAN, rk)))
            text(c, cap, bx + 18 * u, yb + 82 * u, mono(22 * u), DIM, rk, 0.8 * u)
    a, t0 = held(i, t, (ho_window(i)[1] - 0.4) if handover_in(i) else None)
    if first:
        t0 -= 10.0                                                 # frame 0 is the thumbnail: everything already drawn
    a *= leave if a > 0 else 0
    if a <= 0:
        c.restore()
        return
    c.save()
    c.concat(mat)
    c.save()
    c.clipRect(box)
    dur = max(2.0, E(i) - t0)
    for k_, zone in enumerate(v.get("zones", [])):                     # a zone: a lit hatch inside a hairline
        za = a * sm(t, t0 + 0.2 + 0.4 * k_, t0 + 1.0 + 0.4 * k_)
        if za <= 0:
            continue
        zp = skia.Path()
        zp.addPoly([skia.Point(*m["proj"](lo, la)) for lo, la in zone], True)
        R = zp.computeTightBounds()
        sweep = R.left() + (R.width() + 2) * spring((t - t0 - 0.2 - 0.4 * k_) / 1.2)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(R.left() - 4, R.top() - 4, sweep + 4, R.bottom() + 4))
        c.drawPath(zp, skia.Paint(Color=col(CYAN, 0.10 * za), AntiAlias=True))
        c.save()
        c.clipPath(zp, skia.ClipOp.kIntersect, True)
        gap = 14 * u0
        off = (t * 10 * u0) % gap                                      # the hatch drifts, slowly
        hp = skia.Paint(Color=col(CYAN, 0.42 * za), AntiAlias=True, StrokeWidth=1.6 * u0)
        xx = R.left() - R.height() - gap + off
        while xx < R.right() + gap:
            c.drawLine(xx, R.bottom(), xx + R.height(), R.top(), hp)
            xx += gap
        c.restore()
        c.drawPath(zp, skia.Paint(Color=col(CYAN, 0.85 * za), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0 * u0))
        c.restore()
    for k_, rt in enumerate(v.get("routes", [])):                     # a route draws itself on, then a light runs along it
        if len(rt) < 2:
            continue
        ts, td = t0 + 0.4 + 0.6 * k_, min(3.2, max(1.4, dur * 0.5))
        pr = spring((t - ts) / td)
        if pr <= 0:
            continue
        if "rp" not in m:
            m["rp"] = {}
        if k_ not in m["rp"]:
            pp = route_path(m, rt)
            m["rp"][k_] = (pp, skia.PathMeasure(pp, False))
        pp, pm = m["rp"][k_]
        Lr = pm.getLength()
        seg = skia.Path()
        pm.getSegment(0, Lr * pr, seg, True)
        g = glow(CYAN, 0.5 * a, 12 * u0)
        g.setStyle(skia.Paint.kStroke_Style)
        g.setStrokeWidth(7 * u0)
        c.drawPath(seg, g)
        c.drawPath(seg, skia.Paint(Color=col(CYAN, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6 * u0, StrokeCap=skia.Paint.kRound_Cap))
        if pr < 0.999:
            hd = pm.getPosTan(Lr * pr)[0]
            c.drawCircle(hd.x(), hd.y(), 16 * u0, glow(INK, 0.8 * a, 12 * u0))
            c.drawCircle(hd.x(), hd.y(), 5.5 * u0, skia.Paint(Color=col(INK, a), AntiAlias=True))
        else:
            q = ((t - ts - td) % 3.0) / 3.0                             # a pulse runs the route every 3 s
            hd = pm.getPosTan(Lr * q)[0]
            pa = a * math.sin(math.pi * q)
            c.drawCircle(hd.x(), hd.y(), 14 * u0, glow(INK, 0.7 * pa, 10 * u0))
            c.drawCircle(hd.x(), hd.y(), 4.5 * u0, skia.Paint(Color=col(INK, pa), AntiAlias=True))
    for k_, (lo, la) in enumerate(v.get("pins", [])):                 # a pin: a lit point and rings going out from it
        pa = a * sm(t, t0 + 0.1 + 0.3 * k_, t0 + 0.5 + 0.3 * k_)
        if pa <= 0:
            continue
        x, y = m["proj"](lo, la)
        for ph_ in (0.0, 0.5):
            q = ((t - t0 + ph_ * 1.8) % 1.8) / 1.8
            c.drawCircle(x, y, (12 + 46 * q) * u0, skia.Paint(Color=col(CYAN, 0.75 * pa * (1 - q)), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2 * u0))
        c.drawCircle(x, y, 20 * u0, glow(CYAN, 0.6 * pa, 12 * u0))
        c.drawCircle(x, y, 8 * u0, skia.Paint(Color=col(CYAN, pa), AntiAlias=True))
    c.restore()                                                    # labels may lean out of the plate; the rest may not
    labels = v.get("labels", [])
    stag = min(1.1, dur * 0.55 / max(1, len(labels)))
    ft, fs = sans(50 * u), mono(31 * u)
    for k_, ((lo, la, title, sub), (sx, sy, r)) in enumerate(zip(labels, map_labels(i))):   # a label: a point, a leader, a plate
        tl = t0 + 0.5 + stag * k_
        la_ = a * sm(t, tl, tl + 0.45)
        if la_ <= 0:
            continue
        la_ *= on_screen(r.left(), r.right(), r.bottom())
        x, y = m["proj"](lo, la)
        grow = spring((t - tl) / 0.7)
        c.drawCircle(x, y, 5.5 * u0, skia.Paint(Color=col(INK, la_), AntiAlias=True))
        c.drawCircle(x, y, 14 * u0, skia.Paint(Color=col(INK, 0.6 * la_), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4 * u0))
        if sy:                                                      # the leader: from the ring to the plate's near edge
            x_end, y_end = x, (r.top() if sy > 0 else r.bottom())
        else:
            x_end, y_end = (r.left() if sx > 0 else r.right()), y
        dl = math.hypot(x_end - x, y_end - y) or 1.0
        xb, yb_ = x + (x_end - x) / dl * 14 * u0, y + (y_end - y) / dl * 14 * u0
        c.drawLine(xb, yb_, xb + (x_end - xb) * grow, yb_ + (y_end - yb_) * grow, skia.Paint(Color=col(INK, 0.85 * la_), AntiAlias=True, StrokeWidth=1.4 * u0))
        pa = la_ * sm(t, tl + 0.25, tl + 0.6)
        if pa <= 0:
            continue
        c.drawRect(r, skia.Paint(Color=col(BG, 0.92 * pa)))
        c.drawRect(skia.Rect.MakeXYWH(r.left() if sx > 0 else r.right() - 3 * u0, r.top(), 3 * u0, r.height()), skia.Paint(Color=col(CYAN, pa)))
        tx, al = (r.left() + 18 * u, "left") if sx > 0 else (r.right() - 18 * u, "right")
        text(c, title, tx, r.top() + 54 * u, ft, INK, pa, 0.0, al)
        if sub:
            st_ = typed(sub, t, tl + 0.5, 40.0)
            if al == "right":                                              # typed from the left even when set right
                tx_ = tx - (fs.measureText(sub) + 0.5 * u * (len(sub) - 1))
                text(c, st_, tx_, r.top() + 94 * u, fs, CYAN, pa, 0.5 * u)
            else:
                text(c, st_, tx, r.top() + 94 * u, fs, CYAN, pa, 0.5 * u)
    c.restore()
    c.restore()


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
        if p["kind"] == "map":                                      # a map holds still and pushes slowly toward what it is about
            fx, fy = map_frame(n)["focus"]
            if n == 0 and OPEN_RESOLVED:                            # frame 0 is already framed: the thumbnail, ruler and all
                k.append((0.0, (x, y, z)))
                k.append((a + 1.4, (x, y, z * 1.02)))
            elif n == 0:
                k.append((0.0, (x, y + 10, z * 1.12)))
                k.append((a + 1.4, (x, y, z)))
            else:
                far = math.hypot(x - k[-1][1][0], y - k[-1][1][1])
                k.append((a, (x, y, z * 0.97), 0.0 if handover_in(n) else 0.35 + 0.25 * min(1.0, far / 6000)))
            k.append((b, (x + fx * 0.14, y + fy * 0.14, z * 1.08)))
            continue
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
    t = min(max(t, KEYS[1][0] if OPEN_RESOLVED and len(KEYS) > 2 else KEYS[0][0]), KEYS[-1][0])     # a resolved open starts already arrived at its first place (10 Oct: frame 0 was mid-move)
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
    if CHART:                                                       # the chart look: no typing, no block cursor; the line fades with its card
        return s
    n = int(max(0.0, t - t0) * cps)
    return s[:n] + ("█" if 0 < n < len(s) else "")


CAM = [0.0, 0.0, 1.0]                         # the frame's camera, for type that must know where it is on screen


def on_screen(x0, x1, y1):
    """1 when a block is wholly inside the frame and above the caption band, falling to 0 as it nears an edge."""
    cx, cy, z = CAM
    l, r, bot = (x0 - cx) * z + W / 2 - SHIFT, (x1 - cx) * z + W / 2 - SHIFT, (y1 - cy) * z + H / 2 - RAISE
    if CHART and not VERT:                                          # the chart look: type slides through the frame with its card
        return 1 - sm(bot, CAP_TOP - 40, CAP_TOP)
    return sm(l, 14, 70) * (1 - sm(r, W - 70 - 2 * SHIFT, W - 14 - 2 * SHIFT)) * (1 - sm(bot, CAP_TOP - 40, CAP_TOP))


def held(i, t, t0=None):
    """A place's type: on once the camera has arrived, off as it leaves."""
    t0 = S(i) + 0.1 if t0 is None else max(t0, S(i) + 0.1)
    off = min(NXT(i) - 0.2, E(i) + 0.7 + HOLD.get(B[i]["id"], 0.0)) if i < N - 1 else TOTAL + 9     # the last line holds to the end
    if VERT and S(i) - SHORT["t0"] < 0.5:                            # a Short opens with its first card already up
        return 1 - sm(t, off - 0.3, off), t0
    if i == 0 and OPEN_RESOLVED and not VERT:                         # a film can open on its first picture already up
        return 1 - sm(t, off - 0.3, off), t0
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
    maxw = min(maxw, (W - (400 if VERT else 200)) / max(CAM[2], 1e-6))      # never wider than the frame it is drawn in
    f = sans(size)
    while f.measureText(s) > maxw and size > 12:
        size -= 3
        f = sans(size)
    return f, size


def block(c, x0, top, w, h, a, pad=36):
    plate(c, x0 - pad, top - pad * 0.6, w + 2 * pad, h + pad * 1.2, a)


def last_map(i):
    """The map a beat belongs to: itself, else the latest map before it, else the first map after it."""
    for j in list(range(i, -1, -1)) + list(range(i + 1, N)):
        if B[j]["vis"][0] == "map":
            return j
    return None


def fmt_ll(lon, lat, d=2):
    return f"{abs(lat):0{3 + d}.{d}f}°{'N' if lat >= 0 else 'S'}   {abs(lon):0{4 + d}.{d}f}°{'E' if lon >= 0 else 'W'}"


def card_tag(i):
    """A card's reference in the chart look: its chapter.beat number and the place it is about (the map it sits among)."""
    kind = dict(num="FIG", split="CMP", words="NOTE", quote="NOTICE", list="LOG", tl="TIMELINE").get(B[i]["vis"][0], "REF")
    bi = sum(1 for j in range(i) if B[j]["floor"] == B[i]["floor"])
    j = last_map(i)
    if j is None:
        return f"{kind} {B[i]['floor'] + 1:02d}.{bi + 1:02d}"
    L0, A0, L1, A1 = map_frame(j)["view"]
    return f"{kind} {B[i]['floor'] + 1:02d}.{bi + 1:02d}  ·  " + fmt_ll((L0 + L1) / 2, (A0 + A1) / 2, 1)


def chart_frame(c, r, a, tag, u, divider=None):
    """A card as a plate on the instrument: a hairline frame, cyan corner ticks, a small reference tag."""
    if a <= 0:
        return
    c.drawRect(r, skia.Paint(Color=col(BG, 0.55 * a)))
    c.drawRect(r, skia.Paint(Color=col(INK, 0.2 * a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3 * u))
    tk, pt = 34 * u, skia.Paint(Color=col(CYAN, a), AntiAlias=True, StrokeWidth=2.6 * u)
    for x, y, dx, dy in ((r.left(), r.top(), 1, 1), (r.right(), r.top(), -1, 1), (r.left(), r.bottom(), 1, -1), (r.right(), r.bottom(), -1, -1)):
        c.drawLine(x, y, x + dx * tk, y, pt)
        c.drawLine(x, y, x, y + dy * tk, pt)
    if divider is not None:
        c.drawLine(divider, r.top() + 60 * u, divider, r.bottom() - 60 * u, skia.Paint(Color=col(INK, 0.2 * a), AntiAlias=True, StrokeWidth=1.3 * u))
    fm = mono(22 * u)
    text(c, tag, r.left() + 26 * u, r.top() + 44 * u, fm, DIM, a, 1.0 * u)
    for k_ in range(9):                                             # a hairline scale along the bottom edge, like a chart's border
        x = r.right() - 30 * u - k_ * 22 * u
        c.drawLine(x, r.bottom() - 4 * u, x, r.bottom() - (16 if k_ % 4 == 0 else 9) * u, skia.Paint(Color=col(INK, 0.3 * a), AntiAlias=True, StrokeWidth=1.2 * u))


def held_chart(i, t):
    """The chart look: a card is up before the camera arrives and stays as it leaves, so it slides through the frame (no dip to black)."""
    t0 = S(i) - 0.5                                                # its type is already set as it slides in
    if i == N - 1:
        return sm(t, S(i) - 0.9, S(i) - 0.45), t0
    return sm(t, S(i) - 0.9, S(i) - 0.45) * (1 - sm(t, NXT(i) + 0.35, NXT(i) + 0.8)), t0


def world_type(c, t):
    n = now(t)
    for i in range(max(0, n - 1), min(N, n + 2)):
        p, v = PL[i], B[i]["vis"]
        k, x, y, u = p["kind"], p["x"], p["y"], p["ww"] / 2300.0 * (1.7 if VERT else 1.0)      # a Short's type is set much larger: a phone is small
        FR = (W - (400 if VERT else 200)) / max(CAM[2], 1e-6)       # the widest a block may be in this frame
        if k == "map":
            draw_map(c, i, t)
            continue
        a, t0 = held_chart(i, t) if CHART else held(i, t)
        if a <= 0:
            continue
        a_fr = a
        fr_rect, fr_div = None, None
        dur = max(1.0, E(i) - t0)
        if False and k in ("img", "clip") and HAS_PHOTO and len(v) < 3:     # (moved to the screen, 8 Oct: in the world it fell under the captions or the rail)
            tg = "ILLUSTRATION  ·  AI-GENERATED"
            tx, ty = x - p["ww"] * 0.40, y - p["ww"] * 0.235    # top left of the picture: lower down, the caption plate hid it
            fg = mono(30 * u)                                       # large enough to read at 1080p (final critic: 11 px was not)
            ta = a * on_screen(tx - 20 * u, tx + fg.measureText(tg) + 80 * u, ty + 20 * u)
            if ta > 0:
                c.drawRect(skia.Rect.MakeXYWH(tx - 18 * u, ty - 38 * u, fg.measureText(tg) + 0.5 * u * len(tg) + 40 * u, 54 * u), skia.Paint(Color=col(BG, 0.85 * ta)))
                text(c, tg, tx, ty, fg, INK, 0.85 * ta, 0.5 * u)
        if k in ("img", "clip") and RESOLVE > 0:                  # an illustration resolves most of the way into the picture; the characters stay as its grain
            fr = pic(i)
            rr = a * (1.0 if i == 0 and OPEN_RESOLVED else sm(t, S(i) + 0.8, S(i) + 2.0)) * RESOLVE
            if fr and rr > 0:
                hh = p["ww"] * 9 / 16
                im = still(i, 0 if len(fr) == 1 else _pingpong(int(t * 12), len(fr)))
                c.drawImageRect(im, skia.Rect.MakeXYWH(x - p["ww"] / 2, y - hh / 2, p["ww"], hh), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(Color=col("#FFFFFF", rr)))
        if k == "photo":                                          # the characters resolve into the photograph itself
            _, (img, fx, fy, fw, fh) = photo(v[1])
            hh = p["ww"] * 9 / 16
            rr = a * (1.0 if i == 0 and OPEN_RESOLVED else sm(t, S(i) + 1.3, S(i) + 2.6))
            R = skia.Rect.MakeXYWH(x - p["ww"] / 2 + fx * p["ww"], y - hh / 2 + fy * hh, fw * p["ww"], fh * hh)
            if rr > 0:
                c.drawImageRect(img, R, skia.SamplingOptions(skia.CubicResampler.Mitchell()), skia.Paint(Color=col("#FFFFFF", 0.94 * rr)))
                c.drawRect(R, skia.Paint(Color=col(INK, 0.5 * rr), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2 * u))
            if len(v) > 3:
                crt = v[3] if v[3].upper().startswith(("PHOTO", "IMAGE", "FOTO")) else UI["photo"] + v[3]     # no "PHOTO · PHOTO:" when the credit already says it
                cr = typed(crt, t, 0.0 if i == 0 and OPEN_RESOLVED else t0 + 1.4, 40.0)                # the credit sits on the picture's top left, clear of the captions
                fc_ = mono(21 * u)
                c.drawRect(skia.Rect.MakeXYWH(R.left() + 10 * u, R.top() + 10 * u, fc_.measureText(crt) + 0.5 * u * len(crt) + 44 * u, 38 * u), skia.Paint(Color=col(BG, 0.82 * rr / max(RESOLVE, 0.01) if False else 0.82 * a)))
                text(c, cr, R.left() + 24 * u, R.top() + 36 * u, fc_, INK, a, 0.5 * u)
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
                X, Y = x - f.measureText(v[2]) / 2, y - p["ww"] * 0.2 - 60 * u + 150 / max(CAM[2], 1e-6)     # clear of the headline band, which now sits lower
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
            if CHART:
                hw = max(wd, 900 * u) / 2 + 100 * u
                chart_frame(c, skia.Rect.MakeLTRB(x - hw, top - 110 * u, x + hw, top + len(lines) * lh + 60 * u), a_fr, card_tag(i), u)
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
                if CHART:
                    hw = max(wd0, mono(34 * u).measureText(v[2]), 900 * u) / 2 + 110 * u
                    chart_frame(c, skia.Rect.MakeLTRB(x - hw, y - 270 * u, x + hw, y + 400 * u), a_fr, card_tag(i), u)
                text(c, v[1], x - wd0 / 2, y + 60 * u, f, INK, a0)
            fm = mono(34 * u)
            s_ = v[2]
            while fm.measureText(s_) > min(1900 * u, FR):
                fm = mono(fm.getSize() - 1)
            wd = fm.measureText(s_)
            Y = y + 330 * u
            a *= on_screen(x - wd / 2 - 30 * u, x + wd / 2 + 30 * u, Y + 20 * u)
            if a > 0:
                block(c, x - wd / 2, Y - 34 * u, wd, 44 * u, a, 24 * u)
                text(c, typed(s_, t, t0 + 0.2), x - wd / 2, Y, fm, CYAN, a)
        elif k == "split":
            if CHART:
                chart_frame(c, skia.Rect.MakeLTRB(x - 0.45 * p["ww"], y - 190 * u, x + 0.45 * p["ww"], y + 320 * u), a_fr, card_tag(i), u, divider=x)
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
            qw = min(1560 * u, (W - (560 if VERT else 200)) / max(CAM[2], 1e-6))      # a Short's card, with its mark and plate, must sit wholly inside the frame or the edge gate flickers it
            lines = wrap(v[1], f, qw)
            lh = 100 * u
            while len(lines) > (7 if VERT else 6):
                f = sans(f.getSize() * 0.9)
                lh *= 0.9
                lines = wrap(v[1], f, qw)
            wd = max(f.measureText(s_) for s_ in lines)
            hgt = len(lines) * lh + 70 * u
            X, top = x - wd / 2 + (55 * u if VERT else 0), y - hgt / 2 - (230 if VERT else 80) * u      # a Short's captions sit high: a tall quote must clear them
            a *= on_screen(X - 150 * u, X + wd + 40 * u, top + hgt + 30 * u)
            if a > 0:
                if CHART:                                       # a notice slip, not a pull-quote: no big mark
                    chart_frame(c, skia.Rect.MakeLTRB(X - 130 * u, top - 120 * u, X + wd + 90 * u, top + hgt + 70 * u), a_fr, card_tag(i), u)
                    c.drawRect(skia.Rect.MakeXYWH(X - 50 * u, top + 20 * u, 4 * u, len(lines) * lh - 10 * u), skia.Paint(Color=col(CYAN, a)))
                else:
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
            cap = (0.40 * p["ww"] - (70 * u if title else 0)) / (len(items) * 1.55)     # a long list shrinks to fit above the captions (9 Oct: 8 rows were hidden by on_screen)
            if size > cap:
                f, size = fit_sans(max(items, key=len), cap, 1700 * u)
            lh = size * 1.55
            wd = max(f.measureText(s_) for s_ in items)
            hgt = len(items) * lh + (70 * u if title else 0)
            X, top = x - wd / 2, y - hgt / 2 - 80 * u
            a *= on_screen(X - 80 * u, X + wd + 40 * u, top + hgt + 20 * u)
            if a > 0:
                if CHART:
                    chart_frame(c, skia.Rect.MakeLTRB(X - 110 * u, top - 64 * u, X + wd + 90 * u, top + hgt + 50 * u), a_fr, card_tag(i), u)
                else:
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
            span = min(1740 * u, FR)
            X0, Y = x - span / 2, y - 40 * u
            a *= on_screen(X0 - 60 * u, X0 + span + 60 * u, Y + 260 * u)
            if a > 0:
                if CHART:
                    chart_frame(c, skia.Rect.MakeLTRB(X0 - 70 * u, Y - 270 * u, X0 + span + 70 * u, Y + 300 * u), a_fr, card_tag(i), u)
                else:
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
    i_ = now(t)
    if (HAS_PHOTO or ILLUS) and B[i_]["vis"][0] in ("img", "clip") and (len(B[i_]["vis"]) < 3 or ILLUS):      # in a film that also shows real photographs, an illustration says so, where it can be read
        ta = held(i_, t)[0]
        if ta > 0:
            tg, fg = UI["illus"], mono(21)
            c.drawRect(skia.Rect.MakeXYWH(56, 104, fg.measureText(tg) + 0.6 * len(tg) + 30, 40), skia.Paint(Color=col(BG, 0.85 * ta)))
            c.drawRect(skia.Rect.MakeXYWH(56, 104, 3, 40), skia.Paint(Color=col(CYAN, ta)))
            text(c, tg, 72, 131, fg, INK, 0.9 * ta, 0.6)
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

    if CHART:
        chart_header(c, t, cx, cy, z, cur, prog, NC)
    else:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 104), skia.Paint(Color=col(BG, 0.78)))
        chan = SC.TAG.split("·")[0].strip()
        text(c, chan, 70, 62, mono(20), DIM, 1.0, 1.0)
        x0 = max(300, 70 + mono(20).measureText(chan) + len(chan) + 44)    # a long channel name pushes the rail right (9 Oct: THE HOUSEHOLD LEDGER ran into box 01)
        rail(x0, W - 70, 56, 46, 26, 1.0, 14, False)
        step = (W - 70 - x0 - 46) / max(1, NC - 1)
        name = SC.CHAPTERS[cur]["title"] or UI["open"]
        nw = mono(17).measureText(name) + 0.6 * (len(name) - 1)
        text(c, name, min(max(x0 + cur * step, x0), W - 70 - nw), 94, mono(17), CYAN, 1.0, 0.6)
    for i, b in enumerate(B):                                          # the chapter's name, while the camera crosses to it
        if b["first"] and b["title"] and abs(t - S(i)) < 4:
            a = sm(t, S(i) - CHAPTER_GAP + 1.0, S(i) - CHAPTER_GAP + 1.35) * (1 - sm(t, S(i) - 0.55, S(i) - 0.15))
            if a > 0:
                f, size = fit_sans(b["title"], 150, W - 360)
                wd = f.measureText(b["title"])
                c.drawRect(skia.Rect.MakeXYWH(0, H / 2 - 190, W, 400), skia.Paint(Color=col(BG, 0.97 * min(1.0, a * 2.5))))        # a band, up before the name: nothing behind reads through a chapter's name
                for yy in (H / 2 - 190, H / 2 + 210):
                    c.drawLine(0, yy, W, yy, skia.Paint(Color=col(INK, 0.14 * a), AntiAlias=True, StrokeWidth=1))
                text(c, f"{UI['chapter']} {b['floor'] + 1:02d}", W / 2 - wd / 2, H / 2 - 116, mono(28), CYAN, a, 2.0)
                text(c, b["title"], W / 2 - wd / 2, H / 2 + 24, f, INK, a)
                if CHART:                                       # a ruled line with the chapter's place on it, not numbered boxes
                    c.drawLine(W / 2 - wd / 2, H / 2 + 80, W / 2 + wd / 2, H / 2 + 80, skia.Paint(Color=col(INK, 0.25 * a), AntiAlias=True, StrokeWidth=1.2))
                    c.drawLine(W / 2 - wd / 2, H / 2 + 80, W / 2 - wd / 2 + wd * (b["floor"] + 1) / NC, H / 2 + 80, skia.Paint(Color=col(CYAN, a), AntiAlias=True, StrokeWidth=2.4))
                    text(c, f"{b['floor'] + 1:02d} / {NC:02d}", W / 2 + wd / 2, H / 2 + 124, mono(22), DIM, a, 1.0, "right")
                else:
                    rail(200, W - 200, H / 2 + 132, 96, 54, a, 24, True)
    a = sm(t, E(N - 1) + 1.2, E(N - 1) + 2.0)
    if a > 0:                                                       # the sign-off, with room left for end-screen elements above it
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - 430, H - 226, 860, 150), skia.Paint(Color=col(BG, 0.9 * a)))
        text(c, CHANNEL, W / 2, H - 150, sans(64), INK, a, 6.0, align="center")
        text(c, (UI["tagline"] if CHANNEL in ("THE CURVE", "LA CURVA", "CURVAEXPLICA") else "") + UI["sources"], W / 2, H - 100, mono(24), CYAN, a, 1.0, align="center")
    captions(c, t, n)


def chart_header(c, t, cx, cy, z, cur, prog, NC):
    """The chart look's header: the channel on the left; the chapter and a live position readout of the camera's map centre
    on the right, like a navigation instrument; a hairline with the film's progress along it."""
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 86), skia.Paint(Color=col(BG, 0.82)))
    c.drawLine(70, 86, W - 70, 86, skia.Paint(Color=col(INK, 0.16), AntiAlias=True, StrokeWidth=1))
    c.drawLine(70, 86, 70 + (W - 140) * min(1.0, prog / max(1, NC)), 86, skia.Paint(Color=col(CYAN, 0.9), AntiAlias=True, StrokeWidth=2))
    c.drawRect(skia.Rect.MakeXYWH(70, 40, 10, 10), skia.Paint(Color=col(CYAN)))
    chan = SC.TAG.split("·")[0].strip()
    text(c, chan, 94, 52, mono(21), INK, 0.9, 1.5)
    i_ = now(t)
    j = i_ if B[i_]["vis"][0] == "map" else last_map(i_)
    if j is not None:
        if B[i_]["vis"][0] == "map":
            lon, lat = map_geo_at(j, t, cx + SHIFT / z, cy + RAISE / z)
        else:
            L0, A0, L1, A1 = map_frame(j)["view"]
            lon, lat = (L0 + L1) / 2, (A0 + A1) / 2
        rd = fmt_ll(((lon + 180) % 360) - 180, lat, 2)
    else:
        rd = "--"
    fr = mono(21)
    rw = sum(fr.measureText(ch) + 1.0 for ch in rd)
    text(c, rd, W - 70, 52, fr, INK, 0.95, 1.0, "right")
    name = SC.CHAPTERS[cur]["title"] or UI["open"]
    text(c, f"{cur + 1:02d}  {name}", W - 70 - rw - 36, 52, mono(18), CYAN, 1.0, 1.2, "right")
    c.drawLine(W - 70 - rw - 18, 34, W - 70 - rw - 18, 58, skia.Paint(Color=col(INK, 0.25), AntiAlias=True, StrokeWidth=1))


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
        if CHART and not VERT:                                      # the chart look: set left, on a plain plate with a cyan rule; every word in full
            X0 = 190
            pl = skia.Rect.MakeXYWH(X0 - 30, y0 - CL - 2, wmax + 60, len(lines) * CL + 28)
            c.drawRect(pl, skia.Paint(Color=col(BG, 0.94 * k)))
            c.drawRect(skia.Rect.MakeXYWH(pl.left(), pl.top(), 3, pl.height()), skia.Paint(Color=col(CYAN, k)))
            for i, s in enumerate(lines):
                text(c, s, X0, y0 + i * CL, f, INK, k)
            continue
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
HEAD = 300                                    # a Short's headline band: channel name at 250, first line at 330


def short_screen(c, t, n):
    """A Short's furniture: the headline up top, captions above the app's own buttons, an end card to the full film."""
    f = sans(60)
    lines = wrap(SHORT["headline"], f, W - 260)
    c.drawRect(skia.Rect.MakeXYWH(0, 0, W, HEAD + len(lines) * 70), skia.Paint(Color=col(BG, 0.9)))
    text(c, CHANNEL, 75, HEAD - 50, mono(26), CYAN, 1.0, 3.0)      # all of it below the top 12%, which the app covers
    for i, s_ in enumerate(lines):
        text(c, s_, 75, HEAD + 30 + i * 70, f, INK)
    e = sm(t, SHORT["t1"] - 3.4, SHORT["t1"] - 3.1) if SHORT["film"] else 0.0
    if e > 0:
        c.drawRect(skia.Rect.MakeXYWH(0, HEAD + len(lines) * 70, W, H), skia.Paint(Color=col(BG, e)))
        text(c, UI["watch"], W / 2, H / 2 - 150, mono(30), CYAN, e, 3.0, align="center")
        ff, _ = fit_sans(SHORT["film"].upper(), 92, W - 140)
        text(c, SHORT["film"].upper(), W / 2, H / 2 - 30, ff, INK, e, align="center")
        c.drawRect(skia.Rect.MakeXYWH(W / 2 - 60, H / 2 + 20, 120, 7), skia.Paint(Color=col(CYAN, e)))
        text(c, UI["on"] + CHANNEL + UI["link"], W / 2, H / 2 + 110, mono(26), INK, e, 1.0, align="center")
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
    a = (1.0 if OPEN_RESOLVED else sm(t, -0.2, 0.35)) * (1 - sm(t, TOTAL - 1.4, TOTAL - 0.1))     # a film that opens resolved has no fade-in: frame 0 is the thumbnail
    if VERT:
        a = (1 - sm(t, SHORT["t1"] - 0.35, SHORT["t1"])) if SHORT["film"] else 1.0     # a standalone Short loops: no fade to black at the seam
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
        t0, t1 = max(0.0, S(ids.index(a_id)) - 0.15), E(ids.index(b_id)) + 0.5 + (3.4 if film else 0.3)      # a standalone Short (film "") has no end card: it loops
        SHORT.update(t0=t0, t1=t1, headline=head, film=film)
        os.makedirs(os.path.join(FILM, "shorts"), exist_ok=True)
        pic_, out = os.path.join(BUILD, f"short_{name}_pic.mp4"), os.path.join(FILM, "shorts", f"short_{name}.mp4")
        encode(t0, t1, pic_, "1080:1920")
        d = t1 - t0
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pic_, "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", mp4, "-map", "0:v", "-map", "1:a",
                        "-af", f"afade=t=in:d=0.25,afade=t=out:st={d - (2.4 if film else 0.06):.2f}:d={2.3 if film else 0.05}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
        print(out, round(d, 1), "s")
    elif cmd == "times":
        for ln in LINES:
            print(f"{ln['start']:7.2f} {ln['end']:7.2f}  {ln['id']:10s} {B[ln['i']]['vis'][0]}")


if __name__ == "__main__":
    main()
