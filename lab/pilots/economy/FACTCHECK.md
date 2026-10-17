# FACTCHECK: pilot 01, "Why $87,000 Feels Like Less"

Independent check, 9 Oct 2026 (sources pulled 8 Oct 23:10 UTC to 9 Oct 00:15 UTC). The checker did not write the script
and did not rely on VERIFY.md except for URLs.

**Verdict: VOICE AFTER LISTED FIXES.** The unambiguous fixes are already applied to `script.py` (list at the end). No
figure on screen was wrong and all four quotes are verbatim. What had to change was framing (jobs, household debt, real
pay, one wrong date label), one secondary source that is now replaced by the primary, and wording that would go stale.
Three dated releases land before a mid-October upload and need a re-pull (section "Stale by mid-October").

How sources were read: FRED CSVs downloaded with curl and recomputed in Python; Census, Michigan (page and both PDFs),
NY Fed, BEA, Federal Reserve (G.19, SHED, FOMC), EIA, NBER, Brookings, Freddie Mac and Wolf Street pages downloaded and
read as raw text; FHFA's own data file downloaded and read. **BLS pages block direct download**, so the four BLS pages
(CPI release, Employment Situation, Real Earnings, OER factsheet) were read through a fetch tool that returns quoted
text; every BLS number was also cross-checked against the FRED copy of the series.

Counts (91 rows): CORRECT 77 (6 of them also STALE-RISK) · MISLEADING 9 (8 fixed, 1 left as note N1) · WRONG 2 (both
fixed: a date label, and a hedge this check made untrue) · UNSUPPORTED 0 (2 secondary-sourced rows upgraded to primary)
· STALE-RISK 9 (3 reworded, 6 dated lines that need a re-pull on voicing day) · quotes 4 of 4 verbatim.

## 1. Claim table

Beat ids are chapter.beat (1-based). "Sum" = recomputed here.

### Open, credit side

| Beat | Script says | Source says (URL, date of data) | Verdict | Replacement wording |
|---|---|---|---|---|
| open.1 | Typical household earned more in 2025 than any year on record; $87,460; highest since 1967 | "U.S. real median household income was $87,460 in 2025, up 2.6% from the previous year and the highest on record since 1967". census.gov/library/stories/2026/09/median-household-income.html, dated 15 Sep 2026 | CORRECT | none |
| open.2 | Sentiment fell close to its lowest level ever; 48.1, Sep 2026 | Final Sep 2026 = 48.1, Aug 51.7 (sca.isr.umich.edu front page; tbmics.pdf). Sorted all 677 readings: 44.8 (May 2026), then 48.1. Second-lowest ever | CORRECT | none |
| open.3 | RECORD HIGH / NEAR RECORD LOW | as above | CORRECT | none |
| open.4 | 48.1 is lower than anything in the twentieth century | Lowest reading before 2001 is 51.7 (May 1980), tbmics.pdf | CORRECT | none |
| credit.2 | Median = household exactly in the middle | Census: "the midpoint where half of households have higher income, and half have lower income" | CORRECT | none |
| credit.3 | A little under $87,500 before tax; MOE ±$1,040 | "$87,460 (±$1,040)", Census story. Money income is pre-tax | CORRECT | none |
| credit.4 | +2.6% on the year, already inflation-adjusted | "up 2.6%", "All estimates here are adjusted for inflation". Sum: 87,460 / 85,210 = 1.0264. P60-289 page: adjusted with C-CPI-U | CORRECT | none |
| credit.5 | Series since 1967, no year higher | "highest on record dating back to 1967 (Table 2)", P60-289 page. FRED MEHOINUSA672N max = 2025 (FRED only starts 1984) | CORRECT | none |
| credit.6 | 2024 not statistically different from 2019; $85,320 / $85,210 | "The median household income estimate of $85,210 for 2024 was not statistically different from the estimate in 2019". 2019 = 85,320 on FRED MEHOINUSA672N (2025 C-CPI-U dollars) | CORRECT | none |
| credit.7 | +2.5% across six years, all in the last twelve months | Sum: 87,460 / 85,320 = 1.0251. 2024 (85,210) is below 2019 (85,320). Census: 2025 "was higher than in both 2019 and 2024" | CORRECT | none |
| credit.8 | After tax $76,060, not a record | "Post-tax median household income was $76,060 (±$712) in 2025, up 3.1% from $73,760 in 2024 but not a record high." | CORRECT | none |
| credit.9 | The 2.5% "is going to look very small beside a mortgage payment" | 2.5% is a REAL (inflation-adjusted) gain; the +87% payment figure later is NOMINAL. Not like for like. The later card correctly uses nominal pay (+33%) | MISLEADING (fixed) | "Keep that two and a half percent in mind. It is measured after inflation, and in a few minutes we come to a cost that the inflation figures leave out." |

