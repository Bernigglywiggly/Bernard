# CRITIC FINAL — four films and nine Shorts, 8 Oct 2026

Independent review of the rendered files. Nothing edited except this report. Nothing uploaded.
Scratch (frames, sheets, audio measurements): `/private/tmp/claude-501/critic_final/` (`sheets/`, `fr/`, `s1/`, `aud/`).

## 0. Verdicts

| File | Verdict | Worst problem (timestamp) |
|---|---|---|
| `lf01_escape/LF01_FLOW_v6.mp4` | **FIX THEN UPLOAD** | Score drops to silence 6:37.0–6:39.5 (397.0–399.5 s, stem −60 dB) and returns +37 dB in half a second. Two more holes at 7:44 and 9:30.5. Same three holes as v5, only moved 34.5 s earlier |
| `lf02_price/LF02_FLOW_v5.mp4` | **FIX THEN UPLOAD** (upload sheet only, no re-render) | Film is clean. `POST.md` is for a different cut: 9 of 11 chapter times wrong, two of them (9:30, 10:02) past the end of a 9:02 film |
| `lf03_held/LF03_FLOW_v3.mp4` | **FIX THEN UPLOAD** | `POST.md`: all 10 chapter times wrong, two past the end (10:27, 11:11 on a 10:24 film). In the film: score hole 8:01–8:03.5 (481.0–483.5 s, −47 dB, +23 dB return) |
| `mc02_ponzi/MC02_PONZI_v3.mp4` | **FIX THEN UPLOAD** | Music bed sags 8–11 dB for about a minute, three times: 1:45–2:45, 5:45–6:50, 9:30–10:40. Two of these are the drops CRITIC_v2 item 1 listed (102, 344 s) |
| `short_war` | **UPLOAD** | Headline sits in the top 12% (all nine do) |
| `short_jevons` | **UPLOAD** | Empty frame 0:24.0–0:24.5; quote card small and dim 0:27–0:33 |
| `short_held` | **UPLOAD** | Three-line headline runs down to about 18% of the height |
| `short_bigmac` | **UPLOAD** | First frame is an unresolved ASCII blob; "1/60" dim at 0:21 |
| `short_talk` | **FIX THEN UPLOAD** | Frame 0 shows the previous beat ("5%" and a ghost caption about Internal Model 1); empty frame at 0:27 |
| `short_knew` | **FIX THEN UPLOAD** | "SOMETIMES IT ATTACKED ANYWAY." on screen about 0.6 s (0:10.7–0:11.3); empty frame at 0:12.0 |
| `short_escape` | **DO NOT UPLOAD as cut** | 64.59 s: over the 60 s limit set for this review |
| `short_cheat` | **DO NOT UPLOAD as cut** | 68.33 s: over the limit |
| `short_test` | **DO NOT UPLOAD as cut** | 79.25 s: over the limit |

I cannot hear. Every audio statement is a measurement; section 6 lists what needs an ear.

Method: one frame every 6 s of each film (420 frames) and every 2 s of each first 30 s, on contact sheets, all viewed;
2 fps scans of all four films for empty frames and long unresolved ASCII; 1 s strips of every flagged range; full-resolution
crops of the rail, a photo credit and the LF03 timeline. Shorts: every 3 s plus first and last frame, safe-zone lines drawn at
12% and 78%.

Not done: `*_phone.mp4` files; facts and sources; thumbnails. On MC02 I could not read the "ILLUSTRATION · AI-GENERATED"
labels at half resolution, so I cannot say every AI still carries one (see 4.3).

---

## 1. What was fixed since the last review (confirmed on the pictures)

