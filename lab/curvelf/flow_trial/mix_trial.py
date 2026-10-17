#!/usr/bin/env python3
"""The Visa film's sound (ch2/ep06/mix_pre.py: George through the vocal chain and plate, the 2-step garage bed ducked
under him, -14 LUFS) on this trial's picture.   ~/youtube/.venv/bin/python mix_trial.py build/picture.mp4 out.mp4"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ch2", "ep06"))
import mix_pre as mp  # noqa: E402

B = os.path.join(HERE, "build")
picture, out = sys.argv[1], sys.argv[2]
L = json.load(open(os.path.join(B, "lines.json")))["lines"]
m = {ln["id"]: ln for ln in L}
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", picture], capture_output=True, text=True).stdout)
bar = 4 * mp.BEAT
plan = [("date", "intro"), ("site", "a"), ("thirteen", "b"), ("expert", "a"), ("wanted", "b"), ("person", "intro"), ("agents", "b"), ("box", "a")]
marks = [(0.0, "intro")] + [(round(m[i]["start"] / bar) * bar, s) for i, s in plan] + [(dur - 5.0, "out")]
sf.write(os.path.join(B, "garage.wav"), mp.bed(dur, marks), mp.SR)
sf.write(os.path.join(B, "plate.wav"), mp.plate(), mp.SR)
chain = ("highpass=f=85,equalizer=f=260:t=q:w=1.1:g=-2.5,equalizer=f=3400:t=q:w=1.2:g=2.5,highshelf=f=10500:g=4,deesser=i=0.35:m=0.5:f=0.5,"
         "acompressor=threshold=-22dB:ratio=3.2:attack=6:release=110:makeup=5,alimiter=limit=0.89")
fc = (f"[0:a]aformat=channel_layouts=stereo,{chain},asplit=3[v][vw][vk];[vw][2:a]afir=dry=0:wet=1[rev];"
      "[v][rev]amix=inputs=2:weights='1 0.09':normalize=0[vox];"
      "[1:a]volume=0.72[bed];[bed][vk]sidechaincompress=threshold=0.05:ratio=3:attack=20:release=260[duck];"
      f"[vox][duck]amix=inputs=2:normalize=0,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,afade=t=out:st={dur - 3.0:.2f}:d=3.0[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(B, "voice_dry.wav"), "-i", os.path.join(B, "garage.wav"), "-i", os.path.join(B, "plate.wav"),
                "-i", picture, "-filter_complex", fc, "-map", "3:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", out], check=True)
print(out)
