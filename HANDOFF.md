**ACCOUNT B, Wed 28 Oct ~20:45 UK: EVERY CHANNEL ON A ROTA (he, 20:30: "Continue, have all other channels going too and wherever u think best opportunity is to gain views and climb to monetisation best do that, let's get goin").**
- Data (YouTube APIs 20:35): The Curve 42,984 views, 36 subs (Microduck 17,753 in 2 days, Roadster upside down 15,466, iPhone Duo 2,991 in 20 h, SpaceX 844 in its first 3.5 h); How They Profit 183 views, 0 subs; Money Crimes 116, 0; Curva Explica 3, 0. The Curve keeps a Short every day and the most budget; the other three get 2 test Shorts each from Sun 1 Nov in their own looks and narrators, then a views gate (>1,000 views at 72 h = 3 a week; under 300 = 1 a week and its slots go to a second daily Curve Short). Day-by-day lines: `channel/ROTA.md` (the runs read it: change the plan there, not in the tasks). Per-channel specs: `lab/curve_v2/shorts/RUNBOOK_SHORT.md` §8b (Curve topic rule: a viral clip of a machine doing something impossible, explained the day it spreads) and §9 (How They Profit, Money Crimes, Curva Explica: channel ids, Zapier connections, manifests, looks, voices, music, SETUP on the first run).
- New scheduled tasks on this Mac (each skips itself at 92%+ weekly usage; no notifications to this session). **They were saved in the DEFAULT permission mode** (his 20:30 message came through another device, so the app would not keep Bypass): he must set each to Bypass in the app (Scheduled > task > permission mode), or type any message in the desktop app and B re-saves them. Tasks: `b-sun-short` Sat 31 Oct 21:15 (Curve, publishes Sun 1 Nov 17:00), `b-curve-daily` 21:15 every day Nov-Dec, `b-channels-rota` 19:00 every day Nov-Dec, `b-daily-check-0730` 07:30 every day Nov-Dec. Extend the Nov-Dec crons in late December.
- Short 11 (Thu Apple): the 17:40 run stopped at its own 3-round limit with v4 built. An ADDENDUM at the end of ~/.claude/scheduled-tasks/b-thu-apple-short/SKILL.md (the brief the 23:15 and 07:30 checks follow; both checks are still Bypass) lifts that limit: critic round 4 on v4, upload on SHIP, else fix, v5, round 5; upload by 16:30 Thu.
- 20:40: the Mac was on battery at 16% (push sent to him). `caffeinate -s -t 604800` started (stops idle sleep on mains power only, 7 days; `killall caffeinate` ends it).
- Alignment check (Sonnet agent) on the rota: `lab/research/ALIGNMENT_2026-10-28.md`.

