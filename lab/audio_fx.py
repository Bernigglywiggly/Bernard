"""Shared audio tools for the lab: loading, loudness, a synthesised cinema-hall reverb that ducks
under the dry voice (so the voice stays crisp and the room blooms in the gaps), a harmonic exciter
for air above the TTS band, and the "exo" colour (metallic comb, ring mod, crushed parallel layer).

Everything is numpy/scipy/pedalboard, 48 kHz float32. No samples are downloaded.
"""
import os
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

SR = 48000


# ---------------------------------------------------------------- io
def load(path, sr=SR, mono=False):
    x, fs = sf.read(path, dtype="float32", always_2d=True)
    if fs != sr:
        g = np.gcd(fs, sr)
        x = signal.resample_poly(x, sr // g, fs // g, axis=0).astype(np.float32)
    if mono:
        x = x.mean(1)
    return x


def save(path, x, sr=SR, mp3=True, br="192k"):
    x = np.asarray(x, np.float32)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    wav = path if path.endswith(".wav") else path.rsplit(".", 1)[0] + ".wav"
    sf.write(wav, x, sr, subtype="PCM_24")
    if mp3:
        mp = wav[:-4] + ".mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", br, mp], check=True)
        return mp
    return wav


def resample(x, fs, sr=SR):
    g = np.gcd(fs, sr)
    return signal.resample_poly(x, sr // g, fs // g, axis=0).astype(np.float32)


def stereo(x):
    return x if x.ndim == 2 else np.stack([x, x], 1)


def lufs(x, sr=SR):
    return pyln.Meter(sr).integrated_loudness(stereo(x))


def norm_lufs(x, target=-16.0, sr=SR, peak=-1.0):
    g = 10 ** ((target - lufs(x, sr)) / 20)
    y = x * g
    pk = np.max(np.abs(y)) + 1e-9
    lim = 10 ** (peak / 20)
    if pk > lim:
        y = soft_limit(y, lim)
    return y.astype(np.float32)


def soft_limit(x, ceiling=0.89):
    return (np.tanh(x / ceiling) * ceiling).astype(np.float32)


def db(v):
    return 10 ** (v / 20)


# ---------------------------------------------------------------- filters
def bq(x, kind, f, sr=SR, q=0.707, gain_db=0.0):
    """RBJ biquad; kind in lp, hp, bp, peak, lshelf, hshelf."""
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f / sr
    cw, sw = np.cos(w0), np.sin(w0)
    al = sw / (2 * q)
    if kind == "lp":
        b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]; a = [1 + al, -2 * cw, 1 - al]
    elif kind == "hp":
        b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]; a = [1 + al, -2 * cw, 1 - al]
    elif kind == "bp":
        b = [al, 0, -al]; a = [1 + al, -2 * cw, 1 - al]
    elif kind == "peak":
        b = [1 + al * A, -2 * cw, 1 - al * A]; a = [1 + al / A, -2 * cw, 1 - al / A]
    elif kind in ("lshelf", "hshelf"):
        s = 2 * np.sqrt(A) * al
        if kind == "lshelf":
            b = [A * ((A + 1) - (A - 1) * cw + s), 2 * A * ((A - 1) - (A + 1) * cw), A * ((A + 1) - (A - 1) * cw - s)]
            a = [(A + 1) + (A - 1) * cw + s, -2 * ((A - 1) + (A + 1) * cw), (A + 1) + (A - 1) * cw - s]
        else:
            b = [A * ((A + 1) + (A - 1) * cw + s), -2 * A * ((A - 1) + (A + 1) * cw), A * ((A + 1) + (A - 1) * cw - s)]
            a = [(A + 1) - (A - 1) * cw + s, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - s]
    else:
        raise ValueError(kind)
    b, a = np.array(b) / a[0], np.array(a) / a[0]
    return signal.lfilter(b, a, x, axis=0).astype(np.float32)


