"""Sound for the style shoot-out (all versions share it): a liquid jungle bed arranged to the cold open, and the
picture's events (build/events.json) played from the sound palette. No voice yet: captions carry the words until
ElevenLabs George is connected. Master: -14 LUFS, -1 dBTP.

    python3 mix_open.py          # build/open_mix.wav, then muxes onto every build/style_*_silent.mp4
"""
import glob
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "music"))
import audio_fx as fx  # noqa: E402

BUILD = os.path.join(HERE, "build")
SFX = os.path.join(HERE, "..", "out", "sfx")
MAP = {"form": "form", "morph": "whoosh", "glint": "scan", "scan": "scan", "whoosh": "whoosh", "latch": "latch",
       "tick": "tick_run", "thock": "thock", "zoom": "riser", "confirm": "confirm", "chime": "confirm"}
GAIN = {"form": -12, "whoosh": -13, "scan": -16, "latch": -10, "tick_run": -18, "thock": -9, "riser": -12, "confirm": -12}


def bed(total):
    import jungle
    arr = [("intro", 5), ("build", 12), ("full", 5), ("drop", 1), ("coda", 2)]
    jungle.render(arr, "ep03s_open_bed", flavour="liquid", rhodes_on=True, reese_on=False)
    y = fx.load(os.path.join(HERE, "..", "out", "music", "ep03s_open_bed.wav"))
    return y[: int(total * fx.SR)]


def main():
    ev = json.load(open(os.path.join(BUILD, "events.json")))
    total = ev["dur"]
    n = int(total * fx.SR)
    music = bed(total)
    music = np.pad(music, ((0, max(0, n - len(music))), (0, 0)))[:n]
    music *= fx.db(-18.0 - fx.lufs(music))
    sfx = np.zeros((n, 2), np.float32)
    seen, cache = set(), {}
    for at, kind, pan in ev["events"]:
        name = MAP.get(kind)
        if not name or (round(at, 2), name) in seen:
            continue
        seen.add((round(at, 2), name))
        if name not in cache:
            cache[name] = fx.load(os.path.join(SFX, name + ".wav"))
        x = cache[name] * fx.db(GAIN.get(name, -12))
        if pan:
            x = x * np.array([np.sqrt((1 - pan) / 2) * 1.414, np.sqrt((1 + pan) / 2) * 1.414])[None, :]
        i = int(at * fx.SR); j = min(n, i + len(x))
        if j > i:
            sfx[i:j] += x[: j - i]
    mix = fx.master(music + sfx, target=-14.0, ceiling_db=-1.0)
    out = os.path.join(BUILD, "open_mix.wav")
    fx.save(out, mix, mp3=False)
    print("mix", round(fx.lufs(mix), 2), "LUFS,", len(seen), "effects")
    for v in sorted(glob.glob(os.path.join(BUILD, "style_*_silent.mp4"))):
        final = v.replace("_silent.mp4", ".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-i", out, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                        "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest",
                        "-movflags", "+faststart", final], check=True)
        print(final, round(os.path.getsize(final) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
