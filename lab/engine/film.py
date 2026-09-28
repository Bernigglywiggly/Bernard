"""The command line every episode shares (the list is in engine/__init__.py). An episode's film.py is just:

    import engine.film
    engine.film.main(__file__, title="EP04  ·  THE MAN IN THE MACHINE", music=[...], clips=[...], tags="...")
"""
import importlib
import json
import os
import subprocess
import sys

import numpy as np

import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl, look, captions as CAP  # noqa: E402

W, H, FPS = tl.W, tl.H, tl.FPS


def _enc(out, crf=16, extra=()):
    return subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                             "-i", "-", *extra, "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p", out],
                            stdin=subprocess.PIPE)


def sheet(paths, out):
    cols, n = 4, len(paths)
    rows = (n + cols - 1) // cols
    ins = sum((["-i", p] for p in paths), [])
    pad = "".join(f"[{i}]scale=480:-1[s{i}];" for i in range(n))
    blanks = "".join(f"color=c=black:s=480x270:d=1[b{i}];" for i in range(rows * cols - n))
    grid = "".join(f"[s{i}]" for i in range(n)) + "".join(f"[b{i}]" for i in range(rows * cols - n))
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", pad + blanks + grid + f"xstack=inputs={rows * cols}:grid={cols}x{rows}",
                    "-frames:v", "1", out], check=True)
    return out


def preview(src, out, mb=14.0):
    """Two-pass 720p encode sized to fit the artifact's 15 MB file limit."""
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                             capture_output=True, text=True, check=True).stdout)
    kbps = int(mb * 8e3 / d) - 128
    log = out + ".log"
    base = ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "slow",
            "-b:v", f"{kbps}k", "-passlogfile", log]
    subprocess.run(base + ["-pass", "1", "-an", "-f", "mp4", "/dev/null"], check=True)
    subprocess.run(base + ["-pass", "2", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out], check=True)
    for f in os.listdir(os.path.dirname(out)):
        if f.startswith(os.path.basename(log)):
            os.remove(os.path.join(os.path.dirname(out), f))
    print(out, round(os.path.getsize(out) / 1e6, 1), "MB", flush=True)
    return out


def collect_events(scenes, dur, build):
    """Every sound cue the picture makes (forms, morphs, thuds, ticks...), frame by frame at 24 fps."""
    tl.EVENTS.clear()
    surf = skia.Surface(W, H)
    tl.LABELS["mode"] = "collect"
    try:
        for i in range(int(dur * FPS)):
            tl.LABELS["queue"].clear()
            c = surf.getCanvas(); c.clear(skia.ColorBLACK)
            scenes.frame(c, i / FPS)
    finally:
        tl.LABELS["mode"] = "draw"
        tl.LABELS["queue"].clear()
    json.dump(dict(events=tl.EVENTS, dur=dur), open(os.path.join(build, "events.json"), "w"))
    print(len(tl.EVENTS), "sound events")


