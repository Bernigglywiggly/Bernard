"""THE CURVE · LONG-FORM: the engine (3 Oct 2026, the user: "i need daily uploads from 1st channel ... make 5 day
backlog"). A film is a folder with script.py (CHAPTERS of beats: spoken text + one visual each), shots.py (the AI
pictures, ../assets.py) and the narration takes in src/. Everything else is made here, in the house look of the short
films (engine.look): pictures and big type turned into characters, a turquoise glow on black, crisp typed labels in
gold and white, word-by-word captions, the film's name bottom left. House, garage and deep-house beds, one per chapter.

    python3 kit.py <film> vo                 # src/vo_XX.wav + Whisper src/words_XX.json -> build/voice.wav, words.json, chapters.json
    python3 kit.py <film> music              # one bed per chapter -> build/beds/, build/music.json
    python3 kit.py <film> frames 3 41.5 ...  # finished-look stills at those seconds -> build/qc/ (+ sheet.jpg)
    python3 kit.py <film> render [seg ...]   # chapters 4 at a time -> build/seg_XX.mp4; then mix, join, deliver -> out/<name>_1080p.mp4
"""
import difflib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import types
from concurrent.futures import ProcessPoolExecutor

import cv2
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
for _p in (LAB, os.path.join(LAB, "longform"), os.path.join(LAB, "music")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import engine  # noqa: E402,F401  (paths: mograph, sfx)
import skia  # noqa: E402
import mograph as mg  # noqa: E402
from engine import look  # noqa: E402
import doc  # noqa: E402
import audio_fx as fx  # noqa: E402

W, H, FPS = 1920, 1080, 24
SR = 48000
GOLD, GLOW, WHITE, SOFT = "#F2D9A0", mg.TURQ_GLOW, mg.ON_DARK, mg.ON_DARK_SOFT
CAP, JOIN, CARD, TITLE_GAP, LEAD, TAIL = 0.85, 0.7, 3.0, 4.6, 1.0, 20.0
XF = 0.5                     # seconds two beats cross-fade (picture and labels)
ease, seg = mg.ease, mg.seg


# ---------------------------------------------------------------- the film's files
def mod(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def script_of(d):
    return mod(os.path.join(d, "script.py"), "script_" + os.path.basename(d))


def said(b):
    return b[0][1] if isinstance(b[0], tuple) else b[0]


def parts(sc, limit=1350):
    """TTS takes: each chapter's beats packed into reads of at most `limit` characters. [(chapter id, part, text)]"""
    out = []
    for ch in sc.CHAPTERS:
        cur, k = [], 0
        for b in ch["beats"]:
            s = said(b)
            if cur and len(" ".join(cur + [s])) > limit:
                out.append((ch["id"], k, " ".join(cur)))
                cur, k = [], k + 1
            cur.append(s)
        out.append((ch["id"], k, " ".join(cur)))
    return out


# ---------------------------------------------------------------- the narration
def squeeze(y, cap=CAP, thresh_db=-42.0):
    """y with every silence longer than cap cut down to cap, and the map from old seconds to new (lab/longform/lustig)."""
    hop = int(0.01 * SR)
    n = len(y) // hop
    rms = np.sqrt((y[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    silent = 20 * np.log10(rms / (np.abs(y).max() + 1e-9)) < thresh_db
    voiced = np.nonzero(~silent)[0]
    a, b = voiced[0] * hop, min(len(y), (voiced[-1] + 1) * hop)
    cuts, i = [], voiced[0]
    while i <= voiced[-1]:
        if silent[i]:
            j = i
            while j < n and silent[j]:
                j += 1
            if (j - i) * 0.01 > cap:
                half = int(cap / 2 * SR)
                cuts.append((i * hop + half, j * hop - half))
            i = j
        else:
            i += 1
    pieces, pos, marks, new = [], a, [], 0
    for c0, c1 in cuts:
        pieces.append(y[pos:c0]); marks.append((pos, new)); new += c0 - pos; pos = c1
    pieces.append(y[pos:b]); marks.append((pos, new))
    out = []
    for k, p in enumerate(pieces):
        p = p.copy()
        f = min(len(p), int(0.005 * SR))
        if k:
            p[:f] *= np.linspace(0, 1, f)
        if k < len(pieces) - 1:
            p[len(p) - f:] *= np.linspace(1, 0, f)
        out.append(p)
    lens = [len(p) for p in pieces]

    def tmap(t):
        s = t * SR
        for (o, nw), ln in zip(marks, lens):
            if s < o:
                return nw / SR
            if s <= o + ln:
                return (nw + s - o) / SR
        return (marks[-1][1] + lens[-1]) / SR
    return np.concatenate(out).astype(np.float32), tmap


def vo(d):
    sc = script_of(d)
    titles = {c["id"]: c["title"] for c in sc.CHAPTERS}
    t, chunks, words, chapters, last = LEAD, [], [], [], None
    for i, (cid, k, _) in enumerate(parts(sc)):
        y, sr = sf.read(os.path.join(d, "src", f"vo_{i:02d}.wav"), dtype="float32")
        y = y if y.ndim == 1 else y.mean(1)
        assert sr == SR, (i, sr)
        y, tmap = squeeze(y)
        if last is not None and cid != last:
            t += TITLE_GAP if len(chapters) == 1 else CARD
        elif last is not None:
            t += JOIN
        if cid != last:
            gap = 0.0 if last is None else (TITLE_GAP if len(chapters) == 1 else CARD)
            chapters.append(dict(id=cid, title=titles[cid], card=round(t - gap if last else 0.0, 3), v0=round(t, 3)))
        chunks.append((t, y))
        for w, a, b in json.load(open(os.path.join(d, "src", f"words_{i:02d}.json"))):
            words.append([w, round(t + tmap(a), 3), round(t + tmap(b), 3), cid])
        t += len(y) / SR
        chapters[-1]["v1"] = round(t, 3)
        last = cid
    total = t + TAIL
    out = np.zeros(int(total * SR) + 1, np.float32)
    for s, y in chunks:
        i = int(round(s * SR))
        out[i: i + len(y)] += y
    os.makedirs(os.path.join(d, "build"), exist_ok=True)
    sf.write(os.path.join(d, "build", "voice.wav"), out, SR, subtype="PCM_24")
    json.dump(words, open(os.path.join(d, "build", "words.json"), "w"))
    json.dump(dict(total=round(total, 3), end_voice=round(t, 3), chapters=chapters),
              open(os.path.join(d, "build", "chapters.json"), "w"), indent=1)
    print(f"voice ends {t:.1f}s ({t / 60:.1f} min), film {total:.1f}s ({total / 60:.1f} min); {len(words)} words")
    for c in chapters:
        print(f"  {c['card']:7.2f} {c['v0']:7.2f}-{c['v1']:7.2f} {c['title'] or '(cold open)'}")


# ---------------------------------------------------------------- beats on the clock
def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def beat_times(sc, words):
    """Each beat's (start, end) from the Whisper words: the script's words matched to what was heard, chapter by chapter."""
    out = {}
    for ch in sc.CHAPTERS:
        cw = [w for w in words if w[3] == ch["id"]]
        toks, owner = [], []
        for bi, b in enumerate(ch["beats"]):
            for x in said(b).split():
                n = norm(x)
                if n:
                    toks.append(n); owner.append(bi)
        sm = difflib.SequenceMatcher(None, toks, [norm(w[0]) for w in cw], autojunk=False)
        hit = {}
        for a, b_, size in sm.get_matching_blocks():
            for k in range(size):
                hit[a + k] = b_ + k
        nb = len(ch["beats"])
        first = {bi: owner.index(bi) for bi in range(nb)}
        last_tok = {bi: len(owner) - 1 - owner[::-1].index(bi) for bi in range(nb)}
        st, en = [None] * nb, [None] * nb
        for bi in range(nb):
            ms = [ti for ti in range(first[bi], last_tok[bi] + 1) if ti in hit]
            if ms:
                st[bi] = max(0.0, cw[hit[ms[0]]][1] - (ms[0] - first[bi]) * 0.33)
                en[bi] = cw[hit[ms[-1]]][2] + (last_tok[bi] - ms[-1]) * 0.33
        for bi in range(nb):                          # a beat Whisper missed entirely: between its neighbours
            if st[bi] is None:
                prev = en[bi - 1] if bi and en[bi - 1] is not None else (cw[0][1] if cw else 0.0)
                st[bi], en[bi] = prev + 0.1, prev + 2.0
        for bi in range(1, nb):
            st[bi] = max(st[bi], st[bi - 1] + 0.6)
        for bi in range(nb):
            out[(ch["id"], bi)] = (st[bi], en[bi])
    return out


def timeline(d):
    """[{t0, t1, v, key, ch}] covering 0..END: the cold open's beats, then for each chapter its card and its beats, then
    the end card."""
    sc = script_of(d)
    words = json.load(open(os.path.join(d, "build", "words.json")))
    chj = json.load(open(os.path.join(d, "build", "chapters.json")))
    bt = beat_times(sc, words)
    segs = []
    for i, (ch, cj) in enumerate(zip(sc.CHAPTERS, chj["chapters"])):
        if i == 1:
            segs.append(dict(t0=cj["card"], v=("title", sc.TITLE, f"01  ·  {ch['title']}"), key=f"{ch['id']}_card", ch=ch["id"]))
        elif i > 1:
            segs.append(dict(t0=cj["card"], v=("card", i, ch["title"]), key=f"{ch['id']}_card", ch=ch["id"]))
        for bi, b in enumerate(ch["beats"]):
            t0 = 0.0 if (i == 0 and bi == 0) else bt[(ch["id"], bi)][0] - 0.18
            segs.append(dict(t0=max(t0, cj["card"] + (1.2 if i else 0.0)) if bi == 0 else t0, v=b[1],
                             key=f"{ch['id']}_{bi:02d}", ch=ch["id"]))
    segs.append(dict(t0=chj["end_voice"] + 0.8, v=("end",), key="end", ch="end"))
    segs.sort(key=lambda s: s["t0"])
    for a, b in zip(segs, segs[1:]):
        a["t1"] = b["t0"]
    segs[-1]["t1"] = chj["total"]
    return segs


# ---------------------------------------------------------------- the pictures
def fonts():
    return dict(disp=lambda s: mg.font(mg.DISPLAY, s), body=lambda s: mg.font(mg.BODY_M, s), mono=lambda s: mg.font(mg.MONO_M, s))


F = fonts()


def gray_still(path, pad=1.12):
    """An AI still as a grey field ready for the character look: levels stretched, a touch of gamma and edge."""
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if im is None:
        return None
    h, w = im.shape
    s = max(W * pad / w, H * pad / h)
    im = cv2.resize(im, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
    lo, hi = np.percentile(im, 3), np.percentile(im, 99.6)
    g = np.clip((im - lo) / max(1e-3, hi - lo), 0, 1)
    m = float(g.mean())
    g = g ** float(np.clip(math.log(0.2) / math.log(max(1e-3, m)), 1.0, 2.6))      # mean brightness to ~0.2: busy pictures calm down
    bl = cv2.GaussianBlur(g, (0, 0), 3)
    g = np.clip(g + 0.6 * (g - bl), 0, 1)
    return g


def cam_for(key):
    """A slow move per beat, chosen from the key so it never changes between renders."""
    r = (sum(ord(c) for c in key) * 2654435761) % 6
    return [((0.5, 0.5, 1.0), (0.5, 0.5, 1.07)), ((0.5, 0.5, 1.08), (0.5, 0.5, 1.0)), ((0.44, 0.5, 1.06), (0.56, 0.5, 1.06)),
            ((0.56, 0.5, 1.06), (0.44, 0.5, 1.06)), ((0.5, 0.56, 1.06), (0.5, 0.45, 1.06)), ((0.48, 0.48, 1.0), (0.53, 0.52, 1.1))][r]


def place(g, cam, u):
    """The grey still under the camera at u (0..1): a W x H crop."""
    (x0, y0, z0), (x1, y1, z1) = cam
    k = ease(u)
    cx, cy, z = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, z0 + (z1 - z0) * k
    gh, gw = g.shape
    base = max(W / gw, H / gh)
    sc = base * z * (1.0 / 1.12) * 1.12
    m = np.float32([[sc, 0, W / 2 - cx * gw * sc], [0, sc, H / 2 - cy * gh * sc]])
    return cv2.warpAffine(g, m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def count_text(s, k):
    """'18,000' at k=0.4 -> '7,200': numbers count up as they form (prefix and suffix kept)."""
    m = re.match(r"^(\D*?)(\d[\d,]*)(\D*)$", s)
    if not m or k >= 1:
        return s
    v = int(m.group(2).replace(",", ""))
    n = int(round(v * ease(k)))
    body = f"{n:,}" if "," in m.group(2) or v >= 10000 else str(n)
    return m.group(1) + body + m.group(3)


def fit(font_fn, text, size, maxw):
    f = font_fn(size)
    while f.measureText(text) > maxw and size > 20:
        size -= 4
        f = font_fn(size)
    return f


def wrap(text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if cur and f.measureText(t) > maxw:
            lines.append(cur); cur = w
        else:
            cur = t
    return lines + ([cur] if cur else [])


def ctext(c, s, x, y, f, col, a=1.0):
    c.drawString(s, x - f.measureText(s) / 2, y, f, mg.fill(col, a))


def typed(c, s, x, y, t, t0, f, col, a=1.0, align="left", cps=34.0):
    """A label typed on at a human pace, with a cursor while it types (engine.look's rhythm)."""
    if a <= 0.01 or t < t0:
        return
    sched = look.schedule(s, t0, cps)
    n = int(np.searchsorted(sched, t, side="right"))
    if n == 0:
        return
    w = f.measureText(s)
    x0 = x - w / 2 if align == "center" else x - w if align == "right" else x
    c.drawString(s[:n], x0, y, f, mg.fill(col, a))
    if t < sched[-1] + 0.45 and (n < len(s) or (t - sched[-1]) % 0.3 < 0.18):
        sz = f.getSize()
        cx_ = x0 + f.measureText(s[:n]) + 2
        c.drawRect(skia.Rect.MakeXYWH(cx_, y - sz * 0.78, sz * 0.56, sz * 0.94), mg.fill(col, 0.75 * a))


def words_layout(text):
    """A short line, large: the font, its rows, the first baseline and the row height."""
    f = F["disp"](80)
    lines = wrap(text, f, 1500)
    if len(lines) > 2:
        f = F["disp"](64)
        lines = wrap(text, f, 1560)
    lh = f.getSize() * 1.45
    y0 = H * 0.5 - (len(lines) - 1) * lh / 2 + f.getSize() * 0.36
    return f, lines, y0, lh


def words_reveal(f, lines, y0, lh, u):
    """Each word's place and how far it has faded in (one after another, 80 ms apart)."""
    n = 0
    for li, ln in enumerate(lines):
        x = W / 2 - f.measureText(ln) / 2
        for w in ln.split():
            yield li, ln, x, w, ease(seg(u, 0.08 * n, 0.08 * n + 0.45))
            x += f.measureText(w + " ")
            n += 1


# ---------------------------------------------------------------- the house look, fast (3 Oct)
# engine.look's chars() and screen() rebuilt on cv2 and numpy: the same picture (checked against them on LF01's frames)
# at about a third of the cost; skia's CPU blurs were most of a frame's time.
from scipy.ndimage import distance_transform_edt, maximum_filter  # noqa: E402

G = look.G
ATLAS8 = (G.atlas * 255).astype(np.uint8)
BG = np.array((11, 9, 8), np.float32)                          # BGR, as look.screen's clear colour
LO, HI = np.array((90, 96, 16), np.float32), np.array((245, 246, 236), np.float32)
_VIG = []


def vignette():
    if not _VIG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.hypot(xx - W / 2, yy - H / 2) / 1180.0
        a = np.clip((r - 0.55) / 0.45, 0, 1) * (120 / 255.0)
        _VIG.append((1 - a)[..., None].astype(np.float32))
    return _VIG[0]


def chars_fast(fe, t, sea_amt=1.0):
    """look.chars: the character layer (BGR, premultiplied, float32), its coverage (0..1) and the subject field."""
    fld, edge = fe
    fld = np.maximum(fld, maximum_filter(fld, size=3) * 0.28)
    subj = fld.copy()
    if sea_amt > 0:
        mask = fld > 0.14
        d = distance_transform_edt(~mask) if mask.any() else np.full(fld.shape, 99.0)
        fld = np.maximum(fld, look.sea(t, G.cols, G.rows) ** 1.6 * 0.13 * sea_amt * np.clip((d - 2) / 10, 0, 1))
    fld = np.where(subj < 0.2, np.minimum(fld, np.maximum(subj - 0.12, 0) + (fld - subj).clip(0)), fld)
    idx = np.clip((fld * (G.n_ramp - 1)).round().astype(int), 0, G.n_ramp - 1)
    stroke = (edge >= 0) & (subj > 0.12)
    idx = np.where(stroke, G.n_ramp + np.maximum(edge, 0), idx)
    fld = np.where(stroke, np.maximum(fld, 0.9), fld)
    cov = ATLAS8[idx].transpose(0, 2, 1, 3).reshape(G.rows * G.ch, G.cols * G.cw)
    k = (np.clip(fld * 1.15, 0, 1) ** 1.1)[..., None]
    col = (LO * (1 - k) + HI * k).astype(np.float32)                                    # per cell
    colf = cv2.resize(col, (G.cols * G.cw, G.rows * G.ch), interpolation=cv2.INTER_NEAREST)
    a = cov.astype(np.float32) * (1 / 255.0)
    rgb = np.zeros((H, W, 3), np.float32)
    al = np.zeros((H, W), np.float32)
    rgb[: colf.shape[0], : colf.shape[1]] = colf * (a * a)[..., None]        # skia drew it unpremultiplied: colour x cover x cover
    al[: a.shape[0], : a.shape[1]] = a
    return rgb, al, subj


def screen_fast(rgb, al, subj):
    """look.screen + the vignette: a soft light behind the subject, the characters, a tight glow."""
    out = np.empty((H, W, 3), np.float32)
    out[:] = BG
    if subj is not None and np.any(subj > 0.14):
        g = (np.clip(subj, 0, 1) ** 1.5 * 255).astype(np.float32)
        g2 = g * g / 255.0                                                               # unpremultiplied, as in look.screen
        small = np.stack([g2 * 0.74, g2 * 0.78, g2 * 0.22], -1)                          # BGR of (0.22, 0.78, 0.74)
        q = cv2.resize(small, (W // 4, H // 4), interpolation=cv2.INTER_LINEAR)
        q = cv2.GaussianBlur(q, (0, 0), 3)
        out += 0.32 * cv2.resize(q, (W, H), interpolation=cv2.INTER_LINEAR)
    out = rgb + out * (1 - al[..., None])
    h = cv2.resize(rgb, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    h = cv2.GaussianBlur(h, (0, 0), 1.75)
    out += 0.35 * cv2.resize(h, (W, H), interpolation=cv2.INTER_LINEAR)
    out *= vignette()
    return out


class Film:
    def __init__(self, d):
        self.d = d
        self.sc = script_of(d)
        self.segs = timeline(d)
        self.chj = json.load(open(os.path.join(d, "build", "chapters.json")))
        self.END = self.chj["total"]
        self.words = json.load(open(os.path.join(d, "build", "words.json")))
        self.fix = getattr(self.sc, "FIX", {})
        self.shots = mod(os.path.join(d, "shots.py"), "shots_" + os.path.basename(d))
        self.stills, self.readers = {}, {}
        self.phrases = self._phrases()

    # -- media
    def still(self, sid):
        if sid not in self.stills:
            self.stills[sid] = gray_still(os.path.join(self.d, "src", "ai", sid + ".png"))
        return self.stills[sid]

    def clip_frame(self, sg, t):
        """The clip for this beat, conformed to its length at 24 fps (slowed up to 1.6x, then held)."""
        cid = sg["v"][1]
        src = os.path.join(self.d, "src", "ai", cid + ".mp4")
        if not os.path.exists(src):
            return None
        dur = sg["t1"] - sg["t0"] + XF + 0.2
        out = os.path.join(self.d, "build", "clips", f"{sg['key']}.mp4")
        if not os.path.exists(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            n = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                     capture_output=True, text=True).stdout)
            slow = min(1.6, max(1.0, dur / n))
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
                            f"setpts={slow:.4f}*PTS,fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                            f"format=gray,tpad=stop_mode=clone:stop_duration={max(0.0, dur - n * slow) + 1:.2f}",
                            "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", out], check=True)
        i = max(0, int((t - sg["t0"]) * FPS))
        r = self.readers.get(sg["key"])
        if r is None or r["i"] > i:
            if r:
                r["cap"].release()
            r = self.readers[sg["key"]] = dict(cap=cv2.VideoCapture(out), i=-1, last=None)
        while r["i"] < i:
            ok, fr = r["cap"].read()
            if not ok:
                break
            r["i"] += 1
            r["last"] = fr
        if r["last"] is None:
            return None
        g = cv2.cvtColor(r["last"], cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        lo, hi = np.percentile(g, 3), np.percentile(g, 99.6)
        return np.clip((g - lo) / max(1e-3, hi - lo), 0, 1) ** 1.15

    # -- the subject: everything that becomes characters (white on black)
    def subject(self, sg, t):
        v, u = sg["v"], t - sg["t0"]
        dur = max(0.5, sg["t1"] - sg["t0"])
        kind = v[0]
        if kind in ("img", "clip"):
            g = None
            if kind == "clip":
                g = self.clip_frame(sg, t)
                if g is None:
                    g = self.still(self.shots.CLIPS.get(v[1], (v[1],))[0])
                    g = None if g is None else place(g, cam_for(sg["key"]), min(1.0, u / (dur + XF)))
            else:
                st = self.still(v[1])
                g = None if st is None else place(st, cam_for(sg["key"]), min(1.0, u / (dur + XF)))
            if g is None:
                g = np.zeros((H, W), np.float32)
            return g
        surf = skia.Surface(W, H)
        c = surf.getCanvas()
        c.clear(skia.ColorBLACK)
        a_in = ease(seg(u, 0.0, 0.6))
        if kind == "num":
            txt = count_text(v[1], seg(u, 0.1, 1.3))
            f = fit(F["disp"], v[1], 250, 1560)
            ctext(c, txt, W / 2, H * 0.53, f, WHITE, a_in)
        elif kind == "words":
            f, lines, y0, lh = words_layout(v[1])
            glow = skia.Paint(AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=9)
            for li, ln, x, w, k in words_reveal(f, lines, y0, lh, u):
                glow.setColor(skia.Color4f(1, 1, 1, 0.55 * k))
                c.drawString(w, x, y0 + li * lh, f, glow)
        elif kind == "quote":
            f = F["disp"](420)
            c.drawString("“", 120, H * 0.5 + 150, f, mg.fill(WHITE, 0.8 * a_in))
        elif kind == "list":
            n = len(v[1])
            top, step = H * 0.5 - (n - 1) * 44, 88
            c.drawRect(skia.Rect.MakeXYWH(300, top - 62, 7, (n - 1) * step + 90), mg.fill(WHITE, 0.9 * a_in))
            for i in range(n):
                k = ease(seg(u, self._list_t(v, dur, i), self._list_t(v, dur, i) + 0.3))
                c.drawRect(skia.Rect.MakeXYWH(326, top + i * step - 30, 22, 22), mg.fill(WHITE, k))
        elif kind == "split":
            for side, (big, _) in enumerate((v[1], v[2])):
                f = fit(F["disp"], big, 190, 700)
                k = ease(seg(u, 0.1 + 0.35 * side, 0.7 + 0.35 * side))
                ctext(c, count_text(big, seg(u, 0.1 + 0.35 * side, 1.2 + 0.35 * side)), W * (0.29 + 0.42 * side), H * 0.52, f, WHITE, k)
            c.drawRect(skia.Rect.MakeXYWH(W / 2 - 3, H * 0.3, 6, H * 0.36), mg.fill(WHITE, 0.6 * a_in))
        elif kind == "tl":
            n = len(v[1])
            x0, x1, y = 260, W - 260, H * 0.52
            c.drawRect(skia.Rect.MakeXYWH(x0, y - 3, (x1 - x0) * ease(seg(u, 0, 0.8)), 6), mg.fill(WHITE, 0.85))
            for i in range(n):
                x = x0 + (x1 - x0) * (i + 0.5) / n
                k = ease(seg(u, self._tl_t(dur, n, i), self._tl_t(dur, n, i) + 0.35))
                c.drawCircle(x, y, 10 + 14 * k, mg.fill(WHITE, 0.4 + 0.6 * k))
        elif kind == "title":
            f = fit(F["disp"], v[1], 96, 1600)
            glow = skia.Paint(AntiAlias=True, Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=10)
            glow.setColor(skia.Color4f(1, 1, 1, 0.55 * a_in))
            c.drawString(v[1], W / 2 - f.measureText(v[1]) / 2, H * 0.53, f, glow)
        elif kind == "card":
            f = F["disp"](240)
            ctext(c, f"{v[1]:02d}", W / 2, H * 0.5, f, WHITE, 0.95 * a_in)
        elif kind == "end":
            f = F["disp"](120)
            ctext(c, "THE CURVE", W / 2, H * 0.3, f, WHITE, a_in)
        arr = surf.makeImageSnapshot().toarray()
        return arr[..., 0].astype(np.float32) / 255.0

    def _list_t(self, v, dur, i):
        return 0.3 + i * min(0.9, max(0.35, (dur - 1.2) / max(1, len(v[1]))))

    def _tl_t(self, dur, n, i):
        return 0.4 + i * min(1.6, max(0.5, (dur - 1.0) / n))

    # -- crisp: typed labels and text drawn after the look
    def crisp(self, c, sg, t, a):
        v, u = sg["v"], t - sg["t0"]
        dur = max(0.5, sg["t1"] - sg["t0"])
        kind = v[0]
        t0 = sg["t0"]
        if kind in ("img", "clip") and len(v) > 2:
            typed(c, v[2], 120, 124, t, t0 + 0.35, F["mono"](30), GOLD, a)
        elif kind == "num":
            typed(c, v[2], W / 2, H * 0.53 + 120, t, t0 + 0.55, F["mono"](28), GOLD, a, align="center")
        elif kind == "quote":
            f = F["body"](48 if len(v[1]) < 120 else 42)
            lines = wrap(v[1], f, 1280)
            cps = max(38.0, len(v[1]) / max(1.0, dur * 0.55))
            y0 = H * 0.5 - (len(lines) - 1) * f.getSize() * 0.68 - 20
            tt = t0 + 0.3
            for li, ln in enumerate(lines):
                typed(c, ln, 330, y0 + li * f.getSize() * 1.36, t, tt, f, WHITE, a, cps=cps)
                tt += len(ln) / cps + 0.05
            typed(c, v[2], 330, y0 + len(lines) * f.getSize() * 1.36 + 34, t, tt + 0.2, F["mono"](24), GOLD, a, cps=48)
        elif kind == "list":
            n = len(v[1])
            top, step = H * 0.5 - (n - 1) * 44, 88
            if len(v) > 2:
                typed(c, v[2], 300, top - 96, t, t0 + 0.1, F["mono"](24), GOLD, a, cps=48)
            for i, item in enumerate(v[1]):
                typed(c, item, 380, top + i * step, t, t0 + self._list_t(v, dur, i), F["mono"](40), WHITE, a, cps=40)
        elif kind == "split":
            for side, (_, small) in enumerate((v[1], v[2])):
                typed(c, small, W * (0.29 + 0.42 * side), H * 0.52 + 110, t, t0 + 0.6 + 0.35 * side, F["mono"](26), GOLD, a,
                      align="center", cps=44)
        elif kind == "tl":
            n = len(v[1])
            x0, x1, y = 260, W - 260, H * 0.52
            for i, (date, what) in enumerate(v[1]):
                x = x0 + (x1 - x0) * (i + 0.5) / n
                ti = t0 + self._tl_t(dur, n, i)
                typed(c, date, x, y - 52, t, ti, F["mono"](30), GOLD, a, align="center", cps=40)
                f = F["mono"](22)
                for li, ln in enumerate(wrap(what, f, (x1 - x0) / n - 30)):
                    typed(c, ln, x, y + 70 + li * 32, t, ti + 0.25, f, WHITE, a, align="center", cps=48)
        elif kind == "words":
            f, lines, y0, lh = words_layout(v[1])
            for li, ln, x, w, k in words_reveal(f, lines, y0, lh, u):
                c.drawString(w, x, y0 + li * lh, f, mg.fill(WHITE, k * a))
        elif kind == "title":
            f = fit(F["disp"], v[1], 96, 1600)
            ctext(c, v[1], W / 2, H * 0.53, f, WHITE, a * ease(seg(u, 0.0, 0.6)))
            typed(c, "THE CURVE", W / 2, H * 0.53 - 150, t, t0 + 0.2, F["mono"](26), GOLD, a, align="center", cps=30)
            typed(c, v[2], W / 2, H * 0.53 + 110, t, t0 + 0.9, F["mono"](28), SOFT, a, align="center", cps=40)
        elif kind == "card":
            typed(c, v[2], W / 2, H * 0.5 + 130, t, t0 + 0.35, F["mono"](40), WHITE, a, align="center", cps=30)
        elif kind == "end":
            typed(c, "SOURCES FOR EVERY NUMBER ARE IN THE DESCRIPTION", W / 2, H * 0.3 + 90, t, t0 + 0.6, F["mono"](24), GOLD, a,
                  align="center", cps=40)

    # -- captions: the spoken words, word by word
    def _words(self):
        """Whisper's words, tidied for the screen: '18' ',000' -> '18,000', 'GPT' '-5' '.6' -> 'GPT-5.6', and the
        film's FIX spellings (one word or two)."""
        ws = []
        for w in self.words:
            w = list(w)
            if ws and re.match(r"^[-.,]\d", w[0]) and w[3] == ws[-1][3]:
                ws[-1][0] += w[0]
                ws[-1][2] = w[2]
                continue
            ws.append(w)
        out, i = [], 0
        while i < len(ws):
            two = " ".join(x[0] for x in ws[i:i + 2])
            if i + 1 < len(ws) and two in self.fix:
                out.append([self.fix[two], ws[i][1], ws[i + 1][2], ws[i][3]]); i += 2
                continue
            out.append([self.fix.get(ws[i][0], ws[i][0])] + ws[i][1:]); i += 1
        return out

    def _phrases(self):
        out, cur = [], []
        for w in self._words():
            if cur and (w[1] - cur[-1][2] > 0.55 or w[3] != cur[-1][3] or len(cur) >= 9):
                out.append(cur); cur = []
            cur.append(w)
            if w[0][-1:] in ".?!:;" or (w[0][-1:] == "," and len(cur) >= 4):
                out.append(cur); cur = []
        if cur:
            out.append(cur)
        ph = []
        for i, p in enumerate(out):
            nxt = out[i + 1][0][1] if i + 1 < len(out) else p[-1][2] + 1.0
            ph.append(dict(t0=p[0][1] - 0.08, t1=min(p[-1][2] + 0.35, nxt - 0.02),
                           words=[(w[0], w[1]) for w in p]))
        return ph

    def captions(self, c, t):
        live = [p for p in self.phrases if p["t0"] <= t < p["t1"]]
        if not live:
            return
        p = live[-1]
        f = F["body"](38)
        rows, cur = [], []
        for w in p["words"]:
            if cur and f.measureText(" ".join(x[0] for x in cur + [w])) > 1400:
                rows.append(cur); cur = [w]
            else:
                cur.append(w)
        rows.append(cur)
        y0 = H - 112 - (len(rows) - 1) * 48
        for li, ws in enumerate(rows):
            s = " ".join(x[0] for x in ws)
            wt = f.measureText(s)
            x = W / 2 - wt / 2
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 18, y0 + li * 48 - 36, wt + 36, 50), 10, 10, mg.fill("#0B0C0E", 0.55))
            for w, a in ws:
                c.drawString(w, x, y0 + li * 48, f, mg.fill("#FFFFFF" if t >= a - 0.02 else SOFT, 1.0))
                x += f.measureText(w + " ")

    def furniture(self, c):
        c.drawString(self.sc.TAG, 120, H - 46, F["mono"](16), mg.fill(SOFT, 0.8))
        c.drawLine(120, H - 70, 300, H - 70, mg.stroke(SOFT, 1, 0.6))

    # -- one frame
    def at(self, t):
        i = max(k for k, s in enumerate(self.segs) if s["t0"] <= t + 1e-6) if t >= self.segs[0]["t0"] else 0
        cur = self.segs[i]
        g = self.subject(cur, t)
        prev, k = None, 1.0
        if i > 0 and t - cur["t0"] < XF:
            prev = self.segs[i - 1]
            k = ease((t - cur["t0"]) / XF)
            g = self.subject(prev, t) * (1 - k) + g * k
        arr = np.zeros((H, W, 4), np.uint8)
        arr[..., :3] = (np.clip(g, 0, 1) * 255).astype(np.uint8)[..., None]
        arr[..., 3] = 255
        fe = look.cells(arr)
        sea = 0.5 if cur["v"][0] in ("img", "clip") else 1.0
        rgb, al, subj = chars_fast(fe, t, sea_amt=sea)
        frame = np.empty((H, W, 4), np.uint8)
        frame[..., :3] = np.clip(screen_fast(rgb, al, subj), 0, 255).astype(np.uint8)
        frame[..., 3] = 255
        out = skia.Surface(frame, colorType=skia.ColorType.kBGRA_8888_ColorType)   # straight into the array
        c = out.getCanvas()
        if prev is not None:
            self.crisp(c, prev, t, 1 - k)
        self.crisp(c, cur, t, k if prev is not None else 1.0)
        if cur["v"][0] not in ("end",) and not getattr(self, "no_caps", False):
            self.captions(c, t)
        self.furniture(c)
        out.flushAndSubmit()
        return frame


# ---------------------------------------------------------------- sound
SFX_FOR = {"num": ("thock", -8, 0.45), "split": ("thock", -9, 0.45), "card": ("whoosh", -12, 0.0), "title": ("form", -8, 0.2),
           "words": ("form", -14, 0.1), "tl": ("tick_run", -16, 0.3)}


def sfx(film):
    return [(round(s["t0"] + SFX_FOR[s["v"][0]][2], 3), SFX_FOR[s["v"][0]][0], SFX_FOR[s["v"][0]][1])
            for s in film.segs if s["v"][0] in SFX_FOR]


# chapter -> (bed, bpm, key, gain): The Curve's beds (the user liked house and garage, 1 Oct; deep_field for the serious
# turns). A film may override with MUSIC in its script.
CYCLE = [("deep_field", 112, -3, 0.0), ("house", 124, 0, -1.0), ("garage", 130, 2, -1.0), ("deep_field", 112, 0, 0.0),
         ("house", 124, -2, -1.0), ("garage", 130, -1, -1.0)]
BED_XF = 1.5


def plan_for(bars):
    edge = 2 if bars < 24 else 4
    brk = 2 if bars >= 20 else 0
    body = bars - edge - 2 - brk
    a = math.ceil(body * 0.55)
    out = [("intro", edge), ("a", a)]
    if brk:
        out += [("b", body - a - (body - a) // 3), ("break", brk), ("b", (body - a) // 3)]
    else:
        out += [("b", body - a)]
    out += [("out", 2)]
    return [(n, k) for n, k in out if k > 0]


def music(d):
    import beds
    sc = script_of(d)
    chj = json.load(open(os.path.join(d, "build", "chapters.json")))
    plan = getattr(sc, "MUSIC", {})
    cards = [c["card"] for c in chj["chapters"]] + [chj["total"]]
    os.makedirs(os.path.join(d, "build", "beds"), exist_ok=True)
    out = []
    for i, (c, t0, t1) in enumerate(zip(chj["chapters"], cards, cards[1:])):
        bed, bpm, key, gain = plan.get(c["id"], CYCLE[i % len(CYCLE)])
        dur = (t1 - t0) + BED_XF
        bars = math.ceil(dur / (240.0 / bpm)) + 1
        path = os.path.join(d, "build", "beds", f"{c['id']}.wav")
        if not os.path.exists(path):
            x = beds.BEDS[bed](bpm, plan=plan_for(bars), key=key)
            fx.save(path, x, mp3=False)
        out.append([round(t0, 3), round(min(chj["total"], t1 + BED_XF), 3), path, gain])
        print(f"{c['id']:8s} {bed:10s} {bpm} bpm key {key:+d}  {t0:7.2f}-{t1:7.2f}")
    json.dump(out, open(os.path.join(d, "build", "music.json"), "w"), indent=1)


def mix_film(d, film):
    m = types.SimpleNamespace(END=film.END, VOICE=os.path.join(d, "build", "voice.wav"), WORDS=os.path.join(d, "build", "words.json"),
                              MUSIC=json.load(open(os.path.join(d, "build", "music.json"))), SFX=sfx(film))
    return doc.mix(m, os.path.join(d, "build", "mix.wav"), bed_db=-24.0, duck_db=-10.0)


# ---------------------------------------------------------------- render
def segments(film):
    cuts = [0.0] + [c["card"] for c in film.chj["chapters"][1:]] + [film.END]
    return [(a, b, os.path.join(film.d, "build", f"seg_{i:02d}.mp4")) for i, (a, b) in enumerate(zip(cuts, cuts[1:]))]


def render_segment(d, t0, t1, out):
    cv2.setNumThreads(1)                                     # four workers on four cores: no thread pile-up inside each
    film = Film(d)
    tmp = out + ".part.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "superfast", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for f in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
        enc.stdin.write(film.at(f / FPS).tobytes())
    enc.stdin.close()
    enc.wait()
    os.replace(tmp, out)
    return out


def render(d, only=None, workers=4):
    film = Film(d)
    name = getattr(film.sc, "NAME", os.path.basename(d))
    segs = segments(film)
    todo = [segs[i] for i in only] if only else [s for s in segs if not os.path.exists(s[2])]
    for s in todo:
        if os.path.exists(s[2]):
            os.remove(s[2])
    todo.sort(key=lambda s: s[0] - s[1])                      # longest first
    with ProcessPoolExecutor(workers) as ex:
        for p in ex.map(render_segment, [d] * len(todo), [s[0] for s in todo], [s[1] for s in todo], [s[2] for s in todo]):
            print("done", p, flush=True)
    if only:
        return
    wav = os.path.join(d, "build", "mix.wav")
    if not os.path.exists(wav):
        mix_film(d, film)
    lst = os.path.join(d, "build", "segs.txt")
    open(lst, "w").write("".join(f"file '{s[2]}'\n" for s in segs))
    hq = os.path.join(d, "build", f"{name}_hq.mkv")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "pcm_s24le", hq], check=True)
    os.makedirs(os.path.join(d, "out"), exist_ok=True)
    doc.deliver(hq, os.path.join(d, "out", f"{name}_1080p.mp4"), film.END, look=None)


def frames(d, ts):
    film = Film(d)
    os.makedirs(os.path.join(d, "build", "qc"), exist_ok=True)
    paths = []
    for t in ts:
        p = os.path.join(d, "build", "qc", f"t{t:07.2f}.jpg")
        cv2.imwrite(p, cv2.cvtColor(film.at(t), cv2.COLOR_BGRA2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
        paths.append(p)
    ims = [cv2.resize(cv2.imread(p), (640, 360)) for p in paths]
    while len(ims) % 3:
        ims.append(np.zeros_like(ims[0]))
    rows = [np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]
    cv2.imwrite(os.path.join(d, "build", "qc", "sheet.jpg"), np.vstack(rows))
    return paths


if __name__ == "__main__":
    d = os.path.join(HERE, sys.argv[1])
    cmd = sys.argv[2]
    if cmd == "vo":
        vo(d)
    elif cmd == "music":
        music(d)
    elif cmd == "timeline":
        for s in timeline(d):
            print(f"{s['t0']:7.2f}-{s['t1']:7.2f} {s['key']:12s} {s['v'][0]:6s} {str(s['v'][1])[:60] if len(s['v']) > 1 else ''}")
    elif cmd == "frames":
        print("\n".join(frames(d, [float(x) for x in sys.argv[3:]])))
    elif cmd == "mix":
        print(mix_film(d, Film(d)))
    elif cmd == "render":
        render(d, only=[int(x) for x in sys.argv[3:]] or None)
