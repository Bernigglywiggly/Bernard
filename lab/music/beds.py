"""New beds for The Curve (27 Sep). The liquid jungle is scrapped; these are six fresh directions, all synthesised
from nothing (no samples, so nothing to license and nothing for Content ID to claim). Each runs about 70 seconds
with an intro, a build, a main section, a breakdown and an outro, so you can hear how it moves.

  terminal     glitch / IDM, 96 BPM, D minor. Crushed clicks and stutters, an FM-bell arp in ping-pong delay, a warm
               sub and pad. Made for the ASCII look: it sounds like a machine thinking.
  tape_loop    lo-fi hip hop, 84 BPM. Dusty swung drums, jazzy Rhodes (Fm9, Bb13, Ebmaj9, C7b9), upright-ish bass,
               tape wobble and crackle. For the laid-back talk-through videos.
  night_drive  dark synth pulse, 108 BPM, A minor. An 8th-note filtered bass, gated pads, a plucked arp, a
               gated-reverb clap. Tension without cheese.
  low_orbit    cinematic pulse, 120 BPM. A ticking 16th clock, a supersaw that slowly opens, sub swells, a
               heartbeat kick and a felt-piano motif. For the awe moments.
  two_step     UK future garage, 132 BPM. Shuffled 2-step drums, deep sub, airy pads, formant "vox" chops made
               from filters (no real voice), rain and crackle. Moody and very London.
  chrome_marl  back to the A01 bed you liked: Am9 to Cmaj9 pads, felt-piano motifs, soft sub, a quiet pulse,
               grown into a full minute.
  mainframe    dark synth-orchestral, 104 BPM, D minor (28 Sep, after "too lighthearted"; the user pointed at The
               Son of Flynn, and this is an original in that style): a rolling 16th synth ostinato, strings, low
               brass swells, booms at the section changes, no drum kit.
  deep_field   dark deep house, 112 BPM, F minor (28 Sep night: "more serious... futuristic tech, deep house", slower):
               a round 4/4 kick, an off-beat bass, filtered m9 stabs with dub echoes, a pumping pad, a pulse arp.
               The user, 29 Sep: "still way too lighthearted".
  arena        dark hybrid orchestral-electronic, 100 BPM, D minor, an original in the spirit of the Tron: Legacy score
               (29 Sep: "as serious as The Son of Flynn", the arena build-up): low brass, a low-string ostinato, a
               mechanical synth arp, a sub pedal, war drums, a braam on each arrival, a Shepard tone in the breaks.

Stems are balanced to loudness targets per bed (the mix is decided by numbers, then checked), the bus gets a small
dip around 2.8 kHz so a voice sits on top, and the preview master is -14 LUFS / -1 dBTP.

    python3 beds.py              # all six -> lab/out/music/new/<name>.mp3 (+ .wav)
    python3 beds.py terminal     # just one
"""
import os
import sys

import numpy as np
from scipy import signal
from pedalboard import Chorus, Compressor, Delay, LadderFilter, Pedalboard, Reverb, Bitcrush

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import audio_fx as fx  # noqa: E402

SR = fx.SR
OUT = os.path.join(os.path.dirname(__file__), "..", "out", "music", "new")


def hz(m):
    return 440.0 * 2 ** ((np.asarray(m, float) - 69) / 12)


def T(d):
    return np.arange(int(round(d * SR))) / SR


# ---------------------------------------------------------------- the song grid and buses
class Song:
    def __init__(self, bpm, bars, swing=0.0, seed=1, tail=4.0, grid=16):
        self.bpm, self.bars, self.swing, self.grid = bpm, bars, swing, grid
        self.beat = 60.0 / bpm
        self.bar = 4 * self.beat
        self.step = self.beat / 4
        self.dur = bars * self.bar
        self.n = int((self.dur + tail) * SR)
        self.stems = {}
        self.kicks = []
        self.rng = np.random.default_rng(seed)

    def at(self, bar, step=0.0, jitter=0.0):
        """Time of a 16th step in a bar, with swing on the off 16ths and optional human jitter (seconds)."""
        s = bar * self.bar + step * self.step
        if self.swing and self.grid == 16 and int(step) % 2 == 1:
            s += self.swing * self.step
        elif self.swing and self.grid == 8 and int(step) % 4 == 2:
            s += self.swing * 2 * self.step
        if jitter:
            s += self.rng.normal(0, jitter)
        return max(0.0, s)

    def stem(self, name):
        if name not in self.stems:
            self.stems[name] = np.zeros((self.n, 2), np.float32)
        return self.stems[name]

    def put(self, name, x, t, pan=0.0, gain=1.0):
        """Place a mono or stereo clip at time t (seconds), constant-power panned."""
        buf = self.stem(name)
        i = int(round(t * SR))
        if i >= self.n:
            return
        x = np.asarray(x, np.float32)
        if x.ndim == 1:
            lg, rg = np.sqrt((1 - pan) / 2) * 1.4142, np.sqrt((1 + pan) / 2) * 1.4142
            x = np.stack([x * lg, x * rg], 1)
        if i < 0:                                   # a note nudged before zero by humanising
            x, i = x[-i:], 0
        f = min(len(x), int(0.004 * SR))            # a 4 ms fade on every clip's tail: a note cut off mid-decay clicks
        if f > 1:
            x = x.copy()
            x[-f:] *= np.linspace(1.0, 0.0, f, dtype=np.float32)[:, None]
        j = min(self.n, i + len(x))
        buf[i:j] += x[: j - i] * gain

    def duck(self, depth=0.5, rel=0.16):
        """A sidechain curve from the kicks: dips on every kick and breathes back."""
        g = np.zeros(self.n, np.float32)
        m = int(rel * 6 * SR)
        tt = np.arange(m) / SR
        curve = np.exp(-tt / rel) * np.clip(tt / 0.004, 0, 1) ** 0.5
        curve = np.maximum(curve, np.exp(-tt / rel) * (tt > 0.004))
        for tk in self.kicks:
            i = int(tk * SR)
            k = min(m, self.n - i)
            if k > 0:
                g[i:i + k] = np.maximum(g[i:i + k], curve[:k])
        return (1 - depth * g)[:, None]


def pb(x, *plugins):
    return Pedalboard(list(plugins))(np.ascontiguousarray(x.T, np.float32), SR).T


def ladder(x, cut, res=0.15, drive=1.0, chunk=512, mode=LadderFilter.Mode.LPF24):
    """A 24 dB ladder filter whose cutoff follows cut(t) (a function of seconds), in small blocks."""
    lf = LadderFilter(mode=mode, cutoff_hz=float(cut(0.0)), resonance=res, drive=drive)
    out = np.zeros_like(x)
    for i in range(0, len(x), chunk):
        lf.cutoff_hz = float(np.clip(cut(i / SR), 40, 18000))
        out[i:i + chunk] = lf.process(np.ascontiguousarray(x[i:i + chunk].T, np.float32), SR, reset=False).T
    return out


def pingpong(x, d, fb=0.38, taps=6, mix=0.3, tone=4500):
    """Echoes that bounce left, right, left..., each a little darker."""
    y = np.zeros_like(x)
    mono = x.mean(1)
    for k in range(1, taps + 1):
        s = int(k * d * SR)
        if s >= len(x):
            break
        e = np.zeros(len(x), np.float32)
        e[s:] = mono[: len(x) - s] * fb ** (k - 1)
        e = fx.bq(e, "lp", tone / (1 + 0.25 * k), q=0.6)
        y[:, (k + 1) % 2] += e
    return x + mix * y


def reverb(x, size=0.8, wet=0.3, damp=0.5, width=1.0):
    return pb(x, Reverb(room_size=size, damping=damp, wet_level=wet, dry_level=1.0, width=width))


def wobble(x, depth_ms=2.2, rate=0.5):
    """Tape wow and flutter: a slowly wandering delay."""
    n = len(x)
    t = np.arange(n) / SR
    d = depth_ms / 1000 * (np.sin(2 * np.pi * rate * t) + 0.3 * np.sin(2 * np.pi * rate * 3.7 * t + 1.3))
    d += 0.00012 * np.sin(2 * np.pi * 9.5 * t)
    idx = np.arange(n) - (d - d.min()) * SR
    return np.stack([np.interp(idx, np.arange(n), x[:, c]) for c in range(2)], 1).astype(np.float32)


def crackle(n, rng, rate=14.0, hiss=0.012):
    """Vinyl: sparse pops and a soft hiss, different on each side (a delayed copy would comb-filter in mono)."""
    def side():
        y = np.zeros(n, np.float32)
        k = rng.poisson(rate * n / SR / 2)
        pos = rng.integers(0, n, k)
        y[pos] = (rng.pareto(2.5, k) * 0.25 + 0.05) * rng.choice([-1, 1], k)
        return fx.bq(fx.bq(y, "hp", 900), "lp", 7000) + fx.bq(rng.normal(0, hiss, n).astype(np.float32), "bp", 3500, q=0.4)
    a, b = side(), side()
    return np.stack([a + 0.3 * b, b + 0.3 * a], 1)


# ---------------------------------------------------------------- oscillators and voices
def saw(f, n, ph0=0.0):
    """Band-limited saw (polyBLEP); f may be a scalar or a per-sample array."""
    dt = np.broadcast_to(np.asarray(f, np.float64) / SR, (n,))
    ph = (ph0 + np.cumsum(dt)) % 1.0
    y = 2 * ph - 1
    m = ph < dt
    x = ph[m] / dt[m]
    y[m] -= x + x - x * x - 1
    m = ph > 1 - dt
    x = (ph[m] - 1) / dt[m]
    y[m] -= x * x + x + x + 1
    return y.astype(np.float32)


def env(n, a=0.01, hold=1.0, r=0.3, d=None, s=1.0):
    """Attack, optional decay to sustain, hold (the gate) and an exponential release."""
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / max(a, 1e-4))
    if d:
        e = np.where(t < a, e, s + (1 - s) * np.exp(-(t - a) / d))
    return (e * np.where(t > hold, np.exp(-(t - hold) / max(r / 4, 1e-4)), 1.0)).astype(np.float32)


def supersaw(m, dur, rng, voices=5, detune=0.14, r=1.2, a=0.6):
    n = int((dur + r) * SR)
    L, R = np.zeros(n, np.float32), np.zeros(n, np.float32)
    for v in range(voices):
        k = (v - (voices - 1) / 2) / max(1, (voices - 1) / 2)
        y = saw(float(hz(m + k * detune)), n, rng.random())
        p = 0.75 * k
        L += y * np.sqrt((1 - p) / 2); R += y * np.sqrt((1 + p) / 2)
    e = env(n, a, dur, r)[:, None]
    return np.stack([L, R], 1) * e / voices


def sines(m, dur, rng, r=1.5, a=1.2, det=0.04):
    """The A01 pad voice: two slightly detuned sines per note, soft and clean."""
    n = int((dur + r) * SR)
    t = np.arange(n) / SR
    p1, p2 = rng.random() * 6, rng.random() * 6
    lo_, hi_ = np.sin(2 * np.pi * float(hz(m - det)) * t + p1), np.sin(2 * np.pi * float(hz(m + det)) * t + p2)
    L, R = lo_ + 0.55 * hi_, 0.55 * lo_ + hi_                                  # wide, but it still sums to mono
    return (np.stack([L, R], 1) * env(n, a, dur, r)[:, None] / 1.55).astype(np.float32)


_CACHE = {}


def rhodes(m, dur, vel=0.8):
    """FM electric piano: a 1:1 carrier/modulator whose index falls away (bright attack, round body) plus a
    faint 14:1 tine ping."""
    key = ("rh", m, round(dur, 3), round(vel, 2))
    if key in _CACHE:
        return _CACHE[key]
    n = int((dur + 1.6) * SR)
    t = np.arange(n) / SR
    f = float(hz(m))
    idx = (0.6 + 1.9 * vel) * np.exp(-t * 5.5) + 0.25
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    y += 0.10 * vel * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t * 28)
    y *= np.exp(-t * (0.55 + 0.004 * f)) * np.minimum(1, t / 0.002)
    y *= np.where(t > dur, np.exp(-(t - dur) * 9), 1.0)
    _CACHE[key] = (y * vel).astype(np.float32)
    return _CACHE[key]


