"""EP03's caption-free picture in two waves of four slices (each wave well under the cloud session's 30-minute job
limit), then the captioned film from it in one drawing pass instead of a second full render.

    EP03_FULL=1 NO_CAPTIONS=1 python3 render_waves.py wave 0      # slices 0-3
    EP03_FULL=1 NO_CAPTIONS=1 python3 render_waves.py wave 1      # slices 4-7
    EP03_FULL=1 NO_CAPTIONS=1 python3 render_waves.py concat      # -> build/ep03_full_clean_silent.mp4
    EP03_FULL=1 python3 render_waves.py captions                  # -> build/ep03_full_silent.mp4 (then ascii_open.py sound_full)
"""
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ascii_open as AO  # noqa: E402

JOBS = 8
BUILD = AO.BUILD


def cuts():
    n = int(AO.DUR * AO.FPS)
    w = np.where(np.arange(n) / AO.FPS < AO.X7B + 0.3, 4.0, 1.0)          # the cold open costs about 4x (Blender, chrome)
    cw = np.cumsum(w)
    return [0] + [int(np.searchsorted(cw, cw[-1] * k / JOBS)) for k in range(1, JOBS)] + [n]


def part(k):
    return os.path.join(BUILD, f"full_clean_part{k}.mp4")


def main():
    cmd = sys.argv[1]
    c = cuts()
    if cmd == "wave":
        w = int(sys.argv[2])
        ks = range(4 * w, 4 * w + 4)
        procs = [subprocess.Popen([sys.executable, os.path.join(HERE, "ascii_open.py"), "chunk", str(c[k]), str(c[k + 1]), part(k)]) for k in ks]
        codes = [p.wait() for p in procs]
        assert all(x == 0 for x in codes), codes
        print("wave", w, "done", [c[k] for k in ks])
    elif cmd == "concat":
        lst = os.path.join(BUILD, "full_clean_parts.txt")
        open(lst, "w").write("".join(f"file '{part(k)}'\n" for k in range(JOBS)))
        out = os.path.join(BUILD, "ep03_full_clean_silent.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
        print(out)
    elif cmd == "captions":                                              # the captions over the clean picture
        import skia
        W, H, FPS = AO.W, AO.H, AO.FPS
        src = os.path.join(BUILD, "ep03_full_clean_silent.mp4")
        out = os.path.join(BUILD, "ep03_full_silent.mp4")
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "bgra", "-"], stdout=subprocess.PIPE)
        enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                                "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        i = 0
        while True:
            buf = dec.stdout.read(W * H * 4)
            if len(buf) < W * H * 4:
                break
            arr = np.frombuffer(buf, np.uint8).reshape(H, W, 4).copy()
            s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
            AO.ST.captions(s.getCanvas(), i / FPS)
            s.flushAndSubmit()
            enc.stdin.write(arr.tobytes())
            i += 1
        dec.wait(); enc.stdin.close(); enc.wait()
        print(out, i, "frames")


if __name__ == "__main__":
    main()
