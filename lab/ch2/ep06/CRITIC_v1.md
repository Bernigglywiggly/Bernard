# CRITIC v1: HTP06 (Visa) · HTP06_full_v1.mp4 (1280x720, 4:18, 30 fps)

Independent critic, judged from the render only. Method: 129 frames at 2 s steps on 7 contact sheets, all read; 30
full-resolution frames and 7 quarter-second strips of the fast passages read; frame-difference on all 7,740 frames
(caption area excluded); ebur128 and RMS against `build_george/lines.json`. Timestamps are accurate to about 1 s
unless a decimal is given. Pixel positions are in the 1280x720 frame.

Counts: **4 BLOCKER · 18 FIX · 7 NICE**

## Issues, most severe first

| # | Time | Sev | What is wrong | Suggested fix (camera / layout words) |
|---|---|---|---|---|
| 1 | 2:44-3:26 (whole close-up, 42 s) | BLOCKER | **The suspected patch is real.** Hard-edged black rectangles cut into the teal glow around the lit cell. At 3:02 a black slab sits right of the cell at x 885-980, y 205-600; at 3:21 it is x 578-1000, y 383-585, under the "bank needs" list; a second one sits left of the cell. They are the neighbouring (empty) cells' masks clipping the glow, so the halo reads as a broken render. | Draw the glow after the neighbour masks, or clip it to the lit cell only, or drop the halo (CRAFT bans glows on UI anyway). Re-check at 2:46, 3:02, 3:21. |
| 2 | 0:28-0:29.5, 2:33.5-2:35.5, 3:28.5-3:29.5 | BLOCKER | Three camera transits cross empty space at huge zoom: 1-2 s of near-black frame showing only giant dim fragments chopped by the edges: "issued the card", "38.72N 009.14" (cut right), "approve" (cut right), "ed the card" (cut left). Looks like a glitch each time. | Do not route moves through the map's label area at that zoom. Pull out first, travel wide, then push in; or travel straight between the two scenes. No frame should be only cropped ghost text. |
| 3 | 3:31-4:07 (36 s, the verdict scene) | BLOCKER | Chopped leftovers of other scenes line the left edge throughout the lawsuit and verdict: "tion.”", "for account holders.", "ards.", "n the wire." / "wire.", "ank", later "illion transactions processed" and a cut cyan "700 million a day" tag. Half the card's-bank node and its cut tag "rries the loss when a bill goes unpaid" also hang at the edge. | Shift the litigation column about 350 px further right of the card's bank (or frame so the left margin is clean), or dim/hide neighbouring scenes to 0 while this one is framed. |
| 4 | 3:59-4:07 on screen; narration 1:05 and 3:59 | BLOCKER (facts) | On screen as a plain fact: "If you run a shop: most of a card payment's cost goes to banks." Narration says "most of what a card payment costs you goes to banks" and, at 1:05, "a large part of what accepting a card costs". FACTS.md lists this as **NOT verified** ("check a primary source before voicing"). No source line near it, and the film gives advice on the back of it. | Source it (Fed Reg II data or Visa's published US interchange schedule) and add a mono source line under it, or soften the on-screen line to what the 10-K supports ("interchange is paid to the cardholder's bank, not to Visa"). |
| 5 | 3:28-3:31 red arc; 3:35-4:07 "$2.5 billion" | FIX | Red appears **twice**, not once: the interchange arc turns red, and "$2.5 billion" is also red. Worse, the red arc (the intended single weak point) is framed for about 3 s and is then pushed off the left edge as a sliver, while the red number holds for 30 s. | Keep red on the arc only; set "$2.5 billion" in white. Frame the verdict so the red arc stays fully in shot (camera 300 px left, or move the litigation text under the arc). |
| 6 | 3:36-4:07 | FIX | The cyan wire leaving the card's bank runs straight through the middle of "$2.5 billion" like a strikethrough (y 252, x 210-560). Text over shape. | End the wire at the node, or drop the number 40 px below the wire. |
| 7 | 0:53-1:01 | FIX | The quote "“Visa is not a financial institution.”" and its detail line are cropped by the top and left edges ("Visa is not…" loses its opening, "…cards, extend credit or set rates…" starts mid-phrase) exactly while the narration paraphrases that line. At 1:11-1:17 the detail line is sliced by the top edge again. | Hold the wider framing from 0:49 through 0:59 so the whole quote stays in shot; push in on the network node only after "the loss belongs to the bank". |
| 8 | 2:39-2:40.5 | FIX | Caption plate covers the lit cell (the subject of the sentence "Visa kept about 24 cents") while the camera pushes in; it clears about 1 s before the figure is spoken. | Start the push 1 s earlier, or aim so the lit cell lands in the upper two thirds, never behind the plate. |
| 9 | 0:26-0:28, 2:36-2:39, 3:26-3:28 | FIX | Caption plate sits on top of the cell grid and slices "$17 trillion" in half (2:36-2:38 the headline shows as "$17 trilli" cut by the plate and the bottom edge). | Keep the map framing clear of the grid, or frame the grid fully; never park a headline on the bottom edge. |
| 10 | 0:26-0:28, 2:36, 3:27, 4:08-4:18 incl. the final frame | FIX | A strip of grey grid cells pokes into the bottom right of the map shot (x 725-1240, y 688-720). It is in the **last frame of the film**. | Move the grid 200 px lower in the drawing or tighten the map framing by 8%. |
| 11 | 0:13-0:21 | FIX | Two collisions on the $17T shot: the source note "Visa Form 10-K" runs under the first grid cell (reads "Visa Form 10" + a grey block), and the header "How They Profit · 06" prints on top of the map's "100W" axis label. The map's axis and dot rows also intrude along the top. | Shorten the mono line or start the grid 60 px further right; drop the header 30 px below the axis; frame the map out. |
| 12 | 3:02-3:26 | FIX | Inside the lit cell: "50¢ of every dollar" runs hard into the black divider (no margin); "buybacks and dividends · fiscal 2025" overflows the cell border and crosses the frame line (x 563); the cyan leader line cuts through "net revenue"; "one more message costs it almost [nothing]" is cut off by the right edge for 8 s. | Narrow the type or widen the profit half; keep the buyback note inside the cell or wholly outside; pull the camera back 10% so the right column fits. |
| 13 | 1:32-2:09, 2:18-2:33 | FIX | Leftovers linger in the meters scene: "The fee pays banks to issue the cards. / Every card sends more messages down the wire." stays top right for about 30 s, as bright as the meters' title, then gets sliced by the top edge (2:01-2:09). At 2:18-2:33 the "$14.2B / $4.1B" rows are cut by the top edge. | Dim finished scenes to about 25% once the camera leaves, and frame so a neighbour is either fully in or fully out. |
| 14 | 0:30-0:44 | FIX | "Four parties": one box of about 220 px in a 1280 frame, then three boxes of about 180 px with 80% of the frame empty. Sub-labels ("card tapped here", "collects card payments") are about 9-10 px. CRAFT bans "a small card floating in an empty frame"; lead subject should fill 60-85%. | Start tight on the café node (fills half the frame), track right along the wire to each bank as it is named; only go wide at 0:44 when the network node lights. |
| 15 | throughout, worst 1:36-2:33 | FIX | Tiny mono notes carry real information at 9-11 px in the 720p frame: meter row labels, "three meters · fiscal 2025 · Visa results, 28 Oct 2025", "charged to banks and partners · $55.8 billion", "257.5 billion transactions processed" (a headline figure shown only as a 9 px note at the right edge), "handed back as incentives". Unreadable on a phone. | Double the mono size for anything the narration relies on; give 257.5 billion a proper figure beside the meter. |
| 16 | 0:00-0:11 | FIX | The Lisbon/Ohio payment **is** labelled ("illustration · one card payment across a border · not a real transaction"), but only once the wide map appears at about 0:11, at about 11 px, and at 0:13-0:20 it is tangled with the axis. For the first 11 s the film shows "A café, Lisbon 38.72N 009.14W · card tapped" and a precise-looking timer ("message out · 0.12 s", "0.44 s") with no label. | Put the illustration note under the Lisbon label from frame 0, at caption-adjacent size. |
| 17 | 0:23-0:27 | FIX | The lit cell and "$40.0 billion · what Visa kept" appear two minutes before the narration reaches net revenue (2:31), with no source, while the voice says the company "never held any of the money". A viewer reads "kept $40 billion" against "never held". | On the first visit show the lit cell unlabelled (or "Visa's slice, in a minute"); reveal the figure at 2:31. |
| 18 | 2:45-2:57 (12 s), 2:44-3:26 overall | FIX | Frame difference stays under 0.15 for 12 s (165.7-177.5 s): a flat teal block with a slow push while two sentences pass. The scene then sits on the same object for 42 s. Also 1:33.8-1:35.9 near-still. | Animate the fill inside the cell on each figure (opex wipes in from the right, profit counts up), and cut the hold to about 25 s. |
| 19 | 3:25.6-3:29.7; also 0:25-0:29, 2:33-2:38 | FIX | Camera detours: lit cell → grid → map → push through the map → whole drawing at thumbnail size → nodes, in 4 s, while the voice delivers the pivot line ("The weak point…"). Nothing is readable; the same grid-map-detour happens three times. Peak frame difference of the film (62) is here and at 0:26. | One direct move per transition: pull straight out from the cell to the whole drawing (1.5 s), settle, push to the arc as it turns red. |
| 20 | 0:01-0:08 | FIX | Hook. The first 8 s say a card is tapped and approved in a second: true, not surprising. The surprising thing ($17 trillion crossing a company that never holds it and keeps half its revenue as profit) arrives at 0:14-0:26. Frame 0 is a designed composition, which is right. | Open on "never held any of the money" with $17 trillion, then drop into the Lisbon tap. |
| 21 | 0:14, 1:41, 1:49, 2:21, 2:49, 3:34 | FIX | "Last year" is spoken six times for fiscal 2025 (year to Sep 2025). Fiscal 2026 already closed on 30 Sep 2026 and reports late October; FACTS.md says to swap every figure before voicing. Published now, "last year" is wrong within weeks. | Either hold for the FY2026 release and re-voice the figures, or re-voice "last year" as "in fiscal 2025". |
| 22 | 4:15-4:18 | FIX | The music is still at -35 dB in the final 50 ms: it stops dead with the file, no fade, no end card or pointer to the next film. | 1.5 s fade on the bed; end card or a resolved final frame. |
| 23 | 0:11-0:13 | NICE | "A bank, Ohio / 39.96N 083.00W" is drawn over map glyphs ("*", "#" print through the coordinates); the ASCII landmasses are hard to recognise as North America and Iberia. | Knock the map out behind labels; add two or three more coastline rows or a faint outline. |
| 24 | 0:09 | NICE | "A café, Lisbon" and its coordinates slide half behind the caption plate as the camera tilts. | Tilt 60 px less. |
| 25 | 0:26.0, 3:25.75 | NICE | For about a quarter second two captions are superimposed in a grey box over the grid (outgoing and incoming line cross-fading). | Hard-swap captions, no cross-fade. |
| 26 | 0:48-1:18 | NICE | The 10-K detail line is shown as "We do not issue cards, extend credit or set rates and fees for account holders." with a full stop; the filing continues "of Visa products nor do we…". The regulators quote (3:41) is also trimmed and re-capitalised. Accurate in sense, not verbatim. | End the trimmed line with an ellipsis; keep quotation marks only on verbatim text. |
| 27 | 3:31-4:07 | NICE | "Shops have been taking Visa to court over this fee for years." repeats the caption almost word for word (and "for years" is flagged unverified in FACTS). | Replace with a dated, sourced fact (the MDL case name and year) or drop it. |
| 28 | 2:44-3:26, arcs | NICE | Teal halo around the lit cell and the glowing arcs are "glows on UI", on CRAFT's banned list. | Flat fills, thin lines. |
| 29 | whole film | NICE | Sound balance: bed alone measures -35 dB RMS (tail), voice lines -16.9 dB, so music sits about 18 dB under the voice; LRA is only 1.4 LU. On a phone the garage bed will be close to inaudible and the film will sound like voice only. | Lift the bed 3-4 dB in gaps longer than 0.5 s (side-chain), keep -14 LUFS. |

## Facts check (on-screen vs FACTS.md vs narration)
All match: $17 trillion (10-K, sourced on screen); grid of 170 cells at "$100 billion moved" each; $17.5B, $20.0B,
$14.2B, $4.1B (bar lengths proportional within 2%; source "Visa results, 28 Oct 2025" on screen); 257.5 billion and
"about 700 million a day"; $55.8 billion charged, $15.8B incentives, $40.0 billion net revenue; "about 24¢ of every
$100 moved"; $16.0B to run; $20.1B profit after tax; 50¢ of every dollar; $22.8B back to shareholders; $2.5 billion
"for the interchange litigation and other legal matters". The lit cell is filled 40% ($40B of a $100B cell): correct.
Coordinates are plausible (Lisbon 38.72N 9.14W; 39.96N 83.00W is Columbus, Ohio).
Problems: item 4 (unverified claim), item 21 (fiscal year), item 16 (illustration label late and tiny), item 26 (trimmed
quotes). No source line near the profit cell ($16.0B, $20.1B, 50¢, $22.8B): add "Visa results, 28 Oct 2025".

## Motion (frame difference, 320x180, caption area excluded)
- Frozen (diff < 0.02 for 1.5 s or more): none. Share of frozen frames 1.6%; near-still (< 0.08) 11%. No near-black
  stretch of 1.5 s by mean luma, but see item 2 for the ghost-text transits.
- Slowest: 93.8-95.9 s and 165.7-177.5 s (item 18).
- Too fast to read: 20.5-25.0 s (4.5 s continuous push into the grid), 25.7-27.4, 158.0-160.9, 205.6-209.7, 247.4-248.7 s.

## Sound (measured)
| Measure | Result | Target |
|---|---|---|
| Integrated loudness | -14.0 LUFS | -14 |
| True peak | -1.9 dBFS | at or below -1 |
| First 30 s / last 30 s | -13.9 / -14.2 LUFS | consistent |
| Loudness range | 1.4 LU | (very flat) |
| Voice lines RMS | -16.9 dB | |
| Gaps between lines RMS | -26.0 dB (9 dB under, includes voice tails and effects) | |
| Music alone (tail 255-258 s) | about -35 dB (18 dB under the voice) | |
| Clipping | none (max sample 0.78) | |
| Start | first word at 1.2 s, bed fades in from 0 | fine |
| End | 3.0 s of bed after the last word, no fade, hard stop | item 22 |
No effect is louder than the voice. Per 10 s the level holds between -16.8 and -17.6 dB: consistent.

## Structure against CRAFT.md
- Hook in the first 8 s: weak (item 20). Frame 0 is a finished composition.
- Point of view: yes, "Here's how I'd read it" at 3:49, plus practical advice at 3:59 (which leans on the unverified claim).
- Forward teases: 0:20 ("the reason it is so profitable"), 1:27 ("In a minute, what Visa charges"), 2:52 ("which we
  will come back to"). Spacing is within 60-90 s. Nothing teases the final minute.
- Loop: yes. The end returns to the Lisbon-Ohio map and "the next time a reader says approved".
- Shape differs from EP05 (a map and one tap, not a followed $100): good against the template risk.
- Length is 4:18; the script header planned about 7 minutes. Under 8 minutes there are no mid-roll ads.

## What works
- The one-drawing, one-camera idea holds: the wire, the four nodes, the sagging interchange arc under the wire and the
  meters all sit in one space, and returning to the map at the end pays it off.
- The cell grid is honest and clever: 170 cells for $17 trillion, one cell lit 40% for the $40 billion, then that
  same cell split into cost and profit.
- Interchange drawn as an arc that bypasses the network node, with "collects none of it" under the node, is the
  clearest image in the film.
- The meter bars are proportional and build in step with the narration; the cyan accent on the largest meter is right.
- Captions are clean, word-timed and on a solid plate; narration is measured and free of hype.
- Loudness, peak and consistency are on target. No frozen frames.

## Verdict
Not publishable as it stands; **yes, publishable after the BLOCKER and FIX items**, with no re-voice needed unless
the fiscal-year wording (item 21) is fixed by re-recording. The drawing and the argument are good and the numbers are
right, but the owner's worry is justified: the camera repeatedly frames one scene with chopped pieces of its
neighbours along the edges, three transits pass through empty space full of giant cropped ghost text, the close-up on
the lit cell has visible black slabs cut into its glow for 42 seconds, and the film's single red accent is used twice
while the one that matters slides out of frame. Most fixes are layout offsets and camera targets, not new scenes. The
one fact problem (most of a card's cost goes to banks) must be sourced or softened before upload, and the "last year"
figures expire when Visa reports fiscal 2026 in late October.