### The mood

| Beat | Script says | Source says | Verdict | Replacement |
|---|---|---|---|---|
| mood.1 | Michigan has asked since 1952 | Index table begins November 1952 (tbmics.pdf) | CORRECT | none |
| mood.2 | Five questions, as listed | Five index questions x1 to x5 (data.sca.isr.umich.edu/fetchdoc.php?docid=24770). On-screen wording is a fair shortening | CORRECT | none |
| mood.3 | 99.8 in January 2020 | 99.8 (tbmics.pdf; FRED UMCSENT). February 2020 was 101.0, so January is not a flattering base | CORRECT | none |
| mood.4 | 48.1 is less than half | Sum: 48.1 / 99.8 = 0.482 | CORRECT | none |
| mood.5 | Crisis low 55.3, November 2008 | 55.3 (tbmics.pdf) | CORRECT | none |
| mood.6 | 51.7 in May 1980, lowest before 2022 | 51.7; no lower reading until June 2022 (50.0) | CORRECT | none |
| mood.7 | All-time low 44.8 in May 2026; timeline values | 44.8 May 2026; 50.0 Jun 2022; 55.3 Nov 2008; 51.7 May 1980; 48.1 Sep 2026 (tbmics.pdf) | CORRECT | none |
| mood.8 QUOTE | "Views of current and year-ahead expected personal finances both weakened about 10% this month" · Joanne Hsu · Director · September 2026 | Front page, under "Surveys of Consumers Director Joanne Hsu": "...Views of current and year-ahead expected personal finances both weakened about 10% this month, with concerns over high prices continuing to climb." Character match; the quote is the opening clause of a longer sentence | CORRECT | none. The page will be overwritten by the October text on 9 Oct, so keep a dated copy |

### The race, the basket, the level

