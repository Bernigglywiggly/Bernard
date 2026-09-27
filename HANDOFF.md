# Handoff: the AI explainer channel + walk-in sales (read this first in a new session)

This repo is a scratch space (the DeepSeek-V3 files are unrelated). The user works across **two Claude accounts**
(a Mac desktop session and cloud sessions). They share **nothing but this GitHub repo**: artifacts, Notion and
databases on one account can't be read from the other. Push anything the other side needs here.
Updated 26 Sep 2026 (late), cloud session on branch `claude/lucid-archimedes-77tqpt` (built on `claude/funny-newton-gd9w8v`).

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

## Newest: the Six Floors format and EP01 (after the @pollar.news inspo)
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
