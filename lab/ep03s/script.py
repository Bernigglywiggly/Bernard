"""EP03 · THE SHOVEL SELLERS, v2 (28 Sep): the new register. No jokes, no swearing, no gaps for punchlines.
Straight into the facts, precise and sourced, fast; curiosity carries it, and one clearly labelled what-if stretches
the imagination. George (ElevenLabs), fast. Pollar's lessons (lab/inspo/pollar_playbook.md): a concrete hook in the
first line, numbers made physical, the hidden mechanism, what is uncertain said plainly, a mirrored close, sources.

Fields: id (what the visuals key on; the cold open's ids are unchanged), text (the caption), say (what the voice
reads, with years spelled out), card (big number, small line), air (half-bars of silence before), cut (a hard
drop before a reveal), floor (the section).
Facts: SOURCES below, checked 28 Sep 2026.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="bottle", card=("1848", "SAN FRANCISCO · A BOTTLE OF GOLD"),
         text="May 1848. San Francisco. A shopkeeper named Sam Brannan walks through the streets holding up a bottle of gold dust.",
         say="May, eighteen forty-eight. San Francisco. A shopkeeper named Sam Brannan walks through the streets holding up a bottle of gold dust."),
    dict(floor=0, id="mind", text="Within weeks the town empties. Its newspaper stops printing, because its readers have gone to dig."),
    dict(floor=0, id="shop", text="Brannan had already bought every pan, pick and shovel he could find. A pan that cost him twenty cents sold for fifteen dollars."),
    dict(floor=0, id="36k", card=("$36,000", "IN NINE WEEKS · ONE STORE"), text="In nine weeks, his store took in thirty-six thousand dollars."),
    dict(floor=0, id="e2", text="About one and a half million dollars today."),
    dict(floor=0, id="never", cut=True, card=("1ST MILLIONAIRE", "CALIFORNIA · WITHOUT MINING"),
         text="He never panned for gold. He became California's first millionaire."),
    dict(floor=0, id="rule", air=1, text="So who actually gets rich in a gold rush?"),
    # 1 · MECHANISM
    dict(floor=1, id="census", card=("1850 · 1852", "CENSUS RECORDS · CLAY & JONES, 2008"),
         text="In 2008, two economists went through the census records of 1850 and 1852 to find out.",
         say="In two thousand and eight, two economists went through the census records of eighteen fifty and eighteen fifty-two to find out."),
    dict(floor=1, id="verdict", cut=True, card=("SMALL OR EVEN ZERO", "FOR MINERS · CLAY & JONES, 2008"),
         text="For miners, the gains were small, or even zero. For everyone else, positive and large."),
    dict(floor=1, id="split", text="A rush splits one prize between everyone chasing it."),
    dict(floor=1, id="pan", text="But every one of them needs a pan, whether or not they ever find gold. The supplier is paid either way."),
    # 2 · NOW
    dict(floor=2, id="now", air=1, text="Now look at 2026.", say="Now look at twenty twenty-six."),
    dict(floor=2, id="capex", card=("$725 BILLION", "AMAZON · MICROSOFT · ALPHABET · META · 2026 PLANS"),
         text="This year, Amazon, Microsoft, Alphabet and Meta plan to spend around seven hundred and twenty-five billion dollars, most of it on AI data centres."),
    dict(floor=2, id="nvidia", card=("$96.2 BILLION", "NVIDIA · ONE QUARTER · 75% GROSS MARGIN"),
         text="The company selling the chips inside them, Nvidia, took in ninety-six billion dollars in three months. Its gross margin: seventy-five per cent."),
    dict(floor=2, id="openai", card=("$5.7B IN · $3.7B OUT", "OPENAI · JAN–MAR 2026 · THE INFORMATION"),
         text="The best-known company doing the digging, OpenAI, took in five point seven billion in the first three months of the year, and burned through three point seven."),
    dict(floor=2, id="fair", text="That doesn't make the diggers wrong. Some of them will find gold. But the supplier is paid first, whoever finds it."),
    # 3 · IDEA
    dict(floor=3, id="before", air=2, cut=True, text="It has happened before."),
    dict(floor=3, id="acts", card=("272 ACTS", "RAILWAY MANIA · PARLIAMENT, 1846"),
         text="1846. Britain's railway mania. Parliament approves two hundred and seventy-two new railway companies in a single year.",
         say="Eighteen forty-six. Britain's railway mania. Parliament approves two hundred and seventy-two new railway companies in a single year."),
    dict(floor=3, id="third", card=("1/3 NEVER BUILT", "TRACK AUTHORISED 1844–47"),
         text="About a third of the track they authorised was never built. Then the bubble burst."),
    dict(floor=3, id="miles", card=("~6,000 MILES", "BRITAIN'S RAILWAYS BY 1850"),
         text="Investors lost fortunes. But by 1850, Britain had about six thousand miles of railway.",
         say="Investors lost fortunes. But by eighteen fifty, Britain had about six thousand miles of railway."),
    dict(floor=3, id="layers", text="The speculation disappears. The infrastructure stays."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine it's 2030, and the build-out is finished.",
         say="So imagine it's twenty thirty, and the build-out is finished."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="cheap", text="Intelligence is cheap, and everywhere, all the time."),
    dict(floor=4, id="scarce", text="Then what becomes scarce? Electricity. Chips. Land and water to cool them."),
    dict(floor=4, id="trust", text="And something harder to manufacture: knowing which answer to trust."),
    dict(floor=4, id="question", air=1, text="In every rush, the question isn't where the gold is. It's what everyone looking for it will need."),
    # 5 · SURFACE
    dict(floor=5, id="rush", air=2, cut=True, text="They saw a gold rush."),
    dict(floor=5, id="chain", cut=True, text="He saw a supply chain."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "Sam Brannan: bottle of gold in the streets, May 1848; pans bought for 20 cents, sold for $15; $36,000 in nine weeks "
    "(some accounts: three months); California's first millionaire (Wikipedia; Britannica; FoundSF)",
    "The Californian suspended publication on 29 May 1848: readers, advertisers and staff had left for the goldfields "
    "(Library of Congress; Wikipedia)",
    "$1 in 1848 ≈ $42 today, US CPI (officialdata.org), so $36,000 ≈ $1.5 million",
    "Clay & Jones, 'Migrating to Riches? Evidence from the California Gold Rush', Journal of Economic History 68(4), "
    "2008, 997-1027: gains 'small or even zero' for miners, 'positive and large' for non-miners",
    "Big-tech 2026 capital expenditure ~$725 billion, company guidance after Q2 2026 earnings (CNBC; MLQ)",
    "Nvidia Q2 fiscal 2027 (quarter to 26 July 2026): revenue $96.2 billion, gross margin 75.0% (Nvidia 8-K, 26 Aug 2026)",
    "OpenAI Jan-Mar 2026: revenue $5.7 billion, cash burn $3.7 billion (The Information)",
    "Railway Mania: 272 Acts of Parliament in 1846; about a third of the mileage authorised 1844-47 never built; "
    "~6,000 miles by 1850 (Wikipedia, 'Railway Mania')",
    "The 2030 section is a labelled what-if, not a forecast",
]
