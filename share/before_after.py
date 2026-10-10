#!/usr/bin/env python3
"""A square before/after clip for sharing: the old look on the left, the new on the right, the new version's sound.
    ~/youtube/.venv/bin/python before_after.py <old 9:16 mp4> <new 9:16 mp4> <out mp4> [seconds]"""
import subprocess
import sys

import skia

old, new, out = sys.argv[1:4]
secs = sys.argv[4] if len(sys.argv) > 4 else "42"
font = skia.Font(skia.Typeface.MakeFromFile("/Users/daestigwood/Bernard/a01_v6/fonts/InterTight-600.ttf"), 46)
s = skia.Surface(1080, 120)
c = s.getCanvas()
c.clear(skia.Color(4, 5, 6))
for txt, x, colr in (("BEFORE", 270, skia.Color(123, 133, 140)), ("AFTER", 810, skia.Color(95, 240, 228))):
    c.drawString(txt, x - font.measureText(txt) / 2, 78, font, skia.Paint(AntiAlias=True, Color=colr))
s.makeImageSnapshot().save("/tmp/_ba_head.png", skia.kPNG)
fc = ("[0:v]scale=540:960,setsar=1,fps=30[a];[1:v]scale=540:960,setsar=1,fps=30[b];[a][b]hstack=inputs=2[h];"
      "[2:v][h]vstack=inputs=2[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", secs, "-i", old, "-t", secs, "-i", new, "-loop", "1", "-t", secs, "-i", "/tmp/_ba_head.png",
                "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "23", "-preset", "slow", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", out], check=True)
print(out)
