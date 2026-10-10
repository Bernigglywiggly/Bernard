# FACTCHECK: Fehmarnbelt pilot (`script.py`)

Independent check, 9 Oct 2026. Every page below was fetched fresh today as raw HTML and read in full (not through a
summariser), except where marked (search) or (summary). VERIFY.md was used only as a list of URLs.

**Result: 65 claim rows. CORRECT 53 · WRONG 0 · UNSUPPORTED 3 · MISLEADING 5 · STALE-RISK 4.**
All 8 UNSUPPORTED and MISLEADING items are already fixed in `script.py`. Six CC BY-SA photos (7 beats) were taken out.
Script loads, 94 beats, unchanged count.

Source keys: S1-S17 are the URLs in the `script.py` docstring. New ones opened by this check:
- N1 femern.com fact sheet, 2 Mar 2026: https://femern.com/media/rarfzhzq/fakta-femern-baelt-projektet-2026.pdf
- N2 femern.com, "First tunnel element ... to be immersed", 4 May 2026: https://femern.com/press/news/first-tunnel-element-of-the-fehmarnbelt-tunnel-to-be-immersed/
- N3 femern.com, "Second element ... successfully immersed", 29 Jun 2026: https://femern.com/press/news/second-element-for-the-fehmarnbelt-tunnel-successfully-immersed/
- N4 femern.com Danish version of S4, 28 Sep 2026: https://femern.com/da/presse/nyheder/nedsaenkning4/
- N5 Sund & Bælt half-year announcement, 3 Sep 2026: https://sundogbaelt.dk/nyheder-presse/nyheder/2026/selskabsmeddelelse-sund-baelt-fik-fremgang-i-forste-halvar/
- N6 femern.com and sundogbaelt.dk news listings (EN, DA), read 9 Oct 2026: https://femern.com/press/news/
- N7 Ingeniøren, 2 Jul 2026 (summary, paywalled): https://ing.dk/artikel/femern-klods-paa-stoerrelse-med-krydstogtskib-nedsaenket-men-byggeriet-gaar-alt-langsomt
- N8 ADAC, 5 May 2026 (summary): https://www.adac.de/news/fehmarnsundtunnel/
- N9 Witteveen+Bos, May 2026 (summary): https://www.witteveenbos.com/news/operation-fehmarbelt-tunnel-gets-underway
- N10 Wikimedia Commons API (`extmetadata`) for all 22 files, read 9 Oct 2026

## 1. Claims

