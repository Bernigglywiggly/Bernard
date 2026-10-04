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
The plan, the rules and the money: `channel/CHANNELS.md`. Daily trend ideas: `channel/trends/` (the Trend desk routine publishes a private page each morning; this session files it as `<date>.md` and updates `BOARD.md`).

## Upload pages (claude.ai, private to the user)
- The Curve LF01 The AI That Escaped: https://claude.ai/artifact/NC5QdLVBaBEMemcsaHLPYM (shorts: https://claude.ai/artifact/SXhZZiVogib4tEhsbR7tNs)
- The Curve LF02 The Price of Thinking: https://claude.ai/artifact/JgAJPt8FQ45dJivdXQy7f9 (shorts: https://claude.ai/artifact/4LqUZUotHs9EEvvuj1gr7J)
- The Curve LF03 Too Dangerous to Release: https://claude.ai/artifact/8sMGypbJ7BnKu8Zvkxqikr (shorts: https://claude.ai/artifact/ErxxqE9BmuSbxpFZgJbzBy)
- **YouTube go-live page** (set-up steps, channel kits, the 5-18 Oct running order): https://claude.ai/artifact/SGW5GGULhWhdNZxaBtMNSm
- How They Profit film 01 Banks With Wings (7:40): https://claude.ai/artifact/FDHDmXNLLTdKuFpbVmMrbp (5 Shorts: https://claude.ai/artifact/NjP42S3wuphcMSXHhi2BqQ)
- How They Profit film 02 The Landlord in the Golden Arches (8:01): https://claude.ai/artifact/XBJfqmdXyYQvA9syVe35YZ (5 Shorts: https://claude.ai/artifact/PwxaSffr73rhXBtRf7qdNH)
- How They Profit film 03 The $65 Membership (7:20): https://claude.ai/artifact/CRxtMNF8YCwFzcrqz7rWQQ (5 Shorts: https://claude.ai/artifact/PktR2P3q7bUJ9kenGWn4cX)
- How They Profit film 04 The Cloud Behind the Cart (Amazon, 7:15): https://claude.ai/artifact/Ci2aP8aP3TuBbnNuN1TLva
- Money Crimes film 02 The Original Ponzi Scheme (13:27): https://claude.ai/artifact/XaV9wVSnvrJzPA2HEV7Ngj (7 Shorts: https://claude.ai/artifact/3dQC4krr7X2cssm2o6CcJK)
- Money Crimes film 01 Shorts (now 6: Capone, escape, money box, bribe, death certificate, commandments): https://claude.ai/artifact/2A19evbUw3Lsz8Kftyj2d1
- EP05, EP08, EP04: https://claude.ai/artifact/V2Tz5smkY5w1uzroS85YzB
- EP06, EP07: https://claude.ai/artifact/PvzxoDzvJVvKdoXTD6S6pU
- EP09-EP12: https://claude.ai/artifact/XuGVGPichLJ6oR9TnUS1sq
- Season One: https://claude.ai/artifact/7aPVnXn8UW6LgBUmki6BqV
- Season Two: https://claude.ai/artifact/8wNVR2gvWLkZUdvNnGiR44
- AI shorts (Money crimes 01, What if 01): https://claude.ai/artifact/J5CqJtyMALxMBsxTGb6un6
- **Money crimes long-form 01, The Man Who Sold the Eiffel Tower (14:56):** https://claude.ai/artifact/B4DiPy9qxvVKaZgucpYK3Q
- Shorts cut from it (Capone, the escape, the money box): https://claude.ai/artifact/2A19evbUw3Lsz8Kftyj2d1

## Engines and tools
| What | Where |
|---|---|
| 16:9 film engine (motion graphics, captions, mix, shorts) | `lab/engine` (`film.py` commands: voice, lines, still, parts, join, sound, remux, audition, master, shorts) |
| 9:16 AI-short engine (AI clips + kinetic captions + stamps + score) | `lab/shorts/reel.py`, one `make.py` per short |
| 16:9 long-form documentary engine (AI stills/clips, archive prints, maps, documents, counters, chapter cards, parallel render) | `lab/longform/doc.py`, one folder per film (`lustig/`: script, vo, music, film, thumb) |
| Public-domain archive search and download (Wikimedia Commons, credits recorded) | `lab/longform/tools/commons.py` |
| The Curve long-form (3 Oct) | `lab/curvelf/kit.py`: script of beats -> the character look at 11-14 min; `assets.py` pictures, `thumb.py` thumbnails |
| Motion graphics in code (3 Oct): Remotion 4, React, Studio preview, agent instructions | `lab/motion` (`npm run dev`, `npm run new -- Name`, `npm run render:sample`; read `lab/motion/AGENTS.md`) |
| Music beds (all synthesised, no samples) | `lab/music/beds.py`: house, garage, caper, arena, deep_field, ...; previews `lab/out/music/new` |
| Jazz for true-story films (3 Oct) | `lab/music/jazz/library.py`: Kevin MacLeod, CC BY 4.0; `section()` cuts a cue, `credit_line()` for descriptions |
| Voice | ElevenLabs line cache `lab/voice/cache/eleven` + `lab/tools/eleven_tts.py`, `lab/engine/voice.py`; auditions `lab/tools/voice_audition.py`; Higgsfield Seed Audio for the shorts |
| Sound effects | `lab/out/sfx` (synthesised), `lab/sfx` |
| Automation and scale plan (3 Oct): limits, route to 50 channels, every stage's tool and status | `AUTOMATION.md`; uploading: `UPLOADING.md`, `lab/tools/youtube_upload.py` |
| Upload pages | `lab/pack/build.py` (new, films1, films2, season1, season2, shorts, lustig, lustig_shorts) |
| Thumbnails and channel art | `lab/engine/thumb.py`, `lab/engine/brand.py`, `lab/ch2/thumbs.py`, `lab/ch2/brand.py` |
| Checks | `lab/music/analyse.py` (tonal balance, clicks), `lab/qa_audio.py` |

## Research, plans, other work
- `channel/CHANNELS.md` (five channels, YouTube rules, RPMs), `channel/MONEY.md`, `channel/BACKLOG.md`
- `lab/research`, `lab/format` (episode bank), `lab/inspo` (reference videos)
- `sales/`: the walk-in sales research (NFC review stands, Business Profile tune-ups, takeaway websites)

## Archive (earlier experiments, kept for reference)
`a01_v5`, `a01_v6`, `deliver`, `lab/pilot`, `lab/ep01`-`lab/ep03`, `lab/ep03s`, `lab/stickman`, `lab/visual`, `lab/plan`,
`lab/shorts2`, `lab/voice` (the local Kokoro voice lab: never in anything published).
