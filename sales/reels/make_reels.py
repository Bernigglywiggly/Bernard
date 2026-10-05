#!/usr/bin/env python3
"""Walk-in demo Reels (Kitchen Pass): a 10 s, 9:16 Reel made for one shop from its public food hygiene record, to
show on the phone when walking in and to hand over free ("it's yours, post it tonight").

The Reel is a kitchen order ticket hanging from the pass rail under a heat lamp: the shop's name (frame 0), a "rated
5" rubber stamp with the inspection month, a pen circle, then "find us" with the street, then a pull back to the whole
ticket and the service bell. Our own design, never the FSA's badge artwork, and no AI food photos: every word on it
comes from the FSA register (Open Government Licence) via sales/prospects_routed.json. Sound is synthesised (printer,
stamp, pen, pin, service bell, room tone); no music, so the owner can add a trending sound in the app.

    python3 sales/reels/make_reels.py stills [ids...]      # key frames per shop -> build/stills/<order>_<slug>.jpg
    python3 sales/reels/make_reels.py render [ids...]      # default: every FSA-5 shop in Stone, in walking order
    python3 sales/reels/make_reels.py render --town Tamworth
    python3 sales/reels/make_reels.py render --sample special   # a sample of the monthly product (SAMPLES)
"""
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
import skia
from scipy import ndimage, signal

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "lab"))
import audio_fx as AX  # noqa: E402

BUILD = os.path.join(HERE, "build")
W, H, FPS, DUR = 1080, 1920, 30, 8.0
SR = AX.SR
FONT_DIRS = [os.path.join(REPO, d) for d in ("lab/shorts/fonts", "a01_v6/fonts", "lab/motion/public/fonts", "lab/ch2/fonts")]

PAPER, PAPER_EDGE, INK, INK2, INK3 = "#F6F2E9", "#E6DFD1", "#1C1D20", "#4E5258", "#8A8E93"
GREEN, RED, AMBER = "#1E7445", "#C0392B", "#FFB15A"
TW, PX = 900, 58                      # ticket width and side margin, world px
STOP = {"OF", "THE", "AND", "&", "IN", "DI", "DE", "LA", "AT", "ON", "A"}
MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()

# The timeline (seconds). Hook = name at frame 0; something new every 1-3 s; the camera rides one ticket throughout.
# Name and the rating line are printed at frame 0 (t = -1); the stamp lands at 1.1 s, inside the 3 s hook.
T_RULE, T_RATE1, T_RATE2, T_RATE3 = -1, -1, 0.25, 0.45
T_STAMP, T_PEN, T_RULE3 = 1.10, 2.05, 2.60
T_FIND, T_PRE, T_STREET, T_TOWN, T_PIN, T_RULE4, T_SRC1, T_SRC2 = 3.45, 3.62, 3.75, 4.05, 4.45, 4.60, 4.85, 5.00
T_THANKS = 6.55
PRINT = 0.14                          # a line prints top to bottom in this long


# ---------------------------------------------------------------- drawing helpers
_TF = {}


def font(name, size):
    if name not in _TF:
        path = next(os.path.join(d, name + ".ttf") for d in FONT_DIRS if os.path.exists(os.path.join(d, name + ".ttf")))
        _TF[name] = skia.Typeface.MakeFromFile(path)
    f = skia.Font(_TF[name], size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def anton(size):
    return font("Anton-Regular", size)


def mono(size):
    return font("IBMPlexMono-500", size)


def col(hexs, a=1.0):
    h = hexs.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * max(0.0, min(1.0, a))))


def fill(hexs, a=1.0):
    return skia.Paint(Color=col(hexs, a), AntiAlias=True)


