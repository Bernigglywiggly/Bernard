# Critic round 2: SHORT4_v2 (34.8 s)

Voice re-transcribed; frames (every 0.1 s), beat grid (124.1 BPM), loudness and motion measured.

## Round-1 items
| Item | v2 |
|---|---|
| Twist at 24.4 s; headline vs voice | FIXED (3.8 s) |
| Five text layers (1.6-3.4) | STILL PRESENT |
| Flip never at 1× | FIXED |
| Frame 0: 13 words, car fills bottom 40% | STILL PRESENT |
| 3D label in top 7% | PARTLY: moved to y 163, still 28 px |
| Labels under 48 px | PARTLY: 32-38 px |
| Right-button zone | PARTLY: four new intrusions |
| 4,096 comma, "Ul/St" | FIXED |
| Split captions | PARTLY: 7 down to 5 |
| Near-still diagram (8.1-11.5) | STILL PRESENT |
| Label hold | PARTLY: no judder; frozen 27.33-27.67, 28.20-28.53 |
| Swirl, zoom blur | PARTLY: 2 frames, 1 frame |
| One palette; fades; card on blur | STILL PRESENT (palette 18.4 s) |
| Knife crop | FIXED (see new 3) |
| 50× on the real robot; "so" | FIXED |
| 4,096 over kickers | PARTLY: walkers, but follows "each move works" |
| Cuts on beat | PARTLY: off at 0.60 (+92 ms), 31.57 (+114), 34.07 (+197) |
| Twist pause, drop, hit | PARTLY: ~15 dB music drop for 0.35 s; voice gap 0.24 s; no hit |
| Frame-0 formula | STILL PRESENT |
| Borrowed footage 56% | FIXED: 45.5% |

## New in v2
1. **Clipped:** "ADJUSTS IT" loses its T (21.6-25.6); the verdict reads "THE BODYGUARI" (32.3-34.07).
2. **Button zone:** "ABOUT THE BODYGUARD." reaches x 979, "THE CONTROLLER ADJUSTS" x 987, "STANDING, NOT FIGHTING" x 1023, plus "THE BODYGUARD".
3. **Knife scene:** a 16:9 band floating on black (3.4-7.27, 28.57-30.97); the robot is 21% of frame height.
4. **Captions:** none for 0-1.6 s; page 1 is "WATCHING FROM ITS H2-X". Bad breaks: SMALL / PRINT, LIKE / IT, UNTIL /, TRAINING / CODE, KNIFE / ATTACK.
5. **Wrong picture:** "IS REAL," over the staged scene (3.40-3.7); "REAL" over CGI (31.40-31.57).
6. **Stutter:** the verdict clip repeats every fifth frame.
7. **Loop:** a jump into a 10-frame freeze that doesn't match frame 0.
8. **Short 3's skeleton:** "N A SECOND" card, red-stamp verdict.

## Scores
1. **Hook and frame 0: 7/10.** Line 1 says "you", Unitree, H2-X and kung fu.
2. **Readability: 5/10.** Strong captions (53-62 px), but clipping and the button zone.
3. **Motion: 6/10.** Smooth 7× replay. Diagram, freezes, stutter, loop.
4. **Variety and composition: 6/10.** Good scale changes; one palette; the floating band.
5. **Accuracy: 8/10.** Figures match facts #4-6 and #12-13, with scope. "NOT FIGHTING" is our inference set under their quote; item 5.
6. **Sound: 7/10.** -14.2 LUFS, -1.5 dBTP, music ~12 dB under the voice; 177 wpm; the twist is half-built.
7. **Authorship: 6/10.** The small-print push and the 4,096 pull-back are ours; the structure repeats Short 3.

## Five fixes
1. **Layout (Remotion):** text between x 65 and 950 with auto-fit; verdict at 95 px or less; "STANDING, NOT FIGHTING" above y 864; a render assert for the zones.
2. **Captions:** start at 0.0 and break at phrase ends (SMALL PRINT / TELLS, ROBOTS LIKE IT / START, FALLING OVER / UNTIL, KNIFE ATTACK / IS). Drop the "Real Footage" box. Labels at 48 px.
3. **Cuts:** move the knife cut to the 3.89 beat ("but") and the real-kick cut to 31.45. Re-crop the knife scene tall, pushing 4%.
4. **Motion:** RIFE the verdict clip to 30 fps; push 4% through 27.0-28.57; animate the diagram's kick; hard cut instead of the swirl; loop on an exact copy of frame 0 (≥ 40 dB), no freeze.
5. **Twist:** a 0.45 s voice gap before "But the small print"; a sub hit at 25.63, at least 6 dB over the kicks; slam the card in, no blur.

## Verdict: ONE MORE PASS
Fixes 1-2, the RIFE pass and the 3.89 cut take about an hour. The source is 3 days old (our best Short shipped within ~60 h): make those, check, ship. Skip the rest if it costs a day.
