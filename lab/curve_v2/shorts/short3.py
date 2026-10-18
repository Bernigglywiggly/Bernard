"""Roadster Short 3 (for Tue 20 Oct): "How Long Can the Tesla Roadster Fly?".

Answer in line 1 (seconds, then hours), "you" and the search term in line 1 (CRAFT §9.1), <=35 s, ends on the
second-best fact (Musk vs his engineer), loops into the opening picture. Facts: TESLA_ROADSTER_FACTS.md P1 (12:11-12:20,
12:30), S1 (Moravy to Top Gear: one launch per fill, 2-6 h refill from a nitrogen rig), §5 [EST] (about 2 s at 80 kN).
"""
TITLE = "How Long Can the Tesla Roadster Fly?"
LINES = [
    dict(id="r1", facts="§5 [EST] S1", text="You're looking at a Tesla Roadster that can fly for seconds, then has to wait hours for more gas."),
    dict(id="r2", facts="P1 (12:11-12:20) S1", text="Its two carbon-wrapped tanks hold about a quarter of a tonne of compressed gas."),
    dict(id="r3", facts="§5 [EST]", text="By our maths, the rear nozzles at full power would empty them in about two seconds."),
    dict(id="r4", facts="S1", text="Tesla told Top Gear the Thrust version gets a single launch per fill."),
    dict(id="r5", facts="S1", text="And its head of vehicle engineering said a refill from a high-pressure nitrogen rig takes hours."),
    dict(id="r6", facts="P1 (12:30) S1", text="Yet on stage, Musk said the car can refill its own tank, a long way from what his engineer told Top Gear."),
]