| Beat | Script says | Source says | Verdict | Replacement |
|---|---|---|---|---|
| race.2 | Prices +29.9%, Jan 2020 to Aug 2026 | CPI-U all items NSA 257.971 to 334.980 (FRED CPIAUCNS). Sum: 1.2985 | CORRECT | none |
| race.3 | $100 basket now $129.85 | 100 × 1.2985 | CORRECT | none |
| race.4 | Hourly pay $28.43 to $37.76 | FRED CES0500000003 (all private employees, SA): 28.43, 37.76. The 11 Sep Real Earnings release printed 37.75; 37.76 is the 2 Oct revision | CORRECT | none |
| race.5 | +32.8%, pay won | Sum: 37.76 / 28.43 = 1.3282 | CORRECT, label tightened | card now reads "ALL PRIVATE EMPLOYEES" |
| race.6 | Margin "roughly two percent"; card 1.328 ÷ 1.299 | Mixed series: SA wage ÷ NSA prices = 1.0229. Like for like: NSA wage (CEU0500000003 28.56 to 37.79, +32.3%) ÷ NSA CPI = 1.019; SA wage ÷ SA CPI (CPIAUCSL 259.127 to 334.131, +28.9%) = 1.030. The honest answer is a range | MISLEADING, mild (fixed) | "between two and three percent"; card "2–3%" |
| race.7 | "An average worker is a little better off on paper" | Average hourly earnings is a mean across all jobs, not a tracked worker. Production and nonsupervisory workers (FRED AHETPI) went 23.91 to 32.53, +36.1%, a lead of about 5% | CORRECT, see note N1 | optional, see N1 |
| basket.2 | Rent +33.1% | CUSR0000SEHA 337.591 to 449.321. Sum 1.3310 | CORRECT | none |
| basket.3 | Food at home +32.0% | CUSR0000SAF11 243.511 to 321.335. Sum 1.3196 | CORRECT | none |
| basket.4 | Food away +37.6% | CUSR0000SEFV 289.137 to 397.868. Sum 1.3761 | CORRECT | none |
| basket.5 | Electricity +43.0%, gasoline +42.4% | CUSR0000SEHF01 213.531 to 305.444 (1.4304); CUSR0000SETB01 242.397 to 345.169 (1.4240). A February 2020 base would give gasoline +49.7%, so January is the cautious base | CORRECT | none |
| basket.6 | New vehicles +21.2%, medical care services +18.3% | CUSR0000SETA01 147.877 to 179.259 (1.2122); CUSR0000SAM2 552.331 to 653.532 (1.1832) | CORRECT | none |
| basket.7 | The ranked list | all eight match the rows above | CORRECT | none |
| basket.8 | Pay tied or lost on weekly and monthly bills, won on things bought rarely | Holds on the all-employee measure (pay 32.8 vs rent 33.1, groceries 32.0). Medical services are not a rare purchase for many households. On the production-worker measure (+36.1%) pay beat rent and groceries | MISLEADING, mild (left, note N1) | see N1 |
| level.2 | Food at home +2.2% in the year to August | "The food at home index rose 2.2 percent over the 12 months ending in August." BLS CPI release, 11 Sep 2026. FRED CUUR0000SAF11: +2.19% | CORRECT | none |
| level.3 | Still 32% above 2020 | as basket.3 | CORRECT | none |
| level.5 | Harvard economist Stefanie Stantcheva; Brookings Papers 2024 | brookings.edu/articles/why-do-we-dislike-inflation/: "Stefanie Stantcheva of Harvard University" | CORRECT | none |
| level.6 | 80% believe prices systematically rise faster than wages | "80% of respondents to recent surveys she conducted believe prices systematically increase faster than wages" | CORRECT | none |
| level.7 | Raises credited to performance or career progress | "people tend to attribute it to job performance or career progression rather than an adjustment for inflation" | CORRECT | none. "I EARNED IT / IT WAS DONE TO ME" is the script's own gloss; it is not in a quote card, keep it that way |
| level.8 | 33% raise vs 30% price rise | 32.8 and 29.9 | CORRECT | none |

### The price of money, two streets

