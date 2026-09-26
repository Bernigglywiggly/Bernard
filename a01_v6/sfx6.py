"""v6 sound: a restrained, layered, satisfying palette driven by the visual events (events.json).

Three layers, all following the picture:
1. Foreground: one quiet sound per visual action, placed in stereo where it happens on screen:
   tick (a character resolves) · pip (a grid cell fills, climbing a scale) · form (a line forms) ·
   chime (something completes) · thock (a card docks) · morph (lines flow into a new form) ·
   thum ("It isn't") · shimmer (chrome) · zoom (the push through the 0) · scan · blip · dots ·
   burst · glint · lift · pierce · tunnel.
2. Sweeteners: reversed swells that breathe in before the big moments, felt-piano notes as cards and
   chapters arrive (ending on a rolled Cmaj9), and one shared room so everything sits in one space.
3. Bed: a pad (Am9 on graphite, Cmaj9 once the room opens at 14.3 s), a sub you feel more than hear,
   and a quiet air texture for each world. The bed ducks under the voice.

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
DUR = 55.5
rng = np.random.default_rng(6)


def t_(d):
    return np.arange(int(d * SR)) / SR


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def lp(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def hp(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)


def verb(x, sec=1.8, wet=0.3, damp=6000):
    n = int(sec * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * sec / 5))
    ir = lp(ir, damp) / np.sqrt(np.sum(ir ** 2))
    return x + wet * fftconvolve(x, ir)[:len(x)]


def norm(x, pk=1.0):
    return x / (np.max(np.abs(x)) or 1) * pk


def st(left, right):
    """Two renders of a noisy sound (or two detuned tones) side by side: natural stereo width."""
    n = min(len(left), len(right))
    return np.column_stack([left[:n], right[:n]])


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


PENTA = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3]


# ---------------------------------------------------------------- foreground
def tick(pitch=1.0):
    t = t_(0.012)
    x = bp(rng.normal(0, 1, len(t)), 3500 * pitch, 7000 * pitch) * np.exp(-t * 700)
    return norm(x + 0.4 * np.sin(2 * np.pi * 3200 * pitch * t) * np.exp(-t * 500))


def pip(k):
    """A cell filling: a glassy note with a soft body an octave below, climbing the scale."""
    f = 1760 * PENTA[k % 5] * (2 if (k // 5) % 2 else 1)
    t = t_(0.12)
    return norm(np.sin(2 * np.pi * f * t) * np.exp(-t * 55) + 0.2 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t * 90)
                + 0.3 * np.sin(np.pi * f * t) * np.exp(-t * 40))


def form():
    t = t_(0.03)
    f0 = 1200 * rng.choice(PENTA)
    ph = np.cumsum(np.linspace(f0, f0 * 1.6, len(t))) / SR
    return norm(np.sin(2 * np.pi * ph) * np.sin(np.pi * t / t[-1]))


def chime(f=880, dur=1.8, bright=1.0):
    """Glass chime with a warm sub-octave; the right side is detuned a hair for width."""
    t = t_(dur)

    def one(ff):
        x = sum(a * np.sin(2 * np.pi * ff * r * t) * np.exp(-t * d)
                for r, a, d in ((1, 1, 2.2), (2.76, 0.5 * bright, 4), (5.40, 0.25 * bright, 7), (8.93, 0.12 * bright, 11)))
        return verb(x + 0.3 * np.sin(np.pi * ff * t) * np.exp(-t * 3), 2.2, 0.35)
    return norm(st(one(f), one(f * 1.002)))


def thock():
    """A card docking: a soft body, a low magnetic thump, felt and a tiny click."""
    t = t_(0.22)
    x = (np.sin(2 * np.pi * 210 * t) * np.exp(-t * 38) + 0.5 * np.sin(2 * np.pi * 72 * t) * np.exp(-t * 22)
         + 0.35 * bp(rng.normal(0, 1, len(t)), 800, 2500) * np.exp(-t * 160)
         + 0.2 * bp(rng.normal(0, 1, len(t)), 3000, 8000) * np.exp(-t * 600))
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


def whoosh_st(d=0.8, lo=300, hi=3000):
    return norm(st(whoosh(d, lo, hi), whoosh(d, lo, hi)))


def morph():
    """Lines flowing into a new form: wide air, a rising glide and a faint chord inside it."""
    t = t_(1.0)
    gl = np.sin(2 * np.pi * np.cumsum(np.geomspace(300, 620, len(t))) / SR) * 0.25 * np.sin(np.pi * t)
    chord = sum(np.sin(2 * np.pi * hz(m) * t) for m in (69, 76)) * 0.06 * np.sin(np.pi * t) ** 2
    return norm(st(whoosh(1.0, 400, 2400) + gl + chord, whoosh(1.0, 400, 2400) + gl + chord))


def thum():
    """'It isn't': a sub drop with a C-major bloom opening inside it (the room opens)."""
    t = t_(2.4)
    sub = np.sin(2 * np.pi * np.cumsum(np.geomspace(70, 48, len(t))) / SR) * np.exp(-t * 2.2)
    env = np.minimum(1, t / 0.25) * np.exp(-t * 1.4)
    air = 0.2 * lp(rng.normal(0, 1, len(t)), 300) * np.exp(-t * 20)

    def side(det):
        bloom = sum(np.sin(2 * np.pi * hz(m) * det * t) for m in (60, 67, 76)) * 0.09 * env
        return verb(sub + bloom + air, 2.0, 0.3)
    return norm(st(side(1.0), side(1.003)))


