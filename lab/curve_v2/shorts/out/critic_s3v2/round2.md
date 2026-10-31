# Round 2 critic: SHORT3_v2.mp4 (18 Oct)

**7.7/10 (was 6.6). ONE MORE PASS, code only.**

## Round 1
- **Fix 1** PARTLY. The 2-6 HOURS block is clear, and TOP GEAR, FROM and HIS are fixed. Still split: IN ABOUT TWO / SECONDS. (14.2), OF COMPRESSED / GAS. (9.1), THE THRUST / VERSION GETS (16.7). Tank labels are 33 px.
- **Fix 2** FIXED: "estimate", 2:1 bars, hover line.
- **Fix 3** FIXED: hover frame 0, loop 41.5 dB, car left of 956 px, dated credit.
- **Fix 4** PARTLY. Six cuts are within 31 ms of the beat, but 25.17-26.37 is still an empty frame.
- **Fix 5** FIXED (28.97).
- "Maps", collisions and the verdict are FIXED.
- STILL PRESENT:
  - text cards from 15.5 to 31.0
  - the missing 5 s and 30-minute figures
  - TOLD TOP GEAR. flashes for 3 frames (30.87), then plays uncaptioned under a rewind effect about 5 dB down

## New
- **15.43:** the empty tanks and red 2.0 s get 2 frames before the cut. The answer never lands.
- **0-5.83:** 36% duplicate frames (v1: 1%) from the 6× RIFE clip at 0.6×, the 18 Oct stutter.
- **25.17:** a stale TAKES HOURS. sits under MUSK, ON STAGE.
- **31.33-31.93:** "10× SLOWER" runs over a 1.7× rewind.
- `short3.py` r3 still reads "maths".

## Accuracy
Every number matches §4, §5, S1 and P1. The 10× label checks out: 14 source frames fill 5.83 s.

**UNPROVEN is fair.** The file tags the claim CONFLICT, §13.6 finds nothing new, nothing was shown, and §5 puts a refill at 38 kWh or more. The stamp rates the evidence without saying false.

Nits: the timer ends at 2.0 (250 ÷ 130 = 1.9); the credit says 15 OCT, the description 16 Oct.

## Scores
| Area | Score | Problems (s) |
|---|---|---|
| Hook | 8 | Stutter 0-5.8 |
| Readability | 7 | Splits; 31 px formula (10.8) |
| Motion | 7 | Payoff 15.43; empty 25.17 |
| Composition | 7 | Text only 15.5-31.0 |
| Accuracy | 9 | Nits |
| Sound | 8 | -14.3 LUFS, -1.5 dBTP; rewind at 30.97 |
| Authorship | 8 | Own x-ray, estimate, stamp; footage 21% |

## Fixes
1. **Drain:** start at 13.07, on the beat. The red 2.0 s then lands at 15.07 and holds 0.43 s.
2. **Hook:** run RIFE at 10× (`-n 175`), play at 1.0× and rebuild the reverse.
3. **Captions:**
   - Split IN ABOUT / TWO SECONDS.
   - Drop the stale TAKES HOURS.
   - Bring in THE CAR REFILLS ITSELF at 25.67.

**ONE MORE PASS.** Then frame-check 0-6, 15-15.6 and 25-26.5.
