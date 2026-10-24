# Channel 5 · What if (science and scale, first person)

## The format (3 Oct 2026, from what's working on TikTok)
The user sent nine TikToks that were "popping off"; four were @pov.what.if0's "What if...?" POV films (Earth into a
black hole, Yellowstone erupting, a 1,700-ft wave, shrinking forever), 64-102 s each. What makes them work:
- **One fixed first-person shot** that escalates for over a minute (over 60 s also qualifies for TikTok's Creator
  Rewards) to a climax.
- **A live readout top left:** a small label, a big number counting up or down (distance, height, time), a small
  sub-line.
- **The question as an elegant title**, then **one short italic line per beat** ("It has a ring now.").
- No narration; music and sound only.

**How ours is different (the user: "way more surreal 4k, unreal engine visuals... way more dramatised"):**
- **Visuals:** cinematic, photoreal AI frames instead of low-poly 3D. Eight GPT Image keyframes share one first-person
  view, and Kling 3.0 clips run from one keyframe to the next, so the film reads as one continuous shot.
- **Real physics in the readout:** two lines that matter (for the black hole, distance and tides as a multiple of the
  Moon's); the working is kept in each film's `SCIENCE.md`.
- **Our own sound design:** deep layered bass that phones can actually play, with a few big moments only (the "Fire
  Force" drop is saved for the climax, after half a second of near-silence). Every film also ships silent plus the
  sound on its own, so a trending TikTok sound can go on top.
- **Our own type:** IBM Plex Serif italic for the title and captions, IBM Plex Mono and Serif for the readout.

## How a film is made (about 130 Higgsfield credits, 70 s)
1. Beats and science: the escalation in 7 steps, captions, and the readout numbers (`lab/motion/src/whatif/<film>.ts`
   holds the captions and the readout as a function of time; `public/whatif/<film>/SCIENCE.md` the working).
2. Keyframes: GPT Image 2.5, high, 2k, 9:16. Make frame 0, then frames 1-7 with frame 0 as the image reference ("the
   exact same view, later..."). Check the sheet: a frame that undoes the story (the ground back after it's gone) is
   regenerated with "no ground, no tree".
3. Clips: Kling 3.0 pro, 10 s, sound off, `start_image` = keyframe i, `end_image` = keyframe i+1 (15 credits each; 4K
   mode is 60, so generate in pro and upscale only if needed).
4. Sound: `python3 lab/whatif/sound_<film>.py` (bed, hits on the beats, a riser and gap into the drop, a void, a
   resolve; mastered to about -16 LUFS).
5. Assemble and render: the reusable Remotion template `lab/motion/src/whatif/WhatIfPov.tsx`;
   `npx remotion render WhatIf-<Film> out/whatif_<film>.mp4`; the silent copy with `ffmpeg -an -c:v copy`.

## Films
| # | What if... | Status | Files |
|---|---|---|---|
| 01 | Earth fell into a black hole? (70 s) | Made 3 Oct | `lab/motion/src/whatif/blackhole.ts`, `public/whatif/blackhole/`, `lab/whatif/` |

## Next (each with a readout that's real physics)
The Sun vanished (light delay, temperature), the Moon fell (distance, tide height), you fell into Jupiter (depth,
pressure, temperature), a hole through the Earth (depth, speed, temperature), a mile-wide asteroid hit the ocean (wave
height), a neutron star passed by, Earth stopped spinning (remake of short 01), the magnetic field vanished, a
gamma-ray burst.
