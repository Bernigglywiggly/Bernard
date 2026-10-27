# SpaceX: facts for Film 2 "How SpaceX Makes Money" (backlog; radar 26 Oct §4b, 27 Oct)

Checked Tue 27 Oct 2026, 04:40-04:55 UK, by account C. Row numbers are what the script's `facts=` fields point at.
Anything not in this file does not go on screen or in the voice.

**Method:** web search extracts of press coverage, plus SpaceX's SEC filing index (read from EDGAR's submissions feed). SEC.gov
blocks scripted page reads without a declared contact address, and we never use his email, so **the filings themselves weren't
opened here: open the 8-K and 10-Q below on the Mac before scripting and copy the numbers from them.** **V** = two or more
independent outlets agree on the number. **U** = one outlet. **OUR MATHS** = our arithmetic, labelled on screen.

## Sources

Primary (SEC filings, Space Exploration Technologies Corp, CIK 1181412, ticker SPCX, Nasdaq)
- **E1** Q3 2026 earnings 8-K, filed 20 Oct 2026: https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spcx-20261020.htm
- **E2** Q3 2026 10-Q (quarter to 30 Sep), filed 22 Oct 2026: https://www.sec.gov/Archives/edgar/data/1181412/000162828026066880/spcx-20260930.htm
- **E3** 8-K filed 26 Oct 2026 (GPU finance-lease commitment): https://www.sec.gov/Archives/edgar/data/1181412/000110465926118614/tm2628247d1_8k.htm
- **E4** IPO prospectus (424B4), 12 Jun 2026: https://www.sec.gov/Archives/edgar/data/1181412/000162828026042639/spaceexplorationtechnologi.htm
- **E5** Q2 2026 10-Q, filed 4 Aug 2026: https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm

Press
- **N1** CNBC, Q3 live updates, 20 Oct: https://www.cnbc.com/2026/10/20/spacex-spcx-earnings-live-updates-q3-2026html.html
- **N2** Quartz, 20 Oct: https://qz.com/spacex-earnings-revenue-net-income-super-intelligence-starlink-102026
- **N3** The Next Web: https://thenextweb.com/news/spacex-quarterly-revenue-ai-starlink-q3 · SpaceQ: https://spaceq.ca/spacex-q3-2026-ai-passes-starlink-profit/ · Yahoo Finance: https://finance.yahoo.com/markets/stocks/articles/spacex-beats-q3-2026-estimates-204304560.html
- **N4** CNBC, $40B GPU financing, 26 Oct: https://www.cnbc.com/2026/10/26/spacex-closes-40-billion-debt-deal-for-ai-chips-elon-musk-.html · Fox Business: https://www.foxbusiness.com/technology/spacex-secures-40b-financing-gpus-elon-musk-warns-ai-cloud-industry-consolidation
- **N5** Barclays upgrade of Tesla on the merger case, 26 Oct: https://finance.yahoo.com/markets/stocks/articles/tesla-soars-6-barclays-upgrade-152930834.html · StreetInsider: https://www.streetinsider.com/Investing/Barclays+upgrades+Tesla,+says+SpaceX+merger+%22now+a+key+part+of+bull+case%22/27230339.html
- **N6** Cursor (Anysphere) deal: The Next Web https://thenextweb.com/news/spacex-cursor-acquisition-official-60-billion · Quartz https://qz.com/spacex-buying-cursor-anysphere-60-billion-deal-061626
- **N7** IPO: BusinessDay/Reuters https://www.businessday.co.za/world/international-companies/2026-05-17-spacex-targets-june-12-for-mega-ipo/ · Wikipedia https://en.wikipedia.org/wiki/Initial_public_offering_of_SpaceX
- **N8** Launch and constellation counts: KeepTrack https://keeptrack.space/live-count/how-many-satellites-does-spacex-have

## 0. Checked on the SEC filings themselves (Tue 27 Oct ~13:05 UK, account C, Mac session)

E1's 8-K page only furnishes the release; the numbers are in its Exhibit 99.1:
**E1a** https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm . All $ in millions as printed.
**P** = read in the filing. Where a row below says V or U, this table wins.

