**VERDICT: FIX THEN UPLOAD.** The facts, the argument and the verdict are upload-grade. The picture is not yet its own channel, and the maps read as static at phone size.

Critic round 1 · HORMUZ_v1.mp4 (9:32.7, 1920x1080, 24 fps) · independent critic, did not build the film · 9 Oct 2026
Evidence: `out/critic/` (sheetA/B/C.jpg every 8 s, `full/` map grabs, strips.jpg, phone_maps.png, transcript.txt, loudness.txt, black.txt, motion.txt)

## Scores
| Area | Score | One line |
|---|---|---|
| Hook / frame 0 | 6 | The twist is in the first sentence (good), but frame 0 is a bare, unlabelled map texture. |
| Readability at 360 px | 5 | Big labels read. Mono sub-lines, rulers and source lines do not. The coastline reads as noise. |
| Motion | 7 | Frozen 1%, near-still 2%, no stretch ≥ 2 s. But 44 dips to near-black (0.33-1.0 s), one per beat. |
| Variety / composition | 5 | Maps are 38% of the runtime. The rest is The Curve's split, number, words and quote cards. |
| Accuracy | 9 | Every on-screen figure I spot-checked (20) matches FACTCHECK.md. The map geometry fixes landed, apart from the overflow below. |
| Sound | 6 | Loudness is on target. The garage bed is the wrong genre, and two place names are mangled. |
| Authorship | 5 | The narration has a voice ("My answer", "If I am reading this correctly", three things to watch). The chrome is The Curve's, pixel for pixel. |

## Problems by severity

### HIGH (fix before upload)

**H1. The channel is visually The Curve with maps added.** Same top-left tag, same numbered 01-09 rail with a typed chapter name, same teal/white/red palette, same split, number, words and quote cards, same caption plate with progressive white-on-grey words, same typed mono sub-lines with a block cursor, same drifting glyph speckles in the background (compare `lab/curvelf/lf03_held/LF03_FLOW_v5.mp4` at 1:35 and 3:20). CRAFT Learned 9 Oct (3) already says each new channel needs its own visible look before launch. This is the single biggest risk to the channel's monetisation. Fixes, in order of yield:
1. **A theme block per script, read by `flow.py`** (`THEME = dict(palette=..., rail=False, corner="coords", cards="chart", speckles=False, cap_font=...)`). Maps palette: water `#07121C` (blue-black, so the sea has a colour), land glyphs warm grey `#8C877D`, routes and accents **amber `#F2A93B`**, danger red `#E5533D`, with teal removed entirely. One accent colour that is not The Curve's.
2. **Drop the numbered rail** (`rail=False`). Put a live **coordinate readout** top-left that tracks the camera centre ("26.6N 56.4E · 1:2,000,000"), plus a scale bar in km/nmi bottom-right. That is the brand promised in CHANNEL.md.
3. **Put the numbers on the map, not on black.** Twenty-four of the 77 beats are full-screen split/number cards. Re-set them as callout plates anchored to their place over a dimmed map: flows_00 20M on the strait, around_01 7M on the pipeline, october_00 "9" on the narrows with the six pins, price_* in a chart-style title block. Where a card has to be full-screen, style it as a **nautical chart title block** (ruled box, small caps serif title, mono data rows) rather than The Curve's centred big number.
4. **Quote card (closing_02, the IEA line):** set it as a teleprinter/"notice to mariners" slip (mono, ruled, date-time group header), not The Curve's quote mark.
5. **Transitions:** map-to-map beats should be one continuous camera (nested zooms: narrows → Gulf → world → narrows) with no fade. See M1.

**H2. The coastline does not read as a coastline at phone size** (phone_maps.png; full/f_0044, f_0074). Glyphs `#+%*` are chosen at random per cell, so the shore flickers like corrupted text. Land is filled with `:` dots and the sea is empty black, so a viewer has to work out which side is water. At V_NARROWS, **Qeshm merges into the Iranian mainland** (the Clarence channel is not drawn), so "the islands that overlook them" (gap_04) shows three pins on one landmass. The Musandam hook is recognisable once you know it. Hormuz and Larak are single glyph clumps. Engine fix in `lab/curvelf/flow.py`:
- `map_pics` / `land_rings`: choose the glyph **by distance to the coast**, not at random: `#` on the shoreline cell, `+` one cell in, `·` beyond. Also **stroke the coast ring itself** as a 1.5 px vector line under the glyphs, so the contour is continuous.
- Give the sea a fill (`#07121C`) and one or two faint depth contours or a 2-nmi hatch, so water reads as water.
- Scale glyph cell size with the view span (`map_frame`): about half the current cell at V_NARROWS (1.2° wide), so Qeshm, Hormuz, Larak and the Quoins separate. Islands under 2 cells get a minimum solid dot.
- The world view (open_03 at 0:24, flows_05/06 at 2:12-2:20) is unreadable at this cell size. India, the Malay peninsula and Japan dissolve. Either use a coarser simplified land set at world scale or switch that beat to a stroked outline.

