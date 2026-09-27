"""The EP03 cold open as a style relay: the four looks from the shoot-out in one piece, each beat in the medium that
suits it, and every hand-off built so the shapes carry straight through (the styles share one timeline, so an object
is in the same place, at the same moment, in every look).

  0.0  D  chrome 1848 in Blender, a strong first frame
  1.4  D->A  TRACE: light lines draw over the chrome numerals (matched to them), the chrome dissolves, and the camera
             pulls back into the flat A framing
       A  the chrome fill, 1848 flows into the bottle, the gold pours in
  8.9  A->D  FILL: the line bottle is pushed onto the glass bottle (stretched to its outline) under a sheen
       D  the glass bottle of gold turning like a trophy, then the burst
 12.5  D->C  FRENZY: the burst's bright gold is fed into the feedback loop, and the trails become the stampede
       C  the town running for the river, in echo tunnels
 16.2  C->A  CALM: the feedback dies away, leaving clean lines; Sam's store forms
 19.9  A->B  DIGITISE: a scan sweeps left to right and turns the picture into characters, in step with the weeks
       B  nine weeks as progress bars, $36,000, the street selling out, all in characters
 29.0  B->D  DEVELOP: the characters re-form into the Blender dunes (matched to the line shovel), then develop from
             the shovel outwards into the image
       D  the lone shovel, the scoop that stops dead, the push into its grip
 32.0  D->A  THROUGH THE RING: both push into the grip at the same moment; a flash, and out comes A's prize

Captions, the episode label and a vignette go on top of everything, so it reads as one film.

    python3 relay.py still 1.0 2.2 9.3 ...   # build/relay_still_*.png + build/relay_sheet.jpg
    python3 relay.py render                  # build/style_R_relay.mp4 (1080p24, with the relay mix)
"""
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "visual"))
import ep03s as S  # noqa: E402
from ep03s import mg, skia, W, H  # noqa: E402
import styles as ST  # noqa: E402
import holo  # noqa: E402

FPS = 24
BUILD = S.BUILD
DUR = S.ls("rule") + 2.4
D_DIR = os.path.join(BUILD, "d24")                   # the Blender frames at 24 fps, before scaling and captions
ND = len([f for f in os.listdir(D_DIR) if f.endswith(".png")])
ease, seg, lerp, clamp = mg.ease, mg.seg, mg.lerp, mg.clamp
S.FURNITURE["label"] = False

# ---------------------------------------------------------------- the hand-off times (all from the voice's timing)
TB = S.ls("bottle")
T2A = S.at("bottle", 0.77); T2B = T2A + 0.8              # A -> D  fill
T3A = S.ls("mind") + 1.2; T3B = T3A + 0.8                # D -> C  frenzy
T4A = S.ls("shop") - 0.2; T4B = T4A + 0.9                # C -> A  calm
T5A = S.ls("36k") - 0.06; T5B = T5A + 0.7                # A -> B  digitise
T6A = S.ls("never") + 0.95; T6D0 = T6A + 0.4; T6D1 = T6D0 + 0.9   # B -> D  develop
T7A = S.ls("rule") - 0.42; T7B = S.ls("rule") - 0.05     # D -> A  through the ring
FB_START = T3A - 0.15

# where the shapes sit in each look (measured from the renders), for the match-moves
A1848_C, D1848_C, S1848 = (974.5, 496.5), (1008.0, 591.5), (1.68, 1.80)      # A's 1848 -> D's chrome 1848
BOTTLE_PIVOT, BOTTLE_S = (960.0, 480.0), (1.72, 2.0)                        # A's bottle stretched onto the glass
D_GRIP, A_GRIP, SHOVEL_S = (960.0, 59.0), (960.0, 28.0), 1.2               # D's shovel onto A's big shovel

EXTRA_SFX = [(TB + 0.05, "scan", -17), (T2A + 0.25, "swell", -15), (T3A - 0.05, "glitch", -18), (T3A + 0.05, "whoosh", -15),
             (T4A + 0.1, "thum", -14), (T5A, "glitch", -16), (T6A + 0.35, "swell", -16), (S.ls("rule") - 0.12, "sub_drop", -13)]

