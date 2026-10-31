# FACTS: MAPS & POWER 01, "The Strait of Hormuz"

Compiled Fri 9 Oct 2026 (sources opened 9 Oct, 20:40-21:30 BST). This is the only source for on-screen numbers,
names and claims in `script.py`. Before voicing, a separate checker who did not write the script verifies every
on-screen claim against these rows (CRAFT §5).

How sources were read: EIA, IEA, CSIS, Al Jazeera, Middle East Eye and Windward pages downloaded with curl and read as
raw text; EIA figure data (fig1.xlsx, fig3.xlsx of TIE 65504) parsed directly; FRED DCOILBRENTEU (the EIA's Europe
Brent spot price FOB series) downloaded as CSV and recomputed in Python. UKMTO's own site, Lloyd's List, S&P Global,
USNI and Euronews returned 403/empty, so UKMTO figures are read through the wire copy (AFP/DPA in Al Jazeera) and
Windward's daily briefing, which cites UKMTO. Wikipedia used only as a pointer (and for coordinates of places).

Confidence: HIGH = primary source read directly, or two independent good sources agree. MEDIUM = one reputable
secondary source quoting a primary, or a figure with a definitional ambiguity. LOW / UNVERIFIED = kept out of the script.

## 0. Title and thesis (CRAFT, Learned 6 Oct: put the title claim here before scripting)

