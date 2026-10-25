# START HERE: second Claude account (written 25 Oct 2026, 05:10 UK)

You are a Claude Code session on a SECOND account, working the same projects as the first. Memory is NOT shared
between accounts. The shared memory is the set of FILES below. Read them in this order before doing anything:

1. `~/.claude/CLAUDE.md`: the owner's standing rules (goal, personal notes, formatting, agents, handoff, emoji call-to-action). It outranks everything.
2. `~/Bernard/HANDOFF.md`: top block = the current state. Everything below it is history.
3. `~/Bernard/CLAUDE.md`, `~/Bernard/CRAFT.md` (house rules for every video), `~/Bernard/lab/motion/AGENTS.md` (Remotion).
4. `~/youtube/DECISIONS.md` (tail): decisions he has made.

## The mission (short version; details in ~/.claude/CLAUDE.md)
- **Goal:** money, fastest route. **£2,000/month digital first**, then £4,000. Judge every task by revenue per hour of his time. Redirect when something is low value. Say the uncomfortable version.
- **Main engine now:** the YouTube channel **The Curve** (@thecurve.explained, channel UCI7lgtrs_En_L9MmPnJbwEg). Format locked 19 Oct: "the clip everyone is sharing, explained". That means the real viral clip, our own Blender 3D and Remotion diagrams. ASCII style is retired.
- **His direction (23 Oct):** "usage credits on, use the new video style with real clips, blender, highest production quality etc for long and short form... stay up to date with trending news/events... mostly high rpm and viral topics".
- **What works (analytics):** Short 1 (Roadster hangs upside down) got 15.4k views and 50% stayed past the first second. Follow-ups on the same event got ~1.1k. Lesson: open on a visual-mystery frame and chase NEW viral moments within ~48 h.

## How he wants to be talked to (locked)
- Bare checklist (`- [ ] Thing → action`), short lines, visuals and tables first, bold the action.
- Every line that needs HIS input or hands starts with **5 random emojis**. One burst per ask.
- **Do not lecture** on personal matters (see ~/.claude/CLAUDE.md "PERSONAL"). Treat it as engineering.
- Use agents: an independent critic on the actual output before anything ships, and an alignment check at big forks.

## Hard rules
- Repo `~/Bernard`, branch **`claude/funny-newton-gd9w8v` only**. Commit and push after each piece. **No model names in commit messages.**
- **Uploads, posts and publishing need his explicit "yes" per item.** Never change visibility in YouTube Studio through a browser. A long film must never exist twice on the channel.
- Never touch TikTok `thegoldenplate` / `passdaboof2`. Pinterest DTwork7, Chrome, Telegram, Discord and Skool are read-only. Never copy API keys into files or chat (WaveSpeed key lives in ~/Bernard/ofm/.env).
- His email is for identification only; never put it in web requests.
- Run the film-critic (`~/Bernard/.claude/skills/film-critic/`) before any upload.
- Save the handoff BEFORE limits hit, to all locations: HANDOFF.md, ~/RESUME_HERE_2026-10-05.md, ~/youtube/CURRENT_STATE.md, ~/CLAUDE_HANDOFF_BUNDLE/HANDOFF.md, ~/Downloads/CLAUDE_HANDOFF/HANDOFF.md, and ~/Downloads/GoldenPlate_Vault/{00_RESUME_HERE,00_START_HERE,00_CURRENT_STATE,CURRENT_STATE}.md. Keep them identical.

## Five accounts, one repo: read `TEAM.md` next (from 25 Oct 17:50)
- **`TEAM.md` is the lane map, file ownership, queue and sync rules.** A = Curve Shorts · B = Curve long-form + strategy · C = trend desk, facts, QA critic · D = money now (off YouTube) · E = channels 2 and 3.
- Split the work by area, as TEAM.md says, unless he says otherwise.
- Before starting, `git pull`. Commit only your own files (`git add <paths>`, never `git add -A`). Push often.
- Write what you are doing at the top of HANDOFF.md ("ACCOUNT B working on: ...") so the other session sees it.