def env_follow(x, sr=SR, att=0.005, rel=0.12):
    """Peak envelope (mono) with separate attack/release."""
    m = np.abs(x if x.ndim == 1 else x.mean(1))
    ga, gr = np.exp(-1 / (att * sr)), np.exp(-1 / (rel * sr))
    # vectorised-ish one-pole: run in chunks through lfilter on the release, then take max with attack
    e = signal.lfilter([1 - gr], [1, -gr], m)
    e2 = signal.lfilter([1 - ga], [1, -ga], m)
    return np.maximum(e, e2 * 0.9).astype(np.float32)


# ---------------------------------------------------------------- the room
def cinema_ir(sr=SR, rt60=3.2, predelay=0.05, seed=7, width=1.0, dark=0.55):
    """A big, expensive-sounding hall: sparse early reflections, then a dense tail whose highs die
    faster than its lows (like a real room with seats and curtains). Stereo-decorrelated."""
    rng = np.random.default_rng(seed)
    n = int(sr * (predelay + rt60 * 1.15))
    ir = np.zeros((n, 2), np.float32)
    # early reflections: 14 taps between 12 and 90 ms after the predelay, panned
    for i in range(14):
        tt = predelay + rng.uniform(0.012, 0.09)
        k = int(tt * sr)
        g = 0.55 * np.exp(-tt * 9) * rng.uniform(0.5, 1.0)
        pan = rng.uniform(-0.9, 0.9) * width
        ir[k, 0] += g * np.sqrt((1 - pan) / 2) * 1.4
        ir[k, 1] += g * np.sqrt((1 + pan) / 2) * 1.4
    # late tail in 4 bands, each with its own decay
    t = np.arange(n) / sr
    start = int((predelay + 0.03) * sr)
    tail = np.zeros((n, 2), np.float32)
    bands = [("lp", 250, rt60 * 1.15), ("bp", 900, rt60), ("bp", 3000, rt60 * 0.72), ("hp", 6000, rt60 * 0.45 * (1.2 - dark))]
    for kind, f, T in bands:
        nz = rng.normal(0, 1, (n, 2)).astype(np.float32)
        nz = bq(nz, kind, f, sr, q=0.7 if kind != "bp" else 0.9)
        decay = np.exp(-6.91 * np.clip(t - predelay, 0, None) / T)[:, None]
        tail += nz * decay
    fade_in = np.clip((np.arange(n) - start) / (0.06 * sr), 0, 1)[:, None]
    tail *= fade_in * 0.22
    ir += tail
    # gentle slow modulation feel: tiny stereo spread
    ir[:, 1] = np.roll(ir[:, 1], int(0.0007 * sr))
    return (ir / (np.sqrt((ir ** 2).sum(0)).max() + 1e-9)).astype(np.float32)


def convolve(x, ir):
    x = stereo(x)
    out = np.zeros((x.shape[0] + ir.shape[0] - 1, 2), np.float32)
    for ch in range(2):
        out[:, ch] = signal.fftconvolve(x[:, ch], ir[:, ch])
    return out


def ducked_room(dry, ir, wet_db=-8.0, duck_db=7.0, sr=SR, tail_s=None):
    """Convolve, then pull the wet down while the dry is loud: crisp words, a room that blooms in gaps."""
    wet = convolve(dry, ir)
    wet = bq(bq(wet, "hp", 260, sr, q=0.6), "lp", 9000, sr)     # return EQ: no mud, no fizz in the tail
    e = env_follow(np.pad(stereo(dry).mean(1), (0, wet.shape[0] - dry.shape[0])), sr, att=0.004, rel=0.35)
    e = e / (np.percentile(e[e > 1e-4], 95) + 1e-9) if np.any(e > 1e-4) else e
    g = db(wet_db) * db(-duck_db * np.clip(e, 0, 1))[:, None]
    out = np.pad(stereo(dry), ((0, wet.shape[0] - dry.shape[0]), (0, 0))) + wet * g
    if tail_s is not None:
        out = out[: dry.shape[0] + int(tail_s * sr)]
    return out.astype(np.float32)


