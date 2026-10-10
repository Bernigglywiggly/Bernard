# Talking stickman (Flash-game style)

The chrome-hat stickman, lip-synced to your own recorded voice. Thick black wobbly ink (the line "boils" at
12 drawings a second, held on twos at 24 fps), a Flash-game arena or a flat bright background, snap poses with
anticipation and overshoot, impact frames, speed lines, a pixel-font LOADING card and a fake health bar.

## 1. Record (phone voice memo is fine)
- Quiet room, soft furnishings, no fan or telly. Phone 15-20 cm from your mouth, slightly off to the side.
- **10-30 seconds.** Short punchy lines with real pauses between them. Pauses are when he changes pose.
- Act it out. Loud words get head nods, `!` lines and the loudest punchline get an impact frame.
  Saying an onomatopoeia (**boom, bang, pow, bam, wham, smash, crash, zap, bonk, oof**) triggers a comic SFX burst.
- AirDrop or copy it into `lab/stickman/in/`. Name it whatever you like, e.g. `in/line01.m4a` (wav/m4a/mp3/aiff all work).

## 2. Voice changer (optional)
The parent Claude session runs the raw file through ElevenLabs speech-to-speech and saves the result as
**`in/changed.<ext>`** (e.g. `in/changed.mp3`). If a `changed.*` file exists, it is used. If not, your raw file is used.
`--raw` forces the raw file. Delete `in/changed.*` before the next take.

## 3. Render
```
cd ~/Bernard/lab/stickman
PY=~/youtube/.venv/bin/python
$PY talk.py auto out/take01.mp4                      # 16:9 1080p, arena
$PY talk.py auto out/take01_vert.mp4 --vert          # 9:16 1080x1920 for Shorts (captions on)
$PY talk.py in/line01.m4a out/x.mp4 --bg flat        # yellow Newgrounds rays
$PY talk.py auto out/x.mp4 --bg 33CCFF --no-intro --captions --sheet out/sheet.jpg
```
`auto` = `in/changed.*` if present, else the newest file in `in/`. Flags: `--vert`, `--bg arena|flat|<hex>`,
`--captions/--no-captions` (default: on for vertical only), `--no-intro` (skips the 0.75 s LOADING card),
`--sheet` (8-frame contact sheet labelled with word + mouth), `--name` (HUD name). It takes about 10 s per 15 s clip.

## How it works
`talk.py`: ffmpeg → 16 kHz mono → faster_whisper `small.en` word timings (cached in `out/.cache`) + RMS envelope.
Word edges are pulled in to where the audio is actually voiced. Each word is split into letter-rule chunks →
8 mouths (`rest, MBP, small, open, wide, O, U, FV`). One mouth per drawing at 12 fps, with lip closures (M/B/P)
given priority and loudness controlling how wide the jaw opens. Silence closes the mouth. On top of that:
blinks, glances in pauses, nods on stressed words, a gesture pose at each phrase (shrug on `?`, fist pump on `!`,
arms crossed and smug on the last line), hard camera cuts wide/medium/close, and an impact frame on SFX words
(or the loudest punchline). `flash.py` holds all the art (rig, mouths, hat, arena, bitmap font, effects, HUD).
`character.py` / `gag_reel.py` are the older dark-mograph version of the same character, kept for reference.

## Limits
- Mouth shapes come from spelling rules, not a phoneme dictionary, so odd words can be slightly off.
  The loudness gate keeps the timing right regardless.
- English only (`small.en`). Mumbled audio means poor word timing, so it falls back to loudness-only mouths.
- He faces the camera and stays in one spot: no walking or props yet.