| Beat | Script says | Source says | Verdict | Replacement |
|---|---|---|---|---|
| money.2 QUOTE | "Spending to purchase and improve houses and other housing units is treated as investment and not consumption in the CPI." · BLS · CPI factsheet | Same sentence returned verbatim from bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm (last modified 13 Feb 2026). The next sentence on the page begins "Interest costs (such as mortgage interest), property taxes, real estate fees...", which supports "mortgage interest is left out" | CORRECT (read through a fetch tool, BLS blocks direct download; one human click advised) | none |
| money.3 | 3.72% on 2 Jan 2020 | FRED MORTGAGE30US 2020-01-02 = 3.72 | CORRECT | none |
| money.4 | 2.65% on 7 Jan 2021, low of the decade | 2.65; it is also the lowest in the whole series back to 1971 | CORRECT | none |
| money.5 | 7.40% on 8 Oct 2026, highest since November 2023 | Freddie Mac PMMS: "averaged 7.40% as of October 8, 2026, up from last week when it averaged 7.28%. A year ago at this time, the 30-year FRM averaged 6.30%." Last reading at or above 7.40 was 7.44 on 16 Nov 2023 | CORRECT · STALE-RISK | dated wording survives. If the 15 Oct print is higher, "highest since November 2023" may need a new month |
| money.6 | Median new house $329,000 in Q1 2020 | FRED MSPUS (Census/HUD, new houses) 2020Q1 = 329,000 | CORRECT | none |
| money.7 | $1,214 a month | 80% × 329,000 = 263,200; 360 payments at 3.72% = $1,214.44 | CORRECT | none |
| money.8 | $410,700 in Q2 2026, about $80,000 more, +25% | 410,700; difference 81,700; 1.2483 | CORRECT | none |
| money.9 | "At this week's rate" $2,275 | 80% × 410,700 = 328,560 at 7.40% = $2,274.88. Mixes a Q2 price with an October rate (disclosed on the card) | STALE-RISK (fixed) | "At that October rate, ..." |
| money.10 | Payment +87%; price +25%; pay +33% | 2,274.88 / 1,214.44 = 1.873 | CORRECT | none |
| money.11 | Card rate 15.09% (Feb 2020), 21.19% (Aug 2026, preliminary) | FRED TERMCBCCALLNS 2020-02 = 15.09; G.19 released 7 Oct 2026, credit card plans, all accounts, latest = 21.19. Context not in the script: it was 21.39 a year earlier and peaked at 21.76 in Aug 2024 | CORRECT | none |
| money.12 | ≈$755 vs ≈$1,060, about $300 more | 5,000 × 0.1509 = 754.50; × 0.2119 = 1,059.50; gap 305 | CORRECT | none |
| money.13 | Four economists incl. former Treasury Secretary Summers, 2024 | NBER w32163: Bolhuis, Cramer, Schulz, Summers (2024). Summers was Treasury Secretary 1999 to 2001 (public record, not on the page) | CORRECT | none |
| money.14 | Their measure accounts for almost three quarters of the 2023 sentiment gap | Abstract: "can account for almost three quarters of the gap in US consumer sentiment in 2023" | CORRECT | none |
| streets.2 | ≈49% of mortgages below 4%, "reported by the site Wolf Street" | **Now confirmed in FHFA's own file** (fhfa.gov/data/nmdb, outstanding mortgage statistics, national, all mortgages, 2026Q2, file dated 24 Sep 2026): below 3% 19.2%, 3 to 4% 29.9%. Sum 49.1% (shares of loans) | CORRECT, attribution fixed | "According to the Federal Housing Finance Agency, about forty-nine percent..." |
| streets.3 | 22.5% at 6% or more | FHFA same file: PCT_INTRATE_GE_6 = 22.5 | CORRECT, attribution fixed | card now credits FHFA |
| streets.4 | "Those shares come from a secondary report... treat them as approximate" | No longer true: the primary file matches to the decimal | WRONG after this check (fixed) | "Across every outstanding mortgage in that database, the average rate was four point four percent, far below the rate on a new loan." (FHFA AVE_INTRATE 2026Q2 = 4.4) |
| streets.6 | $300,000 at 3% = $1,265 | $1,264.81 | CORRECT | none |
| streets.7 | Same sum "today" at 7.40% = $2,077 | $2,077.14 | STALE-RISK (fixed) | "borrows the same sum at this October's rate" |
| streets.8 | Gap $812 | 2,077.14 − 1,264.81 = 812.33 | CORRECT | none |
| streets.9 | Debt service ratio 11.73% (Q4 2019), 11.11% (Q2 2026) | FRED TDSP 11.7277, 11.1114 | CORRECT | none |
| streets.10 | "Half the borrowers are sheltered" | 49.1% of mortgages are below 4% (FHFA). It is the script's inference that this explains the calm average | CORRECT as opinion | none |

### The cushion

