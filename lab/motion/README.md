# Motion Lab

Programmatic motion graphics for the channels, built with [Remotion](https://www.remotion.dev/docs/) 4.0.532:
title cards, animated stats and charts, kinetic type, lower thirds, thumbnails and Shorts, written as React code
that AI coding agents can create and edit. Agent instructions are in [AGENTS.md](AGENTS.md) (Claude Code reads them
through [CLAUDE.md](CLAUDE.md)).

Needs Node.js 18 or newer. The first render downloads Remotion's headless Chrome (about 90 MB) automatically.

## Commands

```bash
cd lab/motion
npm install                         # first time, or after a pull
npm run dev                         # Remotion Studio at http://localhost:3000 (preview, scrub, edit props, render)
npm run new -- MyScene              # new composition in src/compositions, registered in src/Root.tsx
npm run new -- MyShort --vertical   # 1080x1920; also --width, --height, --fps, --seconds
npm run render:sample               # the sample, 1920x1080 at 30 fps, to out/showreel.mp4
npm run render:vertical             # the same sample as a 1080x1920 Short
npx remotion render <Id> out/x.mp4  # any composition
npm run still                       # thumbnail still to out/thumbnail.png
npm run frames                      # a few frames as JPEGs, to check the look without a full render
npm run lint                        # ESLint and TypeScript
npm run upgrade                     # upgrade Remotion (all @remotion/* packages together)
```

## The sample

`Showreel` (15 s, 1920x1080, 30 fps): a kinetic title with a line drawing under it and a typed subtitle, a number
counting up beside a bar chart, shapes springing in around an audio-reactive star, and an end card with a lower
third, joined by fade, slide and wipe transitions, with a synthesised house bed and sound effects on the cuts.

Its size, frame rate and length are props: change them in the Studio's props panel, or pass a JSON file:

```bash
npx remotion render Showreel out/showreel-4k.mp4 --props=props/4k-60fps.json
```

For other compositions, set `width`, `height`, `fps` and `durationInFrames` on the `<Composition>` in `src/Root.tsx`.

## Licence

Remotion is free for individuals and for companies of up to three people; larger companies need a company licence
(https://www.remotion.pro/license). The fonts (OFL 1.1) and audio (synthesised here) in `public/` are free to use.
