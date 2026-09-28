"""The EP03 cold open in the decided look: ASCII all the way, a little Blender realism, other looks as rare accents.

  1848          Blender's chrome numerals, shaded in characters (tonal ASCII), with the line trace drawn in over them
                and a glint of bright characters sweeping across
  1848 → bottle the lines flow into the bottle in characters; the gold pours in
  the bottle    the characters re-form as Blender's glass bottle, then DEVELOP into the real image from the bottle out
  the burst     the photo breaks back into characters and, once, the feedback loop runs on them: character trails for
                "the whole city loses its mind"
  the store     the trails die away into clean characters; $36,000 in dense blocks with a glint; the street sells out
  the shovel    the characters re-form as the Blender dunes and develop into the image again, for the one lonely shot
  the grip      the push into the grip breaks back into characters, and the prize is a character too

Scored with Terminal (lab/music/beds.py), re-arranged so the drums arrive on "loses its mind" and drop out on
"never dug".

    python3 ascii_open.py still 2 9.6 13 ...   # build/ascii_still_*.png + build/ascii_sheet.jpg
    python3 ascii_open.py render               # build/style_S_ascii.mp4
"""
import math
import os
import subprocess
import sys

import numpy as np
from scipy.ndimage import maximum_filter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "music"))
import relay as R  # noqa: E402
from relay import S, ST, mg, skia, W, H, FPS, ASC, surface, plus, a_img, d_img, blend, cells_to_px  # noqa: E402

BUILD = S.BUILD
DUR = S.ls("rule") + 2.4
ease, seg, lerp = mg.ease, mg.seg, mg.lerp

TB, TM, TSH, TN, TR = S.ls("bottle"), S.ls("mind"), S.ls("shop"), S.ls("never"), S.ls("rule")
T_MORPH = S.at("bottle", 0.55)                                   # A's 1848 → bottle morph, and D's cut to the bottle
X1A, X1B = T_MORPH - 0.6, T_MORPH + 0.2                          # D's chrome characters hand over to the line ones
P1A, P1B = T_MORPH + 0.1, T_MORPH + 1.2                          # ...and the framing eases back to A's own
X2A = S.at("bottle", 0.95); X2B = X2A + 0.45                     # once the pour has settled, the line bottle re-forms as
DV2A, DV2B = X2A + 0.2, X2A + 0.8                                # the glass one (in characters), then develops into the image
UD3A, UD3B = TM + 1.2, TM + 1.75                                 # the cork pops, the gold streams out, then back to characters
X3A, X3B = TM + 1.5, TM + 2.3                                    # the characters' source: the Blender stream → the line one
FB_ON, FB_OFF = UD3A, TSH - 0.2                                  # the feedback loop on the characters
SW36 = S.at("36k", 0.55) + 1.25                                  # the $36,000 glint
SW1848 = TB + 1.5                                                # the 1848 glint
X6A = TN + 0.95; DV6A, DV6B = X6A + 0.4, X6A + 1.3               # the dunes: re-form, then develop
UD7A, UD7B = TR - 0.6, TR - 0.12                                 # into the grip: back to characters
X7A, X7B = TR - 0.3, TR + 0.15                                   # ...and on to A's ring and prize

EXTRA_SFX = [(SW1848, "scan", -18), (X2A + 0.3, "swell", -15), (UD3A - 0.05, "glitch", -17), (FB_OFF + 0.1, "thum", -15),
             (SW36, "scan", -17), (X6A + 0.35, "swell", -16), (UD7A + 0.1, "glitch", -19), (TR - 0.12, "sub_drop", -13)]


# ---------------------------------------------------------------- characters
def cells(arr, photo=0.0):
    """A frame (BGRA array) → the character field: the line mapping (thin strokes light a cell) or the tonal one
    (a lit surface becomes graded characters), blended by `photo`."""
    lum = (0.2126 * arr[..., 2] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 0]) / 255.0
    L2 = lum[: ASC.rows * ASC.ch, : ASC.cols * ASC.cw].reshape(ASC.rows, ASC.ch, ASC.cols, ASC.cw)
    mean, mx = L2.mean(axis=(1, 3)), L2.max(axis=(1, 3))
    line = np.clip((np.maximum(mean * 2.4, mx * 0.95) - 0.10) / 0.9, 0, 1) ** 0.75
    if photo <= 0:
        return line
    tonal = np.clip((0.75 * mean + 0.25 * mx - 0.04) * 1.6, 0, 1) ** 0.9
    return line * (1 - photo) + tonal * photo


