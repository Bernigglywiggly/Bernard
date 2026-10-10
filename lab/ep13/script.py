"""EP13 · THE NINETY-MINUTE WAR, v1 (1 Oct 2026): the bank's EP02 (lab/format/EPISODES.md; the 9:16 cut in lab/ep02)
rebuilt for the 16:9 films, as EP12 was from EP01. Same lines as the 9:16 cut, with ids and the house cards, and
`say` where a number needs speaking. George (ElevenLabs) at his own pace; no jokes. Score: Arena.

NOT VOICED YET: the 9:16 cut was voiced at another speed, so 23 of these 24 lines aren't in the George cache at 1.0.
A session with ELEVENLABS_API_KEY runs `python3 film.py voice` here (24 lines), then parts/join/sound/master/shorts.

The hidden mechanism: when a product improves every few months, buyers compare two things, how good and how much,
and only the price can be read in an afternoon. So price is the signal, and a cut by one lab gets an answer in hours.
The Red Queen (Carroll 1871; Van Valen 1973): running to stay in place. Every step makes thinking cheaper for you.

Checked 1 Oct 2026: on 22 Sep 2026 Anthropic cut Claude Opus 5.5 to $4 / $20 per million tokens (Opus 5 was $5 /
$25); about 90 minutes later OpenAI launched GPT-6 Sol ($2 / $10) and Luna ($0.10 / $0.50), each about half the
per-token price of its predecessor (The Neuron, 22 Sep 2026; AIOS Guide, "a two-hour window"). The film doesn't name
them on the soundtrack; the screen and the description do.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="cut20", card=("−20%", "22 SEP 2026 · $5 → $4 PER MILLION INPUT TOKENS"),
         text="On the twenty-second of September, one AI lab cut the price of its best model by a fifth."),
    dict(floor=0, id="rival", card=("−50%", "ABOUT 90 MINUTES LATER · TWO NEW MODELS"),
         text="About ninety minutes later, its biggest rival launched two new models, at half the price."),
    dict(floor=0, id="both", cut=True, text="Two companies. One afternoon. Both went cheaper."),
    # 1 · MECHANISM: price is the only signal you can read in an afternoon
    dict(floor=1, id="actually", air=2, text="Here's what's actually going on."),
    dict(floor=1, id="compare", text="When a product gets better every few months, customers really compare two things. How good. And how much."),
    dict(floor=1, id="see", text="Nobody can tell how good in an afternoon. Everyone can see the price."),
    dict(floor=1, id="signal", cut=True, text="So price is the signal. And once one lab moves, the other has hours, not weeks."),
    dict(floor=1, id="thousand", card=("1,000×", "$60 → $0.06 PER MILLION TOKENS · 2021 → 2024 · a16z"),
         text="Between 2021 and 2024, the same level of AI went from sixty dollars a million tokens, to six cents.",
         say="Between twenty twenty-one and twenty twenty-four, the same level of AI went from sixty dollars a million tokens, to six cents."),
    # 2 · YOU: a million tokens in your units
    dict(floor=2, id="novels", air=1, card=("≈ 8 NOVELS", "1 MILLION TOKENS ≈ 750,000 WORDS"),
         text="A million tokens is about seven hundred and fifty thousand words. Roughly eight novels."),
    dict(floor=2, id="tenp", card=("< 10P", "$0.10 PER MILLION INPUT TOKENS · THE NEW CHEAPEST"),
         text="At the new cheapest price, a machine can read all eight for less than ten pence."),
    dict(floor=2, id="list", text="Your whole reading list. Every review a takeaway has ever had. A year of your emails."),
    # 3 · IDEA: the Red Queen
    dict(floor=3, id="name", air=2, cut=True, text="Biologists have a name for this."),
    dict(floor=3, id="queen", card=("THE RED QUEEN", "LEWIS CARROLL · 1871"),
         text="In Through the Looking-Glass, the Red Queen tells Alice: it takes all the running you can do, to keep in the same place."),
    dict(floor=3, id="vanvalen", card=("VAN VALEN", "\"A NEW EVOLUTIONARY LAW\" · 1973"),
         text="In 1973, a biologist called Leigh Van Valen borrowed her, to explain why species never get ahead. Their rivals keep evolving too.",
         say="In nineteen seventy-three, a biologist called Leigh Van Valen borrowed her, to explain why species never get ahead. Their rivals keep evolving too."),
    dict(floor=3, id="running", text="Two labs, running as fast as they can, to stay exactly where they are. And every step they take, you get it cheaper."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine the running never stops."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="tutor", text="Imagine the best tutor on Earth costs less than a text message."),
    dict(floor=4, id="coder", text="Then the best coder. The best translator. The best second opinion."),
    dict(floor=4, id="expensive", air=1, text="When thinking is almost free, what gets expensive?"),
    dict(floor=4, id="maybe", air=1, text="Maybe the things a machine can't send you. Your time. Your attention. Someone who turns up."),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="tonight", air=2, text="Tonight's version: find the one job you've been putting off because it means hours of reading, and hand it over for pennies."),
    dict(floor=5, id="fifth", air=1, cut=True, text="One lab cut its price by a fifth. The other cut it in half."),
    dict(floor=5, id="still", cut=True, text="And both of them are still running."),
]

FLOORS = ["GROUND", "MECHANISM", "YOU", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "22 Sep 2026: Anthropic's Claude Opus 5.5 at $4 / $20 per million input / output tokens, down from $5 / $25 for "
    "Opus 5; about 90 minutes later OpenAI's GPT-6 Sol ($2 / $10) and Luna ($0.10 / $0.50), about half the per-token "
    "price of their predecessors (The Neuron daily digest, 22 Sep 2026; AIOS Guide, \"The AI Model Price War Arrived in a "
    "Two-Hour Window\")",
    "a16z, \"Welcome to LLMflation\" (Nov 2024): the cheapest model at GPT-3's level went from $60 to $0.06 per million "
    "tokens between Nov 2021 and late 2024, about 1,000x",
    "Tokens to words: about 0.75 words per token (a common rule of thumb); a novel is about 90,000 words. Less than 10p: "
    "$0.10 is under 10p whenever a pound buys more than a dollar",
    "Lewis Carroll, Through the Looking-Glass (1871); Leigh Van Valen, \"A New Evolutionary Law\", Evolutionary Theory 1 "
    "(1973)",
    "The what-if is labelled as imagined, not a forecast",
]
