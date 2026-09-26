# EP02-specific parts, spliced into the EP01 engine by make_ep02.py (the furniture, captions, cards,
# the gauge and the frame loop are shared). Price ruler + six floors + cues.

RX0, RX1, RY = 96, 900, 1488                  # price ruler (log dollars per million tokens)
R_MIN, R_MAX = math.log10(0.001), math.log10(100.0)
TICKS = [(0.001, "$0.001"), (0.01, "1¢"), (0.1, "10¢"), (1.0, "$1"), (10.0, "$10"), (100.0, "$100")]


def rx(dollars):
    return lerp(RX1, RX0, (math.log10(max(dollars, 0.001)) - R_MIN) / (R_MAX - R_MIN))   # cheaper to the right


def ruler(c, t):
    a = ease(seg(t, ls(0) - 0.4, ls(0) + 0.6))
    if a <= 0:
        return
    c.drawLine(RX0, RY, RX1, RY, mg.stroke(MID, 1.3, 0.6 * a))
    for s, lab in TICKS:
        x = rx(s)
        c.drawLine(x, RY - 9, x, RY + 9, mg.stroke(MID, 1.2, 0.7 * a))
        h.mono(c, lab, x, RY + 34, 14, SOFT, 0.85 * a, align="center")
    h.mono(c, "$ PER 1M TOKENS", RX0, RY - 26, 12, SOFT, 0.7 * a)
    h.mono(c, "CHEAPER →", RX1, RY + 60, 12, SOFT, 0.7 * a, align="right")

    def tag(x, lab, col, k, up=0):
        path = skia.Path(); path.moveTo(x, RY - 4); path.lineTo(x - 8, RY - 18); path.lineTo(x + 8, RY - 18); path.close()
        c.drawPath(path, mg.fill(col, a * k))
        h.mono(c, lab, x, RY - 30 - up, 13, col, a * k, align="center", font=mg.MONO_M)
    # the flagship: $5 slides to $4 (line 0)
    k0 = smooth(seg(t, ls(0) + 1.0, ls(0) + 2.2))
    tag(rx(lerp(5.0, 4.0, k0)), "$4" if k0 > 0.5 else "$5", WHITE, 1.0)
    # the rival's two models appear at half price (line 1)
    k1 = ease(seg(t, ls(1) + 0.6, ls(1) + 1.4))
    if k1 > 0:
        tag(rx(lerp(4.0, 2.0, k1)), "$2", TURQ, k1, up=16)
        tag(rx(lerp(0.2, 0.1, k1)), "$0.10", TURQ, k1)
    # history: the same capability, $60 -> $0.06 (line 7), with a trail
    L7 = next(i for i, x in enumerate(L) if x.get("mark") == 0.06)
    kh = smooth(seg(t, ls(L7) + 1.0, le(L7) - 0.5))
    if kh > 0:
        fade = 1 - ease(seg(t, first_of_floor(3)["start"], first_of_floor(3)["start"] + 1.0))
        v = 10 ** lerp(math.log10(60.0), math.log10(0.06), kh)
        x0, x1 = rx(60.0), rx(v)
        glow = mg.stroke(GLOW, 5, 0.9 * fade * a)
        c.drawLine(x0, RY, x1, RY, glow)
        c.drawCircle(x1, RY, 7, mg.fill(GLOW, fade * a))
        h.mono(c, f"${v:,.2f}" if v >= 0.1 else f"${v:.2f}", x1, RY + 62, 16, GLOW, fade * a, align="center", font=mg.MONO_M)
    # IMAGINE: a dotted marker off towards free
    ki = ease(seg(t, ls(DROP_LINE + 1) + 0.4, ls(DROP_LINE + 1) + 1.4)) * (1 - ease(seg(t, F_START[5], F_START[5] + 1.2)))
    if ki > 0:
        x = rx(0.0012)
        p = mg.stroke(GLOW, 1.4, ki); p.setPathEffect(skia.DashPathEffect.Make([5, 6], 0))
        c.drawLine(rx(0.1), RY - 6, x, RY - 6, p)
        h.mono(c, "≈ FREE · IF", x - 8, RY - 30, 13, GLOW, ki, align="right", font=mg.MONO_M)


