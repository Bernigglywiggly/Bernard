# Daily Short runbook (The Curve): from facts to a scheduled upload

Written by account B, Wed 28 Oct 2026 ~15:30 UK, from the Short 10 build (hLhHU7O3x4M). For a session with zero
history: follow it top to bottom. Every command is the one that worked on Short 10. `N` = the Short's number.

## 0. Rules that outrank this file
- `~/.claude/CLAUDE.md` (his standing rules), `CLAUDE.md`, `CRAFT.md` (house rules + "Learned on our films"), `TEAM.md`.
- Branch `claude/funny-newton-gd9w8v` only. Commit your own paths only (`git add <paths>`, never `-A`), no model names in
  commit messages. If `.git/index.lock` exists, another account is committing: wait 30 s and retry.
- Never put his email address in any request. Never change a video's visibility in YouTube Studio through a browser.
  Never promote credit cards, loans, BNPL, trading or crypto (FCA). Uploads: on 28 Oct he approved daily scheduled runs uploading each Short for 17:00 without asking him first (after critic SHIP, private with publishAt); a long film, a new style or another channel still needs his yes.
- Any line that needs his hands or decision starts with 5 random emojis, one ask per line.
- Heavy jobs (Remotion full renders, RIFE) go through the lock: `ACCOUNT=B bash lab/tools/heavy.sh <command>`.
- Checkpoint after every step: commit the step's files and push, so a session that dies can be resumed from git.

## 1. Script (`lab/curve_v2/shorts/shortN.py`, same format as `short10.py`)
- `TITLE`, then `LINES = [dict(id, facts, text, cap, shot), ...]`: about 6 lines, 28-32 s voiced. `facts=` names the
  rows of the facts file each line uses; nothing goes on screen or in the voice unless the facts file has it.
- `cap` splits the line into 2-4 word caption phrases with ` / `. `shot` says what is on screen.
- Read numbers aloud the way Whisper will hear them right ("twelve cents of every dollar", never "one dollar in eight").
- Lint: `python3 .claude/skills/film-critic/script_lint.py lab/curve_v2/shorts/shortN.py`. Fix every flag first.

## 2. Voice (ElevenLabs claude.ai connector, account B)
- Load with ToolSearch: `creative_generate_speech` and `creative_get_generations` (server
  `mcp__d429fd8a-62d2-4b55-b286-65bf03f9b2b6__`). If they are not in the session, stop here, commit, and send a
  PushNotification saying the voice connector is missing.
- One continuous take of every line joined with spaces: `{context, model_id: "eleven_v4", voice_id:
  "iP95p4xoKVk53GoZ742B"` (Chris)`, generations_count: 2, prompt: <text>}`. Then `creative_get_generations
  {context, flow_id, generation_ids}` and download each `full_res_url` (they expire after 2 h):
  `curl -sSL -o lab/curve_v2/shorts/vo/sN_chris_v1a.mp3 '<url>'` (and `v1b`).
- Tighten and transcribe (ABSOLUTE paths, or whisper writes nothing):
```bash
V=~/Bernard/lab/curve_v2/shorts/vo; cd ~/Bernard/lab/motion && for k in a b; do
  python3 scripts/tighten_vo.py $V/sN_chris_v1$k.mp3 $V/sN_chris_v1${k}_tight.mp3 --tempo 1.05 >/dev/null 2>&1
  ffmpeg -y -loglevel error -i $V/sN_chris_v1${k}_tight.mp3 -ar 16000 -ac 1 $V/sN_v1${k}_tight16k.wav
  node scripts/transcribe.mjs $V/sN_v1${k}_tight16k.wav $V/sN_v1${k}_tight.json >/dev/null 2>&1
  python3 -c "import json; print('$k', ''.join(x['text'] for x in json.load(open('$V/sN_v1${k}_tight.json'))).strip())"; done
```
- Pick the take whose transcript matches the script word for word and reads more naturally. If a number is misheard,
  reword the line and re-voice: never ship a caption that disagrees with the voice.
