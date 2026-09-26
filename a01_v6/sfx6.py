"""v6 sound: a restrained, layered, satisfying palette driven by the visual events (events.json).

Every visual action has one quiet, consistent sound (sound as punctuation, never decoration):
tick (a character resolves) · pip (a grid cell fills, climbing a scale) · form (a line forms) ·
chime (something completes) · thock (a card docks) · morph (lines flow into a new form) ·
thum ("It isn't") · shimmer (chrome) · zoom (the push through the 0).
Under it: a clean pad that moves from minor (the dark world) to major (the light world).

    python3 sfx6.py <voice.mp3>   ->  $A01V6_BUILD/mockup_mix.wav
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
BUILD = os.environ.get("A01V6_BUILD", os.path.join(os.path.dirname(os.path.abspath(__file__)), "build"))
DUR = 54.0
rng = np.random.default_rng(6)


def t_(d):
    return np.arange(int(d * SR)) / SR


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def lp(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def verb(x, sec=1.8, wet=0.3, damp=6000):
    n = int(sec * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * sec / 5))
    ir = lp(ir, damp) / np.sqrt(np.sum(ir ** 2))
    return x + wet * fftconvolve(x, ir)[:len(x)]


def norm(x, pk=1.0):
    return x / (np.max(np.abs(x)) or 1) * pk


PENTA = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3]


def tick(pitch=1.0):
    t = t_(0.012)
    x = bp(rng.normal(0, 1, len(t)), 3500 * pitch, 7000 * pitch) * np.exp(-t * 700)
    return norm(x + 0.4 * np.sin(2 * np.pi * 3200 * pitch * t) * np.exp(-t * 500))


def pip(k):
    f = 1760 * PENTA[k % 5] * (2 if (k // 5) % 2 else 1)
    t = t_(0.09)
    return norm(np.sin(2 * np.pi * f * t) * np.exp(-t * 55) + 0.2 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t * 90))


def form():
    t = t_(0.03)
    f0 = 1200 * rng.choice(PENTA)
    ph = np.cumsum(np.linspace(f0, f0 * 1.6, len(t))) / SR
    return norm(np.sin(2 * np.pi * ph) * np.sin(np.pi * t / t[-1]))


def chime(f=880, dur=1.8, bright=1.0):
    t = t_(dur)
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d)
            for r, a, d in ((1, 1, 2.2), (2.76, 0.5 * bright, 4), (5.40, 0.25 * bright, 7), (8.93, 0.12 * bright, 11)))
    return norm(verb(x, 2.2, 0.35))


def thock():
    t = t_(0.18)
    x = np.sin(2 * np.pi * 210 * t) * np.exp(-t * 38) + 0.35 * bp(rng.normal(0, 1, len(t)), 800, 2500) * np.exp(-t * 160)
    return norm(x)


def whoosh(d=0.8, lo=300, hi=3000):
    t = t_(d)
    n = rng.normal(0, 1, len(t))
    x = np.zeros_like(n)
    parts = 8
    for i in range(parts):                     # stepped band sweep, cross-faded
        s, e = int(i * len(t) / parts), int((i + 1) * len(t) / parts)
        f = lo * (hi / lo) ** (i / parts)
        x[s:e] = bp(n, f * 0.7, f * 1.4)[s:e]
    return norm(lp(x, 6000) * np.sin(np.pi * t / t[-1]) ** 2)


def morph():
    t = t_(1.0)
    gl = np.sin(2 * np.pi * np.cumsum(np.geomspace(300, 620, len(t))) / SR) * 0.25
    return norm(whoosh(1.0, 400, 2400) + gl * np.sin(np.pi * t))


def thum():
    t = t_(1.4)
    x = np.sin(2 * np.pi * np.cumsum(np.geomspace(70, 48, len(t))) / SR) * np.exp(-t * 3)
    return norm(verb(x + 0.2 * lp(rng.normal(0, 1, len(t)), 300) * np.exp(-t * 20), 1.5, 0.25))


def shimmer(d=1.4):
    t = t_(d)
    x = np.zeros(len(t))
    for _ in range(40):
        s = int(rng.uniform(0, d * 0.8) * SR)
        f = 2637 * rng.choice(PENTA) * rng.choice([1, 2])
        n = min(len(t) - s, int(0.4 * SR))
        tt = np.arange(n) / SR
        x[s:s + n] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 12) * rng.uniform(0.2, 1)
    return norm(verb(x, 2.0, 0.5, 9000))


def zoom():
    return norm(whoosh(1.3, 200, 5000) * np.linspace(0.3, 1, int(1.3 * SR)))


def scan(d=1.5):
    """A soft scanning sweep for grids and landscapes drawing in (like a slow radar/print pass)."""
    t = t_(d)
    sw = np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 720, len(t))) / SR) * 0.35
    return norm((whoosh(d, 500, 4000) * 0.6 + sw) * np.sin(np.pi * t / t[-1]) ** 1.5)


def blip():
    """Two-tone UI blip for a callout, bracket or pin appearing."""
    t = t_(0.028)
    a = np.sin(2 * np.pi * 2349 * t) * np.exp(-t * 90)
    b = np.sin(2 * np.pi * 3136 * t) * np.exp(-t * 90)
    return norm(np.concatenate([a, np.zeros(int(0.012 * SR)), b]))


def dots(d=0.9):
    """A granular run of tiny pips as a dot-matrix icon assembles."""
    t = t_(d)
    x = np.zeros(len(t))
    for i in range(22):
        s = int((i / 22) * d * 0.85 * SR)
        f = 3136 * PENTA[i % 5] * (1 + (i // 5) * 0.12)
        n = int(0.04 * SR)
        tt = np.arange(n) / SR
        x[s:s + n] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 120) * rng.uniform(0.4, 1)
    return norm(x)


def burst():
    """The particle ring: a sparkle burst riding a soft outward whoosh."""
    a, b = shimmer(1.4), whoosh(1.2, 600, 6000)
    b = np.pad(b, (0, len(a) - len(b)))
    return norm(a * 0.8 + b * 0.5)


def glint():
    """Spectral glint: a bright, shimmering upward glide."""
    t = t_(0.7)
    f = np.geomspace(2600, 5200, len(t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t)) * np.sin(np.pi * t / t[-1])
    return norm(verb(x, 1.6, 0.4, 9000))


def lift():
    """A card tilting up into the stack: an airy swish with a faint rising tone."""
    t = t_(0.55)
    tone = np.sin(2 * np.pi * np.cumsum(np.geomspace(330, 520, len(t))) / SR) * 0.2 * np.sin(np.pi * t / t[-1])
    return norm(whoosh(0.55, 700, 3500) + tone)


def pierce():
    """The one line through every layer: a clean, glassy laser tone."""
    t = t_(1.2)
    f = np.geomspace(880, 1320, len(t))
    x = sum(np.sin(2 * np.pi * np.cumsum(f * r) / SR) * g for r, g in ((1, 1), (1.003, 0.6), (2, 0.25)))
    return norm(verb(x * np.minimum(1, t / 0.05) * np.exp(-t * 2.5), 2.0, 0.4, 8000))


def tunnel():
    """Travelling through the rings: accelerating soft ticks over a rising whoosh."""
    d = 1.3
    x = whoosh(d, 250, 5000) * 0.7
    ts = np.cumsum(np.geomspace(0.12, 0.02, 24))
    for k, at in enumerate(ts[ts < d - 0.05]):
        c = tick(0.7 + k * 0.03)
        s = int(at * SR)
        x[s:s + len(c)] += c * 0.5
    return norm(x)


def pad(dur):
    """Clean pad: Am9 in the dark world, then Cmaj9 from 'It isn't' (14.3 s) onward."""
    t = t_(dur)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    out = np.zeros(len(t))
    for notes, a, b in (([45, 52, 55, 59, 60, 64], 0, 14.6), ([48, 55, 59, 62, 64, 67], 14.0, dur)):
        s, e = int(a * SR), min(len(t), int(b * SR))
        tt = t[s:e] - t[s]
        env = np.minimum(1, tt / 2.5) * np.minimum(1, (tt[-1] - tt) / 1.2 + 1e-9)
        for m in notes:
            for det in (-0.04, 0.04):
                out[s:e] += np.sin(2 * np.pi * hz(m + det) * tt) * env
    out = lp(out, 1800)
    air = lp(rng.normal(0, 1, len(t)), 900) * 0.15
    return norm(verb(out + air, 3.0, 0.4))


