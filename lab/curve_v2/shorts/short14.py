"""Curve Short 14 (PRE-BUILT Sat 31 Oct 2026; uploads the day Starship Flight 15 gets a date or flies): "How SpaceX Will Catch a Falling Starship"

Account A, Sat 31 Oct 2026 ~08:55 UK (one-off a-starship-prebuild run). Facts: lab/research/STARSHIP_FLIGHT15_FACTS.md
(rows; section 0 = the 31 Oct re-check). Pictures: SpaceX's own video of the first tower catch (Flight 5, 13 Oct 2024;
"Starship's Fifth Flight Test" on SpaceX's YouTube), 5 s or less a shot, credited, shown as a band; everything else is our
own drawing: the catch scoreboard, the belly-first fall, the flip into the arms, the no-legs trade, the verdict.
Playbook rules (RUNBOOK §8b): frame 0 already moving with one drawn mark and a 4-word question, our drawing on screen
from frame 0, the spoken end line with "subscribe".

LAUNCH DAY: only DATE_PHRASE (x2) changes, e.g. "on November 8th" once SpaceX posts the date; re-voice x2 if it changes,
and change DATE_STAMP in CurveV2Short14.tsx to match. After the flight, re-write the facts file before any upload.

Frame 0: SpaceX's shot of the booster dropping into the tower's arms at sunset, a ring drawn on the arms, kicker
"NOW CATCH / THE SHIP?", the scoreboard BOOSTER 3 / SHIP 0. Loop: the verdict eases back to that picture.
"""
TITLE = "How SpaceX Will Catch a Falling Starship"
DATE_PHRASE = "expected in November"  # launch day: "on November 8th" (SpaceX's own date only)
LINES = [
    dict(id="x1", facts="3 + section 0 (three booster catches: Flights 5, 7, 8); 10 (next: the ship)",
         text="You're watching a tower catch a falling rocket, which it has done three times. Next, SpaceX wants it to catch the ship on top.",
         cap="You're watching / a tower catch / a falling rocket, / which it has done / three times. / Next, SpaceX wants it / to catch / the ship on top.",
         shot="frame 0 = SpaceX's booster dropping into the arms (band), ring on the arms, kicker 'NOW CATCH / THE SHIP?'; "
              "under the band our scoreboard BOOSTER 3 / SHIP 0, ticks land on 'three times'"),
    dict(id="x2", facts="4 (no ship caught); 13 + section 0 (Flight 15, NET Nov, no SpaceX date)",
         text=f"Nobody has ever caught one, and SpaceX plans to try on Flight 15, {DATE_PHRASE}.",
         cap=f"Nobody has ever / caught one, / and SpaceX plans / to try on Flight 15, / {DATE_PHRASE}.",
         shot="SpaceX's steam-wrapped catch in the band; stamp 'FLIGHT 15' + DATE_STAMP; our drawing of booster and ship side by side, "
              "the ship's tick box still empty"),
    dict(id="x3", facts="20 (falls belly-first, steering with its flaps)",
         text="The ship falls back from space belly first, steering with its flaps like a skydiver.",
         cap="The ship falls back / from space / belly first, / steering with its flaps / like a skydiver.",
         shot="our drawing: the ship flat on its belly, falling through streaks, four flaps twitching; tags 'BELLY FIRST', 'FLAPS STEER'"),
    dict(id="x4", facts="20 (engines fire near the tower, swings upright, drops between the arms, the arms close)",
         text="Near the tower, its engines light, it swings upright, and drops between two giant arms.",
         cap="Near the tower, / its engines light, / it swings upright, / and drops between / two giant arms.",
         shot="our drawing: flame on 'light', the ship rotates to vertical on 'upright', drops between the tower's arms, which close; "
              "label 'OUR DRAWING OF SPACEX'S PLAN'"),
    dict(id="x5", facts="22 (no landing legs = less mass; Musk's goal: fly again in under an hour)",
         text="No landing legs means less to carry, and Musk wants it flying again in under an hour.",
         cap="No landing legs / means less to carry, / and Musk wants it / flying again / in under an hour.",
         shot="our drawing: legs on the ship crossed out, tag 'NO LEGS = LESS WEIGHT'; a clock face sweeps to 'UNDER 1 HOUR', "
              "tag 'MUSK'S GOAL'"),
    dict(id="x6", facts="verdict, ours; the end line is the playbook's T3 line",
         text="Our take? If the arms hold, a rocket stops being thrown away and starts working like an airliner. Subscribe for one machine in trouble, explained, every day.",
         cap="Our take? / If the arms hold, / a rocket stops / being thrown away / and starts working / like an airliner. / Subscribe for / one machine in trouble, / explained, / every day.",
         shot="verdict rows (CAUGHT SO FAR → 3 BOOSTERS, NEXT → THE SHIP, OUR TAKE → LIKE AN AIRLINER); the promise plate on "
              "'subscribe'; ease back to frame 0 (loop)"),
]
