**VERDICT: FIX THEN UPLOAD.** Two re-voices are needed: the verdict's first watch-item is still heard as "a tax", and the hook still says "crewed". The maps are now upload-grade. The palette is still The Curve's teal.

Critic round 2 · HORMUZ_v2.mp4 (9:34.6, 1920x1080, 24 fps) · independent critic, did not build the film · 9 Oct 2026
Evidence: `out/critic_v2/` (p480_0-7.jpg are 480 px phone-width sheets every 6 s; ch_*.jpg are strips at each chapter crossing; frame0.png, f_*.png, transcripts.txt, loudness.txt, black.txt, mix.wav, spec_ch2.png)

## v1 HIGH / MEDIUM items

| # | Item | Status | Evidence |
|---|---|---|---|
| H1 | Visually The Curve with maps added | **PARTLY** | Done: the numbered rail is gone, replaced by a chapter name and a live coordinate readout top-right ("09 THE VERDICT · 26.02°N 056.16°E"). Cards now sit in ruled chart frames with corner ticks and a "FIG 04.03 · 26.5°N" header. Map-to-map moves are camera zooms. **Not done:** the palette is still teal/white/red. No theme block exists (`THEME` is not in script.py or flow.py). The "■ MAPS & POWER" top-left tag is the same. 24+ number cards still sit on black instead of on the map (20M, 9, 7M, 84%). The IEA quote (2:48) is in a ruled box, not a notice-to-mariners slip. Glyph speckles are still drifting outside the plate (frame0 at 330,920 and 1730,1030; f_376 at 1390,100). |
| H2 | Coast does not read as coast | **FIXED** | Coast glyphs are now oriented (`/ \ |`) over a stroked contour, the sea has a fill plus a faint `~` texture, and land is dotted. Qeshm is separate from the mainland, and Hormuz, Larak and the Tunbs read as outlined islands (frame0, f_566). The world view at 7:06 reads (India, Malaya, Japan). |
| H3 | Overlays spill out of the plate | **FIXED** | around_05 (5:24-5:33), october_03 (6:42) and verdict_10 (9:18-9:32) all now sit inside a plate that runs to 25.5N. No pin or route crosses the ruler. |
| M1 | Dip to black between beats | **FIXED** | blackdetect (d=0.2, pix_th=0.06) finds **70 dips in v1 and 7 in v2**, all 0.21-0.42 s. The longest is still 3:15.7 (0.42 s, before "false starts"). Map-to-map moves are now continuous. Cards push sideways. |
| M2 | Mangled names (faster_whisper small.en on the final mix) | **PARTLY** | See the table below. Five are fixed. **verdict_05 and the open_00 "crude" are not.** |
| M3 | Wrong-genre music | **FIXED (with a caveat)** | The bed is a beatless D-minor drone with no drums, at 17.5 dB under speech. **Caveat:** 79% of its energy is the 36.7 Hz sub. Above 150 Hz it sits 27 dB under the voice, so **on phone speakers the bed effectively disappears**. See S2. |
| M4 | Frame 0 bare | **FIXED** | Frame 0 shows the narrows with lanes, route, "8 SHIPS · 5 IN · 3 OUT · WINDWARD" and "STRAIT OF HORMUZ · 26.6N 56.4E · 8 OCT 2026". The ruler is uncropped. It works as the thumbnail fallback. |

**Score: 5 fixed, 2 partly, 0 not fixed** (of 7 HIGH/MEDIUM).

### Re-voiced lines, as heard
| Line | Time | Heard | Status |
|---|---|---|---|
| **open_00** (not re-voiced) | 0:07 | "Middle East **crewed** exports" | **NOT FIXED.** It is in the hook. v1 listed 0:07. |
| gap_05 | 1:19 | "the two **tombs**" | OK. "Toonbs" ≈ the correct pronunciation. |
| flows_05 | 2:09 | "crude oil" | FIXED |
| closing_04 | 2:59 | "crude oil" | FIXED |
| closing_06 | 3:16 | "false starts" | FIXED |
| around_07 / _08 | 5:45, 5:53 | "Kepler" ×2 | FIXED |
| october_04 | 6:46 | "Fujairah" | FIXED |
| october_05 | 6:56 | "Fujaira is where…" | OK |
| **verdict_05** | 8:50 | "the first is **a tax near Fujaira**" | **NOT FIXED.** The comma did not help, because "attacks" is still heard as "a tax". |

## New problems the rebuild introduced

