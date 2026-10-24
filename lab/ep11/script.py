"""EP11 · THE LIBRARY OF EVERY BOOK, v1 (1 Oct 2026), from the episode bank (lab/format/EPISODES.md). The Curve's
format (lab/inspo/pollar_playbook.md): a concrete hook, the hidden mechanism, numbers made physical, what's reported vs
known said plainly, one labelled what-if, a mirrored close. George (ElevenLabs) at his own pace; no jokes. Score: Arena.

The hidden mechanism: a language model is a compressor. It reads far more text than it could ever store, so it keeps
the patterns, not the pages (Shannon: predicting the next letter and compressing text are one problem; DeepMind 2023:
a model trained mostly on text squeezes photos smaller than PNG; in the sources, not the script). So it is fluent by design and right only where the
pattern carries the fact: a fact seen once in training is a fact it will often get wrong, and tests that reward a
confident guess make that worse (OpenAI, 2025).

Fields as in lab/ep03s/script.py: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="library", card=("1941", "JORGE LUIS BORGES · THE LIBRARY OF BABEL"),
         text="In 1941, Jorge Luis Borges imagined a library that holds every possible book.",
         say="In nineteen forty-one, Jorge Luis Borges imagined a library that holds every possible book."),
    dict(floor=0, id="rule", text="Every arrangement of letters, spaces, commas and full stops, 410 pages long, is on a shelf somewhere.",
         say="Every arrangement of letters, spaces, commas and full stops, four hundred and ten pages long, is on a shelf somewhere."),
    dict(floor=0, id="answer", text="So somewhere in it is the answer to every question you could ask. And every wrong answer too."),
    dict(floor=0, id="never", cut=True, text="You would never find the right one."),
    dict(floor=0, id="opposite", air=1, text="Today's AI works the other way round. It keeps patterns, not pages. And it answers in seconds."),
    dict(floor=0, id="why", air=1, text="How do you answer from books you didn't keep?"),
    # 1 · MECHANISM: the size of everything, and a model that is a compression
    dict(floor=1, id="size", card=("1,834,098", "DIGITS · THE NUMBER OF BOOKS IN BORGES' LIBRARY"),
         text="Borges' library is big. Written out, the number of books has more than 1.8 million digits.",
         say="Borges' library is big. Written out, the number of books has more than one point eight million digits."),
    dict(floor=1, id="atoms", card=("10⁸⁰", "ATOMS IN THE OBSERVABLE UNIVERSE · 81 DIGITS"),
         text="The number of atoms in the observable universe has 81.",
         say="The number of atoms in the observable universe has eighty-one."),
    dict(floor=1, id="read", air=1, card=("15 TRILLION", "TOKENS · META'S LLAMA 3, 2024"),
         text="Now a real model. In 2024, Meta trained Llama 3 on more than 15 trillion tokens: pieces of words.",
         say="Now a real model. In twenty twenty-four, Meta trained Llama 3 on more than fifteen trillion tokens: pieces of words."),
    dict(floor=1, id="kept", card=("~140 GB", "THE BIGGER LLAMA 3 · FROM TENS OF TERABYTES OF TEXT"),
         text="Tens of terabytes of text, into a model hundreds of times smaller."),
    dict(floor=1, id="patterns", cut=True, text="It can't have kept the pages. It kept what text tends to look like: which word usually comes next."),
    dict(floor=1, id="shannon", air=1, card=("1951", "CLAUDE SHANNON · PREDICTION AND ENTROPY OF PRINTED ENGLISH"),
         text="In 1951, Claude Shannon showed why that works: guessing the next letter and compressing text are the same problem.",
         say="In nineteen fifty-one, Claude Shannon showed why that works: guessing the next letter and compressing text are the same problem."),
    # 2 · NOW: fluent by design, right by effort
    dict(floor=2, id="fluent", air=2, cut=True, text="That's the trade. A model is fluent by design. Being right takes more."),
    dict(floor=2, id="once", text="When a fact appears thousands of times, the pattern carries it. When it appears once, there's no pattern."),
    dict(floor=2, id="birthday", card=("3 TRIES", "3 DIFFERENT WRONG DATES"),
         text="OpenAI researchers asked a leading open model for a co-author's birthday, and to answer only if it knew. Three tries, three wrong dates."),
    dict(floor=2, id="fifth", card=("20% → 20%", "FACTS SEEN ONCE · AT LEAST AS MANY WRONG"),
         text="Their maths: if a fifth of such facts appear only once in training, expect the raw model to get at least a fifth of them wrong."),
    dict(floor=2, id="guess", air=1, card=("75%", "WRONG · THE MODEL THAT NEARLY ALWAYS GUESSED"),
         text="And tests reward a confident guess. On one quiz, a model that nearly always guessed was wrong 75% of the time.",
         say="And tests reward a confident guess. On one quiz, a model that nearly always guessed was wrong seventy-five percent of the time."),
    dict(floor=2, id="idk", card=("26%", "WRONG · THE ONE THAT SAID \"I DON'T KNOW\""),
         text="One that said \"I don't know\" half the time was wrong 26%, and right almost as often.",
         say="One that said I don't know half the time was wrong twenty-six percent, and right almost as often."),
    # 3 · IDEA
    dict(floor=3, id="path", air=2, cut=True,
         text="Borges' library had every true page and no way to find it. A model finds a likely page at once."),
    dict(floor=3, id="likely", text="But likely isn't true. Finding is the machine's job now. Checking is still ours."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine a librarian who has read every shelf, beside every child on Earth."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="bloom", card=("98%", "OF A NORMAL CLASS · BELOW THE AVERAGE TUTORED STUDENT · BLOOM, 1984"),
         text="In 1984, Benjamin Bloom reported that one-to-one tutoring lifted the average student above 98% of a normal class. Too costly for everyone.",
         say="In nineteen eighty-four, Benjamin Bloom reported that one-to-one tutoring lifted the average student above ninety-eight percent of a normal class. Too costly for everyone."),
    dict(floor=4, id="nigeria", card=("6 WEEKS", "≈ 1.5 TO 2 YEARS OF SCHOOL · WORLD BANK TRIAL, NIGERIA"),
         text="In 2024, in Nigeria, six weeks of after-school sessions with an AI tutor gave gains a World Bank team put at one and a half to two years of school.",
         say="In twenty twenty-four, in Nigeria, six weeks of after-school sessions with an AI tutor gave gains a World Bank team put at one and a half to two years of school."),
    dict(floor=4, id="question", air=1, text="If every child had that librarian, what would school be for?"),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="Borges imagined every book, and no way to find the one you need."),
    dict(floor=5, id="now2", cut=True, text="We built the opposite: the page you ask for, and no promise it's true."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "J. L. Borges, \"La biblioteca de Babel\" (1941; in El jardín de senderos que se bifurcan): books of 410 pages, 40 "
    "lines a page, about 80 letters a line, 25 symbols (22 letters, the space, the comma, the full stop); 25^1,312,000 "
    "≈ 1.96 × 10^1,834,097 books, a number of 1,834,098 digits",
    "The observable universe: about 10^80 atoms (a common order-of-magnitude estimate)",
    "Meta, \"Introducing Meta Llama 3\" (18 April 2024): pretrained on over 15T tokens from publicly available sources; "
    "8B and 70B parameters. A 70B model at 16 bits is about 140 GB; 15T tokens at about 4 bytes a token is about 60 TB",
    "C. E. Shannon, \"Prediction and Entropy of Printed English\", Bell System Technical Journal, 1951",
    "G. Delétang et al. (Google DeepMind), \"Language Modeling Is Compression\", 2023 (ICLR 2024): Chinchilla 70B "
    "compressed ImageNet patches to 43.4% of their size, PNG to 58.5%; LibriSpeech 16.4% vs FLAC 30.3%",
    "A. T. Kalai, O. Nachum, S. Vempala, E. Zhang, \"Why Language Models Hallucinate\" (OpenAI, 4 Sep 2025): three "
    "attempts, three wrong birthdays; \"if 20% of birthday facts appear exactly once in the pretraining data, then one "
    "expects base models to hallucinate on at least 20% of birthday facts\"",
    "OpenAI, \"Why language models hallucinate\" (5 Sep 2025), SimpleQA: o4-mini abstained 1%, accurate 24%, wrong 75%; "
    "gpt-5-thinking-mini abstained 52%, accurate 22%, wrong 26%",
    "B. S. Bloom, \"The 2 Sigma Problem\", Educational Researcher, 1984: \"the average tutored student was above 98% of "
    "the students in the control class\"",
    "M. De Simone et al., \"From Chalkboards to Chatbots\", World Bank Policy Research Working Paper 11125 (2025): a "
    "six-week after-school programme with Microsoft Copilot (GPT-4) in Benin City, Edo State, June-July 2024; +0.31 SD, "
    "which the authors equate to 1.5 to 2 years of business-as-usual schooling",
    "The section on a librarian beside every child is a labelled what-if, not a forecast",
]