| Beat | Script says | Source says | Verdict | Replacement |
|---|---|---|---|---|
| cushion.2 | Saving rate 4.1% in August | BEA, 30 Sep 2026: "the personal saving rate... was 4.1 percent" | CORRECT | none |
| cushion.3 | 2019 average 7.3%; lowest since Nov 2022 | FRED PSAVERT: 2019 mean 7.31; Nov 2022 = 4.0, nothing at or below 4.1 since | CORRECT | none |
| cushion.4 | Spending +0.9%, income +0.2% | BEA: personal income "0.2 percent", PCE "0.9 percent" (disposable income +0.3). Both nominal | CORRECT | none |
| cushion.5 | "The difference comes from borrowing. Household debt stood at $18.77 trillion" | NY Fed, 11 Aug 2026. Headline: "Household Debt Balances Decreased Slightly". "total household debt decreased by $13 billion, a 0.1% decrease, in Q2 2026, to $18.8 trillion". Year on year +$383bn (+2.1%), below 3.4% inflation. The figure is right; the implication that total borrowing is climbing is not | MISLEADING (fixed) | "...can come from is borrowing. Household debt stood at eighteen point eight trillion dollars in the second quarter, a touch lower than three months before." Card adds "DOWN $13 BILLION ON THE QUARTER" |
| cushion.6 | Card balances $1.263tn, +$54bn in a year | Table: Credit Card Debt, annual change (+) $54, total $1.263. Sum: +4.5% on the year | CORRECT, link word changed | "Credit card balances, though, kept climbing, to about one and a quarter trillion dollars." |
| cushion.7 | 6.97% of card balances becoming 90+ days late, annual rate | Table "Flow into Serious Delinquency": Credit Card Debt Q2 2026 6.97% (6.93% a year earlier); rates are annualised | CORRECT | none |
| cushion.8 QUOTE | "new delinquencies for auto loans and credit cards remain at elevated levels, a trend we'll continue to monitor." · Joelle Scally · 11 August 2026 | "“Delinquency rates across most products have held steady over the past two years,” said Joelle Scally... “Still, new delinquencies for auto loans and credit cards remain at elevated levels, a trend we’ll continue to monitor.”" Character match (source uses a curly apostrophe). Narration dropped "across most products" | CORRECT quote · narration hedge added | "...delinquency rates across most products have held steady for two years..." |
| cushion.9 | 73% doing at least okay; 78% in 2021; survey Oct 2025 | Fed, 13 May 2026: "73 percent of adults reported either doing okay or living comfortably financially... below the overall high of 78 percent in 2021"; "fielded in October 2025" | CORRECT | none |
| cushion.10 | 63% could cover $400 with cash | "The share who would cover a $400 emergency expense using cash or its equivalent also remained unchanged from 2024 at 63 percent." | CORRECT | none |

### This year, the median, the verdict

