"""EP09 · THE LAUNDRY PROBLEM, v1 (30 Sep 2026), from the episode bank (lab/format/EPISODES.md: "Why the Robot Can Pass
the Exam but Can't Fold Your Shirt"). The Curve's format (lab/inspo/pollar_playbook.md): a concrete hook, the hidden
mechanism, numbers made physical (Big Macs for money), what's reported vs known said plainly, one labelled what-if, a
mirrored close. George (ElevenLabs) at his own pace; no jokes. Score: Arena.

The hidden mechanism: Moravec's paradox (1988). What feels effortless to us (seeing, gripping, balancing) is what
evolution has been refining for hundreds of millions of years; what feels hard to us (maths, chess) is new. So machines
learn the new skills first and the old ones last.

Fields as in lab/ep03s/script.py: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="gold", card=("35 / 42", "GOLD · INTERNATIONAL MATHEMATICAL OLYMPIAD · JULY 2025"),
         text="In July 2025, an AI scored gold at the International Mathematical Olympiad.",
         say="In July twenty twenty-five, an AI scored gold at the International Mathematical Olympiad."),
    dict(floor=0, id="few", text="Only 67 of the 630 young mathematicians competing did the same.",
         say="Only sixty-seven of the six hundred and thirty young mathematicians competing did the same."),
    dict(floor=0, id="laundry", card=("$89M", "RAISED FOR A LAUNDRY-FOLDING MACHINE"),
         text="Years earlier, a company raised about $89 million to build a machine that folds laundry.",
         say="Years earlier, a company raised about eighty-nine million dollars to build a machine that folds laundry."),
    dict(floor=0, id="bust", cut=True, text="In 2019 it went bankrupt. The machine never shipped.",
         say="In twenty nineteen it went bankrupt. The machine never shipped."),
    dict(floor=0, id="why", air=1, text="Why is the exam easy, and the laundry hard?"),
    # 1 · MECHANISM: Moravec's paradox, and age
    dict(floor=1, id="moravec", card=("1988", "HANS MORAVEC · MIND CHILDREN"),
         text="In 1988, the roboticist Hans Moravec put it like this.",
         say="In nineteen eighty-eight, the roboticist Hans Moravec put it like this."),
    dict(floor=1, id="quote", text="It's comparatively easy to make computers match adults on intelligence tests, and difficult "
                                   "or impossible to give them the skills of a one-year-old at seeing and moving."),
    dict(floor=1, id="age", cut=True, text="The reason is age."),
    dict(floor=1, id="eyes", card=("500,000,000", "YEARS OF SEEING"), text="Animals have been seeing for more than 500 million years.",
         say="Animals have been seeing for more than five hundred million years."),
    dict(floor=1, id="limbs", text="Limbs for walking and gripping: about 375 million.",
         say="Limbs for walking and gripping: about three hundred and seventy-five million."),
    dict(floor=1, id="numbers", card=("5,000", "YEARS OF WRITTEN NUMBERS"), text="Writing numbers down: about 5,000 years.",
         say="Writing numbers down: about five thousand years."),
    dict(floor=1, id="day", text="If the history of seeing were a single day, written numbers would arrive in its last second."),
    dict(floor=1, id="hand", card=("17,000", "TOUCH NERVE FIBRES · THE PALM SIDE OF ONE HAND"),
         text="The palm side of your hand alone has about 17,000 touch nerve fibres, feeling every fold of the fabric.",
         say="The palm side of your hand alone has about seventeen thousand touch nerve fibres, feeling every fold of the fabric."),
    # 2 · NOW: chess fell long ago; the laundry hasn't
    dict(floor=2, id="chess", air=1, card=("1997", "DEEP BLUE BEATS KASPAROV"), text="In 1997, a computer beat the world chess champion.",
         say="In nineteen ninety-seven, a computer beat the world chess champion."),
    dict(floor=2, id="towels", card=("AUG 2025", "A HUMANOID FOLDS TOWELS ON ITS OWN"),
         text="In August 2025, a humanoid robot folding towels on its own was still news.",
         say="In August twenty twenty-five, a humanoid robot folding towels on its own was still news."),
    dict(floor=2, id="price", card=("$16,000", "THE LAUNDRY MACHINE'S PLANNED PRICE"),
         text="That laundry machine was meant to cost about $16,000.",
         say="That laundry machine was meant to cost about sixteen thousand dollars."),
    dict(floor=2, id="macs", card=("2,600", "BIG MACS"), text="About 2,600 Big Macs. And it struggled with an ordinary T-shirt.",
         say="About two thousand six hundred Big Macs. And it struggled with an ordinary T-shirt."),
    # 3 · IDEA
    dict(floor=3, id="idea", air=2, cut=True,
         text="Difficulty isn't a measure of how clever a skill is. It's a measure of how recently we learned it."),
    dict(floor=3, id="flip", text="What feels hard to us is new. What feels effortless is ancient, and ancient is the hardest thing to copy."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine the first robot that moves like a toddler."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="where", text="Unsteady, curious, able to pick up anything. What changes in a care home? A kitchen? A building site?"),
    dict(floor=4, id="you", air=1, text="And in your own job, the parts that use your hands, your eyes and your read of a room are the "
                                        "oldest skills you have. They may be the last to go."),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="In 1997, a machine beat the best chess player on Earth.",
         say="In nineteen ninety-seven, a machine beat the best chess player on Earth."),
    dict(floor=5, id="now2", cut=True, text="In 2026, the laundry is still yours.", say="In twenty twenty-six, the laundry is still yours."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "Google DeepMind, \"Advanced version of Gemini with Deep Think officially achieves gold-medal standard at the "
    "International Mathematical Olympiad\", July 2025: 35 of 42 points; at IMO 2025, 67 of 630 contestants won gold",
    "Seven Dreamers (the Laundroid): about $89 million raised; bankruptcy announced 23 April 2019; a planned price of "
    "about $16,000; in 2018 it struggled with ordinary T-shirts (Engadget and Digital Trends, April 2019)",
    "H. Moravec, Mind Children, 1988: \"it is comparatively easy to make computers exhibit adult level performance on "
    "intelligence tests or playing checkers, and difficult or impossible to give them the skills of a one-year-old when "
    "it comes to perception and mobility\"",
    "Eyes: animals with eyes appear in the Cambrian, more than 500 million years ago; limbs: Tiktaalik and the first "
    "tetrapods, ~375 million years ago (Daeschler, Shubin & Jenkins, Nature, 2006); written numbers: Mesopotamian tallies "
    "and proto-cuneiform, ~5,000 years ago",
    "R. S. Johansson & Å. B. Vallbo, J. Physiol. 286, 1979: ~17,000 tactile nerve fibres supply the palm-side (glabrous) "
    "skin of each hand",
    "IBM's Deep Blue beat Garry Kasparov, May 1997; Figure AI, Helix folding towels autonomously, 13 Aug 2025",
    "One day: 5,000 / 500,000,000 of 24 hours is under a second · Big Mac $6.22 (The Economist, July 2026): $16,000 is "
    "~2,570 Big Macs",
    "The section on a robot that moves like a toddler is a labelled what-if, not a forecast",
]