# ================================================================ small drawing helpers
def big_parts(s, f):
    if not s.endswith("%"):
        return s, None, f.measureText(s), 0.0
    fu = mg.font(mg.MONO_M, f.getSize() * 0.42)
    num = s[:-1]
    return num, fu, f.measureText(num) + f.getSize() * 0.06 + fu.measureText("%"), f.measureText(num) + f.getSize() * 0.06


def draw_big(c, s, x, y, f, paint, align="left"):
    num, fu, w, ux = big_parts(s, f)
    x0 = x - w if align == "right" else x - w / 2 if align == "center" else x
    c.drawString(num, x0, y, f, paint)
    if fu is not None:
        c.drawString("%", x0 + ux, y - f.getSize() * 0.40, fu, paint)
    return w


def price_card(c, x, y, w, title, old, new, pct, t0, t, col=WHITE, a=1.0, big=64, small=30):
    """A glass price tag: the old price gets struck through, the new one lands, the % stamps in."""
    mg.glass(c, x, y, w, 250, 18, a)
    h.mono(c, title, x + 30, y + 50, 16, SOFT, a, font=mg.MONO_M)
    f = mg.font(mg.DISPLAY, 54)
    c.drawString(old, x + 30, y + 132, f, mg.fill(MID, a))
    ks = ease(seg(t, t0, t0 + 0.5))
    if ks > 0:
        wo = f.measureText(old)
        c.drawLine(x + 26, y + 112, x + 26 + (wo + 8) * ks, y + 112, mg.stroke(TURQ, 4, a))
    kn = ease(seg(t, t0 + 0.4, t0 + 0.9), "o")
    if kn > 0:
        c.drawString(new, x + 30, y + 214, mg.font(mg.DISPLAY, big), mg.fill(col, a * kn))
        h.mono(c, pct, x + w - 26, y + 60, small, TURQ, a * kn, align="right", font=mg.MONO_M)


def queen(c, cx, cy, s, a, col=WHITE, bob=0.0):
    """A line-art chess queen (crown of five points, body, base)."""
    y = cy + bob
    p = mg.stroke(col, 2.6, a)
    crown = skia.Path()
    pts = [(-30, -40), (-24, -78), (-12, -48), (0, -86), (12, -48), (24, -78), (30, -40)]
    crown.moveTo(cx + pts[0][0] * s, y + pts[0][1] * s)
    for px, py in pts[1:]:
        crown.lineTo(cx + px * s, y + py * s)
    c.drawPath(crown, p)
    for px, py in ((-24, -82), (0, -90), (24, -82)):
        c.drawCircle(cx + px * s, y + py * s, 4.5 * s, p)
    body = skia.Path()
    body.moveTo(cx - 30 * s, y - 40 * s); body.lineTo(cx - 18 * s, y + 20 * s); body.lineTo(cx + 18 * s, y + 20 * s); body.lineTo(cx + 30 * s, y - 40 * s)
    c.drawPath(body, p)
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 38 * s, y + 20 * s, 76 * s, 16 * s), 4, 4, p)
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 46 * s, y + 36 * s, 92 * s, 14 * s), 4, 4, p)


def book_spines(c, x, y, n, k, a):
    for i in range(n):
        kk = clamp(k * n - i)
        if kk <= 0:
            continue
        w = 58
        hh = 300 - (i % 3) * 26
        r = skia.Rect.MakeXYWH(x + i * (w + 10), y + (300 - hh) + (1 - kk) * 40, w, hh)
        c.drawRoundRect(r, 6, 6, mg.stroke(WHITE if i % 2 else MID, 2.0, a * kk))
        c.drawLine(r.left() + 10, r.top() + 30, r.right() - 10, r.top() + 30, mg.stroke(TURQ, 1.6, a * kk))
        c.drawLine(r.left() + 10, r.bottom() - 30, r.right() - 10, r.bottom() - 30, mg.stroke(MID, 1.2, a * kk * 0.7))


