"""The v7 sound palette: mechanical, futuristic, ethereal. No chimes, no sparkle.

Every sound is synthesised here (no samples, so nothing to license or get claimed):
  thock / clack / typing   creamy, dampened keyboard switches (downstroke body + softer upstroke)
  relay / latch / dock     electromechanical contacts, magnetic snaps, a card locking into place
  servo / hydraulic        small motors with gear grain, pressure releases
  tick / chatter / confirm dry HUD ticks, data chatter for ASCII decoding, a dull two-tone confirm
  scan / form / power_up   a line sweeping, a line energising (resonant filter, no glitter), systems waking
  whoosh                   a pass-by for camera moves (doppler band sweep, travels across the stereo field)
  vortex / sub_drop / thum the stomach-drop family: a hang at the top, an endless descending Shepard-Risset
                           fall, a sub that drops out from under you, and a deep impact
  riser / glitch / swell   tension up, digital stutter, an F-minor air swell for transitions

    python3 palette.py            # out/sfx/<name>.wav|mp3 + out/sfx/palette_reel.mp3 (with spoken labels)
"""
import os
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import audio_fx as fx  # noqa: E402

SR = fx.SR
OUT = os.path.join(os.path.dirname(__file__), "..", "out", "sfx")
RNG = np.random.default_rng(170)


# ---------------------------------------------------------------- primitives
def T(dur):
    return np.arange(int(dur * SR)) / SR


def noise(n, rng=RNG):
    return rng.normal(0, 1, n).astype(np.float32)


def modal(freqs, decays, amps, dur, rng=RNG, jitter=0.0):
    t = T(dur)
    y = np.zeros_like(t)
    for f, d, a in zip(freqs, decays, amps):
        f = f * (1 + rng.uniform(-jitter, jitter))
        y += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 2 * np.pi)) * np.exp(-t / d)
    return y.astype(np.float32)


def burst(dur, lo, hi, decay, rng=RNG):
    """A short band-limited noise burst (the 'click' of a contact)."""
    n = noise(int(dur * SR) + 1, rng)
    n = fx.bq(fx.bq(n, "hp", lo), "lp", hi)
    return (n * np.exp(-T(dur + 1 / SR)[: len(n)] / decay)).astype(np.float32)


def sweep_phase(f):
    return 2 * np.pi * np.cumsum(f) / SR


def glide(f0, f1, dur, kind="exp"):
    x = np.linspace(0, 1, int(dur * SR))
    if kind == "exp":
        return f0 * (f1 / f0) ** x
    e = x * x * (3 - 2 * x)
    return f0 + (f1 - f0) * e


def env(dur, a=0.005, r=0.05, curve=3.0):
    n = int(dur * SR)
    e = np.ones(n, np.float32)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na) ** 2
    e[-nr:] *= np.linspace(1, 0, nr) ** curve
    return e


def add(*xs):
    """Sum arrays of different lengths (all start at t=0)."""
    n = max(len(x) for x in xs)
    y = np.zeros(n, np.float32)
    for x in xs:
        y[: len(x)] += x
    return y


def place(dst, src, at):
    i = int(at * SR)
    j = min(len(dst), i + len(src))
    if j > i:
        dst[i:j] += src[: j - i]
    return dst


def tv_band(x, fc, bw_oct=0.7, nfft=1024, hop=256):
    """Time-varying band-pass by STFT masking (fc is per-sample, Hz)."""
    f, tt, Z = signal.stft(x, SR, nperseg=nfft, noverlap=nfft - hop)
    fcs = np.interp(tt, np.arange(len(fc)) / SR, fc)
    lf = np.log2(np.maximum(f, 1.0))[:, None]
    mask = np.exp(-0.5 * ((lf - np.log2(fcs)[None, :]) / (bw_oct / 2.355)) ** 2)
    _, y = signal.istft(Z * mask, SR, nperseg=nfft, noverlap=nfft - hop)
    y = y[: len(x)]
    return np.pad(y, (0, len(x) - len(y))).astype(np.float32)


def sat(x, drive=1.5):
    return (np.tanh(x * drive) / np.tanh(drive)).astype(np.float32)


def peak(x, db=-3.0):
    return (x / (np.max(np.abs(x)) + 1e-9) * fx.db(db)).astype(np.float32)


