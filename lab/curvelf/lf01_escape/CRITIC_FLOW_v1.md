# CRITIC — LF01_FLOW_v1.mp4 ("The AI That Escaped")

Checked 7 Oct 2026. File: 1920x1080, 24 fps, 689.21 s (11:29), h264 + AAC 48 kHz stereo.
No project file was edited. Scratch frames and sheets: `/private/tmp/claude-501/-Users-daestigwood/275206fb-be3d-4593-9960-ef311d798e6a/scratchpad/qc_lf01/`

**VERDICT: FIX THEN UPLOAD.** The single-camera world works, there are no cuts, loudness is on target and no on-screen
text contradicts the corrected script. But there is one real render bug (picture labels arrive late and blink off
mid-line), one 3.5 s black hole under speech, a debug camera readout burned into every frame, and a weak first three
seconds. All are re-render fixes, none need new narration.

What was looked at: 87 frames (75% point of every line, 11 contact sheets, all viewed); 0.2 s strips across 4 chapter
crossings (test, board, us, box) and 6 hops (40.5, 82.3, 261.6, 470.2, 579.6, 607.4); 11 further strips for label
timing, type-on timing, the opening and the ending; a full-film 320x180 grayscale decode for per-frame brightness and
frame-difference; ffmpeg scene detection at 0.2 and 0.08; blackdetect; ebur128; volumedetect; the three audio stems in
`flow/` against the final mix; `lines.json` word lists against script text.

Not done: nobody listened. Every audio statement below is a measurement, not a hearing. Items marked "by ear" need a
human listen.

---

## 1. PICTURE BUGS

### 1.1 Picture labels arrive late and blink off before the beat ends (render bug)

Labels on `img`/`clip` beats appear 0.9–2.2 s after the line starts, and on four beats they fade out mid-line and pop
back for the last ~0.3 s as the camera leaves.

| Line | Label | Line span | Label visible | Problem |
|---|---|---|---|---|
| open_00 | 11 JULY 2026 | 1.20–5.53 | 3.42–5.25 | Appears as the narrator finishes saying the date. 2.2 s late. First 3.4 s of the film has no bright element. |
| hours_00 | 11 – 13 JULY 2026 | 259.17–262.45 | 260.1–261.3, then 262.0–262.2 | Off at 261.6, back at 262.0 (blink). On screen 1.4 s in total. |
| sense_02 | GLM 5.2 · Z.AI | 335.01–338.12 | 336.0–337.0, then 337.7–337.9 | Off at 337.4, back at 337.8 (blink). The only place the model is named; on screen ~1.2 s. |
| us_00 | 21 JULY 2026 | 366.54–371.89 | 367.5–370.1, then 371.4–371.6 | Fading at 370.2, gone at 370.8, back at 371.4 (blink). |
| fallout_05 | 29 SEPTEMBER 2026 · SAN FRANCISCO | 593.72–608.33 | ~594.6–603.6, then 607.8–608.2 | Fading at 605.0, gone at 606.4, back at 607.8 (blink). |
| board_06 | 4 JULY 2026 | 184.47–193.56 | from 186.5 | 2.0 s late, no blink. |
| sense_03 | 16 JULY 2026 | 338.42–346.53 | from 340.3 | 1.9 s late. |
| sense_05 | 19 JULY 2026 | 354.62–363.54 | from 356.8 | 2.2 s late. |
| fallout_00 | 18 AUGUST 2026 | 542.05–547.97 | from 543.5 | 1.5 s late. |
| fallout_07 | OCTOBER 2026 · CALIFORNIA | 616.92–622.05 | ~618.0–621.5 | Gone by 622.0, before the line ends. |

Labels that held steady once on: test_03, board_04, us_05, why_05, else_03 (strips viewed). The blink is the same
pattern each time (fade out, return ~0.4 s before the hop), so it looks like one timing rule, not four accidents.

### 1.2 Near-black frames while someone is speaking

- **board_02, 147.6–151.3 (3.5 s).** "Each agent was supposed to be on its own. They found a way to talk." The picture
  (s11) is a single hair-thin dim line between two specks; mean luminance 4.9/255, 0.36% of pixels lit. ffmpeg
  blackdetect flags 148.13–150.33 as black. This is the worst frame in the film and it sits on a story turn.
