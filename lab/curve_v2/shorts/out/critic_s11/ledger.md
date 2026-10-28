# Short 11 critic ledger

| Round | # | Finding | Fix | Status |
|---|---|---|---|---|
| scaffold | 1 MUST | Grid: finger covers the lit crossing; generic ripples; row/column lit only on "cross"; scan dot flickers | Lit dot drawn above the finger; row and column light on "changes"; grid zooms 1 to 1.35 about the crossing (clipped to the panel); four field lines bow into the fingertip; scan = one crossing a frame with a 6-dot fading trail | FIXED 28 Oct 15:55 (B) |
| scaffold | 2 MUST | Hinge: bare L-shape for 3.3 s; no "distance"; arcs 2.9x | Lid opens on "hangs"; the drawn finger taps at exactly L and L/2; bold FAR (acid) and HALF (cyan) dimension bars; equal-radius arcs, 80 and 40 degrees; a ghost screen at each peak swing | FIXED 15:55 (B) |
| scaffold | 3a MUST | "MACBOOK PRO · YES" fits the non-touch M6 model too | `PRODUCT_2026` constant shows "⏳ APPLE'S NAME" until slot 100 is filled | THE 17:40 RUN: set it from Apple's press release |
| scaffold | 3b MUST | "TOUCH AS AN EXTRA" is REPORTED; "WHEN IT'S QUICKER" is our take | Row 2 reads "MACRUMORS REPORTS →" (`EXTRA_SOURCE`), row 3 "OUR TAKE →" | FIXED 15:55; THE RUN switches row 2 to "APPLE, 2026 →" only if slot 104 says touch is optional |
| scaffold | 3c MUST | Cook's 2012 line was about merging tablet and laptop | Cook removed: the timeline is Jobs 2010, Federighi 2014, Federighi 2018, then 2026 | FIXED 15:55 (script note updated) |
| scaffold | 4 MUST | Verdict: small floating laptop, giant finger, label on the pill, still for 4.1 s | Bigger laptop; a hand (palm + finger) works the trackpad with a cursor dot following it, reaches the screen on "reach", taps, comes back; YOUR ARM bar at 10%; rows at 200/380/560 | FIXED 15:55 |
| scaffold | 5 MUST | Labels under 48 px cap height; OUR MATHS tape and YES stamp in the Shorts button strip | ROWS SEND, COLUMNS LISTEN, HINGE, YOUR ARM, TAP AT THE TOP, HALFWAY DOWN at 68 px; tags at 60 px, the hook's Jobs tag and the maths tape on two lines (right edge under 930); stamps above y 1000 | FIXED 15:55 |
| scaffold | 6 MUST | No channel mark | Short 8's ChannelPromise from "quicker" - 14 to the loop; captions hidden under it; gone before the loop, so the last frame is still frame 0 (PSNR inf) | FIXED 15:55 |
| scaffold | 7 SHOULD | Arm scene short; bar 84% full by f215 | Bar and sag now linear, with a growing tremor | PART: scene length is set by the voice line; the run can lengthen the line |
| scaffold | 8 SHOULD | Templated look | The drawn finger now carries through hook, grid, hinge and verdict | PART: the rising-curve mark is not used yet |
| r1 (v1) | 1 MUST | Stray "A" at the start of caption pages from 11 s on | Root cause: "a" and "screen" share startMs 7850, so the kit's caption spans had duplicate React keys and an orphan node stayed on screen; kit key is now fromMs + index | FIXED v2 |
| r1 (v1) | 2 MUST | Frame 0 shows no Mac | Hook and loop recut from Apple's wider shot (40.35 s): a hand reaching to the screen, keyboard in frame | FIXED v2 |
| r1 (v1) | 3 MUST | Federighi 2014/2018 stamped NO on unverified rows; unsourced end plate; stamps in the button strip | 2014 verified (BGR quoting CNET: "We're not all that interested in building one."), 2018 dropped; end plate now "THE CURVE: HOW NEW TECH ACTUALLY WORKS" at y 1310; stamps under each year at x 56 | FIXED v2 |
| r1 (v1) | 3 MUST (part) | Verdict line is our opinion | Kept: on screen it is split APPLE, 2026 → TOUCH + TRACKPAD (Apple's "in tandem") and OUR TAKE → WHEN IT'S QUICKER | NO CHANGE (labelled) |
| r1 (v1) | 4-5 SHOULD | Diagrams under 60%; small text | Timeline type 84/56/48 → 96/64/56; diagrams unchanged | PART |
| r2 (v2) | 1 MUST | Spoken verdict "so Apple made touch the thing you reach for..." put our take in Apple's mouth | x6 now "Our take? Jobs was right about tired arms, so touch is the thing you reach for only when it's quicker."; re-voiced (Chris take v2b, word-perfect, 31.6 s) | FIXED v3 |
| r2 (v2) | 3 SHOULD | Timeline sublabels small | 56 → 64 px | FIXED v3 |
| r2 (v2) | sound | v3 first master peaked -0.9 dBFS | loudnorm TP -2 + limiter: -14.3 LUFS, -1.9 dBFS | FIXED v3 |
| r2 (v2) | 2, 4, 5 SHOULD | Caption size varies; grid under 80%; tag pops in small; 3-8 s music hot | not changed | OPEN (cosmetic) |