| Film | Fixed |
|---|---|
| LF01 | hours_01 picture replaced (4:21 is now a branching network, not a hand with a bar). Last crossing levels even |
| LF02 | "3.2 QUADRILLION" on the card (5:40–5:45) with "3,200 TRILLION" in the label. "~20 YRS" now crisp type (2:15) |
| LF03 | Timeline headings no longer overlap (0:46–0:51). "CANCELLED / DEFENDERS ONLY" in crisp type (9:58–10:02). Last crossing at 9:48 now −24 dB like the others. Score join moved onto the crossing at 5:00 |
| MC02 | Photo credits now pinned at the top edge of each photo and readable through the beat (0:27, 0:40, 5:14, 6:37, 8:27 checked). End music holds to the end (−18 dB, clean fade) |
| Shorts | Frame 0 no longer black on any of the nine. "1,200 / 700" inside the frame (escape 0:45–0:51). "≈ 10 BIG MACS" on while spoken (bigmac 0:18). "3.2 QUADRILLION" (jevons 0:45). short_held now has identifiable pictures. End cards hold about 3 s |

---

## 2. Audio, measured

| File | Integrated | LRA | True peak | Silences > 1.5 s at −45 dB | Stretch > 4 s under −40 dB |
|---|---|---|---|---|---|
| LF01 v6 | −14.4 LUFS | 1.9 LU | −3.9 dBFS | none | none |
| LF02 v5 | −14.1 | 2.1 | −2.0 | none | none |
| LF03 v3 | −14.1 | 2.1 | −2.8 | none | none |
| MC02 v3 | −14.1 | 2.1 | −2.9 | none | none |
| short_cheat | −14.4 | 1.8 | −3.7 | none | — |
| short_escape | −14.5 | 1.5 | −4.0 | none | — |
| short_talk | −14.5 | 1.8 | −4.1 | none | — |
| short_bigmac | −14.0 | 1.7 | −3.1 | none | — |
| short_jevons | −13.9 | 1.7 | −2.8 | none | — |
| short_war | −14.1 | 1.8 | −2.8 | none | — |
| short_held | −14.3 | 1.9 | −3.1 | none | — |
| short_knew | −14.1 | 1.9 | −3.3 | none | — |
| short_test | −14.1 | 1.6 | −3.2 | none | — |

No clipping. No film has 4 s of total level under −40 dB, because speech covers every hole. The holes are in the music.

Music bed (from `flow/garage.wav` and from the mix in the gaps between lines):

| Film | Bed between lines, median | At chapter crossings | Holes and jumps in the music |
|---|---|---|---|
| LF01 | −30.7 dB | −25 to −29 | **397.0–399.5 s: −60 dB, then +37 dB at 399.5** (mix reads −59 in the word gap at 398.2). **464.0–466.0: −44, then +18.** **570.5–573.0: −48, then +26** |
| LF02 | −31.4 dB | −27 to −28 | None. Even throughout |
| LF03 | −28.8 dB | −24 to −29 | **481.0–483.5 s: −47 dB, then +23 dB**, under the first line of "Who decides". 442.0–443.5: −38, then +13 (mix −41 in the gap at 442) |
| MC02 | −32.7 dB | −26 to −34 (8 dB spread) | Bed normally −22 dB. **105–165 s: −27 to −33. 345–410 s: −27 to −33. 570–640 s: −26 to −33.** Inside each, 4.5 s stretches at −38/−39 followed by +16 dB hits (107.0–111.5, 350.0–354.5, 573.5–578.0). Then 185 s and 425–470 s run at −17 to −19 |

---

## 3. LF01 · The AI That Escaped · `LF01_FLOW_v6.mp4` · FIX THEN UPLOAD

First 30 s: date and figure by 0:02, picture clear by 0:04, "< 13 H" at 0:14, list at 0:28. The spoken hook lands at 0:01.
A cold viewer gets a reason to stay. The picture at 0:22–0:27 (a cloud of dots) says nothing, and frame 0 is dim.

