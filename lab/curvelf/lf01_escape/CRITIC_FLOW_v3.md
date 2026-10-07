# CRITIC — LF01_FLOW_v3.mp4 ("The AI That Escaped"), third cut

Checked 7 Oct 2026. File: 1920x1080, 24 fps, 697.21 s (11:37), h264 2.9 Mb/s + AAC 48 kHz stereo 265 kb/s.
No project file was edited or deleted. Scratch frames, sheets and measurement files:
`/private/tmp/claude-501/-Users-daestigwood/275206fb-be3d-4593-9960-ef311d798e6a/scratchpad/qc_lf01_v3/`

**VERDICT: FIX THEN UPLOAD.** Picture: one visible layout defect (a 9 s card that runs into the header), a chapter
number that disagrees with the top-right indicator for about a second on every crossing, and a set of v1 items that
were not touched (caption plate cutting pictures, caption spelling, coral notes, jargon note). Sound: on target by
measurement, no clipping, but nobody has listened, the bed is still one 14.55 s loop for 11 minutes, and the ducking
swings the music about 10 dB between speech and gaps. Nothing on screen contradicts the narration.

What was looked at: 174 frames (30% and 80% point of all 87 lines, 22 contact sheets, all viewed); 160 frames at 0.2 s
across all ten chapter crossings plus 160 full-resolution crops of the top-right indicator at the same instants (all
viewed); 0.2–0.4 s strips of the opening (0–5.8), hours_00, sense_02, us_01, fallout_05, fallout_07, two type-beat
starts, open_07, the hop at 580 and the tail (684–697); a frame-by-frame strip at 183.4–183.8; per-frame luminance of
the picture area for the whole film; ffmpeg scene detection at 0.12; ebur128, volumedetect, astats per minute; 50 ms RMS
envelopes of mid, side, L and R of the mix and of `flow/garage.wav` and `flow/voice_dry.wav`.

Not done: nobody listened (every audio statement is a measurement). `LF01_FLOW_v3_phone.mp4` was not checked. Label
start times were strip-checked on 5 of the 10 labelled beats; the other 5 were confirmed present at their 30% frame
only. One hop (580) was strip-checked; hop softness elsewhere is not verified.

---

## A. The 16 fixes from CRITIC_FLOW_v1.md

Count: **4 FIXED, 8 PARTLY, 4 NOT FIXED.**