def pluck(m, dur=0.6, bright=1.0, decay=3.0, K=28):
    """A plucked string / filtered saw: harmonics that die faster the higher they are."""
    key = ("pl", m, round(dur, 3), bright, decay)
    if key in _CACHE:
        return _CACHE[key]
    f = float(hz(m))
    n = int((dur + 0.4) * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(1, K + 1):
        if f * k > 16000:
            break
        y += np.sin(2 * np.pi * f * k * t + 0.7 * k) / k ** 1.05 * np.exp(-t * (decay + bright * 1.6 * k))
    y *= np.minimum(1, t / 0.0015) * np.where(t > dur, np.exp(-(t - dur) * 25), 1.0)
    _CACHE[key] = (y / 1.6).astype(np.float32)
    return _CACHE[key]


def bell(m, dur=1.6, vel=0.8, ratio=2.0, bright=1.0):
    """FM bell/mallet: a non-integer-feeling modulator (ratio) with a fast-falling index."""
    key = ("bl", m, round(dur, 3), round(vel, 2), ratio, bright)
    if key in _CACHE:
        return _CACHE[key]
    n = int((dur + 1.0) * SR)
    t = np.arange(n) / SR
    f = float(hz(m))
    idx = bright * (0.4 + 2.2 * vel) * np.exp(-t * 9) + 0.15
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * ratio * t)) * np.exp(-t * 2.2) * np.minimum(1, t / 0.001)
    _CACHE[key] = (y * vel).astype(np.float32)
    return _CACHE[key]


def felt(m, dur=2.6, vel=0.8):
    """Soft felt piano (from the A01 sound): warm harmonics, a gentle hammer thud, rounded top."""
    key = ("fe", m, round(dur, 3), round(vel, 2))
    if key in _CACHE:
        return _CACHE[key]
    t = T(dur)
    f = float(hz(m))
    x = sum(a * np.sin(2 * np.pi * f * r * t + ph) * np.exp(-t * d)
            for r, a, d, ph in ((1, 1, 1.6, 0), (2, 0.35, 2.6, 0.3), (3, 0.12, 4, 0.7), (4.01, 0.05, 6, 1.1)))
    x = x * np.minimum(1, t / 0.006) + 0.25 * fx.bq(np.random.default_rng(int(m)).normal(0, 1, len(t)), "lp", 900) * np.exp(-t * 60)
    _CACHE[key] = (fx.bq(x, "lp", 3500) * vel * 0.6).astype(np.float32)
    return _CACHE[key]


def sub(m, dur, glide_from=None, harm=0.12):
    n = int((dur + 0.08) * SR)
    t = np.arange(n) / SR
    f = np.full(n, float(hz(m)))
    if glide_from is not None:
        f = f + (float(hz(glide_from)) - f) * np.exp(-t / 0.04)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + harm * np.sin(2 * ph)
    y *= np.minimum(1, t / 0.006) * np.where(t > dur, np.exp(-(t - dur) / 0.018), 1.0)
    return (np.tanh(1.4 * y) / np.tanh(1.4)).astype(np.float32)


def formant_vox(m, dur, vowel="ah", rng=None):
    """A 'vocal' made only from filters: a buzzy saw through two formant band-passes, with a little vibrato."""
    F = {"ah": (800, 1150), "oh": (500, 850), "ee": (320, 2300)}[vowel]
    n = int((dur + 0.3) * SR)
    t = np.arange(n) / SR
    f = float(hz(m)) * (1 + 0.006 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.4))
    y = saw(f, n, 0.0) * 0.6 + saw(f * 1.003, n, 0.3) * 0.4
    v = fx.bq(y, "bp", F[0], q=5) + 0.7 * fx.bq(y, "bp", F[1], q=6)
    return (v * env(n, 0.03, dur, 0.25)).astype(np.float32)


# ---------------------------------------------------------------- drums
def kick(f0=48, f1=150, tp=0.035, ta=0.32, click=0.35, dur=0.55, soft=False, seed=0):
    t = T(dur)
    f = f0 + (f1 - f0) * np.exp(-t / tp)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / ta)
    c = fx.bq(fx.bq(np.random.default_rng(seed).normal(0, 1, len(t)), "hp", 1800), "lp", 7000) * np.exp(-t / 0.0025)
    y = np.tanh(2.0 * (y + click * c)) / np.tanh(2.0)
    if soft:
        y = fx.bq(y, "lp", 3500)
    y *= np.minimum(1, (dur - t) / 0.03)
    return y.astype(np.float32)


def snare(tone=190, dur=0.34, nt=0.11, tt=0.06, crisp=1.0, seed=1):
    t = T(dur)
    rng = np.random.default_rng(seed)
    body = np.sin(2 * np.pi * tone * t) * np.exp(-t / tt) + 0.45 * np.sin(2 * np.pi * tone * 1.62 * t) * np.exp(-t / (tt * 0.6))
    nz = rng.normal(0, 1, len(t))
    nz = (fx.bq(nz, "bp", 2200, q=0.5) + 0.5 * crisp * fx.bq(fx.bq(nz, "hp", 6000), "lp", 10000)) * np.exp(-t / nt)
    y = 0.55 * body + 0.9 * nz
    return (y * np.minimum(1, t / 0.0008) / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def clap(dur=0.45, seed=2):
    t = T(dur)
    rng = np.random.default_rng(seed)
    nz = fx.bq(rng.normal(0, 1, len(t)), "bp", 1300, q=0.9)
    e = np.zeros(len(t))
    for k, o in enumerate((0.0, 0.009, 0.019, 0.031)):
        e += np.exp(-np.maximum(0, t - o) / 0.006) * (t >= o) * (0.8 if k < 3 else 1.0)
    e += 0.5 * np.exp(-np.maximum(0, t - 0.031) / 0.12) * (t >= 0.031)
    y = nz * e
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def rim(dur=0.12):
    t = T(dur)
    y = (np.sin(2 * np.pi * 1720 * t) * 0.6 + np.sin(2 * np.pi * 480 * t)) * np.exp(-t / 0.012)
    return (y / np.max(np.abs(y))).astype(np.float32)


_HAT_F = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)


