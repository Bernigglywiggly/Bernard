"""The score: one bed per chapter, cut to the chapter's length in bars, starting on its title card and crossfading into
the next (2 Oct). The 1920s caper (beds.caper) carries the cons; the dark synth-orchestral bed (mainframe) the cold
open and Capone; deep house (deep_field) the counterfeiting; the calm night drive the arrest; chrome_marl the tower
and the prison years; terminal the modern scams. Writes build/beds/<chapter>.wav and build/music.json for film.py.

    python3 music.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, "music"))
import audio_fx as fx  # noqa: E402
import beds  # noqa: E402

# chapter -> (bed, bpm, key or None, gain dB)
PLAN = {
    "open": ("mainframe", 104, None, 0.0),
    "boy": ("caper", 118, 0, 0.0),
    "box": ("caper", 118, 3, 0.0),
    "tower": ("chrome_marl", 72, None, 1.0),
    "sale": ("caper", 118, 0, 0.0),
    "back": ("caper", 118, -2, -1.0),
    "capone": ("mainframe", 104, None, 0.0),
    "money": ("deep_field", 112, -3, -1.0),
    "locker": ("night_drive", 108, None, 0.0),
    "escape": ("caper", 118, 2, 0.0),
    "rock": ("chrome_marl", 72, None, 1.0),
    "rules": ("terminal", 96, None, 0.0),
}
XF = 1.5      # seconds a bed runs on under the next one


def plan_for(bed, bars):
    """Sections for `bars` bars, in the names each bed knows."""
    edge = 2 if bars < 24 else 4
    if bed == "night_drive":
        a = (bars - edge) // 2
        return [("intro", edge), ("a", a), ("b", bars - edge - a)]
    if bed == "chrome_marl":
        body = bars - edge - 2
        return [("intro", edge), ("a", body // 2), ("b", body - body // 2), ("out", 2)]
    brk = 2 if bars >= 20 else 0
    body = bars - edge - 2 - brk
    a = math.ceil(body * 0.55)
    out = [("intro", edge), ("a", a)]
    if brk:
        out += [("b", body - a - (body - a) // 3), ("break", brk), ("b", (body - a) // 3)]
    else:
        out += [("b", body - a)]
    out += [("out", 2)]
    return [(n, k) for n, k in out if k > 0]


def main():
    ch = json.load(open(os.path.join(HERE, "build", "chapters.json")))
    cards = [c["card"] for c in ch["chapters"]] + [ch["total"]]
    os.makedirs(os.path.join(HERE, "build", "beds"), exist_ok=True)
    out = []
    for c, t0, t1 in zip(ch["chapters"], cards, cards[1:]):
        bed, bpm, key, gain = PLAN[c["id"]]
        dur = (t1 - t0) + XF
        bars = math.ceil(dur / (240.0 / bpm)) + 1
        plan = plan_for(bed, bars)
        assert sum(k for _, k in plan) == bars, (c["id"], plan, bars)
        path = os.path.join(HERE, "build", "beds", f"{c['id']}.wav")
        if not os.path.exists(path):
            fn = beds.BEDS[bed]
            kw = dict(plan=plan)
            if key is not None:
                kw["key"] = key
            if bed == "night_drive":
                kw["calm"] = True
            x = fn(bpm, **kw)
            fx.save(path, x, mp3=False)
        out.append([round(t0, 3), round(min(ch["total"], t1 + XF), 3), path, gain])
        print(f"{c['id']:7s} {bed:12s} {bpm:4d} bpm {bars:3d} bars {t0:7.2f}-{t1:7.2f}")
    json.dump(out, open(os.path.join(HERE, "build", "music.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
