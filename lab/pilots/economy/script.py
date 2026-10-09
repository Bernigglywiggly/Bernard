"""THE HOUSEHOLD LEDGER · PILOT 01 · WHY $87,000 FEELS LIKE LESS (written 8 Oct 2026).
The typical US household earned a record $87,460 in 2025 (Census, 15 Sep 2026). In the same month the Michigan
sentiment index fell to 48.1, lower than any reading before 2022. Both numbers are right. The film closes the gap in
five entries: (1) since January 2020 pay beat prices by about two points, (2) but tied or lost on rent, groceries,
power and fuel, (3) the price level never came back, (4) the cost of borrowing is not in the CPI, and it roughly
doubled, (5) 2026 itself: an oil shock, a rate rise, weak hiring, real hourly pay down over the year to August.
Independently fact-checked 9 Oct 2026: see FACTCHECK.md (edits applied are listed at its end).
Shape: a ledger (credit side, debit side, verdict). Not the seven-chapter How They Profit template.

Sources (every one opened 8 Oct 2026; date of the data in brackets):
- Census Bureau, "Median Household Income in 2025 Surpassed Previous Highs..." [2025 income, published 15 Sep 2026]
  https://www.census.gov/library/stories/2026/09/median-household-income.html
- Census Bureau, Income in the United States: 2025 (P60-289) [2025; inflation-adjusted with C-CPI-U]
  https://www.census.gov/library/publications/2026/demo/p60-289.html
- FRED MEHOINUSA672N, real median household income, Census data [2019 = $85,320 in 2025 dollars]
  https://fred.stlouisfed.org/series/MEHOINUSA672N
- University of Michigan Surveys of Consumers, front page and index table [Sep 2026 final 48.1; table dated 23 Sep 2026]
  https://www.sca.isr.umich.edu/  ·  https://www.sca.isr.umich.edu/files/tbmics.pdf
- BLS, Consumer Price Index, August 2026 [released 11 Sep 2026]
  https://www.bls.gov/news.release/archives/cpi_09112026.htm
- BLS, CPI-U historical table, all items, not seasonally adjusted [Jan 2020 = 257.971, Aug 2026 = 334.980]
  https://www.bls.gov/regions/mid-atlantic/data/consumerpriceindexhistorical_us_table.htm
- FRED copies of BLS CPI component indexes, seasonally adjusted [Jan 2020 and Aug 2026]: food at home CUSR0000SAF11,
  shelter CUSR0000SAH1, rent CUSR0000SEHA, electricity CUSR0000SEHF01, gasoline CUSR0000SETB01, food away
  CUSR0000SEFV, new vehicles CUSR0000SETA01, medical care services CUSR0000SAM2
  https://fred.stlouisfed.org/series/CUSR0000SAF11 (and the same path with each id)
- BLS, Employment Situation, September 2026 [released 2 Oct 2026]  https://www.bls.gov/news.release/empsit.nr0.htm
- FRED CES0500000003, BLS average hourly earnings, private [Jan 2020 $28.43, Aug 2026 $37.76, Sep 2026 $37.81]
  https://fred.stlouisfed.org/series/CES0500000003
- BLS, Real Earnings, August 2026 [released 11 Sep 2026]  https://www.bls.gov/news.release/realer.htm
- BLS factsheet, "Owners' equivalent rent and rent" [page modified 13 Feb 2026]
  https://www.bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm
- Bolhuis, Cramer, Schulz and Summers, "The Cost of Money is Part of the Cost of Living", NBER w32163 [Feb 2024]
  https://www.nber.org/papers/w32163
- Freddie Mac Primary Mortgage Market Survey [8 Oct 2026: 7.40%; year ago 6.30%]  https://www.freddiemac.com/pmms
  and its weekly history, FRED MORTGAGE30US [2 Jan 2020 3.72%; 7 Jan 2021 2.65%; 16 Nov 2023 7.44%]
  https://fred.stlouisfed.org/series/MORTGAGE30US
- FRED MSPUS, Census/HUD median sales price of new houses sold [Q1 2020 $329,000; Q2 2026 $410,700]
  https://fred.stlouisfed.org/series/MSPUS
- Federal Reserve G.19 Consumer Credit [released 7 Oct 2026; August 2026 preliminary]
  https://www.federalreserve.gov/releases/g19/current/  and FRED TERMCBCCALLNS [Feb 2020 15.09%]
  https://fred.stlouisfed.org/series/TERMCBCCALLNS
- FRED TDSP, Federal Reserve household debt service ratio [Q4 2019 11.73%; Q2 2026 11.11%]
  https://fred.stlouisfed.org/series/TDSP
- FHFA National Mortgage Database, Outstanding Residential Mortgage Statistics, national, all mortgages [Q2 2026:
  below 3% 19.2%, 3-4% 29.9%, 6% or more 22.5%, average rate 4.4%; shares of loans; file dated 24 Sep 2026]
  https://www.fhfa.gov/data/nmdb  (nmdb-outstanding-mortgage-statistics-national-census-areas-quarterly.zip)
  First seen via Wolf Street, 2 Oct 2026; the figures match FHFA's own file.
- New York Fed, Household Debt and Credit, Q2 2026 [released 11 Aug 2026]
  https://www.newyorkfed.org/newsevents/news/research/2026/20260811
- BEA, Personal Income and Outlays, August 2026 [released 30 Sep 2026; annual update, revised back to Jan 2021]
  https://bea.gov/news/2026/personal-income-and-outlays-august-2026  and FRED PSAVERT (2019 average, Nov 2022)
  https://fred.stlouisfed.org/series/PSAVERT
- Federal Reserve, Economic Well-Being of U.S. Households in 2025 [survey Oct 2025; released 13 May 2026]
  https://www.federalreserve.gov/newsevents/pressreleases/other20260513a.htm
- EIA weekly US regular gasoline price, FRED GASREGW [5 Oct 2026 $4.354; 6 Oct 2025 $3.124]
  https://fred.stlouisfed.org/series/GASREGW
- EIA press release, 7 Jul 2026, July Short-Term Energy Outlook  https://www.eia.gov/pressroom/releases/press590.php
- Federal Reserve, FOMC statement [16 Sep 2026]  https://federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- Michigan index questions (the five questions) https://data.sca.isr.umich.edu/fetchdoc.php?docid=24770
- Stefanie Stantcheva, "Why Do We Dislike Inflation?", Brookings Papers on Economic Activity [surveys Dec 2023 to
  Jan 2024; article 27 Mar 2024]  https://www.brookings.edu/articles/why-do-we-dislike-inflation/
Derived figures (the sums) and anything soft are in VERIFY.md. Visuals as in ../../curvelf/lf02_price/script.py.
"""
TITLE = "WHY $87,000 FEELS LIKE LESS"
TAG = "THE HOUSEHOLD LEDGER  ·  WHY $87,000 FEELS LIKE LESS"
NAME = "economy_pilot01"
FIX = {}