# ================================================================ floor 0 · GROUND
def fl_ground(c, t):
    c.drawImage(h.ground("graphite"), 0, 0)
    a_in = ease(seg(t, 0.2, 1.2))
    price_card(c, 150, 430, 780, "ONE LAB · ITS FLAGSHIP", "$5", "$4", "−20%", ls(0) + 1.0, t, WHITE, a_in)
    k1 = ease(seg(t, ls(1) - 0.2, ls(1) + 0.5))
    if k1 > 0:
        price_card(c, 150, 720, 370, "RIVAL · MODEL 1", "$4", "$2", "−50%", ls(1) + 0.8, t, TURQ, k1, big=54, small=22)
        price_card(c, 560, 720, 370, "RIVAL · MODEL 2", "$0.20", "$0.10", "−50%", ls(1) + 1.3, t, TURQ, k1, big=50, small=22)
    # the ninety minutes: a clock ring between the two
    kc = ease(seg(t, ls(1) - 0.3, ls(1) + 1.5))
    if kc > 0:
        cx, cy, r = 540, 1030, 60
        c.drawCircle(cx, cy, r, mg.stroke(MID, 2, 0.5 * kc))
        rect = skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r)
        pth = skia.Path(); pth.addArc(rect, -90, 540 * kc / 1.0 if kc < 1 else 180)
        c.drawPath(pth, mg.stroke(TURQ, 8, kc))
        h.mono(c, "+90 MIN", cx, cy + 8, 22, WHITE, kc, align="center", font=mg.MONO_M)
    kb = ease(seg(t, ls(2), ls(2) + 0.6))
    if kb > 0:
        for j, lab in enumerate(["TWO COMPANIES", "ONE AFTERNOON", "BOTH WENT CHEAPER"]):
            kk = ease(seg(t, ls(2) + j * 0.9, ls(2) + j * 0.9 + 0.4))
            h.mono(c, lab, 540, 1128 + j * 34, 20, TURQ if j == 2 else WHITE, kk, align="center", font=mg.MONO_M)
    h.vignette(c, 0.5)


# ================================================================ floor 1 · MECHANISM
def fl_mechanism(c, t):
    c.drawImage(h.ground("slate"), 0, 0)
    L4 = first_of_floor(1)["i"] + 1
    # the chart: x = price (log, cheaper right), y = how good
    X0, X1, Y0, Y1 = 150, 930, 1160, 420
    ka = ease(seg(t, ls(L4) - 0.3, ls(L4) + 0.8))
    blur_y = ease(seg(t, ls(L4 + 1), ls(L4 + 1) + 0.8)) * (1 - ease(seg(t, ls(L4 + 3), ls(L4 + 3) + 1)))
    glow_x = ease(seg(t, ls(L4 + 1) + 2.0, ls(L4 + 1) + 2.8)) * (1 - ease(seg(t, ls(L4 + 3), ls(L4 + 3) + 1)))
    if ka > 0:
        c.drawLine(X0, Y0, X1, Y0, mg.stroke(TURQ if glow_x > 0.5 else MID, 2.0, ka))
        py = mg.stroke(MID, 2.0, ka * (1 - 0.7 * blur_y))
        if blur_y > 0:
            py.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6 * blur_y))
        c.drawLine(X0, Y0, X0, Y1, py)
        h.mono(c, "HOW MUCH  →  CHEAPER", X1, Y0 + 44, 16, TURQ if glow_x > 0.5 else SOFT, ka, align="right", font=mg.MONO_M)
        h.mono(c, "HOW GOOD", X0, Y1 - 24, 16, SOFT, ka * (1 - 0.6 * blur_y), font=mg.MONO_M)
        if blur_y > 0.3:
            h.mono(c, "?", X0 + 26, (Y0 + Y1) / 2, 60, SOFT, blur_y, font=mg.DISPLAY)
    # models drift up and to the right (better and cheaper) over the months
    kd = seg(t, ls(L4) + 0.6, le(L4 + 2))
    if kd > 0:
        rng = np.random.default_rng(7)
        for j in range(18):
            born = j / 18
            if kd < born:
                continue
            age = (kd - born)
            x = X0 + 60 + (born * 0.75 + age * 0.25) * (X1 - X0 - 120)
            y = Y0 - 60 - (born * 0.7 + age * 0.18) * (Y0 - Y1 - 120) + rng.normal(0, 18)
            col = TURQ if j % 2 else WHITE
            c.drawCircle(x, y, 7, mg.fill(col, 0.85 * ka))
    # two dots racing: once one moves, the other has hours (line L4+2)
    kr = seg(t, ls(L4 + 2) + 1.0, le(L4 + 2))
    if kr > 0:
        for j, (col, delay) in enumerate(((WHITE, 0.0), (TURQ, 0.18))):
            k = smooth(clamp((kr - delay) / (1 - delay)))
            x = lerp(X0 + 380, X1 - 60, k)
            y = Y1 + 110 + j * 70
            c.drawCircle(x, y, 12, mg.fill(col, ka))
            c.drawLine(X0 + 380, y, x, y, mg.stroke(col, 2, 0.5 * ka))
        h.mono(c, "HOURS, NOT WEEKS", X1 - 60, Y1 + 60, 16, TURQ, ease(kr), align="right", font=mg.MONO_M)
    # the a16z journey: a big counter (line L4+3)
    kj = seg(t, ls(L4 + 3) + 1.0, le(L4 + 3) - 0.5)
    if t > ls(L4 + 3) - 0.3:
        a = ease(seg(t, ls(L4 + 3) - 0.3, ls(L4 + 3) + 0.4))
        c.drawRect(skia.Rect.MakeWH(W, H), mg.fill("#0E1013", 0.72 * a))
        v = 10 ** lerp(math.log10(60.0), math.log10(0.06), smooth(kj))
        txt = f"${v:,.2f}"
        f = mg.font(mg.DISPLAY, 120)
        c.drawString(txt, 540 - f.measureText(txt) / 2, 820, f, mg.fill(TURQ if kj >= 1 else WHITE, a))
        h.mono(c, "PER MILLION TOKENS · SAME CAPABILITY", 540, 880, 18, SOFT, a, align="center", font=mg.MONO_M)
        kx = ease(seg(t, le(L4 + 3) - 0.6, le(L4 + 3)))
        if kx > 0:
            c.drawString("1,000×", 540 - mg.font(mg.DISPLAY, 72).measureText("1,000×") / 2, 1040, mg.font(mg.DISPLAY, 72), mg.fill(WHITE, kx * a))
            h.mono(c, "CHEAPER IN THREE YEARS", 540, 1090, 18, TURQ, kx * a, align="center", font=mg.MONO_M)
    h.vignette(c, 0.5)


