# VERIFY: pilot 01, "Why $87,000 Feels Like Less"

Checked 8 Oct 2026 by the writer. **This is the writer's own check, not the independent one.** CRAFT section 5 requires a
separate checker who has not seen the script's reasoning to re-verify every on-screen claim before render. Not yet done.

Status key: **CONFIRMED** = the figure is on the page named. **DERIVED** = our arithmetic from confirmed inputs, sum shown.
**SOFT** = secondary source, a rounding judgement, or not on a page I opened.

How pages were read: official pages were fetched and read through a summarising tool, and data series were downloaded
as CSV from FRED (which republishes BLS, BEA, Census, Freddie Mac, EIA and Federal Reserve series). The Michigan table
was read from the university's own PDF. A human should click each CONFIRMED link once before upload.

## Title and thesis (CRAFT, 6 Oct lesson: check the title as a claim)

| Claim | Figure | Source | Date of data | Status |
|---|---|---|---|---|
| "$87,000" is a record income | $87,460, highest since 1967 | https://www.census.gov/library/stories/2026/09/median-household-income.html | 2025 | CONFIRMED |
| It "feels like less" | Sentiment 48.1; real hourly earnings -0.3% over the year | https://www.sca.isr.umich.edu/ and https://www.bls.gov/news.release/realer.htm | Sep 2026; Aug 2026 | CONFIRMED (the feeling is the survey's, the wording is ours) |
| "Feels Like a Pay Cut" (POST title option) | Real average hourly earnings -0.3%, Aug 2025 to Aug 2026 | https://www.bls.gov/news.release/realer.htm | Aug 2026 | CONFIRMED for hourly pay. Real average *weekly* earnings were +0.3%, so the title is true of the hourly measure only |

## Open, credit side

| Claim | Figure | Source | Date of data | Status |
|---|---|---|---|---|
| Median household income, record | $87,460, margin of error ±$1,040, highest on record since 1967 | census.gov story above | 2025 (published 15 Sep 2026) | CONFIRMED |
| Up on the year, inflation-adjusted | +2.6% from $85,210 | same; and https://www.census.gov/library/publications/2026/demo/p60-289.html | 2024 to 2025 | CONFIRMED |
| 2024 not statistically different from 2019 | wording | census.gov story | 2024 vs 2019 | CONFIRMED |
| 2019 level | $85,320 in 2025 dollars | https://fred.stlouisfed.org/series/MEHOINUSA672N | 2019 | CONFIRMED on FRED; the Census story gives no 2019 dollar figure |
| Six-year gain | +2.5% | 87,460 / 85,320 = 1.0251 | 2019 to 2025 | DERIVED |
| "All of it arrived in the final twelve months" | 2024 ($85,210) is below 2019 ($85,320) | FRED series above | 2019, 2024, 2025 | DERIVED |
| Post-tax median, not a record | $76,060 (±$712) | census.gov story | 2025 | CONFIRMED |
| Release date 15 Sep (timeline) | page "last revised September 15, 2026"; news conference announced for 15 Sep | census.gov P60-289 page and search result for the Census advisory | Sep 2026 | CONFIRMED (date read from page metadata and the advisory) |

## The mood

| Claim | Figure | Source | Date of data | Status |
|---|---|---|---|---|
| Sentiment, September final | 48.1 (August 51.7) | https://www.sca.isr.umich.edu/ and https://www.sca.isr.umich.edu/files/tbmics.pdf | Sep 2026 | CONFIRMED |
| Survey since 1952 | table begins November 1952 | tbmics.pdf | n/a | CONFIRMED |
| Five index questions | the five questions as listed on screen (paraphrased, shortened) | https://data.sca.isr.umich.edu/fetchdoc.php?docid=24770 | n/a | CONFIRMED (on-screen wording is our shortening) |
| January 2020 | 99.8 | tbmics.pdf | Jan 2020 | CONFIRMED |
| "Less than half" | 48.1 / 99.8 = 0.482 | | | DERIVED |
| Crisis low | 55.3, November 2008 | tbmics.pdf | Nov 2008 | CONFIRMED |
| Lowest before 2022 | 51.7, May 1980 | tbmics.pdf, sorted all 677 readings | May 1980 | DERIVED (sort of the table) |
| "Lower than anything in the twentieth century" | no reading before 2022 is below 51.7 | tbmics.pdf | | DERIVED |
| All-time low | 44.8, May 2026; previous low 50.0, June 2022 | tbmics.pdf | May 2026 | DERIVED (lowest of 677 readings; the university page itself was not seen calling it a record) |
| Hsu quote | "Views of current and year-ahead expected personal finances both weakened about 10% this month" | https://www.sca.isr.umich.edu/ | Sep 2026 | CONFIRMED |