| Beat | Script says | Source says | Verdict | Replacement |
|---|---|---|---|---|
| year.1 | Mood card labelled "OCTOBER 2026" | The mood figure used throughout is the SEPTEMBER 2026 final (48.1). No October reading existed when written | WRONG label (fixed) | "SEPTEMBER 2026" |
| year.2 | "This spring" a Middle East conflict disrupted Hormuz shipments and fuel jumped | EIA, 7 Jul 2026: "June 18 memorandum of understanding (MOU) between the United States and Iran to end a months-long conflict and reopen the strait". Michigan: "February before the Iran conflict began". EIA weekly regular gasoline: $3.015 on 2 Mar, $3.502 on 9 Mar, peak $4.50 on 11 May. The jump began in early March | MISLEADING, mild (fixed) | "Earlier this year, ..." |
| year.3 | $3.12 on 6 Oct 2025; $4.35 on 5 Oct 2026 | FRED GASREGW (EIA): 3.124; 4.354 | CORRECT · STALE-RISK | dated, survives |
| year.4 | EIA's July forecast: about $3.60 for the second half; "actual on 5 Oct $4.35" | "averaging about $3.60 per gallon (gal) in the second half of this year, down from $4.48/gal in May". The forecast is a six-month AVERAGE; the script set it against one week. Average of the 14 weekly readings 6 Jul to 5 Oct = $4.13. The script also never said the strait reopened in June (price fell to $3.78 on 6 Jul, then rose again) | MISLEADING, mild (fixed) | "In July, after the strait had reopened, the government's own energy forecasters expected..." Card: "AVERAGE SINCE JULY $4.13 · ON 5 OCT $4.35" |
| year.5 | Energy +16.3%, all items +3.4%, year to August | BLS CPI release 11 Sep 2026: "The index for energy increased 16.3 percent over the past 12 months."; "the all items index increased 3.4 percent before seasonal adjustment". FRED CPIAUCNS: +3.40% | CORRECT · STALE-RISK | September CPI is out 14 Oct |
| year.6 QUOTE | Fed raised a quarter point on 16 Sep, 12 to 0; "Inflation remains elevated." | "decided to raise the target range for the federal funds rate by 1/4 percentage point to 3-3/4 to 4 percent"; "by a 12 – 0 vote"; "Inflation remains elevated." Verbatim, a full sentence. The same statement also says "Economic activity is expanding at a solid pace" and "Job gains have kept pace with the workforce" | CORRECT | none |
| year.7 | Mortgage 6.30% a year ago, 7.40% on 8 Oct | PMMS as above; FRED 2025-10-09 = 6.30. Sum +1.10 points | CORRECT · STALE-RISK | dated, survives |
| year.8 | "Hiring has almost stopped." +29,000 in September; July revised to a loss | BLS, 2 Oct 2026: "Both nonfarm payroll employment (+29,000) and the unemployment rate (4.2 percent) changed little in September"; July revised from +21,000 to −10,000; **August revised to +133,000**. Three-month average +51,000; twelve-month gain 496,000 (FRED PAYEMS). The Fed's own statement says job gains kept pace with the workforce. The script showed the two weak months and left out the strong one between them | MISLEADING (fixed) | "Meanwhile hiring has been weak." Card adds "AUGUST +133,000" |
| year.9 | Unemployment 4.2% | BLS release; FRED UNRATE Sep 2026 = 4.2 | CORRECT | none |
| year.10 | Pay +3.0% (year to Sep) vs prices +3.4% (year to Aug) | BLS: average hourly earnings "$37.81", up 3.0 percent over 12 months. Sum 37.81 / 36.70 = 1.0302. Periods differ by a month (labelled on the card). Like for like in August: 37.76 / 36.62 = +3.1% vs +3.4%. The line holds either way | CORRECT · STALE-RISK | re-check after 14 Oct CPI |
| year.11 | Real average hourly earnings −0.3%, Aug 2025 to Aug 2026 | BLS Real Earnings, 11 Sep 2026: "From August 2025 to August 2026, real average hourly earnings decreased 0.3 percent, seasonally adjusted." The same paragraph reports "a 0.3-percent increase in real average weekly earnings over this period". Production workers: hourly −0.1%, weekly +0.1% | MISLEADING by omission (fixed) | adds "...although slightly longer hours left the weekly pay packet a little ahead." Card adds "REAL WEEKLY EARNINGS +0.3%" |
| year.12 | Timeline: May 44.8; 11 Sep 3.4% and −0.3%; 15 Sep record; 16 Sep Fed; 2 Oct +29,000; 8 Oct 7.40% | all dates and values match the releases above | CORRECT | none |
| median.2 | Half of households earned "less than eighty-seven thousand" | The median is $87,460, so strictly a little under half earned less than $87,000 | CORRECT with "about" (fixed) | "less than about eighty-seven thousand dollars" |
| median.3 | 10th percentile no significant change; 90th +1.7% | P60-289 page: "Household income increased 1.7 percent at the 90th percentile but did not significantly change at the 10th percentile between 2024 and 2025" | CORRECT | none |
| median.4 | 90th percentile up for the third year running | "third consecutive year-over-year increase in both pre- and post-tax income at the 90th percentile" | CORRECT | none |
| median.5 | Ratio 9.23 in 1967, 13.06 in 2025 | "widened from 9.23 in 1967 to 13.06 in 2025". Census adds that 1967 comparisons are not tested for significance | CORRECT | none |
| verdict.2 | Pay outran prices "by about two percent"; credit list | as race.6; 4.2%; 73% | MISLEADING, mild (fixed) | "by two to three percent" |
| verdict.3 | Debit list incl. mortgage 3.72 to 7.40 "roughly doubled", card 15 to 21, saving 7.3 to 4.1, "REAL HOURLY PAY −0.3% THIS YEAR" | 7.40 / 3.72 = 1.99. "This year" reads as year to date; the figure is Aug 2025 to Aug 2026 | CORRECT, label fixed | "REAL HOURLY PAY −0.3% IN THE YEAR TO AUGUST" |
| verdict.4-5 | Record is true, low mood is rational; "the mood counts this month" | opinion, labelled "my verdict". "This month" is loose: the reading is September's | CORRECT as opinion · STALE-RISK | leave, or "the mood counts right now" |
| verdict.6 | Real hourly earnings "is currently negative" | True of August, the latest release. September real earnings are out 14 Oct | STALE-RISK (fixed) | "...which was negative over the year to August." |
| verdict.9 | $87,460 / 48.1 | as above | CORRECT | none |
| TITLE | "WHY $87,000 FEELS LIKE LESS" | $87,460 is a record (Census); sentiment 48.1 (Michigan). The title makes no pay-cut claim | CORRECT | none. Do NOT use the alternate "Feels Like a Pay Cut": real weekly earnings are +0.3% and pay is 2 to 3% ahead of prices since 2020 |

