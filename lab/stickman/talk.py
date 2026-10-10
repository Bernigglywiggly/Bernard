"""Talking Flash-game stickman, lip-synced to a voice file.

    python talk.py <audio|auto> <out.mp4> [--vert] [--bg arena|flat|<hex>] [--captions|--no-captions]
                   [--no-intro] [--raw] [--sheet out/sheet.jpg] [--name STICKMAN]

<audio>   wav / m4a / mp3 / aiff. "auto" = in/changed.* if it exists, else the newest other file in in/.
          If you pass a file that lives in in/ and an in/changed.* exists, the changed (voice-changed) file is used
          instead; --raw forces the file you passed.

Pipeline: ffmpeg -> 16 kHz mono -> faster_whisper word timings + an RMS envelope -> grapheme-to-viseme chunks
inside each word -> one mouth per drawing at 12 drawings/s (held on twos at 24 fps) -> blinks, nods on stressed
words, gesture poses at phrase starts / punctuation / loudness peaks, impact frames on the biggest hits and on
onomatopoeia (BOOM, BANG...) -> skia frames piped to ffmpeg -> H.264 + AAC.
"""
import argparse
import glob
import math
import os
import random
import re
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flash as fl  # noqa: E402

DRAW_FPS = 12           # unique drawings per second (on twos)
OUT_FPS = 24
LEAD = 0.02             # mouth leads the sound slightly
SFX_WORDS = {"boom", "bang", "pow", "bam", "wham", "smash", "crash", "kaboom", "splat", "zap", "yeet", "kapow", "slam", "whack", "thwack", "bonk", "oof"}
AUDIO_EXT = (".wav", ".m4a", ".mp3", ".aiff", ".aif", ".aac", ".ogg", ".flac", ".caf", ".mp4", ".mov")


# ================================================================ audio in
def resolve_audio(arg, raw=False):
    in_dir = os.path.join(HERE, "in")
    changed = sorted(p for p in glob.glob(os.path.join(in_dir, "changed.*")) if p.lower().endswith(AUDIO_EXT))
    if arg == "auto" or os.path.isdir(arg):
        d = in_dir if arg == "auto" else arg
        if changed and not raw:
            return changed[0]
        cands = [p for p in glob.glob(os.path.join(d, "*")) if p.lower().endswith(AUDIO_EXT) and not os.path.basename(p).startswith("changed.")]
        if not cands:
            sys.exit("no audio in %s" % d)
        return max(cands, key=os.path.getmtime)
    if not os.path.exists(arg):
        sys.exit("audio not found: %s" % arg)
    if not raw and changed and os.path.dirname(os.path.abspath(arg)) == in_dir and not os.path.basename(arg).startswith("changed."):
        print("using voice-changed file %s (pass --raw to use %s)" % (changed[0], arg))
        return changed[0]
    return arg


def load_audio(path, tmp):
    wav = os.path.join(tmp, "a16.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", wav], check=True)
    y, sr = sf.read(wav, dtype="float32")
    return wav, y, sr


