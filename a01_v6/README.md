# A01 v6: Chrome & Marl (calm rebuild of the hook)

The hook rebuilt to your notes: the original calm voice, no jokes, and everyday perspectives for
every number. The camera stays still while lines form and flow into new forms. Chrome and heathered
marl with one turquoise accent, and one quiet sound on every motion.

| File | What |
|---|---|
| `mograph.py` | the motion-graphics engine (skia, crisp vector 1080p30): Tron-style line formations, morphs, ASCII decode, the 10×10 grid, cards, chrome type; logs sound events |
| `sfx6.py` | the layered sound palette driven by those events, plus the Am9 → Cmaj9 pad; mixes with the voice at -14 LUFS |
| `PLAYBOOK.md` | script structure, look, motion, sound and Shorts rules, with research sources |
| `PROMPTS.md` | GPT prompts: v6 brief, Pinterest → design system, perspective writer, calm script, voice design, sound kit, score, formation shots |

```bash
pip install skia-python numpy scipy
export A01V6_FONTS=<folder with Michroma-400, InterTight-400/500, IBMPlexMono-400/500 .ttf>  A01V6_BUILD=./build
python3 mograph.py                      # -> build/mockup_silent.mp4 + events.json (about 2.5 min on a laptop)
python3 sfx6.py path/to/voice.mp3       # -> build/mockup_mix.wav
ffmpeg -i build/mockup_silent.mp4 -i build/mockup_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest A01_v6_mockup.mp4
```

The scene times in `mograph.py` are aligned to the George take (52.5 s). If you pick another voice,
shift the scene boundaries to its sentence starts.
