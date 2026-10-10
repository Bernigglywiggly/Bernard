# Maps & Power: style directions (10 Oct 2026)

Same scene each time: the Hormuz narrows, both lanes, 3 October attack pins, the "8 ships" card. Rendered by `style_frames.py`. Board: `sheet.jpg`.

Palette, all on pure black: cyan `#3DFFF2` water/nav · magenta `#FF2BD6` Iran · yellow `#E6FF2E` oil · orange `#FF6A1A` danger · violet `#A77BFF` data/sources · green `#39FF88` Oman.

| Direction | Palette (hex) | Texture | Where to use | Motion | Risk |
|---|---|---|---|---|---|
| **A Highlighter** (his brief) | All 6 above, one meaning each | Flat ink, soft bloom, streaky marker swipes behind black words | Default map look. Any beat that names places | Swipes wipe on left to right (marker speed), bloom breathes in | Six colours at once gets loud. Cap it at 3 per frame |
| **B Topographic** | Sea `#5FFFF4`→`#3DB8FF`→`#5A6BFF`→`#9B4BFF` · land `#39FF88`→`#E6FF2E`→`#FF9A1A`→`#FF4A3A` | Real contours: NOAA ETOPO 2022 15″ (public domain), sea every 20 m, land every 200 m | Geography chapters: "the gap", depth, mountains, chokepoints | Contours draw on from deep to shallow; slow push-in | Busy behind type. Labels need halos. Other regions need their own ETOPO subset (free, ~2 MB) |
| **C Neon** | Tube colours from the palette, white-hot cores | Glass tubes: core + gas + 5-layer halo; unlit glass stays faintly visible | Events and danger only: attacks, closures, deadlines | Flicker-on with stutters, mains-hum shimmer, a faulty letter that buzzes, sparks on impact (`C_neon.mp4`, has audio) | Overuse makes it a cliché. Keep it to 1–2 beats per chapter |
| **D Fluoro Riso** (my pick 1) | Pink `#FF48B0` · blue `#3D8BFF` · yellow `#FFE800`, screen-mixed | 3 halftone plates at 75°/15°/0°, misregistered 2–3 px, ink dropout, paper grain. Dot density = real depth/height | Data cards, explainers, the thumbnail. Gives the channel a tactile signature | Plates slide into register on entry; dots grow from 0 | Halftone shimmers when the camera moves. Lock it to the screen or use stills |
| **E Thermal Flow** (my pick 2) | Volume ramp `#2B3BFF`→`#7A4BFF`→`#FF2BD6`→`#FF6A1A`→`#E6FF2E`→`#FFFDF0` | Particles splatted into a density field. Colour = how much oil shares the water, so the pinch runs white-hot | Any "what flows" beat: oil, LNG, ships, money | Continuous advection, seamless loop (`E_flow.mp4`) | Flow paths are schematic and must be captioned as such. Feeder split is illustrative |
| **F The System** (recommended) | Black base · the 6 highlighter inks as the colour language · one hero colour per chapter | Texture follows meaning: contours = terrain, highlighter = places, particles = flows, neon = events, halftone = data | The whole channel. Each chapter gets a hero colour (October = orange) and everything else steps back | Each texture keeps its own motion from A–E | Needs discipline. One hero colour per chapter and at most 2 textures loud in any frame |

Rules: anything schematic says so on screen. Relief is real or it isn't shown. Coasts are Natural Earth 10m. Borders are approximate (Musandam/UAE line drawn Sha'm→Dibba).
