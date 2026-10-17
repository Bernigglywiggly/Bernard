"""Big Man gag reel (1920x1080, ~12 s): the comedy grammar from the user's brain dump, on stand-in backgrounds
until the real-looking plates arrive.

  1. "we'll be fine here."  -> smash cut: the nuke -> hard cut: soot, two blinks, "fuck.", falls over like a plank
  2. the page rip into the next scene
  3. looks under the car for the tin opener -> a beat -> a comically large fist -> through a letterbox, legs kicking
  4. the cut-off reaction: "oh—" and straight to black

The voice lines are placeholders (George) for the user's own voiceover.

    python3 gag_reel.py        # build/gag_reel.mp4
"""
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "voice"))
import character as ch  # noqa: E402
from character import mg, skia  # noqa: E402
import audio_fx as fx  # noqa: E402

W, H, FPS = 1920, 1080, 30
SR = fx.SR
OUT = os.path.join(HERE, "build")
R = 58
FLOOR = 880
LEG = 3.6 * R

# the beats (seconds)
T_LINE, T_NUKE, T_AFTER, T_FUCK, T_FALL, T_RIP, T_WALK = 0.35, 1.75, 2.85, 4.25, 4.95, 5.75, 6.25
T_LOOK, T_FIST, T_BOX, T_OH, T_END = 7.45, 8.2, 8.75, 10.35, 10.75
DUR = 11.6


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    return clamp((t - a) / (b - a))


def ease(x):
    return x * x * (3 - 2 * x)


def lerp(a, b, k):
    return a + (b - a) * k


def P(x, **kw):
    base = dict(R=R, lean=0, head=0, arms=[(-14, -8), (14, 8)], legs=[(-9, 2), (9, -2)], face="neutral",
                root=(x, FLOOR - LEG), hat=dict(tilt=0))
    base.update(kw)
    return base


def caption(c, s, a=1.0):
    f = mg.font(mg.BODY_M, 46)
    w = f.measureText(s)
    c.drawRoundRect(skia.Rect.MakeXYWH(W / 2 - w / 2 - 22, 958, w + 44, 70), 14, 14, mg.fill("#0B0C0E", 0.6 * a))
    c.drawString(s, W / 2 - w / 2, 1006, f, mg.fill("#FFFFFF", a))


# ---------------------------------------------------------------- stand-in worlds
def ground_day(c):
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [mg.hexc("#2A3440"), mg.hexc("#14171C")], [0.0, 1.0])
    p = skia.Paint(); p.setShader(sh)
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    c.drawRect(skia.Rect.MakeXYWH(0, FLOOR + 4, W, H - FLOOR), mg.fill("#1B1F25", 1.0))
    c.drawLine(0, FLOOR + 4, W, FLOOR + 4, mg.stroke("#8A919C", 2, 0.5))


def sign(c, x, y):
    c.drawLine(x, y, x, FLOOR, mg.stroke("#C9CED6", 8, 1.0))
    r = skia.Rect.MakeXYWH(x - 170, y - 110, 340, 110)
    c.drawRoundRect(r, 10, 10, mg.fill("#E9EBEE", 1.0))
    f = mg.font(mg.MONO_M, 28)
    for j, s in enumerate(("SAFE ZONE", "(PROBABLY)")):
        c.drawString(s, x - f.measureText(s) / 2, y - 64 + j * 38, f, mg.fill("#14161A", 1.0))


def nuke(c, k, shake):
    """The mushroom: a white core, an orange cap, a rising stem, a shock ring."""
    c.save()
    c.translate(shake[0], shake[1])
    sky = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [mg.hexc("#FFD9A8"), mg.hexc("#FF8A3D"), mg.hexc("#3A1C10")], [0.0, 0.5, 1.0])
    p = skia.Paint(); p.setShader(sky)
    c.drawRect(skia.Rect.MakeXYWH(-40, -40, W + 80, H + 80), p)
    cx, base = W / 2, FLOOR + 40
    rise = ease(k)
    top = lerp(base - 160, 150, rise)
    stem = skia.Path()
    stem.moveTo(cx - 150, base); stem.quadTo(cx - 70, (base + top) / 2, cx - 110, top + 90)
    stem.lineTo(cx + 110, top + 90); stem.quadTo(cx + 70, (base + top) / 2, cx + 150, base); stem.close()
    c.drawPath(stem, mg.fill("#FFF1D6", 1.0))
    rng = np.random.default_rng(5)
    for j in range(26):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(60, 380) * (0.4 + 0.6 * rise)
        x, y = cx + math.cos(a) * rr * 1.35, top + math.sin(a) * rr * 0.5
        col = ["#FFFFFF", "#FFE2B0", "#FFB067", "#FF8A3D", "#9A5A3A"][j % 5]
        c.drawCircle(x, y, rng.uniform(90, 190) * (0.5 + 0.5 * rise), mg.fill(col, 0.95))
    ring = mg.stroke("#FFFFFF", 10 * (1 - k) + 2, 0.8 * (1 - k))
    c.drawOval(skia.Rect.MakeXYWH(cx - 900 * k, base - 60 * k, 1800 * k, 120 * k), ring)
    c.restore()
    if k < 0.12:                                                  # the flash
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#FFFFFF", 1 - k / 0.12))


