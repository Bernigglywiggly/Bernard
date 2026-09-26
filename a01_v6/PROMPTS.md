# GPT prompts, v6 (Chrome & Marl)

Paste **the v6 brief** first, then one task. Each task ends with a self-check.

## The v6 brief (paste first)

```
You are the design and sound department for a calm, premium YouTube channel that explains AI by
translating every number into what it means for ordinary people: their time, their money, their
work, their future. Voice: calm, clear, warm; no jokes; curiosity-driven and professional.
Every number gets several everyday perspectives (student, gamer, business owner, parent, driver,
"your time is money") so that it clicks for everyone, and every video makes the viewer's benefit
explicit: what it does for you, what it costs, how people earn with it, what's coming.

LOOK: "Chrome & Marl". Heathered marl grounds (light #E7E8EA for explaining, graphite #14161A for
forming and revealing). Line work in ink #1C1F24. One accent: turquoise #12B8AC (glow #3FE6D8).
Emerald #12A36E only for gains. Chrome only for hero numbers (white, steel, a thin dark horizon,
a faint turquoise reflection). Type: Michroma for numbers and titles, Inter Tight for sentences,
IBM Plex Mono for labels and ASCII.
MOTION: the camera barely moves; the elements move. Lines form objects (Tron: Legacy-style
formations with bright tips), then flow into the next form (morphs, match cuts); characters
resolve out of ASCII noise; cards dock onto shelves; percentages fill a 10x10 "per hundred" grid.
Smooth easing, nothing chaotic, one gentle "whoa" per chapter. Clean, satisfying, detailed,
never overstimulating. Pinterest-editorial layouts: generous margins, one idea per card.
SOUND: restrained and layered; one quiet sound per visual action from one family (ticks, pips
climbing a pentatonic scale, soft thocks, glass chimes, airy morphs, a single sub "thum").
Never stock-trailer, never cartoonish.
```

## 1. Turn my Pinterest board into a design system

```
Here are my reference images (attached). For the channel above, extract: the 6-8 visual moves they
share (layouts, line work, type treatments, textures, ASCII or dither use, colour habits), how
each could animate cleanly, and which ones fit the v6 look without making it busy. Then write a
one-page style guide with do/don't examples, and 10 scene ideas for an AI explainer that use them.
SELF-CHECK: every rule traces back to at least two reference images; nothing contradicts "calm and clean".
```

## 2. Perspective writer (the heart of the script)

```
Number: <e.g. a model scored 14.1 points higher on a coding test: 52.3% -> 66.4% of tasks passed>
Write 10 everyday perspectives that make this number click for someone with zero interest in AI:
a student, a gamer, a small-business owner, a parent, a driver, a nurse, a tradesperson, someone
saving money, a retiree, "your time is money". For each: who -> before -> after -> what it means
for their time or money, in one sentence under 20 words. Keep every conversion mathematically
exact (show the working underneath), and never exaggerate. Mark the 4 strongest and why.
SELF-CHECK: recompute every conversion; delete any that needs a caveat to be true.
```

## 3. Calm script (full video)

```
Write the full narration for <topic> in the v6 voice: calm, clear, warm, no jokes, curiosity-driven.
Structure: 0-10 s the event and the number (no preamble); 10-30 s the reframe ("sounds small, it
isn't") plus the first perspective; a perspective ladder (3-5 people); chapters for what it does for
you, what it costs, how people earn with it, what's coming; an open loop every 2-3 minutes; a
pattern change every 60-90 s (say which visual form each section takes: card, grid, formation,
ASCII, chrome); end hopeful and practical (one thing to try today). 150-165 words per minute.
Mark each paragraph with the visual motif it should use.
Research: <paste the research brief output>
SELF-CHECK: read aloud; every number has a source and an everyday translation; the benefit to the
viewer is explicit at least once a minute.
```

## 4. Voice design (ElevenLabs Voice Design or similar)

Describe traits; never clone or name real actors or characters, which is risky on a monetised channel.

```
Design 4 narrator voices from these descriptions, each reading the attached 45-second script:
A) "Warm buddy": laid-back, slightly raspy, big-hearted, relaxed pace, a smile in the voice.
B) "Earnest baritone": deep, friendly, sincere, a little slow, reassuringly simple.
C) "Wise elder": deep, warm, measured, gravel at the bottom, unhurried, trustworthy.
D) "Gen Z guide": early twenties, natural, quick but clear, no slang overload.
Keep all four calm (no shouting, no hype) and at 150-165 words per minute.
SELF-CHECK: none of them imitates a real, identifiable person.
```

## 5. Satisfying sound kit (v6)

```
Design a UI/motion sound kit for the look above. 48 kHz/24-bit WAV, -1 dBTP peaks, tight trims:
ticks x20 (a character resolving: tiny, crisp, slightly varied); pips x15 (a cell filling, tuned to a
pentatonic scale in C, so runs climb musically); formation chirps x20 (a line lighting up: a short
rising glint); thocks x8 (a card docking: soft, magnetic, tactile); glass chimes x6 (completion, C
major tones); morphs x6 (lines flowing into a new form: airy, tonal, 0.6-1.2 s); thum x3 (one sub
hit for the big line); shimmer x4 (chrome glints); zoom x3 (a gentle push through a letter).
Calm, premium, consistent, like a very good operating system.
SELF-CHECK: play a run of 20 ticks and 15 pips back to back: satisfying, never irritating.
```

## 6. The calm score

```
Compose a minimal score for a calm AI explainer: an Am9 pad for the dark "forming" sections that
lifts to Cmaj9 when the light opens, soft felt piano motifs, sub you feel more than hear, no drums
until an optional gentle pulse in the last chapter. 70 BPM. Deliver 3 cues (dark, light, outro) as
60 s loops plus stems. -18 LUFS so the voice sits on top.
SELF-CHECK: it never masks 1-4 kHz; the Am9-to-Cmaj9 lift is audible on phone speakers.
```

## 7. Formation shots (Blender / TouchDesigner / After Effects)

```
Design a Tron: Legacy-style formation for <object: e.g. a chip, a bar chart, a coin, a brain>:
the object assembles from light lines on graphite marl, edges lighting outward from a seed point
with bright tips, concentric rings sweeping in first, then surfaces filling with chrome. 3-4 s,
locked-off camera, the object slowly rotating. Give step-by-step build instructions for Blender
(geometry nodes or curve bevel with animated factor), TouchDesigner (network outline) and After
Effects (Trapcode/Plexus or shape layers), plus the exact colour values above.
SELF-CHECK: it reads at phone size; nothing flickers; it looks deliberate, not busy.
```