- `cp $V/sN_chris_v1<k>_tight.mp3 public/shorts/sN_vo.mp3`, then
  `python3 scripts/captions_ts.py $V/sN_v1<k>_tight.json src/curve_v2/voSNCaptions.ts VO_SN --script ../curve_v2/shorts/shortN.py`
  (caption words come from the script, timings from Whisper).

## 3. Footage (borrowed footage under half the runtime, 5 s or less a shot, always credited)
- Find the maker's own upload: `yt-dlp --flat-playlist --playlist-end 12 --print "%(id)s %(title)s" https://www.youtube.com/@<channel>/videos`.
- Download only the seconds you need in 4K: `yt-dlp -f "bv*[height<=2160]" --download-sections "*128-152" -o <dir>/<name>.mp4 <url>`
  into `lab/curve_v2/footage/<source>_<date>/`, and write the URL, title and section to `SOURCES.txt` there.
- Shot boundaries: `ffmpeg -i <clip> -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep pts_time`.
- Cut, crop to 9:16 and convert to 30 fps with RIFE in a prep script modelled on `prep/s10_clips.sh` (its `mk` function:
  name, start, duration, crop `1215:2160:x:0` from 4K, slow factor). **The clip must last at least as long as its scene**:
  raise the slow factor rather than let Remotion freeze the last frame. The loop clip is the hook clip's first 30 frames
  reversed, so the last frame of the Short is frame 0. Run it through the lock.

## 4. Composition (`lab/motion/src/curve_v2/CurveV2ShortN.tsx`, copied from `CurveV2Short10.tsx`)
- Kit from `./kit`: `ClipScene, Tag, Stamp, CaptionTrack, Credit, Bed, Sfx, HEADC, MONO, keyline, pop`. Time every scene
  from spoken words: `cue("word", nth)` over `VO_SN`, scene starts on `beatAfter(...)` (124 BPM bed).
  `SHORTN_FRAMES = Math.round((LAST_MS / 1000) * FPS) + 30 + LOOP` with `LOOP = 30`.