CHAPTERS = [
    dict(id="open", title="", beats=[
        ("In September, the Census Bureau reported that the typical American household earned more last year than in any year on record.",
         ("num", "$87,460", "MEDIAN HOUSEHOLD INCOME, 2025 · CENSUS BUREAU · HIGHEST SINCE RECORDS BEGAN IN 1967")),
        ("In the same month, a long-running survey of how those households feel about money fell close to its lowest level ever.",
         ("num", "48.1", "INDEX OF CONSUMER SENTIMENT · SEPTEMBER 2026 · UNIVERSITY OF MICHIGAN")),
        ("Both numbers are accurate, and your household is living somewhere in the gap between them.",
         ("split", ("RECORD HIGH", "WHAT HOUSEHOLDS EARN"), ("NEAR RECORD LOW", "HOW HOUSEHOLDS FEEL"))),
        ("The survey reading, forty-eight point one, is lower than anything it recorded in the entire twentieth century.", ("img", "e01")),
        ("This film goes through that gap one entry at a time, like a ledger, using only figures you can check for yourself.",
         ("img", "e02")),
        ("By the end you should be able to say which of those two numbers describes your own kitchen table.", ("img", "e03")),
    ]),
    dict(id="credit", title="THE CREDIT SIDE", beats=[
        ("We begin with the good news, because it is real and it deserves a fair hearing.", ("img", "e04")),
        ("Median household income means the household exactly in the middle, with half the country above it and half below.",
         ("words", "THE HOUSEHOLD IN THE MIDDLE")),
        ("Last year that household brought in a little under eighty-seven and a half thousand dollars before tax.",
         ("num", "$87,460", "BEFORE TAX · 2025 · MARGIN OF ERROR ±$1,040")),
        ("That was two point six percent more than the year before, and the figure is already adjusted for inflation.",
         ("num", "+2.6%", "REAL MEDIAN HOUSEHOLD INCOME · 2024 → 2025 · CENSUS")),
        ("The Census Bureau has kept this series since 1967, and no year in it comes out higher.", ("img", "e05")),
        ("There is a catch in the small print, though. The 2024 figure was not statistically different from 2019.",
         ("split", ("$85,320", "2019 · IN 2025 DOLLARS"), ("$85,210", "2024 · IN 2025 DOLLARS"))),
        ("So across six years, the typical household gained about two and a half percent, and all of it arrived in the final twelve months.",
         ("num", "+2.5%", "2019 → 2025 · SIX YEARS · $85,320 → $87,460")),
        ("After taxes, the picture is slightly cooler. Median income was seventy-six thousand and sixty dollars, which is not a record.",
         ("num", "$76,060", "MEDIAN HOUSEHOLD INCOME AFTER TAX · 2025 · NOT A RECORD · CENSUS")),
        ("Keep that two and a half percent in mind. It is measured after inflation, and in a few minutes we come to a cost that the inflation figures leave out.",
         ("img", "e06")),
    ]),
    dict(id="mood", title="THE MOOD", beats=[
        ("Now the other number. Since 1952, researchers at the University of Michigan have put a short set of questions to American households.",
         ("img", "e07")),
        ("There are five of them, covering whether you are better off than a year ago, what you expect next, and whether it is a good time for major purchases.",
         ("list", ["BETTER OR WORSE OFF THAN A YEAR AGO?", "BETTER OR WORSE OFF A YEAR FROM NOW?", "GOOD OR BAD TIMES IN THE NEXT 12 MONTHS?", "GOOD OR BAD TIMES OVER 5 YEARS?", "A GOOD TIME TO BUY MAJOR HOUSEHOLD ITEMS?"], "THE FIVE QUESTIONS")),
        ("Just before the pandemic began, the index stood at ninety-nine point eight.",
         ("num", "99.8", "INDEX OF CONSUMER SENTIMENT · JANUARY 2020")),
        ("This September it was forty-eight point one, which is less than half the earlier figure.",
         ("split", ("99.8", "JANUARY 2020"), ("48.1", "SEPTEMBER 2026"))),
        ("For comparison, the worst month of the financial crisis, late in 2008, came in above fifty-five.",
         ("num", "55.3", "NOVEMBER 2008 · THE LOW OF THE FINANCIAL CRISIS")),
        ("The lowest reading before this decade came in May 1980, at just under fifty-two.",
         ("num", "51.7", "MAY 1980 · THE LOWEST READING BEFORE 2022")),
        ("The all-time low was set this May, at forty-four point eight.",
         ("tl", [("MAY 1980", "51.7"), ("NOV 2008", "55.3"), ("JUN 2022", "50.0"), ("MAY 2026", "44.8 · RECORD LOW"), ("SEP 2026", "48.1")])),
        ("The survey's director, Joanne Hsu, wrote that views of personal finances, both current and expected, weakened about ten percent in a single month.",
         ("quote", "Views of current and year-ahead expected personal finances both weakened about 10% this month", "JOANNE HSU · DIRECTOR, SURVEYS OF CONSUMERS · SEPTEMBER 2026")),
        ("A record on one side and a near-record on the other is not something a rounding error produces, so the next step is to follow the money.",
         ("img", "e08")),
    ]),
    dict(id="race", title="THE RACE", beats=[
        ("The simplest test is a race between two lines, prices and pay, both starting in January 2020.", ("img", "e09")),
        ("By August of this year, the Consumer Price Index had risen just under thirty percent.",
         ("num", "+29.9%", "CONSUMER PRICES · JAN 2020 → AUG 2026 · BLS CPI-U")),
        ("Put plainly, a basket of goods that cost a hundred dollars back then now costs about thirty dollars more.",
         ("split", ("$100", "JANUARY 2020"), ("$129.85", "THE SAME BASKET · AUGUST 2026"))),
        ("Over the same period, average hourly pay in the private sector went from about twenty-eight dollars and forty cents to nearly thirty-eight dollars.",
         ("split", ("$28.43", "AVERAGE HOURLY PAY · JAN 2020"), ("$37.76", "AUGUST 2026 · BLS"))),
        ("That is a rise of nearly thirty-three percent, so on the official scoreboard, pay won.",
         ("num", "+32.8%", "AVERAGE HOURLY EARNINGS · ALL PRIVATE EMPLOYEES · JAN 2020 → AUG 2026")),
        ("The margin of victory, however, is only two or three percent.",
         ("num", "2–3%", "HOW FAR PAY FINISHED AHEAD OF PRICES · 1.328 ÷ 1.299 = 1.02 · SEASONALLY ADJUSTED 1.03")),
        ("An average worker is therefore a little better off on paper, and that is an honest result which this channel will not hide. For workers outside management the official rise is nearer thirty-six percent, so this is the cautious figure.",
         ("img", "e10")),
        ("The trouble starts when you ask what, exactly, is inside the basket.", ("words", "WHAT IS IN THE BASKET?")),
    ]),
    dict(id="basket", title="THE BASKET", beats=[
        ("The price index is an average of hundreds of things, and nobody buys the average.", ("img", "e11")),
        ("Take rent first. Since January 2020 it has risen thirty-three percent, almost exactly matching pay.",
         ("num", "+33.1%", "RENT OF PRIMARY RESIDENCE · JAN 2020 → AUG 2026 · BLS")),
        ("Groceries, which the Bureau of Labor Statistics calls food at home, are up thirty-two percent.",
         ("num", "+32.0%", "FOOD AT HOME · JAN 2020 → AUG 2026")),
        ("A meal out is up nearly thirty-eight percent.", ("num", "+37.6%", "FOOD AWAY FROM HOME · JAN 2020 → AUG 2026")),
        ("Electricity has climbed forty-three percent, and gasoline about forty-two.",
         ("split", ("+43.0%", "ELECTRICITY"), ("+42.4%", "GASOLINE · JAN 2020 → AUG 2026"))),
        ("So where did pay actually pull ahead? Largely in categories such as new cars, up twenty-one percent, and medical services, up eighteen.",
         ("split", ("+21.2%", "NEW VEHICLES"), ("+18.3%", "MEDICAL CARE SERVICES"))),
        ("Set those against a pay rise of thirty-three percent, and a pattern appears.",
         ("list", ["ELECTRICITY +43%", "GASOLINE +42%", "EATING OUT +38%", "RENT +33%", "PAY +33%", "GROCERIES +32%", "NEW CARS +21%", "MEDICAL SERVICES +18%"], "SINCE JANUARY 2020")),
        ("Pay tied or lost on the bills that arrive every week or every month, and it won on things most households buy rarely.",
         ("img", "e12")),
        ("My reading is that this alone explains a good part of the mood, because people judge the economy by the purchases they repeat.",
         ("words", "PEOPLE JUDGE BY WHAT THEY REPEAT")),
        ("There is a second effect layered on top, and it concerns the difference between a rate and a level.", ("img", "e13")),
    ]),
    dict(id="level", title="THE LEVEL", beats=[
        ("When officials say inflation has come down, they mean prices are rising more slowly, which is different from prices falling.",
         ("img", "e14")),
        ("Grocery prices rose two point two percent over the past year, which sounds entirely normal.",
         ("num", "+2.2%", "FOOD AT HOME · 12 MONTHS TO AUGUST 2026 · BLS")),
        ("They are still thirty-two percent above where they stood in 2020, and nothing in the data suggests they are going back.",
         ("split", ("+2.2%", "THE RATE · PAST YEAR"), ("+32.0%", "THE LEVEL · SINCE 2020"))),
        ("Economists watch the rate, while shoppers remember the level, and both groups are describing the same receipt.",
         ("img", "e15")),
        ("The Harvard economist Stefanie Stantcheva surveyed Americans about this, and found something that I think is the key to the whole puzzle.",
         ("img", "e16", "\"WHY DO WE DISLIKE INFLATION?\" · BROOKINGS PAPERS · 2024")),
        ("Eighty percent of her respondents believed that prices systematically rise faster than wages.",
         ("num", "80%", "BELIEVE PRICES RISE FASTER THAN WAGES · STANTCHEVA, 2024")),
        ("When people did receive a raise, they tended to credit their own performance or career progress rather than an adjustment for inflation.",
         ("split", ("I EARNED IT", "HOW A RAISE FEELS"), ("IT WAS DONE TO ME", "HOW A PRICE RISE FEELS"))),
        ("Under that psychology, a thirty-three percent raise and a thirty percent price rise do not cancel out. One feels like an achievement and the other feels like a theft.",
         ("img", "e17")),
        ("Even so, psychology is only part of the answer, because one of the largest cost increases of this decade is missing from the price index altogether.",
         ("words", "THE COST THAT ISN'T IN THE INDEX")),
    ]),
    dict(id="money", title="THE PRICE OF MONEY", beats=[
        ("The Consumer Price Index measures what things cost. It does not measure what it costs to borrow the money to buy them.",
         ("img", "e18")),
        ("The Bureau of Labor Statistics says so directly. Buying a house is treated as an investment, and mortgage interest is left out.",
         ("quote", "Spending to purchase and improve houses and other housing units is treated as investment and not consumption in the CPI.", "BUREAU OF LABOR STATISTICS · CPI FACTSHEET")),
        ("At the very start of this decade, the average thirty-year mortgage rate was just under three and three quarters percent.",
         ("num", "3.72%", "30-YEAR FIXED MORTGAGE · 2 JAN 2020 · FREDDIE MAC")),
        ("A year later it touched its low point of the decade, at just over two and a half percent.",
         ("num", "2.65%", "7 JAN 2021 · THE LOW OF THE 2020s · FREDDIE MAC")),
        ("On the eighth of October this year it was seven point four percent. That is the highest since November 2023.",
         ("num", "7.40%", "30-YEAR FIXED MORTGAGE · 8 OCT 2026 · FREDDIE MAC")),
        ("Here is what that does to a real purchase. Early in that first year, the median new house sold for just under a third of a million dollars.",
         ("num", "$329,000", "MEDIAN NEW HOUSE SOLD · Q1 2020 · CENSUS / HUD")),
        ("With a fifth paid up front, the loan cost about twelve hundred and fourteen dollars a month in principal and interest.",
         ("num", "$1,214", "A MONTH · 20% DOWN · 30 YEARS AT 3.72% · OUR SUM")),
        ("By the spring of this year the median new house cost roughly eighty thousand dollars more, a rise of about a quarter.",
         ("num", "$410,700", "MEDIAN NEW HOUSE SOLD · Q2 2026 · +25% · CENSUS / HUD")),
        ("At that October rate, the same kind of loan costs nearly twenty-three hundred dollars a month.",
         ("split", ("$1,214", "A MONTH · EARLY 2020"), ("$2,275", "A MONTH · OCTOBER 2026"))),
        ("The price of the house rose by a quarter, yet the monthly payment rose by eighty-seven percent, before taxes and insurance.",
         ("num", "+87%", "THE MONTHLY PAYMENT · PAY ROSE 33% · THIS COST IS NOT IN THE CPI")),
        ("Credit cards tell a similar story. The average rate was about fifteen percent before the pandemic, and the Federal Reserve's preliminary August figure is above twenty-one.",
         ("split", ("15.09%", "CREDIT CARD RATE · FEB 2020"), ("21.19%", "AUGUST 2026 · PRELIMINARY · FED G.19"))),
        ("Suppose you carry a balance of five thousand dollars for a year. The interest bill is now about three hundred dollars higher than it was.",
         ("split", ("≈ $755", "A YEAR ON $5,000 · AT 15.09%"), ("≈ $1,060", "AT 21.19% · SIMPLE INTEREST"))),
        ("In 2024, four economists including the former Treasury Secretary Lawrence Summers argued that this omission explains much of the gloom.",
         ("img", "e19", "\"THE COST OF MONEY IS PART OF THE COST OF LIVING\" · NBER, 2024")),
        ("When they added borrowing costs back into inflation, their measure accounted for almost three quarters of the gap in sentiment in 2023.",
         ("num", "≈ ¾", "OF THE 2023 SENTIMENT GAP EXPLAINED · BOLHUIS, CRAMER, SCHULZ, SUMMERS")),
        ("Which raises an awkward question. If borrowing has become this expensive, why do so many households seem untouched by it?",
         ("img", "e20")),
    ]),
    dict(id="streets", title="TWO STREETS", beats=[
        ("The answer is that the cost of money landed on some households and missed others almost completely.", ("img", "e21")),
        ("According to the Federal Housing Finance Agency, about forty-nine percent of outstanding mortgages still carry a rate below four percent.",
         ("num", "≈ 49%", "OF MORTGAGES BELOW 4% · Q2 2026 · FHFA NATIONAL MORTGAGE DATABASE")),
        ("Roughly twenty-two percent, by the same count, are at six percent or higher.",
         ("num", "22.5%", "OF MORTGAGES AT 6% OR MORE · Q2 2026 · FHFA NATIONAL MORTGAGE DATABASE")),
        ("Across every outstanding mortgage in that database, the average rate was four point four percent, far below the rate on a new loan.", ("img", "e22")),
        ("Now picture two families on the same street, in the same kind of house, with the same income.", ("img", "e23")),
        ("One took out a large loan when rates were near their lowest. At three percent, the monthly payment is a little under thirteen hundred dollars.",
         ("num", "$1,265", "A MONTH · $300,000 AT 3% · PRINCIPAL AND INTEREST")),
        ("The other borrows the same sum at this October's rate, and pays nearly twenty-one hundred.",
         ("split", ("$1,265", "BORROWED AT 3%"), ("$2,077", "BORROWED AT 7.40%"))),
        ("That is a difference of more than eight hundred dollars every month, for an identical house, and no income statistic will ever show it.",
         ("num", "$812", "A MONTH · THE GAP BETWEEN TWO IDENTICAL LOANS")),
        ("It also explains a figure that looks reassuring. The Federal Reserve's measure of household debt payments as a share of income is lower now than in late 2019.",
         ("split", ("11.73%", "DEBT PAYMENTS ÷ INCOME · Q4 2019"), ("11.11%", "Q2 2026 · FEDERAL RESERVE"))),
        ("The national average is calm because half the borrowers are sheltered, while the renter and the first-time buyer face the full price.",
         ("img", "e24")),
        ("So far this has been a story about six years. The last part of the ledger is about how much room households have left.",
         ("words", "HOW MUCH ROOM IS LEFT?")),
    ]),
    dict(id="cushion", title="THE CUSHION", beats=[
        ("When costs rise faster than pay, the difference has to come from somewhere, and the first place is savings.", ("img", "e25")),
        ("In August, Americans saved four point one percent of their after-tax income, according to the Bureau of Economic Analysis.",
         ("num", "4.1%", "PERSONAL SAVING RATE · AUGUST 2026 · BEA")),
        ("Across the last full year before the pandemic, on the same series, the average was above seven percent.",
         ("split", ("7.3%", "SAVING RATE · 2019 AVERAGE"), ("4.1%", "AUGUST 2026 · LOWEST SINCE NOV 2022"))),
        ("In that single month, spending grew by nine tenths of a percent while income grew by two tenths.",
         ("split", ("+0.9%", "SPENDING · AUGUST"), ("+0.2%", "INCOME · AUGUST · BEA"))),
        ("The second place the difference can come from is borrowing. In the spring quarter, household debt stood at about eighteen point eight trillion dollars, a touch lower than the quarter before.",
         ("num", "$18.77 TRILLION", "TOTAL HOUSEHOLD DEBT · Q2 2026 · DOWN $13 BILLION ON THE QUARTER · NEW YORK FED")),
        ("Credit card balances, though, kept climbing, to about one and a quarter trillion dollars. That is fifty-four billion more than a year earlier.",
         ("num", "$1.263 TRILLION", "CREDIT CARD BALANCES · +$54 BILLION IN A YEAR · NEW YORK FED")),
        ("About seven percent of card balances are sliding into serious delinquency each year, meaning ninety days or more behind.",
         ("num", "6.97%", "CARD BALANCES BECOMING 90+ DAYS LATE · ANNUAL RATE · Q2 2026")),
        ("Joelle Scally of the New York Fed noted that delinquency rates across most products have held steady for two years, but that new delinquencies on car loans and cards remain elevated.",
         ("quote", "new delinquencies for auto loans and credit cards remain at elevated levels, a trend we'll continue to monitor.", "JOELLE SCALLY · NEW YORK FED · 11 AUGUST 2026")),
        ("It would be wrong to call this a collapse. In the Federal Reserve's own household survey, seventy-three percent of adults said they were doing at least okay.",
         ("num", "73%", "DOING OKAY OR LIVING COMFORTABLY · FED SURVEY, OCT 2025 · 78% IN 2021")),
        ("The same survey asked about a four hundred dollar emergency. Only sixty-three percent said they could cover it with cash.",
         ("num", "63%", "COULD COVER A $400 EMERGENCY WITH CASH · FED SURVEY, OCT 2025")),
        ("A country in that position can absorb an ordinary year, and 2026 has been a good deal harder than ordinary.", ("img", "e26")),
    ]),
    dict(id="year", title="THIS YEAR", beats=[
        ("Remember that the record income figure describes 2025. The mood describes right now, and a great deal changed in between.",
         ("split", ("2025", "WHAT THE INCOME FIGURE MEASURES"), ("SEPTEMBER 2026", "WHAT THE MOOD MEASURES"))),
        ("Earlier this year, a conflict in the Middle East disrupted oil shipments through the Strait of Hormuz, and fuel prices jumped.", ("img", "e27")),
        ("A year ago a gallon of regular gasoline averaged three dollars and twelve cents. On the fifth of October it was four thirty-five.",
         ("split", ("$3.12", "A GALLON · 6 OCT 2025"), ("$4.35", "5 OCT 2026 · EIA"))),
        ("In July, after the strait had reopened, the government's own energy forecasters expected about three dollars sixty for the second half of the year, which shows how little anyone can predict this.",
         ("num", "$3.60", "EIA'S JULY FORECAST FOR THE SECOND HALF · AVERAGE SINCE JULY $4.13 · ON 5 OCT $4.35")),
        ("Energy prices as a whole were up sixteen percent in the year to August, and overall inflation stood at three point four.",
         ("split", ("+16.3%", "ENERGY · 12 MONTHS TO AUG 2026"), ("+3.4%", "ALL ITEMS · BLS"))),
        ("On the sixteenth of September the Federal Reserve raised interest rates a quarter point, by twelve votes to none, and its statement was blunt.",
         ("quote", "Inflation remains elevated.", "FEDERAL OPEN MARKET COMMITTEE · 16 SEPTEMBER 2026")),
        ("Mortgage rates have climbed as well, by more than a full percentage point in twelve months.",
         ("split", ("6.30%", "30-YEAR MORTGAGE · A YEAR AGO"), ("7.40%", "8 OCT 2026 · FREDDIE MAC"))),
        ("Meanwhile hiring has been weak. Employers added twenty-nine thousand jobs in September, and the July figure was revised to a loss.",
         ("num", "+29,000", "JOBS ADDED · SEPTEMBER 2026 · JULY REVISED TO −10,000 · AUGUST +133,000 · BLS")),
        ("Unemployment is still low at four point two percent, but a worker with few alternatives has little power to ask for more.",
         ("num", "4.2%", "UNEMPLOYMENT RATE · SEPTEMBER 2026 · BLS")),
        ("And so the race from earlier has turned around. Over the past year pay rose three percent, and prices rose slightly faster.",
         ("split", ("+3.0%", "HOURLY PAY · YEAR TO SEP 2026"), ("+3.4%", "PRICES · YEAR TO AUG 2026"))),
        ("After inflation, the average hourly wage bought three tenths of a percent less in August than it had a year before, although slightly longer hours left the weekly pay packet a little ahead.",
         ("num", "−0.3%", "REAL AVERAGE HOURLY EARNINGS · AUG 2025 → AUG 2026 · REAL WEEKLY EARNINGS +0.3% · BLS")),
        ("Here is the year in one line, and you can see why a record announced in September landed so badly.",
         ("tl", [("MAY", "SENTIMENT 44.8 · RECORD LOW"), ("11 SEP", "INFLATION 3.4% · REAL PAY −0.3%"), ("15 SEP", "RECORD INCOME FOR 2025"), ("16 SEP", "FED RAISES RATES"), ("2 OCT", "+29,000 JOBS"), ("8 OCT", "MORTGAGES 7.40%")])),
    ]),
    dict(id="median", title="WHO IS THE MIDDLE", beats=[
        ("One entry remains, and it is the word median itself.", ("img", "e28")),
        ("By definition, half of all households earned less than about eighty-seven thousand dollars, so the headline describes the midpoint and nobody else.",
         ("words", "HALF OF HOUSEHOLDS ARE BELOW IT")),
        ("At the tenth percentile, near the bottom, the Census Bureau found no significant change in income last year.",
         ("split", ("NO CHANGE", "10TH PERCENTILE · 2024 → 2025"), ("+1.7%", "90TH PERCENTILE · CENSUS"))),
        ("At the ninetieth percentile, near the top, income rose again, for the third year running.", ("img", "e29")),
        ("In 1967 a household at the ninetieth percentile earned about nine times as much as a household at the tenth. Last year the multiple was thirteen.",
         ("split", ("9.23×", "90TH ÷ 10TH PERCENTILE · 1967"), ("13.06×", "2025 · CENSUS"))),
        ("A record at the midpoint is therefore compatible with millions of households that have seen no record of any kind.",
         ("img", "e30")),
    ]),
    dict(id="verdict", title="THE VERDICT", beats=[
        ("So here is the ledger, added up.", ("img", "e31")),
        ("On the credit side, pay has outrun prices by two to three percent since the pandemic began, and the typical household set an income record last year.",
         ("list", ["PAY +32.8% VS PRICES +29.9% SINCE 2020", "MEDIAN INCOME $87,460 · A RECORD", "UNEMPLOYMENT 4.2%", "73% SAY THEY ARE DOING OKAY"], "CREDIT")),
        ("On the debit side sit rent and groceries that matched the raise, fuel and power that beat it, and a mortgage rate that roughly doubled.",
         ("list", ["RENT +33% · GROCERIES +32%", "POWER +43% · GASOLINE +42%", "MORTGAGE RATE 3.72% → 7.40%", "CARD RATE 15% → 21%", "SAVING RATE 7.3% → 4.1%", "REAL HOURLY PAY −0.3% IN THE YEAR TO AUGUST"], "DEBIT")),
        ("My verdict is that the income record is true and the low mood is rational, because they measure different years and different bills.",
         ("words", "BOTH NUMBERS ARE TRUE")),
        ("The record counts 2025, before tax, and before interest. The mood counts this month, at your address, with your loan.",
         ("split", ("2025 · BEFORE INTEREST", "THE RECORD"), ("THIS MONTH · YOUR LOAN", "THE MOOD"))),
        ("If I had to watch a single figure from here, it would be real hourly earnings, which was negative over the year to August.",
         ("num", "−0.3%", "THE ONE TO WATCH · REAL HOURLY EARNINGS · NEXT RELEASE WITH EACH CPI REPORT")),
        ("Nothing in this film is advice about what to do with your money. It is a way of reading the numbers when they next make the news.",
         ("img", "e32")),
        ("Every source is linked below, with the date of each figure, so you can check the sums against your own.", ("img", "e33")),
        ("Eighty-seven thousand dollars is a record, and for a great many households it still feels like less.",
         ("split", ("$87,460", "THE RECORD"), ("48.1", "THE MOOD"))),
    ]),
]
