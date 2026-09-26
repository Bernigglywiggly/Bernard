"""Voice lab: audition local (Kokoro, Apache-2.0) voices and blends for an "exo gunslinger" archetype
(wry, relaxed, American, a smile in the voice), then run the pick through the exo colour and the
cinema room. Nothing here clones a real person: the character is built from blends of stock voices.

    python3 voice_lab.py audition      # out/voice/audition_*.mp3 and one reel
    python3 voice_lab.py final VOICE   # out/voice/exo_{dry,light,cinema}.mp3 for a chosen voice/blend
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import audio_fx as fx  # noqa: E402

KOKORO = os.environ.get("KOKORO_DIR", "/opt/kokoro")
OUT = os.path.join(os.path.dirname(__file__), "..", "out", "voice")

LINE = ("Alright. Pull up a chair. Here's the thing nobody tells you about the future. "
        "It doesn't show up all at once. It compounds. "
        "And the people who notice early? They don't get lucky. They just got here first.")

LONG = ("Alright. Pull up a chair, because this part's fun. "
        "In nineteen fifty-six, a handful of scientists gave themselves one summer to teach machines to think. "
        "It took them seventy years. "
        "Then the gaps started shrinking. Decades. Then years. Then months. "
        "This week, two labs shipped new models ninety minutes apart. Ninety minutes. "
        "That's not a trend line, my friend. That's a launch ramp. "
        "And you're standing right at the bottom of it, holding a coffee, deciding whether to climb.")

CANDIDATES = {
    "michael": "am_michael",
    "puck": "am_puck",
    "fenrir": "am_fenrir",
    "eric": "am_eric",
    "liam": "am_liam",
    "onyx": "am_onyx",
    "echo": "am_echo",
    "michael+puck": {"am_michael": 0.6, "am_puck": 0.4},
    "fenrir+puck": {"am_fenrir": 0.55, "am_puck": 0.45},
    "michael+onyx": {"am_michael": 0.6, "am_onyx": 0.4},
    "eric+fenrir": {"am_eric": 0.5, "am_fenrir": 0.5},
}


def engine():
    from kokoro_onnx import Kokoro
    return Kokoro(os.path.join(KOKORO, "kokoro-v1.0.onnx"), os.path.join(KOKORO, "voices-v1.0.bin"))


def voice_of(k, spec):
    if isinstance(spec, str) and "+" not in spec and spec in CANDIDATES:
        spec = CANDIDATES[spec]
    elif isinstance(spec, str) and spec in CANDIDATES:
        spec = CANDIDATES[spec]
    if isinstance(spec, str):
        return spec
    v = sum(k.get_voice_style(name) * w for name, w in spec.items())
    return v.astype(np.float32)


def say(k, text, spec, speed=1.0, pause=0.32):
    a, sr = k.create(text, voice=voice_of(k, spec), speed=speed, lang="en-us", sentence_pause=pause, clause_pause=0.12)
    return fx.resample(a.astype(np.float32), sr)


def audition():
    k = engine()
    reel = []
    tick = np.zeros(int(0.5 * fx.SR), np.float32)
    tick[:300] = np.sin(2 * np.pi * 1800 * np.arange(300) / fx.SR) * np.linspace(0.3, 0, 300)
    for name, spec in CANDIDATES.items():
        a = say(k, LINE, spec, speed=0.96)
        y = fx.chain_voice(a, exo_amt=0.0, room=None, target=-16)
        fx.save(os.path.join(OUT, f"audition_{name.replace('+', '_')}.wav"), y)
        reel += [np.stack([tick, tick], 1), y, np.zeros((int(0.4 * fx.SR), 2), np.float32)]
        print("done", name, round(len(a) / fx.SR, 1), "s")
    fx.save(os.path.join(OUT, "audition_reel.wav"), np.concatenate(reel))
    print("order:", ", ".join(CANDIDATES))


def final(spec, speed=0.95):
    tag = spec.replace("+", "_")
    k = engine()
    a = say(k, LONG, spec, speed=speed, pause=0.38)
    room = fx.cinema_ir(rt60=3.4, predelay=0.055)
    variants = {
        "dry": dict(exo_amt=0.0, room=None),
        "exo_light": dict(exo_amt=0.45, room=None),
        "exo_cinema": dict(exo_amt=0.45, room=room, room_wet=-7.5),
        "clean_cinema": dict(exo_amt=0.0, room=room, room_wet=-8.5),
        "exo_heavy_cinema": dict(exo_amt=0.9, room=room, room_wet=-7.0),
    }
    for name, kw in variants.items():
        y = fx.chain_voice(a, **kw)
        fx.save(os.path.join(OUT, f"{tag}_{name}.wav"), y)
        print("wrote", name)


if __name__ == "__main__":
    if sys.argv[1] == "audition":
        audition()
    else:
        final(sys.argv[2] if len(sys.argv) > 2 else "michael+puck")
