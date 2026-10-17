"""EP04 · THE MAN IN THE MACHINE (robots), v1 (28 Sep 2026). The Curve's format (lab/inspo/pollar_playbook.md): a
concrete hook, the hidden mechanism, numbers made physical with analogies (Big Macs for money), what's reported vs
known said plainly, one labelled what-if, a mirrored close. George (ElevenLabs), fast; no jokes in the lines.

The hidden mechanism: the robots in the headlines (the Tesla Bot reveal, China's robot boxing, the San Francisco
cage fight, the rifle-carrying robot dog) all had a person deciding the moves. The machines already do the hard
physical part (staying upright); the deciding is the part still ours, and that's the line to watch.

Fields as in lab/ep03s/script.py: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="cage", card=("18 SEP 2026", "SAN FRANCISCO · HUMAN VS HUMANOID"),
         text="18 September 2026. San Francisco. A man steps into a cage to fight a six-foot robot.",
         say="The eighteenth of September, twenty twenty-six. San Francisco. A man steps into a cage to fight a six-foot robot."),
    dict(floor=0, id="lost", text="About 80 kilos of metal. It knocks him into the cage wall, again and again. He hurts his hand, and the fight is stopped."),
    dict(floor=0, id="pilot", cut=True, text="The clips leave one thing out. The robot wasn't deciding anything. A person backstage in a VR headset was."),
    dict(floor=0, id="suit", text="Five years earlier, the most famous robot in the world was a person too."),
    dict(floor=0, id="close", air=1, text="So how close are the machines, really?"),
    # 1 · MECHANISM: who does what
    dict(floor=1, id="tesla", card=("19 AUG 2021", "TESLA AI DAY · THE TESLA BOT"),
         text="August 2021. Tesla announces a humanoid robot. On stage, it's a person in a white bodysuit, dancing.",
         say="August twenty twenty-one. Tesla announces a humanoid robot. On stage, it's a person in a white bodysuit, dancing."),
    dict(floor=1, id="boxing", card=("132 CM · 35 KG", "UNITREE G1 · CHINA'S FIRST ROBOT BOXING, MAY 2025"),
         text="May 2025. Chinese state TV shows the first humanoid robot boxing tournament. Four robots, each steered by a human trainer.",
         say="May twenty twenty-five. Chinese state TV shows the first humanoid robot boxing tournament. Four robots, each steered by a human trainer."),
    dict(floor=1, id="split", cut=True, text="Here's the split. Staying upright, taking a hit, getting back up: the machine does that on its own."),
    dict(floor=1, id="decide", text="Deciding when to punch, and who: that was still a person."),
    dict(floor=1, id="price", card=("$13,500", "UNITREE G1 · ABOUT 2,200 BIG MACS"),
         text="You can buy one of those robots today for $13,500. About 2,200 Big Macs.",
         say="You can buy one of those robots today for thirteen thousand five hundred dollars. About two thousand two hundred Big Macs."),
    # 2 · NOW: the robots that matter don't look like us
    dict(floor=2, id="dogs", air=1, card=("GOLDEN DRAGON 2024", "CHINA · CAMBODIA · A RIFLE ON A ROBOT DOG"),
         text="The robots that matter most don't look like us. In 2024, China's army showed a robot dog with a rifle on its back.",
         say="The robots that matter most don't look like us. In twenty twenty-four, China's army showed a robot dog with a rifle on its back."),
    dict(floor=2, id="remote", text="Walked, like the boxers, by a remote operator."),
    dict(floor=2, id="ukraine", card=("50,000", "GROUND ROBOTS ORDERED FOR 2026 · UKRAINE"),
         text="In April 2026, Ukraine's president ordered fifty thousand ground robots for this year.",
         say="In April twenty twenty-six, Ukraine's president ordered fifty thousand ground robots for this year."),
    dict(floor=2, id="missions", card=("~112,000", "SUPPLY AND EVACUATION RUNS BY SEPTEMBER"),
         text="By September they'd made about 112,000 supply and evacuation runs. Each one, a trip a soldier didn't have to make.",
         say="By September they'd made about a hundred and twelve thousand supply and evacuation runs. Each one, a trip a soldier didn't have to make."),
    dict(floor=2, id="cost", card=("680,000 BIG MACS", "ONE PATRIOT INTERCEPTOR · ABOUT $4.2M"),
         text="And the money has flipped. One Patriot interceptor costs about $4.2 million. About 680,000 Big Macs.",
         say="And the money has flipped. One Patriot interceptor costs about four point two million dollars. About six hundred and eighty thousand Big Macs."),
    dict(floor=2, id="drone", card=("3,000–8,000 BIG MACS", "ONE SHAHED DRONE · $20,000–$50,000 (CSIS)"),
         text="The drone it's often fired at: somewhere between 3,000 and 8,000.",
         say="The drone it's often fired at: somewhere between three thousand and eight thousand."),
    dict(floor=2, id="cheap", text="Cheap machines. Expensive answers. That's the maths of the new war."),
    # 3 · IDEA: the line that moves
    dict(floor=3, id="line", air=2, cut=True, text="Every machine in this story still had a person deciding what it did."),
    dict(floor=3, id="edge", text="But the machine's share keeps growing at the edges: balance, then walking, then finding its own way."),
    dict(floor=3, id="loop", text="The person is still in the loop. The loop just keeps getting smaller."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine it's 2030, and the pilot isn't needed.",
         say="So imagine it's twenty thirty, and the pilot isn't needed."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="who", text="Then who decides when a machine strikes? Someone who wrote the rules, months earlier, far away."),
    dict(floor=4, id="question", air=1, text="The question was never whether robots can fight. It's who is inside them when they do."),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="In 2021, the robot was a person in a suit.", say="In twenty twenty-one, the robot was a person in a suit."),
    dict(floor=5, id="now2", cut=True, text="In 2026, there's still a person inside the robot.", say="In twenty twenty-six, there's still a person inside the robot."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "Human vs humanoid, San Francisco, 18 Sep 2026: Frankie LaPenna vs EngineAI's T800 at Robot Entertainment Kombat; "
    "the robot was piloted by a person in a VR headset; the bout was stopped after a hand/wrist injury (Yahoo Tech; "
    "IBTimes UK; Gadget Review; Startup Fortune)",
    "Tesla AI Day, 19 Aug 2021: the Tesla Bot announced with a dancer in a bodysuit (Fortune; Gizmodo; The Drive)",
    "CMG World Robot Competition, Mecha Fighting Series, Hangzhou, 25 May 2025: four Unitree G1s (132 cm, 35 kg), each "
    "controlled by a human; balance learned with reinforcement training (Live Science; Global Times; Robotics 24/7)",
    "Unitree G1: launched May 2024 at $16,000, $13,500 from late 2025 (The Robot Report; store listings); "
    "Big Mac $6.22, The Economist, July 2026, so $13,500 = about 2,170 Big Macs",
    "PLA robot dog with a rifle, Golden Dragon 2024 with Cambodia, remote-operated (CNN, 28 May 2024)",
    "Ukraine: 50,000 ground robots ordered for 2026 (April); about 112,000 logistics and evacuation missions by early "
    "September 2026 (Defense News; United24 Media; The Defense Post)",
    "Patriot PAC-3 MSE about $4.2M (US Army FY2025 budget); Shahed $20,000-$50,000 (CSIS); in Big Macs at $6.22: about "
    "680,000, and 3,200-8,000",
    "The 2030 section is a labelled what-if, not a forecast",
]