# ================================================================ floor 2 · YOU
def fl_you(c, t):
    c.drawImage(h.ground("slate"), 0, 0)
    L8 = first_of_floor(2)["i"]
    kb = seg(t, ls(L8) + 1.5, le(L8))
    book_spines(c, 180, 440, 8, kb, ease(seg(t, ls(L8), ls(L8) + 0.6)))
    if kb > 0:
        h.mono(c, "≈ 750,000 WORDS", 540, 800, 22, WHITE, ease(kb), align="center", font=mg.MONO_M)
    kc = ease(seg(t, ls(L8 + 1) + 0.8, ls(L8 + 1) + 1.6), "o")
    if kc > 0:
        cx, cy = 540, 960
        c.drawCircle(cx, cy, 86 * kc, mg.stroke(TURQ, 4, kc))
        c.drawCircle(cx, cy, 72 * kc, mg.stroke(TURQ, 1.5, 0.6 * kc))
        txt = "<10P"
        f = mg.font(mg.DISPLAY, 44)
        c.drawString(txt, cx - f.measureText(txt) / 2, cy + 16, f, mg.fill(WHITE, kc))
    for j, lab in enumerate(["YOUR WHOLE READING LIST", "EVERY REVIEW A TAKEAWAY HAS HAD", "A YEAR OF YOUR EMAILS"]):
        tk = ls(L8 + 2) + j * 1.7
        ka = ease(seg(t, tk, tk + 0.45), "o")
        if ka <= 0:
            continue
        y = 1090 + j * 64
        h.mono(c, lab, 540 + (1 - ka) * 40, y, 22, TURQ if j == 1 else WHITE, ka, align="center", font=mg.MONO_M)
    h.vignette(c, 0.5)