def smoke_sky(c, t):
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [mg.hexc("#B7A08A"), mg.hexc("#7A5A46"), mg.hexc("#2A1E18")], [0.0, 0.55, 1.0])
    p = skia.Paint(); p.setShader(sh)
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    c.drawRect(skia.Rect.MakeXYWH(0, FLOOR + 4, W, H - FLOOR), mg.fill("#2A2522", 1.0))
    rng = np.random.default_rng(9)
    for j in range(40):                                           # embers drifting up
        x = rng.uniform(0, W)
        y = (rng.uniform(0, H) - t * rng.uniform(40, 120)) % H
        c.drawCircle(x, y, rng.uniform(1.5, 3.5), mg.fill("#FFB067", 0.7))


def night_street(c):
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, H)], [mg.hexc("#0E1522"), mg.hexc("#1B2433")], [0.0, 1.0])
    p = skia.Paint(); p.setShader(sh)
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    g = mg.fill("#FFB067", 0.25)
    g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
    c.drawCircle(380, 300, 160, g)
    c.drawLine(380, 300, 380, FLOOR, mg.stroke("#3A4352", 10, 1.0))
    c.drawCircle(380, 300, 16, mg.fill("#FFD9A8", 1.0))
    c.drawRect(skia.Rect.MakeXYWH(0, FLOOR + 4, W, H - FLOOR), mg.fill("#161B24", 1.0))
    c.drawLine(0, FLOOR + 4, W, FLOOR + 4, mg.stroke("#8A919C", 2, 0.4))


def car(c, x, y):
    """A side-on hatchback in line art; (x, y) is the bottom-left of the body."""
    body = skia.Path()
    body.moveTo(x, y - 40); body.lineTo(x + 20, y - 130); body.lineTo(x + 170, y - 140); body.lineTo(x + 260, y - 230)
    body.lineTo(x + 470, y - 230); body.lineTo(x + 560, y - 140); body.lineTo(x + 660, y - 120); body.lineTo(x + 680, y - 40); body.close()
    c.drawPath(body, mg.fill("#20262F", 1.0))
    c.drawPath(body, mg.stroke("#C9CED6", 4, 1.0))
    win = skia.Path(); win.moveTo(x + 280, y - 215); win.lineTo(x + 460, y - 215); win.lineTo(x + 530, y - 145); win.lineTo(x + 200, y - 145); win.close()
    c.drawPath(win, mg.fill("#3A4F66", 0.8))
    for wx in (x + 150, x + 540):
        c.drawCircle(wx, y - 30, 62, mg.fill("#0B0C0E", 1.0))
        c.drawCircle(wx, y - 30, 62, mg.stroke("#C9CED6", 4, 1.0))
        c.drawCircle(wx, y - 30, 24, mg.stroke("#8A919C", 3, 1.0))


def fist(c, x, y, s, a=1.0):
    """A comically large cartoon fist punching to the right; (x, y) = the knuckles."""
    c.save(); c.translate(x, y); c.scale(s, s)
    arm = skia.Rect.MakeXYWH(-900, -70, 820, 140)
    c.drawRect(arm, mg.fill("#E9EBEE", a))
    c.drawRect(arm, mg.stroke("#14161A", 6, a))
    palm = skia.Rect.MakeXYWH(-130, -130, 170, 260)
    c.drawRoundRect(palm, 60, 60, mg.fill("#E9EBEE", a))
    c.drawRoundRect(palm, 60, 60, mg.stroke("#14161A", 6, a))
    for j in range(4):
        r = skia.Rect.MakeXYWH(-10, -125 + j * 62, 90, 62)
        c.drawRoundRect(r, 28, 28, mg.fill("#E9EBEE", a))
        c.drawRoundRect(r, 28, 28, mg.stroke("#14161A", 6, a))
    c.restore()


