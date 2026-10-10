VERDICT: FIX THEN UPLOAD

# CRITIC v1: TUNNEL_PILOT_v1.mp4 (Datum Line pilot, Fehmarnbelt)

Independent critic pass, 9 Oct 2026. Render: 1920x1080, 24 fps, 700.25 s (11:40 including the end card; the last voice
line ends at 11:29). Judged from the pixels and audio, against CRAFT.md, FACTCHECK.md, CREDITS.md and POST.md.
Working files: `out/critic/` (motion.txt, loudness.txt, ebur128.txt, sheet_00-07.jpg every 8 s, g/ full-size grabs,
asr.txt, phone.jpg).

The film is in good shape. Sound is on target, nothing is frozen, every on-screen number I checked matches the
fact-check, and it has a real verdict. What stops an upload today is mostly labelling and packaging: a false
"AI-GENERATED" tag on code-drawn diagrams, a POST.md with no chapter times and no photo source links, and a wrong
claim in the description.

## Problems by severity

| # | Sev | Where | Problem | Exact fix |
|---|---|---|---|---|
| 1 | HIGH | 14 diagram beats (e.g. 0:42, 2:02, 3:06, 4:42, 5:14, 6:10, 6:18, 7:22, 7:46, 10:02, 10:42, 11:30) | The tag says "ILLUSTRATION · AI-GENERATED", but g01-g22 are drawn in code (`diagrams.py`, skia). That's false, and it hands viewers an "AI slop" reading the film hasn't earned. It's also inconsistent: the 8 diagrams that have a caption (g01, g03, g05, g07, g10, g12, g15, g19) get no tag at all, and only g01/g12 say "ILLUSTRATION" | Engine (`lab/curvelf/flow.py`): let a film override the tag. At line 738, `tg = getattr(SC, "ILLUS", UI["illus"])`. In `script.py` add `ILLUS = "DIAGRAM  ·  DRAWN FOR THIS FILM"`. At line 735, drop the `len(B[i_]["vis"]) < 3` condition so every `img` beat is tagged, including captioned ones. Then remove " · ILLUSTRATION" from the g01 and g12 captions so the label isn't said twice. Don't use "AI" anywhere for these images |
| 2 | HIGH | POST.md, CHAPTERS | No times, so YouTube won't build chapters | Paste the chapter list at the end of this file |
| 3 | HIGH | POST.md, PHOTO CREDITS | CC BY 4.0/2.0 asks for a link to each source "where reasonably practicable", and the 16 Commons URLs are not in the description. POST.md also mixes in internal notes ("Before upload", "paste the Commons links...") that must not be pasted to YouTube | Add one line per photo: `Title – Author – Licence – Commons URL` (URLs are in `src/photo/CREDITS.md`, 16 non-SA rows). The licence line ends with a stray "·": change it to `Licences: CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ · CC BY 2.0 https://creativecommons.org/licenses/by/2.0/ · Public domain: S. Möller, NASA.` Move the internal notes under a heading marked DO NOT PASTE |
| 4 | MED | POST.md description, sentence 1 | "89 concrete elements that each weigh more than 73,500 tonnes" is wrong. Only the 79 standard elements do; the 10 special elements are shorter (39 m) | Change to: "made of 89 concrete elements; each of the 79 standard ones weighs more than 73,500 tonnes." (Narration `open_01` says "blocks that each weigh more than seventy-three thousand tonnes". The card says STANDARD, so that line is LOW and optional.) |
| 5 | MED | 0:00-0:10 hook | Frame 0 is a near-black ASCII blob (see `g/g_0.jpg`). The voice starts at 1.2 s and the satellite photo only resolves at about 3 s. The twist ("about two years late") lands at 9.3 s, outside CRAFT's 8 s. The superlative ("longest of its kind", 2.7 s) is inside it | Engine: make the first beat start already resolved, and cut the voice lead-in to 0.3 s. Script, optional re-voice of `open_00`: "Denmark's eighteen-kilometre tunnel to Germany is running about two years late, and it is the longest tunnel of its kind in the world." This puts the twist at about 4 s |
| 6 | MED | Every frame, top left, and the end card at 11:38 | The brand on screen reads "MEGAPROJECTS". CHANNEL.md picks "Datum Line" | Decide the channel name before upload. If it's Datum Line, set `TAG = "DATUM LINE  ·  THE FEHMARNBELT TUNNEL"` in `script.py`, and change the end-card word, then re-render |
| 7 | MED | Narration, names (whisper small.en, 29 lines) | Heard as: Fehmarn → "Fehmann" (gap_00), Rødbyhavn → "Rödbehaven" (factory_00), Lolland → "Lowland" (gap_00), Øresund → "Ursund"/"Urusund" (method_05, ivy_02), Scandlines → "Scandalines" (gap_01), Puttgarden → "Putgarden" (fine). Femern and Sund & Bælt are never spoken. Whisper errors and TTS errors look the same here, so this is NOT VERIFIED BY EAR | A human listens to 1:00, 1:05, 2:34, 2:50 and 4:55. If "Fehmann" or "Rödbehaven" is really in the voice, respell for ElevenLabs (e.g. "FAY-marn", "RUTH-boo-hown") and re-voice gap_00 and factory_00 only |
| 8 | MED | Whole film (authorship and format risk) | 55 of 94 beats (59%) are type-only cards (18 words, 16 numbers, 9 splits, 7 lists, 3 timelines, 2 quotes). Only 17 are photos. The look (chapter rail, ASCII-to-picture resolve, caption plate) is the same `curvelf/flow.py` engine as The Curve and Money Crimes, so three channels share one look. That is the "mass-produced" pattern CRAFT §1 warns about. Not a blocker for one pilot | For this cut, optional: swap 2-3 "words" cards for a map (the 1-2 km tow in `night_01` "A SHORT DISTANCE"; trench plus factory in `trench_05`). Before episode 2: give Datum Line its own palette, type and rail so it can't be mistaken for the sister channels |
| 9 | LOW | All 17 photo credits | Says "PHOTO · PHOTO: TONY WEBSTER · CC BY 2.0" and "PHOTO · IMAGE: NASA · PUBLIC DOMAIN" (the prefix is doubled). The credit is 21 px mono: readable at 1080p, unreadable on a phone (fine legally, because the description carries it) | `flow.py` about line 590: use `v[3]` alone when it already starts with "PHOTO" or "IMAGE", otherwise `UI["photo"] + v[3]` |
| 10 | LOW | 4:14 card "15 MILLION m³" | The voice says "almost fifteen million". The card drops the qualifier | `trench_02` card: "≈15 MILLION m³" |
| 11 | LOW | germany_05 (8:39) | FACTCHECK marks the 6½-year / end-of-2032 figure STALE-RISK (newer reports say 2031 or 3-4 years) | Optional: "...no trains before the end of twenty thirty-two at the earliest, though newer reports differ." Otherwise leave it, since it's attributed |
| 12 | LOW | 4:05 and other photo entrances | For about 0.3 s while a photo slides in, the caption plate covers the photo's label ("DREDGER REYNAERT..." is cut off). It's transient | None needed. If touched: fade the photo label in after the move settles |
| 13 | STALE | now_00, 9:18 card "9 OCTOBER 2026"; open_04/05 | The film is dated the day it was recorded. If the upload slips, or Femern announces element 5 or a new timetable, this chapter is wrong | Check https://femern.com/press/news/ on upload day. If anything is new, or the date is past 9 Oct, re-voice now_00 and change the card |

