# Daily Short runbook (The Curve): from facts to a scheduled upload

Written by account B, Wed 28 Oct 2026 ~15:30 UK, from the Short 10 build (hLhHU7O3x4M). For a session with zero
history: follow it top to bottom. Every command is the one that worked on Short 10. `N` = the Short's number.

## 0. Rules that outrank this file
- `~/.claude/CLAUDE.md` (his standing rules), `CLAUDE.md`, `CRAFT.md` (house rules + "Learned on our films"), `TEAM.md`.
- Branch `claude/funny-newton-gd9w8v` only. Commit your own paths only (`git add <paths>`, never `-A`), no model names in
  commit messages. If `.git/index.lock` exists, another account is committing: wait 30 s and retry.
- Never put his email address in any request. Never change a video's visibility in YouTube Studio through a browser.
  Never promote credit cards, loans, BNPL, trading or crypto (FCA). An upload needs his yes for that video.
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
