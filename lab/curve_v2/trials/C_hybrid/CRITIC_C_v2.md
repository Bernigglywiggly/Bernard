# CRITIC: C_real_footage_v2.mp4 (16.6 s segment, Tesla ramp footage + Remotion graphics)

Independent critic, 18 Oct 2026. The critic did not build this segment and judged it blind to earlier critiques.
Judged against Zack D (curiosity, pacing), Kurzgesagt and Real Engineering (clarity), and CRAFT.md §3, §5, §6, §8 and §9.
Fixes are ranked by how much they change **retention in the first 3 s and readability at phone size**, because a vertical Short ships today.

## 1. Score: 6 / 10

The segment has a strong subject, a tight and accurate 50-word script, sync that a top channel would sign off on, and loudness exactly on spec.
These problems hold it back:
- Frame 0 never shows its own claim. The camera looks up at the curl, so the inverted car reads as "a car on a steep ramp". The viewer only learns it is upside down when the diagram lands at 3.9 s.
- The diagram is unreadable on a phone, and it uses the bordered-card look that CRAFT bans.
- The climax (the drop) stutters at about 21 fps.
- The landing is never shown.
- When the Short replays, the loop seam visibly jumps.
- The payoff line uses the "isn't X, it's Y" device, which is both a Claudism and literally wrong.

Fixes 1-8 would make this a 7.5-8 Short.

**Measured**
- Video: 1920x1080, 30 fps.
- Loudness: **I -14.3 LUFS, TP -1.4 dBTP, LRA 1.4 LU**, which is on spec.
- Voice vs music bed: the voice runs at about -12 to -14 LUFS momentary. The bed alone measures about -24 LUFS, roughly 11 LU under the voice, and sits mostly below 150 Hz, so speech stays clear.
- Motion: 0% frozen or near-still.
- Duplicate frames: 2% in the opening (expected, from the 8x interpolated slow motion), **30% in the drop**, 2% in the reprise.
- Narration timing: line 1 0.10-2.50 · gap · line 2 3.40-6.90 · gap 6.95-7.75 · line 3 7.80-12.45 · line 4 12.75-14.05 · line 5 14.55-15.80.
- Cap height at 360 px wide:

| Text | Cap height |
|---|---|
| Hook | ~19 px |
| VACUUMED. | ~14 px |
| UP TO 2x | ~9 px |
| Callout | ~6.5 px |
| Diagram labels and credit | ~5.6 px |

## 2. Ranked fixes

| # | Time | Problem | Exact fix |
|---|---|---|---|
| 1 | 0.0-3.0 | **The inversion doesn't read at frame 0.** Seen from below, the upside-down car looks like a car on a ramp. While the narration says "isn't falling", the 8x slow motion shows the car sliding down the frame. | For 9:16, crop the 4K source tall (1215x2160, scaled to 1080x1920, so no upscale) to show the ramp lip above the car. Put the inset's inverted-car-under-arch icon next to "WHY ISN'T IT FALLING?" from frame 0, or add a "GROUND ↓" cue. Keep the hook in the top third at 120 px cap height or more. |
| 2 | 0.1-2.5 | Line 1 never says the search term (CRAFT §9.1; 79% of Curve views come from search). | Re-voice it as: "Tesla's new Roadster is hanging upside down, and it isn't falling." |
| 3 | 2.5-3.4 | 0.9 s of music only, including 0.7 s with nothing new on screen, right in the swipe window. | Cut the gap to 0.25 s or less, so "Fans underneath…" starts at about 2.75 s and the diagram enters on it. |
| 4 | 3.4-7.2 | **The diagram fails at phone size and breaks house rules.** <br>• Labels are ~5.6 px tall at 360 px wide. <br>• WEIGHT sits on the arch and butts into its own arrowhead. <br>• SUCTION crosses the arch and spills about 30 px outside the card. <br>• The bordered card and the "SIDE VIEW" corner label are banned defaults (CRAFT §3). <br>• The suction arrow grows up out of empty space below the car, so it reads as air blowing up (the opposite of suction). <br>• The left wheel floats about 20 px below the ramp. | • Rebuild it full-width in the 9:16 lower half, with no card, border or corner label. <br>• Labels at 48 px cap height or more on a 1080-wide frame. <br>• Badge reads "UP TO 2× ITS WEIGHT". <br>• Anchor the suction arrow on the car's floor, pointing up into the ramp, and add two small outflow arrows from the gap. <br>• Keep the 2:1 arrow lengths. <br>• Wheels touch the ramp line. |
| 5 | 7.43-11.63 | **The climax stutters.** 38 of 127 frames are duplicates, held for 1-3 frames in an irregular pattern, so only about 21 distinct frames per second reach the screen. The 23.976 fps source was converted to 30 fps by duplicating frames, without interpolation. The graphics animate at a true 30 fps on top, which makes the stutter more obvious. | Re-time the drop from the 4K source with RIFE, or with `minterpolate=mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`, at 30 fps. Check the plumes and smoke for warping. Alternatively, render the whole Short at 23.976 fps. |
| 6 | 11.07-12.45 | **The landing is never shown.** The rewind starts at 11.67 s while the car is still hovering (at 11.63 s its wheels are clear of the smoke), so "soften the landing" plays over the rewind. | Hold the drop about 0.8 s longer so the car settles into the smoke on "landing", and start the rewind after that word, at about 12.5 s. |
| 7 | 12.75-15.8 | The payoff "So it isn't driving on the ceiling. It's being vacuumed to it." uses the banned "isn't X, it's Y" device. It only repeats line 2, and it is **misleading**: the car *is* driving upside down, and suction is what lets its tyres grip. `script_lint.py` passes it, because it only flags sentences that start with "Not". | Replace it with a new sourced fact (row 52 / P10): "It's vacuumed on so hard that Tesla says it could hang there standing still." Slam VACUUMED. onto the word "vacuumed". |
| 8 | 16.57 → 0.00 | **The loop seam jumps.** The last frame is the opening shot about 4 s further on (car lower, framing tighter), so the replay visibly snaps back. | Make the last frame the exact frame-0 picture: either reverse the reprise, or end the rewind exactly on frame 0 and hold it under the end word. |
| 9 | 9.4-10.7 | The tracked ring drifts 50-60 px off the car into empty air (10.4-10.7 s), pointing where no jet is firing. | Track the ring onto the down-jets that are actually firing, and exit it by 10.3 s. |
| 10 | 7.40 | One-frame leftover: a sliver of the inset ("TION" plus a corner of the badge) shows on the first frame of the drop shot. | Finish the slide-out before the cut, or cut one frame later. |
| 11 | 7.40, sound | The cut to the drop misses the bed's downbeat: the bed runs at about 124 BPM with a downbeat at 7.74 s. The cut also comes 0.6 s before "Then". There are no sound effects anywhere. | Cut at 7.74 s on "Then". Add a soft whoosh on the cut, a cold-gas hiss under the plumes, a low settle on touchdown, and a tape-rewind zip at the rewind. |
| 12 | Throughout | • Glows on FALLING?, VACUUMED. and the suction arrow (banned "glows on UI"). <br>• 8x slow motion with no read-out. <br>• The credit stays up for all 16.6 s and is about 6 px tall at phone size. | • Replace the glows with a hard outline. <br>• Change the credit to "FOOTAGE: TESLA · 8× SLOWER" (honest, and more transformative). <br>• In 9:16, show the credit above the bottom 20% for 0-3 s and for the last 2 s only. <br>• Put the URL in the description (ZACK_D §12 rule 5). |