def shimmer(d=1.4):
    """Chrome glints: sparkles scattered across the stereo field."""
    t = t_(d)
    x = np.zeros((len(t), 2))
    for _ in range(40):
        s = int(rng.uniform(0, d * 0.8) * SR)
        f = 2637 * rng.choice(PENTA) * rng.choice([1, 2])
        n = min(len(t) - s, int(0.4 * SR))
        tt = np.arange(n) / SR
        g = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 12) * rng.uniform(0.2, 1)
        p = rng.uniform(0.15, 0.85)
        x[s:s + n, 0] += g * np.sqrt(1 - p)
        x[s:s + n, 1] += g * np.sqrt(p)
    return norm(st(verb(x[:, 0], 2.0, 0.5, 9000), verb(x[:, 1], 2.0, 0.5, 9000)))


def zoom():
    return norm(whoosh_st(1.3, 200, 5000) * np.linspace(0.3, 1, int(1.3 * SR))[:, None])


def scan(d=1.5):
    """A soft scanning sweep that travels across the stereo field as a grid or landscape draws in."""
    t = t_(d)
    sw = np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 720, len(t))) / SR) * 0.35
    env = np.sin(np.pi * t / t[-1]) ** 1.5
    a = (np.linspace(-0.6, 0.6, len(t)) + 1) * np.pi / 4
    x = st((whoosh(d, 500, 4000) * 0.6 + sw) * env, (whoosh(d, 500, 4000) * 0.6 + sw) * env)
    return norm(x * np.column_stack([np.cos(a), np.sin(a)]) * np.sqrt(2))


def blip():
    """Two-tone UI blip for a callout, bracket or pin appearing."""
    t = t_(0.028)
    a = np.sin(2 * np.pi * 2349 * t) * np.exp(-t * 90)
    b = np.sin(2 * np.pi * 3136 * t) * np.exp(-t * 90)
    return norm(np.concatenate([a, np.zeros(int(0.012 * SR)), b]))


def dots(d=0.9):
    """A granular run of tiny pips as a dot-matrix icon assembles, drifting left to right like the dots."""
    t = t_(d)
    x = np.zeros((len(t), 2))
    for i in range(22):
        s = int((i / 22) * d * 0.85 * SR)
        f = 3136 * PENTA[i % 5] * (1 + (i // 5) * 0.12)
        n = int(0.04 * SR)
        tt = np.arange(n) / SR
        g = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 120) * rng.uniform(0.4, 1)
        p = 0.35 + 0.3 * i / 21
        x[s:s + n, 0] += g * np.sqrt(1 - p)
        x[s:s + n, 1] += g * np.sqrt(p)
    return norm(x)


def burst():
    """The particle ring: a sparkle burst riding a soft outward whoosh."""
    a, b = shimmer(1.4), whoosh_st(1.2, 600, 6000)
    b = np.pad(b, ((0, len(a) - len(b)), (0, 0)))
    return norm(a * 0.8 + b * 0.5)


def glint():
    """Spectral glint: a bright, shimmering upward glide."""
    t = t_(0.7)
    f = np.geomspace(2600, 5200, len(t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t)) * np.sin(np.pi * t / t[-1])
    return norm(st(verb(x, 1.6, 0.4, 9000), verb(x, 1.6, 0.4, 9000)))


def lift():
    """A card tilting up into the stack: an airy swish with a faint rising tone."""
    t = t_(0.55)
    tone = np.sin(2 * np.pi * np.cumsum(np.geomspace(330, 520, len(t))) / SR) * 0.2 * np.sin(np.pi * t / t[-1])
    return norm(whoosh(0.55, 700, 3500) + tone)


def pierce():
    """The one line through every layer: a clean, glassy laser tone, slightly detuned across the sides."""
    t = t_(1.2)
    f = np.geomspace(880, 1320, len(t))

    def side(det):
        x = sum(np.sin(2 * np.pi * np.cumsum(f * r * det) / SR) * g for r, g in ((1, 1), (1.003, 0.6), (2, 0.25)))
        return verb(x * np.minimum(1, t / 0.05) * np.exp(-t * 2.5), 2.0, 0.4, 8000)
    return norm(st(side(1.0), side(1.002)))


def tunnel():
    """Travelling through the rings: accelerating soft ticks passing side to side over a rising whoosh."""
    d = 1.3
    x = whoosh_st(d, 250, 5000) * 0.7
    ts = np.cumsum(np.geomspace(0.12, 0.02, 24))
    for k, at in enumerate(ts[ts < d - 0.05]):
        c = tick(0.7 + k * 0.03)
        s = int(at * SR)
        side = k % 2
        x[s:s + len(c), side] += c * 0.5
        x[s:s + len(c), 1 - side] += c * 0.2
    return norm(x)


# ---------------------------------------------------------------- sweeteners
def swell(d=1.1, notes=(57, 60, 64, 71)):
    """A reversed bloom that rises into a hit: the breath in before a big moment."""
    t = t_(0.5)
    hit = np.pad(sum(np.sin(2 * np.pi * hz(m) * t) for m in notes) * np.exp(-t * 8), (0, int(2.4 * SR)))
    x = st(verb(hit, 2.4, 1.0, 7000), verb(hit, 2.4, 1.0, 7000))[::-1][-int(d * SR):]
    x *= np.minimum(1, np.arange(len(x)) / (0.3 * SR))[:, None]
    return norm(x)


def felt(m, dur=2.6):
    """A soft felt-piano note: warm harmonics, a gentle hammer thud, rounded top."""
    t = t_(dur)
    f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * r * t + ph) * np.exp(-t * d)
            for r, a, d, ph in ((1, 1, 1.6, 0), (2, 0.35, 2.6, 0.3), (3, 0.12, 4, 0.7), (4.01, 0.05, 6, 1.1)))
    x = x * np.minimum(1, t / 0.006) + 0.25 * lp(rng.normal(0, 1, len(t)), 900) * np.exp(-t * 60)
    return norm(lp(x, 3500))


