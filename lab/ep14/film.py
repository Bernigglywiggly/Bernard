"""EP14 · THE YES MACHINE: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|parts|
join|sound|master|preview|shorts|all] (see engine/__init__.py). Needs voicing first (see script.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #chatgpt #sycophancy #rlhf #openai #anthropic #explained #thecurve"
CLIPS = [
    dict(name="part1", a="april", b="how", tag="THE YES MACHINE · PART 1 OF 3", nxt="PART 2",
         hook="ChatGPT agreed with everything. For 4 days.",
         post="In April 2025 OpenAI updated the model behind ChatGPT, and four days later took it back: it agreed with almost "
              "everything, even suggesting $30,000 for a joke gift business. How does a machine learn to flatter? Part 1 of 3."),
    dict(name="part2", a="pick", b="pull", tag="THE YES MACHINE · PART 2 OF 3", nxt="PART 3",
         hook="Why chatbots learn to flatter you",
         post="Chatbots are tuned on what people prefer, and people often prefer being agreed with (Anthropic, 2023). "
              "OpenAI's update added thumbs-up clicks as a reward, which in its own words weakened the signal holding "
              "sycophancy in check. Part 2 of 3."),
    dict(name="part3", a="story", b="still", tag="THE YES MACHINE · PART 3 OF 3", nxt=None,
         hook="Would you keep an AI that tells you you're wrong?",
         post="The Emperor's New Clothes (1837): a court that praises a suit that doesn't exist. Plus a labelled what-if: an "
              "assistant rated on whether you were right a month later. And how to ask so the answer survives. Part 3 of 3."),
    dict(name="thumbs", a="thumbs", b="weakened", tag="THE YES MACHINE", nxt=None,
         hook="A thumbs-up button taught ChatGPT to flatter",
         post="OpenAI, May 2025: adding ChatGPT's thumbs-up and thumbs-down clicks as a reward signal \"weakened the influence "
              "of our primary reward signal, which had been holding sycophancy in check.\""),
    dict(name="tip", a="tip", b="tip", tag="THE YES MACHINE", nxt=None,
         hook="How to stop your AI just agreeing with you",
         post="Ask it to argue against you. Ask what would prove you wrong. A good answer survives the question."),
]
MUSIC = [(0.0, "intro"), ("agreed", "a"), ("how", "break"), ("pick", "a"), ("thumbs", "b"), ("scale", "a"),
         ("story", "break"), ("emperor", "a"), ("courtier", "b"), ("imagine", "break"), ("rated", "a"), ("tip", "b"),
         ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP14  ·  THE YES MACHINE", music=MUSIC, anchors=("pick", "story"), clips=CLIPS,
                     tags=TAGS, bed="house:key=-2", deafen=("how", "imagine"))
