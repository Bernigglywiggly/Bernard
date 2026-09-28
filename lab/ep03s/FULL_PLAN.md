# EP03 in full: the build plan (28 Sep)

The cold open is done (`ep03s.py` line art → `ascii_open.py` characters, ASCII v5.1). The rest of script v4
(`script.py`, 34 lines, about 2:55) needs its visuals, in the same system: line art keyed by line id, turned into
characters, one focal point, labels crisp on top, Blender realism only where an object carries the story, and every
analogy drawn as the thing itself.

**Order of work, once `ELEVENLABS_API_KEY` is set (a new session picks it up):**
1. `cd lab && python3 tools/eleven_tts.py ep03s --speed 1.2`, then `cd ep03s && python3 voice_build.py` (George).
2. Build the beats below in `ep03s.py` (a `frame()` section per floor), test stills with `ascii_open.py still`.
3. Score: `beds.mainframe` re-cut to the floors (below), then render, mix, publish, send.

| Floor | Line ids | The picture (characters) |
|---|---|---|
| 1 MECHANISM | census, verdict, split, pan | census ledger rows scrolling (1850, 1852); two bars, MINERS small or zero vs EVERYONE ELSE large; the prize orb from the cold open splitting into slivers across a crowd of dots; every dot gets a pan, the supplier's counter ticks |
| 2 NOW | now, capex, rome, nvidia, nvidia_mac, margin, openai, openai_mac, fair | "1848" morphs to "2026"; $725 BILLION over data-centre rows; a timeline from AD 43 to 2026 with a million-a-day counter running along it; the cold open's shovel morphs into a GPU; Big Macs pour like the gold dust with "≈2,000 / SECOND"; four coins, one goes to MAKING THE CHIPS; two flows, $5.7B in and $3.7B out; "$1.65 OUT FOR EVERY $1 IN"; a few digger dots strike gold |
| 3 IDEA | before, acts, third, miles, layers | 272 Acts stacking with "5 A WEEK"; a railway map of Britain, a third of its lines fading; the 6,000 miles stretched London to Tokyo on a globe arc; the speculation fades, the rails stay |
| 4 IMAGINE | imagine, whatif, cheap, scarce, trust, question | dotted IF markers and a shifted sea; a tap running characters ("like tap water"); a bolt, a chip, land and water; many answers, one lit; the question |
| 5 SURFACE | rush, chain | the gold stream again; it becomes a chain of links; sources |

**Score (Mainframe, one bar grid for the film):** cold open as now (intro, a on "mind", b with the Big Mac, break
on "never"); MECHANISM a; NOW b (brass for the money); "It has happened before." a boom into a break; IDEA a;
IMAGINE break-like (strings and a filtered ostinato only); SURFACE b, then out. Hard dips before each `cut` line.
