"""Stickman motion test (1920x1080, 8 s): idle, the emergency alert, the jump, the panic, the hat coming home,
then the title. Proves the rig moves and sets the cartoon sound palette for the WW3 video.

    python3 test_anim.py        # build/stickman_test.mp4
"""
import math
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import character as ch  # noqa: E402
from character import mg, skia  # noqa: E402
import audio_fx as fx  # noqa: E402

W, H, FPS, DUR = 1920, 1080, 30, 8.0
SR = fx.SR
OUT = os.path.join(HERE, "build")
X0, FLOOR = 760, 860                     # where he stands; the floor line


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    return clamp((t - a) / (b - a))


def ease(x):
    return x * x * (3 - 2 * x)


def back(x, s=1.7):                      # overshoot, for cartoon snaps
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def lerp(a, b, k):
    return a + (b - a) * k


def mix_pose(p, q, k):
    out = dict(p)
    for key in ("lean", "head"):
        out[key] = lerp(p.get(key, 0), q.get(key, 0), k)
    for key in ("arms", "legs"):
        out[key] = [(lerp(a[0], b[0], k), lerp(a[1], b[1], k)) for a, b in zip(p[key], q[key])]
    out["root"] = (lerp(p["root"][0], q["root"][0], k), lerp(p["root"][1], q["root"][1], k))
    out["face"] = q["face"] if k > 0.5 else p["face"]
    return out


R = 62
LEG = 3.6 * R                            # hip height above the feet when standing straight


def P(**kw):
    base = dict(R=R, lean=0, head=0, arms=[(-14, -8), (14, 8)], legs=[(-9, 2), (9, -2)], face="neutral",
                root=(X0, FLOOR - LEG), hat=dict(tilt=0))
    base.update(kw)
    return base


IDLE = P()
CROUCH = P(arms=[(-40, -30), (40, 30)], legs=[(-38, 76), (38, -76)], root=(X0, FLOOR - LEG + 70), face="panic")
AIR = P(arms=[(-150, -25), (150, 25)], legs=[(-30, 70), (30, -70)], root=(X0, FLOOR - LEG - 240), face="panic")
SMUG = P(lean=-3, head=8, arms=[(40, -120), (-40, 120)], legs=[(-6, 0), (14, -6)], face="smug", hat=dict(tilt=14))


def pose_at(t):
    if t < 2.2:                                                  # idle, breathing
        p = dict(IDLE)
        p["root"] = (X0, FLOOR - LEG + 3 * math.sin(t * 2.4))
        p["arms"] = [(-14 - 2 * math.sin(t * 2.4), -8), (14 + 2 * math.sin(t * 2.4), 8)]
        return p, True
    if t < 2.55:                                                 # the alert lands: he crouches
        return mix_pose(IDLE, CROUCH, ease(seg(t, 2.2, 2.55))), True
    if t < 2.95:                                                 # up
        return mix_pose(CROUCH, AIR, back(seg(t, 2.55, 2.95), 1.2)), False
    if t < 3.3:                                                  # down
        return mix_pose(AIR, CROUCH, ease(seg(t, 2.95, 3.3)) ** 2), False
    if t < 5.0:                                                  # panic on the spot
        u = t - 3.3
        k = ease(seg(t, 3.3, 3.6))
        p = mix_pose(CROUCH, P(face="panic"), k)
        p["arms"] = [(-128 + 34 * math.sin(u * 13), -45 + 20 * math.sin(u * 17)), (132 - 34 * math.sin(u * 13 + 1.2), 50 - 20 * math.sin(u * 15))]
        p["legs"] = [(-14 + 30 * math.sin(u * 16), 30 + 20 * math.sin(u * 16 + 0.5)), (14 - 30 * math.sin(u * 16), -30 - 20 * math.sin(u * 16 + 0.5))]
        p["root"] = (X0 + 6 * math.sin(u * 9), FLOOR - LEG + 18 - 16 * abs(math.sin(u * 16)))
        p["face"] = "panic"
        return p, False
    if t < 5.5:                                                  # bonk: the hat comes home, he freezes
        return P(face="panic", arms=[(-60, -20), (60, 20)]), True
    return mix_pose(P(face="panic", arms=[(-60, -20), (60, 20)]), SMUG, ease(seg(t, 5.5, 6.0))), True


