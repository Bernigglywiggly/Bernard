"""The score: a bed from lab/music/beds.py (Mainframe by default: dark synth-orchestral, the channel's bed for serious
topics) re-cut to the film. One bar grid near 104 BPM, stretched a little so bar lines land on two anchor moments,
and the sections switching on bar lines where the film asks (marks):

  intro   strings and a filtered ostinato          a       the low pulse under the ostinato
  b       brass and violins on top (money, stakes)  break   strings, cello and sub only (a question, a what-if)
  out     the tail
"""
import math
import os

import numpy as np

import engine  # noqa: F401  (paths)
import audio_fx as fx  # noqa: E402
import beds  # noqa: E402


def grid(anchors=None, bpm=104.0):
    """(bar length, lead): the grid starts at lead and, with two anchors, has a whole number of bars between them."""
    bar = 240.0 / bpm
    if anchors and len(anchors) == 2:
        ta, tb = anchors
        n = max(1, round((tb - ta) / bar))
        bar = (tb - ta) / n
    lead = (anchors[0] % bar) if anchors else 0.0
    return bar, lead


def plan(marks, dur, bar, lead):
    """marks: [(time, section)] -> [(section, bars)]: each bar takes the section of the last mark before its first
    quarter."""
    marks = sorted(marks)
    total = int(math.ceil((dur - lead) / bar)) + 1
    names = []
    for b in range(total):
        tb = lead + (b + 0.25) * bar
        nm = marks[0][1]
        for tm, s in marks:
            if tm <= tb:
                nm = s
        names.append(nm)
    out = []
    for nm in names:
        if out and out[-1][0] == nm:
            out[-1][1] += 1
        else:
            out.append([nm, 1])
    return [tuple(p) for p in out]


BPM = {"mainframe": 104.0, "low_orbit": 120.0, "night_drive": 108.0, "terminal": 96.0}


def build(out_path, marks, dur, anchors=None, bed="mainframe", bpm=None):
    bar, lead = grid(anchors, bpm or BPM.get(bed, 104.0))
    p = plan(marks, dur, bar, lead)
    x = getattr(beds, bed)(240.0 / bar, p, lead)
    fx.save(out_path, np.asarray(x, np.float32), mp3=False)
    print(f"score: {bed} at {240.0 / bar:.2f} BPM, lead {lead:.2f}s, plan {p}")
    return out_path
