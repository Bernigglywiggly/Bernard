# Short 8 claims check (before upload)

Account C, Tue 27 Oct 2026, 04:45 UK. **This is the CRAFT §5 claims pass, not the render critic:** C works in the cloud and
can't see `SHORT8_*.mp4`, so this checks every spoken line (`lab/curve_v2/shorts/short8.py`, captions `voS8Captions.ts`),
every on-screen string in `lab/motion/src/curve_v2/CurveV2Short8.tsx` and the manifest entry (`channel/uploads_curve.json`
index 4) against `lab/research/IPHONE_DUO_FACTS.md`, plus a fresh search for anything new since 26 Oct. The film-critic
skill (motion, loudness, readability on the actual render) still runs on the Mac before upload.

**Verdict: ONE MORE PASS (text only, ~1 re-render).** One must-fix (two numbers on screen contradict each other), four
quick should-fixes. Everything spoken checks out; nothing needs re-voicing.

## Must fix

| # | Where | Problem | Fix |
|---|---|---|---|
| 1 | Layers scene, `CurveV2Short8.tsx` ~line 228 (`"OUTER LAYER 10.7%"`, `"BOOK PAGES: 1.1%"`) | These come from facts row 93 at a **1.4 mm** fold. The scene before shows the same 30 µm glass at "SAME ~1.9 mm FOLD" = **0.8%**. So one 30 µm layer reads 0.8% and then 1.1% seconds apart, with nothing saying the fold changed. Comment bait ("you said 0.8%") | At ~1.9 mm (OUR MATHS, facts row 93b): glued 0.3 / 3.8 = **7.9%**, sliding 0.03 / 3.8 = **0.8%**. Strings: `"OUTER LAYER 7.9%"`, `"BOOK PAGES: 0.8%"`; tag `"ILLUSTRATIVE · 10 LAYERS OF 30 µm, ~1.9 mm FOLD"` |

## Should fix (all text; do them in the same re-render)

| # | Where | Problem | Fix |
|---|---|---|---|
| 2 | Apple card, ~line 258 | The quote stops mid-phrase: "...ON A SMALL NUMBER". Apple's full sentence (CNBC, Reuters, MacTech, iClarified, 26 Oct): "aware of an issue impacting the inner display on a small number of iPhone Duo units" | `“AN ISSUE IMPACTING THE INNER DISPLAY ON A SMALL NUMBER OF IPHONE DUO UNITS”` at ~72 px (84 px would push it into the APPLECARE stamp at top 690). Render a still of that frame before the full render (CRAFT 26 Oct lesson 1) |
| 3 | Frame 0 and loop credit, ~line 319 | JRE's green line came from his **bend test**, not normal folding, and we don't know that it runs along the fold (facts rows 56-57, do-not-claim). Under "WHY DO IPHONE DUOS CRACK?" and after "it's where the reported cracks are", the cut implies it's a fold crack | Credit text `"JERRYRIGEVERYTHING · BEND TEST"` (same spot, same size) |
| 4 | Manifest description, first sentence | "Apple's iPhone Duo is getting cracked inner screens" states a defect as fact; Apple's words are an issue on "a small number" of units | "Some iPhone Duo owners are reporting cracked inner screens, and JerryRigEverything's durability test (24 Oct 2026) is the clip everyone's sharing." Optional extra line after Apple's statement: "iFixit's teardown found two possible causes in the hinge, neither confirmed." (row 34e, corrected 04:50: it's a centre bar or a guide rail, not the display cable) |
| 5 | Manifest `"file"` | Points at `SHORT8_v1.mp4`; commit 43db7eb says "v2 rendered" | Point it at the final mastered file before uploading |

## Nits (only if free)
- The stack draws 7 strips under a "10 LAYERS" label. Either draw 10 or say "ILLUSTRATIVE STACK".
- "over thirteen percent" (spoken) and "13%+": 0.5 / 3.8 = 13.2% at 1.9 mm; at HTX's exact 3.85 mm gap it's 12.99%, and "or tighter" (row 94) only pushes it up. Fine as is; don't re-voice.

## Checked and fine
| Line or element | Facts rows | Status |
|---|---|---|
| d1 "Every time you fold an iPhone Duo, its screen glass stretches almost as far as glass can before it cracks." + readout 0.8% vs "GLASS CRACKS ≈1%" + tag "OUR MATHS · 30 µm GLASS, ~1.9 mm FOLD" | 70, 71, 76, 94 | OK: inference, labelled on screen and in the description (Apple publishes neither number) |
| d2 rule + "STRETCH = t ÷ 2r", "2× THICKER → 2× THE STRETCH", "2× TIGHTER → 2× THE STRETCH" | 70, 72, 74 | OK |
| d3 "Ordinary phone glass bent like this would stretch over thirteen percent and shatter... about thirty microns thick." + "0.5 mm / 13%+ / SHATTERS", "30 µm / 0.8% / BENDS", "OUR MATHS · SAME ~1.9 mm FOLD" | 76, 91, 94 | OK |
| d4 "...the glass is toughened and the layers slide like book pages." + "APPLE: \"MORE THAN 10 ULTRATHIN LAYERS\"", "APPLE: LAYERS \"GLIDE\" PAST EACH OTHER" | 20, 22, 23, 79 | OK (Apple: "high-strength glass"; add row 22 to the script's facts field) |
| d5 "Apple says a small number of inner screens have an issue, and it's replacing them." + "APPLECARE REPLACEMENT", "NO CAUSE GIVEN" | 34 | OK; Reuters: "Apple says it will replace iPhone Duo units showing screen problems". Still no cause from Apple (27 Oct 04:40) |
| d6 "...the fold is where this screen works hardest, and it's where the reported cracks are." + "REPORTED CRACKS: ALONG THE HINGE" | 34b, 34c | OK: "reported" hedge kept; Reuters and Inven also place the lines along the hinge |
| Title "iPhone Duo Crack: Why It Happens at the Fold" (44 chars) | 34b, 70-75 | OK: explains where, not what caused it |
| Description: our maths paragraph, footage credits, AI-voice line, no `<` `>` | 70-94 | OK |
