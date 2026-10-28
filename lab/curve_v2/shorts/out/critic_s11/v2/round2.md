# Critic round 2: SHORT11_v2.mp4 (33.5 s)

Method: rendered frames (sheets every 0.5 s, frame 0, last frame, extra stills at 0.5, 29.3 and 31.5 s) and ffmpeg stats. I did not play the audio. Spoken lines are read from short11.py.

## Round 1 items
| Item | Status |
|---|---|
| Stray "A" at page starts | FIXED. No orphan tokens on any page I could see. |
| Frame 0 had no Mac | FIXED. Keyboard, screen bezel and finger now in frame, "APPLE SAID NO / FOR 16 YEARS". The finger is pointing, not touching, and there is no hinge. |
| "IT DOESN'T WORK" tag tiny in its first second | PARTLY. At 1.0 s it is still a tiny strip; full size only from about 1.5 s. |
| Hook line opens on a date | STILL PRESENT. "In 2010," is still the first caption page. |
| NO/YES stamps in the button strip | FIXED. They now sit at the left, under the year. |
| End plate "story behind the clip everyone's sharing" | FIXED. It is now "THE CURVE: HOW NEW TECH ACTUALLY WORKS" at about 70% height. |
| 2018 Federighi paraphrase | FIXED. Dropped. 2014 is row 43, status V, shown as CNET. |
| Verdict wording as Apple's | PARTLY. The screen now has JOBS / APPLE / OUR TAKE rows. The spoken line and the page "THE THING YOU REACH FOR" are unchanged and still credit Apple. |
| Caption size inconsistent | PARTLY. "FOR SIXTEEN YEARS," (4.5 s), "CHANGES THE ELECTRIC FIELD" (about 15 s), "TWISTS IT TWICE AS HARD" and "THE THING YOU REACH FOR" (29 s) are still smaller than their neighbours. |
| Small sublabels (APPLE EVENT, CNET, TOUCH ON MAC, OUR MATHS, TRACKPAD, YOUR ARM) | STILL PRESENT. About 7 px at 360 px wide. |
| Diagrams too small | PARTLY. The torque diagram is now big and good (about 55% of the height). The grid is still about 35% of the width, and the verdict laptop is still small. |
| Loudness 3-8 s hot | STILL PRESENT. Short-term loudness there is -13.3 to -13.9, which is 0.7 LU hotter than the rest. |
| Recurring object | FIXED. The yellow dot appears at the hinge, in the torque diagram, at the crossing and on the verdict laptop. |

## Scores
| # | Area | Score | Notes |
|---|---|---|---|
| 1 | Hook / frame 0 | 7 | The Mac is clearly a laptop and the kicker is large. The finger does not touch the glass and the busy 3D app competes with the kicker. |
| 2 | Readability | 6 | Captions are good. Sublabels and the shrinking caption pages are not. "TOUCH + TRACKPAD" runs to about 89% width at 29 s, which grazes the button strip. |
| 3 | Motion | 8 | Frozen 3%, near-still 4%, no stretch of 2 s or more. The torque build (18-24 s) and the pinch / swipe / drag word stack are strong. |
| 4 | Variety / composition | 7 | Apple footage, the timeline, the grid, the torque diagram, the footage again and the verdict give clear rhythm. The grid scene (about 12-18 s) is still a small card in empty gradient. |
| 5 | Accuracy | 6 | See below. |
| 6 | Sound | 8 | -14.2 LUFS, true peak -1.5 dBFS, LRA 1.4 LU. Passes. The 3-8 s sections are hot, and the last second fades to -17.4, which suits the loop. |
| 7 | Authorship | 7 | Our maths tags, the yellow-dot motif and the loop (the last frame rebuilds frame 0 exactly). Apple footage is about 9 s of 33.5 s (about 27%): 0-4 s, then about 21.5-26.5 s as two cuts, none over 5 s, all credited APPLE. The purple gradient is still generic. |

## Accuracy detail
- Correct: "A NEWLY DESIGNED HINGE · APPLE, 28 OCT" (row 103); PINCH TO ZOOM / A NATURAL SWIPE / DRAG AND DROP (row 104); Jobs's "IT DOESN'T WORK." and "YOUR ARM WANTS TO FALL OFF." (quote file); 2014 Federighi labelled CNET; "2026 APPLE / TOUCH ON MAC / YES"; OUR MATHS 2x.
- MUST: the spoken line x6 says "Jobs was right about tired arms, so Apple made touch the thing you reach for only when it's quicker." This puts our opinion in Apple's mouth and invents a causal link. Row 109 says Apple said nothing on ergonomics or why, and §8 forbids implying it. The on-screen OUR TAKE row fixes the text but not the voice. "so Apple made" is the offending clause.
- SHOULD: "its bosses kept saying no for sixteen years" with two stamps (2010, 2014) implies a continuous refusal. Cook 2012 was left out and 2018 was dropped. Say "Apple's bosses said no in 2010 and again in 2014".
- "APPLE SAID NO FOR 16 YEARS" in the hook is our arithmetic (2026 - 2010), not Apple's wording. The kicker is acceptable because 2010 and 2014 are verified.

## 5 highest-impact fixes
1. MUST: rewrite x6 and its caption page so the voice does not attribute our take to Apple. For example: "Jobs was right about tired arms. Apple's answer is touch alongside the trackpad. Our take: reach for it only when it's quicker." Re-voice, rebuild the audio, and keep the verdict rows.
2. SHOULD: lock the caption font size across every page, including "FOR SIXTEEN YEARS," and "THE THING YOU REACH FOR".
3. SHOULD: raise every sublabel (APPLE EVENT, CNET, TOUCH ON MAC, TRACKPAD, YOUR ARM, OUR MATHS) to about 40 px cap height. Pull "TOUCH + TRACKPAD" in to under 85% of the width.
4. SHOULD: enlarge the grid scene to about 80% of the width with a push-in on the finger crossing, and make the verdict laptop at least 40% of the height.
5. SHOULD: start the "IT DOESN'T WORK" tag at full size at 0.5 s. Duck the 3-8 s music about 0.7 LU. Optionally open on a shot with the finger touching the glass.

VERDICT: ONE MORE PASS
