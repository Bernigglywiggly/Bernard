# FACTCHECK: Maps & Power 01, "Hormuz Is Closed. The Oil Isn't."

Independent check, Fri 9 Oct 2026, 20:50-22:00 BST. The checker did not write the script and used FACTS.md only as a
list of URLs. Every figure was re-read at source.

**Verdict: VOICE AFTER LISTED FIXES.** The fixes are already applied to `script.py` (list in section 5). Lint is clean
(0 flagged), the module imports, and there are still 9 chapters and 77 beats. Every headline number checks out:
8 ships, ~125 a day, 20 mb/d, 84%, 38%, the 400 mb release, at least 10 mb/d cut, $71.32 to $138.21, the nine attacks,
11.13m and 9.09m bbl, 18.3 mb/d, ~40%, 25-30% freight, $200m vs $130m, $125.44, -507 mb, -2.5 mb/d and $3.124 to $4.354.
The IEA quote is verbatim. What had to change:

- **The lanes were drawn on the wrong side.** The narration says the lanes are in Omani waters, but the old drawing put
  the inbound lane, and the eastern ends of both lanes, closer to Iran's coast than to Oman's. They are now redrawn.
- **A wrong producer order.** Iran ships more crude through the strait than Kuwait or Qatar.
- **One unsupported number.** No source backs "nearly two thousand ships".
- **"Settled"** on the $99.57 futures price is unsupported. The source gives an intraday trade, not a settlement.
- **A misleading mechanism.** The futures-to-spot gap was presented as "freight, insurance and scarcity". Dated Brent is
  priced FOB in the North Sea, so Gulf freight and insurance are not part of it. The gap is prompt scarcity.
- **Verdict framing.** It said "did not stop the oil" without saying that flows were cut hard for months.
- **Dates and labels.** The July strike happened on the night of 6 Jul. The IEA verdict came ten days after the
  closure, not "a few days". The 13-tanker figure is "at least" 13, and the 10 mb/d cut is "at least" 10 mb/d.
- **Map geometry.** One attack pin was on land, one pin sat on the coast, and two routes crossed land (the Europe route
  over Oman and the Iran-approved route over Larak).

How sources were read: the EIA, IEA, CSIS, Al Jazeera, Middle East Eye, Fortune and Windward pages were downloaded with
curl and read as raw text. The EIA figure data (fig1.xlsx, fig3.xlsx) was parsed directly. FRED DCOILBRENTEU and
GASREGW were downloaded as CSV and recomputed. Map points and lanes were tested against Natural Earth 10m land
(`lab/curvelf/data/ne_10m_land.geojson`), including a nearest-coast test for the Iran/Oman side. Web search was used
only where no primary page was available: the MoU date, the 13 Apr blockade, the IMO seafarer count, IRGC VHF warnings
and IRGC seizures. Those rows are marked.

**Counts (76 rows, by main verdict): CORRECT 57 (4 of them had a caption or card fix, and open.1 had its export
clause fixed as misleading) · WRONG 8 (all fixed: 3 map-geometry, 2 dates, 1 order, 1 timing word, 1 label) ·
MISLEADING 9 (8 fixed, 1 left as note N1) · UNSUPPORTED 2 (both fixed: "nearly two thousand ships", "settled") ·
STALE-RISK flags 9 (dated lines to re-pull on upload day, section 3).** The quote is verbatim (1 of 1). Opinion lines are marked as the narrator's own
("My answer", "If I am reading this correctly", "I would treat that with care", "I read it as"). The only forecast is
the IEA demand figure, and it is labelled FORECAST.

## 1. Claim table

Beat ids are chapter.beat (1-based, as in the current script).

### Open and the gap

