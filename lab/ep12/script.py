"""EP12 · SIXTEEN HOURS, v2 (1 Oct 2026): the bank's EP01 (lab/format/EPISODES.md; the 9:16 cut in lab/ep01) rebuilt
for the 16:9 films. The Curve's format (lab/inspo/pollar_playbook.md): a concrete hook, the hidden mechanism, numbers
made physical, what's reported vs known said plainly, one labelled what-if, a mirrored close. George (ElevenLabs) at his
own pace; no jokes. Score: Arena.

The hidden mechanism: METR's time horizon. Time skilled people on a few hundred tasks, give the same tasks to AI agents,
find the task length where the agent succeeds half the time. It has doubled about every seven months since 2019 and
about every four since 2023, and in spring 2026 it reached the end of the ruler: at least 16 hours, where METR has only
five tasks that long and calls its numbers unreliable. Said carefully (lab/research/script_facts.md, "say this, not
that"): half the time, on mostly software tasks; at 80% the same model's horizon was about three hours.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="task", card=("16 H", "HUMAN EXPERT TIME"),
         text="This task takes a skilled person about sixteen hours. Two full working days."),
    dict(floor=0, id="spring", card=("≥ 16 H · 50%", "TIME HORIZON · METR, MARCH 2026"),
         text="In March 2026, an AI was measured finishing tasks like it about half the time. On its own."),
    dict(floor=0, id="before", cut=True, card=("2 SEC", "2019 · METR"),
         text="Seven years earlier, the best AI could only manage tasks that take you two seconds."),
    dict(floor=0, id="ruler", air=1, text="And the people measuring it are running out of ruler."),
    dict(floor=0, id="why", air=1, text="How do you measure something that outgrows the test?"),
    # 1 · MECHANISM: the time horizon
    dict(floor=1, id="how", card=("228 TASKS", "METR TIME HORIZON 1.1 · JANUARY 2026"),
         text="A research group called METR timed skilled people on 228 tasks. Coding, research, fixing broken systems. From a few seconds to two working days.",
         say="A research group called meter timed skilled people on two hundred and twenty-eight tasks. Coding, research, fixing broken systems. From a few seconds to two working days."),
    dict(floor=1, id="same", text="Then they gave the same tasks to AI agents, and found the length of task where the AI succeeds half the time."),
    dict(floor=1, id="name", cut=True, text="They call it the time horizon."),
    dict(floor=1, id="ladder", air=1,
         text="Two seconds in 2019. About thirty seconds in 2022. Four minutes in 2023. An hour by early 2025. Sixteen hours in 2026.",
         say="Two seconds in twenty nineteen. About thirty seconds in twenty twenty-two. Four minutes in twenty twenty-three. An hour by early twenty twenty-five. Sixteen hours in twenty twenty-six."),
    dict(floor=1, id="five", card=("5 OF 228", "TASKS THAT TAKE A PERSON 16 HOURS OR MORE"),
         text="But only five of the 228 tasks take a person sixteen hours or more. Above that, METR says its numbers stop being reliable.",
         say="But only five of the two hundred and twenty-eight tasks take a person sixteen hours or more. Above that, meter says its numbers stop being reliable."),
    # 2 · NOW: what half the time means
    dict(floor=2, id="half", air=2, cut=True, text="And half the time is not every time."),
    dict(floor=2, id="eighty", card=("3 H 6 MIN", "THE SAME MODEL · AT 80% SUCCESS"),
         text="Ask for eighty percent success, and the same model's horizon falls to about three hours.",
         say="Ask for eighty percent success, and the same model's horizon falls to about three hours."),
    dict(floor=2, id="kind", text="The tasks are mostly software, with a clear goal and a way to check the answer. Not a wedding speech. Not a hard conversation."),
    # 3 · IDEA: we think in steps, this grows in folds
    dict(floor=3, id="brains", air=2, cut=True, text="Here's what our brains get wrong."),
    dict(floor=3, id="folds", text="We think in steps. This grows in folds."),
    dict(floor=3, id="paper", card=("42 FOLDS", "0.1 MM × 2⁴² ≈ 440,000 KM · THE MOON: 384,400 KM"),
         text="Fold a sheet of paper forty-two times, and it would reach past the Moon."),
    dict(floor=3, id="doubling", card=("× 2", "EVERY ~7 MONTHS SINCE 2019 · ~4 SINCE 2023"),
         text="Since 2019, the horizon has doubled about every seven months. Since 2023, closer to every four.",
         say="Since twenty nineteen, the horizon has doubled about every seven months. Since twenty twenty-three, closer to every four."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine the folds keep coming."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="six", card=("256 H", "4 MORE DOUBLINGS · ABOUT 6 WORKING WEEKS"),
         text="Four more doublings, under a year and a half at that pace, and sixteen hours becomes two hundred and fifty-six. Six working weeks."),
    dict(floor=4, id="project", text="Not a chore. A project. The first version of the business. The first draft of the book."),
    dict(floor=4, id="question", air=1, text="What would you hand over? And what would you keep?"),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="It took six years to get from two seconds to an hour."),
    dict(floor=5, id="now2", cut=True, text="It took about one more to get from an hour to sixteen."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "METR, \"Measuring AI Ability to Complete Long Tasks\" (19 Mar 2025): the 50% time horizon doubled about every 7 "
    "months from 2019; about 2 s (2019), about 30 s (2022), about 4 min (Mar 2023), about 1 h (early 2025)",
    "METR, \"Time Horizon 1.1\" (29 Jan 2026): 228 tasks (31 of 8 hours or more); post-2023 doubling about 130.8 days",
    "METR on an early Claude Mythos Preview, evaluated March 2026 (published May 2026): 50% time horizon at least 16 h "
    "(95% CI 8.5-55 h); 80% time horizon about 3 h 6 min; only 5 of the 228 tasks take people 16 h or more, and "
    "measurements above 16 h are unreliable with the current suite",
    "METR, \"Clarifying limitations of time horizon\" (22 Jan 2026): the tasks are mostly software and research work "
    "with automatic scoring; a horizon is not how long a model can work, nor any job of that length",
    "Paper folding: 0.1 mm × 2^42 ≈ 439,805 km; the mean Earth-Moon distance is 384,400 km",
    "The what-if (not a forecast): 16 h × 2^4 = 256 h; four doublings at ~4.3 months ≈ 17 months; 256 h / 40 h a week "
    "≈ 6.4 working weeks",
]
