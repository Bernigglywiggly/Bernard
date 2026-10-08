#!/usr/bin/env python3
"""Put each film's current sound back on its Shorts (their pictures are kept in <film>/flow/short_<name>_pic.mp4), and
print each film's loudness, peak, and the level of the music in the gaps between lines, minute by minute."""
import json
import subprocess

import numpy as np
import soundfile as sf

SH = {"lf01_escape": ("LF01_FLOW_v7.mp4", {"escape": ("open_00", "open_07"), "talk": ("board_02", "board_07"), "cheat": ("why_00", "why_08")}),
      "lf02_price": ("LF02_FLOW_v6.mp4", {"war": ("open_00", "open_05"), "bigmac": ("bigmac_00", "bigmac_07"), "jevons": ("paradox_00", "paradox_06")}),
      "lf03_held": ("LF03_FLOW_v4.mp4", {"held": ("open_00", "open_05"), "test": ("test_00", "test_07"), "knew": ("knew_00", "knew_06")})}
for F, (f, shorts) in SH.items():
    L = json.load(open(f"{F}/flow/lines.json"))["lines"]
    by = {l["id"]: l for l in L}
    for name, (a, b) in shorts.items():
        t0, t1 = max(0.0, by[a]["start"] - 0.15), by[b]["end"] + 0.5 + 3.4
        d = t1 - t0
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{F}/flow/short_{name}_pic.mp4", "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", f"{F}/{f}", "-map", "0:v", "-map", "1:a",
                        "-af", f"afade=t=in:d=0.25,afade=t=out:st={d - 3.0:.2f}:d=2.9", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{F}/shorts/short_{name}.mp4"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{F}/{f}", "-ac", "1", "-ar", "16000", "/tmp/_t.wav"])
    y, sr = sf.read("/tmp/_t.wav")
    sp = np.zeros(len(y), bool)
    for l in L:
        sp[int(l["start"] * sr):int((l["end"] + 0.05) * sr)] = True
    out = []
    for m in range(0, int(len(y) / sr / 60) + 1):
        a_, b_ = m * 60 * sr, min(len(y), (m + 1) * 60 * sr)
        g = ~sp[a_:b_]
        out.append(f"{m}:{20 * np.log10(np.sqrt((y[a_:b_][g] ** 2).mean()) + 1e-9):.0f}" if g.sum() > sr else f"{m}:--")
    pk = subprocess.run(f"ffmpeg -hide_banner -nostats -i {F}/{f} -af ebur128=peak=true -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2 | tr -s ' ' | tr '\\n' ' '", shell=True, capture_output=True, text=True).stdout
    print(F, pk, "| gaps per minute:", " ".join(out))
