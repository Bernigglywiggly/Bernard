# sh_steve · FACTS (checked Sat 10 Oct 2026)

The user's premise: "Games got AI reverse-engineered and you can play as Steve in GTA 5 now."

## Verdict: half true. The clip is real; the description of it is wrong in three ways

| Premise | What's true | Confidence |
|---|---|---|
| "AI reverse-engineered games" | **Partly true.** No game's code was decompiled and merged. Two **unmodified** games (Minecraft Java and GTA V story mode) run **side by side** on one Windows PC, and a mod in each passes data over a local connection every frame. The toolkit behind it *does* ship reverse-engineering tools (Ghidra, ILSpy, Frida, RenderDoc) for other jobs, but the GTA demo is a bridge, not a decompile. | HIGH |
| "AI did it" | **True, with a human.** Claude Code (Opus 5.5) wrote the code over about **two days** of agent sessions, with **one person** directing it and doing the clicks reserved for humans. The creator called it "a few prompts" on X; the agent's own field notes say about two days. | HIGH (field note), MEDIUM ("a few prompts") |
| "You can play it now" | **Mostly false for normal people.** Source code only, on GitHub. You build it yourself, need your own copies of both games, a Windows PC, GTA V **story mode** only (offline; GTA Online is off-limits). There is no download-and-play. | HIGH |
| "World model / AI dreams the game" | **Not this.** No AI generates the frames. The pictures are drawn by the real games. (World models are a separate, real story: see Background.) | HIGH |

**The true story in one line:** an AI coding agent wired two real games together in about two days, open-sourced the toolkit on 30 September 2026, and set off a wave of "impossible" game mash-ups, some real, some unverifiable.

## Who, when, where

| Fact | Value | Source | Conf. |
|---|---|---|---|
| Creator | Rehan Sheikh (@rehan_shei), former CTO of Remade AI, now an engineer at fal | S2, S3 | HIGH |
| Toolkit | **universal-modder**, MIT licence, "skills, tools and a shared knowledge base that let any AI coding agent mod almost any PC game you own" | S1 | HIGH |
| Released | **30 September 2026** (repo created and announced that day) | S1, S2, S4 | HIGH |
| Stars | 4,225 by 6 Oct (S4); **6.1k** stars, 575 forks when opened 10 Oct (S1) | S1, S4 | HIGH |
| Launch post views | about 3.6 million (X) | S2 | MEDIUM |
| Agents supported | Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor, OpenCode | S1 | HIGH |
| Other demos in repo | Terraria "Fal Arsenal" weapons and boss; Age of Empires II civilisation with a robotaxi unit | S1 | HIGH |
| Rules it enforces | single-player or self-hosted only; refuses anti-cheat bypass and cheats against other players; never ships game files or decompiled code | S1 | HIGH |

## How the Minecraft-in-GTA V "passthrough" works (plain words)

| Step | Mechanism | Source | Conf. |
|---|---|---|---|
| 1 | Both games run at once. A GTA script (ScriptHookV, `MCPassthrough.asi`) and a Minecraft Fabric mod talk over a **local WebSocket** (127.0.0.1) | S3 | HIGH |
| 2 | GTA sends Minecraft its **camera position and angle** every frame. Scale: **1 GTA metre = 1 block** | S3 | HIGH |
| 3 | GTA **probes the ground** around the player each tick (VGTimes: **160 probes**); Minecraft turns them into **invisible barrier blocks**, so the blocky hero can walk on GTA's streets | S3 (mechanism), S2 (160) | HIGH / MEDIUM (160) |
| 4 | Minecraft writes its picture **plus a depth map** to shared memory; a **ReShade** add-on paints it into GTA's frame only where GTA has nothing closer (depth test) | S3 | HIGH |
| 5 | Blocks Steve places come back to GTA as **invisible collision props**, so GTA cars and trains hit them | S3 | HIGH |
| 6 | Explosions, arrows and fireworks deal damage across the bridge; GTA police appear in Minecraft as invisible figures that mobs attack | S2, S3 | MEDIUM |
| 7 | Minecraft renders slightly behind GTA's camera, so the compositor **re-projects** the picture to hide the lag (default lag setting 0; "1 frame" mentioned in a gotcha) | S3 | MEDIUM |

### Limits and numbers (for on-screen use)

| Number | Value | Source | Conf. |
|---|---|---|---|
| Build time | about **2 days** of Claude Code sessions, one human | S2, S3 | HIGH |
| Block cap | **400** placed blocks, because around **1,500** objects crash GTA | S2 | MEDIUM (one source) |
| GTA install | 125 GB; the agent wrote most of the code before it finished downloading, testing against a dummy GTA (`fakegta.cpp`, `fakehost.py`) | S2 (125 GB), S3 (dummies) | MEDIUM / HIGH |
| Frame rate / latency | **No published figure.** Don't put an fps number on screen. | S3 | HIGH (absence) |
| Versions | GTA V Legacy (Steam build 3889, story mode), ScriptHookV 3889.0, ReShade 6.8.0, Minecraft Java 26.3 + Fabric | S3 | HIGH |
| Near miss | an auto-click script focused GTA while the user typed elsewhere; GTA nearly went online with mods loaded; the mod loader blocked it | S2, S3 | HIGH |
| Weapons | Steve fights with sword and crossbow; GTA weapons only in an experimental mode | S2 | MEDIUM |

