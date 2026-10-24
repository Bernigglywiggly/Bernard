# Thumbnails v2: the rules (11 Oct 2026)

Generator: `lab/tools/thumbs_v2.py` (`~/youtube/.venv/bin/python lab/tools/thumbs_v2.py [film ...]`, `--feed` for the
sheet). Feed test: `lab/tools/thumbs_v2_feed.jpg` (every variant at 168x94 on white and dark YouTube UI, beside the
old thumbnail and synthetic "typical" neighbours). Output per film: `out/thumbs_v2_{a,b,c}.jpg`, 1280x720, < 0.4 MB.

## The system (one page)
1. **One focal subject at 60-70% of the frame**: a picture from the film (AI still graded to the channel ramp with a
   rim light and outer glow, an archive object inked and tilted, the film's own map plate), **or** a giant number.
   Never both fighting: the number sits on black, the picture on the other side.
2. **2-5 big words**, keylined in black so they read on any picture. Type is a brand mark: The Curve and How They
   Profit use Archivo Black (900, cut from the variable font with fontTools); Money Crimes uses Anton, tall and
   condensed like a 1920s headline. One idea per thumbnail. Small mono lines vanish at 168 px: use them only for
   optional dates/sources, never for anything the claim depends on (LF03 B carries "IN A TEST" on a tape for that reason).
3. **Fluoro on black, one pair per channel**. The Curve: cyan `#3DFFF2` + magenta `#FF2BD6`, acid yellow `#E6FF2E`
   for the number. Money Crimes: red `#FF2A2A` + white (orange for the drawn device). How They Profit: acid green
   `#C6FF1A` + yellow `#FFE81A`, red only for the device. Highlighter swipes carry words; neon is for events.
4. **One honest curiosity device**: an arrow or ring on the real detail, a before→after split, a crossed-out number
   or belief, a red X, a big counter. It must point at something the film shows.
5. **Every word is a claim the film shows before or at the beat named in the recipe comment** (CRAFT §9 rules 9-11).
   If the picture and the words disagree, change the words (see Ponzi below).
6. **No faces of real people, no fake faces, no logos.** Visa is a drawn generic card; "Visa" appears only in our type
   when needed. Silhouettes and robot hands are fine.
7. **Brand mark top-left** (bottom-left when the subject needs the top): The Curve's cyan curve + dot, the MC and HTP
   ring initials. Bottom-right stays empty: YouTube puts the duration badge there.
8. **Test at 168 px** before anything else. If a word needs squinting, it goes or grows.

Feed finding: on the white UI every black thumbnail jumps out; on the dark UI the black ground merges with the page,
so the glowing number/word has to do all the work (it does in A variants; Hormuz B's neon outline is the weakest).

## Recommended lead variant (A/B/C go into Test & Compare together)
| Film | Lead | Words | Why |
|---|---|---|---|
| Hormuz | **A** | 125 ~~struck~~ → **8 SHIPS** | Biggest, simplest contrast in the set; the bend of the oil route is the picture; pairs with title A. B ("CLOSED / TO SHIPS / OIL?") pairs with title B, C ("OPEN TO OIL") with title C, as POST.md planned. |
| LF01 The AI That Escaped | **A** | **700 AI AGENTS ATTACKED** | Giant counter plus the robot hand through bars; adds what the title doesn't say. C ("NOT A PERSON" + X) is the strongest curiosity test. |
| LF02 The Price of Thinking | **B** | ~~$60~~ → **6¢**, 1,000× CHEAPER | Before→after price reads instantly at 168 px. A (500 NOVELS + the burger) needs the mono line to land. |
| LF03 Too Dangerous to Release | **A** | **CANCELLED** stamp + GPT-6.1 | One word, red stamp over the open vault; reads at any size. B (29% PLANTED BAD CODE, marked "simulated") is the hard-number test. |
| Visa | **A** | **24¢ OF EVERY $100** + ring on the card's sliver | The rebuilt "who gets this?" idea, now with the answer as the hook; pairs with "Visa Isn't a Credit Card Company". B (LENDS $0 / KEEPS $20B) suits title 2. |
| Ponzi | **B** | **WHERE'S THE MONEY?** + the 1920 "EXTRA!" front page | The film's own question over a real 1920 front page; no face (the old thumbnail used Ponzi's photo). A (+50% ON PAPER, ring on the note's "$300") is the test. |

## Independent review (11 Oct, a subagent that did not design them)
Every v2 beat the old thumbnail at phone size; it picked the same six leads. Fixed after it: the LF01 B arrow now
leaves the box; LF02 A burger warmed and "= 1 BIG MAC" added; LF02 B tape moved off the ¢; LF03 B says "IN A TEST";
LF03 C ring tightened; Visa A ¢ spacing, Visa B words clear of the logo; Ponzi A ring on "THREE HUNDRED DOLLARS";
unreadable mono captions dropped; Money Crimes given its own face. Not done: printing "6¢" on LF02 B's tag; the
open vault in LF03 A (it is the film's own shot of the held model).

## Things to know
- **Ponzi "double in 90 days" was dropped**: the film says it, but the note the film shows promises $300 for $200 at
  ninety days (50%). Putting "DOUBLE IN 90 DAYS" next to that note contradicts itself. Worth a look in the film too.
- Ponzi C's struck "COUPONS" is the least legible line in the set at 168 px; keep C last.
- Hormuz map: the plate is rendered from `lab/maps/style/style_frames.py` without labels and cached in
  `lab/tools/cache_thumbs_v2/hormuz_plate.png`; delete the cache to re-render. Oil routes are schematic, as in the film.
- skia-python ignores the `wght` axis on variable-font clones; `font()` cuts static instances with fontTools instead.
