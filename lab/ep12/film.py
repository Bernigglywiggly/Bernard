"""EP12 · SIXTEEN HOURS: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|parts|
join|sound|master|preview|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #agents #metr #exponential #future #tech #explained #thecurve"
CLIPS = [
    dict(name="part1", a="task", b="why", tag="SIXTEEN HOURS · PART 1 OF 3", nxt="PART 2",
         hook="This task takes a person 16 hours",
         post="In March 2026, METR measured an AI finishing tasks that take a skilled person about 16 hours, about half the "
              "time, on its own. Seven years earlier: two seconds. Part 1 of 3."),
    dict(name="part2", a="how", b="kind", tag="SIXTEEN HOURS · PART 2 OF 3", nxt="PART 3",
         hook="How do you measure an AI in hours?",
         post="METR's time horizon: time people on 228 tasks, give the same tasks to AI agents, find the length where the AI "
              "succeeds half the time. Only 5 tasks take 16 hours or more. At 80% success: about 3 hours. Part 2 of 3."),
    dict(name="part3", a="brains", b="now2", tag="SIXTEEN HOURS · PART 3 OF 3", nxt=None,
         hook="We think in steps. This grows in folds.",
         post="The horizon has doubled about every 7 months since 2019, closer to every 4 since 2023. Plus a labelled what-if: "
              "four more doublings. Part 3 of 3."),
    dict(name="ladder", a="name", b="ladder", tag="SIXTEEN HOURS", nxt=None,
         hook="2 seconds to 16 hours in 7 years",
         post="METR's time horizon, the task length an AI finishes half the time: about 2 seconds in 2019, 30 seconds in 2022, "
              "4 minutes in 2023, an hour by early 2025, at least 16 hours in March 2026."),
    dict(name="ruler", a="five", b="kind", tag="SIXTEEN HOURS", nxt=None,
         hook="The test is running out of ruler",
         post="Only 5 of METR's 228 tasks take a person 16 hours or more, so above that its numbers stop being reliable. And "
              "half the time isn't every time: at 80% success the same model's horizon was about 3 hours."),
    dict(name="paper", a="brains", b="doubling", tag="SIXTEEN HOURS", nxt=None,
         hook="Fold paper 42 times and it reaches the Moon",
         post="0.1 mm × 2^42 ≈ 440,000 km, past the Moon. We think in steps; this grows in folds. METR's time horizon has "
              "doubled about every 7 months since 2019, closer to every 4 since 2023."),
]
MUSIC = [(0.0, "intro"), ("spring", "a"), ("before", "break"), ("ruler", "a"), ("how", "b"), ("ladder", "a"), ("five", "b"),
         ("half", "break"), ("eighty", "a"), ("brains", "break"), ("folds", "a"), ("doubling", "b"), ("imagine", "break"),
         ("six", "a"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP12  ·  SIXTEEN HOURS", music=MUSIC, anchors=("how", "brains"), clips=CLIPS, tags=TAGS,
                     bed="house:key=4", deafen=("before", "imagine"))
