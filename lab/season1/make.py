"""THE CURVE · SEASON ONE: the five finished films as one long film (~13.5 min) for YouTube.

Why: Shorts earn almost nothing and their views don't count towards the Partner Programme's watch hours; a long film
earns watch hours and, past 8 minutes, mid-roll ads. This stitches the films the channel already has, in upload order:

    cold open (George's strongest lines over their pictures, Arena under them, the ears going) -> THE CURVE · SEASON ONE
    -> a chapter card before each film -> the wordmark and George's closing line, with time for YouTube's end screen.

    cd lab && python3 season1/make.py stills     # one frame of every card, to check the type fits
    cd lab && python3 season1/make.py cards      # -> season1/build/seg_*.mp4 (cold open, title, chapter cards, outro)
    cd lab && python3 season1/make.py join       # -> season1/build/the_curve_season1.mp4, chapters.txt, description.txt
    cd lab && python3 season1/make.py thumbs     # thumbnail options -> season1/build/thumb_*.jpg
Each film needs build/<ep>.mp4 and build/<ep>_clean_silent.mp4 first (film.py voice, parts, join, sound, master).
"""
import importlib.util
import json
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
sys.path.insert(0, LAB)
import engine  # noqa: E402,F401  (paths)
import audio_fx as fx  # noqa: E402
import beds  # noqa: E402
import eleven_tts as el  # noqa: E402
import skia  # noqa: E402
from engine import tl, look, captions as CAP, mix, kit  # noqa: E402
from engine.draw import CX, GLOW, WHITE, bignum, lines_in  # noqa: E402

