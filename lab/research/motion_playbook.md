# Motion and video playbook: Claude Code, Remotion, HyperFrames, AI video (researched 4 Oct 2026)

Public research on how people make motion graphics and video with Claude Code, boiled down to what applies to this
studio (`lab/motion` Remotion project, the `ch2` and `curvelf` engines, Higgsfield for pictures and clips). The user's own
X likes and bookmarks are a separate pass (run locally with Claude in Chrome); its notes go in `x_notes.md` beside this.

## 1. How the good results are made (the shared pattern)

1. **Taste, not code, is the bottleneck.** Collect references first (Pinterest "infographic", "data visualization",
   "title card design"; screen-grabs of YouTube explainers) into a folder, then ask Claude to recreate one.
2. **Give the reference with minimal instructions, then iterate.** "Use this image as inspiration to create a new
   composition", then plain-English edits ("make this an upward graph to 12,500 subscribers"). Front-loading a long spec
   gives more room for misreading than a first pass plus corrections.
3. **For video references, extract frames with FFmpeg** (Claude can't watch video): "Use FFmpeg to analyse the video in
   my Animation Inspiration folder and create a similar animation where words come in one by one."
4. **Proof as stills before rendering.** Build every graphic as one HTML (or Remotion still) storyboard at production
   size, check it, then render frames. We already do this with contact sheets; keep doing it.
5. **Brief Claude like a motion designer.** A CLAUDE.md that reads as a creative brief (brand colours, fonts, timing
   defaults, caption style, QA checkpoints) makes every edit consistent without repeating it.
6. **Be exact about time.** "Title at 0:02, hold 3 s, fade out by 0:05" beats "add a title".
7. **Describe the look, not the technique.** "Blur the background slightly so the text pops."
8. **Correct once, then make it a rule.** After a correction: "Update CLAUDE.md so you don't make that mistake again."
9. **Batch with templates.** Once a look works, encode it as a template and apply it to every video in a folder.

## 2. Remotion specifics (our `lab/motion`)

- Official skills (installed here): `remotion-best-practices` (routes to the rest), `-create`, `-markup`, `-studio`,
  `-render`, `-maps` (animated routes, GeoJSON, 3D flyovers), `-captions`, `-interactivity` (Studio-editable props),
  `-docs`, `-upgrade`, `-multimedia`. Start prompts with "Use the Remotion best practices skill."
- **Every animation from the frame number**: `useCurrentFrame()` + `interpolate()` / `spring()`. CSS transitions,
  `setTimeout` and `requestAnimationFrame` flicker in renders.
- Spring defaults: mass 1, stiffness 100, damping 10. Useful presets seen in good work:
  - kinetic word stagger: 8 frames apart, `{damping: 12, stiffness: 200, mass: 0.5}`
  - bar-chart reveal: 10-frame stagger, `{damping: 15, stiffness: 80}`
  - list items: 0.4 s stagger, `{damping: 15, stiffness: 120}`
  - logo or title settle: `{stiffness: 80, damping: 12}`, scale 0.5 to 1
  - stat card slide-up: `{damping: 14}`; CTA pulse: scale 1.00 to 1.03 on a 60-frame sine loop
- Fonts via `@remotion/google-fonts` `loadFont()`; images via `<Img>` from `public/`; layout with `<AbsoluteFill>` +
  flexbox and few elements; `npx remotion compositions` to check ids; draft renders at 720p, `--concurrency=8`.
- Masters for editing: ProRes `.mov` at top quality; H.264 MP4 for upload.

### Prompt templates that work (fill the brackets)

Text intro:
```
Create a [N]-second video at [W]x[H], 30fps. Background: solid [hex]. Text: "[TEXT]" in [colour], [weight], [size]px,
centred. 0.0s: opacity 0, scale 0.8. 0.0-0.8s: spring in to scale 1. Hold. Last 1s: fade to 0.
```
Counter: `Count from [start] to [end] over [N] s with interpolate, formatted as [$ / % / commas].`
Explainer Short: `Use the Remotion best practices skill. Create an educational explainer (1080x1920, 30fps, 30 s) that
teaches [TOPIC]. Research and show me the script before coding; 5 scenes; SVG animation; spring motion.`
Data dashboard: `I've placed data at public/data.csv. Create an animated dashboard (1080x1920, 30fps, 15 s): KPI cards,
bar, donut and line charts from the real data.`
Talking-head overlay: `Play public/avatar.mp4 full frame as the background; add transcribed captions synced to speech,
an animated title and badges; never crop the footage.`
Map route (new for us): `Use remotion-maps. Animate a route from [A] to [B] and make the camera follow it.`

## 3. HyperFrames (HeyGen, open source): HTML to MP4

- Write an HTML page with CSS/GSAP/Lottie/Three.js animation; timing comes from data attributes (start, duration,
  track); a headless browser captures it frame by frame into a deterministic MP4. Node 22+ and FFmpeg locally.
- Ships agent skills for: product launches, website-to-video, faceless explainers, captions and motion graphics,
  music-to-video, slideshows. Repo: https://github.com/hyperframes/hyperframes
- Fit for us: our engines already render frames in Python; HyperFrames is worth a test for web-native looks (GSAP
  kinetic type, Three.js) where Pillow is clumsy. Remotion stays the main motion tool.

## 4. AI video generation prompts (Higgsfield: Kling, Veo, Seedance)

- Formula: **[camera move + speed] + [subject and action] + [what the move reveals] + [mood/pacing]**, or Subject +
  Environment + Action + Lighting + Style + Camera.
- One shot type, one move, one lens per clip ("medium close-up, slow dolly in, 35mm"); two or three modifiers max.
- Multi-beat clips: "starts... then... as..." act as edit points; keep to two or three beats.
- Strengths: Seedance 2.0 for tracking and orbits; Veo 3.1 for handheld and dialogue realism; Kling for standard
  cinematography terms.
- Moves that read well: slow dolly in (tension), pull-back reveal, 180-degree orbit, side tracking, crane up (reveal),
  FPV dive (energy), handheld follow (documentary), whip pan (transition).
- For Money Crimes reconstructions: handheld follow + period lighting + "documentary realism"; never show a real
  person's face (our rule).

## 5. Faceless channel retention (applies to all three channels)

- Hook in the first 3 s for Shorts, about 8 s for long films: a question, a surprising number, a curiosity gap. A
  visual change inside the first 5 s helps.
- A pattern interrupt about every 60 s (new visual, question, section card); a forward tease every 60-90 s ("in a
  minute: the trick that made it work").
- Cut narration pauses over ~0.5 s (our `voice_hf._squeeze` does this for Seed Audio).
- Script from a structure that already works, then fill it; strip filler, add specific numbers and examples.

## 6. Claude Code habits worth copying (from the Claude Code team)

- Plan mode first for anything big (shift+tab twice); agree the plan, then let it run. Re-plan when it goes sideways.
- Keep CLAUDE.md in git and add a line every time Claude gets something wrong.
- Turn repeated workflows into skills or slash commands (a "new HTP film" skill would fit our ch2 engine).
- Give Claude a way to check its own work (contact sheets, ffprobe, frame grabs); it is the biggest quality lever.

## 7. Next experiments for this studio

1. A `remotion-maps` route animation for a Money Crimes film (Lustig Paris to New York; Ponzi Italy to Boston).
2. A Remotion data-dashboard insert for How They Profit (company figures from the 10-K as CSV).
3. One HyperFrames test: a GSAP kinetic-type cold open for The Curve, compared with our Pillow version.
4. A `motion-design-critique` style QA pass (LobzyJay/motion-design-with-claude, MIT) on our timing: does everything
   enter at once, is anything linear?

## Sources

- Remotion agent skills: https://github.com/remotion-dev/skills
- Louise de Sadeleer, custom motion graphics with Claude Code + Remotion: https://louisedesadeleer.substack.com/p/how-i-make-custom-motion-graphics
- 5 Claude Code video prompts: https://www.sabrina.dev/p/5-insane-claude-code-video-prompts
- Motion graphics guide (templates, timing table, mistakes): https://github.com/ThamJiaHe/claude-code-handbook/blob/main/docs/motion-graphics-claude-remotion-guide.md
- Motion design skills for AE and Blender: https://github.com/LobzyJay/motion-design-with-claude
- Claude Code video editing workflow: https://www.mindstudio.ai/blog/claude-code-video-editing-motion-graphics
- HyperFrames: https://github.com/hyperframes/hyperframes, https://www.heygen.com/research/html-to-video
- Camera prompts: https://www.atlabs.ai/blog/ultimate-prompt-guide-best-camera-movement-prompts-for-ai-videos-2026
- Retention: https://fluxnote.io/guides/faceless-channel-retention-strategies-2026, https://flarecut.com/blog/script-writing-faceless-videos/
- Claude Code team tips: https://github.com/shanraisshan/claude-code-best-practice/blob/main/tips/claude-boris-13-tips-03-jan-26.md
- Claude Code with Chrome: https://code.claude.com/docs/en/chrome