- Register it in `lab/motion/src/Root.tsx` after Short 10 (add only your own lines).
- Learned on Short 10 (CRAFT, 28 Oct): captions from the first word, in 2-4 word phrases; a kicker of at least 84 px
  held on screen; every sticker held 1.4 s or more and citing its own source; a slow push (scale 1 to 1.035) on dark
  scenes; nothing frozen for more than 2 s; the loop end rebuilds frame 0 exactly (eased `interpolate`, not a spring,
  and nothing on frame 0 that isn't on the last frame).
- Check: `npx tsc --noEmit -p .` and stills: `npx remotion still CurveV2-ShortN out/sN_f<frame>.png --frame=<frame>`.

## 5. Render and master
```bash
cd ~/Bernard/lab/motion && ACCOUNT=B bash ../tools/heavy.sh npx remotion render CurveV2-ShortN ../curve_v2/shorts/out/SHORTN_v1_raw.mp4 > /tmp/sN_v1.log 2>&1; tail -1 /tmp/sN_v1.log
cd ../curve_v2/shorts/out && ffmpeg -y -hide_banner -loglevel error -i SHORTN_v1_raw.mp4 -c:v copy \
  -af "acompressor=threshold=-22dB:ratio=3:attack=4:release=90:makeup=3,loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 48000 SHORTN_v1.mp4
```

## 6. Critic (the builder never grades its own work)
- Invoke the `film-critic` skill. Measure into `lab/curve_v2/shorts/out/critic_sN/v<k>/`; also check the loop:
```bash
F=lab/curve_v2/shorts/out/SHORTN_v1.mp4; O=lab/curve_v2/shorts/out/critic_sN/v1; mkdir -p $O
ffmpeg -loglevel error -y -i $F -frames:v 1 $O/frame0.png; N=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $F)
ffmpeg -loglevel error -y -i $F -vf "select=eq(n\,$((N-1)))" -frames:v 1 $O/lastframe.png
ffmpeg -hide_banner -i $O/frame0.png -i $O/lastframe.png -lavfi psnr -f null - 2>&1 | grep -o "average:[0-9.inf]*"   # want 35 dB or more
```
- Round 1: a NEW subagent (Agent tool, `model: "sonnet"`), the skill's prompt, nothing about what you think of it.
  Fix every must-fix, re-render, re-measure. Round 2: another new subagent with round 1's report. **Upload only on SHIP.**
  Keep `critic_sN/ledger.md`: each finding, the fix, the version it landed in.

## 7. Upload (Zapier YouTube connection, scheduled publish)
- Manifest: append an entry to `channel/uploads_curve.json` shaped like index 5 (file, title, title_alts, description
  ending with sources and "Not investment advice." only if money is discussed, tags, channel "the-curve", public true,
  category "28", made_for_kids false, synthetic true, kind "short", `publish_at` "YYYY-MM-DDT17:00:00Z" for 17:00 UK in
  GMT). Load and dump with `json.dumps(m, indent=1, ensure_ascii=False) + "\n"`. No `<` or `>` in the description
  (YouTube rejects them).
- Open the session: `~/youtube/.venv/bin/python lab/tools/youtube_upload.py zapier-init channel/uploads_curve.json <index> > /tmp/sN_init.json`
  (prints `headers` and `body`).
- Zapier tools (server `mcp__7add4ff2-4c2d-4108-b936-5f366a3ca57b__`): `execute_zapier_write_action` with
  `selected_api "YouTubeV4CLIAPI"`, `action "_zap_raw_request"`, `tool_name "youtube_make_api_mutating_request"`,
  `connection_id "02f9e902-69d2-8a12-af4b-b4f4cd146eeb"` (The Curve, UCI7lgtrs_En_L9MmPnJbwEg), params: method POST,
  url `https://www.googleapis.com/upload/youtube/v3/videos`, `querystring {"uploadType": "resumable", "part": "snippet,status"}`
  (in the URL they get dropped), the init's headers, `fail_on_errors "false"`, body = the init's body string.
- Send the file into the session from the response's `Location`:
  `~/youtube/.venv/bin/python lab/tools/youtube_upload.py put '<location>' lab/curve_v2/shorts/out/SHORTN_vK.mp4 --manifest channel/uploads_curve.json`
  (use the venv python: the system one has no `requests`). It records the id in `channel/uploads_curve.done.json`.
- Verify: `execute_zapier_read_action`, same api/action/connection, `tool_name "youtube_make_api_get_request"`, url
  `https://www.googleapis.com/youtube/v3/videos`, `querystring {"part": "status,processingDetails,snippet", "id": "<id>"}`.
  Want `privacyStatus` private with the right `publishAt`, and processing succeeded.

## 8. Close
- One dated line under "Learned on our films" in `CRAFT.md`: what the critic caught.
- Tick the line in `TEAM.md` §4; your block at the top of `HANDOFF.md`; `bash lab/tools/sync_handoff.sh`; commit; push.
- PushNotification (under 200 characters): the link and the publish time, or the blocker and what he must do.

## 8b. The Curve's topic rule (from our analytics, 28 Oct)
- Winners: a **viral clip of a machine doing something that looks impossible**, explained the day it spreads:
  Microduck robot 17,753 views in 2 days, Roadster upside down 15,466. Follow-ups on a story we already did fall to
  ~1,100-1,300 (Roadster 2 and 3); money and earnings angles get ~850-1,700.
- So pick, in this order: (1) the most-viewed NEW clip (last 48 h) of a robot, vehicle, gadget or spacecraft doing
  something surprising, where the maker's own footage exists and one drawn diagram explains the mechanism in 30 s;
  (2) a big launch with the maker's own film; (3) a money story only when it rides a moment people are already sharing.
- Sharper (alignment check 28 Oct): **only a clip where something familiar is visibly in trouble or beating the odds**
  (falls, flips, cracks, gets back up) and is already being shared. Test: a stranger with the sound off thinks "wait,
  what?" within 2 seconds, or skip it. The three "thing in trouble" Shorts (duck, Roadster upside down, iPhone crack)
  are 85% of all new-format views; same car, same week, "upside down" beat "launch" 14x. Earnings, demos and
  announcements average ~1,300: that is How They Profit's lane.
- Title: the question the clip makes people ask, search words first ("How Did This Robot Duck Learn to Get Back Up?").
- A slot (b-curve-daily, 17:00): never a story that a live or scheduled Curve Short already covers (titles in
  `channel/uploads_curve.json`). B slot (a ROTA row, 23:00 UK from Sun 1 Nov): may be a sequel to a Curve Short past 5,000 views, made
  within 7 days of it, answering a NEW question about the same clip; otherwise the next-best clip by this rule.

- **Playbook rules (account C, 30 Oct; `lab/research/SHORTS_PLAYBOOK_2026-10-29.md` §10, evidence grades there):**
  1. Frame 0 is the impossible instant **already moving**, one drawn mark on it, a question of 5 words or fewer.
  2. Our own drawing is on screen **by second 2** (YouTube's 1 Oct 2026 originality change rewards added value).
  3. No line only describes the clip: each adds a why, a number or our verdict.
  4. Judge on engaged views and "stayed to watch" (goal 70%); loops and public views don't count toward the Partner Programme.
  5. End: the channel promise spoken plus "subscribe", then the loop frame (provisional: test T3 in the playbook).
  6. Set the related-video link on every Short: the matching film, else the previous Short on the same subject.
  7. Title: the typed question, object and maker first, no hashtags in the title.
  8. Never the same scene structure three days running.
  9. A series is one subject with new questions; a sequel only for a Short past 5,000 views (as above).

## 8c. The Curve's evergreen B slot (account C, 30 Oct: `lab/research/BREAKOUT_CONCEPTS_2026-10-29.md`)
Only when a ROTA row says "evergreen B slot". Proven by Under Six Minutes Studio (latest-10 median 494,000 views, 27 of 58
Shorts over 1M) and The Why Side; it needs no viral clip and no footage permission, which is the A slot's bottleneck.
- **Format:** "How Engineers Solved [the X Problem]" or "Why [a familiar thing] Is [its odd feature]": one everyday object
  with an odd feature everyone has seen and few can explain, the problem it solves, the mechanism as our own animated
  cross-section, one number on screen, our verdict. 30-40 s.
- **Pick:** cone-shaped train wheels, round plane windows, escalator comb teeth, the ridge on ring-pull cans, and so on.
  Search YouTube first: skip a topic any channel posted in the last 30 days, and never a leader's own hero topic.
- **Frame 0:** the object drawn with the odd feature circled, 2-6 words ("WHY ARE THESE CONES?"). Line 1 asks the question
  with "you" in it.
- **Facts:** a facts file per Short (manufacturer, standards body or university pages; patents), CRAFT §5.
- **Pictures:** our own drawings only (Remotion SVG or Blender). The Curve's narrator, look and bed, but vary the scene
  order from the A-slot Shorts (CRAFT §1).
- **Title:** the exact question, search words first, 6 words or fewer.
- **Read at 72 h** against The Curve's latest-10 median (1,300): PASS = 3,000+ views or 60%+ engaged → 2 evergreen B slots a week.

## 9. Other channels (same steps 1-8, with these changes). Each channel has its own look, narrator and music:
**PIVOTS (account C, 30 Oct): How They Profit and Money Crimes are re-pointed** (`lab/research/BREAKOUT_CONCEPTS_2026-10-29.md`). For those two, §9-P1 and §9-P2 at the end of this section replace the Format, Facts, Look, Music, Pictures and Description rows of this table; their channel ids, Zapier connections, manifests, code folders and narrator rules still apply.
YouTube punishes one template re-skinned across channels owned by one person, so never copy the Curve's look.
| | How They Profit (§9a) | Money Crimes (§9b) | Curva Explica (§9c) |
|---|---|---|---|
| Channel | HowTheyProfitHQ, UC7BbkaTRGMD44rZnUd3ZI_Q | MoneyCrimesFiles, UCXoYGDg8TxCPvIqx5TdVTkw | Curva Explica, UCuymwi0CdK0XU-CKATzJ3BQ |
| Zapier connection | `02d0de21-a222-85ea-aea9-5b0920dd34b0` | `02ce9a67-dbe7-8998-8da5-26da5fc35e26` | `020e1621-8ed2-8623-aa3a-11cd759b5c3e` |
| Manifest (new) | `channel/uploads_htp.json` | `channel/uploads_crimes.json` | `channel/uploads_curva.json` |
| Format | "How <company> Really Makes Money": one surprising number from the company's own results or filing (this week's earnings first), the money machine drawn as a ledger or flow, our verdict | "How the <scam or heist> Actually Worked": the trick drawn step by step, the one detail that exposed it, our verdict | The Curve's best Shorts by views, in Spanish: Microduck first, then Roadster upside down, then the next by views |
| Facts | primary only: the company's release, 10-Q/10-K or annual report, numbers copied with the URL | only charged or convicted people: court records, DOJ, SEC, SFO, FCA or police releases; "the story goes" for anything contested | the Curve facts file of the original Short; nothing new is claimed |
| Look | the ledger look of `lab/ch2/look.py`: navy #0A0F17, paper #EFE7D6, brass #C9A35B, red #B4553F, muted #8C93A0; IBM Plex Serif headings, mono labels with tracking, a "SOURCE ·" line | case-file look (`channel/money-crimes/README.md`): warm tungsten and cool shadows, gold name cards, red rubber-stamp numbers, document and map drawings | the original Short's pictures; every on-screen word translated |
| Code | `lab/motion/src/htp/` (kit + `HtpShort<N>.tsx`), scripts `lab/ch2/shorts/htp_short<N>.py` | `lab/motion/src/crimes/`, scripts `lab/shorts/crimes/mc_short<N>.py` | copy `CurveV2Short<k>.tsx` to `lab/motion/src/curva/CurvaShort<k>.tsx`, script `lab/curvelf/curva/curva_short<k>.py` |
| Narrator | an ElevenLabs voice that is not Chris: pick once in SETUP (calm, authoritative), write its id in `channel/channel2/README.md` | a different ElevenLabs voice again (low, measured), id in `channel/money-crimes/README.md` | a native Spanish ElevenLabs voice (eleven_v4 speaks Spanish), id in `channel/ROTA.md` |
| Music | its own bed from `lab/music/beds.py`, never the Curve's 124 BPM bed | Kevin MacLeod jazz (`lab/music/jazz/library.py`), credit line in the description | the original Short's bed |
| Pictures | our charts and drawings, plus the company's own publicity footage at 5 s or less a shot, credited | our drawings, public-domain archive (`lab/longform/tools/commons.py`, credits kept), public court documents; no news-agency footage | the original's, credits kept and translated |
| Description | sources, then "Not investment advice." | sources; "Charged" or "convicted" stated exactly as the record says | sources in Spanish, plus "Versión en español de The Curve" |
- **Money Crimes: no new builds** until How They Profit or Curva Explica passes the gate in `channel/ROTA.md` (alignment check 28 Oct: best Short 33 views, footage is hard to clear, defamation risk, and AI reenactments are the style most likely to be flagged as mass-produced). Until then it only gets its finished backlog (ROTA.md BACKLOG PREP).
- **SETUP (first run per channel):** build the kit (palette, fonts copied into `lab/motion/public/<channel>/fonts`,
  caption style, credit line, a channel promise end plate in its own words), pick and record the narrator, then make
  Short 1 in the same run. Usage guard: SETUP + Short is about 9% of the weekly allowance.
- All three are new styles on dead channels, so the critic round is not optional: round 1 must say SHIP before upload.
- Every run on these channels also obeys §0: FCA (never promote credit cards, loans, BNPL, trading, crypto or
  investing), no email address in requests, no Studio in a browser, one Short per run, private with publishAt.

### 9-P1. How They Profit → map geography (concept 5; account C, 30 Oct 00:27, after the web widening; replaces §9a's format rows; tests in week 1)
Proven best of any 2026 concept: World Ji Ke (created 9 May 2026; latest-10 median **915,500** views; 47 of 66 Shorts over 1M;
84.6k subscribers), One Map, One Battle (created 7 Oct; 85,000), historicalmiracles (created 23 Sep; 65,000), MapLore (created
9 Apr; 132.4M views). Maps are pure drawing (no footage), and the map kit already exists from the Hormuz film.
| Row | Spec |
|---|---|
| Format | "Map curiosities" in 30-45 s: one surprising geographic fact, shown on our own animated map ("[countries or places] that [surprise]"): borders that almost touch, enclaves, a strait that carries a share of the world's trade, a country that changed shape. Build the reveal place by place, one highlight per beat; end on the most surprising one and our one-line verdict. A money angle only where it is natural (a strait, a canal, a tiny rich state) |
| Series | design every topic so a "Part 2" exists (World Ji Ke's Part 2s pass 1M); say "part 2" on screen only when it is made |
| Topic | search YouTube first: skip any topic a map channel posted in the last 30 days, and never copy a title or list from World Ji Ke, MapLore or One Map, One Battle; no active wars (limited ads) |
| Frame 0 | the finished map with the first highlight lit and a 2-5 word question ("THEY ALMOST TOUCH?") |
| Facts | facts file `lab/research/MAP_<topic>_FACTS.md` before the script: borders and areas from Natural Earth / CIA World Factbook / national statistics, distances measured on the map we draw, two sources for anything contested |
| Look | the Hormuz map kit (`lab/maps/hormuz`, `lab/maps/style`) in How They Profit's ledger palette (paper #EFE7D6 land, navy #0A0F17 sea, brass #C9A35B highlights, red #B4553F one accent), never the Curve's look; captions in its own style |
| Narrator, music | How They Profit's own voice (SETUP picks it, calm and authoritative, never Chris); its own bed from `lab/music/beds.py` |
| Pictures | our maps only |
| Title, description | the curiosity as a question or list, 6 words or fewer ("Countries That Almost Touch"-style wording is World Ji Ke's: write our own); sources in the description |
| Pass mark | the ROTA gate: one test 1,000+ views in 72 h, or both 500+ |
| Name | the channel keeps the name "How They Profit" until he renames it in Studio (a maps name in his own words) |

### 9-P2. Money Crimes → "Evolution of" (concept 4; account C, 30 Oct 00:27; replaces §9b's format rows; tests only after the Sun 8 Nov gate)
Proven by Untold Theory (created 20 Aug 2026; latest-10 median 579,500; 7 of 57 Shorts over 1M; 42.5k subscribers); concept 4
has the best subscriber conversion in the breakout sample (median 4.03 subs per 1,000 views; ours 0.84).
| Row | Spec |
|---|---|
| Format | "Evolution of the [Object]" in 40-50 s: 6-8 eras, one beat each = the year + our drawing of that version + one spec + its price then (today's money in small type); the last beat is today's version; the verdict is ours. Loop: today's object morphs back into the first one, which is frame 0 |
| Topic | an everyday object with a big visual change and a price story: kettle, phone, camera, car key, TV, headphones, calculator, trainers. Search YouTube first; never Untold Theory's own topics (bicycles, bulletproof vests) |
| Frame 0 | the oldest version beside today's, "?" between them, 2-6 words |
| Facts | facts file `lab/research/EVO_<object>_FACTS.md` before the script: dates and specs from the maker's history page, a museum (Science Museum Group, Smithsonian) or a patent; prices from dated catalogues or adverts (archive.org); today's money via the Bank of England calculator (UK) or BLS CPI (US) |
| Look | its own: warm tungsten and paper from the case-file look, gold year stamps, objects as our own line drawings (Remotion SVG), never AI images or stock photos |
| Narrator, music | Money Crimes' voice (`channel/money-crimes/README.md`); its own bed from `lab/music/beds.py` |
| Pictures | our drawings only |
| Title, description | "Evolution of the [Object]", 6 words or fewer; sources per era + the inflation calculator in the description |
| Pass mark | the ROTA gate, from week 2 |
| Later (not now) | a long-form animated money-crime documentary line (fern, Coffeezilla, Kento Bento pull 2.75-4.7M per film and long-form pays 23-340x more per view than Shorts) once a channel has subscribers to watch it |
