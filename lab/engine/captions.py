"""The 16:9 captions (EP03's): the line's words at the bottom on a dark box, at most two rows, each word turning
white as George says it (his word timings; spread evenly when a line has none)."""
import engine  # noqa: F401  (paths)
import mograph as mg  # noqa: E402
import skia  # noqa: E402

from engine import tl  # noqa: E402

W, H = tl.W, tl.H
F = {}


def word_times(ln):
    """(word, start, end) for the caption text: displayed words take George's timings by position when the spoken
    words differ (a date read out as words)."""
    shown = ln["text"].split()
    spoken = ln.get("words") or []
    if not spoken:
        d = (ln["end"] - ln["start"]) / max(1, len(shown))
        return [(w, ln["start"] + i * d, ln["start"] + (i + 1) * d) for i, w in enumerate(shown)]
    n, m = len(shown), len(spoken)
    starts = [spoken[int(round(i * (m - 1) / max(1, n - 1))) if n > 1 else 0][1] for i in range(n)]
    out = []
    for i, w in enumerate(shown):
        e_ = starts[i + 1] - 0.02 if i + 1 < n else spoken[-1][2]
        out.append((w, starts[i], max(e_, starts[i] + 0.05)))
    return out


def draw(c, t, until=None):
    live = [ln for ln in tl.L if ln["start"] - 0.05 <= t <= ln["end"] + 0.25 and (until is None or ln["start"] < until)]
    if not live:
        return
    ln = live[-1]                                     # the newest line wins, so two never overlap at a hand-over
    if "f" not in F:
        F["f"] = mg.font(mg.BODY_M, 38)
    f = F["f"]
    wt = word_times(ln)
    rows, cur = [], []
    for w in wt:
        if f.measureText(" ".join(x[0] for x in cur + [w])) > 1400 and cur:
            rows.append(cur); cur = [w]
        else:
            cur.append(w)
    rows.append(cur)
    y0 = H - 150 - (len(rows) - 1) * 48
    for li, ws in enumerate(rows):
        s = " ".join(x[0] for x in ws)
        wtot = f.measureText(s)
        x = W / 2 - wtot / 2
        c.drawRoundRect(skia.Rect.MakeXYWH(x - 18, y0 + li * 48 - 36, wtot + 36, 50), 10, 10, mg.fill("#0B0C0E", 0.55))
        for w, a, _ in ws:
            c.drawString(w, x, y0 + li * 48, f, mg.fill("#FFFFFF" if t >= a - 0.02 else mg.ON_DARK_SOFT, 1.0))
            x += f.measureText(w + " ")
