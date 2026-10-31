"""The end card for a How They Profit film: 15 seconds (up to 20 to carry a film past 8:00) of the ledger look with the channel's name at the top and the
lower two thirds left clear for YouTube's end-screen elements (two videos and Subscribe), over the opening of the
film's own score, faded. Appended to the master -> <ep>/out/<ep>_1080p.mp4.

    python3 ch2/endcard.py ep01
"""
import os
import subprocess
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import engine  # noqa: E402,F401  (paths)
import audio_fx as fx  # noqa: E402
from ch2 import look as L  # noqa: E402
from ch2 import ledger  # noqa: E402

DUR, FPS = 15.0, 24
MIDROLL = 481.0     # a film that lands just under 8:00 gets a longer card (YouTube end screens run up to 20 s): mid-rolls


def card_len(film_mp4):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", film_mp4],
                             capture_output=True, text=True, check=True).stdout)
    return min(20.0, MIDROLL - d) if DUR < MIDROLL - d <= 20.0 else DUR


def card_png(path):
    arr = np.zeros((L.H, L.W, 4), np.uint8)
    s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
    c = s.getCanvas()
    L.ground(c, margin=False)
    L.text(c, ledger.BRAND, L.W / 2, 250, L.font(L.SERIF_B, 110), L.fill(L.PAPER), "center", track=0.06)
    c.drawLine(L.W / 2 - 360, 300, L.W / 2 + 360, 300, L.stroke(L.BRASS, 2, 0.9))
    c.drawLine(L.W / 2 - 360, 308, L.W / 2 + 360, 308, L.stroke(L.BRASS, 1, 0.6))
    L.text(c, "ONE COMPANY'S MONEY MACHINE, OPENED UP", L.W / 2, 368, L.font(L.MONO_M, 26), L.fill(L.BRASS), "center",
           track=0.18)
    L.text(c, "EVERY SOURCE IS IN THE DESCRIPTION", L.W / 2, L.H - 70, L.font(L.MONO, 20), L.fill(L.MUTED, 0.9), "center",
           track=0.2)
    s.flushAndSubmit()
    import cv2
    cv2.imwrite(path, arr[:, :, :3])


def main(ep):
    d = os.path.join(HERE, ep)
    b, out = os.path.join(d, "build"), os.path.join(d, "out")
    os.makedirs(out, exist_ok=True)
    png, wav, mp4 = os.path.join(b, "endcard.png"), os.path.join(b, "endcard.wav"), os.path.join(b, "endcard.mp4")
    card_png(png)
    dur = card_len(os.path.join(b, f"{ep}.mp4"))
    bed = fx.load(os.path.join(b, "bed.wav"))[: int(dur * fx.SR)]
    bed = bed * fx.db(-18.0 - fx.lufs(bed))
    n = len(bed)
    env = np.ones(n, np.float32)
    fi, fo = int(0.6 * fx.SR), int(4.0 * fx.SR)
    env[:fi] = np.linspace(0, 1, fi)
    env[n - fo:] = np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
    fx.save(wav, bed * env[:, None], mp3=False)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.2f}", "-i", png, "-i", wav,
                    "-vf", "fade=t=in:st=0:d=0.6", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", mp4], check=True)
    final = os.path.join(out, f"{ep}_1080p.mp4")
    # Audio is joined from the WAVs and encoded to AAC once: re-encoding the film's AAC track raised the true peak from
    # -1.1 to -0.2 dBTP (EP04). The film's mix is trimmed to its video length so the card starts on the cut.
    film_len = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                                     "-of", "csv=p=0", os.path.join(b, f"{ep}.mp4")],
                                    capture_output=True, text=True, check=True).stdout)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(b, f"{ep}.mp4"), "-i", mp4,
                    "-i", os.path.join(b, "mix.wav"), "-i", wav, "-filter_complex",
                    f"[2:a]aresample=48000,atrim=0:{film_len:.3f},asetpts=PTS-STARTPTS[fa];"
                    "[3:a]aresample=48000,asetpts=PTS-STARTPTS[ca];"
                    "[0:v][fa][1:v][ca]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", final], check=True)
    print(final, round(os.path.getsize(final) / 2**20, 1), "MiB")


if __name__ == "__main__":
    main(sys.argv[1])