W, H, FPS, SR = 1920, 1080, 24, fx.SR
BUILD = os.path.join(HERE, "build")
OUT = os.path.join(BUILD, "the_curve_season1.mp4")
# (episode, chapter title, the line under it), in the channel's upload order
CHAPTERS = [
    ("ep05", "FOLLOW THE SUN", "WHY AI IS LEAVING THE PLANET"),
    ("ep08", "CHEAPER MAKES MORE", "WHY CHEAPER AI MEANS MORE OF IT"),
    ("ep04", "THE MAN IN THE MACHINE", "WHO'S REALLY INSIDE THE ROBOTS"),
    ("ep06", "WHO'S HUMAN HERE?", "THE TURING TEST AND PROVING YOU'RE YOU"),
    ("ep07", "THE THIRTY-YEAR DELAY", "WHY AI HASN'T CHANGED PRODUCTIVITY (YET)"),
]
LABELS = {  # how each chapter reads in YouTube's chapter list and the description
    "ep05": "Follow the Sun: why AI is leaving the planet",
    "ep08": "Cheaper Makes More: why cheaper AI means more data centres",
    "ep04": "The Man in the Machine: who's really inside the robots",
    "ep06": "Who's Human Here? The Turing test and proving you're you",
    "ep07": "The Thirty-Year Delay: why AI hasn't changed productivity (yet)",
}
CARD_S, TITLE_S, OUTRO_S = 4.2, 6.5, 15.0
# the films' own master settings, so every segment joins without re-encoding
ENC_V = ["-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "5000k", "-bufsize", "10000k", "-pix_fmt", "yuv420p"]
ENC_A = ["-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2"]


def trailer():
    """The channel trailer's builder (its montage, frame reader and outro scene are reused here)."""
    spec = importlib.util.spec_from_file_location("trailer_make", os.path.join(LAB, "trailer", "make.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Title:
    TRAILS, GLINTS = (), ()

    @staticmethod
    def frame(c, t):
        from engine.brand import _curve
        lines_in(c, [_curve(40, 1880, 990, 150, 5.0)], t, 0.1, 1.2, GLOW, 3.0, seed_pt=(40, 990))
        bignum(c, t, "THE CURVE", 150, CX, 540, 0.4)
        tl.label(c, "SEASON ONE", CX, 645, t, 1.8, 28, GLOW)
        tl.label(c, "FIVE HIDDEN MECHANISMS BEHIND THE AI HEADLINES", CX, 698, t, 2.6, 22, WHITE)


def card_size(title):
    return min(110, int(1650 / (0.86 * len(title))))         # the wide type stays inside the frame


def chapter(n, title, sub):
    size = card_size(title)

    class Card:
        TRAILS, GLINTS = (), ()

        @staticmethod
        def frame(c, t):
            tl.label(c, f"CHAPTER {n}", CX, 430, t, 0.05, 24, GLOW)
            bignum(c, t, title, size, CX, 560, 0.25)
            tl.label(c, sub, CX, 560 + size * 0.5 + 60, t, 0.9, 22, WHITE)
    return Card


def scene_of(name):
    if name == "title":
        return Title
    if name == "outro":
        return trailer().Outro
    n = int(name[2:])
    _, title, sub = CHAPTERS[n - 1]
    return chapter(n, title, sub)


def render_scene(job):
    """Frames of a card scene -> a silent mp4 (one process per scene; the look keeps no state between scenes)."""
    name, dur, out, fade_in, fade_out = job
    tl.EP["title"] = ""
    scene = scene_of(name)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-"] + ENC_V + [out], stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for i in range(n):
        tt = i / FPS
        arr = np.array(look.compose(scene, tt).toarray())
        k = min(1.0, tt / fade_in if fade_in else 1.0, (dur - tt) / fade_out if fade_out else 1.0)
        if k < 1:
            arr[..., :3] = (arr[..., :3] * max(0.0, k)).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(arr).tobytes())
    enc.stdin.close()
    enc.wait()
    return out


def sfx(name, peak_db):
    """A palette sound at a peak level (some are shorter than a loudness meter's 400 ms block)."""
    x = mix.load_sfx(name)
    x = x if x.ndim == 2 else np.stack([x, x], 1)
    return x / max(1e-6, float(np.abs(x).max())) * fx.db(peak_db)


def place(buf, x, at):
    i = int(at * SR)
    j = min(len(buf), i + len(x))
    if j > i:
        buf[i:j] += x[: j - i]


def mux(silent, wav, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy"]
                   + ENC_A + ["-shortest", "-movflags", "+faststart", out], check=True)


def card_audio(dur, out):
    """A chapter card: a low hit as it opens, the formation's glint as the title forms; quiet beside the films."""
    a = np.zeros((int(dur * SR), 2), np.float32)
    place(a, sfx("thum", -9.0), 0.02)
    place(a, sfx("form", -18.0), 0.30)
    place(a, sfx("scan", -22.0), 1.15)
    fx.save(out, fx.master(a, target=-21.0, ceiling_db=-3.0), mp3=False)


def cold_open(tr):
    """The trailer's montage (George's strongest lines over their pictures and captions, one Arena bed, the ears going),
    ending on the season title instead of the wordmark."""
    silent = os.path.join(BUILD, "open_silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-"] + ENC_V + [silent], stdin=subprocess.PIPE)
    voice, talk, starts, t_cur = [], [], [], 0.0
    for ep, ids in tr.SEGS:
        d = os.path.join(LAB, ep)
        tl.load(d, "")
        t0, t1 = tl.ls(ids[0]) - tr.PRE, tl.le(ids[-1]) + tr.POST
        dur = t1 - t0
        v = fx.load(os.path.join(d, "build", "voice.wav"))
        voice.append((t_cur, v[int(t0 * SR): int(t1 * SR)]))
        starts.append(t_cur)
        talk += [(t_cur + tl.ls(i) - t0, t_cur + tl.le(i) - t0) for i in ids]
        n = 0
        for arr in tr.frames(os.path.join(d, "build", f"{ep}_clean_silent.mp4"), t0, dur):
            t = t0 + n / FPS
            s = skia.Surface(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
            CAP.draw(s.getCanvas(), t, t1)
            s.flushAndSubmit()
            k = min(1.0, n / FPS / tr.FADE, (dur - n / FPS) / tr.FADE)
            if k < 1:
                arr[..., :3] = (arr[..., :3] * max(0.0, k)).astype(np.uint8)
            enc.stdin.write(arr.tobytes())
            n += 1
        t_cur += n / FPS
        print("open", ep, ids, f"{dur:.2f}s", flush=True)
    o0 = t_cur
    tl.EP["title"] = ""
    for i in range(int(TITLE_S * FPS)):
        tt = i / FPS
        arr = np.array(look.compose(Title, tt).toarray())
        k = min(1.0, (TITLE_S - tt) / 0.6)
        if k < 1:
            arr[..., :3] = (arr[..., :3] * k).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(arr).tobytes())
    enc.stdin.close()
    enc.wait()
    total = o0 + TITLE_S
    n = int(total * SR)
    vo = np.zeros((n, 2), np.float32)
    for at, x in voice:
        x = x if x.ndim == 2 else np.stack([x, x], 1)
        i = int(at * SR)
        j = min(n, i + len(x))
        vo[i:j] += x[: j - i]
    bar = 2.4                                               # Arena at 100 BPM; the arrival on the robot, as in the trailer
    t_robot = starts[3]
    plan = [("intro", 1), ("a", max(1, int(round(t_robot / bar)) - 1)), ("b", max(1, int(np.ceil((o0 - t_robot) / bar)))), ("out", 4)]
    bed = np.asarray(beds.arena(240.0 / bar, plan, 0.0, key=0), np.float32)
    bed = np.pad(bed, ((0, max(0, n - len(bed))), (0, 0)))[:n]
    bed = bed * fx.db(-19.0 - fx.lufs(bed))
    tk = np.zeros(n, np.float32)
    for a, b in talk:
        tk[int(max(0, a - 0.12) * SR): int((b + 0.05) * SR)] = 1.0
    tk = np.convolve(tk, np.ones(int(0.15 * SR)) / int(0.15 * SR), mode="same").astype(np.float32)
    lo = fx.bq(fx.bq(bed, "lp", 160.0), "lp", 160.0)
    hi = fx.bq(fx.bq(bed, "hp", 160.0), "hp", 160.0)
    bed = lo * fx.db(-9.0 * tk)[:, None] + hi * fx.db(-12.5 * tk)[:, None]
    bed = mix.deafen(bed, [o0 - 0.05])                      # the ears go as the season title forms
    tail = np.clip((total - np.arange(n) / SR) / 1.2, 0, 1).astype(np.float32)[:, None]
    pre = (vo + bed + mix.ring(n, [o0 - 0.05])) * tail
    wav = os.path.join(BUILD, "open.wav")
    fx.save(wav, fx.master(pre, target=-14.0, ceiling_db=-1.5), mp3=False)
    out = os.path.join(BUILD, "seg_00_open.mp4")
    mux(silent, wav, out)
    print(out, f"{total:.1f}s", flush=True)
    return out


def outro_audio(tr, out):
    """The wordmark forms, George closes (the trailer's cached line), Arena's ending under him, then quiet for the end screen."""
    (y, sr), _ = el.synth(tr.OUTRO, os.environ.get("ELEVENLABS_API_KEY", ""), voice=el.GEORGE, speed=1.0)
    y = fx.resample(y.astype(np.float32), sr)
    room = fx.cinema_ir(rt60=1.4, predelay=0.02, seed=5, dark=0.6)
    yv = fx.chain_voice(y, room=room, room_wet=-16.0, target=-16.0)
    n = int(OUTRO_S * SR)
    vo = np.zeros((n, 2), np.float32)
    place(vo, yv if yv.ndim == 2 else np.stack([yv, yv], 1), 1.2)
    bed = np.asarray(beds.arena(100.0, [("out", 6)], 0.0, key=0), np.float32)
    bed = np.pad(bed, ((0, max(0, n - len(bed))), (0, 0)))[:n]
    bed = bed * fx.db(-24.0 - fx.lufs(bed))
    fade = np.clip((OUTRO_S - np.arange(n) / SR) / 3.0, 0, 1).astype(np.float32)[:, None]
    fx.save(out, fx.master(vo + bed * fade, target=-16.0, ceiling_db=-1.5), mp3=False)


def cards():
    os.makedirs(BUILD, exist_ok=True)
    tr = trailer()
    jobs = [(f"ch{i}", CARD_S, os.path.join(BUILD, f"card_{i}_silent.mp4"), 0.25, 0.35) for i in range(1, len(CHAPTERS) + 1)]
    jobs.append(("outro", OUTRO_S, os.path.join(BUILD, "outro_silent.mp4"), 0.3, 1.5))
    with Pool(4) as pool:
        res = pool.map_async(render_scene, jobs)
        cold_open(tr)                                       # the montage runs alongside the card renders
        res.get()
    for i in range(1, len(CHAPTERS) + 1):
        wav = os.path.join(BUILD, f"card_{i}.wav")
        card_audio(CARD_S, wav)
        mux(os.path.join(BUILD, f"card_{i}_silent.mp4"), wav, os.path.join(BUILD, f"seg_{i:02d}a_card.mp4"))
    wav = os.path.join(BUILD, "outro.wav")
    outro_audio(tr, wav)
    mux(os.path.join(BUILD, "outro_silent.mp4"), wav, os.path.join(BUILD, "seg_99_outro.mp4"))
    print("cards done", flush=True)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def stamp(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def join():
    segs, marks, t = [os.path.join(BUILD, "seg_00_open.mp4")], [(0.0, "Cold open: the five films in five lines")], 0.0
    t += probe(segs[0])
    for i, (ep, title, sub) in enumerate(CHAPTERS, 1):
        card = os.path.join(BUILD, f"seg_{i:02d}a_card.mp4")
        film = os.path.join(LAB, ep, "build", f"{ep}.mp4")
        marks.append((t, f"{i}. {LABELS[ep]}"))
        segs += [card, film]
        t += probe(card) + probe(film)
    segs.append(os.path.join(BUILD, "seg_99_outro.mp4"))
    marks.append((t, "What's next on The Curve"))
    lst = os.path.join(BUILD, "segments.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    "-movflags", "+faststart", OUT], check=True)
    chapters = "\n".join(f"{stamp(a)} {b}" for a, b in marks)
    open(os.path.join(BUILD, "chapters.txt"), "w").write(chapters + "\n")
    open(os.path.join(BUILD, "description.txt"), "w").write(description(chapters))
    json.dump(dict(duration=probe(OUT), mb=round(os.path.getsize(OUT) / 1e6, 1), chapters=marks),
              open(os.path.join(BUILD, "season1.json"), "w"), indent=1)
    print(OUT, round(probe(OUT), 1), "s", round(os.path.getsize(OUT) / 1e6, 1), "MB")
    print(chapters)


def description(chapters):
    films = {e["slug"]: e for e in kit.EPISODES}
    parts = ["Five hidden mechanisms behind the AI headlines, in one film: why the AI industry is trying to leave the "
             "planet, why cheaper AI means more data centres, not fewer, who's really inside the robots, why people picked "
             "an AI as the human, and why AI hasn't made most companies more productive (yet). Every figure is sourced "
             "below, film by film, and every price comes in Big Macs.\n",
             "Chapters\n" + chapters + "\n",
             "The five films, one by one, are on the channel. A new film every two days, shorts daily.\n",
             "Sources, film by film"]
    for i, (ep, title, _) in enumerate(CHAPTERS, 1):
        parts.append(f"\n{i}. {LABELS[ep].split(':')[0].split('?')[0]}{'?' if '?' in LABELS[ep] else ''} ({films[ep]['yt'][0]})")
        parts += ["• " + s for s in kit.sources(films[ep])]
    parts.append("\nThe narrator is an AI voice (ElevenLabs). Labelled what-ifs are imagined, not forecasts.")
    parts.append("\n#ai #artificialintelligence #aiexplained #documentary #technology #economics #robots #datacenter #thecurve")
    return "\n".join(parts) + "\n"


THUMBS = [  # (episode feed, seconds, lines, accent line, focus, zoom, place): checked against the contact sheets
    ("ep05", 61.5, "WHAT THE AI|HEADLINES|DON'T TELL YOU", 2, (0.39, 0.52), 1.05, 0.76),  # the globe, right
    ("ep08", 100.0, "5 HIDDEN|FORCES|BEHIND AI", 1, (0.5, 0.45), 1.35, 0.74),  # the bulb, right
    ("ep04", 22.5, "THERE'S|A HUMAN|INSIDE", 1, (0.55, 0.47), 1.1, 0.732),  # robot and VR operator, joined by the arc
]


def thumbs():
    from engine import thumb
    os.makedirs(BUILD, exist_ok=True)
    for k, (ep, t, lines, acc, focus, zoom, place) in enumerate(THUMBS):
        out = os.path.join(BUILD, f"thumb_{chr(97 + k)}.jpg")
        thumb.make(os.path.join(LAB, ep, "build", f"{ep}_clean_silent.mp4"), t, lines.split("|"), out, acc, focus, zoom, place)
        print(out)


def stills():
    os.makedirs(BUILD, exist_ok=True)
    tl.EP["title"] = ""
    for name, tt in [("title", 4.5), ("outro", 6.0)] + [(f"ch{i}", 3.7) for i in range(1, len(CHAPTERS) + 1)]:
        p = os.path.join(BUILD, f"still_{name}.png")
        look.compose(scene_of(name), tt).save(p, skia.kPNG)
        print(p, flush=True)


if __name__ == "__main__":
    {"cards": cards, "join": join, "thumbs": thumbs, "stills": stills}[sys.argv[1] if len(sys.argv) > 1 else "stills"]()
