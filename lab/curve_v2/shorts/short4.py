"""Curve Short 4 (for Sat 24 Oct): "How Does a Robot Learn Kung Fu? (Unitree H2-X)".

Answer and twist in line 1 (critic round 1: the learned kung fu, then the demo bodyguard), "you" and the search term in line 1 (CRAFT §9.1),
<=35 s, ends on our verdict, loops into the opening picture. Facts: lab/research/UNITREE_H2X_FACTS.md (numbers by row).
The "no speed-up" claim is shown on screen as Unitree's own label, not spoken.
"""
TITLE = "How Does a Robot Learn Kung Fu? Unitree's H2-X"
LINES = [
    dict(id="u1", facts="4 (Unitree's own label), 5-6", text="Unitree says the kung fu you're watching from its H2-X is real, but its own small print tells a different story about the bodyguard."),
    dict(id="u2", facts="14", text="Robots like it start by copying a person's moves, joint by joint."),
    dict(id="u3", facts="11", text="Then virtual copies practise in a simulator, falling over until each move works."),
    dict(id="u4", facts="12", text="Unitree's own public training code runs 4,096 of them at once."),
    dict(id="u5", facts="13", text="In that code, the controller adjusts the robot fifty times a second."),
    dict(id="u6", facts="5, 6", text="But the small print says its eight-hour battery is for standing, and the knife attack is labelled a demonstration."),
    dict(id="u7", facts="verdict", text="The kicks are real; the bodyguard is still a demo."),
]