def pan(x, p):
    """Equal-power pan; p may be a scalar or per-sample array in -1..1."""
    p = np.clip(p, -1, 1)
    l, r = np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)
    return np.stack([x * l, x * r], 1).astype(np.float32)


def shepard(dur, rate=-0.9, n=8, fmin=26.0, wave="sine", rng=RNG):
    """Shepard-Risset glissando: partials an octave apart sliding forever (rate in octaves/s; negative = falling)."""
    t = T(dur)
    y = np.zeros_like(t)
    for i in range(n):
        pos = (i + rate * t) % n
        f = fmin * 2 ** pos
        ph = sweep_phase(f) + rng.uniform(0, 2 * np.pi)
        amp = 0.5 - 0.5 * np.cos(2 * np.pi * pos / n)
        osc = np.sin(ph) if wave == "sine" else (np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.1 * np.sin(3 * ph))
        y += amp * osc
    return (y / n * 2.2).astype(np.float32)


# ---------------------------------------------------------------- the lab room (shared by everything)
_ROOM = {}


def room(x, wet_db=-17.0, kind="lab"):
    if kind not in _ROOM:
        _ROOM[kind] = fx.cinema_ir(rt60=0.55, predelay=0.008, seed=3, dark=0.7) if kind == "lab" else fx.cinema_ir(rt60=3.4, predelay=0.05, seed=11)
    st = x if x.ndim == 2 else pan(x, 0)
    wet = fx.convolve(st, _ROOM[kind])
    wet = fx.bq(fx.bq(wet, "hp", 200), "lp", 9000)
    out = np.pad(st, ((0, len(wet) - len(st)), (0, 0))) + wet * fx.db(wet_db)
    # trim trailing silence
    e = np.abs(out).max(1)
    last = np.nonzero(e > 1e-4)[0]
    return out[: (last[-1] + 1 if len(last) else len(out))].astype(np.float32)


# ---------------------------------------------------------------- keys
def thock(v=0, up=True, low=1.0):
    """Creamy, dampened linear switch bottoming out: a woody low body, a muted click, a softer upstroke."""
    r = np.random.default_rng(100 + v)
    dur = 0.22
    y = np.zeros(int(dur * SR), np.float32)
    body = modal([182 * low, 404 * low, 880 * low, 1640], [0.042, 0.028, 0.016, 0.009], [1.0, 0.55, 0.28, 0.12], 0.14, r, jitter=0.035)
    thump = np.sin(2 * np.pi * glide(130 * low, 88 * low, 0.05)[:int(0.05 * SR)] * T(0.05)) * np.exp(-T(0.05) / 0.018)
    click = burst(0.004, 1400, 4200, 0.0012, r) * 0.55
    place(y, body * 0.8, 0.0)
    place(y, thump * 0.6, 0.0)
    place(y, click, 0.0)
    if up:
        u = modal([520, 1180, 2250], [0.014, 0.009, 0.005], [0.5, 0.3, 0.12], 0.05, r, jitter=0.05) * 0.28
        u = add(u, burst(0.002, 2000, 5000, 0.0008, r) * 0.18)
        place(y, u, r.uniform(0.075, 0.095))
    y = fx.bq(y, "lp", 5200)
    return peak(sat(y, 1.3), -4)


def clack(v=0):
    """Brighter, marbly key: higher modes, sharper click, shorter body."""
    r = np.random.default_rng(200 + v)
    y = modal([610, 1330, 2870, 4100], [0.022, 0.014, 0.008, 0.005], [1.0, 0.6, 0.35, 0.15], 0.1, r, jitter=0.04)
    y[: int(0.003 * SR)] += burst(0.003, 3000, 8000, 0.0009, r)[: int(0.003 * SR)] * 0.9
    return peak(y, -5)


def typing(n=16, v=0):
    r = np.random.default_rng(300 + v)
    t, out = 0.05, np.zeros(int(2.6 * SR), np.float32)
    for i in range(n):
        space = i in (5, 11)
        k = thock(v=i, up=True, low=0.8 if space else 1.0 + r.uniform(-0.06, 0.06)) * (1.1 if space else r.uniform(0.62, 0.9))
        if space:  # the space bar rattles a little
            k = add(k, np.pad(modal([2400, 3100], [0.02, 0.015], [0.08, 0.05], 0.06, r), (int(0.004 * SR), 0)))
        place(out, k, t)
        t += r.normal(0.118, 0.028) * (1.6 if space else 1.0)
    return out[: int((t + 0.25) * SR)]