## 2. Required edits, in order of severity

All of 1 to 9 are applied. 10 and 11 need a decision or a re-pull.

1. **Jobs framing (year.8).** "Hiring has almost stopped" beside only the two weak months. August was +133,000. Applied.
2. **Real pay omission (year.11, verdict.6, verdict.3).** Hourly −0.3% shown, weekly +0.3% in the same BLS paragraph left out. Applied.
3. **Household debt implication (cushion.5-6).** Total debt fell on the quarter; only cards were climbing. Applied.
4. **Wrong date label (year.1).** "OCTOBER 2026" on a September reading. Applied.
5. **Secondary source replaced (streets.2-4).** FHFA's own file confirms 49.1% and 22.5%; the "treat as approximate" beat was replaced with FHFA's 4.4% average rate so the beat count holds. Applied.
6. **Real vs nominal tease (credit.9).** Applied.
7. **Mixed seasonal adjustment in the pay lead (race.6, verdict.2).** Now "between two and three percent". Applied.
8. **Gasoline forecast comparison and the reopened strait (year.2, year.4).** Applied.
9. **Stale wording (money.9, streets.7) and small hedges (cushion.8, median.2, race.5 label).** Applied.
10. **N1, the pay measure (race.7, basket.8). Not applied, needs the writer.** The whole basket chapter rests on all-employee average hourly earnings (+32.8%). For production and nonsupervisory workers, about four in five private jobs, BLS shows +36.1% (FRED AHETPI 23.91 to 32.53), which beats rent and groceries. One sentence would cover it, for example after race.7: "For workers outside management the official rise is nearer thirty-six percent, so this is the cautious figure." Also "things most households buy rarely" does not fit medical services.
11. **Re-pull on voicing day** (next section).

## 3. Stale by mid-October 2026

| Item | Next release | Lines affected | How to word it to survive |
|---|---|---|---|
| Michigan preliminary October | 9 Oct, 10am ET (not out at check time) | open.2-4, mood.4, mood.7, year.1, verdict.9 | Lines say "In September" and "This September", which survive. If October prints below 44.8, mood.7 "all-time low was set this May" becomes wrong: change to "The low before this autumn..." or update the timeline |
| CPI, September | 14 Oct, 8:30am ET | race.2-6, all basket figures, level.2, year.5, year.10 | Every card carries "AUG 2026", which survives. Keep "By August of this year" in speech |
| Real Earnings, September | 14 Oct | year.11, year.12, verdict.3, verdict.6 | Now worded "over the year to August". If September turns positive, the last third of the film needs a rewrite, not a patch |
| Freddie Mac weekly rate | 15 Oct, then weekly | money.5, money.9, streets.7, year.7, year.12, verdict.3 | Always "On the eighth of October". "Highest since November 2023" holds unless a later week passes 7.44 |
| EIA weekly gasoline | 13 Oct, then weekly | year.3, year.4 | Always "On the fifth of October" |
| Jobs | 6 Nov (September and August revised) | year.8, year.12 | Say "the first estimate for September" if voicing after 6 Nov |
| BEA income and outlays, September | late Oct | cushion.2-4 | "In August" survives |

## 4. Could not settle

- **BLS pages were not read as raw HTML** (bot block). Figures agree with FRED and the quote came back verbatim, but one human click on the OER factsheet quote is still worth doing.
- **G.19 "preliminary" flag for August 21.19%.** The value is on the 7 Oct release; the "p" marker was not separately located in the table text. Latest-month G.19 figures are preliminary as a rule.
- **"Summers, former Treasury Secretary"** is public record, not on the NBER page.
- **Why gasoline rose again from late July to $4.48 in September** after the June reopening. No primary source opened. The script does not state a cause; keep it that way.
- **Whether the 2019 to 2025 gain (+2.5%) is itself statistically significant.** Census says 2025 "was higher than in both 2019 and 2024", which supports it; the test statistic was not seen.
- **N1** above is a judgement call for the writer.

## 5. Edits applied to script.py (before → after)

Loads after edits; beat count 115, unchanged.

