# Round 2 critic: SHORT2_v2.mp4 (29.9 s)

Independent critic, 18 Oct 2026, 14:57 render. **7.6/10. SHIP.** The blockers are fixed; polish remains.

## Measured
- **Race:** both cars fit constant acceleration (residual ≤1.6 px). Distance ratio 0.503 (true 0.489), time ratio 0.501 (true 0.488): to scale within 3%.
- **Stopwatches:** 12.43-13.23 and 26.10-26.90, 24 frames each at 1.01× real time, stopping at 0.81 s.
- **Voice:** whisper hears "Rimac's Neverer"; "Navara" is gone.
- **Sound:** -14.6 LUFS, -1.4 dBTP. No loop dip (the tail holds -25 dBFS). Loop PSNR 41 dB. Footage is 22% of the runtime.
- **Beat (124 BPM):** cuts at 17.47 and 20.8 are on the beat; 6.07 (-235 ms), 12.30 (+190), 24.07 (-143) and 29.43 (-101) miss.

## Round 1
- **FIXED:** jets, Nevera, true scale, the stopwatch speed, "<0.81 s", loop dip, ATTACHED. (held 0.6 s), fades (now hard cuts), car size.
- **PARTLY:**
  - Payoff: the stopwatch is 330 px, not 700, and the lower half of 24.1-29.4 is empty.
  - The credit has no date.
  - No THE/A/IN breaks, but seven bad ones remain, e.g. OF A RIMAC / NEVERA R,
  - The Rimac still exits under the buttons (10.4-11.75).
  - The clip is still 0.76 of Tesla's 0.96 s.
  - Performance <1.6 s is shown but never said.
- **STILL PRESENT:** tags at 36-37 px and the 60 MPH flags at 26 px (house minimum 48).

## Scores
| # | Area | Score | Notes (s) |
|---|---|---|---|
| 1 | Hook / frame 0 | 8 | Car fills the frame, jets lit, answer in line 1 |
| 2 | Readability | 7 | Small tags; bad breaks; ROCKET (OFF-ROAD)<0.59 s touches (17.8-20.8) |
| 3 | Motion | 8 | 2-frame blank at 20.80; static 26.9-28.85 |
| 4 | Composition | 7 | ≈3.4 g and the ending leave half the frame empty |
| 5 | Accuracy | 8 | All numbers check; "quicker still" plays over two trims slower than 0.81 s, unexplained |
| 6 | Sound | 7 | Four cuts off the beat |
| 7 | Authorship | 8 | Own race, maths and verdict |

## Three fixes (code only; ship without them if they take more than an hour)
1. **17.5-20.8:** add a tag, ONLY THE OFF-ROAD ROCKET BEATS 0.81 s, and leave a 40 px gap after each label.
2. **Captions:** break at phrase ends, e.g. RIMAC NEVERA R, / ONE OF THE QUICKEST, and THE PRODUCTION CAR / WILL BE QUICKER STILL,
3. **24.1-28.8:** a 650 px stopwatch under 0.81 s, then shrink it onto the "s". Snap the cuts to 5.82, 12.11, 24.21 and 29.53.