# ---------------------------------------------------------------- tone
def exciter(x, amount=0.18, sr=SR):
    """Air above the TTS band: saturate the 3-11 kHz band and keep only the new harmonics up top."""
    band = bq(bq(x, "hp", 3000, sr), "lp", 11000, sr)
    h = np.tanh(band * 6.0)
    h = bq(bq(h, "hp", 9500, sr), "hp", 9500, sr)
    return (x + h * amount).astype(np.float32)


def crisp(x, sr=SR, presence=2.5, air=2.0, mud=-2.5):
    y = bq(x, "hp", 75, sr, q=0.6)
    y = bq(y, "peak", 280, sr, q=1.0, gain_db=mud)
    y = bq(y, "peak", 4600, sr, q=0.9, gain_db=presence)
    y = bq(y, "hshelf", 10000, sr, gain_db=air)
    return y


def deess(x, sr=SR, f=6500, thresh=0.06, ratio=3.0):
    s = bq(x, "hp", f, sr)
    e = env_follow(s, sr, att=0.001, rel=0.04)
    over = np.clip(e / thresh, 1, None)
    g = over ** (1 / ratio - 1)
    g = g[:, None] if x.ndim == 2 else g
    return (x - s + s * g).astype(np.float32)


def compress(x, sr=SR, thresh_db=-20, ratio=3.0, att=0.006, rel=0.12, makeup_db=4):
    e = env_follow(x, sr, att, rel)
    edb = 20 * np.log10(e + 1e-9)
    over = np.clip(edb - thresh_db, 0, None)
    gdb = -over * (1 - 1 / ratio) + makeup_db
    g = db(gdb)
    return (x * (g[:, None] if x.ndim == 2 else g)).astype(np.float32)


def exo(x, sr=SR, amount=0.5, ring_hz=62.0):
    """The synthetic-body colour: a short metallic comb (the voice in a chassis), a faint ring-mod
    buzz, and a crushed parallel layer. `amount` 0..1 scales the whole character."""
    x = x if x.ndim == 1 else x.mean(1)
    n = len(x)
    y = x.copy()
    # metallic comb: two short feedback delays (1.3 ms, 2.9 ms)
    for d_ms, fb in ((1.3, 0.42), (2.9, 0.33)):
        d = int(sr * d_ms / 1000)
        b = np.zeros(d + 1); b[0] = 1
        a = np.zeros(d + 1); a[0] = 1; a[d] = -fb
        comb = signal.lfilter(b, a, x)
        y = y + comb * 0.22 * amount
    # ring mod at low mix
    t = np.arange(n) / sr
    y = y + x * np.sin(2 * np.pi * ring_hz * t) * 0.10 * amount
    # crushed layer: 9-bit, band-limited so it reads as texture not fizz
    q = 2 ** 9
    cr = np.round(bq(x, "hp", 900, sr) * q) / q
    cr = bq(cr, "lp", 7000, sr)
    y = y + cr * 0.12 * amount
    # tiny doubling (synthetic sheen): 11 ms, slightly detuned by resampling
    dbl = signal.resample(x, int(n * 1.003))[:n]
    dbl = np.pad(dbl, (int(0.011 * sr), 0))[:n]
    y = y + dbl * 0.14 * amount
    y = y / (1 + 0.35 * amount)
    return y.astype(np.float32)


def chain_voice(x, sr=SR, exo_amt=0.0, room=None, room_wet=-9.0, air=0.18, target=-16.0):
    """Full voice chain: exo colour (optional) -> clean-up EQ -> de-ess -> compress -> exciter -> room."""
    y = x if x.ndim == 1 else x.mean(1)
    if exo_amt > 0:
        y = exo(y, sr, exo_amt)
    y = crisp(y, sr)
    y = deess(y, sr)
    y = compress(y, sr)
    y = exciter(y, air, sr)
    if room is not None:
        y = ducked_room(y, room, wet_db=room_wet, sr=sr, tail_s=2.5)
    return norm_lufs(stereo(y), target, sr)