- Every crisp-type beat (quote, list, timeline) opens with 0.9–1.7 s of empty frame (thread and HUD only) while the
  narrator is already talking, because the hop lands on an empty plate and the type then types on:
  34.1–35.5 (open_05), 67.5–68.5 (test_01), 211.2–212.5 (weak_01), 227.8–228.8 (weak_04), 288.3–289.7 (hours_04),
  346.6–348.0 (sense_04), 372.2–373.4 (us_01), 384.5–385.9 (us_03, blackdetect 385.04–385.79), 427.1–428.2 (why_02),
  518.2–519.8 (else_04, blackdetect 518.38–519.67), 568.1–569.4 (fallout_03), 628.1–629.4 (box_01),
  635.4–637.1 (box_02, blackdetect 636.13–637.04), 647.8–648.9 (box_04). Fourteen times.
- Frame 0 is pure black; the picture fades up over the first ~1 s.

### 1.3 Type that is on screen too briefly

- **us_01, 372.19–375.41**: quote "an unprecedented cyber incident" finishes typing ~374.4; attribution
  "OPENAI · 21 JULY 2026" finishes ~374.7; camera leaves at 375.1. The attribution is fully on screen for about 0.4 s.
- Type-on is slow against the speech everywhere: the list or quote reaches half its text 2–6 s after the line starts
  (weak_04: half at +6.0 s, full at +8.9 s of a 15.2 s line; hours_02: full at +9.4 s; fallout_03: full at +10.2 s of
  12.8 s). All crisp type is removed ~0.35 s before the line ends as the camera leaves.
- hours_00 and sense_02 labels (see 1.1): about 1.2–1.4 s total.

### 1.4 ASCII words too dim or thin to read

Big numbers and one- or two-word lines read well. Two- and three-line phrases do not: the first line is set smaller,
so its strokes are one character wide and it reads as grey texture.

- board_05, 174.4–184.2: "CHEATING RATE: HIGHEST / OF ANY PUBLIC MODEL / TESTED" — three lines, the top two are barely legible. Worst case.
- else_05, 523.0–530.0: "BELIEVED TO BE THE FIRST / AI HACK OF A GOVERNMENT" — both lines thin.
- sense_01, 327.7–334.7: "THE AI DECLINED TO / ANALYSE THE ATTACK" — both lines thin.
- First line weak, second fine: test_07 110.3–117.1 ("SAFEGUARDS OFF," with the comma hanging low), board_07 193.9–201.3,
  weak_06 248.6–256.2, fallout_04 581.0–593.4, fallout_06 608.6–616.6, box_05 656.7–665.5.

### 1.5 ASCII pictures too dim or unreadable

- test_00 64.7–67.3 and weak_05 243.3–248.3 (both s05): mean luminance 6.5; a faint shape, not identifiable.
- open_00 1.2–5.5 and open_01 5.8–12.5: luminance 8.4 and 8.9. The opening 12 s is among the dimmest in the film.
- box_07 673.5–683.9 (k01 again): luminance 6.8 for 10 s. The mirrored close is the second-dimmest long beat.
- why_03 432.1–437.4 (s29): cannot tell what the object is.
- why_07 460.2–466.4 (s31): ambiguous (a card or paper under a lens).

### 1.6 Pictures cut by the caption plate or the frame

The caption plate is solid and hides whatever is under it, so tall pictures end in a hard horizontal line:
test_04 padlock (90.4–97.1), test_06 (105.6–110.0), board_03 (151.8–163.2), hours_00 (259.2–262.5), else_03
(509.5–517.9), fallout_00 hourglass base (542.1–548.0), fallout_02 Capitol base (560.0–567.7), fallout_05 courthouse
(593.7–608.3, four-line plate covers the lower third), box_07 (673.5–683.9).

Pictures running off the right frame edge because the camera frames label-plus-picture off-centre: board_04 key
(163.5–174.1), hours_00 (259.2–262.5), sense_03 (338.4–346.5), us_00 right-hand figure (366.5–371.9).

### 1.7 Hard picture edges

- hours_06 302.4–310.7: straight vertical column of characters down the left side of the picture.
- weak_02 217.8–222.5: straight left boundary to the shaded area.
- us_05 398.7–412.9: vertical bars at the picture's left edge.
Mild in each case; soft vignette on the rest.

### 1.8 Text over text / text over picture

