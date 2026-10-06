#!/usr/bin/env python3
"""Preview mix for the one-camera look (user, 6 Oct: "crisp, like the best microphone ever, slight reverb, perfect
mix; the music garage or house, to keep energy up"). Three things, all made here so we own them:

  1. a 2-step garage bed synthesised in code (132 BPM, F minor: swung hats, a skipping kick, clap on 2 and 4, a
     sliding sub, organ stabs, an airy pad), arranged to the film's chapter marks;
  2. a vocal chain on the DRY narration: high-pass, a mud cut, presence, air, de-ess, compression, then a short
     bright plate (a synthesised impulse, about 9% wet, 18 ms pre-delay);
  3. the mix: the bed ducks under the voice (side-chain), a limiter, -14 LUFS, true peak under -1.5 dB.

    ~/youtube/.venv/bin/python mix_pre.py <build dir> <picture.mp4> <out.mp4>
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy import signal
import soundfile as sf

SR = 48000
BPM = 132.0
BEAT = 60.0 / BPM
STEP = BEAT / 4
SWING = 0.16                                   # how late every second 16th lands, as a fraction of a step
F = 43.654                                     # F1
RNG = np.random.default_rng(7)


def env(n, a, d, curve=4.0):
    t = np.arange(n) / SR
    return np.minimum(1.0, t / max(a, 1e-4)) * np.exp(-curve * t / max(d, 1e-4))


def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], "band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, "high", fs=SR, output="sos"), x)


def kick():
    n = int(0.34 * SR)
    t = np.arange(n) / SR
    f = 48 + 110 * np.exp(-t * 38)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.22, 5)
    return np.tanh(1.6 * (y + 0.25 * hp(RNG.standard_normal(n), 3000) * env(n, 0.0005, 0.012, 6)))


def clap():
    n = int(0.22 * SR)
    y = np.zeros(n)
    for d in (0.0, 0.011, 0.021, 0.034):
        k = int(d * SR)
        y[k:] += bp(RNG.standard_normal(n - k), 900, 4200) * env(n - k, 0.0005, 0.06 if d < 0.03 else 0.13, 5)
    return 0.95 * y


def hat(open_=False):
    n = int((0.16 if open_ else 0.045) * SR)
    return hp(RNG.standard_normal(n), 7500) * env(n, 0.0005, 0.11 if open_ else 0.02, 5) * (0.95 if open_ else 0.8)


def rim():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1700 * t) + 0.5 * np.sin(2 * np.pi * 2600 * t)) * env(n, 0.0003, 0.02, 6) * 0.3


def sub(f0, f1, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 26)                     # a quick slide into the note
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    a = np.minimum(1, t / 0.006) * np.minimum(1, (dur - t) / 0.03).clip(0, 1)
    return np.tanh(1.4 * y * a)


def organ(freqs, dur=0.2):
    """The garage organ stab: drawbar-ish partials, a fast decay, slightly bright."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f in freqs:
        for h, g in ((1, 1.0), (2, 0.55), (3, 0.32), (4, 0.12)):
            y += g * np.sin(2 * np.pi * f * h * t)
    return lp(y / len(freqs), 3800) * env(n, 0.002, dur * 0.7, 3.2) * 0.42


def pad(freqs, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f in freqs:
        for det in (-0.004, 0.0, 0.005):
            y += signal.sawtooth(2 * np.pi * f * (1 + det) * t + RNG.uniform(0, 6.28))
    y = lp(y / (3 * len(freqs)), 1500, 2)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.8).clip(0, 1)
    return y * a * 0.5


def note(semi, octave=3):
    return 174.614 * 2 ** ((semi + 12 * (octave - 3)) / 12.0)   # F3 = 174.61 Hz


# F minor: Fm9, Dbmaj7, Ab add9, Eb (as semitones above F)
CHORDS = [[0, 3, 7, 10, 14], [-4, 0, 3, 7], [3, 7, 10, 14], [-2, 2, 5, 10]]
ROOTS = [0, -4, 3, -2]
KICKS = [(0, 1.0), (7, 0.7), (10, 0.95)]                       # 2-step: no kick on 2 or 4
KICKS_B = [(0, 1.0), (3, 0.6), (10, 0.95), (14, 0.55)]
BASS = [(0, 3, 0), (3, 2, 0), (6, 2, 12), (10, 3, 0), (14, 2, 7)]   # (step, length in steps, semitone above the root)
STABS = [(2, 1.0), (5, 0.7), (11, 0.9), (14, 0.6)]


