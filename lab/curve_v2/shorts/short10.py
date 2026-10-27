"""Curve Short 10 (Sat 31 Oct fallback, needs nobody's permission): "How SpaceX Really Makes Money".

DRAFT by account C (facts desk), Tue 27 Oct 13:01 UK: script only, not voiced, no picture yet. The Shorts lane (A, or B if
A is away) owns the build; use it if Airport Action doesn't say yes to the crosswind Short (CROSSWIND_737_FACTS.md) and
the 17:00 radar doesn't find something hotter. Every number was read in SpaceX's own SEC filings on 27 Oct (facts §0):
the Q3 2026 10-Q and earnings release. The thumbnail carries the twist ("NOT ROCKETS"); the title keeps the search phrase.

Frame 0: SpaceX's own booster-catch shot (credited, short) with three bars rising over it: AI 7.56, STARLINK 5.25,
ROCKETS 1.77 ($B, Q3 2026). Our bars and margin diagram carry most of the runtime (borrowed footage under half, CRAFT
18 Oct). Never name a compute customer (the filing doesn't: row 0j), never call the $40B GPU deal closed (row 0k), never say
"SpaceX is profitable" without "last quarter" (§9). Verdict: rockets make the headlines, Starlink makes the profit, AI makes
the bets (its own $16.4B capex in Q3 vs $7.56B revenue, on screen). Loop: the last bar drop lands on frame 0's catch. Facts: lab/research/SPACEX_MONEY_FACTS.md (rows).
"""
TITLE = "How SpaceX Really Makes Money"
LINES = [
    dict(id="x1", facts="0c, 67 (OUR MATHS: 7,560 vs 5,248 + 1,767 = 7,015, Q3 2026 revenue)",
         text="SpaceX now makes more money from AI than from its rockets and Starlink put together.",
         cap="SpaceX now makes more money / from AI / than from its rockets / and Starlink put together.",
         shot="frame 0 = SpaceX's booster catch (credited 'SPACEX'), three bars rise: AI 7.56 > STARLINK 5.25 + ROCKETS 1.77, "
              "'$B · Q3 2026 · SEC FILING'"),
    dict(id="x2", facts="0c, 0g, 66 (7,560 vs 813: about 9x, on screen only)",
         text="Its AI business alone took seven and a half billion dollars last quarter.",
         cap="Its AI business alone took / seven and a half billion dollars / last quarter.",
         shot="the AI bar grows from $0.81B (Q3 2025) to $7.56B (Q3 2026); tag 'OUR MATHS · 9× IN A YEAR' (not voiced)"),
    dict(id="x3", facts="0c, 0d, 60 (1,767 / 14,575 = 12%; Space operating result -7)",
         text="Rockets, the part you see on the news, bring in about one dollar in eight, and they lost money.",
         cap="Rockets, / the part you see on the news, / bring in about / one dollar in eight, / and they lost money.",
         shot="a dollar split into eight coins, one lights up ROCKETS; stamp 'LOST $7M' on a Falcon landing still"),
    dict(id="x4", facts="0j (Customer B = 34.5% of Q3 revenue, SI segment, not named)",
         text="And one customer SpaceX doesn't name paid about a third of all its revenue.",
         cap="And one customer / SpaceX doesn't name / paid about a third / of all its revenue.",
         shot="the 10-Q line typeset: 'CUSTOMER B · 34.5% OF REVENUE', a blank name plate with a question mark; "
              "tag 'SEC 10-Q · NOT NAMED'"),
    dict(id="x5", facts="0d, 63 (2,367 / 5,248 = 45%)",
         text="The profit still comes from Starlink, which earns about forty-five cents of operating profit on every dollar.",
         cap="The profit still comes / from Starlink, / which earns about forty-five cents / of operating profit / "
             "on every dollar.",
         shot="a Starlink dish; a dollar coin splits 45/55, the 45 glows; tag 'OUR MATHS · Q3 2026'"),
    dict(id="x6", facts="verdict; 0h (SI capex 16,444 of 19,593 total; on screen only)",
         text="So rockets make the headlines, Starlink makes the profit, and AI makes the bets.",
         cap="So rockets make the headlines, / Starlink makes the profit, / and AI makes the bets.",
         shot="the three bars become HEADLINES / PROFIT / BETS; under BETS, the AI arm's Q3 capex bar $16.4B towers over its "
              "$7.56B revenue ('SEC · Q3 2026'); hard cut to frame 0's catch (loop)"),
]
