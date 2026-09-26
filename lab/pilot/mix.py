"""The pilot mix: voice on top, the jungle bed ducked under it (drums less, pads more), the vortex window
cleared for the fall, every picture cue from build/events.json placed from the sound palette.
Master at -14 LUFS with peaks under -1 dBFS. Muxes onto build/pilot_silent.mp4.

    python3 mix.py            # build/pilot_mix.wav, build/THE_CURVE_pilot.mp4
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import audio_fx as fx  # noqa: E402

SR = fx.SR
BUILD = os.path.join(HERE, "build")
SFX = os.path.join(HERE, "..", "out", "sfx")
STEMS = os.path.join(HERE, "..", "out", "music", "stems")


def fit(x, n):
    x = fx.stereo(x)
    return np.pad(x, ((0, max(0, n - len(x))), (0, 0)))[:n]


def smooth_env(x, att, rel):
    ga, gr = np.exp(-1 / (att * SR)), np.exp(-1 / (rel * SR))
    up = signal.lfilter([1 - ga], [1, -ga], x)
    down = signal.lfilter([1 - gr], [1, -gr], x)
    return np.maximum(up, down)


def main():
    ev = json.load(open(os.path.join(BUILD, "events.json")))
    lines = json.load(open(os.path.join(BUILD, "lines.json")))["lines"]
    total = ev["total"] + 0.5
    n = int(total * SR)
    voice = fit(fx.load(os.path.join(BUILD, "voice.wav")), n)
    dry = fit(fx.load(os.path.join(BUILD, "voice_dry.wav")), n).mean(1)

    # voice activity (0..1) from the dry voice, smoothed: the key for ducking
    e = np.abs(dry)
    e = smooth_env(e, 0.01, 0.25)
    act = np.clip(e / (np.percentile(e[e > 1e-4], 70) + 1e-9), 0, 1)
    act = smooth_env(act, 0.06, 0.45)

    # music: stems with their own duck depths
    stems = {}
    for k, depth in (("drums", 5.0), ("sub", 3.0), ("pads", 9.0), ("keys", 10.0), ("air", 4.0)):
        p = os.path.join(STEMS, f"pilot_bed_{k}.wav")
        if os.path.exists(p):
            stems[k] = fit(fx.load(p), n) * fx.db(-depth * act)[:, None]
    music = sum(stems.values())
    # automation: clear the air for the drop (the hang, the fall), bring it back after the landing
    t = np.arange(n) / SR
    hang, fall, land = lines[11]["end"] + 0.3, ev["fall"], ev["land"]
    auto_db = np.interp(t, [0, hang - 0.4, hang, fall, land + 0.1, land + 1.4, total], [0, 0, -18, -30, -30, 0, 0])
    music *= fx.db(auto_db)[:, None]
    # tuck the music into the voice's presence band while it speaks (a static dip, gated by activity)
    dip = fx.bq(music, "peak", 3200, q=0.8, gain_db=-4.0)
    music = music * (1 - act[:, None]) + dip * act[:, None]
    music_gain = fx.db(-24.5 - fx.lufs(music))
    music *= music_gain

    # sound effects from the cues
    sfx = np.zeros((n, 2), np.float32)
    cache = {}
    for at, name, gain_db, pan in ev["cues"]:
        if name not in cache:
            cache[name] = fx.load(os.path.join(SFX, name + ".wav"))
        x = cache[name] * fx.db(gain_db)
        if pan:
            x = x * np.array([np.sqrt((1 - pan) / 2) * 1.414, np.sqrt((1 + pan) / 2) * 1.414])[None, :]
        i = int(at * SR)
        j = min(n, i + len(x))
        if j > i:
            sfx[i:j] += x[: j - i]
    sfx *= fx.db(-6.0)            # palette files peak near -3..-8 dBFS; this seats them 10-20 dB under the voice

    mix = voice + music + sfx
    mix = fx.bq(mix, "hp", 24)
    g = fx.db(-14.0 - fx.lufs(mix))
    mix = mix * g
    # true-peak-ish ceiling: 4x oversampled peak check, then a gentle soft clip if needed
    up = signal.resample_poly(mix, 4, 1, axis=0)
    tp = 20 * np.log10(np.max(np.abs(up)) + 1e-9)
    if tp > -1.0:
        mix = fx.soft_limit(mix, fx.db(-1.2))
    out = os.path.join(BUILD, "pilot_mix.wav")
    fx.save(out, mix, mp3=False)
    print("mix", round(fx.lufs(mix), 2), "LUFS", "true peak before limit", round(tp, 2), "dB",
          "| voice", round(fx.lufs(voice * g), 1), "music", round(fx.lufs(music * g), 1), "sfx", round(fx.lufs(sfx * g), 1))
    vid = os.path.join(BUILD, "pilot_silent.mp4")
    if os.path.exists(vid):
        final = os.path.join(BUILD, "THE_CURVE_pilot.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", out, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", final], check=True)
        print(final)


if __name__ == "__main__":
    main()
