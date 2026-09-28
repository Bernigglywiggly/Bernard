"""Type-on text, one schedule for the picture and the sound: the characters of a label appear at these times and a
mechanical key (lab/sfx/detail.py) lands on each one, so what you see typing is what you hear typing. The rhythm is
human (a touch uneven, a beat longer after a space) but fixed per text, so every render agrees with itself."""
import zlib

import numpy as np

CPS = 17.0                                         # characters a second: quick, but you can hear every key


def schedule(text, t0, cps=CPS):
    """The time each character of text appears, starting at t0."""
    r = np.random.default_rng(zlib.crc32(text.encode()))
    base = 1.0 / cps
    gaps = np.clip(r.normal(base, 0.22 * base, max(0, len(text) - 1)), 0.55 * base, 1.8 * base)
    for i in range(len(gaps)):
        if text[i] == " ":
            gaps[i] *= 1.25
        if text[i + 1] in "·,":
            gaps[i] *= 1.3
    return t0 + np.concatenate([[0.0], np.cumsum(gaps)])


def shown(text, t0, t, cps=CPS):
    """How many characters are on screen at t."""
    if t < t0:
        return 0
    return int(np.searchsorted(schedule(text, t0, cps), t, side="right"))