def hat_flight(t, head):
    """Where the hat is while it's off his head: shot up, spinning, hanging, then dropping home."""
    hx, hy = head
    top = (X0 + 60, 150)
    if t < 2.7:
        return None
    if t < 3.4:
        k = back(seg(t, 2.7, 3.4), 0.8)
        return lerp(hx, top[0], k), lerp(hy - 0.6 * R, top[1], k), (t - 2.7) * 900
    if t < 4.6:
        u = t - 3.4
        return top[0] + 30 * math.sin(u * 3), top[1] + 12 * math.sin(u * 5), 630 + u * 520
    if t < 5.0:
        k = seg(t, 4.6, 5.0) ** 2
        return lerp(top[0], hx, k), lerp(top[1], hy - 0.42 * R, k), lerp(630 + 1.2 * 520, 1080, k)
    return None


def draw_frame(c, t):
    W0, H0 = mg.W, mg.H
    c.drawImage(GROUND, 0, 0)
    c.drawLine(120, FLOOR + 6, W - 120, FLOOR + 6, mg.stroke(ch.INK_SOFT, 2, 0.35))
    p, on_head = pose_at(t)
    hat = hat_flight(t, ch.joints(p)["head"])
    p = dict(p)
    p["hat"] = dict(p.get("hat", {}))
    if hat is not None or (2.7 <= t < 5.0):
        p["hat"]["a"] = 0.0
    squash = 0.0
    if 5.0 <= t < 5.35:                                          # the bonk
        squash = math.sin(math.pi * seg(t, 5.0, 5.35)) * 0.12
    c.save()
    c.translate(X0, FLOOR)
    c.scale(1 + squash, 1 - squash)
    c.translate(-X0, -FLOOR)
    glint = clamp(1 - abs(t - 1.3) / 0.25) if t < 2 else clamp(1 - abs(t - 7.2) / 0.3)
    J = ch.draw(c, p, 1.0, glint=glint)
    c.restore()
    if hat is not None:
        ch.hat(c, hat[0], hat[1], R, hat[2] % 360, 1.0)
    if 3.3 < t < 5.0:                                            # sweat
        for j, (dx, ph) in enumerate(((-110, 0.0), (120, 0.4), (-150, 0.8))):
            u = ((t - 3.3) * 1.6 + ph) % 1.0
            x, y = J["head"][0] + dx * (0.6 + 0.4 * u), J["head"][1] - 40 + 120 * u
            d = skia.Path(); d.moveTo(x, y - 18); d.quadTo(x + 12, y, x, y + 10); d.quadTo(x - 12, y, x, y - 18)
            c.drawPath(d, mg.fill(ch.GLOW, 0.9 * (1 - u)))
    if 5.0 <= t < 5.8:                                           # stars
        k = seg(t, 5.0, 5.8)
        for j in range(4):
            a = t * 6 + j * math.pi / 2
            x, y = J["head"][0] + math.cos(a) * 95, J["head"][1] - 70 + math.sin(a) * 26
            c.drawCircle(x, y, 7 * (1 - k) + 2, mg.fill(ch.GLOW, 1 - k))
    # the alert card
    ka = ease(seg(t, 2.1, 2.35)) * (1 - ease(seg(t, 4.8, 5.2)))
    if ka > 0:
        x, y = W - 560 + (1 - ka) * 160, 120
        mg.glass(c, x, y, 460, 150, 18, ka)
        pulse = 0.6 + 0.4 * abs(math.sin(t * 9))
        c.drawCircle(x + 56, y + 75, 26, mg.fill(ch.DANGER, ka * pulse))
        c.drawString("!", x + 49, y + 88, mg.font(mg.DISPLAY, 34), mg.fill("#15181C", ka))
        c.drawString("EMERGENCY ALERT", x + 102, y + 68, mg.font(mg.MONO_M, 26), mg.fill(ch.INK, ka))
        c.drawString("SEVERE ALERT · HYPOTHETICAL", x + 102, y + 104, mg.font(mg.MONO, 17), mg.fill(ch.DANGER, ka))
    # the title
    kt = seg(t, 6.2, 6.45)
    if kt > 0:
        s = lerp(1.6, 1.0, back(kt, 1.4))
        c.save()
        c.translate(1400, 520)
        c.scale(s, s)
        f = mg.font(mg.DISPLAY, 58)
        for j, (line, col) in enumerate((("HOW TO SURVIVE", ch.INK), ("WW3", ch.TURQ))):
            fs = mg.font(mg.DISPLAY, 58 if j == 0 else 150)
            c.drawString(line, -fs.measureText(line) / 2, j * 150, fs, mg.fill(col, min(1, kt * 3)))
        f2 = mg.font(mg.MONO_M, 26)
        c.drawString("(HYPOTHETICALLY)", -f2.measureText("(HYPOTHETICALLY)") / 2, 220, f2, mg.fill(ch.GLOW, min(1, kt * 3)))
        c.restore()


