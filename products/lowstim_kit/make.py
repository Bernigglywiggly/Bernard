"""Low-stim phone kit: wallpapers + monochrome icons.

    ~/youtube/.venv/bin/python make.py            # everything into out/kit/
Fonts in _vendor/: Material Symbols Rounded (Apache 2.0), Inter (OFL). Licences copied into the kit.
"""
import os, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import gaussian_filter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, "_vendor")
OUT = os.path.join(HERE, "out", "kit")

# palette: warm-neutral greys, nothing saturated
BG = (38, 39, 41)        # graphite
BG2 = (30, 31, 33)       # deeper
ASH = (142, 144, 147)
FOG = (188, 189, 191)
LINE = (58, 59, 62)

SIZES = {"iphone": (1320, 2868), "android": (1440, 3200)}

ICONS = [  # (file name, material symbol)
    ("phone", "call"), ("messages", "chat_bubble"), ("mail", "mail"), ("camera", "photo_camera"),
    ("photos", "photo_library"), ("browser", "language"), ("maps", "map"), ("music", "music_note"),
    ("podcasts", "podcasts"), ("notes", "edit_note"), ("calendar", "calendar_today"), ("clock", "schedule"),
    ("alarm", "alarm"), ("weather", "partly_cloudy_day"), ("settings", "settings"), ("app_store", "apps"),
    ("wallet", "account_balance_wallet"), ("bank", "account_balance"), ("health", "favorite"),
    ("fitness", "fitness_center"), ("books", "menu_book"), ("reminders", "checklist"),
    ("calculator", "calculate"), ("files", "folder"), ("contacts", "person"), ("video_call", "videocam"),
    ("translate", "translate"), ("news", "newspaper"), ("shopping", "shopping_bag"),
    ("food", "restaurant"), ("taxi", "local_taxi"), ("travel", "flight"), ("smart_home", "home"),
    ("games", "sports_esports"), ("video", "play_circle"), ("social", "forum"), ("chat", "sms"),
    ("voice_memos", "mic"), ("tasks", "task_alt"), ("timer", "timer"), ("meditation", "self_improvement"),
    ("sleep", "bedtime"), ("savings", "savings"), ("cloud", "cloud"), ("passwords", "key"),
    ("scanner", "document_scanner"), ("compass", "explore"), ("stocks", "show_chart"),
    ("search", "search"),
    ("downloads", "download"),
    ("printer", "print"),
    ("wifi", "wifi"),
    ("devices", "devices"),
    ("flashlight", "flashlight_on"),
    ("battery", "bolt"),
    ("remote", "settings_remote"),
    ("tv", "tv"),
    ("radio", "radio"),
    ("headphones", "headphones"),
    ("speaker", "speaker"),
    ("watch", "watch"),
    ("car", "directions_car"),
    ("bus", "directions_bus"),
    ("train", "train"),
    ("bike", "pedal_bike"),
    ("parking", "local_parking"),
    ("fuel", "local_gas_station"),
    ("coffee", "coffee"),
    ("grocery", "local_grocery_store"),
    ("recipes", "skillet"),
    ("pharmacy", "local_pharmacy"),
    ("doctor", "medical_services"),
    ("medication", "medication"),
    ("water", "water_drop"),
    ("running", "directions_run"),
    ("pets", "pets"),
    ("plants", "potted_plant"),
    ("journal", "auto_stories"),
    ("learning", "school"),
    ("quotes", "format_quote"),
    ("assistant", "auto_awesome"),
    ("code", "code"),
    ("terminal", "terminal"),
    ("work", "work"),
    ("meetings", "groups"),
    ("docs", "description"),
    ("sheets", "table_chart"),
    ("slides", "present_to_all"),
    ("upload", "cloud_upload"),
    ("vpn", "encrypted"),
    ("security", "fingerprint"),
    ("authenticator", "verified_user"),
    ("crypto", "currency_bitcoin"),
    ("cards", "credit_card"),
    ("receipts", "receipt_long"),
    ("deals", "sell"),
    ("tickets", "confirmation_number"),
    ("events", "event"),
    ("movies", "movie"),
    ("subscriptions", "subscriptions"),
]
TONES = {  # tile, glyph
    "graphite": ((44, 45, 47), (170, 172, 175)),
    "ash": ((150, 152, 155), (40, 41, 43)),
}


def codepoints():
    cp = {}
    for line in open(os.path.join(V, "MaterialSymbolsRounded.codepoints")):
        name, hexv = line.split()
        cp[name] = chr(int(hexv, 16))
    return cp


def sym_font(px, weight=300, fill=0):
    f = ImageFont.truetype(os.path.join(V, "MaterialSymbolsRounded.ttf"), px)
    f.set_variation_by_axes([fill, 0, 48, weight])
    return f


