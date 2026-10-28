# Critic round 1: SHORT11_v1.mp4 (33.5 s)

Method: rendered frames and ffmpeg stats only (sheets, full-size frame 0, frames at 15.4 s and 32.0 s, loudness.txt, motion.txt, astats). I did not play the audio.

## Scores
| # | Area | Score |
|---|---|---|
| 1 | Hook / frame 0 | 5 |
| 2 | Readability | 6 |
| 3 | Motion | 8 |
| 4 | Variety / composition | 5 |
| 5 | Accuracy | 7 |
| 6 | Sound | 8 |
| 7 | Authorship | 6 |

## 1. Hook (5)
- Frame 0 (0-0.2 s) is a finger prodding a 3D-modelling app (purple spiky mesh, toolbar at the bottom). No Mac, no laptop edge and no hinge is visible, so "APPLE SAID NO FOR 16 YEARS" has no payoff image. It reads as "a finger on some software", not "a touchscreen MacBook".
- The picture is busy and the finger is cropped at the left edge. The kicker is large and good (about 50% of the width, high contrast), and the lime second line reads at thumbnail size.
- Line 1 opens on a date and a claim ("In 2010, Apple said..."). Attention-playbook rule 1 wants the payoff image plus the surprising fact, with "you" said once.
- The "IT DOESN'T WORK. STEVE JOBS, 2010" tag grows in at 0.5-1.5 s and is tiny at first. Its first 1 s is unreadable on a phone.
- The first caption page "IN 2010," is short, so the hook has no ask in its first 1.5 s.

## 2. Readability at 360 px (6)
- Kicker, captions and verdict rows are fine. The verdict (30-32 s) is the best-looking frame.
- Too small at 360 px: timeline sublabels "APPLE EVENT / CNET / WIRED" (7-12 s) and "TOUCH ON MAC", the "APPLE" credit chip, the "OUR MATHS" label (19-20 s), "TRACKPAD" and "YOUR ARM" (28-33 s), and "THE THING YOU REACH FOR" at 28-29 s, which shrinks to roughly 60% of the size of neighbouring pages.
- Safe areas: the NO and YES stamps sit at x of about 76-93% (7-12 s), which overlaps the Shorts button strip (x above 88%). The end plate "THE STORY BEHIND THE CLIP EVERYONE'S SHARING" (32-33.5 s) sits at y of about 77-83%, in the title area.
- CAPTION BUG (MUST FIX): many pages start with a stray "A": "A TIRES YOUR ARM." (about 11 s), "A UNDER THE GLASS", "A OF INVISIBLE WIRES,", "A AND YOUR FINGER", "A BUT A LAPTOP SCREEN", "A SO A TAP", "A HANGS ON A HINGE", "A TWISTS IT TWICE AS HARD", "A ONLY WHEN". The tell-tale is the page after "…TO A SCREEN": the stray token is a carry-over. It looks broken and also breaks the "never end/start a page on a function word" rule.

## 3. Motion (8)
- motion.txt: frozen 3%, near-still 4%, with no stretch of 2 s or more. Passes.
- Dead spots: the hinge diagram (about 15-16 s) is a thin line alone in the frame. The timeline holds roughly 5 s of stamp-stamp-stamp at the same size. The grid scene (about 12-15 s) has the first 1 s empty (a blank panel with the "A" caption).
- Easing looks consistent: the same stamp and pop everywhere. Vary the speed (a slow hold followed by a fast exit).

## 4. Variety / composition (5)
- Scenes 2-6 share one layout: dark purple gradient, header at the top, one diagram in the middle, caption at about 72%. This is the "small card floating in an empty frame" and "centred gradient" the banned list names.
- Subject sizes: the grid is about 35% of the frame width, the hinge/torque diagram about 30% wide and 15% tall (15.4 s), the verdict laptop about 25% of the height. None reaches 60-85%. Roughly 40% of the frame is empty gradient in most scenes.
- No scale variation: there is no close-up on the fingertip crossing and no full-frame type moment.
- Borrowed footage is about 8 s of 33.5 s (about 25%, two shots under 5 s, credited APPLE). That is compliant, but the first shot is the weakest of the clips.

