"""An estimated timeline for an episode that isn't voiced yet, so its scenes can be drawn and checked before the
voice exists: each line's length from its word count at George's measured pace, the same gaps and grid as
engine.voice, and word times spread by word length. Writes <ep>/build_est/lines.json only (never build/), with
engine="estimate" so nothing mistakes it for a real voice. No audio is made.

    python3 tools/est_timeline.py ep13
    python3 tools/est_timeline.py ch2/ep01 2.1           # Curve Elder A's pace (~125 wpm with pauses: 2.1 words/s)
    EP_BUILD=build_est python3 ep13/film.py lines 12.5 30     # quick line-art stills on the estimate
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine  # noqa: E402,F401  (paths)
import eleven_tts as el  # noqa: E402
from engine import voice  # noqa: E402

WPS = 2.55                      # George at speed 1.0: EP05-EP12 run ~140-155 words a minute with their pauses


def build(ep_dir, wps=WPS):
    lines = voice.script(ep_dir).LINES
    out = os.path.join(ep_dir, "build_est")
    os.makedirs(out, exist_ok=True)
    prev_end, meta = voice.LEAD, []
    for i, ln in enumerate(lines):
        spoken = el.spoken(ln, {}).split()
        dur = 0.35 + len(spoken) / wps
        start = max(voice.LEAD, prev_end + voice.gap(ln, 1.0))
        start = math.ceil((start - voice.LEAD) / voice.GRID - 1e-6) * voice.GRID + voice.LEAD
        end = start + dur
        weights = [max(2, len(w)) for w in spoken]
        tot, acc, words = sum(weights), 0.0, []
        for w, k in zip(spoken, weights):
            a = start + 0.15 + (dur - 0.3) * acc / tot
            acc += k
            words.append((w, round(a, 3), round(start + 0.15 + (dur - 0.3) * acc / tot, 3)))
        meta.append(dict(i=i, floor=ln["floor"], text=ln["text"], start=round(start, 3), end=round(end, 3), card=ln.get("card"),
                         id=ln.get("id"), slot=None, cut=bool(ln.get("cut")), air=ln.get("air", 0), words=words))
        prev_end = end
    total = prev_end + 3.0
    json.dump(dict(total=round(total, 3), bpm=voice.BPM, engine="estimate", voice=None, speed=1.0, lines=meta),
              open(os.path.join(out, "lines.json"), "w"), indent=1)
    print(os.path.join(out, "lines.json"), f"{total:.1f}s (estimated)")


if __name__ == "__main__":
    build(os.path.join(engine.LAB, sys.argv[1]), float(sys.argv[2]) if len(sys.argv) > 2 else WPS)
