"""The stickman in the chrome hat: a small 2D rig (forward kinematics), faces, and the hat, drawn with skia.

Poses are plain dicts so animation can interpolate them:
    root (x, y)      hip position in pixels
    R                head radius in pixels (everything scales from it)
    lean             spine angle from vertical, degrees (+ = leaning right)
    head             head tilt, degrees
    arms             [(shoulder, elbow), (shoulder, elbow)] for left/right, degrees; 0 = hanging straight down
    legs             [(hip, knee), (hip, knee)], degrees; 0 = straight down
    face             neutral | panic | determined | smug | serious
    hat              dict(tilt=deg, lift=R units above the head, dx=R units, a=alpha)

    python3 character.py        # build/concept_sheet.png (+ .jpg)
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.join(HERE, "..", "..", "a01_v6")
sys.path.insert(0, V6)
os.environ.setdefault("A01V6_FONTS", os.path.join(V6, "fonts"))
import mograph as mg  # noqa: E402
import skia  # noqa: E402

INK, INK_MID, INK_SOFT = mg.ON_DARK, mg.ON_DARK_MID, mg.ON_DARK_SOFT
TURQ, GLOW = mg.TURQ, mg.TURQ_GLOW
DANGER = "#FF8A3D"
HEAD_FILL = "#16181C"


def _rad(d):
    return math.radians(d)


def _dir(deg):
    """Unit vector for an angle measured from straight down, positive = towards +x."""
    a = _rad(deg)
    return np.array([math.sin(a), math.cos(a)])


def joints(p):
    """Forward kinematics: returns a dict of joint positions in pixels."""
    R = p["R"]
    hip = np.array(p["root"], float)
    up = -_dir(p.get("lean", 0.0))                       # spine points up
    shoulder = hip + up * 2.6 * R
    neck_top = shoulder + up * 0.45 * R
    head = neck_top + _dir(180 + p.get("lean", 0.0) + p.get("head", 0.0)) * 1.0 * R
    J = dict(hip=hip, shoulder=shoulder, neck=neck_top, head=head)
    for side, (s_ang, e_ang) in zip(("l", "r"), p.get("arms", [(-15, -10), (15, 10)])):
        base = p.get("lean", 0.0)
        elbow = shoulder + _dir(base + s_ang) * 1.45 * R
        hand = elbow + _dir(base + s_ang + e_ang) * 1.35 * R
        J["elbow_" + side], J["hand_" + side] = elbow, hand
    for side, (h_ang, k_ang) in zip(("l", "r"), p.get("legs", [(-8, 0), (8, 0)])):
        knee = hip + _dir(h_ang) * 1.8 * R
        foot = knee + _dir(h_ang + k_ang) * 1.8 * R
        J["knee_" + side], J["foot_" + side] = knee, foot
    return J


def _limb(c, pts, w, col, a):
    path = skia.Path()
    path.moveTo(*pts[0])
    for q in pts[1:]:
        path.lineTo(*q)
    paint = mg.stroke(col, w, a)
    paint.setStrokeCap(skia.Paint.kRound_Cap)
    paint.setStrokeJoin(skia.Paint.kRound_Join)
    c.drawPath(path, paint)


def hat(c, cx, cy, R, tilt=0.0, a=1.0, glint=0.0, soot=False):
    """The chrome conical hat. (cx, cy) is the centre of the brim; tilt in degrees. soot=True: blackened."""
    c.save()
    c.translate(cx, cy)
    c.rotate(tilt)
    w, h = 3.5 * R, 1.3 * R
    under = skia.Path()
    under.addOval(skia.Rect.MakeXYWH(-w / 2, -0.2 * R, w, 0.42 * R))
    c.drawPath(under, mg.fill("#0C0D10", 0.95 * a))
    cone = skia.Path()
    cone.moveTo(0, -h)
    cone.lineTo(w / 2, 0)
    cone.quadTo(0, 0.28 * R, -w / 2, 0)
    cone.close()
    cols = ["#1F242B", "#5E6772", "#E4E8EC", "#FFFFFF", "#A7AFBA", "#1F242B", "#9FE9E2", "#EEF2F5", "#5E6772"]
    if soot:
        cols = ["#0B0B0C", "#1A1A1C", "#2C2C2F", "#3A3A3D", "#1E1E20", "#0B0B0C", "#252527", "#303033", "#151517"]
    pos = [0.0, 0.14, 0.30, 0.36, 0.46, 0.60, 0.76, 0.88, 1.0]
    sh = skia.GradientShader.MakeLinear([(-w / 2, -h), (w / 2, 0.2 * R)], [mg.hexc(x, a) for x in cols], pos)
    fp = skia.Paint(AntiAlias=True)
    fp.setShader(sh)
    c.drawPath(cone, fp)
    c.drawPath(cone, mg.stroke("#0C0D10", 0.08 * R, 0.9 * a))
    for k in range(1, 4):                                   # the weave, pressed into the chrome
        t = k / 4
        c.drawLine(-w / 2 * t * 0.98, -h * (1 - t), w / 2 * t * 0.98, -h * (1 - t), mg.stroke("#FFFFFF", 0.03 * R, 0.18 * a))
    c.drawLine(-0.12 * R, -h * 0.92, -w * 0.30, -0.08 * R, mg.stroke("#FFFFFF", 0.07 * R, 0.75 * a))      # the specular streak
    rim = mg.stroke(GLOW, 0.06 * R, (0.55 + 0.45 * glint) * a)
    rp = skia.Path()
    rp.moveTo(-w / 2, 0)
    rp.quadTo(0, 0.28 * R, w / 2, 0)
    c.drawPath(rp, rim)
    if glint > 0:
        g = mg.fill("#FFFFFF", glint * a)
        g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 0.12 * R))
        c.drawCircle(-0.1 * R, -h * 0.9, 0.16 * R, g)
    c.restore()


def face(c, cx, cy, R, kind, a=1.0, tilt=0.0, col=None, bg=None):
    INK, HEAD_FILL = col or globals()["INK"], bg or globals()["HEAD_FILL"]
    c.save()
    c.translate(cx, cy)
    c.rotate(tilt)
    ink = mg.fill(INK, a)
    ln = lambda x0, y0, x1, y1, w=0.1: _limb(c, [(x0 * R, y0 * R), (x1 * R, y1 * R)], w * R, INK, a)
    ey, ex = 0.12, 0.36
    if kind == "blink":
        for s_ in (-1, 1):
            ln(s_ * 0.24, ey, s_ * 0.48, ey, 0.08)
        ln(-0.14, 0.5, 0.14, 0.5, 0.07)
    elif kind == "shock":
        for s_ in (-1, 1):
            c.drawCircle(s_ * ex * R, ey * R, 0.06 * R, ink)
        c.drawCircle(0, 0.5 * R, 0.1 * R, mg.stroke(INK, 0.06 * R, a))
    elif kind == "oh":
        for s_ in (-1, 1):
            c.drawCircle(s_ * ex * R, ey * R, 0.14 * R, ink)
        c.drawOval(skia.Rect.MakeXYWH(-0.12 * R, 0.38 * R, 0.24 * R, 0.3 * R), mg.stroke(INK, 0.07 * R, a))
    elif kind == "neutral":
        for s in (-1, 1):
            c.drawCircle(s * ex * R, ey * R, 0.1 * R, ink)
        ln(-0.16, 0.5, 0.16, 0.5, 0.07)
    elif kind == "panic":
        for s in (-1, 1):
            c.drawCircle(s * ex * R, ey * R, 0.24 * R, mg.fill(INK, a))
            c.drawCircle(s * ex * R + 0.02 * R, ey * R + 0.03 * R, 0.07 * R, mg.fill(HEAD_FILL, a))
        c.drawOval(skia.Rect.MakeXYWH(-0.14 * R, 0.4 * R, 0.28 * R, 0.36 * R), mg.fill(INK, a))
        c.drawOval(skia.Rect.MakeXYWH(-0.08 * R, 0.5 * R, 0.16 * R, 0.2 * R), mg.fill(HEAD_FILL, a))
    elif kind == "determined":
        for s in (-1, 1):
            c.drawCircle(s * ex * R, ey * R + 0.04 * R, 0.1 * R, ink)
            ln(s * 0.18, -0.12, s * 0.52, -0.02, 0.08)
        ln(-0.14, 0.52, 0.14, 0.48, 0.07)
    elif kind == "smug":
        c.drawCircle(ex * R, ey * R, 0.1 * R, ink)
        arc = skia.Path(); arc.addArc(skia.Rect.MakeXYWH(-ex * R - 0.14 * R, ey * R - 0.1 * R, 0.28 * R, 0.2 * R), 200, 140)
        c.drawPath(arc, mg.stroke(INK, 0.08 * R, a))
        ln(0.2, -0.2, 0.52, -0.3, 0.07)                                     # one brow up
        sm = skia.Path()
        sm.moveTo(-0.34 * R, 0.42 * R)
        sm.quadTo(0.02 * R, 0.66 * R, 0.4 * R, 0.34 * R)                     # a lopsided smirk, pulled up on one side
        _p = mg.stroke(INK, 0.08 * R, a); _p.setStrokeCap(skia.Paint.kRound_Cap)
        c.drawPath(sm, _p)
        ln(0.4, 0.34, 0.47, 0.26, 0.06)
    elif kind == "serious":
        for s in (-1, 1):
            ln(s * 0.22, ey + 0.02, s * 0.5, ey - 0.02, 0.09)
        ln(-0.2, 0.52, 0.2, 0.52, 0.08)
    c.restore()


SOOT = dict(line="#17181B", back="#111214", head="#0E0F11", face="#F4F5F7")


def draw(c, p, a=1.0, glint=0.0, skin=None):
    """Draw one pose: limbs, the head (filled so it hides what's behind), the face, the hat.
    skin = dict(line, back, head, face) recolours him (SOOT after an explosion)."""
    sk = skin or {}
    line, backc, head_fill, face_col = sk.get("line", INK), sk.get("back", INK_MID), sk.get("head", HEAD_FILL), sk.get("face", INK)
    R = p["R"]
    J = joints(p)
    w = 0.34 * R
    back, front = ("l", "r")
    _limb(c, [J["hip"], J["knee_" + back], J["foot_" + back]], w, backc, a)
    _limb(c, [J["shoulder"], J["elbow_" + back], J["hand_" + back]], w, backc, a)
    _limb(c, [J["hip"], J["shoulder"], J["neck"]], w, line, a)
    _limb(c, [J["hip"], J["knee_" + front], J["foot_" + front]], w, line, a)
    _limb(c, [J["shoulder"], J["elbow_" + front], J["hand_" + front]], w, line, a)
    hx, hy = J["head"]
    c.drawCircle(hx, hy, R, mg.fill(head_fill, a))
    c.drawCircle(hx, hy, R, mg.stroke(line, w * 0.85, a))
    tilt = p.get("lean", 0.0) + p.get("head", 0.0)
    face(c, hx, hy, R, p.get("face", "neutral"), a, tilt, col=face_col, bg=head_fill)
    hp = p.get("hat", {})
    ha = hp.get("a", 1.0)
    if ha > 0:
        ang = _rad(tilt)
        up = np.array([math.sin(ang), -math.cos(ang)])
        rt = np.array([math.cos(ang), math.sin(ang)])
        base = np.array([hx, hy]) + up * (0.42 * R + hp.get("lift", 0.0) * R) + rt * hp.get("dx", 0.0) * R
        hat(c, base[0], base[1], R, tilt + hp.get("tilt", 0.0), a * ha, glint, soot=bool(skin))
    return J


# ---------------------------------------------------------------- the concept sheet
POSES = {
    "idle": dict(R=46, lean=0, head=0, arms=[(-14, -8), (14, 8)], legs=[(-9, 2), (9, -2)], face="neutral", hat=dict(tilt=0)),
    "panic": dict(R=46, lean=-4, head=-6, arms=[(-128, -45), (132, 50)], legs=[(-26, 12), (24, -14)], face="panic",
                  hat=dict(tilt=-38, lift=2.3, dx=0.8)),
    "run": dict(R=46, lean=24, head=-10, arms=[(-60, -70), (70, 80)], legs=[(-50, 60), (55, -10)], face="determined", hat=dict(tilt=-22, lift=0.25)),
    "smug": dict(R=46, lean=-3, head=6, arms=[(40, -120), (-40, 120)], legs=[(-6, 0), (14, -6)], face="smug", hat=dict(tilt=14)),
}


def _label(c, s, x, y, col=INK_SOFT, size=18):
    f = mg.font(mg.MONO_M, size)
    c.drawString(s, x - f.measureText(s) / 2, y, f, mg.fill(col, 1.0))


def sheet(out):
    W, H = 1920, 1080
    surf = skia.Surface(W, H)
    c = surf.getCanvas()
    W0, H0 = mg.W, mg.H
    mg.W, mg.H = W, H
    try:
        c.drawImage(mg.marl(mg.DARK, 2, 2.4), 0, 0)
    finally:
        mg.W, mg.H = W0, H0
    f = mg.font(mg.DISPLAY, 38)
    c.drawString("THE STICKMAN", 80, 110, f, mg.fill(INK, 1.0))
    _label(c, "CONCEPT 0.1 · CHROME HAT · CAN'T DIE · NEVER SPEAKS", 80 + 330, 150, TURQ, 18)
    xs = [260, 640, 1030, 1400]
    base_y = 720
    labels = ["IDLE", "PANIC", "LOONEY RUN", "SMUG (OUR OWN FACE)"]
    for (name, p), x, lab in zip(POSES.items(), xs, labels):
        q = dict(p); q["root"] = (x, base_y)
        if name == "run":                                         # the wheel of legs and the dust
            for k in range(5):
                qq = dict(q); ang = k * 72
                qq["legs"] = [(-60 + ang * 0.3, 40), (60 - ang * 0.3, -30)]
                J = joints(qq)
                _limb(c, [J["hip"], J["knee_l"], J["foot_l"]], 0.3 * q["R"], INK_SOFT, 0.18)
            ring = mg.stroke(INK_SOFT, 3, 0.35)
            c.drawOval(skia.Rect.MakeXYWH(x - 120, base_y + 30, 220, 150), ring)
            for k in range(4):
                c.drawCircle(x - 150 - k * 34, base_y + 160 - k * 10, 22 - k * 4, mg.stroke(INK_SOFT, 3, 0.5 - k * 0.1))
            for k in range(3):
                c.drawLine(x - 200, base_y - 110 - k * 40, x - 120, base_y - 110 - k * 40, mg.stroke(INK_SOFT, 3, 0.4))
        if name == "panic":
            for dx, dy in ((-100, -200), (110, -230), (-130, -120)):
                d = skia.Path(); d.moveTo(x + dx, base_y + dy - 18); d.quadTo(x + dx + 12, base_y + dy, x + dx, base_y + dy + 10)
                d.quadTo(x + dx - 12, base_y + dy, x + dx, base_y + dy - 18)
                c.drawPath(d, mg.fill(GLOW, 0.9))
            for k in range(3):
                a0 = -60 - k * 25
                c.drawLine(x + 160 * math.cos(_rad(a0)), base_y - 260 + 160 * math.sin(_rad(a0)),
                           x + 200 * math.cos(_rad(a0)), base_y - 260 + 200 * math.sin(_rad(a0)), mg.stroke(INK, 4, 0.6))
        draw(c, q, 1.0, glint=0.6 if name == "idle" else 0.0)
        _label(c, lab, x, 930)
    # the serious close-up, in its own frame
    fx0, fy0, fw, fh = 1570, 250, 290, 560
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(fx0, fy0, fw, fh))
    c.drawRect(skia.Rect.MakeXYWH(fx0, fy0, fw, fh), mg.fill("#0B0C0E", 1.0))
    R = 110
    hx, hy = fx0 + fw / 2, fy0 + 330
    c.drawLine(hx, hy + R, hx, fy0 + fh, mg.stroke(INK, 0.34 * R, 1.0))
    rim = mg.stroke(GLOW, 16, 0.5)
    rim.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    arcp = skia.Path(); arcp.addArc(skia.Rect.MakeXYWH(hx - R, hy - R, 2 * R, 2 * R), -70, 140)
    c.drawPath(arcp, rim)
    c.drawCircle(hx, hy, R, mg.fill(HEAD_FILL, 1.0))
    c.drawCircle(hx, hy, R, mg.stroke(INK, 0.3 * R, 1.0))
    face(c, hx, hy, R, "serious", 1.0)
    shade = skia.Paint(AntiAlias=True)
    shade.setShader(skia.GradientShader.MakeLinear([(0, hy - R), (0, hy + 0.1 * R)], [skia.Color4f(0, 0, 0, 0.85), skia.Color4f(0, 0, 0, 0.0)]))
    c.drawCircle(hx, hy, R * 0.97, shade)
    hat(c, hx, hy - 0.42 * R, R, -4, 1.0, glint=0.3)
    vg = skia.Paint(AntiAlias=True)
    vg.setShader(skia.GradientShader.MakeRadial((hx, hy), fh * 0.7, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0.75)], [0.45, 1.0]))
    c.drawRect(skia.Rect.MakeXYWH(fx0, fy0, fw, fh), vg)
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(fx0, fy0, fw, fh), mg.stroke(INK_SOFT, 1.5, 0.6))
    _label(c, "SERIOUS CLOSE-UP", fx0 + fw / 2, 930)
    # swatches
    for k, (col, name) in enumerate(((INK, "LINE"), ("#16181C", "HEAD"), (TURQ, "BRAND"), ("#E4E8EC", "CHROME"), (DANGER, "DANGER"))):
        x = 80 + k * 150
        c.drawRoundRect(skia.Rect.MakeXYWH(x, 985, 40, 40), 8, 8, mg.fill(col, 1.0))
        c.drawRoundRect(skia.Rect.MakeXYWH(x, 985, 40, 40), 8, 8, mg.stroke(INK_SOFT, 1.2, 0.6))
        c.drawString(name, x + 52, 1012, mg.font(mg.MONO_M, 15), mg.fill(INK_SOFT, 1.0))
    surf.makeImageSnapshot().save(out + ".png", skia.kPNG)       # skia writes PNG in the right channel order
    from PIL import Image
    Image.open(out + ".png").convert("RGB").save(out + ".jpg", quality=88)


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    sheet(os.path.join(HERE, "build", "concept_sheet"))
    print("wrote build/concept_sheet.png")
