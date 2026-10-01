"""EP10 · COUNTING SUMS: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|
sound|master|preview|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #regulation #euaiact #compute #goodhartslaw #tech #economics #thecurve"
CLIPS = [
    dict(name="part1", a="line", b="why", tag="COUNTING SUMS · PART 1 OF 3", nxt="PART 2",
         hook="One number decides which AI gets watched",
         post="Europe's AI Act presumes a model carries systemic risk if it took more than 10^25 calculations to train. Not a "
              "test score: a count of sums. Why? Part 1 of 3."),
    dict(name="part2", a="cant", b="move", tag="COUNTING SUMS · PART 2 OF 3", nxt="PART 3",
         hook="Why the law counts sums instead of danger",
         post="You can't measure how dangerous a model is before it exists, so the law measures the effort. California's line "
              "(SB 53, signed 29 Sep 2025) is 10x higher. And the compute for the same result halved about every 8 months. Part 2 of 3."),
    dict(name="part3", a="goodhart", b="now2", tag="COUNTING SUMS · PART 3 OF 3", nxt=None,
         hook="When a measure becomes a target",
         post="Goodhart's law: when a measure becomes a target, it stops being a good measure. Plus a labelled what-if: "
              "thinking rationed like carbon. Part 3 of 3."),
    dict(name="size", a="size", b="everyone", tag="COUNTING SUMS", nxt=None,
         hook="How big is 10^25?",
         post="If every person on Earth did one sum a second, 10^25 sums would take about 39 million years. That's the line "
              "in Europe's AI Act."),
    dict(name="dinosaur", a="cal", b="land", tag="COUNTING SUMS", nxt=None,
         hook="California's AI line: 390 million years of sums",
         post="California's frontier AI law (SB 53) starts at 10^26 operations: ten times Europe's line. In sums a second by "
              "everyone on Earth, about 390 million years, long before the first dinosaur."),
    dict(name="halves", a="halves", b="under", tag="COUNTING SUMS", nxt=None,
         hook="The compute for the same AI halves every 8 months",
         post="From 2012 to 2023, the compute language models needed for the same result halved about every eight months "
              "(Ho, Besiroglu et al., 2024). So a model can do more while staying under a fixed line."),
]
MUSIC = [(0.0, "intro"), ("what", "a"), ("why", "break"), ("cant", "a"), ("everyone", "b"), ("cal", "a"), ("halves", "b"),
         ("goodhart", "break"), ("count", "a"), ("imagine", "break"), ("allow", "a"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP10  ·  COUNTING SUMS", music=MUSIC, anchors=("cant", "cal"), clips=CLIPS, tags=TAGS,
                     bed="house:key=-3", deafen=("above", "imagine"))