| # | Time | Problem | Fix |
|---|---|---|---|
| 1 | 6:37.0–6:39.5 (397.0–399.5) | Music stem falls to −60 dB and returns +37 dB in 0.5 s. Mix reads −59 dB between words | The silence is inside the generated piece. Cut that 2.5 s out of the piece or crossfade over it, re-mix. No picture render |
| 2 | 7:44.0–7:46.0 (464–466) | Same: −44 dB, +18 dB return | Same |
| 3 | 9:30.5–9:33.0 (570.5–573) | Same: −48 dB, +26 dB return | Same |
| 4 | `POST.md` | Names `LF01_FLOW_v3.mp4` as the upload file and asks for "a critic pass on v3" | Change to v6. Chapter times are right (see below) |
| 5 | 0:45–0:54 | "700" drawn larger than "1,200" before "seven hundred" is said; "1,200" still dim at 0:45 | Lead with 1,200 at full brightness |
| 6 | 6:39–6:53 | "REPORTED BY REUTERS · DISPUTED BY OPENAI" still the smallest label in the film; three-line caption over the picture | Raise the label size |
| 7 | 9:57–10:07 | Three-line caption covers the base of the courthouse; date label tiny in a dark box | Raise the picture or split the line |
| 8 | 0:27, 7:51, 8:42.5–8:43.5, 9:40.5–9:41.5 | Empty frame for 0.5–1 s at beat changes (the 7:51 one under the end of a line) | Bring the next plate in sooner |
| 9 | 7:21, 8:03 | Outgoing ASCII words cut by the frame edge ("ARD / ING"); chapter title ghost over the globe | Clear the old plate before the move |
| 10 | 8:39–8:43 | Timeline sub-labels very small | Raise the size |
| 11 | 0:51, 6:21 | Coral labels ("JOINED THE ATTACK", "AN UNNAMED PRE-RELEASE MODEL") against the cyan scheme | Cyan |

Chapters in `POST.md` against the film: a chapter band is on screen at every listed time +1 s (1:02, 2:07, 3:22, 4:16, 5:16,
6:04, 6:53, 8:00, 8:59, 10:22). Pass.

Numbers against `script.py`: "< 13 H", "1,200 / 700", "898", "95% / 5%", "8", "15–18,000", "2,000+", "53", "1,100+" all match.

Rail legible at 1080p (chapter name about 11 px: readable on a monitor, not on a phone). End card present from 11:27.
No next-video line.

## 4. LF02 · The Price of Thinking · `LF02_FLOW_v5.mp4` · FIX THEN UPLOAD (sheet only)

First 30 s: "−20%" at 0:00, "−50%" at 0:08, "TWO COMPANIES. ONE AFTERNOON." at 0:16, "$1 TRILLION+" at 0:26. The best opening
of the four. A cold viewer stays.

| # | Where | Problem | Fix |
|---|---|---|---|
| 1 | `POST.md` chapters | Only 0:00, 0:42 and 1:45 are right. 3:12 lands mid-chapter on "≈ 8 NOVELS"; 4:11, 5:02, 5:36, 6:39, 7:38, 8:39 are 25–70 s late; 9:30 and 10:02 are past the end of the film. YouTube will not accept the list | Replace with: 0:00 Cold open · 0:39 One afternoon · 1:45 A thousand times · 2:56 In Big Macs · 3:44 Why they cut · 4:24 The Red Queen · 4:54 The paradox · 5:46 The catch · 6:34 Who pays · 7:28 Who wins · 8:03 Imagine · 8:28 Still running |
| 2 | `POST.md` header | Says 10:48 and `out/lf02_price_1080p.mp4`; end screen "from 10:28" | 9:02, `LF02_FLOW_v5.mp4`, end screen from 8:52 |
| 3 | `POST.md` sources | "Big Mac index (US $6.12, January 2026)". The film shows "$6.22 · THE ECONOMIST, JUL 2026" (script line 69) | Make the description match the film |
| 4 | 4:26.7–4:29.3 | Red Queen engraving is ASCII noise at 4:27, clear for about 1 s, shrinking by 4:29 | Hold the picture through the next line, or start it resolved |
| 5 | 0:15, 1:21, 5:39, 7:33, 8:03–8:05 | Empty or near-empty frame for 0.5–1 s; 7:33 is under the start of a line | Bring the next plate in sooner |
| 6 | 3:39 | Picture for "Your whole reading list" does not resolve into anything nameable at the sample | Check it resolves; replace if not |
| 7 | 2:21, 3:57, 5:51, 6:57, 8:39 | Coral labels | Cyan |
| 8 | 0:00 | "%" of "−20%" touches the right frame edge on the first frame | Start the camera settled |

