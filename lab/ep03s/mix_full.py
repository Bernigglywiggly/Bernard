"""The full EP03 mix (28 Sep): the voice on top, the music well under it, and a detailed layer of sound under the
picture. The user: "background music not too loud", "the voice whatever volume level is needed", "lots of detail
sound effects". Then, on v1: no typing sounds, and only the very first British voice (ElevenLabs George), never the
local stand-in: "get rid of this voice right now".

  voice   ElevenLabs George only (lines.json engine "eleven"): build/voice.wav, de-essed, on top. With any other
          engine there is no voice at all (captions carry the words) and the music isn't ducked
  music   Arena re-cut to the floors (ascii_open.score_full; Mainframe until 29 Sep), ducked whenever the voice
          talks (12.5 dB above 160 Hz, 9 below, so the groove holds) and breathing back up in the gaps; a hard dip
          into every "cut" line (the silence before a reveal)
  detail  the picture's own events (forms, morphs, latches, coins, paper, pops, links, ticks...), tucked 4 dB under
          the voice while it talks. No keystrokes (the user took them out)
  master  -14 LUFS integrated, -1 dBTP

    python3 mix_full.py     # after ascii_open.py collect/score: build/ep03_full_mix.wav, with a level report
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "sfx"))
import audio_fx as fx  # noqa: E402
import palette as PAL  # noqa: E402

SR = fx.SR
BUILD = os.path.join(HERE, "build")
SFX = os.path.join(HERE, "..", "out", "sfx")
# event kind -> (sound, gain dB); the files are peak-normalised, so these are the relative levels
MAP = {"form": ("form", -13), "morph": ("whoosh", -15), "whoosh": ("whoosh", -15), "glint": ("scan", -18),
       "scan": ("scan", -18), "latch": ("latch", -12), "thock": ("thock", -9), "zoom": ("riser", -16),
       "confirm": ("confirm", -14), "coin": ("coin", -11), "paper": ("paper", -11), "pop": ("pop", -12),
       "link": ("link", -10), "grains": ("grains", -15), "tick": ("tick", -15)}
DUCK_MUSIC, DUCK_LOW, DUCK_SFX = -12.5, -9.0, -4.0                     # the kick and bass (below SPLIT) duck less
SPLIT = 160.0


def load(name):
    if name == "tick":
        return None                                                    # synthesised per event, a little different each
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
    """A split-band de-esser: the band above ~5 kHz is turned down only while it outweighs the rest (the "s" sounds),
    by up to 9 dB, so a bright TTS voice stops hissing and a warm one is left alone. Linkwitz-Riley split (sums flat)."""
    lp = lambda x: fx.bq(fx.bq(x, "lp", xover, q=0.7071), "lp", xover, q=0.7071)
    hp = lambda x: fx.bq(fx.bq(x, "hp", xover, q=0.7071), "hp", xover, q=0.7071)
    lo, hi = lp(v), hp(v)
    m = lambda x: np.sqrt(np.convolve((x.mean(1) if x.ndim == 2 else x) ** 2, np.ones(240) / 240, mode="same")) + 1e-7
    r = m(hi) / m(v)
    g_db = np.clip((r - thresh) / thresh, 0, 1) * max_db
    k = int(0.004 * SR)                                                 # smooth the gain a little (4 ms)
    g_db = np.convolve(g_db, np.ones(k) / k, mode="same")
    return (lo + hi * fx.db(g_db)[:, None]).astype(np.float32)


def talking(lines, n):
    """0..1 per sample: the voice is talking (attack 120 ms ahead of each line, release 500 ms after)."""
    k = 100                                                            # a control rate of 100 Hz
    a = np.zeros(int(n / SR * k) + 2)
    for ln in lines:
        a[int((ln["start"] - 0.12) * k): int((ln["end"] + 0.05) * k) + 1] = 1.0
    env = np.zeros_like(a)
    for i in range(1, len(a)):                                         # fast up, slow down
        c = 0.35 if a[i] > env[i - 1] else 0.02
        env[i] = env[i - 1] + c * (a[i] - env[i - 1])
    return np.interp(np.arange(n) / SR, np.arange(len(env)) / k, env).astype(np.float32)


def cut_dips(lines, n):
    """A hard dip in the music just before each 'cut' line: the silence before a reveal."""
    g = np.zeros(n, np.float32)
    t = np.arange(n) / SR
    for ln in lines:
        if ln.get("cut"):
            s = ln["start"]
            g = np.minimum(g, np.interp(t, [s - 0.55, s - 0.3, s + 0.05, s + 0.9], [0, -14, -14, 0]).astype(np.float32))
    return g


def main(bed_path=os.path.join(BUILD, "full_bed.wav"), out_name="ep03_full_mix.wav"):
    meta = json.load(open(os.path.join(BUILD, "lines.json")))
    lines = meta["lines"]
    ev = json.load(open(os.path.join(BUILD, "events.json")))
    total = ev["dur"]
    n = int(total * SR)
    fit = lambda y: np.pad(y, ((0, max(0, n - len(y))), (0, 0)))[:n]

    george = meta.get("engine") == "eleven"                          # the local stand-in voice is never heard
    voice = fit(deess(fx.load(os.path.join(BUILD, "voice.wav")))) if george else np.zeros((n, 2), np.float32)
    music = fit(fx.load(bed_path))
    music = music * fx.db(-19.0 - fx.lufs(music))
    tk = talking(lines, n) if george else np.zeros(n, np.float32)
    lo = fx.bq(fx.bq(music, "lp", SPLIT), "lp", SPLIT)                # as engine/mix.py: the groove holds under him
    hi = fx.bq(fx.bq(music, "hp", SPLIT), "hp", SPLIT)
    dips = cut_dips(lines, n)
    music = lo * fx.db(DUCK_LOW * tk + dips)[:, None] + hi * fx.db(DUCK_MUSIC * tk + dips)[:, None]

    detail = np.zeros((n, 2), np.float32)
    cache = {}
    seen = set()
    for i, (at, kind, pan) in enumerate(ev["events"]):
        if kind not in MAP or (round(at, 2), kind) in seen:
            continue
        seen.add((round(at, 2), kind))
        name, gain = MAP[kind]
        if name == "tick":
            x = PAL.tick(i % 7)
        else:
            if name not in cache:
                cache[name] = load(name)
            x = cache[name]
        place(detail, x, at, gain, pan)
    detail = detail * fx.db(DUCK_SFX * tk)[:, None]

    pre = voice + music + detail
    mix = fx.master(pre, target=-14.0, ceiling_db=-1.5)                 # -1.5 dBTP: room for the AAC encode
    g = fx.db(fx.lufs(mix) - fx.lufs(pre))                             # the master's gain, to measure the stems as heard
    speech = tk > 0.9
    st = lambda y: fx.lufs(y[speech]) if speech.any() else float("nan")
    gaps = tk < 0.1
    report = dict(voice="George" if george else "none (captions only)", master=round(fx.lufs(mix), 2),
                  voice_talking=round(st(voice * g), 1) if george else None, music_under_voice=round(st(music * g), 1) if george else None,
                  music=round(fx.lufs(music * g), 1), detail=round(fx.lufs(detail * g), 1), events=len(seen))
    out = os.path.join(BUILD, out_name)
    fx.save(out, mix, mp3=False)
    for nm, y in (("stem_voice.wav", voice * g), ("stem_music.wav", music * g), ("stem_detail.wav", detail * g)):
        fx.save(os.path.join(BUILD, nm), y.astype(np.float32), mp3=False)
    print("mix", report)
    return out


if __name__ == "__main__":
    main()