def stroke(hexs, w, a=1.0):
    return skia.Paint(Color=col(hexs, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def spring(p, zeta=0.72, w=11.0):
    """Step response of a damped spring: fast away, a small overshoot, a slow landing."""
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    wd = w * math.sqrt(1 - zeta * zeta)
    return 1 - math.exp(-zeta * w * p) * (math.cos(wd * p) + zeta * w / wd * math.sin(wd * p))


def ease_out(p):
    p = clamp(p)
    return 1 - (1 - p) ** 3


def lerp(a, b, e):
    return tuple(x + (y - x) * e for x, y in zip(a, b))


# ---------------------------------------------------------------- the shop's ticket
def clean_name(name):
    n = name.replace("’", "'").strip()
    n = re.sub(r"\s+(ltd\.?|limited)$", "", n, flags=re.I)
    return re.sub(r"\s+", " ", n).upper()


def fit_name(name, maxw=TW - 2 * PX, max_size=300.0, max_h=600.0):
    """Split the name over 1-3 lines and pick the biggest type; avoid lines that end on 'OF', 'THE', '&'."""
    f100 = anton(100)
    if " / " in name:                                   # two names in one shop: one per line, the slash kept on the first
        parts = [x.strip() for x in name.split(" / ")]
        lines = [x + " /" for x in parts[:-1]] + parts[-1:]
        size = min(max_size, maxw / (max(f100.measureText(ln) for ln in lines) / 100))
        block = len(lines) * 0.859 * size + (len(lines) - 1) * 0.16 * size
        return (size * min(1.0, max_h / block)), lines
    words = name.split()
    best = None
    for n in range(1, min(3, len(words)) + 1):
        cuts = [()]
        for _ in range(n - 1):
            cuts = [c + (k,) for c in cuts for k in range((c[-1] + 1 if c else 1), len(words))]
        for cut in cuts:
            idx = (0,) + cut + (len(words),)
            lines = [" ".join(words[idx[i]:idx[i + 1]]).rstrip("/").strip() for i in range(n)]
            if any(not ln for ln in lines):
                continue
            wmax = max(f100.measureText(ln) for ln in lines) / 100
            size = min(max_size, maxw / wmax)
            block = n * 0.859 * size + (n - 1) * 0.16 * size
            if block > max_h:
                size *= max_h / block
            score = size * (1 - 0.06 * (n - 1))
            if any(ln.split()[-1] in STOP for ln in lines[:-1]) or lines[-1].split()[0] in STOP and n > 1 and len(lines[-1].split()) == 1:
                score *= 0.9
            if best is None or score > best[0] + 0.01:
                best = (score, size, lines)
    return best[1], best[2]


UNIT = re.compile(r"^(unit|units|shop|flat|suite)\b", re.I)


def split_address(shop):
    """(line above the street, the street, locality + town + postcode). The register spells towns several ways
    ("Newcastle Under Lyme"), may lead with the business's own name, and may add a locality after the street."""
    pc, town = shop["postcode"], shop["town"]
    norm = lambda x: re.sub(r"[^a-z]", "", x.lower())  # noqa: E731
    drop = {norm(pc), norm(town), "staffordshire", "staffs"}
    parts = [p.strip() for p in shop["address"].split(",") if p.strip() and norm(p) not in drop]
    words = lambda x: {w for w in re.findall(r"[a-z]+", x.lower()) if len(w) > 3}  # noqa: E731
    if len(parts) > 1 and not re.search(r"\d", parts[0]) and words(parts[0]) & words(shop["name"]):
        parts = parts[1:]                                  # "Walton Fish Bar, 5 Eccleshall Road"
    if not parts:
        return "", town.upper(), f"{town.upper()}  {pc}"
    num = [i for i, p in enumerate(parts) if re.search(r"\d", p) and not UNIT.match(p)]
    unit = [i for i, p in enumerate(parts) if UNIT.match(p)]
    k = num[-1] if num else (unit[-1] + 1 if unit and unit[-1] + 1 < len(parts) else len(parts) - 1)
    local = [p.upper() for p in parts[k + 1:]]
    return ", ".join(parts[:k]).upper(), parts[k].upper(), " · ".join(local + [town.upper()]) + f"  {pc}"


def inspected(d):
    y, m, _ = d.split("-")
    return f"INSPECTED {MONTHS[int(m) - 1]} {y}"


def rating_spec(shop):
    """The walk-in gift: the shop's own name, its 5 for food hygiene and its street, all from the FSA record."""
    pre, street, townpc = split_address(shop)
    return dict(header="ORDER UP", big=clean_name(shop["name"]), line=("1 x FOOD HYGIENE RATING", "5/5"),
                sub=("  TOP RATING  ·  VERY GOOD", "  " + inspected(shop["fsaDate"])),
                stamp=("5", "FOOD HYGIENE RATING  ·  VERY GOOD  ·  "), find="FIND US", pre=pre, street=street,
                townpc=townpc, src=("RATING: FOOD STANDARDS AGENCY", "RATINGS.FOOD.GOV.UK"))


# Samples of the monthly product (the owner's own specials). Shown as a format sample, never as a real shop.
SAMPLES = {
    "special": (dict(id="900001", order=0, town="Sample", name="Your Takeaway", address="", postcode="", fsaDate="2026-10-01"),
                dict(header="TONIGHT", big="CHICKEN TIKKA MASALA", line=("1 x TONIGHT'S SPECIAL", "£8.95"),
                     sub=("  WITH PILAU RICE AND A NAAN", "  WHILE IT LASTS"),
                     stamp=("£8.95", "TONIGHT'S SPECIAL  ·  TONIGHT ONLY  ·  "), find="ORDER", pre="CALL OR WALK IN",
                     street="YOUR TAKEAWAY", townpc="12 HIGH STREET", src=("", ""))),
}


class Ticket:
    """Every element on the ticket in world coordinates (x 0..TW, y down from the rail), with its print time."""

    def __init__(self, shop, spec=None):
        self.shop = shop
        sp = self.spec = spec or rating_spec(shop)
        self.els = []
        y = 0.0
        y += 86
        self.text(f"*  *  *   {sp['header']}   *  *  *", mono(30), TW / 2, y, INK, -1, align="center")
        y += 44
        self.rule(y, -1)
        # the name, as big as it will go
        size, lines = fit_name(sp["big"])
        cap = 0.859 * size
        y += 40
        top = y
        for ln in lines:
            y += cap
            self.text(ln, anton(size), PX - 2, y, INK, -1)
            y += 0.16 * size
        self.name_box = (top, y - 0.16 * size)
        y += 34
        self.rule(y, T_RULE)
        # the rating, as order lines
        y += 76
        f = mono(34)
        left, right = sp["line"]
        self.text(left, f, PX, y, INK, T_RATE1)
        rx = TW - PX
        self.text(right, mono(40), rx, y + 2, INK, T_RATE1, align="right")
        lw, rw = f.measureText(left), mono(40).measureText(right)
        dots = int((rx - rw - 14 - (PX + lw + 14)) / f.measureText("."))
        self.text("." * max(0, dots), f, PX + lw + 10, y, INK3, T_RATE1)
        self.five = (rx - rw, y - 0.70 * 40, rx, y + 2)
        y += 52
        self.text(sp["sub"][0], mono(28), PX, y, INK2, T_RATE2)
        y += 44
        self.text(sp["sub"][1], mono(28), PX, y, INK2, T_RATE3)
        self.rate_box = (self.five[1] - 30, y)
        # the stamp
        y += 40
        self.stamp_c = (TW / 2 + 50, y + 228)
        y += 466
        self.rule(y, T_RULE3)
        # find us
        y += 74
        self.text(sp["find"], mono(34), PX, y, INK, T_FIND)
        self.pin_at = (PX + mono(34).measureText(sp["find"]) + 44, y - 12)
        find_top = y - 30
        pre, street, townpc = sp["pre"], sp["street"], sp["townpc"]
        if pre:
            y += 52
            self.text(pre, mono(30), PX, y, INK2, T_PRE)
        ssize = min(150.0, (TW - 2 * PX) / (anton(100).measureText(street) / 100))
        y += 0.859 * ssize + 30
        self.text(street, anton(ssize), PX - 2, y, INK, T_STREET)
        y += 60
        self.text(townpc, mono(34), PX, y, INK, T_TOWN)
        self.find_box = (find_top, y)
        y += 46
        self.rule(y, T_RULE4)
        if sp["src"][0]:
            y += 52
            self.text(sp["src"][0], mono(22), PX, y, INK3, T_SRC1)
            y += 32
            self.text(sp["src"][1], mono(22), PX, y, INK3, T_SRC2)
        y += 82
        self.text("*  *  *   THANK YOU   *  *  *", mono(30), TW / 2, y, INK, T_THANKS, align="center")
        y += 70
        self.h = y
        self.grain = paper_grain(int(self.h), int(shop["id"]))
        self.ink = stamp_ink(int(shop["id"]))

    def text(self, s, f, x, y, colour, t, align="left"):
        w = f.measureText(s)
        x0 = x - (w if align == "right" else w / 2 if align == "center" else 0)
        m = f.getMetrics()
        self.els.append(dict(kind="text", s=s, f=f, x=x0, y=y, colour=colour, t=t,
                             box=(x0 - 4, y + m.fAscent * 0.86, x0 + w + 4, y + m.fDescent * 0.6)))

    def rule(self, y, t):
        self.els.append(dict(kind="rule", y=y, t=t, box=(PX, y - 3, TW - PX, y + 3)))


def paper_grain(h, seed):
    rng = np.random.default_rng(seed)
    g = ndimage.gaussian_filter(rng.normal(0, 1, (h // 3 + 1, TW // 3 + 1)), 0.7)
    a = np.clip(np.abs(g) * 7, 0, 16).astype(np.uint8)
    img = np.zeros(a.shape + (4,), np.uint8)
    img[..., 0:3] = 60
    img[..., 3] = a
    return skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType)


def stamp_ink(seed, size=440):
    """A rubber stamp never inks evenly: blotchy gaps plus speckle, used to erase bits of the impression."""
    rng = np.random.default_rng(seed + 1)
    blot = ndimage.gaussian_filter(rng.normal(0, 1, (size, size)), 9)
    blot = (blot - blot.min()) / (blot.max() - blot.min())
    speck = rng.random((size, size)) > 0.93
    a = np.clip((blot - 0.62) * 3.2, 0, 0.85) + speck * 0.55
    img = np.zeros((size, size, 4), np.uint8)
    img[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
    return skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType)


# ---------------------------------------------------------------- camera
def holds(T):
    """Camera holds (t0, t1, start state, end state); a spring carries the camera between them. State = cx, cy, z, roll."""
    yA = (T.name_box[0] + T.name_box[1]) / 2 + 150
    yB = (T.rate_box[0] + T.stamp_c[1]) / 2 + 70
    yC = (T.find_box[0] + T.find_box[1]) / 2 + 40
    zD = min(0.92, (H - 260) / (T.h + 140))
    yD = (T.h - 110) / 2 + 30
    return [
        (0.00, 0.55, (TW / 2, yA, 1.11, -0.6), (TW / 2, yA + 10, 1.13, -0.5)),
        (1.00, 2.85, (TW / 2 + 20, yB, 1.18, 0.5), (TW / 2 + 26, yB + 26, 1.27, 0.3)),
        (3.40, 5.55, (TW / 2 - 10, yC, 1.13, -0.3), (TW / 2 - 10, yC + 22, 1.19, -0.2)),
        (6.35, DUR, (TW / 2, yD, zD, 0.0), (TW / 2, yD - 10, zD * 1.04, 0.15)),
    ]


def camera(t, hs):
    for i, (t0, t1, s0, s1) in enumerate(hs):
        if t < t0:
            if i == 0:
                return s0
            pt1, ps1 = hs[i - 1][1], hs[i - 1][3]
            return lerp(ps1, s0, spring((t - pt1) / (t0 - pt1)))
        if t <= t1:
            p = (t - t0) / (t1 - t0)
            return lerp(s0, s1, 0.5 - 0.5 * math.cos(math.pi * p) if i == 0 else p)
    return hs[-1][3]


def shake(t):
    d = t - T_STAMP
    if d < 0 or d > 0.5:
        return 0.0, 0.0
    a = 11 * math.exp(-d * 9)
    return a * math.sin(2 * math.pi * 17 * d) * 0.6, a * math.sin(2 * math.pi * 23 * d + 1.3)


# ---------------------------------------------------------------- the scene
_BG = None


def background():
    """Dark brushed steel: horizontal streaks, a little warmer at the top where the heat lamp is."""
    global _BG
    if _BG is None:
        rng = np.random.default_rng(3)
        h2 = H + 900
        rows = ndimage.gaussian_filter1d(rng.normal(0, 1, h2), 1.2)
        streak = ndimage.gaussian_filter(rng.normal(0, 1, (h2, W)), (0.6, 40))
        v = 34 + rows[:, None] * 2.2 + streak * 9
        img = np.zeros((h2, W, 4), np.uint8)
        img[..., 0] = np.clip(v - 2, 0, 255)
        img[..., 1] = np.clip(v + 3, 0, 255)
        img[..., 2] = np.clip(v + 6, 0, 255)
        img[..., 3] = 255
        _BG = skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType)
    return _BG


def draw_rail(c):
    """The ticket rail on the pass: a brushed aluminium bar the ticket hangs from."""
    r = skia.Rect.MakeLTRB(-2000, -120, TW + 2000, 18)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([(0, -120), (0, 18)],
                                               [col("#9AA3A8"), col("#D9DEE0"), col("#7C858A"), col("#4A5156")],
                                               [0.0, 0.35, 0.8, 1.0]))
    c.drawRect(r, p)
    c.drawRect(skia.Rect.MakeLTRB(-2000, 6, TW + 2000, 18), fill("#2A2F33", 0.9))
    c.drawRect(skia.Rect.MakeLTRB(-2000, -120, TW + 2000, -114), fill("#EEF2F3", 0.6))
    for bx in (TW / 2 - 300, TW / 2 + 300):          # the ball bearings that grip the ticket
        c.drawCircle(bx, 2, 15, fill("#3B4247"))
        c.drawCircle(bx - 4, -3, 6, fill("#C8CFD2", 0.8))


def ticket_path(h):
    p = skia.Path()
    tooth = 22
    p.moveTo(0, -30)
    p.lineTo(TW, -30)
    p.lineTo(TW, h)
    n = int(TW / tooth)
    for i in range(n, 0, -1):
        p.lineTo(i * tooth - tooth / 2, h + 9)
        p.lineTo((i - 1) * tooth, h)
    p.close()
    return p


def draw_stamp(c, T, t):
    cx, cy = T.stamp_c
    R = 215.0
    if t < T_STAMP - 0.12:
        return
    if t < T_STAMP:                                   # the stamp coming down: a faint shadow tightens
        p = (t - (T_STAMP - 0.12)) / 0.12
        s = 1.35 - 0.35 * p * p
        sh = skia.Paint(Color=col("#000000", 0.13 * p), AntiAlias=True,
                        MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30 * (1.2 - p)))
        c.drawCircle(cx + 18 * (1 - p), cy + 26 * (1 - p), R * s, sh)
        return
    d = t - T_STAMP
    s = 1.0 + 0.07 * math.exp(-d * 16) * math.cos(d * 34)
    c.save()
    c.translate(cx, cy)
    c.rotate(-9)
    c.scale(s, s)
    c.saveLayer(None, None)
    ink = fill(GREEN, 0.92)
    c.drawCircle(0, 0, R, stroke(GREEN, 13, 0.92))
    c.drawCircle(0, 0, R - 64, stroke(GREEN, 4, 0.92))
    ring = T.spec["stamp"][1]
    f = mono(29)
    step = 360.0 / len(ring)
    for i, ch in enumerate(ring):
        c.save()
        c.rotate(i * step)
        c.drawString(ch, -f.measureText(ch) / 2, -(R - 52), f, ink)
        c.restore()
    word = T.spec["stamp"][0]
    size = min(250.0, 2 * (R - 92) / (anton(100).measureText(word) / 100))
    big = anton(size)
    c.drawString(word, -big.measureText(word) / 2, 0.859 * size / 2, big, ink)
    er = skia.Paint(AntiAlias=True)
    er.setBlendMode(skia.BlendMode.kDstOut)
    c.drawImageRect(T.ink, skia.Rect.MakeLTRB(-R - 24, -R - 24, R + 24, R + 24), skia.SamplingOptions(skia.FilterMode.kLinear), er)
    c.restore()
    rng = np.random.default_rng(int(T.shop["id"]) + 5)    # a few spatters from the impact
    for _ in range(9):
        a, rr, sz = rng.uniform(0, 2 * math.pi), rng.uniform(R + 14, R + 46), rng.uniform(1.6, 4.2)
        c.drawCircle(rr * math.cos(a), rr * math.sin(a), sz, fill(GREEN, 0.8 * clamp(d / 0.05)))
    c.restore()


def draw_pen(c, T, t):
    if t < T_PEN:
        return
    x0, y0, x1, y1 = T.five
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2 + 30, (y1 - y0) / 2 + 22
    path = skia.Path()
    n = 90
    for i in range(n + 1):
        u = i / n
        a = math.radians(205 + 400 * u)
        k = 1 + 0.05 * math.sin(3 * a + 0.7) + 0.06 * u
        x, y = cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)
        (path.moveTo if i == 0 else path.lineTo)(x, y)
    m = skia.PathMeasure(path, False)
    seg = skia.Path()
    m.getSegment(0, m.getLength() * ease_out((t - T_PEN) / 0.45), seg, True)
    c.drawPath(seg, stroke(RED, 7, 0.9))