## The race, the basket, the level

| Claim | Figure | Source | Date of data | Status |
|---|---|---|---|---|
| CPI-U all items, not seasonally adjusted | 257.971 (Jan 2020), 334.980 (Aug 2026) | https://www.bls.gov/regions/mid-atlantic/data/consumerpriceindexhistorical_us_table.htm | Jan 2020, Aug 2026 | CONFIRMED |
| Prices since Jan 2020 | +29.9% | 334.980 / 257.971 = 1.2985 | | DERIVED |
| $100 basket now | $129.85 | 100 x 1.2985 | | DERIVED |
| Average hourly earnings, private | $28.43 (Jan 2020), $37.76 (Aug 2026), $37.81 (Sep 2026) | https://fred.stlouisfed.org/series/CES0500000003 ; Sep also at https://www.bls.gov/news.release/empsit.nr0.htm | as stated | CONFIRMED. Note: the 11 Sep Real Earnings release printed August as $37.75; FRED shows $37.76 after the 2 Oct revision |
| Pay since Jan 2020 | +32.8% | 37.76 / 28.43 = 1.3282 | | DERIVED |
| Pay ahead of prices | about 2% | 1.3282 / 1.2985 = 1.0229 | | DERIVED. Mixes a seasonally adjusted wage with an unadjusted price index; with the adjusted CPI (259.127 to 334.131, +28.9%) the lead is about 3%. "Roughly two percent" is the cautious end |
| Rent | +33.1% | CUSR0000SEHA: 337.591 to 449.321 | Jan 2020 to Aug 2026 | DERIVED |
| Food at home | +32.0% | CUSR0000SAF11: 243.511 to 321.335 | same | DERIVED |
| Food away from home | +37.6% | CUSR0000SEFV: 289.137 to 397.868 | same | DERIVED |
| Electricity | +43.0% | CUSR0000SEHF01: 213.531 to 305.444 | same | DERIVED |
| Gasoline | +42.4% | CUSR0000SETB01: 242.397 to 345.169 | same | DERIVED |
| New vehicles | +21.2% | CUSR0000SETA01: 147.877 to 179.259 | same | DERIVED |
| Medical care services | +18.3% | CUSR0000SAM2: 552.331 to 653.532 | same | DERIVED |
| "Won on things most households buy rarely" | interpretation of the two rows above | | | SOFT (author's reading; medical services are not rare for every household) |
| Food at home, past year | +2.2% | https://www.bls.gov/news.release/archives/cpi_09112026.htm | 12 months to Aug 2026 | CONFIRMED |
| Stantcheva: prices seen as rising faster than wages | 80% of respondents | https://www.brookings.edu/articles/why-do-we-dislike-inflation/ | surveys Dec 2023 to Jan 2024 | CONFIRMED |
| Stantcheva: raises credited to performance, not inflation | wording | same | same | CONFIRMED |
| "Achievement / theft" | our characterisation | | | SOFT (ours, not hers; never shown as a quote) |

All component indexes are at https://fred.stlouisfed.org/series/ followed by the id (BLS data, seasonally adjusted).

## The price of money, two streets

| Claim | Figure | Source | Date of data | Status |
|---|---|---|---|---|
| CPI leaves out house purchase and mortgage interest | BLS quote on screen | https://www.bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm | page modified 13 Feb 2026 | CONFIRMED (re-read the quote character by character before render) |
| 30-year fixed rate now | 7.40% (week ago 7.28%, year ago 6.30%) | https://www.freddiemac.com/pmms | 8 Oct 2026 | CONFIRMED |
| Rate at start of 2020 | 3.72% | https://fred.stlouisfed.org/series/MORTGAGE30US | 2 Jan 2020 | CONFIRMED |
| Low of the decade | 2.65% | same | 7 Jan 2021 | CONFIRMED as the lowest since 2019. It is widely reported as the all-time low but I only checked 2019 onward, so the script says "of the decade" |
| "Highest since November 2023" | last reading at or above 7.40% was 7.44% on 16 Nov 2023 | same | | DERIVED |
| Median new house sold | $329,000 (Q1 2020), $410,700 (Q2 2026) | https://fred.stlouisfed.org/series/MSPUS (Census/HUD) | as stated | CONFIRMED. These are new houses; the script says "new house" |
| House price rise | +24.8%, "about a quarter", "roughly $80,000" | 410,700 / 329,000; 410,700 - 329,000 = 81,700 | | DERIVED |
| Payment in early 2020 | $1,214 a month | 80% of $329,000 = $263,200; 30 years at 3.72% | | DERIVED |
| Payment now | $2,275 a month | 80% of $410,700 = $328,560; 30 years at 7.40% | | DERIVED. Mixes a Q2 2026 price with an October 2026 rate; principal and interest only |
| Payment rise | +87% | 2,275 / 1,214 = 1.874 | | DERIVED |
| Credit card rate, all accounts | 15.09% (Feb 2020); 21.19% (Aug 2026, preliminary) | https://fred.stlouisfed.org/series/TERMCBCCALLNS and https://www.federalreserve.gov/releases/g19/current/ | as stated | CONFIRMED. August is preliminary and said so in the line |
| Interest on $5,000 for a year | about $755 and about $1,060; "about $300 higher" | 5,000 x 0.1509 = 754.5; 5,000 x 0.2119 = 1,059.5 | | DERIVED (simple interest, illustration only) |
| NBER paper: borrowing costs explain most of the 2023 gap | "almost three quarters" | https://www.nber.org/papers/w32163 | Feb 2024 | CONFIRMED (abstract) |
| Summers is a former Treasury Secretary | background fact | not on the page opened | | SOFT (public record; add a link or drop the description) |
| Mortgages below 4% | 19.2% + 29.9% = 49.1% | https://wolfstreet.com/2026/10/02/homeowners-are-clinging-to-their-below-4-mortgages-for-dear-life-as-mortgage-rates-went-over-7/ | Q2 2026 | **SOFT**: secondary. FHFA's dashboard would not load. Hedged in the line and on screen |
| Mortgages at 6% or more | 22.5% | same | Q2 2026 | **SOFT**, same reason |
| $300,000 at 3% and at 7.40% | $1,265 and $2,077; gap $812 | 30-year amortisation | | DERIVED (illustration; 3% is a round figure, not a quoted average) |
| Household debt service ratio | 11.73% (Q4 2019), 11.11% (Q2 2026) | https://fred.stlouisfed.org/series/TDSP | as stated | CONFIRMED |
| "Half the borrowers are sheltered" | rests on the 49.1% above | | | SOFT |

## The cushion

| Claim | Figure | Source | Date of data | Status |
|---|---|---|---|---|
| Saving rate | 4.1% | https://bea.gov/news/2026/personal-income-and-outlays-august-2026 | Aug 2026 | CONFIRMED. Released with the annual update; values from Jan 2021 were revised |
| 2019 average | 7.3% | mean of 12 monthly values, https://fred.stlouisfed.org/series/PSAVERT | 2019 | DERIVED |
| "Lowest since November 2022" | Nov 2022 = 4.0%; nothing lower until Aug 2026 | same | | DERIVED |
| Spending and income in August | +0.9% and +0.2% | BEA release | Aug 2026 | CONFIRMED (personal income +0.2%; disposable income +0.3%) |
| Total household debt | $18.771 trillion | https://www.newyorkfed.org/newsevents/news/research/2026/20260811 | Q2 2026 | CONFIRMED |
| Credit card balances | $1.263 trillion, +$54 billion on the year | same | Q2 2026 | CONFIRMED |
| Cards flowing into serious delinquency | 6.97% (annualised) | same | Q2 2026 | CONFIRMED |
| Scally quote | as on screen; the "held steady over the past two years" half is paraphrased in narration | same | 11 Aug 2026 | CONFIRMED |
| Doing okay or living comfortably | 73% (78% in 2021) | https://www.federalreserve.gov/newsevents/pressreleases/other20260513a.htm | survey Oct 2025 | CONFIRMED |
| Could cover $400 with cash | 63% | same | survey Oct 2025 | CONFIRMED |

## This year, the median

| Claim | Figure | Source | Date of data | Status |
|---|---|---|---|---|
| Middle East conflict disrupted Hormuz shipments this spring | wording | https://www.eia.gov/pressroom/releases/press590.php | release 7 Jul 2026 | CONFIRMED in outline (the release refers to the conflict, the strait and an April 2026 price peak). "Fuel prices jumped" is supported by the gasoline rows below |
| Regular gasoline | $3.124 (6 Oct 2025), $4.354 (5 Oct 2026) | https://fred.stlouisfed.org/series/GASREGW (EIA) | as stated | CONFIRMED |
| EIA's July forecast for the second half | about $3.60 a gallon | EIA release above | 7 Jul 2026 | CONFIRMED |
| Energy and all items, past year | +16.3% and +3.4% | BLS CPI release | 12 months to Aug 2026 | CONFIRMED |
| Fed raised rates | +0.25 point to 3.75%-4%, vote 12-0, "Inflation remains elevated." | https://federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm | 16 Sep 2026 | CONFIRMED |
| Mortgage rate up more than a point in a year | 6.30% to 7.40% | Freddie Mac PMMS | 8 Oct 2026 | CONFIRMED |
| Jobs | +29,000 in September; July revised to -10,000 | https://www.bls.gov/news.release/empsit.nr0.htm | Sep 2026 (released 2 Oct) | CONFIRMED. First print; will be revised |
| "Hiring has almost stopped" | our reading of +29,000 | | | SOFT (judgement; BLS says employment "changed little") |
| Unemployment | 4.2% | same | Sep 2026 | CONFIRMED |
| Pay over the year | +3.0% | same | year to Sep 2026 | CONFIRMED |
| Real average hourly earnings | -0.3% | https://www.bls.gov/news.release/realer.htm | Aug 2025 to Aug 2026 | CONFIRMED |
| 10th percentile unchanged, 90th +1.7%, third straight rise at the 90th | wording and figure | census.gov story and P60-289 page | 2025 | CONFIRMED |
| 90/10 ratio | 9.23 (1967), 13.06 (2025) | census.gov story | as stated | CONFIRMED |
| "Mortgage rate roughly doubled" (verdict) | 7.40 / 3.72 = 1.99 | | | DERIVED |

## Removed or hedged because it could not be confirmed

- **NAR median existing-home price ($429,100, Aug 2026):** NAR's own page did not show the price. Removed; the house sum uses Census/HUD new-house prices instead.
- **Share of mortgages by rate band:** only seen via Wolf Street. Kept, but attributed and hedged in two lines and on screen. Replace with FHFA's own table or cut the two beats.
- **"Record low" mortgage rate of 2.65%:** changed to "low point of the decade".
- **"When inflation was running in double digits" (May 1980):** removed; no source opened.
- **"Sentiment below the 1st percentile" and "lowest in four months":** from secondary coverage; not used.
- **Motor vehicle insurance since 2020:** the series would not download; not used.
- **Fed "responded" to energy prices, and mortgage rates "followed" the Fed:** causal wording removed; the statement does not mention energy.
- **Renewed tanker attacks in late July, Brent prices:** secondary only; not used.

## Things that will go stale

- Mortgage rate and pump price: weekly. Re-pull on the day of voicing.
- Michigan preliminary October reading: due 9 Oct 2026. If it sets a new low, the open and the timeline change.
- CPI for September and real earnings: due mid-October. The "-0.3%" and "+3.4%" lines must be re-checked.
- Jobs figure: revised with each monthly release.
