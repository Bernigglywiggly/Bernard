<!-- Brief for the KDP rows in channel/ROTA.md ("KDP AUDIT" once, then "KDP BUILD" on Mondays only). The 07:30 task
b-daily-check-0730-2 runs them as its MORNING rows. Written by account B, 29 Oct 2026; rewritten by account A, Fri 30 Oct
2026 01:40 UK, to KDP's real cap (TEAM §4, from C 30 Oct 00:37). Edit this file to change the plan. -->

KDP factory for the cozy large-print word search line. Toolchain: ~/🧧/🏭_TOOLS/📗_kdp_tools/ (pre-upload gate
`kdp_gate.py`; large-print cover `largeprint/lp_cover.py`; word-search generator and PDF read-back check in `truecrime/`
(`tc_gen.py`, `tc_book.py`, `verify_pdf.py`); `wordsearch_audit/`). Built books go in ~/🧧/📚_KDP_BUILDS/<slug>/ (never in
the repo: PDFs are large); the text files (STATE, QUEUE, listing packs) go in ~/Bernard/kdp/ and are committed.

THE OWNER (29 Oct): "kdp books are worth building as can just make infinite amount to an extent and the more books, more chance of sales, a focus on these for now and building them to a good point will be good, I'm trying not to spread attention".

THE CAP (KDP help G202172740, read 30 Oct 2026; in force since 21 Sep 2026, was 10 a week; our own block on 23 Sep = D-416)
| Rule | Number |
|---|---|
| New titles CREATED per format per week (drafts count) | 2 |
| New titles SUBMITTED per format per week (counted at first submit) | 2 |
| Reset | every Sunday 00:00 UTC |
| Formats | counted separately: eBook, paperback, hardcover |
| New paperbacks a year | 104 |
- So: **build 2 new titles a week, never 2 a day.** Keep **at most 4 built-but-unpublished** at any time (one week's 2 he can
  submit now + the next week's 2). More than that rots in the queue.
- Case Files Vol 8-9 (true crime) would use the same paperback slots: only if he says so.
- Hardcover has its own 2-a-week cap: build a hardcover edition **only of a title that sells 5+ a month** (check KDP's
  hardcover trim sizes first; 8.5 × 11 may not be offered for hardcover).

THE EVIDENCE (`kdp/THEMES_RESEARCH.md`, `lab/research/MONEY_ROUTES_INDEPENDENT_2026-10-29.md` §3; read both first)
- True crime word search is dead (category leader BSR #156,403). Build NO more true crime.
- What sells: a MOOD, SEASON, NOSTALGIA or FAITH theme, large print, for adults and seniors, judged on amazon.com (the
  US buyer first; .co.uk sells about a tenth). Leaders read 30 Oct: Nostalgic #1,051, Cozy Winter #3,811, Cozy Christmas
  #4,382 (climbing). One publisher's series holds the top 4: **win on print size and word quality, not puzzle count.**
- A big season does not lift a weak book (a 3000-word winter title sits at #1,046,378).
- Royalty, 105 pages, black and white, 8.5 × 11 at 60%: **£4.44 on .co.uk at £10.99, $4.95 on .com at $12.99**
  (printing £2.15 / $2.84, same cost up to 110 pages).
- The lever is hit rate, not count: one title at BSR #1,000 out-earns 60 average ones.

BUILD ORDER: `kdp/THEMES_RESEARCH.md` "Build order" table, top to bottom (week 1: Hearthside Winter + Hearthside
Christmas; week 2: Back When Vol 1 + Still Waters Vol 1; week 3: Winter Jumbo Print + Still Waters Vol 2 ...). Seasonal
titles must be live 8-10 weeks before their season; KDP review takes up to 72 h, so submit 3 days before each "go live
by" date. kdp/STATE.md records what is built, submitted and live; the next build is the first title in the order that
is none of those.
- **One-off, Fri 30 Oct (account A):** if he has created no paperback since Sun 25 Oct, this week's 2 slots are free until
  Sat 31 Oct 23:59 UTC: A builds Hearthside Winter + Hearthside Christmas on Fri 30 Oct for him to submit by Sat night,
  and the whole order moves up one week (Mon 2 Nov then builds Back When Vol 1 + Still Waters Vol 1).

THE BRAND: with a free KDP ISBN Amazon shows the imprint as "Independently published"; your own imprint needs a bought ISBN
(KDP help G201834170). So the brand goes on the cover and in the author field. **Not "Dark Archive Press"** (it reads as
true crime to a 70-year-old buyer). Use the name he picks, recorded at the top of kdp/STATE.md, byte-identical on every
title so Amazon links them. Until he picks, write `{BRAND}` in the packs and keep the cover's brand line one variable.
Check every brand and series name on Amazon, UK IPO and USPTO before first use.

KDP AUDIT (one run, Sun 1 Nov; skip at 90%+ weekly usage):
1. Inventory every finished book under ~/🧧/📚_KDP_BUILDS/, the toolchain's build folders and
   ~/Downloads/GoldenPlate_Vault/KDP_*: title, series, pages, trim, cover file, listing file, and whether
   `python3 kdp_gate.py <cover> <interior> <w> <h>` passes.
2. Live catalogue: only if the claude-in-chrome tools are connected and his Chrome is already logged into KDP, read the
   Bookshelf and the Reports page (units by title, last 90 days) with get_page_text. READ ONLY: never click publish,
   save, edit or delete, never type into KDP. Note any paperback created or submitted since the last Sunday 00:00 UTC
   (it uses this week's cap). If Chrome isn't available, skip it and say so.
3. Write ~/Bernard/kdp/STATE.md, leading with a table:
   - the brand (his pick, or "not picked yet");
   - live titles, with any sales;
   - built-but-unpublished titles (at most 4);
   - this week's cap: paperbacks created/submitted since Sunday 00:00 UTC, slots left;
   - the free fixes for his hands: categories on the live titles (Word Search Games + Word Games + Puzzles), the
     duplicate "True Crime Word Search Vol 16" draft, and the "Dark Archive press" lower-case typo on Vol 11;
   - the build order from THEMES_RESEARCH.md with each title's state (to build / built / submitted / live).
4. Write ~/Bernard/kdp/QUEUE.md: his publish list, **2 a week**, finished books first, each line linking its
   copy-paste pack and the date it must be submitted by.
5. Commit kdp/*.md and push. Then a PushNotification under 200 characters with the two-line summary.

KDP BUILD (the Monday row only; skip at 90%+ weekly usage; stop at once if 4 or more titles are built-but-unpublished):
- Take the next 2 titles in the build order (see BUILD ORDER).
- Interior: 100 themed word-search puzzles, one a page, each with its own sub-theme title and 15-20 words from a
  **fresh, hand-checked list for this volume** (no word twice in one puzzle, no word in more than 2 puzzles of a
  volume, no puzzle list copied from another of our volumes: 2025-26 account closures cite reused interiors and
  templates). Grid letters 18-20 pt, answer key at the back, **105-110 pages**, 8.5 × 11 in,
  no bleed, all fonts embedded. One short theme line per page is the leaders' extra (a winter fact, a decade memory);
  keep it true and plain. US spellings for US-first titles (avoid words whose spelling differs where you can); UK
  spellings only in the British edition. Make it with the existing generators adapted to themed lists; put new code
  next to them and keep the old files.
- Words never allowed: brand, character, celebrity or trademark names (Frosty, Rudolph, Grinch, Elf on the Shelf, Hula
  Hoop, Slinky, Frisbee, Jell-O, Barbie, Peeps, Cadbury, Guinness, Brain Games ...); song lyrics (carol titles are fine);
  Bible text from NIV/ESV/NLT (names, places and virtues only); medical claims (never "dementia", "memory loss" or
  "Alzheimer's" anywhere: interior, cover, listing).
- Cover: a full wrap PDF at KDP's size for that page count (spine = pages × 0.002252 in on white paper; spine text at
  least 0.0625 in from each fold, as kdp_gate.py checks). Our own design, no copied artwork; the theme word and
  "LARGE PRINT" readable at thumbnail size (check a 160 px-wide render); the brand line from THE BRAND.
- Listing pack ~/Bernard/kdp/packs/<slug>.md containing:
  - title: "[Series] [Theme] Word Search for Adults & Seniors: 100 Large Print Puzzles …" (never the leader's
    "… for Adults: Large Print Word Puzzles for …");
  - author exactly the brand; series name and number;
  - a description (what's inside, the print size, who it's for; no medical claims, no review requests);
  - the 7 keyword phrases and 3 categories from that theme's row in THEMES_RESEARCH.md;
  - price £10.99 / $12.99 (60% royalty: £4.44 / $4.95);
  - the AI declaration: **"AI-generated"** for AI-written word lists, fact lines and any AI image (KDP G200672390:
    "even if you applied substantial edits"); accuracy stays our job;
  - print settings: 8.5 × 11, black and white on white paper, no bleed, matte; free KDP ISBN;
  - "submit by" date (3 days before its go-live date).
- Quality gate:
  - kdp_gate.py passes;
  - a read-back check proves every word is in its grid, no word repeats across the volume and the answer key matches
    (adapt verify_pdf.py);
  - then a NEW Sonnet subagent critic looks at 6 rendered interior pages and the cover as PNGs (plus the 160 px
    thumbnail) against the leaders' standard: legibility for older eyes, theme appeal, nothing broken, nothing banned;
  - fix whatever it finds and re-check. Only then add the title to kdp/QUEUE.md.
- Log the real usage per title in kdp/STATE.md (aim ~1-2% of the weekly allowance; quality beats count here).
- Commit kdp/*.md and push. No notification unless something blocks.

Tue-Sat: **no new KDP title** (the week's cap is used); only finish or fix Monday's two.

NEVER publish, edit or delete anything on KDP, Amazon or any store: that is his hands, about 15 minutes a title by the
queue. Never copy another publisher's puzzles, artwork, titles or descriptions. Branch claude/funny-newton-gd9w8v only;
git add <paths>, never -A; end commit messages with "Co-Authored-By: Claude <noreply@anthropic.com>" and no model names.
