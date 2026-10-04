# X notes: Claude Code, motion design and AI video (public X, 4 Oct 2026)

**Scope.** This pass covers **public X posts only**, read through the vxtwitter mirror from the cloud session. The
user's own bookmarks and likes need their logged-in Chrome (a local `claude --chrome` session; X redirects to login
from the cloud), so they aren't here yet. X Articles (long posts) only show their preview without a login; where the
full text matters, its linked repo or gist was read instead. Builds on `motion_playbook.md` (public web research); this
file adds what's new from X. Like counts are as of 4 Oct.

## 1. The workflows the best results share

**Reference → style guide → layout library → scenes** (the setup that fixes "out of the box isn't good enough"):
> "Each project you work on gets a new folder. Within each folder, create a folder for reference frames... tell Claude
> to reference those images, and build out your style guide... I normally have 10-15 different layouts per brand.
> These are reusable scenes... 'Create a scene that references this part of the script "..." and use the "x" scene
> layout.'" — @JJEnglert, 16 Apr 2026, https://x.com/JJEnglert/status/2044889694949826821

**Dump context, storyboard, animate** (HyperFrames; "20M+ views from videos made using HyperFrames"): storyboard as one
still per scene in a contact-sheet grid before any motion; then edit conversationally (one intro took 20 minutes and 26
prompts) rather than regenerating. Lint and validate before rendering: `npx hyperframes lint`, `npx hyperframes
validate` (missing assets, runtime errors, contrast). — @jake11moran, 23 Sep 2026,
https://x.com/jake11moran/status/2102878602316652828; @petergyang (generate a `frame.md`, storyboards), 20 Jun 2026,
https://x.com/petergyang/status/2068333151186022460

**Why most Opus motion videos look the same:** "centered text on a gradient, everything fading in, a logo at the end.
They don't give it a reference..." (7.6k likes; full article behind login). — @0xMovez, 27 Sep 2026,
https://x.com/0xMovez/status/2104216919033192746

**Remotion's own prompt history** (how their viral launch animation was made; read in full from the gist): many tiny
plain-English steps, each one change: "make a new composition 1280x1000px of a macos terminal window... light theme" →
"remove the background and the font size needs to be a lot bigger" → "add a typewriter animation" → "refactor the
cursor into its own component; keep it blinking while there is no typing" → "make a master composition and add the
current one as a sequence" → "add a 3d rotation, like 20 degrees of x and y" → "add the transform to the sequence, not
the terminal itself" → "over the total length, slowly rotate Y from 20 to -20 degrees" → "run the command yourself, look
at the output and add it as terminal content" → "stagger the lines, one every 50ms" → "make the terminal jump in from
the bottom using a fast spring animation, but no bounce" → "add a scale animation, ease-out, half a second" → "scale
only from 0.9 to 1" → "the rotation is a bit much, only 10 to -10" → "flip the terminal towards the camera by rotating
the X axis" → "render it". Lesson: exact numbers, one change per prompt, use real output as content. — @Remotion,
20 Jan 2026 (3.6k likes), https://x.com/Remotion/status/2013628043105890779,
https://gist.github.com/JonnyBurger/5b801182176f1b76447901fbeb5a84ac

**The one-line showreel prompt** (4k likes; shows how far the model goes with an open brief):
> "make a dynamic 15-second motion graphics video that shows what an incredible motion designer you are, like it's
> your showreel for a résumé. go all out." — @ajith_io, 25 Sep 2026, https://x.com/ajith_io/status/2103449416325890146

## 2. The full pipeline posts (most useful for us)

**Opus 5.5 video workflow after 10+ hours of testing** (2k likes):
- Use Claude Code, not the app. One OpenRouter key for image, video and audio models.
- Make a TTS skill that puts emotion into the voice. Motion graphics with Manim, HyperFrames or Motion Canvas.
- Keyframes with an image model, then Veo 3.1 / Seedance 2.5 for motion ("Seedance does better with motion shots").
  Reference images for consistency; **generate an animatic before the full video**.
- A script-planning skill; assemble with OpenTimelineIO; ffmpeg for the rest.
- **"Explicitly tell it to avoid Claudisms like short punchy sentences and a lot of numbers. 'Narrate like a university
  professor.'"**
- yt-dlp search to pull Creative Commons clips; ElevenLabs music; a caption skill with word-level timing from ASR.
- **A critic skill that takes screenshots and uses transcription to validate audio and video.**
- Prompt = what you want + aspect ratio + length + style.
— @deedydas, 29 Sep 2026, https://x.com/deedydas/status/2104957026199900220

**"The only prompt you need for high-end motion graphics"** (2.2k likes): studies reference videos frame by frame,
storyboards first, builds in GSAP + Three.js, renders and critiques every section, checks motion, contrast, audio and
transitions, iterates to a quality bar. It points to **motion-video-kit** (MIT), now vendored in this repo as the skill
`.claude/skills/business-motion-film` (see section 4). — @RoundtableSpace, 30 Sep 2026,
https://x.com/RoundtableSpace/status/2105209785335373948

**Automated editing skill:** understand the video → split into scenes → use supplied assets or propose motion graphics
per scene → **wait for approval** → generate → assemble. — @ayushunleashed, 6 Mar 2026,
https://x.com/ayushunleashed/status/2029747545132486985