| # | What | Filing says | Rows it settles |
|---|---|---|---|
| 0a | Revenue, Q3 2026 vs Q3 2025 | **14,575** vs 5,576 (+161%) (E2) | 1: P |
| 0b | Net income; income from operations | **4,404** (Q3 2025: -1,054); **2,791** (Q3 2025: -273) (E2) | 2: P (operating was U) |
| 0c | Segment revenue, Q3 2026 vs Q3 2025 | SI **7,560** vs 813 · Connectivity **5,248** vs 3,097 · Space **1,767** vs 1,666 (E2) | 10-12: P |
| 0d | Segment operating income, Q3 2026 vs Q3 2025 | SI **431** vs -1,722 · Connectivity **2,367** vs 1,190 · Space **-7** vs 259 (E1a) | 10-12: P |
| 0e | Connectivity split | Consumer **3,121** (Q3 2025: 1,986); government and enterprise = 5,248 - 3,121 = 2,127 (OUR MATHS) (E2) | 11: P |
| 0f | Starlink consumer subscribers; ARPU | **13.6M** at 30 Sep (7.2M a year earlier); ARPU **$69** a month, "improved 5% sequentially", but **$83** a year earlier (E1a). Never say ARPU is rising without "since last quarter" | 11: P |
| 0g | Cursor | Closed **14 Aug 2026**; added **608** of revenue to 30 Sep; **1,217** of share-based pay "related to acquisitions" in SI (E1a) | 10, 32 (close date): P |
| 0h | Capital spending | Q3 **19,593** (SI 16,444, Connectivity 1,543, Space 1,606) (E1a). Cash-flow check: 9 months 48,069 (E2) - 6 months 28,476 (E5) = 19,593 | 3: P |
| 0i | Adjusted EBITDA | **8,809** (E1a). Capex ÷ adjusted EBITDA = 2.2 (OUR MATHS) | 3 ("more than double"): P |
| 0j | Who rents the compute | **No customer is named.** E2: "Customer A" = **16.6%** of Q3 revenue ("relates to all three segments"); "Customer B" = **34.5%** of Q3 revenue ("relates to the SI segment"; under 10% a year earlier). One customer held 27.7% of receivables. OUR MATHS: 34.5% × 14,575 ≈ 5,030, about two thirds of SI's 7,560 | 13: **never name a customer on screen**. Usable line: "one unnamed customer paid about a third of all SpaceX's revenue" |
| 0k | The $40B GPU deal | E3, Item 8.01: on **24 Oct 2026** SpaceX "entered into a binding commitment letter to enter into a master finance lease" with "an entity managed by Apollo Global Management, Inc.", which buys "certain graphics processing unit pods and related equipment"; principal payments "to total approximately $40 billion"; master lease "expected to close prior to year end"; schedules "commence during the first half of 2027 upon delivery of the GPUs"; risk "that the transaction may not close on the anticipated terms or timeline, or at all"; "subject to certain specified closing conditions" | 21: P (wording copied) |
| 0l | 2025 revenue (row 33) | Not checked: E4 is over 10 MB, too big for the page reader. Open it in a browser before using row 33 | 33: still U |

## 1. The quarter (Q3 2026, three months to 30 Sep; reported 20 Oct)

| # | Fact | Source | Status |
|---|---|---|---|
| 1 | Revenue $14.6B, up 161% from $5.6B a year earlier | N1, N2, N3 (E1) | V |
| 2 | First profit as a public company: net income $4.4B; operating income $2.8B | N3 (E1) | V (net), U (operating) |
| 3 | Capital spending $19.6B in the quarter, more than double adjusted EBITDA | N3 | U |
| 4 | Three segments: **Super Intelligence** (AI), **Connectivity** (Starlink), **Space** (launch) | N1-N3 | V |

## 2. Where the money comes from (the film's spine)

| # | Segment, Q3 2026 | Revenue | Operating result | Driver, as reported | Source | Status |
|---|---|---|---|---|---|---|
| 10 | **Super Intelligence** (AI) | **$7.56B**, up 830% from $813M | +$431M (after $1.2B of stock pay tied to the Cursor deal) | Cloud contracts renting SpaceX's computing to outside AI developers; Cursor (bought mid-August) added $608M; Grok use by businesses and consumers | N2, N3 | V |
| 11 | **Connectivity** (Starlink) | **$5.25B**, up 69% | +$2.37B (about doubled) | 13.6M consumer subscribers (12M the quarter before); average revenue per user $69 (from $66). Consumer $3.12B, government and enterprise $2.13B | N2, N3 | V |
| 12 | **Space** (launch, Starship) | **$1.77B** (from $1.67B) | **-$7M** (vs +$259M a year earlier). Q2: -$542M as Starship R&D rose | Falcon launches; Starship development costs | N2, N3 | V |
| 13 | Which outside AI developers rent the compute: one extract says Fortune named Anthropic, Google, Grok and X; a second search couldn't find that Fortune line | N/A | | | search extract | **U: check E2 before naming any customer** |

## 3. The bill and the borrowing

| # | Fact | Source | Status |
|---|---|---|---|
| 20 | **Musk said on X (26 Oct)** SpaceX had "closed" about $40B of mostly callable debt for GPUs, arriving in H1 2027, and warned that more than 200 "neocloud" AI-compute firms could fail or consolidate | N4 | V (that he said it) |
| 21 | **The 8-K says something more conditional:** on 24 Oct SpaceX signed a binding commitment letter for a master finance lease with an entity managed by Apollo Global Management, which would buy GPU pods and lease them to SpaceX; principal payments expected to total about $40B; it may not close "on the anticipated terms or timeline, or at all" | N4 (quoting E3) | V (two outlets); **copy the wording from E3** |
| 22 | Earlier reports: ~$10B bank loans + ~$30B investment-grade debt, through a special-purpose vehicle to keep it off the balance sheet (Bloomberg); Goldman Sachs leading talks | N4 | U |