DARK_CHORD, LIGHT_CHORD = (57, 60, 64, 71), (60, 64, 67, 74)
SWELLS = [(6.2, DARK_CHORD, 1.1), (11.5, DARK_CHORD, 1.1), (14.3, LIGHT_CHORD, 1.6), (41.9, LIGHT_CHORD, 1.0),
          (43.6, LIGHT_CHORD, 0.9), (52.6, LIGHT_CHORD, 1.4)]
MOTIFS = [(15.35, (72, 76, 79)), (22.45, (74, 79, 83)), (28.25, (76, 79, 84)), (32.65, (79, 83, 86)),   # the four cards, rising
          (47.5, (72,)), (49.2, (76,)), (50.3, (79,))]                                                  # the three chapter tiles
END_CHORD = (53.85, (48, 55, 64, 71, 74, 79))          # rolled Cmaj9 under the end card: home


# ---------------------------------------------------------------- bed
def pad(dur):
    """Clean pad: Am9 in the graphite world, then Cmaj9 from 'It isn't' (14.3 s) onward."""
    t = t_(dur)
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


def sub(dur):
    """A sub on the chord roots (A1, then C2): felt more than heard."""
    t = t_(dur)
    out = np.zeros(len(t))
    for m, a, b in ((33, 0, 14.6), (36, 14.0, dur)):
        s, e = int(a * SR), min(len(t), int(b * SR))
        tt = t[s:e] - t[s]
        out[s:e] += np.sin(2 * np.pi * hz(m) * tt) * np.minimum(1, tt / 3) * np.minimum(1, (tt[-1] - tt) / 1.5 + 1e-9)
    return norm(out)


def air(dur):
    """Room tone for each world: deep, dark air on graphite; a lighter, airier room on slate. Slowly breathing."""
    t = t_(dur)
    k = np.clip((t - 14.3) / 0.9, 0, 1)[:, None]
    breathe = (0.85 + 0.15 * np.sin(2 * np.pi * 0.06 * t))[:, None]
    dark = st(lp(rng.normal(0, 1, len(t)), 450), lp(rng.normal(0, 1, len(t)), 450))
    light = st(bp(rng.normal(0, 1, len(t)), 300, 1600) + 0.05 * hp(rng.normal(0, 1, len(t)), 6000),
               bp(rng.normal(0, 1, len(t)), 300, 1600) + 0.05 * hp(rng.normal(0, 1, len(t)), 6000))
    return norm((dark / np.std(dark) * (1 - k) + light / np.std(light) * 0.8 * k) * breathe)


def room(bus, sec=2.2):
    """One shared room for all the foreground sounds (decorrelated per side): the glue."""
    n = int(sec * SR)
    out = np.zeros_like(bus)
    for ch in range(2):
        ir = lp(rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * sec / 5)), 6500)
        out[:, ch] = fftconvolve(bus[:, ch], ir / np.sqrt(np.sum(ir ** 2)))[:len(bus)]
    return out