# ================================================================ floor 3 · IDEA
def fl_idea(c, t):
    c.drawImage(h.ground("graphite"), 0, 0)
    L11 = first_of_floor(3)["i"]
    # the treadmill: a chessboard scrolling towards us, the queens running and staying put
    run = seg(t, ls(L11 + 1), DUR)
    cam = h.Cam((0, 3.2, 9.0), (0, 0.4, -6.0), fov=58)
    fr = h.Frame(cam, fade=(6, 40))
    off = (t * 2.2) % 2.0
    lines_ = []
    for z in np.arange(-40, 10, 2.0):
        zz = z + off
        lines_.append(np.array([[-8, 0, zz], [8, 0, zz]]))
    for x in np.arange(-8, 8.1, 2.0):
        lines_.append(h.densify(np.array([[x, 0, -40], [x, 0, 10]]), 2.0))
    ka = ease(seg(t, F_START[3], F_START[3] + 1.2))
    fr.lines(lines_, MID, 1.2, 0.55 * ka, glow=0.0, tip=False)
    c.saveLayer()
    fr.draw(c, 0.6, 0.2)
    mask = skia.Paint(BlendMode=skia.BlendMode.kDstIn)
    mask.setShader(skia.GradientShader.MakeLinear([(0, 960), (0, 1130)], [skia.Color4f(0, 0, 0, 1), skia.Color4f(0, 0, 0, 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), mask)
    c.restore()
    kq = ease(seg(t, ls(L11 + 1) - 0.2, ls(L11 + 1) + 0.8))
    if kq > 0:
        bob1 = abs(math.sin(t * 7.0)) * -16
        bob2 = abs(math.sin(t * 7.0 + 1.3)) * -16
        queen(c, 380, 1030, 1.6, kq, WHITE, bob1)
        queen(c, 700, 1030, 1.6, kq, TURQ, bob2)
        kl = ease(seg(t, ls(L11 + 3), ls(L11 + 3) + 0.6))
        if kl > 0:
            h.mono(c, "LAB A", 380, 1150, 18, WHITE, kl, align="center", font=mg.MONO_M)
            h.mono(c, "LAB B", 700, 1150, 18, TURQ, kl, align="center", font=mg.MONO_M)
    # the quote, set like a page
    kq2 = ease(seg(t, ls(L11 + 1) + 0.6, ls(L11 + 1) + 1.4)) * (1 - ease(seg(t, ls(L11 + 2) + 0.2, ls(L11 + 2) + 0.8)))
    if kq2 > 0:
        mg.glass(c, 130, 420, 820, 250, 18, kq2)
        f = mg.font(mg.BODY, 36)
        for j, ln in enumerate(["“It takes all the running", "you can do, to keep", "in the same place.”"]):
            c.drawString(ln, 170, 490 + j * 50, f, mg.fill(WHITE, kq2))
        h.mono(c, "THE RED QUEEN · THROUGH THE LOOKING-GLASS · 1871", 170, 646, 13, SOFT, kq2)
    kv = ease(seg(t, ls(L11 + 2) + 0.4, ls(L11 + 2) + 1.2)) * (1 - ease(seg(t, ls(L11 + 3) - 0.2, ls(L11 + 3) + 0.4)))
    if kv > 0:
        mg.glass(c, 130, 420, 820, 250, 18, kv)
        c.drawString("THE RED QUEEN", 170, 500, mg.font(mg.DISPLAY, 40), mg.fill(TURQ, kv))
        c.drawString("HYPOTHESIS", 170, 556, mg.font(mg.DISPLAY, 40), mg.fill(WHITE, kv))
        h.mono(c, "LEIGH VAN VALEN · 1973 · RIVALS KEEP EVOLVING TOO", 170, 630, 14, SOFT, kv)
    kc = ease(seg(t, ls(L11 + 3) + 3.2, ls(L11 + 3) + 4.0))
    if kc > 0:
        h.mono(c, "EVERY STEP THEY TAKE", 540, 520, 24, WHITE, kc, align="center", font=mg.MONO_M)
        c.drawString("YOU GET IT CHEAPER", 540 - mg.font(mg.DISPLAY, 46).measureText("YOU GET IT CHEAPER") / 2, 600, mg.font(mg.DISPLAY, 46), mg.fill(TURQ, kc))
    h.vignette(c, 0.5)


# ================================================================ floor 4 · IMAGINE (the drop is shared)
def dream_extras(c, t, kout):
    Lg = DROP_LINE + 1
    stamp = ease(seg(t, LAND + 0.4, LAND + 1.0)) * kout
    if stamp > 0:
        r = skia.Rect.MakeXYWH(300, 350, 480, 64)
        p = mg.stroke(GLOW, 1.6, stamp); p.setPathEffect(skia.DashPathEffect.Make([7, 6], 0))
        c.drawRoundRect(r, 10, 10, p)
        h.mono(c, "IMAGINE · NOT A FORECAST", 540, 392, 20, GLOW, stamp, align="center", font=mg.MONO_M)
    ghosts = [("THE BEST TUTOR", "≈ 0P"), ("THE BEST CODER", "≈ 0P"), ("THE BEST TRANSLATOR", "≈ 0P"), ("THE BEST SECOND OPINION", "≈ 0P")]
    for j, (a1, a2) in enumerate(ghosts):
        tk = ls(Lg + 1) - 1.2 + (j - 1) * 1.4 if j else ls(Lg) + 0.6
        kk = seg(t, tk, tk + 3.6)
        if 0 < kk < 1:
            a = math.sin(math.pi * kk) * kout
            y = lerp(1180, 520, kk) + j * 16
            x = [320, 740, 380, 700][j]
            p = mg.stroke(GLOW, 1.4, 0.8 * a); p.setPathEffect(skia.DashPathEffect.Make([4, 5], 0))
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 230, y - 64, 460, 128), 16, 16, p)
            h.mono(c, a1, x, y - 4, 22, WHITE, a, align="center", font=mg.MONO_M)
            h.mono(c, a2, x, y + 32, 20, GLOW, a, align="center", font=mg.MONO_M)
    qi = next(i for i, x in enumerate(L) if x.get("quiet"))
    kq = ease(seg(t, ls(qi), ls(qi) + 0.6)) * kout
    if kq > 0:
        f = mg.font(mg.DISPLAY, 44)
        for j, s_ in enumerate(["WHEN THINKING IS FREE,", "WHAT GETS EXPENSIVE?"]):
            c.drawString(s_, 540 - f.measureText(s_) / 2, 700 + j * 64, f, mg.fill(WHITE if j == 0 else TURQ, kq))
    for j, s_ in enumerate(["YOUR TIME", "YOUR ATTENTION", "SOMEONE WHO TURNS UP"]):
        tk = ls(qi + 1) + 2.4 + j * 1.2
        ka = ease(seg(t, tk, tk + 0.4)) * kout
        if ka > 0:
            h.mono(c, s_, 540, 900 + j * 56, 28, GLOW if j == 2 else WHITE, ka, align="center", font=mg.MONO_M)


