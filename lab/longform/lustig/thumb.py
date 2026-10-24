"""Thumbnails for the long-form (1280x720, under 2 MB), three to A/B with YouTube's Test & Compare:

    a  "SOLD" stamped over the tower, Lustig with the key (the hook in one word)
    b  "HE SOLD THE EIFFEL TOWER" in serif beside him (the title as a claim)
    c  the real 1935 newspaper clipping, "SMOOTHEST CON MAN EVER BORN" (the archive as proof)

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
BASE = os.path.join(HERE, "src", "ai", "th1.png")


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


def a():
    """Lustig on the left, the tower filling the right, SOLD across the tower's legs."""
    surf, c = canvas()
    tower = doc.image(os.path.join(HERE, "src", "ai", "o06.png"))
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(skia.ColorFilters.Matrix([1.18, 0, 0, 0, -0.05, 0, 1.12, 0, 0, -0.05, 0, 0, 1.05, 0, -0.05, 0, 0, 0, 1, 0]))
    doc.draw_cover(c, tower, 0.53, 0.42, 1.55, p, (520, 0, TW - 520, TH))
    img = doc.image(BASE)
    q = skia.Paint(AntiAlias=True)
    q.setColorFilter(skia.ColorFilters.Matrix([1.15, 0, 0, 0, -0.05, 0, 1.1, 0, 0, -0.05, 0, 0, 1.0, 0, -0.05, 0, 0, 0, 1, 0]))
    c.saveLayer(skia.Rect.MakeWH(TW, TH))                     # Lustig, fading out into the tower
    doc.draw_cover(c, img, 0.22, 0.5, 1.12, q, (0, 0, 760, TH))
    c.drawRect(skia.Rect.MakeWH(TW, TH), skia.Paint(BlendMode=skia.BlendMode.kDstIn, Shader=skia.GradientShader.MakeLinear(
        [(540, 0), (760, 0)], [0xFF000000, 0x00000000])))
    c.restore()
    stamp(c, "SOLD", 965, 560, 190, -10)
    save(surf, "thumb_a.jpg")


def b():
    surf, c = canvas()
    base(c, 0.42, 0.5, 1.05)
    c.drawRect(skia.Rect.MakeXYWH(TW * 0.52, 0, TW * 0.48, TH),
               skia.Paint(Shader=skia.GradientShader.MakeLinear([(TW * 0.52, 0), (TW * 0.7, 0)], [0x00000000, 0xCC000000])))
    f = skia.Font(doc.FONT["serif"], 92)
    for i, line in enumerate(["HE SOLD", "THE EIFFEL", "TOWER."]):
        y = 230 + i * 104
        doc.text(c, line, 1236, y + 5, f, doc.shadow(0.9, 12), align="right")
        doc.text(c, line, 1232, y, f, doc.P(0xFFF1E6CF if i < 2 else 0xFFE2B866), align="right")
    save(surf, "thumb_b.jpg")


def c_():
    surf, c = canvas()
    c.drawRect(skia.Rect.MakeWH(TW, TH), doc.P(0xFF14110D))
    clip = doc.image(os.path.join(HERE, "src", "arch", "lustig_1935.jpg"))
    p = skia.Paint(AntiAlias=True)
    p.setColorFilter(doc.grade_filter("bw"))
    s = TH * 0.92 / clip.height()
    w, h = clip.width() * s, clip.height() * s
    c.save()
    c.translate(330, TH / 2)
    c.rotate(-3)
    r = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)
    c.drawRect(r.makeOffset(10, 14), doc.shadow(0.8, 20))
    c.drawImageRect(clip, r, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()
    img = doc.image(BASE)
    pp = skia.Paint(AntiAlias=True)
    doc.draw_cover(c, img, 0.3, 0.45, 1.25, pp, (660, 0, TW - 660, TH))
    c.drawRect(skia.Rect.MakeXYWH(660, 0, 40, TH), skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(660, 0), (700, 0)], [0xFF14110D, 0x0014110D])))
    stamp(c, "1935", 520, 650, 86, -8, col=0xFFD8261A)
    save(surf, "thumb_c.jpg")


if __name__ == "__main__":
    a()
    b()
    c_()