def chars(cell, t, boost=None, sea=1.0):
    """The character layer (on black) from a field: strokes grow a character thick, the drifting sea underneath."""
    cell = np.maximum(cell, maximum_filter(cell, size=3) * 0.45)
    if boost is not None:
        cell = np.maximum(cell, boost)
    if sea > 0:
        cell = np.maximum(cell, ST.sea(t, ASC.cols, ASC.rows) ** 1.6 * 0.30 * sea)
    rgba = ASC.compose(cell, tint_lo=(18, 120, 112), tint_hi=(240, 244, 246))
    return skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)


def screen(layer):
    """Characters on the dark ground with their soft glow."""
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(8, 9, 11))
    c.drawImage(layer, 0, 0)
    gp = plus(0.5); gp.setImageFilter(skia.ImageFilters.Blur(6, 6))
    c.drawImage(layer, 0, 0, skia.SamplingOptions(), gp)
    return s.makeImageSnapshot()


def glint(k, cell, width=0.035):
    """A diagonal band of bright characters sweeping left to right, only where there's something to light."""
    yy, xx = np.mgrid[0:ASC.rows, 0:ASC.cols]
    u = xx / ASC.cols + 0.35 * (yy / ASC.rows)
    x0 = lerp(-0.2, 1.4, k)
    return np.exp(-((u - x0) / width) ** 2) * 0.95 * (cell > 0.12)


def develop(k, cx, cy):
    """Per-cell photo mask, spreading out from (cx, cy), each cell fading over a few frames."""
    yy, xx = np.mgrid[0:ASC.rows, 0:ASC.cols]
    dist = np.hypot((xx + 0.5) * ASC.cw - cx, ((yy + 0.5) * ASC.ch - cy) * 1.4) / 1150
    return np.clip((k * 1.35 - dist - 0.2 * R.NOISE2) / 0.12, 0, 1).astype(np.float32)


# ---------------------------------------------------------------- feedback on the characters (the one accent)
FB = {"prev": None, "i": None}


def fb_gain(t):
    if t < FB_OFF:
        return lerp(0.5, 0.86, ease(seg(t, FB_ON, FB_ON + 0.6)))
    return 0.86 * (1 - ease(seg(t, FB_OFF, FB_OFF + 0.7)))


def fb_at(t, layer_fn):
    i_t, i0 = int(round(t * FPS)), int(round(FB_ON * FPS))
    if FB["i"] is None or FB["i"] >= i_t or FB["i"] < i0 - 1:
        R.FB["prev"], FB["i"] = None, i0 - 1
    out = R.FB["prev"]
    for i in range(FB["i"] + 1, i_t + 1):
        out = R.fb_step(layer_fn(i / FPS), i / FPS, fb_gain(i / FPS))
        FB["i"] = i
    return out


