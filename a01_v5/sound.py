"""Sound design for A01 v5, synthesised (numpy + scipy), so it lands on the exact cut frames.

Hook: a quiet air bed plus whooshes on every world change, impacts on the slams, glitches on the
SIGNAL bursts, a riser into chrome, shimmer while the points become the line, a boom on the map.
Outro: a slow, warm synth pad (the "going home" feeling) for the ending template.

    python3 sound.py   ->  $A01_BUILD/audio/hook_sfx.wav, outro_music.wav
"""
import os

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, istft, sosfilt, stft

from shots import BUILD, DURATION, SHOTS

SR = 48000
RNG = np.random.default_rng(7)


def t_(dur):
    return np.arange(int(dur * SR)) / SR


def lp(x, hz, order=2):
    return sosfilt(butter(order, hz, "low", fs=SR, output="sos"), x)


def hp(x, hz, order=2):
    return sosfilt(butter(order, hz, "high", fs=SR, output="sos"), x)


def verb(x, seconds=1.6, damp=4000, wet=0.35, seed=1):
    """Cheap convolution reverb: decaying filtered noise as the impulse response."""
    n = int(seconds * SR)
    ir = np.random.default_rng(seed).normal(0, 1, n) * np.exp(-np.arange(n) / (SR * seconds / 5))
    ir = lp(ir, damp) / np.sqrt(np.sum(ir ** 2))
    return x + wet * fftconvolve(x, ir)[:len(x)]


def swept_noise(dur, f0, f1, width=0.35, seed=0):
    """Noise with a moving band-pass (STFT-domain), the core of every whoosh and riser."""
    x = np.random.default_rng(seed).normal(0, 1, int(dur * SR))
    f, tt, Z = stft(x, SR, nperseg=1024)
    centre = np.geomspace(f0, f1, Z.shape[1])
    Z *= np.exp(-0.5 * (np.log((f[:, None] + 1) / centre[None, :]) / width) ** 2)
    return istft(Z, SR, nperseg=1024)[1][:len(x)]


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


def whoosh(dur=0.5, up=True, seed=0):
    x = swept_noise(dur, 250 if up else 3500, 3500 if up else 250, seed=seed)
    return norm(x * np.sin(np.pi * np.linspace(0, 1, len(x))) ** 2)


def impact(dur=1.4, f0=95, f1=36, click=0.6, seed=0):
    t = t_(dur)
    sub = np.sin(2 * np.pi * np.cumsum(np.geomspace(f0, f1, len(t))) / SR) * np.exp(-t * 4.5)
    n = lp(np.random.default_rng(seed).normal(0, 1, len(t)), 2500) * np.exp(-t * 40) * click
    return norm(verb(sub + n, 1.2, 1800, 0.25, seed))


def tick(dur=0.05, hz=2600):
    t = t_(dur)
    return norm(np.sin(2 * np.pi * hz * t) * np.exp(-t * 160) + 0.2 * RNG.normal(0, 1, len(t)) * np.exp(-t * 400))


def glitch(dur=0.09, seed=0):
    r = np.random.default_rng(seed)
    t = t_(dur)
    sq = np.sign(np.sin(2 * np.pi * r.uniform(180, 1400) * t))
    sq = np.round(sq * np.sin(2 * np.pi * r.uniform(20, 80) * t) * 4) / 4          # 3-bit crunch
    sq = np.repeat(sq[::6], 6)[:len(t)]                                                # sample-and-hold
    return norm(sq * np.exp(-t * 18))


def riser(dur=1.0, seed=0):
    t = t_(dur)
    x = swept_noise(dur, 300, 6000, 0.3, seed) * (t / dur) ** 2
    s = np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 900, len(t))) / SR) * (t / dur) ** 3 * 0.4
    return norm(x + s)


