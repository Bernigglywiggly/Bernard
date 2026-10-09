# START HERE: state at Fri 9 Oct 2026, 17:10 UK (written for a Claude with zero history)

This block is the truth. Everything below it in this file is older history, kept for detail only.
Repo: `~/Bernard`, branch `claude/funny-newton-gd9w8v` ONLY (push with: `git push -q origin claude/funny-newton-gd9w8v 2>/dev/null || git -c http.curloptResolve=github.com:443:140.82.121.4 push -q origin claude/funny-newton-gd9w8v`). Python: `~/youtube/.venv/bin/python`. Videos, voice takes and pictures are on THIS Mac only (not in git): a cloud session cannot render or upload them.

## 1. Done this session (9 Oct afternoon) and what is still running
| Item | File | State |
|---|---|---|
| Spanish film 2 | `lab/curvelf/lf02_price_es/LF02_ES_v2.mp4` | DONE. 8 lines re-voiced; critic `CRITIC_ES_v2.md` = UPLOAD; chapters in POST.md. WAITING ON USER: which channel (The Curve or a new "La Curva"), and his ear check of `ear_check_v2.mp3` (xAI said "equis A I"). Old takes in `flow/takes_old_v1/` |
| LF03 music drops | `lab/curvelf/lf03_held/LF03_FLOW_v5.mp4` | DONE. `mix_flow.py` gained `fill()` (lifts short holes in a score bed); sound-only re-mix; dips now about 5 dB. Manifest index 8 points at v5. Upload after 19:30 9 Oct |
| `short_escape` | index 5 of `channel/uploads_newlook.json` | Upload after 19:30 UK 9 Oct (daily cap hit 8 Oct) |
| Tunnel pilot ("Megaprojects"/"Datum Line") | `lab/curvelf/pilot_tunnel/TUNNEL_PILOT_v2.mp4` (= `lab/pilots/megaprojects/`) | DONE. Critic v1 (`CRITIC_v1.md`, FIX THEN UPLOAD) fixes applied in v2: honest diagram label, frame 0 shows the photo, hook at 5.4 s, ≈15 MILLION, POST.md with photo links + chapters. NOT done: name pronunciations by ear (Fehmarn, Rødbyhavn, Øresund, Lolland, Scandlines); channel name; channel does not exist |
| Economy pilot ("The Household Ledger") | `lab/curvelf/pilot_ledger/LEDGER_PILOT_v2.mp4` (= `lab/pilots/economy/`) | 33 pictures drawn in code (`illustrations.py`, no AI generator), 115 lines voiced, lint clean, v2 rendered. Critic RUNNING -> `lab/pilots/economy/CRITIC_v2.md`; if missing, re-run the film-critic skill on v2 |
| Engine (`lab/curvelf/flow.py`) | | New script options: `ILLUS = "..."` (picture label), `LEAD` (seconds before the first word), `OPEN_RESOLVED = True` (frame 0 shows the first picture). Long channel names push the chapter rail right. Photo credit no longer doubles "PHOTO" |
| Trend desk report (another session) | https://claude.ai/artifact/FXjyxJ6wRAA1sXaUzdp3Qp | Read only; nothing in the repo |

ElevenLabs: about 89,000 characters left until about 16 Oct. Strategic warning from a critic (CRAFT "Learned", 9 Oct): every channel shares one engine look; a new channel needs its own look before launch.

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
1. After 19:30 UK 9 Oct: upload `short_escape` (index 5) and LF03 v5 (index 8) via section 3. Before each upload, a critic must have passed the file (LF03: picture as v4 which passed; only the music bed changed).
2. Read `lab/pilots/economy/CRITIC_v2.md`; apply its fixes (one more render at most).
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