CUBIC = skia.SamplingOptions(skia.CubicResampler.Mitchell())
LINEAR = skia.SamplingOptions(skia.FilterMode.kLinear)


def plus(a=1.0):
    p = skia.Paint(BlendMode=skia.BlendMode.kPlus)
    p.setAlphaf(a)
    return p


def alpha(a):
    p = skia.Paint()
    p.setAlphaf(a)
    return p


def surface():
    s = skia.Surface(W, H)
    s.getCanvas().clear(skia.ColorBLACK)
    return s


# ---------------------------------------------------------------- the four sources
def a_img(t, xf=None, lines_only=False):
    """A (line morph) at time t, optionally through a transform (ax, ay, sx, sy, px, py): p -> a + s * (p - pivot)."""
    s = surface(); c = s.getCanvas()
    if xf:
        ax, ay, sx, sy, px, py = xf
        c.translate(ax, ay); c.scale(sx, sy); c.translate(-px, -py)
    g0 = S.GROUND["dark"]
    if lines_only:
        S.GROUND["dark"] = ST.BLACK
    S.frame(c, t)
    S.GROUND["dark"] = g0
    return s.makeImageSnapshot()


_D = {"i": None, "img": None}


def d_raw(t):
    i = min(max(0, int(round(t * FPS))), ND - 1)
    if _D["i"] != i:
        _D["img"] = skia.Image.open(os.path.join(D_DIR, f"{i:04d}.png"))
        _D["i"] = i
    return _D["img"]


def d_img(t, xf=None):
    """D (Blender) at time t, upscaled to 1080p, optionally through a transform like a_img's."""
    s = surface(); c = s.getCanvas()
    if xf:
        ax, ay, sx, sy, px, py = xf
        c.translate(ax, ay); c.scale(sx, sy); c.translate(-px, -py)
    c.drawImageRect(d_raw(t), skia.Rect.MakeWH(W, H), CUBIC)
    return s.makeImageSnapshot()


ASC = holo.Ascii(cols=192, rows=72)
RNG = np.random.default_rng(3)
NOISE = RNG.random((ASC.rows, ASC.cols))
NOISE2 = RNG.random((ASC.rows, ASC.cols))


def b_img(arr, t, boost=None, photo=0.0):
    """B (heavy ASCII) of a BGRA frame, as in styles.py, with an optional per-cell boost (the scan edge).
    photo (0..1) blends in a gentler mapping for photographic sources, so a lit surface becomes a tonal field of
    characters instead of a solid block (the line mapping boosts thin strokes hard)."""
    from scipy.ndimage import maximum_filter
    lum = (0.2126 * arr[..., 2] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 0]) / 255.0
    rows, cols, ch, cw = ASC.rows, ASC.cols, ASC.ch, ASC.cw
    L2 = lum[: rows * ch, : cols * cw].reshape(rows, ch, cols, cw)
    mean, mx = L2.mean(axis=(1, 3)), L2.max(axis=(1, 3))
    cell = np.clip((np.maximum(mean * 2.4, mx * 0.95) - 0.10) / 0.9, 0, 1) ** 0.75
    if photo > 0:
        tonal = np.clip((0.75 * mean + 0.25 * mx - 0.04) * 1.6, 0, 1) ** 0.9
        cell = cell * (1 - photo) + tonal * photo
    cell = np.maximum(cell, maximum_filter(cell, size=3) * 0.45)
    if boost is not None:
        cell = np.maximum(cell, boost)
    field = np.maximum(cell, ST.sea(t, cols, rows) ** 1.6 * 0.30)
    rgba = ASC.compose(field, tint_lo=(18, 120, 112), tint_hi=(240, 244, 246))
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(8, 9, 11))
    simg = skia.Image.fromarray(rgba, colorType=skia.ColorType.kRGBA_8888_ColorType)
    c.drawImage(simg, 0, 0)
    gp = plus(0.5); gp.setImageFilter(skia.ImageFilters.Blur(6, 6))
    c.drawImage(simg, 0, 0, skia.SamplingOptions(), gp)
    return s.makeImageSnapshot()