def door(c, x, legs_t=None):
    """A front door with a letterbox; legs_t animates his legs kicking out of it."""
    c.drawRect(skia.Rect.MakeXYWH(x, FLOOR - 560, 300, 560), mg.fill("#2B4B6F", 1.0))
    c.drawRect(skia.Rect.MakeXYWH(x, FLOOR - 560, 300, 560), mg.stroke("#C9CED6", 5, 1.0))
    for j in range(2):
        c.drawRect(skia.Rect.MakeXYWH(x + 36, FLOOR - 520 + j * 250, 228, 200), mg.stroke("#1B3350", 5, 1.0))
    c.drawCircle(x + 262, FLOOR - 280, 10, mg.fill("#E0B458", 1.0))
    slot = skia.Rect.MakeXYWH(x + 90, FLOOR - 330, 120, 26)
    c.drawRoundRect(slot, 4, 4, mg.fill("#0B0C0E", 1.0))
    c.drawRoundRect(slot, 4, 4, mg.stroke("#E0B458", 4, 1.0))
    if legs_t is not None:
        for j, ph in enumerate((0.0, 1.7)):
            ang = 20 * math.sin(legs_t * 16 + ph)
            x0, y0 = x + 130 + j * 40, FLOOR - 317
            k1 = (x0 - 120 * math.cos(math.radians(160 + ang)), y0 + 120 * math.sin(math.radians(160 + ang)) * -0.2 + 40)
            ch._limb(c, [(x0, y0), (x0 - 90 - j * 12, y0 - 60 + ang), (x0 - 200 - j * 12, y0 - 20 + ang * 1.8)], 0.36 * R, ch.INK, 1.0)


def page_rip(c, img_old, k):
    """The old scene tears down the middle and both halves fall away."""
    n = 18
    xs = [W / 2 + (38 if j % 2 else -38) * (1 if j % 3 else 0.5) for j in range(n + 1)]
    ys = [H * j / n for j in range(n + 1)]
    for side in (-1, 1):
        path = skia.Path()
        if side < 0:
            path.moveTo(-10, -10)
            for x, y in zip(xs, ys):
                path.lineTo(x, y)
            path.lineTo(-10, H + 10)
        else:
            path.moveTo(W + 10, -10)
            for x, y in zip(xs, ys):
                path.lineTo(x, y)
            path.lineTo(W + 10, H + 10)
        path.close()
        c.save()
        c.translate(side * 900 * ease(k), 400 * k * k)
        c.rotate(side * 14 * k)
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        c.drawImage(img_old, 0, 0)
        c.restore()
        edge = skia.Path()
        edge.moveTo(xs[0] + side * 900 * ease(k), ys[0] + 400 * k * k)
        for x, y in zip(xs[1:], ys[1:]):
            edge.lineTo(x + side * 900 * ease(k), y + 400 * k * k)
        c.drawPath(edge, mg.stroke("#F4F1EA", 5, 0.9))


# ---------------------------------------------------------------- the reel
def scene1(c, t):
    ground_day(c)
    sign(c, 1320, 560)
    p = P(820, face="smug", arms=[(-14, -8), (150, -70)], hat=dict(tilt=10))
    ch.draw(c, p, 1.0, glint=clamp(1 - abs(t - 0.9) / 0.2))
    if T_LINE <= t < T_NUKE:
        caption(c, "we'll be fine here.")


def scene_after(c, t):
    smoke_sky(c, t)
    fall = ease(seg(t, T_FALL, T_FALL + 0.35))
    blink = (T_AFTER + 0.55 < t < T_AFTER + 0.68) or (T_AFTER + 1.0 < t < T_AFTER + 1.12)
    p = P(W / 2, face="blink" if blink else "shock", arms=[(-8, -2), (8, 2)], legs=[(-4, 0), (4, 0)])
    c.save()
    c.translate(W / 2, FLOOR)
    c.rotate(-88 * fall)
    c.translate(-W / 2, -FLOOR)
    ch.draw(c, p, 1.0, skin=ch.SOOT)
    c.restore()
    for j in range(3):                                            # smoke off the hat
        u = ((t - T_AFTER) * 0.7 + j * 0.33) % 1.0
        hx = W / 2 + 20 * math.sin(u * 6 + j)
        hy = FLOOR - LEG - 5.5 * R - 160 * u
        if fall < 0.1:
            c.drawCircle(hx, hy, 16 + 26 * u, mg.fill("#3A3A3D", 0.7 * (1 - u)))
    if T_FUCK <= t < T_FALL + 0.4:
        caption(c, "fuck.")


