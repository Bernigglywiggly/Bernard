FIX THEN UPLOAD

# sh_steve · CRITIC v1 (independent review, 10 Oct 2026)

Render: `shorts/short_steve.mp4`, 1080x1920, 30 fps, 34.8 s. Evidence in `out/critic/`: `frame0.png`,
`sheet_1p5.jpg` (every 1.5 s), `phone.jpg` (360 px wide), `seam.jpg` (last 1 s over first 1 s), `gaps.jpg`,
`loudness.txt`, `motion.txt`, `transcript.txt`.

## Scorecard

| Check | Result | Verdict |
|---|---|---|
| Length | 34.8 s (CRAFT 9.3: 20-35 s) | PASS |
| Loudness | -14.2 LUFS integrated, true peak -2.3 dBFS, LRA 1.8 | PASS |
| Motion | 0% frozen, 3% near-still, no still stretch of 2 s or more | PASS |
| Transcript vs script | All 8 lines word for word (Whisper writes "GTA 5" for the spoken "GTA Five") | PASS |
| Claims vs FACTS.md | All 8 lines and every on-screen label trace to HIGH-confidence rows (S1, S3). The one-source numbers (160 probes, 400 blocks, 1,500 objects, 125 GB) are correctly left out | PASS |
| IP safety | No game footage, logos, HUD, map, Steve or GTA characters. The teal cube robot has an antenna, a visor slit and no face, hair or skin, so it reads as a robot, not Steve. The city is ASCII type. Brand names appear only as words | PASS |
| Safe zones | Brand line starts at y=231 (12.0%, right on the top line). Captions sit at y 1301-1490 (68-78%), clear of the bottom 20% (y 1536). Nothing in the right rail | PASS (tight) |
| Hook / frame 0 | Good payoff picture, but 14 words on screen and the surprise lands at 4-5 s | FIX |
| Loop seam | Last ~0.4 s fades to black and the music falls to -28.6 dB, then it jumps to a bright frame 0 with a label the end frame lacks | FIX |
| Captions | Full 3-line sentences with a karaoke highlight; CRAFT 9.5 asks for 2-4 word chunks | FIX |
| Smallest text | Source line and "TO PLAY IT" are 16-17 px tall at 1080 (about 5 px on a phone), so nobody can read them | FIX |
| Pacing | The picture changes about every 4.3 s (8 beats); CRAFT 9.6 asks for every 1.5-2.5 s. Black dips at about 9.5 s and 21.3 s | MINOR |

## Problems and exact fixes (in order of impact)

1. **The hook buries the surprise and never names the myth (CRAFT 9.1).** Line 1 runs 0-5.1 s, and "two games
   running at once" only arrives at about 4 s. The misconception the audience arrives with ("AI reverse-engineered
   GTA") is never said, so the myth-bust is implicit. **Fix:** re-voice line 1 so it is 3 s or shorter and says the
   search term: *"That Steve-in-GTA clip isn't AI hacking the game. It's two games running at once."* (Narration
   may name Steve; FACTS IP note allows names in words.) Keep "you" once by changing line 7 to "To play it, you
   need both games...".
2. **Frame 0 carries 14 words (CRAFT 9.1 says 2-6).** The headline "Minecraft's hero in GTA V is two games at once"
   (10 words) and the plate "TWO GAMES · ONE SCREEN" (4) compete. **Fix:** headline `TWO GAMES, ONE SCREEN` and drop the
   h01 plate label. Or keep the plate and set the headline to `MINECRAFT + GTA V`. The headline stays up for the
   whole Short, so it does not need to repeat the narration.
3. **The loop seam breaks.** The picture and captions fade to near black over the last ~0.4 s and the music tails
   out (last 0.6 s at -28.6 dB vs -16.8 dB at the start). The last frame also lacks the plate label that frame 0
   has. **Fix:** no fade-out on the final beat. Hold h01 at full brightness, with the same label and camera position
   as frame 0, until the last frame. Keep the music bed at level to the end, or crossfade the last 0.3 s into the
   bed's first 0.3 s. The words already loop ("...two other games running at once." → "You've seen...").
4. **The captions are sentence blocks, not chunks (CRAFT 9.5).** About 15 words sit on screen in 3 lines.
   **Fix:** 2-4 word chunks, one line, at the same y (about 1330), with the font at least 64 px. That also frees the
   lower third.
5. **Unreadable small text.** `CLAUDE CODE + ONE PERSON · FIELD NOTE, 30 SEP 2026` (16 px) and `TO PLAY IT`
   (17 px) are about 5 px on a phone. **Fix:** set both to 36 px or more, or cut them. If space is short, shorten the
   source line to `CLAUDE CODE + 1 PERSON`. "THE CURVE" (19 px) is a brand mark; 28 px would help.
6. **Dips through black between beats** (about 9.3-9.7 s and 21.2-21.6 s show near-empty frames). **Fix:** use a
   0.25 s crossfade or a push instead of out-then-in. Add one state change inside the long beats so something new
   lands every ~2 s: probe dots dropping in h02 (9.7-12.5 s), and the lamp post sliding in front in h04 (17.9-21.3 s).
7. (Minor) The `TO PLAY IT` list builds one item at a time, which leaves a mostly empty frame at about 25.5 s.
   Bring all 4 items in within 1.5 s, timed to the words.

There is no accuracy fix and no IP fix. Items 1 and 3 matter most for retention, and 1 needs one re-voiced line.

## Title and headline vs CRAFT 9.9-9.10
- Script title "IT'S TWO GAMES, NOT ONE": the claim is shown on screen by 0:05, so it is not clickbait. But it has
  no concrete subject and gives the outcome away, which fails 9.10 and is weak for search.
- **Suggested title (36 chars):** `How Minecraft's Steve Got Into GTA 5`. The subject is concrete, the outcome is
  withheld, and the promise is paid on screen by 0:05 (9.9). Alt (24 chars): `How Steve Got Into GTA 5`.

## Description (paste)

```
That viral clip of Minecraft's Steve walking around GTA 5 isn't AI hacking or dreaming up a game. It's two unmodified games running side by side on one PC, with a bridge passing the camera, the ground and the picture between them every frame. An AI coding agent (Claude Code) wrote that bridge in about two days, with one person directing it. To try it, you need both games, a Windows PC, GTA V story mode only, and a build from source.

Sources:
universal-modder (MIT), GitHub README: https://github.com/rehan-remade/universal-modder
Field note "minecraft-passthrough", 30 Sep 2026: https://github.com/rehan-remade/universal-modder/blob/main/knowledge/games/gta-v/minecraft-passthrough.md
VGTimes, how the AI game mash-ups work: https://vgtimes.com/articles/169886-how-ai-game-mashups-work.html
GamingBible, 7 Oct 2026: https://www.gamingbible.com/news/gta-5-minecraft-mod-does-impossible-124923-20261007

Disclosure: the mod was built with Claude Code, and The Curve is also made with Claude.
Not affiliated with or endorsed by Mojang, Microsoft, Rockstar Games or Take-Two. Minecraft and Grand Theft Auto are trademarks of their owners. All visuals are original diagrams drawn for this Short; no game footage is shown.
```

## Hashtags
#Minecraft #GTA5 #AI #ClaudeCode #Shorts
