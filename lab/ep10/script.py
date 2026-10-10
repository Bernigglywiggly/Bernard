"""EP10 · COUNTING SUMS, v1 (30 Sep 2026), from the episode bank (lab/format/EPISODES.md: "The Number That Decides What
Gets Watched"). The Curve's format (lab/inspo/pollar_playbook.md): a concrete hook, the hidden mechanism, numbers made
physical, what's reported vs known said plainly, one labelled what-if, a mirrored close. George (ElevenLabs) at his own
pace; no jokes. Score: Arena.

The hidden mechanism: you can't measure how dangerous a model is before it exists, so the law measures the arithmetic
that built it (training compute). Europe presumes "systemic risk" above 10^25 operations; California's frontier law
starts at 10^26. But the arithmetic needed for the same ability keeps falling (Ho et al.: it halves about every eight
months), and a line that becomes a target stops measuring what it was drawn for (Goodhart's law).
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="line", card=("10²⁵", "OPERATIONS · EU AI ACT, ARTICLE 51"),
         text="In Europe, one number decides which AI models get the closest watch: ten to the power of twenty-five.",
         say="In Europe, one number decides which AI models get the closest watch: ten to the power of twenty-five."),
    dict(floor=0, id="what", text="It isn't a test score. It's how many calculations it took to train the model."),
    dict(floor=0, id="above", cut=True, text="Above it, the law presumes the model carries systemic risk."),
    dict(floor=0, id="why", air=1, text="Why would a law count sums?"),
    # 1 · MECHANISM: you can't measure danger, so you measure effort
    dict(floor=1, id="cant", text="Because you can't measure how dangerous a model is before it exists. You can measure the effort that built it."),
    dict(floor=1, id="more", text="For a decade, more training compute has meant more capable models. So effort stands in for danger."),
    dict(floor=1, id="size", air=1, cut=True, text="Here's how big the number is."),
    dict(floor=1, id="everyone", card=("39,000,000", "YEARS · EVERYONE ON EARTH, ONE SUM A SECOND"),
         text="If every person on Earth did one sum a second, it would take about 39 million years.",
         say="If every person on Earth did one sum a second, it would take about thirty-nine million years."),
    # 2 · NOW: two lines, and a moving target
    dict(floor=2, id="cal", air=1, card=("10²⁶", "CALIFORNIA · SB 53 · SIGNED 29 SEPTEMBER 2025"),
         text="California drew its line ten times higher, in a law signed on the 29th of September 2025.",
         say="California drew its line ten times higher, in a law signed on the twenty-ninth of September twenty twenty-five."),
    dict(floor=2, id="land", card=("390,000,000", "YEARS · LONG BEFORE THE FIRST DINOSAUR"),
         text="In sums a second, that's 390 million years. Long before the first dinosaur.",
         say="In sums a second, that's three hundred and ninety million years. Long before the first dinosaur."),
    dict(floor=2, id="halves", card=("8 MONTHS", "TO HALVE THE COMPUTE FOR THE SAME RESULT"),
         text="But the arithmetic needed for the same ability keeps falling. For language models, from 2012 to 2023, it halved about every eight months.",
         say="But the arithmetic needed for the same ability keeps falling. For language models, from twenty twelve to twenty twenty-three, it halved about every eight months."),
    dict(floor=2, id="under", text="So a model can do more while staying under the line."),
    dict(floor=2, id="move", text="Europe's law expects this. It lets the Commission move the number as the technology moves."),
    # 3 · IDEA
    dict(floor=3, id="goodhart", air=2, cut=True, card=("1975", "CHARLES GOODHART"),
         text="There's a name for the trap. Goodhart's law: when a measure becomes a target, it stops being a good measure.",
         say="There's a name for the trap. Goodhart's law: when a measure becomes a target, it stops being a good measure."),
    dict(floor=3, id="count", text="A line in sums works until builders start counting the sums."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine thinking rationed like carbon."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="allow", text="Every lab gets an allowance of sums. Spare ones are traded. The price of a thought goes up and down like fuel."),
    dict(floor=4, id="question", air=1, text="Who would set the allowance? And what would we choose not to think?"),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="They couldn't count the danger."),
    dict(floor=5, id="now2", cut=True, text="So they counted the sums."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "EU AI Act (Regulation 2024/1689), Article 51: a general-purpose model is presumed to have high-impact capabilities "
    "(systemic risk) when its training used more than 10^25 floating-point operations; Article 51(3) lets the Commission "
    "amend the threshold by delegated act; the general-purpose AI rules applied from 2 August 2025",
    "California SB 53, the Transparency in Frontier Artificial Intelligence Act, signed 29 September 2025: frontier models "
    "are those trained with more than 10^26 operations",
    "A. Ho, T. Besiroglu et al., \"Algorithmic progress in language models\", NeurIPS 2024 (Epoch AI): the compute needed "
    "to reach a set performance halved about every 8 months (95% CI ~5-14 months), 2012-2023",
    "C. Goodhart, 1975: \"Any observed statistical regularity will tend to collapse once pressure is placed upon it for "
    "control purposes\"; M. Strathern, 1997: \"When a measure becomes a target, it ceases to be a good measure\"",
    "J. Kaplan et al., \"Scaling laws for neural language models\", 2020, and J. Hoffmann et al., 2022: performance improves "
    "predictably with training compute",
    "The sums: 10^25 / 8.2 billion people / 31.6 million seconds a year ≈ 39 million years; 10^26 ≈ 390 million years; "
    "the first dinosaurs appear ~230-245 million years ago",
    "The section on thinking rationed like carbon is a labelled what-if, not a forecast",
]