def main(film_file, title, music, anchors=None, clips=(), tags="", bed="mainframe", extra_sfx=()):
    ep_dir = os.path.dirname(os.path.abspath(film_file))
    build = os.path.join(ep_dir, "build")
    os.makedirs(build, exist_ok=True)
    name = os.path.basename(ep_dir)
    argv = sys.argv[1:] or ["help"]
    cmd = argv[0]
    if cmd == "help":
        print(engine.__doc__)
        return
    if cmd == "voice" or not os.path.exists(os.path.join(build, "lines.json")):
        from engine import voice
        voice.build(ep_dir)
        if cmd == "voice":
            return
    tl.load(ep_dir, title)
    sys.path.insert(0, ep_dir)
    scenes = importlib.import_module("scenes")
    dur = scenes.end_time() if hasattr(scenes, "end_time") else tl.end_time()
    feed = os.path.join(build, f"{name}_clean_silent.mp4")
    mix_wav = os.path.join(build, "mix.wav")
    final = os.path.join(build, f"{name}.mp4")
    t_of = lambda m: (tl.L[-1]["end"] + 1.0 if m == "end" else tl.ls(m) - 0.4) if isinstance(m, str) else float(m)

    if cmd == "lines":                                            # quick line-art stills (no characters)
        for tt in map(float, argv[1:]):
            s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.ColorBLACK)
            scenes.frame(c, tt)
            p = os.path.join(build, f"lines_{tt:06.2f}.png")
            s.makeImageSnapshot().save(p, skia.kPNG)
            print(p)
        return
    if cmd == "still":                                            # the finished look, with captions, + a contact sheet
        paths = []
        for tt in sorted(map(float, argv[1:])):
            p = os.path.join(build, f"still_{tt:06.2f}.png")
            look.compose(scenes, tt, lambda c, t: CAP.draw(c, t, dur - 0.6)).save(p, skia.kPNG)
            paths.append(p)
            print(p, flush=True)
        print(sheet(paths, os.path.join(build, "sheet.jpg")))
        return
    if cmd == "chunk":                                            # one slice of the caption-free picture
        i0, i1, out = int(argv[1]), int(argv[2]), argv[3]
        ff = _enc(out)
        for i in range(i0, i1):
            ff.stdin.write(look.compose(scenes, i / FPS).tobytes())
            if (i - i0) % 240 == 0:
                print(f"chunk {i0}-{i1}: {i / FPS:6.1f}s", flush=True)
        ff.stdin.close(); ff.wait()
        return
    if cmd in ("render", "all"):
        jobs = int(argv[1]) if len(argv) > 1 else 4
        n = int(dur * FPS)
        cuts = [round(n * k / jobs) for k in range(jobs + 1)]
        parts = [os.path.join(build, f"part{k}.mp4") for k in range(jobs)]
        procs = [subprocess.Popen([sys.executable, os.path.abspath(film_file), "chunk", str(cuts[k]), str(cuts[k + 1]), parts[k]])
                 for k in range(jobs)]
        codes = [p.wait() for p in procs]
        assert all(c == 0 for c in codes), codes
        lst = os.path.join(build, "parts.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", feed], check=True)
        for p in parts:
            os.remove(p)
        print(feed, flush=True)
    if cmd in ("sound", "all"):
        from engine import score, mix
        collect_events(scenes, dur, build)
        marks = [(t_of(m), s) for m, s in music]
        anc = tuple(t_of(a) for a in anchors) if anchors else None
        bed_path = score.build(os.path.join(build, "bed.wav"), marks, dur, anc, bed)
        mix.build(build, bed_path, "mix.wav", extra=[(t_of(m), k, p) for m, k, p in extra_sfx])
    if cmd in ("master", "all"):                                  # captions over the clean picture + the mix, one pass
        dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", feed, "-f", "rawvideo", "-pix_fmt", "bgra", "-"], stdout=subprocess.PIPE)
        enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                                "-i", "-", "-i", mix_wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                                "-maxrate", "5000k", "-bufsize", "10000k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                                "-shortest", "-movflags", "+faststart", final], stdin=subprocess.PIPE)
        i = 0
        while True:
            buf = dec.stdout.read(W * H * 4)
            if len(buf) < W * H * 4:
                break
            t = i / FPS
            if any(ln["start"] - 0.05 <= t <= ln["end"] + 0.25 for ln in tl.L):
                arr = np.frombuffer(buf, np.uint8).reshape(H, W, 4).copy()
                s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
                CAP.draw(s.getCanvas(), t, dur - 0.6)
                s.flushAndSubmit()
                buf = arr.tobytes()
            enc.stdin.write(buf)
            i += 1
        dec.wait(); enc.stdin.close(); enc.wait()
        print(final, round(os.path.getsize(final) / 1e6, 1), "MB", flush=True)
    if cmd in ("preview", "all"):                                 # a 720p copy under 14 MB, for the posting kit page
        preview(final, os.path.join(build, f"{name}_720.mp4"))
    if cmd in ("shorts", "all"):
        from engine import shorts
        want = argv[1:] if cmd == "shorts" else ()
        print(shorts.make_all(list(clips), tl.L, feed, mix_wav, dur, os.path.join(build, "shorts"), tags, want))