- Chapter titles fade in over the outgoing picture and fade out over the incoming one for ~0.3–0.4 s each:
  62.6 and 64.4 (THE TEST), 127.2–127.4 and 129.0 (THE MESSAGE BOARD — the title crosses the sandbox picture),
  364.4–364.6 and 366.2 (IT WAS US), 622.9–623.1 and 624.7 (THE BOX). Title fully clear for about 1.6 s.
- At 364.0 the fading "19 JULY 2026" label and the incoming chapter title are within 0.4 s of each other.
- Labels sit on top of the picture with a dark box: sense_05 "19 JULY 2026" (356.8–363.8), fallout_07
  (618–621.5), us_00, fallout_05. Readable, but boxed type over ASCII breaks the "one world" look.
- us_05: "REPORTED BY REUTERS · DISPUTED BY OPENAI" runs right up to the picture's edge.

### 1.9 Small type

Long labels are shrunk to fit and end up ~14 px cap height at 1080p: "EXPLOITGYM · LAUNCHED 11 MAY 2026" (test_03),
"REPORTED BY REUTERS · DISPUTED BY OPENAI" (us_05 — this is the disclaimer, and it is the smallest type in the film),
"29 SEPTEMBER 2026 · SAN FRANCISCO" (fallout_05). Unreadable on a phone. The `LF01_FLOW_v1_phone.mp4` was not checked.

### 1.10 Debug overlay

Every frame carries "CAM +005597 -00235 x0.81" top right (camera position and zoom, changing every frame), plus tiny
beat numbers ("07", "55", "79") beside the thread node. If the CAM readout is intended as set dressing, say so; it
reads as a debug HUD left on. The beat numbers are 6–8 px specks.

The thread node and its glow sit on or above the top frame edge on many beats and are cut by it (e.g. 10.9, 25.7,
124.1, 337.4).

---

## 2. CAMERA

- **Cuts: none.** Scene detection at 0.2 finds 0; at 0.08 finds one hit, 580.17 (score 0.087), which is a hop. Largest
  frame-to-frame difference anywhere is 17.2/255 (580.25). The 0.2 s strips show continuous travel on all ten
  transitions checked.
- **Hops.** Each lasts about 0.8–1.0 s, pulls back to ~x0.5 and pushes in again. There is no motion blur, so each frame
  of the travel is sharp. The hops that carry big bright type across the frame are the ones that read as whips:
  580.2 (quote → ASTRA, the fastest in the film), 608.0, 41.3, 82.9, 471.6, 470.6, 262.2, 559.5.
  The hop starts ~0.3–0.4 s before the line ends (e.g. at 40.5 the quote is already shrinking while "can sell" is
  still being said), so the last words of most lines play over travel.
- **Chapter crossings** (61.7–64.7, 126.3–129.3, 363.5–366.5, 622.0–625.0): smooth, zoom to ~x0.42, title centred.
  Before each one the camera holds almost still for ~0.6–0.8 s (126.4–127.0: CAM moves 4 units).
- **Stills.** No stretch of 2 s or more with a static frame. Inside beats the camera drifts ~10 units/s with a slow
  zoom change (us_05: x0.81 → x0.73 over 13 s). It is not frozen, but on the 12–15 s beats (weak_04, us_05,
  fallout_03, fallout_05) it is close to a slow Ken Burns on one plate.

---

## 3. CAPTIONS

- **Two at once: not seen.** At every boundary sampled the outgoing caption fades before the incoming one appears
  (34.3/34.6, 40.9, 83.3, 262.6, 471.2, 580.8/581.0, 608.4/608.6, all four crossings). Not every one of the 86
  boundaries was sampled.
- **Against narration.** Script text versus the word list in `lines.json`: differences are numerals, US spellings and
  names only ("eleventh"/"11th", "analyse"/"analyze", "Hobbhahn"/"hobhan"). Four to check by ear, where the aligner
  heard something else: test_04 ~90.4 "Give an" heard as "given"; board_05 ~176 "that" heard as "the"; else_02 ~506
  "use" heard as "used"; board_04 and hours_01 "flaw(s)" heard as "floor(s)" (expected in a British read).
- **METR**: caption shows "METR" at 174.4–184.2, said "Meter". As expected.
- **Inconsistent model names.** Captions show "GPT 5.6 Sol" at board_01 (136.8–147.3) and us_02 (375.7–384.4) but
  "GPT-5.6 Sol" at board_05 (174.4–184.2); "GPT 6.1 Astra" at fallout_04 (581.0–593.4). On-screen cards use the
  hyphen every time ("GPT-5.6 SOL", "GPT-6.1 ASTRA:").
