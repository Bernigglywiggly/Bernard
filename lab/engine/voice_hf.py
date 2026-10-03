"""The voice from Higgsfield Seed Audio, for a channel that can't use George (each channel has its own narrator) when
there's no ElevenLabs key: one take per floor, cut back into the script's lines at the pauses Whisper finds between
them, then laid out exactly as engine.voice lays out George (the same breaths, air and cuts on the 170 BPM grid). The
outputs are engine.voice's (build/voice_dry.wav, voice.wav, lines.json), so every later step is unchanged.

    cd lab
    python3 -m engine.voice_hf ch2/ep01 reqs     # build/hf_reqs.json: one Seed Audio request per floor; submit them and
                                                 # record each take in <ep>/hf_voice.json {"<floor>": {"job", "url"}}
    python3 -m engine.voice_hf ch2/ep01 fetch    # the takes -> build/hf/vo_XX.wav, then longform/tools/words.py on them
    python3 -m engine.voice_hf ch2/ep01 build    # cut, lay out, room -> voice.wav and lines.json
"""
import difflib
import json
import math
import os
import re
import subprocess
import sys
import urllib.request

import numpy as np

import engine  # noqa: F401  (paths)
import audio_fx as fx  # noqa: E402
import eleven_tts as el  # noqa: E402
from engine.voice import BPM, GRID, LEAD, gap, script  # noqa: E402

VOICES = {"sterling": "dc382508-c8bd-443c-8cb2-46e57b8d2e6f"}       # How They Profit (The Curve is Harrison)
VOICE = os.environ.get("HF_VOICE", "sterling")
RATE = int(os.environ.get("HF_RATE", "-10"))                        # a little slower than the preset: calm, unhurried
SAY_FIX = {"AAdvantage": "Advantage"}                                # what the reader should say, not what's shown


def said(ln, slots):
    t = el.spoken(ln, slots)
    for a, b in SAY_FIX.items():
        t = t.replace(a, b)
    return t


def _paths(ep_dir):
    out = os.path.join(ep_dir, os.environ.get("EP_BUILD", "build"))
    return out, os.path.join(out, "hf"), os.path.join(ep_dir, "hf_voice.json")


def _slots(out):
    sp = os.path.join(out, "slots.json")
    return json.load(open(sp)) if os.path.exists(sp) else {}


def reqs(ep_dir):
    out, _, _ = _paths(ep_dir)
    os.makedirs(out, exist_ok=True)
    lines, slots = script(ep_dir).LINES, _slots(out)
    floors = sorted({ln["floor"] for ln in lines})
    rq = [dict(index=f, params=dict(model="seed_audio", voice_type="preset", voice_id=VOICES.get(VOICE, VOICE), format="wav",
                                    sample_rate=48000, speech_rate=RATE,
                                    prompt="\n\n".join(said(ln, slots) for ln in lines if ln["floor"] == f)))
          for f in floors]
    json.dump(rq, open(os.path.join(out, "hf_reqs.json"), "w"), indent=1)
    print(len(rq), "takes,", sum(len(r["params"]["prompt"].split()) for r in rq), "words ->", os.path.join(out, "hf_reqs.json"))


