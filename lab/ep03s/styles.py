"""The EP03 cold open in three completely different styles, from one timeline and one pass:

  A  LINE MORPH  the A01 grammar: formations, morphs, chrome, push-through (ep03s.frame as it is)
  B  ASCII       everything rebuilt from characters: the scene becomes a character field over a drifting
                 character sea, lines turn into strokes of glyphs, chrome into dense blocks
  C  FEEDBACK    the TouchDesigner look: every frame is fed back into the next (zoomed, rotated, split into
                 red/green/blue), so shapes leave echo trails and tunnels; built in code since TouchDesigner
                 has no Linux version

Captions stand in for the voice until ElevenLabs George is connected. Music and effects are shared.

    python3 styles.py          # build/style_A_line.mp4, style_B_ascii.mp4, style_C_feedback.mp4 (silent)
"""
import json
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "visual"))
import ep03s as S  # noqa: E402
from ep03s import mg, skia, W, H, FPS, L  # noqa: E402
import holo  # noqa: E402

BUILD = S.BUILD
DUR = S.ls("rule") + 2.4


def captions(c, t, dark_box=True):
    live = [ln for ln in L if ln["start"] - 0.05 <= t <= ln["end"] + 0.25 and ln["start"] < DUR - 0.6]   # no flash of the next part's line
    if not live:
        return
    ln = live[-1]                             # the newest line wins, so two never overlap at a hand-over
    f = mg.font(mg.BODY_M, 38)
    words, lines, cur = ln["text"].split(), [], []
    for w in words:
        if f.measureText(" ".join(cur + [w])) > 1400 and cur:
            lines.append(cur); cur = [w]
        else:
            cur.append(w)
    lines.append(cur)
    k = (t - ln["start"]) / max(0.1, ln["end"] - ln["start"])
    spoken = int(k * len(words) + 0.5)
    y0 = H - 150 - (len(lines) - 1) * 48
    wi = 0
    for li, ws in enumerate(lines):
        s = " ".join(ws)
        wtot = f.measureText(s)
        x = W / 2 - wtot / 2
        if dark_box:
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 18, y0 + li * 48 - 36, wtot + 36, 50), 10, 10, mg.fill("#0B0C0E", 0.55))
        for w in ws:
            col = "#FFFFFF" if wi < spoken else mg.ON_DARK_SOFT
            c.drawString(w, x, y0 + li * 48, f, mg.fill(col, 1.0))
            x += f.measureText(w + " ")
            wi += 1


# ---------------------------------------------------------------- B · ASCII
ASC = None
SEA_T = [0.0]


def sea(t, cols, rows):
    yy, xx = np.mgrid[0:rows, 0:cols]
    u, v = xx / cols, yy / rows
    f = np.sin(u * 9.0 + t * 0.6) * np.cos(v * 7.0 - t * 0.4) + 0.5 * np.sin((u - v) * 13.0 + t * 0.9)
    return (f - f.min()) / (f.max() - f.min() + 1e-9)


def ascii_frame(src_bgra, t):
    global ASC
    if ASC is None:
        ASC = holo.Ascii(cols=192, rows=72)
    lum = (0.2126 * src_bgra[..., 2] + 0.7152 * src_bgra[..., 1] + 0.0722 * src_bgra[..., 0]) / 255.0
    rows, cols = ASC.rows, ASC.cols
    ch, cw = ASC.ch, ASC.cw
    L2 = lum[: rows * ch, : cols * cw].reshape(rows, ch, cols, cw)
    cell = np.maximum(L2.mean(axis=(1, 3)) * 2.4, L2.max(axis=(1, 3)) * 0.95)        # thin lines still light a cell
    cell = np.clip((cell - 0.10) / 0.9, 0, 1) ** 0.75
    from scipy.ndimage import maximum_filter
    halo = maximum_filter(cell, size=3) * 0.45                                        # strokes grow a character thick
    cell = np.maximum(cell, halo)
    bg = sea(t, cols, rows) ** 1.6 * 0.30
    field = np.maximum(cell, bg)
    img = ASC.compose(field, tint_lo=(18, 120, 112), tint_hi=(240, 244, 246))
    return img


# ---------------------------------------------------------------- C · feedback
FB = {"prev": None}


def feedback_frame(src_img, t):
    """out = src + 0.88 * warp(prev); warp = zoom 1.6 %, rotate 0.4 deg, with the red and blue channels
    scaled a little differently, so echoes fringe into colour at the edges."""
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    c.clear(skia.ColorBLACK)                  # accumulate on black; the ground goes under at the end
    prev = FB["prev"]
    if prev is not None:
        for (r, g, b), z in (((1, 0, 0), 1.022), ((0, 1, 0), 1.016), ((0, 0, 1), 1.010)):
            p = skia.Paint()
            p.setColorFilter(skia.ColorFilters.Matrix([r, 0, 0, 0, 0, 0, g, 0, 0, 0, 0, 0, b, 0, 0, 0, 0, 0, 0.88, 0]))
            p.setBlendMode(skia.BlendMode.kPlus)
            c.save()
            c.translate(W / 2, H / 2 - 20); c.rotate(0.4 * math.sin(t * 0.7) + 0.25); c.scale(z, z); c.translate(-W / 2, -(H / 2 - 20))
            c.drawImage(prev, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), p)
            c.restore()
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kPlus)
    c.drawImage(src_img, 0, 0, skia.SamplingOptions(), p)
    out = surf.makeImageSnapshot()
    FB["prev"] = out
    return out