**ACCOUNT B, Wed 28 Oct 18:05 UK: THU APPLE SHORT (Short 11) BUILT, NOT UPLOADED: 3 critic rounds ended ONE MORE PASS, so the run stopped before the upload as its brief says.**
- Apple announced it (Newsroom 17:09 UK): "MacBook Pro with PROLED XDR Display", "Touch for the first time on Mac", "a newly designed hinge provides greater stability while using Touch", £2899, on sale Fri 6 Nov. Facts §5 slots 100-109 filled from Apple's own pages (branch T). Federighi 2014 verified (BGR quoting CNET); 2018 WIRED dropped.
- Built: script `lab/curve_v2/shorts/short11.py` (x5 in Apple's words; x6 "Our take? ..."), voice Chris take v2b word-perfect 31.6 s, Apple's film hnZI5uUSdEo for the hook (40.35 s, hand reaching the screen, keyboard in frame), x5 (pinch/drag) and the loop (PSNR 38.8 dB). Kit fix: caption span keys made unique (orphan "A" bug, affects every Short using CaptionTrack).
- Critic: r1 v1 ONE MORE PASS (captions A, frame 0 with no Mac, unverified NO stamps, unsourced end plate) → all fixed in v2; r2 v2 ONE MORE PASS (voiced verdict sounded like Apple's intent) → re-voiced in v3; r3 v3 ONE MORE PASS (the "PROJECTED CAPACITIVE TOUCH" tag clipped off the right edge at ~12 s) → fixed in **v4** `lab/curve_v2/shorts/out/SHORT11_v4.mp4` (-14.3 LUFS, -1.9 dBFS, no frozen stretch; measurements `critic_s11/v4/`). Reports and ledger: `lab/curve_v2/shorts/out/critic_s11/`. Open SHOULDs (cosmetic): caption size varies by page, grid and verdict laptop could be bigger, the Jobs tag pops in small.
- **NEXT (any account with Zapier, i.e. A or B; the 23:15 / Thu 07:30 resume runs can do it):** one fresh Sonnet critic round on v4 (send round3.md; measurements already in `critic_s11/v4/`). On SHIP: manifest index 6 already points at v4 with publish_at 2026-10-29T17:00:00Z → RUNBOOK §7 upload (zapier-init index 6, Zapier POST, put, verify private + publishAt). Not SHIP: don't upload, tell him. Then tick TEAM §4 with the link. Fri 30 = Short 12 (phone clock, task Thu 18:30); Sat 31 = Short 13 (task Fri 18:30).

**ACCOUNT C (cloud), Wed 28 Oct 17:25 UK: Apple fill ran (the cloud's scheduled run).** Branch T confirmed: touch announced. Apple facts rows 100-102, 105-106 filled from press; 103-104, 107-109 still need Apple's own pages (Mac). No separate radar written: the Mac's daily Short runs cover the next picks. That was the cloud's last scheduled run.

**ACCOUNT B, Wed 28 Oct ~15:40 UK: THU APPLE SHORT (Short 11) SCHEDULED, he said yes to the upload ("schedule a run tonight after Apple's event to build, critic-check and upload Thursday's Apple Short, publishing Thursday 17:00").** Local one-off tasks on this Mac, saved in Bypass mode: `b-thu-apple-short` Wed 17:40 (fills §5 of `lab/research/APPLE_PRO_AND_TELL_FACTS.md` from Apple's pages if C hasn't, picks branch T/N1/N2, builds, 2 Sonnet critic rounds, uploads ONLY on SHIP, private + publishAt 2026-10-29T17:00:00Z, manifest index 6, PushNotification), resume checks `b-thu-apple-short-check-2315` and `-0730` (do nothing if it's done or still running). Every step's exact command: `lab/curve_v2/shorts/RUNBOOK_SHORT.md` (new; reusable for every daily Short). Apple Newsroom had nothing new at 15:10 (last: Tue's M6 MacBook Pro + iMac). C's `bernard-c-*` task files exist in ~/.claude/scheduled-tasks but this app's list doesn't show them, so the 17:40 run fills §5 itself if needed. Needs the Mac awake with the Claude app open tonight. **PRE-BUILT 15:15-15:35** (commits a4d432c, 2f03083, b200c51): `lab/curve_v2/shorts/short11.py` (branch T draft, lint 0, ⏳ = launch lines), `lab/motion/src/curve_v2/CurveV2Short11.tsx` = composition CurveV2-Short11 on PLACEHOLDER captions (our MacBook drawing for frame 0, who-said-no timeline 2010-2026, gorilla-arm figure, capacitive grid, hinge torque 2x vs 1x, verdict + drawing; loop end = frame 0, PSNR inf; switches HAS_VO/HOOK_CLIP/LOOP_CLIP/FIX_CLIP), `prep/s11_clips.sh` (Apple film template), Jobs's 2010 words verified from two recordings (`lab/curve_v2/footage/apple_2026-10-28/JOBS_2010_QUOTE.md`). Stills: `node lab/motion/out/s11_stills.mjs <frames>` from lab/motion. Early Sonnet critic on the pre-build → `lab/curve_v2/shorts/out/critic_s11/scaffold_review.md`; its verdict: a sound base. B fixed MUSTs 1, 2, 3b, 3c, 4, 5, 6 at 15:55 (ledger `critic_s11/ledger.md`; Cook's 2012 line dropped from the timeline: it was about merging tablet and laptop); 3a (`PRODUCT_2026`) and the Apple-dependent parts are the 17:40 run's. **FRI 30 SCHEDULED TOO (15:40, he said "continue"):** Short 12 "Who Changes Your Phone's Clock?" (`PHONE_CLOCK_FACTS.md`, all pictures ours), task `b-fri-clock-short-2` Thu 18:30 → publish Fri 17:00, check `b-fri-clock-short-check-0730-2` Fri 07:30, both in Bypass mode (the first two copies were in the default mode and are deleted). **HE APPROVED DAILY UPLOADS (28 Oct ~15:55): "Yes: the daily scheduled runs can upload each Short (scheduled for 17:00) without asking me first."** Still: critic SHIP first, private + publishAt 17:00 UK, one Short a day. **SAT 31 SCHEDULED (he said yes ~16:00: "build Fri evening, publish Sat 17:00, topic picked from Friday's news, permission-free only"):** task `b-sat-short` Fri 18:30 → Short 13, check `b-sat-short-check-0730` Sat 07:30, both Bypass; skips itself at 93%+ weekly usage. Weekly usage 72% at 15:33 (resets Sat 21:00): keep each Short lean.

**ACCOUNT B, Wed 28 Oct ~02:50 UK: SHORT 10 UPLOADED, PUBLISHES 17:00 TODAY: https://youtu.be/hLhHU7O3x4M** ("How SpaceX Really Makes Money"; v5 after critic round 1 = ONE MORE PASS, fixes in, round 2 = SHIP; private with publishAt 2026-10-28T17:00:00Z, confirmed by the API; ledger `lab/curve_v2/shorts/out/critic_s10/ledger.md`). Short 8 dhcs3kk4itc public and processed. NEXT (1 video a day): Thu 29 = Apple touchscreen MacBook Short (event Wed 17:00 UK; facts `lab/research/APPLE_PRO_AND_TELL_FACTS.md`, C fills §5 after the event; A's lane, B if A is away: B has the voice and upload); Fri 30 = a Short unless he asks for the iPhone Duo film (film MRRLbIveEJc got 5 impressions; C's alignment says drop the Fri film); Sat 31 = phone clock or the motorbike if he gives a footage route. B weekly usage ~70%: one critic round per Short, Sonnet critics.

**ACCOUNT B, Wed 28 Oct ~01:05 UK (he: "check files i used other claude accounts to sub off tasks, bar that continue as usual, dont stop"). C's work read (Short 8 v3-v5, facts for Wed-Sat, money files, prospects, outreach rules); B does not redo any of it.**
- **SHORT 8 LIVE 00:35: https://youtu.be/dhcs3kk4itc** (C's v5 after round 2; B checked the five round-2 stills = pass; title shortened to "iPhone Duo Crack: The Fold Explained", old title in title_alts; recorded in uploads_curve.done.json).
- **PLAN DECK DONE: all 15 slides** https://claude.ai/artifact/TqozTPCqA4yMb89XsoLzLk (scoreboard, truth, map, ranked, lock-in = 3 lanes, youtube, service, products, fanvue, perks, physical, projection, asks, daily). Built from C's four money files + B's *_B_local versions. Deck source files: this session's scratchpad `deck_runitup/project/` (re-read from the artifact if lost).
- **TODAY'S VIDEO = SHORT 10 "How SpaceX Really Makes Money"** (C's permission-free script, rockets line reworded to "about twelve cents of every dollar"; lint 0; Chris take v2b word-perfect, 29.3 s; SpaceX's own Flight 5 4K footage `lab/curve_v2/footage/spacex_2026-10-28/`, clips via `lab/curve_v2/shorts/prep/s10_clips.sh`; comp `CurveV2-Short10`; manifest index 5). Rendering → `lab/curve_v2/shorts/out/SHORT10_v1.mp4`, measurements → `out/critic_s10/`. NEXT: fresh critic, fixes, upload Wed evening (Zapier, connection 02f9e902-69d2-8a12-af4b-b4f4cd146eeb; `~/youtube/.venv/bin/python lab/tools/youtube_upload.py zapier-init channel/uploads_curve.json 5`).
- Voice: B now has the ElevenLabs connector (creative_generate_speech, voice Chris iP95p4xoKVk53GoZ742B, eleven_v4; fetch the take via creative_get_generations full_res_url). B can voice for A, C and E.
- B's weekly usage: 60% at 00:36 Wed (resets Sat 21:00): lean builds, one critic pass per video.

**ACCOUNT C (cloud), Tue 27 Oct 17:45 UK: scheduled 17:00 radar ran** → `lab/research/RADAR_2026-10-27b.md`. Apple announced the M6 14-inch MacBook Pro (no touch) and M6 iMac today; touch OLED model still expected Wed 28 (`APPLE_PRO_AND_TELL_FACTS.md` rows 22, 110 filled). Top 3: Thu Apple touch Short · Sat SpaceX money (short10.py) · Sat/Sun phone clock (US change Sun 1 Nov). Short 8 v4 still needs critic round 2 + upload (Mac, A or B). The cloud's Wed 17:20 run is still scheduled: 🗓️🧹☁️🔕🧷 tell the cloud session to cancel it if the Mac's local run will do it.

**ACCOUNT C (Mac), USAGE LIMIT HIT ~13:45 UK. NEXT C, START HERE:**
1. **Short 8 v4 is RENDERED, NOT YET CRITIQUED:** `lab/curve_v2/shorts/out/SHORT8_v4.mp4` (33.6 s, -14.3 LUFS, -1.5 dBFS, frozen 14% / near-still 20%, no stretch ≥ 2 s). Measurements are already in `critic_s8/v4/` (motion, loudness, short/short_b sheets, strips at 2.9/11.13/18.87/20.6/22.13/23.7/27.57/32.5 s, frame0, phone). It has every fix from `critic_s8/v3/round1.md` (commit e1b66e4). **Do next:** a fresh critic round 2 (film-critic skill; send it round1.md, CRAFT.md, IPHONE_DUO_FACTS.md, manifest index 4; it marks each item FIXED/PARTLY/STILL PRESENT and writes `critic_s8/v4/round2.md`). On SHIP: ask him for the upload yes; **the upload needs A or B (Zapier)**; manifest index 4 already points at v4 and cites S1/S2. Not changed (critic flagged, his call): the title is 9 words.
2. Local clips not in git (`public/shorts/` is ignored): `s8_hook2.mp4` = frames 32-73 of `s8_hook.mp4` run through RIFE `-n 88` (rife-v4.6), x264 crf 15; `s8_loop2.mp4` = the first 30 frames of s8_hook2, reversed (last frame = frame 0, 48.4 dB).
3. **DONE 18:00:** `lab/research/PROSPECTS_SENDABLE_2026-10-27.md` (commit 4d9ed54): 24 firms on Companies House + own sites → 16 ready to email (Ltd, published address, opt-out), 5 web-form, 1 phone/letter, 2 dissolved (dropped). Strongest: Parker Software (£750), DPC Accountants (MTD £30k+ from 6 Apr 2027), Tinsley Garner. Independent QA of the 21 drafts running → `lab/research/PROSPECTS_DRAFTS_QA_2026-10-27.md`; nothing goes to him to send before it passes. **Evening radar DONE:** cloud `RADAR_2026-10-27b.md` (17:45) + Mac view counts `RADAR_2026-10-27b_mac.md` (JRE 12.7M and climbing; crosswind 105×, SpaceX money 18×, clocks 242×; moto weakest). The local 17:00 run failed on the usage limit (disabled now). The local Wed Apple task moved to **18:05** (after the cloud's 17:20 fill: it now checks §5 on Apple's pages). Short 8 round-2 critic running → `critic_s8/v4/round2.md`.
4. His open asks: the redirect question (alignment check below), cancel the cloud's 17:00 and Wed 17:20 runs, the Wed footage route, a voice for Wed-Sat, and permission modes on the 3 local `bernard-c-*` tasks.

**ACCOUNT C working on (since Tue 27 Oct 12:45 UK, Mac session, took over from the cloud C session): Short 8 critic → his upload yes; outreach routes for the 52 reels; Wed-Sat videos; Mac-only checks.** State at 13:00:
- **SHORT 8 v3 RENDERED** `lab/curve_v2/shorts/out/SHORT8_v3.mp4` (33.6 s, -14.3 LUFS, -1.5 dBFS, no frozen stretch ≥ 2 s). All claims-check fixes in (commit ab2c846): layers 7.9%/0.8% at the same ~1.9 mm fold, 10 strips under the "10 LAYERS" tag, Apple's whole sentence (checked on MacRumors' page) in 4 balanced lines, "JERRYRIGEVERYTHING · BEND TEST", softer description + iFixit line, manifest index 4 → v3. Stills checked (`critic_s8/r2_stills/`). Fresh critic running → `critic_s8/v3/round1.md`. **Upload needs his yes AND an account with Zapier (A or B): this account has no Zapier and no ElevenLabs.**
- MAC CHECKS DONE: SpaceX Q3 numbers all match the 10-Q/release/8-K (`SPACEX_MONEY_FACTS.md` §0; no customer named, one SI customer = 34.5% of revenue). Short 5's "+$523M" is right (Tesla Update slide 30, SBC net of tax 459 → 982; rows 14b-14c). ICO page confirms DMs = electronic mail and sole traders = individuals. iFixit's page: "several possible culprits", not two (IPHONE_DUO row 34h). Moto clip row 80 is CGTN Europe's (row 80b). CRAFT 24 Oct line back in order.
- RUNNING: Companies House check of the 52 shops → `lab/research/OUTREACH_ROUTES_52_2026-10-27.md`; alignment check (text only).
- SCHEDULED ON THIS MAC (local, one-off): radar Tue 17:00, Apple §5 fill Wed 17:20, Studio 48 h numbers Wed 18:45 (task ids `bernard-c-*`). The cloud session's 17:00 and Wed 17:20 runs must be cancelled by him so they don't double up (the local prompts write `_mac` files if they do).
- WED SHORT blockers: footage route (his), voice (no ElevenLabs here), upload (no Zapier here). Scripts drafted, lint 0, not voiced: `lab/curve_v2/shorts/short9.py` (Wed, motorcycle on water) and `short10.py` (Sat fallback, How SpaceX Really Makes Money, SEC numbers).
- **ALIGNMENT CHECK 13:04 (C's agent, text only): REDIRECT.** 1 Curve video a day ≈ £0-20 in 60 days (YPP needs 1,000 subs; we have 20). The only route that scales is the £400-750 business-video offer (300 emails by ~20 Nov ≈ £345-1,725, guess-heavy). D has no commits to `sales/`/`products/` since 12 Oct; `offers/` doesn't exist. Its advice: keep 1 video a day but only permission-free topics (SpaceX money, Apple, phone clock), A or B builds, C critiques; drop the moto Short and the Fri film; C makes the 24 prospects sendable (running now → `lab/research/PROSPECTS_SENDABLE_2026-10-27.md`), then a 45 s "MTD for Income Tax, April 2027" sample for accountants. Owner decides.
- The pull hit 3 untracked research files B's 02:50 agents wrote on this Mac; B's longer versions are kept untouched as `lab/research/{ASSET_AUDIT,MONEY_ROUTES_ONLINE,PHYSICAL_INVEST_UK}_2026-10-27_B_local.md` (not committed: B's call).

**ACCOUNT C, Tue 27 Oct 05:00 UK (cloud session: web research only; no renders, no Chrome, no Studio; the container blocks yt-dlp, RSS and most sites, so sources come through web search; SEC.gov needs a declared contact address, so filings are linked, not read).**
- ⚠️ **BEFORE THE 52 REELS GO OUT (B's ask to him):** cold Facebook/Instagram DMs to sole traders and ordinary partnerships need their consent under PECR (the ICO counts social-media DMs as electronic mail); only 1 of 52 names shows "Ltd". Ltd/LLP → DM with opt-out; the rest → walk in or post a QR card; phone after TPS/CTPS screening → `lab/research/OUTREACH_RULES_UK_2026-10-27.md`.
- **SHORT 8 (today's video): claims check = ONE MORE PASS, text only, no re-voice** → `lab/curve_v2/shorts/out/critic_s8/claims_check.md`. Must: the layers scene shows 1.1%/10.7% (1.4 mm maths) right after 0.8% for the same 30 µm layer: use 0.8%/7.9% (facts row 93b). Should: Apple's full sentence, "BEND TEST" in the JRE credit, soften the description's first line, manifest path says v1 but the commit says v2. The render critic (film-critic skill) still runs on the Mac.
- **1 VIDEO A DAY, facts status (C, 05:05):** Tue 27 Short 8 iPhone Duo (built; claims fixes, then render critic, then upload) · Wed 28 motorcycle on water (`MOTO_WATER_FACTS.md`; footage route = his call) · Thu 29 Apple touch MacBook (`APPLE_PRO_AND_TELL_FACTS.md`, C fills at 17:20 Wed) · Fri 30 iPhone Duo long film (`IPHONE_DUO_FACTS.md` §10) · Sat 31: crosswind 737 if Airport Action says yes (`CROSSWIND_737_FACTS.md`), else "SpaceX's Biggest Business Isn't Rockets" (`SPACEX_MONEY_FACTS.md`) or "Who Changes Your Phone's Clock?" (`PHONE_CLOCK_FACTS.md`, US change Sun 1 Nov) · Starship ship catch the day Flight 15 gets a date (`STARSHIP_FLIGHT15_FACTS.md`).
- FACTS READY (all `lab/research/`): `MOTO_WATER_FACTS.md` (Wed 28) · `APPLE_PRO_AND_TELL_FACTS.md` (Thu 29; Gurman: reveal Wed 28, ships Fri 6 Nov) · `IPHONE_DUO_FACTS.md` §10 (Fri 30 long film: iFixit's two possible hinge causes, HTX crease 48→167 µm, fold counts as months of use; row 34e corrected) · `CROSSWIND_737_FACTS.md` (Sat 31 candidate, needs Airport Action's yes) · `STARSHIP_FLIGHT15_FACTS.md` (pre-build, first ship catch, NET ~7-21 Nov) · `SPACEX_MONEY_FACTS.md` (Film 2: Q3 AI $7.56B > Starlink $5.25B > rockets $1.77B; Musk says the $40B GPU deal "closed", the 8-K says a commitment).
- RADAR `RADAR_2026-10-27.md` (04:50, delta): the week holds; next Shorts = crosswind 737, Starship ship catch, SEMA (3-6 Nov); EICMA 5-8 Nov; Zhuhai 10-15 Nov.
- MONEY: `ASSET_AUDIT`, `MONEY_ROUTES_ONLINE`, `PERKS_AND_POINTS`, `PHYSICAL_INVEST_UK` (all `_2026-10-27.md`) + `PROSPECTS_VIDEO_OFFER_2026-10-27.md` (24 sourced Staffordshire firms, hooks, PECR contact rules). Also `RETENTION_PLAYBOOK_2026-10-25.md`. CRAFT "Learned" +1 (27 Oct).
- QUEUED in TEAM §4 for A, B, D. SCHEDULED in this cloud session: radar 17:00 today (`RADAR_2026-10-27b.md`); Wed 28 17:20 fill Apple §5 + radar.
- HIS ASKS (ranked in `ASSET_AUDIT_2026-10-27.md` §5): 🏦🪙🔁🧾🌤️ switch his current account for a bonus (Barclays up to £300 first) · 🎥🏍️🌊📜🧭 footage route for Wed's Short (ZXMOTO ask text, CCTV+ licence, or ≤5 s credited news clips) · ✈️🌬️📹🙏🛬 send Airport Action the ask in `CROSSWIND_737_FACTS.md` §5 if he wants the Sat Short · 🧶🛒✂️🧮🍂 switch off Etsy Plus unless it sold something · 🌐🔓🛰️🧰📡 optional: widen this cloud environment's network access.

**ACCOUNT B, Tue 27 Oct ~03:00 UK: 5-HOUR LIMIT HIT (resets 03:00 UTC). NEW DIRECTION from him (02:40): "ur connected to my chrome, do what u need to do... 1 vid per day on current yt channels as i have habit of splitting focus and need to lock in" + a full brainstorm of every money route (KDP, Etsy, Fanvue AI creator, AI influencer, affiliates, video/3D tours for free stays, Amex points, storage units, Airbnb).**
- LIVE NUMBERS 27 Oct 02:50: The Curve 20 subs; Shorts 15,464 / 1,087 / 1,300 / 1,219 / 1,373 / 3,027 views; film MRRLbIveEJc = 5 impressions, 0 views in 31 h (long-form gets nothing at 20 subs: Shorts first, long-form only on strong search gaps). Etsy ArchivedPress: 45 listings, 9 visits in 30 days, Etsy Plus on. Gumroad thegoldenplate: 3 products, 0 sales, BOTH CHRISTMAS PRODUCTS UNPUBLISHED (planner £7.90, collection £24.90). KDP Dark Archive Press: ~12 live formats, 1 order today (£4.56). Fanvue: not logged in. ElevenLabs: signed out in Chrome.
- Chrome (claude-in-chrome) is connected, logged in to Etsy, Gumroad, KDP, Facebook, YouTube Studio. Only read so far. Publishing, sending, downloads = his yes per item.
- VOICE: the official ElevenLabs connector card was shown (claude.ai directory uuid 4a542638-16d2-4bd1-9937-efa473d3f2f0). After he connects: voice Short 8 per the finish steps in the 26 Oct 23:30 block below, render, critic, upload index 4.
- CASH NOW: 52 personalised sample reels for local food places (`sales/reels/send_sheet.html`: 34 Facebook, 14 phone, 4 Instagram; MSG template in the sheet) are UNSENT. Ask his yes to send them from his Facebook in Chrome (show him the message text first).
- RESEARCH (4 Sonnet agents launched 02:50, may have died on the limit): `lab/research/ASSET_AUDIT_2026-10-27.md`, `MONEY_ROUTES_ONLINE_2026-10-27.md`, `PERKS_AND_POINTS_2026-10-27.md`, `PHYSICAL_INVEST_UK_2026-10-27.md`. Any file missing = re-launch it (background, ranked table first, UK rules, evidence-graded, FCA rules on credit-card promotion for the perks one).
- DECK https://claude.ai/artifact/TqozTPCqA4yMb89XsoLzLk ("Run It Up: the plan to £2,000 a month"): deck.json (15 slides: cover, scoreboard, truth, map, ranked, lockin, youtube, service, products, fanvue, perks, physical, projection, asks, daily) + cover are published. Read deck.json from the artifact, then write the other 14 slides from the four research files.
- 1 VIDEO A DAY queue (The Curve): Tue 27 Short 8 (built, voice only) · Wed 28 motorcycle-on-water Short (radar 26 Oct #3, footage credit) · Thu 29 Apple "Pro and tell" Short (event Wed 17:00 UK) · Fri 30 iPhone Duo long-form "Why folding screens break" (reuses Short 8 diagrams). Keep each lean: kit + real clips + our diagrams, one critic pass.

**ACCOUNT B working on (since Sun 25 Oct 11:30 UK): the Roadster long-form film (critic round 1 fixes -> render v2 -> critic round 2) + research.** Files B touches: `lab/curve_v2/film_roadster/**`, `lab/motion/src/curve_v2/film/**`, `lab/motion/public/film/**`, `lab/research/**` (not the Shorts). Account A = Shorts.

**ACCOUNT B, Mon 26 Oct ~23:30 UK: SHORT 8 "iPhone Duo Crack: Why It Happens at the Fold" BUILT, WAITING ONLY FOR VOICE** (radar `lab/research/RADAR_2026-10-26.md`: JRE 11.77M, still +99k/h; ship by Tue 12:00). Done: facts updated (Apple's 26 Oct statement = row 34, source P9; never use owner crack photos), script `lab/curve_v2/shorts/short8.py` (lint 0), clips `lab/motion/public/shorts/s8_{hook,loop,layers,unfold}.mp4` (JRE + Apple, 1080x1920 30 fps; loop last frame = frame 0), comp `CurveV2-Short8` (`src/curve_v2/CurveV2Short8.tsx`, every scene cued by spoken words), manifest index 4. TO FINISH: (1) voice the 6 lines as ONE take (Chris iP95p4xoKVk53GoZ742B, eleven_v4, stab 0.5, sim 0.75, style 0.3, speed 1.08) -> `lab/curve_v2/shorts/vo/s8_chris_v1.mp3`; (2) `python3 lab/motion/scripts/tighten_vo.py` -> `_tight.mp3` -> copy to `lab/motion/public/shorts/s8_vo.mp3`; (3) 16 kHz wav -> `node scripts/transcribe.mjs` -> `python3 scripts/captions_ts.py <json> src/curve_v2/voS8Captions.ts VO_S8 --script ../curve_v2/shorts/short8.py` (replaces the PLACEHOLDER timings); (4) `HAS_VO = true` in CurveV2Short8.tsx; (5) render via `lab/tools/heavy.sh` -> `lab/curve_v2/shorts/out/SHORT8_v1_raw.mp4`, master (START file chain) -> `SHORT8_v1.mp4`; (6) fresh critic; (7) upload index 4.

**ACCOUNT B, Mon 26 Oct ~19:15 UK: VOICE BLOCKER.** B has no ElevenLabs (no claude.ai connector, no key on the Mac, vidIQ 0 credits to 5 Nov). ElevenLabs is now ENABLED in Zapier (App226160CLIAPI, actions text_to_speech + _zap_raw_request) but needs HIS login: https://mcp.zapier.com/api/v1/connect-auth/App226160CLIAPI?accountId=28606652 . After he connects: list_zapier_connections App226160CLIAPI, set it default, voice Chris iP95p4xoKVk53GoZ742B. Radar agent writing `lab/research/RADAR_2026-10-26.md` (trending + evergreen, next 3 Shorts + 2 films).

**ACCOUNT B, Mon 26 Oct ~19:00 UK: FOUR VIDEOS LIVE ON THE CURVE (all public, processed, ids in `channel/uploads_curve.done.json`):** Short 4 Unitree https://youtu.be/frW41Ezd1S8 · Short 5 Tesla Q3 https://youtu.be/ISxIuCMlGEc · **Short 7 Microduck https://youtu.be/BurRBxo3ny8** (v3 = A's v2 + critic round 2 label fixes) · **Roadster film https://youtu.be/MRRLbIveEJc, RETITLED 26 Oct ~19:10 to "How the Flying Tesla Roadster Really Works"** (he: "whatever best optimised for clicks"; search phrase first, thumbnail D carries the twist) (v3, 5:23, thumbnail D set; round 2 = ONE MORE PASS with one must-fix, fixed and checked in frames; the title was B's proposal: he may want "How the Flying Tesla Roadster Actually Works" back, a one-call change). NEXT for B: 48 h numbers Wed 28 Oct ~19:00 (stayed-to-watch, CTR, AVD) into CRAFT; Test & Compare (titles/thumbs A, C, D) is Studio-only = his hands. Still open for A: iPhone Duo Short (facts ready; B has no voice connector).

**ACCOUNT B, Mon 26 Oct 17:45 UK: RESUMED by him ("carry on... let's get these videos up and live").** No other account has committed since 25 Oct 17:50. DONE: **Short 4 LIVE https://youtu.be/frW41Ezd1S8, Short 5 LIVE https://youtu.be/ISxIuCMlGEc** (public, processed; ids in `channel/uploads_curve.done.json`). Zapier lesson: the resumable POST needs `uploadType`/`part` in the **querystring field** (in the URL they are dropped, 400 "media type"), and YouTube rejects `<` `>` anywhere in a description (400 invalidDescription). IN PROGRESS (B): critic round 2 on film v2 AND on **Short 7 v2** (`lab/curve_v2/shorts/out/SHORT7_v2.mp4`: A rendered it Sun 09:38, mastered -14.2 LUFS, never critiqued or committed; B took it over so it ships today; tracks already match the v2 Blender json). Both upload on SHIP. **Account A: don't redo Short 7.**

**25 Oct 17:50: FIVE ACCOUNTS from now (he is adding C, D, E). Read `TEAM.md`: lanes A Shorts / B long-form + strategy / C trend desk, facts, QA critic / D money now / E channels 2-3, file ownership, the queue (B's paused items are queued there for C, D, E), heavy-job lock `lab/tools/heavy.sh`.**

**ACCOUNT B PAUSED by him, Sun 25 Oct 17:38 UK ("pause all work for time being"). Nothing is running. Resume ONLY when he says so, in this order:**
1. **Critic round 2** on `lab/curve_v2/film_roadster/out/FILM_ROADSTER_v2.mp4` (fresh agent, film-critic skill; measurements already in `out/critic_v2/`: motion 3% frozen / 5% near-still, no stretch >= 2 s; -14.1 LUFS, -1.2 dBTP). The round-2 agent was stopped before writing anything: start a new one with the round-1 report `out/critic/round1.md`. Then fixes, then ask him for the upload yes (manifest index 3; title + thumbnail D are proposals).
2. **Research for his pitch** (both agents stopped before writing): `lab/research/RETENTION_PLAYBOOK_2026-10-25.md` (retention rules + 3 style recipes for test shots) and `lab/research/MONEY_MAP_2026-10-25.md` (niches for 2 more channels, affiliate/credit programmes, other platforms' payouts, 12-month projections). Re-launch both.
3. **Style test snippets** (3 x ~10 s, for his approval before any new-style production), then the **pitch deck**: an empty Slides artifact already exists at https://claude.ai/artifact/TqozTPCqA4yMb89XsoLzLk ("Run It Up: The Studio Plan"; fill `project/deck.json` + `project/slides/*.html` per its type instructions).
He was sent: `FILM_ROADSTER_v2_preview.mp4` (720p) + `thumb_D.jpg`. His open asks: connect The Curve's TikTok/IG/FB/X in Metricool (or say no accounts exist); the 38 shop messages.

**ACCOUNT B STATE, Sun 25 Oct 17:30 UK (resume from here):**
- **For Account A: `lab/research/IPHONE_DUO_FACTS.md` IS READY** (primary sources; frame 0 = JRE ~12:05-12:15 green line, credit him; 3 hooks §8; do-not-claim §9; row 57 = A must watch JRE 11:45-12:30 to see which way he bends it). Radar refresh `lab/research/RADAR_2026-10-25b.md` (Apple "Pro and tell" Wed 28 Oct 17:00 UK pre-build brief; Starship Flight 15 still no page; F1 title race tonight = footage claim risk). Note for A: Short 4's description in `channel/uploads_curve.json` says "in its launch video (21 Oct 2026)" twice.
- **Film v2 DONE in code, rendering:** all critic round 1 fixes in (commit 863df58): verbatim Musk quotes, "<1.6 s" = press reports (not Tesla), Top Gear's "road legal" outside Tesla's page, refund clause stamp, S9 cut, `EvidenceStamp` (fx.tsx: SHOWN LIVE / TESLA SAYS / OUR MATHS / UNPROVEN / CHECKED, 54 px, title-safe), promise beat at 0:04-0:09, frame 0 pushed 1.6x, no loop-back, b1 = backlit 1978 fan car, b2 = head-on lift "AIRCRAFT? / OR CAR?", Blender tank refill shot (B_blender `--shot refill`, `--shot gauge`; fixed the dead `drain` property), fresh 4K clips (`prep_v2_clips.sh`), S8 opens on the unused climb clip, -5 dB on all effects, 8 s end card with spoken pointer. Narration = v1 takes + 6 pickups spliced (`vo_v2.py`, `words_v2.py`; all re-transcribed word for word). Half-res preview checked. Full render -> `lab/curve_v2/film_roadster/out/FILM_ROADSTER_v2.mp4` (5:22.6; mastered -14 LUFS). NEXT: measure, critic round 2 (fresh agent, film-critic skill), fix, ask him for the upload yes. Manifest index 3 updated (v2 file, chapters, proposed title "Tesla Won't Promise the Flying Roadster Arrives", alts in `title_alts`).
- **NEW DIRECTION from him (25 Oct ~17:00):** long-form first (Shorts continue), maximum retention/virality, creative freedom on style, **snippet test shots for his approval first**, then a 2-3 video backlog only (room for trends), trend-led topics on all platforms, crazy scroll-stop hooks for Shorts, 2 more channels + niche advice + projections pitched to him, affiliate/discount/access angles, connect all socials. B is building: `lab/research/RETENTION_PLAYBOOK_2026-10-25.md` + `MONEY_MAP_2026-10-25.md` (agents running), then 3 style test snippets, then a pitch page. Alignment today: `lab/research/ALIGNMENT_2026-10-25.md` (film = ship but cap effort; YouTube pays £0 before 2027; 30 min of his on the 38 shop messages = £60-180/h).
- Metricool (read 25 Oct): one brand, ONE YouTube channel connected (UC2-TlkkkMcRn0tOLug_wE1Q, not The Curve), no TikTok/IG/FB/X: nothing can be cross-posted until he connects them.

# START HERE: state at Sun 18 Oct 2026, evening (written for a Claude with zero history)

This block is the truth. Everything below it in this file is older history, kept for detail only.
Repo: `~/Bernard`, branch `claude/funny-newton-gd9w8v` ONLY (push with: `git push -q origin claude/funny-newton-gd9w8v 2>/dev/null || git -c http.curloptResolve=github.com:443:140.82.121.4 push -q origin claude/funny-newton-gd9w8v`). Python: `~/youtube/.venv/bin/python`. Videos, voice takes and pictures are on THIS Mac only (not in git): a cloud session cannot render or upload them.

**FRI 23 OCT, NEW DIRECTION (his words): "usage credits on, use the new video style with real clips, blender, highest production quality etc for long and short form... stay up to date with trending news/events... adjust the curve as it is displayed as ai focused but we want to do all (mostly high rpm and viral topics)".**
Stats 23 Oct: Short 1 15,413 views · Short 2 1,087 · Short 3 1,275 · channel 10 subs, 20,203 views. Lesson: the visual-mystery hook on the most jaw-dropping clip, 3 days after the event, wins; same-event follow-ups decay to ~1k. So: chase NEW viral moments, not more Roadster follow-ups.
Plan in motion: (1) rebrand The Curve to "the story behind the clip everyone's sharing" (tech, cars, space, robots, money); (2) trend radar lab/research/RADAR_2026-10-23.md; (3) facts files: Unitree H2-X (robot, 21 Oct), Meta Class C stock (21 Oct), Tesla Q3 2026 (21 Oct); (4) reusable kit lab/motion/src/curve_v2/kit/; (5) Shorts: Unitree, Meta, Tesla Q3, clocks-go-back (UK Sun 25 Oct); (6) long-form: Tesla Roadster film (gate passed: Shorts average 5.9k). vidIQ: 0 credits until 5 Nov and The Curve not connected to it. Uploads still need his yes.

Done 23 Oct (evening): channel description + keywords rewritten (no longer AI-only) and a NEW BANNER uploaded via API (lab/motion/src/curve_v2/Brand.tsx, files in channel/the-curve/brand/v2/). New avatar rendered (channel/the-curve/brand/v2/avatar.png) but the API can't set avatars: HE uploads it in YouTube Studio > Customization > Branding. Kit for new Shorts: lab/motion/src/curve_v2/kit/index.tsx. The 4 research agents (radar, Unitree, Meta, Tesla Q3) died on the weekly limit at ~17:40 (resets 7am Sat); resume them with SendMessage or redo inline. Zapier GET tip: put query params in the "querystring" dict, not the URL (URL query strings get dropped).

**23 Oct, 18:40: Short 4 (Unitree H2-X, "How Unitree's Kung Fu Robot Learned to Fight") rendered + measured: lab/curve_v2/shorts/out/SHORT4_v1.mp4 (-14.3 LUFS, 1% frozen, loop 39.9 dB). Short 5 (Tesla Q3, "Tesla Showed a Flying Car. Then Its Profit Fell 43%") rendered + measured: SHORT5_v1.mp4. Critic round 1 running on both (reports to out/critic_s4/round1.md and out/critic_s5/round1.md). Manifest for both: channel/uploads_curve.json ("public": true = goes live on upload). Uploads still need HIS yes. Next: apply critic fixes, then a UK clocks-go-back Short (Sun 25 Oct) or Meta Class C; then the Roadster long-form.**

**23 Oct ~19:10 — USAGE LIMIT HIT. EXACT STATE (resume from here):**
- DONE + LIVE: channel rebrand (description, keywords, NEW BANNER via API). Avatar ready at channel/the-curve/brand/v2/avatar.png: HE must upload it in YouTube Studio (API can't).
- SHORT 4 (Unitree H2-X): v1 rendered (lab/curve_v2/shorts/out/SHORT4_v1.mp4), critic round 1 = ONE MORE PASS (out/critic_s4/round1.md). v2 IN PROGRESS: new script lab/curve_v2/shorts/short4.py (line 1 = Unitree says it's real + small-print tease; u5 = "in that code, the controller..."; verdict "The kicks are real; the bodyguard is still a demo"), new VO public/shorts/s4_vo.mp3 (34.2 s, from vo/s4_chris_v5_tight.mp3), captions regenerated FROM THE SCRIPT (scripts/captions_ts.py --script). Blender (lab/curve_v2/shorts/blender/s4_sim.py) renders started: --shot hero -> blender/out_s4_hero (+ track.json = per-frame screen coords of CoM and stance foot for the balance overlay) and walking reveal -> blender/out_s4_walk (frames 301-436). TODO: encode them (hero -> public/shorts/s4_sim_hero.mp4, walk -> s4_sim_f.mp4), re-time CurveV2Short4.tsx to the new VO (planned cuts: real-speed flip 0-18 then 7x replay to 102; knife tease as a full 16:9 inset 102-218; mocap 218-348; practise 348-508; 4,096 walking reveal 508-639; Blender hero balance + CoM dot/plumb line from track.json 639-769; music dip + hit at 769; small print push 769-857; knife label + stamp 857-929; verdict over Blender hero kick match-cut into real kick 929-1022; rewind + frame 0 to 1044), credits 44 px, labels >= 46 px, nothing in x>950 between y 864-1728, 4,096 margin, balance clip crop x0 <= 600. Then critic round 2.
- SHORT 5 (Tesla Q3): v1 rendered (out/SHORT5_v1.mp4), critic round 1 = ONE MORE PASS (out/critic_s5/round1.md). MUST FIX before upload: remove the inserted "an" from Tesla's quote (exact: "increase in operating expenses driven by SI and other R&D projects, SBC (including 2025 CEO Performance Award) and SG&A"); SI = "Super Intelligence" per Tesla's own highlights page (fix TESLA_Q3_2026_FACTS.md + narration: "its Super Intelligence and other research projects"); label -43% as GAAP (non-GAAP net income fell only ~4%: 1,770 -> 1,697); "said" -> "reported"; new line 1 "Tesla's net profit just fell 43%, six days after this flying Roadster"; frame 0 = airborne-with-jets frame, not Short 1's; captions via captions_ts.py --script; hold -73% >= 1.5 s.
- FILM (Roadster long-form, 16:9): script v2 lab/curve_v2/film_roadster/script.py (60 lines, 1,030 words, lint clean, adds S9 "the bill"). All 11 narration parts voiced: film_roadster/vo/<seg>_t.mp3 (5.4 min), copied to lab/motion/public/film/vo_<seg>.mp3. Scaffolding: src/curve_v2/film/{FilmRoadster.tsx, util.ts (cue(seg, word)), words.ts, EndCard.tsx}, compositions Film-Roadster + Film-<seg> registered. 16:9 Tesla clips (RIFE 30 fps): public/film/*.mp4 (prep_film_clips.sh). Blender 16:9 car shots (hang/xray/drop) rendering to lab/curve_v2/trials/B_blender/v2/frames/{hang_h,xray_h,drop_h}. Two builder agents were writing S5FanCar/S6Legal/S7Deposit and S9Bill/S8Verdict when the limit hit: CHECK those files (may be partial or placeholders). S1-S4, B1, B2 are still placeholders: build them (S1 hang_slow8 + Blender hang_h + wing-vs-fans bars + drop; S2 kick_side + Blender xray_h + 80 kN; S3 zero60 + lanes race; S4 tanks drain + 2-6 h clock + Musk vs engineer).
- Uploads need HIS yes (manifest channel/uploads_curve.json holds Shorts 4-5). Subagents die on the weekly limit; extra usage didn't cover them.

**24 Oct ~01:30 STATE:** Shorts 4 and 5 v2 rendered + measured (lab/curve_v2/shorts/out/SHORT4_v2.mp4, SHORT5_v2.mp4); round-2 critics running (reports to out/critic_s4v2/round2.md, out/critic_s5v2/round2.md). Film: S1, S2, S3, S4, B1, B2 BUILT (src/curve_v2/film/*.tsx, compositions Film-S1..); builder agents writing S5FanCar/S6Legal/S7Deposit and S9Bill/S8Verdict (check files); then render Film-Roadster -> lab/curve_v2/film_roadster/out/FILM_ROADSTER_v1.mp4, loudness chain, film-critic, thumbnail. Long-form upload entry with chapters drafted in channel/uploads_curve.json (kind "long"). Uploads need HIS yes.

**24 Oct ~09:40 STATE:** SHORT 4 v3 (lab/curve_v2/shorts/out/SHORT4_v3.mp4) and SHORT 5 v3 (SHORT5_v3.mp4) are FINAL after two critic rounds each (round-2 fixes applied; measured -14.1/-14.2 LUFS, 0% frozen, loop PSNR ~43 dB). Manifest channel/uploads_curve.json points at both v3 files ("public": true). WAITING FOR HIS YES TO UPLOAD (Unitree story is 3 days old: ship asap). Upload route = HANDOFF Zapier route: put query params in the URL for the resumable POST (uploadType=resumable&part=snippet,status), then youtube_upload.py put. Film: S1-S4, B1, B2 (me) and S9, S8 (agent) built; S5-S7 agent still running; then render Film-Roadster + loudness + film-critic. Radar 24 Oct: lab/research/RADAR_2026-10-23.md, top pick Microduck ($399 Nvidia/Pollen robot duck, sim-to-real clip youtu.be/szW7N_7B3tU 9-13 s) publish Sun 25-Mon 26; Starship Flight 15 catch (pre-build, publish within 6-12 h of launch); Short 6 (Roadster kickflip) scripted + voiced: lab/curve_v2/shorts/short6.py, public/shorts/s6_vo.mp3, s6_kick_6x.mp4 — comp not built yet. Note: the Short 5 round-2 critic agent put his email in an SEC User-Agent header (told him).

**25 Oct 05:10 STATE:** A second Claude account is joining: it reads START_NEW_ACCOUNT.md first (shared memory = these files). Split: account A = Shorts, account B = film + research. Short 7 v2: script, voice, real clips and composition done; Blender v2 frames done in lab/curve_v2/shorts/blender/out_s7v2_{wrong,tripod,crowd}; next = encode them, regenerate s7Tracks.ts from their json, render, critic round 2. Film builder agent died mid-fix (script.py edited, not voiced). The iPhone Duo facts agent died (IPHONE_DUO_FACTS.md may be partial). Shorts 4/5 still wait for his go.

**25 Oct ~00:15 STATE (limit hit ~21:30 Sat, reset 00:10 Sun; resume from here):**
- SHORTS 4 + 5 v3 FINAL, still WAITING FOR HIS YES (manifest channel/uploads_curve.json). Avatar upload still his.
- SHORT 7 MICRODUCK v1 rendered: lab/curve_v2/shorts/out/SHORT7_v1.mp4 (34.4 s, -14.1 LUFS, 0% frozen, loop 41.5 dB); preview sent to him (SHORT7_v1_preview.mp4). Comp lab/motion/src/curve_v2/CurveV2Short7.tsx (+ s7Tracks.ts, voS7Captions.ts); clips public/shorts/s7_*.mp4; Blender frames lab/curve_v2/shorts/blender/out_s7_{grid,tripod,variants}. Manifest entry added (index 2, "public": true, needs his yes).
  - CRITIC ROUND 1 = ONE MORE PASS (lab/curve_v2/shorts/out/critic_s7/round1.md). Fixes to make: (1) frame 0 = the duck at its lowest point with hand in shot + <=6-word question ("WHO TAUGHT IT THIS?"), re-time the rewind to land on it; (2) 23.2-28.5 s = ONE continuous Blender shot of one duck, spec lines accumulate per spoken word (MASS ±5% scale squash; BALANCE POINT UP TO ±8 mm marker INSIDE torso tagged "exaggerated"; FOOT GRIP 0.7-1.3x ice slip; BATTERY SAG bar drains; SHOVE EVERY 3-6 s arrow + stagger), chips >= 48 px, no whips; (3) replace the 10.6-15.5 s grid (too like Short 4): ~50 visibly different ducks tumbling/resetting + static "4,096 AT ONCE", push into one duck; (4) end on the real duck: verdict "...and it has already practised on thousands of them", hold Pollen's shove clip under ONE MORE WRONG BODY; (5) re-voice m2 from fact 14 ("its only points came from ending up standing; it found the moves itself", on screen POINTS FOR: ENDING UP STANDING), drop "The real trick:" colon, phrase-end caption breaks, tripod head x <= 850, whoosh peaks on cuts, mask Pollen's "Straig..." caption at 10.3-10.6 s.
- FILM: FILM_ROADSTER_v1.mp4 rendered + mastered (lab/curve_v2/film_roadster/out/, 5:49, -14.2 LUFS, peak -1.2). Critic measurements in film_roadster/out/critic/. Film critic agent died on the limit: resume it (or start a fresh one) and wait for its round1.md before any upload request.
- RADAR refresh agent died on the limit mid-run (it had found Defender OCTA + JCB land speed record clip, 90k views): resume it; output -> lab/research/RADAR_2026-10-25.md.

**24 Oct ~19:15 STATE (usage limit hit ~14:45, reset 19:10; resume from here):**
- SHORTS 4 + 5 v3 FINAL (lab/curve_v2/shorts/out/SHORT4_v3.mp4, SHORT5_v3.mp4), manifest channel/uploads_curve.json ("public": true). STILL WAITING FOR HIS YES. His hands too: avatar upload (channel/the-curve/brand/v2/avatar.png, YouTube Studio > Customization > Branding).
- SHORT 7 MICRODUCK (radar top pick, publish Sun 25 - Mon 26 Oct) IN PROGRESS:
  - Facts: lab/research/MICRODUCK_FACTS.md (primary sources: Pollen's own training repo github.com/pollen-robotics/microduck_rl README/AGENTS.md/velocity env cfg; Pollen videos RAtzEyGBGFU + szW7N_7B3tU; Nvidia blog 23 Oct). Key facts: rewards = upright / follow joystick / lift feet; no reference animation; "head-tripod instead of standing" loophole; domain randomisation per copy: mass ±5%, balance point ±3->8 mm, foot grip 0.7-1.3x, battery voltage + sag + delay, pushes every 3-6 s.
  - Script: lab/curve_v2/shorts/short7.py (6 lines m1-m6, cap fields). Line 1: "The Microduck you're watching was never shown how to get back up; it learned that in a simulator." Verdict: "So the real duck is just one more wrong body, and it has already beaten thousands."
  - Voice: lab/curve_v2/shorts/vo/s7_chris_v1.mp3 -> s7_chris_v1_tight.mp3 (33.45 s; whisper json s7_v1_tight.json matches the script word for word).
  - Footage (4K AV1): lab/curve_v2/footage/microduck_2026/newrobot.mp4 (shove/balance recovery 16-32 s, slow-mo x0.25 get-up 34-40 s, floor picking 42-54, roller skating 56-64, chorus of ducks 66-84) and sim2real.mp4 (left half = sim, right half = real; title overlay 0-2 s, caption 5-8 s, falls 9-11 s).
  - Blender: lab/curve_v2/shorts/blender/s7_duck.py = OUR OWN duck (Pollen's meshes are CC BY-NC-SA: never show them), sized from their Apache MJCF. Shots: grid (64x64, 130 f), tripod (head-tripod hero + tripod.json contact-point track, 150 f), variants (5 wrong bodies + wide, 360 f, variants.json label track). grid + tripod test frames LOOK GOOD. variants layout BROKEN (each camera blocked by the duck in front): change the row direction to (3.4, 1.4) per duck, heavy duck to 3/4 profile so the lead weight shows, battery lower (z ~2.95), hide the pusher outside V5/W. Then full renders (~13 s/frame at full res), encode to lab/motion/public/shorts/s7_*.mp4, captions (scripts/captions_ts.py --script short7.py), CurveV2Short7.tsx, render, measure, critic, ask for upload yes.
- FILM (Roadster long-form): S5-S7 builder agent ab282aa11bb60fbc8 died on the limit while applying the stills critic's MUST-FIX list (critic agent a1f56d7bef95cdf04, findings in its output). Resume it with SendMessage. Then render Film-Roadster, loudness chain, film-critic, ask for upload yes (never two copies of a long film on the channel).
- SHORT 6 (Roadster kickflip): scripted + voiced (short6.py, public/shorts/s6_vo.mp3, s6_kick_6x.mp4), composition not built (lower priority than Microduck: Roadster follow-ups decay to ~1k).
- Mistakes not to repeat: Blender 5.2 BMesh moves elements when you add geometry: keep index ranges, never BMVert refs. Geometry Nodes Random Value outputs by name ("Value"), not index. Homebrew python3.15 has a broken expat: use `uv run --python 3.12 --with mujoco ...` for MJCF work. zsh: never start an echo argument with "=".

## 0. NOW (Sun 18 Oct, 04:30 UK): read this first, then section 1f

**FORMAT LOCKED 19 Oct: ASCII style retired; "clip, explained" (real clip + Blender/Remotion diagram) is The Curve standard. Slate + recipe: lab/curve_v2/SLATE_2026-10-19.md. Next session: build the reusable template, then Short 4 (the contract).**

**Mon 19 Oct update:** Short 1 (kRsPY8Ptei8) at 9,276 views. Short 2 LIVE as 3v6KK8LmdXA (public 06:21 UTC). Short 3 uploaded, scheduled public Tue 20 Oct 11:00 UTC (see uploads_roadster.done.json). Zapier tip: put the query string IN the url; the separate querystring field is ignored. Python is ~/youtube/.venv/bin/python. Next: track numbers; a Q3-call Short only if there is Roadster news.
**Alignment verdict (lab/research/ALIGNMENT_2026-10-17.md, agent, 17 Oct 23:30):** the Roadster film and Musk series
pay £0 before 2027 (The Curve median 7.5 views, 0 subs, YPP by 1 Feb under 5%). Run the Curve on machine time only,
**Shorts first**; cut the standalone 8-min film (stitch Shorts into a film only if they average 1,000+ views); the
quality budget goes to the dated Voyager 1 film (18 Nov). Roadster news decays 40-55% a day: Short 1 must go out
**Sun 18 Oct 18:00 UK**, then one a day (Mon: 0.81 s self-timed; Tue: 2-6 h refill; Thu: Q3 call only if Roadster news).
**His hands today (the gate set on 8 Oct, ALIGNMENT_8OCT.md):** (1) send the 38 ready shop messages,
`sales/reels/send_sheet.html` (30 min; no messages + no doors = "December about £30"); (2) list the low-stim kit
(`products/lowstim_kit/`, LISTING.md, ~45 min); (3) say yes to the Short 1 upload; (4) narrator pick (default Chris).

| Item | Path | State |
|---|---|---|
| Short 1 "How the Tesla Roadster Hangs Upside Down" | **LIVE since 10:25 UK: https://youtu.be/kRsPY8Ptei8. 14:32: 1,312 views; 19:33: 3,175 views, 53 likes, 2 comments** (Curve median 7.5; previous best the Steve Short, 280 in 2 days) | File `lab/curve_v2/shorts/out/SHORT1_v2.mp4`. Critic round 2 DONE: 8/10, SHIP, no must-fix (`shorts/out/critic_v2/round2.md`); lessons in CRAFT Learned 18 Oct. Read its 48 h numbers in Studio (stayed-to-watch %) |
| Film script v1 (8 segments = 7 Shorts) | `lab/curve_v2/film_roadster/script.py` | Lint clean; S1 synced with Short 1; S5 (fan car: Brabham BT46B won its only race, Swedish GP 17 Jun 1978; Chaparral 2J 1970, 0 wins, banned) and S7 (US contract clause 4 "cannot guarantee... if it will be delivered") now verified from facts §13 |
| Short 2 "The Tesla Roadster's 0.81 Second Launch" | **READY: `lab/curve_v2/shorts/out/SHORT2_v2.mp4`** (critic round 2 = 7.6/10, SHIP; plus the 'only the off-road Rocket beats 0.81 s' tag) | Manifest index 1 points at it. Upload ONLY after his yes (asked: tonight 19:00 or Mon 12:00) |
| Short 3 "How Long Can the Tesla Roadster Fly?" (Tue) | **READY: `lab/curve_v2/shorts/out/SHORT3_v3.mp4`** (32 s, -14.3 LUFS, 0 duplicate frames in the opening, loop 41 dB) | Critic round 2 = 7.7/10 with 3 code-only must-fixes, all done and measured (true 10x RIFE hover `public/shorts/s3_hover_10x.mp4`, drain from 13.07 s so EMPTY shows, IN ABOUT / TWO SECONDS. pages, claim card fills 25.2-26.4 s). Manifest index 2 -> v3. Upload ONLY after his yes |
| Blender v2 | `lab/curve_v2/trials/B_blender/v2/` | shot2_xray_9x16.mp4 DONE (used in Short 3); shot3_hang (red car, off-look) needs a redo. Agent stopped by the 10:10 limit and deliberately NOT resumed: the Shorts plan uses real footage for the drop/landing, so shots (iii) and (iv) only matter if the long film is greenlit (alignment: stitch only at 1,000+ views per Short) |
| Tools | `~/tools/rife-ncnn-vulkan-20221029-macos/` | RIFE (official nihui release, universal binary): `./rife-ncnn-vulkan -i in/ -o out/ -m rife-v4.6 -n <frames> -f %04d.png` (outputs are 1-based; last few frames repeat). `script_lint.py` now flags "isn't X, it's Y" |
| Film clips (Tesla, 4K, 3-7 s each) | `lab/curve_v2/footage/tesla_2026-10-15/film/` | 9 clips + clip log in SOURCES.txt. The livestream (qt5p-_tE8d0) and product film sections fail (ffmpeg code 8) |
| Agents killed by the session limit at ~23:40 | | Resume with SendMessage (work is saved): critic of C v2 (-> `trials/C_hybrid/CRITIC_C_v2.md`), Blender v2 (-> `trials/B_blender/v2/`, empty so far), facts update (-> `TESLA_ROADSTER_FACTS.md` §13; had found Alef Aeronautics = the "11-year-old flying car company") |
| New 17 Oct news worth a Short | Google News RSS | The Drive: Tesla "cannot guarantee" reservation holders get a car; Engadget: fan cars since 1970 (Chaparral 2J, Brabham BT46B); FAA "not an aircraft"; Altman praise after refund row |

Mistakes not to repeat: news Shorts need the answer in line 1 and must ship within ~48 h; one critic pass, not
trial loops; never imply the TSLA drop was a verdict on the Roadster (the Nasdaq fell the same 2%); don't claim the car
was at 0 mph at the top (it hangs ~1 s in real time); 0.81 s is Tesla's own timing; "about two seconds of gas" is OUR
estimate (label it).

## 1. Done this session (9 Oct afternoon) and what is still running
| Item | File | State |
|---|---|---|
| Weekly growth review + radar (14 Oct, scheduled run) | `lab/research/REVIEW_2026-10-14.md` · `lab/research/RADAR_2026-10-14.md` | DONE. **OWNER ACTION:** 4 Curve uploads stuck "processing" since 8 Oct (yTt9_y5DTZ0, 38tmCX4gq34, BrNE7GCltBo, x4cBx9G5luU): delete and re-upload in Studio. Escape Short is on the channel twice (kQK54NgtQxc + S5nN7Yxk6_A). Best so far: Steve Short (280 views, answer in line 1) and Money Crimes Shorts (50-63% viewed). Make next: LF04 rogue agents, power-grid Short, OpenAI maths Short, HTP gas stations, MC object-first Shorts. 4 lessons added to CRAFT "Learned" |
| Spanish film 2 | `lab/curvelf/lf02_price_es/LF02_ES_v2.mp4` | DONE. 8 lines re-voiced; critic `CRITIC_ES_v2.md` = UPLOAD; chapters in POST.md. UPLOADED 9 Oct to Curva Explica (@curvaexplica, Zapier connection `020e1621-8ed2-8623-aa3a-11cd759b5c3e`): id D_kET09mB6U, private, public 10 Oct 22:00Z. Phone-verified (user, 9 Oct): The Curve, Curva Explica, How They Profit; Money Crimes tomorrow. Thumbnails SET 9 Oct on 982Z-6peFbM (LF02) and yTt9_y5DTZ0 (LF01). UPLOADED 9 Oct 19:35: short_escape S5nN7Yxk6_A (13 Oct 12:00Z), LF03 v5 j17HdEgAQ04 (16 Oct 16:00Z). LF03 thumbnail SET 9 Oct 20:40. STILL TO DO: Ponzi thumbnail (MYerI1teKMg, mc02_ponzi/out/thumbflow_a.jpg, Money Crimes connection 02ce9a67-...) was REFUSED 9 Oct 20:40 and again 11 Oct: channel not phone-verified yet; retry after the user verifies, and his ear check of `ear_check_v2.mp3` (xAI said "equis A I"). Old takes in `flow/takes_old_v1/` |
| LF03 music drops | `lab/curvelf/lf03_held/LF03_FLOW_v5.mp4` | DONE. `mix_flow.py` gained `fill()` (lifts short holes in a score bed); sound-only re-mix; dips now about 5 dB. Manifest index 8 points at v5. Upload after 19:30 9 Oct |
| `short_escape` | index 5 of `channel/uploads_newlook.json` | Upload after 19:30 UK 9 Oct (daily cap hit 8 Oct) |
| Tunnel pilot ("Megaprojects"/"Datum Line") | `lab/curvelf/pilot_tunnel/TUNNEL_PILOT_v2.mp4` (= `lab/pilots/megaprojects/`) | DONE. Critic v1 (`CRITIC_v1.md`, FIX THEN UPLOAD) fixes applied in v2: honest diagram label, frame 0 shows the photo, hook at 5.4 s, ≈15 MILLION, POST.md with photo links + chapters. NOT done: name pronunciations by ear (Fehmarn, Rødbyhavn, Øresund, Lolland, Scandlines); channel name; channel does not exist |
| Economy pilot ("The Household Ledger") | `lab/curvelf/pilot_ledger/LEDGER_PILOT_v3.mp4` (= `lab/pilots/economy/`) | DONE. 33 pictures drawn in code, 116 lines voiced. Critic `CRITIC_v2.md` (FIX THEN UPLOAD): H1-H3, M1, M2 fixed in v3 and checked on the file (ranked list visible, frame 0 bright, hook in line 1, October sentiment 46.3 verified at the source, POST.md honest + chapters). M3 (a look of its own) waits on the user. Stale after 13 Oct (CPI 14 Oct) |
| Engine (`lab/curvelf/flow.py`) | | New script options: `ILLUS = "..."` (picture label), `LEAD` (seconds before the first word), `OPEN_RESOLVED = True` (frame 0 shows the first picture). Long channel names push the chapter rail right. Photo credit no longer doubles "PHOTO" |
| Trend desk report (another session) | https://claude.ai/artifact/FXjyxJ6wRAA1sXaUzdp3Qp | Read only; nothing in the repo |

ElevenLabs: about 89,000 characters left until about 16 Oct. Strategic warning from a critic (CRAFT "Learned", 9 Oct): every channel shares one engine look; a new channel needs its own look before launch.

## 1b. NEW DIRECTION from the user (9 Oct, evening): a maps channel in the Visa typography look
- He loves the How They Profit Visa film's opening: the world map set in type (# + % * coastlines, dots for land, one
  glowing route line, nested zooms). Engine: `lab/ch2/ep06/flow.py` (`ocean()` etc.), look study `rend_test.py` B.
- His idea: geography / maps & power as its own channel, starting with the Strait of Hormuz (trend desk pick #1,
  23/25: https://claude.ai/artifact/FXjyxJ6wRAA1sXaUzdp3Qp). This also answers the critic's warning that every channel
  shares one look: the typographic map becomes this channel's signature, distinct from The Curve.
- HORMUZ v2 RENDERED 9 Oct 21:50: `lab/maps/hormuz/HORMUZ_v2.mp4` (render with FLOW_BED=drone; CHROME="chart" in script; names respelled). Verify critic running -> CRITIC_v2.md. User to choose channel: How They Profit (recommended) or The Curve; then set TAG to that channel name and re-render. v1 history: HORMUZ v1 RENDERED 9 Oct 21:25: `lab/maps/hormuz/HORMUZ_v1.mp4` (9:33, -14.1 LUFS; engine link `lab/curvelf/maps_hormuz`), all 77 lines voiced, FACTCHECK.md applied. Critic running -> `lab/maps/hormuz/CRITIC_v1.md` (re-run film-critic if missing). Preview sent to the user. STARTED 9 Oct 20:45 (user: "usage reset lets go"). Two background agents: (a) `map` beat kind in `lab/curvelf/flow.py` + Natural Earth 10m data in `lab/curvelf/data/`, test film `lab/curvelf/maps_test/`; (b) Hormuz FACTS.md, script.py, POST.md, CHANNEL.md in `lab/maps/hormuz/`. If those files are missing, the agent died: re-launch. Original plan: (1) generalise the ASCII map so it can draw any region from real coastline
  data (Natural Earth, public domain); (2) fact base for Hormuz (EIA chokepoint figures: width, share of world oil;
  the trend desk's "21 miles" and "a fifth" are UNVERIFIED); (3) script to CRAFT, lint, voice George; (4) stills, render,
  critic. Channel name to pick with him. Money: same YouTube arithmetic as the other channels (£0 before 2027).
- Economy pilot ERROR found by the Hormuz research (9 Oct): its line "In July, after the strait had reopened" is partly wrong (a June reopening collapsed in early July). Fix `year_03` before that pilot is ever uploaded.
- Also unanswered: Visa film to How They Profit on Wed 14 Oct (recommended: its figures are right until Visa reports in late Oct).

## 1c. 10 Oct, early hours: DONE, waiting on the user's three decisions
| Item | File | State |
|---|---|---|
| Map style frames A-F + neon and flow clips | `lab/maps/style/` (sheet.jpg, STYLE.md, style_frames.py; real relief ETOPO 2022 in data/) | DONE, sent. Recommended: F (system) with E (thermal flow) and C (neon) as set pieces. WAITING: user picks the look; then restyle Hormuz in the engine and re-render |
| Steve/GTA Short (UPLOADED 11 Oct: The Curve id 4k1Mbfggud8, public 12 Oct 12:00Z, user said "do whatever needs done") | `lab/curvelf/sh_steve/shorts/short_steve.mp4` (35 s, loops; facts `FACTS.md`; premise half true: universal-modder bridge, not AI dreaming) | DONE, sent. Needs a film-critic pass before upload. WAITING: user yes/no to The Curve |
| Attention playbook | `lab/research/ATTENTION_PLAYBOOK.md`, CRAFT.md §9 | DONE. Key: AI narration costs engagement (likes -5.4%, shares -7.4%) -> the user's own voice is an edge |
| Flash stickman talker | `lab/stickman/talk.py`, `flash.py`, `out/test_talk*.mp4` | DONE (tested on macOS `say`). WAITING: user's 10-30 s voice memo into `lab/stickman/in/`; then ElevenLabs speech-to-speech (premade voice) -> `in/changed.*` -> `talk.py` |
| Hormuz | `lab/maps/hormuz/HORMUZ_v2.mp4` | USER 10 Oct: goes on THE CURVE, style F. UPLOADED 10 Oct 22:30: HORMUZ_v5.mp4 -> The Curve, id teTMVjz6LTs, private, public Sun 11 Oct 16:00Z, title "Hormuz Is Closed. The Oil Isn't.", thumbnail out/thumb_8ships.jpg SET. Strait status checked 10 Oct: still ~5-10% of normal traffic (title holds). Test & Compare pairs in POST.md (user adds in Studio). Pin comment by hand. Two re-voiced lines and a brighter drone are laid, not yet rendered. Render with FLOW_BED=drone |
Engine changes 10 Oct: standalone Shorts (film "") loop with no end card; OPEN_RESOLVED starts the camera at its first place.

## 1f. 16 Oct night: AI MODEL PAUSED, THE CURVE STYLE REBOOT (user)
- User: 'stop the AI model for now'. Nadia launch kit is complete (ofm/POSTING_PACK.md, POST_READY/); Fanvue launch Mon 19 Oct is ON HOLD until he restarts it. Nothing running for OFM.
- User wants The Curve to move from the flat 'chart' style to crisp, colourful 3D (Unreal/Blender quality), Zack-D-Films-level curiosity and pacing, real-footage cuts (short, commented), segments built to cut into Shorts. Already-scheduled videos stay. First film: Tesla's new Roadster (thrusters / upside-down showcase), then a Musk-universe series (Starlink count, space debris, xAI data-centre city, Dyson sphere / Kardashev).
- STYLE TRIALS (in progress, folder lab/curve_v2/trials/): A = AI video hyper-real (A_aivideo/make_a.py: Seedream stills -> Kling 2.6, ~$0.71 WaveSpeed; plus 1 Higgsfield Cinema Studio clip job 7cb05651-484e-4946-8c48-34387a2e37cf); B = Blender procedural 3D (agent building lab/curve_v2/trials/B_blender/); C = hybrid real footage + 3D overlays (waits for research); VO tests in trials/vo/ (George, Chris, Callum). Research agent writing lab/research/TESLA_ROADSTER_FACTS.md, MUSK_UNIVERSE_TOPICS.md, RADAR_2026-10-16.md, ZACK_D_SKELETON.md.
- 17 Oct: TOOLCHAIN (lab/research/TOOLCHAIN_2026-10-16.md, evidence-ranked). INSTALLED + vetted: MCP for Blender (`claude mcp add blender` user scope, DISABLE_TELEMETRY=true, BLENDER_MCP_SAFE_MODE=1; add-on in ~/Library/Application Support/Blender/5.2/scripts/addons/blender_mcp.py, content telemetry opt-in default OFF, socket localhost:9876; to use: open Blender GUI > enable add-on > Start MCP Server, then new Claude session); Camera Shakify (Blender extension, enabled); @remotion/install-whisper-cpp 4.0.532 + scripts/whisper-setup.mjs (whisper.cpp 1.7.6 + medium.en into lab/motion/whisper.cpp, gitignored). Remotion deps installed (npm install). NOT installed (his call): C4D 2026.4 built-in MCP (Maxon app update), Z-Image Turbo in Draw Things (thumbnails, in-app download), Sonniss GDC 2026 SFX (7.47 GB), mlx-audio (ElevenLabs v4 beats best open TTS by ~270 Elo), HyperFrames (overlaps Remotion; A/B later). Unreal skipped (M1 + disk).
- STYLE C REAL v1 DONE: lab/curve_v2/trials/C_hybrid/C_real_footage_v1.mp4 (Remotion comp CurveV2-HybridC-Real; real Tesla clips in lab/curve_v2/footage/tesla_2026-10-15 + SOURCES.txt; Chris VO; -14.8 LUFS). Critic running -> trials/C_hybrid/CRITIC_C_v1.md. Roadster facts: lab/research/TESLA_ROADSTER_FACTS.md (demo 15 Oct 2026 McGregor TX; 0-60 0.81 s Tesla-timed; fans 2 g + 10 gas thrusters; production 2028).
- 17 Oct late: STYLE C v1 critic 5/10 (CRITIC_C_v1.md). C v2 BUILT per fixes: lab/curve_v2/trials/C_hybrid/C_real_footage_v2.mp4 (Remotion comp CurveV2-HybridC-Real2; 4K Tesla clip punched 2.6x, 8x slow-mo via ffmpeg minterpolate; side-view force inset; callback ending 'VACUUMED.'; 40px credit strip; -14.3 LUFS after acompressor+loudnorm). Fresh critic running -> CRITIC_C_v2.md. Shorts cut of v1 exists (C_real_footage_v1_SHORT.mp4, comp CurveV2-HybridC-Real-Vertical, whisper captions); redo the Short from v2 after critic. Blender v2 (accurate mechanism: fans+skirts, 200 L + 400 L COPVs, 10 nozzles 4 rear/4 corner/2 front; HDRI studio_small_09 in lab/curve_v2/assets/polyhaven) running -> trials/B_blender/v2/. Style B v1 + A clips sent to user. WAITING ON USER: style pick ('go hybrid' recommended = real footage + Blender explainers + rare AI), narrator pick (1 George / 2 Chris used in trials / 3 Callum), Sonniss SFX yes/no, WaveSpeed top-up.
- CRAFT conflict to resolve after the user picks: CRAFT §2 says 'narrate like a professor'; the user now wants a Zack-D-style curiosity narrator. Update CRAFT once the trial is decided.
- CONNECTORS 16 Oct (after app update): all claude.ai connectors he uses are connected (Zapier/YouTube, Higgsfield 9.46 cr, ElevenLabs 0/208,793 chars used, vidIQ (0 credits to 5 Nov), Canva, Figma, Notion, Gmail, Drive, scheduled tasks). Claude in Chrome: NO browser connected (user must open Chrome + the Claude extension). The long needs-auth/failed list = ~90 claude.ai ACCOUNT plugins he never uses (finance, bio-research, zoom, cockroachdb, stackhawk...); disable in claude.ai Customize > Plugins (also stops the hawkscan post-commit hook spam). Budget: WaveSpeed $1.01 before trial A.

## 1e. 13 Oct: THE CURVE CHANNEL AUDIT (user asked why videos show 'uploading shortly')
- 5 new-look uploads STUCK in YouTube processing since 8 Oct 17:07-17:20 (just before the daily cap): 38tmCX4gq34 (Two AI Labs Short, public), BrNE7GCltBo (Big Macs Short, public), x4cBx9G5luU (1865 Paradox Short, public), yTt9_y5DTZ0 (THE AI THAT ESCAPED long film, public), tFBpt5B1z10 (Reward Hacking Short, sched 15 Oct). YouTube has all bytes (fileSize = local size); encoding identical to ones that processed. Fix = delete the 5 stuck + re-upload the same files (indices 0,2,3,4,7 of uploads_newlook.json). WAITING ON USER OK (deletion).
- 4 Oct old-look uploads still on the channel: long films z6Z5LNa0HGE (Too Dangerous v1) and J9mpX99QEZc (Price of Thinking v1) are private but SCHEDULED 26 Nov = would duplicate long films (rule breach). Unscheduling via API was BLOCKED by permissions: needs user OK. qz2esWpcIto (Escaped v1) private, unscheduled. Old public Shorts duplicate new scheduled ones: kQK54NgtQxc vs S5nN7Yxk6_A (13 Oct), VUlCncjg_jg vs SQSkx0EMVwg (14 Oct), 50unbceaWQs vs tFBpt5B1z10, cuc-0dapdUY vs QP1PpnXz_K4 (17 Oct); also public ULdI4-Sj5Z4, YNNxOdi6mxU, ewxP_ION8lk (old versions of the stuck Shorts). User to choose which set stays.
- v2 thumbnails APPLIED 13 Oct: 982Z-6peFbM (LF02 B), j17HdEgAQ04 (LF03 A), teTMVjz6LTs (Hormuz A), Lnb7eAGzNEA (Visa A). Still to apply: LF01 A once Escaped is re-uploaded; Ponzi B blocked (Money Crimes not phone-verified).
- Hormuz title check: an undated CENTCOM report says 55 vessels transited in a day; if current, 'Hormuz Is Closed' is stale. hormuz-48h-review (13 Oct 18:00) must verify.

- 14 Oct 11:10 UTC, USER SAID YES to fixes 1-5. DONE via API (all set private, no publishAt): SQSkx0EMVwg (dup Short, was due 14 Oct 12:00), z6Z5LNa0HGE + J9mpX99QEZc (26 Nov auto-publish removed), stuck 38tmCX4gq34, BrNE7GCltBo, yTt9_y5DTZ0, tFBpt5B1z10. BLOCKED by permission classifier despite the yes: x4cBx9G5luU (stuck 1865 Short, still PUBLIC + broken) and QP1PpnXz_K4 (dup Short, still scheduled 17 Oct 12:00) -> user can set both to private in Studio or allow the Zapier write. RE-UPLOADED The AI That Escaped 14 Oct 11:42 UTC: NEW ID qlDCnRmScRw, private, public 2026-10-15T16:00:00Z, v2 thumbnail A SET; PROCESSED OK (11:38) within minutes; old stuck id moved to key 'STUCK_PRIVATE_8OCT:...' in done.json. After put: record new id, set thumbnail via zapier-thumb, verify processing. Not in scope: S5nN7Yxk6_A (new Escape Short, published 13 Oct) duplicates public kQK54NgtQxc.

- 15 Oct: WAVESPEED LIVE (key in ofm/.env, gitignored; user pasted it in chat, suggest rotating). Refs locked: characters/a1_refs.json (A1 + 3 Nano Banana edits). SOCIAL SET (Seedream, user's pick): 20/20 approved in ofm/pipeline/out/a1/approved/ (APPROVAL.md, approved_sheet.jpg; avatar p12 v1; first posts p05, p08, p13 sq; p10 reshot with fixed prompt). FANVUE RAW SET (Nano Banana, real-photo look per user): out/a1/shoots/fanvue_raw/ 20/20 face-pass, not yet independently reviewed (its p10 used the OLD prompt: check phone logo/neckline). REELS: stills for r01-r03 shot (out/a1/shoots/a1_reels), 3 test clips generating (reels.py). Rule: socials polished/Seedream, Fanvue raw/Nano Banana. Balance ~$6.90 at 15 Oct.

- 15 Oct evening: LAUNCH CONTENT READY. 17 Reels pass QC (R16, R19 rejected: TV faces / mirror second person; R04 newspaper blurred; R11 trimmed 4.3 s). Every day 19 Oct-1 Nov has a Reel; 11 by Mon 26. POSTING PACK: `ofm/POSTING_PACK.md` (day-by-day files, captions, times, Day 0 setup). Phone folder: `ofm/POST_READY/` (63 files, gitignored). WaveSpeed balance ~$1 (top up ~$20). LESSON: never chain a prompt edit and a paid shoot with ';' (failed edit -> shoot ran on old prompts, $0.39 wasted); use '&&'. Prompts with mirrors make duplicate people: avoid mirrors. WAITING ON USER: Fanvue sign-up + KYC (blocks 19 Oct launch), IG/X/Threads accounts with AI labels, PPV sets (his), WaveSpeed top-up.

## 1d. 12 Oct: FOCUS SWITCHED TO AI OFM (user: "yt decent backlog, move away for a bit")
- YouTube backlog is scheduled to 19 Oct (see section 2 + uploads_newlook.done.json); Spanish Hormuz UPLOADED 12 Oct 04:20 to Curva Explica: id Br0OyTJqSHA, private, public Thu 15 Oct 22:00Z, title "Ormuz está cerrado. El petróleo no.", thumbnail `lab/maps/hormuz_es/out/thumbs_v2_a.jpg` SET. Weekly growth review runs Mondays 09:00.
- AI OFM (Fanvue AI persona): plan `FANVUE_PLAN_8OCT.md`; ChatGPT's earlier research in `~/Documents/Codex/2026-10-09/vidiq-plugin-app-69dd11f3e50c8191b1ca48d03cf7e2ad-openai-curated/outputs/fanvue/`. User has the paid Skool "AI Model Academy" (aimodelacademy) and is in its Telegram + Discord; Chrome is logged in to all three (Claude in Chrome connected). He wants: a fresh persona built from research, viral social potential, high spenders, conversion + upsell. DONE 12 Oct: public market research `ofm/MARKET_RESEARCH_2026-10-12.md` (committed); 3 persona options `ofm/PERSONA_OPTIONS_2026-10-12.md` + concept images `ofm/concepts/PERSONA_OPTIONS.jpg` (gitignored, Higgsfield soul_2, ~16 credits left). Recommendation: A1 face (mature 39, silver streak) + gaming/cosy hobbies for chat. USER PICKED A1 (14 Oct): Nadia Vale, mature 39, silver streak. Build on CHARACTER_BIBLE_A / a1.json. DONE: community/course analysis `ofm/COMMUNITY_INSIGHTS_2026-10-12.md` (LOCAL ONLY, gitignored: summarises his paid private course/chats, never push it). Key: IG link-in-bio/landing pages flagged 1-7 Oct; AI label restored reach for several; skit Reels pull non-buying audiences (109K followers = 59 subs); money is in chat; Fanvue withheld earnings for face-swapped/stolen base content; coach upsells are traps; much course advice breaks rules (marked DO NOT USE). Gaps: Telegram General Chat before 25 Sep, some topics, Wins screenshots. DONE: WaveSpeed pipeline `ofm/pipeline/` (README.md, MODELS.md, ws.py, prompts.py, character.py, shoot.py, qc.py, reels.py; dry runs pass; spend caps block before sending). Stack: Seedream 5.0 Flash Edit $0.027/photo (10 refs), Nano Banana 2.1 Edit ~$0.07 fixes, Kling 2.6 Std $0.21/5s Reel; ~$23/month for 60 photos + 20 Reels. LoRA: Z-Image trainer ~$2.50/run, $0.01/image, train after 15-25 approved images. Paid test (~$0.08) waits for `ofm/.env`. IDENTITY TEST 12 Oct 04:45 (`ofm/IDENTITY_TEST_2026-10-12.md`): reference-edit (Nano Banana 2.1, 1 ref) HOLDS the A1 face + age across new scenes; Higgsfield soul_2 + image ref does NOT (copies pose, face changes, drifts young). Higgsfield credits ~9.6 left. OVERNIGHT DONE 12 Oct ~05:30: `ofm/CHARACTER_BIBLE_A.md` (name Nadia Vale; alt Livia Marlowe, Inès Calder; streak on her right side; handles not checked), `ofm/COPY_PACK.md`, `ofm/PLAYBOOK.md` (launch Mon 19 Oct or stop; chat + PPV ladder before content; X reply + AI-allowed Reddit carry the link; IG link-free until 18 Nov; gates with numbers), `ofm/BACKLOG_A.md` (30 Reels/60 photos/14-day calendar; launch set R01-R14 + P01-P20; 'with her' POV lead), `ofm/pipeline/characters/a1.json`, `ofm/pipeline/shots/a1_photos.yaml`, `a1_reels.yaml` (dry-runs pass), `ofm/ALIGNMENT_2026-10-12.md` (VERDICT: right main bet, ~£0 cash by day 30; mid case £35/£145/£315 net at day 30/60/90; ~5% chance £2k by day 90; ~£3/h ramp; the 38 shop messages in ALIGNMENT_8OCT are still best £/hour, 30 min of his time). Pipeline fixes: age guard 25-45, QC rejects faces reading 5+ years young, generic keep-identity text in reels. QC DONE `ofm/QC_2026-10-12.md` (28 pass, 27 fixed incl. spec now matches images: green-hazel eyes, parting on her right, 3-5 cm streak; honesty lines rewritten; IG link-free 30 days to Wed 18 Nov). R11-R19 added to a1_reels.yaml (19/19 dry-run). NEEDS OWNER: gates (day 14 = Mon 26 Oct is only 7 days live; suggest counting from launch: Mon 2 Nov / Wed 18 Nov), Threads link (tied to IG), avatar not the low-cut image, reject branded controller + bus/cab shots at face approval. MORNING ASKS: pick A/B/C (A1 recommended); create `ofm/.env` (WAVESPEED_API_KEY=...); then: WaveSpeed paid test (~$0.08), compare Seedream vs Nano Banana on 3 scenes, build 20-30 image identity set + face QC, launch set, his KYC + accounts. No `ofm/.env` yet (user creates it; never paste the key). Next after pick: character bible, 20-30 image identity set + face QC + lock, 30 Reels + 60 photos backlog, merge into `ofm/PLAYBOOK.md`.
- LOW-STIM PHONE KIT (user idea 12 Oct evening, 'yes go'): dark-grey low-stimulation home-screen kit for Etsy/Gumroad. `products/lowstim_kit/` (make.py wallpapers+200 icons, mock.py listing images, guide_pdf.py, GUIDE.md, LISTING.md, PROMO.md, QC.md). Built + QC'd + fixed: 24 wallpapers (6 designs, home+lock, iPhone 1320x2868 + Android 1440x3200), 100 icons x 2 tones (Material Symbols, Apache 2.0, no brand logos), 7-page PDF, 6 listing images. Files to upload: `products/lowstim_kit/out/LowStim_1..3_*.zip` (Etsy, each <20 MB), `LowStim_Phone_Kit_FULL.zip` (Gumroad only, 27 MB). Price £5.99. WAITING ON USER: upload listing (Etsy shop had 0 search visits in 21 days per ALIGNMENT_8OCT, so traffic must come from PROMO.md short videos). Don't claim 'Niagara/Lawnchair icon pack' (needs APK).
- Lines kept: AI disclosed (Fanvue rule), never claim to be a real person, no fabricated emergencies, no off-platform payment; assistant makes SFW promo + strategy only, paid content is his; READ-ONLY in his chats (never post/DM); no usernames in our notes.

## 2. YouTube: what is uploaded (all PRIVATE with a publish time; ids also in `~/Bernard/channel/uploads_newlook.done.json`)
| Video | Channel | Public (UTC) | Id |
|---|---|---|---|
| Short: Two AI Labs Cut Their Prices | The Curve | 9 Oct 12:00 | 38tmCX4gq34 |
| The Price of Thinking (LF02_FLOW_v6) | The Curve | 9 Oct 16:00 | 982Z-6peFbM |
| Short: Big Macs | The Curve | 10 Oct 12:00 | BrNE7GCltBo |
| Short: 1865 Paradox (jevons) | The Curve | 11 Oct 12:00 | x4cBx9G5luU |
| The AI That Escaped (LF01_FLOW_v7) | The Curve | 12 Oct 16:00 | yTt9_y5DTZ0 |
| The Original Ponzi Scheme (MC02_PONZI_v4) | Money Crimes | 13 Oct 16:00 | MYerI1teKMg |
| Short: Secret Message Board (talk) | The Curve | 14 Oct 12:00 | SQSkx0EMVwg |
| Short: Why AI Cheats (cheat) | The Curve | 15 Oct 12:00 | tFBpt5B1z10 |
| Short: Why OpenAI Cancelled (held) | The Curve | 17 Oct 12:00 | QP1PpnXz_K4 |
| Short: Safety Filters Off (test) | The Curve | 18 Oct 12:00 | RIXR2MT2_wU |
| Short: It Knew the Rules (knew) | The Curve | 19 Oct 12:00 | tAuA_hP9v1c |
NOT uploaded yet:
- `lab/curvelf/lf01_escape/shorts/short_escape.mp4` (index 5 of `channel/uploads_newlook.json`, due 13 Oct 12:00Z): READY. YouTube refused on 8 Oct ~19:00 UK: daily upload cap on The Curve. Retry after ~19:30 UK on 9 Oct.
- `lab/curvelf/lf03_held/LF03_FLOW_v4.mp4` (index 8, due 16 Oct 16:00Z): two music dips of about 1 s near 7:24 and 8:02 (12-15 dB). User was asked to listen and say "fine"; no answer yet. Fix in `lab/curvelf/mix_flow.py` `steady()` or upload as is with his OK.
- Thumbnails (`lab/curvelf/<film>/out/thumbflow_a.jpg`): YouTube returns forbidden until the user phone-verifies each channel at youtube.com/verify. Then: `youtube_upload.py zapier-thumb VIDEO_ID file` and the same two-step send.
- How They Profit 06 Visa film UPLOADED 11 Oct (user: "do whatever needs done"): id Lnb7eAGzNEA, public Wed 14 Oct 16:00Z, thumbnail D set; critic v7 = UPLOAD. Visa reports fiscal 2026 on 27 Oct: after that the "last year" figures are stale (pin a correction comment then).
Lustig correction: APPLIED 8 Oct (film fvCbFDHik1s, Capone Short r1l_L9kkTkk, comment posted). User must PIN the comment by hand.

## 3. How to upload (Zapier is on a paid plan since 8 Oct and works)
1. `~/youtube/.venv/bin/python lab/tools/youtube_upload.py zapier-init channel/uploads_newlook.json N` prints url, headers (X-Upload-Content-Length) and body.
2. Send it with the Zapier connector: app api `YouTubeV4CLIAPI`, action `_zap_raw_request`, tool_name `youtube_make_api_mutating_request`, method POST, url `https://www.googleapis.com/upload/youtube/v3/videos`, querystring `uploadType=resumable&part=snippet,status`, the headers, the body, and the channel's `connection_id`: The Curve `02f9e902-69d2-8a12-af4b-b4f4cd146eeb`, Money Crimes `02ce9a67-dbe7-8998-8da5-26da5fc35e26`, How They Profit `02d0de21-a222-85ea-aea9-5b0920dd34b0`. (`02587cb2-...` is a personal account with no channel: ignore.)
3. Take the `location` header from the reply: `youtube_upload.py put "<location>" <file> --manifest channel/uploads_newlook.json`.
4. TRAP: `put` often ends with "410 Gone" although the video landed. NEVER re-send. Look the id up first (Zapier GET `https://www.googleapis.com/youtube/v3/search?part=snippet&forMine=true&type=video&order=date`), confirm fileSize with `videos?part=fileDetails,status`, then write the id into `channel/uploads_newlook.done.json`.
5. RULE from the user: a long-form film must never exist twice on a channel. Do not change visibility in YouTube Studio through a browser (blocked; it is the user's job).

## 4. The film engine (one-camera look)
- `lab/curvelf/flow.py <film> est|lay|lines|times|still <t...>|seg a b|short ...` (Shorts need `FLOW_VERT=1`). A film folder = `script.py` + `src/ai/<id>.*` + `src/photo/<id>.*`; work files in `<film>/flow/`.
- Voice: ElevenLabs George `JBFqnCBsd6RMkjVDRZzb`, one take per line into `<film>/flow/takes/NNN_<id>/` (make the folder first), then `flow.py <film> lay`. About 130,000 characters left until ~16 Oct. Never use the local Kokoro voice. Never clone a real voice.
- Render: `lab/curvelf/render_flow.sh <film> <OUTNAME> 6` (serious score: `FLOW_MUSIC=a.mp3,b.mp3`; LF01 also `FLOW_LIMIT=0.56`). Shorts: `shorts_all.sh`; sound re-cut: `remux_shorts.py`.
- Changed 8 Oct: every figure is crisp type (LONG_NUM=0, LONG_SPLIT=0); script `HOLD = {beat: seconds}`; AI-illustration tag pinned to the screen; Shorts headline band at HEAD=300; quote cards narrower and higher in Shorts; a script with `LANG = "es"` gets the multilingual word-timing model and Spanish engine words (table `UI` in flow.py).
- Critic reports: `lab/curvelf/CRITIC_FINAL_8OCT.md`, `lab/curvelf/CRITIC_V2_8OCT.md`. Thumbnails: `lab/curvelf/thumb_flow.py`. Before any upload run a critic on the actual file (repo skill `film-critic`).

## 5. Money plan and the user's decisions today
- Goal: £2,000/month digital first, then £4,000. He wants to quit the warehouse job by the end of 2026. Report: `~/Bernard/ALIGNMENT_8OCT.md` (quit by 31 Dec about 2%; £2k December about 10%; only walk-in sales + websites + selling video-making sum to £2k; gate Sun 18 Oct = 10 doors walked). His record: 0 doors, 0 of 38 ready shop messages sent. DO NOT LECTURE: arithmetic only.
- Open asks he has not answered: order the NFC kit (~£55, links in `~/Bernard/sales/research.md` A1/A3/A5); which account sends the 38 shop messages (`~/Bernard/sales/reels/send_sheet.html`); a town + afternoon for 10 doors; yes/no to a "videos for businesses" offer page; "build the admin offer" (AI back-office for local shops); phone-verify the YouTube channels; connect TikTok/Instagram/Facebook and Google Drive in Metricool (only one YouTube channel is connected there, so NOTHING is cross-posted).
- Dropped by him on 8 Oct: Uber Eats.
- Fanvue AI persona ("AI OFM"): he called it the next step. Plan: `~/Bernard/FANVUE_PLAN_8OCT.md` (6-9 month build; about 8% chance of £500+ in Dec; day-30 gate Sat 7 Nov). Waiting on him: pick persona A "Mara" / B "Ines" / C "Tess" (or his own), Fanvue sign-up + ID. Assistant limits: safe-for-work material only, invented face only, no account creation or ID. Bio and messages must say AI.
- Scale: he wants 10 channels by 31 Oct and 100 by 31 Dec. He was told 100 is blocked (one phone number verifies 2 channels a year; monetisation is per channel; linked-network bans; capacity) and said "go" to: pilot two new channels + translate one film into Spanish. New channels: NO Higgsfield; use GPT/Claude/public image generation and real photos with clear rights. Existing scale plan: `~/Bernard/AUTOMATION.md`.

## 6. Next steps, in order
1. After 19:30 UK 9 Oct: upload `short_escape` (index 5) and LF03 v5 (index 8) via section 3. Before each upload, a critic must have passed the file (LF03: picture as v4 which passed; only the music bed changed).
2. Both pilots are finished files. Nothing more on them until the user decides on the channels (and on M3, a look of their own).
3. Spanish film: upload when the user names the channel. YouTube multi-language audio on the English video would be the ideal home but is not available through the API.
4. New channels need the user: create, phone-verify, connect in Zapier; names from each pilot's CHANNEL.md.
5. Still unmade: Shorts for Ponzi and Visa; TikTok/Reels wait on Metricool connections.

## 7. Standing rules (never break)
- Never touch TikTok `thegoldenplate` or `passdaboof2`. Pinterest DTwork7: read-only. Nothing is sent to any shop without his approval. Never copy API keys into a handoff. No model names in commits or PRs. Delete `media/` in a commit before the PR is merged.
- Reply format: tables first, bare `- [ ]` checklists, short lines; every line that needs him starts with 5 emojis and one bold ask.
- A hook asks for a security scan after each commit: not applicable (no running app); skip and say so.
- Save this handoff to ALL of: `~/RESUME_HERE_2026-10-05.md`, `~/youtube/CURRENT_STATE.md`, `~/CLAUDE_HANDOFF_BUNDLE/`, `~/Downloads/CLAUDE_HANDOFF/`, `~/Downloads/GoldenPlate_Vault/` (00_RESUME_HERE.md, 00_START_HERE.md, 00_CURRENT_STATE.md, CURRENT_STATE.md), and `~/Bernard/HANDOFF.md` top.

---

---
# Earlier handoff (older; the block above wins where they disagree)

# Handoff: the AI explainer channel + walk-in sales (read this first in a new session)

This repo is a scratch space (the DeepSeek-V3 files are unrelated). The user works across **two Claude accounts**
(a Mac desktop session and cloud sessions). They share **nothing but this GitHub repo**: artifacts, Notion and
databases on one account can't be read from the other. Push anything the other side needs here.
Updated 5 Oct 2026 (evening UTC), cloud session on branch `claude/funny-newton-gd9w8v`. **Start with "5 Oct, evening: SWITCHING ACCOUNTS"
just below (`STUDIO.md` maps everything), then "4 Oct", "3 Oct evening", "3 Oct: jazz", "2 Oct" and the rest.**

## 6 Oct, early hours: Mac desktop session on the second account (start here)
- **Direction change (user, 6 Oct):** "is this something places will buy... I want really high quality, impressive
  products so I can feel confident walking in... like the Google review cards". Claude's answer: the hygiene Reel is NOT
  the product (templated, no food, owners don't post Reels); it becomes a free extra. **Lead product = the Google
  review stand** (NFC + QR, the shop's name printed on it), £35 (£49 personalised), then "review care" £25/mo. Prices
  are Claude's suggestion, NOT approved. Next build: a print-ready stand insert generator (per-shop name, QR fallback),
  one demo stand, inserts for the first 10 doors. The user must order blanks (sales/research.md A1-A3); not ordered yet.
- **Alignment agent (6 Oct):** messaging the free Reel then visiting warm replies = about £150-400 in 14 days; £79 is
  under market (suggested £99 list, first 10 shops £49 first month then £79); at £79 it takes 25 shops for £2k, not 20;
  pause AI influencer, music packs, channels 4-10, websites, weekly TikTok, paying for Zapier; a Christmas bookings
  pack for pubs/restaurants (£149-199) is the best alternative. He has built kits three times and walked into 0 shops.
- **Built tonight:** `sales/reels/contacts.csv` (public Facebook/Instagram/email/phone for the 52 shops: 38 can be
  messaged, 14 phone or walk-in only; pages were not opened, matches rest on search results) ·
  `sales/reels/send_sheet.py` -> `send_sheet.html` (per shop: contact link, first-touch message with no price, Reel
  file, sent tick, notes; batches keep same-street neighbours apart) · `sales/reels/QC_REPORT.md` (two independent
  passes on the real frames) · `make_reels.py`: names with an unspaced "/" split as two names, and an inspection date
  over 18 months old is replaced by "THE HIGHEST RATING THERE IS" (11 shops). All 52 Reels are rendered on the Mac in
  `sales/reels/build/reels/` (gitignored). Nothing has been sent to any shop; the user approves every message.
- **Money Crimes 03:** `lab/longform/saladoil/VERIFY.md` (44 claims: 34 confirmed, 4 wrong, 4 softened, 2
  unverifiable). Script and FACTS corrected: bankruptcy 19 Nov 1963 (Kennedy three days later), NYSE up to $12M (not
  $36M), "American Express Warehousing" (not Field Warehousing), 60,000 tons, soybean and cottonseed. Before voicing:
  re-read the court quotes and check Miller directly (the file's last section).
- **This account's connections:** GitHub (gh, Bernigglywiggly, push works), Zapier (same account, the 4 YouTube
  connections are there, still at the task limit: reads fail too), vidIQ, Notion, Gmail, Canva, Metricool; Higgsfield
  CLI is signed in on the Mac. Python with skia: `~/youtube/.venv/bin/python` (system python3 has no skia).
- **Gotchas:** in zsh an unquoted `$IDS` is ONE argument, so `render $IDS` silently rendered Stone instead: pass ids
  literally and check file times. Terminal `claude` in ~/Bernard was on API billing (cash): use the desktop app.
- **6 Oct, 01:45: the user switched to YouTube** ("I just enjoy it"; he likes watching the work happen, so send stills
  and sheets as they are made). The stand work is parked, not dropped.
  - **HTP 06 Visa** (`lab/ch2/ep06`): script v0 (36 lines, about 7 min, lint 0), a new shape (one card tap on a map:
    Lisbon cafe to an Ohio bank, an illustration, labelled), every figure checked against the 8-K and 10-K on sec.gov
    (FACTS.md "Verified 6 Oct"; 329 billion was NOT found, the script uses 257.5 billion). `scenes.py` storyboard v0
    and `film.py`; stills on an estimate: `python3 tools/est_timeline.py ch2/ep06 2.1` then
    `EP_BUILD=build_est ~/youtube/.venv/bin/python film.py still <times>`; sheet in `storyboard_v0.jpg`. Known
    weak spots: frame 0 is a sparse map (one pin); node sub-labels are small; CLIPS (Shorts) not written; no critic
    has seen it. **Visa reports fiscal 2026 in late October: swap the figures before voicing.** sec.gov blocks curl;
    read filings through the browser pane.
  - **The Curve LF04 "The Pause": the script's premise is wrong** (`lab/curvelf/lf04_pause/VERIFY.md`: 28 claims, 12
    confirmed, 5 wrong, 7 disputed, 4 unverifiable). OpenAI's own report says the pause followed a 20 Sep incident (an
    agent got through a DNS gap in its sandbox and queried an outside chatbot); the Census/SEC/Education incidents were
    May-June and only disclosed the same day (25 Sep). Also: the first pause was 18 August, not July (LF01 says August);
    the pause covers "all training, evaluation, and inference with tool-use" of the most capable models. Rewrite the
    open and the "why" chapter around the DNS incident (OpenAI published its timestamps) before anything else.
  - **Voice is the bottleneck:** Higgsfield has 26.72 credits (HTP 05 needs about 36, The Curve about 130, Money
    Crimes about 200). There is no ElevenLabs key in the environment. Uploads are still blocked by Zapier's task limit.
- **6 Oct, 02:10: NEW LOOK, CHOSEN BY THE USER ("B. 1 million percent holy shit that looks good").** He dislikes the
  serif ledger look. References: eight pollar.news TikToks (black, white hairlines, tiny mono notes, a heavy grotesque
  sans, ONE accent as highlight boxes, charts made of small squares, wireframe schematics, and NO CUTS: one drawing,
  one continuous camera). His own taste on top: ASCII art, a slight futuristic edge, ethereal light (Tron Legacy,
  Titanfall 2, Destiny's Fallen colourways). What he approved: `lab/ch2/ep06/rend_test.py` rendition B ("flow"): the
  map set in type (# + % * coast, dots for land), one glowing line, Inter Tight 600 + IBM Plex Mono 400, accent ether
  cyan #5FF0E4 (violet #A98BFF and red #FF6A4D were offered; he has not picked, cyan is the working default), nested
  zoom levels (ocean -> figure -> one lit cell). `look_test.py` = the still study. Do not copy pollar's yellow.
  NEXT: rebuild HTP 06 as one page with one camera (`lab/ch2/ep06/flow.py`, in progress): ocean -> $17T matrix ->
  push into the arc where the four-party route lives -> interchange under the network -> meters -> back out to the lit
  cell. The serif storyboard (`scenes.py`, `storyboard_v0.jpg`) is the OLD look, kept for its content and timings.
  Whether the other channels and the 59 finished videos change look is NOT decided: ask before converting anything.
- **6 Oct, 03:00: SOUND APPROVED BY THE USER ("yes").** Voice = **George** (ElevenLabs premade
  `JBFqnCBsd6RMkjVDRZzb`, eleven_multilingual_v2, defaults, speed 1.0), NOT Sterling ("same american guy... tacky, get
  rid"). He also liked Rob (`2ajXGJNYBR0iNHpS4VZb`): Claude suggested Rob for Money Crimes, not decided. Music = a
  2-step **garage** bed synthesised in code (132 BPM, F minor) so we own it; vocal chain = high-pass, mud cut,
  presence, air, de-ess, compression, a 9% bright plate; the bed side-chains under the voice; -14 LUFS. All in
  `lab/ch2/ep06/mix_pre.py <build> <picture.mp4> <out.mp4>`. Voice pipeline without an API key: the ElevenLabs
  connector saves one mp3 per line into `<build>/takes/NN_<line id>/` (the folder must exist first), then
  `lay_takes.py <build>` writes lines.json + voice_dry.wav (word times from faster-whisper), then
  `EP_BUILD=<build> flow.py clip 0 <secs>` and `mix_pre.py`. Approved preview: `HTP06_preview_george.mp4` (chapters
  0-2, 1:34; build dir `build_george`). ElevenLabs had about 160k characters left (resets about 16 Oct); Higgsfield
  16.12 credits (10.6 went on Sterling takes that are now unused). Claude cannot hear: the user is the only check on
  pronunciation and on whether the bed sounds good. NEXT: chapters 3-6 drawn, voiced in George, sound effects, critic.
- **6 Oct, 03:45: HTP 06 FIRST FULL CUT EXISTS.** `lab/ch2/ep06/HTP06_full_v1.mp4` (4:18, 1280x720 preview; phone copy
  `HTP06_full_v1_phone.mp4`; both gitignored, rebuild below). All 37 lines are voiced in George
  (`build_george/takes/NN_<id>/*.mp3`, gitignored: about 4,600 ElevenLabs characters to redo), all seven chapters are
  drawn in `flow.py` (chapters 3-6 = `meters`, `cell_story`, `rulebook`, `last_crossing`, camera `keys2`), the music
  plan covers the whole film and `mix_pre.py` has a synthesised sound-effects pass. Rebuild: takes in place ->
  `lay_takes.py build_george` -> `EP_BUILD=build_george flow.py clip 0 258` -> `mix_pre.py build_george
  flow_000_258.mp4 HTP06_full_v1.mp4` (about 6 minutes). Sent to the user at 03:45; NO REACTION YET.
  **NOT DONE:** (1) the independent critic: launched and killed by the account's session limit at about 03:50
  (resets 04:50 London) before writing `CRITIC_v1.md`; re-run it (the brief is the film-critic skill plus the user's
  worry "text overlapping with certain animations and little bugs"). (2) Known flaws: a visible dark patch right of
  the lit cell in the close-up (cell_story blanks far labels with a rectangle); two long fast camera moves; about 1 s
  of near-black in the first dive; SFX levels unheard. (3) Fiscal 2026 figures in late October: re-check FACTS, swap,
  re-voice the changed lines. (4) Full-resolution render, end card, thumbnail, Shorts, POST.md. (5) The other films and
  channels have NOT been moved to this look or voice; ask before converting.
- **6 Oct, 13:05: HTP 06 IS AT VERSION 5** (`HTP06_full_v5.mp4` + `_phone.mp4`, gitignored; rebuild as above). Four
  independent critic passes are in `lab/ch2/ep06/CRITIC_v1..v4.md`: READ v4 FIRST. Claude overclaimed "fixed" on v2 and
  v3; what finally worked was structural, not patching: (1) every block fades out when its chapter ends; (2) the camera
  gets over its target before closing in, and far moves are single "hops" (a 4th value in a camera key = how far to dip
  out); (3) the last chapter is ONE held frame; (4) scenes are populated from their first second (meter tracks, the
  four boxes sketched in). v5 measured: no black frames in any hop or scene. **v5 has NOT been seen by a critic or by
  the user** (the user last reacted to the 1:34 George preview; he has been sent v1-v5 of the full film).
  KNOWN IN v5: in the last 8 s of the last chapter the three-line caption plate covers the bottom box label (fixed in
  flow.py after the render: camera y NY+32; re-render to pick it up); four-parties scene still sparse (about 2% lit);
  hops are quick; small grey notes are small. CONTENT, BLOCKS UPLOAD: two spoken lines about interchange being most of
  a card's cost are unsourced (FACTS.md "Open after the critic pass"); "last year" x6 with fiscal 2026 due late Oct.
  Do not run more critic passes before the user has watched: each costs about 230k tokens and he hit a session limit.
- **6 Oct, 23:45: HTP 06 MASTER IS v7** (`lab/ch2/ep06/HTP06_MASTER_v7.mp4`, 1920x1080, 4:19; phone copy
  `HTP06_v7_phone.mp4`; `flow.py master 0 259.4` then `mix_pre.py`). The user said "v5 looks good". The pre-upload
  critic on v6 (`CRITIC_v6.md`) gave PASS / PASS WITH NOTES on all four gates and "UPLOAD after edits", and its one
  check found a REAL ERROR: **Visa does settle payments and guarantees settlement** (10-K: settlement receivable $4.2B,
  payable $4.6B; non-dollar settlements outstanding 1-2 business days; it indemnifies banks for settlement losses). So
  "never touches / never held your money" was FALSE. Fixed in v7: lines `never` and `close` re-voiced ("lends none of
  that money and keeps almost none of it"; "a company that lent none of it"), the old title dropped (new options in
  `POST.md`), FACTS.md section "Settlement". NEVER reuse the phrase "never touches your money" for Visa.
  Also in v7: no wire-scene boxes over the opening, the cost block in proportion (50/40/10), the headline back for the
  hop to the cell, sources larger; the interchange lines are sourced (Richmond Fed EB 11-05, FACTS.md).
  **v7 has not been through a critic** (v6 had; v7 = v6 plus those changes). NOT DONE: thumbnail, end card, Shorts.
  WAITING ON THE USER: a title; upload now or hold for fiscal 2026 (late Oct; "last year" is said six times); the
  upload itself is by hand in YouTube Studio while Zapier is at its task limit.
- **6 Oct, late: HTP 06 PACKAGING CHOSEN** (user: "u choose the strongest curiosity trigger combo"). Title
  "Visa Isn't a Credit Card Company" + thumbnail D "WHO GETS THIS?" (`lab/ch2/ep06/thumb_D.png`, mock
  `combo_pick.png` from `combo.py`). Test & Compare: D vs H vs A. Nine thumbnails A to I exist (`thumbs.py`,
  `thumbs2.py`). An independent reviewer preferred H as the main and said the first D failed at phone size; D and H
  were rebuilt with the fixes and the rebuilt D has not been re-reviewed. Hold back E (repeats the title) and G
  (misreads as half your spend). Detail in `lab/ch2/ep06/POST.md`. Still owed before upload: critic pass on v7, end
  card, Shorts; upload is by hand in YouTube Studio (Zapier at its task limit).
- **7 Oct, 00:45: THE CURVE IN THE ONE-CAMERA LOOK: TRIAL MADE** (user: "this is what I wanted to do in the first
  place with the curve ... trial run"; keep the Curve's detailed pictures as moving ASCII, add the constant camera and
  the palette). `lab/curvelf/flow_trial/`: `curve_flow.py` (pictures are places in one world; characters live on the
  screen and the pictures slide beneath; camera keys from the voice timeline; thread, labels on plates, captions),
  `script.py` (LF01's opening, 8 lines, quote line left out), `lay_takes.py`, `mix_trial.py` (reuses
  `ch2/ep06/mix_pre.py`). Output `CURVE_FLOW_TRIAL_v3.mp4` (54 s, 1080p, George + garage bed; gitignored, as are
  `src/` pictures re-fetched from `lf01_escape/assets_ai.json` and `build/`). Needs `opencv-python-headless` in
  `~/youtube/.venv` (installed with uv). Render: `curve_flow.py seg a b` x4 in parallel, concat, `mix_trial.py`.
  Bugs fixed on the way: labels under the caption band, two captions up at once, labels lingering through a hop.
  The trial's facts are LF01's (checked 3 Oct by its author, not re-verified): NOT for upload. A QC agent passed v2
  with notes (type clipped at the left edge during drift, two pictures unreadable, whip-fast hops, too dim); v3 fixes
  those: `on_screen()` fades any block near a frame edge or the caption band, hops take 1.5 s, s12 and s15 replace s02
  and s03, levels raised. v3 was checked on stills by its maker only, not by a second agent. Next: the user's verdict, then convert LF01 in full.
- **7 Oct, 01:15: THE CURVE LF01 IS BEING CONVERTED IN FULL** (user: "go"). Engine `lab/curvelf/flow.py <film> est|lay|
  still|seg|lines|times`: every beat of `script.py` is a place in one world; img/clip/num/words/split are characters,
  quote/list/tl are crisp type on plates; chapter names ride the long crossings; thread over the top of each place.
  Pictures re-fetched to `lf01_escape/src/ai/` (gitignored); work files in `lf01_escape/flow/` (gitignored). Running
  on ESTIMATED timings (12:31) until the voice exists. NOT YET VOICED on purpose: a fact-check agent is writing
  `lf01_escape/VERIFY.md` first (the script names models and events from after July 2026; a sibling script had a wrong
  premise). After VERIFY: fix the script, voice all 88 lines with George into `flow/takes/NNN_<id>/` (ids from
  `flow.py lf01_escape lines`, about 10,500 characters), `lay`, render segs in parallel, concat, mix (adapt
  `flow_trial/mix_trial.py`: bed sections per chapter), critic pass, then show the user. Trial v3 passed its checks.
- **7 Oct, 01:40: LF01 FACT-CHECKED, CORRECTED, VOICED; FULL RENDER RUNNING.** `lf01_escape/VERIFY.md`: premise holds
  (66 claims: 34 confirmed, 23 partly, 2 wrong, 7 unverifiable). 24 edits applied to `script.py` (VERIFY section 6):
  the German wiki moved to "what else" as a separate incident; "700 of about 1,200"; five datasets opened; three
  unsourced quote cards cut or replaced; dates and figures corrected. STILL TO CHECK BY HAND BEFORE UPLOAD: WSJ for the
  two Wolf quotes, OpenAI's 26 Aug report (the `weak` chain), the 1 Oct Washington Post report (100+ organisations).
  All 87 lines voiced with George (`flow/takes/`, 10,613 characters), laid: 11:29. `render_flow.sh lf01_escape
  LF01_FLOW_v1 6` renders parts, joins, mixes (`mix_flow.py`) -> `lf01_escape/LF01_FLOW_v1.mp4` (+ `_phone`). The old
  kit.py film (`out/lf01_escape_1080p.mp4`, uploaded page copy) still has the UNCORRECTED script: do not upload it.
  Next: critic agent on LF01_FLOW_v1, fix, show the user; POST.md chapters and description need redoing for the new
  timings and corrected facts.
- **7 Oct, 02:05: LF01 SECOND CUT MADE** `lab/curvelf/lf01_escape/LF01_FLOW_v2.mp4` (1080p, 11:37, -14.1 LUFS, peak
  -1.3 dBFS; `_phone` is 720p). Critic on v1 (`CRITIC_FLOW_v1.md`: FIX THEN UPLOAD, no cuts, loudness fine) and what v2
  changed: labels sooner and inside the frame; long punch lines are crisp type (LONG_WORDS), short ones ASCII at one
  size; three weak visuals swapped in `script.py` (board_02, hours_06, open_07 now a 1,200 / 700 split); quotes type
  faster; bed holds through chapter names, haas-widened, 0.62; 11 s tail with a sign-off; corner readout is now
  "03 / 11  CHAPTER NAME" (the user said "u choose"; a first-time viewer read the camera readout as debug text).
  KNOWN IN v2, FIXED IN CODE FOR THE NEXT RENDER: chapter cards say "CHAPTER 01" for the second chapter while the
  corner says 02 / 11. v2 was checked by its maker on ten frames; a second critic was launched on it. Not for upload
  until: the three hand source checks in VERIFY.md section 6, POST.md redone, the user's go-ahead.
- **7 Oct, 02:20: USER APPROVED THE LOOK** ("looks really good i like it alot, continue"). The second critic on v2
  died on the session limit (no CRITIC_FLOW_v2.md): re-run it on v3. v3 = v2 plus the chapter-card numbering fix
  (`./render_flow.sh lf01_escape LF01_FLOW_v3 6`). Then POST.md, then LF02 and LF03 the same way (fact-check first).
- **7 Oct, 10:20: LF01 v3 MADE; LF02 VOICED AND RENDERING; LF03 CORRECTED, NOT VOICED.** LF01: `LF01_FLOW_v3.mp4`
  (chapter cards numbered right; critic running -> `CRITIC_FLOW_v3.md`). LF02: `lf02_price/VERIFY.md` (premise holds,
  43 claims, 1 wrong), 15 edits, 75 takes, `render_flow.sh lf02_price LF02_FLOW_v1 6`. LF03: `lf03_held/VERIFY.md`
  (premise holds, 53 claims, 1 wrong), 19 edits; before voicing, check the open and close chapters against Anthropic
  widening Mythos access on 6 Oct. `flow.py lay` now leaves an 11 s tail; the corner indicator turns over with the
  chapter card. Each film still needs: critic on the finished file, new-look thumbnails, POST.md, hand source checks.
- **7 Oct, 10:45: SHORTS MODE, SCHEDULE SHEET, YOUTUBE STATE.** `flow.py` has a 9:16 mode (`FLOW_VERT=1 ... short`):
  headline up top, captions above the app's buttons, end card to the full film. Sheet for the user to schedule by hand:
  `channel/the-curve/SCHEDULE_NEW_LOOK.md`. On YouTube the OLD uncorrected LF01 and two old Shorts are public; old LF02
  was set to private by the assistant in Studio (Chrome); a further Studio change was blocked by the permission system
  and is the user's to make (ids and actions in the sheet). The assistant cannot upload (Zapier limit, no vidIQ channel,
  10 MB Chrome cap). LF03: corrected, voicing next.
- **GitHub push has been failing since about 01:55** ("Failed to connect to github.com port 443"); commits are local
  on the Mac (`git status -sb` shows "ahead N"). Retry `git push origin claude/funny-newton-gd9w8v`.
- **Waiting on the user:** order NFC blanks + A6 holders; home town; a Stripe or SumUp account; which account sends
  messages; "Tandoor" or "Tandoori" on The Tamworth Tandoor's sign; Zapier reset date (billing page).

## 5 Oct, evening: SWITCHING ACCOUNTS (weekly limit). Other account: start here
- **Artifacts live on the old account and the other account can't open them.** Everything is rebuildable from this
  repo. Walk-in Reels: `python3 sales/reels/make_reels.py render --town Stone` (then `--town Newcastle-under-Lyme`,
  `--town Tamworth`, `--sample special`), `manifest`, `python3 sales/reels/page.py`, then publish
  `sales/reels/index.html` with `capabilities {"downloads": true}` and the files from `page.py --files <Town>`, in
  batches under 64 MB (52 Reels ≈ 200 MB, ~85 s each, run 2-3 at a time). Or the user shares the old page
  (https://claude.ai/artifact/LzxsswDEPP1441T5sUibSb) to the other account from its Share menu.
- **Saved for the switch (5 Oct, late):** the 29 finished videos still to upload are in `media/2026-10-05_youtube/`
  (the only copies; big ones split into `.partNN`, join with the command in `media/README.md`), each channel with an
  `UPLOAD_SHEET.md`. Scratchpad sources (TikTok queue generators, X research, fact sources, upload scripts) are in
  `lab/_saved_scratch/`. Delete `media/` in a commit before the PR is merged.
- **Waiting on the user (ask first thing):** (1) the Reels pack price (suggested £79/mo for 4); (2) which extra
  service to lead with, from `sales/OPTIONS.md` (Claude recommends #1, the photo shoot + delivery-app glow-up);
  (3) their home town; (4) Zapier upgrade + YouTube phone verification.
- **Phone playback:** the iPhone app loaded none of the page's own files (no posters, no video, Save failed), so every
  Reel and poster was also uploaded to the artifact's **asset store** (`capabilities {"downloads": true, "assets": {}}`;
  ids in `sales/reels/assets_LzxsswDEPP1441T5sUibSb.tsv`; `page.py` uses `/_blob/<id>`, which serves in every view).
  A rebuilt page on another artifact needs its own uploads: Artifact publish with `url`, `asset: true`, `file_paths`
  (25 per call), then write that artifact's tsv.
- **Connectors the other account needs** (same user accounts behind them): Zapier (YouTube connection ids below),
  Higgsfield (voice; TikTok publishing), Notion (QUIT HQ), GitHub.
- **Scheduled upload retry** `trig_019aN3CvKVUt2nuTjs94xCQu` ran at 5 Oct 21:20 UTC: Zapier still answers "reached its
  task limit for the current billing period", so nothing uploaded (29 left). Once the user upgrades Zapier, compare
  `channel/uploads.done.json` with `channel/uploads.json` and upload what's missing (about 10 a channel a day).
- **Next work, in order:** build the kit for whichever service the user picks; voice HTP 05 PayPal when Higgsfield
  renews (needs ~36 credits, had 26.72); verify Money Crimes 03 against primary sources (`lab/longform/saladoil/`),
  then voice; The Curve LF04.

## 5 Oct, afternoon: the plan to December, walk-in Reels, HTP drift
- **The honest plan** (now in Notion QUIT HQ, section "Plan to 31 December"): income is £27/mo (KDP). The quit rule
  (£2k/mo for 3 months + 3 months saved) can't be met by 31 Dec; December can be the first £2k month (about 20 shops on
  a £79/mo Reels pack + 1-2 website builds), so quit day is about March-April 2027. That needs ~30 shops walked a week at
  1 in 10; at 20 a week and 1 in 15 it slips to February. YouTube: £0 before 2027, runs on Claude's time. The user's
  hours go to walking. QUIT HQ's Ventures rows (walk-in, Kitchen Pass, YouTube) and four Action Plan rows were updated.
- **Walk-in Reels** (`sales/reels/make_reels.py`, page `sales/reels/page.py` -> `sales/reels/index.html`): an 8 s 9:16
  Reel per shop rated 5, built from its FSA record: a kitchen ticket on the pass rail under a heat lamp, the name at
  frame 0, a green "5" rubber stamp at 1.1 s, a pen circle, "find us" with a map pin, the service bell. Synthesised
  sound, no music, no AI food photos, our own stamp (never the FSA badge). `render [ids] [--town T]` then `manifest`;
  ~85 s a Reel alone. All 52 (Stone 16, Newcastle 19, Tamworth 17) plus a monthly-product sample are on the **Walk-in Reels** page
  https://claude.ai/artifact/LzxsswDEPP1441T5sUibSb
  (`downloads` capability; published in two halves under the 64 MB cap; source `sales/reels/index.html`). A new town: pull its council's FSA file into `sales/prospects_routed.json`, then
  `render --town <Town>`, `manifest`, `page.py --files <Town>` (publish in batches under 64 MB).
- **Not approved yet (ask, don't assume):** the Reels pack price (suggested £79/mo for 4 Reels), and the older offer
  ladder. The page shows the price as "not set yet". Still unknown: the user's home town ("Here").
- **How They Profit motion:** `ch2/kit.py` `DRIFT` gives every beat a 3.5% push and a side drift, and `ch2/ledger.py`
  lets the ruled ground breathe. EP05's first 120 s (estimated timeline): frozen 69% -> 12%, near-still 88% -> 60%; with the $100
  note's float and light sweep (`ep05/scenes.py` note()) frozen 9%, near-still 47%. More in-beat motion is per scene. `DRIFT["push"] = 0` restores the old behaviour for a re-render of EP01-04.
- **Gotchas:** a job list fed to `while read` loses its last line without a trailing newline: 5 of 16 Reels silently
  never rendered. Count the outputs against the list. The FSA register spells towns its own way ("Newcastle Under
  Lyme"), leads some addresses with the business name and adds localities ("Kettlebrook"): `split_address` handles these
  now, but look at a contact sheet of every new town's "find us" frame (t=4.3 s) before publishing.

## 4 Oct, evening: 30 of 59 uploads live and scheduled (Route Z works)
- **Zapier YouTube connections** (one per channel; pass as `connection_id`): The Curve `02f9e902-69d2-8a12-af4b-b4f4cd146eeb`
  (@thecurve.explained), Money Crimes `02ce9a67-dbe7-8998-8da5-26da5fc35e26` (@moneycrimesfiles), How They Profit
  `02d0de21-a222-85ea-aea9-5b0920dd34b0` (@howtheyprofithq). `02587cb2-...` is the personal account with no channel: ignore.
- **Done:** indices 0-21, 24, 25, 27, 28, 30, 31, 34, 38 of `channel/uploads.json` (ids in `channel/uploads.done.json`), all
  private with `publishAt`, synthetic-media flag on, not for kids. Channel descriptions, keywords, language and country set
  via `channels.update`.
- **Daily cap:** each channel refuses new uploads after about 10 a day (`uploadLimitExceeded`) until it is phone-verified.
  **Left (29):** 22, 23, 26, 29, 32, 33, 35-37, 39-58 (earliest publishes 11 Oct). Re-run on 5 Oct after ~21:10 UTC: open
  sessions with the Zapier raw request (body from `zp.py`-style `yu.body_for(yu.entry_from(plan[i], "channel"))`), then
  `youtube_upload.py put SESSION FILE --manifest channel/uploads.json`. How They Profit has 14 left, so it needs two days
  unless verified.
- **Thumbnails** fail with "doesn't have permissions to upload and set custom video thumbnails" until each channel is
  verified by phone (www.youtube.com/verify). Then: `youtube_upload.py zapier-thumb VIDEO_ID thumb.jpg`, open it through
  Zapier, `put` the image.
- **TikTok plan (4 Oct, late):** the user is reusing old TikTok accounts: archivepearls → How They Profit, issolaurent →
  The Curve, a new account for Money Crimes (`bernardinio555+crimes@gmail.com`, Gmail plus-alias). **Never touch
  thegoldenplate (it's for the user's food project) or passdaboof2.** Connect for posting via Higgsfield's TikTok tools
  once renamed.
- **TikTok is connected in Higgsfield** (connectors: tiktok-howtheyprofit, tiktok-thecurve, tiktok-moneycrimes), but every
  post needs the user to submit TikTok's form in a widget-capable Claude client, and the API can't schedule. So TikTok
  runs from the **TikTok Queue page** https://claude.ai/artifact/2wDDNCdD65rqGrmLyQCTSW (27 Shorts for 5-14 Oct, 18:00 UK,
  compressed under 15 MB each): the user schedules them weekly in TikTok Studio (web). Make the next page for 15-24 Oct.
- **5 Oct, 00:00 UTC, blockers and progress:**
  - **Zapier hit its monthly task limit.** Every YouTube call fails ("reached its task limit for the current billing
    period"), so the remaining 29 uploads (22, 23, 26, 29, 32, 33, 35-37, 39-58) and the banners are blocked until the
    user upgrades Zapier or the period resets. vidIQ can't upload to YouTube (its upload tool only feeds its own editor);
    it can set thumbnails (5 credits each) once channels are connected and verified, and can publish Instagram Reels.
    Channel check before the limit: The Curve has name, avatar and banner; Money Crimes and How They Profit have avatars
    but still the old names (MoneyCrimesFiles, HowTheyProfitHQ) and no banners; all three `longUploadsStatus: eligible`
    (not yet phone-verified).
  - **TikTok Queue page 2** (15-24 Oct, 21 Shorts): https://claude.ai/artifact/XH21v2cnsnRv9oVCUoB1rM
  - **Next films, briefed** (`channel/NEXT_FILMS.md`): The Curve LF04 "The Pause" (script v0 + FACTS in
    `lab/curvelf/lf04_pause`; OpenAI's second training pause, the first being LF01's Hugging Face breach: a trilogy),
    Money Crimes 03 "The Salad Oil Swindle" (`lab/longform/saladoil/FACTS.md`), HTP 06 Visa (`lab/ch2/ep06/FACTS.md`).
  - **Audio fix**: finals peaked at -0.2 dBTP. `ch2/endcard.py` now encodes AAC once; `longform/doc.py` and
    `shorts/reel.py` master at -1.5 dBTP. Applies to new renders only (the scheduled uploads keep the old masters).
  - **HTP film 05 (PayPal) v0**: `lab/ch2/ep05/script.py` (new "follow one $100" structure per CRAFT §1) and
    `FACTS.md` (FY2025 10-K/8-K; fee rates checked 5 Oct; Venmo revenue as reported), `POST.md` (titles, description,
    5 Shorts with different shapes), `scenes.py` (the $100 note as the persistent object; the $1.85 sliver grows into
    the next bar) and `film.py` (CLIPS, MUSIC). Stills checked on an estimated timeline (`build_est`, ~6:03 at 2.1 w/s;
    `EP_BUILD=build_est python3 film.py still ...`). Next: voice (~36 Higgsfield credits; about 27 left), render,
    film-critic, endcard (now single AAC encode).
- **Research → upgrades (4 Oct, night):** the user's X account is new, so `lab/research/x_notes.md` is a public-X sweep
  (about 25 searches; full X Articles read through `api.fxtwitter.com/<user>/status/<id>`, which X itself hides behind
  a login). Distilled into **`CRAFT.md`** (house rules every session reads; CLAUDE.md points to it) and the
  **`film-critic` skill** (`.claude/skills/film-critic`: motion_report.py + loudness + sheets, then a fresh critic
  subagent, then a verifying critic). First findings: HTP Amazon is near-still 70% of the time; masters peak at -0.2 dBTP
  (target -1). The biggest strategic risk found: YouTube's "inauthentic content" demonetisations of templated AI
  channels, so vary HTP's fixed seven-chapter structure from film 05. `.claude/skills/business-motion-film` is the
  vendored motion-video-kit (MIT). `lab/research/motion_playbook.md` is the public-web pass.
- **Only the user can:** rename "MoneyCrimesFiles" to Money Crimes and "HowTheyProfitHQ" to How They Profit (the API
  ignores titles), profile pictures, phone verification.

## 4 Oct, afternoon: "we go full in with yt" (the user, at work: do everything possible, list what only they can do)
- **Go-live page** (the user's checklist, on their phone): https://claude.ai/artifact/SGW5GGULhWhdNZxaBtMNSm. Four steps
  only the user can do: make the three channels (youtube.com/channel_switcher), dress them (art and copy in the page),
  verify by phone, connect YouTube in Zapier (one connection per channel). Then Claude uploads everything.
- **Nothing was connected on 4 Oct:** vidIQ is signed in (to a different Google account from the user's Claude email)
  with no channel; Zapier had no YouTube connection (its YouTube actions are now enabled: find_video, get_report,
  add_video_to_playlist, upload_video, upload_video_thumbnail, _zap_raw_request); Higgsfield has no TikTok account.
- **Upload plan:** `channel/uploads.json` from `lab/tools/plan_uploads.py` (SLOTS = the 5-24 Oct running order: 11 films,
  48 Shorts; every slot checked against YouTube's limits; the season descriptions are cut to fit 5,000 bytes and no
  longer claim the single episodes are on the channel). Route: `UPLOADING.md`, "Route Z" (Zapier opens a resumable
  session, `youtube_upload.py put` streams the file from here). GitHub releases are refused in this session type, so
  public hosting of the 247 MB films isn't available; googleapis.com is reachable for the direct stream.
- **How They Profit films 02 and 03** voiced with Sterling (about 36 credits each): McDonald's 8:01 (page
  https://claude.ai/artifact/XBJfqmdXyYQvA9syVe35YZ, Shorts https://claude.ai/artifact/PwxaSffr73rhXBtRf7qdNH), Costco
  7:20 (page https://claude.ai/artifact/CRxtMNF8YCwFzcrqz7rWQQ, Shorts https://claude.ai/artifact/PktR2P3q7bUJ9kenGWn4cX). **Film 04, The Cloud Behind the Cart** (Amazon: AWS 18%
  of 2025 sales, 57% of operating profit; sourced from the FY2025 8-K) written, storyboarded (`kit.server`, `kit.parcel`),
  voiced and rendered the same day (7:15, page https://claude.ai/artifact/Ci2aP8aP3TuBbnNuN1TLva, Shorts https://claude.ai/artifact/HbiwF8JbBuYzAcKVowLLEV), for Tue 20 Oct. Next HTP topics: the trend board (Canada's tariff, PayPal). `engine/voice_hf.py` now squeezes any quiet
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
