"""EP02 voice: a calm British narrator (Kokoro bm_george, the closest local match to the inspo's voice:
~142 Hz, ~147 wpm), a small studio room, lines on the 170 BPM half-bar grid, extra room before hard cuts.
Writes build/voice_dry.wav, build/voice.wav, build/lines.json.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "voice"))
import audio_fx as fx  # noqa: E402
import voice_lab as vl  # noqa: E402
from script import LINES  # noqa: E402

BUILD = os.path.join(HERE, "build")
BPM = 170.0
HB = 2 * 60.0 / BPM
LEAD = 4 * HB
VOICE, SPEED = "bm_george", 0.92


def trim(a, thresh=0.004):
    idx = np.nonzero(np.abs(a) > thresh)[0]
    return a[max(0, idx[0] - 240): idx[-1] + 2400] if len(idx) else a


def main():
    os.makedirs(BUILD, exist_ok=True)
    k = vl.engine()
    prev_end, clips, meta = LEAD - 0.3, [], []
    for i, ln in enumerate(LINES):
        y = trim(vl.say(k, ln["text"], VOICE, speed=SPEED, pause=0.36))
        gap = 0.24 + ln.get("air", 0) * HB + (0.45 if ln.get("cut") else 0.0)
        start = max(LEAD, prev_end + gap)
        start = math.ceil((start - LEAD) / HB - 1e-6) * HB + LEAD
        end = start + len(y) / fx.SR
        clips.append((start, y))
        meta.append(dict(i=i, floor=ln["floor"], text=ln["text"], start=round(start, 3), end=round(end, 3),
                         card=ln.get("card"), mark=ln.get("mark"), cut=bool(ln.get("cut")), ladder=bool(ln.get("ladder")), drop=bool(ln.get("drop")), quiet=bool(ln.get("quiet"))))
        prev_end = end
        print(f"{i:2d} F{ln['floor']} {start:6.2f}-{end:6.2f} {ln['text'][:64]}")
    total = prev_end + 4.0
    dry = np.zeros(int(total * fx.SR), np.float32)
    for s, y in clips:
        dry[int(s * fx.SR): int(s * fx.SR) + len(y)] += y
    fx.save(os.path.join(BUILD, "voice_dry.wav"), dry, mp3=False)
    room = fx.cinema_ir(rt60=1.6, predelay=0.02, seed=5, dark=0.6)
    wet = fx.chain_voice(dry, exo_amt=0.0, room=room, room_wet=-13.0, target=-16.0)
    fx.save(os.path.join(BUILD, "voice.wav"), wet, mp3=False)
    json.dump(dict(total=round(total, 3), bpm=BPM, half_bar=HB, lead_in=LEAD, voice=VOICE, lines=meta),
              open(os.path.join(BUILD, "lines.json"), "w"), indent=1)
    print("total", round(total, 2))


if __name__ == "__main__":
    main()