def fetch(ep_dir):
    _, hf, rec = _paths(ep_dir)
    os.makedirs(hf, exist_ok=True)
    takes = json.load(open(rec))
    for f, v in sorted(takes.items(), key=lambda kv: int(kv[0])):
        p = os.path.join(hf, f"vo_{int(f):02d}.wav")
        if not os.path.exists(p):
            urllib.request.urlretrieve(v["url"], p)
            print(p)
    new = [os.path.join(hf, f"vo_{int(f):02d}.wav") for f in takes
           if not os.path.exists(os.path.join(hf, f"words_{int(f):02d}.json"))]
    if new:
        subprocess.run([sys.executable, os.path.join(engine.LAB, "longform", "tools", "words.py"), *new], check=True)


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def _quiet(y, a, b, db=-40.0, hop=0.01):
    """The middle of the longest quiet stretch of y between a and b seconds (10 ms RMS under db from the take's peak)."""
    h = int(hop * fx.SR)
    i0, i1 = max(0, int(a * fx.SR) // h), min(len(y) // h, int(b * fx.SR) // h)
    lv = np.array([np.sqrt(np.mean(y[k * h:(k + 1) * h] ** 2) + 1e-12) for k in range(i0, i1)])
    q = 20 * np.log10(lv / (np.abs(y).max() + 1e-9)) < db
    best, run, at = (0, (a + b) / 2), 0, 0
    for k, v in enumerate(np.append(q, False)):
        if v:
            run, at = run + 1, (at if run else k)
        else:
            if run > best[0]:
                best = (run, (i0 + at + run / 2) * hop)
            run = 0
    return best[1]


def cut_take(y, words, texts):
    """The take y (with Whisper's words) split into one clip per text. Each cut goes in the longest quiet stretch of the
    audio between the last word matched to one line and the first word matched to the next (Whisper's own gaps can't be
    trusted: on 3 Oct it dropped "as the airline" and reported 2 s of silence where the words were). Each line keeps
    every Whisper word that falls inside its cuts, numbers included. -> [(clip, [(word, start, end)])]"""
    sw, owner = [], []
    for i, t in enumerate(texts):
        for w in t.split():
            if _norm(w):
                sw.append(_norm(w)); owner.append(i)
    ww = [_norm(w[0]) for w in words]
    sm = difflib.SequenceMatcher(None, sw, ww, autojunk=False)
    to_w = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            to_w[a + k] = b + k
    first = [min((to_w[j] for j in range(len(sw)) if owner[j] == i and j in to_w), default=None) for i in range(len(texts))]
    last = [max((to_w[j] for j in range(len(sw)) if owner[j] == i and j in to_w), default=None) for i in range(len(texts))]
    if None in first or None in last:
        bad = [texts[i][:50] for i in range(len(texts)) if first[i] is None]
        raise SystemExit(f"Whisper didn't hear these lines in the take (re-take it): {bad}")
    cuts = [0.0]
    for i in range(len(texts) - 1):
        a, b = last[i], first[i + 1]
        if b <= a:
            raise SystemExit(f"lines out of order in the take near: {texts[i + 1][:50]}")
        cuts.append(_quiet(y, words[a][2] - 0.3, words[b][1] + 0.3))
    cuts.append(len(y) / fx.SR)
    out = []
    for i in range(len(texts)):
        s0, s1 = int(cuts[i] * fx.SR), int(cuts[i + 1] * fx.SR)
        seg = y[s0:s1]
        idx = np.nonzero(np.abs(seg) > 0.01 * (np.abs(y).max() + 1e-9))[0]
        a = max(0, idx[0] - int(0.03 * fx.SR)) if len(idx) else 0
        b = min(len(seg), idx[-1] + int(0.12 * fx.SR)) if len(idx) else len(seg)
        x = seg[a:b].copy()
        fi, fo = min(len(x), int(0.008 * fx.SR)), min(len(x), int(0.04 * fx.SR))
        x[:fi] *= np.sin(np.linspace(0, np.pi / 2, fi)) ** 2
        x[len(x) - fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
        t0 = (s0 + a) / fx.SR
        ws = [(w[0], round(max(0.0, w[1] - t0), 3), round(w[2] - t0, 3)) for w in words
              if cuts[i] <= (w[1] + w[2]) / 2 < cuts[i + 1]]
        out.append((x, ws))
    return out


def build(ep_dir, lead=LEAD):
    ep_dir = os.path.abspath(ep_dir)
    out, hf, _ = _paths(ep_dir)
    lines, slots = script(ep_dir).LINES, _slots(out)
    clips_by_line = {}
    for f in sorted({ln["floor"] for ln in lines}):
        idx = [i for i, ln in enumerate(lines) if ln["floor"] == f]
        y = fx.load(os.path.join(hf, f"vo_{f:02d}.wav"), mono=True)
        words = json.load(open(os.path.join(hf, f"words_{f:02d}.json")))
        for i, c in zip(idx, cut_take(y, words, [said(lines[i], slots) for i in idx])):
            clips_by_line[i] = c
    prev_end, placed, meta = lead, [], []
    for i, ln in enumerate(lines):
        shown = slots[ln["slot"]].strip() if ln.get("slot") and (slots.get(ln["slot"]) or "").strip() else ln["text"]
        x, ws = clips_by_line[i]
        start = max(lead, prev_end + gap(ln, 1.0))
        start = math.ceil((start - lead) / GRID - 1e-6) * GRID + lead
        end = start + len(x) / fx.SR
        placed.append((start, x))
        meta.append(dict(i=i, floor=ln["floor"], text=shown, start=round(start, 3), end=round(end, 3), card=ln.get("card"),
                         id=ln.get("id"), slot=ln.get("slot"), cut=bool(ln.get("cut")), air=ln.get("air", 0),
                         words=[(w, round(start + a, 3), round(start + b, 3)) for w, a, b in ws]))
        prev_end = end
        print(f"{i:2d} F{ln['floor']} {start:6.2f}-{end:6.2f} {shown[:70]}")
    total = prev_end + 3.0
    dry = np.zeros(int(total * fx.SR), np.float32)
    for s, x in placed:
        dry[int(s * fx.SR): int(s * fx.SR) + len(x)] += x
    fx.save(os.path.join(out, "voice_dry.wav"), dry, mp3=False)
    room = fx.cinema_ir(rt60=1.4, predelay=0.02, seed=5, dark=0.6)
    wet = fx.chain_voice(dry, room=room, room_wet=-16.0, target=-16.0)
    fx.save(os.path.join(out, "voice.wav"), wet, mp3=False)
    json.dump(dict(total=round(total, 3), bpm=BPM, engine="higgsfield", voice=VOICE, speed=1.0, lines=meta),
              open(os.path.join(out, "lines.json"), "w"), indent=1)
    print("total", round(total, 2))
    return total


if __name__ == "__main__":
    ep = os.path.join(engine.LAB, sys.argv[1]) if not os.path.isdir(sys.argv[1]) else sys.argv[1]
    {"reqs": reqs, "fetch": fetch, "build": build}[sys.argv[2]](os.path.abspath(ep))
