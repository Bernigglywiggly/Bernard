# Critic round 3: Short 13 v3 (35.03 s, 1051 frames)

**ONE MORE PASS, but no re-render.** The video has no MUST left; one round-2 MUST is still open, in the upload manifest.

## Round-2 items
- MUST 1 dial collision: FIXED. 3.83-6.30 s, label ends x 608, ABOUT/150/MPH start x 650, "ABOUT 2 S" beneath.
- MUST 2 verdict rows: FIXED. "A CONTROLLED CRASH" peaks x 967, settles 957 (26.4-26.8 s); no text at x 1066+ in any frame.
- MUST 3 label holds: FIXED. Stamp 1.40 s (9.73), BELOW DECK 1.37 (14.60), BOLTER 1.37 (23.80), HEAVY JET 1.33 (19.47).
- MUST 4 manifest entry 8: STILL PRESENT. channel/uploads_curve.json line 224 is still SHORT13_v1.mp4.
- Stamp at x 60, two-line tags, button strip, A STEEL WIRE, catch loop, bed 0.085: FIXED. Strip, bottom 20% and edges clear in all 1051 frames.
- Dial vs footage: PARTLY. Needle hits 0 at 6.23 s; jet still rolling at 6.15 s.
- "About" before "two seconds": PARTLY. Dial says ABOUT 2 S; voice (5.3-6.5 s), kicker and caption do not.
- Head clip re-cut, trim x2: STILL PRESENT. 0.00 s crewman at left, jet 350x125 px (2%); x2 runs 6.30-11.13 s.
- Stern clip x1.6: STILL PRESENT. Band frozen 10.70-11.13 s (clip 133 frames, scene 145).
- Rewind onto a kick: STILL PRESENT. 34.03 s, 162 ms after the 33.87 s kick.
- Caption size lock: STILL PRESENT. Six pages at cap height 37-44 px vs 63 (8.5-9.9, 13.4-15.6, 17.6-18.9, 22.6-23.7, 26.2-27.4 s).
- Credit and date 68-72 px: STILL PRESENT (56, 64).
- "Stealth", "single wire" not in facts: STILL PRESENT (6.72 s; 3.84-4.63 s).
- 1.6x cross-section, SOURCE line, live curve: STILL PRESENT. One deck drawing serves 11.1-16.0, 20.8-25.2, 25.2-34.0 s.

## Scores
- Hook, frame 0: 6. 0.00 s: red-vest crewman is the loudest object, jet small, lower 30% empty; kicker static to 3.8 s; 6.3-11.1 s only describes the clip.
- Readability at 360 px: 7. Strip, bottom 20% and edges clear; HEAVY JET touches x 951 (20.5-20.8 s); six caption pages under 48 px cap height.
- Motion: 7. Longest still run 0.43 s (10.70 s); 29.3-34.0 s moves only via the mini replay.
- Composition: 5. Drawing scenes light 6-10% of the frame (11.1-25.2 s); jet 404 px wide; stamp touches "FORD CLASS" (9.7-11.1 s).
- Accuracy: 8. Numbers, names, tags and voice match the facts; DoD line present. "IDLE" (20.8-25.2 s) and "for each jet" (19.2-20.7 s) exceed rows 3 and 6.
- Sound: 8. -14.2 LUFS, TP -1.5 dBFS, LRA 1.3, no gaps; six cuts within 10 ms of kicks.
- Authorship: 5. Take spoken and shown, but S10-S12 structure and no on-screen source.
- Loop: 9. Last frame against frame 0: 42.75 dB; kicker eased to scale 1; rewind sound off-beat.

## MUST
1. **Manifest ships the wrong file.** channel/uploads_curve.json line 224: change `../lab/curve_v2/shorts/out/SHORT13_v1.mp4` to `../lab/curve_v2/shorts/out/SHORT13_v3.mp4` (or the final render). v1 has clipped tags and the unqualified dial.

## SHOULD, cheapest first
- prep/s13_clips.sh: `mk s13_stern trap_side.mp4 246 92 1.6`.
- CurveV2Short13.tsx line 32: `+ 30 + LOOP` to `+ 25 + LOOP` (rewind on kick 70).
- Stamp13 `top={1292} rot={-2}`; HEAVY JET `left={560}`.
- CaptionTrack `width={860} maxSize={72}`; re-break the three pages over 22 characters.
- Voice and kicker say "about two seconds".
- Re-prep s13_head from source frame ~186 at real speed, crewman out; trim x2 to one sentence.
- Source or cut "stealth", "single", "IDLE"; "for a broad range of jets".
- Next Short: new shape, 1.6x cross-section, a QINETIQ source line.