## State at 05:10 Sun 25 Oct (also in HANDOFF.md)
| Item | State | Next |
|---|---|---|
| Shorts 4 (Unitree) + 5 (Tesla Q3) | FINAL, `lab/curve_v2/shorts/out/SHORT4_v3.mp4`, `SHORT5_v3.mp4`; manifest `channel/uploads_curve.json` | **Waiting for his "go"** |
| Short 7 Microduck | v1 rendered; critic round 1 = ONE MORE PASS (`shorts/out/critic_s7/round1.md`). v2: new script + voice (`lab/motion/public/shorts/s7_vo.mp3`), new composition `CurveV2Short7.tsx`, real clips `s7_hook2/s7_end/s7_split2/s7_slowmo.mp4` done. Blender v2 frames DONE in `lab/curve_v2/shorts/blender/out_s7v2_{wrong,tripod,crowd}` | Encode those frames to `lab/motion/public/shorts/s7_{wrong,tripod,crowd}.mp4` (30 fps, x264 crf 15), regenerate `s7Tracks.ts` from `out_s7v2_*/{tripod,wrong}.json`, render, master, measure, critic round 2, then ask him |
| Roadster film | v1 `lab/curve_v2/film_roadster/out/FILM_ROADSTER_v1.mp4`; critic round 1 = ONE MORE PASS (`film_roadster/out/critic/round1.md`: Musk misquote at 1:30, "road legal" wrongly credited to Tesla at 3:38, "-43%" needs a GAAP label, unsourced Cybercab/Semi rows, an EvidenceStamp component, empty frames, a new opening, S9 and the end card). A builder agent died mid-way: `script.py` has uncommitted edits (lint clean), and the changed lines were not voiced yet | Finish these fixes (likely Account B), render v2, critic round 2 |
| Next Short | Radar `lab/research/RADAR_2026-10-25.md`: #1 iPhone Duo durability (JerryRigEverything 7M views in a day; use Apple's own film), #2 Typhoon Champi (today only) | Facts file `lab/research/IPHONE_DUO_FACTS.md` (agent died, may be partial), then script, voice, Blender, Short |
| His hands | Avatar upload (`channel/the-curve/brand/v2/avatar.png`, YouTube Studio → Customization → Branding); 38 shop messages (`sales/reels/send_sheet.html`) | |

## Tools that work on this Mac
- Python `~/youtube/.venv/bin/python`. MJCF / mujoco work: `uv run --python 3.12 --with mujoco ...` (Homebrew python3.15 has a broken expat).
- Remotion: `cd ~/Bernard/lab/motion; npx remotion render <Id> <out.mp4>`. Captions: `scripts/transcribe.mjs` + `scripts/captions_ts.py --script <short.py>`. Voice trim: `scripts/tighten_vo.py`.
- Voice: ElevenLabs MCP, voice Chris `iP95p4xoKVk53GoZ742B`, model eleven_v4, stability 0.5, similarity 0.75, style 0.3, speed 1.08 for Shorts (1.02 for the film), mp3_44100_192.
- RIFE: `~/tools/rife-ncnn-vulkan-20221029-macos/rife-ncnn-vulkan -i in -o out -m <dir>/rife-v4.6 -n N -f %04d.png`.
- Blender 5.2: `blender -b -P script.py -- args`. BMesh element refs go stale when geometry is added, so track index ranges; Geometry Nodes Random Value outputs by name ("Value").
- YouTube upload and analytics go through Zapier (YouTubeV4CLIAPI `_zap_raw_request`, connection 02f9e902-69d2-8a12-af4b-b4f4cd146eeb), plus `lab/tools/youtube_upload.py`. The method is in HANDOFF.md. The Zapier connection lives on account A's claude.ai, so account B may need to connect its own Zapier.
- Loudness master: `-af "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:makeup=3,loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 48000`.
