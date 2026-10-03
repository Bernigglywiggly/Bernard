"""EP08 · CHEAPER MAKES MORE, v1 (28 Sep 2026), from the episode bank (lab/format/EPISODES.md). The Curve's format
(lab/inspo/pollar_playbook.md): a concrete hook, the hidden mechanism, numbers made physical (Big Macs for money),
what's reported vs known said plainly, one labelled what-if, a mirrored close. George (ElevenLabs), fast; no jokes.
Bed: Terminal (a machine thinking).

The hidden mechanism: the Jevons paradox. When something gets cheaper to use, we don't just save, we find new uses,
so total use can rise. Coal (1865), light (3,000x cheaper, 40,000x more used in Britain, 1800-2000), and now AI
(a million tokens from ~$60 to ~$0.06; Google's monthly tokens up 300x in two years). So cheaper AI means more data
centres, power and chips, not fewer.

Fields as in lab/ep03s/script.py: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="coal", card=("1865", "WILLIAM STANLEY JEVONS · THE COAL QUESTION"),
         text="In 1865, a British economist noticed something strange about coal.",
         say="In eighteen sixty-five, a British economist noticed something strange about coal."),
    dict(floor=0, id="engines", text="Steam engines had become far more efficient. They needed much less coal for the same work."),
    dict(floor=0, id="more", cut=True, text="So Britain should have burned less coal. It burned more."),
    dict(floor=0, id="ai", air=1, text="The same thing is now happening to AI."),
    # 1 · MECHANISM: cheaper makes more
    dict(floor=1, id="mech", text="Here's the mechanism. When something gets cheaper, we don't just save money. We find new things to use it for."),
    dict(floor=1, id="light", card=("3,000×", "CHEAPER LIGHT · BRITAIN, 1800–2000"),
         text="Light is the clearest case. Between 1800 and 2000, the real price of light in Britain fell about 3,000 times.",
         say="Light is the clearest case. Between eighteen hundred and two thousand, the real price of light in Britain fell about three thousand times."),
    dict(floor=1, id="used", card=("40,000×", "MORE LIGHT USED"),
         text="We didn't pocket the savings. We used about 40,000 times more light.",
         say="We didn't pocket the savings. We used about forty thousand times more light."),
    dict(floor=1, id="lit", text="Streetlights. Shop windows. Screens. Things nobody would have lit when light cost a fortune."),
    # 2 · NOW: the same curve
    dict(floor=2, id="curve", air=1, cut=True, text="AI is on the same curve."),
    dict(floor=2, id="tokens", card=("$60 → $0.06", "A MILLION TOKENS, 2021 → 2024 · a16z"),
         text="A million tokens of AI, about eight novels of text, cost around $60 in 2021. By 2024, about six cents.",
         say="A million tokens of AI, about eight novels of text, cost around sixty dollars in twenty twenty-one. By twenty twenty-four, about six cents."),
    dict(floor=2, id="macs", card=("10 → 1/100", "BIG MACS PER MILLION TOKENS"),
         text="In Big Macs: from about ten, to about a hundredth of one."),
    dict(floor=2, id="google", card=("3.2 QUADRILLION", "TOKENS A MONTH · GOOGLE, MAY 2026"),
         text="And use exploded. Google now handles about 3.2 quadrillion tokens a month.",
         say="And use exploded. Google now handles about three point two quadrillion tokens a month."),
    dict(floor=2, id="times", card=("300×", "IN TWO YEARS"),
         text="More than 300 times what it handled two years earlier.", say="More than three hundred times what it handled two years earlier."),
    dict(floor=2, id="nadella", card=("27 JAN 2025", "SATYA NADELLA, MICROSOFT"),
         text="When a cheap Chinese model shook the markets in January 2025, Microsoft's boss posted: Jevons paradox strikes again.",
         say="When a cheap Chinese model shook the markets in January twenty twenty-five, Microsoft's boss posted: Jevons paradox strikes again."),
    # 3 · IDEA
    dict(floor=3, id="unlock", air=2, cut=True, text="Efficiency doesn't shrink demand. It unlocks it."),
    dict(floor=3, id="why", text="That's why cheaper AI means more data centres, more power and more chips. Not fewer."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine thinking gets as cheap as light."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="uses", text="What would we use it for that nobody bothers with today? A tutor for every child. A second look at every scan. A patient explanation of every letter you don't understand."),
    dict(floor=4, id="question", air=1, text="The question isn't how much we'll save. It's how much more we'll do."),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="In 1865, better engines burned more coal.", say="In eighteen sixty-five, better engines burned more coal."),
    dict(floor=5, id="now2", cut=True, text="In 2026, cheaper thinking means more thinking.", say="In twenty twenty-six, cheaper thinking means more thinking."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "W. S. Jevons, The Coal Question, 1865: \"It is wholly a confusion of ideas to suppose that the economical use of "
    "fuel is equivalent to a diminished consumption. The very contrary is the truth.\"",
    "R. Fouquet & P. Pearson, \"Seven Centuries of Energy Services: The Price and Use of Light in the United Kingdom "
    "(1300-2000)\", The Energy Journal 27(1), 2006: the real price of light fell ~3,000-fold and total use rose "
    "~40,000-fold, 1800-2000",
    "a16z, \"Welcome to LLMflation\" (Nov 2024): a million tokens at GPT-3-level capability, ~$60 (2021) to ~$0.06 "
    "(2024); a million tokens is ~750,000 words, about eight novels",
    "Google I/O, May 2026: ~3,200 trillion tokens a month, up from 9.7 trillion two years earlier",
    "Satya Nadella on LinkedIn and X, 27 Jan 2025: \"Jevons paradox strikes again!\"",
    "Big Mac $6.22 (The Economist, July 2026): $60 is ~9.6 Big Macs, $0.06 is ~1/100 of one",
    "The section on thinking as cheap as light is a labelled what-if, not a forecast",
]