def draw_pin(c, T, t):
    if t < T_PIN - 0.2:
        return
    px, py = T.pin_at
    p = clamp((t - (T_PIN - 0.2)) / 0.55)
    drop = (1 - spring(p, 0.45, 13)) * -140
    c.drawOval(skia.Rect.MakeXYWH(px - 16, py + 26, 32, 9), fill("#000000", 0.18 * clamp(p * 2)))
    c.save()
    c.translate(px, py + drop)
    pin = skia.Path()
    pin.moveTo(0, 30)
    pin.cubicTo(-10, 12, -24, 2, -24, -16)
    pin.cubicTo(-24, -32, -12, -42, 0, -42)
    pin.cubicTo(12, -42, 24, -32, 24, -16)
    pin.cubicTo(24, 2, 10, 12, 0, 30)
    pin.close()
    c.drawPath(pin, fill(RED, 0.95))
    c.drawCircle(0, -16, 8.5, fill(PAPER))
    c.restore()


def draw_els(c, T, t):
    for e in T.els:
        if t < e["t"]:
            continue
        r = clamp((t - e["t"]) / PRINT) if e["t"] >= 0 else 1.0
        x0, y0, x1, y1 = e["box"]
        c.save()
        if r < 1:
            c.clipRect(skia.Rect.MakeLTRB(x0 - 20, y0 - 10, x1 + 20, y0 - 10 + (y1 - y0 + 20) * r))
        if e["kind"] == "text":
            c.drawString(e["s"], e["x"], e["y"], e["f"], fill(e["colour"], 0.94))
        else:
            dash = stroke(INK3, 3)
            dash.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
            c.drawLine(PX, e["y"], TW - PX, e["y"], dash)
        c.restore()


