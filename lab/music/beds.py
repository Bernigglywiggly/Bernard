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
     "7b9": [0, 4, 7, 10, 13], "6/9": [0, 4, 7, 9, 14], "sus2": [0, 2, 7, 14], "add9": [0, 4, 7, 14]}


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
def night_drive():
    s = Song(108, 32, seed=33)
    rng = s.rng
    claps = []
    prog = [(33, "m9"), (29, "maj9"), (38, "m9"), (40, "7sus4")]            # Am9  Fmaj9  Dm9  E7sus4
    sec = sections(s, [("intro", 4), ("a", 8), ("b", 8), ("break", 4), ("b2", 8)])
    for b in range(s.bars):
        root, q = prog[b % 4]
        v = voicing(root, q, 52)
        name = sec[b]
        # the pulse: 8th-note bass, octave jumps on the offbeats in the b sections
        for e in range(8):
            m = low(root, 40) + (12 if name in ("b", "b2") and e % 2 == 1 else 0)
            s.put("bass", pluck(m, s.step * 1.6, 0.9, 7.0, 16), s.at(b, e * 2), gain=1.0 if e % 2 == 0 else 0.8)
            if name != "intro":
                s.put("sub", sub(low(root, 28), s.step * 1.8), s.at(b, e * 2), gain=0.9)
        for m in v:
            s.put("pad", supersaw(m, s.bar * 0.99, rng, voices=7, detune=0.16, r=1.0, a=0.25), s.at(b))
        if name in ("b", "b2"):
            tones = sorted(set(v + [x + 12 for x in v]))
            for st in range(16):
                m = tones[(st * 3 + b) % len(tones)]
                s.put("arp", pluck(m, s.step * 0.9, 1.2, 9.0, 14), s.at(b, st), pan=0.5 * np.sin(st), gain=0.9 if st % 4 == 0 else 0.6)
        if name in ("a", "b", "b2"):
            for beat in range(4):
                s.put("kick", kick(47, 160, 0.03, 0.3, 0.4, seed=beat), s.at(b, beat * 4)); s.kicks.append(s.at(b, beat * 4))
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
        if name == "break" and b == 23:
            s.put("fx", riser(s.bar, 300, 8000), s.at(b))
    # gates and rooms
    gate = np.ones(s.n, np.float32)
    tt = np.arange(s.n) / SR
    ph = (tt / s.step) % 1
    gate = 0.55 + 0.45 * np.clip(1 - ph * 1.6, 0, 1)                         # a soft 16th trance gate on the pad
    s.stems["pad"] = s.stems["pad"] * gate[:, None]
    cut = lambda t: 700 + 2600 * (0.5 + 0.5 * np.sin(2 * np.pi * t / (s.bar * 8) - 1.5))
    s.stems["pad"] = reverb(ladder(s.stems["pad"], cut, 0.25), 0.8, 0.3, 0.5)
    bcut = lambda t: 600 + 1800 * np.clip((t - 4 * s.bar) / (16 * s.bar), 0, 1) * (1 - 0.7 * (sec[min(s.bars - 1, int(t / s.bar))] == "break"))
    s.stems["bass"] = ladder(s.stems["bass"], bcut, 0.3, 1.5)
    s.stems["arp"] = reverb(pingpong(s.stems["arp"], s.step * 3, 0.35, 5, 0.35, 5000), 0.6, 0.2, 0.5)
    s.stems["pad"] = pb(s.stems["pad"], Chorus(rate_hz=0.4, depth=0.3, mix=0.45))
    s.stems["hats"] = fx.bq(s.stems["hats"], "lp", 9500)
    s.stems["arp"] = fx.bq(s.stems["arp"], "lp", 8000)
    cl = fx.bq(s.stems["clap"], "lp", 9000)
    g = np.zeros(s.n, np.float32)                                             # the gated reverb: a big room cut short
    for tc in claps:
        i = int(tc * SR); k = min(s.n - i, int(0.24 * SR))
        g[i:i + k] = np.maximum(g[i:i + k], np.clip((0.24 - np.arange(k) / SR) / 0.05, 0, 1))
    s.stems["clap"] = cl + 0.7 * pb(cl, Reverb(room_size=0.95, damping=0.25, wet_level=1.0, dry_level=0.0)) * g[:, None]
    return balance(s, {"bass": -22, "sub": -25, "pad": -23, "arp": -25, "kick": -20, "clap": -24, "hats": -33, "fx": -30},
                   sidechain={"pad": (0.5, 0.22), "bass": (0.45, 0.12), "sub": (0.6, 0.12), "arp": (0.2, 0.12)},
                   hpf={"bass": 60}, dyn=(sec, {"intro": -4, "a": -1, "b": 0, "break": -4, "b2": 0.5}))