# ================================================================ floor 5 · SURFACE
def fl_surface(c, t):
    c.drawImage(h.ground("graphite"), 0, 0)
    L21 = first_of_floor(5)["i"]
    ka = ease(seg(t, ls(L21) + 0.3, ls(L21) + 1.2)) * (1 - ease(seg(t, ls(L21 + 1) - 0.6, ls(L21 + 1))))
    if ka > 0:
        mg.glass(c, 150, 520, 780, 360, 20, ka)
        h.mono(c, "TONIGHT'S VERSION", 190, 580, 18, TURQ, ka, font=mg.MONO_M)
        for j, s_ in enumerate(["1 · THE JOB THAT MEANS HOURS OF READING", "2 · HAND IT OVER", "3 · IT COSTS PENNIES"]):
            kk = ease(seg(t, ls(L21) + 1.2 + j * 1.8, ls(L21) + 1.7 + j * 1.8))
            c.drawString(s_, 190, 670 + j * 80, mg.font(mg.BODY_M, 29), mg.fill(WHITE, ka * kk))
    # the mirrored close: −20% and −50%, then both still running
    k1 = ease(seg(t, ls(L21 + 1) + 0.1, ls(L21 + 1) + 0.6))
    if k1 > 0:
        f = mg.font(mg.DISPLAY, 96)
        draw_big(c, "−20%", 300, 760, f, mg.fill(WHITE, k1), align="center")
        k2 = ease(seg(t, ls(L21 + 1) + 2.0, ls(L21 + 1) + 2.5))
        draw_big(c, "−50%", 780, 760, f, mg.fill(TURQ, k2), align="center")
        h.mono(c, "ONE LAB", 300, 820, 18, SOFT, k1, align="center", font=mg.MONO_M)
        h.mono(c, "ITS RIVAL", 780, 820, 18, SOFT, k2, align="center", font=mg.MONO_M)
    k3 = ease(seg(t, ls(L21 + 2) + 0.1, ls(L21 + 2) + 0.7))
    if k3 > 0:
        bob1 = abs(math.sin(t * 7.0)) * -12
        bob2 = abs(math.sin(t * 7.0 + 1.3)) * -12
        queen(c, 420, 1080, 1.2, k3, WHITE, bob1)
        queen(c, 660, 1080, 1.2, k3, TURQ, bob2)
        h.mono(c, "BOTH STILL RUNNING", 540, 1180, 22, TURQ, k3, align="center", font=mg.MONO_M)
    ke = ease(seg(t, le(L21 + 2) + 0.4, le(L21 + 2) + 1.2))
    if ke > 0:
        h.mono(c, "EP02 · THE NINETY-MINUTE WAR", 540, 1250, 20, WHITE, ke, align="center", font=mg.MONO_M)
        for j, s_ in enumerate(SOURCES[:4]):
            h.mono(c, s_[:86] + ("…" if len(s_) > 86 else ""), 540, 1600 + j * 22, 11, SOFT, 0.8 * ke, align="center")
    h.vignette(c, 0.5)