## 4. How it got here (2026)

| # | Fact | Source | Status |
|---|---|---|---|
| 30 | xAI (Grok's maker) merged into SpaceX in February 2026; X came with it | N6, Wikipedia "SpaceXAI" | U (terms not found) |
| 31 | IPO: Nasdaq, ticker SPCX, first trade 12 Jun 2026; reported target ~$1.75T and a raise of up to $75B; one source: priced $135, first-day close $161, ~$2.1T | N7 | V (date, ticker), U (prices) |
| 32 | Cursor (Anysphere) bought for a stated $60B, all stock; announced 16 Jun 2026, closed mid-August; ~$2.6B annualised revenue at the time (Reuters) | N6, N3 | V (price, structure), U (close date) |
| 33 | 2025 revenue $18.67B per the prospectus figure quoted by one compiler (it may include xAI and X after the merger) | search extract (E4) | **U: check E4** |
| 34 | Musk owns about 48% of SpaceX and controls about 82% of the votes through Class B shares (Barclays note as reported) | N5 | U |

## 5. The Tesla merger talk

| # | Fact | Source | Status |
|---|---|---|---|
| 40 | Musk on SpaceX's earnings call: "a lot of merit" to combining; both companies have special committees; no terms agreed; not guaranteed | N5 | V |
| 41 | Barclays (26 Oct) raised Tesla to Overweight, target $450 (from $370), calling a SpaceX deal "now a key part of the bull case"; it assumes an all-stock offer of about 3.1 SpaceX shares per Tesla share at a 20% premium. **An analyst's assumption, not a proposal** | N5 | V (the note), the terms are Barclays' |
| 42 | Musk: approval would need holders of 50% of Tesla's outstanding shares, not just a majority of votes cast | N5 | U |
| 43 | Tesla rose about 5-6% on the day | N5 | V |

## 6. Rockets and satellites (for the launch chapter; recheck before use)

| # | Fact | Source | Status |
|---|---|---|---|
| 50 | 100th Falcon 9 flight of 2026 on 23 Aug; pace ~155 for the year | N8 | U |
| 51 | Starlink satellites in orbit ~10,800 active, ~11,100 total (Oct 2026) | N8 | U |
| 52 | Most-flown booster: B1067, 36th flight on 9 Jul 2026 (may be beaten since) | N8 | U |
| 53 | Starship Flight 15 aims to catch both the booster and, for the first time, the ship; no date (NET ~7-21 Nov) | radar 27 Oct | V (plan), date U |

## 7. OUR MATHS (label on screen)

| # | Sum | Result |
|---|---|---|
| 60 | Launch share of Q3 revenue: 1.77 / 14.6 | **about 12%**: rockets are now SpaceX's smallest business |
| 61 | AI share: 7.56 / 14.6 | **about 52%**, more than half |
| 62 | Starlink share: 5.25 / 14.6 | **about 36%** |
| 63 | Starlink operating margin: 2.37 / 5.25 | **about 45%**: the profit engine |
| 64 | AI operating margin: 0.431 / 7.56 | **about 6%** |
| 65 | Capex against revenue in the quarter: 19.6 / 14.6 | **about 1.3x**: it spent more than it took in |
| 66 | AI revenue growth: 7.56 / 0.813 | **about 9x in a year** |
| 67 | AI against Starlink + rockets: 7.56 vs 5.25 + 1.77 = 7.02 | **AI revenue is bigger than the other two combined** (Q3 only; in operating profit Starlink leads, row 63) |

## 8. Hooks (film: thumbnail promise on screen by 0:08)

| # | Line 1 | Frame 0 |
|---|---|---|
| H1 | "SpaceX now brings in more from AI than from its rockets and Starlink put together." (revenue, not profit: row 67) | A booster catch, then three bars: AI 7.56, Starlink 5.25, rockets 1.77 ($B, Q3) |
| H2 | "Elon Musk says SpaceX closed a forty-billion-dollar loan; its own filing calls it a commitment." | The X post beside the 8-K line (H4 formula: authority says vs document says) |
| H3 | "Rockets are now SpaceX's smallest business, and last quarter they lost money." | Falcon landing, "12%" |

Title options (≤ 50 chars): "How SpaceX Really Makes Money (It's Not Rockets)" (48) · "SpaceX's Biggest Business Isn't Rockets" (39).

## 9. Do not claim

- That the $40B is "closed" debt as fact: Musk says closed; the 8-K says a binding commitment to a finance lease that may not close (rows 20-21). Show both.
- Named compute customers (Anthropic, Google) until E2 names them (row 13).
- A merger as agreed, or Barclays' 3.1 ratio as an offer (rows 40-41).
- Anthropic's draft-filing numbers as SpaceX facts; never mix the two companies' figures.
- "SpaceX is profitable" without the quarter: one quarter, after a capex bill larger than revenue (rows 2-3, 65).
- 2025 revenue or IPO prices before checking E4 (rows 31, 33).
- Any launch or satellite count from row 50-52 without a fresh check on the day.
