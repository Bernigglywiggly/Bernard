# Handoff: the AI explainer channel + walk-in sales (read this first in a new session)

This repo is a scratch space (the DeepSeek-V3 files are unrelated). The user works across **two Claude accounts**
(a Mac desktop session and cloud sessions). They share **nothing but this GitHub repo**: artifacts, Notion and
databases on one account can't be read from the other. Push anything the other side needs here.
Updated 28 Sep 2026 (afternoon), cloud session on branch `claude/lucid-archimedes-77tqpt` (built on `claude/funny-newton-gd9w8v`).

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

## Newest (29 Sep, night): George at his own pace, and Deep Field
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