def place(buf, y, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    y = y[:len(buf) - i]
    buf[i:i + len(y), 0] += y * g * (1 - max(0, pan))
    buf[i:i + len(y), 1] += y * g * (1 + min(0, pan))


def bed(dur, marks, lead=0.0):
    """marks = [(time, section)], sections: intro (pad, hats), a (the groove), b (groove + stabs), out (pad only)."""
    n = int((dur + 2) * SR)
    drums, bass, keys, air = (np.zeros((n, 2)) for _ in range(4))
    K, C, H, O, R = kick(), clap(), hat(), hat(True), rim()
    bars = int((dur - lead) / (4 * BEAT)) + 1

    def sect(t):
        s = "intro"
        for mt, name in marks:
            if t >= mt - 1e-6:
                s = name
        return s

    for b in range(bars):
        t0 = lead + b * 4 * BEAT
        s = sect(t0)
        ch = b % 4
        root = ROOTS[ch]
        st = lambda k: t0 + k * STEP + (SWING * STEP if k % 2 else 0.0)   # noqa: E731
        place(air, pad([note(x, 3) for x in CHORDS[ch]], 4 * BEAT + 0.6), t0, 0.5 if s != "out" else 0.7)
        if s in ("intro", "a", "b"):
            for k in range(16):                                      # hats: swung, ghosted, an open one off the beat
                if k % 4 == 2:
                    place(drums, O, st(k), 0.5 if s == "intro" else 0.75, 0.25)
                else:
                    place(drums, H, st(k), (0.34 if k % 2 else 0.6) * (0.7 if s == "intro" else 1.0), -0.2 if k % 2 else 0.15)
        if s in ("a", "b"):
            for k, g in (KICKS_B if b % 4 == 3 else KICKS):
                place(drums, K, st(k), g * 0.62)
            for k in (4, 12):
                place(drums, C, st(k), 0.9)
            for k in ((9, 15) if b % 2 else (15,)):
                place(drums, R, st(k), 0.8, 0.4)
            for k, ln, semi in BASS:
                f = F * 2 ** ((root + semi) / 12.0)
                place(bass, sub(f * 1.12, f, ln * STEP * 0.95), st(k), 0.8)
        if s == "b":
            for k, g in STABS:
                place(keys, organ([note(x, 4) for x in CHORDS[ch][:4]]), st(k), g, 0.3 if k % 4 == 2 else -0.3)
    # the kick pumps everything that isn't the kick, a little
    pump = np.ones(n)
    for b in range(bars):
        t0 = lead + b * 4 * BEAT
        if sect(t0) in ("a", "b"):
            for k, _ in KICKS:
                i = int((t0 + k * STEP) * SR)
                m = min(n - i, int(0.26 * SR))
                if m > 0:
                    pump[i:i + m] = np.minimum(pump[i:i + m], 1 - 0.38 * np.exp(-np.arange(m) / (0.085 * SR)))
    keys = keys + 0.25 * np.roll(keys, int(0.75 * BEAT * SR), axis=0)[:, ::-1]     # a dotted-eighth echo on the stabs
    mix = drums * 0.9 + (bass * 0.30 + keys * 2.1 + air * 1.7) * pump[:, None]
    fade = np.minimum(1, np.arange(n) / (0.8 * SR)) * np.minimum(1, (n - np.arange(n)) / (3.0 * SR))
    mix = mix * fade[:, None]
    return (mix / (np.abs(mix).max() + 1e-9) * 0.89)[:int(dur * SR)]


def plate(seconds=0.95, pre=0.018):
    """A short bright plate as an impulse response: filtered noise with an exponential tail after a pre-delay."""
    n = int(seconds * SR)
    out = np.zeros((int(pre * SR) + n, 2))
    for ch in range(2):
        y = RNG.standard_normal(n) * np.exp(-np.arange(n) / (0.17 * SR))
        out[int(pre * SR):, ch] = lp(hp(y, 350), 8500)
    return out / np.abs(out).max()


def sfx(dur, m, words):
    """A light pass: a tick on the tap, a soft whoosh under each long camera move, a blip as each figure lands, a low
    hit on the lawsuit number. All synthesised here."""
    buf = np.zeros((int(dur * SR), 2))

    def tick(f=2400.0, d=0.05, g=0.5):
        n = int(d * SR)
        t = np.arange(n) / SR
        return np.sin(2 * np.pi * f * t) * np.exp(-t * 90) * g

    def whoosh(d=1.6, g=0.22):
        n = int(d * SR)
        y = RNG.standard_normal(n)
        k = np.linspace(0, 1, n)
        y = bp(y, 300, 2600) * np.sin(np.pi * k) ** 2
        return y * g

    def hit(g=0.7):
        n = int(0.7 * SR)
        t = np.arange(n) / SR
        return np.sin(2 * np.pi * (52 + 30 * np.exp(-t * 20)) * t) * np.exp(-t * 6) * g

    def at(line, word=None, d=0.0):
        if line not in m:
            return None
        if word:
            for w, a_, _b in words.get(line, []):
                if "".join(ch for ch in w.lower() if ch.isalnum()) == word:
                    return a_ + d
        return m[line]["start"] + d

    ev = [(at("tap", "touches"), tick(), 0.0), (at("tap", "approved"), tick(1800, 0.09, 0.4), 0.0),
          (at("ocean", None, 0.6), whoosh(3.6, 0.16), 0.0), (at("four", None, 1.6), whoosh(2.6), 0.0),
          (at("cents", None, 0.6), whoosh(2.4), 0.0), (at("thin", None, 0.4), whoosh(2.2, 0.18), 0.0),
          (at("weak", None, 0.4), whoosh(3.0), 0.0), (at("close", None, 0.4), whoosh(2.2), 0.0),
          (at("scale", "seventeen", -0.1), tick(900, 0.12, 0.35), -0.3), (at("service", "seventeen", -0.1), tick(1200, 0.08, 0.3), -0.3),
          (at("processing", "twenty", -0.1), tick(1200, 0.08, 0.3), -0.3), (at("border", "fourteen", -0.1), tick(1200, 0.08, 0.3), -0.3),
          (at("incentives", "fifteen", -0.1), tick(700, 0.12, 0.3), 0.3), (at("net", "forty", -0.1), tick(1500, 0.1, 0.35), -0.2),
          (at("profit", "twenty", -0.1), tick(1500, 0.1, 0.35), -0.2), (at("suits", "two", -0.1), hit(), 0.0)]
    for t0, y, pan in ev:
        if t0 is not None and t0 >= 0:
            place(buf, y, t0, 1.0, pan)
    return buf


def main(build, picture, out):
    m = {ln["id"]: ln for ln in json.load(open(os.path.join(build, "lines.json")))["lines"]}
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", picture],
                               capture_output=True, text=True).stdout)
    plan = [("ocean", "a"), ("never", "intro"), ("four", "a", 2.0), ("quote", "b"), ("risk", "a"), ("fee", "b"), ("whyset", "a"),
            ("meters", "b"), ("border", "a"), ("back", "b"), ("cents", "intro"), ("thin", "a"), ("profit", "b"), ("why", "intro"),
            ("returned", "a"), ("weak", "b"), ("regulators", "a"), ("verdict", "intro"), ("shop", "a"), ("close", "b")]
    marks = [(0.0, "intro")] + [(m[p[0]]["start"] + (p[2] if len(p) > 2 else 0.0), p[1]) for p in plan if p[0] in m] + [(dur - 6.0, "out")]
    bar = 4 * BEAT
    marks = [(round(t / bar) * bar, s) for t, s in marks]                    # sections change on bar lines
    sf.write(os.path.join(build, "garage.wav"), bed(dur, marks), SR)
    sf.write(os.path.join(build, "plate.wav"), plate(), SR)
    L_ = json.load(open(os.path.join(build, "lines.json")))["lines"]
    sf.write(os.path.join(build, "sfx.wav"), sfx(dur, m, {ln["id"]: ln.get("words") or [] for ln in L_}), SR)
    dry = os.path.join(build, "voice_dry.wav")
    chain = ("highpass=f=85,equalizer=f=260:t=q:w=1.1:g=-2.5,equalizer=f=3400:t=q:w=1.2:g=2.5,"
             "highshelf=f=10500:g=4,deesser=i=0.35:m=0.5:f=0.5,"
             "acompressor=threshold=-22dB:ratio=3.2:attack=6:release=110:makeup=5,alimiter=limit=0.89")
    fc = (f"[0:a]aformat=channel_layouts=stereo,{chain},asplit=3[v][vw][vk];"
          "[vw][2:a]afir=dry=0:wet=1[rev];"
          "[v][rev]amix=inputs=2:weights='1 0.09':normalize=0[vox];"
          "[1:a]volume=0.72[bed];[bed][vk]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=260[duck];"
          "[vox][duck][4:a]amix=inputs=3:normalize=0,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", dry, "-i", os.path.join(build, "garage.wav"), "-i", os.path.join(build, "plate.wav"),
                    "-i", picture, "-i", os.path.join(build, "sfx.wav"), "-filter_complex", fc, "-map", "3:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                    "-shortest", out], check=True)
    print(out)


if __name__ == "__main__":
    main(*sys.argv[1:4])
