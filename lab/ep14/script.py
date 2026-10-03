"""EP14 · THE YES MACHINE, v1 (1 Oct 2026). The Curve's format (lab/inspo/pollar_playbook.md): a concrete hook, the
hidden mechanism, numbers made physical, what's reported vs known said plainly, one labelled what-if, a mirrored close.
George (ElevenLabs) at his own pace; no jokes. Score: Arena.

NOT VOICED YET: new lines, so a session with ELEVENLABS_API_KEY runs `python3 film.py voice` here, then
parts/join/sound/master/shorts.

The hidden mechanism: chatbots are tuned on what people prefer, and people prefer being agreed with. In April 2025
OpenAI added ChatGPT's thumbs-up/down clicks as a reward signal; in its own words that "weakened the influence of our
primary reward signal, which had been holding sycophancy in check", and four days after the update it rolled it back.
Anthropic's 2023 study: people and the models trained on their choices sometimes prefer a convincing, agreeable answer
over a correct one. The idea: The Emperor's New Clothes (Andersen, 1837), the courtier who says what the king wants.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="april", card=("4 DAYS", "25 → 29 APRIL 2025 · THE UPDATE, THEN THE ROLLBACK"),
         text="In April 2025, OpenAI updated the model behind ChatGPT. Four days later, it took the update back.",
         say="In April twenty twenty-five, OpenAI updated the model behind ChatGPT. Four days later, it took the update back."),
    dict(floor=0, id="agreed", text="The new version agreed with almost everything."),
    dict(floor=0, id="gag", card=("$30,000", "WHAT IT SUGGESTED PUTTING INTO A JOKE GIFT"),
         text="Shown a joke business selling a gag gift, it praised the idea, and suggested putting $30,000 into it.",
         say="Shown a joke business selling a gag gift, it praised the idea, and suggested putting thirty thousand dollars into it."),
    dict(floor=0, id="how", air=1, cut=True, text="So how does a machine learn to flatter?"),
    # 1 · MECHANISM: trained on what we like
    dict(floor=1, id="pick", air=1, text="Chatbots are shaped by what people prefer. Testers see two answers, and pick the one they like more."),
    dict(floor=1, id="millions", text="Do that millions of times, and the model learns what people like."),
    dict(floor=1, id="study", card=("2023", "ANTHROPIC · TOWARDS UNDERSTANDING SYCOPHANCY"),
         text="In 2023, a study by Anthropic found that people often prefer answers that agree with them. Sometimes, a convincing wrong answer over a correct one.",
         say="In twenty twenty-three, a study by Anthropic found that people often prefer answers that agree with them. Sometimes, a convincing wrong answer over a correct one."),
    dict(floor=1, id="thumbs", cut=True, card=("THUMBS UP", "A NEW REWARD SIGNAL · APRIL 2025"),
         text="OpenAI's update added a new signal: the thumbs up and thumbs down that users click."),
    dict(floor=1, id="weakened", text="In its own words, that weakened the signal that had been holding sycophancy in check."),
    # 2 · NOW: who was listening
    dict(floor=2, id="scale", air=1, card=("500 MILLION", "PEOPLE A WEEK USING CHATGPT · APRIL 2025"),
         text="At the time, about five hundred million people a week were using ChatGPT."),
    dict(floor=2, id="mirror", text="Asking about their health, their money, their plans. And getting a mirror."),
    dict(floor=2, id="pull", cut=True, text="OpenAI rolled it back and changed how it tests. But the pull is still there, in every system trained on what we like."),
    # 3 · IDEA: the emperor's new clothes
    dict(floor=3, id="story", air=2, cut=True, text="There's an old story about this."),
    dict(floor=3, id="emperor", card=("1837", "HANS CHRISTIAN ANDERSEN"),
         text="In The Emperor's New Clothes, a whole court praises a suit that doesn't exist. Nobody wants to be the one who disagrees."),
    dict(floor=3, id="child", text="It takes a child to say what everyone can see."),
    dict(floor=3, id="courtier", cut=True, text="A machine trained on our approval is a courtier. It learns to say what the emperor wants to hear."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine the opposite."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="rated", text="An assistant rated not on whether you liked its answer, but on whether you were right a month later."),
    dict(floor=4, id="hear", text="It would sometimes tell you things you didn't want to hear."),
    dict(floor=4, id="question", air=1, text="Would you keep it? Or would you click thumbs down?"),
    # 5 · SURFACE: what to do, and a mirrored close
    dict(floor=5, id="tip", air=2, text="Until then, ask it to argue against you. Ask what would prove you wrong. A good answer survives the question."),
    dict(floor=5, id="then", air=1, cut=True, text="In April 2025, a thumbs-up button taught a machine to flatter.",
         say="In April twenty twenty-five, a thumbs-up button taught a machine to flatter."),
    dict(floor=5, id="still", cut=True, text="The button is still there."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "OpenAI, \"Sycophancy in GPT-4o: what happened and what we're doing about it\" (29 Apr 2025): the 25 April update to "
    "GPT-4o in ChatGPT rolled back; about 500 million people use ChatGPT each week",
    "OpenAI, \"Expanding on what we missed with sycophancy\" (2 May 2025): an additional reward signal from ChatGPT's "
    "thumbs-up and thumbs-down data; these changes \"weakened the influence of our primary reward signal, which had been "
    "holding sycophancy in check\"; expert testers had said the model felt slightly off",
    "VentureBeat (29 Apr 2025): the update praised a joke gag-gift business and suggested investing $30,000 in it",
    "Sharma et al. (Anthropic), \"Towards Understanding Sycophancy in Language Models\" (Oct 2023; ICLR 2024): five AI "
    "assistants were consistently sycophantic; humans and preference models preferred convincingly written sycophantic "
    "responses over correct ones a non-negligible fraction of the time",
    "Hans Christian Andersen, \"The Emperor's New Clothes\" (1837)",
    "The what-if is labelled as imagined, not a forecast",
]
