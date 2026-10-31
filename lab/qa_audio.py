"""Audio QA: loudness, peaks, and a spectrogram + waveform sheet for one or more files, so a sound
can be checked by eye (levels, tails, harshness, clipping) before anyone listens.

    python3 qa_audio.py out/voice/a.wav out/voice/b.wav --png out/qa_voice.png
"""
import argparse
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal


def sheet(paths, png, max_s=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(len(paths), 1, figsize=(16, 2.6 * len(paths)), squeeze=False)
    for ax, p in zip(axes[:, 0], paths):
        x, sr = sf.read(p, dtype="float32", always_2d=True)
        if max_s:
            x = x[: int(max_s * sr)]
        m = x.mean(1)
        lufs = pyln.Meter(sr).integrated_loudness(x) if len(x) > sr * 0.5 else float("nan")
        pk = 20 * np.log10(np.max(np.abs(x)) + 1e-9)
        f, t, S = signal.spectrogram(m, sr, nperseg=2048, noverlap=1536)
        ax.pcolormesh(t, f / 1000, 10 * np.log10(S + 1e-12), shading="auto", cmap="magma", vmin=-110, vmax=-20)
        ax.set_ylim(0, min(sr / 2000, 20))
        ax.set_ylabel("kHz")
        tt = np.arange(len(m)) / sr
        ax2 = ax.twinx()
        ax2.plot(tt[::50], m[::50], color="#3FE6D8", lw=0.3, alpha=0.6)
        ax2.set_ylim(-1, 1)
        ax2.set_yticks([])
        ax.set_title(f"{os.path.basename(p)}   {len(m)/sr:.1f}s   {lufs:.1f} LUFS   peak {pk:.1f} dBFS", fontsize=10, loc="left")
    plt.tight_layout()
    plt.savefig(png, dpi=70)
    print("wrote", png)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--png", default="qa.png")
    ap.add_argument("--max-s", type=float, default=None)
    a = ap.parse_args()
    sheet(a.paths, a.png, a.max_s)
