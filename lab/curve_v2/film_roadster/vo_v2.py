"""Film v2 narration: splice the critic-round-1 pickups (vo/pickups_v2/) into the v1 segment takes (vo/<seg>_t.mp3).

Every cut sits in the middle of a measured silence, so each junction keeps about the 0.26 s pause tighten_vo.py leaves.
Writes vo/v2/<seg>_t.mp3 for every segment in the v2 film (unchanged ones are copied) and lab/motion/public/film/v2/.
Then run words_v2.py to transcribe and regenerate src/curve_v2/film/words.ts.
  python3 vo_v2.py
"""
import pathlib, re, shutil, subprocess

HERE = pathlib.Path(__file__).parent
VO, PK = HERE / "vo", HERE / "vo" / "pickups_v2"
OUT = VO / "v2"
PUB = HERE.parents[1] / "motion" / "public" / "film" / "v2"
PAD = 0.15  # silence each pickup keeps (or is given) at either end, so a junction pause lands at about 0.25-0.3 s


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True, check=True).stdout)


def speech_bounds(f, noise="-40dB"):
    """First and last moment of speech (silencedetect at the file's edges)."""
    log = subprocess.run(["ffmpeg", "-nostats", "-i", str(f), "-af", f"silencedetect=noise={noise}:d=0.05", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    d = dur(f)
    a = en[0] if st and st[0] < 0.01 and en else 0.0
    b = st[-1] if st and (len(en) < len(st) or en[-1] >= d - 0.01) else d
    return a, b


def build(seg, parts):
    """parts: list of (file, t0, t1); t0/t1 None = the speech bounds of a pickup with PAD either side."""
    OUT.mkdir(parents=True, exist_ok=True)
    chain, inputs = [], []
    for i, (f, t0, t1) in enumerate(parts):
        lead = tail = 0.0
        if t0 is None:
            a, b = speech_bounds(f)
            t0, t1 = max(0.0, a - PAD), min(dur(f), b + PAD)
            lead, tail = PAD - (a - t0), PAD - (t1 - b)   # top up silence the take doesn't have
        inputs += ["-i", str(f)]
        chain.append(f"[{i}:a]aresample=44100,aformat=channel_layouts=mono,atrim={t0:.4f}:{t1:.4f},asetpts=PTS-STARTPTS,"
                     f"adelay={lead * 1000:.0f},apad=pad_dur={max(tail, 0):.3f}[p{i}]")
    cat = "".join(f"[p{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[o]"
    out = OUT / f"{seg}_t.mp3"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(chain) + ";" + cat, "-map", "[o]",
                    "-c:a", "libmp3lame", "-b:a", "192k", str(out)], check=True)
    print(f"{seg}: {dur(out):.2f} s")


# cut points (s) = middles of the silences measured on vo/<seg>_t.mp3 (silencedetect -40 dB, 0.12 s)
S1, S6, S7 = VO / "S1_t.mp3", VO / "S6_t.mp3", VO / "S7_t.mp3"
build("S1", [(S1, 0.0, 3.519), (PK / "s1_1b.mp3", None, None), (S1, 3.519, 23.492)])           # + promise beat, - loop-back line
build("S6", [(S6, 0.0, 20.827), (PK / "s6_4.mp3", None, None), (S6, 26.041, dur(S6))])         # s6_4 attributed to Top Gear
build("S7", [(S7, 0.0, 5.531), (PK / "s7_1b.mp3", None, None), (S7, 5.531, dur(S7))])          # + refund clause
for seg in ("b1", "b2"):
    build(seg, [(PK / f"{seg}.mp3", None, None)])                                               # bridges re-aimed
build("END", [(PK / "end_1.mp3", None, None)])                                                  # spoken end-card pointer
for seg in ("S2", "S3", "S4", "S5", "S8"):
    shutil.copy(VO / f"{seg}_t.mp3", OUT / f"{seg}_t.mp3")
PUB.mkdir(parents=True, exist_ok=True)
for f in OUT.glob("*_t.mp3"):
    shutil.copy(f, PUB / f"vo_{f.name[:-6]}.mp3")
print("->", PUB)