| Beat | Script says | Source says (URL, date) | Verdict | Replacement wording |
|---|---|---|---|---|
| open.1 | 8 ships crossed on 8 Oct; Middle East "is exporting roughly as much crude as before the war" | Windward Daily Intelligence, data as of 8 Oct (insights.windward.ai, 9 Oct): "5 inbound (all AIS) and 3 outbound on 8 Oct, down from 18 on 7 Oct". Export claim = Kpler 7-day average on 30 Sep, *provisional* (Al Jazeera 6 Oct). Kpler also: Gulf ex-Iran only ">81 percent of pre-war levels in September" | CORRECT (ships) · MISLEADING (exports stated as a present-tense fact from one provisional 7-day peak) · fixed | "...and yet, by one tracker's count, Middle East crude exports are back to about where they were before the war." |
| open.1 card | 5 IN · 3 OUT · WINDWARD | as above | CORRECT · STALE-RISK | re-pull Windward on upload day |
| open.2 | ~125 large ships a day before 28 Feb | AJ/AFP 8 Oct: "typically handled about 125 large commercial vessels a day" (AJ 7 Jul gives 120-140) | CORRECT | none |
| open.4 | Cross by speedboat in under an hour | 21 nmi at >21 knots < 1 h (arithmetic) | CORRECT | none |
| gap.1 | Gulf's only way out is between Iran and the tip of Oman | EIA TIE 65504 (16 Jun 2025): strait "located between Oman and Iran, connects the Persian Gulf with the Gulf of Oman" | CORRECT | none |
| gap.1 map | Bandar Abbas 27.2N 56.3E, Musandam 25.9N 56.2E, Khasab 26.2N 56.3E | Natural Earth test: Bandar Abbas on the shore (0.4 km); Khasab and Musandam on land | CORRECT | none |
| gap.2-3 | Narrowest ~21 nmi ≈ 39 km, Larak to Great Quoin | EIA TIE 4430 (4 Jan 2012): "At its narrowest point, the Strait is 21 miles wide" (unit not given). Measured here: Larak's south shore (~26.82N 56.37E) to Great Quoin (26.494N 56.529E) ≈ 38.5 km = 20.8 nmi | CORRECT (only in nautical miles; the script says nautical) | none. The caption credits EIA for a unit EIA does not state. Acceptable because Wikipedia is also credited |
| gap.4 | Two lanes ~2 mi wide, 2 mi buffer, inbound north / outbound south | EIA TIE 4430: "the width of the shipping lane in either direction is only two miles, separated by a two-mile buffer zone" | CORRECT | none |
| gap.4-5, open.1, verdict.1, verdict.10 map | Lanes drawn as Z_INBOUND / Z_OUTBOUND | Nearest-coast test on the old drawing: 8 of 10 inbound points and 3 of 10 outbound points were nearer Iran (including the 56.95E ends and the 26.68-26.71N mid-section) | WRONG (the drawing contradicted "Omani waters") · fixed | Lanes redrawn as 2 nmi lanes with a 2 nmi median that follow Musandam and bend round the Quoins. All 24 points are now nearer Oman. Still schematic and still captioned so. R_GULF_OUT moved onto the outbound lane |
| gap.5 | Lanes in Omani waters; Qeshm, Hormuz, Larak are Iranian | AJ 7 Jul (Milani: Iran's "sovereignty over half of the strait"); the traffic separation scheme lies in Oman's territorial sea (FACTS F03, Maritime Executive) | CORRECT | none |
| gap.6 | Tunbs and Abu Musa taken by Iran in 1971, claimed by UAE | Long-standing (Nov-Dec 1971) | CORRECT | none |

### What flows (EIA TIE 65504 + fig1/fig3 data, Vortexa)

| Beat | Script says | Source says | Verdict | Replacement wording |
|---|---|---|---|---|
| flows.1 | ~20 mb/d, 2024 | fig1: 20.26 mb/d in 2024 | CORRECT | none |
| flows.2 | ~20% of world consumption | "the equivalent of about 20% of global petroleum liquids consumption" | CORRECT | none |
| flows.3 | >¼ seaborne oil; ~⅕ LNG, mostly Qatar | "more than one-quarter of total global seaborne oil trade"; "around one-fifth of global liquefied natural gas trade ... primarily from Qatar" | CORRECT | none |
| flows.4 | Saudi first, "with Iraq, the Emirates, Kuwait, Qatar and Iran behind it" | fig3, 2024 crude by origin (mb/d): Saudi 5.48, Iraq 3.22, UAE 1.89, **Iran 1.40, Kuwait 1.33, Qatar 0.65** | WRONG (order) · fixed | "...with Iraq, the Emirates, Iran, Kuwait and Qatar behind it." |
| flows.4 card | 38% of Hormuz crude | "38% of total Hormuz crude flows (5.5 million b/d)"; 5.48/14.32 = 38.3% | CORRECT | none |
| flows.5 map | China 4.8, India 1.9, S. Korea 1.7, Japan 1.5, Europe 0.7 mb/d | fig3 destinations 2024: 4.78 / 1.89 / 1.73 / 1.52 / 0.72 | CORRECT | none |
| flows.6 | 84% to Asia | "84% of the crude oil and condensate ... went to Asian markets in 2024" | CORRECT | none |
| flows.7 | China about a third, "India, South Korea and Japan close behind" | 4.78/14.32 = 33%; the next three are 1.5-1.9 mb/d, less than half of China's | MISLEADING ("close behind") · fixed | "...with India, South Korea and Japan well behind." |
| flows.8 | Europe ~5%, US ~3% | 0.72/14.32 = 5.0%; 0.48/14.32 = 3.4% | CORRECT | none |

### The closing (timeline)

| Beat | Script says | Source says | Verdict | Replacement wording |
|---|---|---|---|---|
| closing.1 | 28 Feb strikes; IRGC radioing ships that none would pass | AJ 6/8 Oct: war "began on February 28". Reuters (EU Aspides official) and UKMTO Advisory 003-26 upd. 002 (report time 28 Feb 0700 UTC): VHF messages claiming no ship could pass (web search; advisory PDF at mscio.eu) | CORRECT · caption was wrong (credited AJ/CSIS) · fixed | caption "SOURCE: REUTERS · UKMTO ADVISORY 003-26" |
| closing.2 | Effectively closed by 2 Mar (CSIS) | CSIS 22 Apr 2026: "effectively closed since March 2" | CORRECT | none |
| closing.3 | "A few days later" the IEA verdict | IEA OMR published 12 Mar = 10 days after 2 Mar, 12 after 28 Feb | WRONG (mild) · fixed | "Ten days later the International Energy Agency..." |
| closing.3 quote | "The war in the Middle East is creating the largest supply disruption in the history of the global oil market." | IEA OMR March 2026, Highlights, first sentence, published 12 March 2026: identical | CORRECT, verbatim | none |
| closing.4 | 400 mb agreed 11 Mar | "IEA Member countries unanimously agreed on 11 March to make 400 mb ... available" | CORRECT | none |
| closing.5 | Output cut by at least 10 mb/d | "Gulf countries have cut total oil production by at least 10 mb/d" | CORRECT · card lacked "at least" · fixed | card "AT LEAST · BARRELS A DAY OF GULF OUTPUT CUT..." |
| closing.6 | $71.32 on 27 Feb; $138.21 on 7 Apr, highest since July 2008 | FRED DCOILBRENTEU, recomputed: 27 Feb 71.32; 7 Apr 138.21 (2026 max); last higher close 14 Jul 2008 (142.43). 138.21/71.32 = 1.94 ("nearly doubled") | CORRECT | none |
| closing.7 tl | 13 APR blockade | CENTCOM: blockade from 13 Apr 14:00 GMT (web search; Windward timeline "Blockade (13 Apr)") | CORRECT | none |
| closing.7 tl | 17 APR open for a day | CSIS: declared open 17 Apr, IRGC "announced it shut just one day later" | CORRECT | none |
| closing.7 tl | 17 JUN deal | AJ 7 Jul: MoU "announced on June 14"; AJ 17 Jun: Iran confirms it was signed electronically (17 Jun) | CORRECT (signing date). Note: the announcement was 14 Jun | none |
| closing.7 tl | 7 JUL missiles hit ships | AJ/Reuters 7 Jul: struck "on Monday night" = 6 Jul, reported early 7 Jul | WRONG (date) · fixed | "6 JUL" |
| closing.7 tl | 6 OCT, 9 tankers hit this month | see october.1 | CORRECT | none |
| closing.8 | 17 Apr open, 18 Apr shut; 13 tankers made it | CSIS: "at least 13 tankers made it through" | CORRECT · label needed "at least" · fixed | label "AT LEAST 13 · TANKERS MADE IT THROUGH" |
| closing.9 | June deal brought a brief reopening "which ended in early July when missiles struck..." | AJ 7 Jul: traffic was rising (31-43 crossings a day on 3-5 Jul) and talks were continuing; the attacks "complicate the talks" but "do not necessarily mean the process is over". IEA Sep: "continuing impasse", "renewed hostilities" | MISLEADING (the causal "ended ... when" is stronger than the source) · fixed | "In June, a deal between Washington and Tehran brought a brief, partial reopening. It began to unravel in early July, when missiles struck a Qatari gas carrier and a Saudi tanker." |
| closing.9 map | 7 JUL, Qatari LNG carrier off Limah, pin (56.45, 25.95) | UKMTO via AJ: "about 8 nautical miles (15km) off the coast of Limah"; ship named Al Rekayyat by Reuters sources. The old pin was 0.5 km from the coast | WRONG (date; pin) · fixed | label "6–7 JUL"; pin moved to (56.60, 25.95), ≈15 km offshore |

### How to close a strait

| Beat | Script says | Source says | Verdict | Replacement wording |
|---|---|---|---|---|
| how.1 | Radio warnings, drones, missiles, occasional seizures | VHF (above); projectiles and drones in Windward's log; IRGC seizures of MSC Francesca and Epaminondas (Apr) and Talara (Jun), via web search | CORRECT | none |
| how.1 map | Uses October pins to show the closure | The pins are from 1-6 Oct, not March | MISLEADING, minor · left | Note N1 |
| how.3 | War-risk cover ~0.2% to as much as 1% of hull value | AJ 3 Mar: "as high as 1 percent of the value of a ship in the past 48 hours, from about 0.2 percent last week" (industry sources); "for a single voyage" | CORRECT | none |
| how.4 | 1% of a ~$130m new VLCC is more than $1m | 1% × $130m = $1.3m. The premium is per voyage (AJ). The $130m newbuild price is Windward's from Oct, applied to a March premium | MISLEADING (did not say per voyage) · fixed | "On a new supertanker, that one percent comes to more than a million dollars for a single voyage." Card adds "PER VOYAGE" |
| how.5 | IMO: ~20,000 seafarers trapped, "aboard nearly two thousand ships" (19 Mar) | IMO SG Dominguez: ~20,000 seafarers stranded in the Gulf (to The National 5 Mar; to the IMO Council 18 Mar). **No source found for "2,000 ships"**: Windward counted 1,290 foreign-flagged cargo and tanker vessels on 19 Mar, and Mission to Seafarers said >3,000. FACTS F29b came from a search summary only | UNSUPPORTED (ship count, date) · fixed | "By March, the head of the International Maritime Organization said about twenty thousand seafarers were stranded inside the Gulf. They could not safely sail out." Label "≈20,000 SEAFARERS · STRANDED IN THE GULF · IMO, MARCH 2026" |
| how.6 | Approved route closer to Iran's coast, sharing voyage details, sometimes a fee | CSIS: "preapproved routes closer to Iranian waters", "sharing detailed voyage information, and in some cases paying additional fees" | CORRECT | none |
| how.6 map | R_NORTH Iran-approved route | The old path crossed Larak Island (Natural Earth) | WRONG (geometry) · fixed | waypoint (56.30, 26.90) added so the route passes north of Larak |
| how.7 | 187 ships, over half from 4 countries, China first; card "4 MAR TO ~20 APR" | CSIS: "Of the 187 vessels that have successfully transited the strait since March 4, over half are operated by shipping companies located in just four countries. China's position at the top" | CORRECT · card date range was inexact · fixed | card "4 MAR TO 22 APR" (the CSIS publication date) |
| how.8 | "A permission system" | Interpretation of CSIS | CORRECT (framed as analysis) | none |

### The way around

| Beat | Script says | Source says | Verdict | Replacement wording |
|---|---|---|---|---|
| around.1 | East-West line, Abqaiq to Yanbu; 5M rated, 7M expanded | EIA 65504: "5 million-b/d East-West crude oil pipeline ... from the Abqaiq ... to the Yanbu port"; "temporarily expanded ... to 7.0 million b/d in 2019". Drawn path: all on land | CORRECT | none |
| around.2 | Reported flat out at 7M by late March | Fortune/Bloomberg 28 Mar: "pumping oil at its full capacity of 7 million barrels a day, according to a person familiar"; 2 mb/d of that goes to Saudi refineries | CORRECT ("reported") | none |
| around.3 | Habshan to Fujairah, outside the strait; 1.5-1.8 mb/d | EIA 65504: "1.8 million-b/d pipeline links onshore oil fields to the Fujairah export terminal in the Gulf of Oman"; EIA 4430/61002: 1.5 | CORRECT | none |
| around.4 | ~2.5 (card 2.6) mb/d spare bypass | "about 2.6 million b/d ... could be available to bypass" | CORRECT | none |
| around.6 | Small tankers, often with transponders off, shuttle crude out to large tankers | AJ 6 Oct: "smaller shuttle boats, which often turn off their transponders ... offloading their cargoes onto larger tankers waiting just beyond it" | CORRECT | none |
| around.7 | 11.13m bbl out on 7 Oct, 9.09m by ship-to-ship | Windward 9 Oct: "Total crude outbound through Hormuz was 11.13m bbl on 7 Oct ... Ship-to-ship transfers ... 9.09m bbl" | CORRECT · STALE-RISK (daily) | none |
| around.8 | Kpler: ~40% bypass the strait | AJ 6 Oct: "Kpler estimates that about 40 percent of oil exports now bypass the strait" | CORRECT | none |
| around.9 | Kpler provisional 18.3 vs ~18 mb/d | AJ 6 Oct and AJ 8 Oct (identical figures) | CORRECT · STALE-RISK | none |
| around.10 | "IEA's August count still had Gulf exports at nearly half their pre-war level" | IEA Sep OMR: "Total oil exports from Gulf countries in August ... around 13 mb/d, nearly half their pre-war level. Crude losses ... just below 45%". The IEA figure includes products. Kpler's is crude only, and a month later | MISLEADING (not like for like) · fixed | "...because the IEA's count for August, a month earlier and including fuels as well as crude, still had Gulf exports at only about half their pre-war level." |

### October

| Beat | Script says | Source says | Verdict | Replacement wording |
|---|---|---|---|---|
| october.1 | UKMTO: 9 attacks on tankers in the strait, first six days of Oct | AJ/AFP 8 Oct: "UKMTO said on Tuesday [6 Oct] that there had been nine attacks on tankers in the Strait of Hormuz this month" | CORRECT | none |
| october.2 | Half of September's strait + Gulf total (~18) | "representing half of the September total in the waterway and the Gulf combined" (~18 is arithmetic) | CORRECT | none |
| october.3 map | 6 pins labelled "1–8 OCT" | The narrows pins are 1-6 Oct (the 7 and 8 Oct strikes are off Qatar and Fujairah, outside this view). Pin (56.40, 26.36) was on Musandam land | WRONG (label; one pin on land) · fixed | label "1–6 OCT"; pin moved to (56.46, 26.40) |
| october.4 | Every confirmed target was dark in the southern corridor, Omani side | Windward 9 Oct: "MIOC has confirmed 12 of the vessels: all were transiting dark via the southern corridor, and 11 were tankers". "Omani side" fits the log ("~4 nm east of Oman"), though Windward does not say it in those words | CORRECT | none |
| october.5 | 7 Oct tanker hit 94 km N of Qatar; 8 Oct tanker burning off Fujairah | AJ/AFP 8 Oct: "94 kilometres (58 miles) north of Madinat ash Shamal" (UKMTO; struck "on Wednesday" = 7 Oct). Windward: "51 nm" (= 94 km); Fujairah: "reported struck and on fire east of Fujairah, about 10 nm from the SPM area; first strike there in six months" (one source) | CORRECT (Fujairah rests on Windward alone; "reported" kept) | none |
| october.6 | Fujairah is where the UAE bypass reaches the sea | EIA 65504 | CORRECT | none |
| october.7 | "If I am reading this correctly, the attacks are following the oil" | Opinion, flagged as such. Consistent with Windward MIOC: "the westward spread likely extends risk to the GCC terminals and anchorages" | CORRECT (opinion, labelled) | none |
| october.8 map | R_EUROPE route | The old path cut about 400 km across Oman (59.4,23.9 → 57.8,19.5) | WRONG (geometry) · fixed | waypoints (60.0, 22.6), (59.3, 20.6), (58.5, 19.0) take it round Ras al Hadd. The Suez leg still crosses "land" at 10m resolution because it is the canal. R_CHINA got a Singapore Strait waypoint fix |

### The price

| Beat | Script says | Source says | Verdict | Replacement wording |
|---|---|---|---|---|
| price.1 | "That is why oil now has two prices" (after freight beats) | The futures-spot gap is a prompt-scarcity / backwardation effect (IEA Sep: "Backwardation reached extreme levels") and not caused by freight | MISLEADING (causal link) · fixed | "And oil now has two prices." |
| price.2 | Freight 25-30% of delivered cost vs 1-3% | Windward 9 Oct: "Freight now makes up 25–30% of the delivered cost of Gulf crude, against 1–3% normally" | CORRECT (one firm, attributed) · STALE-RISK | none |
| price.3 | Second-hand VLCC ~$200m record vs ~$130m new | Windward: "A second-hand VLCC sold for a record of about $200m, against roughly $130m for a newbuild" | CORRECT | none |
| price.4 | Brent futures "settled just under a hundred" at $99.57 on 6 Oct; card "ICE BRENT FUTURES" | AJ 6 Oct: "Brent crude ... dropping 0.75 percent to $99.57 a barrel on Tuesday ... according to data from Oilprice.com". This is an intraday quote from an article published that day. No settlement was found | UNSUPPORTED ("settled") · fixed | "...traded just under a hundred dollars." Card "BRENT FUTURES · 6 OCT 2026 · OILPRICE.COM VIA AL JAZEERA" |
| price.5 | Physical Brent spot $125.44 on 6 Oct, EIA | FRED DCOILBRENTEU 2026-10-06 = 125.44 (5 Oct 125.51, 2 Oct 135.51, 1 Oct 114.82) | CORRECT · STALE-RISK (swings of $20 in a day) | none |
| price.6 | "The gap ... is the strait's toll, paid in freight, insurance and scarcity" | The EIA series is Brent FOB (North Sea), so Gulf freight and insurance are not in it. IEA Sep: "physical benchmarks were significantly higher" than futures | MISLEADING · fixed | "That gap measures how scarce real barrels are right now, and I read it as part of the strait's toll." Card "THE GAP IS SCARCITY" |
| price.7 | Stocks down >500 mb since war began (-507M "since February") | IEA Sep OMR: "cumulative draws since February to 507 mb" (data to end-August) | CORRECT · STALE-RISK (the October OMR lands before or near upload) · card now dated | card "FEB TO END-AUG" |
| price.8 | Demand to shrink 2.5 mb/d in 2026, FORECAST | "World oil demand is forecast to decline by 2.5 mb/d in 2026"; "higher fuel prices ... will continue to weigh on consumption" | CORRECT (labelled forecast) · STALE-RISK | none |
| price.9 | Gasoline $3.12 (6 Oct 2025) → $4.35 (5 Oct 2026) | FRED GASREGW: 3.124 and 4.354 | CORRECT · STALE-RISK (weekly; the next print is 12 Oct) | none |

### Verdict

| Beat | Script says | Source says | Verdict | Replacement wording |
|---|---|---|---|---|
| verdict.2 | Hormuz is "less like a tap and more like a tollgate" | Opinion ("My answer") | CORRECT (opinion, labelled) | none |
| verdict.3 | "Closing it did not stop the oil, but it made every barrel more expensive to move" | IEA: flows went "to a trickle" in March; >10 mb/d of Gulf output was still shut in through August; exports were about half of pre-war in August | MISLEADING (it left out that flows were cut hard for months, which is the "tap" effect) · fixed | "Closing it cut the flow hard for months, but it never stopped the oil. Once the detours were built, it mostly made every barrel more expensive to move, and the world drew on its reserves to cover the difference." |
| verdict.4 list | $71 → $138; 10M+ cut; -507M; demand falling; oil kept moving | as above | CORRECT | none |
| verdict.5 | "buffers are much thinner now than in March" | -507 mb against 8.2 bn bbl of observed stocks in January (IEA Mar OMR), about -6%. IEA: "buffers shrinking" | MISLEADING (mild, "much") · fixed | "...the buffers are thinner now than they were in March." Card "DRAWN TO END-AUGUST" |
| verdict.6-8 | What to watch | Framed as the narrator's watch-list. verdict.9 says "None of this is a forecast or advice about money" | CORRECT (opinion, not forecast) | none |
| verdict.10 | 8 ships on 8 Oct | Windward | CORRECT · STALE-RISK | none |

## 2. Notes left as they are

- **N1.** how.1 uses three of the October attack pins to illustrate the March closure mechanism. The caption says
  "positions approximate", but a viewer may read these as the March attacks. Either drop the pins from how.1 or
  accept it as illustrative.
- **N2.** The POST.md thumbnail "8 SHIPS A DAY" rests on one day (8 Oct; 7 Oct was 18). Windward's own weekly figure
  (55 transits on 16-23 Sep, about 8 a day) supports it as a typical rate. Traffic was much higher during the
  June-July reopening (31-43 a day, AJ 7 Jul), so "a day" should not be read as "all year".
- **N3.** The attack pins remain approximate by design. Six of nine early-October strait attacks are pinned.
- **N4.** `flow/lines.json` and the `flow/qc` frames are a draft render of the old text. Re-render before voicing.

## 3. Stale by upload: re-check on upload day

1. **Windward daily** (open.1, verdict.10, around.7): 8 transits, 11.13m / 9.09m bbl. These change daily. Either
   keep "on the eighth of October" exactly as dated, or re-pull.
2. **Brent pair** (price.4-5): $99.57 futures (intraday, 6 Oct) vs $125.44 spot (6 Oct). Spot moved $114.82 →
   $135.51 → $125.51 → $125.44 across 1-6 Oct. If the upload is after mid-October, re-pull both numbers for the
   same date and use a futures *settlement* from a named source.
3. **IEA October OMR** (around mid-October): -507 mb, -2.5 mb/d, the August export figure. Replace with the
   October figures if it is out.
4. **UKMTO / Kpler** (october.1-2, around.8-9): "this month" counts and the provisional 18.3 mb/d. Kpler revises.
5. **GASREGW** (price.9): the next weekly print is Mon 12 Oct.
6. **Status of the strait and the talks**: AJ's navigation on 8 Oct showed "Why have strikes resumed?". Check that
   nothing on upload day (a reopening, a deal, or a new closure) makes "closed" in the title untrue.

## 4. Could not settle

- The ICE Brent *settlement* on 6 Oct: not found (no ICE or Reuters settle page available). That is why the
  script now says "traded".
- The exact charted TSS coordinates: IMO and UKHO charts were not available. The lanes are redrawn
  schematically from the geometry above. They are on Oman's side of a nearest-coast median, which is consistent
  with the TSS being in Omani territorial waters.
- The "2,000 ships" figure: no source found. Removed.

## 5. Edits applied to script.py (before → after)

Lint: `script.py: 0 flagged`. Import: 9 chapters, 77 beats (unchanged). Geometry re-tested: no pin on land, no lane
point nearer Iran, R_NORTH / R_EUROPE (except the Suez Canal) / R_CHINA clear of land.

1. R_GULF_OUT points 4-12: `(55.3,26.40) ... (56.96,26.53),(57.2,26.1),(57.9,25.2)` → `(55.3,26.32),(56.12,26.37),(56.26,26.47),(56.43,26.54),(56.55,26.53),(56.63,26.39),(56.67,26.12),(57.4,25.4)`. The route now follows the outbound lane and no longer crosses Iran's coast at 57.2E. The slice `[4:11]` still covers the narrows.
2. Z_INBOUND / Z_OUTBOUND: replaced with lanes on the Omani side (2 nmi lanes, 2 nmi median, bending round the Quoins and down the Musandam side), with a comment.
3. R_NORTH: added waypoint (56.30, 26.90) so the route no longer crosses Larak.
4. R_EUROPE: `(59.4,23.9),(57.8,19.5)` → `(59.4,23.9),(60.0,22.6),(59.3,20.6),(58.5,19.0)` (no longer crosses Oman).
5. R_CHINA: `(103.8,1.2)` → `(103.0,1.45),(103.8,1.15),(104.4,1.3)` (Singapore Strait instead of Johor).
6. OCT_HITS[0]: (56.40, 26.36) [on land] → (56.46, 26.40).
7. open.1: "...and yet the Middle East is exporting roughly as much crude oil as it did before the war." → "...and yet, by one tracker's count, Middle East crude exports are back to about where they were before the war."
8. gap.4 labels: INBOUND (56.20,26.70) → (56.22,26.62); OUTBOUND (56.30,26.45) → (56.34,26.44).
9. flows.4: "Iraq, the Emirates, Kuwait, Qatar and Iran" → "Iraq, the Emirates, Iran, Kuwait and Qatar".
10. flows.7: "close behind" → "well behind".
11. closing.1 caption: "SOURCE: AL JAZEERA · CSIS" → "SOURCE: REUTERS · UKMTO ADVISORY 003-26".
12. closing.3: "A few days later" → "Ten days later".
13. closing.5 card: added "AT LEAST".
14. closing.7 timeline: "7 JUL" → "6 JUL".
15. closing.8 label: "13 TANKERS / MADE IT THROUGH · CSIS" → "AT LEAST 13 / TANKERS MADE IT THROUGH · CSIS".
16. closing.9: "...brought a brief reopening, which ended in early July when missiles struck..." → "...brought a brief, partial reopening. It began to unravel in early July, when missiles struck..."; label "7 JUL" → "6–7 JUL"; pin (56.45,25.95) → (56.60,25.95) (≈8 nm off Limah).
17. how.4: "...one percent of the hull is more than a million dollars." → "...that one percent comes to more than a million dollars for a single voyage."; card adds "PER VOYAGE".
18. how.5: "...counted about twenty thousand seafarers trapped west of the strait. They were aboard nearly two thousand ships." → "...the head of the International Maritime Organization said about twenty thousand seafarers were stranded inside the Gulf. They could not safely sail out."; label → "≈20,000 SEAFARERS / STRANDED IN THE GULF · IMO, MARCH 2026"; caption → "SOURCE: IMO SECRETARY-GENERAL, 18 MAR 2026".
19. how.7 card: "4 MAR TO ~20 APR" → "4 MAR TO 22 APR".
20. around.10: "...the IEA's August count still had Gulf exports at nearly half their pre-war level." → "...the IEA's count for August, a month earlier and including fuels as well as crude, still had Gulf exports at only about half their pre-war level."
21. october.3 label: "1–8 OCT" → "1–6 OCT".
22. price.4: "That is why oil now has two prices. ... settled just under a hundred dollars." → "And oil now has two prices. ... traded just under a hundred dollars."; card "ICE BRENT FUTURES · 6 OCT 2026 · VIA AL JAZEERA" → "BRENT FUTURES · 6 OCT 2026 · OILPRICE.COM VIA AL JAZEERA".
23. price.6: "The gap between those two numbers is the strait's toll, paid in freight, insurance and scarcity." → "That gap measures how scarce real barrels are right now, and I read it as part of the strait's toll."; card "THE GAP IS THE TOLL" → "THE GAP IS SCARCITY".
24. price.7 card: "SINCE FEBRUARY" → "FEB TO END-AUG".
25. verdict.3: "Closing it did not stop the oil, but it made every barrel more expensive to move, ..." → "Closing it cut the flow hard for months, but it never stopped the oil. Once the detours were built, it mostly made every barrel more expensive to move, ..."
26. verdict.5: "much thinner" → "thinner"; card "BARRELS ALREADY DRAWN" → "BARRELS DRAWN TO END-AUGUST".

Also edited, outside script.py: the POST.md source list. The IMO line now reads "18 Mar 2026, IMO Council"
(it was "via Reuters 19 Mar"), and a line was added for UKMTO Advisory 003-26 / Reuters on the VHF warnings.
