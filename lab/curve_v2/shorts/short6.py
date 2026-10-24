"""Curve Short 6 (for Mon 26 Oct): "How Does a Car Do a Kickflip? (Tesla Roadster)".

Built on the 24 Oct analytics lesson (CRAFT Learned): open on the single most impossible-looking frame with a question
about it. Answer in line 1, "you" and the search term in line 1, <=35 s, ends on our verdict, loops to frame 0.
Facts: TESLA_ROADSTER_FACTS.md §4 (10 nozzles = 4 rear + 4 corner pointing down + 2 front; valves from Optimus,
"micro adjustments within a fraction of a second"), §1 (the kickflip over five Teslas; 27 ft high according to Tesla,
via NBC). Line 3 is the physics of a roll (unequal push on the two sides), not a Tesla claim.
"""
TITLE = "How Does a Car Do a Kickflip? (Tesla Roadster)"
LINES = [
    dict(id="k1", facts="§1, §4", text="You're watching a Tesla Roadster do a kickflip over a row of trucks, turned over by jets of compressed gas."),
    dict(id="k2", facts="§4 S1 S11", text="Ten nozzles sit around the car, and the four at its corners point down."),
    dict(id="k3", facts="physics", text="Push one side up harder than the other, and the car starts to roll, like a skateboard flicked at one edge."),
    dict(id="k4", facts="§4 S1 P10", text="Valves borrowed from Tesla's Optimus robot trim every jet within a fraction of a second, so it lands flat."),
    dict(id="k5", facts="§1 S8 S10", text="Tesla says the car flew about twenty-seven feet high, over five of its own vehicles."),
    dict(id="k6", facts="verdict", text="So it really is rocket science, spent on a skateboard trick."),
]
