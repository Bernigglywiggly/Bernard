# GPT Astra prompt pack

Paste **Block 0** first in every chat, then one task prompt. Every task ends with a self-check, so
ask Astra to run it and fix anything that fails before it hands the file over. Drop finished files
into the folders named in each prompt; the Blender scripts in `a01_v5/` pick them up from there.

## Block 0: the channel brief (paste first, every time)

```
You are the art department for a YouTube channel that explains AI news by translating the numbers
into things people have actually held ("every number gets a street unit"). The narrator persona is
"the Cousin": hella smart, street smart, two beers deep; funny in the jokes, exact in the facts,
and one quiet deep line per video. The channel should feel like a safe, warm place: complex and
energetic, with soul, and every video ends on a hopeful note.

VISUAL SYSTEM: "one line, many worlds". Every visual world is a room on the same glowing amber line.
Constants that never change:
- Amber #FFB23F is the only warm accent, and the drift line is always the warmest thing in frame.
- Near-black ground #07080B at the edges of every frame.
- Type: Unbounded (800/900) for numbers and headlines, IBM Plex Mono (500/600) for labels. No other faces.
- One finish on everything: soft highlight bloom, gentle vignette, fine film grain.
- Frame furniture: thin crop marks, small mono labels, generous negative space.
Worlds (palettes), each tied to what the narrator is doing:
- W0 CORE (facts): fog and concrete stairs, an imperial-blue #0B2A6B grid lobby, black void.
- W1 PRESS (translating a number into a street unit): bone paper #ECE6DA, black ink #0B0B0C,
  crop marks, barcodes, risograph texture, editorial layouts.
- W2 CLOUD (the deep line): white point clouds and particles on black.
- W3 CHROME (the big payoff number): icy mirror chrome lit by softboxes, one amber reflection.
- W4 SIGNAL (the jokes): 3-colour ordered dither (#07080B, phosphor #5CFF9D, amber #FFB23F),
  animated on twos like stop-motion.
- HOME (the ending): still water, fireflies, the amber line running to an amber dawn.
Taste: premium but not sterile. Hand-made details over stock looks. Never cheesy, never
"AI slop": no glossy robot faces, no blue brains, no generic circuit boards, no lens-flare spam,
no text baked into images unless asked. No real brands, logos or real people.
```

## Evergreen kit (build once, use in every video)

### 1. Texture and overlay library

```
Make a texture and overlay library for the channel above. Deliver PNG/EXR stills and MP4/ProRes loops:
1. Film grain plates: 6 loops, 10 s each, 3840x2160, 24 fps, luma-only grain on mid-grey (#808080)
   for Overlay/Soft Light blending; fine, medium, 16mm-coarse, each in "clean" and "slightly gate-weaving".
2. Light leaks: 8 loops, 6 s, 3840x2160, black background (Screen blend), strictly in amber #FFB23F
   plus warm white; slow organic movement, no rainbow colours.
3. Dust and hair: 4 loops, 10 s, white on black, sparse, realistic.
4. Paper: 12 bone-paper scans #ECE6DA at 4096 px: risograph grain, slight misregistration, fold
   lines, a coffee ring on one, tape marks on two. Seamless tiling where possible.
5. Concrete: 6 seamless 4096 px PBR sets (albedo, roughness, normal), warm grey #56524C, poured and brushed.
6. Dither and halftone patterns: 8 seamless 1024 px tiles, 1-bit, for the SIGNAL world.
File names: tex_<type>_<nn>.<ext>. Folder: a01_v5/kit/textures/.
SELF-CHECK before delivering: every loop is seamless (last frame into first frame shows no jump); no
colour outside the palette in leaks; paper tiles tile with no visible seam at 2x2; grain has no chroma.
```

### 2. The sound identity kit

