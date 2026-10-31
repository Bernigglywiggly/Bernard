"""Vertical shorts (9:16, 1080x1920) from a finished film, for TikTok, Instagram Reels, YouTube Shorts and Facebook.
The user (28 Sep): break every long video into short-form, both as parts that add up to the whole and as the most
interesting, most visual moments, and push them hard.

Each short: a hook line on top (what the clip is about, true to the film), the film in the middle (a crop of the
caption-free render, over a blurred glow of itself), George's words as big captions synced word by word (the
ElevenLabs timings in build/lines.json) in the zone the apps leave clear, a thin progress line, and at the end a
pointer to the next part or to the full video. The sound is the film's own mix, faded in and out.

    EP03_FULL=1 NO_CAPTIONS=1 python3 ascii_open.py render_full 4   # the caption-free film (build/ep03_full_clean_silent.mp4)
    python3 shorts.py                     # every clip below -> build/shorts/<name>.mp4 + build/shorts/kit.json
    python3 shorts.py part1 bigmac        # just those
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(HERE, "..", "..", "a01_v6")
sys.path.insert(0, V6)
os.environ.setdefault("A01V6_FONTS", os.path.join(V6, "fonts"))
import mograph as mg  # noqa: E402
import skia  # noqa: E402

BUILD = os.path.join(HERE, "build")
OUT = os.path.join(BUILD, "shorts")
W, H, FPS = 1080, 1920, 24
SW, SH = 1920, 1080
CROP = (280, 90, 1360, 800)                        # the part of the 16:9 frame that holds the picture (x, y, w, h)
FILM_Y = 560
FILM_H = int(W * CROP[3] / CROP[2])
CAP_Y = FILM_Y + FILM_H + 150                      # caption baseline: clear of TikTok's bottom and right-hand UI
TURQ, WHITE, SOFT = "#35D6C6", "#FFFFFF", "#9AA3A8"

# every clip: first line id, last line id, the tag, the hook (true to the film), the post caption and hashtags
TAGS = "#ai #nvidia #openai #goldrush #history #money #economics #tech #bigmac #thecurve"
CLIPS = [
    dict(name="part1", a="bottle", b="rule", tag="THE SHOVEL SELLERS · PART 1 OF 4", nxt="PART 2",
         hook="Who actually gets rich in a gold rush?",
         post="May 1848: a shopkeeper walks through San Francisco holding up a bottle of gold. He'd already bought every shovel in town. Part 1 of 4."),
    dict(name="part2", a="census", b="rome", tag="THE SHOVEL SELLERS · PART 2 OF 4", nxt="PART 3",
         hook="Two economists checked the gold rush census",
         post="For miners, the gains were small or even zero. For everyone else, positive and large. Then 2026: $725 billion. Part 2 of 4."),
    dict(name="part3", a="nvidia", b="fair", tag="THE SHOVEL SELLERS · PART 3 OF 4", nxt="PART 4",
         hook="The company selling today's shovels",
         post="Nvidia took in about 2,000 Big Macs of money every second. OpenAI spent about $1.65 for every $1 it made. Part 3 of 4."),
    dict(name="part4", a="before", b="chain", tag="THE SHOVEL SELLERS · PART 4 OF 4", nxt=None,
         hook="It has happened before",
         post="1846: Britain's railway mania. The speculation disappeared. The infrastructure stayed. So what becomes scarce next? Part 4 of 4."),
    dict(name="bigmac", a="shop", b="never", tag="THE SHOVEL SELLERS", nxt=None,
         hook="He never dug for gold. He became California's first millionaire.",
         post="Sam Brannan bought every pan and shovel before the gold rush. A 20-cent pan sold for $15. At that markup a Big Mac would cost $466."),
    dict(name="romans", a="capex", b="rome", tag="THE SHOVEL SELLERS", nxt=None,
         hook="$725 billion is a million dollars a day since AD 43",
         post="Amazon, Microsoft, Alphabet and Meta plan to spend around $725 billion this year, mostly on AI data centres. Spend $1M a day since the Romans invaded Britain and you'd only just have spent it."),
    dict(name="nvidia", a="nvidia", b="margin", tag="THE SHOVEL SELLERS", nxt=None,
         hook="Nvidia makes about 2,000 Big Macs of money a second",
         post="Nvidia took in $96.2 billion in three months. That's about $12,000 a second, or 2,000 Big Macs. And of every $4, only about $1 goes on making the chips."),
    dict(name="openai", a="openai", b="fair", tag="THE SHOVEL SELLERS", nxt=None,
         hook="OpenAI spends about $1.65 for every $1 it makes",
         post="OpenAI took in $5.7 billion in Q1 2026 and burned through $3.7 billion. The diggers aren't wrong. But the supplier is paid first."),
    dict(name="railway", a="before", b="layers", tag="THE SHOVEL SELLERS", nxt=None,
         hook="Britain's railway bubble left something behind",
         post="1846: Parliament approved 272 railway companies in one year, more than five a week. A third of the track was never built. By 1850 Britain still had about 6,000 miles of it."),
    dict(name="scarce", a="imagine", b="question", tag="THE SHOVEL SELLERS · A WHAT-IF", nxt=None,
         hook="If intelligence gets cheap, what gets scarce?",
         post="Imagine it's 2030 and the AI build-out is finished. Not a forecast, a what-if. Intelligence is everywhere, like tap water. So what becomes scarce?"),
]


def lines():
    return json.load(open(os.path.join(BUILD, "lines.json")))["lines"]


def by_id(L, i_d):
    return next(x for x in L if x.get("id") == i_d)


def span(L, clip, total):
    """Where a clip starts and ends: a beat before its first line, a breath after its last (parts butt together)."""
    a, b = by_id(L, clip["a"]), by_id(L, clip["b"])
    t0 = 0.0 if a is L[0] else max(0.0, a["start"] - 0.35)
    t1 = min(total, b["end"] + 0.9)
    return t0, t1


def caption_words(L, t0, t1):
    """(word, start, end) for the caption text (not the spelled-out spoken text): the displayed words take their
    timings from George's, matched by position when a line's spoken words differ ("1848" said as three words)."""
    out = []
    for ln in L:
        if ln["end"] < t0 or ln["start"] > t1:
            continue
        shown = ln["text"].split()
        spoken = ln.get("words") or []
        if not spoken:
            d = (ln["end"] - ln["start"]) / max(1, len(shown))
            out += [(w, ln["start"] + i * d, ln["start"] + (i + 1) * d) for i, w in enumerate(shown)]
            continue
        n, m = len(shown), len(spoken)
        starts = [spoken[int(round(i * (m - 1) / max(1, n - 1))) if n > 1 else 0][1] for i in range(n)]
        for i, w in enumerate(shown):
            e_ = starts[i + 1] - 0.02 if i + 1 < n else spoken[-1][2]
            out.append((w, starts[i], max(e_, starts[i] + 0.05)))
    return out


def chunks(words, max_chars=18, max_words=3):
    """Group words into short caption chunks, breaking at punctuation."""
    out, cur = [], []
    for w in words:
        cur.append(w)
        text = " ".join(x[0] for x in cur)
        if len(cur) >= max_words or len(text) >= max_chars or w[0][-1] in ".,?!:;":
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def wrap(text, fnt, width):
    lines_, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if fnt.measureText(t) > width and cur:
            lines_.append(cur); cur = w
        else:
            cur = t
    if cur:
        lines_.append(cur)
    return lines_


F_HOOK = mg.font("InterTight-600", 66)
F_CAP = mg.font("InterTight-600", 80)
F_TAG = mg.font("IBMPlexMono-500", 26)
F_END = mg.font("IBMPlexMono-500", 32)


def text_center(c, s, y, fnt, paint, x=W / 2):
    c.drawString(s, x - fnt.measureText(s) / 2, y, fnt, paint)


def outline(col="#000000", w=12.0, a=0.85):
    p = mg.stroke(col, w, a)
    p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def frame(src, t, clip, t0, t1, chs):
    """One vertical frame: src is the 16:9 frame (skia.Image) at clip time t (film time t0 + t)."""
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.Color(6, 7, 9))
    k = 8                                                        # a blurred, dark glow of the film behind it all,
    sm = skia.Surface(W // k, H // k)                            # blurred small and scaled up (the same look, far quicker)
    sc = sm.getCanvas(); sc.clear(skia.Color(6, 7, 9))
    bw = (H // k) * SW / SH
    bg = skia.Paint(); bg.setImageFilter(skia.ImageFilters.Blur(38 / k, 38 / k))
    sc.translate((W // k) / 2 - bw / 2, 0)
    sc.drawImageRect(src, skia.Rect.MakeWH(bw, H // k), skia.SamplingOptions(skia.FilterMode.kLinear), bg)
    c.drawImageRect(sm.makeImageSnapshot(), skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear))
    c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#050607", 0.62))
    x, y, w, h = CROP                                            # the film
    c.drawImageRect(src, skia.Rect.MakeXYWH(x, y, w, h), skia.Rect.MakeXYWH(0, FILM_Y, W, FILM_H),
                    skia.SamplingOptions(skia.FilterMode.kLinear))
    for yy in (FILM_Y, FILM_Y + FILM_H):
        c.drawLine(0, yy, W, yy, mg.stroke(TURQ, 2, 0.35))
    dur = t1 - t0                                                # a thin progress line under the film
    c.drawLine(0, FILM_Y + FILM_H + 3, W * min(1, t / dur), FILM_Y + FILM_H + 3, mg.stroke(TURQ, 5, 0.9))
    c.drawString("THE CURVE", 70, 250, F_TAG, mg.fill(TURQ, 1))   # the brand and the tag
    c.drawString(clip["tag"], W - 70 - F_TAG.measureText(clip["tag"]), 250, F_TAG, mg.fill(SOFT, 1))
    y0 = 350                                                     # the hook
    for i, ln in enumerate(wrap(clip["hook"], F_HOOK, W - 140)[:3]):
        text_center(c, ln, y0 + i * 80, F_HOOK, outline(w=10, a=0.6))
        text_center(c, ln, y0 + i * 80, F_HOOK, mg.fill(WHITE, 1))
    ft = t0 + t                                                  # the captions, word by word
    live = [ch for ch in chs if ch[0][1] - 0.05 <= ft <= ch[-1][2] + 0.35]
    if live:
        ch = live[-1]
        words = [w for w, _, _ in ch]
        total_w = F_CAP.measureText(" ".join(words))
        x = W / 2 - total_w / 2
        for w, a_, b_ in ch:
            col = TURQ if a_ - 0.02 <= ft <= b_ + 0.08 else WHITE
            c.drawString(w, x, CAP_Y, F_CAP, outline(w=14, a=0.9))
            c.drawString(w, x, CAP_Y, F_CAP, mg.fill(col, 1))
            x += F_CAP.measureText(w + " ")
    if t > dur - 2.2:                                            # where to go next
        k = min(1.0, (t - (dur - 2.2)) / 0.3)
        msg = f"{clip['nxt']} NEXT →" if clip.get("nxt") else "FULL VIDEO · THE CURVE ON YOUTUBE"
        text_center(c, msg, CAP_Y + 130, F_END, mg.fill(TURQ, k))
    return s.makeImageSnapshot()


def make(clip, L, src_video, mix_wav, total):
    t0, t1 = span(L, clip, total)
    chs = chunks(caption_words(L, t0, t1))
    os.makedirs(OUT, exist_ok=True)
    silent = os.path.join(OUT, clip["name"] + "_silent.mp4")
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", src_video, "-f", "rawvideo",
                            "-pix_fmt", "bgra", "-r", str(FPS), "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", silent],
                           stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = dec.stdout.read(SW * SH * 4)
        if len(buf) < SW * SH * 4:
            break
        arr = np.frombuffer(buf, np.uint8).reshape(SH, SW, 4)
        src = skia.Image.fromarray(arr, colorType=skia.ColorType.kBGRA_8888_ColorType)
        enc.stdin.write(frame(src, n / FPS, clip, t0, t1, chs).tobytes())
        n += 1
    dec.wait(); enc.stdin.close(); enc.wait()
    out = os.path.join(OUT, clip["name"] + ".mp4")
    d = n / FPS
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", mix_wav,
                    "-map", "0:v", "-map", "1:a", "-af", f"afade=t=in:d=0.08,afade=t=out:st={max(0, d - 0.3):.3f}:d=0.3",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "6000k", "-bufsize", "12000k", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], check=True)
    os.remove(silent)
    print(f"{clip['name']:10s} {t0:6.1f}-{t1:6.1f}s  {d:5.1f}s  {os.path.getsize(out) / 1e6:5.1f} MB", flush=True)
    return dict(name=clip["name"], file=os.path.basename(out), start=round(t0, 2), dur=round(d, 1), tag=clip["tag"],
                hook=clip["hook"], post=clip["post"] + " " + TAGS)


def main():
    L = lines()
    total = json.load(open(os.path.join(BUILD, "events.json")))["dur"]
    src = os.path.join(BUILD, "ep03_full_clean_silent.mp4")
    if not os.path.exists(src):
        src = os.path.join(BUILD, "ep03_full_silent.mp4")
        print("no clean feed yet: using the captioned render", flush=True)
    mix = os.path.join(BUILD, "ep03_full_mix.wav")
    want = sys.argv[1:]
    kit = [make(c, L, src, mix, total) for c in CLIPS if not want or c["name"] in want]
    kp = os.path.join(OUT, "kit.json")
    old = json.load(open(kp)) if os.path.exists(kp) and want else []
    merged = {k["name"]: k for k in old + kit}
    json.dump([merged[c["name"]] for c in CLIPS if c["name"] in merged], open(kp, "w"), indent=1)


if __name__ == "__main__":
    main()