- **Layout.** Line 0 breaks as "…broke into Hugging / Face." with a one-word orphan (1.2–5.5). Plate height jumps
  between one and four lines; four-line blocks at weak_04 (227.8–243.1), us_05 (398.7–412.9), fallout_05
  (593.7–608.3) put ~45 words of small type on screen at once.

---

## 4. CONTENT MISMATCH

No on-screen number, date, quote or attribution contradicts the corrected script. Checked specifically against
VERIFY section 3: open_05 carries "AS REPORTED"; us_01 shows "an unprecedented cyber incident"; hours_05 shows
"ATTACKER ACTIONS · 9–13 JULY"; us_04 shows "8"; fallout_03 shows "OPENAI · 17 SEPTEMBER 2026"; else_05 has no
quotation marks; hours_04 has the ellipsis; else_01 shows "15–18,000 … 11 MAY – 22 JUNE".

Picture does not fit the words:

- **hours_06, 302.4–310.7** — "they launched it from someone else's computer: an unsecured public endpoint". The
  picture (s21) reads as a hand holding a pistol. Wrong object, and wrong register for this film.
- **open_07, 44.9–54.1** — "700" fills the frame from the start, but the narrator says "twelve hundred" first and does
  not reach "seven hundred" until ~51 s. For about 5 s the big number disagrees with the number being spoken.
- **us_02, 375.7–384.4** — big "SOL" with the note "GPT-5.6 SOL" under it: the card says the same thing twice.
- **hours_07, 311.0–316.0** — note says "ONE DATASET POD → CLUSTER-ADMIN"; the narrator says "dataset machine …
  administrator". open_02 used the plain wording for the same fact.
- **board_01 and us_02** — the right-hand note is coral/red. Everything else in the film is cyan or white.
- **board_02, 147.6–151.3** — "They found a way to talk": a thin line (see 1.2).
- **open_00 / box_07** — the attacker is drawn as a human silhouette. Presumably deliberate for the reveal at 41 s;
  at 673–684 the narrator says "It was an AI" over the same human figure.
- Reuse: s05 at test_00 and weak_05; s04 at open_08 and box_03; k01 at open_00 and box_07.

`script.py`'s docstring says number captions are "typed in gold"; they are cyan in the film.

---

## 5. AUDIO

| Measure | Value |
|---|---|
| Integrated loudness | -14.0 LUFS |
| Loudness range | 1.8 LU |
| True peak | -2.3 dBFS (sample peak -2.4 dBFS, no clipping) |
| Mean / max volume | -17.3 dB / -2.4 dB |
| Stereo | L/R correlation 0.9996, side signal -48 dB: the mix is effectively mono |

Per chapter, RMS of the mix during speech versus the 3 s music-only crossing before the chapter:

| Chapter | Speech | Crossing | Gap |
|---|---|---|---|
| open | -14.2 | -34.0 (0–1.2 s) | 19.8 |
| test | -14.0 | -31.6 | 17.6 |
| board | -14.2 | -29.3 | 15.1 |
| weak | -14.0 | -25.6 | 11.7 |
| hours | -14.0 | -31.5 | 17.5 |
| sense | -14.3 | -25.6 | 11.3 |
| us | -14.0 | -31.0 | 17.0 |
| why | -14.1 | -31.3 | 17.2 |
| else | -13.9 | -31.2 | 17.3 |
| fallout | -13.9 | -30.3 | 16.4 |
| box | -14.0 | -30.6 | 16.6 |

- **Voice level** is flat across all eleven chapters (-13.9 to -14.3 dBFS). Good.
- **Voice above music.** In the 0.3 s gaps between lines the mix sits at a median of -24.5 dBFS (range -35.2 to -21.1),
  so the bed under speech is roughly 10 dB below the voice. Speech is above the music throughout by measurement; 10 dB
  is on the tight side for a beat with drums. By ear on a phone speaker before upload.
- **The music drops out at every chapter crossing.** In `flow/garage.wav` the bed falls about 9 dB for the 3 s of each
  crossing (stem -19.5 under speech, -27 to -30 in the crossings). The result is that the chapter title — the one moment
  with no voice — is the quietest point in the film (-30 to -34 dBFS, 16–20 dB below the speech either side). Two
  crossings behave differently: weak (201.3–204.3) and sense (316–319) come back up to about -20 dBFS for the last
  0.75 s, so they measure -25.6. Inconsistent.
