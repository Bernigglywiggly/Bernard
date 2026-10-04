# Channel 3 · Money crimes (scams, frauds, heists, explained)
**Format (2 Oct, the user: "long form yt for money, shorts is bonus and discovery"):** long-form documentaries
(16:9, 12-15 min, mid-roll ads from 8 min) are the product; every film is cut into 3-5 shorts that point back to it. Period-accurate,
photoreal reenactments, labelled "AI reenactment" on screen and with YouTube's synthetic-content box ticked.
**Look:** 35mm film grade, warm tungsten and cool shadows, gold name cards, red rubber-stamp numbers, kinetic captions.
**Voice:** Imogen (Higgsfield Seed Audio preset), one take per short. **Music:** jazz, not synths (3 Oct, the user: "replace with jazz or house jazz for these sorts of vids, futuristic bg music dont match"): Kevin MacLeod's jazz, CC BY 4.0, cut by `lab/music/jazz/library.py`; the credit line goes in every description.
**Facts:** only charged or convicted people; contested stories told as "the story goes"; sources in each `make.py`.

## Long-form
| # | Title | Status | Files |
|---|---|---|---|
| 01 | The Man Who Sold the Eiffel Tower (And Conned Al Capone) · 14:56 | Made 3 Oct · [page](https://claude.ai/artifact/B4DiPy9qxvVKaZgucpYK3Q) | `lab/longform/lustig/` (`script.py`, `film.py`, `POST.md`, `out/`) |
| 02 | The Original Ponzi Scheme · 13:27 | Voiced, pictured and scored 4 Oct; rendering (pages next) | `lab/longform/ponzi/` (about 200 credits: 55 stills, 6 clips, 12 takes) |

## How a long-form film is made (`lab/longform`, about 320 Higgsfield credits for film 01)
1. Script: ~2,000 words in 11-12 chapters, each ending on a question (`script.py`); facts from Wikipedia plus two other
   sources, contested parts flagged in the narration ("the story goes").
2. Voice: Imogen, one Seed Audio take per chapter (`vo.py` joins them, caps TTS pauses at 0.85 s, keeps the Whisper
   word timings). ~13 credits.
3. Pictures (`ai_assets.py`): ~80 GPT Image 2.5 stills (medium 1 credit, high 2.75 for close-ups) with the character
   references, ~20 Kling 3.0 Pro clips; public-domain archive from Wikimedia Commons (`../tools/commons.py`, credits
   kept in `src/arch/credits.json`); drawn graphics (maps from Natural Earth, documents, counters, timelines).
4. Score: one jazz cue per chapter (`music.py` → `lab/music/jazz/library.py`): noir for cons, swing for hustles, dance-jazz for montages; the last cue's own ending lands on the end card. Ducked under the voice; credits (`library.credit_line`) in POST.md.
5. Edit: `film.py` (shots on the word timings, overlays, sound effects), rendered by `lab/longform/doc.py` in parallel
   segments (~1 hour here), delivered as a 1080p file under 240 MiB for the downloads page.
6. `thumb.py` (three thumbnails for Test & Compare) and `POST.md` (title, chapters, sources, credits, AI disclosure).
Cheaper next time: half the Kling clips (archive and graphics carry more), ~180 credits a film. Film 02 (Ponzi) came in at about 200 with 6 clips; real people are never drawn face-on there (their photographs carry the likeness).

## Shorts
| # | Title | Status | Files |
|---|---|---|---|
| 01 | He sold the Eiffel Tower. Twice. (Victor Lustig, 1925) | Made 2 Oct | `lab/shorts/lustig/` (`make.py`, `src/` stills and voice, `clips/` AI video, `out/`) |

## How a short is made (about 160 credits for the flagship; 60-90 for a standard one)
1. Script (~150 words) with a hook in the first line; facts checked.
2. Voice: Higgsfield `generate_audio` (seed_audio, one take, ~1 credit); Whisper word timings (`faster-whisper`).
3. Two character references, then 15-20 stills: GPT Image 2.5 (high, 2k, ~2.75 credits each) with the references.
4. Animate: Kling 3.0 Pro (~1.5 credits a second), Veo 3.1 for the opening hook (~4 a second).
5. Edit: `python3 lab/shorts/<short>/make.py` (the reel engine: grade, grain, captions, stamps, score ducked under the voice, SFX).

## Next ideas
Madoff (how a Ponzi actually works), Theranos, OneCoin's missing "Crypto Queen" (charged, at large), the Great Salad Oil
Swindle (1963), Charles Ponzi himself, pig-butchering scam compounds (protective angle). The Trend desk adds fresh cases.
