"""EP06 · WHO'S HUMAN HERE? v1 (28 Sep 2026), from the backlog. The Curve's format (lab/inspo/pollar_playbook.md): a
concrete hook, the hidden mechanism, numbers made physical, what's reported vs known said plainly, one labelled
what-if, a mirrored close. George (ElevenLabs), fast; no jokes in the lines. Bed: Chrome & Marl (the plan's pick).

The hidden mechanism: the AI that passed the Turing test in 2025 didn't win by knowing more; with a persona prompt
("a young person who is relatively introverted and interested in internet culture") its score doubled, because people
judge by small talk and gut feel. Meanwhile most web traffic is already automated and an agent clicks "verify you are
human". So the test has flipped: the question is whether a person can prove they're a person.

Fields as in lab/ep03s/script.py: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="setup", card=("5 MINUTES", "TWO CHATS AT ONCE · ONE PERSON, ONE AI"),
         text="In 2025, 284 people sat down to chat with two strangers at once, for five minutes. One was a person. One was an AI.",
         say="In twenty twenty-five, two hundred and eighty-four people sat down to chat with two strangers at once, for five minutes. One was a person. One was an AI."),
    dict(floor=0, id="job", text="Their job: pick the human."),
    dict(floor=0, id="result", card=("73%", "PICKED THE AI AS THE HUMAN · GPT-4.5"),
         text="They picked the AI 73% of the time.", say="They picked the AI seventy-three percent of the time."),
    dict(floor=0, id="more", cut=True, text="More often than the real person."),
    dict(floor=0, id="how", air=1, text="So how would you tell?"),
    # 1 · MECHANISM: how it won
    dict(floor=1, id="turing", card=("1950", "ALAN TURING · THE IMITATION GAME"),
         text="In 1950, Alan Turing proposed a test. Chat with a machine and a person, and try to tell which is which.",
         say="In nineteen fifty, Alan Turing proposed a test. Chat with a machine and a person, and try to tell which is which."),
    dict(floor=1, id="predict", card=("30%", "TURING'S BAR FOR 2000: FOOL PEOPLE THIS OFTEN"),
         text="He predicted that by 2000, after five minutes of questions, machines would fool people at least 30% of the time.",
         say="He predicted that by the year two thousand, after five minutes of questions, machines would fool people at least thirty percent of the time."),
    dict(floor=1, id="late", text="He was 25 years early. And the machine went further.", say="He was twenty-five years early. And the machine went further."),
    dict(floor=1, id="persona", cut=True, card=("36% → 73%", "THE SAME AI, WITHOUT AND WITH A PERSONA"),
         text="The trick wasn't knowing more. Told to act like an introverted young person into internet culture, the AI's score doubled."),
    dict(floor=1, id="gut", text="Most people didn't test what it knew. They made small talk, and went with their gut."),
    # 2 · NOW: outnumbered
    dict(floor=2, id="bots", air=1, card=("53%", "OF ALL WEB TRAFFIC IN 2025 WAS AUTOMATED · IMPERVA"),
         text="Online, people are already outnumbered. In 2025, 53% of all web traffic was automated.",
         say="Online, people are already outnumbered. In twenty twenty-five, fifty-three percent of all web traffic was automated."),
    dict(floor=2, id="hundred", text="Out of every hundred visits to a website, fifty-three weren't people."),
    dict(floor=2, id="captcha", card=("JULY 2025", "AN AI AGENT CLICKS \"VERIFY YOU ARE HUMAN\""),
         text="In July 2025, an AI agent was caught on screen clicking the box that says: verify you are human.",
         say="In July twenty twenty-five, an AI agent was caught on screen clicking the box that says: verify you are human."),
    dict(floor=2, id="note", text="Its own note read: \"This step is necessary to prove I'm not a bot.\"",
         say="Its own note read: this step is necessary to prove I'm not a bot."),
    dict(floor=2, id="fbi", card=("DEC 2024", "THE FBI: AGREE A SECRET WORD WITH YOUR FAMILY"),
         text="And now that voices can be copied, the FBI's advice is low-tech: agree a secret word with your family."),
    # 3 · IDEA: the test flips
    dict(floor=3, id="flip", air=2, cut=True, text="Turing asked whether a machine could pass as a person."),
    dict(floor=3, id="other", text="The harder question now runs the other way: can a person prove they're a person?"),
    dict(floor=3, id="claim", text="Being human online used to be the default. Now it's a claim."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine it's 2030, and any voice on a phone call could be synthetic.",
         say="So imagine it's twenty thirty, and any voice on a phone call could be synthetic."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="proof", text="You'd need ways to prove you're you. A secret word. A second channel. Someone you can meet in person."),
    dict(floor=4, id="question", air=1, text="The question stops being what machines can do. It becomes who you can trust."),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="In 1950, the test was for the machine.", say="In nineteen fifty, the test was for the machine."),
    dict(floor=5, id="now2", cut=True, text="In 2026, it's for us.", say="In twenty twenty-six, it's for us."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "Jones & Bergen, \"Large Language Models Pass the Turing Test\" (UC San Diego, arXiv 2503.23674, Mar 2025): 284 "
    "participants, 5-minute three-party tests; GPT-4.5 with a persona prompt judged human 73% of the time, 36% without; "
    "LLaMa-3.1-405B 56%; ELIZA 23%; GPT-4o 21%; small talk in 61% of games",
    "A. M. Turing, \"Computing Machinery and Intelligence\", Mind, 1950: in about fifty years \"an average interrogator "
    "will not have more than 70 per cent chance of making the right identification after five minutes of questioning\"",
    "Imperva (Thales) Bad Bot Report 2026: automated traffic over 53% of all web traffic in 2025 (51% in 2024)",
    "ChatGPT Agent clicking Cloudflare's \"Verify you are human\" checkbox, July 2025, narrating \"This step is necessary "
    "to prove I'm not a bot\" (Ars Technica; Tom's Hardware)",
    "FBI IC3 public service announcement PSA241203, 3 Dec 2024: create a secret word or phrase with your family",
    "The 2030 section is a labelled what-if, not a forecast",
]
