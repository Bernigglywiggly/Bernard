# Creative Research: "Chrome & Marl" AI-Explainer Channel

Compiled 26 Sep 2026 by the research department.

**How this was sourced.** Web search was used until the session's search budget ran out partway through task 3. WebFetch was blocked for every host tried (tiktok.com, fandom, grokipedia, higgsfield.ai, wikipedia). The rest was checked with GitHub code search across public repos: Higgsfield's official SDK source, integrators' API probe logs, third-party research notes that cite Higgsfield's own pages, switch databases, and paper citations. Each claim is tagged by where it came from:
- no tag: confirmed in a search result
- **[3P]**: from a third-party note found on GitHub
- **[K]**: from my own background knowledge and not checked in this session. Verify these before stating them as fact.

Every URL below appeared in a search result. None were constructed. Items without a URL are cited by title.

---

## 0. Key takeaways

1. **Borrow Luca Maxim's structure, not his material.** Open with a flat premise. Switch into second person. Build an escalation ladder. Turn the concrete into an aphorism. Land a punchline built on a metaphor from another domain. End on a deadpan pivot. His shock content (sexual and racial) is the "tacky" line we must not cross.
2. **What makes motion satisfying:** it is easy to read (fluency), it moves with minimum-jerk easing, it follows a predictable grid with one surprise per phrase, and it closes visibly with a sound transient synced 0–20 ms after the visual event.
3. **Aim for medium complexity everywhere.** This applies to break syncopation, edit density, and ASCII noise. Pleasure follows an inverted U.
4. **Bass should be brief and felt.** Very-low-frequency sound measurably moves bodies even when it can't be heard. Sustained infrasound (around 17–19 Hz) is linked to unease. Use short sub drops and a *descending* Shepard–Risset glide for the "falling through a vortex" feeling, and resolve each one.
5. **Higgsfield (Sept 2026)** has 65 camera presets that can be stacked up to 3 axes, its own DoP image-to-video model with `motions[{id,strength}]`, Soul 2.0 images, Cinema Studio 3.x, and Lipsync Studio. It also routes third-party models: Kling 3.0, Veo 3.1, Seedance 2.0, Wan and others. It has a real API: the official SDK uses `https://api.higgsfield.ai`, credentials come from `cloud.higgsfield.ai`, and job status comes from `platform.higgsfield.ai`. Plans run Starter $15, Plus $49 ($39 billed yearly), and Ultra $129 ($99 billed yearly). Credits do not roll over.
6. **Music bed:** atmospheric/intelligent jungle or liquid drum & bass at about 170 BPM, with bass and pads moving at half time. Keep breaks moderately syncopated and thin them out under speech. **Do not use the raw Amen recording.** Re-play or re-program breaks from one-shots with clear provenance.
7. **"Banana keyboard"** most likely means Keychron's *Banana* tactile switches (K Pro Banana / Super Banana; WIRED called them "poppy and responsive"). A second candidate is the enthusiast linear *C³Equalz × TKC Banana Split* (made by JWK). Section 6 has a layered synthesis recipe for the sound.

---

## 1. @santeluca (Luca Maxim): content, speaking and editing style

### 1.1 What is known about him

