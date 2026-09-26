"""THE CURVE: a 90-second pilot in the renegade register (v7 lab).

Structure borrowed (not content) from the research: a flat-premise cold open, "you" by line two,
micro-antitheses, an escalation ladder, one aphorism, a borrowed-domain chiasmus, a deadpan callback
at the close. Every number is sourced on screen (see SOURCES). Lines start on the music's half-bar
grid (170 BPM), with a bar of air before each reveal.

Fields: scene, text, air (extra half-bars of silence before the line), card (on-screen source/number).
"""

LINES = [
    # S1: the chip (cold open)
    dict(scene="chip", text="Hard being a chip in twenty twenty-six."),
    dict(scene="chip", text="You wake up. You predict the next word."),
    dict(scene="chip", text="Nine hundred million people a week ask you for help.", card=("900M+", "WEEKLY USERS · OPENAI, 2026")),
    dict(scene="chip", text="And roughly every four months, your replacement can work twice as long on its own.",
         card=("×2 / 4.3 MO", "TASK LENGTH AI CAN FINISH · METR, JAN 2026")),
    # S2: the curve
    dict(scene="curve", text="Here's the part nobody explains properly.", air=2),
    dict(scene="curve", text="In nineteen fifty-six, ten scientists asked for one summer to teach machines to think.",
         card=("1956", "DARTMOUTH · 'A 2-MONTH, 10-MAN STUDY'")),
    dict(scene="curve", text="That summer lasted seventy years."),
    dict(scene="curve", text="Then the gaps started closing. Decades. Years. Months."),
    dict(scene="curve", text="On September the twenty-second, two labs shipped new models, about ninety minutes apart.",
         card=("22 SEP 2026", "TWO FRONTIER RELEASES · ~90 MIN APART")),
    dict(scene="curve", text="That's not a trend line. That's a launch ramp."),
    dict(scene="curve", text="The same level of AI got a thousand times cheaper in three years.",
         card=("1,000×", "CHEAPER · SAME CAPABILITY · 2021→2024 · a16z")),
    # S3: the drop
    dict(scene="vortex", text="So what do you do... when the floor starts moving?", air=1),
    # S4: the gold rush
    dict(scene="gold", text="Eighteen forty-eight. California. Gold.", air=7),
    dict(scene="gold", text="Everyone ran for the rivers."),
    dict(scene="gold", text="One guy, Sam Brannan, ran for the shovels."),
    dict(scene="gold", text="Thirty-six thousand dollars in nine weeks. Without swinging a pick.",
         card=("$36,000", "IN NINE WEEKS · SELLING SUPPLIES, 1848")),
    dict(scene="gold", text="They saw a gold rush. He saw a supply chain.",
         card=("MINERS: 'SMALL OR EVEN ZERO'", "EVERYONE ELSE: 'POSITIVE AND LARGE' · CLAY & JONES, 2008")),
    # S5: the shovels now
    dict(scene="shop", text="Right now, everyone's digging for the same gold. Apps. Agents. Startups.", air=1),
    dict(scene="shop", text="Meanwhile, the takeaway round the corner is still handing up to thirty percent of every order to an app.",
         card=("UP TO 30%", "DELIVERY-APP COMMISSION PER ORDER")),
    dict(scene="shop", text="The shovel isn't the model. The shovel is knowing what it can do... and walking in the door."),
    # S6: close
    dict(scene="close", text="So here's your homework, from one chip to another.", air=1),
    dict(scene="close", text="Find one thing the curve just made cheap. Sell it to someone who hasn't noticed yet."),
    dict(scene="close", text="See you on the curve.", air=1),
]

SOURCES = [
    "900M+ weekly users: OpenAI (2026)",
    "Task-length doubling ~130.8 days: METR Time Horizon 1.1, 29 Jan 2026 — metr.org/blog/2026-1-29-time-horizon-1-1",
    "Dartmouth proposal, 31 Aug 1955: 'a 2-month, 10-man study of artificial intelligence… summer of 1956'",
    "22 Sep 2026 releases ~90 minutes apart (single source: The Neuron)",
    "1,000× cheaper, GPT-3-level output $60 → $0.06 per million tokens, Nov 2021 → late 2024: a16z 'LLMflation'",
    "Sam Brannan, $36,000 in nine weeks selling supplies: foundsf.org / Wikipedia",
    "Clay & Jones (2008), gains 'small or even zero for miners… positive and large for nonminers'",
    "Delivery-app commission ranges (Uber Eats 15–30%, Deliveroo 14–30%, Just Eat 14–22%): 2026 comparisons",
]
