# Consistent-character pipeline (WaveSpeed)

SFW promo content for a **disclosed AI persona**: same invented adult woman (25-30) in every photo and Reel,
realistic phone/35mm look, posted with the platforms' AI labels. Model choices and prices: `MODELS.md`.

## Your part (only you can do this)

🔑🧾🛡️📁✋ **Create `~/Bernard/ofm/.env` yourself with one line: `WAVESPEED_API_KEY=your-key`** (key from wavespeed.ai/accesskey). Never paste it in chat.

- [ ] Make the file in TextEdit (plain text) or Terminal: `nano ~/Bernard/ofm/.env` → paste → save
- [ ] It is git-ignored (`ofm/.gitignore`, `pipeline/.gitignore`). The code never prints or logs it
- [ ] Say "key is in" → the ≤ $1 validation run below can go

## The flow

```
characters/<name>.json  (fixed traits: face, eyes, hair, marks with exact placement, build, age 25-30)
      │
      ▼  character.py master        anchor portrait + front / 3-4 L / 3-4 R / profile / full body
      ▼  qc.py                      face-embedding score vs the anchor, contact sheet, CHECKLIST.md
      ▼  character.py pick          lock the best 4-6 as references
      ▼  shoot.py <shotlist.yaml>   new scenes, identity locked to the refs (+ realism layer)
      ▼  qc.py --approve-to ...     only PASS + ticked checklist images survive
      ▼  (15-25 approved) character.py dataset + train  → LoRA; A/B it against refs, keep the winner
      ▼  reels.py                   5-8 s 9:16 clips from approved 9:16 stills + caption + frame sheet
```

## Commands (Python: `~/youtube/.venv/bin/python`, run inside this folder)

| Step | Command | Cost |
|---|---|---|
| Any step, no money | add `--dry-run` (prints exact request JSON + estimate) | $0 |
| Master set | `python character.py master --char NAME` (`--anchors 4` to choose between 4 faces first) | ~$0.16 |
| Score it | `python qc.py --char NAME out/NAME/master` | $0 |
| Lock refs | `python character.py pick --char NAME out/NAME/master/front.jpg out/NAME/master/34l.jpg ...` | $0 |
| Photos | `python shoot.py --char NAME shots/my_week.yaml --variants 2` | $0.027 / image |
| Fix a miss | `python shoot.py ... --only shot_id --model google/nano-banana-2.1/edit` | ~$0.07 |
| QC + approve | `python qc.py --char NAME out/NAME/shoots/my_week --approve-to out/NAME/approved` | $0 |
| LoRA | `python character.py dataset --char NAME --src out/NAME/approved` then `python character.py train --char NAME --run-cap 3` | $2.50 |
| Photos via LoRA | `python shoot.py --char NAME shots/my_week.yaml --mode lora` | $0.01 / image |
| Reels | `python reels.py --char NAME out/NAME/approved/x.jpg --motion turn --caption "..."` | $0.21 / 5 s |
| Money | `python ws.py balance` · `python ws.py ledger` | $0 |

Motion presets: `hair`, `turn`, `walk`, `laugh`, `sip`, or any free text.

## Money guards

- Every call is priced first (+10% margin). A run stops before it would pass **$2** (`--run-cap`) or the month passes **$100** (`--month-cap`, env `WS_MONTH_CAP`).
- `out/spend.csv` logs every call, plus the real account balance at the start and end of each run (truth check on estimates).
- A model with no price on file is refused, not guessed.

## Safety rules built into the code

- SFW only: nude / explicit / lingerie / see-through terms are refused before any call.
- Clearly adult: bible age must be 25-30; teen / schoolgirl / petite-young / youthful etc. are refused.
- Invented person only: celebrity / lookalike / resembling terms are refused; no real photo is ever uploaded.
- WaveSpeed's own policy bans nudity on every model anyway (`MODELS.md` §2).
- Posts carry the AI label on every platform; bios say AI (Fanvue rule, `FANVUE_PLAN_8OCT.md`).

## QC: what "consistent" means here

- `qc.py` uses OpenCV YuNet + SFace (an ArcFace-style recogniser, CPU, models fetched once into `cache/models/`).
- Score = cosine similarity to the average of the locked references. Gate 0.40 (OpenCV's same-person line is 0.363). Recalibrate after the first real batch.
- Embeddings cannot check moles, freckles, the wrist tattoo or eye colour. `CHECKLIST.md` lists those per image: tick them by eye.
- Reels: check `reels_sheet.jpg` (first / mid / last frame) for face drift.

## Validation run (≤ $1, uses the placeholder `characters/test_ava.json`)

```
python character.py master --char test_ava --views ""          # 1 anchor portrait          $0.027
python character.py pick   --char test_ava out/test_ava/master/anchor_00.jpg
python shoot.py --char test_ava shots/test_shots.yaml --only cafe_window,street_evening --run-cap 1   # $0.054
python qc.py    --char test_ava out/test_ava/shoots/test_shots
```

## Files

| File | What |
|---|---|
| `ws.py` | API client: key loading, submit/poll/download, upload, balance, ledger, caps, dry-run |
| `prompts.py` | identity / scene / realism layers, payload builders per model, safety lint |
| `character.py` | master set, pick, LoRA dataset + training |
| `shoot.py` | shot list → photos (refs, lora, lora-edit modes) |
| `qc.py` | identity score, contact sheet, checklist, approve |
| `reels.py` | image-to-video, 1080x1920 finish, caption, silent track, frame sheet |
| `characters/test_ava.json` | placeholder test character (invented) |
| `shots/test_shots.yaml` | example shot list |
| `out/`, `cache/` | outputs, ledger, uploads cache, QC models (git-ignored) |