- **Who he is.** Luca Maxim Khocholava is a Georgian musician, influencer and fashion designer, and owner of the apparel brand **Children Of Khan**. The brand is "narrative-driven" and mixes lore, memes, history, music and fashion ([Wikitubia](https://youtube.fandom.com/wiki/Luca_Maxim)). He spent much of his life in the Netherlands before returning to Georgia ([Grokipedia summary](https://grokipedia.com/page/Luca_Maxim); [Viberate](https://www.viberate.com/artist/luca-maxim/) lists him as Netherlands-based).
- **Reach at search time.** About 943K TikTok followers and 80.1M likes ([TikTok @santeluca](https://www.tiktok.com/@santeluca)); about 419K on Instagram.
- **Timeline** ([Wikitubia](https://youtube.fandom.com/wiki/Luca_Maxim)):
  - Oct 2020: first YouTube upload, a music video for "Streets Too Quiet".
  - Jul 2024: first Shorts.
  - From May 2025: Shorts and Reels "with his own story, narration and song, accompanied with AI-generated videos or clips of himself".
  - 19 Oct 2025: a 22-minute talk, "Luca Maxim is planning something big" ([YouTube](https://www.youtube.com/watch?v=uGqLWRABfAA)).
  - After 23 Oct 2025: true-story videos, such as being fired from ZARA ([YouTube](https://www.youtube.com/watch?v=pPIuXXJZHzA)) or rejected from art school twice.
- **The lore.** A fake company, "Azerbaijan Technology", in a surreal world that parodies media and trends. A review describes the premise as "genuinely delves deep into various different cultures" ([AOTY user reviews](https://www.albumoftheyear.org/album/1405507-luca-maxim-azerbaijan-technology/user-reviews/); see also [this review](https://www.albumoftheyear.org/user/krudd/album/1405507-azerbaijan-technology/)). Recurring characters include Selim Kerimov ("CEO of Azerbaijan Technology") and Skebob, and running bits include "Agarthan citizenship", "goon coins" and "uncles". The song "Azerbaijan Technology" (25 Jul 2025, 2:20; [music video](https://www.youtube.com/watch?v=fY_1mMN49eM)) scores 94 from users on Album of the Year ([AOTY](https://www.albumoftheyear.org/album/1405507-luca-maxim-azerbaijan-technology/user-reviews/)).
- **How he describes his approach:**
  - "The music came before the videos and promotion became its own product" (interview snippet in search results).
  - AI is "purely a production instrument to quickly prototype" his ideas, and "taste can't be automated" ([Grokipedia](https://grokipedia.com/page/Luca_Maxim); Shorts: [how he comes up with ideas](https://www.youtube.com/shorts/f4Xvk3M3FVM), [why his work is not AI slop](https://www.youtube.com/shorts/ySdX_Uemmh0)).
  - On originality: "Imitate and iterate" ([Short](https://www.youtube.com/shorts/I5Ak-ploO7A), [IG reel](https://www.instagram.com/lucamaxiim/reel/DQesghWkgdF/)).
  - A reviewer adds that AI video's "weird… tendencies to make mistakes/create surreal imagery perfectly compliments the nature of the art" ([AOTY user reviews](https://www.albumoftheyear.org/album/1405507-luca-maxim-azerbaijan-technology/user-reviews/)).
- **Voice.** Described as "charismatic, deadpan" (Grokipedia). A voice-clone listing describes it as "a charismatic male voice with a young, conversational tone and a hint of humor" ([Fish Audio](https://fish.audio/m/906caca783fd4061a7ab02273b0325f9/)).
- **Titles and captions seen.** These are the main structural evidence:
  - "it's hard being Luca Maxim." ([TikTok](https://www.tiktok.com/@santeluca/video/7627222979927084320))
  - "It's hard dating in 2026" ([TikTok](https://www.tiktok.com/@santeluca/video/7593455826702961952))
  - "Spent 1600 minutes with myself" ([TikTok](https://www.tiktok.com/@santeluca/video/7444550478706396438))
  - "Agartha Passport Procedure Explained: Skebob Edition™" ([TikTok](https://www.tiktok.com/@santeluca/video/7526689803006381344))
  - "Dubai Labubu: Habubu™" ([TikTok](https://www.tiktok.com/@santeluca/video/7523378547897928993))
  - "Debunking the Prompt Theory in AI Content Creation" ([TikTok](https://www.tiktok.com/@santeluca/video/7522113655937240352))
  - "Enroll at Children of Khan" ([TikTok](https://www.tiktok.com/@santeluca/video/7537015957332577568))
  - "Who Is Luka Maxim? Quick Search Guide" ([TikTok](https://www.tiktok.com/@santeluca/video/7677826823073336609))
  - lowercase captions "no allowance can fix this" and "only the best rng"
  - TikTok search clusters: "[santeluca lore](https://www.tiktok.com/discover/santeluca-lore?lang=en)" and "[santeluca millionaire](https://www.tiktok.com/discover/santeluca-millionaire?lang=en)". The millionaire cluster sits beside "how I became a millionaire at 16" hustle content, which he parodies (my inference).
- **Hard editing data [3P]** comes from a transcript and shot log of three of his TikToks (GitHub: `chiefofbrief/social_media`, file "sample transcript – Luca Maxim.md"):
  - One video: about 24 shots in 45 s (about 1.9 s per shot), hard cuts throughout, no dissolves, high-saturation CGI in a warm gold "luxury" palette, and karaoke-style bold white captions at centre screen. The first shot (0:00–0:02) is a medium shot carrying the premise line. The end card is the product.
  - Another: about 22 shots in 50 s, word-by-word centre captions, and it "resolves into a clothing ad".
  - The shot log shows **each cut lands on a clause of 2–4 caption words** ("you go" / "while wearing").

### 1.2 Mechanics seen in the full transcript

The transcript comes from the same third-party source. Its premise is crude, so it is paraphrased here and only structural lines are quoted.

- **Premise as the first line (≤8 words):** "Hard being the son of [X]." It is stated as settled fact, with no setup.
- **Straight into second person:** "You go to school… You cry, they laugh."
- **Escalation ladder built on one repeated frame:** "no money in the world can buy back…" / "No allowance is large enough to…" / "A luxury vacation [isn't] gonna erase…"
- **Concrete details, then an aphorism:** "You inherit a problem you never signed up for."
- **A punchline that borrows another domain's metaphor:** finance and subscription vocabulary applied to an emotional wound: "paying social interest on somebody else's financial decision", then "[they] saw a monthly payout. You got a lifetime subscription…"
- **Deadpan pivot at the close.** The same sentence slides straight into the product: "…while wearing an Azerbaijan Technology Camel tee. Get yours at… Link in bio." The tone does not change; the tonal whiplash *is* the joke.

### 1.3 Twelve techniques to borrow (structure, not content or persona)

| # | Technique | What it looks like at our channel |
|---|---|---|
| 1 | **Flat-premise cold open.** The first line (2 s max) states an odd premise as fact. No "hey guys" and no question. | "Hard being a GPU in 2026." / "This is the most overworked chip on Earth." |
| 2 | **Switch to "you" by line 2.** Put the viewer inside the system. | "You get four thousand tokens at once. You have twelve milliseconds." |
| 3 | **Micro-antithesis beats.** 3–5-word paired clauses reset the rhythm after longer sentences. | "You predict. It punishes." |
| 4 | **Escalation ladder.** Same syntactic frame three times, each rung bigger. | "No cache is big enough… No cluster is fast enough… No budget is large enough…" |
| 5 | **Turn concrete into aphorism.** After 3–4 concrete images, one quotable universal line. Make it the thumbnail and the chapter title. | "A model is just a very confident compression of everything we wrote." |
| 6 | **Borrowed-domain metaphor as punchline.** Describe tech in human, finance or bureaucracy terms, or the reverse, as a chiasmus: "They saw X. You got Y." | "OpenAI saw a benchmark. You got a subscription." |
| 7 | **Deadpan commitment, flat pivot.** Play the absurd premise with total sincerity, then pivot to a recurring motif *without changing tone*. We pivot to lore or a callback, never merch-bait. | End each episode on the same dry sign-off line and card. |
| 8 | **Invented institutional vocabulary and a small lore canon.** Fake-official names ("Procedure Explained", "Edition™", "Enroll at…") and recurring characters build a world viewers return to. | "The Department of Gradients", "Token Postal Service", a recurring chrome mascot object. Reuse across episodes. |
| 9 | **Oddly specific, intimate titles.** "Spent 1600 minutes with myself." Precise numbers plus first-person framing read like a friend's text message. | "I watched a model think for 1,600 tokens." / lowercase community-post captions. |
| 10 | **Music-first narration.** His VO rides his own song. Lines land on musical phrase boundaries. | Write the VO to the bar. At 170 BPM half time, 2 bars ≈ 2.8 s, so one sentence per 2 bars. Leave 1 bar of air before reveals. |
| 11 | **Cut on the clause and illustrate literally.** One image per 2–4 words, hard cuts, centred word-by-word captions. | For long-form, keep the *principle*: every visual change lands on a clause boundary. Slow the average shot to 3–6 s and use camera moves instead of hard cuts to stay calm (see §3). |
| 12 | **State the stance: taste over tools.** He owns the AI question ("taste can't be automated") and turns AI's glitches into texture. | One recurring stance line. Let holographic glitch be a *designed* style, and keep typography and layout human-made. |

**On delivery (inferred from transcripts and descriptions):**
- Declarative, present-tense sentences with no hedges ("kind of", "maybe") and no filler.
- Sentence-final stops rather than trailing intonation, with a pause at each full stop that coincides with a cut.
- Rhetorical questions are rare and answered immediately.
- The "weird-but-cool" comes from sincerity applied to absurdity, not from a jokey voice.

### 1.4 Do not borrow

- His shock material: sexualised premises, and in one sampled video a racial caricature [3P shot log]. This is exactly the "tacky" line.
- Persona details: his Georgian/Azerbaijan lore, "uncles", or Children of Khan-style product end-cards.
- The high-saturation gold palette. Ours is graphite with a single turquoise.

---

## 2. Visual references (24, grouped), one technique to borrow from each

### A. FUI and holographic interfaces
1. **Territory Studio, *Blade Runner 2049* screen graphics.** [territorystudio.com](https://territorystudio.com/project/blade-runner-2049/) · [UI reel](https://www.youtube.com/watch?v=H07HumKRQKE). Borrow a limited palette plus designed decay: ghosting, warping and screen-burn used sparingly on clean utilitarian icons.
2. **GMUNK, *TRON: Legacy* holograms.** [gmunk.com](https://gmunk.com/TRON-Legacy) · [Behance](https://www.behance.net/gallery/52206573/Tron-Legacy-Holograms). Borrow generative line growth from real 3D meshes: they loaded OBJ geometry and grew branching light streamers from it (openFrameworks, with Josh Nimoy).
3. **GMUNK / Digital Domain, *TRON: Legacy* opening titles.** [gmunk.com](https://gmunk.com/TRON-Opening-Titles) · [MN8](https://www.mn8studio.com/project/tron-legacy-opening-titles) · [process video](https://vimeo.com/62739219). This is *the* reference for "gliding along line-work". Light lines travel a strict grid and light up grid points for parallax, and the whole piece was synced to Flynn's voiceover.
4. **GMUNK, *Oblivion* GFX.** [gmunk.com](https://gmunk.com/OBLIVION-GFX) · [Motionographer](https://motionographer.com/2013/04/19/bradley-g-munkowitz-oblivion-screen-graphics/). Borrow one graphic language across every screen: functional minimalism in a unified palette that reads on both dark and bright grounds.
5. **Ash Thorp, *Prometheus* UI concepts.** [Behance](https://www.behance.net/gallery/17932895/PROMETHEUS) · [ALT](https://www.altcinc.com/work/prometheus). Borrow the data-as-metaphor sculpture ("all human culture as a time capsule"). For us: "the internet compressed into a crystal".
6. **Jayse Hansen, Iron Man / Avengers HUDs.** [portfolio](https://jayse.tv/v2/?portfolio=hud-2-2) · [interview](https://thenextweb.com/news/jayse-hansen-on-creating-tools-the-avengers-use-to-fight-evil-touch-interfaces-and-project-glass). Widgets were researched from real avionics and designed to read from the front, back *and* side. That is essential when the camera orbits a hologram.
7. **Cantina Creative, *Infinity War / Endgame* reel.** [Art of VFX](https://www.artofvfx.com/avengers-infinity-war-endgame-reel-by-cantina-creative/) · [3dtotal](https://3dtotal.com/news/general/cantina-creative-avengers-reel). Borrow volumetric light: HUD elements that cast light and pick up reflections from the scene, so our turquoise line work should *light* the graphite floor.
8. **Perception, *Black Panther* technology.** [experienceperception.com](http://experienceperception.com/black-panther-fui.html). Every interface derives from one physical rule (vibranium sand, drawn from cymatics and acoustic levitation). Give our UI one "physics": for example, tokens behave like iron filings in a field.
9. ***Tron: Ares* (2025), ILM art department and GMUNK UI.** [ILM](https://www.ilm.com/inside-the-ilm-art-department-tron-ares/) · [Domus](https://www.domusweb.it/en/news/gallery/2025/10/10/tron-ares-digital-design-film-review.html) · [a designer's note on the UI](https://x.com/sorayatokyo/status/2015359035416150133). The UI was designed from story analysis, so every element carries a narrative beat. The film moves to sharper, angular grid geometry.

### B. Exploded views and orbit or assembly shots
10. **Daniel Simon, *TRON: Legacy* Light Cycle design.** [danielsimon.com](https://danielsimon.com/film-design/tron-legacy/) · [Asphalt & Rubber](https://www.asphaltandrubber.com/news/tron-lightcycle-design-daniel-simon/). Design hero objects as clean line silhouettes first, as industrial-design drawings, then render. Exploded callouts follow the silhouette logic.
11. **Branch Education (YouTube).** [channel](https://www.youtube.com/@BranchEducation/videos) · [site](https://branch.education/). Exploded assemblies and camera sweeps are hand-keyed in Blender and aligned to the VO. Parts separate *on the word that names them*.
12. **Bartosz Ciechanowski.** [ciechanow.ski](https://ciechanow.ski/). Progressive assembly: his mechanical-watch article builds the mechanism part by part, with one new component per beat.
13. **ManvsMachine.** [mvsm.com](https://mvsm.com/) · [Magnum "exploded" product work](https://www.stashmedia.tv/manvsmachine-demonstrates-proper-flavor-behavior-in-magnum-remix/). Intercut tactile material close-ups (chrome, brushed metal) with graphic abstraction.

### C. ASCII
14. **Andreas Gysin, play.core.** [GitHub](https://github.com/ertdfgcvb/play.core) · [feature](https://www.holo.mg/stream/andreas-gysin-ascii-live-coding-playground/). A per-cell, GLSL-like `main()` lets math (noise, distance fields) drive ASCII fields, rather than converting images to ASCII.
15. **Acerola, ASCII shader.** ["printing" transition](https://x.com/Acerola_t/status/1803039624677527926) · [GitHub](https://github.com/GarrettGunnell). Edge-aware glyphs (Difference of Gaussians plus Sobel) so `/ \ | _` follow contours. That is perfect for line-work outlines, and the "being printed" transition is directly usable.
16. **Oxide Computer, Mitos.** [GitHub](https://github.com/oxidecomputer/mitos). A brand-asset ASCII generator built on play.core. Build our own in-house ASCII texture tool so the textures stay on-brand.

### D. Minimal data art
17. **Ryoji Ikeda, *datamatics* / *test pattern* / *data.tron*.** [datamatics](https://www.ryojiikeda.com/project/datamatics/) · [test pattern](https://www.ryojiikeda.com/project/testpattern/) · [data.tron](https://forma.org.uk/projects/datamatics/data-tron). Data becomes barcodes and binary patterns, with sound and image locked frame-accurately at perceptual thresholds. Use this in short doses only, because of flicker and photosensitivity risk.

### E. Satisfying 3D loops
18. **Andreas Wannerstedt, "Oddly Satisfying".** [interview](https://designwanted.com/andreas-wannerstedt-interview/) · [Scandinavian MIND](https://scandinavianmind.com/how-andreas-wannerstedt-became-a-forerunner-for-oddly-satisfying-art/). Perfect loops with Rube-Goldberg logic and integrated sound design, built "to trigger and release a sense of satisfaction" and feel hypnotic and calm.

### F. Morph-driven explainers
19. **3Blue1Brown / Manim.** [manim](https://github.com/3b1b/manim) · [attention lesson](https://www.3blue1brown.com/lessons/attention/). "Universal transformation": any object morphs into any other. Morph word → token → vector instead of cutting between them.
20. **Welch Labs.** [site](https://www.welchlabs.com/) · [YouTube](https://www.youtube.com/@WelchLabs). Mixes hand-drawn overhead inserts with Manim animation, with history and human narrative carrying the maths. Tactile inserts keep a CG-heavy look warm.

### G. Kinetic typography
21. **Saul Bass.** [Art of the Title](https://www.artofthetitle.com/designer/saul-bass/). Type and shape act as narrative agents, and reduction does the work.
22. ***Stranger Things* main titles (Imaginary Forces).** [Art of the Title](https://www.artofthetitle.com/title/stranger-things/) · [Maxon case study](https://www.maxon.net/en/article/animating-the-stranger-things-title-sequence-case-study). Large hollow letterforms drift through a void and assemble slowly, with optical imperfections (light passed through Kodaliths). Swap the red for turquoise strokes on graphite and have the camera glide along the letters.

### H. Premium explainer benchmarks and AI imagery
23. **Kurzgesagt.** [Wikipedia](https://en.wikipedia.org/wiki/Kurzgesagt). Not our look, but a benchmark for a *system*: consistent shapes, colour logic and orchestrated layouts across every episode.
24. **Google DeepMind, *Visualising AI*.** [deepmind.com](https://www.deepmind.com/visualising-ai) · [It's Nice That](https://www.itsnicethat.com/features/google-deepmind-visualising-ai-digital-sponsored-content-051224). Commissioned, free-to-use artworks that avoid robot and brain clichés. A calibration set for "AI imagery that isn't tacky".

Archive for more frames: [HUDS+GUIS: Blade Runner 2049](https://www.hudsandguis.com/home/2018/blade-runner-2049).

---

## 3. Perception science: 18 actionable rules

### Satisfying motion and layout

**R1. Make every frame instantly readable. Ease of processing is felt as beauty.**
Aesthetic pleasure rises with processing fluency: figural goodness, figure-ground contrast, repetition, symmetry and prototypicality.
- Apply it: one focal subject per frame and a high-contrast graphite/turquoise split.
- Build layouts on a symmetric or column grid, and reuse the same card, stroke and type system.

Source: Reber, Schwarz & Winkielman 2004, [PDF](https://pages.ucsd.edu/~pwinkiel/reber-schwarz-winkielman-beauty-PSPR-2004.pdf) · [journal](https://journals.sagepub.com/doi/10.1207/s15327957pspr0804_3).

**R2. Prime before you reveal.**
The same paper reports that visual priming raises fluency and liking.
- Apply it: flash a faint ghost wireframe or ASCII silhouette 0.5–1 s before the solid object resolves.
- Tease a chrome number's outline before it lands.

Source: [Reber et al. 2004](https://pages.ucsd.edu/~pwinkiel/reber-schwarz-winkielman-beauty-PSPR-2004.pdf).

**R3. Move like a hand: minimum-jerk easing.**
Natural point-to-point motion has bell-shaped velocity. On curved paths, speed drops where curvature is high.
- Apply it: use the ease `s(τ) = 10τ³ − 15τ⁴ + 6τ⁵` for camera and object moves. No linear starts or stops.
- In orbits and dolly paths, slow down on tight turns.

Source: Flash & Hogan 1985, [J Neurosci](https://www.jneurosci.org/content/5/7/1688).

**R4. Predictable grid, one surprise per phrase.**
Pleasure is highest when a surprising event lands in a *predictable* context, or when an *expected* event resolves an uncertain one. This was measured on about 80,000 chords.
- Apply it: keep grid, rhythm and camera logic steady, then break them once per phrase (a part snaps in from an unexpected side).
- After chaotic sections, resolve with the expected.

Source: Cheung et al. 2019, [Current Biology](https://www.cell.com/current-biology/fulltext/S0960-9822(19)31258-8) · [summary](https://www.sciencedaily.com/releases/2019/11/191107111744.htm).

**R5. Medium complexity wins (inverted U).**
Medium syncopation produced the most pleasure and the strongest urge to move. Low and high syncopation did less.
- Apply it: keep ASCII density, edit density and break chops at *medium*.
- Caveat: a 2024/25 replication with new patterns found a null effect, so treat this as a guideline, not a law.

Source: Witek et al. 2014, [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0094446) · [null replication](https://pmc.ncbi.nlm.nih.gov/articles/PMC11567550/).

**R6. Design for closure, and close loudly.**
"Satisfying" loops are built to "trigger and release a sense of satisfaction": parts fit, loops seam, things complete.
- Apply it: let line work draw itself incomplete, then snap shut, and put a crisp switch-click on the exact closing frame.
- Make B-roll loops seamless: the first and last frames match, with constant velocity through the seam.

Sources: [Wannerstedt interview](https://designwanted.com/andreas-wannerstedt-interview/); "figural goodness" in [Reber et al.](https://pages.ucsd.edu/~pwinkiel/reber-schwarz-winkielman-beauty-PSPR-2004.pdf).

### Curiosity and open loops

**R7. Size the curiosity gap. The viewer should *almost* know.**
Curiosity is a drive triggered by a perceived knowledge gap. It fades when the gap is too big (hopeless) or too small (obvious).
- Apply it: open each chapter with a question the viewer has partial footing on ("You know autocomplete. So why can this write a proof?").

Sources: Loewenstein 1994, reviewed in Kidd & Hayden 2015, [Neuron](https://www.sciencedirect.com/science/article/pii/S0896627315007679) · [explainer](https://psychologyfanatic.com/information-gap-theory/).

**R8. Teach inside the curiosity window.**
In a high-curiosity state, people remember the answer *and* incidental material shown while they wait, both immediately and a day later. Midbrain dopamine and hippocampal activity drive this.
- Apply it: after posing the question, put the key diagram or definition *before* the answer lands.

Source: Gruber, Gelman & Ranganath 2014, [Neuron DOI](https://doi.org/10.1016/j.neuron.2014.08.060).

**R9. Open loops drive continuation, not memory. So close them.**
A 2025 meta-analysis found **no** reliable memory advantage for unfinished tasks (the Zeigarnik effect; pooled recall ratio about 0.99). It did find a robust urge to *resume* them (the Ovsiankina effect; about 67% vs a 50% baseline).
- Apply it: use open loops ("we'll come back to the tokenizer") to keep people watching, then close every loop explicitly with a visual click and a callback line.

Source: Ghibellini & Meier 2025, [Humanities & Social Sciences Communications](https://www.nature.com/articles/s41599-025-05000-w).

### Audio-visual synchrony

**R10. Sync sound to visual transients. Synchrony makes things pop.**
A tone synchronised with a visual change makes that element "pop out" of clutter, even though the tone carries no spatial information. It works only with *transient* (abrupt) visual events, not gradual ones.
- Apply it: give ticks to snaps, cuts and part separations, never to slow fades.

Sources: Van der Burg et al. 2008, [Semantic Scholar](https://www.semanticscholar.org/paper/Pip-and-pop%3A-nonspatial-auditory-signals-improve-Burg-Olivers/7ddb4798846e0d5442781aeb1b121d449a0b905d); 2010, [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0010664).

**R11. Land sound 0–20 ms after the visual event, never early.**
Broadcast tolerance (EBU R37) is audio no more than 40 ms early and no more than 60 ms late. ITU-R BT.1359 puts detectability at about +45 ms (early) and −125 ms (late), so people tolerate late sound far better than early.
- Apply it: nudge SFX slightly late, not early.

Sources: [Audio-to-video synchronization](https://en.wikipedia.org/wiki/Audio-to-video_synchronization) · [TV Tech](https://www.tvtechnology.com/opinions/updating-lip-sync-issues).

### Retention and pacing

**R12. Treat the first 30 seconds as their own product.**
YouTube Analytics reports intro retention for the **first 30 s** and flags top moments, spikes and dips.
- Apply it: state the premise in the first line (technique #1), show the hero visual by second 5, and promise the payoff by second 20.
- Diagnose every dip against the edit.

Sources: [YouTube Help: key moments for audience retention](https://support.google.com/youtube/answer/9314415) · [Backlinko retention guide](https://backlinko.com/hub/youtube/retention).

**R13. Use pattern interrupts, but stay within working-memory capacity.**
Structural features trigger orienting responses that boost attention: cuts, edits, voice changes, sound effects, music onsets. Too many, stacked, overload processing capacity.
- Apply it (our heuristic): change *one* dimension every ~3–8 s in long-form (a camera move, card, SFX or music layer). Never stack a cut, new information and a music change on the same dense sentence.
- Shorts can run faster: santeluca averages about 2 s per shot.

Source: Lang 2000, "The Limited Capacity Model of Mediated Message Processing", *J. Communication* 50(1):46–70, DOI 10.1111/j.1460-2466.2000.tb02833.x. Auditory structural features: Potter & Choi 2006, cited in Neuendorf's *Content Analysis Guidebook* [3P].

### Sound, body and arousal

**R14. Silence resets the body. Drop out before big reveals.**
In cardio-respiratory measurements, faster music raised breathing rate and arousal. The paper's headline finding is "the importance of silence": pauses between tracks produced marked relaxation.
- Apply it: take 150–400 ms of near-silence (music ducked, sub only) before a key reveal or drop. It resets arousal so the next hit lands without the piece becoming overstimulating.

Source: Bernardi, Porta & Sleight 2006, [Heart / PubMed](http://www.ncbi.nlm.nih.gov/pubmed/16199412).

**R15. Tempo sets arousal. Run jungle at two speeds at once.**
The same study links faster tempi to higher arousal. [K] Jungle at about 170 BPM with bass and pads moving in half time (about 85 BPM feel) gives motion without agitation.
- Apply it: thin the double-time breaks under dense VO. Bring them back under visual-only passages.

Source: [Bernardi et al. 2006](http://www.ncbi.nlm.nih.gov/pubmed/16199412).

**R16. Very-low bass is *felt*: use it briefly, for the stomach-drop.**
At a live concert, very-low-frequency speakers (inaudible to the audience) increased dancing by about 12%.
- Sustained infrasound near 17–19 Hz has been linked to unease. Tandy's 18.98 Hz extractor fan is the classic case of "ghost" anxiety.
- Apply it: use short sub drops (sine glide, e.g. 80→30 Hz over 0.8–1.5 s) on transitions. Never sit a sustained sub-20 Hz tone under narration.
- Add harmonics so phone speakers imply the fundamental [K].

Sources: Cameron et al. 2022, [Current Biology](https://www.cell.com/current-biology/fulltext/S0960-9822(22)01535-4) · [ScienceDaily](https://www.sciencedaily.com/releases/2022/11/221107114445.htm) · [NPR](https://www.npr.org/2022/11/10/1135856162/inaudible-low-frequency-bass-makes-people-boogie-more-on-the-dancefloor). Tandy & Lawrence 1998, [PDF](http://www.richardwiseman.com/resources/ghost-in-machine.pdf) · [Higgs Centre explainer](https://higgs.ph.ed.ac.uk/outreach/higgshalloween-2021/haunted-frequency).

**R17. The "falling" feeling: a *descending* Shepard–Risset glide, then resolve.**
Octave-spaced partials under a bell-shaped spectral envelope produce endless apparent descent (or ascent) with no arrival. That is the sensation of falling without a floor. Nolan and Zimmer wrote *Dunkirk* around the Shepard illusion [3P: Wikipedia text].
- Apply it: 3–8 s descending glide under a camera dive or vortex, then silence (R14), then the sub drop (R16) on the downbeat.
- Don't leave it unresolved, or it becomes dread instead of thrill.

Sources: [Shepard tone](https://en.wikipedia.org/wiki/Shepard_tone) · [Shepard–Risset glissando](https://en.wikipedia.org/wiki/Shepard_tone#Shepard%E2%80%93Risset_glissando). Original paper: Shepard 1964, *JASA* 36:2346–2353.

**R18. Tactile UI sounds signal quality, but keep them short, dry and non-oral.**
- ASMR videos raised pleasant affect *only* in people who experience ASMR, while lowering heart rate and raising skin conductance. Tactile triggers help some viewers and irritate others.
- Separately, boosting the high-frequency crunch made crisps taste crisper and fresher. Crisp transients read as "fresh and precise".
- Apply it:
  - Switch-like clicks with crisp tops, rolled off below about 80 Hz, sitting under the VO.
  - Vary them with round-robin samples (R10 means they fire often, so avoid machine-gunning).
  - Avoid mouth, whisper and chewing-like sounds.

Sources: Poerio et al. 2018, [PLOS ONE DOI](https://doi.org/10.1371/journal.pone.0196645). Zampini & Spence 2004, *J. Sensory Studies* 19:347–363, "The role of auditory cues in modulating the perceived crispness and staleness of potato chips".

### Pacing template for a 10-minute video (heuristic, built from R4, R7–R9, R12–R14 and R16–R17)

| Time | Beat |
|---|---|
| 0:00–0:02 | Premise line over the hero object. |
| 0:02–0:20 | Second-person immersion plus open loop #1. |
| ≈0:25 | First orbit reveal with one surprise. |
| Every 60–90 s | A micro-payoff (a loop closes with a click). |
| Every 2–3 min | A bigger reveal with the silence → Shepard → sub drop sequence. |
| Mid-point | Open loop #2. |
| Final 30 s | Close all loops, then the aphorism, then the deadpan sign-off. |

---

## 4. Higgsfield AI (state as of Sep 2026)

Higgsfield was founded by an ex-Snap executive and was valued at $1.3B in Jan 2026 ([TechCrunch](https://techcrunch.com/2026/01/15/ai-video-startup-higgsfield-founded-by-ex-snap-exec-lands-1-3b-valuation/)). "Supercomputer 2.0" is its enterprise agent, built with NVIDIA ([TheNextWeb](https://thenextweb.com/news/higgsfield-supercomputer-enterprise-marketing-nvidia)).

Most product facts below come from a July 2026 third-party research note that cites Higgsfield's pages [3P: GitHub `BELCORT-SDN-BHD/FIKIRTIVE`, `docs/archive/research/2026-07-03-higgsfield.md`]. Official pages it cites include [ai-video](https://higgsfield.ai/ai-video), [camera-controls](https://higgsfield.ai/camera-controls), [cinematic-video-generator](https://higgsfield.ai/cinematic-video-generator), [soul-intro](https://higgsfield.ai/soul-intro), [ai-image](https://higgsfield.ai/ai-image), [lipsync-studio](https://higgsfield.ai/lipsync-studio), [pricing](https://higgsfield.ai/pricing), [popcorn](https://higgsfield.ai/popcorn), [mcp](https://higgsfield.ai/mcp), [cli](https://higgsfield.ai/cli) and [credits help](https://higgsfield.ai/creator-hub/help-center/credits/how-credits-work).

### 4.1 Products relevant to us
- **Camera Controls:** 65 one-click presets, with **up to 3 motion axes stacked**. This is their signature differentiator [3P].
- **DoP ("Director of Photography"):** Higgsfield's own image-to-video model, in Standard and Turbo versions.
  - The API accepts `image_url`, optional `end_image_url` (the last frame, useful to lock an exploded end state), `prompt`, and `motions: [{id, strength}]`. The strength setting is how you keep camera moves *tasteful*.
  - One integrator's probes found that `duration`, `resolution` and `aspect_ratio` are *not* accepted on `dop/standard`, and that motion IDs are not publicly listed [3P: GitHub `aqm857886159/Nomi`, 2026-09-17 probe logs].
- **Video model hub** (T2V, I2V, V2V, Draw-to-Video, First/Last Frame, Motion Control from a reference video, Character Locking) [3P]:
  - Seedance 2.0: native audio and video, with lip-sync, SFX and music sync.
  - Kling 3.0 (4K), Kling O1, Kling 2.6 / 2.5 Turbo / 2.1.
  - Veo 3.1.
  - Wan 2.7 / 2.6.
  - MiniMax Hailuo 02.
  - Sora 2, which the note says OpenAI is retiring (web Apr 2026, API Sep 2026). Don't build on it.
- **Cinema Studio 3.x:** choose a camera body (RED, Sony, IMAX, ARRI, Panavision), spherical or anamorphic lenses, focal length, aperture and depth of field, and sensor size. Supports 21:9 and has photo and video modes [3P].
- **Soul 2.0** (in-house image model) [3P]:
  - 20+ aesthetic presets, e.g. Editorial Street Style, Old Smartphone, Y2K Studio, Frutiger Aero, Subtle Flash, Siren.
  - **Soul ID**: train a character from 20 or more photos in about 3 minutes.
  - Soul Inpaint, and Soul Cinema (an API endpoint).
- **Other image models:** Nano Banana Pro (draw-to-edit, up to 8 references, native 4K), GPT Image 2, Seedream 4.5, FLUX, Reve, Kling O1 [3P]. Seedream v4 and Qwen Image 3 are exposed via the API [3P code].
- **Lipsync Studio:** combines Speak v2, lipsync-2, InfiniteTalk, Kling AI Avatar, Kling Lipsync and Veo 3. Script or audio in, talking avatar out, and it can use your Soul ID as presenter [3P].
- **Also available:**
  - Popcorn: consistent storyboards.
  - Marketing Studio: runs on Seedance 2.0 with 10 modes, including "Hyper Motion" CGI product hero shots.
  - UGC Factory, and Apps (41 listed).
  - Supercomputer: an agent that shows a credit quote you approve before it runs.
  - MCP server and CLI [3P].

### 4.2 Camera-preset names (use them verbatim in prompts)

From a scrape allowlist of the Higgsfield UI [3P: GitHub `m0saan/comfyui-modal`] plus other integrators:

`General, Static, 360 Orbit, Arc Left, Lazy Susan, Bullet Time, Aerial Pullback, BTS, Buckle Up, Car Chasing, Car Grip, Crane Up, Crane Down, Crane Over The Head, Crash Zoom In, Crash Zoom Out, Dolly In, Dolly Out, Dolly Left, Dolly Right, Dolly Zoom In, Dolly Zoom Out, Double Dolly, Super Dolly In, Super Dolly Out, Dutch Angle, Eating Zoom, Fisheye, Flying Cam Transition, Focus Change, FPV Drone, Glam, Handheld, Head Tracking, Hero Cam, Hyperlapse, Incline, Jib up, Jib down, Low Shutter, Mouth In, Object POV, Overhead, Rapid Zoom In, Rapid Zoom Out, Road Rush, Robo Arm, Snorricam, Through Object In, Through Object Out, Tilt Up, Tilt Down, Timelapse Human, Timelapse Landscape, Whip Pan, Wiggle`

The same list also contains effect-style presets that are *off-brand* for us: Levitation, Rap Flex, Tentacles, and similar.

**Best presets for our look:**
- 360 Orbit, Lazy Susan and Arc Left for exploded subjects.
- Super Dolly In and Through Object In for gliding along line work.
- Crane Up and Aerial Pullback for scale reveals.
- Robo Arm for precise macro teardowns.
- Bullet Time for frozen exploded moments.
- Dolly Zoom In and FPV Drone for the vortex or falling feel.
- Focus Change for label reveals.
- Static for editorial cards.

### 4.3 Pricing and credits (Jul 2026 snapshot; verify on the pricing page)

| Plan | Price | Credits / month | Notes |
|---|---|---|---|
| Free | $0 | about 10 per day | watermarked |
| Starter | $15 | 200 | some models only; no Veo 3 family |
| Plus | $49 ($39/mo billed yearly) | 1,000 | all models |
| Ultra | $129 ($99/mo billed yearly) | 3,000 (expandable to 9,000) | 365-day "unlimited" pass on **one** chosen model |
| Business | $89/seat ($62 billed yearly) | 1,500 per seat, pooled | — |

- Credits **reset monthly** and do not roll over.
- Top-ups are about $5 per 100 credits and expire after 90 days (unverified in the note).
- "Unlimited" and free generations apply **only on the web app**. They do not apply via MCP, CLI, Canvas or Supercomputer.
- Agent chats also cost credits [3P]. The optional *Seedance Unlimited* add-on gives 30 days of Seedance 2.0 Fast at 480/720p on a slower queue [3P].
- **Real-world cost:**
  - Third-party estimate [3P], including 3–5 discarded iterations: Kling 3.0 costs about $0.61–1.03 per usable clip; Veo 3.1 or Sora 2 about $3.36–9.33.
  - One integrator's logged API cost: Soul 2 text-to-image $0.004 per image; DoP Turbo $0.407 for a 1264×720, 5.4 s clip [3P].
- **Reputation:** Trustpilot 3.2/5 from 1,200+ reviews. The main complaints are about "unlimited" wording [3P].

### 4.4 API and host names
- **Official Python SDK:** [github.com/higgsfield-ai/higgsfield-client](https://github.com/higgsfield-ai/higgsfield-client), created Nov 2025 and active.
  - Its source sets `BASE_URL = 'https://api.higgsfield.ai'`.
  - Credentials come from **Higgsfield Cloud** (`https://cloud.higgsfield.ai/`).
  - Auth header: `Authorization: Key <key_id>:<key_secret>`.
  - Methods: `submit / subscribe / status / result / cancel`. Uploads go through `POST /files/generate-upload-url`, which returns a presigned S3 URL.
  - There is also an Agent API, available on request.
- **`platform.higgsfield.ai`**
  - Returned in job `status_url` and `cancel_url`.
  - Also the default base in many integrations, for example Symfony AI's Higgsfield bridge ("Defaults to https://platform.higgsfield.ai") [3P code].
- **Model routes seen** [3P code]:
  - `/higgsfield-ai/dop/standard` (and turbo), `/higgsfield-ai/soul/standard`, `/higgsfield-ai/soul/cinema`
  - `/bytedance/seedream/v4/text-to-image`, `/alibaba/qwen-image-3/text-to-image`, `/marketing-studio/image`
  - Older scripts use `/v1/image2video/dop` and `/v1/text2image/soul` with `hf-api-key`/`hf-secret` headers. That is the legacy style.
- **Outputs** are delivered from CloudFront; uploads go to `fnf-api-input-prod-*.s3.amazonaws.com` [3P].

### 4.5 Workflow for the Chrome & Marl look
1. Build **keyframes as stills.** Use Soul 2.0, Nano Banana Pro or Seedream, or better, render exact hero objects and type in Blender or C4D.
2. Run **I2V** in DoP or Kling 3.0 with a named preset at low-to-medium motion strength. Use **First/Last Frame** to lock the "assembled → exploded" states.
3. **Put all typography, chrome numbers and ASCII overlays in post.** Generated text is unreliable.
4. Grade to lock the palette: graphite and slate at about 5–15% luminance, a single #12B8AC accent, chrome speculars. Add grain.
5. Keep clips at 5 s and cut on clauses (santeluca's rule), with motion continuity across cuts.

**Prompt tips seen in third-party skill files [3P]:**
- Name presets exactly.
- Write continuous "fluid narrative" action rather than timestamps.
- Stack at most 2 motions for calm.

### 4.6 Ten prompts in house style

Shared style suffix (append to all): *"Dark graphite void, matte slate floor with a faint turquoise (#12B8AC) grid fading into fog, thin single-weight turquoise holographic line work, chrome and brushed-metal materials, soft top light with crisp rim light, subtle scanlines and fine ASCII glyph dust, calm precise motion, only turquoise as accent color, no neon rainbow, no lens-flare spam, no readable text, cinematic 2.39:1, fine film grain."*

1. **Exploded GPU** · Preset: **360 Orbit** · Model: DoP Standard or Kling 3.0 I2V, First/Last Frame. *"A graphics card floats in the void and separates into a clean exploded view along one axis: aluminum heatsink fins, copper heat pipes, green-black PCB, silicon die, memory chips. Every part drifts apart with equal spacing and stops precisely, each outlined by a thin turquoise holographic contour, with tiny ASCII part labels flickering on beside them. 360 Orbit, slow and constant."*
2. **Token light-cycle** · Preset: **FPV Drone** · Model: Kling 3.0. *"A small glowing capsule labelled only by light (a 'token') races across an infinite graphite grid, leaving a razor-thin turquoise light-wall that folds into crisp right-angle turns, Tron-style. Chrome reflections streak on the floor. FPV Drone following low behind, smooth banking, no shake."*
3. **Attention threads** · Preset: **Arc Left** · Model: DoP Standard. *"Twelve frosted-glass word cards hover in a row above a slate table. Fine turquoise threads connect every card to every other, brighter where the connection is stronger, and ASCII digits ripple along the threads like current. Arc Left, a slow semicircle revealing the depth of the web."*
4. **Line-work typography glide** · Preset: **Super Dolly In** · Model: DoP with a Blender-rendered start frame that contains the real letters. *"Monumental hollow letterforms built from single turquoise light strokes stand on a dark slate plane like architecture. The camera glides at letter-height along the strokes, past corners and counters. ASCII dust drifts through the beams. Super Dolly In, steady, minimum-jerk ease."*
5. **Embedding galaxy** · Preset: **Dolly Zoom In** · Model: Kling 3.0. *"A vast cloud of tiny chrome points hangs in the graphite void, loosely clustered. A turquoise wireframe sphere highlights one cluster while faint ASCII tags orbit it. Dolly Zoom In, a vertigo pull that makes the cluster swell while the background stretches away."*
6. **Server blade, frozen** · Preset: **Bullet Time** · Model: DoP Standard. *"A server blade sliding out of a monolithic graphite rack is frozen mid-motion. Its components hang in an exploded arrangement with turquoise callout lines and ASCII part numbers, and dust motes are frozen in the air. Bullet Time, an arc around the frozen instant."*
7. **Switch teardown macro** · Preset: **Robo Arm** · Model: DoP or Kling 3.0. *"Extreme macro on a slate surface: a mechanical keyboard switch separates into top housing, translucent stem, steel spring and bottom housing, each part rimmed by a turquoise contour. The spring compresses and releases once. Robo Arm, a precise motion-control pass sweeping close past each part."*
8. **Neural city reveal** · Preset: **Crane Up** (alternative: **Aerial Pullback**) · Model: Veo 3.1 or Kling 3.0. *"A neural network rendered as a night city of graphite monoliths joined by turquoise light-roads; signal pulses travel the roads as packets of light. Crane Up rising from street level to reveal the full layered grid."*
9. **Model-weights crystal** · Preset: **Lazy Susan** · Model: DoP Standard. *"A faceted chrome crystal on a slate plinth rotates as if on a turntable. Inside, layers of turquoise wireframe planes are stacked like a transformer's layers, and ASCII noise shimmers across the facets. Lazy Susan, slow, perfectly smooth, seamless loop."*
10. **Vortex drop** · Preset: **Through Object In** (then cut to **FPV Drone**) · Model: Kling 3.0. *"Concentric rings of turquoise line work form a spiral tunnel descending into darkness, with ASCII characters streaming along the tunnel walls. The camera slips through the first ring and falls down the center, accelerating then easing to a stop above a faint grid. Through Object In."*
    - Sound: pair with the descending Shepard glide, then 200 ms silence, then a sub drop (R14, R16, R17).

---

## 5. Jungle as a narration bed

### 5.1 Anatomy [K unless marked]
- **Tempo.** About 160–175 BPM (early-'90s jungle ran about 160–170; modern drum & bass about 172–176). For a bed, use roughly 164–172 BPM with bass, pads and chord changes at **half time (about 82–86 BPM)**. The ear then rides the slow layer while the breaks shimmer on top.
- **Breakbeats.** Classic sources are "Amen, Brother" (The Winstons, 1969), "Think (About It)" (Lyn Collins, 1972), "Apache" (Incredible Bongo Band, 1973) and "Funky Drummer" (James Brown, 1970). Breaks are sped up from their original tempos (the Amen sits in the mid-130s BPM) [K].
- **Chopping ("choppage").**
  - Slice the break into individual hits and re-sequence them.
  - Techniques: ghost-note shuffles, snare rolls and "rushes", reversed and pitched snares, and the metallic artefacts of time-stretching.
  - Layer a clean programmed kick and snare underneath for weight. High-pass the break (about 150–250 Hz) so the sub owns the low end.
  - "Choppage", resampling and time-stretch artefacts are defined in a jungle glossary [3P: GitHub `visualsbytheRob/Wavgen.ca_on_GitHub`].
- **Reese bass.** Named after Kevin Saunderson's 1988 track "Just Want Another Chance", released under his "Reese" alias. The sound is two or more detuned oscillators beating against each other; the original is credited to a Casio CZ synth. It was taken up by jungle, for example Renegade "Terrorist" (Moving Shadow, 1994), Alex Reece "Pulp Fiction" (Metalheadz, 1995; spelled "Pulp Friction" in the source text) and DJ Trace "Sonar" (1998) [3P: Wikipedia-derived text].
  - For a calm bed: low-pass the Reese to about 300–800 Hz, detune gently (±5–15 cents), and let a slow LFO "breathe" the filter. Keep it mono below about 120 Hz.
- **Sub.** A pure sine at 40–60 Hz on root notes with slow glides, lightly sidechained. It is the dub-reggae soundsystem inheritance.
- **Pads and atmosphere.** Rhodes 7th/9th chords, warm analog or string pads, choir "ahh"s, distant diva fragments, rain or wind field recordings, a ride cymbal as the time-keeper, long dark reverbs. **No bright shimmer or sparkle** (your "less magical" brief).
- **Arrangement.** 8/16/32-bar phrases: DJ intro (16–32 bars, sparse), first drop, breakdown (pads and sub only), second drop, outro.

### 5.2 Subgenres that suit calm-but-flowing narration
- **Atmospheric / intelligent jungle**, around 1993–97: LTJ Bukem's Good Looking Records and Moving Shadow. Lush pads, rolling breaks, a sense of space. **Best fit.**
- **Liquid drum & bass** (late '90s onward; Hospital Records, Calibre, High Contrast): warmer, more musical, smoother breaks.
- **Autonomic / minimal** (around 2009; dBridge, Instra:mental): sparse, deep sub, half-time feel. Great under dense explanation.
- **Avoid under VO:** techstep, neurofunk and darkstep (too aggressive), and ragga jungle (its vocals clash with speech).

### 5.3 Mixing the bed under VO (heuristics)
- Deliver **stems**: breaks, sub, Reese, pads, FX. Under dense lines, mute the chopped snares and keep ride, sub and pads. Bring the full breaks back for visual-only passages.
- Sidechain the music to the VO by about 3–6 dB. Carve 1–4 kHz in the pads for intelligibility.
- Write VO to the bar: 2 bars at half time ≈ 2.8 s. Land reveals on the downbeat of a phrase.
- Master to the loudness target you use for YouTube, then check on phone speakers. Put harmonics on the sub so it translates (R16).

### 5.4 Reference tracks (10) [K, titles and years from memory; spot-check]
1. LTJ Bukem, "Horizons" (1995): the atmospheric template.
2. LTJ Bukem, "Music" (1993): long pad-led flow.
3. Blame, "Music Takes You" (1992): euphoric but spacious.
4. Omni Trio, "Renegade Snares" (1993): piano-led and melodic; famous chopped snares.
5. PFM, "One & Only" (1995): dreamy and airy.
6. Goldie, "Inner City Life" (1994). Burial's 2017 remix is an even closer bed reference.
7. Adam F, "Circles" (1995): jazzy, warm Rhodes.
8. Alex Reece, "Pulp Fiction" (1995): minimal two-step roller with a Reese bass [3P].
9. Photek, "The Hidden Camera" (1996): restrained, precise, cinematic.
10. A Guy Called Gerald, "Finley's Rainbow" (from *Black Secret Technology*, 1995): textural.

Bass study: Reese (Kevin Saunderson), "Just Want Another Chance" (1988) [3P].

### 5.5 Content ID and licensing
- **How Content ID works.** Rights holders upload reference files, uploads are scanned, and a match can block, monetise or track the video ([YouTube Help](https://support.google.com/youtube/answer/2797370)).
- **Self-made music.** You own both composition and recording.
  - Keep project files, stems and dated exports as proof of authorship.
  - If you later distribute the same tracks through a distributor that opts into Content ID, **allow-list your own channel** so you aren't claimed on your own uploads [K].
  - Don't register music in Content ID unless you hold exclusive rights to all of it, including samples [K].
- **AI-generated music.**
  - The US Copyright Office says protection "does not extend to purely AI-generated material, or material where there is insufficient human control over the expressive elements" ([Part 2 report, Jan 2025](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf) · [hub](https://www.copyright.gov/ai/)). You may have *usage rights* but no exclusive right to enforce or register.
  - Tool terms matter. Per 2026 third-party summaries [3P], Suno's free tier is non-commercial. Pro/Premier grant commercial-use rights for songs made *while subscribed*, and Suno's newer documentation dropped the "you own your songs" wording. Re-check the current terms before publishing.
  - Human-authored layers (your own chords, arrangement, played parts, edits) strengthen your position.
- **YouTube monetisation.** On 15 Jul 2025 YouTube renamed its "repetitious content" policy to **"inauthentic content"**, explicitly covering mass-produced or repetitive content [3P: archived policy text]. An AI-heavy channel should keep human authorship obvious: an original script, a real VO, and bespoke design.
- **The Amen break.**
  - It is a roughly 6–7 s drum break played by **Gregory Coleman** on The Winstons' B-side "Amen, Brother" (1969). It is described as the most-sampled recording in history, with over 7,500 documented uses [3P].
  - The band reportedly never earned royalties from sampling, and Coleman died homeless in 2006 [3P].
  - The **sound recording and the composition are still under copyright.** Sample-pack "royalty-free Amen" edits usually *derive from that recording*, so the pack can't license rights its maker never had.
  - **Practical risks:**
    - (a) Content ID false matches against other registered tracks that use the same raw break.
    - (b) Manual claims.
    - (c) The ethics of the unpaid-creator story, given our "never tacky" stance.
  - **Recommendation:** re-play or re-program "Amen-style" patterns from your own or clearly licensed one-shots or multitrack drums. A rhythm pattern alone is generally hard to protect; the *recording* is the problem [K].

---

## 6. The "banana" keyboard: identification and sound for synthesis

### 6.1 What they probably mean
1. **Keychron "Banana" tactile switches** (most likely, because Keychron sells whole boards with them, which fits "banana keyboard"):
   - **K Pro Banana:** tactile, PC/nylon housing, POM stem, 57 g, 2.2 mm pre-travel, 3.3 mm total travel, 3-pin. Shipped in gasket-mounted aluminium Keychron Q-Pro boards [3P: switch datasets on GitHub; product listings].
   - **Super Banana:** tactile, 5-pin, 47 g actuation / 60 g bottom-out, 2.0 mm pre-travel, 3.6 mm total. Used on the Keychron C1 Pro 8K, K10 Max and Lemokey P1.
     - WIRED: "Keychron's tactile Super Banana switches are poppy and responsive."
     - Reviewed by ThereminGoat (22 Dec 2024).
     - [3P: WIRED text archived on GitHub; GitHub `ThereminGoat/switch-scores`]
   - Also "Lava Optical Banana" (tactile, 57 g) [3P].
2. **C³Equalz × TKC "Banana Split"** (enthusiast linear): made by JWK/Durock, 5-pin, filmed. Originally C³'s "Macho" switch (early 2020), relaunched Sept 2020 as the first of TKC's "Snack Time" line. It is "very comparable to Alpaca" linears [3P: GitHub `BWLR/switches.mx` data] · [sound comparison: Banana Split vs Alpaca v2](https://www.youtube.com/watch?v=Tf6wUgKwL5c).
3. Less likely: the budget Ajazz × Huano "Banana" switch ([vendor page](https://thockeys.com/banana-switch-46-pack/)).

**Ask the creator one question: "bump or smooth?"**
- **Tactile** ("poppy"): Keychron Banana.
- **Smooth** ("creamy"): Banana Split.

### 6.2 Sound vocabulary (enthusiast terms translated) [K]
- **Thock:** low-pitched, rounded bottom-out. Energy sits in the low-mids (about 150–600 Hz), highs are damped, decay is short. Comes from POM/nylon, dense PBT caps, foam and gasket mounts.
- **Clack:** brighter, higher-pitched and sharper. Energy about 1.5–6 kHz, harder attack. Comes from PC housings, thin ABS caps and tray mounts.
- **Creamy:** smooth, soft and muted, with no scratch or spring noise. A lubed linear with a gentle, rounded bottom-out. Think Banana Split.
- **Marbly:** clean, round, *slightly pitched* clicks, like glass marbles tapping. A couple of narrow resonances (about 1.5–3.5 kHz) ring briefly. A premium, "expensive" sound.
- **Poppy:** a crisp tactile event on the way down and a snappy, clean return. Think Keychron Banana.

### 6.3 Anatomy of one keystroke (what to synthesise)

Acoustic side-channel research separates each keystroke into a **push peak** (finger contact, then the key hitting bottom) and a **release peak** about **100 ms later**. Source: Asonov & Agrawal 2004, "Keyboard Acoustic Emanations"; Zhuang, Zhou & Tygar 2005, "Keyboard Acoustic Emanations Revisited"; a later CCS paper by Zhu et al. confirms "about 100 milliseconds" [3P: paper texts on GitHub].

A tactile switch adds a small **bump tick** just before bottom-out.

1. **Bump tick** (tactile only): a very soft 2–5 kHz transient, about 0.5–1 ms, −18 to −24 dB relative to the impact.
2. **Bottom-out impact** (the main event):
   - A broadband attack of 0.5–2 ms, into a resonant body.
   - Thock: main mode about 250–450 Hz. Clack or marbly: about 600–1,200 Hz.
   - Secondary modes at about 1.2–1.8 kHz and 3–4 kHz.
   - Decay about 25–60 ms for thock, about 15–30 ms for clack.
3. **Low "thump"** (for thock): a 90–160 Hz sine or low-passed noise, 10–25 ms, felt more than heard.
4. **Spring ping** (the "cheap" tell): a sine around 3–6 kHz ringing 100–200 ms. **Leave it out** for a premium sound.
5. **Release / top-out:** a second transient 60–150 ms later, 6–10 dB quieter and slightly higher pitched. Crisp for tactile, soft for linear.

### 6.4 Synthesis recipe (starting points [K])
- **Layers:** noise burst → modal resonator bank (3–4 band-pass resonators, Q 8–30), plus a click (1–3 ms, high-passed at 2–4 kHz), plus an optional low sine thump.
- **"Marbly" upgrade:** add two narrow, slightly *inharmonic* resonances (e.g. 2.1 kHz and 3.4 kHz, 40–80 ms decay).
- **Variation:** round-robin 6–8 variants, with ±3% pitch, ±1.5 dB level and ±5 ms timing jitter. This avoids the machine-gun effect when ticks fire in sequence.
- **Space for "ethereal-mechanical":**
  - Keep the dry signal very close: 5–15 ms early reflections, narrow stereo.
  - Send 5–10% to a long, dark reverb: 40–80 ms pre-delay, 3–6 s decay, high-cut about 5 kHz. This gives distance without sparkle.
- **Mix:** high-pass clicks at 60–80 Hz. Tame 2–3 kHz if fatiguing. Sit UI ticks well under the VO. Sync to picture 0–20 ms after the event (R11).

### 6.5 Chrome & Marl UI sound kit (8 sounds built from 6.3–6.4)

| Sound | Recipe | Fires on |
|---|---|---|
| Line-draw | Band-passed noise "zip", rising about 1 semitone over 120–250 ms, ending on a soft tick | Line work tracing itself |
| Card snap (closure) | Tactile bump plus thock bottom-out, 40–70 ms | Loop closes or a card lands (R6) |
| Card lift | Release tick, quieter and higher | Card leaves |
| ASCII scramble | Granular micro-clicks 5–15 ms apart, 2–6 kHz, very low level | Glyph fields resolving |
| Hologram power-up | Two sines beating 0.5–2 Hz apart, 1–2 s swell, low-passed at 6 kHz, no chimes | Hologram appears |
| Chrome number lands | Thock, plus a 100–140 Hz thump, plus a struck-bar metallic tail (partials at about 1 : 2.76 : 5.40, 150–300 ms) | Hero number hits |
| Orbit air | Very soft low-passed air whose filter tracks the camera's angular velocity | Orbits |
| Vortex drop | Descending Shepard–Risset glide (3–8 s), then 150–300 ms silence, then a sine sub-drop 80→30 Hz on the downbeat (R14, R16, R17) | Big transitions |

---

## Appendix: source reliability notes
- **Solid.** Peer-reviewed sources in §3, YouTube Help, the US Copyright Office, and Higgsfield's official SDK source (api host, cloud host, auth format).
- **Good but third-party [3P].**
  - Higgsfield plan prices, models and preset list (a July 2026 research note that cites official pages, a UI-scrape allowlist, and integrator probe logs).
  - santeluca transcripts and shot logs (one GitHub repo).
  - Switch specs (community datasets).
  - Verify Higgsfield prices on the live pricing page before budgeting.
- **Knowledge-only [K].** Jungle anatomy numbers, reference-track years, synthesis parameters, Amen tempo, and distributor allow-list practice. These are standard practice but were not re-checked this session.
- **Not found.** No long-form press interview with Luca Maxim turned up. His own Shorts and the 22-minute YouTube talk are the primary first-person sources.
