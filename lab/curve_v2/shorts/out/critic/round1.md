# Round 1 critic: SHORT1_v1.mp4 (27.2 s, 1080x1920)

Independent critic, 18 Oct 2026. Judged on the pixels, the measured audio and TESLA_ROADSTER_FACTS.md.

**Overall 7/10, ONE MORE PASS.** The narration is accurate, the audio is on spec, the loop is seamless and the drop is smooth. What holds it back: a cluttered, then dead, swipe window; a payoff that repeats the question; labels under the like button; a bar chart implying numbers we don't have; and Tesla's footage frozen for 14.8 s.

## Measured
- **Loudness:** -14.2 LUFS, true peak -1.4 dBTP. Music bed about 11 dB under the voice. Sound-effect peaks -3 to -5 dBFS.
- **Motion:** 0% frozen, 1% near-still. The footage area at 4.17-18.97 is a still (median frame difference 0.06).
- **Frames:** 0 duplicates in the drop. Frame 816 matches frame 0 (PSNR 41.4 dB).
- **"20× SLOWER":** source frames 6-11 over 4.13 s = 19.8×, so it's correct.
- **Beats (124 BPM):** the drop cut is 8 ms off the beat; the rewind at 24.47 is 197 ms off.

## Scores

| # | Area | Score | Problems (seconds) |
|---|---|---|---|
| 1 | Hook / frame 0 | 7 | Nothing shows which way is down, so the car reads as stuck sideways on a wall (0-3.8). Barely moves until 2.0. VACUUMED lands on AND NOT / FALLING? (2.03-2.23). Same screen 2.4-3.6 while the voice pauses (3.18-3.86). |
| 2 | Readability at 360 px | 7 | SKIRTS (x 775-1045) sits under the side buttons and on the 2× badge (13.4-14.9). Bar ends and MPH under the buttons (15.4-19.3). Credit about 9 px cap height, ITS WEIGHT about 12 px. Captions break after "THE" / "A" (10.5, 15.0, 22.6). |
| 3 | Motion | 7 | Graphics land on their words. Footage frozen 4.17-18.97. Muddy crossfades at 3.75-4.3, 14.83-14.97 and 19.0-19.3. |
| 4 | Variety | 7 | One split layout holds 15.5 s (57%). Car about 21% of the frame width at frame 0. Three crossfades: the banned "everything fading in" look. |
| 5 | Accuracy | 8 | Every narrated claim is in the facts file (§1, §2, §5). ✗ 100 MPH, and a WING bar at 55% of the "UP TO 2×" track, implies about 1.1× the car's weight from a wing at 100 mph: no source (15.35-19.3). |
| 6 | Sound | 8 | Rewind off the beat. The bed fades out over the last 0.4 s and in over the first 0.3 s: a dip at the loop. |
| 7 | Authorship | 6 | No point of view: six lines paraphrase Tesla, and the payoff repeats the hook (CRAFT §1, §9.8). Almost the whole of Tesla's best shot (19.3-24.5) with thin commentary (ZACK_D §12 rules 1, 2, 4). Credit leaves out "YouTube" (rule 5). |

## CRITIC_C_v2 items
- **FIXED:** 2, 4 (new: SKIRTS collision), 5, 6, 7 (the new payoff is weak), 8 (an audio dip remains), 9, 11, 12.
- **PARTLY:** 1 (no ground cue), 3 (the gap is now 3.18-3.86).
- **N/A:** 10.

## Five fixes
1. **2.0-3.9 s.** End the hook's exit by frame 58, before VACUUMED (frame 60). Cut the 3.25-3.70 s voice pause to 0.2 s and move every later cue 14 frames earlier.
2. **24.9-27.2 s.** Re-voice line 6 with the second-best fact: "Racing banned the same trick after the 1970 season, when the Chaparral 2J used fans to suck itself to the track." (§13.2, U11-U14.)
3. **13.4-19.3 s.** Nothing right of x 940 between 45% and 90% height. SKIRTS edge 1046 → 930; badge top 1128 → 1175 and text 64/46 px; bar track x1 1010 → 930; MPH margin 70 → 150.
4. **15.35-19.3 s.** Delete the "UP TO 2×" inside the bar so the bars read as shapes. Or count down from 50 MPH, Moravy's own figure (U28).
5. **4.17-18.97 s.** Play s1_hook_20x forward and back under the diagram, ending forward at frame 579. Keep the panel opaque before 3.77.

Also: move the rewind to frame 740, which is on the beat.

**Verdict: ONE MORE PASS.** Four fixes are code; one needs a re-voiced line. All fit before 18:00.
