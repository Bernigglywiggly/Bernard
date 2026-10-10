"""HOW THEY PROFIT (was The Margin) · EP01 · BANKS WITH WINGS: the film, on the shared engine with the ledger look (ch2/ledger.py).
Voice: Higgsfield Seed Audio "Sterling" (3 Oct; there's no ElevenLabs key), one take per floor cut back into lines:

    cd lab && python3 -m engine.voice_hf ch2/ep01 fetch && python3 -m engine.voice_hf ch2/ep01 build   (takes: hf_voice.json)
    then  python3 film.py parts 4 0 4 · join 4 · sound · master
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import engine.film  # noqa: E402
import ch2.ledger as ledger  # noqa: E402
from script import FLOORS  # noqa: E402

ledger.FLOORS[:] = FLOORS
ledger.style_shorts()
TAGS = "#money #airlines #creditcards #business #explained #howtheyprofit"
CLIPS = [
    dict(name="part1", a="paid", b="wings", tag="BANKS WITH WINGS · PART 1 OF 5", nxt="PART 2",
         hook="A card company paid Delta more than Delta's profit",
         post="In 2025 American Express paid Delta $8.2 billion, more than Delta's whole pre-tax profit of $6.2 billion "
              "(Delta, Jan 2026). The biggest airlines are closer to banks. Part 1 of 5."),
    dict(name="part2", a="print", b="breakage", tag="BANKS WITH WINGS · PART 2 OF 5", nxt="PART 3",
         hook="How airlines print their own money",
         post="A mile is a currency: the airline creates it, sets its value and runs the only shop that takes it, then sells "
              "it to banks for cash today. Unused miles have a name: breakage. Part 2 of 5."),
    dict(name="part3", a="2020", b="third", tag="BANKS WITH WINGS · PART 3 OF 5", nxt="PART 4",
         hook="The miles were worth twice the airline",
         post="June 2020: United borrowed $6.8B against MileagePlus, valued at $21.9B, when the whole company was worth about "
              "$10.5B. Delta's SkyMiles: about $26B. Part 3 of 5."),
    dict(name="part4", a="whybank", b="everyone", tag="BANKS WITH WINGS · PART 4 OF 5", nxt="PART 5",
         hook="Why your bank pays for airline miles",
         post="Every card payment carries a fee, about 2% in the US, and part of it goes to the bank. Miles win your spending. "
              "Delta's Amex spend is approaching 1% of the US economy. Part 4 of 5."),
    dict(name="part5", a="you", b="spendit", tag="BANKS WITH WINGS · PART 5 OF 5", nxt=None,
         hook="Miles are not savings",
         post="In Britain card fees are capped at 0.3%, so cards give fewer miles. The airline controls the currency; a Delta or "
              "United mile is worth about 1.2 cents (NerdWallet). Earn them, then spend them. Part 5 of 5."),
]
MUSIC = [(0.0, "intro"), ("print", "a"), ("2020", "b"), ("whybank", "a"), ("you", "b"), ("imagine", "intro"), ("then", "a"),
         ("end", "out")]

if __name__ == "__main__":
    os.environ.setdefault("EL_VOICE", "elder")
    engine.film.main(__file__, title="HOW THEY PROFIT  ·  BANKS WITH WINGS", music=MUSIC, anchors=("print", "whybank"),
                     clips=CLIPS, tags=TAGS, bed="chrome_marl", look_mod=ledger, cap_mod=ledger.CAPTIONS)
