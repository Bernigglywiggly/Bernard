# CRITIC v2: HTP06 (Visa) · HTP06_full_v2.mp4 (1280x720, 4:18, 30 fps)

Second independent critic. Did not build the film, did not write CRITIC_v1. Judged from the render only.
Method: 129 frames at 2 s steps on 7 contact sheets (all read); 4 half-second strips of the camera transits
(0:24.5-0:30, 2:32.5-2:41, 3:24.5-3:31.5, 4:06.5-4:10.5); 46 near-full-resolution frames incl. v1 comparisons;
frame-difference, lit-pixel share and red-pixel count on all 7,740 frames (caption area excluded); ebur128, sample
peak and RMS against `build_george/lines.json`. Timestamps accurate to about 0.5 s.

**v1 items: 6 FIXED · 8 PARTLY · 15 NOT FIXED · 0 WORSE** (29 items)
**New issues: 0 BLOCKER · 7 FIX · 4 NICE**
**Remaining BLOCKERs: 2** (item 4 facts, spoken at 1:05-1:10 and 3:59-4:07; items 2+19 camera transits at
0:26-0:30, 2:34-2:39, 3:25.5-3:29.5)

## 1. Every v1 item

| # | v1 sev | Time | Status | Evidence in v2 |
|---|---|---|---|---|
| 1 | BLOCKER | 2:44-3:26 | **FIXED** | 2:46, 3:02, 3:21, 3:23: halo is a smooth radial fall-off, no hard-edged black rectangle right of or under the cell (v1 3:02 and 3:21 show the slabs at the same spots). The halo itself is still there (item 28). |
| 2 | BLOCKER | 0:28, 2:33, 3:28 | **PARTLY** | Ghost labels are dimmed, not removed. 0:27.0: "A café, Lisbon / 38.72N 009.14W · card tapped" at about 35% grey plus "W · issued the card" cut by the left edge and giant axis labels "060W 040W 020W 000E". 3:27.0: same frame, labels at about 15% grey, a clipped "approved" tag at the top edge. 2:35.5: no labels, but giant map glyphs and "080W" cut by the left edge. The fix traded ghost text for empty frames: see new issues N1, N2. |
| 3 | BLOCKER | 3:31-4:07 | **FIXED** | 3:36-4:07: left edge is clean in every sampled frame; no "tion.”", "wire.", "ank", meter or node fragments. (The 3 s before it are not clean: N7.) |
| 4 | BLOCKER (facts) | 1:05, 3:59 | **PARTLY** | On screen now reads "If you run a shop: interchange goes to the banks, not to Visa." (10-K supports it). The narration is unchanged: "a large part of what accepting a card costs" (1:05-1:10) and "most of what a card payment costs you goes to banks" (3:59-4:07), captioned word for word. FACTS.md still lists both as unverified. Still a BLOCKER until sourced or re-voiced. |
| 5 | FIX | 3:28-4:07 | **PARTLY** | "$2.5 billion" is white. Red pixels exist only 3:28.9-3:31.8 (the arc) and for 5 frames at 4:07.8 (N8). But the arc is still framed for only 2.9 s and then slides off the left edge (3:31.5 shows half of it); the verdict plays for 36 s with the weak point out of shot. |
| 6 | FIX | 3:36-4:07 | **FIXED** | No wire through "$2.5 billion" at 3:36, 3:46, 3:56, 4:02 (v1 3:42 shows the strike-through). |
| 7 | FIX | 0:53-1:01, 1:11-1:17 | **PARTLY** | 0:48-1:10: quote, detail line and source are whole and centred above the network node. 1:12: the quote headline is out of frame and the detail line sits on the top edge; 1:16: "We do not issue cards…" is sliced through by the top edge, "Visa Form 10-K · fiscal 2025" orphaned under it. |
| 8 | FIX | 2:39-2:40.5 | **FIXED** | 2:40.0 the lit cell is at the plate's top-right corner, 2:40.5 it is clear at frame centre with its label readable; the figure is spoken at 2:41-2:42. |
| 9 | FIX | 0:26, 2:36, 3:26 | **NOT FIXED** | 0:26.5, 2:39.0, 3:26.5: caption plate sits on the full-frame cell grid. 2:36.0-2:38.0: "$17 trilli" / "trillion" / "on" cut by the bottom edge and half covered by the plate, exactly as v1. Also 0:14.5 (N6). |
| 10 | FIX | map shots, final frame | **PARTLY** | 4:09-4:18 and the final frame (4:17.9) are clean: no grid strip (v1 final frame has it). The strip is still in the three mid-film map shots: 0:27.5-0:28.0, 2:36.0-2:37.0, 3:27.5, bottom right, under the caption plate. |
| 11 | FIX | 0:13-0:21 | **PARTLY** | Header no longer prints on "100W". Still there at 0:16-0:20: "Visa Form 10-K" runs under the first grid cell ("10" + grey block + "K"), and axis labels "020W 000E" plus dot rows intrude along the top edge. New collision at 0:14.5 (N6). |
| 12 | FIX | 3:02-3:26 | **NOT FIXED** | 3:02: "50¢ of every dollar" still runs into the divider, no margin. 3:21, 3:23: "buybacks and dividends · fiscal 2025" still crosses the cell border ("fi|scal"); the leader line still cuts "net rev|enue"; "one more message costs it almos" still cut by the right edge. |
| 13 | FIX | 1:32-2:09, 2:18-2:33 | **NOT FIXED** | 1:34-2:00: "The fee pays banks to issue the cards. / Every card sends more messages down the wire." at full brightness top right, with the cut "interchange" tag above it until 1:46; sliced by the top edge 2:02-2:08. 2:18-2:32: "$20.0B" / "$14.2B" rows cut by the top edge (2:20 shows "$20.0B" halved). |
| 14 | FIX | 0:30-0:44 | **NOT FIXED** | 0:30: one box about 120 px wide in a black frame. 0:33: two boxes about 230 px each. Lit pixels above the caption stay under 1.2% from 0:34.4 to 0:44.1 (9.7 s). |
| 15 | FIX | throughout | **NOT FIXED** | Mono notes unchanged: meter labels, "three meters · fiscal 2025 · Visa results, 28 Oct 2025", "charged to banks and partners · $55.8 billion" about 8-9 px; "257.5 billion transactions processed" still only a small note (1:50, 2:05); "set aside for the interchange litigation…" about 7 px (3:36). |
| 16 | FIX | 0:00-0:11 | **PARTLY** | "illustration · one card payment across a border · not a real transaction" is on screen from frame 0 (v1 frame 0 has no header at all) and again on every map shot. It is still about 11 px mono in the top-left corner. "Late" is fixed, "tiny" is not. |
| 17 | FIX | 0:23-0:27 | **FIXED** | 0:24.5-0:26.0: lit cell shown with no figure or label. The "$40.0 billion · what Visa kept" label first appears at 2:40. |
| 18 | FIX | 2:45-2:57 | **NOT FIXED** | 165.7-177.5 s: mean frame difference 0.115, 80% of frames under 0.15 (v1's threshold). Same flat teal block and slow push; the scene still sits on one object for 42 s. 93.8-95.9 s: 94% under 0.15. |
| 19 | FIX | 0:25-0:29, 2:33-2:38, 3:25.6-3:29.7 | **NOT FIXED** | All three detours are intact: cell → full-frame grid → map label area → map → push through → next scene. Peak frame difference of the film is still here (62.9 at 3:26.5, 61.5 at 0:26.5). At 3:28.5-3:29.0 the whole drawing passes as a thumbnail under the line "The weak point…". |
| 20 | FIX | 0:01-0:08 | **NOT FIXED** | Unchanged (builder lists as open). |
| 21 | FIX | six lines | **NOT FIXED** | "Last year" still spoken and captioned at 0:14, 1:41, 1:49, 2:21, 2:49, 3:34 (builder lists as open). |
| 22 | FIX | 4:15-4:18 | **FIXED** | Bed falls from -34.6 dB at 4:15.0 to -59.6 dB at 4:17.75; last 50 ms at -78 dB (v1: -37 dB). No end card or pointer to the next film; the film ends on the map. |
| 23 | NICE | 0:11-0:13 | **PARTLY** | 0:12.7 and the final frame: map glyphs are knocked out behind "A bank, Ohio" and its coordinates. The landmasses are the same sparse outlines. |
| 24 | NICE | 0:09 | **NOT FIXED** | 0:09.0: "A café, Lisbon" is entirely behind the caption plate (only descender stubs show above it) and the coordinates read "38.7" cut by the plate. |
| 25 | NICE | 0:26.0, 3:25.75 | **NOT FIXED** | Two captions superimposed and unreadable at 2:34.0 ("What remained…" under "Set against…") and at 3:34 ("Shops have been…" under "Last year the company…"). |
| 26 | NICE | 0:48-1:18 | **NOT FIXED** | Detail line still ends "…for account holders." with a full stop; regulators quote unchanged. |
| 27 | NICE | 3:31-4:07 | **NOT FIXED** | "Shops have been taking Visa to court over this fee for years." still on screen 3:31-4:00, and for 3.6 s it is the only thing on screen (N3). |
| 28 | NICE | 2:44-3:26 | **NOT FIXED** | Teal halo around the lit cell and glow on the arcs remain. |
| 29 | NICE | whole film | **NOT FIXED** | Mix is sample-identical to v1 except the tail: voice -16.9 dB RMS, gaps -26.5 dB median, bed alone about -35 dB, LRA 1.4 LU. |

### The builder's two lists, checked
Claimed fixed: black slabs **yes**; ghost text in transits **only dimmed** (0:27.0, 3:27.0 still show it; 2:35 is
clean of text but not of chopped glyphs); left edge of the verdict scene **yes**; red twice and the strike-through
**yes**; cropped quote **yes for 0:48-1:10, no at 1:16**; caption over the lit cell **yes**; stray grid cells **final
frame yes, the three mid-film map shots no**; music hard stop **yes**; illustration note **no longer late, still tiny**.
Claimed open: unsourced interchange claim **confirmed open** (1:05-1:10, 3:59-4:07); fast passages **confirmed**,
and there are five, not three (20.3-25.0 s, 25.4-27.5, 158.1-160.9, 205.6-206.9, 208.7-209.8); weak first 8 s
**confirmed**; "last year" **confirmed, six times**.

## 2. New issues (introduced by the fixes, or missed in v1)

| # | Time | Sev | What | Suggested fix |
|---|---|---|---|---|
| N1 | 0:28.9-0:30.4 | FIX | Empty black frame. Lit pixels above the caption are 0.00% from 0:29.0 to 0:29.7 and under 0.4% for 1.4 s, then one 120 px box appears. With the labels dimmed, the transit that used to show ghost text now shows nothing; in a no-cuts film it reads as a dropout, 29 s in. | Travel straight from the map's café pin to the café node with the wire as the carried object; keep one lit element in frame for the whole move. |
| N2 | 2:34.5-2:35.5 | FIX | The meters scene shrinks to a thumbnail at the top edge (2:34.5), the frame is near-empty at 2:35.0 (0.03-0.5% lit for about 0.6 s), then giant chopped map glyphs and "080W" cut by the left edge. | Pull straight out from the $40.0 billion bar to the grid; do not pass the map. |
| N3 | 3:31.9-3:35.5 | FIX | 3.6 s where the only thing on screen is one 13 px line ("Shops have been taking Visa to court over this fee for years.") in a black frame (under 1% lit). At 3:32 a cut node and a clipped "unpaid" tag hang on the left edge. Caused by moving the litigation column away from the nodes. | Bring "$2.5 billion" in with the first line, or hold the red arc in the left third while the column builds on the right. |
| N4 | 3:36-4:07 | FIX | The verdict column fills the left 45% of the frame; the right half is empty black for 31 s. The film's conclusion ("Visa's real product is the rulebook…") is set about 20 px, its supporting notes 7-8 px. Lead subject is far under CRAFT's 60-85%. | Frame tighter (column fills the width) or put the red arc and the four nodes in the right half so the verdict is read against the drawing. |
| N5 | 4:00-4:07 | FIX | The column scrolls up into the top edge: "Shops have been taking…" is sliced off at 4:00, "$2.5 billion" sits on the edge and is clipped at 4:04-4:07 while the shop advice appears below it. | Dim and release the upper lines before scrolling, or stop the scroll 40 px earlier. |
| N6 | 0:13.5-0:15.5 | FIX | Pile-up on the pull-back: "$17 trillion" is half behind the caption plate and its mono line is cut ("…volume on the ne"); "A bank, Ohio" touches the illustration note line; the "approved" tag is clipped to "proved"; the arc is chopped by the top edge; "each cell $100 billion moved" sits on the bottom edge. | Hold the map 0.5 s longer, then move; land the headline in the upper two thirds before the caption changes. |
| N7 | 3:29.3-3:31.5 | FIX | The only 3 s the red arc is in shot also carry chopped neighbours: "hat Visa charges the banks" / "arges the banks" and a meter row cut by the bottom-left corner and partly under the caption plate; a cut box on the left edge; then "cial institution.” " sliced by the left edge at 3:31.5. | Frame the arc 80 px higher and tighter, or dim the meters to 0 while the arc is red. |
| N8 | 4:07.7-4:08.7 | NICE | Whip back to the map: the whole drawing passes as a thumbnail with chopped meters down the left edge and the red arc visible for 5 frames, then giant map glyphs. | Fade the red before leaving; one direct pull-out. |
| N9 | 1:48-2:16 | NICE | The travelling message ticks on meter 02 run along its own label row and print over "02 data processing · a charge on every message". | Run the ticks 12 px above the label or along the bar. |
| N10 | 0:00.0 | NICE | Frame 0 is the header, a faint ring and dim map glyphs on the right; "A café, Lisbon" is absent and fades in over the first 1.5 s. As a fallback thumbnail it is nearly black. (Same in v1.) | Start with the label and pin already drawn. |
| N11 | 0:12-0:13 | NICE | "A café, Lisbon" is cut by the right edge ("Lisbo") while the answer returns. | Frame 60 px right. |

No flash was found (no luma spike of 8 or more that returns within 3 frames). No frozen stretch of 1 s or more
(frozen share 2.3%, near-still 10.9%: same as v1).

## 3. Sound (measured)

| Measure | v1 | v2 | Target |
|---|---|---|---|
| Integrated loudness | -14.0 LUFS | -14.0 LUFS | -14 |
| True peak | -1.9 dBFS | -1.9 dBFS | at or below -1 |
| Loudness range | 1.4 LU | 1.4 LU | (very flat) |
| Max sample / clipped samples | 0.777 / 0 | 0.777 / 0 | none |
| Voice lines RMS | -16.9 dB | -16.9 dB | |
| Gaps between lines (12 gaps, 0.3-0.5 s) | -26.5 dB median | -26.5 dB median | |
| Bed alone (after last word, 4:15.0) | -34.3 dB | -34.6 dB | |
| Last 0.25 s / last 50 ms | -34.1 / -37.3 dB | -59.6 / -78.1 dB | faded |
| Per-10 s RMS | -16.8 to -17.6 | -16.8 to -17.6 | consistent |

The fade is real: about 3 s, monotonic from -34.6 dB to silence, no click (last sample 1e-7). Everything else is
identical to v1. Music under lines cannot be separated from the voice, but the bed measures -35 dB alone and the
gaps (which include voice tails) -26.5 dB, so the bed is still about 18 dB under the voice and is not lifted
between lines. No clipping, no digital silence, L/R balanced, no effect louder than the voice.

## 4. Verdict

Sound is publishable as it stands: loudness, peak and the new fade are on target, and the quiet bed is a taste
note. The picture is not there yet. Six of the things the owner could see are really gone (the black slabs, the
leftovers down the edge of the verdict, the second red, the struck-through number, the caption on the lit cell, the
grid in the final frame), but the largest picture problem was only repainted: the camera still makes the same three
detours through the grid and the map (0:26-0:30, 2:34-2:39, 3:25.5-3:29.5), the giant labels are dimmed rather than
gone, and two of those transits now pass through an empty black frame. Moving the verdict column bought a clean
left edge at the cost of 3.6 s of one small line in a void and a half-empty frame for the film's last 36 s of
argument, with the red arc out of shot. Fifteen of the 29 v1 items were not touched at all, including the
neighbour text that lingers and gets sliced in the meters scene, the collisions inside the lit cell, the tiny notes
and the small boxes in an empty frame. Apart from the content items the builder listed as open, I would not upload
this render: one more pass that reroutes the three transits as single direct moves, reframes 3:29-4:07, and clears
items 9, 12 and 13 would make the picture publishable. The spoken interchange claim (item 4) remains a hard stop
on its own.
