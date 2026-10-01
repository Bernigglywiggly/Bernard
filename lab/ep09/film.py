"""EP09 · THE LAUNDRY PROBLEM: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|
sound|master|preview|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #robots #robotics #moravec #science #evolution #tech #bigmac #thecurve"
CLIPS = [
    dict(name="part1", a="gold", b="why", tag="THE LAUNDRY PROBLEM · PART 1 OF 3", nxt="PART 2",
         hook="AI won maths gold. A laundry robot went bust.",
         post="July 2025: an AI scored gold at the International Mathematical Olympiad (35 of 42). A company that raised "
              "about $89 million to build a laundry-folding machine went bankrupt in 2019. Why is the exam easy and the "
              "laundry hard? Part 1 of 3."),
    dict(name="part2", a="moravec", b="hand", tag="THE LAUNDRY PROBLEM · PART 2 OF 3", nxt="PART 3",
         hook="Why the easy things are hardest for robots",
         post="Moravec's paradox (1988): tests are easy for computers; the skills of a one-year-old are hard. Seeing is 500 "
              "million years old, written numbers about 5,000. Part 2 of 3."),
    dict(name="part3", a="chess", b="now2", tag="THE LAUNDRY PROBLEM · PART 3 OF 3", nxt=None,
         hook="Chess fell in 1997. The laundry hasn't.",
         post="Difficulty isn't how clever a skill is; it's how recently we learned it. The oldest skills, hands, eyes, "
              "reading a room, may be the last to go. Part 3 of 3."),
    dict(name="olympiad", a="gold", b="few", tag="THE LAUNDRY PROBLEM", nxt=None,
         hook="An AI scored gold at the maths olympiad",
         post="IMO 2025: Google DeepMind's Gemini Deep Think scored 35 of 42, gold-medal standard. Only 67 of the 630 "
              "young mathematicians competing did the same."),
    dict(name="day", a="eyes", b="day", tag="THE LAUNDRY PROBLEM", nxt=None,
         hook="If evolution were one day, maths arrived in the last second",
         post="Seeing: 500+ million years. Limbs: about 375 million. Writing numbers down: about 5,000 years. That's why "
              "robots learn exams before laundry."),
    dict(name="hand", a="hand", b="macs", tag="THE LAUNDRY PROBLEM", nxt=None,
         hook="17,000 touch nerve fibres in the palm side of one hand",
         post="Your palm side alone has about 17,000 touch nerve fibres (Johansson & Vallbo, 1979). Chess fell to a "
              "computer in 1997; in August 2025 a humanoid folding towels was still news."),
    dict(name="toddler", a="imagine", b="you", tag="THE LAUNDRY PROBLEM · A WHAT-IF", nxt=None,
         hook="The first robot that moves like a toddler",
         post="Not a forecast, a what-if: unsteady, curious, able to pick up anything. What changes in a care home, a "
              "kitchen, a building site? And which parts of your job are the oldest skills you have?"),
]
MUSIC = [(0.0, "intro"), ("few", "a"), ("why", "break"), ("moravec", "a"), ("eyes", "b"), ("chess", "a"), ("idea", "break"),
         ("flip", "a"), ("imagine", "break"), ("where", "a"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP09  ·  THE LAUNDRY PROBLEM", music=MUSIC, anchors=("moravec", "chess"), clips=CLIPS, tags=TAGS,
                     bed="garage:key=3", deafen=("bust", "imagine"))
