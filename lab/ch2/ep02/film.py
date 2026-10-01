"""THE MARGIN · EP02 · THE LANDLORD IN THE GOLDEN ARCHES: the film, on the shared engine with the ledger look (ch2/ledger.py).
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
ledger.style_shorts()
TAGS = "#money #mcdonalds #franchise #realestate #business #explained #themargin"
CLIPS = [
    dict(name="part1", a="rent", b="landlord", tag="THE LANDLORD · PART 1 OF 5", nxt="PART 2",
         hook="McDonald's made more from rent than profit",
         post="In 2025 McDonald's collected $10.4 billion in rent from the people who run its restaurants, more than its "
              "$8.6 billion net income (Form 10-K). Part 1 of 5."),
    dict(name="part2", a="count", b="first", tag="THE LANDLORD · PART 2 OF 5", nxt="PART 3",
         hook="Who really pays McDonald's",
         post="About 95% of its 45,356 restaurants are run by franchisees, who pay a royalty and, for most, rent on a building "
              "McDonald's owns or leases: a share of every sale. Part 2 of 5."),
    dict(name="part3", a="rescue", b="dividend", tag="THE LANDLORD · PART 3 OF 5", nxt="PART 4",
         hook="We are not in the food business",
         post="Ray Kroc took 1.9% of sales, half a percent of it to the McDonald brothers. Harry Sonneborn's idea: own the land. "
              "In 2025 rent alone beat all the food McDonald's sold itself. Part 3 of 5."),
    dict(name="part4", a="where", b="before", tag="THE LANDLORD · PART 4 OF 5", nxt="PART 5",
         hook="Of every $10 at McDonald's, who gets what",
         post="On average about $1.28 of every $10 spent at a franchised McDonald's goes to McDonald's, about 80 cents of it rent "
              "(10-K 2025). It's paid before anyone knows if the restaurant made money. Part 4 of 5."),
    dict(name="part5", a="you", b="often", tag="THE LANDLORD · PART 5 OF 5", nxt=None,
         hook="Read the lease before the menu",
         post="Higher prices mean higher sales and higher rent: the landlord wins either way. Own the thing everyone else has "
              "to use. Part 5 of 5."),
]
MUSIC = [(0.0, "intro"), ("count", "a"), ("rescue", "b"), ("where", "a"), ("you", "b"), ("imagine", "intro"), ("then", "a"),
         ("end", "out")]

if __name__ == "__main__":
    os.environ.setdefault("EL_VOICE", "elder")
    engine.film.main(__file__, title="THE MARGIN  ·  THE LANDLORD IN THE GOLDEN ARCHES", music=MUSIC, anchors=("count", "where"),
                     clips=CLIPS, tags=TAGS, bed="chrome_marl", look_mod=ledger, cap_mod=ledger.CAPTIONS)
