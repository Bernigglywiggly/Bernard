"""The voice for any episode: ElevenLabs George (the user's "very original British voice") at his own speed, 1.0, from
the line cache in lab/voice/cache/eleven (tools/eleven_tts.py fills it; credits are spent once per line). There is no
stand-in: without every line cached and no ELEVENLABS_API_KEY in the environment, it stops.

Pace: the user asked for fast on 28 Sep (George at 1.2, lines nearly touching), then that night: "way too fast... go
back to the original voice speed". So 1.0 with a breath between sentences is the default; EL_SPEED=1.2 rebuilds the
fast cut exactly as it was. Lines sit on an eighth-note grid at 170 BPM; `air` adds half-bars before a line, `cut` a
beat of silence before a reveal. Writes <ep>/build/voice_dry.wav, voice.wav (a touch of cinema room) and lines.json (with
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
SPEED = float(os.environ.get("EL_SPEED", "1.0"))


def script(ep_dir):
    spec = importlib.util.spec_from_file_location("script_" + os.path.basename(ep_dir), os.path.join(ep_dir, "script.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gap(ln, speed):
    """The silence before a line: at 1.0 a breath between sentences and most of a half-bar per unit of air; the 1.2
    cut had almost none (air halved)."""
    air = ln.get("air", 0)
    if speed > 1.1:
        return 0.06 + (air if ln.get("drop") else math.ceil(air / 2)) * HB + (0.25 if ln.get("cut") else 0.0)
    return 0.30 + 0.75 * air * HB + (0.35 if ln.get("cut") else 0.0)


def trim(a, thresh=0.004):
    idx = np.nonzero(np.abs(a) > thresh)[0]
    return (a[max(0, idx[0] - 240): idx[-1] + 1800], max(0, idx[0] - 240)) if len(idx) else (a, 0)


def build(ep_dir, lead=LEAD, speed=SPEED, voice=None):
    """voice: a name in eleven_tts.VOICES (or an id); EL_VOICE, else George. EP_BUILD names the build folder, so a
    variant (EP_BUILD=build_elder EL_VOICE=elder) never touches the main cut."""
    ep_dir = os.path.abspath(ep_dir)
    vname = voice or os.environ.get("EL_VOICE", "george")
    vid = el.VOICES.get(vname, vname)
    out = os.path.join(ep_dir, os.environ.get("EP_BUILD", "build"))
    os.makedirs(out, exist_ok=True)
    lines = script(ep_dir).LINES
    sp = os.path.join(out, "slots.json")
    slots = json.load(open(sp)) if os.path.exists(sp) else {}
    texts = [el.spoken(x, slots) for x in lines]
    missing = [t for t in texts if el.cached(t, voice=vid, speed=speed)[0] is None]
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if missing and not key:
        sys.exit(f"{len(missing)} lines aren't in the George cache and there's no ELEVENLABS_API_KEY: nothing built")
    prev_end, clips, meta = lead, [], []
    for i, ln in enumerate(lines):
        shown = slots[ln["slot"]].strip() if ln.get("slot") and (slots.get(ln["slot"]) or "").strip() else ln["text"]
        (y, sr), al = el.synth(texts[i], key, voice=vid, speed=speed, prev=texts[i - 1] if i else None,
                               nxt=texts[i + 1] if i + 1 < len(texts) else None)
        y = fx.resample(y.astype(np.float32), sr)
        y, off = trim(y)
        w = el.words_from_alignment(al, texts[i])
        start = max(lead, prev_end + gap(ln, speed))
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
    json.dump(dict(total=round(total, 3), bpm=BPM, engine="eleven", voice=vname, speed=speed, lines=meta),
              open(os.path.join(out, "lines.json"), "w"), indent=1)
    print("total", round(total, 2))
    return total


if __name__ == "__main__":
    build(os.path.join(engine.LAB, sys.argv[1]) if not os.path.isdir(sys.argv[1]) else sys.argv[1])