- **Line ends.** In `voice_dry.wav` the last 50 ms of all 87 lines is below -70 dB and the last aligned word ends
  0.25–0.35 s before the line end. No cut-off tails by measurement.
- **Line starts.** hours_02 at 270.71 ("One,") goes from silence to -20 dB in under 20 ms; weak_05 at 243.35 and box_01
  at 628.04 are milder versions. Possible clipped onset. By ear.
- **Music monotony.** The bed is one 8-bar loop at about 132 BPM (envelope autocorrelation 0.8 at 14.55 s and at its
  multiples up to 174.6 s), repeated about 47 times. Level per 30 s stays within -19.2 to -20.1 dBFS and the spectral
  centroid alternates between two states (~1750 Hz and ~1930 Hz). There is no build, no breakdown apart from the
  crossings, and no change for the "why" chapter or the close. Eleven minutes of it, in mono.
- **Start.** 0–1.2 s is near-silent (-53 rising to -33 dBFS) under a black-then-dim frame.
- **Ending.** Last word ends 685.9. Mix is at -30.7 dBFS by 686.2–687, -43.5 by 688–689, silent at 689.2. The picture
  ("WHAT ARE WE REWARDING?") holds to ~688 and is black by 689.1. Clean, but only 3 s after the last word: no sign-off,
  no next-video prompt, and too short for YouTube end-screen elements (minimum 5 s, normally 15–20 s).

---

## 6. RETENTION

**First 30 seconds.** The words are strong: date, break-in, "under thirteen hours", "like no attacker they had seen".
The picture undersells them. Frame 0 is black; 0–3.4 s is a dim silhouette with no bright element; the date arrives
after it has been spoken; 5.8–12.5 is another dim picture. The first frame that would stop a scroll is "< 13 H" at
about 13.5 s. open_03 (22.3–26.9) and open_04 (27.2–34.3) are fine. Then 34.1–35.5 is an empty frame.
The reveal at 41.0–54.1 ("IT WASN'T A PERSON." → "700") lands, but it is 41 s in.

**Three dullest stretches**

1. **366.5–412.9 (IT WAS US, 46 s).** Date picture, three quote/number cards in a row each opening on an empty frame
   (372.2, 384.5), then a 14.2 s single plate (us_05) under a four-line caption. The chapter title promises a
   confession; the pictures are office furniture.
2. **542.1–622.1 (THE FALLOUT, 80 s).** Eight dated items in sequence. 567.97–608.33 is 40 s made of three lines of
   12.8, 12.4 and 14.6 s, each on one near-static plate. No variation in music.
3. **204.3–256.2 (THE WEAKEST POINT, 52 s).** The 15.2 s list at 227.8–243.1 (JRuby, kernel bug, metadata service,
   cluster-admin) is the most jargon-dense moment in the film and types on over 9 s, followed by the dimmest reused
   picture (243.3–248.3).

Also weak: 147.6–151.3 (black), and 483.2–539.1 (a second list chapter directly before the fallout list chapter).

**Three best moments**

1. **41.0–54.1** — "IT WASN'T A PERSON." into "700". Biggest type, clearest idea, best hop.
2. **441.1–480.2** — CoastRunners ring, Goodhart quote, "SOMETIMES CHEATING IS EASIER", "INCLUDING THE SANDBOX."
   The argument of the film in 40 s, and the pictures match the words.
3. **327.7–338.1** — Anthropic's models decline, so they use a Chinese open model. Best story beat in the middle;
   let down only by thin type at 327.7 and the blinking "GLM 5.2 · Z.AI" label.

---

## 7. VERDICT: FIX THEN UPLOAD

Numbered by importance.

1. **Fix the picture-label timing rule.** Labels must be on within ~0.3 s of the line start and stay until the camera
   leaves. Kills the blink at 261.3–262.0, 337.0–337.7, 370.1–371.4, 605.0–607.8 and the 1.5–2.2 s late arrivals at
   3.4, 186.5, 340.3, 356.8, 543.5. Re-check fallout_07 at 621.5–622.0.