## The wider wave (context, not the lead)

| Event | Date | Real? | Source |
|---|---|---|---|
| Skateboarding in MW2 (chasm) starts the wave | 27 Sep 2026 | real, playable; 7.3M views | S2 |
| Minecraft in Elden Ring (Tobyn Jacobs) | 29 Sep 2026 | real but unreleased; **22.5M views**; internals unknown | S2 |
| universal-modder launch | 30 Sep 2026 | real, open source | S1, S2 |
| "Steve stops a GTA train with a bedrock wall" clip (GameJoker_), "with the help of Claude" | covered 7 Oct 2026 | clip real; how Claude was used not explained | S5 |
| RDR2 Minecraft TNT, Quake-in-Skyrim | early Oct | **UNVERIFIABLE** (no code, tiny accounts) | S2 |
| INXANITY launcher: "AI game mashups in one click" | Oct 2026 | **UNVERIFIED** marketing claim; not checked | S6 |

**Key distinction (from S2):** none of the projects with known internals merges two games' code. They either run side by side and exchange data, or one game is rewritten from scratch.

## Background: the real "AI generates the game" story (world models), for contrast only

| System | Date | Numbers | Source | Conf. |
|---|---|---|---|---|
| Google GameNGen (DOOM) | Aug 2024 | about 20 fps on one TPU; memory about 3 s | S7 | HIGH |
| Decart + Etched Oasis (Minecraft-like) | 31 Oct 2024 | 20 fps on one H100; web demo 360x360 px; hallucinations | S8 | HIGH |
| Google DeepMind Project Genie (Genie 3) | 29 Jan 2026 to AI Ultra subscribers | n/a | S9 | MEDIUM |

No source links any world model to the Steve-in-GTA clips. Don't conflate them on screen.

## Sources (opened 10 Oct 2026)

- S1 GitHub, rehan-remade/universal-modder README · https://github.com/rehan-remade/universal-modder
- S2 VGTimes, "Minecraft in Elden Ring and TNT in RDR2: The Wild AI Mashups That Broke the Internet — What's Real and What You Can Download" · https://vgtimes.com/articles/169886-how-ai-game-mashups-work.html
- S3 universal-modder field note, `knowledge/games/gta-v/minecraft-passthrough.md`, author @rehan_shei, dated 2026-09-30 · https://github.com/rehan-remade/universal-modder/blob/main/knowledge/games/gta-v/minecraft-passthrough.md
- S4 LaoZhang blog, "Universal Modder for Claude Code: Install, fal Costs, Limits" · https://blog.laozhang.ai/en/posts/universal-modder (stars 4,225 on 6 Oct; fal sprite about $0.21)
- S5 GamingBible, Sam Cawley, "Minecraft's Steve has finally done what GTA 5 players have tried for years" · 7 Oct 2026 · https://www.gamingbible.com/news/gta-5-minecraft-mod-does-impossible-124923-20261007
- S6 INXANITY launcher · https://www.inxanitylabs.com/ (not opened; claim unverified)
- S7 GameNGen, "Diffusion Models Are Real-Time Game Engines" · https://huggingface.co/papers/2408.14837 · The Register 28 Aug 2024 https://www.theregister.com/2024/08/28/google_doom_ai/
- S8 Oasis coverage · https://www.3dtested.com/video-games/ai-powered-minecraft-runs-without-a-game-engine-game-rendered-in-real-time-at-a-continuous-20-fps · https://charonhub.deeplearning.ai/ai-creates-an-interactive-minecraft-like-world-in-real-time/
- S9 Wikipedia, "Genie (AI model)" · https://en.wikipedia.org/wiki/Genie_(AI_model)
- Also seen: hardware.com.br, vidaextra.com, cybersport.metaratings.ru (2 Oct report of the footage), techora.ru (dated 30 Sep), GitHub fork utku6767/Gta-V-Enhanced-Minecraft-Steve-Passthrough (a port to GTA V Enhanced; not opened).

## Not checked / to verify before render
- The 160 probes, 400-block cap, 1,500-object crash and 125 GB figures come from VGTimes only: open the field note's full text or Rehan's X thread and confirm before they go on screen.
- The 3.6M view count on the launch post: confirm on X.
- Disclosure: The Curve is made with Claude, and this story is about Claude Code. Say so in the description (CRAFT s.5).

## IP note
GTA, Rockstar, Minecraft, Mojang and Steve are third-party IP. We name them in narration and captions (factual reference) but **draw none of them**: no game footage, logos, the Steve character, GTA's map or HUD. Our figure is an original cube-headed voxel robot with a visor slit; our city is generic type.
