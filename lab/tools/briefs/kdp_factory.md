<!-- Brief for the KDP rows in channel/ROTA.md ("KDP AUDIT" once, then "KDP BUILD" each morning). The 07:30 task
b-daily-check-0730-2 runs them as its MORNING rows. Written by account B, 29 Oct 2026. Edit this file to change the plan. -->

KDP factory for Dark Archive Press (account B). Toolchain: ~/🧧/🏭_TOOLS/📗_kdp_tools/ (generators `truecrime/tc_gen.py`,
`tc_build.py`, `tc_cover.py`, `sudoku/make_volume.py`, `largeprint/lp_cover.py`, `casefiles_*`; pre-upload gate
`kdp_gate.py`; PDF read-back check `truecrime/verify_pdf.py`). Built books go in ~/🧧/📚_KDP_BUILDS/<slug>/ (never in the
repo: PDFs are large); the text files (state, queue, listing packs) go in ~/Bernard/kdp/ and are committed.

THE OWNER (29 Oct): "kdp books are worth building as can just make infinite amount to an extent and the more books, more chance of sales, a focus on these for now and building them to a good point will be good, I'm trying not to spread attention".

THE EVIDENCE (read ~/Bernard/lab/research/KDP_MARKET_RESEARCH_2026-09-10.md first; BSR read off Amazon pages):
- True crime word search is dead: the category leader is BSR #156,403 (under 1 sale a day); his ~20 titles earn ~£3-4 a month. Build NO more true crime titles.
- What sells is a MOOD, SEASON or IDENTITY theme, in large print, for adults and seniors: Cozy Autumn Word Search #841, Nostalgic Word Search for Adults & Seniors #1,038, Inspirational Bible Word Search #13,732, Cozy Christmas #37,479 (climbs through Nov-Dec).
- The winners' format: ~100 puzzles, 104-107+ pages, £10.49-£10.99, categories Word Search Games + Word Games + Puzzles, large print. His old books: 50 puzzles, 60 pages, £7.40, filed under Humor › Law & Crime.
- Seasonal titles need to be live 8-10 weeks before their season.
- "Infinite" is capped: KDP allows 3 new titles a day per account, and 2 a day is the safe rate (clusters risk a velocity flag; enforcement is account-wide, so the live titles are at stake). That is about 60 a month. Each new title starts at 0 reviews against winners with 250-500: a compounding asset with a long fuse.
- Royalty on a £10.99, 105-page black-and-white paperback: 60% of list minus printing (about £2.10 in the UK) ≈ £4.40 a sale [EST: check KDP's printing-cost calculator and write the real figure into STATE.md].

KDP AUDIT (one run; skip at 90%+ weekly usage):
1. Inventory every finished book under the toolchain's build folders and ~/Downloads/GoldenPlate_Vault/KDP_*: title, series, pages, trim, cover file, listing file, and whether `python3 kdp_gate.py <cover> <interior> <w> <h>` passes.
2. Live catalogue: only if the claude-in-chrome tools are connected and his Chrome is already logged into KDP, read the Bookshelf and the Reports page (units by title, last 90 days) with get_page_text. READ ONLY: never click publish, save, edit or delete, never type into KDP. If Chrome isn't available, skip it and say so.
3. Demand check: if Chrome is available, read up to 8 Amazon product pages for candidate themes (the BSR line and page count only).
4. Write ~/Bernard/kdp/STATE.md, leading with a table:
   - live titles, with any sales;
   - built-but-unpublished titles;
   - the free fixes for his hands: categories on the live titles (Word Search Games + Word Games + Puzzles), the duplicate "True Crime Word Search Vol 16" draft, and the "Dark Archive press" lower-case typo on Vol 11;
   - a ranked BUILD PLAN of 20 new titles in the winners' formula, as 2-3 KDP series of numbered volumes so volume 1 sells volume 2. Seasonal themes must go live 8-10 weeks ahead: winter for Dec-Feb, Valentine's, spring and Easter, Mother's Day. Identity themes: nostalgic decades, faith and inspiration, cats, dogs, birds, gardening, cooking, travel, cosy home. Never trademarks, characters, brands or real people.
5. Write ~/Bernard/kdp/QUEUE.md: his publish list, 2 a day, finished books first, each line linking its copy-paste pack.
6. Commit kdp/*.md and push. Then a PushNotification under 200 characters with the two-line summary.

KDP BUILD (each morning row; skip at 90%+ weekly usage; stop at once if kdp/QUEUE.md already has 10 or more unpublished titles, since he publishes 2 a day and more would rot):
- Take the next 2 titles from the BUILD PLAN in kdp/STATE.md.
- Interior: 100 themed word-search puzzles, each with 15-25 words from a hand-checked themed list (no duplicates across a volume, family-friendly, UK and US spellings checked). Use large-print grid letters (16-18 pt), one puzzle per page, the answer key at the back, 105 pages or more, 8.5 x 11 in, no bleed, all fonts embedded. Make it with the existing generators, adapted to themed lists; put new code next to them and keep the old files.
- Cover: a full wrap PDF at KDP's size for that page count (spine = pages x 0.002252 in on white paper; spine text at least 0.0625 in from each fold, as kdp_gate.py checks). Use our own design, no copied artwork, with the theme and "LARGE PRINT" readable at thumbnail size.
- Listing pack ~/Bernard/kdp/packs/<slug>.md containing:
  - title and subtitle (theme + "Word Search for Adults" + "Large Print" + puzzle count);
  - author/imprint exactly "Dark Archive Press";
  - series name and number;
  - a description;
  - 7 keywords and 3 categories;
  - price £10.99 / $12.99;
  - the AI declaration ("AI-assisted, human-directed" for anything generated);
  - print settings: 8.5 x 11, black and white on white, no bleed, matte.
- Quality gate:
  - kdp_gate.py passes;
  - a read-back check proves every word is in its grid and the answer key matches (adapt verify_pdf.py);
  - then a NEW Sonnet subagent critic looks at 6 rendered interior pages and the cover as PNGs against the winners' standard (legibility for older eyes, theme appeal, nothing broken).
  - Fix whatever it finds and re-check. Only then add the title to kdp/QUEUE.md.
- Each title should cost well under 1% of the weekly allowance. If it costs more, write why in kdp/STATE.md.
- Commit kdp/*.md and push. No notification unless something blocks.

NEVER publish, edit or delete anything on KDP, Amazon or any store: that is his hands, 15 minutes a title by the queue. Never copy another publisher's puzzles, artwork, titles or descriptions. Branch claude/funny-newton-gd9w8v only; git add <paths>, never -A; end commit messages with "Co-Authored-By: Claude <noreply@anthropic.com>" and no model names.
