"""Curve Short 13 (Sat 31 Oct 2026, publishes 17:00 UK): "How Do Jets Land on Aircraft Carriers?"

Account A, Fri 30 Oct 2026 ~01:50 UK (Saturday's A slot; B's b-sat-short skips itself at 93% weekly usage).
Facts: lab/curve_v2/shorts/short13_facts.md (rows). Pictures: U.S. Navy video of the F-35C's first landing on the
John F. Kennedy (CVN 79), 13 Oct 2026 (public domain, 5 s or less a shot, credited, shown as a band), and our own
drawings: the 150-to-0 dial, the hook and wire cross-section, the machine below deck (water turbine + electric motor),
the full-power bolter, the verdict. First Short under the 30 Oct playbook rules (RUNBOOK §8b): frame 0 already moving
with one drawn mark and a 4-word question, our drawing on screen from frame 0, the spoken end line with "subscribe".

Frame 0: the head-on landing, the jet just down on the deck, a ring drawn on the hook and wire, kicker
"STOPPED IN / 2 SECONDS?", the dial at 150 MPH. Loop: the verdict eases back to that picture.
"""
TITLE = "How Do Jets Land on Aircraft Carriers?"
LINES = [
    dict(id="x1", facts="4 (about 130 knots = 150 mph to a stop in about two seconds); 5 (a wire)",
         text="You land on an aircraft carrier at about 150 miles an hour. A single wire stops you in two seconds.",
         cap="You land on / an aircraft carrier / at about 150 / miles an hour. / A single wire / stops you / in two seconds.",
         shot="frame 0 = the Navy's head-on landing in a band, ring on the hook and wire, kicker 'STOPPED IN / 2 SECONDS?'; "
              "below the band our dial drops 150 MPH to 0 on 'two seconds'"),
    dict(id="x2", facts="1 (13 Oct 2026, the Kennedy's first aircraft recovered, an F-35C of VX-23, first F-35C on a Ford-class carrier)",
         text="This stealth jet was the first to land on the Navy's newest carrier, on October 13th.",
         cap="This stealth jet / was the first / to land on / the Navy's newest carrier, / on October 13th.",
         shot="the Navy's side and stern landing shots in the band; stamp '13 OCT 2026', tags 'F-35C' and 'JOHN F. KENNEDY · CVN 79'"),
    dict(id="x3", facts="5 (tailhook, cross-deck wire, cable to the arresting engine below deck)",
         text="Its tail hook grabs a steel wire, which pulls a machine hidden below the deck.",
         cap="Its tail hook / grabs a steel wire, / which pulls a machine / hidden below the deck.",
         shot="our cross-section: deck line, the jet in profile, hook down, the wire across the deck; the hook catches, the wire "
              "pays out over two pulleys to a box below the deck line, tag 'BELOW DECK'"),
    dict(id="x4", facts="2 (the Kennedy uses AAG); 3 (water turbines + large induction motor, fine control, a broad range of aircraft)",
         text="On this ship, it's water turbines and a big electric motor that tune the pull for each jet.",
         cap="On this ship, / it's water turbines / and a big electric motor / that tune the pull / for each jet.",
         shot="the box opens: a cable drum turning a water turbine (water swirling) and an electric motor; a PULL gauge whose "
              "needle moves for HEAVY JET / LIGHT JET; tag 'ADVANCED ARRESTING GEAR'"),
    dict(id="x5", facts="6 (throttles to full power at touchdown; a missed wire = a bolter, the jet flies off and goes round)",
         text="And pilots land at full power, so if the hook misses, the jet just flies off again.",
         cap="And pilots land / at full power, / so if the hook misses, / the jet just / flies off again.",
         shot="our profile drawing: a throttle lever slams to FULL; the hook skips over the wire; the jet runs off the deck edge "
              "and climbs away; tag 'BOLTER'"),
    dict(id="x6", facts="7 (verdict, ours); the end line is the playbook's T3 line",
         text="Our take? It's a controlled crash, with the clever part hidden below deck. Subscribe for one machine in trouble, explained, every day.",
         cap="Our take? / It's a controlled crash, / with the clever part / hidden below deck. / Subscribe for / one machine in trouble, / explained, / every day.",
         shot="verdict rows (THE CATCH → ONE WIRE, THE BRAKE → WATER + MOTOR, OUR TAKE → A CONTROLLED CRASH); the promise plate "
              "on 'subscribe'; ease back to frame 0 (loop)"),
]