Numbers against `script.py`: "−20%", "−50%", "$1 TRILLION+", "$4 / $20", "$2 / $10", "1,000×", "~20 YRS / 3 YRS", "9.7 T",
"480 T", "3.2 QUADRILLION", "128,000", "$2.56", "$5 TRILLION" all match.

Audio has no fault. End card present ("STILL RUNNING." plus sign-off) from 8:51.

## 5. LF03 · Too Dangerous to Release · `LF03_FLOW_v3.mp4` · FIX THEN UPLOAD

First 30 s: the model in a glass case is clear by 0:04, "CANCELLED." at 0:09, the hand at the door, the control room, the
magnifier. Readable pictures and a plain hook. A cold viewer stays.

| # | Where | Problem | Fix |
|---|---|---|---|
| 1 | `POST.md` chapters | Every time after 0:00 is wrong (7 s to 80 s late). 10:27 and 11:11 are past the end of a 10:24 film | Replace with: 0:00 Cold open · 0:42 One week · 1:45 The test · 3:04 It knew · 3:52 Don't stop · 5:00 Thinking in the dark · 6:08 The other door · 7:07 The same skill · 7:58 Who decides · 9:13 What it means for you · 9:48 Still in the box |
| 2 | `POST.md` | Length 11:57, file `out/lf03_held_1080p.mp4`, card "at 5:25", end screen "from 11:38" | 10:24, `LF03_FLOW_v3.mp4`. The line "there's a whole film about that one" is spoken at 4:51.6: put the card at 4:50. End screen from 10:14 |
| 3 | 8:01.0–8:03.5 (481–483.5) | Music stem −47 dB then +23 dB, under the first line of chapter 9 | Cut or crossfade that 2.5 s of the piece, re-mix |
| 4 | 7:22.0–7:23.5 (442–443.5) | Music −38 dB then +13 dB; mix −41 in the word gap | Same |
| 5 | 3:16.2–3:17.6 | "SOMETIMES IT / ATTACKED ANYWAY." is on from 196.6 to 197.4 s: 0.8 s including fades. Frame empty at 3:16.0–3:16.4. Not fixed since the last review | Bring it on at 196.2 with the first word and hold to 198.5 over the gap |
| 6 | 9:15 | Chapter title ghost "WHAT IT MEANS FOR YOU" lies across the incoming hand picture | Clear the title before the picture arrives |
| 7 | 0:46–0:51 | Timeline sub-labels readable at 1080p but very small | Raise the size |
| 8 | 1:03–1:15 | Quote card and a three-line caption carry the same words at once | Drop the caption to the attribution only, or shorten the card |
| 9 | 2:51, 3:27, 4:39, 9:59 | Coral labels | Cyan |

Numbers against `script.py`: "99%", "33.1%", "24.6%", "29.2%", "6.3% / 0%", "52% / 8%", "50 TO 90%", "27 YEARS", "THOUSANDS"
all match. The "38.8%" card (voice says "thirty-nine") and the "redlines that exists" quote card did not fall on a sample
frame: not re-checked.

Score: character changes at 5:00 and 9:20, both now on chapter crossings. End card present from 10:15.

## 6. MC02 · The Original Ponzi Scheme · `MC02_PONZI_v3.mp4` · FIX THEN UPLOAD

First 30 s: a real 1920 photograph of School Street is clear by 0:04 with its credit, "RECONSTRUCTION" labelled at 0:12,
"WHERE IS THE MONEY COMING FROM?" at 0:18, Ponzi's face at 0:27. A cold viewer stays. Frame 0–0:03 is ASCII noise.