## Measurements

| Check | Result | Target | Pass |
|---|---|---|---|
| Integrated loudness | -14.0 LUFS | -14 | yes |
| True peak (ebur128 peak=true) | -1.6 dBTP | ≤ -1.0 | yes |
| LRA | 1.7 LU | n/a | ok (very flat; fine for VO) |
| Silence > 0.8 s at -40 dB | none | none in body | yes |
| Chapter-gap dips | short-term loudness falls to about -22 LUFS for 2-3 s at each chapter change (music only) | n/a | intended |
| Cut-off lines | none: the 29 sampled lines transcribe complete, last word present | none | yes |
| Frozen (motion_report) | 5.3 s total (1%), 0 stretches ≥ 2 s | 0 over 2 s | yes |
| Near-still | 11.6 s (2%), 0 stretches ≥ 2 s | low | yes |
| Black frames | 8 dips of 0.38-0.42 s, all at chapter cards (0:52, 1:58, 2:48, 3:56, 4:38, 6:52, 9:15, 10:17) | none unintended | yes (intended dips) |
| Stray debug text | none seen in 88 sheet frames + 31 grabs | none | yes |
| Photo credit on every photo | 17 of 17 photo beats show the credit (checked each) | all | yes |
| Text over pictures | the label sits on a plate; captions sit below the picture | readable | yes |
| Diagrams readable | yes. g07 cross-section draws road, road, service, rail, rail, which matches the FACTCHECK fix | readable | yes |
| ASR sample | 29 lines across all 11 chapters. Wording matches the script except for name renderings (#7) and "football pitchers"/"krona" (most likely ASR) | n/a | see #7 |

## On-screen numbers vs FACTCHECK.md (spot-check of every number card)

All match their CORRECT rows: 73,500 t (STANDARD) · 89 / 4 (28 Sep) · 45 min / 10 min · 4½-5 h / 2½ h · 2008 treaty roles ·
under 7 km / 18 km · ≈15 m (dpa) / up to 40 m (Femern) · 2,000+ from 40+ countries · 217 m, 9 segments, about 9 weeks ·
42 m x 9 m (ENR) · 79 / 10 · 120 years · 15 million m³ (see #10) · 0.5 cm (Hemmingsen via dpa) · nearly 2 years
(21 Jan 2026) · tow on 4 May, noon 6 May, +14 h, laser 7 May · 7 May / 27 Jun / 1 Aug / 28 Sep · ≈900 m of 18 km ·
DKK 55.1 bn (2015 prices) · DKK 7.3 bn reserves · €7 bn (2016) / $8 bn (ENR 2026) · ≈€1.3 bn EU · ≈88 km · Jan 2020 /
Jul 2025 / Jul 2025 · 6½ years (attributed; STALE-RISK) · €714 m / €2.3 bn (NDR via YACHT) · two stages, 17 May 2026 ·
19+ / 4 · 39 x 47 x 13 m · +1,600 t (11 Sep) · "no earlier than 2031" (dpa, marked not confirmed) · 1 every 5-7 weeks ·
85 / 8-11 years.
Arithmetic recomputed: intervals of 51, 35 and about 41-58 days give 5-7 weeks per element. 85 x 5 weeks = 8.2 years;
85 x 7 weeks = 11.4 years, so "8-11 years" holds. 18 km - 0.9 km = 17.1 km, so "seventeen to go" holds.

## Authorship (CRAFT §1) and hook

- **Point of view: yes, strong.** It's told in the first person ("my own estimate", "I think he's right"). It does its
  own arithmetic, labelled "OUR SUM, NOT A FORECAST". It ends on a clear verdict (the engineering is solved; the
  calendar and the German land works are not) and gives the viewer something to watch for ("watch the elements per
  month"). It doesn't read as a template script.
- **Structure:** it opens on the first immersion, goes back to the ferry, and builds toward a verdict. The order differs
  from the sister channels' films. The CHANNEL.md promise "cold open on the night it worked" is only partly kept: the
  night itself is told at 5:51, and the open is a summary.
- **Template risk is in the picture, not the words:** see #8.
- **Hook in 8 s:** partial. Subject and superlative arrive by 2.7 s; the tension ("two years late") arrives at 9.3 s, over a dark frame 0. See #5.

## Diagram label: is "ILLUSTRATION · AI-GENERATED" accurate?

No, it's inaccurate. `diagrams.py` draws every g-image procedurally with skia; no generative model is involved
(IMAGES.md is an old prompt list that was replaced). The label is not a policy breach: over-disclosing is legal and YouTube's synthetic-content
box covers realistic content, and line diagrams aren't realistic. But it's false, it invites "AI slop" comments, and
it contradicts the channel promise of "real photographs". It's also applied to only 14 of the 22 diagrams.
**Recommendation:** "DIAGRAM · DRAWN FOR THIS FILM" on all 22 (fix #1). POST.md should say "Diagrams are drawn for this
film from the owner's published descriptions; they are not photographs." The synthetic voice is a separate question:
keep ticking the altered-content box if house policy wants it, but not because of the diagrams.

## Rights check (CREDITS.md)

The 17 photo beats on screen use 16 files, all on the kept list: fehmarnbelt_satellite_nasa (PD), prinsesse_benedikte_2018,
ice_train_on_ferry_2014, rodby_harbour_2014, drogden_tunnel_2024, pilen_viewpoint_c/b/_2026, reynaert_fehmarnbelt_2026,
oresund_tunnel_portal_2019, puttgarden_site_2022 (x2), gpo_amethyst_fehmarnbelt_2026, rodby_femern_2020,
fehmarnsund_bridge_2018, fehmarnsund_bridge_2005 (PD), ferry_deutschland_2014. All are CC BY 4.0, CC BY 2.0 or PD.
**None of the six CC BY-SA files appears** (I checked every photo beat in the render). Cropping and colour grading are
stated in POST.md, as CC BY requires. Not verified: the Commons pages themselves; CREDITS.md asks a human to open each once.
The NASA image's provenance is MEDIUM confidence (no NASA ID).

## Packaging

- Title "Europe's Sunken Tunnel Is Years Late" (36 characters, 6 words) meets CRAFT §6, and the owner's "about two years
  behind" supports it. Thumbnail "4 OF 89" complements the title. Good.
- Description: fix #3 and #4. "Illustrations are generated diagrams" → "Diagrams are drawn for this film" (#1).
- Corrected CHAPTERS for POST.md. Each new `floor` in lines.json starts a chapter; the time is where the chapter card
  appears (the gap between voice lines):

```
0:00 Two years late
0:52 Forty-five minutes of water
1:58 A tunnel you don't dig
2:48 The factory
3:56 The trench
4:38 The ship that wasn't ready
5:49 Fourteen hours
6:52 The money
8:01 The German half
9:16 Where it stands
10:17 The arithmetic
```
(11 chapters, each over 10 s, first at 0:00; YouTube's rules are met. Times hold only for this exact render; recompute
if any line is re-voiced.)

## Not verified

- Pronunciation by ear (#7): ASR only.
- Commons pages opened by a human (rights tags as of today).
- Whether femern.com has posted news since 9 Oct.
- Thumbnail image: none exists yet to judge.
