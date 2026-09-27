"""EP03 · THE SHOVEL SELLERS (Six Floors format, 9:16, target under 3:00 for Shorts).

The metric ruler is a timeline with a broken axis (1840–1860 | 2000–2032): history on the left, now on the right.
Fields as in EP01/EP02: floor, text, air (half-bars of silence before), cut (hard drop before), card (big, sub),
mark (the year the timeline marker moves to on this line; negative = a dotted "if" marker), drop (the vortex line),
quiet (drums out from here), say (what the voice reads when the caption's digits would be misread). Facts: lab/research/script_facts.md §3a/§3b (verified unless noted in SOURCES).
"""

LINES = [
    # 0 · GROUND
    dict(floor=0, text="In 1848, a shopkeeper called Sam Brannan walked through San Francisco, holding up a bottle of gold.", mark=1848,
         card=("1848", "SAN FRANCISCO · A BOTTLE OF GOLD")),
    dict(floor=0, text="He'd already stocked his store with pans and shovels."),
    dict(floor=0, text="In nine weeks, he made thirty-six thousand dollars.",
         card=("$36,000", "IN NINE WEEKS · SELLING SUPPLIES")),
    dict(floor=0, text="California's first millionaire never dug for gold.", cut=True,
         card=("1ST MILLIONAIRE", "CALIFORNIA · WITHOUT MINING")),
    # 1 · MECHANISM
    dict(floor=1, text="Here's the rule underneath.", air=2),
    dict(floor=1, text="In a rush, everyone chases the same prize. So the prize gets split a thousand ways."),
    dict(floor=1, text="But every one of them needs a pan, whether they find gold or not."),
    dict(floor=1, text="In 2008, two economists went back to the census records of 1850 and 1852.", mark=2008,
         say="In 2008, two economists went back to the census records of eighteen fifty and eighteen fifty-two.",
         card=("1850 · 1852", "CENSUS RECORDS · CLAY & JONES, 2008")),
    dict(floor=1, text="For the miners, the gains were small, or even zero. For everyone else, positive, and large.", cut=True,
         card=("SMALL OR EVEN ZERO", "MINERS · 'POSITIVE AND LARGE' FOR NON-MINERS")),
    # 2 · YOU
    dict(floor=2, text="Now look at 2026. Everyone's digging for the same gold. Apps. Agents. Startups.", air=1, mark=2026),
    dict(floor=2, text="Meanwhile, the takeaway round the corner still hands up to thirty percent of every order to an app.",
         card=("UP TO 30%", "DELIVERY-APP COMMISSION PER ORDER")),
    dict(floor=2, text="It doesn't need a startup. It needs someone who knows what the tools can do, and walks in the door."),
    # 3 · IDEA
    dict(floor=3, text="It's happened before.", air=2, cut=True),
    dict(floor=3, text="In 1846, Britain's Parliament approved hundreds of new railway companies.", mark=1846,
         card=("260+ ACTS", "RAILWAY MANIA · PARLIAMENT, 1846")),
    dict(floor=3, text="About a third of the track they approved was never built. The bubble burst.", mark=1847,
         card=("1/3 NEVER BUILT", "TRACK AUTHORISED 1844–47")),
    dict(floor=3, text="The investors lost. But by 1850, Britain had about six thousand miles of railway.", mark=1850,
         say="The investors lost. But by eighteen fifty, Britain had about six thousand miles of railway.",
         card=("~6,000 MILES", "BRITAIN'S RAILWAYS BY 1850")),
    dict(floor=3, text="The gold runs out. The tracks stay. And the steady money sits one layer below the prize."),
    # 4 · IMAGINE
    dict(floor=4, text="So imagine it's 2030, and the rush is still on.", air=3, cut=True),
    dict(floor=4, text="Not a forecast. A what-if.", air=7, drop=True),
    dict(floor=4, text="On your high street, a shop that sells certainty. Every answer, checked by a person.", mark=-2030),
    dict(floor=4, text="Next door, a repair shop for AI agents that got confused. A tailor who fits a model to one family, like a suit."),
    dict(floor=4, text="What will the people chasing AI gold need, that nobody's selling yet?", air=1, quiet=True),
    dict(floor=4, text="Whatever it is, it's probably boring. Shovels always are.", air=1),
    # 5 · SURFACE
    dict(floor=5, text="Tonight's version: walk past three shops, and write down one job each of them still does by hand. That's your shovel list.", air=2),
    dict(floor=5, text="They saw a gold rush.", air=1, cut=True, mark=1848),
    dict(floor=5, text="He saw a supply chain.", cut=True, mark=2026),
]

FLOORS = ["GROUND", "MECHANISM", "YOU", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "Sam Brannan: stocked supplies, spread word of gold with a bottle of it; $36,000 in nine weeks; California's first millionaire (Wikipedia, FoundSF, Sausalito Historical Society)",
    "Clay & Jones, 'Migrating to Riches? Evidence from the California Gold Rush', J. Econ. History 68(4), 2008: 'small or even zero for miners… positive and large for nonminers'",
    "Delivery-app commission ranges, 2026 comparisons: Uber Eats 15–30%, Deliveroo 14–30%, Just Eat 14–22%",
    "Railway Mania: 263–272 Acts in 1846; about a third of the mileage authorised 1844–47 never built; collapse around the Panic of 1847; ~6,000 miles by 1850 (single source)",
    "What-if section: labelled speculation, not a forecast",
]
