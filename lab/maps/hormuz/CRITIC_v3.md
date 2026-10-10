**VERDICT: FIX THEN UPLOAD.** The fixes are three on-screen strings, about 20 minutes with no re-voice: the old channel name "MAPS & POWER · 01" is on screen at 0:23-0:32 of a The Curve upload; the verdict_05 caption says something different from the voice; and one map has no "drawn schematically" note. Both re-voices landed, the sound is on target, the facts hold, and the restyle (style F) is upload-grade.

Critic round 3 · HORMUZ_v3.mp4 (9:35.4, 1920x1080, 24 fps, x264 CRF 16) · independent critic, did not build the film · 10 Oct 2026
Evidence: `out/critic_v3/` (p480_0-3.jpg are 480 px sheets, about one frame every 6 s; ch_*.jpg are 8 fps strips across chapter crossings; f/ holds the full-res frames; frame0.png, loudness.txt, motion.txt, revoiced_transcripts.txt, mix.wav)

## 1. Items carried over from CRITIC_v2

| v2 item | Status | Evidence |
|---|---|---|
| verdict_05 re-voice ("a tax" heard for "attacks") | **FIXED** | small.en: "the first is more strikes near Fujaira". medium: "more strikes near Fujairah and on the East-West pipeline, the routes that kept the oil flowing." |
| open_00 "crude" heard as "crewed" | **FIXED** | Both models: "Middle East crude oil exports are back to about where they were before the war." The first word still lands at 0.40 s (LEAD holds). |
| 3. Chapter card overlaps outgoing card and incoming map | **STILL PRESENT** | ch_500.0.jpg: "$3.12 $4.35" ghosts beside "THE VERDICT" (8:21.0), a "$4.35" fragment hangs top-left for about 0.75 s, then the map wipes in under the title at full opacity. ch_284.2.jpg: one frame reads "A PERMISSION ~~AROUND~~ SYSTEM" (4:45.2). LOW. |
| 4. Labels covering what they name; around_10 source line | **PARTLY** | "STRAIT OF HORMUZ" no longer covers Musandam (frame 0), but its swipe sits over the inbound lane's west end and the route junction (0:00-0:10, 9:18-end). "OCTOBER" (6:14-6:20) still sits on the route and the strait, and that map still has no schematic note (its caption is only "RELIEF: NOAA ETOPO 2022"). |
| 5. Tiny chrome at 480 px | **NOT FIXED** | Source lines are about 15 px tall at 1080p, so about 4 px at 480. Card headers ("CMP 08.05 · 19.0°N") are also about 4 px. Pin sub-labels are about 5 px. Captions, swipe labels and numbers read. Acceptable as texture. |
| 6. "Now follow it out into the world" (2:07) shows a bare world map | **PARTLY** | f/h_128.6: bare map, then the 84% card. The routes fan out at 2:15 on the China line (f/h_138), so the payoff arrives about 6 s late. |
| S2. The bed vanishes on phone speakers | **PARTLY** | See §3. Above 200 Hz the bed is about 5 dB louder than in v2, but it is still 22-27 dB under the voice. |
| v1/v2 identity items (teal palette, speckles, numbers on black) | **Teal: FIXED. Speckles and numbers on black: STILL PRESENT** | The style F palette replaces the teal. Small `:::` dot clusters still drift in the background (f/f_393 at 90,140, 1160,180, 1450,180). 33 of the 77 beats (43%) are number or split cards on black, the same as v1. |

## 2. New problems from the restyle

**MUST FIX (strings; re-render 3 segments; audio unchanged)**
1. **The old channel name is on screen.** At 0:23-0:32 the world-map source line reads "MAPS & POWER · 01" (f/z_27_caption.png). It sits in the hook window of a The Curve film. `script.py` line 155: `"caption": "MAPS & POWER · 01"` → `"caption": "COASTLINES: NATURAL EARTH"`.
2. **verdict_05: the caption does not match the voice.** At 8:51 the screen says "the first is attacks around Fujairah", but the voice says "more strikes near Fujairah". Change the shown half of the beat-5 tuple in the verdict chapter to: `"If I had to watch three things, the first is more strikes near Fujairah and on the East-West pipeline, the routes that kept the oil flowing."`
3. **around_10 (6:14-6:20) breaks the house rule "anything schematic says so on screen".** Line 313: `"caption": ""` → `"caption": "CORRIDOR DRAWN SCHEMATICALLY"` (the engine appends "RELIEF: NOAA ETOPO 2022" on its own). While there, move the label off the route. Line 312: `(56.62, 26.0, "OCTOBER", ...)` → `(54.9, 26.2, "OCTOBER", ...)`, which puts it in open Gulf water west of Musandam, clear of the corridor (it starts at about 56.0E). Check the frame after the render.

Re-render segments 0000, 0360 and 0480, then re-concat with the existing mix.