def main():
    S.setup()
    os.makedirs(BUILD, exist_ok=True)
    outs = {k: os.path.join(BUILD, f"style_{k}_silent.mp4") for k in ("A_line", "B_ascii", "C_feedback")}
    ffs = {k: subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                                "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", v], stdin=subprocess.PIPE)
           for k, v in outs.items()}
    base = skia.Surface(W, H)
    lines_only = skia.Surface(W, H)
    n = int(DUR * FPS)
    for i in range(n):
        t = i / FPS
        c = base.getCanvas(); c.clear(skia.ColorBLACK)
        S.frame(c, t)
        img = base.makeImageSnapshot()
        arr = img.toarray()
        # A: as it is, plus captions
        a = skia.Surface(W, H); ca = a.getCanvas(); ca.drawImage(img, 0, 0); captions(ca, t)
        ffs["A_line"].stdin.write(a.makeImageSnapshot().tobytes())
        # B: ASCII
        asc = ascii_frame(arr, t)
        b = skia.Surface(W, H); cb = b.getCanvas(); cb.clear(skia.Color(8, 9, 11))
        simg = skia.Image.fromarray(asc, colorType=skia.ColorType.kRGBA_8888_ColorType)
        cb.drawImage(simg, 0, 0)
        gp = skia.Paint(BlendMode=skia.BlendMode.kPlus); gp.setImageFilter(skia.ImageFilters.Blur(6, 6)); gp.setAlphaf(0.5)
        cb.drawImage(simg, 0, 0, skia.SamplingOptions(), gp)
        captions(cb, t)
        ffs["B_ascii"].stdin.write(b.makeImageSnapshot().tobytes())
        # C: feedback, fed from the line layer drawn on black (no ground), so trails read
        cl = lines_only.getCanvas(); cl.clear(skia.ColorBLACK)
        g0 = S.GROUND["dark"]; S.GROUND["dark"] = BLACK
        S.frame(cl, t)
        S.GROUND["dark"] = g0
        fb = feedback_frame(lines_only.makeImageSnapshot(), t)
        cc = skia.Surface(W, H); c3 = cc.getCanvas(); c3.drawImage(S.GROUND["dark"], 0, 0)
        c3.drawImage(fb, 0, 0, skia.SamplingOptions(), PLUS); captions(c3, t)
        ffs["C_feedback"].stdin.write(cc.makeImageSnapshot().tobytes())
        if i % 150 == 0:
            print(f"{t:5.1f}s / {DUR:.1f}s", flush=True)
    for f in ffs.values():
        f.stdin.close(); f.wait()
    json.dump(dict(events=S.EVENTS, dur=DUR), open(os.path.join(BUILD, "events.json"), "w"))
    print("done", outs)


_b = skia.Surface(W, H); _b.getCanvas().clear(skia.ColorBLACK)
BLACK = _b.makeImageSnapshot()
PLUS = skia.Paint(BlendMode=skia.BlendMode.kPlus)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "still":
        S.setup()
        for tt in map(float, sys.argv[2:]):
            base = skia.Surface(W, H); c = base.getCanvas(); c.clear(skia.ColorBLACK); S.frame(c, tt)
            arr = base.makeImageSnapshot().toarray()
            asc = ascii_frame(arr, tt)
            b = skia.Surface(W, H); cb = b.getCanvas(); cb.clear(skia.Color(8, 9, 11))
            simg = skia.Image.fromarray(asc, colorType=skia.ColorType.kRGBA_8888_ColorType)
            cb.drawImage(simg, 0, 0); captions(cb, tt)
            b.makeImageSnapshot().save(os.path.join(BUILD, f"styleB_{tt:05.1f}.png"), skia.kPNG)
            # feedback needs history: run the 1.5 s before this frame
            FB["prev"] = None
            for k in range(45, -1, -1):
                t2 = tt - k / FPS
                ll = skia.Surface(W, H); cl = ll.getCanvas(); cl.clear(skia.ColorBLACK)
                g0 = S.GROUND["dark"]; S.GROUND["dark"] = BLACK; S.frame(cl, t2); S.GROUND["dark"] = g0
                fb = feedback_frame(ll.makeImageSnapshot(), t2)
            cc = skia.Surface(W, H); c3 = cc.getCanvas(); c3.drawImage(S.GROUND["dark"], 0, 0)
            c3.drawImage(fb, 0, 0, skia.SamplingOptions(), PLUS); captions(c3, tt)
            cc.makeImageSnapshot().save(os.path.join(BUILD, f"styleC_{tt:05.1f}.png"), skia.kPNG)
            print(tt)
    else:
        main()
