"""Curve Short 8 (for Tue 27 Oct, by 12:00 UK): "iPhone Duo Crack: Why It Happens at the Fold".

Radar 26 Oct #1 (21/25): JerryRigEverything's durability video at 11.77M and still climbing (99k/h), search has moved
to "iphone duo crack", Apple answered on Mon 26 Oct. Opens on the visual mystery (the green line on the inner screen
after JRE's bend), per the 24 Oct CRAFT lesson; answer, "you" and the search term in line 1; <=35 s; ends on our
verdict and loops back into the crack. The twist is the physics reviewers don't show: a bent layer stretches by its
thickness over twice the bend radius, and glass cracks near 1%. We never say what broke JRE's phone, or that his line
runs along the fold (facts rows 56-57). Facts: lab/research/IPHONE_DUO_FACTS.md (rows).
"""
TITLE = "iPhone Duo Crack: Why It Happens at the Fold"
LINES = [
    dict(id="d1", facts="70, 71, 94 (OUR MATHS)",
         text="Every time you fold an iPhone Duo, its screen glass stretches almost as far as glass can before it cracks.",
         cap="Every time you fold / an iPhone Duo, / its screen glass stretches / almost as far as glass can / before it cracks.",
         shot="frame 0 = JRE ~12:05-12:15, the green line, 'WHY AT THE FOLD?'; then our bend: the outer face glows, "
              "'≈0.8% STRETCH' against 'GLASS CRACKS ≈1%' (OUR MATHS: 30 µm at a ~1.9 mm fold, row 94)"),
    dict(id="d2", facts="70, 72, 74",
         text="Bend anything and its outside stretches, more when it's thicker or bent tighter.",
         cap="Bend anything / and its outside stretches, / more when it's thicker / or bent tighter.",
         shot="one strip bending round a circle: outer edge in tension (arrows out), inner squeezed; t and r labelled"),
    dict(id="d3", facts="91 (OUR MATHS at 1.9 mm: 0.5 / 3.8 = 13%), 76",
         text="Ordinary phone glass bent like this would stretch over thirteen percent and shatter, so folding phones use glass "
              "about thirty microns thick.",
         cap="Ordinary phone glass / bent like this / would stretch over 13% / and shatter, / so folding phones use glass / "
             "about 30 microns thick.",
         shot="side by side: 0.5 mm sheet cracks at '13%+'; a 30 µm sheet bends at '0.8%'; tag OUR MATHS"),
    dict(id="d4", facts="90, 79, 23, 93",
         text="That's still near its limit, so the glass is toughened and the layers slide like book pages.",
         cap="That's still / near its limit, / so the glass is toughened / and the layers slide / like book pages.",
         shot="Apple's film A7 ~1:20-1:28 ('more than 10 ultrathin layers'), then our stack fanning like pages as it bends: "
              "glued solid 10.7% vs sliding 1.1% (illustrative, row 93)"),
    dict(id="d5", facts="34 (Apple to MacRumors, 26 Oct)",
         text="Apple says a small number of inner screens have an issue, and it's replacing them.",
         cap="Apple says / a small number of inner screens / have an issue, / and it's replacing them.",
         shot="typeset card: \"an issue impacting the inner display on a small number\" + 'APPLECARE REPLACEMENT', stamp APPLE TO MACRUMORS"),
    dict(id="d6", facts="verdict; 34b (MacRumors: cracks reported along the hinge)",
         text="So the fold is where this screen works hardest, and it's where the reported cracks are.",
         cap="So the fold / is where this screen / works hardest, / and it's where / the reported cracks are.",
         shot="our stack, the fold line glowing hottest; hard cut back to JRE's green line = frame 0 (loop)"),
]
