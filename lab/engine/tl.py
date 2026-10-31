"""The timeline: every line's start and end (and George's word times) from <ep>/build/lines.json, by line id, so a new
voice re-times the whole film; plus the two queues the picture fills while it draws: sound events (the mix plays
them) and small labels (the look types them on, crisp, over the characters)."""
import json
import os
import re

import numpy as np

W, H, FPS = 1920, 1080, 24
EP = {"dir": None, "build": None, "meta": None, "title": "", "name": ""}
L, IDS, EVENTS = [], [], []
LABELS = {"mode": "draw", "queue": []}


def load(ep_dir, title=""):
    d = os.path.abspath(ep_dir)
    b = os.path.join(d, os.environ.get("EP_BUILD", "build"))             # EP_BUILD: a variant's own folder
    EP.update(dir=d, build=b, title=title, name=os.path.basename(d))
    p = os.path.join(b, "lines.json")
    EP["meta"] = json.load(open(p)) if os.path.exists(p) else {"lines": [], "total": 0.0}
    L[:] = EP["meta"]["lines"]
    IDS[:] = [x.get("id") for x in L]
    return EP["meta"]


def I(name):
    return IDS.index(name)


def ls(name):
    return L[I(name)]["start"]


def le(name):
    return L[I(name)]["end"]


def at(name, frac):
    """A time a fraction of the way through a line."""
    return ls(name) + frac * (le(name) - ls(name))


def nxt(name):
    """The start of the line after this one (or this one's end + 3 s)."""
    i = I(name)
    return L[i + 1]["start"] if i + 1 < len(L) else L[i]["end"] + 3.0


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word(name, w, k=0, end=False):
    """When George says word w (its k-th time) in line `name`: exact from the ElevenLabs timings (the spoken text, so
    numbers are words: "thirteen"), else estimated from the word's place in the line."""
    ln = L[I(name)]
    ws = ln.get("words") or []
    hits = [x for x in ws if _norm(x[0]) == _norm(w)]
    if len(hits) > k:
        return hits[k][2] if end else hits[k][1]
    shown = [_norm(x) for x in ln["text"].split()]
    idx = [i for i, x in enumerate(shown) if x == _norm(w)]
    if len(idx) > k:
        return at(name, (idx[k] + (1.0 if end else 0.0)) / max(1, len(shown)))
    raise KeyError(f"{w!r} not in line {name!r}")


def end_time(tail=3.0):
    return L[-1]["end"] + tail if L else 0.0


def ev(t_evt, kind, now, x=None):
    """Record a sound event once, on the frame it happens (the mix places the sound; x pans it)."""
    if now - 1 / FPS < t_evt <= now:
        EVENTS.append((round(t_evt, 3), kind, 0.0 if x is None else float(np.clip((x - W / 2) / (W / 2), -0.8, 0.8))))


def label(c, s, x, y, t, t0, size=20, col=None, align="center", a=1.0, cps=None):
    """A small monospace label: queued and typed on crisp over the characters (t0 < 0: shown whole, a live counter);
    cps is its typing speed. Drawn directly only for quick line-art stills."""
    import mograph as mg
    col = col or mg.ON_DARK_SOFT
    if LABELS["mode"] == "skip":
        return
    if LABELS["mode"] == "collect":
        LABELS["queue"].append((s, x, y, t, t0, size, col, align, a, cps))
        return
    if t >= max(0.0, t0):
        f = mg.font(mg.MONO_M, size)
        w = f.measureText(s)
        x0 = x - w / 2 if align == "center" else x - w if align == "right" else x
        c.drawString(s, x0, y, f, mg.fill(col, a))