def frame(c, T, hs, t):
    cx, cy, z, roll = camera(t, hs)
    sx, sy = shake(t)
    # steel, with a little parallax against the ticket
    c.clear(col("#121518"))
    off = -((cy * z) * 0.12) % 900
    c.drawImage(background(), 0, -off)
    # world
    dt = 1 / FPS
    v = abs(camera(t + dt, hs)[1] - camera(t - dt, hs)[1]) / 2 * z
    blur = min(26.0, v * 0.42)
    c.save()
    if blur > 0.8:
        c.saveLayer(None, skia.Paint(ImageFilter=skia.ImageFilters.Blur(0.01, blur)))
    c.translate(W / 2 + sx, H / 2 + sy)
    c.rotate(roll)
    c.scale(z, z)
    c.translate(-cx, -cy)
    c.save()
    c.rotate(-1.1, TW / 2, 0)                          # the ticket hangs a touch crooked
    path = ticket_path(T.h)
    c.save()
    c.translate(16, 26)
    c.drawPath(path, skia.Paint(Color=col("#000000", 0.5), AntiAlias=True,
                                MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22)))
    c.restore()
    paper = skia.Paint(AntiAlias=True)
    paper.setShader(skia.GradientShader.MakeLinear([(0, 0), (TW, 0)], [col(PAPER_EDGE), col(PAPER), col(PAPER), col(PAPER_EDGE)],
                                                   [0.0, 0.12, 0.88, 1.0]))
    c.drawPath(path, paper)
    c.save()
    c.clipPath(path, doAntiAlias=True)
    c.drawImageRect(T.grain, skia.Rect.MakeLTRB(0, 0, TW, T.h), skia.SamplingOptions(skia.FilterMode.kLinear))
    draw_els(c, T, t)
    draw_stamp(c, T, t)
    draw_pen(c, T, t)
    draw_pin(c, T, t)
    c.restore()
    c.restore()
    draw_rail(c)
    c.restore()
    if blur > 0.8:
        c.restore()
    # the heat lamp: warm light falling from above, breathing very slightly
    k = 1 + 0.04 * math.sin(t * 2.1) + 0.02 * math.sin(t * 5.3)
    lamp = skia.Paint(AntiAlias=True)
    lamp.setShader(skia.GradientShader.MakeRadial((W / 2, -300), 1350 * k, [col(AMBER, 0.42), col(AMBER, 0.12), col(AMBER, 0.0)],
                                                  [0.0, 0.45, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), lamp)
    vig = skia.Paint(AntiAlias=True)
    vig.setShader(skia.GradientShader.MakeRadial((W / 2, H * 0.45), H * 0.78, [col("#000000", 0.0), col("#000000", 0.0), col("#000000", 0.42)],
                                                 [0.0, 0.62, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), vig)


# ---------------------------------------------------------------- sound
def sound(T):
    n = int(DUR * SR)
    rng = np.random.default_rng(int(T.shop["id"]))
    out = np.zeros((n, 2), np.float32)
    tt = np.arange(n) / SR

    def add(x, at, gain_db, pan=0.0, delay_r=0.0):
        i = int(at * SR)
        x = np.asarray(x, np.float32)[: max(0, n - i)]
        g = AX.db(gain_db)
        out[i:i + len(x), 0] += x * g * math.sqrt(0.5 * (1 - pan))
        j = i + int(delay_r * SR)
        xr = x[: max(0, n - j)]
        out[j:j + len(xr), 1] += xr * g * math.sqrt(0.5 * (1 + pan))

    def noise(sec):
        return rng.normal(0, 1, int(sec * SR)).astype(np.float32)

    def env(sec, a=0.004, r=0.03):
        m = int(sec * SR)
        e = np.ones(m, np.float32)
        ka, kr = max(1, int(a * SR)), max(1, int(r * SR))
        e[:ka] = np.linspace(0, 1, ka)
        e[-kr:] *= np.linspace(1, 0, kr)
        return e

    # room: extractor fan, mains hum, the low wash of a kitchen
    for ch in range(2):
        wash = AX.bq(AX.bq(rng.normal(0, 1, n).astype(np.float32), "lp", 520), "lp", 520)
        fan = AX.bq(rng.normal(0, 1, n).astype(np.float32), "bp", 190, q=2.5)
        out[:, ch] += wash * AX.db(-40) + fan * AX.db(-44) + np.sin(2 * np.pi * 50 * tt + ch) * AX.db(-56) \
            + np.sin(2 * np.pi * 100 * tt) * AX.db(-60)

    def printer(sec=PRINT + 0.04):
        m = int(sec * SR)
        u = np.arange(m) / SR
        stepper = (signal.square(2 * np.pi * 96 * u) * 0.5 + 0.5)
        x = AX.bq(noise(sec) * stepper, "bp", 2300, q=0.9) + 0.25 * np.sin(2 * np.pi * 1180 * u)
        return x * env(sec, 0.003, 0.02)

    def whoosh(sec, f0=260, f1=2600):
        m = int(sec * SR)
        x = noise(sec)
        y = np.zeros(m, np.float32)
        hop = 512
        zi = np.zeros(2)
        for k in range(0, m, hop):
            p = k / m
            f = f0 + (f1 - f0) * math.sin(math.pi * p) ** 1.5
            w0 = 2 * math.pi * f / SR
            al = math.sin(w0) / (2 * 0.8)
            b = np.array([al, 0, -al]) / (1 + al)
            a = np.array([1, -2 * math.cos(w0) / (1 + al), (1 - al) / (1 + al)])
            y[k:k + hop], zi = signal.lfilter(b, a, x[k:k + hop], zi=zi)
        return y * np.sin(np.pi * np.linspace(0, 1, m)) ** 1.6

    def thump():
        sec = 0.6
        u = np.arange(int(sec * SR)) / SR
        f = 48 + 70 * np.exp(-u / 0.05)
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-u / 0.10)
        click = AX.bq(noise(sec), "lp", 3200) * np.exp(-u / 0.007)
        slap = AX.bq(noise(sec), "bp", 950, q=1.2) * np.exp(-u / 0.035)
        return body * 1.0 + click * 0.5 + slap * 0.9

    def scribble(sec=0.48):
        u = np.arange(int(sec * SR)) / SR
        am = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 8.5 * u + 2 * np.sin(2 * np.pi * 1.3 * u)))
        return AX.bq(noise(sec), "bp", 3300, q=1.4) * am * env(sec, 0.03, 0.08)

    def tok():
        u = np.arange(int(0.25 * SR)) / SR
        return np.sin(2 * np.pi * 1550 * u) * np.exp(-u / 0.018) + 0.5 * np.sin(2 * np.pi * 2480 * u) * np.exp(-u / 0.01)

    def bell():
        sec = 2.4
        u = np.arange(int(sec * SR)) / SR
        x = np.zeros_like(u)
        for fr, amp, dec in ((2218, 1.0, 1.5), (2224.5, 0.6, 1.35), (5940, 0.32, 0.55), (8360, 0.16, 0.28)):
            x += amp * np.sin(2 * np.pi * fr * u) * np.exp(-u / dec)
        return x + AX.bq(noise(sec), "hp", 4000) * np.exp(-u / 0.004) * 0.6

    sp = T.spec
    for at in (T_RULE, T_RATE1, T_RATE2, T_RATE3, T_RULE3, T_FIND, T_PRE if sp["pre"] else -1, T_STREET, T_TOWN, T_RULE4,
               T_SRC1 if sp["src"][0] else -1, T_SRC2 if sp["src"][0] else -1, T_THANKS):
        if at >= 0:
            add(printer(), at, -27, pan=rng.uniform(-0.2, 0.2))
    hs = holds(T)
    for i in range(1, len(hs)):
        t0, t1 = hs[i - 1][1], hs[i][0]
        add(whoosh(t1 - t0 + 0.15), t0 - 0.05, -23 if i < 3 else -25, pan=0.15 * (-1) ** i)
    add(thump(), T_STAMP, -6)
    add(scribble(), T_PEN, -25, pan=0.25)
    add(tok(), T_PIN + 0.12, -20)
    add(tok(), T_PIN + 0.26, -30)
    add(bell(), T_THANKS, -13, pan=0.1, delay_r=0.0004)
    return AX.master(out, SR, target=-16.0, ceiling_db=-1.5)