def shimmer(dur=3.0, seed=0, density=14):
    r = np.random.default_rng(seed)
    t = t_(dur)
    out = np.zeros(len(t))
    scale = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2]
    for _ in range(int(density * dur)):
        s = int(r.uniform(0, dur * 0.85) * SR)
        f = 1175 * r.choice(scale) * r.choice([1, 2])
        n = min(len(t) - s, int(0.6 * SR))
        tt = np.arange(n) / SR
        out[s:s + n] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) * r.uniform(0.3, 1)
    return norm(verb(out, 2.2, 7000, 0.5, seed))


def place(bus, clip, at, gain_db, pan=0.0, pan_to=None):
    """Mix a mono clip into the stereo bus at time `at` (s), constant-power pan (sweeps if pan_to)."""
    s = int(at * SR)
    if s < 0:
        clip, s = clip[-s:], 0
    n = min(len(clip), bus.shape[0] - s)
    if n <= 0:
        return
    p = np.linspace(pan, pan if pan_to is None else pan_to, n)
    a = (p + 1) * np.pi / 4
    g = 10 ** (gain_db / 20)
    bus[s:s + n, 0] += clip[:n] * np.cos(a) * g
    bus[s:s + n, 1] += clip[:n] * np.sin(a) * g


def hook_sfx():
    bus = np.zeros((int(DURATION * SR) + SR, 2))
    # air bed: soft low noise with a slow breath, and a 55 Hz hum under the core worlds
    n = bus.shape[0]
    air = lp(RNG.normal(0, 1, n), 700) * (0.75 + 0.25 * np.sin(2 * np.pi * np.arange(n) / SR / 7))
    place(bus, norm(air), 0, -36, -0.3)
    place(bus, norm(air[::-1]), 0, -36, 0.3)
    hum = np.sin(2 * np.pi * 55 * np.arange(n) / SR)
    place(bus, hum, 0, -40)
    # the line drawing itself
    place(bus, riser(2.3, 1) * 0.6, 0.0, -24, -0.4, 0.4)
    # world changes: a whoosh whose peak lands on the cut, panned with the camera
    prev = None
    for i, s in enumerate(SHOTS):
        w = s["world"].split("·")[-1].strip()
        if prev is not None and w != prev and s["id"] not in ("S07", "S12", "S17"):
            place(bus, whoosh(0.55, up=i % 2 == 0, seed=i), s["t0"] - 0.3, -15, -0.7, 0.7)
        prev = w
    # orbs land, the 90 stands up, the bar rises, the +14 pops
    for at in (3.93, 4.11):
        place(bus, impact(1.0, 120, 45, 0.8, int(at * 10)), at, -14)
    place(bus, impact(0.9, 140, 60, 1.0, 3), 6.95, -16)
    place(bus, riser(0.65, 2), 13.3, -20)
    place(bus, tick(), 13.6, -14)
    place(bus, impact(0.8, 160, 70, 0.6, 5), 13.62, -18)
    place(bus, tick(0.04, 1800), 16.45, -18)
    # SIGNAL bursts: a glitch on every cut
    for f in (47, 71, 83, 87, 91, 95, 99, 103, 107, 111, 115):
        place(bus, glitch(0.09, f), 7.60 + (f - 1) / 24, -17, ((f * 7) % 11) / 5.5 - 1)
    for at in (30.4, 31.55):
        place(bus, glitch(0.12, int(at * 3)), at, -15)
        place(bus, whoosh(0.25, True, int(at)), at - 0.12, -19)
    # chrome: riser in, swoop, soft landing
    place(bus, riser(1.0, 3), 16.5, -16)
    place(bus, whoosh(0.9, True, 9), 17.5, -14, 0.8, -0.8)
    place(bus, impact(1.2, 110, 40, 0.3, 9), 19.1, -19)
    # cloud: the question lands on a low pulse
    place(bus, impact(1.8, 70, 30, 0.1, 11), 21.8, -18)
    # 'cool' snap zoom
    place(bus, whoosh(0.22, True, 13), 28.2, -16)
    place(bus, tick(0.05, 3200), 28.4, -15)
    # WRONG slams, then the spiral dive
    place(bus, impact(1.6, 100, 32, 1.0, 21), 32.5, -9)
    place(bus, impact(1.2, 120, 40, 0.8, 22), 33.6, -12)
    place(bus, whoosh(2.3, False, 23), 34.6, -16, -0.5, 0.5)
    for at in (34.65, 35.5, 36.4):
        place(bus, tick(0.05, 2200), at, -16)
    # the points become the line
    place(bus, shimmer(3.2, 31), 37.2, -20, -0.4, 0.4)
    place(bus, shimmer(1.4, 32, 22), 40.2, -17)
    # whip pan on 'hands'
    place(bus, whoosh(0.4, True, 41), 46.2, -14, -0.8, 0.8)
    # the map: boom and a long shimmer tail
    place(bus, impact(2.8, 80, 28, 0.5, 47), 47.5, -11)
    place(bus, shimmer(2.8, 48, 10), 47.6, -22)
    return bus