**H3. Map overlays spill out of the map plate.** V_NARROWS is `(55.85, 26.1, 57.05, 27.0)`, but `OCT_HITS` has pins at 25.97N, `Z_SOUTH` runs to 25.90N and `R_SHUTTLE` to 25.40N. In the render the corridor, pins and routes drop below the longitude ruler toward the caption band: october_03 at 6:40-6:46 (pin and hatched corridor under the axis), around_05 at 5:28-5:33 (the "SHIP-TO-SHIP" pin sits under the ruler), and verdict_10 at 9:18-9:32 (the route runs off the bottom of the frame). Fix both:
(a) In `draw_map`, `clipRect` routes, zones and pins to `(bx, by, w, h)`.
(b) Give those beats a view that contains the data: `V_NARROWS_S = (55.85, 25.35, 57.05, 27.0)` for around_05, october_03 and verdict_10.
Also check two `OCT_HITS` pins, (56.46, 26.40) and (56.48, 26.26): at this cell size they render on top of the Musandam shore glyphs and read as hits on land.

### MEDIUM

**M1. A dip to near-black between almost every beat.** blackdetect found 44 dips of 0.33-1.0 s (list in black.txt; the longest is 3:14.9-3:15.9, before "Then came months of false dawns"). This is CRAFT §3's banned "everything fading", and it breaks the one-object-carries-across rule. Fix in `draw_map` (`leave`/`am`) and the card renderers: when beat i and i+1 are both maps, cross-move the camera instead of fading. Card ↔ map should push the card through the camera (CRAFT §3, "the foreground becomes the transition"). The 8-SHIPS pin is the obvious carried object.

**M2. Names the voice mangles** (faster_whisper small.en on the final mix, transcript.txt):
| Time | Said as | Fix (spoken text via the `(shown, said)` tuple) |
|---|---|---|
| 5:44, 5:52 (around_07, around_08) | **Kpler → "Capella"** | said "Kepler" |
| 6:53, 6:57 (october_04, _05) | Fujairah → "Fujaira" | said "Foo-JAI-rah" |
| **8:48 (verdict_05)** | "attacks around Fujairah" → **"a tax around Fajera"**. This is the verdict's first watch-item, and it is unintelligible. | said "attacks near Foo-JAI-rah", and add a comma pause before it |
| 0:07, 2:09, 2:58 | "crude" → "crewed/crew" (×3) | said "crude oil" at 2:09 and 2:58 |
| 3:15 (closing_06) | "false dawns" → "false storms" | said "false dawns" with a comma, or reword "months of false starts" |
| 1:11 (gap_04) | Qeshm → "Keshum" | acceptable. Optionally said "Gheshm" |
| 1:18 (gap_05) | Tunbs → "Tums" | said "Toonbs" |
Larak, Great Quoin ("coin" is correct), Hormuz, Musandam (not spoken), Habshan, Abqaiq, Yanbu and UKMTO are all clear. No cut-off lines. Every one of the 77 lines ends cleanly.

**M3. The music is the wrong genre.** `flow/garage.wav` is a 2-step garage bed, about 132 BPM (librosa reads 66, half-time). The film covers stranded seafarers, missile strikes and burning tankers, and a shuffling club groove under that undercuts the narrator's authority. It is also The Curve's sonic identity. **Recommendation:** a dark, slow pulse bed, 70-80 BPM or beatless, minor-key drone with a sub pulse and sparse metallic or sonar pings, plus a faint VHF/radio-static texture as the channel's sound motif (it ties to the IRGC radio warnings). No drums, or a very light low tom on chapter turns. Mix the bed about 12 dB under the voice (it currently sits at about -24 dB RMS in voice gaps against -17 dB under speech, which is too present for a news film). Make it this channel's fixed sonic signature.

**M4. Frame 0 / thumbnail fallback.** OPEN_RESOLVED and LEAD 0.4 are set, but frame 0 is the narrows map with no labels, no route, no lanes and a clipped latitude ruler ("7.0N", "6.8N": the left edge is cut while the camera settles). For open_00, make the labels, Z_INBOUND/Z_OUTBOUND and the route present at t=0, and start the camera already framed so the ruler isn't cropped. Then frame 0 is the "8 SHIPS · STRAIT OF HORMUZ" image.

### LOW
- **L1. gap_05 (1:18-1:26):** the LESSER TUNB and GREATER TUNB labels sit stacked, and Lesser's stem runs through Greater's pin halo. A stray white anchor ring sits under Lesser Tunb (f_0082: 636,597). ABU MUSA arrives ghosted, and its dark backplate covers the Musandam coast. Fan the labels left/up, and drop the backplate when a label sits on the sea.
- **L2. gap_04 (1:11):** HORMUZ's label backplate blanks the Iranian coast east of Bandar Abbas. Shrink the plate to the text bbox or set the label in the water to the south-east.
- **L3. Long holds on one card:** 6:00-6:13 (the "~½ vs ≈ PRE-WAR" split, 11 s) and 8:23-8:39 ("IT TAXES EVERY BARREL", 16 s across the whole verdict). The verdict deserves a picture. Use the narrows map with a tollgate bar across the lanes and the bypass routes lit in amber, then cut to the words card on "tollgate".
- **L4. Background glyph speckles** (small `:::` patches drifting outside the plate, e.g. f_0000 at 1110,420 and 270,960) read as dirt. Drop them for this channel.
- **L5.** The mono sub-lines (about 13-15 px at 1080p) and the source lines are under 4 px tall on a 360-px phone. Raise the sub-lines to ≥ 22 px and the source line to ≥ 20 px.
- **L6.** The world map beat at open_03 (0:22-0:31) shows nothing but a dot. Either show the routes fanning to Asia there (a first payoff) or cut it.

