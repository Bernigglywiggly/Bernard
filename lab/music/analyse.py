"""Objective checks on a rendered bed (for when nobody can listen): tonal balance by octave against a typical
mix slope, short-term loudness over time (does the arrangement move?), true peak, stereo correlation, clicks, and
a log-frequency spectrogram picture.

    python3 analyse.py ../out/music/new/terminal.wav [...]    # prints a report, writes <name>_spec.png
"""
import os
import sys

import numpy as np
from scipy import signal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import audio_fx as fx  # noqa: E402

BANDS = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]


def octave_levels(x, sr):
    mono = x.mean(1)
    f, p = signal.welch(mono, sr, nperseg=16384)
    out = []
    for c in BANDS:
        m = (f >= c / np.sqrt(2)) & (f < c * np.sqrt(2))
        out.append(10 * np.log10(np.sum(p[m]) + 1e-20))
    return np.array(out)


def short_term(x, sr, win=3.0, hop=1.0):
    vals = []
    for i in range(0, max(1, len(x) - int(win * sr)), int(hop * sr)):
        seg = x[i:i + int(win * sr)]
        vals.append(fx.lufs(seg) if np.any(seg) else -70)
    return np.array(vals)


def clicks(x, sr):
    """Broadband spikes: 5 ms blocks whose peak above 12 kHz is far above the level around them (200 ms).
    Drum hits rise with their surroundings; a discontinuity stands alone."""
    h = np.abs(fx.bq(fx.bq(x.mean(1), "hp", 12000), "hp", 12000))
    blk = int(0.005 * sr)
    nb = len(h) // blk
    pk = h[: nb * blk].reshape(nb, blk).max(1)
    rms = np.sqrt((h[: nb * blk].reshape(nb, blk) ** 2).mean(1))
    ctx = np.sqrt(signal.convolve(rms ** 2, np.ones(40) / 40, mode="same")) + 1e-6
    return int(np.sum((pk > 12 * ctx) & (pk > 1e-3)))


def report(path):
    x = fx.load(path)
    sr = fx.SR
    lv = octave_levels(x, sr)
    rel = lv - lv[BANDS.index(1000)]
    # a typical modern mix falls roughly 4.5 dB per octave above ~100 Hz; show the difference from that line
    ref = np.array([+6, +7, +4.5, 3.0, 1.5, 0.0, -3.5, -8.0, -13.5, -22.0])
    st = short_term(x, sr)
    up = signal.resample_poly(x, 4, 1, axis=0)
    tp = 20 * np.log10(np.max(np.abs(up)) + 1e-12)
    corr = np.corrcoef(x[:, 0], x[:, 1])[0, 1]
    side = 20 * np.log10(np.std(x[:, 0] - x[:, 1]) / (np.std(x[:, 0] + x[:, 1]) + 1e-12) + 1e-12)
    name = os.path.basename(path).rsplit(".", 1)[0]
    print(f"\n== {name}  {len(x) / sr:.1f}s  {fx.lufs(x):.1f} LUFS  TP {tp:.2f} dBTP  corr {corr:.2f}  side/mid {side:.1f} dB  clicks {clicks(x, sr)}")
    print("   octave  " + " ".join(f"{b:>6.0f}" for b in BANDS))
    print("   vs 1k   " + " ".join(f"{v:>6.1f}" for v in rel))
    print("   vs ref  " + " ".join(f"{v:>6.1f}" for v in rel - ref))
    print("   loudness/3s: " + " ".join(f"{v:.0f}" for v in st[::3]))
    # spectrogram picture
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        f, t, S = signal.spectrogram(x.mean(1), sr, nperseg=4096, noverlap=3072)
        fig, ax = plt.subplots(figsize=(14, 4), dpi=80)
        ax.pcolormesh(t, f, 10 * np.log10(S + 1e-12), shading="auto", vmin=-120, vmax=-30, cmap="magma")
        ax.set_yscale("symlog", linthresh=100); ax.set_ylim(20, 20000); ax.set_title(name)
        fig.tight_layout(); fig.savefig(path.rsplit(".", 1)[0] + "_spec.png"); plt.close(fig)
    except Exception as e:  # noqa: BLE001
        print("   (no picture:", e, ")")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
