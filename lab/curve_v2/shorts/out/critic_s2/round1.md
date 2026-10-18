# Round 1 critic: SHORT2_v1.mp4 (29.9 s, 1080x1920)

Independent critic, 18 Oct 2026. Re-measured on this render (09:44); the older files in this folder predate it.

**Overall 6.5/10, ONE MORE PASS.** The numbers are right and the loop is seamless. But line 1 names jets that aren't visible, "Nevera" is voiced "Navara", the race doubles the gap and the payoff plays over an empty frame.

## Measured
- **Motion:** 1% frozen, 8% near-still. **Loop:** PSNR 41.3 dB.
- **3.4 g:** 26.82 ÷ 0.81 ÷ 9.81 = 3.38 g ✓. **8× SLOWER:** about 7.9× ✓.
- **Race:** the timers match the icons, and the lanes take 1.90 s and 3.87 s (ratio 2.04; true 2.05) ✓. But when the Roadster finishes (8.27), the Rimac is 24% along an equal-length lane. On one shared track it would be at 49% (5.3 m of 10.9 m).
- **"Nevera":** whisper medium hears "Navara". The stressed vowel's F2 is 950-1030 Hz, this voice's "stop" vowel, not its "e" (~1600 Hz).

## Scores

| # | Area | Score | Problems (s) |
|---|---|---|---|
| 1 | Hook / frame 0 | 6 | Frame 0 and line 1 are strong, but the jets are an orange smudge (x 900-1000, 0.4-1.8) and the plume (source frames 11-22) is never in the crop. |
| 2 | Readability, 360 px | 7 | The smallest text carries the argument: TESLA'S OWN TIMING at 33 px (8.5-11.9), DEWESOFT-VERIFIED at 35 px. Eight chunks end on THE/A/IN. ATTACHED. is up for one frame (28.90). The Rimac icon sits under the buttons (10.3-11.9). |
| 3 | Motion | 7 | Nothing new 24.0-28.3, under the payoff. Fades at 11.95, 16.9, 23.5 and 28.9. |
| 4 | Composition | 6 | The race cars are 16% of the frame width; half the frame is empty (6.1-11.9). 24.0-28.9 is a lone number on a purple vignette, the banned "title on a gradient". |
| 5 | Accuracy | 6 | "Navara" (8.2-8.7). The race gap is doubled (8.27). The stopwatch runs 1.4× fast (12.27-12.83). "< 0.81 s" (19.5) is given for "the production car", but Thrust claims under 0.9 s and Performance under 1.6 s (§3); only the off-road Rocket claims under 0.59 s. |
| 6 | Sound | 7 | -14.5 LUFS, -1.5 dBTP, bed 9-13 dB under the voice. A loop dip: the tail fades to -44 dBFS (29.45-29.90) and frame 0 opens at -51. Beat grid not measured. |
| 7 | Authorship | 6 | It has a verdict and its own graphics. But Tesla footage fills 46% of the runtime, including 0.76 s of the 0.96 s clip: the whole stunt (ZACK_D §12 rule 2). The credit has no YouTube or date and is missing at 17.3-24.0 (rule 5). The sharpest fact is absent: the Performance trim ($50,000 reservation) claims under 1.6 s, about a Rimac. |

**Repeated from Short 1:** credit, THE/A breaks, crossfades, loop dip, an icon under the buttons.

## Five fixes
1. **0.0-6.07, show the jets.** Anchor the crop on the rear axle so the nozzle glow (source frames 2-10) sits at x 700-1000 under GAS JETS FIRE (0.9-1.64). Then pan so the plume fills the right third.
2. **8.2-8.7, re-voice.** Use the (shown, said) tuple: "Rimac Nevera R" / "Ree-mack Neh-VAIR-uh R". Keep it only if whisper returns "Nevera".
3. **24.0-29.9, fill the payoff.** Put the stopwatch at about 700 px beside 0.81 s and sweep it in real time: 24 frames, linear (the same at 12.2). Slide it onto the number at "attached" (28.88) and hold ATTACHED. to 29.40. Hard-cut the seam and keep the bed at full level.
4. **6.07-11.95, true scale.** Keep the Rimac lane (x 170-932, which is 22.3 m). Put the Roadster's 60 mph flag at x 542 (10.9 m), and let the car run on past x 932, which it reaches at race time 1.24 s. Cars 300 px wide, tags at least 48 px, Rimac finish left of x 940.
5. **17.3-24.0, credit and context.** Put FOOTAGE: TESLA, YOUTUBE, 15 OCT 2026 on every Tesla shot. At 19.5, replace "< 0.81 s" with ROCKET <0.59 s (OFF-ROAD) · THRUST <0.9 s · PERFORMANCE <1.6 s.

Also: no chunk ends on THE/A/OF; cut instead of fading; log 3.4 g as [EST].

**Verdict: ONE MORE PASS.** Four fixes are code; one is a single TTS line.
