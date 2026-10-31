# Critic round 2: Short 14 v2 (SHORT14_v2.mp4, 36.9 s)
Judged on contact sheets (0.5 s, plus extra frames 19-37 s), phone.jpg, motion/loudness/loop files, facts, CRAFT, RUNBOOK 8b. Limit: I heard only the mix, not stems or SFX.

## Round 1 findings
| # | Finding | Status | Evidence |
|---|---|---|---|
| 1 | Footage band small, bottom third empty | PARTLY | Band now full-width, ~17-66% of height, booster about 2x bigger; caption at y~1450. Bottom ~25% still empty (Shorts UI zone, acceptable). |
| 1b | Drawings 15-25% fill in 8-15, 23-26, 28-36 s | STILL PRESENT | Booster/ship pair is ~35% wide; why-legs ship ~15%; verdict tower+ship ~12% wide, in the lower-right, upper-left empty. |
| 2 | Text under 68 px floor | PARTLY | "THE BOOSTER UNDER IT" (10-12 s) still auto-shrunk to ~45 px; "EXPECTED NOV 2026" (12-14 s) ~40 px; "SPACEX'S PLAN, DRAWN BY US" ~40 px grey; "BELLY FIRST" tag pops in at ~15 px for a frame. Credit mono ~36 px. |
| 3 | Twist + our drawing by 2 s | FIXED | "Nobody has ever caught a Starship" is line 1; frame 0 has ring, our ship above the arms, scoreboard. |
| 4 | Dead beats | PARTLY | 8-14 s now builds (ticks, FLIGHT 15 stamp, date); fall, flip, arms and clock sweep are new. Verdict 28-35 s is still a static small tower with rows landing. |
| 5 | Authorship / one ship across scenes | PARTLY | Ship recurs (fall, flip, legs, verdict) but the scenes are all the same dark layout. |
| 5b | NOT TO SCALE, FLIGHT 5 credit | FIXED | Both on screen. |

## Scores
1. **Hook / frame 0: 7/10.** Moving catch footage, ring, ship drawn above, 4-word kicker, twist spoken at 0-3 s. As a thumbnail the booster is still tiny (~60 px wide) and the dark band bottom is empty. 0-3 s.
2. **Readability: 5/10.** Problems: 10-12 s, 12-14 s, 15-19 s (see above); all pop-in tags start tiny. Safe areas are fine (nothing at x>950 except the scoreboard's 3rd box, inside).
3. **Motion: 7/10.** Frozen 0%, near-still 4% (1.6 s), no stretch over 2 s. Weak: the verdict 28-35 s and the legs scene 23-25 s (static ship, then a clock). Easing looks uniform.
4. **Variety/composition: 5/10.** Better than v1 (band, comparison, side-on fall, tower, clock, text stack), but subjects are small and centred or lower-right with empty space in 8-15, 23-26 and 28-36 s. Banned defaults still there: small subject floating in an empty frame, corner kickers.
5. **Accuracy: 8/10.** Matches the facts: 3 boosters (rows 3, 0), ships 0 (row 4), Flight 15, "Expected Nov 2026" month only (row 13 U, allowed), belly-first, flaps, engines, upright, two arms (row 20), no legs, under an hour (row 22), no speeds. Risks: (a) the clock sweeps a ~20 min wedge to "UNDER 1 HOUR" (visually a number SpaceX never gave; row 23); make it a full sweep to 60 min or remove the wedge. (b) The "Musk's goal" tag has no date, add "MUSK, 20 OCT". (c) The ship is drawn with 4 flaps visible only as grey fins; "FLAPS STEER" has no moving flap. (d) "NOW CATCH THE SHIP?" is in the kicker for 12 s over footage that shows the booster: fine.
6. **Sound: 7/10.** -14.1 LUFS, -1.4 dBFS peak, LRA 1.2 LU, short-term -13.3 to -14.8: on target and very flat. Loop PSNR 41.9 dB (near-identical). Last second drops to -16.7 (fade, fine). SFX on scene cuts (8, 13, 18, 23, 28 s) not verified.
7. **Authorship: 5/10.** Consistent but templated (kicker, drawing, yellow caption, dark purple). The "3 BOOSTERS / THE SHIP / LIKE AN AIRLINER" stack is the most ours.

Compliance 8b: frame 0 moving + mark + question PASS; drawing by 2 s PASS; every line adds why/number/verdict PASS; end line with subscribe PASS (plate at y~1450, above the UI). Footage ~12.5 s of 37 s (34%): PASS under half, if each shot is under 5 s of source.

## Top 5 fixes
1. **MUST: Fixed type floor.** Kill the auto-shrink: "THE BOOSTER UNDER IT" to two lines at the standard size; "EXPECTED NOV 2026" and "SPACEX'S PLAN, DRAWN BY US" to 68 px with a bright colour; the tags must scale in from at least 0.8, not 0.2.
2. **MUST: Clock honesty.** Remove the ~20 min wedge; sweep a full hour, or show just "UNDER 1 HOUR" without a pie.
3. **SHOULD: Scale the drawings.** Make the verdict tower and catch scenes (19-25 s, 28-36 s) fill 60% of the height, centred; ship at 25% frame width. Scale the legs scene ship to 45% height.
4. **SHOULD: Animate the verdict.** On "stops being thrown away" lower the ship into the arms and close them; add a ship that visibly rotates through all scenes via a hard-cut scale match.
5. **SHOULD: Thumbnail/authorship.** Zoom the frame 0 footage so the booster is about 25% of the width; vary a background colour per scene; add "MUSK, 20 OCT" to the goal tag; check the whoosh/click SFX at cuts.

**ONE MORE PASS** (MUST 1-2 are quick; then ship).
