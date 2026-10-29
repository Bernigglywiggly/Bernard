# Short 12 v2 critic, round 2 (34.1 s, 1080x1920)

| # | Area | Score |
|---|---|---|
| 1 | Hook / frame 0 | 7 |
| 2 | Readability at 360 px | 7 |
| 3 | Motion | 8 |
| 4 | Variety / composition | 5 |
| 5 | Accuracy | 8 |
| 6 | Sound | 9 |
| 7 | Authorship | 6 |

## Round 1 fixes
1. Tag overshoot into the button strip: FIXED. "KEPT BY VOLUNTEERS" now sits at x 60, y about 1270, one line (5.5 s). Longest line, "IT RUNS ON HOMEWORK", ends near x 980 but at y about 715, outside the strip. "MOST OF ARIZONA" (23-25 s) now touches the phone edge (see S1).
2. Labels under 48 px: FIXED for labels. Hawaii/Arizona note, tags, UTC, CELL TOWER/TIME SERVER, zone list and the end-card promise (2 lines) read at 360 px. Captions are a separate class (see S2).
3. Big phone, fill the frame, US map: PARTLY. Frame 0 phone is now about 52% of width and reads as the subject. The US map is still missing (the Hawaii/Arizona tag has no picture). Phone is still tiny at 12-15 s and 20-33 s, and the lower 35% of every frame is empty.
4. Caption size lock: STILL PRESENT. "PHONES ACROSS AMERICA" (1.5-4 s), "FIRST SUNDAY IN NOVEMBER," (22-24 s), "OF EVERY TIME ZONE'S" (14-15 s) and "FOR MOST OF THE US," are visibly smaller than "ONE LINE SAYS" or "HISTORY."
5. "You" in the hook, soften "rewrite" / "only works because": STILL PRESENT. Voice is unchanged (ledger says "not re-voiced").

## New or remaining findings (no MUSTs found)
- SHOULD (S1): 20-25 s, the "MOST OF THE US" tag overlaps the top-left of the small phone (covers part of the notch) and "MOST OF ARIZONA" butts against its left edge. Move the phone down or right by about 40 px, or shorten the tag.
- SHOULD (S2): caption size varies, noted above. The first caption of the Short is one of the small ones, so the hook second is the least legible. Pick one size and wrap to two lines.
- SHOULD (S3): at 5-9 s the tag "KEPT BY VOLUNTEERS" and the caption "KEPT BY VOLUNTEERS." say the same words about 100 px apart. Drop the tag or change it to "THE TIME ZONE DATABASE" (the label already used at 14 s).
- SHOULD (S4): release scene (16-21 s) regressed from v1's full-width cards. Six small cards fill the top-left third and the rest is empty. Make the cards two columns at 1.5x, or fill the lower half with the real IANA list.
- SHOULD (S5): the 12-15 s tower scene is a thin tower and a 120 px phone in a big empty frame (CRAFT's banned small-object-in-empty-frame). Scale up the tower and server by about 1.5x.
- SHOULD (S6, accuracy wording): "Volunteers rewrite that rulebook whenever a country moves its clocks" and on-screen "REWRITTEN BY VOLUNTEERS" are present tense and total. The checks file notes RFC 6557 says "previously maintained by volunteers" and that a TZ Coordinator now runs it; not every release is a country moving its clocks. Safer: "Volunteers keep updating that rulebook, six releases already this year." "It only works because volunteers do the homework" / "IT RUNS ON HOMEWORK" skips NTP/NITZ and OS update delivery; it is labelled OUR TAKE, so acceptable.
- SHOULD (S7): voice says "phones across America" at 0 s while 22 s says "most of the US". Minor mismatch. "Most of America" would match.
- SHOULD (S8): hook line has no "you" and 0-2.5 s is a flat statement. The 1:59 to 1:00 flip at about 2.5 s is the real hook and lands late. Cut the first two captions shorter so the flip lands by 1.5 s.

## Verified OK
- Dates and numbers: SUN 1 NOV, 2:00 to 1:00, 2026A-F with 2026F "27 OCT" (matches checks), "6 IN 2026 · IANA", UTC 05:59 = 1:59 EDT (correct; the script's shot note said 06:59, the render fixed it). Hawaii/Arizona wording matches "most of the US". No House-vote claim. NTP/NITZ described as "tower or time server", no GPS claim. Rule line "FIRST SUN · NOV 02:00 -1 HOUR" correct.
- Loop: last frame vs frame 0 PSNR 46.2 dB (not byte-identical, visually identical). Channel promise ("THE CURVE: HOW NEW TECH ACTUALLY WORKS") shows before the loop at about 31-33 s on 2 lines, y about 1400, clear of the strip.
- Motion: frozen 0 s, near-still 0.2 s, no stretch over 2 s.
- Sound: -14.2 LUFS, -1.4 dBFS, LRA 1.6, steady -13.4 to -15.2 through 31 s, tail fade to -22 for the loop. Measured only; music/voice balance not judged by ear.

## Authorship (6)
Verdict ("OUR TAKE") and our own drawings, plus a recurring phone and rulebook object, which improves on v1. Still the same neon-on-purple top headline, caption-below template as other Shorts, and no artefact that only we could show (for example a drawn iana.org release list).

## Verdict
SHIP. No MUST remains; the five round 1 fixes are two FIXED, one PARTLY, two STILL PRESENT, all SHOULD-level. If the voice is re-recorded anyway, do S6 and S8 first, then S1, S3 and S2, which are cheap layout changes. Publishing for Fri 30 Oct as is would be acceptable.