def place(bus, clip, at, db, pan=0.0):
    s = int(at * SR)
    n = min(len(clip), len(bus) - s)
    if n <= 0 or s < 0:
        return
    g = 10 ** (db / 20)
    a = (pan + 1) * np.pi / 4
    bus[s:s + n, 0] += clip[:n] * g * np.cos(a)
    bus[s:s + n, 1] += clip[:n] * g * np.sin(a)


def build(events):
    bus = np.zeros((int(DUR * SR) + SR, 2))
    last = {}
    pip_k = 0
    for at, kind in events:
        gap = at - last.get(kind, -9)
        if kind in ("tick", "form", "count", "blip") and gap < 0.035:     # keep it crisp, never a buzz
            continue
        last[kind] = at
        pan = float(rng.uniform(-0.35, 0.35))
        if kind == "tick":
            place(bus, tick(rng.uniform(0.9, 1.15)), at, -30, pan)
        elif kind == "count":
            place(bus, tick(0.6), at, -31, 0)
        elif kind == "pip":
            place(bus, pip(pip_k), at, -28, pan * 0.5)
            pip_k += 1
        elif kind == "form":
            place(bus, form(), at, -33, pan)
        elif kind == "chime":
            place(bus, chime(880), at, -21)
        elif kind == "chime_soft":
            place(bus, chime(1320, 1.2, 0.6), at, -26, pan)
        elif kind == "thock":
            place(bus, thock(), at, -20, pan)
        elif kind in ("morph",):
            place(bus, morph(), at, -24)
        elif kind == "whoosh":
            place(bus, whoosh(0.8), at, -27, pan)
        elif kind == "thum":
            place(bus, thum(), at, -15)
        elif kind == "shimmer":
            place(bus, shimmer(), at, -25)
        elif kind == "decode":
            for j in range(10):
                place(bus, tick(rng.uniform(0.8, 1.2)), at + j * 0.045, -31, float(rng.uniform(-0.5, 0.5)))
        elif kind == "zoom":
            place(bus, zoom(), at, -20)
        elif kind == "scan":
            place(bus, scan(), at, -27)
        elif kind == "blip":
            place(bus, blip(), at, -29, pan)
        elif kind == "dots":
            place(bus, dots(), at, -30, pan * 0.5)
        elif kind == "burst":
            place(bus, burst(), at, -21)
        elif kind == "glint":
            place(bus, glint(), at, -26)
        elif kind == "lift":
            place(bus, lift(), at, -27, pan)
        elif kind == "pierce":
            place(bus, pierce(), at, -22)
        elif kind == "tunnel":
            place(bus, tunnel(), at, -21)
    p = pad(DUR)
    place(bus, p, 0.0, -30)
    return bus


def main():
    voice = sys.argv[1]
    events = json.load(open(os.path.join(BUILD, "events.json")))
    bus = build(events)
    sfx = os.path.join(BUILD, "sfx6.wav")
    wavfile.write(sfx, SR, (np.clip(bus, -1, 1) * 32767).astype(np.int16))
    out = os.path.join(BUILD, "mockup_mix.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", voice, "-i", sfx, "-filter_complex",
                    "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0[v];[v][1:a]amix=inputs=2:normalize=0:duration=longest,"
                    "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", "-t", str(DUR), out], check=True)
    print(out)


if __name__ == "__main__":
    main()
