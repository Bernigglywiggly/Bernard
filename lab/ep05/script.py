"""EP05 · FOLLOW THE SUN (AI data centres in orbit), v1 (28 Sep 2026), from the backlog's "A Ring of Thinking Around
the Earth". The Curve's format (lab/inspo/pollar_playbook.md): a concrete hook, the hidden mechanism, numbers made
physical with analogies (Big Macs for money), what's reported vs known said plainly, one labelled what-if, a
mirrored close. George (ElevenLabs), fast; no jokes in the lines. Bed: Low Orbit (scale, awe: space compute).

The hidden mechanism: industry has always gone to its power (mills to rivers, data centres to reactors), and the
AI build-out now wants more electricity than grids can give it, so the next place with endless power is orbit,
where a panel in the right orbit barely sees night. What's known: the first chips are going up and the filings are
in. What isn't: whether it ever pays (Google's own break-even needs launch ~35x cheaper), heat, repairs.

Fields as in lab/ep03s/script.py: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · GROUND: the cold open
    dict(floor=0, id="launch", card=("1 OCT 2026", "PROJECT SUNCATCHER · FOUR GOOGLE AI CHIPS"),
         text="Google has built a satellite to carry four of its AI chips into orbit. Launch date: 1 October.",
         say="Google has built a satellite to carry four of its AI chips into orbit. Launch date: the first of October."),
    dict(floor=0, id="test", text="The test is simple. Do they survive up there?"),
    dict(floor=0, id="fridge", card=("DEC 2025", "STARCLOUD-1 · ONE NVIDIA H100 IN ORBIT"),
         text="Last December, a satellite the size of a small fridge trained an AI model in orbit. On Shakespeare."),
    dict(floor=0, id="why", air=1, cut=True, text="So why is the AI industry trying to leave the planet?"),
    # 1 · MECHANISM: industry goes to its power
    dict(floor=1, id="mill", card=("1771", "CROMFORD MILL · ENGLAND"),
         text="In 1771, Richard Arkwright built a cotton mill at Cromford, in England. He built it there for one thing: the water that turned its wheel.",
         say="In seventeen seventy-one, Richard Arkwright built a cotton mill at Cromford, in England. He built it there for one thing: the water that turned its wheel."),
    dict(floor=1, id="follow", cut=True, text="Mills followed rivers. Computers follow electricity."),
    dict(floor=1, id="twh", card=("1.5%", "OF ALL THE WORLD'S ELECTRICITY · DATA CENTRES, 2024 · IEA"),
         text="In 2024, the world's data centres used about one and a half percent of all the electricity on Earth.",
         say="In twenty twenty-four, the world's data centres used about one and a half percent of all the electricity on Earth."),
    dict(floor=1, id="japan", card=("945 TWh", "BY 2030 · ABOUT ALL OF JAPAN · IEA"),
         text="By 2030, that's expected to double, to about as much as Japan uses in a year.",
         say="By twenty thirty, that's expected to double, to about as much as Japan uses in a year."),
    dict(floor=1, id="tmi", text="Microsoft has signed a deal to restart a nuclear reactor at Three Mile Island, to power its data centres."),
    dict(floor=1, id="look", cut=True, text="Now look up. In the right orbit, the sun almost never sets."),
    dict(floor=1, id="eight", card=("UP TO 8×", "THE SOLAR ENERGY OF THE SAME PANEL ON THE GROUND · GOOGLE"),
         text="Up there, a solar panel can collect up to eight times more energy than the same panel on the ground."),
    # 2 · NOW: the filings, the ticket
    dict(floor=2, id="filings", air=1, text="And the filings are already in."),
    dict(floor=2, id="starcloud", card=("88,000", "SATELLITES · STARCLOUD'S FCC FILING"),
         text="Starcloud has asked to launch 88,000 satellites.", say="Starcloud has asked to launch eighty-eight thousand satellites."),
    dict(floor=2, id="spacex", card=("1,000,000", "SATELLITES · SPACEX'S FCC FILING, JAN 2026"),
         text="SpaceX has asked for up to a million."),
    dict(floor=2, id="today", card=("~16,500", "WORKING SATELLITES TODAY · EVERY COUNTRY"),
         text="Today, about 16,500 satellites are working. All of them, from every country.",
         say="Today, about sixteen and a half thousand satellites are working. All of them, from every country."),
    dict(floor=2, id="china", card=("12 OF 2,800", "CHINA'S COMPUTING CONSTELLATION · MAY 2025"),
         text="In May 2025, China launched the first 12 of a planned 2,800 computing satellites.",
         say="In May twenty twenty-five, China launched the first twelve of a planned two thousand eight hundred computing satellites."),
    dict(floor=2, id="ticket", cut=True, card=("$7,000", "PER KILO TO ORBIT · SPACEX RIDESHARE, 2026"),
         text="The catch is the ticket. A SpaceX rideshare to orbit costs about $7,000 a kilo.",
         say="The catch is the ticket. A SpaceX rideshare to orbit costs about seven thousand dollars a kilo."),
    dict(floor=2, id="mac", card=("≈ 250 BIG MACS", "TO LAUNCH ONE BIG MAC (219 G)"),
         text="Sending one Big Mac to space: about $1,500. About 250 Big Macs.",
         say="Sending one Big Mac to space: about fifteen hundred dollars. About two hundred and fifty Big Macs."),
    dict(floor=2, id="breakeven", card=("< $200", "A KILO: WHERE GOOGLE SAYS ORBIT STARTS TO COMPETE · MID-2030s"),
         text="Google's own maths says orbit starts to compete below $200 a kilo. About 35 times cheaper.",
         say="Google's own maths says orbit starts to compete below two hundred dollars a kilo. About thirty-five times cheaper."),
    dict(floor=2, id="hard", text="And up there, there's no air to carry the heat away. And no one to fix a broken chip."),
    # 3 · IDEA: every age builds next to its power
    dict(floor=3, id="every", air=2, cut=True, text="Every age builds its machines next to its power."),
    dict(floor=3, id="list", text="The river. The coal field. The reactor."),
    dict(floor=3, id="sun", text="Now, maybe, the sun."),
    # 4 · IMAGINE
    dict(floor=4, id="imagine", air=3, cut=True, text="So imagine it's 2040, and the biggest computer in the world isn't in any country.",
         say="So imagine it's twenty forty, and the biggest computer in the world isn't in any country."),
    dict(floor=4, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=4, id="ring", text="A ring of satellites around the Earth, thinking in permanent daylight."),
    dict(floor=4, id="laws", text="Whose rules does it follow? Under a treaty from 1967, no one can own space. But every country answers for what it launches.",
         say="Whose rules does it follow? Under a treaty from nineteen sixty-seven, no one can own space. But every country answers for what it launches."),
    dict(floor=4, id="question", air=1, text="So the question isn't who owns the sunlight. It's who owns what catches it."),
    # 5 · SURFACE: a mirrored close
    dict(floor=5, id="then", air=2, cut=True, text="In 1771, the mill went to the river.", say="In seventeen seventy-one, the mill went to the river."),
    dict(floor=5, id="now2", cut=True, text="In 2026, the computer is going to the sun.", say="In twenty twenty-six, the computer is going to the sun."),
]

FLOORS = ["GROUND", "MECHANISM", "NOW", "IDEA", "IMAGINE", "SURFACE"]

SOURCES = [
    "Project Suncatcher: Google's prototype with Planet, four Trillium TPUs, Falcon 9 Transporter-18, set for 1 Oct 2026 "
    "(SiliconANGLE, 24 Sep 2026; DCD); up to 8x the solar energy in a dawn-dusk orbit; launch below $200/kg by the "
    "mid-2030s makes orbit roughly comparable per kW-year (Google Research, Suncatcher paper, Nov 2025)",
    "Starcloud-1: first Nvidia H100 in orbit (Nov 2025), trained NanoGPT on Shakespeare (Dec 2025) (CNBC, 10 Dec 2025); "
    "FCC filing for 88,000 satellites (Quartz)",
    "Cromford Mill, Richard Arkwright, 1771, water-powered (Derwent Valley Mills)",
    "Data centres: ~415 TWh in 2024, ~1.5% of world electricity; ~945 TWh by 2030, about Japan's consumption today "
    "(IEA, Energy and AI, 2025)",
    "Microsoft-Constellation deal to restart Three Mile Island Unit 1 (Crane Clean Energy Center), Sep 2024",
    "SpaceX FCC application for up to 1,000,000 orbital data-centre satellites, 30 Jan 2026 (SpaceNews; DCD)",
    "~16,500 active satellites, Sep 2026 (CelesTrak-based counts)",
    "China's Three-Body Computing Constellation: first 12 of a planned 2,800, May 2025 (SpaceNews)",
    "SpaceX rideshare to SSO: $350,000 for 50 kg, ~$7,000/kg (2026 pricing); Big Mac 219 g (McDonald's US), $6.22 "
    "(The Economist, July 2026): 0.219 kg x $7,000 = $1,533 = ~246 Big Macs",
    "Outer Space Treaty, 1967: Art. II (no national appropriation), Art. VI (states answer for their national activities, "
    "including companies')",
    "The 2040 section is a labelled what-if, not a forecast",
]