1. Docstring: "hiring near zero, real hourly pay falling again." → "weak hiring, real hourly pay down over the year to August." plus a line pointing here.
2. Docstring source: Wolf Street "SECONDARY" entry → FHFA National Mortgage Database entry with the Q2 2026 figures and URL.
3. credit.9: "Keep that two and a half percent in mind, because in a few minutes it is going to look very small beside a mortgage payment." → "Keep that two and a half percent in mind. It is measured after inflation, and in a few minutes we come to a cost that the inflation figures leave out."
4. race.5 card: "AVERAGE HOURLY EARNINGS · JAN 2020 → AUG 2026" → "AVERAGE HOURLY EARNINGS · ALL PRIVATE EMPLOYEES · JAN 2020 → AUG 2026"
5. race.6: "is roughly two percent" → "is between two and three percent"
6. race.6 card: "≈ 2%" / "... · 1.328 ÷ 1.299" → "2–3%" / "... · 1.328 ÷ 1.299 = 1.02 · SEASONALLY ADJUSTED 1.03"
7. money.9: "At this week's rate, the same kind of loan..." → "At that October rate, the same kind of loan..."
8. streets.2: "According to federal housing data reported by the site Wolf Street, about forty-nine percent..." → "According to the Federal Housing Finance Agency, about forty-nine percent..."
9. streets.2 card: "FHFA DATA VIA WOLF STREET" → "FHFA NATIONAL MORTGAGE DATABASE"
10. streets.3 card: same change.
11. streets.4: "Those shares come from a secondary report rather than the agency's own tables, so treat them as approximate." → "Across every outstanding mortgage in that database, the average rate was four point four percent, far below the rate on a new loan."
12. streets.7: "The other borrows the same sum today, and pays..." → "The other borrows the same sum at this October's rate, and pays..."
13. cushion.5: "The second place the difference comes from is borrowing. Household debt stood at eighteen point eight trillion dollars in the second quarter." → "The second place the difference can come from is borrowing. Household debt stood at eighteen point eight trillion dollars in the second quarter, a touch lower than three months before."
14. cushion.5 card: "TOTAL HOUSEHOLD DEBT · Q2 2026 · NEW YORK FED" → "TOTAL HOUSEHOLD DEBT · Q2 2026 · DOWN $13 BILLION ON THE QUARTER · NEW YORK FED"
15. cushion.6: "Credit card balances alone reached about one and a quarter trillion dollars." → "Credit card balances, though, kept climbing, to about one and a quarter trillion dollars."
16. cushion.8: "delinquency rates have held steady for two years" → "delinquency rates across most products have held steady for two years"
17. year.1 card: "OCTOBER 2026" → "SEPTEMBER 2026"
18. year.2: "This spring, a conflict..." → "Earlier this year, a conflict..."
19. year.4: "In July, the government's own energy forecasters..." → "In July, after the strait had reopened, the government's own energy forecasters..."
20. year.4 card: "ACTUAL ON 5 OCT: $4.35" → "AVERAGE SINCE JULY $4.13 · ON 5 OCT $4.35"
21. year.8: "Meanwhile hiring has almost stopped." → "Meanwhile hiring has been weak."
22. year.8 card: "JULY REVISED TO −10,000 · BLS" → "JULY REVISED TO −10,000 · AUGUST +133,000 · BLS"
23. year.11: "...less in August than it had a year before." → "...less in August than it had a year before, although slightly longer hours left the weekly pay packet a little ahead."
24. year.11 card: "AUG 2025 → AUG 2026 · BLS" → "AUG 2025 → AUG 2026 · REAL WEEKLY EARNINGS +0.3% · BLS"
25. median.2: "less than eighty-seven thousand dollars" → "less than about eighty-seven thousand dollars"
26. verdict.2: "by about two percent" → "by two to three percent"
27. verdict.3 list: "REAL HOURLY PAY −0.3% THIS YEAR" → "REAL HOURLY PAY −0.3% IN THE YEAR TO AUGUST"
28. verdict.6: "real hourly earnings, which is currently negative." → "real hourly earnings, which was negative over the year to August."

Side effects to check before render: edits 6, 14, 20, 22 and 24 lengthen card captions (check they fit); edits 13 and 23 make two long sentences (run `script_lint.py`); VERIFY.md still describes the Wolf Street rows as SOFT and was not touched.