def scene_street(c, t):
    night_street(c)
    car(c, 520, FLOOR)
    door(c, 1480, legs_t=t if t >= T_BOX else None)
    if t < T_FIST:                                                # walks over, crouches, looks under
        kx = ease(seg(t, T_WALK, T_LOOK - 0.3))
        x = lerp(1250, 1000, kx)
        walk = math.sin(t * 12) * 22 if t < T_LOOK - 0.3 else 0
        crouch = ease(seg(t, T_LOOK - 0.3, T_LOOK))
        p = P(x, face="neutral" if crouch < 0.5 else "determined", lean=lerp(0, -58, crouch), head=lerp(0, -20, crouch),
              arms=[(-20 + walk, -10), (20 - walk, 10)] if crouch < 0.5 else [(-90, -20), (-70, -10)],
              legs=[(-walk, 0), (walk, 0)] if crouch < 0.5 else [(-30, 70), (30, 40)])
        p["root"] = (x, FLOOR - LEG + 60 * crouch)
        ch.draw(c, p, 1.0)
        if T_LOOK - 0.1 <= t < T_FIST:
            caption(c, "tin opener?")
    elif t < T_BOX:                                               # WHAM
        k = seg(t, T_FIST, T_FIST + 0.12)
        fx_ = lerp(760, 1060, ease(k))
        fist(c, fx_, FLOOR - 70, 1.0)
        u = seg(t, T_FIST + 0.1, T_BOX)
        x, y = lerp(1060, 1530, u), lerp(FLOOR - 250, FLOOR - 330, u) - math.sin(math.pi * u) * 380
        p = P(0, face="shock", arms=[(-150, 40), (150, -40)], legs=[(-60, 40), (60, -40)])
        p["root"] = (x, y)
        c.save(); c.translate(x, y); c.rotate(u * 540); c.translate(-x, -y)
        ch.draw(c, p, 1.0)
        c.restore()
        if k < 1:
            for j in range(10):                                   # impact lines
                a = j * math.pi / 5
                c.drawLine(1060 + math.cos(a) * 60, FLOOR - 120 + math.sin(a) * 60, 1060 + math.cos(a) * 140, FLOOR - 120 + math.sin(a) * 140, mg.stroke("#FFFFFF", 6, 1 - k))
    else:
        fist(c, 1060 - 900 * seg(t, T_BOX, T_BOX + 0.4), FLOOR - 70, 1.0, 1 - seg(t, T_BOX, T_BOX + 0.4))


def scene_oh(c, t):
    ground_day(c)
    z = 1 + 0.12 * ease(seg(t, T_OH, T_OH + 0.08))                # the punch-in
    p = P(W / 2, face="oh", arms=[(-40, -60), (40, 60)])
    hx, hy = ch.joints(p)["head"]
    c.save()
    c.translate(W / 2, H / 2 + 60); c.scale(3.2 * z, 3.2 * z); c.translate(-hx, -hy)
    ch.draw(c, p, 1.0)
    c.restore()


SNAP = {}


def frame(c, t):
    if t < T_NUKE:
        scene1(c, t)
    elif t < T_AFTER:
        k = seg(t, T_NUKE, T_AFTER)
        rng = np.random.default_rng(int(t * 1000))
        shake = rng.normal(0, 18 * (1 - k), 2)
        nuke(c, k, shake)
    elif t < T_RIP:
        scene_after(c, t)
    elif t < T_WALK:                                              # the page rip, back to white
        if "after" not in SNAP:
            s = skia.Surface(W, H); scene_after(s.getCanvas(), T_RIP - 0.01); SNAP["after"] = s.makeImageSnapshot()
        scene_street(c, T_WALK)
        page_rip(c, SNAP["after"], seg(t, T_RIP, T_WALK))
    elif t < T_OH:
        scene_street(c, t)
    elif t < T_END:
        scene_oh(c, t)
    else:
        c.clear(skia.ColorBLACK)
        f = mg.font(mg.MONO_M, 22)
        s = "BIG MAN · GAG REEL TEST · PLACEHOLDER VOICE"
        c.drawString(s, W / 2 - f.measureText(s) / 2, H / 2, f, mg.fill("#8A919C", seg(t, T_END + 0.2, T_END + 0.5)))