FB = {"prev": None, "i": None}


def fb_gain(t):
    if t < T4A:
        return lerp(0.55, 0.88, ease(seg(t, FB_START, T3A + 0.5)))
    return 0.88 * (1 - ease(seg(t, T4A, T4A + 0.6)))


def fb_source(t):
    """What feeds the loop: the burst's bright gold (keyed out of D), handing over to A's line layer."""
    lines = a_img(t, lines_only=True)
    w = ease(seg(t, T3A, T3B))
    if w >= 1:
        return lines
    arr = d_img(t).toarray()
    key = np.empty_like(arr)
    key[..., :3] = np.clip((arr[..., :3].astype(np.int16) - 80) * 1.7, 0, 255).astype(np.uint8)
    key[..., 3] = 255
    s = surface(); c = s.getCanvas()
    c.drawImage(skia.Image.fromarray(key, colorType=skia.ColorType.kBGRA_8888_ColorType), 0, 0, skia.SamplingOptions(), alpha(1 - w))
    c.drawImage(lines, 0, 0, skia.SamplingOptions(), plus(w))
    return s.makeImageSnapshot()


def fb_step(src, t, gain):
    """C (feedback): out = src + gain * warp(prev), the warp zooming each colour channel a touch differently."""
    s = surface(); c = s.getCanvas()
    prev = FB["prev"]
    if prev is not None and gain > 0.002:
        for (r, g, b), z in (((1, 0, 0), 1.022), ((0, 1, 0), 1.016), ((0, 0, 1), 1.010)):
            p = skia.Paint()
            p.setColorFilter(skia.ColorFilters.Matrix([r, 0, 0, 0, 0, 0, g, 0, 0, 0, 0, 0, b, 0, 0, 0, 0, 0, gain, 0]))
            p.setBlendMode(skia.BlendMode.kPlus)
            c.save()
            c.translate(W / 2, H / 2 - 20); c.rotate(0.4 * math.sin(t * 0.7) + 0.25); c.scale(z, z); c.translate(-W / 2, -(H / 2 - 20))
            c.drawImage(prev, 0, 0, LINEAR, p)
            c.restore()
    c.drawImage(src, 0, 0, skia.SamplingOptions(), plus())
    out = s.makeImageSnapshot()
    FB["prev"] = out
    return out


def fb_at(t):
    """The loop's output at t, stepping it one frame at a time from wherever it is (or from its start)."""
    i_t, i0 = int(round(t * FPS)), int(round(FB_START * FPS))
    if FB["i"] is None or FB["i"] >= i_t or FB["i"] < i0 - 1:
        FB["prev"], FB["i"] = None, i0 - 1
    out = FB["prev"]
    for i in range(FB["i"] + 1, i_t + 1):
        tt = i / FPS
        out = fb_step(fb_source(tt), tt, fb_gain(tt))
        FB["i"] = i
    return out


def c_img(t):
    s = surface(); c = s.getCanvas()
    c.drawImage(S.GROUND["dark"], 0, 0)
    c.drawImage(fb_at(t), 0, 0, skia.SamplingOptions(), plus())
    return s.makeImageSnapshot()


# ---------------------------------------------------------------- the hand-offs
def xf_1848(w):
    """A's flat 1848 laid over D's chrome one (w=0), easing back to A's own framing (w=1)."""
    return (lerp(D1848_C[0], A1848_C[0], w), lerp(D1848_C[1], A1848_C[1], w), lerp(S1848[0], 1, w), lerp(S1848[1], 1, w)) + A1848_C


def xf_bottle(w):
    return BOTTLE_PIVOT + (lerp(1, BOTTLE_S[0], w), lerp(1, BOTTLE_S[1], w)) + BOTTLE_PIVOT


def xf_d_bottle(t):
    z = lerp(1.1, 1.0, ease(seg(t, T2A + 0.35, T2B + 0.6), "o"))
    return BOTTLE_PIVOT + (z, z) + BOTTLE_PIVOT


