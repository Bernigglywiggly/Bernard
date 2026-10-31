"""HOW THEY PROFIT · EP04 · THE CLOUD BEHIND THE CART: the film, on the shared engine with the ledger look (ch2/ledger.py).
Voice: Higgsfield Seed Audio "Sterling" (there's no ElevenLabs key), one take per floor cut back into lines:

    cd lab && python3 -m engine.voice_hf ch2/ep04 reqs    (submit build/hf_reqs.json, record the takes in hf_voice.json)
    cd lab && python3 -m engine.voice_hf ch2/ep04 fetch && python3 -m engine.voice_hf ch2/ep04 build
    then  python3 film.py parts 4 0 4 · join 4 · sound · master, and  cd lab && python3 ch2/endcard.py ep04
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import engine.film  # noqa: E402
import ch2.ledger as ledger  # noqa: E402
from script import FLOORS  # noqa: E402

ledger.FLOORS[:] = FLOORS
ledger.style_shorts()
TAGS = "#money #amazon #aws #business #explained #howtheyprofit"
CLIPS = [
    dict(name="part1", a="sales", b="front", tag="THE CLOUD BEHIND THE CART · PART 1 OF 5", nxt="PART 2",
         hook="57% of Amazon's profit comes from something you never see",
         post="Amazon's 2025 sales: $716.9B. 57% of its operating profit came from AWS, which rents out computers "
              "(Amazon, Feb 2026). Part 1 of 5."),
    dict(name="part2", a="five", b="anyone", tag="THE CLOUD BEHIND THE CART · PART 2 OF 5", nxt="PART 3",
         hook="Amazon is five businesses behind one website",
         post="The shop ($265B), the marketplace (sellers paid $172B; a 15% commission in most categories), adverts "
              "($68.6B), subscriptions ($49.6B) and AWS. Part 2 of 5."),
    dict(name="part3", a="began", b="plan", tag="THE CLOUD BEHIND THE CART · PART 3 OF 5", nxt="PART 4",
         hook="18% of Amazon's sales, 57% of its profit",
         post="2025: Amazon's North American shops made about 7¢ per $1, the rest of the world under 3¢, AWS 35¢. AWS "
              "opened in 2006; Amazon first showed its profit in 2015. Part 3 of 5."),
    dict(name="part4", a="where", b="engine", tag="THE CLOUD BEHIND THE CART · PART 4 OF 5", nxt="PART 5",
         hook="Where your money goes when you buy on Amazon",
         post="Commission, storage, delivery, adverts: by one estimate (ILSR, Dec 2023), sellers pay Amazon about 45¢ "
              "of every $1 they take. Part 4 of 5."),
    dict(name="part5", a="you", b="parcel", tag="THE CLOUD BEHIND THE CART · PART 5 OF 5", nxt=None,
         hook="Look for the word Sponsored",
         post="The first result isn't always the best one; sometimes it's the one that paid. Scroll past the adverts, "
              "check the seller, compare the price elsewhere. Part 5 of 5."),
]
MUSIC = [(0.0, "intro"), ("five", "a"), ("began", "b"), ("where", "a"), ("you", "b"), ("imagine", "intro"), ("then", "a"),
         ("end", "out")]

if __name__ == "__main__":
    os.environ.setdefault("EL_VOICE", "elder")
    engine.film.main(__file__, title="HOW THEY PROFIT  ·  THE CLOUD BEHIND THE CART", music=MUSIC, anchors=("five", "where"),
                     clips=CLIPS, tags=TAGS, bed="chrome_marl", look_mod=ledger, cap_mod=ledger.CAPTIONS)