# ================================================================ 4 · LOW ORBIT (cinematic pulse, 120 BPM)
def low_orbit():
    s = Song(120, 36, seed=44)
    rng = s.rng
    prog = [(36, "maj7"), (40, "m7"), (33, "m9"), (29, "maj7#11")]          # Cmaj7  Em7  Am9  Fmaj7#11, 2 bars each
    sec = sections(s, [("intro", 4), ("build", 8), ("main", 8), ("peak", 8), ("out", 8)])
    motif = [67, 64, 62, 60]
    for b in range(s.bars):
        root, q = prog[(b // 2) % 4]
        v = voicing(root, q, 50)
        name = sec[b]
        k_in = min(1.0, b / 12)
        if b % 2 == 0:
            for m in v:
                s.put("pad", supersaw(m, s.bar * 1.98, rng, voices=7, detune=0.1, r=2.5, a=1.2), s.at(b))
            s.put("sub", sub(low(root, 28), s.bar * 1.9, harm=0.05) * env(int((s.bar * 1.9 + 0.08) * SR), 1.5, s.bar * 1.9, 1.0), s.at(b))
        # the clock: muted 16th plucks on the fifth and root, louder as it builds
        if name != "out" or b < 32:
            for st in range(16):
                m = low(root, 55) + (7 if st % 2 else 0)
                s.put("clock", pluck(m, 0.05, 1.5, 30.0, 8), s.at(b, st), pan=0.4 * (-1) ** st,
                      gain=(0.35 + 0.65 * k_in) * (1.0 if st % 4 == 0 else 0.6))
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
        if b == 17:
            s.put("fx", riser(s.bar * 3, 200, 9000), s.at(17))
    cut = lambda t: 280 + 4200 * np.clip(t / (20 * s.bar), 0, 1) ** 1.6 * (1 - 0.5 * np.clip((t - 28 * s.bar) / (8 * s.bar), 0, 1))
    s.stems["pad"] = reverb(ladder(s.stems["pad"], cut, 0.2), 0.95, 0.42, 0.4)
    s.stems["cello"] = reverb(fx.bq(s.stems["cello"], "lp", 1600), 0.8, 0.3, 0.5)
    s.stems["clock"] = reverb(fx.bq(s.stems["clock"], "hp", 700), 0.4, 0.12, 0.7)
    s.stems["piano"] = reverb(s.stems["piano"], 0.9, 0.4, 0.5)
    s.stems["shimmer"] = fx.bq(reverb(s.stems["shimmer"], 0.97, 0.6, 0.3), "lp", 11000)
    return balance(s, {"pad": -19, "sub": -23, "clock": -26, "kick": -24, "piano": -24, "cello": -27, "fx": -30, "shimmer": -28},
                   sidechain={"pad": (0.2, 0.3)},
                   dyn=(sec, {"intro": -6, "build": (-4, -1), "main": 0, "peak": 1, "out": (-1, -6)}))


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
def chrome_marl():
    s = Song(72, 22, seed=66)
    rng = s.rng
    prog = [(45, "m9"), (45, "m9"), (41, "maj9"), (41, "maj9"), (48, "maj9"), (48, "maj9"), (40, "m7"), (43, "6/9")]
    sec = sections(s, [("intro", 2), ("a", 8), ("b", 8), ("out", 4)])
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
    return balance(s, {"pad": -18, "sub": -25, "piano": -22, "tick": -34, "shaker": -34, "kick": -27, "air": -38},
                   sidechain={"pad": (0.12, 0.35)}, glue=False, dyn=(sec, {"intro": -4, "a": -1.5, "b": 0, "out": (-1, -4)}),
                   hpf={"pad": 120})


BEDS = {"terminal": terminal, "tape_loop": tape_loop, "night_drive": night_drive, "low_orbit": low_orbit,
        "two_step": two_step, "chrome_marl": chrome_marl}


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
