"""Thumbnails for the Ponzi film (1280x720, under 2 MB), three to A/B with YouTube's Test & Compare:

    a  the real 1920 photograph (boater and cane) over the queue, "50% IN 45 DAYS" stamped across (the promise)
    b  "HE GAVE THE SCAM ITS NAME." in serif beside the queue (the claim; he didn't invent the trick)
    c  the police photograph over the crowd at the run, "INSOLVENT" stamped beside it (the Post's verdict)

    python3 thumb.py   -> out/thumb_a.jpg, thumb_b.jpg, thumb_c.jpg
"""
import os
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import doc  # noqa: E402

TW, TH = 1280, 720
BASE = os.path.join(HERE, "src", "ai", "o01.png")


def canvas():
    surf = skia.Surface(TW, TH)
    return surf, surf.getCanvas()


def base(c, cx=0.5, cy=0.5, z=1.0, punch=1.15):
    img = doc.image(BASE)
    p = skia.Paint(AntiAlias=True)
    k = punch                                              # a little more contrast and warmth than the film
    p.setColorFilter(skia.ColorFilters.Matrix([k * 1.04, 0, 0, 0, -0.06, 0, k, 0, 0, -0.06, 0, 0, k * 0.94, 0, -0.06,
                                               0, 0, 0, 1, 0]))
    doc.draw_cover(c, img, cx, cy, z, p, (0, 0, TW, TH))
    g = skia.GradientShader.MakeRadial((TW * 0.5, TH * 0.5), TW * 0.75, [0x00000000, 0xAA000000])
    c.drawRect(skia.Rect.MakeWH(TW, TH), skia.Paint(Shader=g))


def stamp(c, s, x, y, size, rot, col=0xFFD8261A):
    f = skia.Font(doc.FONT["cap"], size)
    tw = f.measureText(s)
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    box = skia.Rect.MakeLTRB(-tw / 2 - 26, -size * 0.86, tw / 2 + 26, size * 0.2)
    c.drawRect(box.makeOffset(6, 8), doc.shadow(0.7, 16))
    c.drawRect(box, doc.P(0x66000000))
    c.drawRect(box, doc.P(col, Style=skia.Paint.kStroke_Style, StrokeWidth=12))
    c.drawString(s, -tw / 2, 0, f, doc.P(col))
    c.restore()


def save(surf, name):
    out = os.path.join(HERE, "out", name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    arr = surf.makeImageSnapshot().toarray()[:, :, :3]
    import cv2
    cv2.imwrite(out, arr, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(out, round(os.path.getsize(out) / 1024), "KB")


def print_(c, f, x, y, hfrac, rot, grade="bw"):
    """An archive photograph as a print with a shadow, centred at (x, y), hfrac of the frame tall."""
    img = doc.image(os.path.join(HERE, "src", "arch", f))
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(doc.grade_filter(grade))
    s = TH * hfrac / img.height()
    w, h = img.width() * s, img.height() * s
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    r = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)
    c.drawRect(r.makeOffset(10, 14), doc.shadow(0.8, 20))
    c.drawRect(r.makeOutset(10, 10), doc.P(0xFFEDE4D0))
    c.drawImageRect(img, r, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()


def a():
    surf, c = canvas()
    base(c, 0.62, 0.5, 1.1)
    print_(c, "ponzi_1920.jpg", 330, 372, 0.84, -3)
    stamp(c, "50% IN 45 DAYS", 860, 600, 92, -7)
    save(surf, "thumb_a.jpg")


def b():
    surf, c = canvas()
    base(c, 0.35, 0.5, 1.05)
    c.drawRect(skia.Rect.MakeXYWH(TW * 0.45, 0, TW * 0.55, TH),
               skia.Paint(Shader=skia.GradientShader.MakeLinear([(TW * 0.45, 0), (TW * 0.66, 0)], [0x00000000, 0xD8000000])))
    f = skia.Font(doc.FONT["serif"], 96)
    for i, line in enumerate(["HE GAVE", "THE SCAM", "ITS NAME."]):
        y = 230 + i * 108
        doc.text(c, line, 1236, y + 5, f, doc.shadow(0.9, 12), align="right")
        doc.text(c, line, 1232, y, f, doc.P(0xFFF1E6CF if i < 2 else 0xFFE2B866), align="right")
    save(surf, "thumb_b.jpg")


def c_():
    surf, c = canvas()
    img = doc.image(os.path.join(HERE, "src", "ai", "r01.png"))
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(skia.ColorFilters.Matrix([1.1, 0, 0, 0, -0.05, 0, 1.06, 0, 0, -0.05, 0, 0, 1.0, 0, -0.05, 0, 0, 0, 1, 0]))
    doc.draw_cover(c, img, 0.6, 0.5, 1.08, p, (0, 0, TW, TH))
    g = skia.GradientShader.MakeRadial((TW * 0.5, TH * 0.5), TW * 0.75, [0x00000000, 0xAA000000])
    c.drawRect(skia.Rect.MakeWH(TW, TH), skia.Paint(Shader=g))
    c.drawRect(skia.Rect.MakeXYWH(TW * 0.5, 0, TW * 0.5, TH),
               skia.Paint(Shader=skia.GradientShader.MakeLinear([(TW * 0.5, 0), (TW * 0.68, 0)], [0x00000000, 0xD8000000])))
    print_(c, "ponzi_5247.jpg", 360, 360, 0.82, 3)
    stamp(c, "INSOLVENT", 1000, 560, 90, -7)
    f = skia.Font(doc.FONT["serif"], 84)
    for i, line in enumerate(["THE ORIGINAL", "PONZI SCHEME"]):
        y = 300 + i * 96
        doc.text(c, line, 1236, y + 5, f, doc.shadow(0.9, 12), align="right")
        doc.text(c, line, 1232, y, f, doc.P(0xFFF1E6CF if i == 0 else 0xFFE2B866), align="right")
    save(surf, "thumb_c.jpg")


if __name__ == "__main__":
    a()
    b()
    c_()
