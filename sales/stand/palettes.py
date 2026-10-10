#!/usr/bin/env python3
"""A colourway per shop for the review stand, taken from the shop's own branding: the logo or icon on its website
(sales/reels/contacts.csv), else a default by trade, marked so it gets checked against the shop sign.

    python3 sales/stand/palettes.py [--town Stone]     # -> sales/stand/palettes.json (+ build/logos/<id>.png)

Each entry: bg (card colour), acc (stars, rule and tap ring), source ("logo" | "theme-color" | "default"), swatches
(what was found, most common first) and url. A photo of the shop front always beats this: put the two hex values in
OVERRIDES below and re-run.
"""
import colorsys
import csv
import io
import json
import os
import re
import sys
from urllib.parse import urljoin

import numpy as np
import requests
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"}
OVERRIDES = {           # id -> (bg, acc), read by eye from the real logo or a photo of the sign
    "1195796": ('#1B6B3A', '#F0683C'),   # Crown Of India
    "1195354": ('#232323', '#F4EFE4'),   # Bear Coffee Company Ltd
    "1195901": ('#25333E', '#A9C4A4'),   # Little Seeds Bar & Kitchen
    "1195552": ('#C4121A', '#F4EFE4'),   # The Ovilash Restaurant
}
DEFAULTS = [            # trade (matched on name + cuisine) -> bg, acc
    (r"fish|chip", ("#12305A", "#F2C230")), (r"tea|cafe|café|coffee|bakery|sandwich|oatcake|roll", ("#F4EFE4", "#B5651D")),
    (r"pizza|pasta|ital", ("#7A1E1E", "#F2C230")), (r"india|tandoor|spice|balti|curry", ("#5A1230", "#E8B23A")),
    (r"chin|wok|canton|noodle|asian|sushi", ("#8C1C13", "#E8B23A")), (r"kebab|grill|burger|bun|chicken|peri", ("#17181B", "#E4572E")),
]


def hx(rgb):
    return "#%02X%02X%02X" % tuple(int(round(v)) for v in rgb)


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hsv(c):
    return colorsys.rgb_to_hsv(*(v / 255 for v in c))


def swatches(img, k=6):
    """Most common colours of a logo, with transparent and near-white pixels dropped."""
    im = img.convert("RGBA")
    im.thumbnail((160, 160))
    a = np.asarray(im).reshape(-1, 4).astype(float)
    a = a[a[:, 3] > 200][:, :3]
    if len(a) < 50:
        return []
    q = Image.fromarray(a.reshape(1, -1, 3).astype("uint8"), "RGB").quantize(k, method=Image.Quantize.MEDIANCUT)
    pal = np.asarray(q.getpalette()[:k * 3]).reshape(-1, 3)
    counts = np.bincount(np.asarray(q).ravel(), minlength=k)
    return [(tuple(int(v) for v in pal[i]), counts[i] / counts.sum()) for i in np.argsort(-counts) if counts[i]]


def pick(sw):
    """bg = the main brand colour (not white, not grey unless nothing else); acc = the next colour that differs."""
    cols = [(c, w) for c, w in sw if w > 0.03]
    brand = [(c, w) for c, w in cols if not (hsv(c)[1] < 0.12 and hsv(c)[2] > 0.85)]
    if not brand:
        return None
    strong = [(c, w) for c, w in brand if hsv(c)[1] > 0.35 and hsv(c)[2] > 0.2] or brand
    bg = max(strong, key=lambda t: t[1])[0]
    rest = [c for c, _ in brand if sum(abs(x - y) for x, y in zip(c, bg)) > 120]
    acc = max(rest, key=lambda c: hsv(c)[1] * 0.6 + hsv(c)[2] * 0.4) if rest else None
    return bg, acc


def candidates(html, base):
    out = []
    for m in re.finditer(r"<img[^>]+>", html, re.I):
        tag = m.group(0)
        if re.search(r"logo|brand", tag, re.I):
            s = re.search(r'(?:data-src|src)=["\']([^"\']+)', tag, re.I)
            if s and not s.group(1).startswith("data:"):
                out.append(("logo", urljoin(base, s.group(1))))
    for rel in ("apple-touch-icon", "icon", "shortcut icon"):
        for m in re.finditer(r"<link[^>]+>", html, re.I):
            if re.search(rf'rel=["\'][^"\']*{rel}', m.group(0), re.I):
                s = re.search(r'href=["\']([^"\']+)', m.group(0), re.I)
                if s:
                    out.append(("logo", urljoin(base, s.group(1))))
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m:
        out.append(("logo", urljoin(base, m.group(1))))
    return out


def from_site(sid, url):
    r = requests.get(url, headers=UA, timeout=15)
    r.raise_for_status()
    for kind, u in candidates(r.text, r.url)[:6]:
        try:
            if u.lower().split("?")[0].endswith(".svg"):
                continue
            b = requests.get(u, headers=UA, timeout=15).content
            img = Image.open(io.BytesIO(b))
            sw = swatches(img)
            p = pick(sw)
            if p and not re.search(r"foodhub|dineorder|expireddomains|feedmeonline|flipdish|orderyoyo", u):
                os.makedirs(os.path.join(HERE, "build", "logos"), exist_ok=True)
                img.convert("RGBA").save(os.path.join(HERE, "build", "logos", f"{sid}.png"))
                return dict(bg=hx(p[0]), acc=hx(p[1]) if p[1] else None, source=kind, url=u, swatches=[hx(c) for c, _ in sw])
        except Exception:
            continue
    m = re.search(r'<meta[^>]+name=["\']theme-color["\'][^>]+content=["\'](#[0-9a-fA-F]{6})', r.text)
    if m and hsv(rgb(m.group(1)))[1] > 0.15:
        return dict(bg=m.group(1).upper(), acc=None, source="theme-color", url=r.url, swatches=[m.group(1).upper()])
    return None


def default(name, cuisine):
    text = f"{name} {cuisine}".lower()
    bg, acc = next((v for k, v in DEFAULTS if re.search(k, text)), ("#17181B", "#E8B23A"))
    return dict(bg=bg, acc=acc, source="default", url="", swatches=[])


def main(a):
    town = a[a.index("--town") + 1] if "--town" in a else None
    shops = {s["id"]: s for s in json.load(open(os.path.join(REPO, "sales", "prospects_routed.json")))}
    sites = {c["id"]: c["website"].strip() for c in csv.DictReader(open(os.path.join(REPO, "sales", "reels", "contacts.csv")))}
    path = os.path.join(HERE, "palettes.json")
    out = json.load(open(path)) if os.path.exists(path) else {}
    for sid, s in shops.items():
        if town and s["town"] != town:
            continue
        p = None
        if sid in OVERRIDES:
            p = dict(bg=OVERRIDES[sid][0], acc=OVERRIDES[sid][1], source="checked", url="", swatches=[])
        elif sites.get(sid):
            try:
                p = from_site(sid, sites[sid])
            except Exception as e:
                print(f"  ! {s['name']}: {type(e).__name__}")
        p = p or default(s["name"], s.get("cuisine", ""))
        out[sid] = dict(p, name=s["name"], town=s["town"])
        print(f"{s['name'][:30]:30} {p['source']:11} bg {p['bg']} acc {p['acc']}")
    json.dump(out, open(path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