def rms_env(y, sr, hop=0.01, win=0.03):
    h, w = int(sr * hop), int(sr * win)
    n = max(1, (len(y) - w) // h + 1)
    idx = np.arange(w)[None, :] + h * np.arange(n)[:, None]
    idx = np.clip(idx, 0, len(y) - 1)
    r = np.sqrt((y[idx] ** 2).mean(1))
    voiced = r[r > r.max() * 0.05]
    norm = np.percentile(voiced, 95) if len(voiced) else r.max() + 1e-9
    return np.clip(r / (norm + 1e-9), 0, 1.5)


def transcribe(wav):
    import hashlib
    import json
    cache_dir = os.path.join(HERE, "out", ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    key = os.path.join(cache_dir, hashlib.sha1(open(wav, "rb").read()).hexdigest()[:16] + ".json")
    if os.path.exists(key):
        return json.load(open(key))
    words = _transcribe(wav)
    json.dump(words, open(key, "w"))
    return words


def _transcribe(wav):
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(wav, word_timestamps=True, language="en", vad_filter=False)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append(dict(text=w.word.strip(), start=float(w.start), end=float(w.end)))
    return words


def refine_words(words, env, hop=0.01, thr=0.10):
    """Whisper word edges drift into silences; pull them in to where the envelope is actually voiced."""
    for w in words:
        a, b = int(w["start"] / hop), int(w["end"] / hop)
        seg = env[a:b + 1]
        on = np.where(seg > thr)[0]
        if len(on):
            w["start"] = max(w["start"], (a + on[0]) * hop - 0.02)
            w["end"] = min(w["end"], (a + on[-1]) * hop + 0.04)
        w["peak"] = float(seg.max()) if len(seg) else 0.0
        w["clean"] = re.sub(r"[^a-z']", "", w["text"].lower())
        w["punct"] = re.sub(r"[\w']", "", w["text"])[-1:] if re.search(r"[.,!?;:]$", w["text"]) else ""
    return words


# ================================================================ grapheme -> viseme
_MULTI = [
    ("tch", ["small"]), ("ough", ["O"]), ("augh", ["O"]), ("igh", ["open", "wide"]), ("eigh", ["wide"]),
    ("th", ["small"]), ("sh", ["U"]), ("ch", ["U"]), ("ph", ["FV"]), ("wh", ["U"]), ("ck", ["small"]),
    ("ng", ["small"]), ("qu", ["small", "U"]), ("oo", ["U"]), ("ou", ["open", "U"]), ("ow", ["O", "U"]),
    ("oa", ["O"]), ("oi", ["O", "wide"]), ("oy", ["O", "wide"]), ("ee", ["wide"]), ("ea", ["wide"]),
    ("ie", ["wide"]), ("ei", ["wide"]), ("ai", ["wide"]), ("ay", ["wide"]), ("ey", ["wide"]),
    ("ar", ["open"]), ("er", ["small"]), ("ir", ["small"]), ("ur", ["small"]), ("or", ["O"]),
    ("aw", ["O"]), ("au", ["O"]), ("ew", ["U"]),
]
_SINGLE = {"a": "open", "e": "wide", "i": "wide", "o": "O", "u": "open", "m": "MBP", "b": "MBP", "p": "MBP",
           "f": "FV", "v": "FV", "w": "U", "r": "U", "l": "small", "y": "wide"}
_VOWEL_VIS = {"open", "wide", "O", "U"}
_W = {"open": 2.0, "wide": 1.8, "O": 2.0, "U": 1.6, "small": 1.0, "MBP": 1.0, "FV": 1.1}
_SPECIAL = {"i": ["open", "wide"], "i'm": ["open", "wide", "MBP"], "a": ["small"], "the": ["small", "small"],
            "my": ["MBP", "open", "wide"], "you": ["wide", "U"], "to": ["small", "U"], "do": ["small", "U"],
            "one": ["U", "open", "small"], "are": ["open"], "eye": ["open", "wide"], "oh": ["O"], "people": ["MBP", "wide", "MBP", "small"], "what": ["U", "open", "small"], "was": ["U", "open", "small"], "ok": ["O", "small", "wide"]}


def word_visemes(word):
    w = word.lower().replace("'", "") if word.lower() not in _SPECIAL else word.lower()
    if w in _SPECIAL:
        return [(v, _W[v]) for v in _SPECIAL[w]]
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return []
    base = w[:-1] if (w.endswith("s") and len(w) > 3 and w[-2] == "e" and w[-3] not in "sxzh") else w
    magic = len(base) > 2 and base.endswith("e") and base[-2] not in "aeiouy" and base[-3] in "aeiouy"
    if magic:
        w = base[:-1] + w[len(base):]
    out = []
    i = 0
    while i < len(w):
        hit = None
        for g, vs in _MULTI:
            if w.startswith(g, i):
                hit = (g, vs)
                break
        if hit:
            for v in hit[1]:
                out.append(v)
            i += len(hit[0])
            continue
        ch = w[i]
        if i > 0 and ch == w[i - 1] and ch not in "aeiou":
            i += 1
            continue
        if magic and i == len(base) - 3 and ch in "aiou":
            out += {"a": ["wide"], "i": ["open", "wide"], "o": ["O"], "u": ["U"]}[ch]
        elif ch == "y" and i == len(w) - 1 and not re.search(r"[aeiou]", w[:-1]):
            out += ["open", "wide"]
        elif ch == "e" and i == len(w) - 1 and len(w) > 2:
            pass                                                   # silent final e
        elif ch == "h":
            out.append("small")
        else:
            out.append(_SINGLE.get(ch, "small"))
        i += 1
    return [(v, _W[v]) for v in out]


def chunk_timeline(words):
    chunks = []
    for w in words:
        vs = word_visemes(w["clean"])
        if not vs:
            continue
        tot = sum(x[1] for x in vs)
        t = w["start"]
        dur = max(0.05, w["end"] - w["start"])
        for v, wt in vs:
            d = dur * wt / tot
            chunks.append((t, t + d, v))
            t += d
    return chunks


_PRIO = {"MBP": 3.0, "FV": 1.7, "open": 1.3, "wide": 1.25, "O": 1.35, "U": 1.25, "small": 1.0}


def mouths(chunks, env, n_draw, hop=0.01):
    out = []
    dt = 1.0 / DRAW_FPS
    ci = 0
    for i in range(n_draw):
        a, b = i * dt + LEAD, (i + 1) * dt + LEAD
        amp = float(env[int(a / hop):max(int(a / hop) + 1, int(b / hop))].mean()) if int(a / hop) < len(env) else 0.0
        score = {}
        while ci < len(chunks) and chunks[ci][1] < a - 0.2:
            ci += 1
        for t0, t1, v in chunks[ci:ci + 12]:
            ov = min(b, t1) - max(a, t0)
            if ov > 0:
                if v == "MBP" and ov < 0.018:
                    continue
                score[v] = score.get(v, 0) + ov * _PRIO[v]
        if score:
            vis = max(score, key=score.get)
        else:
            vis = "open" if amp > 0.55 else ("small" if amp > 0.2 else "rest")
        if vis != "MBP" and amp < 0.07:
            vis = "rest"
        open_k = float(np.clip(0.55 + 0.6 * amp, 0.55, 1.2))
        if vis == "open" and amp < 0.22:
            vis = "small"
        out.append((vis, open_k, amp))
    return out


# ================================================================ performance (gestures, nods, impacts, blinks)
def plan(words, n_draw, dur, seed=7):
    rng = random.Random(seed)
    # phrases: split on punctuation or a pause
    phrases, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1] if k + 1 < len(words) else None
        gap = (nxt["start"] - w["end"]) if nxt else 9
        if (w["punct"] and w["punct"] in ".!?;:") or (w["punct"] == "," and gap > 0.15) or gap > 0.3:
            phrases.append(cur)
            cur = []
    if cur:
        phrases.append(cur)
    peaks = sorted(w["peak"] for w in words) or [1]
    q_stress = peaks[int(len(peaks) * 0.6)]
    q_top = peaks[int(len(peaks) * 0.9)] if len(peaks) > 3 else peaks[-1]

    keys = [(0.0, "idle", "neutral", "wide")]
    impacts, nods = [], []
    cycle = ["point", "explain", "talk", "hips", "think", "explain", "point", "talk"]
    ci = 0
    last_shot = "wide"
    last_cut = -9
    for pi, ph in enumerate(phrases):
        t0 = ph[0]["start"] - 0.1
        end_p = ph[-1]["punct"]
        sfx = next((w for w in ph if w["clean"] in SFX_WORDS), None)
        first, last = pi == 0, pi == len(phrases) - 1
        if sfx:
            pose, mood = rng.choice(["wide", "pump"]), "angry"
            impacts.append(dict(t=sfx["start"], word=sfx["clean"].upper() + "!", sfx=True))
        elif end_p == "?":
            pose, mood = "shrug", "raised"
        elif end_p == "!":
            pose, mood = rng.choice(["pump", "point"]), "angry"
        elif last:
            pose, mood = "cross", "smug"
        elif first:
            pose, mood = "hips", "neutral"
        else:
            pose = cycle[ci % len(cycle)]
            ci += 1
            mood = "raised" if max(w["peak"] for w in ph) >= q_top else ("neutral" if pi % 2 else "raised")
        if keys and keys[-1][1] == pose and pose not in ("shrug",):
            pose = cycle[ci % len(cycle)]
            ci += 1
        # shot
        if sfx:
            shot = "close"
        elif end_p == "?" or last:
            shot = "medium"
        else:
            shot = "medium" if last_shot == "wide" else "wide"
        if t0 - last_cut < 1.1 and not sfx:
            shot = last_shot
        if shot != last_shot:
            last_cut = t0
        last_shot = shot
        keys.append((max(0.0, t0), pose, mood, shot))
        # an extra beat inside long phrases, on the strongest word
        if ph[-1]["end"] - ph[0]["start"] > 1.7:
            w = max(ph[1:], key=lambda x: x["peak"])
            if w["start"] - t0 > 0.6:
                keys.append((w["start"] - 0.08, cycle[ci % len(cycle)], mood, shot))
                ci += 1
        # nods on stressed words (and phrase starts)
        for k, w in enumerate(ph):
            if (w["peak"] >= q_stress or k == 0) and (not nods or w["start"] - nods[-1] > 0.32):
                nods.append(w["start"])
        # "!" lines and the single loudest word also get an impact
        if end_p == "!" and not sfx:
            impacts.append(dict(t=ph[-1]["start"], word=None, sfx=False))
    late = [ph[-1] for ph in phrases if ph[-1]["start"] > dur * 0.4]        # punchline candidates: phrase-final words
    if late and not impacts:
        w = max(late, key=lambda x: x["peak"])
        if all(abs(w["start"] - i["t"]) > 2.0 for i in impacts):
            impacts.append(dict(t=w["start"], word=None, sfx=False))
    impacts.sort(key=lambda d: d["t"])
    keys.sort(key=lambda k: k[0])
    # settle into idle during long pauses
    extra = []
    for a, b in zip(words, words[1:]):
        if b["start"] - a["end"] > 0.7:
            extra.append((a["end"] + 0.25, "idle", "neutral", None))
    keys = sorted(keys + extra, key=lambda k: k[0])
    # blinks: every 2-4.5 s, plus on some cuts
    blinks = set()
    t = rng.uniform(0.8, 1.6)
    while t < dur:
        blinks.add(int(t * DRAW_FPS))
        if rng.random() < 0.15:
            blinks.add(int(t * DRAW_FPS) + 2)
        t += rng.uniform(2.0, 4.5)
    for k in keys:
        if rng.random() < 0.35:
            blinks.add(int(k[0] * DRAW_FPS) + 1)
    # glances in pauses
    looks = []
    for a, b in zip(words, words[1:]):
        if b["start"] - a["end"] > 0.45:
            looks.append((a["end"] + 0.08, b["start"] - 0.12, rng.choice([-1, 1])))
    return dict(keys=keys, impacts=impacts, nods=nods, blinks=blinks, looks=looks, phrases=phrases)


def ease_back(x, s=1.9):
    x = min(1.0, max(0.0, x)) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


# ================================================================ render
def render(audio, out, vert=False, bg="arena", captions=None, intro=True, sheet=None, name="STICKMAN"):
    tmp = tempfile.mkdtemp(prefix="talk_")
    wav, y, sr = load_audio(audio, tmp)
    dur = len(y) / sr
    env = rms_env(y, sr)
    print("transcribing %.1fs ..." % dur)
    words = refine_words(transcribe(wav), env)
    print(" ".join(w["text"] for w in words))
    chunks = chunk_timeline(words)
    tail = 0.7
    n_talk = int(math.ceil((dur + tail) * DRAW_FPS))
    M = mouths(chunks, env, n_talk)
    P = plan(words, n_talk, dur)
    if captions is None:
        captions = vert

    W, H = (1080, 1920) if vert else (1920, 1080)
    if vert:
        R, floor, cx = 74.0, 1520.0, W / 2
    else:
        R, floor, cx = 60.0, 905.0, W * 0.47
    HR = 1.6 * R
    if bg == "arena":
        scene = fl.Arena(W, H, floor)
    else:
        col = "#FFD23F" if bg == "flat" else "#" + bg.lstrip("#")
        scene = fl.Flat(W, H, floor, col)
    cam = fl.Cam(W, H)
    J0 = fl.joints(fl.POSES["idle"], R, HR)
    low = max(J0["foot_l"][1], J0["foot_r"][1])
    neck0 = np.array([cx, floor - low + J0["neck"][1]])
    head0 = np.array([cx, floor - low + J0["head"][1]])
    shots = {"wide": (np.array([W / 2, H / 2]), 1.0),
             "medium": (neck0 + np.array([0, -0.2 * HR]), 1.55 if not vert else 1.3),
             "close": (head0 + np.array([0, -0.15 * HR]), 1.95 if not vert else 1.6)}
    if vert:
        shots["wide"] = (np.array([W / 2, H / 2 + 60]), 1.12)

    n_intro = int(0.75 * DRAW_FPS) if intro else 0
    intro_s = n_intro / DRAW_FPS
    n_total = n_intro + n_talk

    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "%dx%d" % (W, H), "-framerate", str(DRAW_FPS),
           "-i", "-", "-i", audio, "-filter_complex", "[1:a]aresample=48000,adelay=%d:all=1,apad[a]" % int(intro_s * 1000),
           "-map", "0:v", "-map", "[a]", "-r", str(OUT_FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-tune", "animation",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    c = surf.getCanvas()

    keys = P["keys"]
    caption_chunks = _caption_chunks(words)
    score, hp = 0, 1.0
    scored = set()
    pop = None
    thumbs = []
    sheet_pick = _sheet_indices(M, n_talk, dur)

    for f in range(n_total):
        c.clear(fl.hexc("#000000"))
        if f < n_intro:
            k = f / max(1, n_intro - 3)
            fl.loading(c, W, H, k, f >= n_intro - 2)
            ff.stdin.write(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
            continue
        i = f - n_intro
        t = i / DRAW_FPS
        vis, open_k, amp = M[min(i, len(M) - 1)]

        # ---- gesture / pose
        ki = max(j for j, k in enumerate(keys) if k[0] <= t + 1e-6)
        kt, kpose, kmood, kshot = keys[ki]
        prev = keys[ki - 1] if ki > 0 else keys[0]
        dt = t - kt
        pose = fl.blend_pose(fl.POSES[prev[1]], fl.POSES[kpose], ease_back(dt / 0.25))
        sy = 1.0
        nxt = keys[ki + 1] if ki + 1 < len(keys) else None
        if nxt and 0 < nxt[0] - t <= 1.0 / DRAW_FPS + 1e-6:             # anticipation drawing
            pose = fl.blend_pose(pose, fl.POSES["crouch"], 0.3)
            sy = 0.93
        elif dt < 1.0 / DRAW_FPS:
            sy = 1.05
        mood = kmood
        shot = kshot
        if shot is None:
            shot = next((k[3] for k in reversed(keys[:ki]) if k[3]), "wide")
        # idle life + talk energy
        pose["lean"] += 1.6 * math.sin(2 * math.pi * t / 2.7) + amp * 2.5 * math.sin(t * 8.3)
        pose["head"] += amp * 4 * math.sin(t * 6.1 + 1)
        pose["arms"] = [(s + amp * 7 * math.sin(t * 9 + j * 2), e + amp * 9 * math.sin(t * 7 + j)) for j, (s, e) in enumerate(pose["arms"])]
        sy += 0.012 * math.sin(2 * math.pi * t / 2.3)
        # nods
        nod = 0.0
        for tn in P["nods"]:
            d = t - tn
            if 0 <= d < 0.34:
                nod = math.sin(math.pi * d / 0.34)
                sy -= 0.03 * nod
        # impacts
        impact_inv, shake, imp, imp_d = False, (0, 0), None, None
        hat_lift, hat_tilt = 0.05 * nod, -pose["lean"] * 0.25
        for im in P["impacts"]:
            d = t - im["t"]
            if -1e-6 <= d < 0.9:
                imp, imp_d = im, d
        if imp is not None:
            di = int(round(imp_d * DRAW_FPS))
            impact_inv = di == 0
            amp_s = max(0.0, 1 - imp_d / 0.45) * (26 if not vert else 22)
            rr = random.Random(f)
            shake = (rr.uniform(-1, 1) * amp_s, rr.uniform(-1, 1) * amp_s)
            sy *= {0: 1.0, 1: 1.13, 2: 0.9, 3: 1.04}.get(di, 1.0)
            hat_lift += max(0.0, math.sin(min(1.0, imp_d / 0.5) * math.pi)) * 1.1
            hat_tilt += 18 * math.sin(imp_d * 14) * max(0, 1 - imp_d / 0.6)
            shot = "close" if imp_d < 0.6 else shot
            mood = "angry" if di > 0 else mood
            if ("imp", id(imp)) not in scored:
                scored.add(("imp", id(imp)))
                score += 1000
                hp = max(0.18, hp - 0.22)
                pop = ("+1000", t)
        for tn in P["nods"]:
            if tn <= t and ("nod", tn) not in scored:
                scored.add(("nod", tn))
                score += 100
        blink = i in P["blinks"]
        look = 0.0
        for a, b, s in P["looks"]:
            if a <= t <= b:
                look = s
        shock = impact_inv

        focus, zoom = shots[shot]
        cam.set(focus, zoom, shake)
        pen_bg = fl.Pen(c, seed=i % 3, amp=1.6)
        pen = fl.Pen(c, seed=i, amp=max(1.4, R * 0.035), step=22, invert=impact_inv)

        if impact_inv:
            c.clear(fl.hexc("#111111"))
            fl.speed_lines(c, W, H, W / 2, H * 0.42, seed=i, col="#FFFFFF", a=0.9, inner=0.18)
        else:
            scene.draw(c, pen_bg, cam, t)
            if imp is not None and imp_d < 0.55:
                fl.speed_lines(c, W, H, *(_to_screen(cam, head0)), seed=i, col="#FFFFFF" if bg == "arena" else fl.INK, a=0.55)
        st = dict(vis=vis, open_k=open_k, mood=mood, blink=blink and not impact_inv, look=look, shock=shock, sy=sy,
                  nod=nod, hat_lift=hat_lift, hat_tilt=hat_tilt)
        with cam.apply(1.0, c):
            sh = fl.fill("#000000", 0.18)
            c.drawOval(skia.Rect.MakeXYWH(cx - 1.9 * R, floor - 0.22 * R, 3.8 * R, 0.5 * R), sh)
            fl.character(pen, pose, cx, floor, R, HR, st)
        # SFX burst
        if imp is not None and imp["sfx"] and 0 < imp_d < 0.75:
            di = int(round(imp_d * DRAW_FPS))
            s = {1: 1.35, 2: 0.95, 3: 1.05}.get(di, 1.0)
            bx, by = (W * 0.76, H * 0.3) if not vert else (W * 0.5, H * 0.17)
            c.save()
            c.translate(bx, by)
            c.scale(s, s)
            fl.burst(fl.Pen(c, seed=i, amp=2.0), 0, 0, 170 if not vert else 190, seed=i, text=imp["word"], font_size=130 if not vert else 150)
            c.restore()
        if bg == "arena" and not impact_inv:
            pk = None if pop is None else (t - pop[1]) / 0.9
            fl.hud(c, W, H, hp, score, pop[0] if pop else None, pk if pk is not None else 1.0, name=name)
        if captions and not impact_inv:
            for (a, b, toks, starts) in caption_chunks:
                if a <= t < b:
                    act = max([j for j, s0 in enumerate(starts) if s0 <= t + 0.03] or [-1])
                    popk = 1.18 if t - a < 1.0 / DRAW_FPS else 1.0
                    fl.caption(c, toks, act, W, (H - 55) if not vert else H * 0.885, 80 if not vert else 104, popk)
                    break
        img = surf.makeImageSnapshot()
        ff.stdin.write(img.toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        if sheet and i in sheet_pick:
            wi = next((w["text"] for w in words if w["start"] - 0.05 <= t + LEAD <= w["end"] + 0.05), "")
            thumbs.append((img.toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3].copy(), "%.2fs  %s  [%s]" % (t, wi, vis)))
    ff.stdin.close()
    ff.wait()
    if ff.returncode:
        sys.exit("ffmpeg failed")
    if sheet and thumbs:
        _write_sheet(thumbs, sheet)
    print("wrote", out)
    return words, M, P


def _to_screen(cam, p):
    return (np.asarray(p) - cam.focus) * cam.zoom + cam.anchor + cam.shake


def _caption_chunks(words, max_words=3, max_chars=16):
    out, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        txt = " ".join(re.sub(r"[^\w'?!]", "", x["text"]).upper() for x in cur)
        nxt = words[k + 1] if k + 1 < len(words) else None
        if len(cur) >= max_words or len(txt) >= max_chars or w["punct"] or (nxt and nxt["start"] - w["end"] > 0.3) or not nxt:
            toks = [re.sub(r"[^\w'?!]", "", x["text"]).upper() for x in cur]
            out.append([cur[0]["start"] - 0.04, cur[-1]["end"] + 0.25, toks, [x["start"] for x in cur]])
            cur = []
    for a, b in zip(out, out[1:]):
        a[1] = min(a[1], b[0])
    return out


def _sheet_indices(M, n, dur, k=8):
    """One drawing per time bin, preferring a non-rest mouth and visemes not shown yet."""
    seen, pick = set(), set()
    n_sp = int(dur * DRAW_FPS)
    for b in range(k):
        lo, hi = int(n_sp * b / k), int(n_sp * (b + 1) / k)
        best, bs = lo, -1
        for i in range(lo, max(lo + 1, hi)):
            v = M[i][0]
            s = (v != "rest") * 2 + (v not in seen) * 3 + M[i][2]
            if s > bs:
                best, bs = i, s
        seen.add(M[best][0])
        pick.add(best)
    return pick


def _write_sheet(thumbs, path):
    from PIL import Image, ImageDraw, ImageFont
    h0, w0 = thumbs[0][0].shape[:2]
    tw = 640 if w0 > h0 else 300
    th = int(h0 * tw / w0)
    cols = 4
    rows = math.ceil(len(thumbs) / cols)
    pad = 36
    sheet = Image.new("RGB", (cols * tw, rows * (th + pad)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
    except Exception:
        font = ImageFont.load_default()
    for k, (arr, lab) in enumerate(thumbs):
        im = Image.fromarray(arr).resize((tw, th), Image.LANCZOS)
        x, y = (k % cols) * tw, (k // cols) * (th + pad)
        sheet.paste(im, (x, y + pad))
        d.text((x + 8, y + 7), lab, fill=(255, 225, 77), font=font)
    sheet.save(path, quality=88)
    print("wrote", path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("out")
    ap.add_argument("--vert", action="store_true", help="9:16 1080x1920 for Shorts")
    ap.add_argument("--bg", default="arena", help="arena | flat | <hex colour>")
    ap.add_argument("--captions", dest="captions", action="store_true", default=None)
    ap.add_argument("--no-captions", dest="captions", action="store_false")
    ap.add_argument("--no-intro", dest="intro", action="store_false")
    ap.add_argument("--raw", action="store_true", help="ignore in/changed.*")
    ap.add_argument("--sheet", default=None, help="also write an 8-frame contact sheet (jpg)")
    ap.add_argument("--name", default="STICKMAN", help="name on the HUD health bar")
    a = ap.parse_args()
    audio = resolve_audio(a.audio, a.raw)
    print("audio:", audio)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    render(audio, a.out, a.vert, a.bg, a.captions, a.intro, a.sheet, a.name)


if __name__ == "__main__":
    main()