# ---------------------------------------------------------------- sound
def sounds():
    import voice_lab as vl
    n = int(DUR * SR)
    y = np.zeros(n, np.float32)
    rng = np.random.default_rng(7)

    def put(x, at, g=1.0):
        i = int(at * SR)
        j = min(n, i + len(x))
        if j > i:
            y[i:j] += (np.asarray(x[: j - i]) * g).astype(np.float32)

    def noise(d):
        return rng.standard_normal(int(d * SR))

    def env(d, a=0.005, r=0.1):
        tt = np.arange(int(d * SR)) / SR
        return np.minimum(1, tt / a) * np.exp(-tt / r)

    k = vl.engine()
    lines = [("We'll be fine here.", T_LINE, 1.0), ("Fuck.", T_FUCK, 1.0), ("Tin opener?", T_LOOK - 0.05, 1.0)]
    for txt, at, g in lines:
        v = vl.say(k, txt, "bm_george", speed=1.02, pause=0.1)
        put(v / (np.abs(v).max() + 1e-9) * 0.5, at, g)
    oh = vl.say(k, "Oh no.", "bm_george", speed=1.02, pause=0.05)
    oh = oh[: int(0.2 * SR)] * np.minimum(1, (0.2 - np.arange(int(0.2 * SR)) / SR) / 0.01)   # cut off mid-word
    put(oh / (np.abs(oh).max() + 1e-9) * 0.5, T_OH + 0.04)
    boom = noise(2.4) * env(2.4, 0.002, 0.7)
    boom = fx.bq(boom, "lp", 900)
    sub = np.sin(2 * np.pi * np.cumsum(np.linspace(60, 28, int(2.4 * SR))) / SR) * env(2.4, 0.002, 0.9)
    put(boom * 0.9 + sub * 0.9, T_NUKE)
    put(noise(0.08) * env(0.08, 0.001, 0.02) * 0.6, T_AFTER)                          # the hard cut click
    wind = fx.bq(noise(T_RIP - T_AFTER), "bp", 400, q=0.5) * 0.08
    put(wind, T_AFTER)
    for j in range(8):                                                                # crackle
        put(noise(0.01) * env(0.01, 0.0005, 0.003) * 0.3, T_AFTER + 0.2 + j * 0.31)
    thud = np.sin(2 * np.pi * 80 * np.arange(int(0.3 * SR)) / SR) * env(0.3, 0.002, 0.06)
    put(thud * 0.9, T_FALL + 0.35)
    rip = fx.bq(noise(0.45) * (0.5 + 0.5 * np.abs(np.sin(np.arange(int(0.45 * SR)) / SR * 90))), "hp", 1500) * env(0.45, 0.01, 0.3)
    put(rip * 0.6, T_RIP)
    for j in range(5):                                                                # footsteps
        put(fx.bq(noise(0.03), "bp", 900, q=2.0) * env(0.03, 0.001, 0.01) * 0.5, T_WALK + 0.1 + j * 0.24)
    whoosh = fx.bq(noise(0.35), "bp", 1200, q=0.8) * np.hanning(int(0.35 * SR))
    put(whoosh * 0.6, T_FIST - 0.12)
    punch = fx.bq(noise(0.2), "lp", 1500) * env(0.2, 0.001, 0.05) + np.sin(2 * np.pi * 110 * np.arange(int(0.2 * SR)) / SR) * env(0.2, 0.001, 0.06)
    put(punch * 1.0, T_FIST + 0.1)
    tt = np.arange(int(0.55 * SR)) / SR
    slide = np.sin(2 * np.pi * np.cumsum(900 * (1.8 ** (tt / 0.55))) / SR) * np.hanning(len(tt))
    put(slide * 0.25, T_FIST + 0.15)                                                  # flying away
    flap = fx.bq(noise(0.12), "bp", 2200, q=3.0) * env(0.12, 0.001, 0.03)
    put(flap * 0.7, T_BOX)
    put(flap * 0.5, T_BOX + 0.12)
    for j in range(6):                                                                # the kicking legs
        put(fx.bq(noise(0.02), "bp", 1500, q=2.0) * env(0.02, 0.001, 0.008) * 0.4, T_BOX + 0.3 + j * 0.19)
    zoom = fx.bq(noise(0.12), "hp", 3000) * env(0.12, 0.001, 0.04)
    put(zoom * 0.4, T_OH)
    return fx.norm_lufs(fx.stereo(y), -16.0)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mg.W, mg.H = W, H
    silent = os.path.join(OUT, "gag_silent.mp4")
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    for i in range(int(DUR * FPS)):
        c = surf.getCanvas()
        c.clear(skia.ColorBLACK)
        frame(c, i / FPS)
        proc.stdin.write(surf.makeImageSnapshot().tobytes())
    proc.stdin.close(); proc.wait()
    wav = os.path.join(OUT, "gag_sfx.wav")
    fx.save(wav, sounds(), mp3=False)
    final = os.path.join(OUT, "gag_reel.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    print("wrote", final)
