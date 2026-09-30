"""EP07 · THE THIRTY-YEAR DELAY: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|
sound|master|preview|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #productivity #economics #history #electricity #business #work #tech #thecurve"
CLIPS = [
    dict(name="part1", a="survey", b="decades", tag="THE THIRTY-YEAR DELAY · PART 1 OF 3", nxt="PART 2",
         hook="6,000 bosses were asked what AI did for them",
         post="Nearly nine in ten said: nothing. No change in productivity, no change in jobs (NBER, Feb 2026). This has happened before. Part 1 of 3."),
    dict(name="part2", a="five", b="fifty", tag="THE THIRTY-YEAR DELAY · PART 2 OF 3", nxt="PART 3",
         hook="Why electricity took decades to pay off",
         post="Factories swapped the steam engine for one big electric motor and changed nothing else. The gains came when they rebuilt around the motor. Part 2 of 3."),
    dict(name="part3", a="solow", b="now2", tag="THE THIRTY-YEAR DELAY · PART 3 OF 3", nxt=None,
         hook="AI is stuck at the one-big-motor stage",
         post="\"You can see the computer age everywhere but in the productivity statistics\" (Solow, 1987). 95% of company AI pilots made no measurable return (MIT, 2025). Part 3 of 3."),
    dict(name="nothing", a="survey", b="hours", tag="THE THIRTY-YEAR DELAY", nxt=None,
         hook="AI changed nothing for 9 in 10 companies. So far.",
         post="An NBER survey of about 6,000 executives in the US, UK, Germany and Australia (Feb 2026): nearly 90% saw no change in productivity or jobs from AI. The bosses who used it averaged 1.5 hours a week."),
    dict(name="shaft", a="shaft", b="same", tag="THE THIRTY-YEAR DELAY", nxt=None,
         hook="The mistake every factory made with electricity",
         post="Old factories ran on one steam engine turning one long shaft, with belts to every machine. Owners swapped in one big electric motor and changed nothing else. Same shaft, same belts, small savings."),
    dict(name="redesign", a="redesign", b="fifty", tag="THE THIRTY-YEAR DELAY", nxt=None,
         hook="The redesign that finally made electricity pay",
         post="A small motor in every machine, laid out along the flow of the work. By 1920 half of US factory power was electric, and productivity surged (Paul David, 1990)."),
    dict(name="pilots", a="pilots", b="shapes", tag="THE THIRTY-YEAR DELAY", nxt=None,
         hook="Why 95% of company AI pilots don't pay",
         post="MIT's 2025 study: 95% of company AI pilots made no measurable return. Mostly bolted onto the old routine. The tool is rarely the bottleneck. The layout is."),
    dict(name="office", a="imagine", b="look", tag="THE THIRTY-YEAR DELAY · A WHAT-IF", nxt=None,
         hook="What an office built from zero around AI loses first",
         post="Not a forecast, a what-if: the weekly status meeting, the inbox, the jobs that only move information from one place to another."),
]
MUSIC = [(0.0, "intro"), ("nothing", "a"), ("before", "break"), ("edison", "a"), ("redesign", "b"), ("solow", "a"), ("pilots", "b"),
         ("layout", "break"), ("imagine", "break"), ("first", "a"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP07  ·  THE THIRTY-YEAR DELAY", music=MUSIC, anchors=("edison", "solow"), clips=CLIPS, tags=TAGS,
                     bed="arena:key=1", deafen=("before", "imagine"))
