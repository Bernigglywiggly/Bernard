#!/usr/bin/env python3
"""Lay out one-take-per-line narration (made with the ElevenLabs connector, which saves an mp3 per call) as the
engine's lines.json and voice_dry.wav, so flow.py and mix_pre.py can run on it. Takes live in
<build>/takes/NN_<line id>/*.mp3, in script order. Word times come from faster-whisper on each take; the gaps between
lines follow engine.voice (the same breaths and chapter air as the other films).

    ~/youtube/.venv/bin/python lay_takes.py build_george [gap scale, default 0.8]
"""
import glob
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import engine  # noqa: E402,F401  (paths)
from engine import voice  # noqa: E402

SR = 48000


def trim(y, db=-45.0, pad=0.04):
    """Cut the silence ElevenLabs leaves at each end, keeping a few milliseconds of air."""
    lv = np.abs(y)
    on = np.where(lv > 10 ** (db / 20) * lv.max())[0]
    a, b = max(0, on[0] - int(pad * SR)), min(len(y), on[-1] + int(pad * 3 * SR))
    return y[a:b], a / SR


def main(build, scale=0.8):
    out = os.path.join(HERE, build)
    script = voice.script(HERE).LINES
    by_id = {ln["id"]: ln for ln in script}
    takes = sorted(glob.glob(os.path.join(out, "takes", "*")))
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    t, meta, clips = voice.LEAD, [], []
    for i, d in enumerate(takes):
        lid = os.path.basename(d).split("_", 1)[1]
        ln = by_id[lid]
        mp3 = sorted(glob.glob(os.path.join(d, "*.mp3")))[-1]
        wav = os.path.join(d, "take.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", str(SR), wav], check=True)
        y, _ = sf.read(wav)
        y, off = trim(y)
        segs, _ = model.transcribe(wav, word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
        if i:
            t += voice.gap(ln, 1.0) * scale
        words = [[w.word.strip(), round(t + w.start - off, 3), round(t + w.end - off, 3)] for s in segs for w in s.words]
        dur = len(y) / SR
        meta.append(dict(i=i, id=lid, floor=ln["floor"], text=ln["text"], start=round(t, 3), end=round(t + dur, 3),
                         card=ln.get("card"), words=words))
        clips.append((t, y))
        print(f"{i:2d} {lid:12s} {t:6.2f}-{t + dur:6.2f}  {len(words)} words")
        t += dur
    total = t + 3.0
    buf = np.zeros(int(total * SR))
    for t0, y in clips:
        k = int(t0 * SR)
        buf[k:k + len(y)] += y
    sf.write(os.path.join(out, "voice_dry.wav"), buf, SR)
    json.dump(dict(engine="eleven", voice="george", total=round(total, 3), lines=meta), open(os.path.join(out, "lines.json"), "w"), indent=1)
    print("total", round(total, 2))


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.8)
