"""THE MARGIN · EP03 · THE $65 MEMBERSHIP: the film, on the shared engine with the ledger look (ch2/ledger.py).
Voice: Curve Elder A, so every command runs with EL_VOICE=elder (the voice step needs ELEVENLABS_API_KEY):

    EL_VOICE=elder python3 film.py voice      then  parts 4 0 4 · join 4 · sound · master
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import engine.film  # noqa: E402
import ch2.ledger as ledger  # noqa: E402
from script import FLOORS  # noqa: E402

ledger.FLOORS[:] = FLOORS
TAGS = "#money #costco #membership #retail #business #explained #themargin"
CLIPS = []                                                 # shorts in the ledger look: next (engine/shorts.py is The Curve's)
MUSIC = [(0.0, "intro"), ("door", "a"), ("year", "b"), ("why", "a"), ("you", "b"), ("imagine", "intro"), ("then", "a"),
         ("end", "out")]

if __name__ == "__main__":
    os.environ.setdefault("EL_VOICE", "elder")
    engine.film.main(__file__, title="THE MARGIN  ·  THE $65 MEMBERSHIP", music=MUSIC, anchors=("door", "why"),
                     clips=CLIPS, tags=TAGS, bed="chrome_marl", look_mod=ledger, cap_mod=ledger.CAPTIONS)
