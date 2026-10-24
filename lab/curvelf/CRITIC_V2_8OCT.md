# CRITIC V2 — four films and nine Shorts after the fix-all render, 8 Oct 2026

Independent review of the rendered files. Nothing edited except this report. Nothing uploaded.
Previous report: `CRITIC_FINAL_8OCT.md`. Scratch (frames, sheets, audio): `/private/tmp/claude-501/critic_v2/` (`sheets/`, `f1/`, `sh/`, `aud/`).
I cannot hear. Every audio statement is a measurement; section 8 lists what needs an ear.

## 0. Verdicts

| File | Verdict | Worst problem (timestamp) |
|---|---|---|
| `lf01_escape/LF01_FLOW_v7.mp4` | **UPLOAD** | Two short music dips remain: 7:41.0–7:42.0 (10–13 dB down for 1 s) and 9:26.0–9:27.25 (falls to −41 dB, returns +23 dB in a quarter-second). Both under speech. 20-second ear check, not a blocker |
| `lf02_price/LF02_FLOW_v6.mp4` | **UPLOAD** | Opens on 1.25 s of empty frame (0:00.0–0:01.25, rail only). Cosmetic |
| `lf03_held/LF03_FLOW_v4.mp4` | **FIX THEN UPLOAD** (audio re-mix only) | Music holes NOT fixed: 7:22.25–7:25.0 (ramps to −33 dB, snaps back +15 dB at 7:25.0) and 8:02.25–8:03.5 (−36 dB, +19 dB at 8:03.5, under the first line of "Who decides"). The mix reads −39 and −44 dB in the word gaps there against a −28.5 dB median |
| `mc02_ponzi/MC02_PONZI_v4.mp4` | **UPLOAD** | 10:13.5–10:22: Ponzi's own 1920 portrait carries the label "88 YEARS LATER · THE SAME TRICK" while the voice names Bernie Madoff. Can be read as a picture of Madoff. Not a blocker; change the label if anything is re-rendered |
| `short_war` (41.40 s) | **UPLOAD** | Nothing a viewer would notice |
| `short_held` (44.53 s) | **UPLOAD** | Nothing a viewer would notice |
| `short_bigmac` (48.80 s) | **UPLOAD** | First 1.5 s is an unresolved ASCII blob; ends on a list, not a sentence |
| `short_test` (58.53 s) | **UPLOAD** | "29.2%" from the next beat flashes under the end card at 0:55.0 (under half a second) |
| `short_talk` (57.78 s) | **FIX THEN UPLOAD** | 0:37.5–0:46: the headline band covers the top half of the picture's own label "4 JULY 2026" for the whole 8 s beat |
| `short_escape` (56.97 s) | **FIX THEN UPLOAD** | 0:36.5–0:40.0: nothing on screen but the caption for 3.5 s; the quote card before it flickers (dim 0:34–0:35, bright 0:35.5, dim 0:36, gone). Also 0:00–0:02: "11 JULY 2026" sits half under the headline |
| `short_cheat` (59.10 s) | **FIX THEN UPLOAD** | 0:38.5–0:44: the Goodhart quote card appears, fades, vanishes (0:40–0:42 caption only), reappears in a different place at 0:42, vanishes again at 0:43.5 |
| `short_jevons` (53.07 s) | **FIX THEN UPLOAD** | 0:22.6–0:25.5: caption only for about 3 s; the Nadella quote card arrives late and is dim until 0:27 |
| `short_knew` (50.56 s) | **FIX THEN UPLOAD** | 0:12.7–0:13.4: headline only, nothing else, 0.7 s; then caption only to 0:15.0 while the quote card arrives late |

One cause sits behind four of the five Short failures: in the Shorts, quote cards come on 2–3 s after their line starts and fade out early or twice. The films do not do this (LF03 3:19.5: the quote starts typing 0.3 s into its beat). Fix the quote beat's timing in the Short renderer once and re-render escape, cheat, jevons and knew.

