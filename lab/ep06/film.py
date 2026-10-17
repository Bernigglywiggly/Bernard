"""EP06 · WHO'S HUMAN HERE?: the film, on the shared engine (lab/engine). python3 film.py [voice|lines|still|render|
sound|master|preview|shorts|all] (see engine/__init__.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import engine.film  # noqa: E402

TAGS = "#ai #turingtest #chatgpt #bots #deepfake #internet #tech #psychology #thecurve"
CLIPS = [
    dict(name="part1", a="setup", b="how", tag="WHO'S HUMAN HERE? · PART 1 OF 3", nxt="PART 2",
         hook="284 people had to pick the human. They picked the AI.",
         post="Two chats at once, five minutes, one person and one AI. People picked the AI as the human 73% of the time, more often than the real person. Part 1 of 3."),
    dict(name="part2", a="turing", b="gut", tag="WHO'S HUMAN HERE? · PART 2 OF 3", nxt="PART 3",
         hook="How the AI passed the Turing test",
         post="Turing's 1950 bar: fool people 30% of the time by 2000. In 2025 an AI hit 73%, and the trick wasn't knowing more. Part 2 of 3."),
    dict(name="part3", a="bots", b="now2", tag="WHO'S HUMAN HERE? · PART 3 OF 3", nxt=None,
         hook="Can you prove you're human?",
         post="53% of web traffic in 2025 was automated. An AI agent clicked \"verify you are human\". The FBI says: agree a secret word with your family. Part 3 of 3."),
    dict(name="picked", a="setup", b="more", tag="WHO'S HUMAN HERE?", nxt=None,
         hook="They picked the AI as the human 73% of the time",
         post="A 2025 UC San Diego study: 284 people chatted with a person and an AI at the same time for five minutes. GPT-4.5 with a persona was picked as the human 73% of the time."),
    dict(name="persona", a="persona", b="gut", tag="WHO'S HUMAN HERE?", nxt=None,
         hook="The trick that made an AI pass as human",
         post="Without a persona the AI was picked as human 36% of the time. Told to act like an introverted young person into internet culture: 73%."),
    dict(name="captcha", a="captcha", b="note", tag="WHO'S HUMAN HERE?", nxt=None,
         hook="An AI clicked \"I'm not a robot\"",
         post="July 2025: an AI agent clicked Cloudflare's \"Verify you are human\" box. Its own note: \"This step is necessary to prove I'm not a bot.\""),
    dict(name="secretword", a="fbi", b="claim", tag="WHO'S HUMAN HERE?", nxt=None,
         hook="The FBI's advice for AI voice scams is one word",
         post="Voices can be copied now. The FBI's advice (Dec 2024) is low-tech: agree a secret word or phrase with your family."),
    dict(name="bots", a="bots", b="hundred", tag="WHO'S HUMAN HERE?", nxt=None,
         hook="Most of the internet isn't people any more",
         post="In 2025, 53% of all web traffic was automated (Imperva). Out of every 100 visits to a website, 53 weren't people."),
]
MUSIC = [(0.0, "intro"), ("job", "a"), ("more", "break"), ("turing", "a"), ("bots", "b"), ("flip", "break"), ("imagine", "break"),
         ("proof", "a"), ("then", "b"), ("end", "out")]

if __name__ == "__main__":
    engine.film.main(__file__, title="EP06  ·  WHO'S HUMAN HERE?", music=MUSIC, anchors=("turing", "bots"), clips=CLIPS, tags=TAGS,
                     bed="garage:key=-4", deafen=("more", "imagine"))