def build_cues():
    CUES.clear()
    d = 0.012
    cue(0.25, "power_up", -10)
    cue(ls(0) + 1.0 + d, "relay", -10, -0.2)                   # the strike-through
    cue(ls(0) + 1.4 + d, "latch", -9, -0.2)                    # the new price lands
    cue(ls(1) - 0.3, "servo", -14, 0.0)                        # the clock ring
    cue(ls(1) + 0.8 + d, "relay", -11, -0.4)
    cue(ls(1) + 1.2 + d, "latch", -10, -0.4)
    cue(ls(1) + 1.3 + d, "relay", -11, 0.4)
    cue(ls(1) + 1.7 + d, "latch", -10, 0.4)
    for j in range(3):
        cue(ls(2) + j * 0.9 + d, "confirm", -16, 0.0)
    for f in range(1, 6):
        cue(F_START[f] - 0.2, "hydraulic" if f < 4 else "servo", -12, -0.7)
    L4 = first_of_floor(1)["i"] + 1
    cue(ls(L4) - 0.3, "form", -12)
    for k in range(9):
        cue(ls(L4) + 0.6 + k * 0.5, "tick_run", -21, -0.4 + 0.1 * k)
    cue(ls(L4 + 1) + 2.0, "scan", -14, 0.3)
    cue(ls(L4 + 2) + 1.0, "whoosh", -14, 0.2)
    cue(ls(L4 + 3) - 0.3, "dock", -10)
    for k in range(14):
        cue(ls(L4 + 3) + 1.0 + k * 0.5, "tick_run", -20 + k * 0.3, 0.0)
    cue(le(L4 + 3) - 0.6 + d, "thum", -11)
    L8 = first_of_floor(2)["i"]
    for k in range(8):
        cue(ls(L8) + 1.5 + k * ((le(L8) - ls(L8) - 1.5) / 8) + d, "thock", -12, -0.4 + 0.1 * k)
    cue(ls(L8 + 1) + 0.8 + d, "latch", -9)
    for j in range(3):
        cue(ls(L8 + 2) + j * 1.7 + d, "dock", -12, 0.2)
    L11 = first_of_floor(3)["i"]
    cue(ls(L11 + 1) - 0.2, "form", -13)
    cue(ls(L11 + 2) + 0.4, "dock", -11)
    cue(ls(L11 + 3) + 3.2, "confirm", -14)
    cue(FALL_T0 - 0.56, "vortex", -2)
    cue(LAND + 0.4, "swell", -10)
    cue(LAND + 0.5, "chatter", -16)
    for j in range(4):
        cue(ls(DROP_LINE + 1) + 0.6 + j * 1.6, "whoosh", -18, [-0.4, 0.4, -0.2, 0.2][j])
    qi = next(i for i, x in enumerate(L) if x.get("quiet"))
    for j in range(3):
        cue(ls(qi + 1) + 2.4 + j * 1.2 + d, "thock", -11, [-0.3, 0.0, 0.3][j])
    cue(F_START[5] - 0.3, "riser", -15)
    L21 = first_of_floor(5)["i"]
    for j in range(3):
        cue(ls(L21) + 1.2 + j * 1.8 + d, "thock", -10)
    cue(ls(L21 + 1) + 0.1 + d, "latch", -8, -0.3)
    cue(ls(L21 + 1) + 2.0 + d, "latch", -8, 0.3)
    cue(ls(L21 + 2) + 0.1 + d, "servo", -12)
    cue(le(L21 + 2) + 0.4, "thum", -14)
    json.dump(dict(cues=CUES, floors=F_START, fall=FALL_T0, land=LAND, total=DUR,
                   cuts=[x["start"] for x in L if x.get("cut")]), open(os.path.join(BUILD, "events.json"), "w"), indent=1)
    return CUES
