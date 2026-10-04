"""HOW THEY PROFIT · EP05 · WHERE YOUR $100 GOES (PayPal): the film, on the shared engine with the ledger look (ch2/ledger.py).
Voice: Higgsfield Seed Audio "Sterling" (there's no ElevenLabs key), one take per floor cut back into lines:

    cd lab && python3 -m engine.voice_hf ch2/ep05 reqs    (submit build/hf_reqs.json, record the takes in hf_voice.json)
    cd lab && python3 -m engine.voice_hf ch2/ep05 fetch && python3 -m engine.voice_hf ch2/ep05 build
    then  python3 film.py parts 4 0 4 · join 4 · sound · master, and  cd lab && python3 ch2/endcard.py ep05
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import engine.film  # noqa: E402
import ch2.ledger as ledger  # noqa: E402
from script import FLOORS  # noqa: E402

ledger.FLOORS[:] = FLOORS
ledger.style_shorts()
TAGS = "#money #paypal #fintech #business #explained #howtheyprofit"
CLIPS = [
    dict(name="keeps", a="tap", b="small", tag="WHERE YOUR $100 GOES", nxt=None,
         hook="PayPal keeps 34 cents of your $100",
         post="Last year $1.79 trillion moved through PayPal. On average it kept about $1.85 of every $100, and about 34 "
              "cents ended as operating profit (PayPal 10-K and results, 2025). Full film on the channel."),
    dict(name="toll", a="toll", b="why", tag="THE $3.98 BUTTON", nxt=None,
         hook="What a shop pays for the yellow button",
         post="PayPal Checkout costs a US shop on the standard rate 3.49% + 49 cents: $3.98 on a $100 sale (PayPal fees "
              "page). Shops pay because fewer shoppers abandon their basket."),
    dict(name="unbranded", a="avg", b="third", tag="THE PAYPAL YOU NEVER SEE", nxt=None,
         hook="The PayPal you never see",
         post="About 9.3 billion of PayPal's 25.4 billion payments in 2025 were processed without the PayPal name, mostly "
              "Braintree behind other companies' checkouts (PayPal results, 2025)."),
    dict(name="interest", a="still", b="yours", tag="MONEY THAT SITS STILL", nxt=None,
         hook="Your idle balance earns money. Not for you.",
         post="PayPal earned about $1.3 billion of interest in 2025 on money people left in their balances "
              "($15.5B - $14.2B transaction margin with and without it, PayPal results)."),
    dict(name="problem", a="game", b="card", tag="THE BUTTON'S PROBLEM", nxt=None,
         hook="PayPal admitted the problem",
         post="'Our execution has not been where it needs to be, particularly in branded checkout' (PayPal, 3 Feb 2026), "
              "the day it named Enrique Lores CEO."),
]
MUSIC = [(0.0, "intro"), ("toll", "a"), ("networks", "b"), ("still", "a"), ("two", "b"), ("game", "intro"), ("card", "a"),
         ("end", "out")]

if __name__ == "__main__":
    os.environ.setdefault("EL_VOICE", "elder")
    engine.film.main(__file__, title="HOW THEY PROFIT  ·  WHERE YOUR $100 GOES", music=MUSIC, anchors=("avg", "still"),
                     clips=CLIPS, tags=TAGS, bed="chrome_marl", look_mod=ledger, cap_mod=ledger.CAPTIONS)