def sounds():
    """Cartoon palette, synthesised: alert, jump zip, slide whistle up and down, scramble, bonk, stamp."""
    n = int(DUR * SR)
    y = np.zeros(n, np.float32)
    rng = np.random.default_rng(4)

    def put(x, at, g=1.0):
        i = int(at * SR)
        j = min(n, i + len(x))
        y[i:j] += (x[: j - i] * g).astype(np.float32)

    def tone(f, dur, a=0.004, r=0.08):
        tt = np.arange(int(dur * SR)) / SR
        e = np.minimum(1, tt / a) * np.minimum(1, (dur - tt) / r)
        return np.sin(2 * np.pi * np.cumsum(np.full(len(tt), f)) / SR) * e

    def glide(f0, f1, dur, vib=0.0):
        tt = np.arange(int(dur * SR)) / SR
        f = f0 * (f1 / f0) ** (tt / dur) * (1 + vib * np.sin(2 * np.pi * 7 * tt))
        e = np.minimum(1, tt / 0.01) * np.minimum(1, (dur - tt) / 0.05)
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * e

    for k in range(6):                                           # the alert: two tones, twice
        put(tone(880 if k % 2 == 0 else 1175, 0.16) * 0.5, 2.15 + k * 0.17)
    zip_ = rng.standard_normal(int(0.25 * SR)) * np.linspace(0, 1, int(0.25 * SR)) ** 2
    zip_ = fx.bq(zip_, "bp", 2400, q=1.4)
    put(zip_ * 0.8, 2.55)
    put(glide(300, 1500, 0.65, 0.01) * 0.35, 2.72)               # slide whistle up with the hat
    for k in range(28):                                          # the scramble
        tk = 3.35 + k * 0.058
        click = rng.standard_normal(int(0.02 * SR)) * np.exp(-np.arange(int(0.02 * SR)) / (0.004 * SR))
        put(fx.bq(click, "bp", 1800 + 400 * (k % 3), q=2.0) * 0.5, tk)
    put(glide(1500, 260, 0.42, 0.012) * 0.35, 4.6)               # and down again
    wood = sum(np.sin(2 * np.pi * f * np.arange(int(0.25 * SR)) / SR) * np.exp(-np.arange(int(0.25 * SR)) / (d * SR)) * a
               for f, d, a in ((520, 0.05, 1.0), (1230, 0.03, 0.5), (2710, 0.015, 0.3)))
    put(wood * 0.9, 5.0)                                         # bonk
    put(glide(900, 1400, 0.5, 0.03) * 0.12, 5.05)                # the stars
    thump = np.sin(2 * np.pi * 70 * np.arange(int(0.4 * SR)) / SR) * np.exp(-np.arange(int(0.4 * SR)) / (0.09 * SR))
    put(thump * 0.9, 6.2)                                        # title stamp
    put(fx.bq(rng.standard_normal(int(0.2 * SR)) * np.exp(-np.arange(int(0.2 * SR)) / (0.03 * SR)), "hp", 2500) * 0.3, 6.2)
    y = fx.stereo(y) if hasattr(fx, "stereo") else np.stack([y, y], 1)
    return fx.norm_lufs(y, -16.0) if hasattr(fx, "norm_lufs") else y


GROUND = None

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mg.W, mg.H = W, H
    GROUND = mg.marl(mg.DARK, 2, 2.4)
    silent = os.path.join(OUT, "stickman_silent.mp4")
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    for i in range(int(DUR * FPS)):
        c = surf.getCanvas()
        c.clear(skia.ColorBLACK)
        draw_frame(c, i / FPS)
        proc.stdin.write(surf.makeImageSnapshot().tobytes())
    proc.stdin.close(); proc.wait()
    wav = os.path.join(OUT, "stickman_sfx.wav")
    fx.save(wav, sounds(), mp3=False)
    final = os.path.join(OUT, "stickman_test.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    print("wrote", final)
