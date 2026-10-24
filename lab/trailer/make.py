"""The channel trailer (~40 s, 16:9): George's strongest lines from the films over their own pictures and captions, one
continuous Arena bed under them, the ears-going moment, then the wordmark and a closing line. For the YouTube channel
page (Customisation > Layout > Channel trailer) and as a pinned post anywhere else.

    cd lab && ELEVENLABS_API_KEY=... python3 trailer/make.py     # -> lab/trailer/build/the_curve_trailer.mp4
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import engine  # noqa: E402,F401  (paths)
import audio_fx as fx  # noqa: E402
import beds  # noqa: E402
import eleven_tts as el  # noqa: E402
import mograph as mg  # noqa: E402
import skia  # noqa: E402
from engine import tl, look, captions as CAP, mix  # noqa: E402
from engine.draw import CX, GLOW, WHITE, bignum, lines_in  # noqa: E402

W, H, FPS, SR = 1920, 1080, 24, fx.SR
BUILD = os.path.join(HERE, "build")
SEGS = [("ep05", ["why"]), ("ep06", ["job", "result", "more"]), ("ep08", ["unlock"]), ("ep04", ["pilot"]), ("ep07", ["nothing"])]
OUTRO = "This is The Curve. The hidden mechanism behind the AI headlines. A new film every two days."
PRE, POST, FADE = 0.35, 0.55, 0.22
GAP, A_IN, A_OUT = 0.08, 0.04, 0.15     # a clip never reaches into the line before or after; its audio fades in and out


def span(ids):
    """A montage clip's (t0, t1): the lines with a little air either side, but whole lines only. The user (1 Oct): the
    clips "cut halfway through the speech": a fixed 0.55 s of tail took in the start of George's next line."""
    i0, i1 = tl.I(ids[0]), tl.I(ids[-1])
    t0, t1 = tl.ls(ids[0]) - PRE, tl.le(ids[-1]) + POST
    if i0 > 0:
        t0 = max(t0, tl.L[i0 - 1]["end"] + GAP)
    if i1 + 1 < len(tl.L):
        t1 = min(t1, tl.L[i1 + 1]["start"] - GAP)
    return t0, t1


def faded(x):
    """The clip's audio with a short fade in and a gentler fade out, so no edge clicks or clips a word."""
    x = np.array(x, np.float32, copy=True)
    a, b = min(len(x), int(A_IN * SR)), min(len(x), int(A_OUT * SR))
    ramp_in = np.linspace(0.0, 1.0, a, dtype=np.float32)
    ramp_out = np.linspace(1.0, 0.0, b, dtype=np.float32)
    if x.ndim == 2:
        ramp_in, ramp_out = ramp_in[:, None], ramp_out[:, None]
    x[:a] *= ramp_in
    x[len(x) - b:] *= ramp_out
    return x


class Outro:
    TRAILS, GLINTS = (), ()

    @staticmethod
    def frame(c, t):
        from engine.brand import _curve
        lines_in(c, [_curve(40, 1880, 990, 150, 5.0)], t, 0.1, 1.2, GLOW, 3.0, seed_pt=(40, 990))
        bignum(c, t, "THE CURVE", 150, CX, 560, 0.5)
        tl.label(c, "THE HIDDEN MECHANISM BEHIND THE AI HEADLINES", CX, 650, t, 2.2, 24, WHITE)
        tl.label(c, "A NEW FILM EVERY TWO DAYS", CX, 700, t, 4.4, 20, GLOW)


def frames(video, t0, dur):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", video, "-t", f"{dur:.3f}", "-f", "rawvideo", "-pix_fmt", "bgra",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-"], stdout=subprocess.PIPE)
    while True:
        buf = p.stdout.read(W * H * 4)
        if len(buf) < W * H * 4:
            break
        yield np.frombuffer(buf, np.uint8).reshape(H, W, 4).copy()
    p.wait()


