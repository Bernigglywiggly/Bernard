# X research: Claude Code, motion design, AI video, YouTube growth (4 Oct 2026)

**How this was made.** The user's X account is new, so this is a search of public X rather than their bookmarks:
about 25 searches of x.com through web search, then the full text of each post, its thread and its X Article read through
the fxtwitter/vxtwitter mirrors (`api.fxtwitter.com/<user>/status/<id>` returns long X Articles in full, which X itself
hides behind a login). Repos and gists linked from the posts were read directly. Like and view counts are as of 4 Oct.
The rules distilled from this live in `CRAFT.md` (repo root); the review process is the `film-critic` skill. Public
web research is in `motion_playbook.md`.

## 1. How the viral "one prompt" Opus 5.5 videos were really made

Opus 5.5 shipped 22 Sep 2026; within days the feed filled with code-rendered showreels, launch films and history films.
The consensus after people reverse-engineered them: **the prompt is 10% of the video, the harness is 90%.**

- **@0xMovez, "How to build a motion design studio with Opus 5.5 (full course)"** (7.6k likes, 1.8M views):
  https://x.com/0xMovez/status/2104216919033192746
  - Opus writes a program, not a video: one `window.seek(t)` function paints any frame; headless Chromium screenshots
    it and ffmpeg encodes. Deterministic: no timers, no CSS transitions, seeded noise (mulberry32), never Math.random.
  - The one-liner ("make a dynamic 15-second motion graphics video that shows what an incredible motion designer you
    are, like it's your showreel for a résumé. go all out.") works because "showreel" is a genre with known rules.
    But hundreds of identical prompts made reels that rhyme ("brief contagion"). It tests the engine, never the idea.
  - **Reference beats description.** Without one, Opus defaults to: centred text, gradient background, everything
    fading in. Feed a frame, a video (ask it to extract frames and describe pacing shot by shot first) or a library
    (have it write `style_guide.md` from your images).
  - **Write the state list, not the vibe.** The most-bookmarked prompt of the week was an XML spec: `<inputs>`,
    `<direction>` (with a Banned list), `<structure>` (beat by beat on a 120 BPM grid), `<build>`, `<gotchas>`, `<start>`.
  - **Closed-form springs** keep motion a pure function of time. When a value changes target several times, add one
    spring per change (`track(t, keys)`), don't restart it. Tab indicators: leading edge stiffer than trailing.
  - **Motion blur**: render 4 subframes per frame and blend with ffmpeg `tmix`; 8 for anything moving over 15 px a frame.
  - **Sound**: measure a supplied track with librosa (beats → state changes, downbeats → big moments, onset peaks →
    SFX), or synthesise score and SFX in code on the same timeline.
  - **Critique loop**: "Open contact.png, strip.png and phone.png. Be a harsh motion director, not a proud author. Score
    1-10: hook in first 2s, readability at phone size, motion quality, variety, composition, brand accuracy, sound sync.
    List the 3 biggest problems with timestamps... Fix them, re-render only the affected seconds." Repeat until all 8+.
  - QA commands: contact sheet `fps=2,scale=270:-1,tile=6x5`; a 12-frame strip around fast moments; a phone test at
    360 px; a loop check with `-stream_loop 1`; a determinism check (render frame 300 twice, compare hashes).
  - **Director's brief for long pieces** (Donald's 9,500-character brief became a 142-second music video with 2.1M views
    after a 12-hour unattended run): logline, references, tools and keys, character bible, beat sheet with a payoff every
    3-5 s, on-screen text rules, workflow gates (plan → rig → stills → animatic → full pass → polish → audio →
    render), critique loop, deliverables. Have Opus write `ANIMATION_GUIDE.md` first so parallel subagents code in one
    style (John Heibel's PDoom repo, 1.1k stars).
  - Generate-then-trace: Seedance renders base shots with real physics, then Opus redraws the whole film in code on top.
  - Repos: JohnHeibel/PDoomVideo, JohnHeibel/ClaudeAnimationBase, buildwithhanif/claude-animation-skill,
    WinterArc21/Battle-of-Austerlitz-Film, guanmo-ai/awesome-ai-motion (464 works, 69 public prompts),
    athemeroy/awesome-opus-5-5-videos (1,500-post dataset with production paths).
- **@rexan_wong, the six steps behind the good ones** (6.8k likes): https://x.com/rexan_wong/status/2103707054108299437
  1) 1-2 reference videos (whatships.com), name the style; 2) install HyperFrames or Remotion; 3) real UI components
  (21st.dev) instead of invented ones; 4) dump brand, real screenshots, reference and a braindump, and ask for **3
  storyboard variants**; 5) one still per scene before anything moves; 6) director notes in camera words ("slow every
  zoom to 0.7x", "hard cut here", "push in on the button"). "Everyone has the same model. The context you give it is
  what makes it look pro."
- **@neil_xbt, marketing version** (cost reality: a 12-hour run cost one builder $2,175 of tokens; a gated 26-second
  trailer cost about $1.18): https://x.com/neil_xbt/status/2103862582041874854. Effort: medium for storyboard and
  stills, max only for the final pass. Banned list: centred headline over gradient, everything fading in, particle
  bursts, glows, lens flares, stock 3D blobs, italic accent words, numbered 01/02/03 labels, dead time over 0.5 s,
  any claim not in the facts list. Vertical cuts: nothing under 28 px, terminal lines under 46 columns, keep clear of
  platform UI top and bottom.
- **@RoundtableSpace / @everestchris6, "the only prompt you need"** (2.2k likes) and its kit **motion-video-kit**
  (vendored here as `.claude/skills/business-motion-film`, MIT): https://x.com/RoundtableSpace/status/2105209785335373948.
  The prompt runs unattended ("i'm away and won't answer questions"), with a facts file as "the only source for any
  number, name or claim", eight motion principles, a storyboard of 12-15 compositions per 30 s, a critic loop where
  "the builder never judges its own work", and a measured quality bar. The 8 principles: foreground becomes the
  transition; one object carries the story; one lead move with layered smaller ones; speed always changes; cuts only
  when size, direction and subject match; every action produces a visible result; type is motion; vary the scale.
- **Remotion's own prompt history** for its launch animation: about 30 tiny prompts, one change each, with exact
  numbers ("rotate Y from 20 to -20 degrees", "one line every 50ms", "fast spring, but no bounce").
  https://gist.github.com/JonnyBurger/5b801182176f1b76447901fbeb5a84ac
- **@deedydas, Opus video workflow** (2k likes): https://x.com/deedydas/status/2104957026199900220. Use Claude Code,
  not the app; animatic before the full video; a critic skill that screenshots and transcribes; **"Explicitly tell it
  to avoid Claudisms like short punchy sentences and a lot of numbers. 'Narrate like a university professor.'"**

## 2. Remotion or HyperFrames

- **@mvanhorn's /last30days verdict** (Reddit, X, YouTube, TikTok corpus): https://x.com/mvanhorn/status/2063624356484501832.
  Both win, for different jobs. HyperFrames for one-off launch reels, captioned clips and explainers (agents write
  HTML natively); Remotion for templated series, 100 variants and code-reviewed work. One-shot is a myth on both:
  "~100 prompts, not 1. the first few iterations all looked like a powerpoint." The AI tell is pacing: "They only know
  constant easing, no tension relief, no sharp cuts, no short fades."
  - Remotion moves: install skills first; first prompt is structure (5-scene script) not visuals; numbers not
    adjectives (80px, not "large"); budget 3-100 prompts; **constants-first code** (every string, colour and timing
    at the top); state the rhythm (where the sharp cut goes, which beat holds).
  - HyperFrames moves: warm-start with material (URL, PDF, CSV, changelog); pacing dialect (fast 0.2 s energy, medium
    0.4 s professional, slow 0.6 s luxury, very slow 1-2 s cinematic); edit like a conversation; **templatise or burn
    tokens** (build once, swap variables); `npx hyperframes lint` and `validate` before rendering; pin fonts (Inter,
    JetBrains Mono).
- **@jake11moran (20M+ views from HyperFrames videos)**: https://x.com/jake11moran/status/2102878602316652828. Context
  dump → ask for 5 story angles → scene table → contact sheet of stills → animate. Real UI only (`npx hyperframes
  capture <url>`), rebuild just the part the story touches about 1.8x bigger. 380+ catalog blocks; library of launch
  videos at github.com/heygen-com/hyperframes-launches.
- **@JJEnglert**: per brand, a reference-frames folder → style guide → 10-15 reusable scene layouts, then "create a
  scene for this script line using layout X". https://x.com/JJEnglert/status/2044889694949826821

## 3. Long-form history and explainer films in code (closest to Money Crimes and The Curve)

- **Battle of Austerlitz (5:01)**, every frame WebGL, every sound synthesised, narration offline (Kokoro TTS):
  https://github.com/WinterArc21/Battle-of-Austerlitz-Film. Real terrain (SRTM tiles), the real sun azimuth, campaign
  map from Natural Earth data, **sound cues derived from the picture** (each gun heard late by distance, panned),
  narration timed beat by beat, painterly Kuwahara filter, canvas weave, grain, 2.35:1 letterbox.
- **History films reportedly made with Fable 5.5 or Opus 5.5** (creator reports, unverified; see the dataset's
  3 Oct update): human progress as one day; 40,000 years of art with one cat; the atomic bomb in 3D (custom renderer,
  synthesised score); the Titanic in one HTML file (Fable 5.1 selected); a Zheng He voyage film from a reused "film
  skill" (55 minutes, 220k output tokens, 2:05). Recurring devices: **one persistent character carried through eras;
  one continuous camera move as the spine.**
  https://github.com/athemeroy/awesome-opus-5-5-videos/blob/main/docs/claude55-update-2026-10-03.md
- **@Mrooo03, a week of Claude video** (Chinese; the most honest field report):
  https://x.com/Mrooo03/status/2105195950142566783
  - Pixel style, flat cut-out and science explainers: 1-2 hours each, publishable. 2D characters: rigging looks like
    puppets; better to have Claude make a motion reference and let Kling's motion control animate the drawing. 3D
    realistic people: 40+ hours for 20 seconds, not worth starting with.
  - Explainer recipe: fix the narration first (15 lines), voice it line by line, trim silences, build a millisecond
    timeline, then animate to it. The first version "looked empty: things small, lots of white space, like a set of
    diagrams". The redo added **foreground, mid and background layers and camera moves in every scene, kept characters
    in the same screen position across transitions, and made big words appear when the narrator hits the keyword.**
  - Check frames from the exported MP4, not the preview (a `visibility: visible` bug only showed in the render).
    Frame 0 was black, so the auto thumbnail was black: start with a designed frame.
  - Music made separately, mixed with automatic ducking under the voice, so changing music needs no re-render.

## 4. Editing and pipelines

- **video-use** (browser-use, open source): the LLM never watches the video, it reads it. Word-level transcript
  (ElevenLabs Scribe) packed into about 12 KB of text, plus a filmstrip-plus-waveform image only at decision points.
  Cuts on word boundaries, 30 ms audio fades at every cut, self-evaluates every cut boundary of the render, max 3
  fix rounds. https://github.com/browser-use/video-use
- **@shivsakhuja, a 45-second explainer ad in 30 minutes** with a skill per step: /plan concept brief → /prepare
  moodboard (character refs, voice samples, storyboard grid) → /generate keyframes → /animate (2-4 preview scenes
  first, then all) → /stitch (ffmpeg, music, SFX, captions, sync to VO) → /watch (review as an editor and as the target
  viewer) → **/learn (extract learnings and update the skills: "a closed loop system")**.
  https://x.com/shivsakhuja/status/2059086745506046329
- Thariq (Claude Code team): Remotion for UI-style videos, Manim for maths and science; his Remotion CLAUDE.md:
  https://gist.github.com/ThariqS/3d446e7c7aa9eb94f468194deb73028f

## 5. AI pictures and clips (Higgsfield, Veo, Seedance, Kling)

- **Veo 3.1** (@AllaAisling): shot type and subject, one main action, one camera move, named light sources ("amber fire
  glow", "red emergency strobes"), and **end with the exact final pose** so the next shot starts there. Repeat
  character details every 2-3 prompts. 60-90 words (under 40 is vague, over 120 confuses priorities). 1-2 actions per
  8-second clip. https://x.com/AllaAisling/status/1980012830507291110
- **Seedance 2.0 film workflow** (@PJaccetturo's breakdown of a 20-minute Higgsfield film made in a 4-day sprint):
  character sheets (front, back, close-ups, props, emotional states); one master location image spun into five angles
  with Nano Banana Pro as the spatial reference, plus "destroyed" and "night" variants; low-poly Blender blocking with
  coloured shapes, then **Claude writes the Seedance prompts from the spatial maps**; context-first prompting
  (establish environment, then close-ups); keep 3-4 of every 20 generations; **one sentence describing each voice in
  every prompt** for voice consistency; pauses between dialogue lines (crowded dialogue speeds up and looks like
  slop); grain, halation and glow in the grade. https://x.com/PJaccetturo/status/2045180152121098407
- Seedance prompt layout (@maarcoofdezz): a [VISUAL] block (camera body, lens, grade, grain, "no CGI"), the action as
  a camera-directed sequence, an [AUDIO] block. https://x.com/maarcoofdezz/status/2078162454744346803
- Nano Banana Pro "cinematic grid" (@techhalla, 1.75M views): generate a grid of angles from one image, then "extract
  the still x.y". https://x.com/techhalla/status/1994541592729063699
- Kling: in image-to-video keep the prompt short; start and end frames do the work. Kling's motion control animates
  a drawing from a reference video.

## 6. YouTube

- **"Inauthentic content"** (formerly "repetitious content", renamed July 2025): mass-produced template videos,
  slideshows with AI narration, interchangeable faceless uploads. A 588k-subscriber channel making $30k a month was
  demonetised in early 2026 with its reach intact. "YouTube is not banning AI. They are banning the absence of a
  creator." Real creators are also being caught by automated enforcement. https://x.com/natecurtiss_yt/status/2056778156808528063
- **Titles**: across 300k viral videos, 6 words or fewer win; about 30 characters gave median views around 65k, about
  70 characters around 40k. Let the thumbnail carry the context. https://x.com/Richard_YTS/status/1997702737056674171
- **Thumbnail text**: 3 words ideal, never over 6; complement the title, don't repeat it; maximum contrast, black
  outline on busy backgrounds, sans serif. https://x.com/theJosephBlaze/status/1716141371747107071
- CTR naturally falls as impressions grow (YouTube Liaison). Spend longer on title and thumbnail (MagnatesMedia).
- **Shorts**: the decision happens in about 1 s; the first frame is the hook; cut any logo or name card from the first
  2-3 s (a 10-20 point gain in average view duration); end feeding back into the start so it loops; 70-85% retention is
  strong.
- Outlier research: find small channels with views far above their subscriber count, then study structure, not
  content (our vidIQ outliers tool does this).

## 7. Claude Code itself

- Skills load about 100 tokens each until needed, so dozens can be installed. "The best skill you'll ever install is
  one you build yourself: if you keep re-explaining a workflow, that's a skill waiting to be made" (@om_patel5).
- Worth having (@nateherk, 400 hours with clients): skill-creator (`/plugin install skill-creator@claude-plugins-official`),
  Superpowers (plan, test, two-stage self-review), GSD (a fresh subagent per task against context rot), /review,
  Context Mode (keeps raw tool output out of context; rebuilds state after compaction).
  https://x.com/nateherk/status/2050941624578920535
- Subagents: one orchestrator owns a written plan; scope each subagent to one job; cap concurrency
  (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, default 20; `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, up to 3); flagship
  model on lead and reviewer, cheaper models on volume work. https://x.com/PrajwalTomar_/status/2084959382341837042
- **Dynamic Workflows** (shipped 28 May 2026; trigger word `ultracode` or "make a workflow that..."): Claude writes a
  JavaScript harness with agent(), parallel() and pipeline(). It fixes three failure modes: agentic laziness, self-
  preferential bias (a builder judging its own work) and goal drift. The pattern for us is **adversarial
  verification**: every factual claim gets its own verifier that knows only the rubric and the source.
  https://x.com/0xCodez/status/2062127385923776831
- Effort: Opus 5.5 defaults to medium (matching Opus 5 at high); xhigh for new films; max for a flagship's final pass.

## 8. What changed in this repo because of this

- `CRAFT.md`: house rules every session reads (authorship against the inauthentic-content policy, narration without
  Claudisms, banned looks, process gates, facts checking, packaging, AI-video prompting, sound). It ends with a
  "Learned on our films" log, and CLAUDE.md points to it.
- `.claude/skills/film-critic`: measure (motion_report.py, loudness, sheets, strips, phone test, frame 0), then a
  fresh critic subagent scores seven areas, and a new critic verifies the fixes. First measurements on our films are
  logged in CRAFT.md.
- `.claude/skills/business-motion-film`: the vendored motion-video-kit (critic prompts, motion grammar, quality bar,
  scripts).

## 9. Still to try

1. Run film-critic on the next How They Profit film and fix its stillness (continuous drift and object motion
   inside each beat).
2. Vary HTP's structure from film 05 (PayPal) onwards: no fixed seven chapters.
3. A remotion-maps or Austerlitz-style terrain map sequence for a Money Crimes film.
4. Test HyperFrames (`npx skills add heygen-com/hyperframes`) on a Curve cold open against our Pillow engine.
5. Add a -1 dBFS true-peak limiter to the master step of all three engines.
6. A "/learn" step after each film: critic findings go into CRAFT.md (now a standing rule).