def hat(dur=0.05, open_=False, seed=3, metal=0.6, tone=8000):
    """808-style metal (six square waves) plus noise, band-passed high."""
    d = 0.35 if open_ else dur
    t = T(d + 0.05)
    rng = np.random.default_rng(seed)
    sq = sum(np.sign(np.sin(2 * np.pi * f * 2.0 * t + rng.random() * 6)) for f in _HAT_F) / 6
    y = metal * sq + (1 - metal) * rng.normal(0, 1, len(t))
    y = fx.bq(fx.bq(y, "hp", tone), "hp", tone * 0.9)
    y = fx.bq(fx.bq(y, "lp", 11500), "lp", 11500) * np.exp(-t / (d / 3.2))           # silky, not fizzy
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def shaker(seed=4):
    t = T(0.12)
    rng = np.random.default_rng(seed)
    y = fx.bq(rng.normal(0, 1, len(t)), "bp", 6500, q=0.8) * np.minimum(1, t / 0.02) * np.exp(-t / 0.035)
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def grain(rng, dur=None):
    """A glitch grain: a tiny band of noise or a pitched blip, in a smooth window (clicky in feel, never in fact)."""
    d = dur or rng.uniform(0.005, 0.02)
    t = T(d)
    if rng.random() < 0.55:
        y = fx.bq(rng.normal(0, 1, len(t)), "bp", rng.uniform(2200, 6000), q=1.4)
    else:
        f = rng.uniform(1100, 4200)
        y = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    y *= np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.6
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def riser(dur, lo=300, hi=6000, seed=6):
    """Noise through a band-pass that sweeps up, swelling in."""
    t = T(dur)
    nz = np.random.default_rng(seed).normal(0, 1, (len(t), 2)).astype(np.float32)
    y = ladder(nz, lambda tt: lo * (hi / lo) ** (tt / dur), 0.35, 1.0, 256, LadderFilter.Mode.BPF12)
    return (y * ((t / dur) ** 2)[:, None] / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


# ---------------------------------------------------------------- harmony
Q = {"m9": [0, 3, 7, 10, 14], "maj7": [0, 4, 7, 11], "maj9": [0, 4, 7, 11, 14], "maj7#11": [0, 4, 7, 11, 18],
     "7sus4": [0, 5, 7, 10], "m7": [0, 3, 7, 10], "m11": [0, 3, 7, 10, 14, 17], "13": [0, 4, 10, 14, 21],
     "7b9": [0, 4, 7, 10, 13], "6/9": [0, 4, 7, 9, 14], "sus2": [0, 2, 7, 14], "add9": [0, 4, 7, 14],
     "m": [0, 3, 7], "maj": [0, 4, 7], "sus4": [0, 5, 7], "madd9": [0, 3, 7, 14]}


def voicing(root, q, lo=50, rootless=True):
    """Chord tones stacked upwards in order (so a m9 becomes 3-5-7-9, a clean stack of thirds, never a semitone
    cluster), the root left to the bass; of the possible octaves, the stack whose middle sits nearest lo + 9, so
    consecutive chords stay close together."""
    ivs = Q[q][1:] if rootless else Q[q]
    best = None
    for o in range(-2, 4):
        notes = [root + ivs[0] + 12 * o]
        for iv in ivs[1:]:
            m = root + iv
            while m <= notes[-1]:
                m += 12
            notes.append(m)
        if notes[0] < lo - 5:
            continue
        d = abs(np.mean(notes) - (lo + 9))
        if best is None or d < best[0]:
            best = (d, notes)
    return best[1]


def low(m, lo=28):
    """A bass note in [lo, lo+12): the same register for every chord."""
    while m < lo:
        m += 12
    while m >= lo + 12:
        m -= 12
    return m


def sections(song, plan):
    """plan: [(name, bars), ...] -> per bar, the section name."""
    out = []
    for name, bars in plan:
        out += [name] * bars
    assert len(out) == song.bars, (len(out), song.bars)
    return out


# ---------------------------------------------------------------- mixing
LOW_STEMS = ("sub", "kick", "bass", "cello")


def arc(song, sec, dyn):
    """A per-sample gain from per-section levels in dB; a (from, to) pair ramps across the section."""
    pts_t, pts_g = [], []
    bars = {}
    for b, name in enumerate(sec):
        bars.setdefault(name, []).append(b)
    for b, name in enumerate(sec):
        v = dyn.get(name, 0.0)
        if isinstance(v, tuple):
            k = bars[name].index(b) / max(1, len(bars[name]) - 1)
            v = v[0] + (v[1] - v[0]) * k
        pts_t += [b * song.bar + 0.25 * song.bar]
        pts_g += [v]
    g = np.interp(np.arange(song.n) / SR, pts_t, pts_g)
    return fx.db(g).astype(np.float32)[:, None]


def balance(song, targets, glue=True, pocket=True, sidechain=None, hpf=None, dyn=None):
    """Each stem cleaned below (everything but the low stems is high-passed, so the bottom belongs to the kick and
    the sub), set to its loudness target (LUFS), ducked where it pumps; then a glue compressor, a small dip where a
    voice lives, a smooth dark top (the A01 bed you liked is dark up there; the jungle was fizzy), and the master."""
    mix = np.zeros((song.n, 2), np.float32)
    hpf = hpf or {}
    for name, x in song.stems.items():
        if not np.any(x):
            continue
        if name not in LOW_STEMS:
            x = fx.bq(x, "hp", hpf.get(name, 150), q=0.6)
        tgt = targets.get(name, -24)
        L = fx.lufs(x)
        if not np.isfinite(L):
            continue
        y = x * fx.db(tgt - L)
        if sidechain and name in sidechain:
            y = y * song.duck(*sidechain[name])
        mix += y
    if dyn:
        mix = mix * arc(song, *dyn)
    if glue:
        mix = pb(mix, Compressor(threshold_db=-16, ratio=1.8, attack_ms=12, release_ms=180))
    if pocket:
        mix = fx.bq(mix, "peak", 2800, q=0.7, gain_db=-2.0)
    mix = fx.bq(fx.bq(mix, "hshelf", 9000, gain_db=-3.5), "lp", 15500, q=0.6)
    t = np.arange(song.n) / SR
    fade = np.clip((song.dur + 3.5 - t) / 3.5, 0, 1) ** 1.5
    mix *= np.minimum(1, t / 0.02)[:, None] * fade[:, None]
    return fx.master(mix, target=-14.0, ceiling_db=-1.0)


# ================================================================ 1 · TERMINAL (glitch / IDM, 96 BPM)
def terminal(bpm=96, plan=None, lead=0.0):
    """plan: the sections in bars (the default is the 70-second preview); lead: seconds of silence before bar 0,
    so a cut can put a bar line exactly on a spoken line."""
    plan = plan or [("intro", 4), ("a", 8), ("b", 8), ("break", 4), ("out", 4)]
    s = Song(bpm, sum(b for _, b in plan), swing=0.08, seed=11)
    rng = s.rng
    prog = [(38, "m9"), (34, "maj7#11"), (31, "m9"), (33, "7sus4")]          # Dm9  Bbmaj7#11  Gm9  A7sus4
    sec = sections(s, plan)
    n_intro = sum(1 for x in sec if x == "intro")
    first_break = sec.index("break") if "break" in sec else None
    arp_shape = [0, 2, 4, 1, 3, 5, 2, 4, 6, 3, 5, 2, 4, 1, 3, 0]
    for b in range(s.bars):
        root, q = prog[b % 4]
        v = voicing(root, q, 52)
        tones = sorted(set(v + [x + 12 for x in v]))
        name = sec[b]
        # the FM bell arp: always on, darker in the intro and the break
        for st in range(16):
            if name == "out" and st % 2:
                continue
            m = tones[arp_shape[st] % len(tones)]
            vel = (0.9 if st % 4 == 0 else 0.62) * rng.uniform(0.85, 1.0)
            s.put("arp", bell(m, 0.22, vel, ratio=2.0, bright=0.7 if name in ("intro", "break") else 1.0),
                  s.at(b, st, 0.002), pan=0.35 * np.sin(st * 0.8))
        # pad, one chord per bar
        for m in v:
            s.put("pad", supersaw(m, s.bar * 0.98, rng, voices=5, detune=0.12, r=1.4, a=0.35), s.at(b))
        if name in ("a", "b", "break"):
            s.put("sub", sub(low(root, 31), s.bar * 0.95), s.at(b))
        # drums: half-time kick, a rim and crushed snare, glitch hats and stutters
        if name in ("a", "b"):
            for st in (0, 10) + ((7,) if name == "b" and b % 2 else ()):
                s.put("kick", kick(46, 140, 0.03, 0.28, 0.25, soft=True), s.at(b, st, 0.001)); s.kicks.append(s.at(b, st))
            s.put("snare", snare(210, 0.28, 0.09, 0.05, 1.2), s.at(b, 8, 0.002))
            if name == "b":
                s.put("crush", snare(240, 0.2, 0.06, 0.04, 1.5, seed=b), s.at(b, 8), gain=0.9)
                s.put("snare", snare(210, 0.2, 0.07, 0.04, 1.0, seed=b + 9), s.at(b, 15, 0.002), gain=0.35)
        if name in ("a", "b", "break", "out"):
            for st in range(16):
                p = 0.55 if name == "b" else 0.35
                if rng.random() < p:
                    s.put("glitch", grain(rng), s.at(b, st, 0.001), pan=rng.uniform(-0.8, 0.8), gain=rng.uniform(0.4, 1.0))
            if name == "b" and b % 2 == 1:                                    # a 64th-note stutter at the end of the bar
                g = grain(rng, 0.012)
                for k in range(6):
                    s.put("glitch", g, s.at(b, 14) + k * s.step / 4, pan=0.6 * (-1) ** k, gain=0.9 - 0.1 * k)
    # data chatter: tiny high blips drifting across the stereo field
    for k in range(int(s.dur * 5)):
        t0 = rng.uniform(0, s.dur)
        s.put("chatter", grain(rng, 0.006), t0, pan=rng.uniform(-1, 1), gain=rng.uniform(0.2, 0.6))
    if first_break and first_break >= 2:
        s.put("fx", riser(s.bar * 2, 400, 7000), s.at(first_break - 2))
    # processing
    s.stems["arp"] = reverb(pingpong(s.stems["arp"], s.step * 3, 0.42, 6, 0.45, 5000), 0.55, 0.22, 0.6)
    cut = lambda t: 500 + 3200 * np.clip((t - n_intro * s.bar) / (8 * s.bar), 0, 1) * (1 - 0.6 * (sec[min(s.bars - 1, int(t / s.bar))] == "break"))
    s.stems["pad"] = reverb(pb(ladder(s.stems["pad"], cut, 0.22), Chorus(rate_hz=0.3, depth=0.25, mix=0.4)), 0.85, 0.35, 0.5)
    s.stems["crush"] = fx.bq(pb(s.stems["crush"], Bitcrush(bit_depth=6)), "lp", 8000)
    s.stems["glitch"] = fx.bq(pb(s.stems["glitch"], Bitcrush(bit_depth=8)), "lp", 9000)
    s.stems["snare"] = reverb(s.stems["snare"], 0.35, 0.18, 0.5)
    s.stems["chatter"] = fx.bq(s.stems["chatter"], "lp", 7000)
    mix = balance(s, {"arp": -21, "pad": -24, "sub": -23, "kick": -22, "snare": -26, "crush": -32, "glitch": -31,
                      "chatter": -41, "fx": -31},
                  sidechain={"pad": (0.35, 0.2), "sub": (0.55, 0.14), "arp": (0.15, 0.12)}, hpf={"pad": 170, "arp": 240},
                  dyn=(sec, {"intro": -3, "a": -1, "b": 0, "break": -3, "out": (-2, -4)}))
    mix = fx.master(fx.bq(mix, "peak", 380, q=0.8, gain_db=-2.5), target=-14.0)
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


# ================================================================ 2 · TAPE LOOP (lo-fi hip hop, 84 BPM)
def tape_loop():
    s = Song(84, 24, swing=0.3, seed=22)
    rng = s.rng
    prog = [(41, "m9"), (46, "13"), (39, "maj9"), (36, "7b9")]              # Fm9  Bb13  Ebmaj9  C7b9
    sec = sections(s, [("intro", 4), ("a", 8), ("b", 8), ("out", 4)])
    motif = [(0, 72), (3, 75), (6, 77), (10, 79), (14, 77)]                  # a lazy 2-bar phrase (bar 1 of 2)
    motif2 = [(0, 75), (4, 74), (8, 72), (11, 70)]
    for b in range(s.bars):
        root, q = prog[b % 4]
        v = voicing(root, q, 53)
        name = sec[b]
        # Rhodes comping: the chord on 1 (rolled a touch), a pushed stab on the 'and' of 2 some bars
        for k, m in enumerate(v):
            s.put("keys", rhodes(m, s.beat * 2.6, 0.62 + 0.1 * rng.random()), s.at(b, 0) + k * 0.012 + rng.normal(0, 0.003), pan=-0.55 + 0.35 * k)
        if b % 2 == 1 or name == "b":
            for k, m in enumerate(v):
                s.put("keys", rhodes(m, s.beat * 1.1, 0.5), s.at(b, 6) + k * 0.009, pan=0.2 - 0.1 * k)
        if name in ("a", "b"):
            bm = low(root, 33)
            s.put("bass", sub(bm, s.beat * 2.2, harm=0.3) * 0.8 + pluck(bm, s.beat * 2.2, 0.5, 4.0, 6)[: int((s.beat * 2.2 + 0.08) * SR)] * 0.25, s.at(b, 0))
            walk = 7 if (b % 2 or 10 not in Q[q]) else 10                   # the fifth, or the b7 where the chord has one
            s.put("bass", sub(low(root + walk, 33), s.beat * 1.2, harm=0.3), s.at(b, 11))
            # boom bap
            for st in (0, 7, 10) if b % 2 == 0 else (0, 10, 13):
                s.put("kick", kick(52, 120, 0.04, 0.26, 0.15, soft=True, seed=b), s.at(b, st, 0.004), gain=1.0 if st in (0, 10) else 0.7)
                s.kicks.append(s.at(b, st))
            for st in (4, 12):
                s.put("snare", snare(180, 0.32, 0.12, 0.07, 0.6, seed=b), s.at(b, st, 0.005))
            if rng.random() < 0.5:
                s.put("snare", snare(200, 0.15, 0.05, 0.03, 0.4, seed=b + 50), s.at(b, 15, 0.004), gain=0.28)
            for st in range(0, 16, 2):
                s.put("hats", hat(0.045, seed=b * 16 + st, metal=0.35, tone=6500), s.at(b, st, 0.006), pan=0.25,
                      gain=(1.0 if st % 4 == 2 else 0.7) * rng.uniform(0.8, 1.0))
            if name == "b" and b % 2 == 1:
                s.put("hats", hat(open_=True, seed=b, metal=0.4, tone=6000), s.at(b, 14), pan=0.25, gain=0.5)
        if name == "b":
            m2 = motif2 if 13 not in Q[q] else [(0, 75), (4, 73), (8, 72), (11, 70)]   # Db, not D, over the C7b9
            for st, m in (motif if b % 2 == 0 else m2):
                s.put("lead", pluck(m, s.step * 2.5, 0.35, 5.0, 10), s.at(b, st, 0.004), pan=0.15, gain=0.8)
    s.stems["vinyl"] = crackle(s.n, rng, 16, 0.01)
    s.stems["keys"] = reverb(pb(s.stems["keys"], Chorus(rate_hz=1.1, depth=0.18, mix=0.35)), 0.5, 0.22, 0.6)
    s.stems["lead"] = reverb(pingpong(s.stems["lead"], s.beat * 0.75, 0.3, 4, 0.3, 3500), 0.6, 0.25, 0.6)
    s.stems["snare"] = reverb(s.stems["snare"], 0.3, 0.15, 0.7)
    mix = balance(s, {"keys": -19, "bass": -22, "kick": -21, "snare": -24, "hats": -32, "lead": -26, "vinyl": -36},
                  sidechain={"keys": (0.2, 0.2), "bass": (0.25, 0.12)}, hpf={"keys": 200, "lead": 250},
                  dyn=(sec, {"intro": -3, "a": 0, "b": 0, "out": (-1, -3)}))
    mix = fx.bq(mix, "peak", 300, q=0.8, gain_db=-2.5)
    mix = wobble(mix, 2.4, 0.45)                                              # the tape
    mix = fx.bq(fx.bq(mix, "lp", 9500, q=0.6), "lshelf", 120, gain_db=1.0)
    return fx.master(np.tanh(mix * 1.15) / 1.15, target=-14.0)


# ================================================================ 3 · NIGHT DRIVE (dark synth pulse, 108 BPM)
def night_drive(bpm=108, plan=None, lead=0.0, calm=False):
    """plan/lead as for terminal(). calm=True is the bed cut for under a voice (EP03): the same pulse and pads, but
    half-time soft kicks (rounded, no click), no claps or open hats, an 8th-note arp only in the b section, and a
    softer pad gate, so it carries the mood without asking for attention."""
    plan = plan or [("intro", 4), ("a", 8), ("b", 8), ("break", 4), ("b2", 8)]
    s = Song(bpm, sum(n for _, n in plan), seed=33)
    rng = s.rng
    claps = []
    prog = [(33, "m9"), (29, "maj9"), (38, "m9"), (40, "7sus4")]            # Am9  Fmaj9  Dm9  E7sus4
    sec = sections(s, plan)
    n_intro = sum(1 for x in sec if x == "intro")
    for b in range(s.bars):
        root, q = prog[b % 4]
        v = voicing(root, q, 52)
        name = sec[b]
        last_of_break = name == "break" and (b + 1 == s.bars or sec[b + 1] != "break")
        # the pulse: 8th-note bass (octave jumps on the offbeats in the b sections, unless calm)
        for e in range(8):
            jump = name in ("b", "b2") and e % 2 == 1 and not calm
            m = low(root, 40) + (12 if jump else 0)
            s.put("bass", pluck(m, s.step * 1.6, 0.9, 7.0, 16), s.at(b, e * 2), gain=(1.0 if e % 2 == 0 else 0.8) * (0.85 if name == "out" else 1))
            if name not in ("intro", "out"):
                s.put("sub", sub(low(root, 28), s.step * 1.8), s.at(b, e * 2), gain=0.9)
        for m in v:
            s.put("pad", supersaw(m, s.bar * 0.99, rng, voices=7, detune=0.16, r=1.0, a=0.25), s.at(b))
        if name in ("b", "b2"):
            tones = sorted(set(v + [x + 12 for x in v]))
            for st in range(0, 16, 2 if calm else 1):
                m = tones[(st * 3 + b) % len(tones)]
                s.put("arp", pluck(m, s.step * 0.9, 1.2, 9.0, 14), s.at(b, st), pan=0.5 * np.sin(st), gain=0.9 if st % 4 == 0 else 0.6)
        if name in ("a", "b", "b2"):
            for beat in ((0, 2) if calm else range(4)):
                if calm:                                                    # rounded, and eased in over 2 ms: no tick
                    k = kick(47, 140, 0.03, 0.3, 0.15, soft=True, seed=beat)
                    k[:96] *= np.sin(np.linspace(0, np.pi / 2, 96)) ** 2
                else:
                    k = kick(47, 160, 0.03, 0.3, 0.4, seed=beat)
                s.put("kick", k, s.at(b, beat * 4)); s.kicks.append(s.at(b, beat * 4))
            if calm:
                if name != "a":
                    s.put("rim", rim(), s.at(b, 8, 0.002), pan=0.1)
                    for st in range(0, 16, 2):
                        s.put("hats", hat(0.035, seed=st + 17 * b, metal=0.6), s.at(b, st, 0.002), pan=0.3, gain=0.8 if st % 4 == 2 else 0.5)
            else:
                for st in (4, 12):
                    s.put("clap", clap(seed=b), s.at(b, st, 0.002))
                    claps.append(s.at(b, st))
                for st in range(16):
                    if name != "a" or st % 2 == 0:
                        s.put("hats", hat(0.04, seed=st + 17 * b, metal=0.7), s.at(b, st, 0.002), pan=0.3,
                              gain=(1.0 if st % 4 == 2 else 0.55) * rng.uniform(0.85, 1.0))
                if name == "b2":
                    for st in (2, 6, 10, 14):
                        s.put("hats", hat(open_=True, seed=st + b), s.at(b, st), pan=-0.3, gain=0.45)
        if last_of_break:
            s.put("fx", riser(s.bar, 300, 8000), s.at(b))
    # gates and rooms
    tt = np.arange(s.n) / SR
    ph = (tt / s.step) % 1
    depth = 0.25 if calm else 0.45
    gate = (1 - depth) + depth * np.clip(1 - ph * 1.6, 0, 1)                 # a soft 16th trance gate on the pad
    s.stems["pad"] = s.stems["pad"] * gate[:, None]
    cut = lambda t: 700 + 2600 * (0.5 + 0.5 * np.sin(2 * np.pi * t / (s.bar * 8) - 1.5))
    s.stems["pad"] = reverb(ladder(s.stems["pad"], cut, 0.25), 0.8, 0.3, 0.5)
    top = 1300 if calm else 1800
    bcut = lambda t: 600 + top * np.clip((t - n_intro * s.bar) / (16 * s.bar), 0, 1) * (1 - 0.7 * (sec[min(s.bars - 1, int(t / s.bar))] in ("break", "out")))
    s.stems["bass"] = ladder(s.stems["bass"], bcut, 0.3, 1.5)
    if "arp" in s.stems:
        s.stems["arp"] = fx.bq(reverb(pingpong(s.stems["arp"], s.step * 3, 0.35, 5, 0.35, 5000), 0.6, 0.2, 0.5), "lp", 8000)
    s.stems["pad"] = pb(s.stems["pad"], Chorus(rate_hz=0.4, depth=0.3, mix=0.45))
    if "hats" in s.stems:
        s.stems["hats"] = fx.bq(s.stems["hats"], "lp", 9500)
    if claps:
        cl = fx.bq(s.stems["clap"], "lp", 9000)
        g = np.zeros(s.n, np.float32)                                         # the gated reverb: a big room cut short
        for tc in claps:
            i = int(tc * SR); k = min(s.n - i, int(0.24 * SR))
            g[i:i + k] = np.maximum(g[i:i + k], np.clip((0.24 - np.arange(k) / SR) / 0.05, 0, 1))
        s.stems["clap"] = cl + 0.7 * pb(cl, Reverb(room_size=0.95, damping=0.25, wet_level=1.0, dry_level=0.0)) * g[:, None]
    if "rim" in s.stems:
        s.stems["rim"] = reverb(s.stems["rim"], 0.6, 0.25, 0.5)
    if calm:
        levels = {"bass": -23, "sub": -25, "pad": -21, "arp": -30, "kick": -24, "rim": -31, "hats": -37, "fx": -32}
        dyn = {"intro": -3, "a": -1, "b": 0, "break": -3, "out": (-2, -5)}
    else:
        levels = {"bass": -22, "sub": -25, "pad": -23, "arp": -25, "kick": -20, "clap": -24, "hats": -33, "fx": -30}
        dyn = {"intro": -4, "a": -1, "b": 0, "break": -4, "b2": 0.5}
    mix = balance(s, levels, sidechain={"pad": (0.35 if calm else 0.5, 0.22), "bass": (0.45, 0.12), "sub": (0.6, 0.12), "arp": (0.2, 0.12)},
                  hpf={"bass": 60}, dyn=(sec, dyn))
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


# ================================================================ 4 · LOW ORBIT (cinematic pulse, 120 BPM)
def low_orbit(bpm=120, plan=None, lead=0.0):
    """plan/lead as for terminal(). Sections: its own (intro, build, main, peak, out) or the film names the engine
    uses (intro, a = main, b = peak, break = build: the clock and pads without the heartbeat, out), so a film can
    re-cut it to picture (EP05). The pad's filter opens by section instead of across a fixed 70 seconds."""
    alias = {"a": "main", "b": "peak", "break": "build"}
    plan = [(alias.get(n, n), k) for n, k in (plan or [("intro", 4), ("build", 8), ("main", 8), ("peak", 8), ("out", 8)])]
    s = Song(bpm, sum(k for _, k in plan), seed=44)
    rng = s.rng
    prog = [(36, "maj7"), (40, "m7"), (33, "m9"), (29, "maj7#11")]          # Cmaj7  Em7  Am9  Fmaj7#11, 2 bars each
    sec = sections(s, plan)
    motif = [67, 64, 62, 60]
    loud = {"intro": 0.35, "build": 0.65, "main": 1.0, "peak": 1.0, "out": 0.55}
    for b in range(s.bars):
        root, q = prog[(b // 2) % 4]
        v = voicing(root, q, 50)
        name = sec[b]
        if b % 2 == 0:
            for m in v:
                s.put("pad", supersaw(m, s.bar * 1.98, rng, voices=7, detune=0.1, r=2.5, a=1.2), s.at(b))
            s.put("sub", sub(low(root, 28), s.bar * 1.9, harm=0.05) * env(int((s.bar * 1.9 + 0.08) * SR), 1.5, s.bar * 1.9, 1.0), s.at(b))
        # the clock: muted 16th plucks on the fifth and root, louder as it builds
        if name != "out" or b < s.bars - 4:
            for st in range(16):
                m = low(root, 55) + (7 if st % 2 else 0)
                s.put("clock", pluck(m, 0.05, 1.5, 30.0, 8), s.at(b, st), pan=0.4 * (-1) ** st,
                      gain=loud[name] * (1.0 if st % 4 == 0 else 0.6))
        if name in ("main", "peak"):
            for st in (0, 3):                                                   # the heartbeat: da-dum
                s.put("kick", kick(44, 110, 0.04, 0.4, 0.1, soft=True, seed=st), s.at(b, st), gain=1.0 if st == 0 else 0.7)
                s.kicks.append(s.at(b, st))
        if name in ("main", "peak") and b % 2 == 0:
            for k, m in enumerate(motif):
                s.put("piano", felt(m + (12 if name == "peak" else 0), 2.4, 0.7), s.at(b, k * 4 + 2))
        if name == "peak":
            s.put("cello", supersaw(low(root, 40), s.bar * 0.95, rng, voices=3, detune=0.06, r=0.8, a=0.4), s.at(b))
        if name in ("main", "peak") and b % 2 == 1:                          # a high shimmer, far away
            for k, m in enumerate(v[-3:]):
                s.put("shimmer", bell(m + 24, 1.2, 0.5, ratio=3.0, bright=0.6), s.at(b, 4 + k * 4), pan=0.5 * (-1) ** k)
        if b + 1 < s.bars and sec[b + 1] != name and sec[b + 1] in ("main", "peak"):
            s.put("fx", riser(s.bar * min(3, max(1, b)), 200, 9000), s.at(max(0, b - 2) if b >= 2 else b))
    lvl = {"intro": 500, "build": 1600, "main": 3200, "peak": 4600, "out": 900}
    bt = np.arange(s.bars) * s.bar
    bc = np.array([lvl.get(n, 1500) for n in sec], float)
    if sec[0] == "intro":                                                      # the intro opens slowly
        k = [i for i, n in enumerate(sec) if n == "intro"]
        bc[k] = np.linspace(300, 1200, len(k))
    cut = lambda t: float(np.interp(t, bt + s.bar * 0.5, bc))
    s.stems["pad"] = reverb(ladder(s.stems["pad"], cut, 0.2), 0.95, 0.42, 0.4)
    if "cello" in s.stems:
        s.stems["cello"] = reverb(fx.bq(s.stems["cello"], "lp", 1600), 0.8, 0.3, 0.5)
    s.stems["clock"] = reverb(fx.bq(s.stems["clock"], "hp", 700), 0.4, 0.12, 0.7)
    if "piano" in s.stems:
        s.stems["piano"] = reverb(s.stems["piano"], 0.9, 0.4, 0.5)
    if "shimmer" in s.stems:
        s.stems["shimmer"] = fx.bq(reverb(s.stems["shimmer"], 0.97, 0.6, 0.3), "lp", 11000)
    mix = balance(s, {"pad": -19, "sub": -23, "clock": -26, "kick": -24, "piano": -24, "cello": -27, "fx": -30, "shimmer": -28},
                  sidechain={"pad": (0.2, 0.3)},
                  dyn=(sec, {"intro": (-6, -3), "build": -3, "main": 0, "peak": 1, "out": (-1, -8)}))
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


# ================================================================ 5 · TWO-STEP (UK future garage, 132 BPM)
def two_step():
    s = Song(132, 40, swing=0.42, seed=55)
    rng = s.rng
    prog = [(31, "m9"), (27, "maj7"), (36, "m9"), (38, "m7")]               # Gm9  Ebmaj7  Cm9  Dm7, 2 bars each
    sec = sections(s, [("intro", 8), ("a", 16), ("break", 4), ("b", 8), ("out", 4)])
    vowels = ["ah", "oh", "ah", "ee"]
    for b in range(s.bars):
        root, q = prog[(b // 2) % 4]
        v = voicing(root, q, 53)
        name = sec[b]
        if b % 2 == 0:
            for m in v:
                s.put("pad", supersaw(m, s.bar * 1.98, rng, voices=5, detune=0.2, r=2.0, a=0.8), s.at(b))
            if name in ("a", "b"):
                bm = low(root, 28)
                s.put("sub", sub(bm, s.bar * 1.5, glide_from=bm - 2), s.at(b))
                s.put("sub", sub(bm + 7, s.bar * 0.4), s.at(b + 1, 8))
        # vox chops: filter-made 'voices' on chord tones, chopped in 8ths with a lazy drag
        if name in ("a", "b", "break") and b % 2 == 1:
            for st, k in ((2, 0), (6, 1), (7, 2), (12, 1)):
                m = v[(k + b) % len(v)]
                s.put("vox", formant_vox(m, s.step * (1.6 if st != 12 else 3.5), vowels[(b // 2) % 4], rng), s.at(b, st, 0.004),
                      pan=0.35 * (-1) ** st)
        if name in ("a", "b"):
            for st in ((0, 10) if b % 2 == 0 else (0, 11)):                  # the 2-step kick
                s.put("kick", kick(50, 170, 0.028, 0.24, 0.35, seed=b), s.at(b, st)); s.kicks.append(s.at(b, st))
            for st in (4, 12):
                s.put("snare", snare(230, 0.26, 0.08, 0.04, 0.8, seed=b), s.at(b, st, 0.002))
                s.put("rim", rim(), s.at(b, st, 0.002), pan=0.1, gain=0.6)
            for st in range(16):                                              # shuffled hats: off-beats plus ghosts
                if st % 4 == 2 or (rng.random() < 0.35 and st % 2 == 1):
                    s.put("hats", hat(0.035, seed=b * 16 + st, metal=0.55, tone=7500), s.at(b, st, 0.003), pan=0.35,
                          gain=(1.0 if st % 4 == 2 else 0.45) * rng.uniform(0.8, 1.0))
            for st in (1, 3, 5, 9, 13):
                s.put("shaker", shaker(st + b), s.at(b, st, 0.004), pan=-0.35, gain=0.5)
        if name == "break" and b == 26:
            s.put("fx", riser(s.bar * 2, 300, 6000), s.at(b))
    s.stems["rain"] = fx.bq(crackle(s.n, rng, 30, 0.02), "lp", 8000)
    cut = lambda t: 900 + 1400 * (0.5 + 0.5 * np.sin(2 * np.pi * t / (s.bar * 8)))
    s.stems["pad"] = reverb(ladder(s.stems["pad"], cut, 0.2), 0.92, 0.45, 0.35)
    s.stems["vox"] = reverb(pingpong(s.stems["vox"], s.step * 3, 0.4, 5, 0.4, 3500), 0.9, 0.35, 0.4)
    s.stems["snare"] = reverb(s.stems["snare"], 0.6, 0.22, 0.5)
    s.stems["hats"] = fx.bq(s.stems["hats"], "lp", 9500)
    s.stems["shaker"] = fx.bq(s.stems["shaker"], "lp", 8000)
    return balance(s, {"pad": -22, "sub": -20, "vox": -25, "kick": -21, "snare": -24, "rim": -30, "hats": -34,
                       "shaker": -34, "rain": -35, "fx": -31},
                   sidechain={"pad": (0.45, 0.2), "sub": (0.5, 0.12), "vox": (0.25, 0.15)},
                   dyn=(sec, {"intro": -4, "a": 0, "break": -4, "b": 0.5, "out": (-1, -4)}))


# ================================================================ 6 · CHROME & MARL II (72 BPM, calm)
def chrome_marl(bpm=72, plan=None, lead=0.0):
    """plan/lead as for terminal(); "break" plays like the intro (pads, sub and air only), so a film can re-cut it (EP06)."""
    plan = [("intro" if n == "break" else n, k) for n, k in (plan or [("intro", 2), ("a", 8), ("b", 8), ("out", 4)])]
    s = Song(bpm, sum(k for _, k in plan), seed=66)
    rng = s.rng
    prog = [(45, "m9"), (45, "m9"), (41, "maj9"), (41, "maj9"), (48, "maj9"), (48, "maj9"), (40, "m7"), (43, "6/9")]
    sec = sections(s, plan)
    motifs = [(72, 76, 79), (74, 79, 83), (76, 79, 84), (79, 83, 86)]       # the A01 cards, rising
    for b in range(s.bars):
        root, q = prog[(b - 2) % 8] if b >= 2 else prog[0]
        v = voicing(root, q, 52, rootless=False)
        name = sec[b]
        for m in v:
            s.put("pad", sines(m, s.bar * 1.02, rng, r=2.2, a=1.6), s.at(b))
        s.put("sub", sub(low(root, 28), s.bar * 0.98, harm=0.03), s.at(b), gain=0.8)
        if name in ("a", "b") and b % 2 == 0:
            for k, m in enumerate(motifs[(b // 2) % 4]):
                s.put("piano", felt(m, 2.6, 0.75 - 0.1 * k), s.at(b, 2 + k * 3, 0.004), pan=-0.2 + 0.2 * k)
        if name == "b" and b % 2 == 1:
            s.put("piano", felt(v[-1] + 12, 3.0, 0.5), s.at(b, 8), pan=0.3)
        if name in ("a", "b"):
            for beat in range(4):                                             # a quiet glass tick on the beat
                s.put("tick", pluck(96, 0.02, 2.0, 60.0, 4), s.at(b, beat * 4, 0.002), gain=0.9 if beat == 0 else 0.55)
        if name == "b":
            for st in range(0, 16, 2):
                s.put("shaker", shaker(st + b), s.at(b, st, 0.004), pan=0.3, gain=0.8 if st % 4 == 2 else 0.45)
            s.put("kick", kick(42, 90, 0.05, 0.45, 0.0, soft=True), s.at(b, 0), gain=0.9)
            s.kicks.append(s.at(b, 0))
    n = s.n
    shared = fx.bq(rng.normal(0, 1, n).astype(np.float32), "lp", 600)
    air = np.stack([shared + 0.5 * fx.bq(rng.normal(0, 1, n).astype(np.float32), "lp", 600),
                    shared + 0.5 * fx.bq(rng.normal(0, 1, n).astype(np.float32), "lp", 600)], 1)
    s.stems["air"] = air * (0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * np.arange(n) / SR))[:, None]
    s.stems["pad"] = reverb(fx.bq(s.stems["pad"], "lp", 1900), 0.9, 0.45, 0.5)
    s.stems["piano"] = reverb(s.stems["piano"], 0.85, 0.38, 0.5)
    s.stems["tick"] = reverb(fx.bq(s.stems["tick"], "hp", 2000), 0.5, 0.2, 0.6)
    mix = balance(s, {"pad": -18, "sub": -25, "piano": -22, "tick": -34, "shaker": -34, "kick": -27, "air": -38},
                  sidechain={"pad": (0.12, 0.35)}, glue=False, dyn=(sec, {"intro": -4, "a": -1.5, "b": 0, "out": (-1, -4)}),
                  hpf={"pad": 120})
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


# ================================================================ 7 · MAINFRAME (dark synth-orchestral, 104 BPM)
def boom(dur=3.0, seed=9):
    """A cinematic impact: a sub that drops from 75 to 30 Hz under a short dark noise burst."""
    t = T(dur)
    f = 30 + 45 * np.exp(-t / 0.12)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.9)
    y = y + 0.5 * fx.bq(np.random.default_rng(seed).normal(0, 1, len(t)), "lp", 1800) * np.exp(-t / 0.07)
    return (np.tanh(1.6 * y) / np.tanh(1.6) * np.minimum(1, t / 0.002)).astype(np.float32)


def mainframe(bpm=104, plan=None, lead=0.0):
    """Dark synth-orchestral in D minor (the user, 28 Sep: "closer to The Son of Flynn"; an original piece in that
    style, not a copy of it): a rolling 16th-note synth ostinato through a filter that opens section by section,
    8th-note low pulses under a sustained sub, a string ensemble, low "brass" swells on the chord changes, deep booms
    at the section changes, and no drum kit, so it is serious and cinematic but steady enough to sit under a voice.
    plan/lead as for terminal()."""
    plan = plan or [("intro", 4), ("a", 8), ("b", 8), ("break", 4), ("b", 4), ("out", 4)]
    s = Song(bpm, sum(n for _, n in plan), seed=77)
    rng = s.rng
    sec = sections(s, plan)
    prog = [(38, "m"), (34, "maj"), (43, "m"), (45, "sus4")]                   # Dm  Bb  Gm  A(sus4 -> A), 2 bars each
    starts = [b for b in range(s.bars) if b == 0 or sec[b] != sec[b - 1]]
    for b in range(s.bars):
        root, q = prog[(b // 2) % 4]
        if q == "sus4" and b % 2 == 1:
            q = "maj"                                                          # the V resolves its suspension
        name = sec[b]
        strings = voicing(root, q, 50, rootless=False)
        tones = sorted(set(strings + [x + 12 for x in strings]))
        # the ostinato: 16ths rolling through two octaves of the chord, accents on the beat
        if name != "break":
            for st in range(16):
                m = tones[(0, 2, 4, 2, 1, 3, 5, 3)[st % 8] % len(tones)]
                s.put("arp", pluck(m, s.step * 0.95, 0.8, 10.0, 24), s.at(b, st), gain=1.0 if st % 4 == 0 else 0.62)
        # low pulses (8ths) and the sub
        if name in ("a", "b"):
            for e in range(8):
                x = saw(float(hz(low(root, 33))), int(s.step * 1.7 * SR)) * env(int(s.step * 1.7 * SR), 0.003, s.step * 1.3, 0.08)
                s.put("bass", x, s.at(b, e * 2), gain=1.0 if e % 2 == 0 else 0.75)
        if name != "out" or b < s.bars - 2:
            s.put("sub", sub(low(root, 28), s.bar * 0.98, harm=0.08) * env(int((s.bar * 0.98 + 0.08) * SR), 0.08, s.bar * 0.9, 0.3), s.at(b))
        # strings (every chord, two bars long), the low line, and the violins an octave up in b
        if b % 2 == 0:
            for m in strings:
                s.put("strings", supersaw(m, s.bar * 1.96, rng, voices=7, detune=0.09, r=1.6, a=0.7), s.at(b))
            if name != "intro":
                s.put("cello", supersaw(low(root, 38), s.bar * 1.96, rng, voices=3, detune=0.05, r=1.2, a=0.5), s.at(b))
            if name == "b":
                s.put("violins", supersaw(strings[-1] + 12, s.bar * 1.96, rng, voices=5, detune=0.07, r=1.8, a=1.1), s.at(b))
                for m in (low(root, 38), low(root, 38) + 7, low(root, 38) + 12):
                    s.put("brass", supersaw(m, s.bar * 1.9, rng, voices=5, detune=0.06, r=1.0, a=0.9), s.at(b))
                s.put("taiko", kick(62, 110, 0.05, 0.45, 0.08, 1.0, soft=True, seed=b), s.at(b))
        if b in starts and name in ("a", "b", "break"):
            s.put("boom", boom(seed=b), s.at(b))
        if b + 1 < s.bars and sec[b + 1] != name and sec[b + 1] in ("b", "a"):
            s.put("fx", riser(s.bar, 200, 5000, seed=b), s.at(b))
    # the ostinato's filter opens by section; the brass swells on each chord
    lvl = {"intro": 900, "a": 3200, "b": 5200, "break": 800, "out": 1000}
    bt = np.arange(s.bars) * s.bar
    bc = np.array([lvl.get(n, 1500) for n in sec], float)
    if sec[0] == "intro":                                                      # the intro opens slowly
        k = [i for i, n in enumerate(sec) if n == "intro"]
        bc[k] = np.linspace(700, 1800, len(k))
    cut = lambda t: float(np.interp(t, bt + s.bar * 0.5, bc))
    s.stems["arp"] = reverb(pingpong(ladder(s.stems["arp"], cut, 0.2), s.step * 3, 0.35, 5, 0.3, 4200), 0.7, 0.22, 0.55)
    s.stems["bass"] = ladder(s.stems["bass"], lambda t: 500 + 250 * (cut(t) > 2000), 0.25, 1.4)
    scut = lambda t: 1200 + 0.45 * cut(t)
    s.stems["strings"] = fx.bq(reverb(pb(ladder(s.stems["strings"], scut, 0.1), Chorus(rate_hz=0.25, depth=0.25, mix=0.35)), 0.92, 0.4, 0.45),
                               "peak", 300, q=0.8, gain_db=-2.5)
    if "violins" in s.stems:
        s.stems["violins"] = reverb(fx.bq(s.stems["violins"], "lp", 6000), 0.95, 0.45, 0.4)
    if "cello" in s.stems:
        s.stems["cello"] = reverb(fx.bq(s.stems["cello"], "lp", 900), 0.8, 0.3, 0.5)
    if "brass" in s.stems:
        swell = lambda t: 320 + 1700 * np.sin(np.pi * min(1.0, ((t % (2 * s.bar)) / (1.4 * s.bar)))) ** 1.5
        s.stems["brass"] = reverb(ladder(s.stems["brass"], swell, 0.15, 1.3), 0.85, 0.3, 0.5)
    if "boom" in s.stems:
        s.stems["boom"] = reverb(s.stems["boom"], 0.95, 0.5, 0.35)
    if "taiko" in s.stems:
        s.stems["taiko"] = reverb(s.stems["taiko"], 0.9, 0.35, 0.4)
    levels = {"strings": -20, "arp": -21.5, "bass": -24, "sub": -25, "cello": -25, "violins": -26, "brass": -27,
              "boom": -24, "taiko": -29, "fx": -32}
    dyn = {"intro": (-6, -2), "a": 0, "b": 1, "break": -3, "out": (-2, -9)}
    mix = balance(s, levels, hpf={"arp": 180, "strings": 160, "violins": 250, "brass": 90}, dyn=(sec, dyn))
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


# ================================================================ 8 · DEEP FIELD (dark deep house, 112 BPM)
def stab(m, dur, rng, vel=0.8):
    """A deep-house chord-stab voice: a short detuned saw that decays like a pluck, over an FM-piano body."""
    x = supersaw(m, dur, rng, voices=4, detune=0.09, r=0.3, a=0.003)
    t = np.arange(len(x)) / SR
    x = x * (0.3 + 0.7 * np.exp(-t / 0.14))[:, None]
    body = rhodes(m, dur, 0.55)
    k = min(len(x), len(body))
    x[:k] += 0.6 * body[:k, None]
    return (x * vel).astype(np.float32)


def deep_field(bpm=112, plan=None, lead=0.0, key=0):
    """Dark deep house in F minor, for the serious, futuristic topics (the user, 28 Sep night: "more serious...
    futuristic tech, sort of deep house... [the beds] don't really lock people in... too light-hearted", and slower).
    What it leans on: slow and minor reads as serious (tempo weighs even more than mode: Gagnon & Peretz, 2003); fast
    and loud background music hurts comprehension (Thompson, Schellenberg & Letnic, 2012), so it is moderate and sits
    under the voice; and a steady four-on-the-floor with a rolling off-beat bass is what makes house hypnotic: the loop
    locks you in and only the filters move.

      intro   a dark pad, a low drone, the chord stabs far away behind a closed filter, a muffled kick (the room next door)
      a       the groove: a round 4/4 kick, the off-beat bass, off-beat hats, a soft rim on 2 and 4, dub stabs on
              Fm9 Dbmaj7 Bbm9 Cm7 (two bars each, dotted-8th echoes), a pulse arp in 8ths behind a filter
      b       the peak: the arp in 16ths and opening up, a clap, longer hats and a shaker, a far glass motif
      break   no drums: the pad, the drone, the stabs' echoes, the arp filtered down, a riser back in
      out     the tail
    plan/lead as for terminal(); key moves the whole thing by semitones (-3 is D minor), so episodes can share the
    sound without sharing the exact loop."""
    plan = plan or [("intro", 4), ("a", 8), ("b", 8), ("break", 4), ("b", 8), ("out", 4)]
    s = Song(bpm, sum(n for _, n in plan), seed=88 + key)
    rng = s.rng
    sec = sections(s, plan)
    prog = [(41 + key, "m9"), (37 + key, "maj7"), (34 + key, "m9"), (36 + key, "m7")]   # Fm9 Dbmaj7 Bbm9 Cm7, two bars each
    chord = lambda b: prog[(b // 2) % 4]
    STABS = {"a": (2, 10, 18, 23, 30), "b": (2, 7, 10, 18, 23, 26, 30)}   # steps in the two-bar cycle; 30 pushes the next chord
    ARP = (0, 2, 4, 1, 3, 5, 2, 4)
    GLASS = tuple((st, m + key) for st, m in ((0, 84), (6, 80), (12, 79), (20, 75)))   # C6 Ab5 G5 Eb5: in every chord
    starts = [b for b in range(s.bars) if b == 0 or sec[b] != sec[b - 1]]
    for b in range(s.bars):
        root, q = chord(b)
        name = sec[b]
        groove = name in ("a", "b")
        v = voicing(root, q, 50)
        # the pad: the chord for two bars, low and wide
        if b % 2 == 0:
            for m in voicing(root, q, 46):
                s.put("pad", supersaw(m, s.bar * 1.97, rng, voices=7, detune=0.13, r=1.8, a=0.5), s.at(b))
        # the stabs (on the off-beats, a push into the next chord), sparse and far away outside the groove
        for st in (STABS[name] if groove else (10, 26)):
            if (b % 2) * 16 <= st < (b % 2 + 1) * 16:
                r2, q2 = chord(b + 1) if st == 30 else (root, q)
                for k, m in enumerate(voicing(r2, q2, 50)):
                    s.put("stabs", stab(m, s.step * 1.3, rng, (0.9 if st % 8 == 2 else 0.7) * rng.uniform(0.9, 1.0)),
                          s.at(b, st % 16) + 0.004 * k, pan=-0.2 + 0.13 * k)
        # the bass: off-beat sub notes between the kicks, a lead-in note before each chord change
        bm = low(root, 33)
        if groove:
            for st in (2, 6, 10, 14):
                s.put("bass", sub(bm, s.step * 1.5, harm=0.28), s.at(b, st), gain=1.0 if st != 14 else 0.85)
            if b % 2 == 1:
                s.put("bass", sub(low(chord(b + 1)[0], 33) + 12, s.step * 0.8, harm=0.28), s.at(b, 15), gain=0.6)
        elif name != "out" or b < s.bars - 2:
            n_ = int((s.bar * 0.99 + 0.08) * SR)
            s.put("sub", sub(bm, s.bar * 0.99, harm=0.1) * env(n_, 0.4, s.bar * 0.9, 0.5), s.at(b))
        # drums
        if groove:
            for beat in range(4):
                k = kick(44, 125, 0.03, 0.32, 0.1, 0.5, soft=True, seed=beat)
                k[:96] *= np.sin(np.linspace(0, np.pi / 2, 96)) ** 2           # eased in: a thump, no tick
                s.put("kick", k, s.at(b, beat * 4)); s.kicks.append(s.at(b, beat * 4))
            for st in (2, 6, 10, 14):
                s.put("hats", hat(0.09 if name == "b" else 0.05, seed=st + 13 * b, metal=0.55, tone=7000), s.at(b, st, 0.002),
                      pan=0.25, gain=rng.uniform(0.85, 1.0))
            for st in (4, 12):
                if name == "a":
                    s.put("rim", rim(), s.at(b, st, 0.002), pan=-0.1)
                else:
                    s.put("clap", clap(seed=b + st), s.at(b, st, 0.002))
            if name == "b":
                for st in range(16):
                    if st % 4:
                        s.put("shaker", shaker(seed=st + b), s.at(b, st, 0.003), pan=-0.35, gain=0.8 if st % 2 else 0.5)
        elif name == "intro":
            for beat in range(4):
                k = kick(44, 110, 0.03, 0.35, 0.0, 0.5, soft=True, seed=beat)
                s.put("kick_far", k, s.at(b, beat * 4)); s.kicks.append(s.at(b, beat * 4))
        # the arp: the machine thinking, in 8ths in a and the break, 16ths in b
        if name in ("a", "b", "break"):
            tones = sorted(set(voicing(root, q, 62) + [x + 12 for x in voicing(root, q, 62)]))
            for st in range(0, 16, 1 if name == "b" else 2):
                m = tones[ARP[(st + 16 * (b % 2)) % 8] % len(tones)]
                s.put("arp", pluck(m, s.step * 0.8, 1.1, 10.0, 16), s.at(b, st), pan=0.45 * np.sin(1.3 * st),
                      gain=(1.0 if st % 4 == 0 else 0.65))
        # the glass: a far four-note motif in b
        if name == "b" and b % 2 == 0:
            for st, m in GLASS:
                s.put("glass", bell(m, 1.6, 0.5, ratio=3.5, bright=0.7), s.at(b, st % 16) + (s.bar if st >= 16 else 0),
                      pan=0.55 if st % 12 else -0.55)
        # section changes: a riser into the groove, a low boom where it lands
        if b + 1 < s.bars and sec[b + 1] != name and sec[b + 1] in ("a", "b"):
            s.put("fx", riser(s.bar * (2 if b >= 1 else 1), 250, 6500, seed=b), s.at(max(0, b - 1)))
        if b in starts and name in ("a", "b") and b > 0 and sec[b - 1] in ("intro", "break"):
            s.put("boom", boom(2.5, seed=b), s.at(b))
    # filters: everything tonal opens by section (closed in the intro, open at the peak) and breathes over 8 bars
    lvl = {"intro": 650, "a": 1500, "b": 2500, "break": 700, "out": 800}
    bt = np.arange(s.bars) * s.bar
    bc = np.array([lvl.get(n, 1200) for n in sec], float)
    if sec[0] == "intro":
        k = [i for i, n in enumerate(sec) if n == "intro"]
        bc[k] = np.linspace(420, 1000, len(k))
    base = lambda t: float(np.interp(t, bt + s.bar * 0.5, bc))
    lfo = lambda t: 1.0 + 0.18 * np.sin(2 * np.pi * t / (8 * s.bar) - 1.2)
    s.stems["pad"] = reverb(pb(ladder(s.stems["pad"], lambda t: 0.55 * base(t) * lfo(t), 0.2), Chorus(rate_hz=0.3, depth=0.3, mix=0.4)),
                            0.9, 0.38, 0.5)
    s.stems["stabs"] = reverb(pingpong(ladder(s.stems["stabs"], lambda t: 0.9 * base(t) * lfo(t), 0.3, 1.2),
                                       s.step * 3, 0.42, 6, 0.4, 2600), 0.8, 0.28, 0.55)
    if "arp" in s.stems:
        s.stems["arp"] = reverb(pingpong(ladder(s.stems["arp"], lambda t: 1.1 * base(t) * lfo(t), 0.32, 1.1),
                                         s.step * 3, 0.35, 5, 0.3, 4000), 0.6, 0.22, 0.5)
    if "bass" in s.stems:
        s.stems["bass"] = ladder(s.stems["bass"], lambda t: 320 + 0.12 * base(t), 0.2, 1.3)
    if "kick_far" in s.stems:
        s.stems["kick_far"] = fx.bq(fx.bq(s.stems["kick_far"], "lp", 140), "lp", 140)
    for nm, (size, wet) in {"rim": (0.6, 0.25), "clap": (0.75, 0.3), "glass": (0.97, 0.55), "boom": (0.9, 0.4), "fx": (0.7, 0.3)}.items():
        if nm in s.stems:
            s.stems[nm] = reverb(s.stems[nm], size, wet, 0.5)
    for nm, f in {"hats": 9000, "shaker": 8500, "clap": 6000, "glass": 9000}.items():
        if nm in s.stems:
            s.stems[nm] = fx.bq(s.stems[nm], "lp", f)
    levels = {"pad": -21, "stabs": -22, "bass": -21, "sub": -24, "kick": -20, "kick_far": -27, "hats": -31, "shaker": -37,
              "rim": -31, "clap": -28, "arp": -26, "glass": -31, "fx": -31, "boom": -27}
    dyn = {"intro": (-5, -2), "a": 0, "b": 1, "break": -3, "out": (-2, -9)}
    mix = balance(s, levels, sidechain={"pad": (0.4, 0.22), "stabs": (0.25, 0.15), "bass": (0.3, 0.1), "arp": (0.2, 0.12),
                                        "sub": (0.3, 0.2)},
                  hpf={"pad": 120, "stabs": 180, "arp": 250, "kick_far": 20, "boom": 25, "glass": 400}, dyn=(sec, dyn))
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


# ================================================================ 9 · ARENA (dark hybrid orchestral-electronic, 100 BPM)
def shepard(dur, rate=1 / 7.0, fmin=40.0, octaves=8, centre=420.0, width=1.1, seed=12):
    """A Shepard glissando: octave-spaced sines that seem to climb for ever (the rising dread of a war-film score),
    each fading in at the bottom and out at the top. rate is in octaves a second."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    c = np.log2(centre / fmin)
    ph0 = np.random.default_rng(seed).random(octaves) * 2 * np.pi
    for k in range(octaves):
        pos = (k + rate * t) % octaves
        y += np.exp(-0.5 * ((pos - c) / width) ** 2) * np.sin(ph0[k] + 2 * np.pi * np.cumsum(fmin * 2 ** pos) / SR)
    y *= np.minimum(1, t / 1.0) * np.clip((dur - t) / 0.3, 0, 1)
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def horn(m, dur, rng, a=0.35, r=0.9):
    """A brass-section note: three saws a few cents apart, a slow breath in, a little grit. The stem's filter makes the
    'bwah' (it opens with each chord and settles)."""
    n = int((dur + r) * SR)
    f = float(hz(m))
    y = sum(saw(f * 2 ** (c / 1200), n, rng.random()) for c in (-6, 0, 5)) / 3
    return (np.tanh(1.6 * y) / np.tanh(1.6) * env(n, a, dur, r)).astype(np.float32)


def braam(m, dur=4.5, seed=3):
    """The low brass-and-synth blast on a section's arrival: the root in two octaves with its fifth, driven hard,
    through a filter that snaps open and slowly closes, and a sub dropping under it."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    y = np.zeros(n, np.float32)
    for mm, g in ((m - 12, 1.0), (m, 0.9), (m + 7, 0.6), (m + 12, 0.45)):
        for c in (-8, 0, 7):
            y += g * saw(float(hz(mm)) * 2 ** (c / 1200), n, rng.random())
    y = np.tanh(2.2 * y / 6.0)
    x = ladder(np.stack([y, y], 1).astype(np.float32), lambda tt: 170 + 2600 * np.exp(-tt / 0.4) * min(1.0, tt / 0.05), 0.25, 1.5)
    s_ = np.sin(2 * np.pi * np.cumsum(float(hz(m - 12)) * (1 + 0.6 * np.exp(-t / 0.08))) / SR) * np.exp(-t / 1.3)
    e = np.minimum(1, t / 0.03) * np.exp(-t / 1.7)
    return (x * e[:, None] + 0.7 * (s_ * np.minimum(1, t / 0.005))[:, None]).astype(np.float32)


def spicc(m, dur, rng, vel=1.0):
    """A low-strings spiccato note: two saws a hair apart, a bowed bite and a quick decay."""
    n = int((dur + 0.15) * SR)
    t = np.arange(n) / SR
    f = float(hz(m))
    y = 0.6 * saw(f, n, rng.random()) + 0.4 * saw(f * 1.004, n, rng.random())
    return (y * np.minimum(1, t / 0.006) * np.exp(-t / (dur * 0.55)) * vel).astype(np.float32)


def grid_note(m, dur, rng):
    """The arp's voice: a saw and a band-limited square (two saws half a cycle apart), with a short filter-like blip
    at the front: the pulse of the machine."""
    n = int((dur + 0.05) * SR)
    t = np.arange(n) / SR
    f = float(hz(m))
    p = rng.random()
    y = 0.6 * saw(f, n, p) + 0.25 * (saw(f, n, p) - saw(f, n, (p + 0.5) % 1.0))
    y *= np.minimum(1, t / 0.003) * np.where(t > dur, np.exp(-(t - dur) / 0.01), 1.0) * (0.55 + 0.45 * np.exp(-t / 0.06))
    return y.astype(np.float32)


def arena(bpm=100, plan=None, lead=0.0, key=0):
    """Dark hybrid orchestral-electronic in D minor, an original in the spirit of Daft Punk's Tron: Legacy score (the
    user, 29 Sep: "as serious as The Son of Flynn", and the arena build-up with the crowd chanting): low brass, a
    driving low-string ostinato, a mechanical synth arpeggio, a pedal in the sub, war drums, a braam on each arrival,
    a Shepard tone that climbs through the breaks. Nothing bright: the weight sits low, where it reads as serious
    even ducked under a voice.

      intro   strings and a D pedal, the arp in 8ths behind a closed filter
      a       the low strings in 8ths on the pedal, a heartbeat, the arp in 16ths, open fifths in the brass
      b       the arrival: a braam, the strings' 16ths on the chord's root, a driven synth bass, war drums, full brass
              chords, a slow violin line (D, Bb, F, G, Bb, A, C# and home)
      break   tremolo strings and the Shepard tone, the arp filtered down: the held breath before the next arrival
      out     the brass's last chord and the strings, dying away
    Dm Bb Gm A (i bVI iv V), two bars each. plan/lead as for terminal(); key moves it by semitones."""
    plan = plan or [("intro", 4), ("a", 8), ("b", 8), ("break", 4), ("b", 8), ("out", 4)]
    s = Song(bpm, sum(n for _, n in plan), seed=99 + key)
    rng = s.rng
    sec = sections(s, plan)
    D = 38 + key
    prog = [(D, "m"), (D - 4, "maj"), (D + 5, "m"), (D + 7, "maj")]
    chord = lambda b: prog[(b // 2) % 4]
    MEL = {0: (2, 86), 2: (1, 82), 3: (1, 77), 4: (1, 79), 5: (1, 82), 6: (1, 81), 7: (1, 85)}   # bar in the 8: (bars, note)
    ARP = (0, 1, 2, 3, 4, 3, 2, 1)
    starts = [b for b in range(s.bars) if b == 0 or sec[b] != sec[b - 1]]
    for b in range(s.bars):
        root, q = chord(b)
        name = sec[b]
        prev = sec[b - 1] if b else None
        big = name == "b"
        pedal = name in ("intro", "a")
        # strings: the chord for two bars, low and dark
        if b % 2 == 0:
            for m in voicing(root, q, 50, rootless=False):
                s.put("strings", supersaw(m, s.bar * 1.97, rng, voices=6, detune=0.1, r=1.8, a=0.9), s.at(b))
        # brass: open fifths in a (hollow, grave), the full chord in b and at the end
        if b % 2 == 0 and name in ("a", "b", "out"):
            r0 = low(root, 36)
            for m in [r0, r0 + 7, r0 + 12] + ([r0 + 12 + Q[q][1]] if name != "a" else []):
                s.put("brass", horn(m, s.bar * 1.9, rng, a=0.45 if big else 0.8), s.at(b))
        # the low strings' ostinato: 8ths on the pedal in a, 16ths on the chord's root in b
        if name in ("a", "b"):
            bm = low(D if pedal else root, 38)
            k = 1 if big else 2
            for st in range(0, 16, k):
                s.put("cello", spicc(bm + (12 if st % 8 == 6 else 0), s.step * k * 0.9, rng, 1.0 if st % 4 == 0 else 0.7),
                      s.at(b, st, 0.002))
        # the sub: the pedal, then the roots
        if name != "out" or b < s.bars - 1:
            n_ = int((s.bar * 0.99 + 0.08) * SR)
            s.put("sub", sub(low(D if pedal else root, 28), s.bar * 0.99, harm=0.15) * env(n_, 0.05, s.bar * 0.95, 0.2), s.at(b))
        # the driven synth bass and the war drums in b; a heartbeat in a
        if big:
            for e in range(8):
                x = saw(float(hz(low(root, 38))), int(s.step * 1.8 * SR), rng.random())
                s.put("bass", np.tanh(2.5 * x) * env(len(x), 0.004, s.step * 1.4, 0.06), s.at(b, e * 2), gain=1.0 if e % 2 == 0 else 0.8)
            for st, g in ((0, 1.0), (6, 0.55), (8, 0.9), (11, 0.5), (14, 0.65)):
                s.put("taiko", kick(62, 115, 0.05, 0.5, 0.06, 1.0, soft=True, seed=b * 16 + st), s.at(b, st, 0.003), gain=g)
                s.kicks.append(s.at(b, st))
            if b % 4 == 3:
                for j, st in enumerate((12, 13, 14, 15)):
                    s.put("taiko", kick(110 - 12 * j, 170 - 15 * j, 0.03, 0.25, 0.05, 0.5, soft=True, seed=j), s.at(b, st),
                          gain=0.55, pan=0.4 - 0.25 * j)
        elif name == "a":
            for st, g in ((0, 1.0), (3, 0.7)):
                s.put("heart", kick(44, 100, 0.04, 0.4, 0.0, 0.6, soft=True, seed=st), s.at(b, st), gain=g)
                s.kicks.append(s.at(b, st))
        # the arp: 8ths in the intro, 16ths after
        if name != "out":
            tones = voicing(root, q, 57, rootless=False)
            tones = sorted(set(tones + [x + 12 for x in tones]))
            for st in range(0, 16, 2 if name == "intro" else 1):
                s.put("arp", grid_note(tones[ARP[st % 8] % len(tones)], s.step * 0.8, rng), s.at(b, st),
                      pan=0.3 * np.sin(st * 0.7), gain=1.0 if st % 4 == 0 else 0.7)
        # the violins' line in b
        if big and (b % 8) in MEL:
            nb, m = MEL[b % 8]
            s.put("violins", supersaw(m + key, s.bar * nb * 0.97, rng, voices=5, detune=0.06, r=1.6, a=0.5), s.at(b), pan=0.1)
        # the breaks: tremolo strings and the Shepard tone
        if name == "break" and b % 2 == 0:
            for m in voicing(root, q, 62, rootless=False):
                x = supersaw(m, s.bar * 1.97, rng, voices=4, detune=0.08, r=1.0, a=0.3)
                tt = np.arange(len(x)) / SR
                s.put("trem", x * (0.55 + 0.45 * np.sin(2 * np.pi * 11.0 * tt))[:, None], s.at(b))
        # arrivals: a braam into b, a boom into a, the Shepard through each break, a riser before b
        if b in starts:
            if big:
                s.put("braam", braam(low(root, 38), 4.5, seed=b), s.at(b))
            elif name == "a" and prev in ("intro", "break"):
                s.put("boom", boom(3.0, seed=b), s.at(b))
            elif name == "break":
                nb = next((k for k in range(b, s.bars) if sec[k] != "break"), s.bars) - b
                s.put("shepard", shepard(nb * s.bar + 0.5), s.at(b))
        if b + 1 < s.bars and sec[b + 1] == "b" and not big:
            s.put("fx", riser(s.bar * (2 if b >= 1 else 1), 150, 5000, seed=b), s.at(max(0, b - 1)))
    # filters: the arp opens by section; the brass breathes with each chord
    lvl = {"intro": 700, "a": 1000, "b": 1800, "break": 550, "out": 600}
    bt = np.arange(s.bars) * s.bar
    bc = np.array([lvl.get(n, 900) for n in sec], float)
    if sec[0] == "intro":
        k = [i for i, n in enumerate(sec) if n == "intro"]
        bc[k] = np.linspace(420, 800, len(k))
    base = lambda t: float(np.interp(t, bt + s.bar * 0.5, bc))
    peak = lambda t: 1400.0 if sec[min(s.bars - 1, int(t / s.bar))] == "b" else 800.0
    if "arp" in s.stems:                                      # an "out"-only plan (Season One's outro) has no arp
        s.stems["arp"] = reverb(pingpong(ladder(s.stems["arp"], base, 0.42, 1.3), s.step * 3, 0.35, 5, 0.28, 3500), 0.7, 0.2, 0.55)
    s.stems["strings"] = fx.bq(reverb(pb(ladder(s.stems["strings"], lambda t: 700 + 0.8 * base(t), 0.1),
                                         Chorus(rate_hz=0.25, depth=0.25, mix=0.35)), 0.92, 0.4, 0.45), "peak", 300, q=0.8, gain_db=-2.5)
    if "brass" in s.stems:
        s.stems["brass"] = reverb(ladder(s.stems["brass"], lambda t: 250 + peak(t) * np.sin(np.pi * min(1.0, (t % (2 * s.bar)) / (1.3 * s.bar))) ** 1.5,
                                         0.12, 1.4), 0.88, 0.32, 0.5)
    for nm, (size, wet) in {"braam": (0.95, 0.45), "taiko": (0.85, 0.35), "boom": (0.9, 0.4), "fx": (0.7, 0.3), "heart": (0.5, 0.15)}.items():
        if nm in s.stems:
            s.stems[nm] = reverb(s.stems[nm], size, wet, 0.5)
    for nm, f, size, wet in (("cello", 1400, 0.6, 0.18), ("violins", 6000, 0.95, 0.45), ("trem", 4000, 0.9, 0.4), ("shepard", 3500, 0.9, 0.35)):
        if nm in s.stems:
            s.stems[nm] = reverb(fx.bq(s.stems[nm], "lp", f), size, wet, 0.5)
    if "bass" in s.stems:
        s.stems["bass"] = ladder(s.stems["bass"], lambda t: 480.0, 0.2, 1.2)
    levels = {"strings": -21, "cello": -22, "brass": -21, "braam": -23, "arp": -25, "violins": -25, "sub": -24, "bass": -22,
              "taiko": -23, "heart": -26, "trem": -27, "shepard": -28, "fx": -31, "boom": -25}
    dyn = {"intro": (-7, -3), "a": -1, "b": 1, "break": (-4, -1), "out": (-1, -9)}
    mix = balance(s, levels, sidechain={"strings": (0.15, 0.25), "bass": (0.3, 0.1), "arp": (0.12, 0.12)},
                  hpf={"strings": 110, "arp": 200, "violins": 300, "brass": 55, "braam": 25, "taiko": 30, "heart": 25, "boom": 25,
                       "trem": 250, "shepard": 120}, dyn=(sec, dyn))
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


# ================================================================ 10 · HOUSE and GARAGE (124 / 130 BPM)
def organ(m, dur, vel=0.8):
    """The garage organ stab: drawbar partials (1, 2, 3, 4, 6), a fast percussive third and a key click, decaying like a
    stab, kept round (nothing above 8 kHz)."""
    key = ("og", m, round(dur, 3), round(vel, 2))
    if key in _CACHE:
        return _CACHE[key]
    n = int((dur + 0.3) * SR)
    t = np.arange(n) / SR
    f = float(hz(m))
    y = np.zeros(n)
    for r, a in ((1, 1.0), (2, 0.6), (3, 0.32), (4, 0.2), (6, 0.07)):
        if f * r < 8000:
            y += a * np.sin(2 * np.pi * f * r * t + 0.5 * r)
    if f * 3 < 8000:
        y += 0.45 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t / 0.04)
    y *= np.exp(-t / 0.3) * np.minimum(1, t / 0.003) * np.where(t > dur, np.exp(-(t - dur) / 0.04), 1.0)
    _CACHE[key] = (y * vel / 2.3).astype(np.float32)
    return _CACHE[key]


def tom(f=220.0, dur=0.22, seed=0):
    """A soft conga: a sine that drops a little in pitch, with a tap of noise."""
    t = T(dur)
    ff = f * (1 + 0.5 * np.exp(-t / 0.012))
    y = np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t / 0.07)
    y += 0.15 * fx.bq(np.random.default_rng(seed).normal(0, 1, len(t)), "bp", 3000, q=1.0) * np.exp(-t / 0.006)
    y *= np.minimum(1, t / 0.001) * np.clip((dur - t) / 0.02, 0, 1)
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


def soft(x, ms=1.5):
    """A hit with a short attack ramp: still a tick, never a click."""
    x = np.array(x, np.float32)
    k = min(len(x), int(ms / 1000 * SR))
    x[:k] *= np.sin(np.linspace(0, np.pi / 2, k)) ** 2
    return x


def house(bpm=124, plan=None, lead=0.0, key=0, garage=False):
    """UK house with a garage swing (the user, 1 Oct: "I don't like the background music... I think we change it to
    some house music, or a bit of garage"). A four-on-the-floor kick and a rolling bass are what lock people in; the
    hats shuffle the garage way; the chords are minor ninths, so it stays grown-up under a voice. Am9 Fmaj7 Dm9 Em7
    (i VI iv v), two bars each.

      intro   the club next door: a muffled kick, quiet hats, the pad and far stabs behind a closed filter, opening
      a       the groove: kick, a clap on 2 and 4, shuffled 16th hats with an open hat on every off-beat, the rolling
              bass, sparse off-beat chord stabs, the pad pumping with the kick
      b       the peak: busier stabs with the filter open, a shaker and congas, a plucked 3-3-2 riff up high
      break   no drums: the pad, far stabs, a held sub, a riser back into the peak
      out     the groove until the last two bars, the filter closing
    garage=True (the "garage" bed, 130 BPM): the 2-step version: the kick on 1 and the and-of-3 (a beat skipped),
    heavier swing, organ stabs, gliding sub notes. plan/lead as for terminal(); key moves it by semitones."""
    plan = plan or [("intro", 4), ("a", 8), ("b", 8), ("break", 4), ("b", 8), ("out", 4)]
    s = Song(bpm, sum(n for _, n in plan), swing=0.36 if garage else 0.16, seed=124 + key + (7 if garage else 0))
    rng = s.rng
    sec = sections(s, plan)
    A = 45 + key
    prog = [(A, "m9"), (A - 4, "maj7"), (A - 7, "m9"), (A - 5, "m7")]          # Am9 Fmaj7 Dm9 Em7
    chord = lambda b: prog[(b // 2) % 4]
    if garage:
        STABS = {"a": (3, 6, 14, 19, 22, 30), "b": (2, 3, 6, 10, 14, 18, 19, 22, 26, 30)}
        BASS = ((0, 0, 5.0, 1.0), (7, 0, 2.0, 0.8), (10, 12, 1.5, 0.7), (13, 0, 2.5, 0.85))     # (step, interval, steps, gain)
    else:
        STABS = {"a": (3, 10, 19, 26, 30), "b": (3, 6, 10, 14, 19, 22, 26, 30)}             # steps in the two-bar cycle
        BASS = ((2, 0, 1.6, 1.0), (6, 0, 1.6, 1.0), (7, 12, 0.7, 0.5), (10, 0, 1.6, 1.0), (13, 0, 0.8, 0.65),
                (14, 12, 1.0, 0.75))
    RIFF = (0, 3, 6, 8, 11, 14)                                                 # 3-3-2, twice a bar
    starts = [b for b in range(s.bars) if b == 0 or sec[b] != sec[b - 1]]
    for b in range(s.bars):
        root, q = chord(b)
        name = sec[b]
        nxt = sec[b + 1] if b + 1 < s.bars else None
        groove = name in ("a", "b") or (name == "out" and b < s.bars - 2)
        # the pad: the chord for two bars, low and wide; it pumps with the kick
        if b % 2 == 0:
            for m in voicing(root, q, 47):
                s.put("pad", supersaw(m, s.bar * 1.97, rng, voices=6, detune=0.11, r=1.6, a=0.25), s.at(b))
        # the stabs, off the beat; step 30 pushes into the next chord
        for st in (STABS[name] if name in STABS else (10, 26)):
            if (b % 2) * 16 <= st < (b % 2 + 1) * 16:
                r2, q2 = chord(b + 1) if st == 30 else (root, q)
                vel = (0.9 if st % 8 in (2, 3) else 0.75) * rng.uniform(0.9, 1.0)
                for k, m in enumerate(voicing(r2, q2, 52)):
                    v_ = organ(m, s.step * 1.4, vel) if garage else stab(m, s.step * 1.2, rng, vel)
                    s.put("stabs", v_, s.at(b, st % 16) + 0.003 * k, pan=-0.24 + 0.12 * k)
        # the bass: a sine for the weight, a short plucked note an octave up so it's heard on a phone
        bm = low(root, 33)
        if groove:
            for st, iv, ln, g in BASS:
                if b % 2 == 1 and st >= 14:
                    continue
                glide = bm + iv - 2 if garage and st == 0 else None
                s.put("bass", sub(bm + iv, s.step * ln, glide_from=glide, harm=0.3), s.at(b, st), gain=g)
                s.put("bass_top", pluck(bm + iv + 12, s.step * ln * 0.9, 0.6, 8.0, 10), s.at(b, st), gain=g)
            if b % 2 == 1:                                                      # a lead-in to the next chord's root
                nb = low(chord(b + 1)[0], 33)
                s.put("bass", sub(nb + 12, s.step * 0.8, harm=0.3), s.at(b, 15), gain=0.6)
                s.put("bass_top", pluck(nb + 24, s.step * 0.8, 0.6, 8.0, 10), s.at(b, 15), gain=0.6)
        elif name == "break":
            n_ = int((s.bar * 0.99 + 0.08) * SR)
            s.put("sub", sub(bm, s.bar * 0.99, harm=0.1) * env(n_, 0.4, s.bar * 0.9, 0.5), s.at(b))
        # drums
        if groove:
            for st in (((0, 10) if b % 2 == 0 else (0, 11)) if garage else (0, 4, 8, 12)):
                k = kick(46, 150, 0.028, 0.26, 0.12, 0.42, seed=st)
                k[:96] *= np.sin(np.linspace(0, np.pi / 2, 96)) ** 2           # a knock, not a tick
                s.put("kick", k, s.at(b, st)); s.kicks.append(s.at(b, st))
            for st in (4, 12):
                s.put("clap", clap(seed=b + st), s.at(b, st, 0.002))
                s.put("snare", snare(210, 0.2, 0.06, 0.04, 0.2, seed=b + st), s.at(b, st, 0.002), gain=0.5)
                if garage:
                    s.put("rim", soft(rim()), s.at(b, st, 0.002), pan=0.1, gain=0.6)
            for st in range(16):
                if st % 4 == 2:                                                 # the house 'tss' on every off-beat
                    s.put("ohat", soft(hat(0.16, seed=st + 16 * b, metal=0.5, tone=5500)), s.at(b, st, 0.002), pan=0.2,
                          gain=rng.uniform(0.85, 1.0))
                elif garage:
                    if (st % 2 == 1 and rng.random() < 0.6) or (st % 4 == 0 and rng.random() < 0.3):
                        s.put("hats", soft(hat(0.05, seed=st + 16 * b, metal=0.55, tone=6500)), s.at(b, st, 0.003), pan=-0.3,
                              gain=(0.75 if st % 2 else 0.45) * rng.uniform(0.8, 1.0))
                else:
                    s.put("hats", soft(hat(0.06, seed=st + 16 * b, metal=0.6, tone=6500)), s.at(b, st, 0.002), pan=-0.25,
                          gain=(0.7 if st % 2 else 0.4) * rng.uniform(0.85, 1.0))
            if name == "b":
                for st in range(1, 16, 2):
                    s.put("shaker", shaker(seed=st + b), s.at(b, st, 0.003), pan=0.4, gain=0.8)
                for st, f in (((3, 330), (7, 220), (11, 330), (14, 247)) if b % 2 else ((3, 330), (10, 247), (14, 220))):
                    s.put("perc", tom(f, 0.2, seed=st + b), s.at(b, st, 0.003), pan=0.35 * (-1) ** st, gain=0.8)
            if nxt in ("a", "b") and nxt != name:                               # a clap roll into the next section
                for i, st in enumerate((13, 14, 15)):
                    s.put("clap", clap(seed=200 + b + st), s.at(b, st, 0.001), gain=0.45 + 0.2 * i)
        elif name == "intro":
            for beat in range(4):
                k = kick(46, 130, 0.03, 0.3, 0.0, 0.45, soft=True, seed=beat)
                s.put("kick_far", k, s.at(b, beat * 4)); s.kicks.append(s.at(b, beat * 4))
            for st in range(1, 16, 2):
                s.put("hats", soft(hat(0.06, seed=st + 16 * b, metal=0.6, tone=6500)), s.at(b, st, 0.002), pan=-0.25, gain=0.35)
        # the riff: plucked chord tones in 3-3-2, the hook of the peak
        if name == "b":
            tones = voicing(root, q, 66)
            for i, st in enumerate(RIFF):
                s.put("riff", pluck(tones[(i + 2 * (b % 2)) % len(tones)], s.step * 0.9, 0.9, 9.0, 14), s.at(b, st),
                      pan=0.3 * np.sin(1.7 * i), gain=1.0 if i % 3 == 0 else 0.7)
        # a riser out of the intro or a break into the peak, a low boom where it lands
        if nxt == "b" and name in ("intro", "break"):
            s.put("fx", riser(s.bar * (2 if b >= 1 else 1), 250, 6500, seed=b), s.at(max(0, b - 1)))
        if b in starts and name in ("a", "b") and b > 0 and sec[b - 1] in ("intro", "break"):
            s.put("boom", boom(2.5, seed=b), s.at(b))
    # filters: everything tonal opens by section (closed in the intro, open at the peak) and breathes over 8 bars
    lvl = {"intro": 600, "a": 1500, "b": 2600, "break": 750, "out": 900}
    bt = np.arange(s.bars) * s.bar
    bc = np.array([lvl.get(n, 1200) for n in sec], float)
    if sec[0] == "intro":
        k = [i for i, n in enumerate(sec) if n == "intro"]
        bc[k] = np.linspace(400, 1100, len(k))
    base = lambda t: float(np.interp(t, bt + s.bar * 0.5, bc))
    lfo = lambda t: 1.0 + 0.15 * np.sin(2 * np.pi * t / (8 * s.bar) - 1.2)
    s.stems["pad"] = reverb(pb(ladder(s.stems["pad"], lambda t: 0.6 * base(t) * lfo(t), 0.2), Chorus(rate_hz=0.3, depth=0.3, mix=0.4)),
                            0.88, 0.32, 0.5)
    if "stabs" in s.stems:
        s.stems["stabs"] = reverb(pingpong(ladder(s.stems["stabs"], lambda t: base(t) * lfo(t), 0.25, 1.1),
                                           s.step * 3, 0.35, 5, 0.32, 3000), 0.75, 0.25, 0.55)
    if "riff" in s.stems:
        s.stems["riff"] = reverb(pingpong(ladder(s.stems["riff"], lambda t: 1.2 * base(t), 0.3, 1.0),
                                          s.step * 3, 0.38, 5, 0.35, 3800), 0.7, 0.25, 0.5)
    if "bass_top" in s.stems:
        s.stems["bass_top"] = ladder(s.stems["bass_top"], lambda t: 500 + 0.2 * base(t), 0.25, 1.4)
    if "kick_far" in s.stems:
        s.stems["kick_far"] = fx.bq(fx.bq(s.stems["kick_far"], "lp", 160), "lp", 160)
    for nm, (size, wet) in {"clap": (0.7, 0.28), "snare": (0.6, 0.2), "rim": (0.6, 0.25), "perc": (0.6, 0.2), "boom": (0.9, 0.4),
                            "fx": (0.7, 0.3)}.items():
        if nm in s.stems:
            s.stems[nm] = reverb(s.stems[nm], size, wet, 0.5)
    for nm, f in {"hats": 8000, "ohat": 7500, "shaker": 7000, "clap": 6000, "snare": 6000, "perc": 6000, "kick": 7000}.items():
        if nm in s.stems:                                                       # 24 dB/oct: silky, never fizzy or clicky
            s.stems[nm] = fx.bq(fx.bq(s.stems[nm], "lp", f), "lp", f)
    levels = {"pad": -23, "stabs": -22, "riff": -27, "bass": -21, "bass_top": -25, "sub": -24, "kick": -19, "kick_far": -27,
              "clap": -25, "snare": -30, "rim": -31, "hats": -34, "ohat": -33, "shaker": -37, "perc": -31, "fx": -31, "boom": -27}
    dyn = {"intro": (-5, -2), "a": 0, "b": 1, "break": -3, "out": (-1, -8)}
    mix = balance(s, levels, sidechain={"pad": (0.55, 0.2), "stabs": (0.25, 0.14), "bass": (0.35, 0.09), "bass_top": (0.3, 0.09),
                                        "riff": (0.2, 0.12), "sub": (0.3, 0.2)},
                  hpf={"pad": 110, "stabs": 170, "riff": 300, "bass_top": 90, "kick_far": 20, "boom": 25, "perc": 120}, dyn=(sec, dyn))
    return np.pad(mix, ((int(lead * SR), 0), (0, 0))) if lead else mix


def garage(bpm=130, plan=None, lead=0.0, key=0):
    return house(bpm, plan, lead, key, garage=True)


BEDS = {"terminal": terminal, "tape_loop": tape_loop, "night_drive": night_drive, "low_orbit": low_orbit,
        "two_step": two_step, "chrome_marl": chrome_marl, "mainframe": mainframe, "deep_field": deep_field, "arena": arena,
        "house": house, "garage": garage}


def main():
    names = sys.argv[1:] or list(BEDS)
    os.makedirs(OUT, exist_ok=True)
    for name in names:
        _CACHE.clear()
        x = BEDS[name]()
        p = fx.save(os.path.join(OUT, name + ".wav"), x, br="192k")
        print(f"{name:12s} {len(x) / SR:5.1f}s  {fx.lufs(x):6.1f} LUFS  -> {p}", flush=True)


if __name__ == "__main__":
    main()
