"""Vertical shorts (9:16, 1080x1920) from a finished film, for TikTok, Reels, YouTube Shorts and Facebook: a hook on
top (true to the film), the film in the middle (a crop of the caption-free feed over a blurred glow of itself),
George's words as big captions synced word by word, a thin progress line, and at the end a pointer to the next part
or the full video. The sound is the film's own mix, faded in and out.

A clip: dict(name, a (first line id), b (last line id), tag, hook, post, nxt (the next part's label or None)).
"""
import json
import os
import subprocess

import numpy as np

import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine.captions import word_times  # noqa: E402

W, H, FPS = 1080, 1920, 24
SW, SH = 1920, 1080
CROP = (280, 90, 1360, 800)                        # the part of the 16:9 frame that holds the picture (x, y, w, h)
FILM_Y = 560
FILM_H = int(W * CROP[3] / CROP[2])
CAP_Y = FILM_Y + FILM_H + 150                      # caption baseline: clear of the apps' bottom and right-hand UI
TURQ, WHITE, SOFT = "#35D6C6", "#FFFFFF", "#9AA3A8"
BRAND = "THE CURVE"
F = {}


def fonts():
    if not F:
        F.update(hook=mg.font("InterTight-600", 66), cap=mg.font("InterTight-600", 80), tag=mg.font("IBMPlexMono-500", 26),
                 end=mg.font("IBMPlexMono-500", 32))
    return F


def by_id(L, i_d):
    return next(x for x in L if x.get("id") == i_d)


def span(L, clip, total):
    """A beat before its first line, a breath after its last (parts butt together)."""
    a, b = by_id(L, clip["a"]), by_id(L, clip["b"])
    t0 = 0.0 if a is L[0] else max(0.0, a["start"] - 0.35)
    t1 = min(total, b["end"] + 0.9)
    return t0, t1


def caption_words(L, t0, t1):
    out = []
    for ln in L:
        if ln["end"] < t0 or ln["start"] > t1:
            continue
        out += word_times(ln)
    return out


def chunks(words, max_chars=18, max_words=3):
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
    rows, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if fnt.measureText(t) > width and cur:
            rows.append(cur); cur = w
        else:
            cur = t
    if cur:
        rows.append(cur)
    return rows


def text_center(c, s, y, fnt, paint, x=W / 2):
    c.drawString(s, x - fnt.measureText(s) / 2, y, fnt, paint)


def outline(col="#000000", w=12.0, a=0.85):
    p = mg.stroke(col, w, a)
    p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def frame(src, t, clip, t0, t1, chs):
    f = fonts()
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.Color(6, 7, 9))
    k = 8                                                        # a blurred, dark glow of the film behind it all
    sm = skia.Surface(W // k, H // k)
    sc = sm.getCanvas(); sc.clear(skia.Color(6, 7, 9))
    bw = (H // k) * SW / SH
    bg = skia.Paint(); bg.setImageFilter(skia.ImageFilters.Blur(38 / k, 38 / k))
    sc.translate((W // k) / 2 - bw / 2, 0)
    sc.drawImageRect(src, skia.Rect.MakeWH(bw, H // k), skia.SamplingOptions(skia.FilterMode.kLinear), bg)
    c.drawImageRect(sm.makeImageSnapshot(), skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear))
    c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#050607", 0.62))
    x, y, w, h = CROP
    c.drawImageRect(src, skia.Rect.MakeXYWH(x, y, w, h), skia.Rect.MakeXYWH(0, FILM_Y, W, FILM_H),
                    skia.SamplingOptions(skia.FilterMode.kLinear))
    for yy in (FILM_Y, FILM_Y + FILM_H):
        c.drawLine(0, yy, W, yy, mg.stroke(TURQ, 2, 0.35))
    dur = t1 - t0
    c.drawLine(0, FILM_Y + FILM_H + 3, W * min(1, t / dur), FILM_Y + FILM_H + 3, mg.stroke(TURQ, 5, 0.9))
    c.drawString(BRAND, 70, 250, f["tag"], mg.fill(TURQ, 1))
    c.drawString(clip["tag"], W - 70 - f["tag"].measureText(clip["tag"]), 250, f["tag"], mg.fill(SOFT, 1))
    y0 = 350
    for i, ln in enumerate(wrap(clip["hook"], f["hook"], W - 140)[:3]):
        text_center(c, ln, y0 + i * 80, f["hook"], outline(w=10, a=0.6))
        text_center(c, ln, y0 + i * 80, f["hook"], mg.fill(WHITE, 1))
    ft = t0 + t
    live = [ch for ch in chs if ch[0][1] - 0.05 <= ft <= ch[-1][2] + 0.35]
    if live:
        ch = live[-1]
        words = [w for w, _, _ in ch]
        xx = W / 2 - f["cap"].measureText(" ".join(words)) / 2
        for w, a_, b_ in ch:
            col = TURQ if a_ - 0.02 <= ft <= b_ + 0.08 else WHITE
            c.drawString(w, xx, CAP_Y, f["cap"], outline(w=14, a=0.9))
            c.drawString(w, xx, CAP_Y, f["cap"], mg.fill(col, 1))
            xx += f["cap"].measureText(w + " ")
    if t > dur - 2.2:
        kk = min(1.0, (t - (dur - 2.2)) / 0.3)
        msg = f"{clip['nxt']} NEXT →" if clip.get("nxt") else f"FULL VIDEO · {BRAND} ON YOUTUBE"
        text_center(c, msg, CAP_Y + 130, f["end"], mg.fill(TURQ, kk))
    return s.makeImageSnapshot()


def make(clip, L, feed, mix_wav, total, out_dir, tags=""):
    t0, t1 = span(L, clip, total)
    chs = chunks(caption_words(L, t0, t1))
    os.makedirs(out_dir, exist_ok=True)
    silent = os.path.join(out_dir, clip["name"] + "_silent.mp4")
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", feed, "-f", "rawvideo",
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
    out = os.path.join(out_dir, clip["name"] + ".mp4")
    d = n / FPS
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", mix_wav,
                    "-map", "0:v", "-map", "1:a", "-af", f"afade=t=in:d=0.08,afade=t=out:st={max(0, d - 0.3):.3f}:d=0.3",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "6000k", "-bufsize", "12000k", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], check=True)
    os.remove(silent)
    print(f"{clip['name']:10s} {t0:6.1f}-{t1:6.1f}s  {d:5.1f}s  {os.path.getsize(out) / 1e6:5.1f} MB", flush=True)
    return dict(name=clip["name"], file=os.path.basename(out), start=round(t0, 2), dur=round(d, 1), tag=clip["tag"],
                hook=clip["hook"], post=clip["post"] + (" " + tags if tags else ""))


def make_all(clips, L, feed, mix_wav, total, out_dir, tags="", want=()):
    kit = [make(c, L, feed, mix_wav, total, out_dir, tags) for c in clips if not want or c["name"] in want]
    kp = os.path.join(out_dir, "kit.json")
    old = json.load(open(kp)) if os.path.exists(kp) and want else []
    merged = {k["name"]: k for k in old + kit}
    json.dump([merged[c["name"]] for c in clips if c["name"] in merged], open(kp, "w"), indent=1)
    return kp