2. **Replace the board_02 picture, 147.6–151.3.** 3.5 s of black under "They found a way to talk." Needs a readable
   image at normal brightness (two or more agents linked), or a `words` beat.
3. **Remove the "CAM +…… x0.8" readout and the beat numbers** from every frame, unless they are deliberate — in which
   case freeze or restyle them so they do not read as a debug overlay.
4. **Fix the opening, 0.0–5.5.** No black first frame; brighten k01; put "11 JULY 2026" on screen at 1.2 s with the
   first word, not at 3.4 s. Consider bringing "< 13 H" or the "IT WASN'T A PERSON" beat earlier.
5. **Fill the empty frame at the start of the 14 type beats** (34.1, 67.5, 211.2, 227.8, 288.3, 346.6, 372.2, 384.5,
   427.1, 518.2, 568.1, 628.1, 635.4, 647.8): start the type-on as the camera arrives and type faster so the text is
   complete by half-way through the line. Give us_01 (372.2–375.4) at least 1.5 s with its attribution up.
6. **Make multi-line ASCII words readable**: board_05 (174.4–184.2), else_05 (523.0–530.0), sense_01 (327.7–334.7)
   first; then the weak first lines at 110.3, 193.9, 248.6, 581.0, 608.6, 656.7. Same size for every line, or cut the
   phrase to two short lines.
7. **Replace the hours_06 picture, 302.4–310.7** (reads as a handgun). Brighten or replace s05 (64.7–67.3, 243.3–248.3),
   s29 (432.1–437.4), and lift k01 for the close (673.5–683.9).
8. **Audio.** Keep the bed up (or bring it up) through the chapter crossings instead of dropping 9 dB — 61.7–64.7,
   126.3–129.3, 256.2–259.2, 363.5–366.5, 412.9–415.9, 480.2–483.2, 539.1–542.1, 622.1–625.1 — and make 201.3–204.3
   and 316–319 match the rest. Add at least one arrangement change (drop the drums for "why", 415.9–480.2, or for the
   close, 673.5–686.2). Use a stereo bed. Listen once on a phone speaker for voice-over-music, and to 270.71, 243.35,
   628.04 for clipped onsets.
9. **Add an ending.** Hold "WHAT ARE WE REWARDING?" and the music for 15–20 s after 686.2 so end-screen elements fit;
   add a sign-off line or card.
10. **Fix open_07, 44.9–54.1**: show "1,200" first and switch to "700" when it is said (~51 s), or reorder the card.
11. **Stop the caption plate cutting pictures** (90.4, 105.6, 151.8, 259.2, 509.5, 542.1, 560.0, 593.7, 673.5): place
    pictures higher or cap captions at three lines; split the four-line captions at 227.8, 398.7, 593.7.
12. **Raise the minimum label size** — "REPORTED BY REUTERS · DISPUTED BY OPENAI" (398.7–412.9),
    "29 SEPTEMBER 2026 · SAN FRANCISCO" (593.7–608.3), "EXPLOITGYM · LAUNCHED 11 MAY 2026" (83.4–90.1) — break onto two
    lines rather than shrink.
13. **Caption consistency**: "GPT-5.6 Sol" and "GPT-6.1 Astra" with the hyphen at 136.8, 375.7, 581.0. Fix the
    "Hugging / Face." orphan at 1.2–5.5.
14. **Soften the fastest hops** — 580.2 and 608.0 first, then 41.3, 82.9, 471.6 — with motion blur or 0.2 s more
    travel time. Delay hop start so the last word of the line is not spoken over travel.
15. **Tidy**: chapter title should not cross the outgoing picture (127.2–127.4, 364.4–364.6, 622.9–623.1); coral notes
    at 136.8–147.3 and 375.7–384.4 to cyan; "POD"/"CLUSTER-ADMIN" at 311.0–316.0 to the plain wording; "SOL" card at
    375.7 not to repeat itself; pictures off the right edge at 163.5, 338.4, 366.5; hard picture edges at 217.8, 302.4,
    398.7.
16. **Pacing, if a re-cut is on the table**: break up 567.97–608.33 (three 12–15 s lines on single plates) and
    227.8–243.1 with a second visual each; these and 398.7–412.9 are where the camera is closest to standing still.

Still open from VERIFY.md section 6 and not part of this check: the WSJ source for both Wolf quotes, OpenAI's 26 Aug
report for the `weak` chain, the 1 Oct Washington Post report, "over a million models".