| Beat | Script says | Source says (URL key, date) | Verdict | Exact replacement wording |
|---|---|---|---|---|
| Working title | "Europe's Sunken Tunnel Is Years Late" | S2 (17 May 2026): "construction on the Danish side is currently around two years behind schedule". S3 (21 Jan 2026): "no longer realistic to open the link in 2029". Established by the owner for the construction schedule. Not established: any late *opening* (2029 has not arrived, no new date exists) | CORRECT, with the qualifier | Keep. Safer variant if wanted: "Europe's Sunken Tunnel Is Two Years Behind" |
| TITLE card | 89 PIECES UNDER THE BALTIC | S1, S4: 89 elements (79 + 10) | CORRECT | none |
| open-1 | longest of its kind, 18 km, about two years late | S1: "by far ... the longest immersed tunnel in the world", 18 km. S2: around two years behind. ENR (S13) says "at least two years" | CORRECT | none |
| open-2 | each weighs more than 73,000 t; card 73,500 t standard element | S1: standard elements "more than 73,500 tonnes" | CORRECT (the 10 special elements are smaller; the card says "standard") | none |
| open-3 | late evening 4 May, five tugboats | S1: "late on Monday evening, 4 May 2026", five tugboats. N2: left harbour "at 9 pm on 4 May 2026" | CORRECT | none |
| open-4 | landed about two years behind the plan | S2, S3 (pontoon approval "almost two years behind the original schedule") | CORRECT | none |
| open-5 | 89 pieces; four on the seabed in October 2026 | S4 (28 Sep 2026). N6 read today: newest items are 5 Oct (Odense Port) and 28 Sep. No fifth element announced | STALE-RISK | none today; re-check N6 on upload day |
| open-6 | 2029 no longer realistic; no new date published | S3; N6 and N5 read today: no schedule item | STALE-RISK | none today; re-check N6 on upload day |
| gap-1 | about 20 km of open water | S17: crossing "approximately 20 km". S12: "20 km wide strait" | CORRECT | none |
| gap-2, gap-3 | Scandlines 45 minutes; every half hour, around the clock | S17: "takes 45 minutes"; "24/7/365 operation", "departures every 30 minutes" | CORRECT | none |
| gap-4 | in 2014 the Copenhagen-Hamburg express rolled onto the ferry | N10, photographer's caption (Tony Webster, 16 Sep 2014): "ICE 36 train from Copenhagen to Hamburg ... loads itself onto the ... ferry" | CORRECT (one source, a caption) | none |
| gap-5 | 10 minutes by car, 7 by train | S1, S4, S10 | CORRECT | none |
| gap-6 | Copenhagen-Hamburg 2.5 h; today quoted as 5 h and as 4.5 h | S1: "current 5 hours". S10: "from four and a half hours to two and a half" | CORRECT | none |
| gap-7, gap-8 | treaty September 2008; Denmark plans, builds, pays; Germany its own connections | S12: signed 3 Sep 2008; "Denmark assumes responsibility for the planning, construction and funding" | CORRECT | none |
| method-3 | Denmark drives through an immersed tunnel to Sweden | N10 (Drogden tunnel files); S18 | CORRECT (no owner source opened) | none |
| method-4 | about 3.5 km; longest in service under 7 km | S18 Wikipedia only: Drogden 3.51 km; HZMB 6.7 km, Shenzhen-Zhongshan 6.75 km | CORRECT (Wikipedia only) | none |
| method-5 | "so nobody has ever joined this many pieces in a row" | No source counts elements across tunnels. Longest tunnel does not imply most elements | UNSUPPORTED | APPLIED: "The Fehmarnbelt tunnel will be eighteen, which is more than twice the length of any immersed tunnel built before it." (18 / 6.75 = 2.7) |
| method-6 | Øresund about 15 m; trench up to 40 m | S14 dpa: Öresund "at 15 metres", Fehmarn Belt "at 45 metres". S1: "up to 40 metres below the sea surface". N9: trench 45 m, track about 40 m | CORRECT (40 is the owner's figure; 45 is trench bottom) | none |
| method-7 | depth "is where the two years went" | Owner names the cause as "challenges with the specialized vessel" (S2) and pontoon approval (S3). Depth as the cause is dpa's juxtaposition, not a statement | UNSUPPORTED (causal claim) | APPLIED: "Hold on to that difference in depth, because it comes back when we reach the delay." |
| factory-2 | largest in Europe, 300 football pitches, 2,000+ people, 40+ countries | S7 (Summer 2026), verbatim. N1: "Europas største" | CORRECT | none |
| factory-3 | three halls, six lines, five for standard elements | S7 | CORRECT | none |
| factory-4 | 217 m, nine segments, about nine weeks | S8 | CORRECT | none |
| factory-5 | five tubes; "a narrow one in the middle" | S1: five tubes, two road, two rail, one technical. N2: element "is not naturally balanced", "outer railway tube", so the layout is not symmetric and no source puts the service tube in the middle | MISLEADING (position) | APPLIED: "...and a narrow fifth one is for technical installations and access." Check illustration g07 draws it between the road tubes, not at the centre |
| factory-6 | about 42 m wide, 9 m tall (engineering press) | S13: 138 ft x 0.3048 = 42.06 m; 30 ft x 0.3048 = 9.14 m | CORRECT | none |
| factory-7 | 79 standard, 10 special with basement, one about every 2 km | S4, S5, S7 | CORRECT | none |
| factory-8 | "At peak, the works harbour was taking in 65,000 t" | S7: "When ... production is at its peak, the work harbour ... will receive around 65,000 tonnes ... every week" (a planning figure, future tense) | MISLEADING (stated as a measured past fact) | APPLIED: "At peak production, the owner says, the works harbour takes in about sixty-five thousand tonnes ..." |
| factory-9 | design life at least 120 years | S7, S8 | CORRECT | none |
| trench-1 to trench-3 | marine work June 2020; up to 60 vessels; trench done 2024; almost 15 million m3 | S7; S13 (530 million cu ft x 0.0283168 = 15.0 million m3) | CORRECT | none |
| trench-4, trench-5 | about 300 ha of new land; first stretch opened 1 Sep 2026 | S7: "around 300 hectares". Owner news 2 Sep 2026: opened "Tuesday afternoon, 1 September", 300,000 m2 | CORRECT. Note: the Pilen viewpoint in the photo opened earlier and is not the area opened on 1 Sep | APPLIED to label: "THE PILEN VIEWPOINT · PHOTO FROM MAY 2026" |
| ivy-2 | two pontoons, Ivy 1 and Ivy 2, purpose-built | S7: "specifically designed" | CORRECT | none |
| ivy-3 | method used in Øresund at about 15 m; here more than twice that | S14; N2: "significantly deeper water". 40 / 15 = 2.7 | CORRECT | none |
| ivy-4 | CEO told reporters: half a centimetre; harder than planned | S14 dpa, 16 Jan 2026: "It was more difficult than planned ... a precision of half a centimetre" | CORRECT | none |
| ivy-5, ivy-6 | approval nearly two years behind (January) | S3: "almost two years behind the original schedule". S11: approval by "maritime authorities" | CORRECT | none |
| ivy-7 | same statement: 2029 no longer realistic | S3 | CORRECT | none |
| ivy-9, ivy-10 | German approval limits noise, where and when; hard to win back time | S2, near verbatim | CORRECT | none |
| night-1 to night-4 | late Monday 4 May; noon Wednesday; about 14 hours; gravel bed; laser on 7 May | S1; S3 (gravel bed); N3 (steel wires) | CORRECT | none |
| night-5, night-6 | hydraulic arms; bulkheads; water pumped out, sea pressure closes joint | S1, S8 | CORRECT | none |
| night-7 QUOTE CARD | "We are both happy and relieved." Mikkel Hemmingsen, CEO, Sund & Bælt, 7 May 2026 | S1, word for word, first sentence of the quotation. Also S13 | CORRECT (verbatim) | none |
| night-8 | element 2 on 27 Jun; element 3 on 1 Aug; element 4 announced 28 Sep | N3 (29 Jun): towed "Tuesday evening" (23 Jun), in place "Saturday morning" (27 Jun 2026 is a Saturday). S6 (2 Aug): connected "Saturday morning" (1 Aug is a Saturday). S4 | CORRECT | none |
| night-9 | nearly 900 m in place | S4. 4 x 217 = 868 m | CORRECT | none |
| money-1, money-2 | DKK 55.1 bn, 2015 prices, in the 2015 law; DKK 7.3 bn reserves | **The live femern.com/finance page no longer contains this sentence** (read today). It is on the dev mirror only. Confirmed instead by N1 (2 Mar 2026): "Anlægsbudgettet ... er 55,1 mia. kr. (2015-priser) inklusive reserver på 7,3 mia. kr." | CORRECT (source corrected in the docstring) | none |
| money-3, money-4 | EUR 7 bn (German ministry), USD 8 bn (ENR); "roughly the same budget" | S12: Feb 2016 analysis, "7 billion euros including reserves of 1 billion". S13: "$8-billion". DKK 55.1 bn / 7.46 = EUR 7.4 bn. N8 quotes EUR 7.1 bn | CORRECT ("roughly" carries it; the three are not identical budgets) | none |
| money-5 | delay will affect total cost; amount not published | S3; S11 | CORRECT | none |
| money-6 | EU roughly EUR 1.3 bn | S1, S9. S12: EUR 1.288 bn. N1: DKK 10.6 bn including planning grants | CORRECT | none |
| money-7, money-8 | user-financed like the two earlier links; delay only stretches repayment | S3, S9, as the owner's position | CORRECT | none |
| money-9 | cars first earns less early on | Our inference, spoken as "I'd add one caution" | CORRECT (labelled opinion) | none |
| germany-1 | about 88 km Puttgarden-Lübeck | S12: "88-kilometre-long rail infrastructure" | CORRECT | none |
| germany-3 | bridge would not meet future needs; immersed tunnel chosen 2020 | S12: "no longer meet future requirements"; "At the end of January 2020" | CORRECT | none |
| germany-4 | about 2 km; papers filed July 2025 | S12: "early July 2025". Length: 2.2 km (S15), 1.8 km (S16), "rund 1,5 km" (N8) | CORRECT ("about two" covers the spread) | none |
| germany-5 | July 2025: German ministry, rail not ready for 2029 | S2 | CORRECT | none |
| germany-6 | reported build time 6.5 years; no trains before end 2032 | S15 (24 Jul 2025), verbatim, citing sn.dk on an Eisenbahn-Bundesamt paper. Conflicts: S16 says EBA expects "three to four years of construction"; N8 (May 2026) says the German ministry confirmed "nicht vor 2031" | STALE-RISK (15-month-old press report; the document was not seen; newer figures differ) | none applied; the line is attributed. Optional: add "at the earliest" after "twenty thirty-two" |
| germany-7 | EUR 714 m first estimate; NDR reported at EUR 2.3 bn | S16 (4 Oct 2025) citing NDR. NDR's own article not found | CORRECT as attributed (third-hand) | none |
| germany-8, germany-9 | two stages announced in May; CEO: unfortunate for the green transition and rail passengers | S2 (17 May 2026), verbatim | CORRECT | none |
| now-1, now-2 | position on 9 Oct 2026; 4 of 89; a little under 5% | S4; N6 read today. 4 / 89 = 4.49% | STALE-RISK | none today |
| now-3 | 19 cast: 16 standard, 3 special | **The owner's two versions of the same release differ.** S4 English: "16 standard elements and 3 special". N4 Danish: "18 standardelementer og 3 specialelementer". N5 (3 Sep): 16 + 3 | MISLEADING (false precision) | APPLIED: "At least nineteen elements have been cast, three of them special ones ..." and card "19+" |
| now-4 | Danish portal complete; German over 90% of concrete | S7 (Summer 2026) | CORRECT | none |
| now-5, now-6 | special element 39 x 47 x 13 m, four-storey building, this autumn; load test +1,600 t | S5 (11 Sep 2026); S4 | CORRECT | none |
| now-7 | new timetable after five standard and one special; "could arrive within weeks of this video" | S11 (15 Jun 2026). Four standard are down, so two more immersions are needed (the special one and a fifth standard). Intervals so far: 51, 35 and about 41-58 days | UNSUPPORTED ("within weeks") | APPLIED: "That is two more immersions from here, so at this summer's pace it is likely months away." |
| now-8 QUOTE CARD | "No earlier than 2031." DPA, 16 Jan 2026 | S14 (datePublished 2026-01-16): "is now expected to open no earlier than 2031". The words exist, but as running agency text, not as a statement by anyone | MISLEADING (a fragment dressed as a quotation) | APPLIED: card text "now expected to open no earlier than 2031", credit "DPA NEWS AGENCY REPORT · 16 JAN 2026 · NOT CONFIRMED BY THE OWNER" |
| verdict-2 | one every five to seven weeks | Recomputed below | CORRECT (our arithmetic) | none |
| verdict-3 | 85 left; eight to eleven years | Recomputed below | CORRECT (our arithmetic, labelled) | none |
| verdict-4 | crews must speed up "several times over" for anything near 2031 | Our arithmetic, below. N3: owner expects "to increase the pace". N7: earlier target was one element every second week | CORRECT (our arithmetic; 2031 itself is unconfirmed) | none |
| verdict-6 | set "to within millimetres", done four times | S7: "an accuracy of a few millimetres" (a requirement, not a published measurement) | CORRECT (owner's requirement) | none |
| verdict-8 | ferries every half hour; 900 m built, 17 km to go | S17; S4. 18 - 0.87 = 17.1 | CORRECT | none |
| verdict-8 label | photo label "STILL SAILING" on a 2014 photograph | N10: taken 16 Sep 2014 | MISLEADING (implies a current picture) | APPLIED: "THE FERRY DEUTSCHLAND · 2014" |

### Derived figures, recomputed

| Figure | Working | Result |
|---|---|---|
| Completion dates | E1 7 May · E2 27 Jun · E3 1 Aug · E4 between 11 Sep (still in harbour, S5) and 28 Sep (announced, S4) | intervals 51 d, 35 d, 41-58 d |
| Pace, strict (intervals) | 7 May to 28 Sep = 144 d / 3 intervals | 48 d = 6.9 weeks |
| Pace, generous (throughput) | 4 May to 28 Sep = 147 d / 4 elements | 36.75 d = 5.3 weeks |
| "5 to 7 weeks" | 5.3 to 6.9 | holds. The low end is the generous count |
| Years, low | 85 x 36.75 d = 3,124 d / 365.25 | 8.6 years |
| Years, high | 85 x 48 d = 4,080 d / 365.25 | 11.2 years |
| "Several times over" | Oct 2026 to end 2030 = 221 weeks / 85 = 2.6 weeks each, against 6.9 now | about 2.7 times faster; 3.5 times to finish by end 2029 |
| Share in place | 4 / 89 | 4.49% |

This is arithmetic on four data points. It is not a forecast, and the script says so on screen ("OUR SUM, NOT A FORECAST").

## 2. Photos (licence and author read from the Commons API today; every file viewed)

| File | Licence and author confirmed? | Shows what the label says? | Keep / drop |
|---|---|---|---|
| fehmarnbelt_satellite_nasa | Yes. Public domain, "Photograph: NASA", from NASA World Wind. A Commons user drew the yellow route line | Yes: Lolland top right, Fehmarn below | KEEP |
| prinsesse_benedikte_2018 | Yes. CC BY 4.0, Dguendel, 20 Jun 2018 | Yes | KEEP |
| ice_train_on_ferry_2014 | Yes. CC BY 2.0, Tony Webster, 16 Sep 2014 | Yes (train on the ferry's rail deck) | KEEP |
| rodby_harbour_2014 | Yes. CC BY 2.0, Tony Webster, 16 Sep 2014 | Yes | KEEP |
| ferry_deutschland_2014 | Yes. CC BY 2.0, Tony Webster, 16 Sep 2014 | Mast and flag only. Old label "STILL SAILING" implied a current picture | KEEP, relabelled |
| drogden_tunnel_2024 | Yes. CC BY 4.0, Lukas Beck, 31 Mar 2024 | Yes (west portal) | KEEP |
| oresund_tunnel_portal_2019 | Yes. CC BY 2.0 tag, Johan Wessman / News Øresund, 13 Oct 2019 (caption says CC BY 3.0; both attribution only) | Yes. Number plates visible: do not push in on them | KEEP |
| pilen_viewpoint_2026, _b, _c | Yes. CC BY 4.0, Thomas Dahlstrøm Nielsen, 23 May 2026 | Yes. Pilen stands on reclaimed land (owner). It is not the area opened on 1 Sep 2026 | KEEP (one relabelled) |
| reynaert_fehmarnbelt_2026 | Yes. CC BY 4.0, same author, 23 May 2026 | Yes, a hopper dredger. Its task that day is unknown and the trench was finished in 2024; the label carries the date | KEEP |
| gpo_amethyst_fehmarnbelt_2026 | Yes. CC BY 4.0, same author, 23 May 2026 | A ship in the belt. No source ties it to the project; sitting under a line about German conditions, it reads as a project vessel | KEEP only with the neutral label; weakest picture in the film |
| puttgarden_site_2022 (2 beats) | Yes. CC BY 4.0, Fabian Horst, 11 Feb 2022 | Yes. "CROPPED" is on the credit, as the licence requires | KEEP |
| rodby_femern_2020 | Yes. CC BY 2.0 tag, Johan Wessman / News Øresund, 15 Jul 2020 | Yes | KEEP |
| fehmarnsund_bridge_2018 | Yes. CC BY 4.0, Dguendel, 19 Jun 2018 | Yes | KEEP |
| fehmarnsund_bridge_2005 | Yes. Public domain (PD-user), S. Möller, 10 Oct 2005 | Yes | KEEP |
| ferry_car_deck_2015 | Yes. **CC BY-SA 4.0**, Smiley.toerist, 21 Jul 2015 | Upper deck with identifiable passengers; "mid-crossing" is not stated on the file | DROP (applied) |
| oresund_link_aerial_2015 | Yes. **CC BY-SA 4.0**, Eskil Malmberg, 19 Jun 2015 | Yes | DROP (applied) |
| rodbyhavn_site_2021 | Yes. **CC BY-SA 2.0**, Lars Plougmann, 23 May 2021 | Dredging barges; the file does not name Rødbyhavn | DROP (applied) |
| rodbyhavn_portal_2025 (2 beats) | Yes. **CC BY-SA 4.0**, M.lundwall, 16 May 2025 | Yes. Only 1229 x 646 px | DROP (applied, both beats) |
| last_train_rodby_2021 | Yes. **CC BY-SA 4.0**, Leif Jørgensen, 29 Apr 2021 | Yes | DROP (applied) |
| drilling_platform_2015 | Yes. **CC BY-SA 4.0**, Holger.Ellgaard, 21 Sep 2015 | Yes | DROP (applied) |

**Kept: 16 files on 17 beats. Dropped: 6 files on 7 beats.**

### Share-alike, plainly

The engine tones, crops, pushes in and draws a label over each picture. Each of those alters the photograph, so the
result is an adaptation under CC BY-SA. The licence then requires that the adapted picture be released under the same
licence (BY-SA 4.0, or 2.0 or later for the Plougmann file). On the strict reading that covers the film that
incorporates it: anyone could copy, re-upload and remix it, commercially, with credit. YouTube offers no BY-SA
setting, and a monetised channel cannot accept that. POST.md line 85 says the BY-SA pictures "appear unaltered apart
from scaling"; with this engine that statement is false. Hence drop. They can come back only if the engine shows them
untouched (no tone, no crop, no label on the image) and the description says those frames stay BY-SA.

### Credit lines for the kept CC BY pictures

The on-screen line (name plus licence) is not enough alone. CC BY also needs a link to the licence, a link to the
source, and a note of changes. POST.md has names and licence URLs but **no source links** (it points to CREDITS.md,
which viewers cannot see) and no change note. Add to the description: each Commons URL, and one line such as
"Photographs cropped and colour-graded."

## 3. Required edits by severity

**High (all applied)**
1. now-7: "within weeks" was wrong on the owner's own trigger; two immersions are still needed.
2. now-8: quote card rebuilt on the agency's actual words.
3. Six CC BY-SA photographs removed from seven beats.

**Medium (all applied)**
4. method-5: "nobody has ever joined this many pieces" replaced with a length comparison.
5. method-7: depth no longer stated as the cause of the two years.
6. now-3: "nineteen" hedged to "at least nineteen" (owner's EN and DA pages disagree: 16 or 18 standard).
7. factory-8: 65,000 t attributed and put in the owner's tense.

**Low (applied)**
8. factory-5: "in the middle" removed.
9. Two labels: Pilen and the ferry Deutschland.
10. Docstring: source for DKK 55.1 bn corrected; photo count corrected.

**Not applied, needs a decision (other files, outside this brief)**
- POST.md: delete line 85, remove the six BY-SA credits, add Commons links and a change note.
- CREDITS.md and VERIFY.md still describe 22 photos and the old wording.
- Illustration g07: check where it draws the service tube.

## 4. Every edit made to `script.py` (before -> after)

| # | Beat | Before | After |
|---|---|---|---|
| 1 | method-5 | "...will be eighteen, so nobody has ever joined this many pieces in a row." | "...will be eighteen, which is more than twice the length of any immersed tunnel built before it." |
| 2 | method-7 | "...because it's where the two years went." | "...because it comes back when we reach the delay." |
| 3 | factory-5 | "a narrow one in the middle is for technical installations and access." | "a narrow fifth one is for technical installations and access." |
| 4 | factory-8 | "At peak, the works harbour was taking in sixty-five thousand tonnes..." | "At peak production, the owner says, the works harbour takes in about sixty-five thousand tonnes..." |
| 5 | now-3 line | "Nineteen elements have been cast, sixteen standard and three special, so..." | "At least nineteen elements have been cast, three of them special ones, so..." |
| 6 | now-3 card | `("19", "ELEMENTS CAST")` | `("19+", "ELEMENTS CAST · FEMERN A/S, 28 SEP 2026")` |
| 7 | now-7 | "That means it could arrive within weeks of this video." | "That is two more immersions from here, so at this summer's pace it is likely months away." |
| 8 | now-8 card | `("quote", "No earlier than 2031.", "DPA NEWS AGENCY · 16 JAN 2026 · NOT CONFIRMED BY THE OWNER")` | `("quote", "now expected to open no earlier than 2031", "DPA NEWS AGENCY REPORT · 16 JAN 2026 · NOT CONFIRMED BY THE OWNER")` |
| 9 | trench-5 label | "THE PILEN VIEWPOINT · MAY 2026" | "THE PILEN VIEWPOINT · PHOTO FROM MAY 2026" |
| 10 | verdict-8 label | "STILL SAILING" | "THE FERRY DEUTSCHLAND · 2014" |
| 11 | gap-3 | `("photo", "ferry_car_deck_2015", "ON DECK, MID-CROSSING · 2015", "PHOTO: SMILEY.TOERIST · CC BY-SA 4.0")` | `("words", "EVERY HALF HOUR")` |
| 12 | method-4 | `("photo", "oresund_link_aerial_2015", "THE ØRESUND LINK FROM THE AIR · 2015", "PHOTO: ESKIL MALMBERG · CC BY-SA 4.0")` | `("words", "THREE AND A HALF KILOMETRES")` |
| 13 | factory-1 | `("photo", "rodbyhavn_site_2021", "RØDBYHAVN, EARLY WORKS · MAY 2021", "PHOTO: LARS PLOUGMANN · CC BY-SA 2.0")` | `("words", "A FACTORY AT RØDBYHAVN")` |
| 14 | night-2 | `("photo", "rodbyhavn_portal_2025", "THE DANISH TUNNEL ENTRANCE, UNDER CONSTRUCTION · MAY 2025", "PHOTO: M.LUNDWALL · CC BY-SA 4.0")` | `("words", "A SHORT DISTANCE")` |
| 15 | germany-9 | `("photo", "last_train_rodby_2021", "THE LAST TRAIN TO RØDBY FÆRGE LEAVES COPENHAGEN · APRIL 2021", "PHOTO: LEIF JØRGENSEN · CC BY-SA 4.0")` | `("words", "UNFORTUNATE FOR THE GREEN TRANSITION")` |
| 16 | now-4 | `("photo", "rodbyhavn_portal_2025", "THE DANISH ENTRANCE · MAY 2025", "PHOTO: M.LUNDWALL · CC BY-SA 4.0")` | `("words", "CLOSE TO DONE")` |
| 17 | verdict-6 | `("photo", "drilling_platform_2015", "SURVEY DRILLING OFF RØDBY · 2015", "PHOTO: HOLGER.ELLGAARD · CC BY-SA 4.0")` | `("words", "DEEPEST WATER IS STILL AHEAD")` |
| 18 | docstring S9 | (finance page only) | adds: live page no longer has the DKK 55.1 bn sentence; fact sheet N1 confirms it |
| 19 | docstring photos | "22 real pictures, CC BY, CC BY-SA or public domain" | "16 real pictures used, CC BY or public domain"; notes the six removed |

Load check after edits: 94 beats, 17 photo beats, 16 distinct files, none CC BY-SA.

## 5. Unsettled

1. **The "where it stands" chapter dates the moment a fifth element or a timetable is announced.** Read N6 on recording
   day and again on upload day.
2. **Elements cast:** 19 (English page) or 21 (Danish page). The owner has not reconciled them.
3. **Element 4's actual immersion date** is not published (between 11 and 28 Sep). The pace sum uses the announcement date.
4. **Opening year:** dpa "no earlier than 2031" (Jan 2026); Witteveen+Bos "by mid-2032" (N9); German ministry via ADAC:
   Fehmarnsund tunnel and rail "nicht vor 2031" (N8). None is an owner date. N8 and N9 were read through a summariser.
5. **Fehmarnsund build time:** 6.5 years (The Local / sn.dk) against "three to four years" (YACHT, citing the same
   authority). The underlying document was not seen. NDR's own EUR 2.3 bn article was not found.
6. **Planned pace:** Ingeniøren (N7, paywalled, summary only) reports an earlier target of one element every second
   week. If read in full it would strengthen the verdict chapter; it is not in the script.
7. **Øresund depth of about 15 m** rests on dpa alone. Drogden length and "under 7 km" rest on Wikipedia alone.
8. **GPO Amethyst:** no evidence it worked on the project.
9. Line gap-5 says the tunnel "is meant to replace" the ferry. No source says the ferry will stop; left as written.
