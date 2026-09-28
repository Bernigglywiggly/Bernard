"""The voice for any episode: ElevenLabs George at speed 1.2 (the user's "very original British voice"), from the line
cache in lab/voice/cache/eleven (tools/eleven_tts.py fills it; credits are spent once per line). There is no stand-in:
without every line cached and no ELEVENLABS_API_KEY in the environment, it stops.

Lines sit on an eighth-note grid at 170 BPM with short gaps; `air` adds half-bars before a line, `cut` a beat of
silence before a reveal. Writes <ep>/build/voice_dry.wav, voice.wav (a touch of cinema room) and lines.json (with
George's word timings, for the captions and for scenes that sync to a word).

    python3 -m engine.voice ep04          # from lab/
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

import engine  # noqa: F401  (paths)
import audio_fx as fx  # noqa: E402
import eleven_tts as el  # noqa: E402

BPM = 170.0
HB = 2 * 60.0 / BPM
GRID = HB / 4
LEAD = 1.2
SPEED = float(os.environ.get("EL_SPEED", "1.2"))


def script(ep_dir):
    spec = importlib.util.spec_from_file_location("script_" + os.path.basename(ep_dir), os.path.join(ep_dir, "script.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def trim(a, thresh=0.004):
    idx = np.nonzero(np.abs(a) > thresh)[0]
    return (a[max(0, idx[0] - 240): idx[-1] + 1800], max(0, idx[0] - 240)) if len(idx) else (a, 0)


def build(ep_dir, lead=LEAD, speed=SPEED):
    ep_dir = os.path.abspath(ep_dir)
    out = os.path.join(ep_dir, "build")
    os.makedirs(out, exist_ok=True)
    lines = script(ep_dir).LINES
    sp = os.path.join(out, "slots.json")
    slots = json.load(open(sp)) if os.path.exists(sp) else {}
    texts = [el.spoken(x, slots) for x in lines]
    missing = [t for t in texts if el.cached(t, speed=speed)[0] is None]
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if missing and not key:
        sys.exit(f"{len(missing)} lines aren't in the George cache and there's no ELEVENLABS_API_KEY: nothing built")
    prev_end, clips, meta = lead, [], []
    for i, ln in enumerate(lines):
        shown = slots[ln["slot"]].strip() if ln.get("slot") and (slots.get(ln["slot"]) or "").strip() else ln["text"]
        (y, sr), al = el.synth(texts[i], key, speed=speed, prev=texts[i - 1] if i else None,
                               nxt=texts[i + 1] if i + 1 < len(texts) else None)
        y = fx.resample(y.astype(np.float32), sr)
        y, off = trim(y)
        w = el.words_from_alignment(al, texts[i])
        air = ln.get("air", 0)
        air = air if ln.get("drop") else math.ceil(air / 2)
        gap = 0.06 + air * HB + (0.25 if ln.get("cut") else 0.0)
        start = max(lead, prev_end + gap)
        start = math.ceil((start - lead) / GRID - 1e-6) * GRID + lead
        end = start + len(y) / fx.SR
        clips.append((start, y))
        words = [(wd, round(start + a - off / fx.SR, 3), round(start + b - off / fx.SR, 3)) for wd, a, b in w] if w else None
        meta.append(dict(i=i, floor=ln["floor"], text=shown, start=round(start, 3), end=round(end, 3), card=ln.get("card"),
                         id=ln.get("id"), slot=ln.get("slot"), cut=bool(ln.get("cut")), air=ln.get("air", 0), words=words))
        prev_end = end
        print(f"{i:2d} F{ln['floor']} {start:6.2f}-{end:6.2f} {shown[:70]}")
    total = prev_end + 3.0
    dry = np.zeros(int(total * fx.SR), np.float32)
    for s, y in clips:
        dry[int(s * fx.SR): int(s * fx.SR) + len(y)] += y
    fx.save(os.path.join(out, "voice_dry.wav"), dry, mp3=False)
    room = fx.cinema_ir(rt60=1.4, predelay=0.02, seed=5, dark=0.6)
    wet = fx.chain_voice(dry, room=room, room_wet=-16.0, target=-16.0)
    fx.save(os.path.join(out, "voice.wav"), wet, mp3=False)
    json.dump(dict(total=round(total, 3), bpm=BPM, engine="eleven", speed=speed, lines=meta),
              open(os.path.join(out, "lines.json"), "w"), indent=1)
    print("total", round(total, 2))
    return total


if __name__ == "__main__":
    build(os.path.join(engine.LAB, sys.argv[1]) if not os.path.isdir(sys.argv[1]) else sys.argv[1])