# ---------------------------------------------------------------- output
def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:32]


def shops(args):
    data = json.load(open(os.path.join(REPO, "sales", "prospects_routed.json")))
    town = "Stone"
    if "--town" in args:
        town = args[args.index("--town") + 1]
        args = [a for a in args if a not in ("--town", town)]
    ids = [a for a in args if a.isdigit()]
    if ids:
        return [s for s in data if s["id"] in ids]
    return sorted((s for s in data if s["town"] == town and s["fsa"] == "5"), key=lambda s: s["order"])


def name_of(s):
    return f"{s['town'][:3].lower()}{s['order']:02d}_{slug(s['name'])}"


def stills(sel):
    d = os.path.join(BUILD, "stills")
    os.makedirs(d, exist_ok=True)
    times = [0.0, 0.7, 1.13, 1.6, 2.45, 3.6, 4.7, 6.0, 7.9]
    for s, spec in sel:
        T = Ticket(s, spec)
        hs = holds(T)
        tiles = []
        for t in times:
            surf = skia.Surface(W, H)
            frame(surf.getCanvas(), T, hs, t)
            tiles.append(surf.makeImageSnapshot().resize(360, 640))
        sheet = skia.Surface(360 * 9, 640)
        for i, im in enumerate(tiles):
            sheet.getCanvas().drawImage(im, 360 * i, 0)
        out = os.path.join(d, name_of(s) + ".jpg")
        sheet.makeImageSnapshot().save(out, skia.kJPEG)
        print(out)


