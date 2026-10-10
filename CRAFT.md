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

## 9. Attention playbook (10 Oct research)
Full tables, evidence grades and sources: `lab/research/ATTENTION_PLAYBOOK.md`. Rules marked (test) are unproven.
1. Frame 0 of a Short is the payoff image plus 2-6 words; line 1 (≤ 3 s) is the most surprising true fact, says "you"
   once and says the search term out loud.
2. Judge Shorts on engaged views and "Stayed to watch" (target ≥ 70%), never raw views (every replay counts since Mar 2025).
3. Shorts: YouTube 20-35 s by default, 50-60 s only if the story holds; TikTok gets its own 61-90 s cut.
4. No licensed or claimable music in any Short over 60 s: one Content ID claim blocks it worldwide.
5. Shorts get burned-in captions (2-4 words per chunk); long films get keyword overlays plus CC, not full captions.
6. Faster is not better: one visual change every 1.5-2.5 s in Shorts, 2-4 s in films, one dimension at a time.
7. Long films: show the thumbnail's promise by 0:08, a real payoff by 1:00, re-engagement beats near 3:00 and 6:00.
8. End on the second-best fact plus the verdict, then stop within 15 s (peak-end); never say "to wrap up".
9. Every promise in a title or thumbnail appears on screen before 1:00 (YouTube removes "egregious clickbait" on news,
   which covers The Curve and the geopolitics channel).
10. Titles: a concrete subject with the outcome withheld; true negativity is allowed, invented stakes are not.
11. Thumbnails need text and one focal subject; faces are optional (no measured edge). 2-3 vs 4-6 words (test).
12. Every long film goes into Test & Compare with three title/thumbnail combos; it judges by watch time share.
13. Spend expressive-voice effort on the middle third: AI voices lose most engagement where the story builds.
14. Repeat brand marks (colour, sting, recurring object, narrator), never the structure: that is the "mass-produced" flag.
15. One change per test, logged with 48 h and 7 d numbers against the channel's own median (playbook §6).

## Learned on our films
- 9 Oct (tunnel and economy pilots, Spanish LF02): (1) the engine stamped "AI-GENERATED" on diagrams drawn in code: a
  false label that invites "AI slop" comments. A film now sets `ILLUS` in its script ("DIAGRAM · DRAWN FOR THIS FILM").
  (2) Frame 0 was a near-black blob and the twist landed at 9.3 s: `OPEN_RESOLVED = True` and `LEAD = 0.4` put the first
  picture up at frame 0, and the twist moved to the first sentence (5.4 s). (3) A critic warned that three channels on
  one engine look (rail, ASCII resolve, caption plate) is the "mass-produced" pattern: each new channel needs its own
  visible look before launch. (4) Spanish: "cuando + subjuntivo" needs a future main verb; calques ("de por token")
  and regional words ("sale en", "inversionistas") were caught only by a Spanish-reading critic. Respell names the
  voice mangles in the spoken text and keep the real spelling on screen with the `(shown, said)` tuple.
- 6 Oct (HTP 06 Visa, five critic passes): (1) the working TITLE was a factual claim nobody had checked ("never touches
  your money"): Visa settles payments and guarantees settlement, per its own 10-K. Put the title and the thesis line in
  FACTS.md with a source before scripting. (2) In a one-camera film, patching overlaps one at a time failed three
  times; what worked was structural: each block fades out when its chapter ends, the camera gets over its target
  before closing in, far moves are single hops, the last chapter is one held frame. (3) The builder's "fixed" was
  wrong twice: measure (lit-pixel share, black frames) and let a fresh critic mark each item before saying so.
- 5 Oct (HTP engine): move-then-hold beats measured frozen 69% of EP05's first two minutes. A 3.5% push with a side
  drift through every beat (`ch2/kit.py` DRIFT) took it to 12%. A slow push still counts as near-still, so each scene
  also needs something moving inside the beat: a slow float and a light sweep on the recurring $100 note took
  near-still from 60% to 47% and frozen to 9%.
- 5 Oct (walk-in Reels): a stamp's "coming down" shadow lasted 7 frames and read as a grey disc. An impact lands in 3-4
  frames; the anticipation should be felt, not seen.
- 5 Oct: `script_lint.py` (film-critic skill) on our scripts: Amazon (EP04, before CRAFT) 16 flags (number stacks,
  staccato, colon reveals); PayPal (EP05, written to CRAFT) 1; LF04 draft 4. All fixed. Lint every script before voicing.
- 5 Oct (LF04 draft): the first draft opened with "Not because of X... Because of Y", a banned Claudism, caught on
  re-read. Search every draft for "Not " at the start of a sentence before voicing.
- 5 Oct (PayPal stills): a bar slice under ~220 px can't hold its label; put it in a callout under the bar
  (`cut_bar` in ep05/scenes.py). Check node titles fit their boxes at 40 px.
- 4 Oct: `motion_report.py` on finished films: How They Profit (Amazon) is near-still 70% of the time (frozen 54%,
  in short bursts; 5 stretches of 2.5-3.6 s); The Curve LF03 moves throughout except its 17 s end card; Money Crimes
  (Ponzi) is the liveliest. HTP needs continuous camera drift and object motion inside each beat, not move-then-hold.
- 4 Oct: our finished films peaked at -0.2 dBTP (target -1). Cause: the mix is mastered to -1.5 dBTP, but the end-card
  step re-encoded the film's AAC track a second time. `ch2/endcard.py` now joins the WAVs and encodes once (EP04 test:
  -1.1 dBTP, -14.2 LUFS). The Curve and Money Crimes encode once but mastered at a -1.0 ceiling, so AAC's ~0.8 dB overshoot
  gave -0.2: `longform/doc.py` and `shorts/reel.py` now master at -1.5 dBTP like `engine/mix.py`. Applies to new renders.
