"""EP07 · THE THIRTY-YEAR DELAY, v1 (28 Sep 2026), from the episode bank (lab/format/EPISODES.md). The Curve's format
(lab/inspo/pollar_playbook.md): a concrete hook, the hidden mechanism, numbers made physical, what's reported vs
known said plainly, one labelled what-if, a mirrored close. George (ElevenLabs), fast; no jokes in the lines.
Bed: Night Drive, calm (tension without cheese, under a voice).

The hidden mechanism (Paul David, "The Dynamo and the Computer", 1990): electricity took decades to show up in
productivity because factories first swapped the steam engine for one big motor and kept the shaft, the belts and
the building; the gains came when factories were redesigned around small motors in every machine. Computers did the
same (Solow's paradox, then the late-1990s surge). AI in 2026 looks like the one-big-motor stage.

Fields as in lab/ep03s/script.py: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="survey", card=("6,000", "BOSSES ASKED · US, UK, GERMANY, AUSTRALIA · NBER, FEB 2026"),
         text="In February 2026, economists asked 6,000 bosses in America, Britain, Germany and Australia what AI had done for their companies.",
         say="In February twenty twenty-six, economists asked six thousand bosses in America, Britain, Germany and Australia what AI had done for their companies."),
    dict(floor=0, id="nothing", card=("~90%", "OF FIRMS: NO CHANGE IN PRODUCTIVITY OR JOBS"),
         text="Nearly nine in ten said: nothing. No change in productivity. No change in jobs."),
    dict(floor=0, id="hours", card=("1.5 HOURS", "A WEEK: HOW MUCH THE BOSSES USED IT"),
         text="The bosses who used it averaged about an hour and a half a week."),
    dict(floor=0, id="before", air=1, cut=True, text="This has happened before. Almost exactly."),
    # 1 · MECHANISM: the motor and the shaft
    dict(floor=1, id="edison", card=("1882", "EDISON'S PEARL STREET STATION · NEW YORK"),
         text="In 1882, Thomas Edison opened his first power station, on Pearl Street in New York.",
         say="In eighteen eighty-two, Thomas Edison opened his first power station, on Pearl Street in New York."),
    dict(floor=1, id="decades", text="Electricity was cleaner and more flexible than steam. And for decades, it barely showed up in factory productivity."),
    dict(floor=1, id="five", card=("5%", "OF US FACTORY POWER FROM ELECTRIC MOTORS · 1900"),
         text="By 1900, electric motors drove about 5% of the power in American factories.",
         say="By nineteen hundred, electric motors drove about five percent of the power in American factories."),
    dict(floor=1, id="shaft", cut=True, text="Here's why. The old factories ran on one giant steam engine, turning one long shaft, with belts to every machine."),
    dict(floor=1, id="swap", text="So owners swapped the steam engine for one big electric motor. And changed nothing else."),
    dict(floor=1, id="same", text="Same shaft. Same belts. Same building. Small savings."),
    dict(floor=1, id="redesign", cut=True,
         text="The gains came when factories were built around the motor instead: a small motor in every machine, laid out along the flow of the work."),
    dict(floor=1, id="fifty", card=("50%", "OF US FACTORY POWER ELECTRIC BY 1920 · THEN THE SURGE"),
         text="By 1920, about half of factory power was electric. And productivity finally surged.",
         say="By nineteen twenty, about half of factory power was electric. And productivity finally surged."),
    # 2 · NOW: the same gap
    dict(floor=2, id="solow", air=1, card=("1987", "ROBERT SOLOW · NEW YORK TIMES BOOK REVIEW"),
         text="In 1987, the economist Robert Solow wrote: you can see the computer age everywhere but in the productivity statistics.",
         say="In nineteen eighty-seven, the economist Robert Solow wrote: you can see the computer age everywhere but in the productivity statistics."),
    dict(floor=2, id="nineties", text="The gains came in the late nineties, after companies rebuilt how they worked around it."),
    dict(floor=2, id="pilots", card=("95%", "OF COMPANY AI PILOTS: NO MEASURABLE RETURN · MIT, 2025"),
         text="Now AI. In 2025, an MIT study found 95% of company AI pilots made no measurable return.",
         say="Now AI. In twenty twenty-five, an MIT study found ninety-five percent of company AI pilots made no measurable return."),
    dict(floor=2, id="bolted", text="Mostly bolted onto the old routine. One big motor, turning the same shaft."),
    # 3 · IDEA
    dict(floor=3, id="layout", air=2, cut=True, text="The tool is rarely the bottleneck. The layout is."),
    dict(floor=3, id="shapes", text="New power needs new shapes."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine an office designed from zero around AI."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="first", text="What goes first? The weekly status meeting. The inbox. The jobs that exist only to move information from one place to another."),
    dict(floor=4, id="look", air=1, text="The first companies built that way won't look like ours. The way a 1920s factory didn't look like one from the 1890s.",
         say="The first companies built that way won't look like ours. The way a nineteen-twenties factory didn't look like one from the eighteen-nineties."),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="In 1882, the power arrived. Decades later, the factory changed.",
         say="In eighteen eighty-two, the power arrived. Decades later, the factory changed."),
    dict(floor=5, id="now2", cut=True, text="In 2026, the power has arrived again.", say="In twenty twenty-six, the power has arrived again."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "NBER survey of ~6,000 executives in the US, UK, Germany and Australia, Feb 2026: nearly 90% of firms reported no "
    "impact of AI on employment or productivity over the past three years; executives who used AI averaged about 1.5 "
    "hours a week (Fortune, 17 Feb 2026)",
    "Edison's Pearl Street Station, New York, September 1882",
    "Paul A. David, \"The Dynamo and the Computer: An Historical Perspective on the Modern Productivity Paradox\", "
    "American Economic Review, 1990: electric motors ~5% of US factory mechanical drive in 1900, ~50% by 1920; the "
    "productivity surge came in the 1920s with factories redesigned around unit drive",
    "Robert Solow, \"We'd better watch out\", New York Times Book Review, 12 July 1987",
    "US labour productivity growth picked up from the mid-1990s (BLS)",
    "MIT NANDA, \"The GenAI Divide: State of AI in Business 2025\": 95% of generative AI pilots with no measurable P&L return",
    "The office section is a labelled what-if, not a forecast",
]
