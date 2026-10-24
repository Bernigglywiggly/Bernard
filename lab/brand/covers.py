"""Platform covers cut from a YouTube banner (2560x1440, text inside the 1546x423 safe area): the centre band, scaled.

    python3 brand/covers.py <banner.png> <out_dir>   -> x_header_1500x500.jpg, facebook_cover_1640x624.jpg
"""
import os
import sys

from PIL import Image


def covers(banner, out):
    im = Image.open(banner).convert("RGB")
    w, h = im.size
    os.makedirs(out, exist_ok=True)
    for name, (tw, th) in (("x_header_1500x500", (1500, 500)), ("facebook_cover_1640x624", (1640, 624))):
        cw = 1700 * w // 2560                                # a little wider than the safe area
        ch = round(cw * th / tw)
        box = ((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2)
        im.crop(box).resize((tw, th), Image.LANCZOS).save(os.path.join(out, name + ".jpg"), quality=92)


if __name__ == "__main__":
    covers(sys.argv[1], sys.argv[2])
