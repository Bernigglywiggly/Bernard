# Motion Lab: instructions for AI agents

This folder is a [Remotion](https://www.remotion.dev/docs/) 4.0.532 project (React + TypeScript) for programmatic
motion graphics on the channels: title cards, animated stats and charts, kinetic type, lower thirds, thumbnails,
explainer inserts and Shorts. Every frame is a function of the frame number, so a video is code you can diff,
re-render and re-use.

Remotion's official Agent Skills are installed in `.agents/skills/` (linked into `.claude/skills/`). Load
`remotion-best-practices` before writing Remotion code; it routes to the rest (markup, transitions, audio, captions,
rendering, interactivity). Update them with `npm run skills:update`.

## Commands

Run everything from `lab/motion`.

| Task | Command |
| --- | --- |
| Install (first time, or after a pull) | `npm install` |
| Open the Studio (live preview, scrub, edit props, render button) | `npm run dev`, then http://localhost:3000 |
| Open one composition | http://localhost:3000/Showreel (any composition id) |
| New composition | `npm run new -- MyScene` (add `--vertical`, `--width`, `--height`, `--fps`, `--seconds`) |
| Render the sample to MP4 | `npm run render:sample` (writes `out/showreel.mp4`) |
| Render any composition | `npx remotion render <Id> out/<name>.mp4` |
| Render a vertical Short of the sample | `npm run render:vertical` |
| Render a still (thumbnail) | `npm run still`, or `npx remotion still <Id> out/<name>.png --frame=<n>` |
| Check frames as images | `npm run frames`, or `npx remotion render <Id> out/frames --sequence --frames=0,45,90 --image-format=jpeg` |
| Type-check and lint | `npm run lint` |
| Upgrade Remotion | `npm run upgrade` (keeps every `@remotion/*` package on one version) |

Only render to MP4 when asked; otherwise show work in the Studio. To check your own work, render a few frames as
JPEGs and look at them.

## Layout

```
src/
  index.ts            registerRoot (do not edit)
  Root.tsx            every <Composition>/<Still>; npm run new adds to it at the marker comments
  theme.ts            colours and fonts (loads public/fonts); use theme.colors / theme.fonts, never hard-code new ones
  lib/anim.ts         CLAMP, EASE_OUT, EASE_IN_OUT, SPRING, sec(), unitFor(), useUnit()
  lib/audio.tsx       AudioLevelProvider + useBass() (audio-reactive), beatFrame() (cut on the beat)
  components/         reusable, Studio-editable building blocks:
                      Background, KineticTitle, TypeOn, CountUp, BarChart, Chip, LowerThird, DrawLine, PulseRing
  scenes/             full-frame scenes made from components (IntroScene, StatScene, ShapesScene, OutroScene)
  compositions/       finished videos and stills (Showreel, Thumbnail, and whatever npm run new creates)
public/               assets, referenced with staticFile("fonts/..."), staticFile("audio/..."), staticFile("sfx/...")
props/                JSON prop files for --props (vertical.json, 4k-60fps.json)
scripts/              new-composition.mjs and its template
out/                  renders (git-ignored)
```

## Rules

- Drive all motion from `useCurrentFrame()` with `interpolate()` or `spring()`. CSS transitions, CSS animations,
  `setTimeout` and `Math.random()` do not render correctly. For randomness use `random(seed)` from `remotion` or
  `noise2D()` from `@remotion/noise`.
- Time in seconds: `0.5 * fps`, `sec(2, fps)`. Never hard-code frame numbers that assume 30 fps.
- Size in units: `const u = unitFor(width, height)` (or `useUnit()`), then `fontSize: 120 * u`, so layouts hold at
  1920x1080, 1080x1920 and 4K. Check `width >= height` to switch rows to columns on vertical formats.
- Keep the `interpolate()` call inline in the `style` prop and use the `scale`, `translate` and `rotate` properties
  (not `transform` strings): the Studio can then edit the keyframes.
- Clamp interpolations (`...CLAMP` or both `extrapolate*: "clamp"`). Ease entrances with `EASE_OUT`, scene changes
  with `EASE_IN_OUT`; use `output: "perceptual-scale"` when animating `scale`.
- New visual components follow `components/KineticTitle.tsx`: an inner component that takes and forwards `style`,
  wrapped in `Interactive.withSchema({ ..., wrapInSequence: true })` with a schema for its editable props. Number
  fields in a schema need `hiddenFromList: false`. Put timing props (`name`, `from`, `durationInFrames`,
  `premountFor={fps}`) straight on the component instead of wrapping it in a `<Sequence>`.
- Register a substantial scene as its own composition too (see the `Showreel-Scenes` folder in `Root.tsx`) so it
  can be opened on its own timeline. Keep `defaultProps` as an inline object on the `<Composition>`.
- Assets live in `public/` and are loaded with `staticFile()`. Media: `<Audio>`/`<Video>` from `@remotion/media`,
  images with `<Img>` or `<CanvasImage>` from `remotion`. Add `premountFor={fps}` to timed media.
- Add `@remotion/*` packages with `npx remotion add <package>` so the versions match.
- Fonts come from `public/fonts` through `theme.ts`, so renders work offline. `@remotion/google-fonts` is installed
  too, but it needs internet at render time.
- Text sizes at 1080 px on the short side: headlines at least 84 px, important supporting text at least 44 px.
  Keep key content 100 px from the edges.

## How to make things

**A scene.** Copy the shape of `scenes/IntroScene.tsx`: an `AbsoluteFill` root that forwards `style`, a
`<Background />`, then components placed with flexbox or absolute positions. Stagger entrances by giving each
component a `from` (for example `from={Math.round(0.4 * fps)}`).

**A multi-scene video.** Use `<TransitionSeries>` from `@remotion/transitions` like `compositions/Showreel.tsx`:
`<TransitionSeries.Sequence durationInFrames=... premountFor={fps}>` per scene and
`<TransitionSeries.Transition presentation={fade() | slide() | wipe()} timing={linearTiming(...) | springTiming(...)} />`
between them. Each transition overlaps its neighbours, so the video is (sum of scenes) - (sum of transitions) long.

**Typography.** `KineticTitle` (words rise one by one; `accentWord` colours one word), `TypeOn` (typewriter with
caret), `CountUp` (numbers count up, tabular figures), `Chip` (small label), `LowerThird` (name and detail). For
per-letter effects, split the string and stagger each `<span>` the same way `KineticTitle` staggers words. To fit text
to a width, use `fitText()` from `@remotion/layout-utils`.

**Graphics.** `@remotion/shapes` (`Circle`, `Rect`, `Triangle`, `Star`, `Polygon`, `Pie`, ...) for vector shapes;
`DrawLine` (built on `evolvePath()` from `@remotion/paths`) to draw any SVG path on; `BarChart` for animated bars;
`Background` for the house grid and glow.

**Audio and sync.**
- Music: `<Audio src={staticFile("audio/....mp3")} volume={(f) => interpolate(f, [...], [...], CLAMP)} />`. The volume
  callback gives fades and ducking under a voice.
- Sound effects: `<Audio from={frame} src={staticFile("sfx/whoosh.mp3")} volume={0.45} />` on each cut or hit.
  The Showreel computes its cut frames in `showreelTimeline()`.
- Audio-reactive motion: wrap the video in `<AudioLevelProvider src=...>` (outside any sequence) and call `useBass()`
  inside any component (see `PulseRing`).
- On the beat: `beatFrame(n, bpm, fps)` gives the frame of beat `n`. The sample bed is 124 BPM, starting on a beat.
- Narration: put the voice file in `public/audio`, add it as `<Audio>`, and time scenes from its word timestamps. The
  Python pipeline's Whisper output (`lab/longform/tools/words.py`, `[word, start, end]` in seconds) converts to frames
  with `Math.round(start * fps)`. For captions, load the `remotion-captions` skill.

**Format, frame rate and length.** For a new composition, change `width`, `height`, `fps` and `durationInFrames`
on its `<Composition>` in `Root.tsx` (or pass flags to `npm run new`). The Showreel takes them as props instead: edit
them in the Studio's props panel, or render with `--props=props/vertical.json` or your own JSON file; its scenes
stretch to the requested length.

**Thumbnails.** `compositions/Thumbnail.tsx` is a `<Still>` (one frame, no animation): `npm run still`.

## House style and assets

- Look: black background, turquoise accent `#3FE6D8`, gold labels `#F2D9A0`, Michroma for display, Inter Tight for
  body, IBM Plex Mono for labels. These match The Curve's Python engine (`lab/curvelf`), so Remotion inserts can sit
  inside a Curve film.
- Audio in `public/` was synthesised in this repo (`lab/music/beds.py`, `lab/sfx/palette.py`): nothing to license,
  nothing for Content ID to claim. Do not use the meme sound effects from remotion.media in channel videos.
- No real people's likenesses or voices; no logos or brand marks unless the user supplies them.

## Hand-off to the rest of the pipeline

- A finished MP4 from `out/` can be cut into a film by the Python engines (`lab/curvelf`, `lab/longform`).
- For overlays with transparency, render ProRes 4444 from a composition without a background:
  `npx remotion render <Id> out/<name>.mov --codec=prores --prores-profile=4444 --pixel-format=yuva444p10le`.

## Licence

Remotion is free for individuals and for companies of up to three people; larger companies need a company licence
(https://www.remotion.pro/license).
