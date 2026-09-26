"""Jungle beds, synthesised from nothing (no breaks sampled, so nothing to license or get claimed).

170 BPM. A home-made break (kick, crunchy snare with ghosts, hats and a ride), chopped and rolled at
phrase ends; a rolling sub that glides between roots; a reese for the darker sections; F-minor pads
(Fm9 -> Dbmaj7 -> Bbm9 -> C7sus4) through a big room; an FM Rhodes for the liquid flavour.

Arrangements are lists of (section, bars). Stems are written separately so the video mix can duck
the music under the voice and drop the drums out for a vortex moment.

    python3 jungle.py                       # three demo beds: liquid, rollers, dark
    python3 jungle.py --arr pilot.json      # a custom arrangement
"""
import argparse
import json
import os
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import audio_fx as fx  # noqa: E402

SR = fx.SR
BPM = 170.0
BEAT = 60.0 / BPM
STEP = BEAT / 4
BAR = BEAT * 4
OUT = os.path.join(os.path.dirname(__file__), "..", "out", "music")


def T(d):
    return np.arange(int(d * SR)) / SR


def place(dst, src, at):
    i = int(round(at * SR))
    if i < 0:
        src, i = src[-i:], 0
    j = min(len(dst), i + len(src))
    if j > i:
        dst[i:j] += src[: j - i]


def polyblep(t, dt):
    y = np.zeros_like(t)
    m = t < dt
    x = t[m] / dt[m]
    y[m] = x + x - x * x - 1
    m = t > 1 - dt
    x = (t[m] - 1) / dt[m]
    y[m] = x * x + x + x + 1
    return y


def saw(freq, n, phase0=0.0):
    f = np.broadcast_to(np.asarray(freq, np.float64), (n,))
    dt = f / SR
    t = (phase0 + np.cumsum(dt)) % 1.0
    return (2 * t - 1 - polyblep(t, dt)).astype(np.float32)


def sine_f(freq, n, phase0=0.0):
    f = np.broadcast_to(np.asarray(freq, np.float64), (n,))
    return np.sin(2 * np.pi * np.cumsum(f) / SR + phase0).astype(np.float32)


def sat(x, d=1.5):
    return (np.tanh(x * d) / np.tanh(d)).astype(np.float32)