# ---------------------------------------------------------------- mix
def place(bus, clip, at, db, pan=0.0):
    s = int(round(at * SR))
    n = min(len(clip), len(bus) - s)
    if n <= 0 or s < 0:
        return
    a = (max(-1.0, min(1.0, pan)) + 1) * np.pi / 4
    gains = np.array([np.cos(a), np.sin(a)]) * 10 ** (db / 20)
    bus[s:s + n] += (clip[:n, None] if clip.ndim == 1 else clip[:n]) * gains     # stereo clips keep their own width


def build(events):
    n = int(DUR * SR) + SR
    fg, bed = np.zeros((n, 2)), np.zeros((n, 2))
    last = {}
    pip_k = 0
    for e in events:
        at, kind, pos = (list(e) + [None])[:3]
        gap = at - last.get(kind, -9)
        if kind in ("tick", "form", "count", "blip") and gap < 0.035:     # keep it crisp, never a buzz
            continue
        last[kind] = at
        pan = float(rng.uniform(-0.35, 0.35)) if pos is None else 0.8 * pos     # sound follows its motion
        if kind == "tick":
            place(fg, tick(rng.uniform(0.9, 1.15)), at, -30, pan)
        elif kind == "count":
            place(fg, tick(0.6), at, -31, 0)
        elif kind == "pip":
            place(fg, pip(pip_k), at, -28, pan)
            pip_k += 1
        elif kind == "form":
            place(fg, form(), at, -33, pan)
        elif kind == "chime":
            place(fg, chime(880), at, -21, pan * 0.6)
        elif kind == "chime_soft":
            place(fg, chime(1320, 1.2, 0.6), at, -26, pan * 0.6)
        elif kind == "thock":
            place(fg, thock(), at, -20, pan)
        elif kind == "morph":
            place(fg, morph(), at, -24)
        elif kind == "whoosh":
            place(fg, whoosh_st(0.8), at, -27)
        elif kind == "thum":
            place(fg, thum(), at, -15)
        elif kind == "shimmer":
            place(fg, shimmer(), at, -25)
        elif kind == "decode":
            for j in range(10):
                place(fg, tick(rng.uniform(0.8, 1.2)), at + j * 0.045, -31, float(rng.uniform(-0.5, 0.5)))
        elif kind == "zoom":
            place(fg, zoom(), at, -20)
        elif kind == "scan":
            place(fg, scan(), at, -27)
        elif kind == "blip":
            place(fg, blip(), at, -29, pan)
        elif kind == "dots":
            place(fg, dots(), at, -30, pan * 0.5)
        elif kind == "burst":
            place(fg, burst(), at, -21)
        elif kind == "glint":
            place(fg, glint(), at, -26)
        elif kind == "lift":
            place(fg, lift(), at, -27, pan)
        elif kind == "pierce":
            place(fg, pierce(), at, -22)
        elif kind == "tunnel":
            place(fg, tunnel(), at, -21)
    for at, notes, d in SWELLS:
        place(fg, swell(d, notes), at - d, -31)
    for at, notes in MOTIFS:
        for j, m in enumerate(notes):
            place(fg, felt(m), at + j * 0.16, -31, (j - (len(notes) - 1) / 2) * 0.25)
    at, notes = END_CHORD
    for j, m in enumerate(notes):
        place(fg, felt(m, 3.2), at + j * 0.07, -29, (j / (len(notes) - 1) - 0.5) * 0.5)
    fg += 0.2 * room(fg)
    place(bed, pad(DUR), 0.0, -28)
    place(bed, sub(DUR), 0.0, -37)
    place(bed, air(DUR), 0.0, -43)
    return fg, bed


def write(path, x):
    wavfile.write(path, SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))


def main():
    voice = sys.argv[1]
    events = json.load(open(os.path.join(BUILD, "events.json")))
    fg, bed = build(events)
    sfx, bedf = os.path.join(BUILD, "sfx6.wav"), os.path.join(BUILD, "bed6.wav")
    write(sfx, fg)
    write(bedf, bed)
    out = os.path.join(BUILD, "mockup_mix.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", voice, "-i", sfx, "-i", bedf, "-filter_complex",
                    "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[v][key];"
                    "[2:a][key]sidechaincompress=threshold=0.02:ratio=3:attack=30:release=500[bed];"     # the bed breathes around the voice
                    "[v][1:a][bed]amix=inputs=3:normalize=0:duration=longest,"
                    f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,afade=t=out:st={DUR - 1.2}:d=1.2",
                    "-t", str(DUR), out], check=True)
    print(out)


if __name__ == "__main__":
    main()