# ---------------------------------------------------------------- the field at time t
def field(t):
    """The character field for the ASCII parts, from whichever sources are live at t."""
    if t < X1B:                                                    # D's chrome 1848 in tonal characters + the traced lines
        cd = cells(d_img(t).toarray(), 1.0)
        cl = cells(a_img(t, R.xf_1848(0.0), lines_only=True).toarray(), 0.0)
        c = np.maximum(cd * 0.9, cl)
        if t >= X1A:                                               # hand over to the line characters (same framing)
            u = ease(seg(t, X1A, X1B))
            c = c * (1 - u) + cl * u
        g = glint(seg(t, SW1848, SW1848 + 0.9), c) if SW1848 <= t < SW1848 + 0.9 else None
        return c, g
    if t < X2A:                                                    # lines: the morph, the pour
        return cells(a_img(t, R.xf_1848(ease(seg(t, P1A, P1B))), lines_only=True).toarray(), 0.0), None
    if t < X3A:                                                    # line bottle → the glass bottle, in characters
        w = ease(seg(t, X2A, X2B), "i")
        u = ease(seg(t, X2A + 0.1, X2B))
        cd = cells(d_img(t, R.xf_d_bottle(t)).toarray(), 1.0)
        if u >= 1:
            return cd, None
        ca = cells(a_img(t, R.xf_bottle(w), lines_only=True).toarray(), 0.0)
        return ca * (1 - u) + cd * u, None
    if t < X3B:                                                    # the burst → the dust stream
        u = ease(seg(t, X3A, X3B))
        cd = cells(d_img(t).toarray(), 1.0)
        return cd * (1 - u) + cells(a_img(t, lines_only=True).toarray(), 0.0) * u, None
    if t < X6A:                                                    # clean characters: store, $36,000, the street
        c = cells(a_img(t, lines_only=True).toarray(), 0.0)
        g = glint(seg(t, SW36, SW36 + 0.9), c) if SW36 <= t < SW36 + 0.9 else None
        return c, g
    if t < X7A:                                                    # the dunes, in characters (tonal), matched grip to grip
        u = ease(seg(t, X6A, X6A + 0.5))
        cd = cells(d_img(t, R.xf_shovel(t)).toarray(), 1.0)
        if u >= 1:
            return cd, None
        return cells(a_img(t, lines_only=True).toarray(), 0.0) * (1 - u) + cd * u, None
    u = ease(seg(t, X7A, X7B))                                     # into the grip, out into the prize
    cd = cells(d_img(t).toarray(), 1.0)
    return cd * (1 - u) + cells(a_img(t, lines_only=True).toarray(), 0.0) * u, tunnel_and_prize(t)


def tunnel_and_prize(t):
    """ASCII-native ending: rings of bright characters rushing outward as we pass through the grip, then the prize
    as a glowing, pulsing orb of characters."""
    yy, xx = np.mgrid[0:ASC.rows, 0:ASC.cols]
    d = np.hypot((xx + 0.5) * ASC.cw - 960, ((yy + 0.5) * ASC.ch - 520) * 1.15)
    b = np.zeros((ASC.rows, ASC.cols))
    for k in (0.0, 0.11, 0.22):
        a0 = TR - 0.4 + k
        if a0 <= t < a0 + 0.5:
            r = lerp(30, 1400, ease(seg(t, a0, a0 + 0.5), "i"))
            b = np.maximum(b, np.exp(-((d - r) / (14 + 0.05 * r)) ** 2) * 0.9 * (1 - 0.6 * seg(t, a0, a0 + 0.5)))
    if t >= TR - 0.05:
        r = 14 + 60 * ease(seg(t, TR, TR + 0.6), "o") + 5 * math.sin((t - TR) * 5)
        b = np.maximum(b, np.exp(-2 * (d / r) ** 2) * 0.95 + np.exp(-(d / (r * 2.6)) ** 2) * 0.35)
    return b


def photo_mask(t):
    """How much of the real (Blender) image shows, per cell: the bottle and the dunes only."""
    if DV2A <= t < UD3B:
        k = ease(seg(t, DV2A, DV2B)) if t < UD3A else 1 - ease(seg(t, UD3A, UD3B))
        return develop(k, 960, 620) if k > 0 else None, R.xf_d_bottle(t)
    if DV6A <= t < UD7B:
        k = ease(seg(t, DV6A, DV6B)) if t < UD7A else 1 - ease(seg(t, UD7A, UD7B))
        return develop(k, 960, 430) if k > 0 else None, R.xf_shovel(t)
    return None, None


def compose(t):
    c, g = field(t)
    if FB_ON <= t < FB_OFF + 0.8:                                  # the one feedback accent: character trails
        layer_fn = lambda tt: chars(field(tt)[0], tt, sea=0.0)
        fb = fb_at(t, layer_fn)
        s = skia.Surface(W, H); cv = s.getCanvas(); cv.clear(skia.Color(8, 9, 11))
        cv.drawImage(chars(np.zeros_like(c), t), 0, 0)             # the sea stays calm underneath
        cv.drawImage(fb, 0, 0, skia.SamplingOptions(), plus())
        gp = plus(0.45); gp.setImageFilter(skia.ImageFilters.Blur(6, 6))
        cv.drawImage(fb, 0, 0, skia.SamplingOptions(), gp)
        img = s.makeImageSnapshot()
    else:
        img = screen(chars(c, t, g))
    m, xf = photo_mask(t)
    if m is not None:
        img = blend(img.toarray(), d_img(t, xf).toarray(), cells_to_px(m))
    s = skia.Surface(W, H); cv = s.getCanvas()
    cv.drawImage(img, 0, 0)
    cv.drawRect(skia.Rect.MakeWH(W, H), R.VIGNETTE)
    S.furniture(cv)
    ST.captions(cv, t)
    return s.makeImageSnapshot()


