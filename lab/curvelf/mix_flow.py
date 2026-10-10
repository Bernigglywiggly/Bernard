#!/usr/bin/env python3
"""Sound for a one-camera Curve film (flow.py): George through the vocal chain and plate, the 2-step garage bed from
ch2/ep06/mix_pre.py ducked under him (sections alternate by chapter, a breakdown on each chapter's crossing), -14 LUFS.

    ~/youtube/.venv/bin/python mix_flow.py <film> <picture.mp4> <out.mp4>
"""
import json
import os
import subprocess
import sys

import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ch2", "ep06"))
import mix_pre as mp  # noqa: E402

B = os.path.join(HERE, sys.argv[1], "flow")
picture, out = sys.argv[2], sys.argv[3]
L = json.load(open(os.path.join(B, "lines.json")))["lines"]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", picture], capture_output=True, text=True).stdout)
bar = 4 * mp.BEAT
marks, floor, n = [(0.0, "intro")], -1, 0
for ln in L:
    if ln["floor"] != floor:                                  # a new chapter: breakdown on the crossing, then a section
        floor = ln["floor"]
        marks.append((ln["start"] + (2.0 if floor == 0 else 0.0), "ab"[floor % 2]))
        n = 0
    n += 1
    if n % 4 == 0:                                            # and a change inside long chapters, so it never loops flat
        marks.append((ln["start"], "ba"[(floor + n // 4) % 2]))
marks.append((dur - 6.0, "out"))
marks = sorted((round(t / bar) * bar, s) for t, s in marks)
MUSIC = [p for p in os.environ.get("FLOW_MUSIC", "").split(",") if p]     # a serious score instead of the garage bed: pieces, played in turn


def steady(y, SR):
    """A generated piece made fit to sit under a voice for minutes: its silent holes cut out (8 Oct, critic: the music
    vanished for two seconds and slammed back), and its long quiet passages and sudden hits drawn toward one level."""
    import numpy as np
    h = SR // 4
    r = np.array([np.sqrt((y[i:i + h] ** 2).mean()) for i in range(0, len(y) - h, h)])
    med = np.median(r)
    quiet = r < 0.18 * med                                          # 15 dB under the piece: a hole
    keep, i, fade = [], 0, int(0.08 * SR)
    while i < len(r):
        j = i
        while j < len(r) and quiet[j] == quiet[i]:
            j += 1
        if not (quiet[i] and (j - i) * h >= 0.5 * SR):             # holes of 0.75 s or more go; shorter rests are music
            keep.append((i * h, j * h if j < len(r) else len(y)))
        i = j
    merged = []
    for a_, b_ in keep:
        if merged and merged[-1][1] == a_:
            merged[-1] = (merged[-1][0], b_)
        else:
            merged.append((a_, b_))
    parts = []
    for a_, b_ in merged:
        seg = y[a_:b_].copy()
        if len(seg) > 2 * fade:
            seg[:fade] *= np.linspace(0, 1, fade)[:, None]
            seg[-fade:] *= np.linspace(1, 0, fade)[:, None]
        parts.append(seg)
    y = np.concatenate(parts)
    hop = SR // 2                                                   # the level: half-second steps, smoothed over about 2.5 s (a 2 s slide is caught, a beat is not)
    e = np.array([np.sqrt((y[i:i + 2 * hop] ** 2).mean()) for i in range(0, len(y), hop)]) + 1e-6
    k = np.hanning(7)
    e = np.convolve(np.pad(e, 3, mode="edge"), k / k.sum(), mode="valid")
    g = np.clip((np.median(e) / e) ** 0.9, 10 ** (-8 / 20), 10 ** (14 / 20))
    gain = np.interp(np.arange(len(y)), np.arange(len(e)) * hop + hop, g)
    return y * gain[:, None]


def score(paths, dur, cuts=(), xf=6.0):
    """Join generated pieces into one bed: each trimmed to where it is actually playing (they tend to stop early or
    leave a silent tail), crossfaded, repeated in turn until the film is covered."""
    import numpy as np
    SR = mp.SR
    pieces = []
    for p in paths:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "2", "-ar", str(SR), "/tmp/_piece.wav"], check=True)
        y, _ = sf.read("/tmp/_piece.wav")
        r = np.array([np.sqrt((y[i:i + SR] ** 2).mean()) for i in range(0, len(y) - SR, SR)])
        live = 20 * np.log10(r + 1e-9) > -36
        a = int(np.argmax(live))
        b = len(live)
        for i in range(max(a + 20, int(len(live) * 0.35)), len(live) - 3):           # a silence of 3 s or more is the end
            if not live[i:i + 3].any():
                b = i
                break
        while b > a + 10 and not live[b - 1]:
            b -= 1
        lead = np.where(r[a:b] > 0.6 * np.median(r[a:b]))[0]          # start where the piece is properly under way: a quiet opening, joined to, sounds like a drop-out
        a = a + (int(lead[0]) if len(lead) else 0)
        y = y[a * SR:b * SR]
        y = steady(y, SR)
        y = y * (10 ** (-21 / 20) / (np.sqrt((y ** 2).mean()) + 1e-9))      # every piece at the same level, so a quiet first half does not sink under the voice
        pieces.append(np.clip(y, -0.98, 0.98))
        print(os.path.basename(os.path.dirname(p)), "plays", a, "to", b, "s of", len(y) // SR)
    n, x = int((dur + 2) * SR), int(xf * SR)
    out = np.zeros((n, 2))
    pos, k = 0, 0
    while pos < n:
        y = pieces[k % len(pieces)].copy()
        k += 1
        end = (pos + len(y)) / SR                                   # change pieces on a chapter crossing, under its card, where one falls in the piece's last stretch
        ok = [c_ for c_ in cuts if pos / SR + 75 < c_ < end]
        if ok and end < dur:
            y = y[:int((ok[-1] + xf / 2) * SR) - pos]
        if pos:
            y[:x] *= np.sin(np.linspace(0, np.pi / 2, x))[:, None]
        y[-x:] *= np.cos(np.linspace(0, np.pi / 2, x))[:, None]
        e = min(n, pos + len(y))
        out[pos:e] += y[:e - pos]
        pos += len(y) - x
    out = fill(out, SR)
    out[:int(1.5 * SR)] *= np.linspace(0, 1, int(1.5 * SR))[:, None]
    return out


def fill(y, SR):
    """Lift the short holes steady() is too slow to see (9 Oct, LF03: the bed fell 10-13 dB for about a second before a
    hit, at 7:24 and 8:02). Each eighth of a second is held to within 4 dB of the music around it; at most +12 dB."""
    import numpy as np
    h = SR // 8
    e = np.array([np.sqrt((y[i:i + h] ** 2).mean()) for i in range(0, len(y), h)]) + 1e-6
    w = 32                                                          # the reference: the median of the 4 s around
    ref = np.array([np.median(e[max(0, i - w // 2):i + w // 2]) for i in range(len(e))])
    g = np.clip(ref * 10 ** (-4 / 20) / e, 1.0, 10 ** (12 / 20))
    k = np.hanning(5)
    g = np.convolve(np.pad(g, 2, mode="edge"), k / k.sum(), mode="valid")
    gain = np.interp(np.arange(len(y)), np.arange(len(g)) * h + h / 2, g)
    return y * gain[:, None]


def drone(dur, marks):
    """A beatless bed for serious films (9 Oct, Hormuz critic: a garage groove under missile strikes undercuts the
    narrator). D minor: a sub that breathes every 8 s, a slowly detuned fifth, faint band-passed static, and a sonar
    ping on each chapter crossing. Made in code, so we own it."""
    import numpy as np
    SR = mp.SR
    n = int((dur + 2) * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(7)
    sub = np.sin(2 * np.pi * 36.71 * t) * (0.55 + 0.45 * np.sin(2 * np.pi * t / 8.0 - np.pi / 2) ** 2)
    pad = sum(a * np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * t / p_))
              for f, a, p_ in ((73.42, 0.5, 23.0), (110.0, 0.32, 31.0), (146.83, 0.3, 17.0), (174.61, 0.2, 41.0),
                               (220.0, 0.16, 37.0), (293.66, 0.12, 19.0), (349.23, 0.07, 53.0)))   # upper partials: audible on a phone (9 Oct critic: the sub alone vanished)
    pad *= 0.75 + 0.25 * np.sin(2 * np.pi * t / 29.0)
    noise = rng.standard_normal(n)
    k = np.exp(-np.arange(64) / 9.0)
    static = np.convolve(noise, k / k.sum(), mode="same")
    static = (static - np.convolve(static, np.ones(400) / 400, mode="same")) * (0.4 + 0.6 * (np.sin(2 * np.pi * t / 13.0) > 0.6))
    mono = 0.30 * sub + 0.62 * pad + 0.12 * static
    ping = np.zeros(n)
    for tm, _ in marks:
        i0 = int(tm * SR)
        for e, g in ((0.0, 1.0), (0.42, 0.35), (0.84, 0.12)):          # the ping and two returns
            j = i0 + int(e * SR)
            m_ = min(n - j, int(2.5 * SR))
            if m_ > 0:
                tt = np.arange(m_) / SR
                ping[j:j + m_] += g * np.sin(2 * np.pi * 1180 * tt) * np.exp(-tt * 3.2)
    L = mono + 0.18 * ping
    R = np.roll(mono, int(0.011 * SR)) + 0.18 * np.roll(ping, int(0.023 * SR))
    out = np.stack([L, R], 1)
    out *= 10 ** (-21 / 20) / (np.sqrt((out ** 2).mean()) + 1e-9)
    out[:int(2 * SR)] *= np.linspace(0, 1, int(2 * SR))[:, None]
    return np.clip(out, -0.98, 0.98)


BED = os.environ.get("FLOW_BED", "")
if BED == "drone":
    chap = [(ln["start"] - 1.6, "ch") for k_, ln in enumerate(L) if k_ and ln["floor"] != L[k_ - 1]["floor"]]     # a ping on each chapter crossing only
    sf.write(os.path.join(B, "garage.wav"), drone(dur, chap), mp.SR)
elif MUSIC:
    floor_, cuts_ = -1, []
    for ln in L:
        if ln["floor"] != floor_:
            floor_ = ln["floor"]
            cuts_.append(ln["start"] - 1.6)
    sf.write(os.path.join(B, "garage.wav"), score(MUSIC, dur, cuts_[1:]), mp.SR)
else:
    sf.write(os.path.join(B, "garage.wav"), mp.bed(dur, marks), mp.SR)
sf.write(os.path.join(B, "plate.wav"), mp.plate(), mp.SR)
chain = ("highpass=f=85,equalizer=f=260:t=q:w=1.1:g=-2.5,equalizer=f=3400:t=q:w=1.2:g=2.5,highshelf=f=10500:g=4,deesser=i=0.35:m=0.5:f=0.5,"
         "acompressor=threshold=-22dB:ratio=3.2:attack=6:release=110:makeup=5,alimiter=limit=0.89")
fc = (f"[0:a]apad=whole_dur={dur:.2f},aformat=channel_layouts=stereo,{chain},asplit=3[v][vw][vk];[vw][2:a]afir=dry=0:wet=1[rev];"
      "[v][rev]amix=inputs=2:weights='1 0.09':normalize=0[vox];"
      + ("[1:a]volume=0.42[bed];" if BED == "drone" else "[1:a]highpass=f=38,lowshelf=f=110:g=-5,dynaudnorm=f=500:g=31:m=14:p=0.5,volume=0.5[bed];" if MUSIC else "[1:a]volume=0.66,haas=level_in=1:side_gain=0.55:middle_source=mid[bed];")
      + "[bed][vk]sidechaincompress=threshold=0.06:ratio=2:attack=30:release=700[duck];"
      f"[vox][duck]amix=inputs=2:normalize=0,alimiter=limit=0.84,loudnorm=I=-14:TP=-2:LRA=9,aresample=48000,alimiter=limit={os.environ.get('FLOW_LIMIT', '0.71')}:level=false,afade=t=out:st={dur - 3.0:.2f}:d=3.0[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(B, "voice_dry.wav"), "-i", os.path.join(B, "garage.wav"), "-i", os.path.join(B, "plate.wav"),
                "-i", picture, "-filter_complex", fc, "-map", "3:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", out], check=True)
print(out)