# ---------------------------------------------------------------- contacts and magnets
def relay(v=0, release=True):
    r = np.random.default_rng(400 + v)
    y = np.zeros(int(0.3 * SR), np.float32)
    for at, g in ((0.0, 1.0), (0.0042, 0.45), (0.0071, 0.2)):     # contact bounce
        c = add(burst(0.0015, 2500, 9000, 0.0005, r), modal([2380, 3720, 5150], [0.012, 0.008, 0.005], [0.35, 0.22, 0.12], 0.04, r))
        place(y, c * g, at)
    place(y, np.sin(2 * np.pi * 140 * T(0.03)) * np.exp(-T(0.03) / 0.008) * 0.5, 0.0)
    if release:
        c = add(burst(0.001, 3000, 9000, 0.0004, r), modal([2900, 4400], [0.008, 0.005], [0.25, 0.12], 0.03, r))
        place(y, c * 0.4, 0.13)
    return peak(y, -6)


def latch(v=0):
    """A magnetic snap: a short approach swish, a sharp contact with a metal ring, a low thud."""
    r = np.random.default_rng(500 + v)
    y = np.zeros(int(0.45 * SR), np.float32)
    sw = fx.bq(fx.bq(noise(int(0.03 * SR), r), "bp", 2600, q=0.9), "lp", 6000) * np.linspace(0, 1, int(0.03 * SR)) ** 2 * 0.22
    place(y, sw, 0.0)
    hit = add(burst(0.002, 2000, 10000, 0.0006, r), modal([1740, 2610, 4080], [0.09, 0.055, 0.03], [0.34, 0.2, 0.1], 0.3, r, 0.01))
    place(y, hit, 0.03)
    th = np.sin(sweep_phase(glide(120, 78, 0.12))) * np.exp(-T(0.12) / 0.045) * 0.9
    place(y, th, 0.03)
    return peak(sat(y, 1.2), -4)


def dock(v=0):
    """A card locking onto a shelf: latch + soft thock + a low whomp and a puff of air."""
    y = np.zeros(int(0.6 * SR), np.float32)
    place(y, latch(v) * 0.8, 0.0)
    place(y, thock(v, up=False, low=0.85) * 0.6, 0.028)
    wh = np.sin(sweep_phase(glide(90, 55, 0.2))) * np.exp(-T(0.2) / 0.07) * 0.5
    place(y, wh, 0.03)
    air = fx.bq(noise(int(0.12 * SR)), "bp", 1200, q=0.6) * np.exp(-T(0.12) / 0.04) * 0.08
    place(y, air, 0.035)
    return peak(y, -4)


# ---------------------------------------------------------------- motors and air
def servo(dur=0.6, f0=240, f1=470, v=0):
    r = np.random.default_rng(600 + v)
    f = glide(f0, f1, dur, "smooth")
    ph = sweep_phase(f)
    osc = sum(np.sin(k * ph) / k for k in range(1, 9))
    grain_f = 38 + 6 * r.standard_normal()
    grain = 0.75 + 0.25 * np.sign(np.sin(sweep_phase(np.full(len(f), grain_f)) + r.uniform(0, 6)))
    whine = np.sin(2 * ph) * 0.18
    y = (osc * grain + whine) * env(dur, 0.03, 0.08)
    y = fx.bq(fx.bq(y, "hp", 380), "lp", 3200)
    out = np.zeros(int((dur + 0.1) * SR), np.float32)
    place(out, y * 0.5, 0.0)
    place(out, relay(v, release=False) * 0.35, 0.0)
    place(out, relay(v + 1, release=False) * 0.3, dur - 0.01)
    return peak(out, -6)