## 3. Facts table

| Claim (narration or on screen) | Source row | Verdict |
|---|---|---|
| "This car is hanging upside down" | §1 row 32 (P1, P2) | ✓ shown live |
| "it isn't falling" / WHY ISN'T IT FALLING? | rows 32, 52 | ✓ |
| "Fans underneath suck it onto the ramp" | row 52 (P1, P10) | ✓ for the mechanism. The file doesn't say where the fans sit; "pull air from underneath" is the exact wording. Minor |
| "up to twice its own weight" / UP TO 2× | row 32 (Moravy "up to 2 G's", 08:11), row 52, §5 row 106 | ✓ as Tesla's own figure, not independently measured. On screen it needs "its weight" |
| Diagram: car upside down under the arch, suction arrow about 2x the weight arrow | rows 52, 106 | ✓ the core physics is right. Leaving out the ramp's reaction force is fine; the suction arrow drawn as a push is fix 4 |
| "Then it drops off" | row 33 (P2, S3, S5) | ✓ |
| "gas jets roll it upright" / callout | rows 33, 55, 90 | ✓ "Gas" avoids the air-vs-nitrogen conflict in row 83 |
| "and soften the landing" | rows 33, 87, 90 (the demo car has the Rocket setup, row 86) | ✓ true, but not shown on screen (fix 6) |
| "So it isn't driving on the ceiling" | rows 32, 52 | ✗ **misleading**: it does drive upside down, and the suction is what makes that possible |
| "It's being vacuumed to it" / VACUUMED. | row 52 | ✓ as a metaphor |
| FOOTAGE: TESLA · ROADSTER DEMO, 15 OCT 2026 | §0 (15 Oct local), §10 B; SOURCES.txt: The Ramp 0:18-0:25 | ✓ |
| Rows 85-89 (COPVs, nozzles, valves, 80 kN) | — | Not used in this segment, so nothing to conflict |

No number is wrong. The only factual problem is the misleading payoff line, which fix 7 replaces.

## 4. What works and must be kept

- **Footage use within house rules.** The whole segment is built from 7 s of Tesla's 4K Ramp clip. The source file has no audio track, so there is nothing for Content ID to match on sound. It is credited and transformed, which keeps it inside ZACK_D §12.
- **The hook.** A 4-word question in white and magenta that exits fast (0.2 s).
- **Sync.**

| Graphic | Lands at | On the word |
|---|---|---|
| Diagram | 3.33 s | "Fans" |
| Suction arrow | 4.4 s | "suck" |
| 2× badge | 6.27 s | "twice" |
| Callout | 9.23 s | "gas jets" |
| End word | 14.63 s | "It's being" |

- **The script.** One number, said the way people say it. "Gas jets" stays safe on the air-vs-nitrogen question.
- **The diagram's physics.** The car is upside down under the arch, with 2:1 arrows.
- **The opening slow motion.** Clean at 1.0, 3.0 and 6.0 s: 8 consecutive frames at each point show no warping, ghosting or duplicates.
- **The mix.** -14.3 LUFS and -1.4 dBTP, with a low bed that keeps speech clear.
- **The loop structure.** A question at the start, an answer at the end, and a rewind back to the opening image.
- **Pacing.** Springs on entrances, fast exits, and something new at least every 2.5 s.

## Shorts potential

The pull is high: an upside-down car explains itself once it is legible, and the event is three days old. That also means the news window is closing, so ship today.

The 16:9 layout won't survive a centre crop, because the hook text and the inset sit outside it. The Short has to be built natively in 9:16 from the 4K source.

After fixes the Short runs about 17-18 s. That is under the 20-35 s default in CRAFT §9.3, but it is fine for a tight loop once the seam is invisible; don't pad it.

The minimum to do today is fixes 1-4. Add 5-8 if there is time.

Suggested line for CRAFT's "Learned on our films" list: the lint misses "It isn't X. It's Y.", so add a regex for it.
