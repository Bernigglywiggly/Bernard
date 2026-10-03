# Channel 1 · The Curve (AI explained)
**Format (3 Oct, the user: "i need daily uploads from 1st channel... make 5 day backlog"):** long-form films
(16:9, 11-14 min, mid-roll ads from 8 min) are the product; each is cut into 3 shorts that point back to it. The
earlier 2-3 minute films (EP04-EP14) remain the back catalogue and the daily shorts.
**Look:** line art and AI pictures turned into turquoise characters on black, crisp typed labels in gold, big numbers
formed in characters, word-by-word captions, the film's name bottom left.
**Voice:** Harrison (Higgsfield Seed Audio preset), one take per chapter. George (ElevenLabs) is not reachable from
this account; if the key is added, the engine can switch back.
**Music:** house, garage and deep house (`lab/music/beds.py`), one cue per chapter, ducked under the voice.
**Facts:** every number sourced on screen and in the description; reported and known kept apart; one labelled what-if.

## Long-form (`lab/curvelf`, ~30 Higgsfield credits a film)
| # | Title | Status | Files |
|---|---|---|---|
| 01 | The AI That Escaped · 13:19 | Made 3 Oct · [film](https://claude.ai/artifact/NC5QdLVBaBEMemcsaHLPYM) · [shorts](https://claude.ai/artifact/SXhZZiVogib4tEhsbR7tNs) | `lab/curvelf/lf01_escape/` |
| 02 | The Price of Thinking · 10:48 | Made 3 Oct · [film](https://claude.ai/artifact/JgAJPt8FQ45dJivdXQy7f9) · [shorts](https://claude.ai/artifact/4LqUZUotHs9EEvvuj1gr7J) | `lab/curvelf/lf02_price/` |
| 03 | Too Dangerous to Release (GPT-6.1 Astra, Gemini 4 Argon, Mythos) | Script, voice and pictures done 3 Oct; render next (HANDOFF.md) | `lab/curvelf/lf03_held/` |

## How a long-form film is made
1. `script.py`: 11-12 chapters of beats, each beat a spoken line and one visual (img, clip, num, words, quote, list,
   split, tl). ~1,400-1,800 words, about 150 a minute.
2. `shots.py`: the AI pictures, one bright subject on black (`../assets.py` adds the house style). Archive pictures go
   in `src/arch` with their credits.
3. Voice: Harrison, one Seed Audio take per chapter; word timings by faster-whisper small.en
   (`lab/longform/tools/words.py`), then `kit.py <film> vo` joins them and writes the chapter cards.
4. `kit.py <film> music`: one bed per chapter, cycling deep house, house and garage.
5. `kit.py <film> render`: the beats on the word timings, in the character look, four chapters at a time (~25 min),
   then the mix, the join and a 1080p delivery under 246 MiB.
6. `thumb.py <film>` (three thumbnails from the film's own frames) and `POST.md` (title, chapters, sources, settings).
7. Shorts: `python3 lab/longform/vertical.py <abs path to film>` cuts the stretches named in `shorts.py`.
8. Pages: `cd lab && python3 pack/build.py lf01 | lf01_shorts | lf02 | lf02_shorts`.

## Back catalogue (2-3 min, `lab/epNN`)
- **Ready to upload** (pages in `STUDIO.md`): EP05, EP08, EP04, EP06, EP07, Season One, EP09-EP12, Season Two.
- **Next**: EP13 and EP14 are scripted but unvoiced (they need ElevenLabs, or re-voicing with Harrison); EP03 needs
  its Blender frames.
- Code: `lab/engine` + `lab/epNN/{script,scenes,film}.py`; rebuild a film's sound with `film.py sound` then
  `film.py remux`.