# ---------------------------------------------------------------- the score
def score():
    """Terminal, re-arranged so a bar line falls on "loses its mind" (drums in) and on "never dug" (drums out),
    then dipped for "Here's the bit nobody tells you"."""
    import beds
    import audio_fx as fx
    n = max(4, round((TN - TM) / (240.0 / 96)))                   # bars from "mind" to "never", near 96 BPM
    bar = (TN - TM) / n
    bpm = 240.0 / bar
    n_intro = int((TM - 0.5) // bar)
    lead = TM - n_intro * bar
    n_break = max(1, math.ceil((TR - TN) / bar))
    a = min(3, n - 1)
    x = beds.terminal(bpm, [("intro", n_intro), ("a", a), ("b", n - a), ("break", n_break), ("out", 2)], lead)
    t = np.arange(len(x)) / fx.SR
    dip = 1 - 0.8 * np.clip((t - (TR - 0.05)) / 0.12, 0, 1) * np.clip(1 - (t - (TR + 1.2)) / 1.0, 0.35, 1)
    x = (x * dip[:, None]).astype(np.float32)
    path = os.path.join(BUILD, "ascii_bed.wav")
    fx.save(path, x, mp3=False)
    print(f"score: Terminal at {bpm:.2f} BPM, lead {lead:.2f}s")
    return path


def collect_events():
    """The picture's sound cues (forms, morphs, ticks, latches...) on the current timeline, at 30 fps as ep03s
    records them, into build/events.json for the mix."""
    import json
    S.EVENTS.clear()
    surf = skia.Surface(W, H)
    for i in range(int(DUR * S.FPS)):
        c = surf.getCanvas(); c.clear(skia.ColorBLACK)
        S.frame(c, i / S.FPS)
    json.dump(dict(events=S.EVENTS, dur=DUR), open(os.path.join(BUILD, "events.json"), "w"))
    print(len(S.EVENTS), "events")


def main():
    S.setup()
    if sys.argv[1] == "still":
        paths = []
        for tt in sorted(map(float, sys.argv[2:])):
            p = os.path.join(BUILD, f"ascii_still_{tt:05.2f}.png")
            compose(tt).save(p, skia.kPNG)
            paths.append(p)
            print(p, flush=True)
        cols, n = 4, len(paths)
        rows = (n + cols - 1) // cols
        ins = sum((["-i", p] for p in paths), [])
        pad = "".join(f"[{i}]scale=480:-1[s{i}];" for i in range(n))
        blanks = "".join(f"color=c=black:s=480x270:d=1[b{i}];" for i in range(rows * cols - n))
        grid = "".join(f"[s{i}]" for i in range(n)) + "".join(f"[b{i}]" for i in range(rows * cols - n))
        sheet = os.path.join(BUILD, "ascii_sheet.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", pad + blanks + grid + f"xstack=inputs={rows * cols}:grid={cols}x{rows}",
                        "-frames:v", "1", sheet], check=True)
        print(sheet)
        return
    silent = os.path.join(BUILD, "style_S_ascii_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        ff.stdin.write(compose(i / FPS).tobytes())
        if i % 120 == 0:
            print(f"{i / FPS:5.1f}s / {DUR:.1f}s", flush=True)
    ff.stdin.close(); ff.wait()
    import mix_open
    collect_events()
    audio = mix_open.build_mix(extra=EXTRA_SFX, out_name="ascii_mix.wav", bed_path=score(), bed_lufs=-17.0)
    mix_open.mux(silent, audio, os.path.join(BUILD, "style_S_ascii.mp4"), crf=21, maxrate="3600k", abr="192k")


if __name__ == "__main__":
    main()
