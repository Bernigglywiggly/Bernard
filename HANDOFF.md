# Handoff: the AI explainer channel + walk-in sales (read this first in a new session)

This repo is a scratch space (the DeepSeek-V3 files are unrelated). The user works across **two Claude accounts**
(a Mac desktop session and cloud sessions). They share **nothing but this GitHub repo**: artifacts, Notion and
databases on one account can't be read from the other. Push anything the other side needs here.
Updated 4 Oct 2026 (afternoon UTC), cloud session on branch `claude/funny-newton-gd9w8v`. **Start with "4 Oct"
just below (`STUDIO.md` maps everything), then "3 Oct evening", "3 Oct: jazz", "2 Oct" and the rest.**

## 4 Oct, afternoon: "we go full in with yt" (the user, at work: do everything possible, list what only they can do)
- **Go-live page** (the user's checklist, on their phone): https://claude.ai/artifact/SGW5GGULhWhdNZxaBtMNSm. Four steps
  only the user can do: make the three channels (youtube.com/channel_switcher), dress them (art and copy in the page),
  verify by phone, connect YouTube in Zapier (one connection per channel). Then Claude uploads everything.
- **Nothing was connected on 4 Oct:** vidIQ is signed in (to a different Google account from the user's Claude email)
  with no channel; Zapier had no YouTube connection (its YouTube actions are now enabled: find_video, get_report,
  add_video_to_playlist, upload_video, upload_video_thumbnail, _zap_raw_request); Higgsfield has no TikTok account.
- **Upload plan:** `channel/uploads.json` from `lab/tools/plan_uploads.py` (SLOTS = the 5-18 Oct running order: 10 films,
  41 Shorts; every slot checked against YouTube's limits; the season descriptions are cut to fit 5,000 bytes and no
  longer claim the single episodes are on the channel). Route: `UPLOADING.md`, "Route Z" (Zapier opens a resumable
  session, `youtube_upload.py put` streams the file from here). GitHub releases are refused in this session type, so
  public hosting of the 247 MB films isn't available; googleapis.com is reachable for the direct stream.
- **How They Profit films 02 and 03** voiced with Sterling (about 36 credits each): McDonald's 8:01 (page
  https://claude.ai/artifact/XBJfqmdXyYQvA9syVe35YZ, Shorts https://claude.ai/artifact/PwxaSffr73rhXBtRf7qdNH), Costco
  7:20 (page https://claude.ai/artifact/CRxtMNF8YCwFzcrqz7rWQQ). **Film 04, The Cloud Behind the Cart** (Amazon: AWS 18%
  of 2025 sales, 57% of operating profit; sourced from the FY2025 8-K) written, storyboarded (`kit.server`, `kit.parcel`),
  voiced and rendered the same day, for Tue 20 Oct. Next HTP topics: the trend board (Canada's tariff, PayPal). `engine/voice_hf.py` now squeezes any quiet
  stretch inside a line over 1.3 s down to 0.8 s (Seed Audio paused 8 s mid-line in McDonald's take 4);
  `ch2/endcard.py` stretches the card up to 20 s when that carries a film past 8:00 (mid-rolls).
- **Money Crimes:** three more Ponzi Shorts (zarossi, barron, end) for 16-18 Oct; the Ponzi Shorts page has all 7.
- **Season pages** republished: their descriptions were over YouTube's 5,000-byte limit (now ~4.5 KB, via
  `pack/build.py season_description()`), and they now follow the go-live plan (the EPs go out only inside the seasons).
- Credits: about 27 Higgsfield left after film 04 (keep for retakes). Week 3+ for The Curve and Money Crimes needs a
  top-up: a Curve long film is ~130 credits, a Money Crimes film ~200, a How They Profit film ~36. vidIQ: 21 (resets 5 Oct
  to 150; title scoring costs 5 a title, so score the week's titles then).

## 4 Oct, early hours: LF03 shipped, How They Profit film 01 shipped, Money Crimes film 02 (Ponzi) rendering
- **The Curve LF03** (Too Dangerous to Release, 11:57): re-rendered after fixing 15 caption errors (names like Amodei,
  Krueger, Jain; "99 %" and "open -source" now merge in `curvelf/kit.py`); 3 thumbnails, POST.md, 3 Shorts; pages:
  film https://claude.ai/artifact/8sMGypbJ7BnKu8Zvkxqikr, Shorts https://claude.ai/artifact/ErxxqE9BmuSbxpFZgJbzBy.
  `longform/vertical.py` now draws only the newest caption group (two used to overlap for a frame at hand-overs; Shorts
  cut before 4 Oct have that blip).
- **How They Profit film 01** (Banks With Wings, 7:40): there's no ElevenLabs key, so the voice is Higgsfield Seed Audio
  preset **Sterling** (`dc382508-c8bd-443c-8cb2-46e57b8d2e6f`, speech_rate -10), one take per floor, cut back into
  lines at real silences by the new `lab/engine/voice_hf.py` (takes in `lab/ch2/ep01/hf_voice.json`).
  `engine/mix.py` accepts engine="higgsfield" (the guard still keeps the local stand-in voice out). New
  `lab/ch2/endcard.py` adds a 15 s end card. Page: https://claude.ai/artifact/FDHDmXNLLTdKuFpbVmMrbp; its 5 Shorts:
  https://claude.ai/artifact/NjP42S3wuphcMSXHhi2BqQ. Films 02-03 (McDonald's, Costco) voice the same way.
- **Money Crimes film 02** (`lab/longform/ponzi`, The Original Ponzi Scheme, 13:27): sourced script (Wikipedia,
  Smithsonian, Boston.com), Imogen voice (12 takes; take 10 re-voiced, take 11 in halves `vo_11a/b` joined by
  `fetch.py`), 55 stills + 6 clips (Ponzi never drawn face-on; his face is the real 1920 photographs in `src/arch`),
  jazz score, `film.py` timeline, 3 thumbnails, POST.md, `shorts.py` (line, machine, run, today). Done 4 Oct: film
  https://claude.ai/artifact/XaV9wVSnvrJzPA2HEV7Ngj, Shorts https://claude.ai/artifact/3dQC4krr7X2cssm2o6CcJK. Three
  more Lustig Shorts (bribe, certificate, rules) were added to https://claude.ai/artifact/2A19evbUw3Lsz8Kftyj2d1.
- Disk: the session's write allowance filled up mid-render on 4 Oct (the render died with ENOSPC). Rebuildable scraps
  were deleted (published page copies in `lab/pack/build`, render segments and HQ masters of finished films); keep an
  eye on `df -h /home/user` before long renders, and delete `lab/pack/build/<page>` once a page is published.
- Credits: about 135 Higgsfield credits left after the Ponzi pictures (4 Oct). LF04/LF05 need about 130 each.
- Still open with the user: the AI influencer persona, the services offer, and whether LF03's topic is OK.

## 3 Oct, near midnight: the What if POV format (read `channel/what-if/README.md`)
- The user sent nine TikToks that were "popping off" (the @pov.what.if0 "What if...?" POV films) and asked for ours
  with "way more surreal 4k, unreal engine visuals", the same layout, and "very advanced sound design... deep bass,
  like fireforce bass moments, tastefully". They'll often put their own TikTok sound on top.
- Film 01, "What if Earth fell into a black hole?" (70 s): 8 GPT Image keyframes + 7 chained Kling 3.0 clips (start and
  end frames), real-physics readout (distance, tides x the Moon's), the reusable Remotion template
  `lab/motion/src/whatif/WhatIfPov.tsx`, sound by `lab/whatif/sound_blackhole.py`. Media URLs in
  `lab/motion/public/whatif/blackhole/jobs.json` (`python3 lab/whatif/fetch.py blackhole` restores them). Post copy:
  `lab/whatif/blackhole_POST.md`. About 130 credits.

## 3 Oct late: launch three channels (read `channel/LAUNCH.md` and `MONEY.md`)
- The user: set up the YouTube channels with every asset, schedule a week of posts that can be tweaked, review and adjust;
  three channels at a high standard first (The Curve, Money Crimes, How They Profit), ten live by 31 October, every
  platform; then the AI influencer, affiliates and our own products. "We steam roll to making money."
- Kits (profile picture, banner, watermark, X/Facebook covers, `SETUP.md` with names, handles, bios, keywords, defaults):
  `channel/the-curve/brand/`, `channel/money-crimes/brand/` (new, `lab/brand/money_crimes.py`),
  `channel/channel2/brand/` (The Margin renamed **How They Profit** in `lab/ch2/ledger.py`; "Margins" was taken).
- `channel/LAUNCH.md`: one-time set-up steps, the week-1 schedule (5-11 Oct) per channel and platform, the review rules,
  the path to ten channels. `MONEY.md`: every avenue ranked by how soon it pays (services first).
- LF03: word timings, voice and music built on 3 Oct night; render next (`python3 kit.py lf03_held render`). Note the
  new first step on a fresh checkout: `python3 ../longform/tools/words.py lf03_held/src/vo_[0-9][0-9].wav`.

## 3 Oct night: the goal is now 50 channels by 1 Feb 2027, fully automated (read `AUTOMATION.md`)
- The user: set up every API, MCP and connector to automate creation, analysis, critique, upload and review, and have 50
  channels live by the February rule change. `AUTOMATION.md` has the limits (factory networks get terminated; one phone
  number verifies two channels a year; uploads by API need Google's audit), the route (5 proven formats, then
  translations, then new formats, about 8-10 formats x 5-6 languages), every stage's tool and status, and the steps only
  the user can do (channels, Zapier YouTube, vidIQ channels, Metricool, Google Cloud project).
- The other account's work (branch `claude/lucid-archimedes-77tqpt`) is merged here except its superseded `lab/deliver`
  video copies: `UPLOADING.md`, `lab/tools/youtube_upload.py`, the HQ status board (`lab/hq`, published on that account:
  https://claude.ai/artifact/K9nGAFNLCWCuroi2Mwg8He), the brand kit (`lab/brandkit`), the screening room
  (`lab/screening`), and the bios/banner without a posting-rhythm promise.

## 3 Oct evening: handed over to the other account (START HERE)
The user (3 Oct, evening): "Save everything for other claude account to pickup". Everything is pushed; this account's
scheduled check-ins (LF03 continuation, PR #1 hourly) were cancelled so the two accounts don't both work the branch.

**What the user asked for today, in order**
1. Jazz instead of synth beds for Money crimes / true-story films: done (section below).
2. "first i need daily uploads from 1st channel ... make 5 day backlog, then we do other channels": the channel is
   **The Curve** (picked in chat). Five long-form films (12-15 min, 16:9), one a day, each with 3 Shorts, thumbnails,
   POST.md and upload pages. Then the other channels (What if, Maps & power, The Margin).
3. Remotion for motion graphics ("do this: it will help alot with vids and motion graphics"): done, `lab/motion`.
4. Declined (do not revisit): a fake Tesco text-message screenshot (fabricated record), asked twice.

**The Curve long-form backlog** (engine `lab/curvelf/kit.py`; per-film steps in `channel/the-curve/README.md`)
| # | Film | State |
|---|---|---|
| LF01 | The AI That Escaped (13:19) | Finished; pages on the cloud account |
| LF02 | The Price of Thinking (10:48) | Finished 3 Oct: thumbnails, POST.md, 3 Shorts, pages on the cloud account |
| LF03 | Too Dangerous to Release (GPT-6.1 Astra cancelled, the UK AISI test, Gemini 4 Argon for defenders only, Mythos, the FTC) | Script, voice (11 takes), 32 stills and both Kling clips done; **next: render** |
| LF04, LF05 | not started | Candidates: "The Yes Machine" (EP14's sycophancy story at full length), what a one-megawatt AI factory costs and who pays. Bacteriophages are **dropped** (a safety filter stopped the research; don't revisit). |

**Resume LF03 on a fresh checkout** (cloud: 4 CPUs; needs `pip install opencv-python-headless faster-whisper skia-python`)
```
cd lab/curvelf
python3 assets.py lf03_held refetch      # 32 stills + clips (assets_ai.json) and the 11 takes (assets_vo.json; take 7 is
                                         # two halves the voice model would only accept split, joined automatically)
python3 kit.py lf03_held vo              # Whisper (small.en) word timings, squeezes silences -> build/voice.wav, words.json
python3 kit.py lf03_held music           # chapter beds (deep_field / house / garage cycle)
python3 kit.py lf03_held timeline        # check every beat found its words
python3 kit.py lf03_held frames 5 60 300 # QC stills -> build/qc/sheet.jpg (look at it)
python3 kit.py lf03_held render          # ~25 min render + ~15 min encode -> out/lf03_held_1080p.mp4 (<246 MiB, -14 LUFS)
```
Run long jobs in the background (run_in_background), not with nohup. Then: a `thumb.py` FILMS entry (three thumbnails;
ideas: "TOO DANGEROUS TO RELEASE" on the vault, "IT KNEW. IT ATTACKED ANYWAY." on the glass head, "29% WENT ROGUE"),
`POST.md` and `shorts.py` (copy LF02's; Shorts: the cold open, the AISI test numbers, "it knew"), cut them with
`python3 ../longform/vertical.py <abs path to lf03_held>`, add `lf03` / `lf03_shorts` to `lab/pack/build.py` LONGFORM and
the CLI, build, publish (pages over 64 MB go up in batches of about 55 MiB), update `channel/the-curve/README.md` and
`STUDIO.md`, commit, push. All media is recorded: `assets_ai.json` has the 32 stills and both clips (k01 vault door,
k02 loop of light).

**Accounts and tools**
- Pages (claude.ai artifacts) are private to the account that published them: rebuild with `lab/pack/build.py` and
  republish on the other account if needed. The finished films are not in git (too big): re-render from the repo.
- Higgsfield job IDs in `src/jobs.json` / `vo_jobs.json` only resolve on the cloud account, but the result URLs in
  `assets_ai.json` / `assets_vo.json` are public, so `refetch` works anywhere. Cloud-account credits: 504 at handover.
- Voice: Higgsfield Seed Audio preset "Harrison" `573e5163-59b3-4926-aab1-951ef2985f81` (wav, 48 kHz), one take per
  chapter (`kit.parts`). Stills: GPT Image 2.5, medium, 2k, 16:9 (+ `assets.STYLE`). Clips: Kling 3.0 Pro, 5 s, sound off,
  `declined_preset_id 24bae836-2c4a-48e0-89b6-49fcc0b21612`, start image = the still's job ID. Batches of 6 (429s).
- The Trend desk routine still runs daily at 05:49 UTC on the cloud account and publishes a private page there; its
  findings are filed by hand into `channel/trends/<date>.md` and `BOARD.md`.
- PR bernigglywiggly/bernard#1 (draft, this branch): no CI, no reviews at handover.

**Remotion (`lab/motion`, new 3 Oct)**: Remotion 4.0.532 for code-made motion graphics. Read `lab/motion/AGENTS.md`.
`npm install`, `npm run dev` (Studio), `npm run new -- Name`, `npm run render:sample`. Fonts and audio are local.

**Standing rules** (from the user, still in force)
- Pinterest DtWork7 is personal: never touch it. Don't clone or imitate real people's voices.
- No model identifiers in commits, PRs or anything pushed. Push only to `claude/funny-newton-gd9w8v`.
- Keep replies concise (the user's preference). Never put the local Kokoro voice in anything published.
- The ElevenLabs key never goes in the repo; never ask the user to paste a key in chat. Don't send the user's email
  to services. Don't spend vidIQ credits without asking. Higgsfield credits are fine for creative work.
- Uploading to YouTube is outward-facing: only with explicit permission. No fabricated records, no impersonating
  organisations.

## 3 Oct: jazz for the true-story films
- **The user (3 Oct):** "scrap the background music replace with jazz or house jazz for these sorts of vids, futuristic bg
  music dont match". So Money crimes (and other history/true-story films) are scored with jazz; The Curve keeps its
  synth beds. Source: Kevin MacLeod's jazz (incompetech.com, CC BY 4.0: free on monetised YouTube with the credit line in
  the description). `lab/music/jazz/library.py` fetches and cuts it (`section`, `credit_line`); Higgsfield has no music
  model for this and vidIQ music costs 25 credits a track (21 left on 3 Oct).
- Lustig film: `lustig/music.py` maps each chapter to a cue (Covert Affair, No Good Layabout, Spy Glass, I Knew a Guy,
  Dances and Dames, Opportunity Walks, On the Cool Side, Cool Blast, Walking Along, Faster Does It, Night on the Docks -
  Trumpet, Acid Trumpet ending on the end card); `doc.py lustig mix` then `render` re-delivers without re-rendering the
  picture. Its shorts get the new sound by re-cutting (`vertical.py lustig`); the Eiffel short by `make.py audio`
  (`reel.remix`, picture kept). Credits are in both POST.md files and on the pages.

## 2 Oct: AI video, then long-form first (read this first)
- **The direction (the user):** "go all in on best possible vids... full creative reign", then "i wanna target long form yt
  for money, shorts is bonus and discovery". So every channel ships 12-15 minute 16:9 documentaries (mid-rolls from 8
  minutes) and each film is cut into 3-5 shorts that point back to it. `channel/CHANNELS.md` has the plan and budget.
- **Tools:** Higgsfield (connected on the cloud account): GPT Image 2.5 stills (medium 2k = 1 credit, high = 2.75),
  Kling 3.0 Pro clips (5 s, sound off), Seed Audio TTS (narrators Imogen and Zoe; ~1 credit a take). Batch tools take
  12 at a time and sometimes answer 429: resubmit the failed indices. A "preset recommendation" can block a video job:
  pass `declined_preset_id: "24bae836-2c4a-48e0-89b6-49fcc0b21612"`. Credits: 1,498 at the start of 2 Oct, **851 now**.
- **Shorts (`lab/shorts/reel.py`, 9:16):** Money crimes 01 (Victor Lustig, 63 s) and What if 01 (Earth stops spinning,
  66 s), each with `make.py`, `assets.json` + `fetch.py`, `POST.md`. Page: https://claude.ai/artifact/J5CqJtyMALxMBsxTGb6un6
- **Long-form (`lab/longform/doc.py`):** the documentary engine (see its docstring and `channel/money-crimes/README.md`
  for the steps). Film 01 is `lab/longform/lustig`: "The Man Who Sold the Eiffel Tower (And Conned Al Capone)",
  14:56, 11 chapters, ~320 credits. On a fresh checkout: `python3 fetch.py` (AI media and voice), then
  `python3 ../doc.py lustig render` (about an hour; `segs N` re-renders one chapter). Needs
  `pip install opencv-python-headless faster-whisper`. Wikimedia Commons throttles this machine (about one 1 MB image
  a minute): `tools/commons.py` retries; the film's archive photos are committed in `src/arch` with credits.
- **Film 01 page (upload this first):** https://claude.ai/artifact/B4DiPy9qxvVKaZgucpYK3Q (14:56, 1080p, three
  thumbnails, titles, chaptered description with sources and archive credits, upload settings). Its narration quotes the
  real death certificate in full ("apprentice salesman and counterfeiter"; `vo.py` PATCHES splices the re-read).
- **Shorts cut from film 01** (Capone, the escape, the money box; `lab/longform/vertical.py lustig`):
  https://claude.ai/artifact/2A19evbUw3Lsz8Kftyj2d1
- **Still to do:** film 01 for the other channels (What if, Maps & power, The Margin), about 180 credits each.

## 1 Oct afternoon: house and garage, the narration glitch fixed, female voices ready (read this first)
- **Music (the user: "I don't like the background music... house music, or a bit of garage"; on hearing both: "both of
  them are cool"):** `beds.house` (124 BPM: four-on-the-floor, shuffled 16th hats, an open hat on the off-beat, a
  rolling bass, minor-9th chord stabs Am9 Fmaj7 Dm9 Em7, a plucked 3-3-2 riff at the peak) and `beds.garage` (the
  2-step version at 130: the kick on 1 and the and-of-3, heavier swing, organ stabs, gliding subs). Synthesised, no
  samples. The films alternate in upload order (EP05 house, EP08 garage, EP04 house, EP06 garage, EP07 house, EP09
  garage, ... EP14 house), each keeping its key; the trailer and Season One are on house, Season Two on garage.
  Arena is retired. `film.py audition <bed>` lays any bed under a finished film without re-encoding.
- **The narration glitch (the user: "he'll get to the end of a sentence and there'll be a bit buggy moving onto the next
  one... we want it floaty, very human-like and natural"):** ElevenLabs, given the neighbouring lines as context,
  sometimes ends a clip with the first syllable of the next line (after a silence) or starts it with the tail of the
  one before; `engine/voice.py` kept those and cut them off hard (12 of EP05's 30 lines). `voice.clean()` now ends each
  line at the first 120 ms of silence after its last letter and drops a stray sound before a silence at the start, with
  short fades; every timing is unchanged, so no picture re-render: `python3 -m engine.voice <ep>`, `film.py sound`,
  `film.py remux` (swaps the new mix into the finished film, no re-encode), `film.py shorts`.
- **Re-rendered and republished here (scratchpad `night/rollout.sh`, 1h50):** EP04-EP12 (voice, bed, mix, remux,
  shorts), the trailer (sent to the user in chat), both Seasons. Pages: **EP05, EP08, EP04**
  https://claude.ai/artifact/V2Tz5smkY5w1uzroS85YzB and **EP06, EP07** https://claude.ai/artifact/PvzxoDzvJVvKdoXTD6S6pU
  (new: EP04-EP08 with shorts are ~310 MiB, over one version's 256 MiB; `pack/build.py films1|films2`; no thumbnails:
  keep the other account's kit-page thumbnails, whose films still carry the old Arena audio), **EP09-EP12**
  https://claude.ai/artifact/XuGVGPichLJ6oR9TnUS1sq, **Season One** https://claude.ai/artifact/7aPVnXn8UW6LgBUmki6BqV,
  **Season Two** https://claude.ai/artifact/8wNVR2gvWLkZUdvNnGiR44 (same links as before).
- **Female voices, ready to audition:** ElevenLabs premades (nobody's voice copied): `lily` (British, velvety), `alice`
  (British, clear educator), `sarah`, `matilda`, `bella` (American) in `eleven_tts.VOICES`, read with George's settings.
  `python3 tools/voice_audition.py [ep05] [voices...]` reads the film's opening as ONE request per voice (the model
  carries the intonation across sentences, the most natural flow; the films are voiced line by line) over the house
  bed, -> `lab/out/voice/audition/`. Needs `ELEVENLABS_API_KEY` (in the environment's settings, never in the repo);
  about 600 characters per voice. If the user picks a female voice (or the one-request flow for George), the films get
  re-voiced and re-timed: the pictures re-render.

## NEXT SESSION, START HERE (1 Oct, ~10am UTC): polish, prep the channel, upload
**The user, after watching:** "I'm not mad at the videos at all. Let's just make sure that they're polished and then
we'll get them up... the main thing is just getting the videos up, we can change and improve as time goes on."
The other account has a page for the channel's **design and style**: use it for the channel art and look; don't
reinvent it here.

**1. Fix first: the cold opens cut mid-speech.** The user: the "time-travel clips at the very start... cut halfway
through the speech, so it sounds really unrefined, a bit messy". Cause: the montage (`lab/trailer/make.py` main()
and `lab/season1/make.py` cold_open(), both from `trailer.SEGS`) slices `voice.wav` from `ls(first) - PRE (0.35 s)`
to `le(last) + POST (0.55 s)` with no audio fade and no clamp to the neighbouring lines, so when George's next line
starts within 0.55 s, its first syllable is in the clip (and the previous line's tail can be in the pre-roll); the
captions are drawn until t1, so the next line's first word flashes too. Fix (status below): clamp each clip to
whole lines (t0 >= previous line's end + 0.08 s, t1 <= next line's start - 0.08 s), fade the audio (~40 ms in,
~150 ms out), draw captions only until the clip's last line ends. **Done in code (commit ebdf66c,
`trailer.span()` / `trailer.faded()`): the old tail took in 0.12-0.19 s of the next line in four of five clips.**
**Rebuilt and republished (10:15 UTC):** checked all nine clips (Season One's five, Season Two's four): each starts
after the previous line ends and stops before the next one starts. Season One (14:01) and Season Two (10:57) pages are
republished at the same links. The fixed **channel trailer** (38 s) was sent to the user in chat; it replaces the one
on the other account's kit page (or rebuild it there: `cd lab && python3 trailer/make.py`, which needs EP04-EP08's
`build/voice.wav` and `*_clean_silent.mp4`, i.e. those films rendered first). Season rebuild for reference:
`python3 season1/make.py open` then `join` (`SEASON=2` for Two), then `python3 pack/build.py season1|season2`.
**2. Prep the channel** (with the other account's design): name and handle (@thecurve, @thecurveai, ...; check), the
banner/avatar/watermark (the design page's, or `lab/out/brand/` from `python3 -m engine.brand`), the about text and
every setting in `lab/out/brand/channel_setup.md` (AI disclosure ticked on every upload, category Education, not made
for kids), the trailer as the channel trailer, playlists (Every film; one per topic).
**3. Upload on the calendar:** EP05 first (it was due Thu 1 Oct), then a film every two days (EP08, EP04, EP06,
EP07 from the other account's kit pages), Season One Sat 10 Oct, EP03 Sun 11 Oct (other account: Blender frames),
EP09-EP12 13-19 Oct, Season Two Tue 20 Oct, EP13 Wed 21 Oct and EP14 Fri 23 Oct once voiced. Shorts daily.
**4. Then:** the voice queue below (EP13, EP14, Channel 2 x3; needs ELEVENLABS_API_KEY); rename Channel 2
("Margins" exists). **Later polish the user wants to explore:** 3D Blender animation in the films (they'll bring
references); park it until then.
**Where the 1080p files are:** this account's pages (links in the next section; the user can download from them).
The masters live only in this account's container; another session rebuilds them from the repo:
`cd lab/<ep> && python3 film.py parts 4 0 4 && python3 film.py join 4 && python3 film.py sound && python3 film.py
master && python3 film.py shorts` (one film at a time; ~6-15 min each on 4 cores; a tracked job dies at ~30 min;
EP09 needs `pip install matplotlib`).

## Overnight 1 Oct, into the morning (the other account, branch `claude/funny-newton-gd9w8v`)
**Ready to upload:** EP05-EP08 (the other account's kit pages, below), **Season One**
(https://claude.ai/artifact/7aPVnXn8UW6LgBUmki6BqV, Sat 10 Oct) and **EP09-EP12**
(https://claude.ai/artifact/XuGVGPichLJ6oR9TnUS1sq, 13-19 Oct) and **Season Two** (EP09-EP12 as one 10:58 film,
https://claude.ai/artifact/8wNVR2gvWLkZUdvNnGiR44, Tue 20 Oct; `SEASON=2 python3 season1/make.py cards|join|thumbs`,
`python3 pack/build.py season2`). **Ready to voice:** EP13, EP14 and Channel 2's three
films (the voice queue below). **Blocked here:** EP03 (Blender frames).
Picked up while the user slept; nothing here duplicates the queue below. Merge this branch into yours (it fast-forwards
from b05809d plus the commits listed here).
- **Rebuilt the five finished films** from the repo (George from the line cache, Arena, `film.py parts/join/sound/master`):
  the 1080p masters live only in this account's container, so the pages below carry them.
- **Season One** (`lab/season1/make.py`): the five films as one **14:02** film for YouTube (cold open of George's
  strongest lines, THE CURVE · SEASON ONE, a chapter card per film, the wordmark outro with his cached closing line),
  chapters + a description with every film's sources, three thumbnails (A globe, B bulb, C robot + VR operator).
  Long-form = watch hours + mid-rolls. **Upload page: https://claude.ai/artifact/7aPVnXn8UW6LgBUmki6BqV** (goes up
  Sat 10 Oct, the day after EP07).
- **Upload pack pages** (`lab/pack/build.py`): each film's 1080p .mp4 cut into fragmented-MP4 pieces (≤15 MB per
  artifact file) that the page streams (hls.js) and joins back into one .mp4 on download (`downloads` capability),
  plus thumbnails, titles, description, pinned comment and the film's shorts.
- **EP09-EP12**: rendered here (EP09 2:23, EP10 1:56, EP11 3:02, EP12 2:21), each with two thumbnails and its shorts.
  **Upload page: https://claude.ai/artifact/XuGVGPichLJ6oR9TnUS1sq** (films, thumbnails, titles, sourced descriptions,
  pinned comments, shorts with posting days; EP12 added when its render finished). On the calendar 13-19 Oct.
- **EP13 "The Ninety-Minute War"** (`lab/ep13`): the bank's EP02 rebuilt for 16:9 (as EP12 was from EP01): script with
  ids and cards (facts re-checked: 22 Sep 2026, Opus 5.5 to $4/$20, GPT-6 Sol and Luna ~90 min later at about half),
  scenes on the shared engine (a log price ruler, $100 to 1 cent), film.py, shorts clips, kit entry (Wed 21 Oct).
  **Not voiced**: the 9:16 cut used another speed, so 23 of 24 lines aren't in the George cache at 1.0. A session
  with the key runs `cd lab/ep13 && python3 film.py voice`, then `parts 4 0 4`, `join 4`, `sound`, `master`, `shorts`.
  The scenes were checked on an estimated timeline (`python3 tools/est_timeline.py ep13`, `EP_BUILD=build_est`),
  never on a real voice: look at a few stills after voicing.
- **EP14 "The Yes Machine"** (`lab/ep14`): why chatbots flatter (OpenAI's April 2025 rollback; its own words on the
  thumbs-up signal; Anthropic's 2023 sycophancy study; The Emperor's New Clothes). Script, scenes, film, kit entry
  (Fri 23 Oct). Not voiced, like EP13.
- **VOICE QUEUE (for a session with ELEVENLABS_API_KEY)**, about 19,500 characters in all:
  1. `cd lab/ep13 && python3 film.py voice` (24 lines, ~1,850 chars), then `parts 4 0 4`, `join 4`, `sound`, `master`,
     `shorts`; the same for `lab/ep14` (24 lines, ~1,840 chars).
  2. Channel 2, Curve Elder A: `cd lab && EL_VOICE=elder python3 -m engine.voice ch2/ep01` (53 lines, ~5,200 chars),
     then `ch2/ep02` (54, ~5,500) and `ch2/ep03` (52, ~5,100). That writes each film's `build/voice.wav` and
     `lines.json`; the ledger-look scenes come next (see `channel/channel2/BIBLE.md`).
- **EP03** can't be rebuilt here: its cold open needs the Blender frames (`ep03s/build/d24/*.png`) and its lines are
  cached only at the fast 1.2 speed. It stays with the account that has them (Sun 11 Oct on the calendar).
- **Channels plan** (`channel/CHANNELS.md`): the Partner Programme bar doubles on 1 Feb 2027 (8,000 h or 20M Shorts
  views for new applicants), and "inauthentic content" removes templated AI channels, so channels 2-5 need their
  own format, look, voice and music. **Channel 2 bible** (`channel/channel2/BIBLE.md`, The Margin: one company's
  money machine per film, 8-10 min, Curve Elder A as narrator) and its **sourced pilot script**
  (`lab/ch2/ep01/script.py`, "Banks With Wings"; needs the ElevenLabs key to voice: `EL_VOICE=elder`). Overnight:
  the pilot grew to 8 min (v2), plus **film 2 "The Landlord in the Golden Arches"** (McDonald's rent: $10.4B in 2025,
  more than its net income) and **film 3 "The $65 Membership"** (Costco: fees are half its operating profit), every
  figure from the latest filings and sourced; ~930-960 words each, ~8 min at Elder A's pace. **The ledger look v1**:
  style frames in `channel/channel2/look/` (`lab/ch2/look.py`, IBM Plex Serif + Mono, receipts, split bars).
- Render notes: 4 slices take a 2:45 film ~12 min on 4 cores alone; two films' slices at once double both, and a
  tracked job dies at ~30 min, so run one film's slices at a time. Never edit a shell script while a job runs it.

## Links (this account)
- **Curve Lab** (v7 showcase: pilot, 4 visual directions, sound palette, jungle beds, voices, refs, Higgsfield prompts):
  https://claude.ai/artifact/GvXy78rkrDiKJB418rxpsG. The user's picks save to its db, collection `picks`
  (docs: `pilot`, `visual`, `voice`, `bed`, `sfx`, `notes`, each `{value}`). Read them with ArtifactData first.
  Source: `lab/page/index.html` (+ `__LINES__` from `lab/pilot/build/lines.json`); media is published in the artifact.
- **Takeaway Round** (walk-in sales kit: routes, pitch, audit, kit links, tracker): https://claude.ai/artifact/2f7kucmy3ptWePJ4UPgNUU.
  Tracker db: `prospects/<FHRSID>` `{name, town, status, notes, value, updated}`, `setup/<step>` `{done}`.
  Source: `sales/takeaway_round.src.html` (+ `__SEED__` from `sales/prospects_routed.json`).
- Other account: v6.2 review page https://claude.ai/artifact/UcDevRSPUUxQznXKfMLAvL (not readable from here). Notion "QUIT HQ" lives there too.

## State
- **A01 (calm, George, v6 "Chrome & Marl")**: the full ~5-min build is **on the Mac only** (`~/youtube/a01_v6/full.py`,
  `sfx_mech.py`, the full George voice, a jungle bed; handoff `~/RESUME_HERE_2026-09-26.md`). It needs the sound pass
  and the final render, then upload. Fastest: resume that Mac session (sign it into whichever account has credits).
  Or push the folder to branch `mac-sync` (command in the Curve Lab page, section 11) and finish it in the cloud.
- **v7 lab (this session)**: `lab/`. A 105 s pilot "THE CURVE" in a new renegade register (exo-gunslinger voice,
  cinema room, jungle bed, mechanical SFX, holographic/ASCII visuals with a moving camera). Waiting on the user's picks.
- **Sales**: 85 independent takeaways/cafés (FSA register, Sept 2026) in walking order for Stone, Newcastle-under-Lyme
  and Tamworth. "Here" (the user's home town) is still unknown: ask, then pull its council's FSA file the same way.

## Newest (30 Sep – 1 Oct): George + Arena, finished; channel art; the trailer; EP09 and EP10
- The user's call (30 Sep): "george, lets just get it done and posted, backlog and keep chugging, so far just making
  stuff no uploads, need to get on that asap". So: **George at speed 1.0 over the Arena bed**, every film finished,
  uploading made as easy as possible, new episodes keep coming. The elder narrators below are parked.
- **Finals** (George 1.0 + Arena, -14 LUFS, -1.5 dBTP), all sent in the chat: EP05 2:51, EP08 2:15, EP04 2:51,
  EP06 2:16, EP07 2:36. Shorts: EP05 10, EP08 7, EP04 11, EP06 8, EP07 8. EP03, EP09 and EP10 in progress.
- **Posting kit**, two pages (an artifact version holds 256 MiB): page 1 https://claude.ai/artifact/GgTivRE2Kt7UbrafqUJFrE
  (EP05, EP08, EP04, plus the set-up card: channel art, bios, keywords, the trailer) and page 2
  https://claude.ai/artifact/M3fLPJ8vZudgPRuicR93p4 (EP06, EP07, EP03, EP09, EP10). `python3 -m engine.kit [1|2]`
  writes `lab/shorts{,2}/index.html` and prints its files map; an update only needs the new or changed files
  (64 MB per publish). A film's card appears once its shorts are newer than its `lines.json` (`kit.fresh`).
- **Calendar** (`engine/kit.py`): a film every two days from Thu 1 Oct, in the order EP05, EP08, EP04, EP06, EP07,
  EP03, EP09, EP10; each film's shorts start on its upload day.
- **Channel art** (`python3 -m engine.brand` -> `lab/out/brand/`, committed): banner 2560x1440, avatar 800x800,
  watermark 150x150 (solid, transparent), Facebook cover, X header, four Instagram highlight covers, `about.txt` and
  `channel_setup.md` (every name, bio, keyword, setting and pinned comment, platform by platform). Handles to try:
  @thecurve, @thecurveai, @thecurve.explained, @curveexplains.
- **Channel trailer** (`python3 trailer/make.py` -> `lab/trailer/build/the_curve_trailer.mp4`, 39 s, sent): George's
  strongest lines from EP05, EP06, EP08, EP04 and EP07 over their own pictures, one Arena bed, the ears going, then
  the wordmark and "This is The Curve. The hidden mechanism behind the AI headlines. A new film every two days."
- **EP09 "The Laundry Problem"** (Moravec's paradox; `lab/ep09`, voiced 2:17, `arena:key=3`) and **EP10 "Counting
  Sums"** (the 10^25 compute line and Goodhart's law; `lab/ep10`, voiced 1:50, `arena:key=-3`): script, scenes and
  voice done; `film.py render 4`, `sound`, `master`, then `shorts.py` next.
- **EP03** at the new pace: `ep03s/render_waves.py` (two waves of four slices, then a captions pass), then
  `EP03_FULL=1 python3 ascii_open.py sound_full`, then `python3 shorts.py`.
- **Cloud limits**: a tracked background task is killed at about 30 minutes, so run each step as its own task;
  nohup'd jobs die when the idle container restarts.

## Earlier (29 Sep, ~1am): a deep elder narrator (the user asked for "a Morgan Freeman voice variation")
- Not an imitation of him (the user's own rule: no copying real people's voices; he has also objected publicly to AI
  copies of his voice). Instead, three archetypes designed in ElevenLabs from a description (an older American man,
  very deep, warm, slightly gravelly baritone, slow and calm, a veteran documentary narrator) and saved to the
  account: **Curve Elder A** `zCRDVM74mhi1dWed3bbU` (deep, warm, clear; ~88 Hz, ~125 wpm), **B**
  `HZMgvLFIGAb1Xo3Q0QT6` (deeper, rougher), **C** `Al2jx16NmIFECTUrK4O7` (very gravelly). Names in
  `tools/eleven_tts.VOICES` (`george`, `elder`, `elder_b`, `elder_c`); the elders use steadier settings (`CALM`).
- Any film can be voiced by one in its own folder: `EP_BUILD=build_elder EL_VOICE=elder python3 film.py voice`
  then `render 4`, `sound`, `master` with the same two variables (script: `elder_ep08.sh` in the scratchpad). EP08
  in Elder A runs 2:31 (voice built; picture next). The audition reel (George, A, B, C on the same opening over
  Arena) was sent in the chat.

## Earlier (29 Sep, after midnight): Arena, and the ears going
- **The user on Deep Field:** "still way too lighthearted. It needs to be as serious as The Son of Flynn" (Daft
  Punk, Tron: Legacy), and the arena build-up (the crowd chanting "Rinzler"), and the moment "all the sound got
  muted... your ears sort of lose hearing... then slowly come back". They'd also like to hear the real track under
  a film, privately, never published: we can't fetch or ship Daft Punk's audio, so `film.py nomusic` makes
  `build/<ep>_no_music.mp4` (voice + picture sounds only) for them to lay it under in CapCut themselves.
- **Arena** (`beds.arena`, preview `lab/out/music/new/arena.mp3`): an original in that style, 100 BPM, D minor,
  Dm Bb Gm A: low brass (open fifths in a, full chords in b), a low-string ostinato on a D pedal, a mechanical synth
  arpeggio, war drums and a driven bass in b, a braam on each arrival, tremolo strings and a Shepard tone in the
  breaks, a slow violin line. Nothing bright; the weight is low, so it stays serious under the voice.
- **The ears going** (`engine.mix.deafen`, `film.main(..., deafen=("line_id", ...))`): just after the line before,
  a hit, then music and picture sounds drop behind a low-pass (18 kHz to 260 Hz in 70 ms), hold 0.7 s under a
  ring at ~6 kHz, and open again over 3.5 s; George's next line cuts through clear. EP08 uses it before "ai" (the
  cold open's turn) and "imagine" (the what-if).
- **The queue now renders pictures only** (`pictures.sh` in the scratchpad: EP04, EP06, EP07, then EP03 captioned and
  clean); sound, master and shorts wait until the user approves a bed. EP05's picture and voice are done.

## Earlier (29 Sep, night): George at his own pace, and Deep Field
- **The user (28 Sep, late):** the music should be "more serious... futuristic tech, sort of deep house"; the beds
  "don't really lock people in", too light; and the pace is "way too fast": "go back to the original voice speed",
  with the video synced to it. (Earlier that day they had asked for fast; this reverses it.)
- **Voice:** ElevenLabs speed **1.0** (was 1.2) and a breath between sentences (`engine.voice.gap`: 0.30 s, most of
  a half-bar per unit of `air`, 0.35 s before a `cut`). `EL_SPEED=1.2` rebuilds the fast cut exactly. The scenes are
  keyed to line ids and word times, so the picture re-times itself; EP03's Blender frames warp line by line
  (`relay._warp`). Films run ~25% longer (EP08 2:15, EP05 2:44, EP04 2:44, EP06 2:09, EP07 2:30).
- **Deep Field** (`beds.deep_field`, preview `lab/out/music/new/deep_field.mp3`): dark deep house at 112 BPM, F minor
  (round 4/4 kick eased in, off-beat bass, filtered m9 stabs with dotted-8th echoes, a pumping pad, a pulse arp, a far
  glass motif; breaks drop the drums). `key=` moves it per episode: EP08 F (`deep_field`), EP05 D (`:key=-3`), EP04
  G (`:key=2`), EP06 C (`:key=-5`), EP07 E (`:key=-1`), EP03 A (`key=4` in `ascii_open.score_full`). Reasoning, from
  the literature: slow + minor reads as serious (Gagnon & Peretz 2003; tempo weighs more than mode), fast + loud
  background music hurts comprehension (Thompson, Schellenberg & Letnic 2012), so it stays moderate and under him.
- **Mix:** the music is split at 160 Hz; above it ducks 12.5 dB under the voice, the kick and bass only 9, so the
  groove holds; it sits ~13 LU under George (-27 vs -14 LUFS; it was ~-29). The bed now plays from frame one (an
  extra intro bar cut in by `engine/score.py`), not after up to a bar of silence.
- **The fast cuts are kept** beside the new ones in each `build/` as `fast_*` (film, lines.json, mix, bed) and
  `fast_shorts/`. EP08 was the test sent to the user; EP05, EP04, EP06, EP07 follow (the queue script lives in the
  session scratchpad), then EP03.
- **Kit:** the slower shorts don't fit one 256 MiB version, so the kit is two pages: `python3 -m engine.kit` (EP03-EP05,
  the existing artifact) and `python3 -m engine.kit 2` (EP06-EP08, "The Curve Shorts II", `lab/shorts2/index.html`;
  put its URL in `engine/kit.py` PAGES so the pages link to each other). Thumbnails are unchanged (same pictures).

## Earlier (28 Sep, afternoon): the factory — the engine, the posting kit, EP04, EP05
- **The user's plan:** break every long video into shorts (parts that add up to the whole, plus highlights), push them
  hard on TikTok, Reels, YouTube Shorts and Facebook, then repeat across 5-10 channels ("quality of volume").
- **Posting kit** (artifact, `downloads` capability): https://claude.ai/artifact/GgTivRE2Kt7UbrafqUJFrE. Per episode:
  the full film (720p preview; title and description with sources to copy; the 1080p file goes in the chat), a
  suggested posting order, the parts, the highlights, each with its caption + hashtags. Source `lab/shorts/index.html`,
  built by `cd lab && python3 -m engine.kit` (it prints the files map to publish: `media/<slug>/<file>` → disk).
  Media limits: 15 MB per file, 64 MB per publish (publish in batches: files left out are kept), 256 MiB per version.
- **The engine** `lab/engine/`: an episode is `script.py` + `scenes.py` + a small `film.py` (see `lab/ep05/film.py`).
  `python3 film.py voice | lines <t..> | still <t..> | render 4 | sound | master | preview | shorts | all 4`.
  Modules: `tl` (line and word times from lines.json: `word("line_id", "word")`), `draw` (formations, morphs, chrome
  numbers, Big Macs, figures and poses, globe, satellite, sun...), `look` (the ASCII look; the glow is blurred small),
  `captions`, `voice` (George from the cache, or the API with ELEVENLABS_API_KEY), `score` (a bed re-cut by section
  marks and two anchor lines; Mainframe 104, Low Orbit 120), `mix`, `shorts`, `kit`. Render: ~0.6 s a frame a core,
  so a 2:15 film is ~15 min on 4 cores; shorts ~1 min each. EP03 (`lab/ep03s`) predates it and keeps its own scripts.
- **EP04 · The Man in the Machine** (`lab/ep04/`, 2:13, Mainframe): the SF cage fight piloted from a VR headset, the
  Tesla dancer, robot boxing, the G1 as 2,200 Big Macs, the rifle dog, Ukraine's ground robots, Patriot vs Shahed in
  Big Macs, the shrinking loop, a 2030 what-if, a mirrored close. 11 shorts.
- **EP05 · Follow the Sun** (`lab/ep05/`, ~2:14, Low Orbit): timed to Google's Suncatcher launch (four TPUs, set for
  1 Oct 2026). Mills to rivers, data centres to reactors, chips to orbit (up to 8x the solar energy); Starcloud 88,000,
  SpaceX up to 1,000,000 vs ~16,500 working satellites; $7,000 a kilo, so launching one Big Mac costs ~250 Big Macs;
  Google's break-even under $200/kg (~35x cheaper); a 2040 what-if on who owns what catches the sunlight. 10 shorts.
  Post it while the launch is news.
- **EP06 · Who's Human Here?** (`lab/ep06/`, ~1:45, Chrome & Marl): the 2025 Turing test (284 people; the AI picked
  as the human 73% of the time, 36% without its persona), Turing's 1950 30% bar, bots at 53% of web traffic in 2025,
  the agent clicking "verify you are human", the FBI's family secret word, a 2030 what-if. 8 shorts.
- **EP07 · The Thirty-Year Delay** (`lab/ep07/`, ~2:02, Night Drive calm): NBER Feb 2026 (~90% of 6,000 firms saw no
  AI productivity change), Paul David's dynamo story (one big motor on the old shaft; the gains came with a motor in
  every machine), Solow 1987, MIT's 95% of pilots, an office built from zero around AI. 8 shorts.
- **EP08 · Cheaper Makes More** (`lab/ep08/`, 1:45, Terminal): the Jevons paradox (coal 1865; light 3,000x cheaper
  and 40,000x more used; a million tokens from ~10 Big Macs to 1/100 of one; Google's 3.2 quadrillion tokens a month,
  300x in two years; Nadella's post). 7 shorts.
- **Kit storage:** one artifact version holds at most 256 MiB. The kit now carries thumbnails + shorts only (the 720p
  previews came out; the 1080p films go in the chat) and holds EP03-EP08 at ~210 MiB. For EP09 on, either start a
  second kit page ("The Curve Shorts II") or drop the shorts of episodes already posted (publish them as `null`).
- **Every film also gets** a thumbnail (`python3 -m engine.thumb <feed> <t> "LINE|LINE|LINE" <out.jpg> <accent> fx,fy,zoom`)
  and a 720p preview (`film.py preview`); the kit shows both with the YouTube title and description to copy.
- **Channel 2** is still the user's pick (the plan page's vote, db `picks`, was empty on 28 Sep).
- The ElevenLabs key lives only in the session scratchpad (`.el_key`), never in the repo; every voiced line is cached
  in `lab/voice/cache/eleven` (committed), so any session can rebuild the films without the key.

## Earlier: the Six Floors format and EP01 (after the @pollar.news inspo)
- Inspo breakdown: `lab/inspo/pollar_breakdown.md` (frames `lab/inspo/tt1/sheet_*.jpg`, transcript `tt1/transcript.json`).
  The user wants pollar's rigour plus deeper concepts, curiosity, perspective and labelled fantasy ideation.
- Format bible: `lab/format/SIX_FLOORS.md` (GROUND → MECHANISM → YOU → IDEA → IMAGINE → SURFACE, a depth gauge,
  one metric ruler, silence cuts, a mirrored close). Episode bank: `lab/format/EPISODES.md` (facts tagged [V]/[C]/[M]/[I]).
- **EP01 · Sixteen Hours** (`lab/ep01/`, 1080×1920, 2:25): METR time horizons (2 s in 2019 → ≥16 h in Mar 2026),
  the 50% line, a powers-of-ten paper fold to the Moon, the vortex into an ASCII IMAGINE layer, a mirrored close.
  Build: `voice_build.py` → `music_build.py` → `ep01.py render` → `mix.py`; covers: `covers.py`; upload copy:
  `lab/ep01/UPLOAD.md` (pilot: `lab/pilot/UPLOAD.md`). Ladder verified against METR: 2 s, ~30 s, ~4 min, ~1 h, 16 h.
  The inspo MP4 itself is not committed.
- **EP02 · The Ninety-Minute War** (`lab/ep02/`, 1080×1920, 2:47): the 22 Sep 2026 price cuts (−20%, then −50%
  about 90 minutes later; the gap is single-source and flagged on screen), price as the only readable signal, a16z's
  $60 → $0.06 per million tokens, a million tokens ≈ 8 novels for under 10p, the Red Queen (Carroll 1871 / Van Valen
  1973), IMAGINE "when thinking is almost free, what gets expensive?", and a mirrored close. The ruler is price per
  million tokens (log, cheaper to the right). `ep02.py` is **generated**: edit `ep02_parts.py` (or the EP01 engine),
  then `python3 make_ep02.py`. Build: `voice_build.py` → `music_build.py` → `make_ep02.py` → `ep02.py render` →
  `mix.py`; covers: `covers.py`; upload copy: `lab/ep02/UPLOAD.md`. Topical: post it before EP01.
- Offline transcription works: sherpa-onnx + whisper base.en from GitHub releases
  (`k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2`).

## Latest (28 Sep): the format is decided — read `lab/inspo/pollar_playbook.md` first
- **Pollar (@pollar.news) is the core inspiration.** Studied 28 Sep: their hits are AI/big-tech power stories with a
  hidden mechanism (Nvidia's $250B guarantee 4.6M views; an OpenAI agent escaping its sandbox 717K; Meta glasses light
  550K); 2:30-3:00; spoken hooks are concrete and personal, never the headline; numbers made physical by a ladder;
  dated sources; what's unconfirmed said plainly; one visual system per film. (TikTok is reachable now; yt-dlp works with
  `--impersonate chrome` + curl_cffi. Downloads stay in gitignored `lab/inspo/tt*/`.)
- **The user's rules:** NO humour, no swearing, no punchline slots; straight into the facts, then curiosity and one
  labelled IMAGINE; George (ElevenLabs) voices everything, fast (~1.15-1.2); no own-voice recordings, no voice changer.
  Mostly ASCII with a touch of Blender realism (see `ascii_open.py`). All six new beds get used, matched to topic tone
  (table in the playbook and on the plan page). The stickman show is parked (it was built on comedy).
- **Voice blocker:** api.elevenlabs.io is reachable now, but `ELEVENLABS_API_KEY` isn't set. Once it is (new session):
  `cd lab && python3 tools/eleven_tts.py ep03s --speed 1.2` then `cd ep03s && python3 voice_build.py` (auto-picks George)
  then `python3 ascii_open.py render`. Everything re-times itself from lines.json; the Blender frames re-time through
  `relay.D_WARP` (mapping today's lines onto `build/lines_blender.json`, the timeline they were rendered on).
- **EP03 v2** script: `lab/ep03s/script.py` (the old comedic one stays in `lab/ep03/` for the old engine). Facts checked
  28 Sep (Nvidia Q2 FY27 8-K; big-tech 2026 capex ~$725B; OpenAI Q1 2026 via The Information; Clay & Jones 2008; CPI).
- **ASCII v4 (the user's notes on v3, 28 Sep):** v3 was "awesome", but the feedback ("TouchDesigner") moment felt
  sporadic and unpolished, and Terminal took too much attention. v4: the accent is now a phosphor trail in the
  character grid (`ascii_open.trail`: each cell keeps max(now, 0.82 × last frame), eased in at the burst and out as the
  store forms; no zoom, rotation or colour split), and the bed is `beds.night_drive(..., calm=True)`: half-time soft
  kicks, no claps or open hats, the arp in 8ths only in the b section, a softer pad gate. Night Drive's calm cut is
  now the default under a voice (playbook table); Terminal stays for chips/agents/software, thinned out.
- **Analogies, said straight (the user, 28 Sep, after v4):** comedy comes back only through the comparisons, and
  the user wants analogies "as much as possible": what a missile *costs* in Big Macs (their example; cost, not energy),
  a million dollars a day since the Romans invaded Britain, per second, per person, UK houses and salaries. Lines stay
  plain; George reads them deadpan. Rule 12 in the playbook; the sourced bank and calculator is `lab/format/units.py`
  (`usd`, `gbp`, `item`: Big Mac $6.22 = The Economist July 2026; Patriot $4.2M; Tomahawk ~$2M; Javelin $216,717;
  Shahed $20-50K (CSIS); Unitree G1 $16K; UK house £272,611; median pay £39,039). EP03 is now **script v4**
  (34 lines, about 2:55): the cold-open Big Mac line ($466, drawn in `ep03s.markup_beat`), plus Romans, Big Macs a
  second, $1 of every $4, $1.65 out per $1 in, five railway companies a week, London to Tokyo, tap water.
  **ASCII v5** (the cold open with the Big Mac beat, 40.8 s) is on Curve Lab. Old timelines: `build/lines_v4.json`.
- **Mainframe (the user, 28 Sep, on v5):** the calm Night Drive felt "too lighthearted"; they want something closer
  to Tron: Legacy's The Son of Flynn. `beds.mainframe(bpm, plan, lead)` is an original in that style (D minor,
  Dm-Bb-Gm-A, a 16th-note pluck ostinato through a section-opening filter, strings, cello, violins and low brass
  swells in b, booms at section changes, a soft taiko, no drum kit). The cold open is scored with it (v5.1:
  `python3 ascii_open.py mix` re-scores the rendered picture in about 2 minutes); the playbook and plan map EP03
  and serious topics to it. The standalone bed is `lab/out/music/new/mainframe.mp3`.
- **EP03 in full is built (28 Sep, v1.1):** `ep03_body.py` draws everything after the cold open in the same ASCII
  system (plan: `lab/ep03s/FULL_PLAN.md`); labels type on visually (`typeon.py`). Output `build/ep03_full.mp4`
  (1080p, 3:07). **On v1 the user said: no typing sounds, and "go back to the very original British voice ... get rid
  of this voice right now".** So v1.1 has no keystrokes and no voice: captions carry the words until George.
  **Never put the local Kokoro voice in anything the user hears** (bm_george was rejected before, and again here);
  `mix_full.py` now only mixes a voice when lines.json says the engine is "eleven" (George). The ElevenLabs login in
  the user's Chrome can't be used from the cloud; the API key has to go in the environment settings.
- **George is in (28 Sep):** the user sent an ElevenLabs key in the chat (kept out of the repo; only in the session's
  scratchpad); all 34 lines of script v4 are cached in `lab/voice/cache/eleven/` (committed), so any session builds
  with George without the key: `cd lab/ep03s && python3 voice_build.py` (engine "eleven" automatically) then
  `EP03_FULL=1 python3 ascii_open.py full 4`. George at 1.2 runs the film to about 2:36.
- **Particles:** `ep03s.dust_at` is now fixed per-grain smooth paths (pour stream through the neck, fountain matched
  launch-order→landing, drift on the bank, left-to-right re-form); the Blender burst is a cork pop + fountain
  (`blender/cold_open.py`, `LINES_JSON=build/lines_blender.json` to render on the Blender timeline).

## Newest direction (27 Sep): Five by February
- Plan page: https://claude.ai/artifact/8tVyExzYz4cXDneYtUSWxp (source `lab/plan/index.html`; db collections `picks`,
  `lines` = the user's own punchlines per slot id a1..d2, `notes/ideas` = their channel ideas). Read these first next session.
- **Deadline:** from 1 Feb 2027 new YPP applicants need 8,000 watch hours (or 20M Shorts views / 90 days); now 4,000 h or
  10M. Channels already in keep their place. Goal: get channels over 4,000 h before then. Vertical <3 min = Shorts, whose
  watch time doesn't count, so every channel needs a 16:9 long-form backbone.
- **Policy:** since 16 Jul 2026 no ads for generic/templated AI content or AI personas on finance/legal/health; strong
  swearing is fine (since Jul 2025) except in titles/thumbnails, and not constantly.
- **Voice:** "the first British guy" = **ElevenLabs George** (the A01 voice, `a01_v6/voices/george.mp3`), NOT Kokoro
  bm_george (the user disliked it). Pace "pretty fucking fast": samples orig/fast/faster in `lab/plan/media`. Pipeline
  ready in `lab/tools/eleven_tts.py` (speed 1.2, cached in `lab/voice/cache/eleven/`), blocked until
  `ELEVENLABS_API_KEY` + api.elevenlabs.io are allowed (or run it on the Mac and push the cache); Kokoro stands in.
  Style: quick, eloquent, witty, swears where it lands; mark setups as [YOUR LINE] slots for the user's own jokes.
  The user will also try their own voice through ElevenLabs Voice Changer (blocked here; they'll upload results).
- **Next 5 (The Curve):** EP03 Shovel Sellers (new style), Robots "From Spandex Suit to Robot UFC" (user VO), agents
  "Your Job's Night Shift", space compute, "Who's Human Here?". Channel 2 pilot: WW3 Survival Guide with the stickman.
- **Stickman:** `lab/stickman/character.py` (rig + faces + chrome hat; `python3 character.py` → concept sheet). Never
  use the real Trollface (copyrighted); we have our own smug face.
- **Stack:** The Curve, the stickman channel, AI for small business, How It's Built, How They Make Money.
- **Big Man (the stickman show, 27 Sep brain dump):** a god-powered goofball who can't die and never talks (the user
  narrates, sometimes as him); signature move: he rips the frame like paper into the next scene; a flat white cartoon
  inside real-looking backgrounds with real contact (shadows, occlusion, dust, shake); Tom and Jerry / Gen Z editing
  (smash cuts, cut-off reactions, the giant fist, the aux-cable music switch). Tests: `lab/stickman/test_anim.py`,
  `lab/stickman/gag_reel.py`. Guardrails: no famous songs (Content ID), no game assets, our own meme sounds, recreated
  history (no real casualty footage). Blocked: full-size plates (Canva downloads are blocked here; the user uploads to
  `lab/plates/` or allows export-download.canva.com + media.canva.com); ElevenLabs needs `ELEVENLABS_API_KEY` + api.elevenlabs.io.
- **EP03 draft** (`lab/ep03/`): George at 1.02, new register, 7 slots (e2–e8) for the user's punchlines (plan page db
  `lines/e*` → `build/slots.json` → re-voice). 3:35, so a normal video + TikTok; `build/EP03_short_cold_open.mp4` is the 40 s Short.

## Visual direction (27 Sep): back to the A01 morph grammar + a style shoot-out
- The user's favourite draft is the A01 v6.2 "Chrome & Marl" hook: each scene morphs/drives through into a whole new
  visual, always clearly showing the information. They dislike the constant X/Y axes (EP02/EP03's gauge and ruler): drop them.
- `lab/ep03s/`: the EP03 cold open rebuilt in that grammar (`ep03s.py`: formations, `morph_flow`, particles that
  re-form, chrome fills, one push-through). `styles.py` renders it three ways in one pass (A line morph, B heavy ASCII,
  C TouchDesigner-style feedback); `mix_open.py` puts the shared bed + SFX on each; `blender/cold_open.py` is D (Cycles
  on CPU, 12 fps + real 24 fps in-betweens for the fast shots via `--inbetweens`, assembled by `build_blender.sh`);
  `HIGGSFIELD.md` is E (prompt pack, run on the Mac, plates to `lab/ep03s/plates/`).
- All five are on Curve Lab (https://claude.ai/artifact/GvXy78rkrDiKJB418rxpsG, section "Style shoot-out") with
  love/mix picks (db `picks`: `stylelove`, `stylemix`). Build the rest of EP03 in whichever style wins.
- **Decided (27 Sep): ASCII all the way.** One focused style: ASCII (style B) as the channel look, a little Blender
  realism for the big physical objects, the other looks (line morph, feedback) only as rare accents.
  v1 of the look: `lab/ep03s/ascii_open.py` → `build/style_S_ascii.mp4` (Curve Lab card "S · The decided look").
  Grammar: line sources → characters (line mapping); Blender renders → tonal characters; the real Blender image only
  where the characters DEVELOP into it (the bottle of gold, the lone shovel) and break back; one feedback accent
  (character trails) for the frenzy; glints of bright characters over chrome; the prize as an orb of characters.
  Scored with Terminal re-cut so bar lines land on spoken lines (`beds.terminal(bpm, plan, lead)`). Pick: db
  `picks` → `asciilook`. Next: build all of EP03 this way (task: EP03 in ASCII), then the backlog.
- **Music (27 Sep): the jungle is scrapped.** `lab/music/beds.py` renders six new beds (terminal, tape_loop,
  night_drive, low_orbit, two_step, chrome_marl) → `lab/out/music/new/`; `lab/music/analyse.py` checks tonal balance,
  loudness arc, width and clicks (nobody can listen from the cloud). The user liked some *original* music: the A01
  Chrome & Marl bed (`a01_v6/build/bed6.wav` + `sfx6.wav`) and the A01 v5 outro pad are pulled back up. All of it is in
  Curve Lab's "Music box" with picks (db `picks`: `musicnew`, `musicorig`). Keep tops dark and smooth (the user's
  favourite is dark up there; the jungle was fizzy).
- **The relay** (`lab/ep03s/relay.py`, the user's "mix of all, seamlessly blended, contrasting styles"): each beat in
  a different look, 24 fps, with match-moved hand-offs (trace, fill, frenzy, calm, digitise, develop, through the
  ring); captions/label/vignette on top; transition hits in `relay_mix.wav`. Pick: db `picks` → `relay`
  (all / fewer / one).

## What the user asked for (the previous round)
- Video: clean, visually stable, addictive; digital cyber / ASCII / holographic detail; satisfying orchestrated layouts;
  not overstimulating, not bland, nothing tacky. **Camera may move** (orbits around exploded subjects, glides along
  line-work type), tastefully. Palette stays **turquoise + graphite** (the yellow/brown look was a BGRA bug, never a choice).
- SFX: less magical/sparkly; futuristic tech, ethereal, mechanical (satisfying keyboard "banana" switches: most likely
  Keychron Banana tactiles or C³×TKC Banana Split); bass used tastefully for the stomach-drop vortex.
- Music: jungle as a flowing bed. Script: renegade/Rick-Sanchez confidence, fluid, slightly weird-but-cool (santeluca
  structure, see `lab/research/creative_research.md` §1), exponential AI, future possibilities, niche money, gold-rush
  history. Voice experiments incl. a Cayde-6-*like* test (built as an original archetype, no actor cloning).
- Show options and let them pick; full creative freedom; agents allowed.

## What's where
| Path | What |
|---|---|
| `lab/visual/holo.py` | 3D line/point/ASCII renderer on skia: camera, formation reveals, depth fade, glow + bloom, 3D type, ASCII z-buffer, multi-process mp4 writer |
| `lab/visual/clips.py` | the four directions: A exploded accelerator orbit, B type rail, C ASCII torus knot, D curve ride + ring-tunnel fall |
| `lab/pilot/` | `script.py` (lines + on-screen sources) → `voice_build.py` (Kokoro, grid-aligned lines) → `pilot.py` (scenes, captions, cards, sound cues) → `music_build.py` → `mix.py` (ducking, vortex window, -14 LUFS, mux) |
| `lab/sfx/palette.py` | 23 synthesised sounds (thock, typing, relay, latch, dock, servo, hydraulic, ticks, chatter, scan, form, whoosh, sub_drop, thum, vortex, riser, glitch, swell...) → `lab/out/sfx/*.mp3` |
| `lab/music/jungle.py` | synthesised jungle at 170 BPM (breaks, rolls, sub, reese, F-minor pads, FM Rhodes), arrangements + stems |
| `lab/voice/voice_lab.py`, `lab/audio_fx.py` | voice audition/blends, exo colour, ducked cinema reverb, exciter, loudness |
| `lab/research/` | creative research (santeluca, 24 refs, 18 perception rules, Higgsfield presets/prompts, jungle, keyboards); script facts |
| `sales/` | research (suppliers, stats, rules), prospects (+ routed with walking order), the Takeaway Round page source |
| `a01_v6/`, `a01_v5/`, `channel/` | from the earlier cloud session (hook pipeline, backlog A02–A06, money notes) |

## Rebuild (cloud, 4 CPUs)
```bash
pip install skia-python numpy scipy soundfile pyloudnorm pedalboard kokoro-onnx matplotlib; apt-get install -y ffmpeg libegl1
# Kokoro weights come from GitHub releases (Hugging Face is blocked):
#   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/{kokoro-v1.0.onnx,voices-v1.0.bin} -> /opt/kokoro
cd lab/sfx && python3 palette.py                   # sound palette
cd ../music && python3 jungle.py                   # three demo beds
cd ../pilot && python3 voice_build.py && python3 music_build.py && python3 pilot.py render && python3 mix.py   # ~15 min render
cd ../visual && python3 clips.py render A          # or B, C, D; `still A 7.5` for one frame
```
skia pixels are BGRA: keep `-pix_fmt bgra` on the raw pipe, or turquoise turns yellow/brown.

## Blocked from the cloud (network policy)
chatgpt.com (the user's GPT share link couldn't be read; ask them to paste it), Higgsfield (`api.higgsfield.ai`,
`platform.higgsfield.ai`, `cloud.higgsfield.ai`), ElevenLabs, TikTok, YouTube, Hugging Face, Google Maps, the FSA API
(the GitHub mirror `food-hygiene-uk/data` works). Allowing hosts in the environment's Network access + API keys as
environment secrets would let the cloud generate George and Higgsfield clips directly.

## Rules
- The Pinterest account is personal: read-only references, never post, modify or save anything there.
- Don't clone or imitate real people's voices; build described archetypes.
- No model names in commits, PRs or pushed files. Push only to the session's branch.
- Sales: never write reviews for clients, no incentives for reviews, ask every customer (Google policy, DMCC Act 2024).
- The user wants short, concise replies, and to see options before committing to a direction.
