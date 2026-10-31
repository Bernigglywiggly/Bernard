"""Voice for the pilot: synthesise each line (Kokoro, the exo-gunslinger blend), place line starts on the
170 BPM half-bar grid, then run the exo + cinema chain. Writes build/voice_dry.wav, build/voice.wav and
build/lines.json (start/end of every line, for scenes, captions, cards and the music arrangement).

    python3 voice_build.py [--voice michael+puck] [--speed 0.95]
"""
import argparse
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
HALF_BAR = 2 * 60.0 / BPM           # 0.706 s
LEAD_IN = 4 * HALF_BAR              # two bars of music before the first word


def trim(a, thresh=0.004):
    idx = np.nonzero(np.abs(a) > thresh)[0]
    return a[max(0, idx[0] - 240): idx[-1] + 2400] if len(idx) else a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="michael+puck")
    ap.add_argument("--speed", type=float, default=0.95)
    a = ap.parse_args()
    os.makedirs(BUILD, exist_ok=True)
    k = vl.engine()
    clips, t, meta = [], LEAD_IN, []
    prev_end = LEAD_IN - 0.3
    for i, ln in enumerate(LINES):
        y = trim(vl.say(k, ln["text"], a.voice, speed=a.speed, pause=0.30))
        start = max(t, prev_end + 0.22 + ln.get("air", 0) * HALF_BAR)
        start = math.ceil((start - LEAD_IN) / HALF_BAR - 1e-6) * HALF_BAR + LEAD_IN     # on the grid
        end = start + len(y) / fx.SR
        clips.append((start, y))
        meta.append(dict(i=i, scene=ln["scene"], text=ln["text"], start=round(start, 3), end=round(end, 3), card=ln.get("card")))
        prev_end = end
        print(f"{i:2d} {start:6.2f}-{end:6.2f}  {ln['text'][:60]}")
    total = prev_end + 3.0
    dry = np.zeros(int(total * fx.SR), np.float32)
    for s, y in clips:
        i0 = int(s * fx.SR)
        dry[i0: i0 + len(y)] += y
    fx.save(os.path.join(BUILD, "voice_dry.wav"), dry, mp3=False)
    room = fx.cinema_ir(rt60=3.4, predelay=0.055)
    wet = fx.chain_voice(dry, exo_amt=0.45, room=room, room_wet=-8.0, target=-16.0)
    fx.save(os.path.join(BUILD, "voice.wav"), wet, mp3=False)
    json.dump(dict(total=round(total, 3), bpm=BPM, half_bar=HALF_BAR, lead_in=LEAD_IN, voice=a.voice, lines=meta),
              open(os.path.join(BUILD, "lines.json"), "w"), indent=1)
    print("total", round(total, 2), "s")


if __name__ == "__main__":
    main()