def hydraulic(dur=0.8, v=0):
    r = np.random.default_rng(700 + v)
    n = noise(int(dur * SR), r)
    y = tv_band(n, glide(4800, 1100, dur), 0.9)
    e = np.exp(-T(dur) / (dur * 0.35)) * np.clip(T(dur) / 0.006, 0, 1)
    y = y * e
    out = np.zeros(int((dur + 0.05) * SR), np.float32)
    place(out, relay(v, release=False) * 0.4, 0.0)
    place(out, y * 0.9, 0.004)
    return peak(out, -7)


# ---------------------------------------------------------------- HUD
def tick(v=0):
    r = np.random.default_rng(800 + v)
    y = add(burst(0.0012, 1500, 4200, 0.0005, r) * 0.9, modal([920 * (1 + 0.04 * v), 1830], [0.008, 0.005], [0.35, 0.12], 0.02, r))
    return peak(y, -8)


def chatter(dur=0.9, rate=46, v=0):
    """Data chatter for text decoding: tiny grains on a fixed 'digital' set of pitches, dull, fast."""
    r = np.random.default_rng(900 + v)
    y = np.zeros(int(dur * SR), np.float32)
    pitches = np.array([1180, 1570, 1760, 2350, 2640, 3130])
    tt = 0.0
    while tt < dur - 0.02:
        L = r.uniform(0.004, 0.009)
        g = np.sin(2 * np.pi * r.choice(pitches) * T(L)) * np.hanning(int(L * SR))
        if r.random() < 0.25:
            g = burst(L, 1200, 5000, L / 3, r)[: len(g)] * 0.6
        place(y, g * r.uniform(0.3, 0.8), tt)
        tt += r.exponential(1 / rate)
    y = fx.bq(y, "lp", 5500) * env(dur, 0.02, 0.15)
    return peak(y, -10)


def confirm(v=0):
    """Two dull, rounded tones a fifth apart (triangle-ish, low-passed): tech, not twinkly."""
    y = np.zeros(int(0.32 * SR), np.float32)
    for at, f in ((0.0, 698.5), (0.07, 1046.5)):
        ph = sweep_phase(np.full(int(0.2 * SR), f))
        tri = signal.sawtooth(ph, 0.5)
        place(y, fx.bq(tri, "lp", 2400) * np.exp(-T(0.2) / 0.05) * 0.6, at)
    return peak(y, -9)


def scan(dur=0.9, v=0):
    r = np.random.default_rng(1000 + v)
    t = T(dur)
    core = np.sin(sweep_phase(1100 + 8 * np.sin(2 * np.pi * 25 * t))) * 0.25
    band = tv_band(noise(len(t), r), glide(700, 3200, dur), 0.8) * 0.8
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    y = (core + band) * e
    return pan(peak(y, -8), np.linspace(-0.8, 0.8, len(y)))


def form(dur=0.55, v=0):
    """A line energising: a low saw through a resonant low-pass that opens, a crushed layer, a tick to land."""
    t = T(dur)
    f = 110 * (1 + 0.004 * v)
    ph = sweep_phase(np.full(len(t), f))
    saw = signal.sawtooth(ph) + 0.5 * signal.sawtooth(2 * ph * 1.003)
    y = tv_band(saw, glide(260, 3600, dur), 0.55) * 1.6
    crush = np.round(y * 16) / 16
    y = y * 0.85 + fx.bq(crush, "lp", 6000) * 0.15
    y = y * env(dur, 0.02, 0.12)
    out = np.zeros(int((dur + 0.05) * SR), np.float32)
    place(out, y * 0.7, 0.0)
    place(out, tick(v) * 0.9, dur - 0.03)
    return peak(out, -6)


def power_up(dur=1.5):
    t = T(dur)
    f = glide(46, 98, dur, "smooth")
    ph = sweep_phase(f)
    hum = sum(np.sin(k * ph) * (0.6 ** k) for k in range(1, 12))
    y = tv_band(hum, glide(150, 2400, dur), 1.2) * env(dur, 0.3, 0.05)
    out = np.zeros(int((dur + 0.5) * SR), np.float32)
    place(out, sat(y * 1.2, 1.4) * 0.8, 0.0)
    place(out, latch(3) * 0.9, dur - 0.02)
    return peak(out, -4)