## 5. Accuracy (7)
Checked against the facts file, §5 rows 101/103/104/109 and Jobs's quote file.
- Correct: "A NEWLY DESIGNED HINGE · APPLE, 28 OCT"; "PINCH TO ZOOM / A NATURAL SWIPE / DRAG AND DROP"; "TOUCH + TRACKPAD" (Apple: "in tandem with…trackpad gestures"); "TOUCH ON MAC" and 2026 YES; Jobs's "IT DOESN'T WORK." and "YOUR ARM WANTS TO FALL OFF."; "16 years" (our maths); 2x torque (labelled OUR MATHS).
- Mismatch 1: Federighi 2014 (CNET) and 2018 (WIRED) are row 43/44 status U, and 2018 is only a paraphrase. They get a red NO stamp as though they were verbatim refusals. The narration "its bosses kept saying no for sixteen years" turns a mix of unverified and paraphrased items into a continuous refusal.
- Mismatch 2: the verdict says "Apple made touch the thing you reach for only when it's quicker". Row 109: Apple said nothing on ergonomics or why. This is our opinion, shown on screen under an "APPLE, 2026 →" label ahead of "OUR TAKE". Rephrase to something Apple did say ("Apple says touch works with the trackpad and keyboard"), then give our take.
- "Jobs was right about tired arms" is our judgement, which is fine. §8 forbids saying that gorilla arm is measured on laptops, and the Short doesn't claim that.
- End plate "THE STORY BEHIND THE CLIP EVERYONE'S SHARING" is not spoken and not in the facts file. It implies a viral clip and has no source.

## 6. Sound (8)
- Integrated -14.2 LUFS, true peak -1.5 dBFS (it passes), LRA 1.4 LU.
- Short-term runs -13.3 to -13.9 at 3-8 s (hot by about 0.7 LU) and sags to -14.7 at 11-21 s, then -17.4 in the last second (a fade, which helps the loop). The voice and bed ratio can't be judged from this. LRA 1.4 suggests the bed is compressed against the voice, so check that nothing is masking it.
- No silences over 0.4 s at -45 dB, so there are no dead beats.
- I could not verify beat alignment of cuts without a beat grid.

## 7. Authorship (6)
- Positives: it has a clear point of view ("touch as an extra"), our own maths tags, and a loop whose last frame rebuilds frame 0.
- Negatives: the purple gradient with lime and cyan accents and the stamp motif look like every other Short on the channel. Nothing recurs that a viewer would call "The Curve", such as a recurring object. The 2014 and 2018 rows are generic.
- Make it ours: carry one object (the yellow hinge dot or the fingertip) across every scene.

## 5 highest-impact fixes
1. MUST: fix the caption tokeniser. Drop the carried-over stray "A" (and any page starting with a function word) in the caption page builder, then re-render a still of every page. Also hold caption font size constant across pages.
2. MUST: replace frame 0 and the first 4 s. Use a shot where the MacBook Pro edge and keyboard are in frame with the finger on the screen, or composite our hinge diagram's yellow dot over the Apple shot, and put "TOUCH MAC" or "FINGER ON A MAC" in the kicker so it passes the thumbnail test. Start the "IT DOESN'T WORK" tag at full size at 0.5 s.
3. MUST: fix the accuracy items. Stamp NO only on verified items (Jobs 2010). Render 2014 and 2018 as a neutral "SAID IT WAS NOT A PRIORITY / FATIGUING (PARAPHRASE)" or drop them. Reword the verdict to Apple's own words and then "OUR TAKE". Delete or source the "clip everyone's sharing" plate. Keep NO/YES stamps left of x 880.
4. SHOULD: scale the diagrams to 60-85% of the frame. Torque diagram to full height with the arc and force arrow huge, grid to about 80% width with a macro push-in on the crossing, and fill the empty halves with the label or readout. Add one full-frame type moment ("16 YEARS" in the timeline).
5. SHOULD: raise the small text. Timeline sublabels and the credit chip to a 40 px cap height or more, move the end plate up to y of 70% or less, and pull the 3-8 s music down about 0.7 LU. Add a recurring object (the yellow hinge dot), so frames read as this channel.

VERDICT: ONE MORE PASS