| # | Where | Problem | Fix |
|---|---|---|---|
| 1 | 1:45–2:45, 5:45–6:50, 9:30–10:40 | Music bed 8–11 dB under the rest of the film (−27 to −33 against −22), with 4.5 s near-silences and +16 dB hits at 1:51.5, 5:54.5, 9:38. Then 3:05 and 7:05–7:50 run 3–5 dB hot. CRITIC_v2 item 1 asked for no change over 6 dB | Enter each repeat of the piece from where it is at level, or level-match the sections. Needs an ear first: if this is a deliberate sparse passage it may pass |
| 2 | Whole film | "ILLUSTRATION · AI-GENERATED" labels, where they exist, are about 11 px grey. I could not read them at half resolution on 0:33, 1:04, 2:04, 2:13, 3:52, 4:41, 4:52, 5:52, 7:36, 8:58, 9:35, 10:34. On a phone they are invisible | Open those 12 beats at full size and confirm a label is there; raise the size to match "RECONSTRUCTION" |
| 3 | 4:21–4:33 | "50% / 100%" and "18 / $1,800" are dim ASCII with tiny labels; one label coral. This is the core promise of the film | Crisp type, as done for "$250,000" at 5:09 |
| 4 | 9:48–10:27 | About 40 s of type only (quote, card, list, "THE SAME TRICK", card). CRITIC_v2 item 11, not changed | Put a photograph or still behind the Madoff line (10:13.5–10:22) |
| 5 | 3:41.5–3:42.5, 10:00–10:01 | Empty frame for 1 s; the second under the start of a line | Bring the next plate in sooner |
| 6 | 0:00–0:03, 3:14–3:15, 5:45, 7:51–7:52 | Photographs sit as unreadable ASCII blocks for 1–3 s before resolving | Shorten the resolve on photographs to under 1 s |
| 7 | 1:09, 1:15, 9:39–9:45 | Small location labels ("BOSTON HARBOUR, NOVEMBER 1903 · RECONSTRUCTION", "RIO DE JANEIRO · JANUARY 1949 · RECONSTRUCTION") a third the size of the other labels | One size |
| 8 | 0:57 | "BORN 1882 ·" with a dangling separator | Drop the dot |
| 9 | Tail | Sign-off says only "SOURCES IN THE DESCRIPTION"; no next-video line | Add one |

Chapters in `POST.md`: a band or a lit rail box is on screen at all 12 listed times +1 s. Pass.

Photo credits: present and readable on School Street (0:04), Ponzi (0:27, 5:14), Ponzi c.1920 (0:40), Washington Street
(3:03), the coupon (3:16), King's Chapel (4:15), the note (5:43), the house (5:21), the run (6:37), "Ponzi arrested"
(7:53), the Pulitzer page (7:57), custody (8:21), Allen (8:27), Rose (9:27). Type is still about 11 px.

Numbers against `script.py`: "6%", "$400+", "50% / 100%", "18 / $1,800", "$2.5M", "$250,000", "$10–15M", "7–9 YEARS",
"31 YEARS" all match. "$75" did not fall on a sample frame.

Not re-checked from CRITIC_v2: items 5–9 (mugshot plate masking, the Barron file, the Morse hedge, the 2 August front page).

## 7. Shorts

All nine are 1080x1920, 30 fps. Nothing bright anywhere in the bottom 22% of any Short. No text clipped by the frame edge
in a settled frame.

Common to all nine: the "THE CURVE" tag and the first headline line sit at 7–11% from the top, inside the top 12% that the
app covers. Move the headline block down to start at 13%.