def main():
    os.makedirs(BUILD, exist_ok=True)
    out = os.path.join(BUILD, "the_curve_trailer.mp4")
    wav = os.path.join(BUILD, "trailer_mix.wav")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                            os.path.join(BUILD, "trailer_silent.mp4")], stdin=subprocess.PIPE)
    voice, talk, starts, t_cur = [], [], [], 0.0
    for ep, ids in SEGS:
        d = os.path.join(engine.LAB, ep)
        tl.load(d, "")
        t0, t1 = span(ids)
        dur = t1 - t0
        v = fx.load(os.path.join(d, "build", "voice.wav"))
        voice.append((t_cur, faded(v[int(t0 * SR): int(t1 * SR)])))
        starts.append(t_cur)
        talk += [(t_cur + tl.ls(i) - t0, t_cur + tl.le(i) - t0) for i in ids]
        n = 0
        for arr in frames(os.path.join(d, "build", f"{ep}_clean_silent.mp4"), t0, dur):
            t = t0 + n / FPS
            s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
            CAP.draw(s.getCanvas(), t, t1)
            s.flushAndSubmit()
            k = min(1.0, n / FPS / FADE, (dur - n / FPS) / FADE)
            if k < 1:
                arr[..., :3] = (arr[..., :3] * max(0.0, k)).astype(np.uint8)
            enc.stdin.write(arr.tobytes())
            n += 1
        t_cur += n / FPS
        print(ep, ids, f"{dur:.2f}s", flush=True)
    # the outro: the wordmark forms, George closes
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    (y, sr), _ = el.synth(OUTRO, key, voice=el.GEORGE, speed=1.0)
    y = fx.resample(y.astype(np.float32), sr)
    room = fx.cinema_ir(rt60=1.4, predelay=0.02, seed=5, dark=0.6)
    yv = fx.chain_voice(y, room=room, room_wet=-16.0, target=-16.0)
    o0 = t_cur
    voice.append((o0 + 1.2, yv))
    talk.append((o0 + 1.2, o0 + 1.2 + len(y) / SR))
    odur = max(7.5, 1.2 + len(y) / SR + 2.0)
    tl.EP["title"] = ""
    for i in range(int(odur * FPS)):
        tt = i / FPS
        img = look.compose(Outro, tt)
        arr = np.array(img.toarray())
        k = min(1.0, (odur - tt) / 0.8)
        if k < 1:
            arr[..., :3] = (arr[..., :3] * k).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(arr).tobytes())
    enc.stdin.close(); enc.wait()
    total = o0 + odur
    n = int(total * SR)
    vo = np.zeros((n, 2), np.float32)
    for at, x in voice:
        x = x if x.ndim == 2 else np.stack([x, x], 1)
        i = int(at * SR); j = min(n, i + len(x))
        vo[i:j] += x[: j - i]
    # one house bed under it all (the user, 1 Oct: house or garage, not Arena), the peak from the robot, the ears going
    bar = 240.0 / 124
    t_robot = starts[3]
    n_a = max(1, int(round(t_robot / bar)) - 1)
    n_b = max(1, int(np.ceil((o0 - t_robot) / bar)))
    plan = [("intro", 1), ("a", n_a), ("b", n_b), ("out", 4)]
    bed = np.asarray(beds.house(240.0 / bar, plan, 0.0, key=0), np.float32)
    bed = np.pad(bed, ((0, max(0, n - len(bed))), (0, 0)))[:n]
    bed = bed * fx.db(-19.0 - fx.lufs(bed))
    tk = np.zeros(n, np.float32)
    for a, b in talk:
        tk[int(max(0, a - 0.12) * SR): int((b + 0.05) * SR)] = 1.0
    tk = np.convolve(tk, np.ones(int(0.15 * SR)) / int(0.15 * SR), mode="same").astype(np.float32)
    lo = fx.bq(fx.bq(bed, "lp", 160.0), "lp", 160.0)
    hi = fx.bq(fx.bq(bed, "hp", 160.0), "hp", 160.0)
    bed = lo * fx.db(-9.0 * tk)[:, None] + hi * fx.db(-12.5 * tk)[:, None]
    bed = mix.deafen(bed, [o0 - 0.05])
    det = mix.ring(n, [o0 - 0.05])
    pre = vo + bed + det
    out_mix = fx.master(pre, target=-14.0, ceiling_db=-1.5)
    fx.save(wav, out_mix, mp3=False)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(BUILD, "trailer_silent.mp4"), "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, f"{total:.1f}s", json.dumps(dict(lufs=round(float(fx.lufs(out_mix)), 1))))


if __name__ == "__main__":
    main()