# ---------------------------------------------------------------- movement
def whoosh(dur=1.1, v=0):
    r = np.random.default_rng(1100 + v)
    t = T(dur)
    x = t / dur
    fc = 400 * (8 ** np.sin(np.pi * x))            # up then down: a doppler-ish pass
    y = tv_band(noise(len(t), r), fc, 1.0)
    rum = fx.bq(noise(len(t), r), "lp", 120) * 0.8
    e = np.exp(-((x - 0.55) / 0.2) ** 2)
    y = (y + rum) * e
    return pan(peak(y, -6), np.linspace(-0.85, 0.85, len(y)))


# ---------------------------------------------------------------- the stomach-drop family
def sub_drop(dur=1.8, f0=95, f1=27):
    t = T(dur)
    f = glide(f0, f1, dur)
    y = np.sin(sweep_phase(f)) * np.exp(-t / (dur * 0.7)) * np.clip(t / 0.01, 0, 1)
    y = sat(y * 1.6, 1.8)                     # harmonics so phones can 'hear' the fall
    y = y * env(dur, 0.002, 0.3, 2.0)
    return peak(fx.bq(y, "lp", 900), -3)


def thum(dur=1.5):
    t = T(dur)
    f = np.concatenate([glide(74, 43, 0.22), np.full(int((dur - 0.22) * SR), 43.0)])[: len(t)]
    y = np.sin(sweep_phase(f)) * np.exp(-t / 0.55)
    y[: int(0.003 * SR)] += burst(0.003, 600, 5000, 0.001)[: int(0.003 * SR)] * 0.6
    y = y * env(dur, 0.0005, 0.35, 2.0)
    return peak(sat(y * 1.4, 1.6), -2)


def vortex(dur=4.2, impact=True):
    """Top of the ride (inhale), a breath of nothing, then an endless falling Shepard tone over a sub that
    drops out from under you, wind rising, and (optionally) the landing."""
    out = np.zeros(int((dur + 1.6) * SR), np.float32)
    # 1. inhale: reversed swell + a small pitch lift (anticipation)
    a = 0.38
    inh = fx.bq(fx.bq(noise(int(a * SR)), "bp", 1400, q=1.1), "lp", 3000) * np.linspace(0, 1, int(a * SR)) ** 3 * 0.3
    inh += np.sin(sweep_phase(glide(180, 260, a))) * np.linspace(0, 1, int(a * SR)) ** 2 * 0.25
    inh[-int(0.008 * SR):] *= np.linspace(1, 0, int(0.008 * SR))
    place(out, inh, 0.0)
    # 2. the hang: 0.18 s of almost nothing
    t0 = a + 0.18
    fall = dur - t0 - 0.4
    # 3. the fall
    sh = shepard(fall, rate=-1.05, n=8, fmin=24, wave="rich") * env(fall, 0.05, 0.4, 1.5)
    place(out, fx.bq(sh, "lp", 5000) * 0.55, t0)
    sd = sub_drop(fall + 0.3, 110, 26) * 0.9
    place(out, sd, t0)
    wind = tv_band(noise(int(fall * SR)), glide(600, 2600, fall), 1.4) * np.linspace(0, 1, int(fall * SR)) ** 2 * 0.3
    place(out, wind, t0)
    if impact:
        place(out, thum(1.5) * 0.95, dur - 0.4)
        place(out, whoosh(0.5, 3).mean(1) * 0.2, dur - 0.55)
    return peak(out, -2)


def riser(dur=3.0):
    t = T(dur)
    sh = shepard(dur, rate=+0.8, n=7, fmin=60, wave="sine") * 0.5
    nz = tv_band(noise(len(t)), glide(400, 6000, dur), 1.0) * (t / dur) ** 2
    trem_f = glide(4, 26, dur)
    trem = 0.6 + 0.4 * np.sin(sweep_phase(trem_f))
    y = (sh + nz * 0.6) * trem * (t / dur) ** 1.5
    return peak(y, -4)


def glitch(v=0):
    r = np.random.default_rng(1200 + v)
    src = np.concatenate([chatter(0.2, 80, v), form(0.3, v)])
    out, tt = np.zeros(int(0.7 * SR), np.float32), 0.0
    for L in (0.07, 0.05, 0.05, 0.035, 0.035, 0.025, 0.018, 0.012, 0.012, 0.008):
        s = src[int(r.uniform(0, 0.15) * SR):][: int(L * SR)]
        s = signal.resample(s, max(8, int(len(s) * (0.97 - tt))))
        place(out, s * np.hanning(len(s)) ** 0.2, tt)
        tt += L
    return peak(fx.bq(out, "lp", 7000), -7)


