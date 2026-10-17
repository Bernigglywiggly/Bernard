UPLOAD — before 27 Oct 2026 (Visa publishes fiscal 2026 that day after market close). POST.md chapters already corrected in this pass; no re-render required.

# CRITIC v7: HTP06 (Visa) · HTP06_MASTER_v7.mp4 (1920x1080, 30 fps, 259.37 s = 4:19)

Independent critic, 11 Oct 2026. Did not build the film. Measurements in `lab/ch2/ep06/out/critic_v7/`
(loudness.txt, ebur128.txt, motion.txt, transcript.txt [faster-whisper small, two doubtful words re-checked with
medium], frame0.png, phone.jpg, open/scale/hop/cost/end sheets, thumbs_phone.png, thumbD_168.png). Per-frame lit-pixel
scan of the whole film (every 3rd frame, picture area above the caption band).

## 1. The v6 edits: did they land in v7?

| Edit | Verdict | Evidence |
|---|---|---|
| Re-voice `never` (no "never held/touches") | **LANDED** | Audio 20.1-28.2: "lends none of that money and keeps almost none of it, and that turns out to be the reason it is so profitable." Caption matches. No "never held" anywhere in the transcript. |
| Re-voice `close` | **LANDED** | Audio 249.4-256.5: "...on terms written by a company that lent none of it." Caption matches. |
| Settlement claim | **CLEAN** | Film never claims Visa doesn't touch or settle money. Remaining "never collects" (207.98, interchange) is true per the 10-K. |
| No wire-scene boxes over the opening | **LANDED** | 0.2 s sheet 8.6-12.6 s: the cyan "message out" tag and arc are whole on every frame; no black rectangles. v6 N1 closed. |
| Cost block 50/40/10 | **LANDED** | 2:51-2:58: "$16.0B to run" block measures ~40% of the cell (61 of 151 px on the sheet), cyan profit 50% left, 10% sliver right; at 2:59 the sliver becomes "tax". v6 N2 closed. |
| Headline back for the hop to the cell | **PARTLY** | "$40.0 billion / what Visa kept / about 24¢ of every $100 moved" sits beside the lit cell 2:41-2:46. But the hop itself still has an empty picture: 157.2-158.0 s (~24 frames, max pixel 5/255 above the caption) — v6 N3 shortened from 28 frames, not gone. And the "$17 trillion" headline still slides out the left edge 20.0-21.6 ("7 trillion", "rillion", "on") — v6 N7 still present. |
| Larger sources | **PARTLY** | Richmond line now white, ~13 px ink, reads "Federal Reserve Bank of Richmond, 2011 (US)" (v6 F4 closed) at 1:07 and in the last chapter. The 10-K credit under the top quote ("Visa Form 10-K · fiscal 2025") is still ~9 px grey at 1:08 and ~7 px in the last chapter. Unreadable on a phone; the description carries it. |

## 2. Remaining problems

**Sound: PASS.** -14.0 LUFS integrated, true peak -2.2 dBFS, LRA 1.4 LU, short-term within -13.0 to -15.8 throughout,
tail fades from 4:18. Voice audibly clean; whisper's "Your parties"/"playing" were mis-hears (medium model: "Four
parties", "plain").

**Picture: PASS WITH NOTES.** Frozen 6% (no stretch ≥ 2 s), near-still 30% (v6: 41.6%). Remaining, all present in v6:
| # | Time | Sev | What | Fix (next render only) |
|---|---|---|---|---|
| R1 | 2:37.2-2:38.0 | NICE | Empty picture during the hop to the cell (caption only). | Hold the revenue bar until the arc is visible (158.1). |
| R2 | 0:20.0-0:21.6 | NICE | "$17 trillion" cut by the left edge as it exits. | Fade in place before the push. |
| R3 | 0:30.9-0:39.4 | NICE | Four-parties opening dark (<0.8% lit in runs, 2.4 s at 0:37-0:39); near-still 5.9 s from 0:39.1. | 35% grey outlines on unlit boxes. |
| R4 | 2:19.5-2:23.9 | NICE | 4.4 s near-empty: title, empty bar outline, grey stub before the $15.8B fill. | Start the fill at 2:19. |
| R5 | 0:08.8-0:10.8 | NICE | "A café, Lisbon" label slides off under the caption. | Fade before the plate. |
| R6 | 4:19 | NICE | Hard stop on the map, no end card. | Add end card when made. |