def inter(px, weight=300):
    f = ImageFont.truetype(os.path.join(V, "Inter.ttf"), px)
    f.set_variation_by_axes([min(32, max(14, px // 3)), weight])
    return f


def grain(img, amount=4.0, seed=0):
    a = np.asarray(img).astype(np.float32)
    rng = np.random.default_rng(seed)
    n = rng.normal(0, amount, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))


def vgrad(size, top, bottom):
    w, h = size
    t = np.linspace(0, 1, h)[:, None, None]
    a = np.array(top)[None, None, :] * (1 - t) + np.array(bottom)[None, None, :] * t
    return Image.fromarray(np.repeat(a, w, axis=1).astype(np.uint8))


# ---------------------------------------------------------------- wallpapers
def wp_matte(size, lock):
    if not lock:
        return grain(Image.new("RGB", size, BG), 3.5, 1)
    w, h = size  # lock: soft lift low in the frame, clock area stays flat
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / w) ** 2 + ((yy - h * 0.72) / h) ** 2)
    lift = np.clip(1 - r / 0.45, 0, 1) ** 2 * 14
    a = np.array(BG, np.float32)[None, None, :] + lift[..., None]
    return grain(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 3.5, 11)


def wp_fade(size, lock):
    if lock:  # reversed: dark clock area, faint light rising from the bottom
        return grain(vgrad(size, (24, 25, 27), (54, 55, 58)), 3.5, 12)
    return grain(vgrad(size, (46, 47, 49), (24, 25, 27)), 3.5, 2)


def wp_line(size, lock):
    img = wp_matte(size, lock)
    w, h = size
    d = ImageDraw.Draw(img)
    y = int(h * (0.62 if lock else 0.5))
    m = int(w * 0.28)
    d.line([(m, y), (w - m, y)], fill=(92, 93, 96), width=max(3, w // 420))
    return img


def wp_words(size, lock):
    img = wp_fade(size, lock)
    w, h = size
    d = ImageDraw.Draw(img)
    txt = "one thing at a time"
    f = inter(int(w * 0.034), 300)
    tw = d.textlength(txt, font=f)
    y = int(h * (0.80 if lock else 0.47))
    d.text(((w - tw) / 2, y), txt, font=f, fill=(122, 123, 126))
    return img


def wp_ring(size, lock):
    img = wp_matte(size, lock)
    w, h = size
    big = Image.new("L", size, 0)
    d = ImageDraw.Draw(big)
    cy = int(h * (0.62 if lock else 0.5))
    r = int(w * 0.30)
    d.ellipse([w / 2 - r, cy - r, w / 2 + r, cy + r], outline=255, width=max(4, w // 300))
    big = big.filter(ImageFilter.GaussianBlur(w / 700))
    return Image.composite(Image.new("RGB", size, (90, 91, 94)), img, big)


def wp_contour(size, lock):
    w, h = size
    rng = np.random.default_rng(7 if lock else 8)
    z = gaussian_filter(rng.normal(size=(h // 8, w // 8)), sigma=w / 90)
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    fig.patch.set_facecolor(np.array(BG) / 255)
    ax.contour(z, levels=22, colors=[np.array((74, 75, 78)) / 255], linewidths=1.4 * w / 1320)
    ax.set_xlim(0, z.shape[1] - 1); ax.set_ylim(0, z.shape[0] - 1)
    fig.canvas.draw()
    img = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB")
    plt.close(fig)
    img = img.resize(size)
    if lock:  # keep the clock area calm
        mask = vgrad(size, (255, 255, 255), (0, 0, 0)).convert("L").point(lambda v: 255 if v > 150 else int(v * 1.7))
        img = Image.composite(Image.new("RGB", size, BG), img, mask)
    return grain(img, 3.0, 3)


WALLS = [("01_matte", wp_matte), ("02_fade", wp_fade), ("03_line", wp_line),
         ("04_words", wp_words), ("05_ring", wp_ring), ("06_contour", wp_contour)]


def icon(glyph, tone, px=1024):
    tile, ink = TONES[tone]
    img = Image.new("RGB", (px, px), tile)
    d = ImageDraw.Draw(img)
    f = sym_font(int(px * 0.46), 300)
    m = Image.new("L", (px * 2, px * 2), 0)
    ImageDraw.Draw(m).text((px // 2, px // 2), glyph, font=f, fill=255)
    l, t, r, b = m.getbbox()  # actual ink, not font metrics
    glyph_img = m.crop((l, t, r, b))
    gw, gh = glyph_img.size
    img.paste(Image.new("RGB", (gw, gh), ink), ((px - gw) // 2, (px - gh) // 2), glyph_img)
    return img


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    cp = codepoints()
    for dev, size in SIZES.items():
        for kind, lock in (("home", False), ("lock", True)):
            p = os.path.join(OUT, f"wallpapers_{dev}", kind)
            os.makedirs(p, exist_ok=True)
            for name, fn in WALLS:
                fn(size, lock).save(os.path.join(p, f"{name}_{kind}.jpg"), quality=93, subsampling=0)
    for tone in TONES:
        p = os.path.join(OUT, "icons", tone)
        os.makedirs(p, exist_ok=True)
        for fname, sym in ICONS:
            icon(cp[sym], tone).save(os.path.join(p, f"{fname}.png"), optimize=True)
    lic = os.path.join(OUT, "licences")
    os.makedirs(lic, exist_ok=True)
    shutil.copy(os.path.join(V, "LICENSE.txt"), os.path.join(lic, "Material_Symbols_Apache-2.0.txt"))
    shutil.copy(os.path.join(V, "Inter_OFL.txt"), os.path.join(lic, "Inter_OFL.txt"))
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"kit: {n} files -> {OUT}")


if __name__ == "__main__":
    build()