def xf_shovel(t):
    """D's dune shot laid onto A's big line shovel (grip to grip), easing back to the Blender framing."""
    w = ease(seg(t, T6A + 0.2, T6A + 1.4))
    s = lerp(SHOVEL_S, 1.0, w)
    return (lerp(A_GRIP[0], D_GRIP[0], w), lerp(A_GRIP[1], D_GRIP[1], w), s, s) + D_GRIP


def cells_to_px(m):
    return np.repeat(np.repeat(m, ASC.ch, 0), ASC.cw, 1)[..., None]


def blend(a_arr, b_arr, m_px):
    out = a_arr.astype(np.float32) * (1 - m_px) + b_arr.astype(np.float32) * m_px
    return skia.Image.fromarray(out.clip(0, 255).astype(np.uint8), colorType=skia.ColorType.kBGRA_8888_ColorType)


def digitise(t):
    """Per-cell switch A->B behind a scan front sweeping left to right, and a bright column of characters at it."""
    xf = lerp(-0.08, 1.12, ease(seg(t, T5A, T5B)))
    thr = (np.arange(ASC.cols)[None, :] + 0.5) / ASC.cols + 0.10 * (NOISE - 0.5)
    d = xf - thr
    return (d > 0).astype(np.float32), np.exp(-(d / 0.022) ** 2) * 0.95


def develop(t):
    """Per-cell B->D, spreading out from the shovel's handle, each cell fading over a few frames."""
    k = ease(seg(t, T6D0, T6D1))
    yy, xx = np.mgrid[0:ASC.rows, 0:ASC.cols]
    dist = np.hypot((xx + 0.5) * ASC.cw - 960, ((yy + 0.5) * ASC.ch - 430) * 1.4) / 1150
    return np.clip((k * 1.35 - dist - 0.2 * NOISE2) / 0.12, 0, 1).astype(np.float32)


def sheen(c, k, a):
    if a <= 0.001:
        return
    x = lerp(-800, W + 800, k)
    c.save(); c.translate(x, H / 2); c.rotate(18)
    sh = skia.GradientShader.MakeLinear([skia.Point(-170, 0), skia.Point(170, 0)],
                                        [skia.Color(255, 255, 255, 0), skia.Color(255, 255, 255, 255), skia.Color(255, 255, 255, 0)])
    p = skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kPlus); p.setAlphaf(a)
    c.drawRect(skia.Rect(-170, -H, 170, H), p)
    c.restore()


def flash(c, a):
    if a <= 0.001:
        return
    sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), 900,
                                        [skia.Color(230, 255, 250, 255), skia.Color(18, 184, 172, 160), skia.Color(0, 0, 0, 0)], [0.0, 0.35, 1.0])
    p = skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kPlus); p.setAlphaf(a)
    c.drawRect(skia.Rect.MakeWH(W, H), p)


