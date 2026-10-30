# Critic round 1: Short 13 v1 (35.03 s, 1080x1920)

**ONE MORE PASS.** Two small MUSTs; the hook is the real weakness.

## Scores
**1. Hook 6/10.** Passes the 30 Oct rules (moving frame 0, ring, 4-word question, own dial, loop 42.8 dB). But the jet is ~2% of the frame in a 24%-tall band, the bottom 30% is empty, kicker and dial never move 0-3.8 s, and the most saturated object is a half-cropped red-vest crewman (0-1.5 s). The question closes at 6.3 s; the next open loop is at 14.0 s. 6.3-11.1 s only describes the clip, inside the 5-10 s drop window.

**2. Readability 6/10.** Contrast fine. 6 of 22 caption pages are 39-49 px high (13-16 px at 360 wide) against 63 px: 9.2, 13.9, 14.9, 18.4, 26.8, 27.9 s. Credit 44 px (floor 68). Stamp "13 OCT 2026" rests at x 528-1067, clipped on entry and over "KENNEDY"/"CLASS", 10.47-11.13 s; "ADVANCED ARRESTING GEAR" cut at the right edge 16.30-16.43 s; "BOLTER: GO AROUND" reaches x 1014 at 24.60-24.70 s. Cause: Tag spring (230, 10) overshoots ~33%.

**3. Motion 7/10.** No frozen frame over 2 s; cue pops every 1-2 s. 29.5-34.0 s is near-still (frame diff 0.12 vs 0.6-3.9 elsewhere; motion.txt's 0% misses it). Dial and scene pushes are linear; six hard cuts carry nothing across.

**4. Variety and composition 4/10.** Drawn jet 2.4% of frame; lit pixels 3-14% over 11-29 s. The "?" box (14.0-16.0 s) and hull icon with an 80x14 px "jet" (6.3-11.1 s) are small cards in empty frames. One deck-line cross-section serves 3 of 6 scenes (52% of runtime); every scene opens with the same left heading.

**5. Accuracy 7/10.** Names, dates and tags match. Mismatches: (a) dial "150 MPH, 0.0 to 2.0 S" sits on the 13 Oct footage; the facts file forbids any speed or stopping time for that landing (row 4 is MK 7 data). It hits 0 at 5.84 s while the band shows a jet still moving; the head-on source needs ~2.7 s to nearly stop (4.1 s slowed). (b) "ONE STEEL WIRE" 25.2-34.0 s vs "never a count". (c) "two seconds" lacks "about" (kicker, VO). Footage 35%, longest shot 4.83 s: OK. DoD non-endorsement line goes in the description.

**6. Sound 8/10.** -14.2 LUFS, TP -1.5 dBFS, LRA 1.2. Six scene cuts land 0-20 ms after bed kicks; the 34.03 s rewind lands 167 ms late. Bed ~11 dB under voice, a little hot. SFX soft, not harsh.

**7. Authorship 5/10.** S10-S13 share backdrop, heading position, captions and stickers, and S12 (28.7 s) and S13 (25-34 s) end on the same arrow-row stack: palette is brand, the structure repeats. No source on screen but the credit. "A controlled crash" is the only point of view, set as a text row. Unmistakable: a signature drawn curve (the live 150-to-0 speed curve), one continuous camera, an on-screen source.

## Fixes
1. **MUST** Overflow and collision. Stamp to left 60, top ~1300 (names up 30 px); two-line "ADVANCED / ARRESTING GEAR" and "BOLTER / GO AROUND" at 68 px; kit Tag damping 10 to 20 (overshoot 33% to 6%). Re-scan the button strip and right edge: zero bright pixels.
2. **MUST** Facts compliance. Dial: "ABOUT" before 150 and the final "2 S" (no decimal), 68 px "TYPICAL LANDING" under it; "ONE STEEL WIRE" to "A STEEL WIRE".
3. **SHOULD** First 11 s. Re-prep s13_head from source frame ~186 at real speed (no RIFE: crewman out, wire taut, the stop visible), re-measure TRACK, punch 1.4x on the ring. Trim x2 to "This F-35C was the first jet to land on the Navy's newest carrier." to reach the machine ~2 s sooner.
4. **SHOULD** Composition and authorship. Cross-section at 1.6x (jet ~650 px), one camera: push to the hook at T.steel, drop through the deck into the machine at S.aag. Loop the catch (Jet + catchX, 2.5 s) under the verdict, 29.3-34.0 s. Add a 68 px "SOURCE · QINETIQ" line; draw the speed curve live.
5. **SHOULD** Readability. makePages 3 words / 16 characters, CaptionTrack width 860 (every page at 88 px); credit 56 px; Bed 0.12 to 0.085.

**ONE MORE PASS**
