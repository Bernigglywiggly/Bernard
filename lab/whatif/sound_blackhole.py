"""Sound design for "What if Earth fell into a black hole?" (70 s, 48 kHz stereo). Everything is synthesised here.

Built for phone speakers as much as headphones: every sub layer has a saturated twin an octave or two up, so the bass
is still heard (the "missing fundamental") where a phone can't play 35 Hz. The big moments are few and earned: a crack
at 31 s, a build from 40 s, half a second of near-silence, then the drop at 46 s when Earth breaks up; a tape-stop into
the void at 50 s; a warm resolve at 61 s.

    python3 whatif/sound_blackhole.py   -> lab/motion/public/whatif/blackhole/sound.wav (+ sound_preview.mp3)
"""
import os
import sys

import numpy as np
from pedalboard import LadderFilter, Pedalboard, Reverb
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
sys.path.insert(0, LAB)
sys.path.insert(0, os.path.join(LAB, "sfx"))
import audio_fx as fx  # noqa: E402
import palette as P  # noqa: E402

SR = fx.SR
DUR = 70.0
N = int(DUR * SR)
OUT = os.path.join(LAB, "motion", "public", "whatif", "blackhole")
RNG = np.random.default_rng(46)
D1, D2 = 36.71, 73.42          # the key: D


def T(d):
    return np.arange(int(d * SR)) / SR


def curve(points, n=N):
    """A per-sample envelope through (seconds, value) points."""
    t = np.arange(n) / SR
    xs, ys = zip(*points)
    return np.interp(t, xs, ys).astype(np.float32)


def dbc(points):
    return fx.db(curve(points))


def osc_saw(f, n, ph=0.0):
    p = (ph + np.cumsum(np.broadcast_to(f, (n,))) / SR) % 1.0
    return (2 * p - 1).astype(np.float32)


def ladder(x, cut, res=0.2, drive=1.0):
    """LadderFilter with a time-varying cutoff (processed in blocks)."""
    out = np.zeros_like(x)
    blk = 1024
    lf = LadderFilter(mode=LadderFilter.Mode.LPF24, cutoff_hz=float(cut[0]), resonance=res, drive=drive)
    for i in range(0, len(x), blk):
        lf.cutoff_hz = float(max(30.0, cut[min(i, len(cut) - 1)]))
        out[i:i + blk] = lf(x[i:i + blk][None, :].astype(np.float32), SR, reset=False)[0]
    return out


def hall(x, size=0.92, wet=0.35, damp=0.6):
    st = x if x.ndim == 2 else np.stack([x, x], 1)
    rv = Pedalboard([Reverb(room_size=size, wet_level=wet, dry_level=1.0, damping=damp, width=1.0)])
    return rv(st.T.astype(np.float32), SR).T


def place(dst, src, at, gain=1.0):
    src = src if src.ndim == 2 else np.stack([src, src], 1)
    i = int(at * SR)
    j = min(len(dst), i + len(src))
    if j > i:
        dst[i:j] += src[: j - i] * gain
    return dst


def heard(sub, lo=70, hi=420, drive=3.0):
    """The phone-audible twin of a sub: saturated, band-limited to where small speakers live."""
    return fx.bq(fx.bq(P.sat(sub * 1.2, drive), "hp", lo), "lp", hi)


# ---------------------------------------------------------------- layers
def drone():
    """D1 sub with a slow downward drift (gravity), its audible twin, rising to the break, gone in the void."""
    drift = curve([(0, 1.0), (46, 0.94), (70, 0.9)])
    f = D1 * drift * (1 + 0.004 * np.sin(2 * np.pi * 0.07 * np.arange(N) / SR))
    sub = np.sin(P.sweep_phase(f)).astype(np.float32)
    sub = sub + 0.35 * np.sin(2 * P.sweep_phase(f)).astype(np.float32)
    lvl = dbc([(0, -28), (8, -24), (30, -16), (44, -10), (45.4, -9), (45.5, -45), (46.0, -12), (49, -14),
               (50.2, -22), (51.5, -60), (60.5, -60), (63, -18), (68.5, -26), (70, -80)])
    y = sub * lvl
    return y + heard(y, drive=2.5) * 1.15


def pad():
    """Dark Dm cluster on detuned saws behind a filter that opens towards the break; a lifted chord at the end."""
    n = N
    y = np.zeros(n, np.float32)
    dark = [D2, 110.0, 130.81, 174.61]                  # D2 A2 C3 F3
    for k, fr in enumerate(dark):
        for det in (-0.35, 0.0, 0.4):
            y += osc_saw(fr * 2 ** (det / 1200 * 12), n, RNG.uniform()) * 0.18
    cut = curve([(0, 260), (20, 420), (40, 1100), (45.4, 1700), (46, 300), (50, 700), (70, 400)])
    y = ladder(y, cut, res=0.25)
    y *= dbc([(0, -40), (6, -28), (30, -22), (45.4, -18), (45.5, -50), (46.4, -24), (50.2, -26), (51.5, -55),
              (70, -80)])
    lift = np.zeros(n, np.float32)
    for fr in (D2, 110.0, 164.81, 185.0, 220.0):            # D2 A2 E3 F#3 A3: open, not sad
        lift += np.sin(2 * np.pi * fr * np.arange(n) / SR + RNG.uniform(0, 6.28)).astype(np.float32) * 0.2
    lift *= dbc([(0, -90), (60.8, -90), (63.5, -20), (66, -21), (69.5, -70), (70, -90)])
    return hall(y + lift, 0.95, 0.45)