def render(sel):
    d = os.path.join(BUILD, "reels")
    os.makedirs(d, exist_ok=True)
    made = []
    for s, spec in sel:
        T = Ticket(s, spec)
        hs = holds(T)
        base = os.path.join(d, name_of(s))
        wav = base + ".wav"
        import soundfile as sf
        sf.write(wav, sound(T), SR, subtype="PCM_24")
        enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                                "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                                base + ".mp4"], stdin=subprocess.PIPE)
        surf = skia.Surface(W, H)
        for i in range(int(DUR * FPS)):
            frame(surf.getCanvas(), T, hs, i / FPS)
            enc.stdin.write(surf.makeImageSnapshot().toarray().tobytes())
            if i == 0:
                surf.makeImageSnapshot().resize(540, 960).save(base + ".jpg", skia.kJPEG)
        enc.stdin.close()
        enc.wait()
        os.remove(wav)
        meta = dict(id=s["id"], order=s["order"], town=s["town"], name=s["name"], address=s["address"],
                    fsaDate=s["fsaDate"], file=os.path.basename(base) + ".mp4", poster=os.path.basename(base) + ".jpg",
                    mb=round(os.path.getsize(base + ".mp4") / 1e6, 2))
        json.dump(meta, open(base + ".json", "w"), indent=1)
        print(meta["file"], meta["mb"], "MB")


def manifest(_sel=None):
    """Merge the per-Reel sidecars (renders can run in parallel) into build/reels/manifest.json."""
    d = os.path.join(BUILD, "reels")
    rows = [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d)) if f.endswith(".json") and f != "manifest.json"]
    json.dump(sorted(rows, key=lambda m: (m["town"], m["order"])), open(os.path.join(d, "manifest.json"), "w"), indent=1)
    print(len(rows), "Reels in manifest")


if __name__ == "__main__":
    mode, rest = (sys.argv[1] if len(sys.argv) > 1 else "stills"), sys.argv[2:]
    if "--sample" in rest:                            # e.g. render --sample special: the monthly product's format
        sel = [SAMPLES[n] for n in rest[rest.index("--sample") + 1:]] or list(SAMPLES.values())
    else:
        sel = [(s, None) for s in shops(rest)]
    {"stills": stills, "render": render, "manifest": manifest}[mode](sel)
