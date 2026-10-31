---
name: film-critic
description: Independent quality gate for this studio's films and Shorts (The Curve, Money Crimes, How They Profit) before upload, or whenever a render needs reviewing. Measures motion, loudness and readability with ffmpeg, then has a fresh critic subagent that did not build the film judge the render against CRAFT.md and the facts file, and verifies fixes in a second round.
---

# Film critic

The builder never grades its own film. This skill measures the render, then hands it to a **fresh** critic. The
rules it judges against are in `CRAFT.md` at the repo root.

## 0. Before voicing: lint the script

`python3 .claude/skills/film-critic/script_lint.py <script.py>` flags the narration habits CRAFT.md §2 bans ("Not X."
openers, colon reveals, staccato runs, three numbers in a sentence, stock phrases). Fix every flag or justify it in
one line; voicing credits are spent after this, not before.

## 1. Measure (2-3 minutes; save everything under `<film dir>/out/critic/`)

```bash
K=.claude/skills/business-motion-film/scripts    # vendored kit (MIT): contact-sheet, loudness
F=<film>.mp4; O=<film dir>/out/critic; mkdir -p $O
python3 .claude/skills/film-critic/motion_report.py $F > $O/motion.txt   # frozen and near-still stretches
bash $K/loudness.sh $F > $O/loudness.txt                                  # target -14 LUFS, true peak <= -1 dBFS
bash $K/contact-sheet.sh $F $O/sheet.jpg 2 6 5            # films: every 2 s (repeat with start offsets for long films)
bash $K/contact-sheet.sh $F $O/short.jpg 0.5 6 5          # Shorts: every 0.5 s
ffmpeg -loglevel error -y -i $F -vf "fps=1,scale=360:-1,tile=6x4" -frames:v 1 $O/phone.jpg   # readability at phone width
ffmpeg -loglevel error -y -i $F -frames:v 1 $O/frame0.png                                    # the hook and fallback thumbnail
```
For each scene change (from the shot list or the `motion.txt` timestamps), make a 12-frame strip at full rate:
`ffmpeg -ss <t-0.2> -i $F -vf "scale=320:-1,tile=12x1" -frames:v 1 $O/strip_<t>.jpg`. These catch text collisions,
pops and half-entered words that sheets at 2 s miss.

## 2. Critic round (Agent tool, a NEW subagent each round)

Send only: the render path, the critic folder, the brief (channel, audience, what the film argues), `CRAFT.md`, the
facts file or POST.md with sources, and the previous round's report if there is one. **Never tell the critic what
you fixed or what you think of the film.** Prompt:

```
You are an independent, harsh critic for a YouTube documentary channel. You did NOT make this film; judge only the
rendered pixels and measured audio. Film: <path> (<duration>, <WxH>). Channel: <name>, audience: <who>. Read CRAFT.md
(the house rules) and <facts file>. Measurements are in <critic dir> (motion.txt, loudness.txt, sheets, strips,
frame0.png, phone.jpg); pull more frames with ffmpeg wherever you need them.

Score 1-10, each with timestamps for its problems:
1. Hook (first 3 s of a Short, first 8 s of a film) and frame 0 as a thumbnail.
2. Readability at 360 px wide: smallest text, contrast, captions inside safe areas.
3. Motion: frozen > 2 s, near-still stretches, something new every 2-4 s, constant easing, dead beats.
4. Variety and composition: subject fills 60-85%, repeated layouts, empty frames, banned defaults from CRAFT.md.
5. Accuracy: every on-screen number, name and date against the facts file. List any mismatch.
6. Sound: loudness vs target, music under voice, effects audible but not harsh, cuts landing on beats.
7. Authorship: does it look templated or interchangeable with the channel's other films (YouTube's "inauthentic
   content" risk)? What would make it unmistakably this channel's?

Then: the 5 highest-impact fixes, concrete and implementable in our engine. End with SHIP or ONE MORE PASS.
Write the report (under 700 words) to <critic dir>/round<N>.md.
```

## 3. Fix and verify
- Fix the highest-impact items first. Re-render only the affected scenes where the engine allows it.
- Next round: a **new** critic gets the new render plus the previous report, and marks every item FIXED / PARTLY /
  STILL PRESENT, then hunts for anything new that broke. Stop at SHIP, or when gains are cosmetic (usually 2-3 rounds).
- Keep `<critic dir>/ledger.md`: round, findings, what changed, measured before/after (motion %, LUFS).

## 4. Learn
Add one dated line to "Learned on our films" in `CRAFT.md` for anything the critic caught that a rule would have
prevented. Report to the user in two lines: the verdict, and what a human should still watch or listen to.
