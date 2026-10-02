"""Shorts cut from a finished long-form film (2 Oct: "long form for money, shorts is bonus and discovery"): a stretch
of the film's 16:9 picture framed in 9:16 over a blurred, darkened copy of itself, a headline above, and the reel
engine's kinetic captions below (the spoken word lit in gold). The sound is the film's own mix for that stretch,
faded in and out. Each short ends on a card that sends viewers to the full film.

    python3 vertical.py lustig capone        -> lustig/out/short_capone_9x16.mp4   (SHORTS in the film's folder)
"""
import importlib.util
import json
import os
import subprocess
import sys

import cv2
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "shorts"))
import reel  # noqa: E402

VW, VH, FPS = 1080, 1920, 30
SW, SH = 1920, 1080


def spec(film_dir):
    s = importlib.util.spec_from_file_location("shorts_spec", os.path.join(film_dir, "shorts.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def wrap(text, font, width):
    lines, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if cur and font.measureText(t) > width:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    return lines + ([cur] if cur else [])


def make(film_dir, key):
    sp = spec(film_dir).SHORTS[key]
    t0, t1 = sp["t0"], sp["t1"]
    src = os.path.join(film_dir, "out", sp.get("src", os.path.basename(film_dir) + "_1080p.mp4"))
    out = os.path.join(film_dir, "out", f"short_{key}_9x16.mp4")
    words = [w for w in json.load(open(os.path.join(film_dir, "build", "words.json"))) if t0 <= w[1] < t1]
    ws = [(w[0], w[1] - t0, w[2] - t0) for w in words]
    caps = reel.chunks([(w, a, b) for w, a, b in ws])
    end_card = sp.get("end", 2.5)
    dur = (t1 - t0) + end_card
    build = os.path.join(film_dir, "build", f"short_{key}")
    os.makedirs(build, exist_ok=True)
    wav = os.path.join(build, "audio.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", src, "-vn",
                    "-af", f"afade=t=in:d=0.3,afade=t=out:st={t1 - t0 - 0.6:.3f}:d=0.6,apad=pad_dur={end_card}",
                    "-ar", "48000", "-ac", "2", wav], check=True)
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", src, "-f", "rawvideo",
                           "-pix_fmt", "bgra", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{VW}x{VH}", "-r", str(FPS),
                            "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                            "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                            "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    fh = int(VW * SH / SW)                                   # the film's picture: 1080 x 608, a little above centre
    fy = 640
    head = skia.Font(reel.FONT["serif"], 84)
    small = skia.Font(reel.FONT["cap"], 40)
    lines = wrap(sp["headline"].upper(), head, VW - 120)
    last = np.zeros((SH, SW, 4), np.uint8)
    for f in range(int(dur * FPS)):
        t = f / FPS
        if t < t1 - t0:
            buf = rd.stdout.read(SW * SH * 4)
            if len(buf) == SW * SH * 4:
                last = np.frombuffer(buf, np.uint8).reshape(SH, SW, 4)
        frame = last
        bg = cv2.resize(frame, (VW // 6, VH // 6), interpolation=cv2.INTER_AREA)
        bg = cv2.GaussianBlur(bg, (0, 0), 6)
        bg = cv2.resize(bg, (VW, VH), interpolation=cv2.INTER_LINEAR)
        arr = (bg.astype(np.uint16) * 90 >> 8).astype(np.uint8)
        arr[:, :, 3] = 255
        fg = cv2.resize(frame, (VW, fh), interpolation=cv2.INTER_AREA)
        arr[fy:fy + fh] = fg
        s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
        c = s.getCanvas()
        for i, ln in enumerate(lines):                      # the headline, top
            y = 250 + i * 96
            w = head.measureText(ln)
            c.drawString(ln, VW / 2 - w / 2 + 3, y + 5, head, reel.P(0xCC000000, 1.0,
                         MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)))
            c.drawString(ln, VW / 2 - w / 2, y, head, reel.P(reel.GOLD if i == len(lines) - 1 else reel.WHITE))
        for cap in caps:                                     # kinetic captions under the picture
            reel.draw_caption(c, cap, t, y=fy + fh + 190)
        if t >= t1 - t0:                                    # the end card: the full film
            a = reel.ease((t - (t1 - t0)) / 0.4)
            c.drawRect(skia.Rect.MakeWH(VW, VH), reel.P(0xFF000000, 0.75 * a))
            for i, ln in enumerate(wrap(sp.get("cta", "FULL STORY ON THE CHANNEL"), small, VW - 160)):
                w = small.measureText(ln)
                c.drawString(ln, VW / 2 - w / 2, 900 + i * 56, small, reel.P(reel.GOLD, a))
            for i, ln in enumerate(wrap(sp["film"].upper(), head, VW - 140)):
                w = head.measureText(ln)
                c.drawString(ln, VW / 2 - w / 2, 1060 + i * 96, head, reel.P(reel.WHITE, a))
        s.flushAndSubmit()
        enc.stdin.write(arr.tobytes())
    rd.stdout.close()
    rd.wait()
    enc.stdin.close()
    enc.wait()
    print(out, round(os.path.getsize(out) / 1e6, 1), "MB", round(dur, 1), "s")
    return out


if __name__ == "__main__":
    d = os.path.join(HERE, sys.argv[1])
    for k in sys.argv[2:] or spec(d).SHORTS:
        make(d, k)
