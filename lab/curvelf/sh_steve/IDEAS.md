# sh_steve · IDEAS (10 Oct 2026)

Facts: `FACTS.md`. Rule for every concept: we name the games in words, we never draw their characters, logos, maps or
HUDs. Our cast: **VOXEL** (an original cube-headed robot with a visor slit, not Steve) and **THE CITY** (generic
buildings made of monospaced type). Ranked by expected retention x clippability x how fast we can build it in `flow.py`.

| # | Concept | Hook (first 1-2 s: line + picture) | Payoff | Loop ending | Retention | Build cost |
|---|---|---|---|---|---|---|
| **1** | **TWO GAMES, ONE SCREEN** (prototyped: `script.py`) | "That viral clip of Minecraft's hero in GTA Five is really two games running at the same time." Picture: the screen torn down the middle, voxel hero left, type city right, a seam of live data between | The four-step bridge drawn as diagrams: camera pose out, ground probes in, invisible blocks under his feet, depth-tested picture back. Verdict: glue, not fusion | Last line ends on "...two other games running at the same time", the hook's own words; the last frame is the torn screen again | HIGH: myth-bust in 3 s, a mechanism people can repeat in the comments | LOW (existing kinds + 5 drawn PNGs) |
| 2 | **THE INVISIBLE FLOOR** | "He's standing on a street he can't see." Picture: the voxel hero floating, then a grid of ghost cubes fades in under his feet | GTA probes the ground every tick (160 points, VERIFY), the block world turns each into an invisible block. Show the probe dots raining down like sonar | The ghost floor ripples out to fill the frame; a new hero drops onto it = frame 0 | HIGH: a single "wait, what?" image, the most clippable mechanic | MEDIUM: wants a drawn clip (mp4) of probes |
| 3 | **400 BLOCKS** | "Place four hundred and one blocks, and the city dies." Picture: a counter ticking 398, 399, 400 on a wall of cubes | Why: each block becomes an invisible prop in GTA, and around 1,500 objects crash it (VERIFY). A tidy lesson in how a bridge has a budget | Counter resets to 0, first cube placed = frame 0 | HIGH: countdown tension; one number to remember | LOW (`num` + `split` + one drawn wall) |
| 4 | **TWO DAYS** | "An AI wrote this mod while the game was still downloading." Picture: a 125 GB progress bar crawling, a code editor racing beside it | It tested against a fake GTA (`fakegta.cpp`) before the real one arrived; one human, about two days | Progress bar hits 100% just as the line loops to "while the game was still downloading" | HIGH for the AI-curious audience; a strong title ("It coded before the download ended") | LOW |
| 5 | **REAL, FAKE, OR UNRELEASED** | "Three viral game mash-ups. One you can build, one nobody can download, one nobody can trace." Picture: three cards face down | Flip: GTA (open source), Elden Ring (22.5M views, unreleased), RDR2 TNT (no code, tiny account). Teaches viewers how to check | Cards shuffle face down again | HIGH: a quiz format holds to the reveal; strong comments | LOW (`list` / `split`) |
| 6 | **THE NEAR MISS** | "The AI almost took a modded game online." Picture: a cursor jumping to the wrong window | An auto-click script focused GTA while the user typed elsewhere; the mod loader blocked online play. Why the toolkit asks before driving input | Cursor returns to the start position | MEDIUM-HIGH: tension, a real safety story | LOW |
| 7 | **DEPTH IS THE TRICK** | "Why doesn't he walk through the lamp post?" Picture: voxel hero half-hidden behind a pole | Each pixel carries a distance; the city paints the block world in only where nothing of its own is closer. Show a depth map as a heat ramp sliding across | Pole slides back in front = frame 0 | MEDIUM: nerdy, very rewatchable for gamers | MEDIUM (two layered PNGs + a mask reveal clip) |
| 8 | **NOT A DREAM** | "Some AIs dream a game frame by frame. This isn't that." Picture: a frame dissolving into noise, then snapping to a crisp drawn frame | Contrast: world models (Oasis, about 20 fps on one H100, it forgets the hole you dug) vs this bridge, where the real games draw every pixel | Noise dissolves back to frame 0 | MEDIUM: clarifies the confusion behind the user's premise; good second Short | MEDIUM: a noise-to-frame clip |
| 9 | **THE PREDICTION GRID** ("go crazy") | "Every frame, two computers argue about where the camera is." Picture: two crosshairs drifting apart, a lag counter flickering 0 / 1 frame | Re-projection explained as a game of catch-up: the block world draws a beat late, the compositor shifts its picture to match | Crosshairs snap together on the loop point | MEDIUM: mesmerising visual, harder to say plainly | HIGH: needs a new animated kind |
| 10 | **ANY TWO GAMES** | "Pick two games. An AI can now try to stitch them together." Picture: a slot machine of game genres made of type | The toolkit: recon, read the code, build, test, field note. What it refuses (cheats, anti-cheat, online) | Slot machine spins again | MEDIUM: broad; risks sounding like an ad | LOW |

**Why #1 first:** it corrects the premise the audience arrived with (the most surprising true thing), carries the
whole mechanism in 40 s, and its closing words loop to its opening ones. #2, #3 and #5 are the next three to make;
together they're a 4-Short week that never repeats a shape (CRAFT s.1).

## Visuals the engine can't express yet (describe, don't build)
- **Torn screen with a live seam** (#1, #9): two halves drifting apart with packets of type (`x 412.6 y 88.0 yaw 174`)
  flying across the gap. Today: a still PNG of the torn screen; the packets would need a `clip` mp4 drawn in code.
- **Probe rain** (#2): dots falling and freezing into ghost cubes. Would be a drawn `clip` (mp4 into `src/ai/`); the
  engine already plays `clip` frames ping-ponged at 12 fps, which suits a looping scan.
- **Counter on a wall** (#3): a ticking number that is part of the picture; `num` can show a static figure only.
- **Depth heat-ramp wipe** (#7): a mask sweep between two pictures. Needs a new kind or a drawn clip.

## Packaging (CRAFT s.6)
- Title for #1: **"It's Two Games, Not One"** (24 chars). Alt: "Minecraft in GTA, Explained".
- No thumbnail text needed for a Short; frame 0 is the torn screen.
- Description must say: built with Claude Code; The Curve is also made with Claude; sources S1-S5 from FACTS.md.

## Prototype status (script.py, 10 Oct)
- Lint: 0 flags. Estimated 44.5 s to the last word (47.4 s with tail). Not voiced.
- Stills: `flow/qc/sheet_vert.jpg` (8 frames, true 9:16; the engine's own `flow/qc/sheet.jpg` squashes verticals to 16:9).
- Seen on the stills: (1) at 0.0 s the camera hasn't settled, so the robot is cut at the left edge; the same picture is
  framed correctly at 42 s. Frame 0 is the hook, so fix before render (start the camera on place 0, or move VOXEL
  right in h01). (2) h04's label overlaps the top plate a little. (3) `flow.py short` is built to cut a Short out of a
  long film and ends on a "WATCH THE FULL FILM" card; a standalone Short needs that card off (or a different end card).
- Before render: confirm the 400-block figure (one source), write the description disclosure, run film-critic.
