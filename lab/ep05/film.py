"""EP05 · FOLLOW THE SUN: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|sound|
master|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #space #google #spacex #datacenter #satellites #energy #tech #bigmac #thecurve"
CLIPS = [
    dict(name="part1", a="launch", b="why", tag="FOLLOW THE SUN · PART 1 OF 4", nxt="PART 2",
         hook="Why is the AI industry trying to leave the planet?",
         post="Google is sending four of its AI chips into orbit. Last December a satellite the size of a fridge trained an AI model in space. Part 1 of 4."),
    dict(name="part2", a="mill", b="eight", tag="FOLLOW THE SUN · PART 2 OF 4", nxt="PART 3",
         hook="Mills followed rivers. Computers follow electricity.",
         post="Data centres already use about 1.5% of the world's electricity, heading for about all of Japan's by 2030. In orbit, a panel can collect up to 8x the energy. Part 2 of 4."),
    dict(name="part3", a="filings", b="hard", tag="FOLLOW THE SUN · PART 3 OF 4", nxt="PART 4",
         hook="SpaceX has asked to launch up to a million satellites",
         post="There are about 16,500 working satellites today. The catch is the ticket: about $7,000 a kilo to orbit. Part 3 of 4."),
    dict(name="part4", a="every", b="now2", tag="FOLLOW THE SUN · PART 4 OF 4", nxt=None,
         hook="Who owns the sunlight?",
         post="Every age builds its machines next to its power: the river, the coal field, the reactor. Now, maybe, the sun. Part 4 of 4."),
    dict(name="bigmac", a="ticket", b="mac", tag="FOLLOW THE SUN", nxt=None,
         hook="Sending one Big Mac to space costs about 250 Big Macs",
         post="A SpaceX rideshare to orbit costs about $7,000 a kilo. A Big Mac weighs 219 g. So launching one costs about $1,500, or about 250 Big Macs at $6.22."),
    dict(name="million", a="filings", b="today", tag="FOLLOW THE SUN", nxt=None,
         hook="SpaceX wants a million satellites. There are 16,500 today.",
         post="Starcloud has filed for 88,000 satellites, SpaceX for up to 1,000,000, all to put AI data centres in orbit. About 16,500 satellites work today, from every country."),
    dict(name="suncatcher", a="launch", b="test", tag="FOLLOW THE SUN", nxt=None,
         hook="Google is putting its AI chips into orbit",
         post="Project Suncatcher: a satellite with four Google TPUs, set to launch on a Falcon 9 on 1 October 2026. The test is simple: do they survive up there?"),
    dict(name="shakespeare", a="fridge", b="why", tag="FOLLOW THE SUN", nxt=None,
         hook="A satellite trained an AI model in space. On Shakespeare.",
         post="December 2025: Starcloud-1, a satellite about the size of a small fridge, trained an AI model in orbit on one Nvidia H100."),
    dict(name="japan", a="twh", b="tmi", tag="FOLLOW THE SUN", nxt=None,
         hook="By 2030, AI's data centres could use as much power as Japan",
         post="Data centres used about 1.5% of the world's electricity in 2024. By 2030 the IEA expects about 945 TWh, roughly Japan's whole consumption. Microsoft is restarting a reactor at Three Mile Island."),
    dict(name="sunlight", a="imagine", b="question", tag="FOLLOW THE SUN · A WHAT-IF", nxt=None,
         hook="What if the biggest computer on Earth wasn't on Earth?",
         post="Imagine 2040: a ring of satellites in permanent daylight, in no country. Not a forecast, a what-if. Under the 1967 treaty no one owns space, but every country answers for what it launches."),
]
# the score (Low Orbit, for scale and awe): sections from these lines, bar lines landing on the two anchors
MUSIC = [(0.0, "intro"), ("fridge", "a"), ("why", "break"), ("mill", "a"), ("look", "b"), ("filings", "a"), ("ticket", "b"),
         ("every", "break"), ("ring", "b"), ("question", "break"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP05  ·  FOLLOW THE SUN", music=MUSIC, anchors=("look", "ticket"), clips=CLIPS, tags=TAGS,
                     bed="house:key=-2", deafen=("why", "imagine"))
