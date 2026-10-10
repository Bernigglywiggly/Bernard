"""Jazz for the true-story films (3 Oct, the user: "replace with jazz or house jazz for these sorts of vids, futuristic
bg music dont match"). Kevin MacLeod's jazz from incompetech.com, licensed CC BY 4.0: free on monetised YouTube as long
as each title's credit line is in the description (`credits(titles)`). The MP3s stay out of git; `fetch()` downloads them
into src/. `section()` cuts one stretch, at 48 kHz stereo, with a small dip around 2.5 kHz to leave room for the voice.

    python3 library.py        -> fetch every track
"""
import os
import subprocess
import sys
import urllib.parse

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import audio_fx as fx  # noqa: E402

BASE = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/"
# title -> (file on incompetech, what it is)
TRACKS = {
    "Covert Affair": ("Covert Affair.mp3", "heist jazz: electric piano, trumpet, brushes"),
    "No Good Layabout": ("NoGoodLayabout.mp3", "walking bass, piano, clarinet; a young hustler"),
    "Spy Glass": ("Spy Glass.mp3", "mysterious combo with sax and vibes"),
    "I Knew a Guy": ("I Knew a Guy.mp3", "slow walking bass, vibes; scheming"),
    "Dances and Dames": ("Dances and Dames.mp3", "film-noir suspense, building"),
    "Hard Boiled": ("Hard Boiled.mp3", "noir piano trio"),
    "Opportunity Walks": ("Opportunity Walks.mp3", "up-tempo two-piano combo"),
    "On the Cool Side": ("On the Cool Side.mp3", "dark, uneasy: trumpet and tenor"),
    "Cool Blast": ("Cool Blast.mp3", "dance-jazz, the house-jazz colour"),
    "Walking Along": ("Walking Along.mp3", "brushes, bass, vibes; calm before trouble"),
    "Faster Does It": ("Faster Does It.mp3", "frantic acoustic bass and drums"),
    "Night on the Docks - Trumpet": ("Night on the Docks - Trumpet.mp3", "sad, smooth; 1950s detective"),
    "Night on the Docks - Sax": ("Night on the Docks - Sax.mp3", "sad, smooth; tenor"),
    "Acid Trumpet": ("AcidJazz.mp3", "acid jazz: electric piano, muted trumpet"),
    "Bass Walker": ("Bass Walker.mp3", "upright walking bass alone"),
    "Deadly Roulette": ("Deadly Roulette.mp3", "gumshoe mystery groove"),
}
CREDIT = ('"{t}" Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0 License, '
          "http://creativecommons.org/licenses/by/4.0/")


def path(title):
    return os.path.join(HERE, "src", title + ".mp3")


def fetch(titles=None):
    os.makedirs(os.path.join(HERE, "src"), exist_ok=True)
    for t in titles or TRACKS:
        if not os.path.exists(path(t)):
            subprocess.run(["curl", "-s", "-f", "-m", "120", "-o", path(t), BASE + urllib.parse.quote(TRACKS[t][0])],
                           check=True)


def length(title):
    fetch([title])
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path(title)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def section(title, dur, align="start", offset=0.0):
    """`dur` seconds of the track: from `offset` (align='start'), or ending on the track's own last note ('end')."""
    fetch([title])
    if align == "end":
        offset = max(0.0, length(title) - dur - 0.5)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{offset:.3f}", "-t", f"{dur:.3f}", "-i", path(title), "-f", "f32le",
                          "-ac", "2", "-ar", str(fx.SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    return fx.bq(x, "peak", 2500, q=0.8, gain_db=-2.5)


def credits(titles):
    return [CREDIT.format(t=t) for t in dict.fromkeys(titles)]


def credit_line(titles):
    """One line for a description: every title, the author, the source, the licence and its link."""
    names = ", ".join(f'"{t}"' for t in dict.fromkeys(titles))
    return (f"Music by Kevin MacLeod (incompetech.com): {names}. Licensed under Creative Commons: By Attribution 4.0, "
            "http://creativecommons.org/licenses/by/4.0/ (cut and mixed under the narration).")


if __name__ == "__main__":
    fetch()
    for t in TRACKS:
        print(f"{t:30s} {length(t):6.1f}s")
