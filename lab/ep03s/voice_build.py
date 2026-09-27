"""EP03 seamless: the voice at the new pace ("pretty fucking fast"), from the EP03 script.

Engine: ElevenLabs George (the first British guy) whenever lab/voice/cache/eleven has every line at SPEED
(see tools/eleven_tts.py); otherwise a local stand-in so the picture can be timed. Lines sit on an eighth-note
grid at 170 BPM (not the old half-bar grid, which added up to 0.7 s of waiting per line), short gaps, and half
the old air before reveals. Slot lines take the user's punchline from build/slots.json.
Writes build/voice_dry.wav, build/voice.wav, build/lines.json (with word timings when ElevenLabs made them).

    python3 voice_build.py            # auto
    VOICE_ENGINE=kokoro python3 voice_build.py
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "..")
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, "voice"))
sys.path.insert(0, os.path.join(LAB, "tools"))
sys.path.insert(0, os.path.join(LAB, "ep03"))
import audio_fx as fx  # noqa: E402
import eleven_tts as el  # noqa: E402
from script import LINES  # noqa: E402

BUILD = os.path.join(HERE, "build")
BPM = 170.0
HB = 2 * 60.0 / BPM
GRID = HB / 4                                  # an eighth note
LEAD = 1.2
EL_SPEED = float(os.environ.get("EL_SPEED", "1.2"))
KOKORO = ("bm_george", 1.16)
SLOTS_PATH = os.path.join(BUILD, "slots.json")


def trim(a, thresh=0.004):
    idx = np.nonzero(np.abs(a) > thresh)[0]
    return (a[max(0, idx[0] - 240): idx[-1] + 1800], max(0, idx[0] - 240)) if len(idx) else (a, 0)


def main():
    os.makedirs(BUILD, exist_ok=True)
    slots = json.load(open(SLOTS_PATH)) if os.path.exists(SLOTS_PATH) else {}
    texts = [el.spoken(x, slots) for x in LINES]
    engine = os.environ.get("VOICE_ENGINE", "auto")
    have = all(el.cached(t, speed=EL_SPEED)[0] is not None for t in texts)
    if engine == "eleven" or (engine == "auto" and have):
        use = "eleven"
        if not have:
            key = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("VOICE_ENGINE=eleven needs ELEVENLABS_API_KEY or a full cache")
    else:
        use = "kokoro"
        import voice_lab as vl
        k = vl.engine()
    print("voice engine:", use)
    prev_end, clips, meta = LEAD, [], []
    for i, ln in enumerate(LINES):
        text_shown = ln["text"] if not (ln.get("slot") and (slots.get(ln["slot"]) or "").strip()) else slots[ln["slot"]].strip()
        words = None
        if use == "eleven":
            (y, sr), al = el.synth(texts[i], os.environ.get("ELEVENLABS_API_KEY", ""), speed=EL_SPEED,
                                   prev=texts[i - 1] if i else None, nxt=texts[i + 1] if i + 1 < len(texts) else None)
            y = fx.resample(y.astype(np.float32), sr)
            y, off = trim(y)
            w = el.words_from_alignment(al, texts[i])
            if w:
                words = [(wd, round(a - off / fx.SR, 3), round(b - off / fx.SR, 3)) for wd, a, b in w]
        else:
            y, _ = trim(vl.say(k, texts[i], KOKORO[0], speed=KOKORO[1], pause=0.16))
        air = ln.get("air", 0)
        air = air if ln.get("drop") else math.ceil(air / 2)
        gap = 0.06 + air * HB + (0.25 if ln.get("cut") else 0.0)
        start = max(LEAD, prev_end + gap)
        start = math.ceil((start - LEAD) / GRID - 1e-6) * GRID + LEAD
        end = start + len(y) / fx.SR
        clips.append((start, y))
        meta.append(dict(i=i, floor=ln["floor"], text=text_shown, start=round(start, 3), end=round(end, 3),
                         card=ln.get("card"), mark=ln.get("mark"), id=ln.get("id"), slot=ln.get("slot"),
                         cut=bool(ln.get("cut")), drop=bool(ln.get("drop")), quiet=bool(ln.get("quiet")),
                         words=[(wd, round(start + a, 3), round(start + b, 3)) for wd, a, b in words] if words else None))
        prev_end = end
        print(f"{i:2d} F{ln['floor']} {start:6.2f}-{end:6.2f} {text_shown[:64]}")
    total = prev_end + 3.0
    dry = np.zeros(int(total * fx.SR), np.float32)
    for s, y in clips:
        dry[int(s * fx.SR): int(s * fx.SR) + len(y)] += y
    fx.save(os.path.join(BUILD, "voice_dry.wav"), dry, mp3=False)
    room = fx.cinema_ir(rt60=1.4, predelay=0.02, seed=5, dark=0.6)
    wet = fx.chain_voice(dry, room=room, room_wet=-16.0, target=-16.0)
    fx.save(os.path.join(BUILD, "voice.wav"), wet, mp3=False)
    json.dump(dict(total=round(total, 3), bpm=BPM, engine=use, lines=meta), open(os.path.join(BUILD, "lines.json"), "w"), indent=1)
    print("total", round(total, 2))


if __name__ == "__main__":
    main()
