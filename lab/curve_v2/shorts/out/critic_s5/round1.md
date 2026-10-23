# SHORT5_v1: critic round 1

32.3 s, -14.3 LUFS, -1.3 dBTP. Figures checked against the 8-K on sec.gov (filed 21 Oct).

## Scores

**1. Hook and frame 0: 6/10.** "-43%" reads at thumbnail size. But frame 0 is the inverted-ramp frame Short 1 opened on, still reading as "car on a wall" (18 Oct lesson). The car creeps from 0 to 4.2 s and flies at 4.3 s. "43%" is spoken at 5.3 s.

**2. Readability at 360 px: 6/10.** Captions and values pass. Three labels are 24-25 px caps against the 48 px minimum: "SBC = STOCK-BASED PAY" (19.5-21.8 s), the grey "(REGULATORY CREDITS...)" (22-26 s) and "THE HEADLINES / THE BILL" (27-31.6 s). The quote is 6 lines of jargon in 5.8 s. The footage chip runs under the right rail (x≈1000).

**3. Motion: 6/10.** Nothing freezes; a slow push runs under every hold. But the first 4 s are dead. Every diagram cut (6.3, 11.6, 16.0, 21.8 s) opens on empty frames, then fades the title up (banned). The credits scene gives 2.3 s to the static $417M bar and 0.9 s to the payoff ("-73%", 25.2-26.1 s).

**4. Variety and composition: 4/10.** From 6.3 to 26.1 s (61% of runtime), one template repeats four times: purple gradient, title top-left, chart in the top 40%, empty lower band. Gross profit's chart fills 24% of the frame, leaving 910-1320 px bare. Nothing carries across cuts. The end card reuses Short 2's opener.

**5. Accuracy: 7/10.** All four figures and "6 days" (15 to 21 Oct) are correct. Problems:
- **Misquote.** The filing reads "increase in operating expenses driven by SI..."; the screen adds "an".
- **SI is defined.** The deck says "Super Intelligence (SI)" on its highlights page, so the facts-file note is wrong. On screen SI goes unexplained, and the narration is circular ("research costs up... down to research projects").
- **"-43%" is GAAP.** Non-GAAP net income went 1,770 to 1,697 (-4%), on Tesla's highlights page. Unlabelled, the hook invites "misleading" comments.
- **Minor.** "Tesla said... 43%" should be "reported", since the 43% is our arithmetic. The narration drops SG&A. "A QUARTER'S REVENUE" beside "three quarters" can read as 25%.

**6. Sound: 7/10.** Loudness and peak are on target, the voice sits 8-10 LU over the bed, and the effects are clean. The bed pulses at 124 BPM; five of six cuts land 181-204 ms after the beat (one constant offset). The bed is cut at -19 dB RMS: a hard loop seam.

**7. Authorship: 5/10.** The verdict is authored. But the quote is retyped, the karaoke highlights land on "A/THE/HAD" (an auto-caption look), two earlier hero shots are reused and the scene grammar repeats. What would make it ours: the actual 8-K page, Tesla's phrase "Super Intelligence", one carried object (a "bill" printing line items), and our non-GAAP twist ("strip out stock pay and profit barely moved").

## Five highest-impact fixes

1. **Hook.** Line 1: "Tesla's net profit just fell 43%, six days after this flying Roadster". Frame 0 becomes the airborne thruster frame (5.2-5.8 s); start at the launch. Text: "NET PROFIT -43%" plus a small "GAAP".
2. **Quote.** Use a verbatim crop of the filing's Profitability bullet with marker sweeps. Add "SI = SUPER INTELLIGENCE (TESLA'S TERM)" at 48 px or larger. Narration: "...what Tesla calls Super Intelligence...". Fix the facts file.
3. **Fill 60-85% of the frame.** Make the bars 2-3x thicker across y≈350-1250 and add one full-frame number. Replace the fade-ups with carry-overs (the "-43%" pushes into the gross-profit chart).
4. **Captions from script words, not ASR tokens.** Fix "CAR | MAKERS" (23.3-23.9 s). No page ends on an auxiliary, possessive or bare adjective ("PROFIT HAD", "FROM TESLA'S", "SO THE FLYING"). Highlight only numbers and nouns.
5. **Sync and holds.** Apply `adelay=190|190` to the bed, or snap cuts to the 0.484 s grid. Finish the credits shrink by 24.5 s so "-73%" holds 1.5 s or more. Add a 150 ms bed fade at the tail.

## Verdict: ONE MORE PASS

Fixes 1, 2, 4 and 5 are text and timing changes that fit the ~60 h news window. Never ship the misquote, the reused frame 0 or the caption splits.
