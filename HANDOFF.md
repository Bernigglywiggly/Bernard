# Handoff: the AI explainer channel (read this first in a new session)

This repo is a scratch space (the DeepSeek-V3 files are unrelated). Work lives on branch
`claude/funny-newton-gd9w8v`, draft PR bernigglywiggly/bernard#1. Updated 26 Sep 2026.

## Links
- **Review page (current):** https://claude.ai/artifact/UcDevRSPUUxQznXKfMLAvL. The user's picks are in its
  database, collection `picks` (read with ArtifactData). Page source: `a01_v6/page/index.html`; its media
  (video, poster, voice clips, board thumbnails) are already published in the artifact, so republish with
  `url` set and only the changed files.
- Old v5 page: https://claude.ai/artifact/QC6pJenfB7yJZk2WD9x3Zb (source: `a01_v5/page/index.html`).
- Notion "QUIT HQ" is the user's project hub.

## Current state
**v6.2** (page Version 3): the 55.5 s hook, all dark, layered sound, George. The full-quality render was sent
to the user as `A01_v6_2_mockup.mp4`; rebuild it from `a01_v6/` as below. Waiting on their reaction
and a look pick (check the page's `picks`).

## What's where
| Path | What |
|---|---|
| `a01_v6/` | **Current pipeline**, "Chrome & Marl", calm and dark. `mograph.py` (skia vector motion graphics → silent mp4 + `events.json`), `sfx6.py` (event-driven sound design + mix), `PLAYBOOK.md` (rules), `PROMPTS.md` (GPT prompts), `SCRIPT.md` (hook narration, voice IDs, timings), `fonts/`, `voices/` (six takes of the hook), `page/` |
| `a01_v5/` | Superseded Blender/Eevee pipeline (the user found it too energetic). Kept for reference. |
| `channel/BACKLOG.md` | A02–A06 with sources. Order: A02 → A04 → A03 → A06 → A05. |
| `channel/MONEY.md` | Products (infinity table, display mirror), affiliates, Patreon, merch. |
| `channel/board_refs.json` | The CDE Pinterest refs and which ones the hook uses. |

## What the user wants (decisions so far)
- The calm personality of the first full 8-min A01: no humour. Relatable, everyday perspectives so
  non-AI people get it ("+14" for a student, gamer, business owner, "your time is money"). Always the
  benefit to the viewer: use cases, making money, current resources, what's coming. Hopeful endings.
- Visually appealing, satisfying and clean, never chaotic. The camera barely moves; detailed motion
  graphics do the work: line work (Tron: Legacy formations), typography, ASCII, Pinterest-editorial cards,
  smooth morphs. The push through the "0" is a favourite.
- Palette: chrome + marl, turquoise accent, emerald only for gains. **Dark backgrounds, not white**
  (graphite for forming, slate with a dot grid for explaining, dark glass cards).
- Voice: **George** (picked on the page). Sound: **"more layered"** (picked; done in v6.2: every sound
  placed where it happens, one shared room, swells, felt piano, a bed that ducks under the voice).
- The CDE board is woven in (grid, HUD callouts, ridgeline pins, halftone icons, isometric stack,
  particle ring, ring tunnel). Maps are saved for A02; glass hands and gradients were left out.

## Rebuild the hook (about 3 min on 4 CPUs)
```bash
pip install skia-python numpy scipy          # plus ffmpeg
cd a01_v6 && export A01V6_BUILD=build        # fonts load from ./fonts
python3 mograph.py                           # build/mockup_silent.mp4 + build/events.json
python3 sfx6.py voices/george.mp3            # build/mockup_mix.wav at -14 LUFS
ffmpeg -y -i build/mockup_silent.mp4 -i build/mockup_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest build/A01_v6_mockup.mp4
python3 mograph.py --still 20                # a single frame, for checking
```
skia pixels are BGRA: keep `-pix_fmt bgra` on the raw pipe, or the colours shift.

## Next steps
1. Build the full 8-minute A01 in this style with George: write the script (`PROMPTS.md` #3 and the
   perspective writer #2), generate the voice through vidIQ (voice ID in `SCRIPT.md`), and time the scenes to
   its sentence starts.
2. Check the 52.3 → 66.4 (+14.1) coding-test scores against the source before publishing.
3. Then A02 (war prep) from `channel/BACKLOG.md`.

## Rules
- The Pinterest account is personal: read-only references, never post, modify or save anything there.
- Don't clone or imitate real people's voices; use described archetypes (`PROMPTS.md` #4).
- No model names in commits or PRs. Push only to this branch.
- The user wants short, concise replies.
- Tools: vidIQ credits are limited (21 were left until 5 Oct, before the six voice takes). Higgsfield is usable from Thursday.
  If GPT (Codex) returns 401: `unset OPENAI_API_KEY; codex logout; codex login` (with ChatGPT, or a new key).