def outro_music(dur=12.0, bpm=68):
    """A slow, warm, hopeful pad: Dbmaj9 -> Bbm9 -> Gbmaj9 -> Ab6/9, tape wobble, soft plucks."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    chords = [[49, 56, 60, 63, 65], [46, 53, 56, 60, 61], [42, 49, 53, 56, 58], [44, 51, 56, 58, 60]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    seg = dur / len(chords)
    wob = 1 + 0.0018 * np.sin(2 * np.pi * 0.35 * t)                 # tape wow
    pad = np.zeros(n)
    for i, ch in enumerate(chords):
        s, e = int(i * seg * SR), min(n, int((i + 1) * seg * SR + 1.8 * SR))
        tt = t[s:e] - t[s]
        env = np.minimum(1, tt / 1.2) * np.exp(-np.maximum(0, tt - seg) * 2.2)
        for m in ch:
            for det in (-0.07, 0, 0.07):
                ph = np.cumsum(hz(m + det) * wob[s:e]) / SR
                pad[s:e] += (2 * (ph % 1) - 1) * env * 0.12
        ph = np.cumsum(hz(ch[0] - 12) * wob[s:e]) / SR
        pad[s:e] += np.sin(2 * np.pi * ph) * env * 0.5
    pad = lp(pad, 1300, 4)
    pluck = np.zeros(n)
    step = 60 / bpm / 2
    for k in range(int(dur / step)):
        ch = chords[min(len(chords) - 1, int(k * step / seg))]
        m = ch[[4, 2, 3, 1, 4, 3, 2, 0][k % 8]] + 12
        s = int(k * step * SR)
        tt = t[:min(n - s, int(1.2 * SR))]
        pluck[s:s + len(tt)] += np.sin(2 * np.pi * hz(m) * tt) * np.exp(-tt * 5) * (0.5 + 0.5 * (k % 2 == 0))
    crackle = np.zeros(n)
    idx = RNG.integers(0, n, int(dur * 9))
    crackle[idx] = RNG.normal(0, 1, len(idx))
    mix = norm(pad) * 0.7 + norm(verb(pluck, 2.5, 5000, 0.6)) * 0.28 + hp(crackle, 2000) * 0.05
    mix = verb(mix, 3.0, 4500, 0.4, 5)
    fade = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 2.5)
    mono = norm(mix * fade, 0.8)
    wide = hp(np.roll(mono, int(0.012 * SR)), 300) * 0.25            # a little width
    return np.column_stack([mono + wide, mono - wide])


def write(name, x):
    os.makedirs(os.path.join(BUILD, "audio"), exist_ok=True)
    p = os.path.join(BUILD, "audio", name)
    wavfile.write(p, SR, (np.clip(x / max(1.0, np.max(np.abs(x))), -1, 1) * 32767).astype(np.int16))
    return p


if __name__ == "__main__":
    print(write("hook_sfx.wav", hook_sfx()))
    print(write("outro_music.wav", outro_music()))
