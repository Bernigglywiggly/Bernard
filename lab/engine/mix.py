"""The mix (EP03's, 28 Sep): George on top, the music well under him, a detailed layer of the picture's own sounds.
The user: "background music not too loud", "the voice whatever volume level is needed", "lots of detail sound
effects"; no typing sounds; only George, never a stand-in.

  voice   build/voice.wav, de-essed, on top
  music   the score at -19 LUFS, ducked 12.5 dB while George talks, breathing back up in the gaps, with a hard dip
          before every "cut" line (the silence before a reveal)
  detail  the picture's events (forms, morphs, latches, coins, pops, links, ticks...), 4 dB under the voice
  master  -14 LUFS integrated, -1 dBTP
"""
import json
import os

import numpy as np

import engine  # noqa: F401  (paths)
import audio_fx as fx  # noqa: E402
import palette as PAL  # noqa: E402

SR = fx.SR
SFX = os.path.join(engine.LAB, "out", "sfx")
MAP = {"form": ("form", -13), "morph": ("whoosh", -15), "whoosh": ("whoosh", -15), "glint": ("scan", -18),
       "scan": ("scan", -18), "latch": ("latch", -12), "thock": ("thock", -9), "zoom": ("riser", -16),
       "confirm": ("confirm", -14), "coin": ("coin", -11), "paper": ("paper", -11), "pop": ("pop", -12),
       "link": ("link", -10), "grains": ("grains", -15), "tick": ("tick", -15), "thud": ("thock", -7),
       "glitch": ("glitch", -17), "swell": ("swell", -15), "sub_drop": ("sub_drop", -13), "thum": ("thum", -14),
       "servo": ("servo", -15), "hydraulic": ("hydraulic", -14), "power_up": ("power_up", -16), "clack": ("clack", -12),
       "dock": ("dock", -12)}
DUCK_MUSIC, DUCK_SFX = -12.5, -4.0


def load_sfx(name):
    y = fx.load(os.path.join(SFX, name + ".wav"))
    return y if y.ndim == 2 else np.stack([y, y], 1)


def place(dst, x, at, gain_db=0.0, pan=0.0):
    i = int(round(at * SR))
    if i >= len(dst) or i + len(x) <= 0:
        return
    if x.ndim == 1:
        x = PAL.pan(x, pan)
    elif pan:
        x = x * np.array([np.sqrt((1 - pan) / 2) * 1.414, np.sqrt((1 + pan) / 2) * 1.414])[None, :]
    if i < 0:
        x, i = x[-i:], 0
    j = min(len(dst), i + len(x))
    dst[i:j] += x[: j - i] * fx.db(gain_db)


def deess(v, xover=5200.0, thresh=0.32, max_db=-9.0):
    """Split-band de-esser: the band above ~5 kHz turned down only while it outweighs the rest (the "s" sounds)."""
    lp = lambda x: fx.bq(fx.bq(x, "lp", xover, q=0.7071), "lp", xover, q=0.7071)
    hp = lambda x: fx.bq(fx.bq(x, "hp", xover, q=0.7071), "hp", xover, q=0.7071)
    lo, hi = lp(v), hp(v)
    m = lambda x: np.sqrt(np.convolve((x.mean(1) if x.ndim == 2 else x) ** 2, np.ones(240) / 240, mode="same")) + 1e-7
    r = m(hi) / m(v)
    g_db = np.clip((r - thresh) / thresh, 0, 1) * max_db
    k = int(0.004 * SR)
    g_db = np.convolve(g_db, np.ones(k) / k, mode="same")
    return (lo + hi * fx.db(g_db)[:, None]).astype(np.float32)


def talking(lines, n):
    """0..1 per sample: George is talking (attack ahead of each line, a slow release after)."""
    k = 100
    a = np.zeros(int(n / SR * k) + 2)
    for ln in lines:
        a[max(0, int((ln["start"] - 0.12) * k)): int((ln["end"] + 0.05) * k) + 1] = 1.0
    env = np.zeros_like(a)
    for i in range(1, len(a)):
        c = 0.35 if a[i] > env[i - 1] else 0.02
        env[i] = env[i - 1] + c * (a[i] - env[i - 1])
    return np.interp(np.arange(n) / SR, np.arange(len(env)) / k, env).astype(np.float32)


def cut_dips(lines, n):
    g = np.zeros(n, np.float32)
    t = np.arange(n) / SR
    for ln in lines:
        if ln.get("cut"):
            s = ln["start"]
            g = np.minimum(g, np.interp(t, [s - 0.55, s - 0.3, s + 0.05, s + 0.9], [0, -14, -14, 0]).astype(np.float32))
    return g


def build(build_dir, bed_path, out_name="mix.wav", extra=()):
    meta = json.load(open(os.path.join(build_dir, "lines.json")))
    lines = meta["lines"]
    ev = json.load(open(os.path.join(build_dir, "events.json")))
    n = int(ev["dur"] * SR)
    fit = lambda y: np.pad(y, ((0, max(0, n - len(y))), (0, 0)))[:n]
    george = meta.get("engine") == "eleven"
    voice = fit(deess(fx.load(os.path.join(build_dir, "voice.wav")))) if george else np.zeros((n, 2), np.float32)
    music = fit(fx.load(bed_path))
    music = music * fx.db(-19.0 - fx.lufs(music))
    tk = talking(lines, n) if george else np.zeros(n, np.float32)
    music = music * fx.db(DUCK_MUSIC * tk + cut_dips(lines, n))[:, None]
    detail = np.zeros((n, 2), np.float32)
    cache, seen = {}, set()
    for i, (at, kind, pan) in enumerate(list(ev["events"]) + [list(e) for e in extra]):
        if kind not in MAP or (round(at, 2), kind) in seen:
            continue
        seen.add((round(at, 2), kind))
        name, gain = MAP[kind]
        if name == "tick":
            x = PAL.tick(i % 7)
        else:
            if name not in cache:
                cache[name] = load_sfx(name)
            x = cache[name]
        place(detail, x, at, gain, pan)
    detail = detail * fx.db(DUCK_SFX * tk)[:, None]
    pre = voice + music + detail
    mix = fx.master(pre, target=-14.0, ceiling_db=-1.5)            # -1.5 dBTP: room for the AAC encode
    g = fx.db(fx.lufs(mix) - fx.lufs(pre))
    speech = tk > 0.9
    st = lambda y: round(float(fx.lufs(y[speech])), 1) if speech.any() else None
    report = dict(voice="George" if george else "none", master=round(float(fx.lufs(mix)), 2), voice_talking=st(voice * g),
                  music_under_voice=st(music * g), music=round(float(fx.lufs(music * g)), 1),
                  detail=round(float(fx.lufs(detail * g)), 1), events=len(seen))
    out = os.path.join(build_dir, out_name)
    fx.save(out, mix, mp3=False)
    print("mix", report)
    return out