**Voice and music in Remotion:** `npx skills add resemble-ai/remotion-resemble-skill`, then "Create a promo video for
[site] with voice over and background music. Make it in the style of [style]." — @obaid, 26 Jan 2026,
https://x.com/obaid/status/2015708306996883612

**HyperFrames install:** `npx skills add heygen-com/hyperframes` (HeyGen built its launch video with it in Claude
Code; 8.3k likes). Sonnet was enough for a simple PDF-to-video. — @heygen, 16 Apr 2026,
https://x.com/heygen/status/2044827454460871072; @omixam, https://x.com/omixam/status/2045395315197432133

**A sceptical counterpoint:** a week of Claude video across pixel MVs, flat animation, science shorts, 2D and 3D
characters: strong for small promos and explainers, overhyped elsewhere, and no substitute for Seedance-style
generated animation. — @Mrooo03, 30 Sep 2026, https://x.com/Mrooo03/status/2105195950142566783

## 3. AI video prompts (Higgsfield / Seedance)

A strong Seedance 2.0 structure (tagged sections, one continuous shot, audio spelled out). Excerpt:
> "[VISUAL] Shot on ARRI Alexa 35 with anamorphic lenses, cinematic film look, rich color science, organic highlight
> rolloff, subtle halation, fine film grain, practical in-camera lighting only, real haze, atmospheric particles,
> natural lens flares, no CGI. ... handheld camera following from behind at hip height with a slight Dutch angle. ...
> The camera arcs around into a low-angle medium close-up ... pushes past his shoulder to reveal ... tracks forward ...
> tilts up to his face ... Slow-motion emphasizes the reveal ... before returning to real time.
> [AUDIO] No music. SFX only. Distant city ambience, warm wind, footsteps, breathing, a faint harmonic hum ..."
— @maarcoofdezz, 17 Jul 2026, https://x.com/maarcoofdezz/status/2078162454744346803

Pattern: a [VISUAL] look block (camera body, lens, grade, grain, "no CGI"), then the action as a camera-directed
sequence, then an [AUDIO] block. Reference-image prompts add "preserve facial features, hairstyle, clothing, body
proportions... throughout" for consistency (@HaniaAi12, https://x.com/HaniaAi12/status/2105845066514436402).

## 4. Vendored: motion-video-kit (`.claude/skills/business-motion-film`)

Made from 28 professional launch films and dozens of critique rounds. Built for business commercials, but its core
transfers to our explainers:
- **The Gauntlet:** the builder never grades its own work; a fresh critic sees only the render; the next critic checks
  the last list item by item (FIXED / PARTLY / STILL PRESENT). Ready-made critic prompts are in
  `references/critic-prompts.md`.
- **Six motion rules:** the foreground becomes the transition; one persistent actor across shots; density from a
  hierarchy of moves; change speed (land, then exit fast); hard cuts are fine when scale and direction match;
  show cause → effect.
- **Pacing numbers:** frame 0 is a finished composition; no motionless stretch over about 0.6 s; the lead subject fills
  60–85% of the frame; 12–15 compositions per 30 s; slow 3–5% push on reading holds.
- **Measured bar:** `scripts/frozen-time.sh` (frozen stretches), `scripts/loudness.sh` (−14 LUFS punchy, about −16
  calm, true peak ≤ −1 dBFS), and contact sheets.
- **Real client rejections:** "too basic: image, then video, then text"; "so much space is being wasted"; "some parts
  linger too long"; "the first image looks too dark".

## 5. Channel growth claims (treat with care)

- "Claude runs 12 YouTube channels... $100,000 a month" (@woody_research) and "replaced a $4,000/month payroll with
  Claude Code + Higgsfield" (@zeuuss_01): engagement-bait. There's no evidence in the posts, so they're not useful as plans.
- The useful part of the faceless-channel posts: one operator can run script, edit, motion and thumbnails in one
  agent session. That's already our setup.
- Resource list: Refero Styles and awesome-design-md (DESIGN.md files for 74 brands, MIT) give Claude a written style
  to follow. — @Voxyz_ai, https://x.com/Voxyz_ai/status/2104284941437784139

## 6. What to try in this studio (new beyond motion_playbook.md)

1. **Critic pass on every film before upload.** Run the vendored full-film critic prompt as a fresh subagent on the
   render plus contact sheets, and add `frozen-time.sh` to the QA. Our engines measure loudness already; frozen time
   they don't.
2. **"Narrate like a university professor" against Claudisms** in all three channels' script prompts: fewer
   staccato lines and fewer stacked numbers per sentence. Check against our current HTP scripts.
3. **Per-channel layout library** (JJ Englert): 10–15 named scene layouts per brand in `lab/motion` (stat slam, versus
   split, map route, timeline, document zoom, quote card). Then "use layout X for this script line".
4. **Animatic first** for anything Higgsfield-generated: keyframes plus timing as a rough cut before spending video credits.
5. **Seedance prompts in [VISUAL]/[AUDIO] blocks** for Money Crimes reconstructions (period look, handheld, SFX only).
6. **Foreground fly-through transitions** (a stat or headline scales through the camera into the next scene) to
   replace the plain cuts between HTP chapters.
7. **Test HyperFrames** (`npx skills add heygen-com/hyperframes`) on one Curve cold open against the Remotion version.

## Still to do (needs the user's Chrome)

Bookmarks, likes and followed accounts: run locally with `claude --chrome` (Claude in Chrome extension, logged into
X), read-only, and append to this file under "From your bookmarks".