```
Design the channel's sound kit. 48 kHz / 24-bit WAV, peaks at or below -1 dBTP, clean starts,
natural tails, no music in the SFX. The palette is warm analog and tactile: tape, paper, air,
sub-bass, never cartoonish or stock-trailer "braaams".
1. Signature: "the line", a 1.5 s sonic logo. A warm analog tone that rises and resolves, like a
   light switching on in your chest. 3 variants (bright, soft, deep).
2. Whooshes x12 (0.25-1.2 s), stereo sweeps L->R and R->L, air and cloth, not jets.
3. Impacts x8: sub thumps with a paper/wood transient; 2 huge ones for type slams.
4. Glitches x12 for the SIGNAL world: bit-crushed, short, musical, pitched to Db.
5. UI ticks and clicks x10: soft, mechanical, like a good camera shutter or a mechanical watch.
6. Risers x6 (1-4 s) that end on a hard stop, not a crash.
7. Shimmers x6: small bells and glass, pentatonic in Db, for particles assembling.
8. Room tones x4 (60 s): night room, rain on a window, city far away, empty stairwell.
Folder: a01_v5/kit/sfx/<category>/sfx_<category>_<nn>.wav
SELF-CHECK: every file trimmed to its sound with a 10 ms fade in and out; loudness matched within
each category; nothing clips; the signature reads on phone speakers.
```

### 3. The ending ritual: music for the outro

```
Compose the channel's ending theme, the "going home" loop that plays under the last 20-40 seconds
of every video while the narrator says something hopeful. The feeling: that heavy, warm feeling in
your chest at the end of a late-night drive; nostalgia and sadness and gratitude at once, and
underneath it, a certainty that things will be okay. Magical but calm. A safe place.
Musical brief: 66-70 BPM, Db major (Dbmaj9, Bbm9, Gbmaj9, Ab6/9 as a starting point), dreamy
80s-style analog polysynth pads (slow attack, gently detuned, slight tape wow), a soft distant
gated-room drum pattern that enters on the second pass, a sparse sparkling arpeggio, sub-bass
you feel more than hear, subtle vinyl and tape texture. No vocals, no drops, no risers.
Must be original; do not imitate any specific song's melody or chord voicings.
Deliver: a 90 s seamless loop; 12 s, 20 s and 30 s cut-downs with natural endings; stems (pads,
drums, arp, bass, texture). WAV 48 kHz/24-bit, mastered to -16 LUFS, -1.5 dBTP.
Folder: a01_v5/kit/music/.
SELF-CHECK: the loop point is inaudible; the 12 s edit fades naturally; it sits under a speaking
voice without masking 1-4 kHz; it still feels warm on phone speakers.
```

### 4. Street-unit icon set (W1 PRESS)

```
Draw 40 pictograms for "street units", the everyday things we convert numbers into: chocolate bar,
generic cognac bottle, generic ride-share car, shift clock, pay slip, rent key, bus ticket, phone
battery, energy drink can, trainers, gaming controller, pizza box, kettle, bike, headphones,
school bag, group-project folder, fridge, microwave timer, cinema ticket, and 20 more you choose.
Style: editorial print pictograms, 2 colours only (ink #0B0B0C + amber #FFB23F), 3 px stroke at
256 px, rounded caps, flat fills, slightly imperfect like risograph print. No brands or logos.
Deliver: SVG + 2048 px transparent PNG each. Folder: a01_v5/kit/icons/. Names: icon_<thing>.svg
SELF-CHECK: all 40 read at 64 px; stroke weight is identical across the set; only the 2 colours.
```

### 5. Chrome environment (W3)

```
Make a 4K (4096x2048) equirectangular HDRI in EXR for rendering chrome typography: pure black
surroundings with three large soft rectangular softboxes (one wide horizontal strip at +15 degrees,
one tall vertical strip camera-left, one small top light) and one thin warm amber (#FFB23F) strip
light low behind the subject. Clean studio, no floor, no visible rigging.
Folder: a01_v5/kit/hdri/chrome_studio.exr
SELF-CHECK: the black is true black (0,0,0); softboxes have smooth falloff edges; values reach at
least 20 in the brightest strip so reflections read as light, not grey.
```

