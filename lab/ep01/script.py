"""EP01 · SIXTEEN HOURS (Six Floors format, 9:16, ~2:15).

Floors: 0 GROUND · 1 MECHANISM · 2 YOU · 3 IDEA · 4 IMAGINE · 5 SURFACE (see lab/format/SIX_FLOORS.md).
Fields: floor, text, air (extra half-bars of silence before the line), cut (a hard 0.3 s drop before it, the
pollar punctuation), card (big, sub) for the on-screen fact/source card, mark (seconds on the log time ruler
that the horizon marker moves to on this line; negative = a dotted "if" marker).
"""

H = 3600.0
LINES = [
    # 0 · GROUND
    dict(floor=0, text="This task takes a human expert sixteen hours.", mark=16 * H,
         card=("16 H", "HUMAN EXPERT TIME")),
    dict(floor=0, text="In March 2026, an AI finished tasks like it half the time. On its own.",
         card=("≥ 16 H · 50%", "TIME HORIZON · METR, MARCH 2026")),
    dict(floor=0, text="Seven years earlier, the best one could manage took you two seconds.", mark=2.0, cut=True,
         card=("2 SEC", "2019 · METR, MAR 2025")),
    # 1 · MECHANISM
    dict(floor=1, text="Here's how you measure that.", air=2),
    dict(floor=1, text="A research group called METR timed real people on a couple of hundred tasks.",
         card=("228 TASKS", "METR TIME HORIZON 1.1 · JAN 2026")),
    dict(floor=1, text="Coding. Research. Fixing broken systems. From seconds to days."),
    dict(floor=1, text="Then they gave the same tasks to the machines, and found the length where the machine wins half the time."),
    dict(floor=1, text="They call it the time horizon.", cut=True),
    dict(floor=1, text="Two seconds. Nine seconds. Five minutes. An hour. Sixteen hours.", mark=16 * H, ladder=True),
    # 2 · YOU
    dict(floor=2, text="Sixteen hours is two working days.", air=1, card=("2 DAYS", "AT 8 HOURS A DAY")),
    dict(floor=2, text="A coursework essay. A website for the takeaway round the corner. The game mod you never finished."),
    # 3 · IDEA
    dict(floor=3, text="Here's what our brains get wrong.", air=2, cut=True),
    dict(floor=3, text="We think in steps. This kind of growth thinks in folds."),
    dict(floor=3, text="Fold a sheet of paper forty-two times, and it would reach past the Moon.",
         card=("42 FOLDS", "0.1 MM × 2^42 ≈ 440,000 KM · MOON: 384,400 KM")),
    dict(floor=3, text="Since 2019, the horizon has doubled about every seven months. Lately, about every four.",
         card=("×2 / 4.3 MO", "METR · DOUBLING SINCE 2023")),
    # 4 · IMAGINE
    dict(floor=4, text="So imagine it keeps going.", air=3, cut=True),
    dict(floor=4, text="Not a forecast. A what-if.", air=7, drop=True),
    dict(floor=4, text="A working week before this year is out. A working month by the middle of next year.", mark=-160 * H),
    dict(floor=4, text="Imagine handing over a month. Not a chore. A project."),
    dict(floor=4, text="The first draft of the book. The first version of the business. The whole search for the cure you care about."),
    dict(floor=4, text="What would you give it?", air=1),
    dict(floor=4, text="And what would you keep for yourself?", air=1),
    # 5 · SURFACE
    dict(floor=5, text="Tonight's version: pick one task that eats your week, and cut it into pieces an AI can finish before you wake up.", air=2),
    dict(floor=5, text="It took six years to get from two seconds to an hour.", air=1, cut=True, mark=3600.0),
    dict(floor=5, text="It took one more to get from an hour to sixteen.", cut=True, mark=16 * H),
]

LADDER = [(2019, 2.0, "2 SEC"), (2020, 9.0, "9 SEC"), (2023, 300.0, "5 MIN"), (2025, 3600.0, "1 HOUR"), (2026, 16 * H, "16 HOURS")]

FLOORS = ["GROUND", "MECHANISM", "YOU", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "METR, 'Measuring AI Ability to Complete Long Tasks' (19 Mar 2025): time horizon doubling ~7 months since 2019; per-model horizons (check the 2 s / 9 s / 5 min / 1 h rungs against the paper's figure)",
    "METR, 'Time Horizon 1.1' (29 Jan 2026): 228 tasks; post-2023 doubling ~130.8 days",
    "METR measurement, March 2026: an early frontier model at a 50% time horizon of at least 16 hours",
    "Paper folding: 0.1 mm × 2^42 ≈ 439,805 km; mean Earth–Moon distance 384,400 km",
    "What-if extrapolation (not a forecast): 16 h doubling every ~4.3 months → ~64 h by Nov 2026, ~256 h by Jul 2027",
]