| # | v1 fix | Status | Evidence in this cut |
|---|---|---|---|
| 1 | Label timing: on with the line, no blink | **FIXED** | "11 JULY 2026" full at 1.9 (line starts 1.2), holds past 4.3. "11 – 13 JULY 2026" full 259.8, holds to 262.0, fades once with the hop at 262.2. "GLM 5.2 · Z.AI" 335.6–337.6, one fade at 337.8. "29 SEPTEMBER 2026 · SAN FRANCISCO" 594.3–607.8, no blink at 605–607. "OCTOBER 2026 · CALIFORNIA" 617.5–622.3. Arrival is ~0.5–0.6 s after line start, not 0.3 s. |
| 2 | Replace board_02 black picture | **FIXED** | 148.2–151.3 "THEY FOUND A WAY / TO TALK." in crisp type. (Frame is empty 147.58–148.1, see 5.) |
| 3 | Remove CAM readout and beat numbers | **FIXED** | Top right now reads "03 / 11  THE MESSAGE BOARD" on every sampled frame; no CAM text, no beat numbers. |
| 4 | Opening 0.0–5.5 | **PARTLY** | Frame 0 is no longer black (picture visible at 0.0, full by 0.4). Date label at 1.9. But k01 is still one of the dimmest pictures in the film, 0–1.2 s has no voice and no bright element, and the first frame that would stop a scroll is still "< 13 H" at ~13 s. |
| 5 | Empty frame at the start of type beats; us_01 attribution time | **PARTLY** | Empty stretch cut from 0.9–1.7 s to ~0.5–0.6 s, but it is still there on 23 beats, 12.4 s in total, each while a word is being spoken: 27.17, 67.67, 110.38, 147.58, 174.46, 211.25, 227.83, 248.58, 288.42, 327.67, 372.21, 384.71, 471.25, 518.17 (0.71 s, longest), 523.04, 568.00, 581.04, 608.62, 635.88, 647.88, 656.71, 665.79, 684.17. Quotes and lists finish typing at ~57–61% of the line (asked: 50%); why_02 "ONLY WHETHER" (427.2–431.8) and why_06 (454.1–459.9) reach full only as the line ends. us_01: quote and "OPENAI · 21 JULY 2026" complete ~373.5, camera leaves ~374.9 — about 1.4 s (asked 1.5). |
| 6 | Multi-line ASCII words unreadable | **FIXED** | All nine are now crisp white type with a cyan last line: 110.3, 174.4, 193.9, 248.6, 327.7, 523.0, 581.0, 608.6, 656.7. (174.4 has a new layout fault, see B1.) |
| 7 | Replace hours_06 picture; brighten s05, s29, k01 close | **PARTLY** | hours_06 302.4–310.7 is now "SOMEONE ELSE'S / COMPUTER"; the handgun picture is gone. s05 is unchanged and is the dimmest picture in the film (64.7–67.3, 243.3–248.3; picture-area luminance 22.2 against an empty-frame baseline of 19.7). s29 at 432.1–437.4 still cannot be identified. k01 close 673.5–683.9 still dim (23.1) and its figure is cut by a three-line caption. |
| 8 | Audio: bed through crossings, arrangement change, stereo bed, onsets | **PARTLY** | Crossings now sit at -24.2 to -25.9 dBFS in their last two seconds, all ten alike (were -30 to -34, two different). No arrangement change: the stem is the same loop for the whole film (envelope autocorrelation 0.95 at 14.55 s; sub-150 Hz and above-5 kHz energy identical to 0.1 dB in every minute). The music stem is still mono (L/R correlation 0.99); the mix adds width (see D). hours_02 onset at 270.71 is unchanged (silence to -18 dB inside 50 ms). |
| 9 | Ending 15–20 s with a sign-off | **PARTLY** | Tail is 11.0 s (last word 686.2, end 697.2). "THE CURVE / AI, EXPLAINED · SOURCES IN THE DESCRIPTION" is up 688.2–696.0. Matches the stated 11 s intent; shorter than the 15–20 s asked. No next-video prompt. |
| 10 | open_07: "700" shown while "twelve hundred" is said | **PARTLY** | "1,200" and "700" are both on from 45.3. "700" is larger and brighter and sits there from the start; "seven hundred" is not said until ~52. The disagreement is reduced, not removed. |
| 11 | Caption plate cutting pictures; four-line captions | **NOT FIXED** | Padlock base 90.4–97.1; 151.8–163.2 (three-line plate over the picture); 509.5–517.9; hourglass base 542.1–548.0; Capitol base 560.0–567.7; courthouse 593.7–608.3 (four-line plate over the lower third); 673.5–683.9. Four-line captions still at 227.8–243.0, 398.7–412.9, 593.7–608.3. |
| 12 | Minimum label size | **PARTLY** | Cap height is now ~18 px at 1080p (was ~14): "REPORTED BY REUTERS · DISPUTED BY OPENAI" 398.7–412.9, "29 SEPTEMBER 2026 · SAN FRANCISCO" 594.3–607.8, "EXPLOITGYM · LAUNCHED 11 MAY 2026" 83.9–90.1 (~20 px). Still shrunk onto one line, not broken onto two; the disclaimer is still the smallest label in the film. Date-only labels are ~40 px. |
| 13 | Caption consistency | **NOT FIXED** | "GPT 5.6 Sol" at 136.8–147.3 and 375.7–384.4, "GPT-5.6 Sol" at 174.4–184.2, "GPT 6.1 Astra" at 581.0–593.4; cards use the hyphen. "…broke into Hugging / Face." orphan at 1.4–5.5. |
| 14 | Soften fastest hops; last word over travel | **PARTLY** | 580.2: the quote now shrinks and fades in place (580.2–580.6) instead of whipping across; no motion blur anywhere. The leave still starts ~0.3–0.5 s before the line ends (607.8 against 608.33; 262.0 against 262.45). New: a one-frame lurch at 183.58–183.67 (see B4). Only one hop was strip-checked. |
| 15 | Tidy list | **NOT FIXED** | Chapter title still crosses the outgoing picture (127.3, 364.5, 413.9, 623.1) and now also ASCII numbers (316.9, 540.1). Coral notes still at 136.8–147.3 and 375.7–384.4, plus 44.9–54.1. "ONE DATASET POD → CLUSTER-ADMIN · SEVERAL CLUSTERS" still at 311.0–316.0. "SOL" card still labelled "GPT-5.6 SOL" 375.7–384.4. Pictures off the right edge at 338.4–346.5 and 366.5–371.9. Vertical bars at the left of the 398.7 picture. |
| 16 | Pacing (optional re-cut) | **NOT FIXED** | 567.97–608.33 is still three lines of 12.8, 12.4 and 14.6 s on single plates; 227.8–243.0 is still one 15.2 s list. |