# ---------------------------------------------------------------- the kit
class Kit:
    def __init__(self, seed=5, flavour="liquid"):
        self.r = np.random.default_rng(seed)
        self.flavour = flavour

    def kick(self, v=1.0):
        t = T(0.32)
        f = 48 + 115 * np.exp(-t / 0.028)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.11 if self.flavour == "liquid" else 0.14))
        cl = fx.bq(self.r.normal(0, 1, len(t)).astype(np.float32), "hp", 2500) * np.exp(-t / 0.0015) * 0.35
        return sat((y + cl) * v * 1.1, 1.6)

    def snare(self, v=1.0, ghost=False, pitch=1.0):
        t = T(0.3 if not ghost else 0.14)
        body = (np.sin(2 * np.pi * 188 * pitch * t) * np.exp(-t / 0.045) * 0.7 +
                np.sin(2 * np.pi * 332 * pitch * t) * np.exp(-t / 0.03) * 0.45)
        nz = self.r.normal(0, 1, len(t)).astype(np.float32)
        nz = fx.bq(fx.bq(fx.bq(nz, "hp", 1500), "peak", 3400, q=0.8, gain_db=2.5), "lp", 8500)
        tail = nz * np.exp(-t / (0.11 if not ghost else 0.045)) * 0.9
        crack = fx.bq(self.r.normal(0, 1, len(t)).astype(np.float32), "hp", 3500) * np.exp(-t / 0.002) * 0.8
        y = body + tail + crack
        return sat(y * v * (0.4 if ghost else 1.0) * 1.3, 2.2 if self.flavour != "liquid" else 1.6)

    def hat(self, v=1.0, open_=False):
        d = 0.2 if open_ else 0.035
        t = T(d + 0.02)
        metal = sum(signal.square(2 * np.pi * f * t) for f in (317, 478, 563, 796, 1011, 1370)) / 6
        nz = self.r.normal(0, 1, len(t))
        y = fx.bq(fx.bq((metal * 0.6 + nz * 0.5).astype(np.float32), "hp", 6500), "lp", 10500)
        return (y * np.exp(-t / (d * 0.45)) * v * 0.38).astype(np.float32)

    def ride(self, v=1.0):
        t = T(0.9)
        parts = [(3150, 0.5), (4120, 0.4), (5290, 0.3), (6710, 0.25), (8080, 0.2), (2370, 0.25)]
        y = sum(a * np.sin(2 * np.pi * f * t + self.r.uniform(0, 6)) for f, a in parts)
        nz = fx.bq(self.r.normal(0, 1, len(t)).astype(np.float32), "hp", 6000) * 0.25
        y = (y * 0.35 + nz) * np.exp(-t / 0.28)
        y[: int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
        return (fx.bq(fx.bq(y.astype(np.float32), "hp", 2000), "lp", 8500) * v * 0.17).astype(np.float32)

    def rev_snare(self):
        s = self.snare(1.0)
        s = np.concatenate([s, np.zeros(int(0.3 * SR), np.float32)])
        room = fx.cinema_ir(rt60=1.2, predelay=0.01, seed=21)
        w = fx.convolve(s, room).mean(1)[: int(0.55 * SR)]
        return (w[::-1] * 0.8).astype(np.float32)


# ---------------------------------------------------------------- patterns (16 steps per bar; value = velocity)
PAT = {
    "roll":  {"k": {0: 1, 10: .9}, "s": {4: 1, 12: 1}, "g": {7: .5, 9: .55, 14: .4, 15: .6},
              "h": {i: (.6 if i % 4 == 2 else .35) for i in range(0, 16, 2)}, "o": {6: .5}},
    "amen":  {"k": {0: 1, 2: .85, 10: .95, 11: .8}, "s": {4: 1, 12: 1}, "g": {7: .6, 9: .65, 15: .6},
              "r": {i: .7 for i in range(0, 16, 2)}},
    "amen2": {"k": {0: 1, 2: .85, 10: .95}, "s": {4: 1, 14: 1}, "g": {7: .6, 9: .65},
              "r": {i: .7 for i in range(0, 16, 2)}, "o": {10: .6}},
    "fill":  {"k": {0: 1, 3: .8, 10: .9}, "s": {4: 1, 7: .8, 9: .8}, "g": {},
              "roll": 12, "r": {i: .6 for i in range(0, 12, 2)}},
    "half":  {"k": {0: 1}, "s": {8: 1}, "g": {14: .35}, "r": {i: .5 for i in range(0, 16, 2)}},
    "ride":  {"r": {i: .55 for i in range(0, 16, 2)}, "h": {i: .25 for i in range(1, 16, 2)}},
    "none":  {},
}

# bar-by-bar pattern choice per section; the last bar of every 4 or 8 turns into a fill
SECTION = {
    "intro":  lambda i: "ride",
    "build":  lambda i: "half" if i % 4 != 3 else "fill",
    "full":   lambda i: ("fill" if i % 8 == 7 else ("amen2" if i % 4 == 3 else ("amen" if (i // 2) % 2 else "roll"))),
    "roller": lambda i: ("fill" if i % 8 == 7 else "roll"),
    "break":  lambda i: "none",
    "drop":   lambda i: "none",
    "outro":  lambda i: "ride" if i < 2 else "none",
    "coda":   lambda i: "ride" if i < 4 else "none",
}

# the harmony: (chord, bars); roots for the sub (Hz) and pad voicings (Hz)
PROG = [
    ("Fm9", 2, 43.65, [174.61, 207.65, 261.63, 311.13, 392.00]),
    ("Dbmaj7", 2, 69.30, [138.59, 174.61, 207.65, 261.63, 349.23]),
    ("Bbm9", 2, 58.27, [116.54, 138.59, 174.61, 207.65, 261.63]),
    ("C7sus4", 2, 65.41, [130.81, 174.61, 196.00, 233.08, 293.66]),
]


def chord_at(bar):
    b = bar % sum(p[1] for p in PROG)
    for name, n, root, notes in PROG:
        if b < n:
            return name, root, notes
        b -= n


# ---------------------------------------------------------------- layers
def drums(arr, kit, swing=0.06):
    total = sum(n for _, n in arr) * BAR + 2
    y = np.zeros(int(total * SR), np.float32)
    r = kit.r
    bar = 0
    for sec, n in arr:
        for i in range(n):
            p = PAT[SECTION.get(sec, lambda _: "none")(i)]
            t0 = bar * BAR
            for step in range(16):
                sw = swing * STEP if step % 2 else 0.0
                at = t0 + step * STEP + sw + r.normal(0, 0.0018)
                if step in p.get("k", {}):
                    place(y, kit.kick(p["k"][step] * r.uniform(.9, 1.0)), at)
                if step in p.get("s", {}):
                    place(y, kit.snare(p["s"][step] * r.uniform(.92, 1.0), pitch=r.uniform(.99, 1.02)), at)
                if step in p.get("g", {}):
                    place(y, kit.snare(p["g"][step] * r.uniform(.8, 1.0), ghost=True, pitch=1.04), at)
                if step in p.get("h", {}):
                    place(y, kit.hat(p["h"][step] * r.uniform(.8, 1.0)), at)
                if step in p.get("o", {}):
                    place(y, kit.hat(p["o"][step], open_=True), at)
                if step in p.get("r", {}):
                    place(y, kit.ride(p["r"][step] * r.uniform(.85, 1.0)), at)
            if "roll" in p:                                  # 32nd-note snare roll, rising
                s0 = p["roll"]
                for k in range(int((16 - s0) * 2)):
                    place(y, kit.snare(0.45 + 0.5 * k / ((16 - s0) * 2), ghost=k % 2 == 1, pitch=1 + 0.03 * k), t0 + s0 * STEP + k * STEP / 2)
            # reverse snare into the next section (last bar of a section only)
            if i == n - 1 and sec in ("build", "break", "drop", "intro"):
                rs = kit.rev_snare()
                place(y, rs, t0 + BAR - len(rs) / SR)
            bar += 1
    # bus: parallel squash + crunch + gentle 12-bit grit + a short room
    squash = fx.compress(y, thresh_db=-28, ratio=6, att=0.002, rel=0.08, makeup_db=10)
    bus = y * 0.8 + squash * 0.35
    bus = sat(bus * 1.2, 1.4)
    grit = np.round(bus * 2048) / 2048
    bus = bus * 0.85 + grit * 0.15
    bus = fx.bq(fx.bq(bus, "hp", 38), "hshelf", 8000, gain_db=-5.0)
    rm = fx.cinema_ir(rt60=0.45, predelay=0.006, seed=2, dark=0.7)
    wet = fx.convolve(bus, rm).mean(1)[: len(bus)]
    return (bus + fx.bq(wet, "hp", 300) * 0.12).astype(np.float32)


def sub_line(arr, glide_s=0.09):
    bars = sum(n for _, n in arr)
    n = int((bars * BAR + 2) * SR)
    f = np.zeros(n)
    amp = np.zeros(n, np.float32)
    bar = 0
    for sec, nb in arr:
        for i in range(nb):
            _, root, _ = chord_at(bar)
            a, b = int(bar * BAR * SR), int((bar + 1) * BAR * SR)
            f[a:b] = root
            on = sec not in ("intro", "outro") or (sec == "outro" and i < 2)
            amp[a:b] = 1.0 if on else 0.0
            if sec == "break":
                amp[a:b] = 0.8
            bar += 1
    # glide between roots (one-pole in the log domain), smooth the gate
    lf = np.log(np.maximum(f, 1))
    k = np.exp(-1 / (glide_s * SR))
    lf = signal.lfilter([1 - k], [1, -k], lf, zi=[lf[0] * k])[0]
    f = np.exp(lf)
    ka = np.exp(-1 / (0.03 * SR))
    amp = signal.lfilter([1 - ka], [1, -ka], amp).astype(np.float32)
    y = sine_f(f, n) * amp
    y = sat(y * 1.3, 1.5) * 0.9                       # a touch of 2nd/3rd harmonic for small speakers
    return fx.bq(y, "lp", 180).astype(np.float32)


def reese(arr, sections=("full", "roller")):
    bars = sum(n for _, n in arr)
    n = int((bars * BAR + 2) * SR)
    f = np.zeros(n)
    gate = np.zeros(n, np.float32)
    bar = 0
    for sec, nb in arr:
        for i in range(nb):
            _, root, _ = chord_at(bar)
            a, b = int(bar * BAR * SR), int((bar + 1) * BAR * SR)
            f[a:b] = root * 2
            gate[a:b] = 1.0 if sec in sections else 0.0
            bar += 1
    ka = np.exp(-1 / (0.05 * SR))
    gate = signal.lfilter([1 - ka], [1, -ka], gate).astype(np.float32)
    y = saw(f * 1.0042, n) + saw(f * 0.9958, n, 0.37) + 0.5 * saw(f * 0.5, n, 0.11)
    y = fx.bq(fx.bq(sat(y * 0.8, 2.0), "lp", 520, q=0.9), "lp", 900)
    y = fx.bq(y, "hp", 70)
    return (y * gate * 0.35).astype(np.float32)


def pads(arr, room):
    bars = sum(n for _, n in arr)
    n = int((bars * BAR + 3) * SR)
    y = np.zeros(n, np.float32)
    bar = 0
    rng = np.random.default_rng(9)
    for sec, nb in arr:
        for i in range(nb):
            name, _, notes = chord_at(bar)
            if bar % 2 == 0 and sec not in ("outro",) or (sec == "outro" and i == 0):
                dur = 2 * BAR + 1.2
                m = int(dur * SR)
                t = T(dur)
                e = np.minimum(1, t / 0.9) * np.minimum(1, np.maximum(0, (dur - t) / 1.2)) ** 1.5
                ch = np.zeros(m, np.float32)
                for f in notes:
                    for c in (-7, 0, 7):
                        ch += saw(f * 2 ** (c / 1200), m, rng.uniform()) * (0.6 if c else 0.8)
                lfo = 1300 + 500 * np.sin(2 * np.pi * 0.11 * t + bar)
                ch = fx.bq(ch, "lp", 1500, q=0.6)
                ch = ch * (0.85 + 0.15 * (lfo / 1800))
                level = 0.9 if sec in ("break", "intro", "drop") else 0.6
                place(y, ch * e * level / (len(notes) * 3), bar * BAR)
            bar += 1
    y = fx.bq(y, "hp", 110)
    wet = fx.convolve(y, room)[: len(y)]
    return (fx.stereo(y) * 0.55 + fx.bq(wet, "hp", 180) * 0.9).astype(np.float32)


def rhodes(arr, room, sections=("full", "break", "roller", "intro", "coda")):
    """FM electric piano: a 1:1 body with a decaying index and a 14:1 tine for the attack; syncopated stabs."""
    bars = sum(n for _, n in arr)
    n = int((bars * BAR + 3) * SR)
    y = np.zeros(n, np.float32)
    rng = np.random.default_rng(12)
    rhythm = [0, 6, 10]               # 16th steps within a 2-bar phrase where chords land
    bar = 0
    for sec, nb in arr:
        for i in range(nb):
            if sec in sections and bar % 2 == 0:
                _, _, notes = chord_at(bar)
                for s in rhythm:
                    at = bar * BAR + s * STEP
                    dur = 1.4
                    t = T(dur)
                    for f in notes[1:]:
                        f2 = f * 2
                        idx = 1.6 * np.exp(-t / 0.35)
                        mod = np.sin(2 * np.pi * f2 * t) * idx
                        tine = np.sin(2 * np.pi * f2 * 14 * t) * 0.15 * np.exp(-t / 0.02)
                        v = np.sin(2 * np.pi * f2 * t + mod + tine) * np.exp(-t / 0.6)
                        place(y, (v * 0.06 * rng.uniform(.8, 1.0)).astype(np.float32), at + rng.normal(0, 0.004))
            bar += 1
    trem = 0.5 + 0.5 * np.sin(2 * np.pi * 3.8 * np.arange(n) / SR)
    st = np.stack([y * (0.6 + 0.4 * trem), y * (0.6 + 0.4 * (1 - trem))], 1)
    wet = fx.convolve(st.mean(1), room)[: n]
    return (st + fx.bq(wet, "hp", 250) * 0.5).astype(np.float32)


def air(arr):
    bars = sum(n for _, n in arr)
    n = int((bars * BAR + 3) * SR)
    rng = np.random.default_rng(4)
    nz = rng.normal(0, 1, (n, 2)).astype(np.float32)
    nz = fx.bq(fx.bq(nz, "bp", 2400, q=0.4), "lp", 7000)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * np.arange(n) / SR)
    return (nz * lfo[:, None] * 0.012).astype(np.float32)


# ---------------------------------------------------------------- render
LEVELS = {   # stem loudness targets (LUFS) before the master; the balance is the style
    "liquid": {"drums": -17.0, "sub": -19.5, "pads": -22.5, "keys": -24.5, "air": -44.0},
    "rollers": {"drums": -16.0, "sub": -18.5, "pads": -27.0, "reese": -21.0, "air": -46.0},
    "dark": {"drums": -16.5, "sub": -18.5, "pads": -24.0, "reese": -20.5, "air": -44.0},
}

def render(arr, name, flavour="liquid", rhodes_on=True, reese_on=False, master_lufs=-14.0, stems=True):
    os.makedirs(OUT, exist_ok=True)
    kit = Kit(seed=hash(name) % 1000, flavour=flavour)
    room = fx.cinema_ir(rt60=3.0, predelay=0.03, seed=17)
    L = int((sum(n for _, n in arr) * BAR + 2.5) * SR)

    def fit(x):
        x = fx.stereo(x)
        return np.pad(x, ((0, max(0, L - len(x))), (0, 0)))[:L]

    parts = {
        "drums": fit(drums(arr, kit)),
        "sub": fit(sub_line(arr)),
        "pads": fit(pads(arr, room)),
        "air": fit(air(arr)),
    }
    if rhodes_on:
        parts["keys"] = fit(rhodes(arr, room))
    if reese_on:
        parts["reese"] = fit(reese(arr))
    tgt = LEVELS.get(flavour, LEVELS["liquid"])
    for k in parts:                      # balance every stem to its target loudness for this flavour
        if np.any(parts[k]):
            parts[k] = parts[k] * fx.db(tgt.get(k, -30) - fx.lufs(parts[k]))
    mix = sum(parts.values())
    g = fx.db(master_lufs - fx.lufs(mix))
    mix = fx.soft_limit(mix * g, 0.93)
    fx.save(os.path.join(OUT, f"{name}.wav"), mix, br="224k")
    if stems:
        for k, v in parts.items():
            sf_path = os.path.join(OUT, "stems", f"{name}_{k}.wav")
            os.makedirs(os.path.dirname(sf_path), exist_ok=True)
            fx.save(sf_path, (v * g).astype(np.float32), mp3=False)
    print(name, f"{L / SR:.1f}s", {k: round(fx.lufs(v * g), 1) for k, v in parts.items() if np.any(v)})
    return mix


DEMOS = {
    "bed_liquid": dict(arr=[("intro", 4), ("build", 4), ("full", 16), ("break", 4), ("full", 8), ("outro", 4)], flavour="liquid", rhodes_on=True, reese_on=False),
    "bed_rollers": dict(arr=[("intro", 2), ("roller", 16), ("drop", 2), ("roller", 12), ("outro", 2)], flavour="rollers", rhodes_on=False, reese_on=True),
    "bed_dark": dict(arr=[("intro", 4), ("build", 4), ("full", 8), ("drop", 2), ("full", 12), ("outro", 2)], flavour="dark", rhodes_on=False, reese_on=True),
}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--arr", help="json: {name, arr:[[section,bars],...], flavour, rhodes_on, reese_on}")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    if a.arr:
        cfg = json.load(open(a.arr))
        render([tuple(x) for x in cfg.pop("arr")], cfg.pop("name"), **cfg)
    else:
        for nm, cfg in DEMOS.items():
            if a.only and nm not in a.only:
                continue
            render(cfg["arr"], nm, cfg["flavour"], cfg["rhodes_on"], cfg["reese_on"])
