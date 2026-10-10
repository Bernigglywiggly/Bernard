"""HOW THEY PROFIT · EP06 · THE COMPANY THAT NEVER TOUCHES YOUR MONEY (Visa): the film, on the shared engine with the ledger look (ch2/ledger.py).
Voice: Higgsfield Seed Audio "Sterling" (there's no ElevenLabs key), one take per floor cut back into lines:

    cd lab && python3 -m engine.voice_hf ch2/ep06 reqs    (submit build/hf_reqs.json, record the takes in hf_voice.json)
    cd lab && python3 -m engine.voice_hf ch2/ep06 fetch && python3 -m engine.voice_hf ch2/ep06 build
    then  python3 film.py parts 4 0 4 · join 4 · sound · master, and  cd lab && python3 ch2/endcard.py ep06
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import engine.film  # noqa: E402
import ch2.ledger as ledger  # noqa: E402
from script import FLOORS  # noqa: E402

ledger.FLOORS[:] = FLOORS
ledger.style_shorts()
TAGS = "#money #visa #payments #business #explained #howtheyprofit"
CLIPS = []          # Shorts are cut after the voice exists (five, each a different shape: CRAFT.md §1)
MUSIC = [(0.0, "intro"), ("four", "a"), ("fee", "b"), ("meters", "a"), ("back", "b"), ("thin", "a"), ("weak", "intro"),
         ("end", "out")]

if __name__ == "__main__":
    os.environ.setdefault("EL_VOICE", "elder")
    engine.film.main(__file__, title="HOW THEY PROFIT  ·  THE COMPANY THAT NEVER TOUCHES YOUR MONEY", music=MUSIC,
                     anchors=("scale", "cents"), clips=CLIPS, tags=TAGS, bed="chrome_marl", look_mod=ledger,
                     cap_mod=ledger.CAPTIONS)