## What works (keep it)
- The thesis lands in sentence one, and the narration has a real point of view: "a tollgate, not a tap", "the attacks are following the oil", three things to watch. That is authorship in the CRAFT §1 sense.
- The map honesty layer: every map carries a source line, "DRAWN SCHEMATICALLY" and "POSITIONS APPROXIMATE". Keep it, it is the brand.
- Pins are where the labels say (spot-checked: Bandar Abbas, Musandam, Qeshm 26.8N 55.8E, Hormuz, Larak, Tunbs, Abu Musa, Ras Tanura, Yanbu, Abqaiq, Habshan, Fujairah, 7 Oct off Qatar ≈ 27.0N). The pipelines are on land. The lanes and the Iran-approved route are on water and pass north of Larak.
- Motion is healthy: frozen 1%, near-still 2%.

## Map-look judgement
The idea, a typographic chart with honest captions, is a real signature. The execution reads as random-glyph static rather than a designed chart. Make the glyphs follow the coast, stroke the contour, colour the sea, and change the palette to amber on blue-black.

## Measurements
| Measure | Value | Target |
|---|---|---|
| Integrated loudness | **-14.1 LUFS** | -14 ✓ |
| True peak | **-2.0 dBFS** | ≤ -1 ✓ |
| LRA | 1.9 LU | — |
| Silence ≥ 1.2 s at -45 dB | none (the music bed runs through) | — |
| Music in voice gaps vs speech (RMS) | about -24 dB vs -17 dB | bed ≥ 12 dB under |
| Frozen / near-still | 4.4 s (1%) / 10.5 s (2%), no stretch ≥ 2 s | ✓ |
| Dips to near-black | 44, 0.33-1.0 s each | 0 between map beats |
| Glyph boxes (missing font) / debug text | none found | ✓ |
| Clipping of overlays outside the map plate | 3 beats (around_05, october_03, verdict_10) | 0 |
| On-screen figures spot-checked vs FACTCHECK | 20 of 20 match (8, ~125, 21 nmi/39 km, 20M, ~20%, >¼, ~⅕, 38%, 84%, 2 Mar, −10M at least, $71.32/$138.21, 6-7 Jul, at least 13, 187 4 Mar-22 Apr, ~0.2%/1%, ≈20,000, 7M, 2.6M, 11.1M/9.1M, ~40%, 18.3M, 9 (1-6 Oct), ~18, 1-3%/25-30%, $99.57/$125.44, −507M Feb-end-Aug, $3.12/$4.35) | ✓ |

STALE-RISK reminder (from FACTCHECK §3): re-pull Windward 8-ships/11.13M, Kpler 18.3M, FRED Brent spot and GASREGW, and check whether the IEA October OMR has replaced −507M, on upload day.

## POST.md: ready to paste
Titles: keep **"Hormuz Is Closed. The Oil Isn't."** (32 chars, it is the thesis). The alternates are fine. The thumbnail "8 SHIPS A DAY" is good, but make it exactly true: the film says 8 ships on 8 Oct, not a daily rate, so use **"8 SHIPS"** or **"8 SHIPS. 1 DAY."**

Replace the CHAPTERS placeholder in POST.md's description with:
```
CHAPTERS
0:00 Eight ships, and the oil still moves
0:39 The gap
1:36 What flows through it
2:30 The closing
3:42 How to close a strait
4:44 The way around
6:21 October: the attacks follow the oil
7:11 The price of a detour
8:19 The verdict
```
(Floors from flow/lines.json: gap 41.19, flows 98.08, closing 152.10, how 224.03, around 285.98, october 382.69, price 432.96, verdict 500.97, each minus 1.6 s. Recompute if the voice is re-timed for M2.)

Description: the current text is good. Add one line under the disclaimer: "Music: [name of the new bed / licence]." Also replace "MAPS & POWER" across the end card and tags once the name is chosen (CHANNEL.md recommends HARD LINES; check the @handle first).

## Priority order for the fix pass
1. H3 overflow (view plus clip): 20 min, then re-render 3 beats.
2. M2 respellings: Kpler, Fujairah ×3, crude ×2, false dawns, Tunbs. Re-voice 8 lines.
3. H2 coast rendering in `map_pics`/`land_rings`/`map_frame`.
4. H1 theme block (palette, no rail, coordinate readout, chart-style cards), plus M3 new music bed. These two together make this a different channel from The Curve.
5. M1 continuous map camera, M4 frame 0, then the LOW items.
Then a new critic for round 2.
