"""EP11 · THE LIBRARY OF EVERY BOOK: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|
render|sound|master|preview|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #chatgpt #hallucination #borges #libraryofbabel #tech #explained #thecurve"
CLIPS = [
    dict(name="part1", a="library", b="why", tag="THE LIBRARY OF EVERY BOOK · PART 1 OF 4", nxt="PART 2",
         hook="A library that holds every possible book",
         post="In 1941, Borges imagined a library holding every possible book: the answer to every question, and every wrong "
              "answer too. You'd never find the right one. Today's AI works the other way round. Part 1 of 4."),
    dict(name="part2", a="size", b="shannon", tag="THE LIBRARY OF EVERY BOOK · PART 2 OF 4", nxt="PART 3",
         hook="AI keeps patterns, not pages",
         post="Borges' library: a number of books with 1.8 million digits. Meta's Llama 3 read 15 trillion tokens into a model "
              "hundreds of times smaller. It can't have kept the pages. Part 2 of 4."),
    dict(name="part3", a="fluent", b="idk", tag="THE LIBRARY OF EVERY BOOK · PART 3 OF 4", nxt="PART 4",
         hook="Why AI makes things up",
         post="Fluent by design, right by effort. A fact seen once in training is a fact a model often gets wrong (Kalai et al., "
              "OpenAI, 2025). And tests reward confident guessing. Part 3 of 4."),
    dict(name="part4", a="path", b="now2", tag="THE LIBRARY OF EVERY BOOK · PART 4 OF 4", nxt=None,
         hook="A librarian beside every child",
         post="Likely isn't true: finding is the machine's job now, checking is still ours. Plus a labelled what-if: an AI tutor "
              "for every child. Part 4 of 4."),
    dict(name="digits", a="size", b="atoms", tag="THE LIBRARY OF EVERY BOOK", nxt=None,
         hook="Bigger than the universe",
         post="Borges' Library of Babel holds 25^1,312,000 books: a number with 1,834,098 digits. The number of atoms in the "
              "observable universe has 81."),
    dict(name="birthday", a="birthday", b="fifth", tag="THE LIBRARY OF EVERY BOOK", nxt=None,
         hook="Three tries, three wrong birthdays",
         post="OpenAI researchers asked a leading open model for a co-author's birthday, to answer only if it knew: three tries, "
              "three different wrong dates. If a fifth of such facts appear once in training, expect at least a fifth wrong."),
    dict(name="guess", a="guess", b="idk", tag="THE LIBRARY OF EVERY BOOK", nxt=None,
         hook="The AI that always guesses",
         post="On OpenAI's SimpleQA quiz, a model that nearly always guessed was wrong 75% of the time. One that said \"I don't "
              "know\" half the time was wrong 26%, and right almost as often (22% vs 24%)."),
    dict(name="tutor", a="bloom", b="nigeria", tag="THE LIBRARY OF EVERY BOOK", nxt=None,
         hook="An AI tutor: up to 2 years in 6 weeks?",
         post="Bloom, 1984: one-to-one tutoring lifted the average student above 98% of a normal class. A 2024 World Bank trial "
              "in Nigeria: six weeks with an AI tutor after school, gains put at 1.5 to 2 years of school."),
]
MUSIC = [(0.0, "intro"), ("rule", "a"), ("never", "break"), ("opposite", "a"), ("size", "b"), ("read", "a"), ("shannon", "b"),
         ("fluent", "break"), ("once", "a"), ("guess", "b"), ("path", "break"), ("likely", "a"), ("imagine", "break"),
         ("bloom", "a"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP11  ·  THE LIBRARY OF EVERY BOOK", music=MUSIC, anchors=("size", "fluent"), clips=CLIPS,
                     tags=TAGS, bed="garage:key=-1", deafen=("never", "imagine"))
