# START HERE: state at Thu 8 Oct 2026, 21:45 UK (written for a Claude with zero history)

This block is the truth. Everything below it in this file is older history, kept for detail only.
Repo: `~/Bernard`, branch `claude/funny-newton-gd9w8v` ONLY (push with: `git push -q origin claude/funny-newton-gd9w8v 2>/dev/null || git -c http.curloptResolve=github.com:443:140.82.121.4 push -q origin claude/funny-newton-gd9w8v`). Python: `~/youtube/.venv/bin/python`. Videos, voice takes and pictures are on THIS Mac only (not in git): a cloud session cannot render or upload them.

## 1. What is running right now (background agents in the session that wrote this; they die with it)
| Job | Output folder | Done when |
|---|---|---|
| Pilot channel 4: US economy / cost-of-living explainer | `~/Bernard/lab/pilots/economy/` | CHANNEL.md, script.py, IMAGES.md, VERIFY.md, POST.md exist |
| Pilot channel 5: megaprojects / engineering | `~/Bernard/lab/pilots/megaprojects/` | same, plus `src/photo/*.jpg` and `src/photo/CREDITS.md` |
| Spanish version of film 2 | `~/Bernard/lab/curvelf/lf02_price_es/` | script.py (with `LANG = "es"`) and POST.md exist |
If a folder lacks its script.py, that agent died: re-launch it (the briefs are described in section 6).

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
- How They Profit 06 Visa film (`lab/ch2/ep06/HTP06_MASTER_v7.mp4`, sheet `lab/ch2/ep06/POST.md`): finished, never uploaded; user never answered "upload now or hold for late-October figures".
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
1. Read the three agents' output (section 1). Spanish: `flow.py lf02_price_es lines`, voice every line (George, model `eleven_multilingual_v2`, Spanish), `lay`, `./render_flow.sh lf02_price_es LF02_ES_v1 6` (garage bed, no FLOW_MUSIC), critic by a Spanish-reading agent. `lf02_price_es/src` is a symlink to the English film's pictures.
2. Pilots: generate each IMAGES.md picture (black background, monochrome, no text) with an image tool that is NOT Higgsfield, put them in `<pilot>/src/ai/`, voice, render, critic. The pilot folders are film folders for flow.py once `src/` exists (flow.py takes a path relative to `lab/curvelf`, so move or symlink them there).
3. 9 Oct evening: upload short_escape; get the user's word on LF03 and upload it.
4. New channels need the user: create each channel, phone-verify, connect it in Zapier. Ask him for channel names from each pilot's CHANNEL.md.
5. Still unmade: Shorts for Ponzi and for the Visa film; TikTok/Reels versions wait on Metricool connections.

## 7. Standing rules (never break)
- Never touch TikTok `thegoldenplate` or `passdaboof2`. Pinterest DTwork7: read-only. Nothing is sent to any shop without his approval. Never copy API keys into a handoff. No model names in commits or PRs. Delete `media/` in a commit before the PR is merged.
- Reply format: tables first, bare `- [ ]` checklists, short lines; every line that needs him starts with 5 emojis and one bold ask.
- A hook asks for a security scan after each commit: not applicable (no running app); skip and say so.
- Save this handoff to ALL of: `~/RESUME_HERE_2026-10-05.md`, `~/youtube/CURRENT_STATE.md`, `~/CLAUDE_HANDOFF_BUNDLE/`, `~/Downloads/CLAUDE_HANDOFF/`, `~/Downloads/GoldenPlate_Vault/` (00_RESUME_HERE.md, 00_START_HERE.md, 00_CURRENT_STATE.md, CURRENT_STATE.md), and `~/Bernard/HANDOFF.md` top.

---

---
# Earlier handoff (older; the block above wins where they disagree)