def wind():
    """Air that rises and brightens, swirling left to right; it roars after the drop, then the void takes it."""
    n = P.noise(N, RNG)
    fc = curve([(0, 250), (12, 400), (30, 900), (45.4, 2600), (46, 1500), (49, 2200), (50.5, 300), (70, 300)])
    y = P.tv_band(n, fc, bw_oct=1.2)
    y *= dbc([(0, -34), (10, -30), (30, -24), (45.3, -16), (45.5, -50), (46.1, -14), (49.5, -18), (50.6, -60),
              (70, -80)])
    swirl = 0.65 * np.sin(2 * np.pi * np.cumsum(curve([(0, 0.05), (45, 0.45), (50, 0.2)])) / SR)
    return P.pan(y, swirl)


def fall():
    """An endless Shepard-Risset descent under the second half: the fall that never arrives. Cut dead at the gap."""
    d = 26.0
    y = P.shepard(d, rate=-0.16, n=8, fmin=30.0, wave="saw")
    y = fx.bq(fx.bq(y, "hp", 90), "lp", 2400)
    y *= np.interp(np.arange(len(y)) / SR, [0, 6, 18, 25.3, 25.4], [0, 0.25, 0.7, 1.0, 0]).astype(np.float32)
    return hall(y * fx.db(-17), 0.85, 0.3)


def debris(t0, t1, density0, density1, seed=7):
    """Rock knocks and crumbles, sparse to dense (events per second), scattered across the stereo field."""
    r = np.random.default_rng(seed)
    out = np.zeros((N, 2), np.float32)
    t = t0
    while t < t1:
        dens = density0 + (density1 - density0) * (t - t0) / (t1 - t0)
        t += r.exponential(1.0 / dens)
        f = r.uniform(70, 220)
        knock = P.modal([f, f * 2.3, f * 3.9], [0.12, 0.07, 0.04], [1, 0.4, 0.2], 0.35, r, 0.05)
        b = P.burst(0.25, 300, 3500, 0.03, r) * 0.5
        knock[: len(b)] += b[: len(knock)]
        place(out, P.pan(knock * fx.db(r.uniform(-32, -20)), r.uniform(-0.9, 0.9)), t)
    return out


def groan(at, dur=3.5, f0=95, f1=44):
    """Rock under stress: detuned saws sliding down behind a low filter."""
    f = P.glide(f0, f1, dur)
    y = sum(osc_saw(f * k, len(f), RNG.uniform()) for k in (1.0, 1.007, 0.993)) / 3
    y = ladder(y, np.full(len(y), 380.0), res=0.45, drive=2.0)
    y *= P.env(dur, a=0.6, r=1.4) * fx.db(-14)
    return hall(y, 0.9, 0.4), at


# ---------------------------------------------------------------- the hits
def soft_hit(sub_f=60):
    sub = np.sin(P.sweep_phase(P.glide(sub_f, 34, 1.6))) * np.exp(-T(1.6) / 0.6)
    return hall((sub + heard(sub, drive=2.0)) * fx.db(-10), 0.9, 0.3)


def crack():
    """The ground breaking: a split-second crack on top of a long sub drop and a dark ring."""
    n = int(4.5 * SR)
    y = np.zeros(n, np.float32)
    snap = P.burst(0.35, 900, 9000, 0.05) * 0.9
    sub = np.sin(P.sweep_phase(P.glide(110, 28, 3.2))) * np.exp(-T(3.2) / 1.3)
    body = P.sat(sub * 1.5, 2.6)
    ring = P.modal([D2, 98.0, 146.8, 220.0], [1.6, 1.1, 0.8, 0.5], [0.5, 0.35, 0.25, 0.12], 3.0, RNG, 0.01)
    y[: len(snap)] += snap
    y[: len(sub)] += sub * 0.9 + heard(sub, drive=3) * 0.8 + body * 0.25
    y[: len(ring)] += ring * 0.5
    return hall(y * fx.db(-7), 0.93, 0.42)


def heartbeat(t0, t1):
    """Sub pulses that speed up from one a second to four, building into the gap."""
    out = np.zeros((N, 2), np.float32)
    t = t0
    while t < t1:
        k = (t - t0) / (t1 - t0)
        pulse = np.sin(P.sweep_phase(P.glide(70, 40, 0.3))) * np.exp(-T(0.3) / 0.09)
        place(out, (pulse + heard(pulse, drive=2.2)) * fx.db(-14 + 8 * k), t)
        t += 1.0 - 0.75 * k
    return out