### 6. TouchDesigner: the heartbeat field (for the deep moments)

```
Build a TouchDesigner network (.toe) called heartbeat_field: an audio-reactive particle field for
the channel's quiet "deep line" moments. Amber (#FFB23F) and warm-white particles on black, drifting
slowly upward like embers or fireflies, gently pulsing with the low-mids (80-300 Hz) of an audio
file; a soft glowing horizontal line through the middle that breathes with the voice; depth of field
with round bokeh. Calm, never frantic.
Expose parameters: audio file, particle count, rise speed, pulse amount, bokeh size, line on/off.
Render: Movie File Out, 3840x2160, 24 fps, ProRes 4444 with alpha, plus an MP4 preview.
Include a README of how to swap the audio and re-render.
SELF-CHECK: no frame drops at 4K; alpha is clean (no black fringing); motion is smooth when the
audio is silent (never freezes); it looks good paused on any frame.
```

### 7. The finishing LUT

```
Create a .cube 3D LUT (33 point) for the channel's final grade in DaVinci Resolve: slightly cool
shadows, warm highlights, rich but not crushed blacks (floor at about 3%), gentle filmic highlight
roll-off, and exact preservation of the brand amber #FFB23F and phosphor #5CFF9D (within 2%).
Deliver LUT + a before/after frame on a test chart. Folder: a01_v5/kit/lut/
SELF-CHECK: a grey ramp stays neutral in the mids; the two brand colours measure within tolerance.
```

## Per-video tools

### 8. Shot-list director (turns any script into the world/camera plan)

```
You are the shot-list director for the channel above. Input: a narration script with word timings.
For every sentence decide its register: FACT, TRANSLATE (a street unit), JOKE, DEEP, PAYOFF or HOPE.
Map register -> world: FACT->W0, TRANSLATE->W1 PRESS, JOKE->W4 SIGNAL (or W0 VOID type slams),
DEEP->W2 CLOUD, PAYOFF->W3 CHROME, HOPE->HOME. Then give each shot one camera move from this grammar:
worm's-eye crane, god's-eye top-down roll, low orbit, top-down to grazing swing, dutch truck + rack
focus, snap zoom, shot/reverse with dutch, 4-frame burst, FPV swoop that lands, dolly zoom,
long-lens crane, whip pan, spiral dive, crane-up reveal, slow glide.
Rules: at least 50% of runtime in W0; no more than one world change every 6-8 s except JOKE bursts;
never two identical moves back to back; the amber line appears in every shot; cut on the first
syllable of the key word; one "Huey moment" (the deep line) gets the longest, calmest shot of the
video; the video ends in HOME with a hopeful line.
Output: a Python list in exactly this format, one dict per shot:
dict(id="S01", t0=0.00, t1=2.30, world="W0 · STAIR", reg="FACT", move="...", line="...", hits=[...])
then a 3-line summary of the rhythm, then the self-check.
SELF-CHECK: every rule above passes; the times cover the whole script with no gaps or overlaps;
cuts land on word starts.
```

### 9. A01-specific upgrades

```
Using the channel brief, make these A01 assets:
a) Two phone-screen "glow-up" posts for the joke "two AI companies posting a glow-up on the same
   night, like exes": 1080x2160 vertical, black UI, huge type, sparkles, before/after energy,
   one says MODEL A, one says MODEL B. They will be dithered to 3 colours, so use strong shapes.
b) Two editorial illustrations (2400x3200, risograph, ink + amber only): "the one who starts the
   group project" (an empty chair, a half-open laptop, a to-do list with one tick) and "the one
   who actually hands it in" (a stamped folder, a clock at 23:58, a tired smile).
c) Three thumbnail concepts in the v5 language (1280x720): the chrome +14, the dither exes, the
   standing 90. Big type, one idea each, readable at 120 px wide.
Folder: a01_v5/kit/a01/. SELF-CHECK: palette only; no real brands; each thumbnail readable at 120 px.
```
