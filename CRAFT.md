# CRAFT: house rules for every film and Short

Read before writing a script, a storyboard or a prompt for any channel. Distilled from the X and web research in
`lab/research/x_notes.md` and `lab/research/motion_playbook.md` (Oct 2026), and from what our own critics catch.
**After every film, add one line under "Learned on our films" for anything a critic or the user caught.** This file
is how the studio gets better between sessions.

## 1. Survive YouTube's "inauthentic content" rule (the biggest risk to the whole plan)
Since July 2025 YouTube demonetises "mass-produced, repetitive" channels: templated videos, slideshows with AI
narration, interchangeable faceless uploads. Channels with 500k+ subscribers lost monetisation in 2026. AI as a tool
is fine; **no visible author is what gets flagged.**
- Every film needs a point of view: a judgement, a "here's what I'd do", a verdict the sources don't hand you.
- **Vary the structure.** How They Profit's fixed seven chapters (price, machine, proof, money, you, what if, close)
  and "Part N of 5" Shorts are a template. Change the shape every film: cold open in the middle of the story, a
  myth-vs-fact film, a "follow one dollar" film, a timeline.
- Original research on screen (filings, court records, maps) is the authorship. Keep sources in every description.
- Don't flood the channels: about one long film and five to seven Shorts a week per channel is the ceiling.

## 2. Script and narration
- **Narrate like a university professor, not a hype account.** Ban Claudisms: staccato one-line sentences in a row,
  "Not X. Y.", colon reveals, three numbers in one sentence, "Here's the thing", rhetorical questions every line.
- One number per sentence, said the way people say it ("about seven cents in every dollar").
- Hook: the most surprising true thing in the first 3 s of a Short and the first 8 s of a film. Then a forward
  tease every 60-90 s ("in a minute, the trick that made it work").
- Voice first, picture second: voice each line, trim silences, then time the animation to the narration's
  timestamps (our engines already do this; keep it).
- ElevenLabs v3, if used: lines over 250 characters are more stable; steer delivery with tags like [whispers] or
  [sighs] sparingly.

## 3. Look and motion
- **Banned defaults** (the "AI video" look): centred title on a gradient; everything fading in; corner labels and
  frame borders; generic particle bursts; glows on UI; constant easing; a small card floating in an empty frame.
- Something new every 2-4 s. No fully frozen frame over 2 s except the end card. Reading holds get a slow 3-5% push.
- Frame 0 is a finished, designed composition: it's the Shorts hook and YouTube's fallback thumbnail. No logo or
  name card in the first 2-3 s of a Short.
- The lead subject fills 60-85% of the frame. Vary scale: close, wide, overhead, full-frame type.
- **The foreground becomes the transition**: a number, word or object pushes through the camera into the next
  scene. One object carries across cuts (a coin, a document, a map pin) so the film reads as one piece.
- Speed always changes: land slowly enough to read, leave fast. Springs, not linear. Hard cuts on beats when scale
  and direction match.
- Pacing dialect for notes: fast 0.2 s, medium 0.4 s, slow 0.6 s, cinematic 1-2 s per move.
- Maps are a signature for Money Crimes and How They Profit: animated routes, real terrain and real places
  (see the Austerlitz film in x_notes for the standard).

## 4. Process gates (don't skip; fixing a still costs seconds, fixing a render costs a re-render)
1. References: 1-2 videos or frames in the target style. Name the style, extract frames with ffmpeg, write a style
   guide (palette hex, type, shot lengths, transitions) before any code.
2. Shot list on the narration timeline: time, what's on screen, its job, how it exits, what carries over.
3. **Stills first**: one frame per scene as a contact sheet. Review, then animate.
4. Animatic at low resolution for pacing, then the full render.
5. **Critic gauntlet** (`.claude/skills/film-critic`): a fresh subagent that didn't build the film judges the
   render, fixes go in, a new critic verifies. Never grade your own film.
6. Director notes use camera words: "slow every zoom to 0.7x", "hard cut at 4 s", "push in on the number".

## 5. Facts
- A facts file per film is the only source for on-screen numbers, names and claims. Before render, a separate
  checker verifies every on-screen claim against its source (adversarial: it hasn't seen the script's reasoning).
- Label anything generated or imagined ("AI reconstruction", "What if... imagined, not a forecast").

## 6. Packaging
- Titles: 6 words or fewer, about 30-50 characters, one clear tension. The thumbnail carries the context.
- Thumbnail text: 3 words ideal, never over 6; it complements the title, never repeats it. High contrast, sans
  serif, outline on busy backgrounds. Test at phone size.
- Shorts: the first frame is the hook; make the last line or frame lead back into the first so it loops; aim for
  70-85% retention.

## 7. AI pictures and clips (Higgsfield)
- Veo/Kling prompts: 60-90 words. Shot type + subject, one action, one camera move, named light sources ("amber
  fire glow", not "moody"), and the exact end pose so the next shot can start from it.
- Seedance: a [VISUAL] block (camera body, lens, grade, grain, "no CGI"), the action as a camera-directed sequence,
  an [AUDIO] block (SFX only, or nothing).
- Consistency: character sheets (front, back, close-up, props); one master location image spun into several angles
  as a reference; one sentence describing each voice in every prompt; leave pauses between dialogue lines.
- Generate 2-4 representative shots before the rest. Expect to keep 3-4 out of 20.
- Never show a real person's face in reconstructions (our rule).

## 8. Sound
- Cuts on beats. If there's a music track, measure its beat grid first (librosa); put state changes on beats and
  big moments on downbeats.
- -14 LUFS, true peak at or below -1 dBFS. One soft whoosh per real scene change; clicks only on real on-screen
  actions. Keep a music-only fallback.

## Learned on our films
- 5 Oct (PayPal stills): a bar slice under ~220 px can't hold its label; put it in a callout under the bar
  (`cut_bar` in ep05/scenes.py). Check node titles fit their boxes at 40 px.
- 4 Oct: `motion_report.py` on finished films: How They Profit (Amazon) is near-still 70% of the time (frozen 54%,
  in short bursts; 5 stretches of 2.5-3.6 s); The Curve LF03 moves throughout except its 17 s end card; Money Crimes
  (Ponzi) is the liveliest. HTP needs continuous camera drift and object motion inside each beat, not move-then-hold.
- 4 Oct: our finished films peaked at -0.2 dBTP (target -1). Cause: the mix is mastered to -1.5 dBTP, but the end-card
  step re-encoded the film's AAC track a second time. `ch2/endcard.py` now joins the WAVs and encodes once (EP04 test:
  -1.1 dBTP, -14.2 LUFS). The Curve and Money Crimes encode once but mastered at a -1.0 ceiling, so AAC's ~0.8 dB overshoot
  gave -0.2: `longform/doc.py` and `shorts/reel.py` now master at -1.5 dBTP like `engine/mix.py`. Applies to new renders.
