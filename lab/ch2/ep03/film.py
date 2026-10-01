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
ledger.style_shorts()
TAGS = "#money #costco #membership #retail #business #explained #themargin"
CLIPS = [
    dict(name="part1", a="hotdog", b="card", tag="THE $65 MEMBERSHIP · PART 1 OF 5", nxt="PART 2",
         hook="A $1.50 hot dog and a $9.2 billion profit",
         post="Costco's hot dog and drink has cost $1.50 since 1985, and yet it made $9.2 billion last year. The shopping isn't "
              "really what it sells. Part 1 of 5."),
    dict(name="part2", a="door", b="pure", tag="THE $65 MEMBERSHIP · PART 2 OF 5", nxt="PART 3",
         hook="Costco charges you to get in",
         post="$65 a year in the US, £42 in Britain. Markups reportedly capped at 14% (15% for Kirkland), fewer than 4,000 "
              "products, goods on pallets. The fee is almost pure profit. Part 2 of 5."),
    dict(name="part3", a="year", b="sold", tag="THE $65 MEMBERSHIP · PART 3 OF 5", nxt="PART 4",
         hook="Half of Costco's profit is the fee",
         post="Year to Aug 2026: $5.9B of membership fees, $11.7B operating profit. $297B of goods made about 2 cents a dollar. "
              "84.1M members, 92.3% renew. Part 3 of 5."),
    dict(name="part4", a="why", b="never", tag="THE $65 MEMBERSHIP · PART 4 OF 5", nxt="PART 5",
         hook="Why people pay to go shopping",
         post="A basic membership is about $1.25 a week. Half of paid members have the $130 Executive tier. The 2024 rise from "
              "$60 to $65 barely dented renewals. Part 4 of 5."),
    dict(name="part5", a="you", b="go", tag="THE $65 MEMBERSHIP · PART 5 OF 5", nxt=None,
         hook="Is a Costco membership worth it?",
         post="The $130 upgrade pays for itself above about $3,250 a year of spending ($63 a week); in Britain about £2,100. "
              "Check unit prices, buy what you'll use, go with a list. Part 5 of 5."),
]
MUSIC = [(0.0, "intro"), ("door", "a"), ("year", "b"), ("why", "a"), ("you", "b"), ("imagine", "intro"), ("then", "a"),
         ("end", "out")]

if __name__ == "__main__":
    os.environ.setdefault("EL_VOICE", "elder")
    engine.film.main(__file__, title="THE MARGIN  ·  THE $65 MEMBERSHIP", music=MUSIC, anchors=("door", "why"),
                     clips=CLIPS, tags=TAGS, bed="chrome_marl", look_mod=ledger, cap_mod=ledger.CAPTIONS)
