# A01 v5: one line, many worlds

An upgrade pass on the A01 hook (first 50 s): more camera angles and perspectives, and five visual
palettes woven together, built in Blender with Python scripts. It's meant to feel varied without
feeling random.

## The idea

Every palette is a **room on the same amber drift line**. The camera travels the line from room to
room, and the room changes with the script's register (the Taste Map rhythm: fact → translate →
joke → deep).

| Register | World (palette) | Camera grammar |
|---|---|---|
| FACT | **W0 core**: STAIR (fog, concrete), LOBBY (imperial blue grid), VOID (black) | slow crane, low orbit, stable 20–35 mm |
| TRANSLATE | **W1 PRESS**: bone paper, black ink, crop marks, barcode | top-down god's-eye → grazing angle, truck + rack focus |
| JOKE | **W4 SIGNAL**: 3-colour ordered dither (ground, phosphor, amber), on twos | shot/reverse, dutch ±18°, snap zooms, 4-frame bursts |
| DEEP | **W2 CLOUD**: white point clouds on black | dolly zoom (vertigo), 70–110 mm long lens |
| PAYOFF | **W3 CHROME**: icy chrome, softbox reflections | FPV swoop that lands, motion blur |

**Constants** (never change, so the variety reads as one channel):
1. The amber drift line `#FFB23F` is in every world and is always the warmest thing in frame.
2. Near-black ground `#07080B` at the edges of every world.
3. Type: Unbounded 800/900 for numbers and headlines, IBM Plex Mono for labels.
4. One finishing pass on every shot: highlight bloom, vignette, grain.
5. The HUD: crop marks, `A01`, the world code, a mini drift line showing where you are, and a
   palette swatch whose last square is always amber.

**The ending ritual (S18, HOME).** Every video can close in the same place: still water, fireflies,
the amber line running to an amber dawn. The HUD fades away, so the system steps back and it gets
quiet and human. Hopeful words go over it. It's a 12 s template: swap the music for the Astra outro
theme (prompt 3) or your own FL track.

Rules of thumb for the full video: at least half the runtime in W0 (home), at most one world switch
every 6–8 s except in JOKE bursts, and never a world without the line.

## Files

| File | What |
|---|---|
| `shots.py` | the shot list: times in the voice take, world, register, move |
| `posters.py` | PRESS prints, phone screens, floor grid, HUD overlays, captions (Pillow) |
| `worlds.py` | Blender builder: the worlds, the drift line, the camera grammar, one function per shot |
| `sound.py` | synthesised sound design on the cut frames (whooshes, impacts, glitches, risers, shimmer) + the outro pad |
| `assemble.py` | ffmpeg finishing (dither, bloom, grain, HUD + running timecode, world-change flashes), voice + SFX mix at -14 LUFS |
| `PROMPTS.md` | the GPT Astra prompt pack: channel brief, evergreen kit (textures, sound, outro music, icons, HDRI, TouchDesigner, LUT), shot-list director |

## Run it

```bash
export A01_BUILD=~/youtube/a01_v5_build  A01_FONTS=<folder with the .ttf files>
export A01_AUDIO=~/youtube/audio/B_COUSIN_roger_x1.12.mp3
pip install pillow numpy scipy fonttools skia-pathops
python3 posters.py                                       # textures, HUDs, captions, overlap-free fonts
python3 sound.py                                         # sound design + outro pad
for s in S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18; do
  /Applications/Blender.app/Contents/MacOS/Blender -b -P worlds.py -- $s --res 1920x1080 --samples 24
done
python3 assemble.py                                       # -> A01_v5_hook_proof.mp4 + A01_v5_outro_template.mp4
```

Font files (OFL): `Unbounded-500/800/900.ttf`, `PlexMono-500/600.ttf`, from Google Fonts.

S07 (chrome) renders in Cycles for real reflections and uses the Mac GPU (Metal) automatically.
Everything else is Eevee. The cloud proof renders at 960×540 with 8 samples on 4 CPU cores, then upscales. A Mac GPU at
1920×1080 and 24 samples will look noticeably cleaner.

## Before this goes into the real edit

- **Check the numbers.** S06 shows 52.3 → 66.4 (from the Taste Map's rhythm example). Confirm them
  against `~/youtube/scripts/A01_fourteen_points.md`.
- **Voice.** The cuts are timed to `B_COUSIN_roger_x1.12.mp3`. If you re-record the Cousin in your
  own voice, re-time `t0`/`t1` in `shots.py` from the new transcript; the builders use word times
  through `lf()`, so everything else follows.
- **Picks.** The Taste Map picks so far: actor = "my own voice". The others are still open.
