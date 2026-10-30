# Critic round 2: Short 13 v2

**ONE MORE PASS.** Round-1 MUSTs mostly landed; the new dial layout collides, verdict rows overflow, four labels miss the 1.4 s hold.

## Round-1 items (v2 timestamps)
- MUST 1 stamp left 60: PARTLY. Rests clean at x 66-466 (10.97-11.13 s); runs to x 0-25 on entry (10.50-10.57 s), wobbles 0.7x-1.2x, up only 0.67 s.
- MUST 1 two-line ADVANCED / BOLTER tags, Tag damping 20: FIXED (6% overshoot).
- MUST 1 button strip and right edge: PARTLY. Strip clear in all 1051 frames; verdict rows break the right edge (MUST 2).
- MUST 2 dial: PARTLY. ABOUT, 2 S, TYPICAL LANDING are in but collide (MUST 1); needle hits 0 at 6.2 s while the band's jet still rolls; kicker and voice say "two seconds" without "about".
- MUST 2 A STEEL WIRE: FIXED (25.2-34.0 s).
- SHOULD 3 re-cut head clip, trim x2: STILL PRESENT. Crewman in frame 0; jet about 2% of frame; x2 runs 6.5-11.2 s; band frozen 10.73-11.13 s.
- SHOULD 4 loop the catch: FIXED (30-34 s motion 0.23-0.37, was 0.12). 1.6x cross-section, one camera, SOURCE line, live curve: STILL PRESENT.
- SHOULD 5 credit 56 px, bed 0.085: FIXED (bed 14 dB under voice). Caption size lock: STILL PRESENT (6 pages 40-50 px vs 63: 8.5-9.5, 13.5-15.5, 18-18.5, 26.5-28 s).

## Scores
1. **Hook 6/10**: frame 0 unchanged (crewman, small jet); "TYPICAL LANDING" sits 11 px under "MPH".
2. **Readability 6/10**: tags and credit better; dial collision and small captions offset it.
3. **Motion 7/10**: no frozen stretch; kicker static 0-6.3 s; 30-34 s light.
4. **Variety 4/10**: one deck cross-section serves 3 of 6 scenes.
5. **Accuracy 8/10**: typical landing, ABOUT, A STEEL WIRE; description matches facts, DoD line present.
6. **Sound 8/10**: -14.2 LUFS, TP -1.5; six cuts 0-20 ms after kicks; rewind 169 ms late.
7. **Authorship 5/10**: take shown and spoken; structure still the S10-S12 template.

## MUST
1. **Dial collision, 3.83-6.30 s.** "TYPICAL LANDING" (x 61-608) runs into "ABOUT 2 S" (x 602-908). Move ABOUT/150/MPH to left 650, lift the block 60 px, put "ABOUT 2 S" at left 60 under the label.
2. **Verdict rows.** `pop(..., 230, 12)` overshoots 26%: "A CONTROLLED CRASH" is cut at x 1079 (reads "CRAS") 26.50-26.67 s; "BELOW THE DECK" reaches x 1047 at 27.87 s. Use damping 24.
3. **Labels under 1.4 s:** stamp 0.67 s, BOLTER GO AROUND 0.75 s, HEAVY JET 0.73 s, Mech BELOW DECK 1.1 s. Render the stamp outside `First` with `until={T.oct+48}`, damping 18, start scale 1.3, origin left; start the tags at `T.misses+8`, `T.tune`, `T.below-12`.
4. **Upload entry 8** `file` still points to SHORT13_v1.mp4; re-point it to the shipped render.

## SHOULD
Caption width 860, 3 words / 16 characters; head clip re-prep, trim x2; stern clip x1.6; rewind +5 frames onto a kick; credit and date 68-72 px; "about" before "two seconds"; "stealth" and "single wire" are not in the facts file.