No file is DO NOT UPLOAD. All nine Shorts are now under 60 s.

Method: one frame every 8 s of each film on contact sheets (318 frames, all viewed); 2 fps scans of all four films for empty frames; every chapter time at −1, 0, +1 and +2 s (43 chapters); 56 number and split cards at half resolution; 12 AI-tag crops at full resolution; all 19 Ponzi photo beats at five points each. Shorts: every 4 s, the first 1.5 s and last 3.5 s at 2 fps, 10 fps scans for safe zones, and 2 fps strips of every flagged range.

Not done: `*_phone.mp4` files; facts and sources; thumbnails; number cards against `script.py` (they match the previous render's values on every card I saw).

---

## 1. Audio, measured

| File | Integrated | LRA | True peak | Silences ≥ 1.5 s at −45 dB |
|---|---|---|---|---|
| LF01 v7 | −14.5 LUFS | 2.0 LU | −3.9 dBFS | none |
| LF02 v6 | −14.1 | 2.1 | −2.0 | none |
| LF03 v4 | −14.1 | 2.1 | −2.9 | none |
| MC02 v4 | −14.1 | 2.1 | −2.6 | none |
| short_escape | −14.6 | 1.4 | −3.9 | none |
| short_talk | −14.5 | 1.8 | −2.9 | none |
| short_cheat | −14.4 | 1.8 | −2.9 | none |
| short_war | −14.1 | 1.8 | −2.8 | none |
| short_bigmac | −14.0 | 1.7 | −2.9 | none |
| short_jevons | −13.9 | 1.7 | −2.8 | none |
| short_held | −14.3 | 1.9 | −3.1 | none |
| short_test | −14.0 | 1.6 | −3.1 | none |
| short_knew | −14.2 | 3.0 | −2.4 | none |

No clipping anywhere. All inside target.

Music stem (`flow/garage.wav`, 0.5 s windows, first 3 s and last 14 s ignored):

| Film | Stem median | Stretches ≥ 12 dB under median for ≥ 1 s | 30 s means, spread | Biggest half-second jumps up |
|---|---|---|---|---|
| LF01 | −18.7 dB | **none** | −18.9 to −18.1 = 0.8 dB | +11.0 at 567.0 s, +9.8 at 462.0 s |
| LF02 | −19.3 dB | none | −20.1 to −19.2 = 0.9 dB | +8.2 at 3.5 s (the opening fade), then ≤ 5 |
| LF03 | −18.3 dB | **444.0–445.0 s (min −32.4, then +14.6)** and **482.5–483.5 s (min −35.8, then +18.9)** | −20.0 to −18.0 = 2.0 dB | +18.9 at 483.5 s, +14.6 at 445.0 s |
| MC02 | −19.4 dB | none | −21.0 to −17.8 = 3.2 dB | +15.6 at 354.5, +15.5 at 111.5, +15.3 at 578.0, +12.9 at 365.5, +12.8 at 122.5 s |

Finer look (0.25 s windows):
- LF01 461.0–462.0 s reads −20, −28, −27, −31 then back to −20/−18. 566.0–567.25 s reads −21, −28, −30, −34, −41 then −18. The old 397 s hole is gone (one window at −22).
- LF03 442.25–445.0 s ramps −21 → −33 over 2.75 s, then −18. 482.25–483.5 s reads −27, −32, −34, −36, −36, then −17.
- MC02: the three thin passages now sit 3–5 dB under the rest (10 s medians −22 to −25 against −19), down from 8–11 dB. Each still opens with single loud hits (−12 dB against −25 to −29 around them) at 111.5, 122.75, 354.5, 365.75 and 578.0 s that decay over 2 s. They look like drum hits, not faults.

Mix check in the gaps between words (film audio, gaps ≥ 0.35 s):

| Film | Gap level, median | Gaps 7 dB or more under it |
|---|---|---|
| LF01 | −29.8 dB | 5:39.6 (−38), **7:41.2 (−41)** |
| LF02 | −30.0 dB | none |
| LF03 | −28.5 dB | 6:23.3, 7:01.1, 7:35.9, 8:40.5, 9:01.4 (all −36 to −37), **7:23.0 (−39)**, **8:02.8 (−44)** |
| MC02 | −32.5 dB | 6:10.2 (−40) |

LF03's stem was written at 17:10, LF01's at 17:38. LF01 is close to clean and LF03 is not: it looks as if LF03 was mixed before the hole patch went in. Re-run the mix for LF03; no picture render is needed.

---

## 2. LF01 · The AI That Escaped · `LF01_FLOW_v7.mp4` · 11:37 · UPLOAD

| Old finding | Now |
|---|---|
| 1. Music hole 6:37.0–6:39.5 (−60 dB, +37 dB return) | **FIXED** |
| 2. Music hole 7:44–7:46 | **FIXED in the main** (now 7:41.0–7:42.0, 1 s, 10–13 dB down; was 2 s at −44) |
| 3. Music hole 9:30.5–9:33 | **FIXED in the main** (now 9:26.0–9:27.25; still touches −41 dB for a quarter-second and returns +23 dB) |
| 4. `POST.md` names v3 | **FIXED** (v7, 11:37, end screen 11:27) |
| 5. "700" larger than "1,200", "1,200" dim (0:45–0:54) | **FIXED** (same size, crisp, both bright) |
| 6. "REPORTED BY REUTERS · DISPUTED BY OPENAI" the smallest label (6:39–6:53) | **NOT FIXED** (cosmetic) |
| 7. Three-line caption over the courthouse base, tiny date label (9:57–10:07) | **NOT FIXED** (cosmetic) |
| 8. Empty frames 0:27, 7:51, 8:42.5–8:43.5, 9:40.5–9:41.5 | **NOT FIXED** (0:27 and 7:51 about 0.5 s; 8:42.5 and 9:40.5 still 1 s) (cosmetic) |
| 9. Clipped outgoing words 7:21, title ghost 8:03 | **FIXED** |
| 10. Timeline sub-labels very small (8:39–8:43) | **NOT FIXED** (cosmetic) |
| 11. Coral labels (0:51, 6:21) | **NOT FIXED** (cosmetic; every split still has a coral right-hand label) |

Number and split cards (13 checked: "< 13 H" twice, "1,200 / 700", "898", "95% / 5%", "ZERO-DAY", "17,600", "SOL / ?", "8", "15–18,000", "2,000+", "53", "1,100+"): all crisp type, inside the frame, clear of their labels and of the captions.

Chapters (`POST.md` and `uploads_newlook.json` agree): a band is on screen at every listed time +1 to +2 s (1:02, 2:07, 3:22, 4:16, 5:16, 6:04, 6:53, 8:00, 8:59, 10:22). Pass.

New, ranked:
1. 9:26.0–9:27.25 and 7:41.0–7:42.0: the two remaining music dips (section 1). Minor. Fix only if the mix is re-run anyway: crossfade over those two seconds.
2. 0:40.5, 4:57: 1 s of empty frame at the beat change (new samples of an old habit). Cosmetic.
3. 3:04: frame nearly empty with a leftover of the next picture at bottom right while a caption runs. Cosmetic.
4. "THE SCORE." (7:04) and "REWARD HACKING" (7:20) are still drawn in ASCII characters. They are word cards, not figures, and they read. Cosmetic; say if this is unintended.

## 3. LF02 · The Price of Thinking · `LF02_FLOW_v6.mp4` · 9:02 · UPLOAD

| Old finding | Now |
|---|---|
| 1. `POST.md` chapters for a different cut | **FIXED** (all 11 times checked against the picture: band on screen at +1 to +2 s for 0:39, 1:45, 2:56, 3:43, 4:24, 4:53, 5:45, 6:34, 7:27, 8:02, 8:27) |
| 2. `POST.md` length, file name, end screen | **FIXED** (9:02, v6, 8:52) |
| 3. Big Mac price in sources ($6.12 against $6.22 on screen) | **FIXED** ($6.22, July 2026, in `POST.md` and the upload sheet) |
| 4. Red Queen engraving readable about 1 s (4:26.7–4:29.3) | **NOT FIXED** (ASCII to 4:27.5, clear 4:28.0–4:28.5, shrinking at 4:29.0) (cosmetic) |
| 5. Empty frames 0:15, 1:21, 5:39, 7:33, 8:03–8:05 | **NOT FIXED** (single 0.5 s samples at 0:15.0, 1:20.5, 5:39.0, 8:02.5, 8:05.0; 7:33 gone) (cosmetic) |
| 6. 3:39 picture does not resolve | **FIXED** (a stack of papers, clear by 3:42) |
| 7. Coral labels | **NOT FIXED** (cosmetic) |
| 8. "%" touching the right edge on the first frame | **FIXED**, at a cost: see new item 1 |

Number and split cards (18 checked, from "−20%" at 0:06 to "3.2 QUADRILLION" at 5:43): all crisp, inside the frame, clear of labels and captions.

New, ranked:
1. 0:00.0–0:01.25: the film opens on an empty frame (rail only); "−20%" fades in at 1.25 s with the first word. Frame 0 is the fallback thumbnail. Cosmetic if the custom thumbnail is set. Fix: draw "−20%" from frame 0.
2. 2:56.0, 6:34.0: about half a second of empty frame before the chapter band. Cosmetic.

Audio has no fault.

## 4. LF03 · Too Dangerous to Release · `LF03_FLOW_v4.mp4` · 10:25 · FIX THEN UPLOAD

| Old finding | Now |
|---|---|
| 1. `POST.md` chapters all wrong | **FIXED** (band on screen at +1 to +2 s for all ten: 0:42, 1:45, 3:03, 3:53, 5:01, 6:08, 7:08, 7:59, 9:13, 9:49; the 1 s shift after 3:17 is right) |
| 2. `POST.md` length, file, card and end-screen times | **FIXED** (10:25, v4, card 4:51, end screen 10:15) |
| 3. Music hole 8:01.0–8:03.5 (−47 dB, +23 dB) | **NOT FIXED** (now 8:02.25–8:03.5, −36 dB, +19 dB return; shorter and shallower, still there) |
| 4. Music hole 7:22.0–7:23.5 (−38 dB, +13 dB) | **NOT FIXED**, slightly **WORSE** in length (now 7:22.25–7:25.0, a 2.75 s slide to −33 dB, +15 dB return) |
| 5. "SOMETIMES IT ATTACKED ANYWAY." up 0.8 s | **FIXED** (on from 3:16.25 to 3:18.5, about 2.2 s) |
| 6. Chapter title ghost over the hand picture (9:15) | **FIXED** |
| 7. Timeline sub-labels very small (0:46–0:51) | **NOT FIXED** (cosmetic) |
| 8. Quote card and three-line caption carry the same words (1:03–1:15) | **NOT FIXED** (cosmetic) |
| 9. Coral labels | **NOT FIXED** (cosmetic) |

Number and split cards (13 checked: "99%", "38.8%", "33.1%", "24.6%", "29.2%", "6.3% / 0%", "52% / 8%", "EASY / HARD", "50 TO 90%", "650+", "THOUSANDS", "27 YEARS", "CANCELLED / DEFENDERS ONLY"): all crisp, inside the frame, clear of labels and captions.

New, ranked:
1. 7:22.25–7:25.0 and 8:02.25–8:03.5: the music holes (section 1). The only reason this film is not UPLOAD. A listener on headphones will hear the bed drop out and come back. Fix: re-run the mix with the same hole patch LF01 got; audio only. If an ear check at 8:02 and 7:23 says it cannot be heard, upload as is.
2. 5:43.0, 8:30.5, 9:29.5: 1 s of empty frame at beat changes. Cosmetic.
3. 3:18.75–3:19.25: half a second of empty frame after the lengthened card. Cosmetic.

## 5. MC02 · The Original Ponzi Scheme · `MC02_PONZI_v4.mp4` · 10:59 · UPLOAD

| Old finding | Now |
|---|---|
| 1. Music sags 8–11 dB at 1:45–2:45, 5:45–6:50, 9:30–10:40 | **FIXED** (now 3–5 dB; 30 s means within 3.2 dB). The loud single hits at the start of each thin passage remain (1:51.5, 2:02.75, 5:54.5, 6:05.75, 9:38.0): needs an ear |
| 2. "ILLUSTRATION · AI-GENERATED" unreadable | **FIXED** (present and readable at full resolution at all 12 listed times: 0:33, 1:04, 2:04, 2:13, 3:52, 4:41, 4:52, 5:52, 7:36, 8:58, 9:35, 10:34; about 20 px type at top left under the rail). Small on a phone, but there |
| 3. "50% / 100%" and "18 / $1,800" dim ASCII | **FIXED** (crisp, bright) |
| 4. 40 s of type only, 9:48–10:27 | **FIXED** (photos at 9:50–9:56, 10:00.5–10:06, 10:13.5–10:22, each with a label and a credit strip) |
| 5. Empty frame 3:41.5–3:42.5 and 10:00–10:01 | 3:41.5 **NOT FIXED** (1 s); 10:00 **FIXED** |
| 6. Photographs unreadable ASCII for 1–3 s before resolving | **NOT FIXED** (every photo takes 1.5–2 s to resolve; the opening photo is ASCII until 0:03) (cosmetic) |
| 7. Small location labels a third the size of the others | **NOT FIXED** (1:12 "BOSTON HARBOUR, NOVEMBER 1903 · RECONSTRUCTION", 9:12 "NEW ORLEANS · RECONSTRUCTION", 9:42 "RIO DE JANEIRO · JANUARY 1949 · RECONSTRUCTION" are tiny; 5:24 and 7:49 "RECONSTRUCTION" are huge) (cosmetic) |
| 8. "BORN 1882 ·" dangling dot (0:57) | **NOT FIXED** (cosmetic) |
| 9. No next-video line on the sign-off | **NOT FIXED** (cosmetic) |
| Photo credits present | **STILL PRESENT** on all 19 photo beats (strip at the top edge of each photo once resolved) |

Number and split cards (12 checked: "$2.50", "6%", "$400+", "50% / 100%", "18 / $1,800", "$2.5M", "$250,000", "$10–15M", "ABOUT 30¢", "7–9 YEARS", "31 YEARS", "$75"): all crisp, inside the frame, clear of labels and captions.

Chapters: band on screen at +1 to +2 s for all 11 listed times (0:48, 1:42, 2:58, 4:10, 5:09, 5:45, 6:31, 7:11, 7:59, 8:41, 9:28). Pass.

New, ranked:
1. 10:13.5–10:22: the photo is Charles Ponzi (the same portrait as 0:40), labelled "88 YEARS LATER · THE SAME TRICK", while the voice says "a respected New York investor called Bernie Madoff confessed". A viewer can take the face for Madoff. Fix: label it "CHARLES PONZI · c. 1920" with "88 YEARS LATER" as a second line, or use a different picture. Not a blocker: the plate itself reads "CHAS. PONZI" and the same face was named at 0:40.
2. Pictures labelled "RECONSTRUCTION" (0:12, 1:12, 1:49, 2:48, 5:24, 7:18, 7:49, 8:48, 9:10, 9:16, 9:42) do not carry the "ILLUSTRATION · AI-GENERATED" tag. They are AI pictures too. The upload is flagged synthetic, so this is cosmetic; put the tag on them for consistency.
3. 7:52–7:55: the "PONZI ARRESTED" front page is clear for about 1.5 s (resolved 7:53, shrinking 7:54.5). Cosmetic.
4. "VERY HARD WORK" (1:41) and "ONE MORE THING" (6:24) are ASCII word cards, as in LF01. They read. Cosmetic.

---

## 6. Shorts

All nine: 1080x1920, 30 fps. Headline band starts at y = 232 px on every frame of every Short (limit 230). Nothing bright in the top 12% or the bottom 22% on any frame. No black first frame. End cards readable.

| Short | Exact length | Frame 0 | End card at full brightness | Last caption | Mid-Short faults | Verdict |
|---|---|---|---|---|---|---|
| short_war | 41.40 s | "−20%" crisp, clean | 38.3–40.8 (2.5 s) | "…what happens when it gets close to free?" complete | 0:24.0 half a second of caption only | UPLOAD |
| short_held | 44.53 s | Model in case, ASCII, resolves by 1.5 s | 41.4–44.2 (2.8 s) | "…who gets to decide what you're allowed to use?" complete | none | UPLOAD |
| short_bigmac | 48.80 s | Unresolved blob to 1.5 s | 45.7–48.2 (2.5 s) | "Your whole reading list. Every review a restaurant has ever had. Years of your emails." A list with no closing clause | none | UPLOAD |
| short_test | 58.53 s | Silhouette at screens, ASCII | 55.4–58.2 (2.8 s) | "…fake accounts to post supportive comments." complete | 0:55.0 "29.2%" ghost under the incoming end card | UPLOAD |
| short_talk | 57.78 s | Clean: headline and a dim caption, no picture until 0.5 s | 54.7–57.1 (2.4 s) | "…used the folder names as messages." complete | **0:37.5–0:46 "4 JULY 2026" half hidden by the headline band**; 0:04.0 empty for half a second | FIX THEN UPLOAD |
| short_escape | 56.97 s | "11 JULY 2026" half under the headline to about 0:02 | 53.9–56.6 (about 2.7 s with the slow push) | "…Around seven hundred of them joined the attack." complete | **0:36.5–0:40.0 caption only; quote card flickers 0:34–0:36** | FIX THEN UPLOAD |
| short_cheat | 59.10 s | Bars and hand, ASCII, resolves by 1.5 s | 56.0–58.9 (2.9 s) | "…sometimes, cheating is the easier route." complete | **0:38.5–0:44 quote card on, off, on in a new place, off**; "THE SCORE." dim ASCII at 0:08; "INCLUDING THE" ghost under the end card at 0:55.5 | FIX THEN UPLOAD |
| short_jevons | 53.07 s | Portrait, ASCII, name label clear of the band | 50.0–52.8 (2.8 s) | "…More than three hundred times as much, in two years." complete | **0:22.6–0:25.5 caption only; quote dim until 0:27**; 0:40.0 half a second empty | FIX THEN UPLOAD |
| short_knew | 50.56 s | Head in profile, ASCII, resolves by 1.5 s | 47.5–49.9 (2.4 s) | "…might behave differently outside one." complete | **0:12.7–0:13.4 headline only**; 0:13.4–0:15.0 caption only; 0:09.7–0:10.5 near-empty; caveat list about 8 px (0:36–0:46) | FIX THEN UPLOAD |

Old Shorts findings:

| Old finding | Now |
|---|---|
| escape 64.59 s, cheat 68.33 s, test 79.25 s | **FIXED** (56.97, 59.10, 58.53) |
| Headline in the top 12% on all nine | **FIXED** (y = 232 on all nine) |
| short_talk frame 0 stale ("5%" and a ghost caption) | **FIXED** |
| short_escape frame 0: date label under the headline | **NOT FIXED** (0:00 to about 0:02) |
| short_escape "3 H" cut by the left edge at 0:21 | **FIXED** ("< 13 H" inside the frame) |
| short_escape quote dim 0:36, empty under speech 0:39 | **WORSE** (caption only for 3.5 s, 0:36.5–0:40.0) |
| short_cheat empty frame 0:51; "THE SCORE." dim at 0:09 | 0:51 gone with the trim; "THE SCORE." **NOT FIXED**; the Goodhart beat that was meant to be cut is still in and is broken (0:38.5–0:44) |
| short_jevons empty 0:24.0–0:24.5, quote small and dim 0:27–0:33 | **WORSE** (about 3 s, 0:22.6–0:25.5). The old review sampled every 3 s and may have under-measured |
| short_knew "SOMETIMES IT ATTACKED ANYWAY." 0.6 s | **FIXED** (0:10.5–0:12.7, about 2.2 s) |
| short_knew empty frame 0:12.0, caveat list 8 px | **NOT FIXED** (now 0:12.7–0:13.4; list still tiny) |
| short_bigmac first frame an unresolved blob; "1/60" dim | blob **NOT FIXED**; "1/60" **FIXED** (crisp) |
| short_talk empty frame 0:27, small "CHEATING RATE" card | empty frame gone; card readable. **FIXED** |
| short_held three-line headline to 18% | **STILL THREE LINES**, now below the 12% line and clear of the picture. Fine |
| End-card second line ("ON THE CURVE · LINK ON THIS SHORT") about 8 px | **NOT FIXED** (cosmetic; the link must be attached at upload) |
| End cards hold about 3 s | 2.4–2.9 s at full brightness. talk and knew are at 2.4 s, a hair under the 2.5 s asked for; with the fades either side they read for about 3 s. Pass |

Fixes for the five:
1. Quote beats (escape 0:33.5–0:40, cheat 0:38.5–0:44, jevons 0:22.6–0:27, knew 0:13–0:16.5): bring the card on with the first word and hold it to the end of the line, once, in one place.
2. short_talk 0:37.5–0:46 and short_escape 0:00–0:02: drop the picture (or its label) 60 px so "4 JULY 2026" and "11 JULY 2026" clear the band. Check every date-labelled picture in a Short with a two-line headline.
3. short_knew 0:12.7–0:13.4: start the next caption when the card leaves.
4. short_cheat is 59.10 s. Cutting the Goodhart beat (0:38.5–0:44) fixes the flicker and gives 5 s of margin.

---

## 7. What is cosmetic

Everything not named in section 0. In particular: coral labels; small labels (Reuters, timelines, reconstruction locations, the Shorts caveat list, the end-card second line); 0.5–1 s empty frames at beat changes in the films (about 40 per film, four or fewer of a full second each); photos taking 1.5–2 s to resolve; "BORN 1882 ·"; LF02's empty first 1.25 s; ASCII word cards; ghosts under the Shorts end cards.

## 8. What needs a human ear

1. LF03 8:02–8:04 and 7:22–7:25: does the music drop out and slam back? If yes, re-mix. If no, LF03 is UPLOAD.
2. LF01 9:26–9:27.5 and 7:41–7:42: same question, smaller.
3. MC02 1:51.5, 2:02.75, 5:54.5, 6:05.75, 9:38: are the single loud hits musical?
4. All four: the bed sits 14–18 dB under the voice between lines. Does it pump?

## 9. Top fixes, in order

1. LF03: re-run the mix with the hole patch (audio only). Publishes 16 Oct.
2. Shorts quote-beat timing: one renderer fix, then re-render escape (13 Oct), cheat (15 Oct), jevons (11 Oct), knew (19 Oct).
3. short_talk (14 Oct): clear "4 JULY 2026" from under the headline. Same nudge for short_escape frame 0.
4. MC02 10:13.5: relabel the Ponzi portrait so it cannot be taken for Madoff. Only if something else forces a render.
5. LF02 0:00: draw "−20%" from the first frame. Only if something else forces a render.

short_war (9 Oct), LF02 (9 Oct), short_bigmac (10 Oct), LF01 (12 Oct) and MC02 (13 Oct) can go as they are.
