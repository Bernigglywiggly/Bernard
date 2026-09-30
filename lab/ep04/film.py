"""EP04 · THE MAN IN THE MACHINE: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|
render|sound|master|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#robots #ai #humanoid #tesla #military #ukraine #drones #tech #bigmac #thecurve"
CLIPS = [
    dict(name="part1", a="cage", b="close", tag="THE MAN IN THE MACHINE · PART 1 OF 4", nxt="PART 2",
         hook="A man fought a six-foot robot. The clips left one thing out.",
         post="San Francisco, 18 Sep 2026: a man steps into a cage with an 80 kg humanoid robot. It wasn't deciding anything. Part 1 of 4."),
    dict(name="part2", a="tesla", b="price", tag="THE MAN IN THE MACHINE · PART 2 OF 4", nxt="PART 3",
         hook="What the robot does, and what a person still decides",
         post="Tesla's 2021 robot reveal was a dancer in a bodysuit. China's first robot boxers were each steered by a human. Part 2 of 4."),
    dict(name="part3", a="dogs", b="cheap", tag="THE MAN IN THE MACHINE · PART 3 OF 4", nxt="PART 4",
         hook="The robots that matter most don't look like us",
         post="A robot dog with a rifle. 50,000 ground robots ordered by Ukraine. A $4.2M missile fired at a $20,000 drone. Part 3 of 4."),
    dict(name="part4", a="line", b="now2", tag="THE MAN IN THE MACHINE · PART 4 OF 4", nxt=None,
         hook="The person is still in the loop. The loop keeps getting smaller.",
         post="Every machine in this story still had a person deciding what it did. So what happens when the pilot isn't needed? Part 4 of 4."),
    dict(name="cagefight", a="cage", b="pilot", tag="THE MAN IN THE MACHINE", nxt=None,
         hook="Man vs six-foot robot. Who was really fighting?",
         post="18 Sep 2026, San Francisco: a man vs an 80 kg humanoid robot. The robot wasn't deciding anything. A person backstage in a VR headset was."),
    dict(name="tesla", a="suit", b="tesla", tag="THE MAN IN THE MACHINE", nxt=None,
         hook="The most famous robot in the world was a person",
         post="August 2021: Tesla announces a humanoid robot. On stage, it's a person in a white bodysuit, dancing."),
    dict(name="boxing", a="boxing", b="decide", tag="THE MAN IN THE MACHINE", nxt=None,
         hook="Robot boxing: who's actually throwing the punches?",
         post="May 2025: China's first humanoid robot boxing tournament. The machines stay upright on their own. A person decides when to punch."),
    dict(name="price", a="split", b="price", tag="THE MAN IN THE MACHINE", nxt=None,
         hook="You can buy a humanoid robot for 2,200 Big Macs",
         post="A Unitree G1 costs $13,500. At $6.22 a Big Mac, that's about 2,200 Big Macs."),
    dict(name="patriot", a="cost", b="cheap", tag="THE MAN IN THE MACHINE", nxt=None,
         hook="A $4.2 million missile vs a $20,000 drone",
         post="One Patriot interceptor: about $4.2M, or 680,000 Big Macs. The Shahed drone it's often fired at: 3,000 to 8,000. Cheap machines, expensive answers."),
    dict(name="ukraine", a="ukraine", b="missions", tag="THE MAN IN THE MACHINE", nxt=None,
         hook="Ukraine ordered 50,000 ground robots this year",
         post="By September they'd made about 112,000 supply and evacuation runs. Each one, a trip a soldier didn't have to make."),
    dict(name="loop", a="line", b="question", tag="THE MAN IN THE MACHINE · A WHAT-IF", nxt=None,
         hook="What happens when the pilot isn't needed?",
         post="Every robot in this story still had a person deciding. Imagine it's 2030 and that's gone. Not a forecast, a what-if."),
]
# the score (Mainframe): sections from these lines (a beat before each), bar lines landing on the two anchors
MUSIC = [(0.0, "intro"), ("lost", "a"), ("pilot", "b"), ("close", "break"), ("tesla", "a"), ("dogs", "b"), ("line", "break"),
         ("edge", "a"), ("imagine", "break"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP04  ·  THE MAN IN THE MACHINE", music=MUSIC, anchors=("pilot", "dogs"), clips=CLIPS, tags=TAGS,
                     bed="arena:key=2", deafen=("pilot", "imagine"))