| Short | Exact length | Under 60 s | Frame 0 | Faults | End card | Verdict |
|---|---|---|---|---|---|---|
| short_war | 41.40 s | yes | "−20%" large, dim, just inside both edges | Empty frame 0:24.0 | Readable, from about 0:39 | UPLOAD |
| short_jevons | 53.07 s | yes | Portrait as ASCII, name label | Empty frame with caption only 0:24.0–0:24.5; quote card small and dim 0:27–0:33 | Readable, 3.2 s | UPLOAD |
| short_held | 44.53 s | yes | Model in case, ASCII | Three-line headline reaches about 18% | Readable, 3.1 s | UPLOAD |
| short_bigmac | 48.80 s | yes | Unresolved blob | "1/60" dim with a fading caption at 0:21; transition junk at 0:06 | Readable, on by 0:48 (hold not confirmed above 0.8 s) | UPLOAD |
| short_talk | 57.78 s | yes | Stale: "5%" and a ghost caption from the previous beat | Empty frame at 0:27; "CHEATING RATE…" card small 0:30–0:36 | Readable, on by 0:57 (hold not confirmed above 0.8 s) | FIX THEN UPLOAD |
| short_knew | 49.26 s | yes | Head in profile, ASCII | "SOMETIMES IT ATTACKED ANYWAY." 0:10.7–0:11.3 only; empty frame 0:12.0; caveat list about 8 px 0:36–0:45 | Readable, 3.0 s | FIX THEN UPLOAD |
| short_escape | 64.59 s | **no** | Date label "11 JULY 2026" slides under the headline at 0:00 (text on text; clear by 0:03) | "3 H" cut by the left edge at 0:21; empty frame under speech at 0:39; quote card dim at 0:36 | Readable, 3.1 s | DO NOT UPLOAD as cut |
| short_cheat | 68.33 s | **no** | Bars and hand, unresolved | "THE SCORE." dim at 0:09; empty frame at 0:51 | Readable, 3.2 s | DO NOT UPLOAD as cut |
| short_test | 79.25 s | **no** | Silhouette at screens | Near-empty frame at 0:18 | Readable, 3.1 s | DO NOT UPLOAD as cut |

End-card second line ("ON THE CURVE · LINK ON THIS SHORT") is about 8 px on all nine: unreadable on a phone. The card only
works if the related-video link is attached at upload.

To get the three long ones under 60 s: escape, drop the quote beat 0:34–0:40 (it also removes the empty frame); cheat, drop
the Goodhart beat 0:38–0:50; test, cut the set-up 0:00–0:24 to one card and start on "99%".

## 8. What needs a human ear

1. LF01 6:37, 7:44, 9:30.5: does the music vanish and slam back?
2. LF03 8:01 and 7:22: same question.
3. MC02 1:45–2:45, 5:45–6:50, 9:30–10:40: is the thin passage a choice or a fault? Does 7:05–7:50 sound too loud under the voice?
4. All four: bed 14–18 dB under the voice between lines. Does it pump?

## 9. Top fixes, in order

1. LF02 `POST.md`: replace the chapter list, length, file name, end-screen time and Big Mac price (section 4). Ten minutes, no render. Then LF02 can go.
2. LF03 `POST.md`: replace the chapter list, length, file name, card time (4:50) and end-screen time (section 5).
3. LF01 music holes 6:37.0–6:39.5, 7:44–7:46, 9:30.5–9:33: patch the piece, re-mix.
4. LF03 music holes 8:01.0–8:03.5 and 7:22.0–7:23.5: patch, re-mix.
5. MC02 music sags 1:45–2:45, 5:45–6:50, 9:30–10:40: listen, then level-match.
6. Shorts escape (64.59 s), cheat (68.33 s), test (79.25 s): trim under 60 s.
7. All nine Shorts: move the headline below the top 12%.
8. LF03 3:16.2–3:17.6 and short_knew 0:10.7–0:11.3: hold "SOMETIMES IT ATTACKED ANYWAY." for 2 s.
9. MC02: confirm an AI label on the 12 stills listed in section 6 and raise the label size; set "50% / 100%" and "18 / $1,800" (4:21–4:33) in crisp type.
10. short_talk frame 0 (stale beat) and short_escape frame 0 (date label under the headline): start each on a clean first frame. LF01 `POST.md`: change the file name to v6.