def swell(dur=2.6):
    """F-minor air (Fm9: F Ab C Eb G), slow attack, cinema room: for transitions, not a chime."""
    t = T(dur)
    y = np.zeros_like(t)
    for f in (174.6, 207.7, 261.6, 311.1, 392.0):
        for d in (-0.35, 0.35):
            y += signal.sawtooth(sweep_phase(np.full(len(t), f + d)), 0.5) * 0.12
    y = tv_band(y, glide(500, 1800, dur), 1.6)
    y += tv_band(noise(len(t)), glide(900, 3000, dur), 1.0) * 0.08
    y *= (t / dur) ** 2.2 * env(dur, 0.01, 0.12)
    return peak(y, -6)


# ---------------------------------------------------------------- render
SOUNDS = [
    ("thock", lambda: room(thock(0))),
    ("thock_set", lambda: room(np.concatenate([np.pad(thock(i), (0, int(0.18 * SR))) * (0.8 + 0.05 * (i % 3)) for i in range(6)]))),
    ("clack", lambda: room(clack(0))),
    ("typing", lambda: room(typing())),
    ("relay", lambda: room(relay(0))),
    ("latch", lambda: room(latch(0))),
    ("dock", lambda: room(dock(0))),
    ("servo", lambda: room(servo())),
    ("hydraulic", lambda: room(hydraulic())),
    ("tick_run", lambda: room(np.concatenate([np.pad(tick(i), (0, int(0.07 * SR))) for i in range(14)]))),
    ("chatter", lambda: room(chatter())),
    ("confirm", lambda: room(confirm())),
    ("scan", lambda: room(scan())),
    ("form", lambda: room(form())),
    ("power_up", lambda: room(power_up())),
    ("whoosh", lambda: room(whoosh())),
    ("sub_drop", lambda: sub_drop()),
    ("thum", lambda: thum()),
    ("vortex", lambda: room(vortex(), -14, "hall")),
    ("vortex_endless", lambda: room(vortex(5.0, impact=False), -14, "hall")),
    ("riser", lambda: room(riser(), -16, "hall")),
    ("glitch", lambda: room(glitch())),
    ("swell", lambda: room(swell(), -9, "hall")),
]


def edges(y, fin=0.001, fout=0.015):
    """No clicks at the ends of any file."""
    y = y.copy()
    a, b = int(fin * SR), int(fout * SR)
    y[:a] *= np.linspace(0, 1, a)[:, None]
    y[-b:] *= np.linspace(1, 0, b)[:, None]
    return y


def labels(names):
    """Short spoken labels for the reel (local TTS)."""
    try:
        from kokoro_onnx import Kokoro
        k = Kokoro("/opt/kokoro/kokoro-v1.0.onnx", "/opt/kokoro/voices-v1.0.bin")
    except Exception:
        return {}
    out = {}
    for i, n in enumerate(names):
        a, sr = k.create(f"{i + 1}. {n.replace('_', ' ')}.", voice="af_heart", speed=1.05)
        out[n] = fx.resample(a.astype(np.float32), sr) * 0.5
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    rendered = []
    for name, fn in SOUNDS:
        y = fn()
        y = y if y.ndim == 2 else pan(y, 0)
        y = edges(y)
        fx.save(os.path.join(OUT, name + ".wav"), y)
        rendered.append((name, y))
        print("sfx", name, f"{len(y) / SR:.2f}s")
    lab = labels([n for n, _ in rendered])
    reel = []
    for name, y in rendered:
        if name in lab:
            reel.append(pan(lab[name], 0))
            reel.append(np.zeros((int(0.25 * SR), 2), np.float32))
        reel.append(y)
        reel.append(np.zeros((int(0.7 * SR), 2), np.float32))
    fx.save(os.path.join(OUT, "palette_reel.wav"), fx.soft_limit(np.concatenate(reel), 0.95))
    print("reel done")


if __name__ == "__main__":
    main()
