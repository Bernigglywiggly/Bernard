"""A voice audition (1 Oct, the user: "we want the narration to feel very floaty and sort of very human-like and
natural... maybe try female too"). One passage per voice, read in ONE request, so the model carries the intonation from
sentence to sentence the way a person reading aloud does (the films are voiced line by line, which is where the joins
came from), over the house bed, as MP3s in lab/out/voice/audition/ to compare.

    ELEVENLABS_API_KEY=... python3 tools/voice_audition.py                   # EP05's opening: George, Lily, Alice, Sarah
    ELEVENLABS_API_KEY=... python3 tools/voice_audition.py ep08 lily matilda # another opening, other voices
About 600 characters of credits per voice, once: the results are cached like every line.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import engine  # noqa: E402,F401  (paths)
import audio_fx as fx  # noqa: E402
import beds  # noqa: E402
import eleven_tts as el  # noqa: E402
from engine import voice as V  # noqa: E402


def passage(ep, secs=40.0, wps=2.4):
    """The film's opening lines, about secs long, as one text."""
    out, words = [], 0
    for ln in V.script(os.path.join(engine.LAB, ep)).LINES:
        t = el.spoken(ln, {})
        out.append(t)
        words += len(t.split())
        if words / wps >= secs:
            break
    return " ".join(out)


def main():
    args = sys.argv[1:]
    ep = args[0] if args and args[0].startswith("ep") else "ep05"
    names = [a for a in args if not a.startswith("ep")] or ["george", "lily", "alice", "sarah"]
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    text = passage(ep)
    outdir = os.path.join(engine.LAB, "out", "voice", "audition")
    os.makedirs(outdir, exist_ok=True)
    room = fx.cinema_ir(rt60=1.4, predelay=0.02, seed=5, dark=0.6)
    for name in names:
        vid = el.VOICES.get(name, name)
        if el.cached(text, voice=vid)[0] is None and not key:
            sys.exit(f"no ELEVENLABS_API_KEY in the environment, and the passage isn't cached for {name}")
        (y, sr), _ = el.synth(text, key, voice=vid)
        y = np.pad(fx.resample(y.astype(np.float32), sr), (int(1.5 * fx.SR), int(2.5 * fx.SR)))
        v = fx.chain_voice(y, room=room, room_wet=-16.0, target=-16.0)
        v = v if v.ndim == 2 else np.stack([v, v], 1)
        bars = int(np.ceil(len(v) / fx.SR / (240 / 124))) + 1
        bed = np.asarray(beds.house(124, [("intro", 1), ("a", max(1, bars - 3)), ("out", 2)]), np.float32)
        bed = np.pad(bed, ((0, max(0, len(v) - len(bed))), (0, 0)))[:len(v)]
        bed = bed * fx.db(-29.0 - fx.lufs(bed))
        p = fx.save(os.path.join(outdir, f"{ep}_{name}.wav"), fx.master(v + bed, target=-14.0, ceiling_db=-1.0), br="192k")
        print(name, round(len(v) / fx.SR, 1), "s ->", p)


if __name__ == "__main__":
    main()
