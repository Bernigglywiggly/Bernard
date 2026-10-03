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


BPM = {"mainframe": 104.0, "low_orbit": 120.0, "night_drive": 108.0, "terminal": 96.0, "chrome_marl": 72.0,
       "deep_field": 112.0, "arena": 100.0, "house": 124.0, "garage": 130.0}


def build(out_path, marks, dur, anchors=None, bed="mainframe", bpm=None):
    """bed: a name in beds.py, optionally with options after a colon: "night_drive:calm" (Night Drive's version cut
    for under a voice), "deep_field:key=-3" (Deep Field in D minor)."""
    name, _, opt = bed.partition(":")
    bar, lead = grid(anchors, bpm or BPM.get(name, 104.0))
    p = plan(marks, dur, bar, lead)
    kw = {}
    for o in filter(None, opt.split(",")):
        k, eq, v = o.partition("=")
        kw[k] = (float(v) if "." in v else int(v)) if eq else True
    if lead > 0.05:                  # no dead air at the top: one more intro bar, cut in so its last part plays from 0
        p[0] = (p[0][0], p[0][1] + 1)
        x = np.asarray(getattr(beds, name)(240.0 / bar, p, 0.0, **kw), np.float32)[int(round((bar - lead) * fx.SR)):]
        x = x * np.minimum(1.0, np.arange(len(x)) / (0.4 * fx.SR))[:, None]
    else:
        x = getattr(beds, name)(240.0 / bar, p, lead, **kw)
    fx.save(out_path, np.asarray(x, np.float32), mp3=False)
    print(f"score: {bed} at {240.0 / bar:.2f} BPM, lead {lead:.2f}s, plan {p}")
    return out_path
