"""EP03 · THE SHOVEL SELLERS (Six Floors format, 9:16, under 3:00 for Shorts). George, faster, the new register:
quick, eloquent, dry, swearing where it lands.

The metric ruler is a timeline with a broken axis (1840–1860 | 2000–2032): history on the left, now on the right.
Fields as in EP01/EP02: floor, text, air (half-bars of silence before), cut (hard drop before), card (big, sub),
mark (the year the timeline marker moves to on this line; negative = a dotted "if" marker), drop (the vortex line),
quiet (drums out from here), say (what the voice reads when the caption's digits would be misread),
id (the name the visuals use for the line), slot (a gap for the user's own punchline: `text` is my fallback, and
build/slots.json, pulled from the plan page, replaces it when the user has written one).
Facts: lab/research/script_facts.md §3a/§3b (verified unless noted in SOURCES).
"""

LINES = [
    # 0 · GROUND
    dict(floor=0, id="bottle", mark=1848, card=("1848", "SAN FRANCISCO · A BOTTLE OF GOLD"),
         text="1848. San Francisco. A shopkeeper called Sam Brannan walks down the street holding up a bottle of gold, like he's just won the bloody Champions League.",
         say="Eighteen forty-eight. San Francisco. A shopkeeper called Sam Brannan walks down the street holding up a bottle of gold, like he's just won the bloody Champions League."),
    dict(floor=0, id="mind", text="The whole city loses its mind. Half the town downs tools and legs it for the river."),
    dict(floor=0, id="shop", text="And Sam? Sam had already bought up the pans. And the shovels."),
    dict(floor=0, id="36k", text="Nine weeks later, he'd made thirty-six thousand dollars.",
         card=("$36,000", "IN NINE WEEKS · SELLING SUPPLIES")),
    dict(floor=0, slot="e2", text="In 1848 money. That's not rich. That's buy-the-street rich.",
         say="In eighteen forty-eight money. That's not rich. That's buy-the-street rich."),
    dict(floor=0, id="never", cut=True, text="He never dug for gold. Not once. Not one fucking scoop.",
         card=("1ST MILLIONAIRE", "CALIFORNIA · WITHOUT MINING")),
    # 1 · MECHANISM
    dict(floor=1, id="rule", air=2, text="Here's the bit nobody tells you."),
    dict(floor=1, id="split", text="In a rush, everyone chases the same prize, so the prize gets split a thousand ways."),
    dict(floor=1, id="pan", text="But every single one of them needs a pan. Gold or no gold, the pan man gets paid."),
    dict(floor=1, id="census", mark=2008, card=("1850 · 1852", "CENSUS RECORDS · CLAY & JONES, 2008"),
         text="In 2008, two economists went back through the census records of 1850 and 1852 to check.",
         say="In two thousand and eight, two economists went back through the census records of eighteen fifty and eighteen fifty-two to check."),
    dict(floor=1, id="verdict", cut=True, card=("SMALL OR EVEN ZERO", "FOR MINERS · CLAY & JONES, 2008"),
         text="For the miners, the gains were small, or even zero. For everyone else, positive, and large."),
    dict(floor=1, slot="e3", text="Economists. Taking a hundred and sixty years to confirm what Sam worked out in an afternoon."),
    # 2 · YOU
    dict(floor=2, id="now", air=1, mark=2026, text="Now look at 2026. Everyone's digging for the same gold again. Apps. Agents. Startups.",
         say="Now look at twenty twenty-six. Everyone's digging for the same gold again. Apps. Agents. Startups."),
    dict(floor=2, slot="e4", text="Every one of them with a pitch deck that says revolutionary on slide one."),
    dict(floor=2, id="receipt", card=("UP TO 30%", "DELIVERY-APP COMMISSION PER ORDER"),
         text="Meanwhile, the takeaway round the corner still hands up to thirty percent of every order to an app."),
    dict(floor=2, id="door", text="It doesn't need a startup. It needs someone who knows what the tools can do, and has the bollocks to walk in the door."),
    dict(floor=2, slot="e5", text="That's the shovel. It's not glamorous. Neither was a shovel."),
    # 3 · IDEA
    dict(floor=3, id="before", air=2, cut=True, text="And none of this is new. It's the oldest pattern in money."),
    dict(floor=3, id="acts", mark=1846, card=("260+ ACTS", "RAILWAY MANIA · PARLIAMENT, 1846"),
         text="1846. Britain goes railway mad. Parliament approves hundreds of new railway companies.",
         say="Eighteen forty-six. Britain goes railway mad. Parliament approves hundreds of new railway companies."),
    dict(floor=3, id="third", mark=1847, card=("1/3 NEVER BUILT", "TRACK AUTHORISED 1844–47"),
         text="About a third of the track they approved never got built. Then the bubble burst."),
    dict(floor=3, slot="e6", text="Turns out you can't ride a train on a share certificate."),
    dict(floor=3, id="miles", mark=1850, card=("~6,000 MILES", "BRITAIN'S RAILWAYS BY 1850"),
         text="The investors got wiped out. But by 1850, Britain had about six thousand miles of railway.",
         say="The investors got wiped out. But by eighteen fifty, Britain had about six thousand miles of railway."),
    dict(floor=3, id="layers", text="The gold runs out. The tracks stay. And the steady money always sits one layer below the prize."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine it's 2030, and the rush is still on.",
         say="So imagine it's twenty thirty, and the rush is still on."),
    dict(floor=4, id="whatif", air=7, drop=True, text="Not a forecast. A what-if."),
    dict(floor=4, id="certainty", mark=-2030, text="On your high street, there's a shop that sells certainty. Every answer, checked by an actual human being."),
    dict(floor=4, id="repair", text="Next door, a repair shop for AI agents that have gone a bit feral. A tailor who fits a model to one family, like a suit."),
    dict(floor=4, slot="e7", text="And a support group for people whose fridge has started giving them life advice."),
    dict(floor=4, id="question", air=1, quiet=True, text="So what will the people chasing AI gold need, that nobody's selling yet?"),
    dict(floor=4, id="boring", air=1, text="Whatever it is, I promise you it's boring. Shovels always are."),
    # 5 · SURFACE
    dict(floor=5, id="homework", air=2, text="Tonight's homework: walk past three shops, and write down one job each of them still does by hand. That's your shovel list."),
    dict(floor=5, slot="e8", text="Bonus points if the owner looks knackered. That's not a shop. That's a customer."),
    dict(floor=5, id="rush", air=1, cut=True, mark=1848, text="They saw a gold rush."),
    dict(floor=5, id="chain", cut=True, mark=2026, text="He saw a supply chain."),
]

FLOORS = ["GROUND", "MECHANISM", "YOU", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "Sam Brannan: stocked supplies, spread word of gold with a bottle of it; $36,000 in nine weeks; California's first millionaire (Wikipedia, FoundSF, Sausalito Historical Society)",
    "Clay & Jones, 'Migrating to Riches? Evidence from the California Gold Rush', J. Econ. History 68(4), 2008: 'small or even zero for miners… positive and large for nonminers'",
    "Delivery-app commission ranges, 2026 comparisons: Uber Eats 15–30%, Deliveroo 14–30%, Just Eat 14–22%",
    "Railway Mania: 263–272 Acts in 1846; about a third of the mileage authorised 1844–47 never built; collapse around the Panic of 1847; ~6,000 miles by 1850 (single source)",
    "What-if section: labelled speculation, not a forecast",
]