| ID | Claim | Basis | Conf |
|---|---|---|---|
| T1 | "Hormuz is closed, the oil isn't": transits are in single digits while Middle East crude exports are back near pre-war levels | F30 (8 transits on 8 Oct) + F33 (Kpler: 7-day avg 18.3 mb/d on 30 Sep vs ~18 mb/d pre-war) + F34 (40% bypasses the strait; much of the rest crosses in ship-to-ship shuttles) | MEDIUM-HIGH (each part sourced; the export figure is provisional Kpler data via Al Jazeera) |
| T2 | Verdict (our own judgement, not a source's): the strait's power is a tax on moving oil, not a tap that stops it; a "closure" shifts cost into freight, insurance, inventories and the physical price | built from F33-F36, F40-F45 | judgement |

## 1. Geography

| ID | Claim (exact) | Source · URL · date | Conf | Use |
|---|---|---|---|---|
| F01 | Narrowest width 21 nautical miles (about 39 km) between Iran's Larak Island and Oman's Great Quoin Island | Wikipedia infobox "21 nmi" and Larak Island article "24 miles (39 km) lies between this Iranian island and Oman's Great Quoin Island"; EIA TIE 4430 (4 Jan 2012) says "At its narrowest point, the Strait is 21 miles wide" (unit not stated as nautical). Our own check: island centres are 43.5 km apart, so ~39 km shore to shore is consistent. https://www.eia.gov/todayinenergy/detail.php?id=4430 | MEDIUM (unit ambiguity: 21 nmi = 39 km = 24 statute miles; Wikipedia's crisis article says 34 km = 21 statute miles) | USE as "about twenty-one nautical miles / about 39 km" |
| F02 | Shipping lanes about two miles wide in each direction, separated by a two-mile buffer | EIA TIE 4430 (2012): "the width of the shipping lane in either direction is only two miles, separated by a two-mile buffer zone". Wikipedia (citing EIA WOTC 2017): each lane 2 nmi, separated by a similar median | MEDIUM (miles vs nautical miles) | USE as "about two miles" |
| F03 | Inbound and outbound traffic separation scheme lies in Omani territorial waters | Wikipedia (Maritime Executive 3 Apr 2026, 20 Jun 2025) | MEDIUM | USE |
| F04 | Iran's 1968 TSS agreement with Oman: in 2026 Iran argued it is not bound by it | NYT 30 Jun 2026 via Wikipedia | MEDIUM | context only |
| F05 | Islands: Qeshm, Hormuz, Larak (Iran); Greater and Lesser Tunb and Abu Musa (taken by Iran in 1971, claimed by UAE); Musandam is Omani | Wikipedia Strait of Hormuz / Tunbs | HIGH (long-standing) | USE |
| F06 | The strait is deep and wide enough for the world's largest crude tankers | EIA TIE 65504 (16 Jun 2025) | HIGH | USE |
| F07 | Depth figure | none found in a primary source | UNVERIFIED | KEEP OUT |
| F07b | "You could cross it by speedboat in under an hour" | our arithmetic: 21 nmi at 30 knots = 42 min (typical fast patrol/speedboat speeds exceed 30 knots) | MEDIUM (arithmetic) | USE |
| F08 | Before 2026 the strait had never been closed for an extended period in a Middle East conflict | Wikipedia citing OilPrice 17 Jun 2025 | MEDIUM | context only |

## 2. What flows (pre-war baseline, EIA)

Source for F10-F18: EIA, "Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint", Today in
Energy, 16 Jun 2025, https://www.eia.gov/todayinenergy/detail.php?id=65504 , and its figure data fig1.xlsx / fig3.xlsx
(Vortexa tanker tracking).

| ID | Claim (exact) | Conf | Use |
|---|---|---|---|
| F10 | 2024 oil flow averaged 20 million b/d (fig1: 20.26), "the equivalent of about 20% of global petroleum liquids consumption" | HIGH | USE |
| F11 | More than one-quarter of global seaborne oil trade (2024 and 1Q25) | HIGH | USE |
| F12 | Around one-fifth of global LNG trade transited in 2024, primarily from Qatar | HIGH | USE |
| F13 | Saudi Arabia: 38% of Hormuz crude flows in 2024 (5.5 million b/d) | HIGH | USE |
| F14 | 84% of crude and condensate and 83% of LNG through Hormuz went to Asia in 2024 | HIGH | USE |
| F15 | China, India, Japan, South Korea = combined 69% of Hormuz crude and condensate flows in 2024 | HIGH | USE |
| F16 | 2024 crude through Hormuz by destination (fig3, million b/d): China 4.78, India 1.89, South Korea 1.73, Japan 1.52, other Asia 2.07, Europe 0.72, United States 0.48 | HIGH | USE (China ≈ a third; Europe ≈ 5%; US ≈ 3% of ~14.3) |
| F17 | US imported ~0.5 million b/d via Hormuz in 2024 = ~7% of US crude imports, 2% of US liquids consumption | HIGH | USE |
| F18 | 2022: 21 million b/d, ~21% of consumption (EIA TIE 61002, 21 Nov 2023) https://www.eia.gov/todayinenergy/detail.php?id=61002 | HIGH | context |

## 3. Bypass routes

| ID | Claim (exact) | Source · date | Conf | Use |
|---|---|---|---|---|
| F20 | Saudi East-West pipeline, Abqaiq to Yanbu (Red Sea), 5 million b/d; temporarily expanded to 7.0 million b/d in 2019 | EIA TIE 65504 | HIGH | USE |
| F21 | UAE pipeline (Habshan) to Fujairah on the Gulf of Oman: 1.8 million b/d (EIA 2025); EIA 2023 said 1.5 | EIA 65504 / 61002 | HIGH (state "about 1.5 to 1.8") | USE |
| F22 | EIA estimated only ~2.6 million b/d of unused Saudi+UAE pipeline capacity could bypass the strait | EIA 65504 | HIGH | USE |
| F23 | Iran's Goreh-Jask pipeline, effective capacity ~300,000 b/d; loadings stopped after Sep 2024 | EIA 65504 | HIGH | context |
| F24 | East-West pipeline reported pumping at its full 7 million b/d on 28 Mar 2026; Yanbu crude exports ~5 million b/d; ~2 million b/d of the pipeline feeds Saudi refineries | Bloomberg via Fortune, 28 Mar 2026 (search summary; Fortune page not opened) https://fortune.com/2026/03/28/saudi-arabia-east-west-oil-pipeline-strait-hormuz-bypass-7-million-barrels-yanbu-red-sea/ | MEDIUM | USE ("reported") |
| F25 | East-West pipeline suffered temporary closures from drone strikes by Iran-backed groups in Iraq in September 2026 | Al Jazeera, 6 Oct 2026 (Varga quote context) | MEDIUM | USE |
| F26 | Combined capacity of all bypass pipelines (incl. Iraq's Kirkuk-Ceyhan) "about nine million b/d" | Wikipedia only | LOW | KEEP OUT |

## 4. The 2026 story (timeline)

| ID | Claim (exact) | Source · URL · date | Conf | Use |
|---|---|---|---|---|
| F27 | 28 Feb 2026: US and Israeli strikes on Iran begin; IRGC radioed ships that none would be permitted to pass | Al Jazeera 8 Oct / 6 Oct ("war ... began on February 28"); Wikipedia | HIGH (date) | USE |
| F28 | Strait "effectively closed since March 2" | CSIS, "The Strait of Hormuz in 8 Charts", 22 Apr 2026 https://www.csis.org/analysis/strait-hormuz-8-charts | HIGH | USE |
| F29 | 11 Mar: IEA members agreed to release 400 mb of emergency oil. IEA (12 Mar): "the largest supply disruption in the history of the global oil market"; flows "from around 20 mb/d before the war to a trickle"; Gulf producers cut output by at least 10 mb/d | IEA Oil Market Report, March 2026, published 12 Mar https://www.iea.org/reports/oil-market-report-march-2026 | HIGH | USE (quote) |
| F29b | ~20,000 seafarers on nearly 2,000 ships west of the strait (IMO Secretary-General, 19 Mar) | Reuters via search summary (AOL/Yahoo syndication) | MEDIUM | USE ("the IMO said") |
| F29c | 13 Apr: US Navy blockade of Iranian ports begins ("dual blockade") | Windward timeline label "Blockade (13 Apr)"; Wikipedia | MEDIUM-HIGH | USE |
| F29d | 17 Apr: Iran's foreign minister declared the strait open; IRGC shut it a day later; at least 13 tankers made it through | CSIS 22 Apr 2026 | HIGH | USE |
| F29e | Of 187 vessels that transited 4 Mar to ~20 Apr, over half were operated by companies in four countries, China at the top; ships moving on pre-approved routes closer to Iranian waters, some paying fees | CSIS 22 Apr 2026 | HIGH | USE |
| F29f | 5 May: Iran set up a "Persian Gulf Strait Authority" to authorise transits | Wikipedia | MEDIUM | context only |
| F29g | 17 Jun: US-Iran memorandum of understanding; a reopening began ~18 Jun but broke down in early July with missile attacks on ships (7 Jul: Qatari LNG carrier Al Rekayyat and a Saudi tanker hit) | Al Jazeera 7 Jul 2026 https://www.aljazeera.com/news/2026/7/7/ships-attacked-in-the-strait-of-hormuz-what-that-means-for-ongoing-talks ; Wikipedia for the MoU date | MEDIUM-HIGH | USE |
| F29h | Windward attack log: 93 incidents (85 attacks, 8 near misses) in the Hormuz/Gulf/Gulf of Oman threat zone since 28 Feb | Windward daily briefing, 9 Oct 2026 https://insights.windward.ai/ | MEDIUM (one tracker's count) | USE with attribution |
| F29i | UKMTO weekly overview of 2 Oct: 91 incidents of damage to vessels reported since February | Middle East Eye live blog, 4 Oct 2026 https://www.middleeasteye.net/live-blog/live-blog-update/three-commercial-vessels-struck-hormuz-1-oct-ukmto-says | MEDIUM | USE |
| F29j | "US-Iran MoU expired Monday [5 Oct]" | search summary only; contradicted by 60-day term | UNVERIFIED | KEEP OUT |

## 5. Now: October 2026

| ID | Claim (exact) | Source · URL · date | Conf | Use |
|---|---|---|---|---|
| F30 | Hormuz transits: 8 on 8 Oct (5 inbound, 3 outbound), down from 18 on 7 Oct | Windward, 9 Oct (data as of 8 Oct) | MEDIUM-HIGH | USE |
| F31 | Before the war the strait typically handled about 125 large commercial vessels a day | Al Jazeera (AFP/DPA), 8 Oct 2026 https://www.aljazeera.com/news/2026/10/8/tanker-hit-by-multiple-projectiles-off-north-coast-of-qatar-ukmto-says | MEDIUM (other trackers say 88-130+) | USE as "about a hundred and twenty-five" |
| F32 | **"At least nine attacks in October" (trend desk): CONFIRMED in this form.** UKMTO said on Tue 6 Oct "there had been nine attacks on tankers in the Strait of Hormuz this month, representing half of the September total in the waterway and the Gulf combined" | Al Jazeera/AFP 8 Oct | MEDIUM-HIGH (UKMTO via wire) | USE ("by the sixth of October") |
| F32b | UKMTO logged 16 attacks on merchant ships in the Gulf in the 10 days to 8/9 Oct; Windward confirmed 12 vessels, all transiting dark via the southern corridor, 11 of them tankers | Windward 9 Oct | MEDIUM | USE |
| F32c | 7 Oct: tanker hit by several projectiles 94 km (51 nm) north of Madinat ash Shamal, Qatar; first reported attack on a tanker in the western Gulf in weeks (Windward: first outside the Hormuz area since 9 Sep). 8 Oct: tanker reported struck and on fire east of Fujairah, ~10 nm from the loading moorings, first hit there in six months | Al Jazeera 8 Oct; Windward 9 Oct | MEDIUM-HIGH (Qatar), MEDIUM (Fujairah: one source) | USE |
| F32d | 1 Oct: Kuwaiti VLCC Kazimah III struck and set on fire in the strait; 6 Oct: 12 crew injured on a tanker (Indian MEA) | Al Jazeera 6 Oct; Windward | HIGH | USE |
| F33 | Kpler: 7-day average Middle East crude exports 18.3 million b/d on 30 Sep vs about 18 million b/d average in the 12 months before the war; Gulf flows ex-Iran >81% of pre-war in September; Middle East crude exports exceeded pre-war on 14 days in September. Vortexa: 14-day avg 18.6 million b/d | Al Jazeera, 6 Oct 2026 https://www.aljazeera.com/news/2026/10/6/hormuz-ship-attacks-surge-are-increased-oil-exports-sustainable | MEDIUM (provisional, via AJ) | USE with "according to Kpler" |
| F34 | Kpler: about 40% of oil exports now bypass the strait; much of the crude that does cross is transferred between tankers offshore; shuttles often run with transponders off | Al Jazeera 6 Oct | MEDIUM | USE |
| F34b | Windward: on 7 Oct crude outflow through Hormuz 11.13m bbl, of which ship-to-ship 9.09m bbl; 16-23 Sep transits ~94% below pre-war, roughly two-thirds of crude via STS | Windward 9 Oct | MEDIUM | USE (STS share) |
| F35 | IEA (Sep OMR, 11 Sep): Gulf oil exports in August ~13 mb/d, "nearly half their pre-war level"; crude losses just below 45%; more than 10 mb/d of Gulf output still shut in in August | IEA OMR Sep 2026 https://www.iea.org/reports/oil-market-report-september-2026 | HIGH | USE. NOTE: this is August, before the September recovery in F33; the script dates both |
| F36 | IEA: global observed inventories fell 507 mb since the war began (avg draw 2.8 mb/d); world oil demand forecast to FALL 2.5 mb/d in 2026; supply to fall 5.7 mb/d; Gulf recovery deferred to 2027; US diesel above $200/bbl early Sep | IEA OMR Sep 2026 | HIGH | USE |
| F36b | "Demand to shrink this year, as high prices bite" | IEA Sep OMR: "higher fuel prices, notably for diesel, will continue to weigh on consumption" | HIGH | USE |
| F37 | Aramco CEO Nasser (5 Oct, London): nearly three billion barrels of supply lost since late Feb; rebuilding inventories could take up to two years | Al Jazeera 6 Oct (reporting the speech) | MEDIUM | USE ("Aramco's chief executive said") |
| F38 | G7 announced release of up to 100 million barrels of strategic reserves (week of ~29 Sep) | Al Jazeera 6 Oct | MEDIUM | context |

## 6. Money: insurance, freight, prices

| ID | Claim (exact) | Source · URL · date | Conf | Use |
|---|---|---|---|---|
| F40 | Early March: war-risk premiums rose "as high as 1 percent of the value of a ship in the past 48 hours, from about 0.2 percent last week" | Al Jazeera, 3 Mar 2026 (industry sources) https://aljazeera.com/economy/2026/3/3/maritime-insurers-cancel-war-risk-cover-in-gulf-will-it-spike-energy-cost | MEDIUM-HIGH | USE |
| F41 | S&P Global (30 Mar): additional war-risk premium peaked ~2.5% of hull value per 7 days in early March, eased to ~1%, still up to 8x pre-war | search summary of S&P article (page 403) | LOW-MEDIUM | KEEP OUT (could not open) |
| F42 | Freight now 25-30% of the delivered cost of Gulf crude vs 1-3% normally; Saudi-China VLCC benchmark rate above $1.3m/day; a Red Sea to South Korea VLCC lump sum $73.9m (~$37/bbl) vs ~$50m a week earlier | Windward MIOC, 9 Oct 2026 | MEDIUM (one analytics firm) | USE with attribution |
| F43 | A second-hand VLCC sold for a record ~$200m vs ~$130m for a newbuild | Windward 9 Oct | MEDIUM | USE |
| F44 | EIA Europe Brent spot price FOB (FRED DCOILBRENTEU): Feb 2026 average $70.89; 27 Feb $71.32; peak $138.21 on 7 Apr 2026 (highest in the series since 14 Jul 2008); 6 Oct 2026 $125.44 | https://fred.stlouisfed.org/series/DCOILBRENTEU (downloaded 9 Oct; recomputed) | HIGH | USE |
| F45 | ICE Brent futures $99.57 on Tue 6 Oct (Oilprice.com data); IEA Sep OMR: futures $105 "while physical benchmarks were significantly higher"; Dated Brent averaged $91.00 in Aug and hit $113.48 on 9 Sep | Al Jazeera 6 Oct; IEA OMR Sep | MEDIUM (futures figure via AJ), HIGH (IEA) | USE: the gap between the paper price and the price of a real cargo |
| F46 | Brent futures intraday $119.50 on 9 Mar | Gulf News / secondary | LOW | KEEP OUT |
| F47 | US regular gasoline $3.124 (6 Oct 2025) → $4.354 (5 Oct 2026) | EIA via FRED GASREGW, fact-checked in pilot_ledger/FACTCHECK.md | HIGH | USE |

## 7. Qatar LNG

| ID | Claim (exact) | Source | Conf | Use |
|---|---|---|---|---|
| F50 | QatarEnergy CEO al-Kaabi: Iranian attack on Ras Laffan wiped out ~17% of Qatar's LNG export capacity (2 of 14 trains), 12.8 million tonnes a year sidelined for three to five years; ~$20bn lost annual revenue; force majeure on some long-term contracts (Italy, Belgium, South Korea, China) | Al Jazeera/Reuters, 24 Mar 2026 https://www.aljazeera.com/news/2026/3/24/qatarenergy-declares-force-majeure-on-some-lng-contracts | MEDIUM-HIGH | USE |
| F51 | 7 Jul: Qatari LNG carrier Al Rekayyat struck in the strait | Al Jazeera 7 Jul | MEDIUM-HIGH | USE |
| F52 | Current Qatar LNG export volume (Oct 2026) | not found | UNVERIFIED | KEEP OUT |

## 8. Trend desk claims, checked

| Trend desk said | Finding |
|---|---|
| "The 21-mile gap" | Right only in nautical miles (21 nmi ≈ 39 km ≈ 24 statute miles). EIA's own 2012 text says "21 miles". Script says "about twenty-one nautical miles". |
| "Tanker traffic at a low" | MISLEADING. Transits are in single digits (8 on 8 Oct, 18 on 7 Oct), roughly where they have been since March, not a new low. And oil EXPORTS are near pre-war (F33): the oil is moving, by pipeline and ship-to-ship shuttles. |
| "At least nine attacks in October" | CONFIRMED: UKMTO, nine attacks on tankers in the strait by 6 Oct (F32); 16 in the Gulf in 10 days (F32b). |
| Sister pilot: "the strait later reopened (by July)" | PARTLY WRONG. A reopening began ~18 Jun after the 17 Jun MoU and collapsed in early July (attacks 7 Jul onward). The ledger's line "In July, after the strait had reopened" is defensible only for the first week of July (the EIA STEO was 7 Jul). Recommend the ledger say "after a brief reopening in June". |

## 9. Places on screen (lon, lat) · source

| Place | lon, lat | Source |
|---|---|---|
| Larak Island (Iran) | 56.356, 26.853 | Wikipedia coord 26°51′12″N 56°21′20″E |
| Great Quoin / As Salamah (Oman) | 56.529, 26.494 | Wikipedia coord 26°29′39″N 56°31′45″E |
| Hormuz Island | 56.460, 27.068 | Wikipedia 27°04′03″N 56°27′36″E |
| Qeshm Island | 55.773, 26.768 | Wikipedia 26°46′03″N 55°46′21″E |
| Bandar Abbas | 56.288, 27.196 | Wikipedia 27°11′46″N 56°17′16″E |
| Khasab (Musandam) | 56.250, 26.183 | Wikipedia 26°11′N 56°15′E |
| Kumzar (Musandam) | 56.410, 26.337 | Wikipedia 26°20′12″N 56°24′35″E |
| Musandam Peninsula | 56.200, 25.900 | Wikipedia 25°54′N 56°12′E |
| Greater Tunb | 55.267, 26.250 | Wikipedia 26°15′N 55°16′E |
| Lesser Tunb | 55.133, 26.233 | Wikipedia 26°14′N 55°08′E |
| Abu Musa | 55.033, 25.867 | Wikipedia 25°52′N 55°02′E |
| Fujairah | 56.334, 25.122 | Wikipedia 25°07′20″N 56°20′04″E |
| Jask (Iran) | 57.782, 25.653 | Wikipedia 25°39′11″N 57°46′54″E |
| Ras Tanura (Saudi) | 50.053, 26.706 | Wikipedia 26°42′23″N 50°03′10″E |
| Abqaiq (Saudi) | 49.666, 25.935 | Wikipedia 25°56′06″N 49°39′58″E |
| Yanbu (Saudi, Red Sea) | 38.062, 24.089 | Wikipedia 24°05′22″N 38°03′43″E |
| Habshan (UAE) | 53.617, 23.825 | Wikipedia 23°49′30″N 53°37′E |
| Ras Laffan (Qatar) | 51.539, 25.858 | Wikipedia 25°51′27″N 51°32′20″E |
| Kharg Island (Iran) | 50.310, 29.245 | Wikipedia 29°14′42″N 50°18′36″E |
| Madinat ash Shamal (Qatar) | 51.20, 26.13 | approximate (town, north tip of Qatar); attack pin ~94 km north: 51.2, 26.98 (approximate) |
| Sea-route waypoints (Arabian Sea, Malacca, Singapore 103.8,1.25, Ningbo 122.3,29.8, Tokyo Bay 139.8,35.3, Ulsan 129.4,35.5, Sikka/Jamnagar 69.8,22.4, Bab el-Mandeb 43.4,12.6, Suez 32.55,29.95) | as listed | approximate, drawn for the film |
| Shipping lanes (zones) | see script | SCHEMATIC: drawn between Larak and the Quoins from F02 widths; not the charted TSS. On-screen caption says "LANES SCHEMATIC". |
| Pipelines (routes) | endpoints above, paths straight-ish | SCHEMATIC paths; endpoints sourced |

## 10. Counts

62 claim rows: 50 USE (HIGH, or MEDIUM with on-screen attribution), 7 context only, 6 KEEP OUT / UNVERIFIED (F07
depth, F26 nine-million bypass total, F29j MoU expiry, F41 S&P premium path, F46 futures intraday peak, F52 current
Qatar LNG volume), plus the trend desk's "tanker traffic at a low" (misleading, s.8). Every on-screen figure in
script.py traces to a USE row; a separate checker should confirm that before voicing.
