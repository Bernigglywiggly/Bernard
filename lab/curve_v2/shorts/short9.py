"""Curve Short 9 (for Wed 28 Oct): "Motorcycle on Water: Why It Didn't Sink".

DRAFT by account C (facts desk), Tue 27 Oct 13:00 UK: script only, not voiced, no picture yet. The Shorts lane (A, or B if
A is away) owns the build. Blocked on: (1) his footage route (facts §6: he sends ZXMOTO the ask, or a CCTV+ licence, or
<=5 s credited CGTN Europe / Xinhua shots under our commentary), (2) a voice (this account has no ElevenLabs connector).

Radar 26 Oct #3; the record was set Sun 25 Oct, so this ships ~72 h after the event. No English explainer of the physics
was found on YouTube (facts row 80b): the angle is open. Frame 0 is the bike skimming in its own spray plume mid-river,
text "WHY DOESN'T IT SINK?" (facts §7, H1). Line 1 says "you" and the search phrase "motorcycle on water" and lands in
about 3 s. The twist reviewers skip: lift grows with speed squared, so half the speed leaves a quarter of the lift (OUR
MATHS row 73). The 2009 sinking is the middle beat, not the opener (CRAFT 24 Oct: open on the impossible frame, not a
person). Verdict and loop: the skipping stone line, then the bike slowing into the water, hard cut to frame 0.
Never say it floats, never give a sinking speed, a top speed as fact, "lake", "first ever", or the 2009 river's name as
the same river (facts §8). Facts: lab/research/MOTO_WATER_FACTS.md (rows).
"""
TITLE = "Motorcycle on Water: Why It Didn't Sink"
LINES = [
    dict(id="m1", facts="73, 50, 51 (slow down and it sinks; no sinking speed given)",
         text="Slow down on this motorcycle on water, and you sink.",
         cap="Slow down / on this motorcycle on water, / and you sink.",
         shot="frame 0 = the bike mid-river in its own spray plume (owner's or credited agency shot, <=5 s), "
              "text 'WHY DOESN'T IT SINK?'"),
    dict(id="m2", facts="1, 2, 3, 6 (Guinness adjudicator on site)",
         text="On Sunday, Zhang Xue rode it forty kilometres along a river in China, a Guinness world record.",
         cap="On Sunday, Zhang Xue / rode it forty kilometres / along a river in China, / a Guinness world record.",
         shot="our map: a pin on Mayang, Hunan; the river; '40.74 KM' counting up along a back-and-forth track; "
              "'GUINNESS · CHECKED ON SITE' tag"),
    dict(id="m3", facts="21, 22, 66",
         text="Its back wheel's paddles throw water backwards, and skis underneath skim the surface like a water skier.",
         cap="Its back wheel's paddles / throw water backwards, / and skis underneath / skim the surface / "
             "like a water skier.",
         shot="our Blender side view: paddle wheel throwing a spray arrow back (THRUST →), skis planing, a lift arrow up"),
    dict(id="m4", facts="60, 62, 73 (OUR MATHS: half the speed, a quarter of the lift)",
         text="The skis' lift grows with speed squared, so half the speed leaves only a quarter of the lift.",
         cap="The skis' lift / grows with speed squared, / so half the speed / leaves only / a quarter of the lift.",
         shot="the lift arrow shrinking as a speed dial halves: 'SPEED ½ → LIFT ¼', tag OUR MATHS; the skis sink and tilt up"),
    dict(id="m5", facts="43 (V: four falls, best 20 m), 72 (OUR MATHS: about 2,000 times further)",
         text="In 2009 he tried this and sank every time, never getting further than twenty metres.",
         cap="In 2009 / he tried this / and sank every time, / never getting further / than twenty metres.",
         shot="RECONSTRUCTION (our Blender, labelled): a crude bike nosing into the water; scale bar '20 M' vs '40,740 M'"),
    dict(id="m6", facts="verdict (facts §7); 73, 74",
         text="It's a skipping stone with an engine, and like a stone, it sinks the moment it slows.",
         cap="It's a skipping stone / with an engine, / and like a stone, / it sinks / the moment it slows.",
         shot="a stone skipping (our Blender) matched-cut to the bike; the bike slows and settles; hard cut back to frame 0 "
              "(loop: last frame = frame 0)"),
]
