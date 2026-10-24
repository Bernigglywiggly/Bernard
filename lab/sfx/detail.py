"""Detail sounds for the full films (28 Sep): the satisfying layer under the picture, all synthesised (no samples,
nothing to license or get claimed).

  key       an ASMR "thocky" mechanical keyboard: a lubed linear switch bottoming out on a deep, damped case (a small
            pop, a woody body, a cushioned thud, a muted contact click) and a softer, higher upstroke. Every key is a
            little different; the space bar is deeper with a longer, stabilised body.
  coin      a coin set down on a hard surface: bright metal modes and a small table knock
  paper     a sheet laid on a stack: a soft air slap and a short crinkle
  pop       a bubble popping: a quick rising chirp and a soft click (for "the bubble burst")
  link      a chain link settling: small, dull metal
  grains    a soft pour of tiny taps (things streaming out), for texture, very quiet

The user: typing sounds like "the really satisfying ... ones people use for ASMR", not the phone keyboard, and
"don't force it if not needed". So keys only where text actually types on screen.

    python3 detail.py     # out/sfx/detail_reel.wav + one file per sound
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
import audio_fx as fx  # noqa: E402
from palette import T, burst, modal, sat, pan, add, place, peak, edges, OUT  # noqa: E402

SR = fx.SR
_K = {}


def _chirp(f0, f1, tau, dur):
    t = T(dur)
    f = f1 + (f0 - f1) * np.exp(-t / tau)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def key(v=0, kind="alpha"):
    """One keystroke (mono). kind: alpha, space or enter."""
    if (v, kind) in _K:
        return _K[(v, kind)]
    r = np.random.default_rng(5000 + 7 * v + {"alpha": 0, "space": 1, "enter": 2}[kind])
    p = {"alpha": 1.0, "space": 0.72, "enter": 0.86}[kind] * (1 + r.uniform(-0.045, 0.045))
    y = np.zeros(int(0.24 * SR), np.float32)
    dur_body = 0.16 if kind == "alpha" else 0.2
    body = modal([205 * p, 410 * p, 790 * p, 1360 * p, 2420 * p], [0.042, 0.028, 0.017, 0.010, 0.005],
                 [0.8, 0.72, 0.58, 0.38, 0.17], dur_body, r, jitter=0.03)
    if kind != "alpha":                                            # the stabilised bar: a longer, lower wire-damped body
        body = add(body, modal([118 * p, 236 * p], [0.07, 0.04], [0.6, 0.25], 0.2, r))
    pop = (_chirp(1500 * p, 430 * p, 0.0016, 0.012) * np.exp(-T(0.012) / 0.0035)).astype(np.float32)
    thud = (np.sin(2 * np.pi * 92 * p * T(0.05)) * np.exp(-T(0.05) / 0.018)).astype(np.float32)
    click = burst(0.003, 1800, 4500, 0.0008, r)
    place(y, body * 0.85, 0.0)
    place(y, pop * 0.5, 0.0)
    place(y, thud * 0.32, 0.0015)
    place(y, click * 0.3, 0.0)
    up = add(modal([900 * p, 1750 * p, 3100 * p], [0.012, 0.008, 0.004], [0.35, 0.25, 0.12], 0.05, r, jitter=0.05),
             burst(0.002, 2200, 5200, 0.0006, r) * 0.1)
    place(y, up * (0.36 if kind == "alpha" else 0.24), r.uniform(0.075, 0.105))
    y = fx.bq(fx.bq(y, "lp", 7000), "hp", 70)
    y = sat(y, 1.25)
    refl = np.zeros_like(y)                                        # the desk: one soft early reflection
    d = int(0.0085 * SR)
    refl[d:] = fx.bq(y[:-d], "lp", 2500) * 0.16
    _K[(v, kind)] = peak(y + refl, -3 if kind == "alpha" else -2)
    return _K[(v, kind)]


def keystrokes(text, times, seed=0, vel=1.0):
    """Stereo keystrokes for text typed at the given times (one per character, spaces on the bar)."""
    r = np.random.default_rng(seed)
    end = (times[-1] - times[0]) + 0.3 if len(times) else 0.3
    out = np.zeros((int(end * SR) + 1, 2), np.float32)
    for i, (ch, t) in enumerate(zip(text, times)):
        kind = "space" if ch == " " else "enter" if ch == "\n" else "alpha"
        k = key(int(r.integers(0, 24)), kind) * vel * (0.95 if kind != "alpha" else r.uniform(0.7, 1.0))
        x = pan(k, 0.0 if kind != "alpha" else r.uniform(-0.28, 0.28))
        i0 = int((t - times[0]) * SR)
        j = min(len(out), i0 + len(x))
        out[i0:j] += x[: j - i0]
    return out


def coin(v=0):
    r = np.random.default_rng(6000 + v)
    ring = modal([2960, 4410, 6880, 8350], [0.18, 0.12, 0.07, 0.05], [1.0, 0.6, 0.35, 0.18], 0.45, r, jitter=0.02)
    knock = modal([420, 900], [0.02, 0.012], [0.6, 0.3], 0.05, r)
    y = add(ring * 0.35, knock * 0.8, burst(0.002, 3000, 9000, 0.0006, r) * 0.2)
    bounce = modal([2960, 4410], [0.08, 0.05], [0.5, 0.3], 0.2, r) * 0.15      # a small second touch
    place(y, bounce, 0.045)
    return peak(fx.bq(y, "lp", 9000), -6)


def paper(v=0):
    r = np.random.default_rng(6100 + v)
    t = T(0.22)
    air = fx.bq(fx.bq(r.normal(0, 1, len(t)), "hp", 500), "lp", 4000) * np.exp(-t / 0.035)
    crink = np.zeros(len(t))
    for _ in range(9):
        i = int(r.uniform(0.01, 0.12) * SR)
        g = burst(0.004, 2500, 7000, 0.001, r)
        crink[i:i + len(g)] += g[: len(crink) - i] * r.uniform(0.1, 0.3)
    return peak((air * 0.8 + crink).astype(np.float32), -9)


def pop():
    r = np.random.default_rng(6200)
    t = T(0.08)
    c = np.sin(2 * np.pi * np.cumsum(420 + 1500 * (1 - np.exp(-t / 0.01))) / SR) * np.exp(-t / 0.018)
    y = add(c.astype(np.float32) * 0.8, burst(0.003, 1500, 6000, 0.001, r) * 0.4)
    return peak(y, -6)


def link(v=0):
    r = np.random.default_rng(6300 + v)
    y = add(modal([1830, 3120, 4650], [0.05, 0.03, 0.02], [0.7, 0.4, 0.2], 0.12, r, jitter=0.04) * 0.5,
            modal([380, 760], [0.018, 0.01], [0.5, 0.2], 0.04, r))
    return peak(fx.bq(y, "lp", 7000), -7)


def grains(dur=1.5, rate=60, v=0):
    r = np.random.default_rng(6400 + v)
    y = np.zeros(int(dur * SR), np.float32)
    tt = 0.0
    while tt < dur - 0.03:
        g = add(modal([r.uniform(900, 2400)], [0.004], [1.0], 0.012, r), burst(0.002, 1500, 6000, 0.0006, r) * 0.3)
        place(y, g * r.uniform(0.2, 0.6), tt)
        tt += r.exponential(1 / rate)
    e = np.minimum(1, T(dur) / 0.2) * np.minimum(1, (dur - T(dur)) / 0.4)
    return peak(fx.bq(y * e, "lp", 5000), -12)


SOUNDS = {"key": lambda: key(0), "key_space": lambda: key(0, "space"), "coin": coin, "paper": paper, "pop": pop,
          "link": link, "grains": grains}


def main():
    os.makedirs(OUT, exist_ok=True)
    reel = []
    for name, fn in SOUNDS.items():
        y = fn()
        y = edges(y if y.ndim == 2 else pan(y, 0))
        fx.save(os.path.join(OUT, name + ".wav"), y)
        reel += [y, np.zeros((int(0.5 * SR), 2), np.float32)]
    text = "SAM BRANNAN'S STORE · STOCKED FIRST"
    rng = np.random.default_rng(1)
    times = np.cumsum([0.0] + list(np.clip(rng.normal(0.058, 0.012, len(text) - 1), 0.035, 0.1)))
    reel.append(keystrokes(text, times))
    fx.save(os.path.join(OUT, "detail_reel.wav"), fx.true_peak_limit(np.concatenate(reel), -1.0))
    print("detail reel", round(sum(len(x) for x in reel) / SR, 1), "s")


if __name__ == "__main__":
    main()
