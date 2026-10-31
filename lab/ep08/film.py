"""EP08 · CHEAPER MAKES MORE: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|
sound|master|preview|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #economics #jevonsparadox #energy #tech #history #google #bigmac #thecurve"
CLIPS = [
    dict(name="part1", a="coal", b="lit", tag="CHEAPER MAKES MORE · PART 1 OF 3", nxt="PART 2",
         hook="Better engines made Britain burn MORE coal",
         post="1865: steam engines got far more efficient, so Britain should have burned less coal. It burned more. Then light got 3,000x cheaper, and we used 40,000x more. Part 1 of 3."),
    dict(name="part2", a="curve", b="nadella", tag="CHEAPER MAKES MORE · PART 2 OF 3", nxt="PART 3",
         hook="AI got 1,000x cheaper. Use exploded.",
         post="A million tokens: about $60 in 2021, about 6 cents by 2024. Google now handles 3.2 quadrillion tokens a month, 300x two years earlier. Part 2 of 3."),
    dict(name="part3", a="unlock", b="now2", tag="CHEAPER MAKES MORE · PART 3 OF 3", nxt=None,
         hook="What if thinking got as cheap as light?",
         post="Efficiency doesn't shrink demand. It unlocks it. That's why cheaper AI means more data centres, more power and more chips. Part 3 of 3."),
    dict(name="light", a="light", b="lit", tag="CHEAPER MAKES MORE", nxt=None,
         hook="Light got 3,000x cheaper. We used 40,000x more.",
         post="Britain, 1800 to 2000: the real price of light fell about 3,000-fold, and total use rose about 40,000-fold (Fouquet & Pearson). Streetlights, shop windows, screens."),
    dict(name="bigmacs", a="tokens", b="macs", tag="CHEAPER MAKES MORE", nxt=None,
         hook="A million AI tokens: from 10 Big Macs to 1/100 of one",
         post="A million tokens, about eight novels of text: around $60 in 2021, about six cents by 2024 (a16z). At $6.22 a Big Mac, from about ten to about a hundredth of one."),
    dict(name="google", a="google", b="times", tag="CHEAPER MAKES MORE", nxt=None,
         hook="Google handles 3.2 quadrillion AI tokens a month",
         post="Google I/O, May 2026: about 3,200 trillion tokens a month, more than 300 times the 9.7 trillion of two years earlier."),
    dict(name="nadella", a="nadella", b="why", tag="CHEAPER MAKES MORE", nxt=None,
         hook="\"Jevons paradox strikes again\"",
         post="When a cheap Chinese model shook the markets in January 2025, Satya Nadella posted: Jevons paradox strikes again. Cheaper AI means more data centres, not fewer."),
]
MUSIC = [(0.0, "intro"), ("engines", "a"), ("ai", "break"), ("mech", "a"), ("curve", "b"), ("unlock", "break"), ("why", "a"),
         ("imagine", "break"), ("uses", "a"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP08  ·  CHEAPER MAKES MORE", music=MUSIC, anchors=("mech", "curve"), clips=CLIPS, tags=TAGS,
                     bed="garage", deafen=("ai", "imagine"))
