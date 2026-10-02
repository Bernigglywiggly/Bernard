# Studio map: where everything is (start here)

Five money channels plus a gameplay channel, made by code in `lab/`. Code stays where it runs; this map and the channel
folders point at it. The DeepSeek-V3 files at the repo root are unrelated. Latest session notes: `HANDOFF.md`.

## Channels (each has `channel/<name>/README.md`)
| # | Channel | Status (2 Oct) | Plan and notes | Code |
|---|---|---|---|---|
| 1 | **The Curve**: AI explained | EP04-EP12, Seasons One and Two and the trailer finished and on upload pages; EP13-EP14 scripted (need voice) | `channel/the-curve/` | `lab/ep04`-`lab/ep14`, `lab/season1`, `lab/trailer`, `lab/engine` |
| 2 | **The Margin**: how companies make money | 3 films scripted and storyboarded; need voice; needs a new name | `channel/channel2/` | `lab/ch2` |
| 3 | **Money crimes**: scams, frauds, heists | Short 01 (Victor Lustig, the Eiffel Tower) made with AI video | `channel/money-crimes/` | `lab/shorts/lustig`, `lab/shorts/reel.py` |
| 4 | **Maps & power**: geopolitics in 3D | Planned | `channel/maps-and-power/` | - |
| 5 | **What if**: science and scale in 3D | Planned | `channel/what-if/` | - |
| - | **Gameplay rants** (PS5, the user's own voice) | Planned; setup notes | `channel/gameplay/` | - |
The plan, the rules and the money: `channel/CHANNELS.md`. Daily trend ideas: `channel/trends/` (the Trend desk routine).

## Upload pages (claude.ai, private to the user)
- EP05, EP08, EP04: https://claude.ai/artifact/V2Tz5smkY5w1uzroS85YzB
- EP06, EP07: https://claude.ai/artifact/PvzxoDzvJVvKdoXTD6S6pU
- EP09-EP12: https://claude.ai/artifact/XuGVGPichLJ6oR9TnUS1sq
- Season One: https://claude.ai/artifact/7aPVnXn8UW6LgBUmki6BqV
- Season Two: https://claude.ai/artifact/8wNVR2gvWLkZUdvNnGiR44
- AI shorts (Money crimes 01, What if 01): https://claude.ai/artifact/J5CqJtyMALxMBsxTGb6un6

## Engines and tools
| What | Where |
|---|---|
| 16:9 film engine (motion graphics, captions, mix, shorts) | `lab/engine` (`film.py` commands: voice, lines, still, parts, join, sound, remux, audition, master, shorts) |
| 9:16 AI-short engine (AI clips + kinetic captions + stamps + score) | `lab/shorts/reel.py`, one `make.py` per short |
| 16:9 long-form documentary engine (AI stills/clips, archive prints, maps, documents, counters, chapter cards, parallel render) | `lab/longform/doc.py`, one folder per film (`lustig/`: script, vo, music, film, thumb) |
| Public-domain archive search and download (Wikimedia Commons, credits recorded) | `lab/longform/tools/commons.py` |
| Music beds (all synthesised, no samples) | `lab/music/beds.py`: house, garage, caper, arena, deep_field, ...; previews `lab/out/music/new` |
| Voice | ElevenLabs line cache `lab/voice/cache/eleven` + `lab/tools/eleven_tts.py`, `lab/engine/voice.py`; auditions `lab/tools/voice_audition.py`; Higgsfield Seed Audio for the shorts |
| Sound effects | `lab/out/sfx` (synthesised), `lab/sfx` |
| Upload pages | `lab/pack/build.py` (new, films1, films2, season1, season2) |
| Thumbnails and channel art | `lab/engine/thumb.py`, `lab/engine/brand.py`, `lab/ch2/thumbs.py`, `lab/ch2/brand.py` |
| Checks | `lab/music/analyse.py` (tonal balance, clicks), `lab/qa_audio.py` |

## Research, plans, other work
- `channel/CHANNELS.md` (five channels, YouTube rules, RPMs), `channel/MONEY.md`, `channel/BACKLOG.md`
- `lab/research`, `lab/format` (episode bank), `lab/inspo` (reference videos)
- `sales/`: the walk-in sales research (NFC review stands, Business Profile tune-ups, takeaway websites)

## Archive (earlier experiments, kept for reference)
`a01_v5`, `a01_v6`, `deliver`, `lab/pilot`, `lab/ep01`-`lab/ep03`, `lab/ep03s`, `lab/stickman`, `lab/visual`, `lab/plan`,
`lab/shorts2`, `lab/voice` (the local Kokoro voice lab: never in anything published).
