"""EP02 · THE NINETY-MINUTE WAR (Six Floors format, 9:16, ~2:15).

The metric ruler is price per million tokens (log scale, $0.01 → $100). Fields as in EP01:
floor, text, air (half-bars of silence before), cut (hard drop before), card (big, sub),
mark (dollars per million tokens for the price marker), drop (the vortex line), quiet (drums out from here).
"""

LINES = [
    # 0 · GROUND
    dict(floor=0, text="On the twenty-second of September, one AI lab cut the price of its best model by a fifth.", mark=4.0,
         card=("−20%", "22 SEP 2026 · $5 → $4 PER MILLION INPUT TOKENS")),
    dict(floor=0, text="About ninety minutes later, its biggest rival launched two new models, at half the price.", mark=2.0,
         card=("−50%", "~90 MIN LATER · THE GAP IS SINGLE-SOURCE")),
    dict(floor=0, text="Two companies. One afternoon. Both went cheaper.", cut=True),
    # 1 · MECHANISM
    dict(floor=1, text="Here's what's actually going on.", air=2),
    dict(floor=1, text="When a product gets better every few months, customers really compare two things. How good. And how much."),
    dict(floor=1, text="Nobody can tell how good in an afternoon. Everyone can see the price."),
    dict(floor=1, text="So price is the signal. And once one lab moves, the other has hours, not weeks.", cut=True),
    dict(floor=1, text="Between 2021 and 2024, the same level of AI went from sixty dollars a million tokens, to six cents.", mark=0.06,
         card=("1,000×", "$60 → $0.06 PER MILLION TOKENS · 2021 → 2024 · a16z")),
    # 2 · YOU
    dict(floor=2, text="A million tokens is about seven hundred and fifty thousand words. Roughly eight novels.", air=1,
         card=("≈ 8 NOVELS", "1 TOKEN ≈ ¾ OF A WORD")),
    dict(floor=2, text="At the new cheapest price, a machine can read all eight for less than ten pence.", mark=0.10,
         card=("< 10P", "$0.10 PER MILLION INPUT TOKENS")),
    dict(floor=2, text="Your whole reading list. Every review a takeaway has ever had. A year of your emails."),
    # 3 · IDEA
    dict(floor=3, text="Biologists have a name for this.", air=2, cut=True),
    dict(floor=3, text="In Through the Looking-Glass, the Red Queen tells Alice: it takes all the running you can do, to keep in the same place.",
         card=("THE RED QUEEN", "LEWIS CARROLL · 1871")),
    dict(floor=3, text="In 1973, a biologist called Leigh Van Valen borrowed her, to explain why species never get ahead. Their rivals keep evolving too.",
         card=("VAN VALEN", "\"A NEW EVOLUTIONARY LAW\" · 1973")),
    dict(floor=3, text="Two labs, running as fast as they can, to stay exactly where they are. And every step they take, you get it cheaper."),
    # 4 · IMAGINE
    dict(floor=4, text="So imagine the running never stops.", air=3, cut=True),
    dict(floor=4, text="Not a forecast. A what-if.", air=7, drop=True),
    dict(floor=4, text="Imagine the best tutor on Earth costs less than a text message.", mark=-0.001),
    dict(floor=4, text="Then the best coder. The best translator. The best second opinion."),
    dict(floor=4, text="When thinking is almost free, what gets expensive?", air=1, quiet=True),
    dict(floor=4, text="Maybe the things a machine can't send you. Your time. Your attention. Someone who turns up.", air=1),
    # 5 · SURFACE
    dict(floor=5, text="Tonight's version: find the one job you've been putting off because it means hours of reading, and hand it over for pennies.", air=2),
    dict(floor=5, text="One lab cut its price by a fifth. The other cut it in half.", air=1, cut=True),
    dict(floor=5, text="And both of them are still running.", cut=True),
]

FLOORS = ["GROUND", "MECHANISM", "YOU", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "22 Sep 2026: a frontier lab cut its flagship to $4 / $20 per million tokens (was $5 / $25); its rival launched two models at half the previous price (about 90 minutes later, per one outlet)",
    "a16z 'LLMflation' (Nov 2024): GPT-3-level output $60 → $0.06 per million tokens, Nov 2021 → late 2024",
    "Tokens to words: ~0.75 words per token (common rule of thumb); a novel ≈ 90,000 words",
    "Lewis Carroll, Through the Looking-Glass (1871); Leigh Van Valen, 'A New Evolutionary Law' (1973)",
    "What-if section: labelled speculation, not a forecast",
]
