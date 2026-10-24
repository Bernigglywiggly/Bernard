# How to rerun the radar (weekly, under an hour)

Output: `lab/research/RADAR_<YYYY-MM-DD>.md`, same five sections as `RADAR_2026-10-11.md` (copy it as the template).
Read first (5 min): CRAFT.md §1, §6, §9 · `lab/tools/THUMBS.md` · `channel/uploads_newlook.json` and `channel/NEXT_FILMS.md`
(what is made or scheduled, so nothing repeats) · last week's radar (carry over open items, drop stale ones).

| Step | Time | Do this | Tool / command |
|---|---|---|---|
| 0 | 1 min | Check vidIQ credits. If >0 use vidIQ for steps 2-4 (better data); if 0 (renews on the 5th of each month, 150 credits ≈ 30 calls) use the yt-dlp script | `vidiq_balance` (load via ToolSearch "vidiq") |
| 1 | 10 min | **News scan.** Google News topic feeds + Trends + the studio's own radar | `curl -sL "https://trends.google.com/trending/rss?geo=US"` (also GB, ES, MX) · `https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en` (also TECHNOLOGY, WORLD) · `https://news.google.com/rss/search?q=<terms>%20when:7d&hl=en-US&gl=US&ceid=US:en` (item count, max 100 = news volume) · Spanish: `&hl=es-419&gl=MX&ceid=MX:es-419` · `~/youtube/news_radar_latest.txt` |
| 2 | 10 min | **Trending demand.** One line per candidate story in `trend.txt`, then | `python3 lab/tools/radar_outliers.py --file trend.txt --window week --sort views --n 12 --minviews 5000 --out trend.tsv` · vidIQ alternative: `vidiq_trending_videos` (videoFormat long, titleQuery, videoPublishedAfter = 7 days ago) |
| 3 | 15 min (runs in background) | **Evergreen outliers**, one query file per channel (keep and extend last week's files) | `python3 lab/tools/radar_outliers.py --file htp.txt --window year --n 15 --minviews 30000 --out htp.tsv` (same for mc, curve, es) · vidIQ alternative: `vidiq_outliers` (keyword, publishedWithin oneYear, contentType long) and `vidiq_keyword_research` (mode research for volume/competition, mode rising for momentum) |
| 4 | 5 min | **Packaging check**: thumbnails of the top 8 outliers per channel as a contact sheet, plus the first 35 s of 3-4 of them | `curl -o t.jpg https://i.ytimg.com/vi/<ID>/hqdefault.jpg` → PIL sheet → Read the image · `yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" <url>` |
| 5 | 5 min | **Calendar**: earnings dates (search "<company> to announce ... results"), elections, launches, trials, fraud/crash anniversaries, holidays, to today + 90 days | Google News RSS search · Wikipedia anniversaries · keep the 11 Oct calendar rows that are still ahead |
| 6 | 10 min | **Score and write.** D/G/T/F/E (1-5 each, rules below), rank the top 10, pick 3-5 "make next", update section 5 only if the scans show something new | edit the template |

**Scoring rules (keep them the same every week so weeks compare).**
D 5 = top-3 views this week ≥ 2M, or an evergreen outlier ≥ 50× with ≥ 200k views; 3 = ~200k-2M or 10-50×; 1 = nothing ≥ 30k.
G 5 = no YouTube video ≥ 5k on the angle; 3 = covered by news clips only; 1 = big explainers already exist (Kurzgesagt, Johnny Harris, ColdFusion).
T 5 = peaks inside 10 days or a dated hook we can hit; 3 = evergreen; 1 = already stale.
F 5 = map- or number-led, fits the channel's look and voice; 1 = needs footage, faces or game/film clips we can't use.
E 5 = assets or facts already exist (re-voice, re-cut); 3 = a normal new film; 1 = new engine or new look needed.
Make 17+ (GROWTH.md). Anything about real people: charged/convicted facts only, with filings.

**Notes that save time.**
- The ratio understates very new videos (lifetime views) and inflates tiny channels with one hit (median under ~300): read the
  views column too. Treat ≥3× as an outlier, ≥10× as a breakout.
- yt-dlp prints an "older than 90 days" warning to stderr: harmless (`--no-warnings` is already set). Channel medians cache for 7 days in
  `lab/tools/cache_radar/` (gitignore it).
- Put the TSVs in the session scratchpad, not the repo; cite the YouTube links in the radar's Sources.
- Mark anything not checked against a primary source "(unv.)". Titles and hooks in the radar are working drafts: the film's FACTS.md
  must source every number before scripting (CRAFT, 6 Oct lesson).
- After writing, add new winners to `channel/trends/BOARD.md` and tell the owner the top 3 with their windows.