**OPTIONAL (does not block upload; do it on the next film or if you re-render anyway)**
4. **The colour language contradicts itself.** In style F, magenta means Iran and green means Oman. At 1:27 the split card sets IRAN in cyan (the chapter hero colour) and OMAN in white, seconds after the Iranian islands were labelled magenta. At 0:11, "8" on the split card is yellow, while 8 SHIPS on the map was violet (data). Rule: a word that names an entity takes that entity's colour; the hero colour goes to the chrome (chapter label, progress rule, card ticks). For gap_06: OMAN green, IRAN magenta.
5. **The relief makes land and sea muddy at phone size.** Measured on f/f_75: land averages 16-19/255 and Gulf water 4/255, but the dense deep bathymetry in the Gulf of Oman reaches 13/255, the same brightness as land. At 480 px only the hatched coast separates them. Fix in `flow.py` (relief draw): draw sea contours only to −100 m plus every third deeper isobath, at 40% opacity, and raise the land stipple brightness about 1.5×.
6. **Labels sit on routes.** QESHM's swipe covers the inbound lane's west end (1:12-1:19, f/f_75), so nudge QESHM's label anchor 0.15° west. "8 OCT" sits over Musandam and the strait (6:47-6:56). These are small.
7. **The price chapter is 66 s of cards with no map** (7:15-8:20, nine beats in a row). The film's longest map gap falls near the 7-8 minute dip. Turn price_00 ("every shuttle... needs ships") into a map beat that reuses the shuttle map from around_05.
8. **Burned-in full captions on a long film.** CRAFT §9.5 (10 Oct) says long films get keyword overlays plus CC, not full captions. This is a channel-level choice, so flag it to the owner rather than change it here.
9. **The film looks different from the rest of The Curve.** Style F looks nothing like The Curve's other films (teal, rail). That is fine if style F becomes The Curve's look from now on. Otherwise the channel will look like two channels. The owner should decide.

**Checked and clean:** no glyph boxes (½, ≈, →, –, ° all render), no debug text, no clipped overlays. The neon event rings flicker on once (3-4 frames: 9→18→22→9→72, then steady at about 27) and do not buzz. Large-area flash test: 0 opposing-quadrant flashes over 20/255 within ⅓ s, so no photosensitivity risk. The halftone cards do not shimmer more than the camera drift (frame-to-frame difference 11.95 vs 12.62 for a solid number). The particle routes read as solid lines at 480 px. Map positions spot-checked: Greater Tunb, Lesser Tunb, Abu Musa, Qeshm, Hormuz, Larak, the 7 Oct hit (27.0N 51.2E, 94 km north of Qatar) and the 8 Oct hit off Fujairah all match FACTCHECK. On-screen figures re-read against FACTCHECK: 30 of 30 match. Frame 0 works as a fallback thumbnail, although its bottom fifth is empty.

## 3. Sound

| Measure | v3 | Target / v2 |
|---|---|---|
| Integrated (ebur128) | **-14.1 LUFS** | -14 ✓ |
| True peak | **-2.9 dBTP** | ≤ -1 ✓ |
| LRA | 2.0 LU | ✓ |
| Speech RMS (line windows) | -17.0 dB, -18.6 dB above 200 Hz | — |
| Bed alone, 8 chapter gaps | -30 to -35 dB, so **13-18 dB under the voice** | ≥ 12 ✓ |
| Bed 200-900 Hz in the gaps (phone-speaker proxy) | -42 to -47 dB vs speech -20.1 dB in the same band, so **22-27 dB under** | v2: 27 dB under above 150 Hz |
| Bed stem band balance | 20-60 Hz 6.8%, **60-200 Hz 88.5%**, 200-500 Hz 4.3%, above 500 Hz 0.4% | v2: 79% sub |
| Motion | frozen 0.6 s (0%), near-still 5.4 s (1%), no stretch ≥ 2 s | ✓ |
| Dips to near-black (d ≥ 0.2 s) | 7 | v2: 7 |

The new upper partials (220/294/349 Hz) moved the energy out of the sub, but mostly into 60-200 Hz, which phone speakers do not reproduce. On a phone you will hear a faint 294 Hz tone in the 3-s chapter gaps. Under narration (the sidechain duck takes it lower) it is effectively gone. That is acceptable for a voice-led documentary. If wanted, in `mix_flow.py` `drone()`, raise the 293.66 and 349.23 partial amplitudes to 0.30/0.18, add (440.0, 0.08, 29.0), and keep the bed ≥ 15 dB under the voice.

## 4. Date-sensitive figures to re-check on upload day (FACTCHECK §3, plus one new)
1. **Strait status and talks.** A reopening, a deal or a new closure would make the title's "Is Closed" false. This is the only check that can block the title.
2. **NEW: "this month."** around_10 and the October chapter say "this month" for October. Publish before 1 Nov.
3. Windward daily: 8 transits on 8 Oct, 11.13m / 9.09m bbl on 7 Oct (dated on screen).
4. Brent pair: $99.57 futures (intraday) vs $125.44 spot, both 6 Oct. After mid-October, consider a pinned comment with a same-day pair.
5. IEA October OMR (about mid-October): -507 mb (Feb to end-Aug) and the -2.5 mb/d 2026 forecast. If it is out, pin the update.
6. UKMTO / Kpler: 9 attacks 1-6 Oct, ~18 in September, 18.3 mb/d provisional (Kpler revises).
7. GASREGW: $4.35 on 5 Oct 2026. The next print is Mon 12 Oct; the card is dated, so it stays true.

## 5. POST.md
Rewritten for The Curve, with the sources kept:
- The title stays **"Hormuz Is Closed. The Oil Isn't."** (32 characters), and the thumbnail is **8 SHIPS**.
- There are three Test & Compare pairs, each with its promise on screen before 1:00.
- Chapters are recomputed from the v3 lines.json: 0:00, 0:39, 1:36, 2:31, 3:43, 4:45, **6:22, 7:13, 8:21**. The last three each moved 1 s from v2.
- The description now says the maps are drawn schematically and the relief is NOAA ETOPO 2022, names the synthetic voice and the code-made music, and adds the ETOPO and Natural Earth sources.

## 6. For CRAFT "Learned"
10 Oct (Hormuz v3): a placeholder channel name survived in a map caption string ("MAPS & POWER · 01") after the channel changed. When a film changes channel, grep the script for the old name in every string, not just TAG.