1. **MEDIUM: verdict_05 is still unintelligible on its key word.** Change the spoken text to *"the first is, more strikes near Foo-jai-rah and on the East-West pipeline, the routes that kept the oil flowing."* ("strikes" cannot be misheard as "a tax".) Keep the shown caption as written, or change it to "strikes" to match.
2. **MEDIUM: open_00 "crude" → "crewed" at 0:07, in the first sentence.** Change the spoken text to "Middle East crude oil exports". Re-voice open_00 and check the 0.4 s LEAD still lands.
3. **LOW: chapter cards overlap the outgoing card and the incoming map** (ch_*.jpg, verdict at 8:20-8:22, way-around at 4:44). For about 0.5 s the previous card's fragment ("$4.35") sits beside "CHAPTER 09 THE VERDICT", and the next map plate wipes in under the title while it is still at full opacity, so "THE VERDICT" ghosts over the map. Fix: finish the outgoing push before the chapter card's in-point, and start the map only after the title's out-fade ends (sequence them, don't overlap).
4. **LOW: label backplates cover the place they name.** "STRAIT OF HORMUZ" (frame0, f_566) and "OCTOBER" (f_376, 6:12-6:20) blank the Musandam tip, and at 6:12 the start of the route. Set these labels in open water north-west (around 26.2N 55.6E) with a leader line, or shrink the plate to the text bbox at 70% opacity. The around_10 map (6:12-6:20) also has **no source line**, so add "CORRIDOR DRAWN SCHEMATICALLY".
5. **LOW: tiny chrome at 480 px wide.** Card headers ("FIG 04.03 · 26.5°N 056.3°E") are about 3 px tall, the top-right chapter/coord readout and source lines about 4-5 px, and pin sub-labels ("IRAN · 27.2N 56.3E") about 6 px. Captions (about 9 px) and big labels read. This is acceptable as texture, but v1 L5 (sub-lines ≥ 22 px, source ≥ 20 px at 1080p) is not done. Raise the source line and pin sub-labels to 22 px.
6. **LOW: "Now follow it out into the world" (2:07) zooms to a bare world map, then cuts to a "84%" number card on black.** That is the payoff moment, and it should show the routes fanning to Asia on that map (v1 L6). The routes exist at 7:06, so reuse them here.
7. **Checked and clean:** no glyph boxes (tofu), no debug text, no clipped overlays. The push transitions half-frame cards for about 0.25 s, which is intentional. The end card does not collide with the map.

## Sound

| Measure | Value | Target |
|---|---|---|
| Integrated | **-14.0 LUFS** | -14 ✓ |
| True peak | **-2.5 dBTP** | ≤ -1 ✓ |
| LRA | 2.0 LU | — |
| Speech RMS | -17.0 dB | — |
| Bed alone (chapter gaps, about 3 s) | -34.5 dB → **17.5 dB under speech** | ≥ 12 ✓ |
| Bed in 0.3 s line gaps (ducked) | -38.2 dB → 21.2 dB under | ✓ |
| Bed above 150 Hz (phone-speaker proxy) | **27.1 dB under speech** | effectively inaudible |
| Bed file: DC offset | -1.6e-5 / -1.4e-5 | ✓ none |
| Bed file: peak / clipped samples | 0.27 / 0 | ✓ |
| Bed file: max sample step | 0.017 | ✓ no clicks |
| Sonar ping (1180 Hz) at the 8 chapter crossings | about -40 dB RMS, about 23 dB under speech, 3-tap decay | audible, not harsh ✓ |
| Mix: largest sample steps (0.7) | at 0:43.9, 3:14.9, 4:46.9, 8:22.6, 8:25.2 | These are 8-10 kHz sibilance bursts in the voice (the dry take steps only 0.2), from highshelf +4 dB → compressor. They are not splice clicks. **Listen on headphones for harsh "s".** If harsh, set the de-esser to `i=0.5` or cut the highshelf to +2 dB. |

- **S2 (LOW, for the next film):** the drone's band balance is 79% at 30-60 Hz, 21% at 60-200 Hz and about 0% above 200 Hz, and the "VHF static" layer contributes nothing measurable. Raise the 146.8/174.6 Hz partials by 6 dB and lift the static 3-4× so the bed survives phone speakers. Keep the 17 dB headroom under voice.

## Chapters (ready to paste)
Floor starts from flow/lines.json minus 1.6 s: 39.59, 96.45, 151.02, 223.18, 285.14, 381.79, 432.90, 500.91. Recompute if open_00 is re-timed.
```
CHAPTERS
0:00 Eight ships, and the oil still moves
0:39 The gap
1:36 What flows through it
2:31 The closing
3:43 How to close a strait
4:45 The way around
6:21 October: the attacks follow the oil
7:12 The price of a detour
8:20 The verdict
```
(Three timestamps moved by 1 s since v1: closing 2:31, how 3:43, around 4:45, price 7:12, verdict 8:20. Use these.)

## Fix order
1. Re-voice **verdict_05** ("more strikes near Foo-jai-rah") and **open_00** ("crude oil exports"), remix, and re-check the transcript. About 10 minutes.
2. Re-measure chapters if open_00's length changes, then paste.
3. Optional before upload: sequence the chapter-card in/out (item 3) and move the two covering labels (item 4).
4. Next channel pass, not a blocker for this film: the theme block (amber `#F2A93B` on blue-black, teal removed, no speckles, numbers on the map). That remains the channel's biggest identity risk, and is what separates it from The Curve.

STALE-RISK (unchanged): re-pull Windward 8 ships/11.1M, Kpler 18.3M, FRED Brent spot, GASREGW and IEA −507M on upload day.