---

## B. Fresh pass — new or remaining problems

### B1. Text overlap and clipping

- **board_05, 174.9–183.6 (about 9 s).** "CHEATING RATE: / HIGHEST OF ANY / PUBLIC MODEL / TESTED" is four lines of the
  largest type in the film. The block is too tall: its top line sits against the header row ("THE CURVE · THE AI THAT
  ESCAPED" and "03 / 11 THE MESSAGE BOARD"), and the cyan accent dash above it is pushed off the top of the frame for
  most of the beat (visible at 177.3, gone by 182.2). Worst layout fault in this cut.
- Chapter titles over other content, every crossing, 0.2–0.6 s each side:
  316.9–317.9 "MAKING NO SENSE" over then against the ASCII "< 13 H" (text on text; the digits touch the "M" at 317.7);
  540.1–540.7 "THE FALLOUT" over the ASCII "53"; 127.3–127.9 over the sandbox picture; 364.5–364.7; 413.9–414.5;
  623.1–623.5; and the incoming picture under the fading title at 64.1–64.3, 128.5–128.9, 203.7–203.9, 258.4–258.8,
  318.3–318.5, 365.9–366.1, 415.3–415.5, 482.6–482.8, 541.5–541.7, 624.5–624.7.
- Labels in a dark box on top of the picture: "19 JULY 2026" 356.8–363.9, "OCTOBER 2026 · CALIFORNIA" 617.5–622.3,
  "29 SEPTEMBER 2026 · SAN FRANCISCO" 594.3–607.8. Labels sitting directly on picture strokes without a box:
  "11 – 13 JULY 2026" 259.8–262.0, "21 JULY 2026" 367.1–371.7, "26 JUNE 2026 · A ZERO-DAY" 164.0–174.0.
- Nothing was found touching the caption plate as text-on-text. Closest: the note under "15–18,000" (489.8–499.3) and
  the "29 SEPTEMBER" label, each ~25–35 px above the plate.

### B2. Label or number that disagrees

- **Every chapter crossing.** The centre title "CHAPTER 0N" is on from about T-2.7 s; the top-right indicator does not
  change to "0N / 11" until about T-0.85 s. For roughly a second the two disagree: 62.9–63.7 (centre 02, corner 01),
  127.5–128.3, 202.5–203.3, 257.4–258.2, 317.1–317.9, 364.7–365.5, 414.1–414.9, 481.4–482.2, 540.3–541.1, 623.3–624.1.
- open_07 44.9–54.1: see A10.
- No on-screen date, number, quote or attribution contradicts the spoken line or `script.py`.

### B3. Empty frames during speech

See A5: 23 stretches of 0.4–0.7 s, 12.4 s in total. Also after a type beat that ends a chapter the frame is empty
before the title arrives: 201.9–202.1, 256.8–257.0, 480.8–481.0 (no speech there).

### B4. Camera

- No cuts. Scene detection at 0.12 gives one hit: 183.63 (score 0.147, higher than anything in v1). Frame by frame it
  is the camera starting its leave from the big "CHEATING RATE" card: the whole block steps down and shrinks between
  183.583 and 183.667. A lurch, not a cut.

### B5. Pictures that cannot be read or do not fit

- Cannot tell what it is: s03 22.3–26.9 ("It moved like an expert"); s07 83.4–90.1 (ExploitGym); s08 105.6–110.0
  ("brakes off"); s29 432.1–437.4; s33 509.5–517.9 (Medicare portal); s37 616.9–622.1 (subpoena) — which also looks
  like the same object as s31 at 460.2–466.4.
- hours_01, 262.7–270.4 ("a file uploaded like any other"): a hand pushing a bright bar into a slot. It can be read as
  a hand holding a weapon, the same problem v1 raised on the picture that was removed.
- Still dim: s05 (64.7–67.3, 243.3–248.3), k01 (1.2–5.5, 673.5–683.9), s38 625.1–627.7.
- Reuse unchanged: s05 twice, s04 at 54.4 and 640.9, k01 at open and close ("It was an AI" over a human silhouette).

### B6. Style rule not applied evenly

Short punch lines are meant to be ASCII and long ones crisp. ASCII: "IT WASN'T A PERSON." (41.0), "TRY. SCORE.
REPEAT." (78.1), "THE SCORE." (423.7), "REWARD HACKING" (437.7). Crisp, at the same length: "THEY FOUND A WAY TO
TALK." (148.2), "INCLUDING THE SANDBOX." (471.8), "SOMEONE ELSE'S COMPUTER" (303.0), "WHAT ARE WE REWARDING?"
(684.8). The split does not follow length.

Coral/red notes on three cards (44.9–54.1, 136.8–147.3, 375.7–384.4) against a cyan/white brief.

### B7. Small type

"AI, EXPLAINED · SOURCES IN THE DESCRIPTION" on the sign-off (688.2–696.0) and the timeline sub-labels at 518.9–522.7
("AN EMAIL TO A GENERIC INBOX") are ~12–14 px at 1080p. Split-card notes ("SHARED A HIDDEN MESSAGE BOARD") ~14 px.

### B8. Not found

No type on screen under one second (shortest complete hold: us_01 quote, ~1.4 s). No two captions at once on any
sampled frame. No frame-edge clipping of crisp type other than B1. No unreadable ASCII numbers or ASCII words.

---

## C. Chapter crossings (ten, sampled every 0.2 s from T-3.0 to T)

All ten behave the same: fade in over ~0.4 s, full brightness for 1.2–1.4 s, fade out over ~0.4 s, title set left of
centre with "CHAPTER 0N" above and an underline that draws across.

| Chapter | Title fully bright | Clean (nothing touching it) | Centre number | Corner indicator changes at |
|---|---|---|---|---|
| 02 THE TEST | 62.9–64.1 | 63.5–63.9 | 02 | 63.9 |
| 03 THE MESSAGE BOARD | 127.5–128.7 | 128.1–128.3 | 03 | 128.5 |
| 04 THE WEAKEST POINT | 202.5–203.7 | 202.5–203.3 | 04 | 203.5 |
| 05 THIRTEEN HOURS | 257.4–258.6 | 257.4–258.0 | 05 | 258.4 |
| 06 MAKING NO SENSE | 317.1–318.3 | 318.1 only | 06 | 318.1 |
| 07 IT WAS US | 364.7–365.9 | 365.3–365.7 | 07 | 365.7 |
| 08 WHY WOULD IT? | 414.1–415.3 | 414.7–414.9 | 08 | 415.1 |
| 09 WHAT ELSE THEY TOUCHED | 481.4–482.6 | 481.4–482.0 | 09 | 482.4 |
| 10 THE FALLOUT | 540.3–541.5 | 540.9–541.1 | 10 | 541.3 |
| 11 THE BOX | 623.3–624.5 | 623.9–624.1 | 11 | 624.3 |

- Readable for at least 1.2 s: yes on all ten, by the narrowest margin (1.2–1.4 s at 0.2 s sampling).
- The number in the centre is always the right one. It agrees with the corner indicator only for the last ~0.3–0.6 s
  of the title; before that the corner still shows the previous chapter (B2).
- The first chapter has no title; the corner reads "01 / 11 COLD OPEN" from 0.0.

---

## D. Audio (measured, not heard)

| Measure | v3 | v1 |
|---|---|---|
| Integrated loudness | -14.1 LUFS | -14.0 |
| Loudness range | 1.9 LU | 1.8 |
| True peak | -1.3 dBTP | -2.3 |
| Sample peak | -1.73 dBFS at 253.9 s; no flat-topped samples | -2.4 |
| Mean / max volume | -17.2 dB / -1.7 dB | -17.3 / -2.4 |
| L / R RMS | -17.3 / -17.2 dBFS | |

Per minute RMS (mix): -17.3 -17.1 -17.4 -17.1 -17.2 -17.4 -17.3 -17.1 -17.1 -16.9 -17.2, last partial minute -18.3.
Peaks per minute between -3.3 and -1.7 dBFS.

- **True peak** is 1 dB hotter than v1. -1.3 dBTP leaves 0.3 dB to the usual -1 dBTP ceiling before YouTube's own
  re-encode.
- **Voice** per line in the mix: median -16.9 dBFS, range -18.0 to -15.8. Flat.
- **Stereo.** Whole mix: side signal 21.7 dB below mid, L/R correlation ~0.99, because the voice is centred. In the
  music-only passages (crossings) mid is about -25 and side -31.2 dBFS, correlation about 0.6: the bed is audibly
  stereo there. Under speech the side signal is 24 dB below the mid. The music stem itself is still mono
  (correlation 0.992, side -45.6 against mid -21.8); the width comes from the mix.
- **Music under speech versus gaps.** Stem level is constant at -21.8 dBFS. In the mix: crossings -27 rising to about
  -25; the 0.3 s gaps between lines median -28.0 (range -37.6 to -25.3); under speech the side signal falls a further
  7 dB, which puts the bed at roughly -35 dBFS while someone is talking, about 18 dB under the voice. So the bed moves
  about 10 dB between speech and crossings and jumps up about 7 dB in each 0.3 s gap between lines. That is a pumping
  risk and the bed may be close to inaudible under speech on a phone. By ear before upload.
- **Monotony.** One 14.55 s loop about 47 times, no build, no drop, same in "why" and the close as everywhere else.
- **Start.** 0–1.2 s: -63 rising to -35 dBFS, then the voice. The first second is 10 dB quieter than any crossing.
- **Tail.** Last word ends 686.2. Bed comes up to -22 dBFS by 688.5, holds to 690.5, then drops about 9 dB inside half
  a second at 691.0 (-23.6 to -32.4; the stem itself drops there), sits at about -30 until 695, and fades to -65 by
  697.2. The final fade is clean. The 9 dB step at 691.0, six seconds before the end, should be checked by ear.
- **Onsets and ends.** hours_02 at 270.71 goes from digital silence to -18 dB in the first 50 ms: possible clipped
  onset, same as v1. No line has signal above -50 dB in its last 50 ms.

---

## E. VERDICT: FIX THEN UPLOAD

Picture is not upload-ready because of items 1–3. Sound passes every measurement but has not been heard, and item 4
needs ears. Items 1–4 are the blockers; 5–9 are worth doing in the same re-render; the rest are polish and can ship.

1. **board_05, 174.4–184.2.** Shrink or re-break "CHEATING RATE: HIGHEST OF ANY PUBLIC MODEL TESTED" (three lines, or
   a smaller size) so it clears the header row and keeps its accent dash; this also removes the lurch at 183.58–183.67.
2. **Chapter number.** Switch the top-right indicator when the centre title appears, not ~1.8 s later: 62.9, 127.5,
   202.5, 257.4, 317.1, 364.7, 414.1, 481.4, 540.3, 623.3.
3. **Chapter titles over other content.** Delay the title ~0.4 s or clear the outgoing plate first, at least where it
   lands on ASCII numbers: 316.9–317.9 and 540.1–540.7; then 127.3, 364.5, 413.9, 623.1.
4. **Listen once on a phone speaker.** Bed level under speech (measured ~18 dB under the voice), the 7 dB jump in each
   0.3 s gap, the 9 dB step at 691.0, the onset at 270.71. If the bed pumps, ease the duck depth or lengthen the release.
5. **Empty frames under speech**, 23 places, ~0.55 s each (list in A5; longest 518.17). Start the type-on as the camera
   lands. Let "ONLY WHETHER" (427.2–431.8) and the Goodhart quote (454.1–459.9) finish before the line does.
6. **Captions.** "GPT-5.6 Sol" at 136.8 and 375.7, "GPT-6.1 Astra" at 581.0; fix the "Hugging / Face." orphan at
   1.4–5.5; split the four-line captions at 227.8, 398.7, 593.7.
7. **Pictures cut by the caption plate**: 90.4, 151.8, 509.5, 542.1, 560.0, 593.7, 673.5. Place them higher.
8. **Pictures that cannot be read or can be misread**: hours_01 262.7–270.4 (reads as a weapon), s05 64.7 and 243.3,
   s03 22.3, s29 432.1, s33 509.5, s37 616.9 (same object as 460.2). Replace or brighten; a words card is acceptable.
9. **Colour and wording**: coral notes to cyan at 44.9–54.1, 136.8–147.3, 375.7–384.4; "POD / CLUSTER-ADMIN" to plain
   words at 311.0–316.0; the "SOL" card not to say "SOL" twice at 375.7.
10. **open_07, 44.9–54.1.** Bring "700" up (or brighten it) at ~51 s when it is said; until then "1,200" should lead.
11. **Small labels**: break "REPORTED BY REUTERS · DISPUTED BY OPENAI" (398.7) and "29 SEPTEMBER 2026 · SAN FRANCISCO"
    (594.3) onto two lines at the date-label size; lose the dark boxes at 356.8, 594.3, 617.5.
12. **Opening, 0.0–5.5.** Start the voice by ~0.5 s or put a bright element in the first second; brighten k01.
13. **Music.** One arrangement change (drums out for 415.9–480.2 or for 673.5–686.2). Bring true peak back under
    -2 dBTP.
14. **Tail.** If end-screen elements are wanted, 11 s works only if they sit clear of "WHAT ARE WE REWARDING?" and the
    sign-off; add a next-video line.
15. **Style rule**: decide ASCII or crisp for the 20–25 character punch lines (148.2, 303.0, 471.8, 684.8 against 41.0,
    78.1) and apply it one way.
16. **Pacing**, only if re-cutting: 567.97–608.33 and 227.8–243.0 still need a second visual each.

Still open from VERIFY.md section 6 and not part of this check: the WSJ source for both Wolf quotes, OpenAI's 26 Aug
report for the `weak` chain, the 1 Oct Washington Post report, "over a million models".
