"""GUIDE.md -> out/kit/Low-Stim_Phone_Kit_Guide.pdf (A5-ish pages, graphite on stone).

    ~/youtube/.venv/bin/python guide_pdf.py
Handles: # title, ## heading, ### subheading, - bullets, 1. steps, plain paragraphs, **bold** (stripped).
"""
import os, re
from PIL import Image, ImageDraw
import make

SRC = os.path.join(make.HERE, "GUIDE.md")
DST = os.path.join(make.OUT, "Low-Stim_Phone_Kit_Guide.pdf")
PW, PH = 1240, 1754            # A5 at 150 dpi x 1.414
M = 110
BG = (236, 234, 229)
INK = (38, 39, 41)
SOFT = (110, 111, 114)
TAG = {"[iOS]": (70, 72, 76), "[Android]": (96, 98, 102)}


def clean(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", s)
    return s.strip()


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


class Doc:
    def __init__(self):
        self.pages = []
        self.f = {"h1": make.inter(66, 650), "h2": make.inter(44, 600), "h3": make.inter(34, 600),
                  "p": make.inter(29, 400), "tag": make.inter(22, 600), "foot": make.inter(20, 400)}
        self.new()

    def new(self):
        self.img = Image.new("RGB", (PW, PH), BG)
        self.d = ImageDraw.Draw(self.img)
        self.y = M
        self.pages.append(self.img)
        n = len(self.pages)
        self.d.text((M, PH - 70), f"Low-Stim Phone Kit · {n}", font=self.f["foot"], fill=SOFT)

    def need(self, h):
        if self.y + h > PH - 130:
            self.new()

    def text(self, s, style, indent=0, gap=12, colour=INK, bullet=None):
        f = self.f[style]
        lh = int(f.size * 1.42)
        tags = [t for t in TAG if s.startswith(t)]
        lines = wrap(self.d, s, f, PW - 2 * M - indent - (40 if bullet else 0))
        self.need(lh * min(len(lines), 3))
        x = M + indent
        if bullet:
            self.d.text((x, self.y), bullet, font=f, fill=SOFT)
            x += 40
        for i, ln in enumerate(lines):
            self.need(lh)
            if i == 0 and tags:
                t = tags[0]
                ln = ln[len(t):].lstrip()
                tw = self.d.textlength(t[1:-1], font=self.f["tag"]) + 24
                self.d.rounded_rectangle([x, self.y + 4, x + tw, self.y + 40], 10, fill=TAG[t])
                self.d.text((x + 12, self.y + 9), t[1:-1], font=self.f["tag"], fill=(230, 230, 230))
                self.d.text((x + tw + 14, self.y), ln, font=f, fill=colour)
            else:
                self.d.text((x, self.y), ln, font=f, fill=colour)
            self.y += lh
        self.y += gap


def build():
    doc = Doc()
    first_h1 = True
    for raw in open(SRC, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.strip() == "---":
            doc.y += 10
            continue
        if line.startswith("# "):
            if not first_h1:
                doc.new()
            first_h1 = False
            doc.text(clean(line[2:]), "h1", gap=30)
        elif line.startswith("## "):
            doc.need(220)
            doc.y += 24
            doc.text(clean(line[3:]), "h2", gap=16)
        elif line.startswith("### "):
            doc.need(160)
            doc.y += 10
            doc.text(clean(line[4:]), "h3", gap=10)
        elif re.match(r"^\s*[-*] ", line):
            ind = 40 if line.startswith("  ") else 0
            doc.text(clean(re.sub(r"^\s*[-*] ", "", line)), "p", indent=ind, bullet="–", gap=6)
        elif re.match(r"^\s*\d+\. ", line):
            m = re.match(r"^\s*(\d+)\. (.*)", line)
            doc.text(clean(m.group(2)), "p", bullet=m.group(1) + ".", gap=6)
        elif line.startswith("|"):
            if set(line.replace("|", "").strip()) <= set("-: "):
                continue
            cells = [clean(c) for c in line.strip("|").split("|")]
            doc.text("   ·   ".join(c for c in cells if c), "p", gap=4)
        elif line.startswith(">"):
            doc.text(clean(line.lstrip("> ")), "p", indent=30, colour=SOFT)
        else:
            doc.text(clean(line), "p")
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    doc.pages[0].save(DST, save_all=True, append_images=doc.pages[1:], resolution=150)
    print(f"{len(doc.pages)} pages -> {DST}")


if __name__ == "__main__":
    build()
