"""Shorten a narration's pauses: every silence longer than --max is cut down to --keep seconds (split evenly
around the middle), then an optional gentle tempo change. Usage:
  python3 scripts/tighten_vo.py in.mp3 out.mp3 [--max 0.35] [--keep 0.26] [--tempo 1.03] [--noise -40dB]"""
import argparse, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--max", type=float, default=0.35); ap.add_argument("--keep", type=float, default=0.26)
ap.add_argument("--tempo", type=float, default=1.0); ap.add_argument("--noise", default="-40dB")
a = ap.parse_args()
log = subprocess.run(["ffmpeg", "-i", a.inp, "-af", f"silencedetect=noise={a.noise}:d=0.18", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", a.inp],
                           capture_output=True, text=True).stdout)
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
keep, t = [], 0.0
for s, e in zip(starts, ends):
    if e - s > a.max:
        mid = (s + e) / 2
        keep.append((t, mid - a.keep / 2))
        t = mid + a.keep / 2
keep.append((t, dur))
parts = "".join(f"[0:a]atrim={x:.4f}:{y:.4f},asetpts=PTS-STARTPTS[a{i}];" for i, (x, y) in enumerate(keep))
cat = "".join(f"[a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[c]"
tempo = f";[c]atempo={a.tempo}[o]" if a.tempo != 1.0 else ";[c]anull[o]"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.inp, "-filter_complex", parts + cat + tempo, "-map", "[o]",
                "-c:a", "libmp3lame", "-b:a", "192k", a.out], check=True)
new = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", a.out],
                           capture_output=True, text=True).stdout)
print(f"{dur:.2f}s -> {new:.2f}s ({len(keep) - 1} pauses shortened)")
