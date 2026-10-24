FIX THEN UPLOAD

# CRITIC v2: The Household Ledger, pilot 01, "Why $87,000 Feels Like Less"

Render reviewed: `LEDGER_PILOT_v2.mp4` (837.25 s, 1920x1080, 24 fps, AAC 48 kHz stereo). Reviewed 9 Oct 2026 by an
independent critic who did not build the film. This is the first critic pass on this film. Evidence is in `out/critic/`:
`sheet8_0..6.jpg` (a frame every 8 s; the labels run about 4 s early because of how ffmpeg's fps filter samples),
`gsheet1-3.jpg` and `strip_258.jpg` (targeted grabs), `full_*.png`, `loudness.txt`, `silence.txt`, `black.txt` and `motion.txt`.

**What the film does well.** The film argues one point and reaches a verdict of its own. It has four first-person
moments: "My reading is", "I think is the key", "My verdict is" and "If I had to watch a single figure". It gives the good
news a fair hearing. Every number I checked matches FACTCHECK.md, and the sums are right. The sound is on target, and the
picture almost never freezes. What stops it going up today is one broken card (the central chart of the film), one figure
that went stale this morning, and a POST.md that would publish a false statement and a title the fact check ruled out.

---

## Problems by severity

### HIGH (fix before upload)

**H1. The film's key chart never shows: the "SINCE JANUARY 2020" ranked list (basket_06).**
From 254.3 to 258.25 s the frame is empty while the voice says "Set those against a pay rise of thirty-three percent, and
a pattern appears." The eight-row list then flashes for about 0.5 s (258.25 to 258.75) as the camera leaves, too fast to read
(`strip_258.jpg`, `gsheet1.jpg` 254.6 to 258.5). Cause, from `lab/curvelf/flow.py`: the `list` card uses
`fit_sans(..., 96*u, ...)` with `lh = size*1.55`. Eight rows plus a title are taller than the space above the caption
band, so `on_screen()` (the bottom check against `CAP_TOP`) sets the card's alpha to 0 until the camera zooms out to leave.
Lists of six rows or fewer render correctly (the verdict DEBIT list and the five questions).
- Script fix (fastest): basket_06 visual →
  `("list", ["ELECTRICITY +43% · GASOLINE +42%", "EATING OUT +38%", "RENT +33%", "PAY +33%", "GROCERIES +32%", "NEW CARS +21% · MEDICAL +18%"], "SINCE JANUARY 2020")`
- Also add `HOLD` for basket_06 (about 2 s) or put the same list on basket_07 as well, so the pattern stays up while "Pay tied
  or lost..." is spoken. The line is only 4.2 s long.
- Engine fix (prevents a repeat): in the `list` branch, cap `size` so that `hgt` fits between the rail and `CAP_TOP` at the
  card's zoom, for example `size = min(size, avail_h / (len(items)*1.55 + 0.8))`. Then re-run `fit_sans` at that size.

**H2. The mood number went stale today.** Michigan published the **preliminary October 2026** index on 9 Oct: **46.3**,
down from 48.1 (front page read 9 Oct by this critic). September's 48.1 is still correctly labelled everywhere, and May's
44.8 is still the all-time low, so no line is false. But the film says the mood describes "right now" (year_00) and "this
month" (verdict_04), and the closing card pairs $87,460 with 48.1. Anyone who checks will see 46.3. Fix by voicing one new
line and changing one word:
- New beat after mood_03:
  "The preliminary October reading, published on the ninth, slipped again, to forty-six point three."
  `("num", "46.3", "INDEX OF CONSUMER SENTIMENT · OCTOBER 2026 · PRELIMINARY · UNIVERSITY OF MICHIGAN")`
- verdict_04: "...The mood counts this month, at your address, with your loan." → "...The mood counts this autumn, at
  your address, with your loan."
- Optional: in the year_11 timeline, replace `("2 OCT", "+29,000 JOBS")` with `("9 OCT", "SENTIMENT 46.3 · PRELIMINARY")`.
  Do not add a seventh mark, because the date labels already nearly touch at six.
- The Hsu quote's source page now shows October's text. Save the September copy (Wayback or PDF) and link that copy in the
  description.

**H3. POST.md would publish a false statement and the banned title.**
- Description: "Illustrations are AI-generated and show no real people." This is **false**: e01-e33 are drawn in code
  (`illustrations.py`, skia). Replace with: "The illustrations were drawn in code for this film. There are no
  photographs and no real people. The narration is a synthetic voice."
- The lead title is "Why a Record $87,000 Income Feels Like a Pay Cut". FACTCHECK (TITLE row) says **do not use it**:
  real weekly earnings were +0.3%, and pay is 2-3% ahead of prices since 2020. Make the lead title
  **"Why $87,000 Feels Like Less"**, which is also the film's on-screen title.
- Title option 3 ("The Mood Hit 48.1") and thumbnail option 3 ("48.1") are both stale since today. Use thumbnail
  **BOTH ARE TRUE**.
- Sources: delete the Wolf Street line. Add the FHFA National Mortgage Database entry from the `script.py` docstring
  (fhfa.gov/data/nmdb, Q2 2026, file dated 24 Sep 2026). Add Michigan October preliminary if H2 goes in.
- The "Before upload" section is out of date: the fact check has run, the Wolf Street beats are replaced, and this critic has
  run. Rewrite it as the re-pull list in M4.
- Paste the chapter list from the end of this file.
- Disclosure: as I read YouTube's policy, the altered/synthetic-content tick is for **realistic** content. Code-drawn
  diagrams and a voice that does not imitate a real person are not realistic content, so the tick is optional. Saying
  "synthetic voice" in the description is the honest and cheap choice. (This is a policy reading, not verified against
  YouTube today.)

### MEDIUM

**M1. The hook takes 14 s.** The first 8 s say only "record income" (open_00 runs 0.4 to 7.5 s). The opposing fact arrives
at 7.8 s, and "lowest level ever" completes at 14.2 s. CRAFT §2 wants the surprising part inside 8 s. Replace:
- open_00: "The typical American household just earned a record income, yet in the same month it felt worse about money than in almost any month since 1952."
  Keep the `$87,460` card. This is true: 48.1 is below every reading since Nov 1952 except May 2026 and now Oct 2026 prelim.
- open_01: "The record comes from the Census Bureau, and the gloom comes from a survey the University of Michigan has run for more than seventy years."
  Keep the `48.1` card.

**M2. Frame 0 is caught mid fade-in.** The whole frame, including the rail and the $87,460, is at about 30% brightness at
t = 0 (`frame0.png`) and only reaches full brightness around 0.5 s. With `OPEN_RESOLVED = True`, frame 0 should be the
finished composition. Engine fix: skip the global opening fade when `OPEN_RESOLVED` is set, or start it at alpha 1.
Without this, the fallback thumbnail and the first impression are a grey number on black.

**M3. Authorship and the shared engine look (CRAFT §1 and the 9 Oct lesson).** The voice and argument are authored. The
look is The Curve's: the numbered chapter rail across the top, the typed mono captions with a block cursor, the karaoke
caption plate, a cyan glow on the right-hand number of every split, and "CHAPTER NN" title plates. A viewer, or YouTube's
classifier, who has seen The Curve or Money Crimes will see the same channel. The brief's own distinguishing devices are
missing or invisible on screen. The film never shows "one object that carries across cuts: a ledger line or a receipt",
and "OUR SUM" appears only as six mono letters under a number. To give this channel a look of its own:
- **Paper, not terminal.** Use a warm off-white ruled ledger page (cream #F3EEE2, ink #1B2A41, red-ink debit #B23A2E)
  as the ground for every data card. That replaces black-and-cyan.
- **A running ledger replaces the rail.** Use a two-column CREDIT and DEBIT page that stays on screen in a corner. Each
  chapter writes one entry into it with a pen stroke, and the verdict zooms out to the whole page. This is the object that
  carries across cuts, and it is the chapter marker.
- **Show the sums as arithmetic.** Write money_06/money_08 and streets_05/06 out as a column sum ($410,700 × 80% = $328,560 → $2,275 a month)
  in a handwritten or serif face, rather than a single big number.
- **Show the race as an actual race.** race_00 promises "a race between two lines", but no line chart ever appears. Draw
  CPI and hourly pay as two rising lines from Jan 2020 to Aug 2026 that finish 2-3% apart. Put it on race_06 (13.5 s, the
  longest line in the film, now sitting on a decorative scale) and on level_02.
- Use a serif or slab display face for the numbers, not The Curve's grotesque. Drop the typed-cursor effect on this channel.
- About a third of screen time is generic metaphor icons (barometer, key, scales, umbrella-cloud, crowd) that carry no
  data. Each film should replace at least five of them with charts of its own data.

**M4. Releases that go stale before a mid-October upload.** If the film goes up on or before 13 Oct, only H2 applies. After that:
| Date | Release | Lines it touches | Risk |
|---|---|---|---|
| 13 Oct | EIA weekly gasoline | year_02, year_03 | low (dated "On the fifth of October") |
| **14 Oct** | **CPI September + Real Earnings September** | race_01-05, all basket cards, level_01, year_04, year_09, year_10, verdict_02/05, debit list | **high**: "the one to watch" (−0.3%) gets a new value the same day. If it turns positive, the last chapter needs rewriting (FACTCHECK §3) |
| 15 Oct | Freddie Mac PMMS | money_04, money_08, streets_06, year_06, timeline | low (dated); "highest since Nov 2023" is false if the print passes 7.44 |
| 23 Oct | Michigan October final | H2 line | low (labelled preliminary) |
**Recommendation: upload by 13 Oct with H1-H3 fixed.** Otherwise re-pull and re-voice after 14 Oct.

### LOW

**L1. The timelines start blank for about 1 s.** mood_06 has a near-black frame from 141.2 to 142.8 s, and year_11 from
716.7 to 717.6 s, before the first mark appears. Start the `tl` line and first mark at `t0` instead of ramping from 0.

**L2. Split colours carry no meaning.** The right-hand number is always cyan with a glow, and the right-hand label is
always red. So $85,210 (the weaker 2024 figure) glows, "+18.3% MEDICAL CARE SERVICES" is red, and in the end card THE
MOOD is red while 48.1 is cyan. Colour by ledger side instead (credit and debit), or keep both labels neutral.

**L3. The disclaimer is on screen only as the caption** (verdict_06, 807.9 s, over the glasses-on-newspaper picture).
Change its visual to `("words", "NOT ADVICE · A WAY OF READING THE NUMBERS")` so it reads with the sound off.

**L4. Picture empty for about 0.4 s at some line starts** (for example 83.7-84.1 s, before "After taxes"), while the camera
travels. The flow engine does this everywhere and it is acceptable, but on credit_07 the caption plays over an empty frame.

**L5. Pronunciation, check by ear (not verified).** Whisper heard "Stephanie Stanchever" and "Joel Scali". lines.json
shows the respellings "Stephanie Stancheva" and "Scali" were voiced on purpose, and both are acceptable. Listen once to
"Joanne Hsu" (147.1 s): it should be "shoo", not spelled out. Percentile words came out correctly ("10th percentile",
"90th percentile").

---

## Advice risk: clear
The film never tells the viewer what to do. The mortgage and card sums are hypothetical and framed as such ("Suppose
you carry", "Now picture two families"), and the payments are labelled "principal and interest" and "before taxes and
insurance". "If I had to watch a single figure" is a reading, not a recommendation. The spoken disclaimer is plain:
"Nothing in this film is advice about what to do with your money." The description repeats it. L3 makes it visible on
screen. No product, lender or card is named.

## Numbers on screen vs FACTCHECK.md
I compared every card in the contact sheets with FACTCHECK §1: **no mismatches**. All post-check edits appear on screen
(2–3% card, "ALL PRIVATE EMPLOYEES", FHFA attribution, AUGUST +133,000, REAL WEEKLY +0.3%, SEPTEMBER 2026 label, AVERAGE
SINCE JULY $4.13).

I recomputed these:
| Claim | Recomputed |
|---|---|
| 1.328 ÷ 1.299 = 1.02 | 1.0223 ✓ (unrounded 1.3282/1.2985 = 1.0229) |
| CPI +29.9%, $129.85 | 334.980/257.971 = 1.2985 ✓ |
| Pay +32.8% | 37.76/28.43 = 1.3282 ✓ |
| $1,214 (80% of $329,000, 30 yr, 3.72%) | $1,214.44 ✓ |
| $2,275 (80% of $410,700, 30 yr, 7.40%) | $2,274.88 ✓ |
| +87% payment, +25% price | 1.8732 ✓, 1.2483 ✓ ($81,700 more, "roughly eighty thousand" ✓) |
| $1,265 / $2,077 / $812 ($300,000, 30 yr) | $1,264.81 / $2,077.14 / $812.33 ✓ |
| ≈$755 / ≈$1,060 on $5,000 | 754.50 / 1,059.50 ✓ |
| +2.5% 2019→2025 | 87,460/85,320 = 1.0251 ✓ |
| 48.1 "less than half" of 99.8 | 0.482 ✓ |
| Mortgage rate "roughly doubled" | 7.40/3.72 = 1.99 ✓ |
| Pay +3.0% year to Sep | 37.81/36.70 = 1.0302 ✓ |
Script lint (`script_lint.py`): 0 flags.

## Measurements
| Check | Result | Target |
|---|---|---|
| Integrated loudness | **−14.1 LUFS** | −14 ✓ |
| True peak (ebur128 peak=true) | **−2.1 dBTP** | ≤ −1 ✓ |
| Loudness range | 1.6 LU | (voice-led, fine) |
| Short-term dips | about −19 to −23 LUFS for 1-2 s at each chapter break (39-41 s, 102-104 s...) | intended breath, fine |
| Silence (< −45 dB, ≥ 1.2 s) | none | ✓ |
| Frozen | 4.6 s (1%), no stretch ≥ 2 s | ✓ |
| Near-still | 12.5 s (1%), no stretch ≥ 2 s | ✓ |
| Near-black (pix_th 0.06, ≥ 0.3 s) | **3.9 s at 254.3 (H1)**, 1.6 s at 141.2, 0.9 s at 716.7 (L1); all others ≤ 0.55 s at line changes | |
| End card | 826.3 to 837.25 s (11 s hold, allowed) | ✓ |
| Transcript (faster_whisper small.en, all 115 lines from the final mix) | mean similarity 0.90 to the script. Every gap is digit formatting ("$87,500", "48.1") or a homophone ("pay one", "principle"). No missing or extra words | ✓ |
| Clipped lines | none: every line's last word ends before the next line starts | ✓ |
| Debug text, overlaps, text over pictures | none found in about 140 sampled frames | ✓ |
| Unreadable cards | basket_06 list (H1). Mono sub-labels are about 22 px at 1080p, which is fine on desktop and small on phones | |
| Hook inside 8 s | no, about 14 s (M1) | |
| Frame 0 | the designed $87,460 card, but at about 30% brightness (M2) | |
| Picture label | none, which is correct: the pictures are code-drawn generic objects, not photos or reconstructions. Do not set the old "AI-GENERATED" tag | ✓ |

## Chapters (from flow/lines.json: new `floor` = new chapter, start − 1.6 s; matches the on-screen chapter plates)
The render does not change for H3, M4 or the POST edits. If H2 (one new beat) or M1 goes in, every chapter after the
change shifts by the new line's length plus about 0.3 s. Regenerate from the new lines.json.
```
0:00 Two numbers that disagree
0:38 The credit side
1:41 The mood
2:43 The race
3:39 The basket
4:39 The level
5:47 The price of money
7:38 Two streets
8:58 The cushion
10:26 This year
12:04 Who is the middle
12:45 The verdict
```
(The shortest chapter is 41 s; YouTube's minimum is 10 s.)

## Could not verify
- How "Hsu", "Stantcheva" and "Joelle" sound to a human ear (whisper only).
- BLS pages (FACTCHECK could not read them either); the YouTube disclosure policy wording as of today.
- Whether YouTube's handle "The Household Ledger" is free (CHANNEL.md lists this as not yet checked).
- Phone-size readability was judged from frames at full resolution and at 640 px, not from `LEDGER_PILOT_v2_phone.mp4`.

## Order of work
1. H1 (list) + H2 (one new line, one word) + M1 (two lines), then re-voice those lines, re-render and pull new chapter times.
2. M2 engine fade at frame 0.
3. POST.md edits (H3) and the chapters.
4. Upload by 13 Oct. Otherwise re-pull after the 14 Oct CPI.
5. M3 (own look) before episode 2, not before this pilot.

CRAFT "Learned on our films" line suggested (for the builder to add): *9 Oct (Ledger pilot): an 8-row `list` card fails
`on_screen()`'s caption-band check and stays invisible until the camera leaves. Keep lists to 6 rows or let the engine
shrink the type to fit.*
