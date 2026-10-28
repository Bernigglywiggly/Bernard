# Short 10 critic, round 1 (SHORT10_v1.mp4, 30.87 s)
Evidence: `critic_s10/r1_*`. Verdict: ONE MORE PASS.

**1. Hook + frame 0: 6/10.** Frame 0 is a good thumbnail (168 px, light and dark feeds). But the voice starts at 0.1 s and the first caption appears at 2.93 s (frame 88): "SpaceX now makes more money from AI" is never shown. 0.3-1.9 s is the stillest stretch; the title fades out at 1.9 s. The 7.56 vs 7.02 gap (7%) is one unlabelled combined bar; rockets' 1.77 sliver never reads.

**2. Readability: 6/10.** Captions auto-shrink per line: 36 px cap (12 px at 360 w) on 4-5-word pages, 60 px on "SEVEN AND A HALF". Stickers and small labels: 28-31 px (9-10 px at 360). Contrast fine. "SPENT ON KI" is clipped by the bar (28.0-29.87). Credit plate (y 1483-1514) sits in the bottom 25%.

**3. Motion: 6/10.** Studio metric passes. Empty frame 24.20-25.10 (caption only); dark scenes never push (8.3-9.0 dead). Holds under 1.4 s: SPACE SEGMENT sticker 14.2-15.0 (0.8 s); CAPITAL SPENDING 28.4-29.87 (about 1.1 s settled). Two 2.4 s gaps, captions only (9.2-11.6, 19.0-21.4).

**4. Variety: 5/10.** Dark chart cards fill 62% of runtime; 15.0-29.9 has no photograph. One layout four times (kicker top-left, chart in top half, bottom 40% empty); three pies in a row (32-46% of width vs the 60-85% rule); no carried object. AI and Starlink never appear. 4.8-9.2 re-shows $7.56B. Footage 2 (9.2-15.0) is soft. The verdict's proof chart is the smallest text on screen.

**5. Accuracy: 8/10.** Every number matches §0; no §9 breach. Mismatches: (a) capex sticker says "SEC 10-Q", but §0h sources it to E1a (8-K); (b) "45¢ PROFIT" omits "OPERATING"; (c) VO "makes more money" is revenue (facts H1: "brings in"), REVENUE tag only from 2.6 s; (d) VO "seven and a half" vs $7.56B; (e) "LOST $7M" is operating, unlabelled (description too); (f) "9×" includes Cursor's $608M; (g) credit omits footage date (Oct 2024). Description matches; credit URL verified.

**6. Sound: 7/10.** -14.4 LUFS, -1.5 dBTP, LRA 1.3: compliant; voice about 10 dB over a steady bed. VO about 190 wpm, no pause over 0.6 s. SFX sparse: ticks at 5.0, 13.9 (late vs the stamp), 15.05, 24.2; none at the other cuts.

**7. Authorship: 4/10.** Same skeleton as the Tesla net-profit Short (two-bar Q3 vs Q3, vignette, OUR MATHS stickers) and the same "headlines vs bets" verdict; the script's coin, dish and real 10-Q were dropped. Loop: last vs first frame PSNR 11 dB (good: 41).

## Five fixes
1. **Captions (bug).** Rebuild pages from VO word times: first page at frame 3, three words max, one fixed cap height of 54 px or more, phrase-end breaks ("BRING IN / ABOUT TWELVE CENTS"). Assert first caption frame is 9 or less.
2. **Hook, 0-4.8 s.** Title shrinks to a 2-line kicker (no fade); footage push 1.00 to 1.10 from frame 0. Three labelled bars (AI 856 px, STARLINK 596, ROCKETS 200), REVENUE tag on the first bar frame; Starlink and Rockets then slide end to end under AI (7.02 < 7.56). Fold $0.81B in as a ghost mark; cut 4.8-9.2 to about 2 s.
3. **Defects.** Verdict chart: 330 px label column, "CAPITAL SPENDING", "SEC 8-K". "45¢ OPERATING PROFIT"; "LOST $7M · OPERATING". Stickers 40 px cap or more, in 1.5 s before scene end (SPACE SEGMENT at 13.6, scene ends 15.2). "ROCKETS → HEADLINES" in at frame 727 (no empty frame). 3-4% push on dark scenes.
4. **Evidence, 15.0-29.9.** Real 10-Q crop at 90% width, highlighter on "34.5%"; Starlink dish (SpaceX clip with credit, or our labelled render) behind a pie 756 px or wider; verdict as three full-width slabs with pictures, capex bar at 85% width held 2.5 s. Re-crop footage 2 from the best source.
5. **Make it ours.** One persistent `<Coin>` (12/88, 34.5%, 45/55) scaling through the camera between scenes, replacing the pies; give the verdict its own visual, not the Tesla card. Last frame = frame 0 (same grade, title slams in), PSNR 35 dB or more.

**ONE MORE PASS**
