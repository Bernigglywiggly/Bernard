"""THE MARGIN · the ledger look on the shared engine: engine.film.main(..., look_mod=ledger, cap_mod=ledger.CAPTIONS).

No characters, no glow: the scenes draw straight onto a navy-black page ruled like a ledger (lab/ch2/look.py has the
palette, type and the recurring objects), labels are drawn crisp, the furniture is the channel name top left and the
floor top right, and the captions are set in IBM Plex Serif on a navy band, each word turning paper-white as it's said.

    import ch2.ledger as ledger
    ledger.FLOORS[:] = ["THE PRICE", "THE MACHINE", ...]     # the episode's floor names, from its script
"""
import numpy as np

import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402

W, H, FPS = tl.W, tl.H, tl.FPS
BRAND = "THE MARGIN"                # the channel's name on screen: change it here (working name; see BIBLE.md)
FLOORS = []
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
_BG = {}


def background():
    if "img" not in _BG:
        s = skia.Surface(W, H)
        L.ground(s.getCanvas())
        _BG["img"] = s.makeImageSnapshot()
    return _BG["img"]


def current_floor(t):
    live = [ln for ln in tl.L if ln["start"] - 0.4 <= t]
    return live[-1]["floor"] if live else 0


def furniture(c, t):
    L.text(c, BRAND, 190, 70, L.font(L.MONO_M, 20), L.fill(L.BRASS, 0.9), track=0.22)
    if FLOORS and tl.L:
        f = current_floor(t)
        if 0 <= f < len(FLOORS):
            L.text(c, f"{ROMAN[f]} · {FLOORS[f]}", W - 80, 70, L.font(L.MONO, 20), L.fill(L.MUTED, 0.9), "right", track=0.22)


def compose(scenes, t, captions=None):
    """One finished frame: the ruled page, the scene, the furniture, and (optionally) the captions."""
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.drawImage(background(), 0, 0)
    tl.LABELS["mode"] = "draw"
    scenes.frame(c, t)
    furniture(c, t)
    if captions:
        captions(c, t)
    return s.makeImageSnapshot()


class _Captions:
    """The line being said, bottom centre: Plex Serif on a navy band; words not yet said in muted ink."""
    def __init__(self):
        self.f = None

    def draw(self, c, t, until=None):
        from engine.captions import word_times
        live = [ln for ln in tl.L if ln["start"] - 0.05 <= t <= ln["end"] + 0.25 and (until is None or ln["start"] < until)]
        if not live:
            return
        ln = live[-1]
        if self.f is None:
            self.f = L.font(L.SERIF, 40)
        f = self.f
        wt = word_times(ln)
        rows, cur = [], []
        for w in wt:
            if f.measureText(" ".join(x[0] for x in cur + [w])) > 1380 and cur:
                rows.append(cur)
                cur = [w]
            else:
                cur.append(w)
        rows.append(cur)
        lead = 54
        y0 = H - 128 - (len(rows) - 1) * lead
        wmax = max(f.measureText(" ".join(x[0] for x in r)) for r in rows)
        c.drawRoundRect(skia.Rect.MakeXYWH(W / 2 - wmax / 2 - 28, y0 - 44, wmax + 56, (len(rows) - 1) * lead + 66), 6, 6,
                        L.fill("#070B12", 0.78))
        c.drawLine(W / 2 - wmax / 2 - 28, y0 - 44, W / 2 + wmax / 2 + 28, y0 - 44, L.stroke(L.BRASS, 1.2, 0.5))
        for li, ws in enumerate(rows):
            s_ = " ".join(x[0] for x in ws)
            x = W / 2 - f.measureText(s_) / 2
            for w, a, _ in ws:
                c.drawString(w, x, y0 + li * lead, f, L.fill(L.PAPER if t >= a - 0.02 else L.MUTED, 1.0 if t >= a - 0.02 else 0.75))
                x += f.measureText(w + " ")


CAPTIONS = _Captions()


def style_shorts():
    """The vertical shorts in the channel's own dress: THE MARGIN, brass for the live word and the progress line,
    serif for the hook and captions (engine/shorts.py reads these module values when it draws)."""
    from engine import shorts
    shorts.BRAND = BRAND
    shorts.TURQ, shorts.WHITE, shorts.SOFT = L.BRASS, L.PAPER, L.MUTED
    shorts.F.clear()
    shorts.F.update(hook=L.font(L.SERIF_M, 66), cap=L.font(L.SERIF_M, 78), tag=L.font(L.MONO_M, 26), end=L.font(L.MONO_M, 32))