def riser(dur=5.0):
    n = P.noise(int(dur * SR), RNG)
    y = P.tv_band(n, np.geomspace(300, 9000, len(n)), bw_oct=0.9)
    y *= np.geomspace(fx.db(-40), fx.db(-11), len(y)).astype(np.float32)
    tone = P.shepard(dur, rate=0.5, n=7, fmin=55.0, wave="saw") * np.linspace(0, 0.18, int(dur * SR))
    return hall(y + fx.bq(tone, "hp", 120), 0.88, 0.3)


def drop():
    """The break-up: an 808-style sub (fast pitch dive, then a long fall), a distorted mid punch, a crack, a braam."""
    d = 6.0
    t = T(d)
    f = np.concatenate([P.glide(130, 34, 0.12), P.glide(34, 23, d - 0.12)])[: len(t)]
    sub = np.sin(P.sweep_phase(f)) * np.exp(-t / 2.4)
    punch = fx.bq(fx.bq(P.sat(P.noise(len(t), RNG) * 2.5, 4.0), "hp", 55), "lp", 420) * np.exp(-t / 0.28)
    snap = np.pad(P.burst(0.4, 1200, 11000, 0.06), (0, len(t)))[: len(t)]
    braam_f = np.full(len(t), D1)
    braam = sum(osc_saw(braam_f * k, len(t), RNG.uniform()) for k in (1.0, 1.005, 2.0, 2.008, 3.0))
    braam = ladder(braam / 5, np.geomspace(900, 120, len(t)), res=0.35, drive=2.5) * np.exp(-t / 2.2)
    y = sub * 1.0 + heard(sub, 60, 300, 3.5) * 0.9 + punch * 0.55 + snap * 0.7 + braam * 0.5
    return hall(y * fx.db(0.5), 0.95, 0.5)


def tape_stop(x, at, dur=1.4):
    """Everything still sounding slows to a halt (time stretching at the edge): resample with a falling rate."""
    i, j = int(at * SR), int((at + dur) * SR)
    seg = x[i:j].copy()
    rate = np.linspace(1.0, 0.05, j - i) ** 1.6
    pos = np.cumsum(rate)
    pos = np.clip(pos, 0, len(seg) - 1)
    for c in range(seg.shape[1]):
        x[i:j, c] = np.interp(pos, np.arange(len(seg)), seg[:, c]) * np.linspace(1, 0, j - i) ** 0.7
    x[j:j + int(9 * SR)] *= 0.0
    return x


def void_air(d=10.2):
    """Past the edge: a faint, glassy, slowly beating air instead of dead silence."""
    t = T(d)
    y = sum(np.sin(2 * np.pi * f * t + RNG.uniform(0, 6.28)) * (1 + 0.5 * np.sin(2 * np.pi * b * t))
            for f, b in ((880.0, 0.11), (1318.5, 0.07), (1761.0, 0.13)))
    y = y.astype(np.float32) * np.interp(t, [0, 1.5, d - 1.2, d], [0, 1, 1, 0]).astype(np.float32) * fx.db(-44)
    return hall(y, 0.97, 0.6)


# ---------------------------------------------------------------- the mix
def build():
    mix = np.zeros((N, 2), np.float32)
    place(mix, drone(), 0)
    place(mix, pad()[:N], 0)
    place(mix, wind(), 0)
    place(mix, fall(), 20.0)
    mix += debris(26, 45.3, 0.6, 9.0)
    mix += debris(46.2, 50.0, 14.0, 4.0, seed=8)
    for at, f in ((5.5, 58), (12.5, 66), (21.5, 74)):
        place(mix, soft_hit(f), at, 0.45)
    g, at = groan(29.8)
    place(mix, g, at)
    g, at = groan(37.5, 4.0, 88, 40)
    place(mix, g, at)
    place(mix, crack(), 31.0)
    mix += heartbeat(40.5, 45.3)
    place(mix, riser(4.8), 40.5)
    gap = (np.arange(N) / SR > 45.35) & (np.arange(N) / SR < 46.0)       # the held breath before the drop
    mix[gap] *= 0.04
    place(mix, drop(), 46.0)
    mix = tape_stop(mix, 50.2, 1.6)
    place(mix, soft_hit(52), 61.0, 0.5)
    place(mix, void_air(), 51.4)
    mix = fx.bq(mix, "hp", 22)
    mix = fx.bass_mono(mix, f=120.0)
    return fx.master(mix, target=-14.0, ceiling_db=-1.0)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    y = build()
    import soundfile as sf
    sf.write(os.path.join(OUT, "sound.wav"), y, SR, subtype="PCM_24")
    fx.save(os.path.join(OUT, "sound_preview.wav"), y, mp3=True, br="192k")
    print("LUFS", round(fx.lufs(y), 1), "peak dB", round(20 * np.log10(np.abs(y).max() + 1e-9), 2), "s", len(y) / SR)
