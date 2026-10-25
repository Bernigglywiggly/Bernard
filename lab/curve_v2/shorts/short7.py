"""Curve Short 7 (for Sun 25 Oct): "How Did This Robot Duck Learn to Get Back Up? (Microduck)".

Radar top pick of 23 Oct (Microduck 22/25: Nvidia's GTC Berlin keynote and blog, Pollen's 2.1M-view reveal). Opens on
the visual mystery (a hand shoves the real duck and it recovers), per the 24 Oct CRAFT lesson. Answer, "you" and the
search term in line 1; <=35 s; ends on our verdict and loops into the shove (v2, critic round 1: m2 from fact 14,
no colon reveal, "practised on" instead of "beaten"). The twist is the deliberately wrong
bodies (domain randomisation), which Short 4 did not cover. Facts: lab/research/MICRODUCK_FACTS.md (rows).
"""
TITLE = "How Did This Robot Duck Learn to Get Back Up? (Microduck)"
LINES = [
    dict(id="m1", facts="14, 15, 10", text="The Microduck you're watching was never shown how to get back up; it learned in a simulator.", cap="The Microduck / you're watching / was never shown / how to get back up; / it learned / in a simulator."),
    dict(id="m2", facts="14", text="Its only points came from ending up standing; it found the moves itself.", cap="Its only points came / from ending up standing; / it found the moves itself."),
    dict(id="m3", facts="12", text="Then thousands of virtual ducks practised at once, falling and trying again.", cap="Then thousands / of virtual ducks / practised at once, / falling / and trying again."),
    dict(id="m4", facts="16", text="And they cheat. Told to stand, one propped itself on its head, like a tripod.", cap="And they cheat. / Told to stand, / one propped itself / on its head, / like a tripod."),
    dict(id="m5", facts="20-24", text="The trick is giving every copy a slightly wrong body. Heavier, off balance, slippery, low on battery, shoved every few seconds.", cap="The trick is giving / every copy / a slightly wrong body. / Heavier, / off balance, / slippery, / low on battery, / shoved every few seconds."),
    dict(id="m6", facts="verdict (27)", text="So the real duck is just one more wrong body, and it's practised on thousands.", cap="So the real duck / is just / one more wrong body, / and it's practised / on thousands."),
]