**Captions:** burned captions are long-film keyword captions at ~33 px, inside the safe area; they match the audio
word for word. Upload CC too (CRAFT §9.5): YouTube auto-captions are fine; the transcript in `out/critic_v7/` can be
cleaned into an .srt if wanted.

**Frame 0 / first 8 s (CRAFT §9.1, §9.7): WEAK, not a blocker.** Frame 0 is a designed composition (label, ASCII map,
teal ring) and works as a fallback thumbnail only. Line 1 (1.2-6.8 s) is scene-setting ("A card touches a reader..."),
the surprising true fact ("lends none of that money and keeps almost none of it") arrives at 0:20. The title's
promise (Visa isn't a credit card company) is paid at 0:45-0:58 ("Visa is not a financial institution", "doesn't
issue the card and doesn't lend the money"): inside the §9.9 one-minute rule. Fixing the hook needs a re-voice and a
re-cut; not worth it for this film. Next film: open on the contradiction.

## 3. Facts

Every spoken and on-screen figure checked against FACTS.md: $17T (10-K); $17.5B, 257.5B, $20.0B, $14.2B, $4.1B
("about four billion"), $15.8B, $40.0B, $16.0B, $20.1B, $22.8B, $2.5B (8-K); derived $55.8B (= 17.5+20.0+14.2+4.1),
~24¢ per $100 (40.0/17,000), ~700M a day (257.5B/365), 50¢ per dollar (20.1/40.0), tax ≈ 10% (40.0-16.0-20.1 = 3.9).
**No mismatch.** "For years" and "interchange is the largest fee" are now sourced in FACTS.md.

**"Last year" (said 6 times) = fiscal 2025: ACCURATE TODAY.** Visa announced on 8 Oct 2026 that it will release
fiscal Q4 and full-year 2026 results on **Tuesday 27 October 2026, after market close** (webcast 2 pm PT / 5 pm ET)
— investor.visa.com and usa.visa.com press release 22841. From that evening every figure is one year stale and "last
year" points at the wrong fiscal year (on screen it still says "fiscal 2025", so it stays *true*, just dated).
- Upload on or before 26 Oct for the clean window.
- If uploaded after 27 Oct: keep the "Figures are for Visa's fiscal 2025" line at the top of the description and pin
  a comment with the FY2026 net revenue / net income once out. No re-voice needed unless the film is re-cut.

## 4. Packaging

**Title "Visa Isn't a Credit Card Company": PASS.** 32 characters, 6 words, concrete subject, belief-break, says
"credit card" so it escapes immigration-visa traffic. True per the 10-K ("We do not issue cards, extend credit"),
and paid on screen by 0:58.

**Thumbnail D (`thumb_D.png`, 1280x720): USE IT. Readable at phone size.** At 168x94 px "WHO GETS / THIS?" is
legible, the card reads as a card, the red ring and arrow land on the cyan sliver. 3 words, high contrast, one focal
object, no repeat of the title. Bottom-right: the "?" ends ~130 px above the bottom edge, clear of the duration
stamp. Minor: the answer (the sliver is Visa's 24¢) is shown at 2:41, but it is a question rather than a promise, and
"who gets the fee" is answered at 1:05-1:17 (banks get interchange, Visa collects none). Test & Compare arms as
POST.md says: D vs H ("LENDS $0 / MAKES $20B", also readable) vs A ("24¢ OF EVERY $100").

**Description: exists in POST.md and is paste-ready** (summary, fiscal-2025 line, chapters, three sources with URLs,
derived maths, synthetic-voice and Natural Earth note, not-advice line). Two errors corrected in this pass:
- Chapters were ~2 s early again (the re-voiced `never` line lengthened the film by 1.4 s). Now, from lines.json and
  the audio: **0:00, 0:28, 1:02, 1:33, 2:18, 2:45, 3:28.**
- File duration 4:18 → **4:19**.

## Exact fixes

Before upload (all done or zero-cost):
1. DONE — POST.md chapters 0:00 / 0:28 / 1:02 / 1:33 / 2:18 / 2:45 / 3:28; duration 4:19.
2. Upload by 26 Oct 2026; tick "altered or synthetic content: yes"; set thumbnail D; enable Test & Compare with D, H, A.
3. Add CRAFT Learned line (builder): re-voicing a line shifts every chapter mark; regenerate chapters from lines.json
   after any re-voice.

Next render only (none block upload): R1-R6 above, and the 10-K credit lines to ≥ 12 px.
