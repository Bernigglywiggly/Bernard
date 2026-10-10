#!/usr/bin/env python3
"""Where a render stands still. Samples frame-to-frame change at 10 fps and reports still stretches.

Usage: python3 motion_report.py film.mp4 [--min 2.0]

Thresholds are mean luma difference per sample (0-255) at 320 px wide:
  0.05  frozen: nothing moves at all
  0.15  near-still: only a slow push or a tiny element moves
Prints the share of the film in each state and every stretch longer than --min seconds, with timestamps, so a critic
can open those exact moments. For our documentaries: nothing frozen over 2 s except the end card, and something new
every 2-4 s.
"""
import argparse
import re
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("film")
ap.add_argument("--min", type=float, default=2.0, help="report stretches at least this long (seconds)")
a = ap.parse_args()

vf = ("fps=10,scale=320:-1,format=gray,tblend=all_mode=difference,signalstats,"
      "metadata=print:key=lavfi.signalstats.YAVG")
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.film, "-vf", vf, "-an", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
v = [float(x) for x in re.findall(r"YAVG=([0-9.]+)", log)]
total = len(v) / 10


def stretches(th):
    out, start = [], None
    for i, x in enumerate(v + [1e9]):
        if x < th and start is None:
            start = i
        elif x >= th and start is not None:
            out.append((start / 10, (i - start) / 10))
            start = None
    return out


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


print(f"{a.film}: {total:.1f}s sampled")
for name, th in (("frozen", 0.05), ("near-still", 0.15)):
    s = stretches(th)
    share = sum(d for _, d in s)
    long = [(t, d) for t, d in s if d >= a.min]
    print(f"{name:10s} {share:6.1f}s ({100 * share / max(total, 0.1):.0f}%)  stretches >= {a.min}s: {len(long)}")
    for t, d in sorted(long, key=lambda x: -x[1])[:15]:
        print(f"    {mmss(t)}  {d:.1f}s")
