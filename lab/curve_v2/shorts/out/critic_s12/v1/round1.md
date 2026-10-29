# Short 12 v1 critic, round 1 (34.1 s, 1080x1920)

| # | Area | Score |
|---|---|---|
| 1 | Hook / frame 0 | 6 |
| 2 | Readability | 5 |
| 3 | Motion | 8 |
| 4 | Variety / composition | 5 |
| 5 | Accuracy | 8 |
| 6 | Sound | 9 |
| 7 | Authorship | 6 |

## 1. Hook (6)
- Frame 0 is clean and the 1:59 to 1:00 flip at about 2.5 s is a real hook. But frame 0 as a thumbnail is a small phone (about 45% of width, 43% of height) with a left-aligned headline and the bottom 35% empty. It reads as "a phone", not as a tension. Under the 60% subject rule.
- 0-3 s voice ("phones across America will change their own clocks") is a flat statement. No "you", not the most surprising fact, and nothing on the 1:59 frame hints at what is odd.
- Frame 0 has no caption on screen (first caption lands about 0.3 s later), fine.

## 2. Readability at 360 px (5)
- Headline, big captions, 02:00 and FIRST SUN rows are good (white or lime on near-black).
- Too small (cap height roughly 25-40 px, rule is 48): "NOT HAWAII OR MOST OF ARIZONA" (22-33 s), "KEPT BY VOLUNTEERS" tag (4-9 s), "6 IN 2026 · IANA" (22-24 s), "UTC" tag (13-17 s), "CELL TOWER"/"TIME SERVER" (about 40 px), zone list text in the rulebook (16-21 s, mono, about 25 px), AMERICA/NEW_YORK sub-line (24-31 s), and the end-card line "THE CURVE: HOW NEW TECH ACTUALLY WORKS" (about 30 px).
- Caption size is not locked: "PHONES ACROSS AMERICA" (1.5-2.5 s), "KEPT BY VOLUNTEERS." (5 s), "OF EVERY TIME ZONE'S" and "FIRST SUNDAY IN NOVEMBER," are visibly smaller than "ON SUNDAY," and "HISTORY."
- "KEPT BY VOLUNTEERS" tag at about 4.3 s overshoots to the right edge (x about 1075) at y about 1050, inside the Shorts button strip, and settles at x about 960. Same CRAFT overflow that was a MUST on Short 11.
- Captions sit at y about 1340-1450; the lower 25% of every frame is empty, wasting space that the strip rule does not forbid.

## 3. Motion (8)
Measured: frozen 0.1 s, near-still 1.7 s, no stretch over 2 s. Something new about every 1.5-2.5 s. Weak spots: 6.5-9 s (phone plus book static apart from the caption), 24-27 s (rule line builds but phone and tag static), 31-34 s verdict hold with only the strap. Pulses and card stack are linear-looking; add spring or varied speed.

## 4. Variety and composition (5)
- Every scene is the same layout: small headline top-left, 40% diagram, caption lower third, empty bottom. Objects float small in a big dark frame (a CRAFT banned default: small card in empty frame).
- Shot list promised a US map with Hawaii and Arizona greyed; v1 shows only text, so the "most of the US" tag has no picture. The six release cards (22 s) are the one strong, full-width scene.
- Phone shrinks from large (0-9 s) to tiny (13-30 s), losing the continuity object.

## 5. Accuracy (8)
- Facts check: 2026a-f, 27 Oct, six releases; 1 Nov 2:00 to 1:00; UTC 05:59 for 1:59 EDT is correct; Hawaii/Arizona wording matches the "most of the US" rule; no House vote claim. No numeric mismatch.
- SHOULD soften: "Volunteers rewrite that rulebook" is present tense, but RFC 6557 says "previously maintained by volunteers" and the checks file notes a TZ Coordinator now runs it. Say "Volunteers have kept that rulebook".
- Overclaim: "it only works because volunteers do the homework" and the end-card "IT RUNS ON HOMEWORK" skip NTP/NITZ and OS update delivery. It is labelled "Our take", so acceptable, but "it depends on volunteers" is safer.
- "6 IN 2026" shown beside "SIX TIMES ALREADY" is consistent; date stamp "27 OCT" must be re-checked on Fri 30 Oct if a 2026g appears.

## 6. Sound (9)
-14.2 LUFS integrated, true peak -1.4 dBFS, LRA 1.6, per-second short-term -13.4 to -15.2 through 31 s. Passes. The last 3 s fade to -22/-23 LUFS; fine for a loop, but check the loop seam is not a dead gap. Not checked by ear: music-under-voice balance and whoosh harshness (no stems given).

## 7. Authorship (6)
Has a verdict and our own drawings, which helps. But the neon-lime-on-purple, top-left headline, bottom caption look is the same template as other recent Shorts, and nothing here is research on screen that only we could show. Make it ours: a recurring physical object (e.g. a hand-drawn rulebook with a real stamped release date) carried through every scene, plus one real artefact (the iana.org release list for 2026a-f) shown as a screenshot-style drawing.

## Top 5 fixes
1. MUST: Clamp the "KEPT BY VOLUNTEERS" tag (and every popping tag) inside x 930, wrap to two lines, no overshoot past x 960; keep right 120 px at y 1000-1700 clear.
2. MUST: Raise every label to 48 px cap height or more: Hawaii/Arizona note, tag, UTC, CELL TOWER/TIME SERVER, release strap, end-card promise; rulebook list to 48 px with fewer rows visible.
3. SHOULD: Scale the phone to fill 60-70% of frame 0 and keep the large scale in later scenes; move captions to about y 1500 and fill the middle, so the empty bottom quarter disappears. Add a real US map with Hawaii/Arizona greyed.
4. SHOULD: Lock caption size across pages (one font size, auto-wrap to two lines instead of shrinking).
5. SHOULD: Rework the 0-3 s line to carry "you" and the oddity ("Your phone will rewind itself at 2 a.m. Sunday, and volunteers wrote the rule"); soften "rewrite" and "only works because" per section 5; carry one recurring object for authorship.

Verdict: ONE MORE PASS
