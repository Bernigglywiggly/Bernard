"""YouTube thumbnails (1280x720 JPEG): a frame from the film's caption-free feed, a dark fade on the left, and a short
bold title in two or three lines (one line in turquoise). Big, few words, true to the film.

    python3 -m engine.thumb <video> <seconds> "LINE ONE|LINE TWO|LINE THREE" <out.jpg> [accent line index] [shift]
"""
import subprocess
import sys

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

W, H = 1280, 720
TURQ, WHITE = "#35D6C6", "#FFFFFF"


def grab(video, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-"], capture_output=True, check=True).stdout
    return skia.Image.fromarray(np.frombuffer(raw, np.uint8).reshape(H, W, 4).copy(), colorType=skia.ColorType.kBGRA_8888_ColorType)


def make(video, t, lines, out, accent=1, focus=(0.5, 0.5), zoom=1.35, place=0.7):
    """focus: the subject's point in the frame (fractions); it lands at x = place * W, zoomed and brightened."""
    img = grab(video, t)
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.Color(6, 7, 9))
    k = 1.35
    bright = skia.Paint(ColorFilter=skia.ColorFilters.Matrix([k, 0, 0, 0, 0, 0, k, 0, 0, 0, 0, 0, k, 0, 0, 0, 0, 0, 1, 0]))
    x0, y0 = place * W - focus[0] * W * zoom, H / 2 - focus[1] * H * zoom
    c.drawImageRect(img, skia.Rect.MakeXYWH(x0, y0, W * zoom, H * zoom), skia.SamplingOptions(skia.FilterMode.kLinear), bright)
    fade = skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (W * 0.68, 0)], [skia.Color(4, 5, 7, 245), skia.Color(4, 5, 7, 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), fade)
    size = 118 if max(len(x) for x in lines) <= 11 else 96
    f = mg.font("InterTight-600", size)
    lead = size * 1.02
    y = H / 2 - (len(lines) - 1) * lead / 2 + size * 0.36
    for i, ln in enumerate(lines):
        o = mg.stroke("#000000", size * 0.12, 0.85)
        o.setStrokeJoin(skia.Paint.kRound_Join)
        c.drawString(ln, 64, y + i * lead, f, o)
        c.drawString(ln, 64, y + i * lead, f, mg.fill(TURQ if i == accent else WHITE, 1.0))
    c.drawString("THE CURVE", 66, 58, mg.font("IBMPlexMono-500", 24), mg.fill(TURQ, 1.0))
    s.makeImageSnapshot().save(out, skia.kJPEG, 92)
    print(out)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    fx_, fy_, z = (float(v) for v in (a[5] if len(a) > 5 else "0.5,0.5,1.35").split(","))
    make(a[0], float(a[1]), a[2].split("|"), a[3], int(a[4]) if len(a) > 4 else 1, (fx_, fy_), z)
