"""Listing images for the low-stim phone kit (2700x2025, Etsy 4:3).

    ~/youtube/.venv/bin/python mock.py      # after make.py; writes out/listing/
"""
import os, colorsys, random
from PIL import Image, ImageDraw, ImageFilter
import make

KIT = make.OUT
OUT = os.path.join(make.HERE, "out", "listing")
W, H = 2700, 2025
STONE = (222, 219, 213)
INK = (40, 41, 43)
SOFT = (120, 121, 124)


def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255)
    return m


def phone(screen, h=1500):
    """Wrap a 1320x2868 screen in a plain black device frame, return RGBA."""
    sw = int(h * 1320 / 2868)
    scr = screen.resize((sw, h), Image.LANCZOS)
    b = int(h * 0.018)
    fw, fh = sw + 2 * b, h + 2 * b
    out = Image.new("RGBA", (fw + 80, fh + 80), (0, 0, 0, 0))
    sh = Image.new("L", out.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle([40, 55, 40 + fw, 55 + fh], int(fw * 0.16), fill=110)
    out.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(28)))
    frame = Image.new("RGBA", (fw, fh), (14, 14, 15, 255))
    frame.putalpha(rounded_mask((fw, fh), int(fw * 0.16)))
    out.alpha_composite(frame, (40, 40))
    scr = scr.convert("RGBA")
    scr.putalpha(rounded_mask((sw, h), int(sw * 0.14)))
    out.alpha_composite(scr, (40 + b, 40 + b))
    isl = int(sw * 0.30)
    ImageDraw.Draw(out).rounded_rectangle([40 + b + (sw - isl) // 2, 40 + b + int(h * 0.016),
                                           40 + b + (sw + isl) // 2, 40 + b + int(h * 0.016) + int(h * 0.034)],
                                          int(h * 0.017), fill=(0, 0, 0, 255))
    return out


def lock_screen(wall="05_ring"):
    s = Image.open(f"{KIT}/wallpapers_iphone/lock/{wall}_lock.jpg").convert("RGB")
    d = ImageDraw.Draw(s)
    f = make.inter(330, 250)
    t = "9:41"
    d.text(((1320 - d.textlength(t, font=f)) / 2, 330), t, font=f, fill=(176, 177, 180))
    f2 = make.inter(56, 400)
    t2 = "Monday 12 October"
    d.text(((1320 - d.textlength(t2, font=f2)) / 2, 270), t2, font=f2, fill=(150, 151, 154))
    return s


def home_screen(wall="01_matte", tone="graphite", busy=False):
    s = Image.open(f"{KIT}/wallpapers_iphone/home/{wall}_home.jpg").convert("RGB")
    if busy:
        s = make.vgrad((1320, 2868), (255, 120, 90), (110, 60, 220))
    d = ImageDraw.Draw(s)
    # text widget
    f = make.inter(150, 250)
    d.text((110, 300), "Mon 12", font=f, fill=(255, 255, 255) if busy else (170, 172, 175))
    f2 = make.inter(54, 400)
    d.text((116, 480), "2 things today", font=f2, fill=(255, 255, 255) if busy else (120, 121, 124))
    cp = make.codepoints()
    names = ["phone", "messages", "camera", "maps", "notes", "calendar", "music", "settings"]
    dock = ["browser", "mail", "photos", "clock"]
    if busy:
        names = [n for n, _ in make.ICONS[:24]]
    sym = dict(make.ICONS)
    ic, gap, x0, y0 = 230, 60, 110, 800 if not busy else 700
    random.seed(4)
    for i, n in enumerate(names):
        x = x0 + (i % 4) * (ic + gap)
        y = y0 + (i // 4) * (ic + gap + 40)
        if busy:
            r, g, b = colorsys.hsv_to_rgb(random.random(), 0.85, 0.95)
            tile = Image.new("RGB", (ic, ic), (int(r * 255), int(g * 255), int(b * 255)))
            dd = ImageDraw.Draw(tile)
            ff = make.sym_font(int(ic * 0.5), 500, 1)
            l, t_, r_, b_ = dd.textbbox((0, 0), cp[sym[n]], font=ff)
            dd.text(((ic - (r_ - l)) / 2 - l, (ic - (b_ - t_)) / 2 - t_), cp[sym[n]], font=ff, fill=(255, 255, 255))
            badge = random.random() < 0.45
        else:
            tile = Image.open(f"{KIT}/icons/{tone}/{n}.png").resize((ic, ic), Image.LANCZOS)
            badge = False
        s.paste(tile, (x, y), rounded_mask((ic, ic), int(ic * 0.23)))
        if badge:
            d.ellipse([x + ic - 60, y - 20, x + ic + 20, y + 60], fill=(255, 59, 48))
            d.text((x + ic - 35, y - 8), str(random.randint(1, 99)), font=make.inter(44, 600), fill=(255, 255, 255))
    if not busy:
        dy = 2868 - 420
        d.rounded_rectangle([60, dy - 50, 1260, dy + ic + 50], 110, fill=(52, 53, 56))
        for i, n in enumerate(dock):
            tile = Image.open(f"{KIT}/icons/{tone}/{n}.png").resize((ic, ic), Image.LANCZOS)
            s.paste(tile, (x0 + i * (ic + gap), dy), rounded_mask((ic, ic), int(ic * 0.23)))
    return s


def canvas(title=None, sub=None):
    c = Image.new("RGBA", (W, H), STONE + (255,))
    d = ImageDraw.Draw(c)
    if title:
        d.text((150, 150), title, font=make.inter(120, 600), fill=INK)
    if sub:
        d.text((154, 300), sub, font=make.inter(58, 400), fill=SOFT)
    return c, d


def save(c, name):
    os.makedirs(OUT, exist_ok=True)
    c.convert("RGB").save(os.path.join(OUT, name), quality=92)


def build():
    # 1 hero
    c, d = canvas("Low-Stim Phone Kit", "a calm, dark-grey home screen · iPhone + Android")
    c.alpha_composite(phone(lock_screen(), 1480), (1020, 440))
    c.alpha_composite(phone(home_screen(), 1480), (1840, 400))
    y = 560
    for line in ["24 wallpapers", "200 monochrome icons", "10-minute setup guide", "instant download"]:
        d.text((154, y), "—  " + line, font=make.inter(64, 400), fill=INK); y += 120
    save(c, "02_hero.jpg")
    # 2 before / after
    c, d = canvas()
    c.alpha_composite(phone(home_screen(busy=True), 1500), (180, 380))
    c.alpha_composite(phone(home_screen(), 1500), (1000, 380))
    d.text((150, 130), "Make your phone boring.", font=make.inter(130, 650), fill=INK)
    d.text((360, 300), "before", font=make.inter(64, 500), fill=SOFT)
    d.text((1190, 300), "after", font=make.inter(64, 500), fill=INK)
    y = 760
    for line in ["Low-Stim Phone Kit", "iPhone + Android", "24 wallpapers", "200 icons", "10-min setup guide"]:
        big = line == "Low-Stim Phone Kit"
        d.text((1900, y), line, font=make.inter(84 if big else 62, 600 if big else 400), fill=INK if big else SOFT)
        y += 150 if big else 105
    save(c, "01_before_after.jpg")
    # 3 icons
    c, d = canvas("200 icons, two tones", "graphite + ash · 100 everyday apps · 1024 px PNG")
    for k, tone in enumerate(["graphite", "ash"]):
        for i, (n, _) in enumerate(make.ICONS[:24]):
            t = Image.open(f"{KIT}/icons/{tone}/{n}.png").resize((150, 150), Image.LANCZOS)
            x = 150 + (i % 12) * 200
            y = 520 + (i // 12) * 200 + k * 620
            c.paste(t, (x, y), rounded_mask((150, 150), 34))
    save(c, "03_icons.jpg")
    # 4 wallpapers
    c, d = canvas("24 wallpapers", "6 designs · home + lock · iPhone + Android sizes")
    for i, (n, _) in enumerate(make.WALLS):
        w = Image.open(f"{KIT}/wallpapers_iphone/home/{n}_home.jpg").resize((330, 717), Image.LANCZOS)
        c.paste(w, (150 + i * 400, 560), rounded_mask((330, 717), 44))
        d.text((150 + i * 400, 1310), n[3:], font=make.inter(54, 400), fill=SOFT)
    save(c, "04_wallpapers.jpg")
    # 5 lock screens
    c, d = canvas("Quiet lock screens", "the clock area stays clear")
    for i, wname in enumerate(["01_matte", "05_ring", "06_contour"]):
        c.alpha_composite(phone(lock_screen(wname), 1420), (330 + i * 720, 450))
    save(c, "05_lock.jpg")
    print("listing images ->", OUT)


if __name__ == "__main__":
    build()