# ---------------------------------------------------------------- one frame
def compose(t):
    s = surface(); c = s.getCanvas()
    if t < TB + 2.4:                                          # D chrome 1848, traced in light, pulling back to A
        v = ease(seg(t, TB + 0.6, TB + 1.4))
        xf = xf_1848(ease(seg(t, TB + 1.2, TB + 2.4)))
        if v < 1:
            c.drawImage(d_img(t), 0, 0)
        if t >= TB:
            c.drawImage(a_img(t, xf), 0, 0, skia.SamplingOptions(), alpha(v))
            if v < 1:
                c.drawImage(a_img(t, xf, lines_only=True), 0, 0, skia.SamplingOptions(), plus(1 - v))
    elif t < T2A:
        c.drawImage(a_img(t), 0, 0)
    elif t < T3A + 0.1:                                       # A's bottle pushed onto the glass one; D
        w = ease(seg(t, T2A, T2B), "i")
        v = ease(seg(t, T2A + 0.35, T2B))
        if v < 1:
            c.drawImage(a_img(t, xf_bottle(w)), 0, 0)
        c.drawImage(d_img(t, xf_d_bottle(t)), 0, 0, skia.SamplingOptions(), alpha(v))
        sheen(c, seg(t, T2A + 0.15, T2B + 0.15), 0.22 * math.sin(math.pi * seg(t, T2A + 0.15, T2B + 0.15)))
    elif t < T4A:                                             # the burst fed into the loop; C
        v = ease(seg(t, T3A + 0.1, T3B))
        cimg = c_img(t)
        if v < 1:
            c.drawImage(d_img(t), 0, 0)
        c.drawImage(cimg, 0, 0, skia.SamplingOptions(), alpha(v))
    elif t < T4B:                                             # the loop dies away into clean lines
        v = ease(seg(t, T4A + 0.4, T4B))
        c.drawImage(c_img(t), 0, 0)
        c.drawImage(a_img(t), 0, 0, skia.SamplingOptions(), alpha(v))
    elif t < T5A:
        c.drawImage(a_img(t), 0, 0)
    elif t < T5B:                                             # digitise
        a_arr = a_img(t).toarray()
        m, boost = digitise(t)
        c.drawImage(blend(a_arr, b_img(a_arr, t, boost).toarray(), cells_to_px(m)), 0, 0)
    elif t < T6A:
        c.drawImage(b_img(a_img(t).toarray(), t), 0, 0)
    elif t < T6D1:                                            # the characters re-form as the dunes, then develop
        u = ease(seg(t, T6A, T6A + 0.5))
        dx = d_img(t, xf_shovel(t)).toarray()
        src = dx if u >= 1 else (a_img(t).toarray().astype(np.float32) * (1 - u) + dx.astype(np.float32) * u).astype(np.uint8)
        c.drawImage(blend(b_img(src, t, photo=u).toarray(), dx, cells_to_px(develop(t))), 0, 0)
    elif t < T7A:
        c.drawImage(d_img(t, xf_shovel(t)), 0, 0)
    else:                                                     # through the ring: D's push hands over to A's
        v = ease(seg(t, T7A + 0.05, T7B))
        if v < 1:
            c.drawImage(d_img(t), 0, 0)
        c.drawImage(a_img(t), 0, 0, skia.SamplingOptions(), alpha(v))
        flash(c, 0.55 * math.sin(math.pi * seg(t, T7A + 0.1, T7B + 0.15)))
    # one film: the vignette, the label and the captions over every look
    c.drawRect(skia.Rect.MakeWH(W, H), VIGNETTE)
    S.furniture(c)
    ST.captions(c, t)
    return s.makeImageSnapshot()


VIGNETTE = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), 1180,
                                                             [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 120)],
                                                             [0.0, 0.55, 1.0]))


def main():
    S.setup()
    if sys.argv[1] == "still":
        paths = []
        for tt in sorted(map(float, sys.argv[2:])):
            p = os.path.join(BUILD, f"relay_still_{tt:05.2f}.png")
            compose(tt).save(p, skia.kPNG)
            paths.append(p)
            print(p, flush=True)
        sheet = os.path.join(BUILD, "relay_sheet.jpg")
        cols = 4
        ins = sum((["-i", p] for p in paths), [])
        n = len(paths)
        rows = (n + cols - 1) // cols
        pad = "".join(f"[{i}]scale=480:-1[s{i}];" for i in range(n))
        blanks = "".join(f"color=c=black:s=480x270:d=1[b{i}];" for i in range(rows * cols - n))
        grid = "".join(f"[s{i}]" for i in range(n)) + "".join(f"[b{i}]" for i in range(rows * cols - n))
        subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", pad + blanks + grid + f"xstack=inputs={rows * cols}:grid={cols}x{rows}",
                        "-frames:v", "1", sheet], check=True)
        print(sheet)
        return
    silent = os.path.join(BUILD, "style_R_relay_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        ff.stdin.write(compose(i / FPS).tobytes())
        if i % 120 == 0:
            print(f"{i / FPS:5.1f}s / {DUR:.1f}s", flush=True)
    ff.stdin.close(); ff.wait()
    import mix_open
    audio = mix_open.build_mix(extra=EXTRA_SFX, out_name="relay_mix.wav", fresh_bed=False)
    mix_open.mux(silent, audio, os.path.join(BUILD, "style_R_relay.mp4"), crf=21, maxrate="3300k", abr="192k")


if __name__ == "__main__":
    main()
