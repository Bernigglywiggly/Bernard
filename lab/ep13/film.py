"""EP13 · THE NINETY-MINUTE WAR: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|
parts|join|sound|master|preview|shorts|all] (see engine/__init__.py). Needs voicing first (see script.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #pricewar #tokens #llm #redqueen #economics #explained #thecurve"
CLIPS = [
    dict(name="part1", a="cut20", b="signal", tag="THE NINETY-MINUTE WAR · PART 1 OF 4", nxt="PART 2",
         hook="Two AI labs. One afternoon. Both went cheaper.",
         post="On 22 Sep 2026 one AI lab cut its best model's price by a fifth. About 90 minutes later its biggest rival "
              "launched two new models at half the price. Why price moves so fast. Part 1 of 4."),
    dict(name="part2", a="thousand", b="list", tag="THE NINETY-MINUTE WAR · PART 2 OF 4", nxt="PART 3",
         hook="1,000x cheaper in three years",
         post="The same level of AI went from $60 a million tokens in 2021 to 6 cents in 2024 (a16z). A million tokens is "
              "about 750,000 words, roughly eight novels: now under 10p to read. Part 2 of 4."),
    dict(name="part3", a="name", b="running", tag="THE NINETY-MINUTE WAR · PART 3 OF 4", nxt="PART 4",
         hook="Running as fast as you can to stay in place",
         post="The Red Queen (Lewis Carroll, 1871), borrowed by biologist Leigh Van Valen in 1973: species never get ahead "
              "because their rivals keep evolving too. AI labs now run the same race. Part 3 of 4."),
    dict(name="part4", a="imagine", b="still", tag="THE NINETY-MINUTE WAR · PART 4 OF 4", nxt=None,
         hook="When thinking is almost free, what gets expensive?",
         post="A labelled what-if: the best tutor on Earth for less than a text message. Then what gets expensive? Your "
              "time, your attention, someone who turns up. Part 4 of 4."),
    dict(name="novels", a="novels", b="list", tag="THE NINETY-MINUTE WAR", nxt=None,
         hook="Eight novels for less than 10p",
         post="A million tokens is about 750,000 words, roughly eight novels. At $0.10 per million input tokens, the new "
              "cheapest price, a machine reads all eight for less than 10p."),
    dict(name="queen", a="queen", b="running", tag="THE NINETY-MINUTE WAR", nxt=None,
         hook="Why AI labs can never get ahead",
         post="The Red Queen effect: it takes all the running you can do to keep in the same place. Two labs cutting prices "
              "within 90 minutes of each other, and every step makes it cheaper for you."),
]
MUSIC = [(0.0, "intro"), ("rival", "a"), ("both", "break"), ("actually", "a"), ("signal", "b"), ("thousand", "a"),
         ("novels", "b"), ("name", "break"), ("queen", "a"), ("running", "b"), ("imagine", "break"), ("tutor", "a"),
         ("expensive", "b"), ("tonight", "a"), ("fifth", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP13  ·  THE NINETY-MINUTE WAR", music=MUSIC, anchors=("actually", "name"), clips=CLIPS,
                     tags=TAGS, bed="arena:key=1", deafen=("both", "imagine"))
