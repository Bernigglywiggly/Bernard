"""CHANNEL 2 · EP01 · BANKS WITH WINGS, v1 (1 Oct 2026): the pilot for The Margin (channel/channel2/BIBLE.md).

The hidden mechanism: an airline's loyalty scheme is a currency it prints. It sells miles to banks for cash up front;
the banks hand them to cardholders for everyday spending; the airline alone decides what a mile buys, and many are
never spent. So the most valuable part of a big American airline isn't the planes. In 2025 American Express paid
Delta $8.2B, more than Delta's whole pre-tax profit ($6.2B). In 2020 United borrowed against MileagePlus, valued at
$21.9B, while the stock market valued all of United at about $10.5B.

Voice: Curve Elder A (EL_VOICE=elder), calm and unhurried, never George (channel/CHANNELS.md: no shared template across
channels). About 8-9 minutes at the engine's pace. No jokes; straight in; every figure on screen with its source.

Fields as in The Curve's scripts: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · THE PRICE: the cold open
    dict(floor=0, id="paid", card=("$8.2 BILLION", "AMERICAN EXPRESS → DELTA · 2025"),
         text="Last year, one company paid Delta Air Lines $8.2 billion.",
         say="Last year, one company paid Delta Air Lines eight point two billion dollars."),
    dict(floor=0, id="notflights", text="It wasn't an airline. It didn't buy a single seat. It was a credit card company."),
    dict(floor=0, id="profit", cut=True, card=("$6.2 BILLION", "DELTA'S PRE-TAX PROFIT · 2025"),
         text="And that payment was bigger than Delta's entire profit before tax that year: $6.2 billion.",
         say="And that payment was bigger than Delta's entire profit before tax that year: six point two billion dollars."),
    dict(floor=0, id="banks", air=1, text="To understand why, you have to stop thinking of airlines as airlines."),
    dict(floor=0, id="wings", cut=True, text="The biggest ones are closer to banks. Banks with wings."),
    # 1 · THE MACHINE: how a mile is made
    dict(floor=1, id="print", air=1, text="It starts with something that costs an airline almost nothing to make: a mile."),
    dict(floor=1, id="currency", text="A mile is a currency. The airline creates it, sets its value, and runs the only shop that fully accepts it."),
    dict(floor=1, id="sell", text="And it doesn't just give miles to people who fly. It sells them, in bulk, to banks."),
    dict(floor=1, id="cards", text="The banks hand those miles to their cardholders, a few for every coffee, every grocery shop, every bill paid on the card."),
    dict(floor=1, id="cash", text="So the airline is paid in cash today, for seats someone might claim years from now."),
    dict(floor=1, id="empty", text="Often for seats that would have flown empty anyway."),
    dict(floor=1, id="never", cut=True, text="And some miles are never spent at all. They expire, or sit in accounts nobody opens. That money is simply kept."),
    # 2 · THE PROOF: the miles worth more than the airline
    dict(floor=2, id="2020", air=2, card=("JUNE 2020", "NO ONE IS FLYING"),
         text="We know what this machine is worth, because in 2020 the airlines had to prove it.",
         say="We know what this machine is worth, because in twenty twenty the airlines had to prove it."),
    dict(floor=2, id="grounded", text="With the planes grounded, United needed to borrow billions. It needed something lenders would trust."),
    dict(floor=2, id="planes", text="Not its planes. Not its airports. Its miles."),
    dict(floor=2, id="valued", card=("$21.9 BILLION", "MILEAGEPLUS, VALUED FOR THE LOAN · JUNE 2020"),
         text="United had its loyalty scheme, MileagePlus, valued at $21.9 billion, and borrowed $6.8 billion against it.",
         say="United had its loyalty scheme, MileagePlus, valued at twenty-one point nine billion dollars, and borrowed six point eight billion against it."),
    dict(floor=2, id="market", card=("$10.5 BILLION", "ALL OF UNITED, ON THE STOCK MARKET"),
         text="At the time, the stock market valued the whole of United, planes and all, at about $10.5 billion.",
         say="At the time, the stock market valued the whole of United, planes and all, at about ten and a half billion dollars."),
    dict(floor=2, id="worth", cut=True, text="The miles were worth about twice as much as the airline."),
    dict(floor=2, id="american", card=("$19.5–31.5 BILLION", "AADVANTAGE, APPRAISED · 2021"),
         text="A year later, American Airlines did the same. Its scheme was appraised at between $19.5 and $31.5 billion. It borrowed $10 billion against it.",
         say="A year later, American Airlines did the same. Its scheme was appraised at between nineteen and a half and thirty-one and a half billion dollars. It borrowed ten billion against it."),
    dict(floor=2, id="sold", card=("$5.3 BILLION", "MILES UNITED SOLD IN 2019"),
         text="The filings showed how the machine runs. In 2019, United sold about $5.3 billion of miles.",
         say="The filings showed how the machine runs. In twenty nineteen, United sold about five point three billion dollars of miles."),
    dict(floor=2, id="third", card=("71%", "OF THE SCHEME'S REVENUE CAME FROM PARTNERS · 2019"),
         text="And about 71 percent of the scheme's revenue came not from flyers, but from partners. Mostly credit card companies.",
         say="And about seventy-one percent of the scheme's revenue came not from flyers, but from partners. Mostly credit card companies."),
    # 3 · THE MONEY: why a bank pays for miles
    dict(floor=3, id="whybank", air=2, text="So why would a bank pay billions for an airline's miles?"),
    dict(floor=3, id="swipe", text="Because every time you pay by card, the shop pays a fee. Part of it goes to the bank that issued your card."),
    dict(floor=3, id="two", card=("~2%", "AVERAGE US CREDIT CARD FEE TO THE BANK"),
         text="In the United States, that fee averages around 2 percent of everything you buy.",
         say="In the United States, that fee averages around two percent of everything you buy."),
    dict(floor=3, id="spend", text="So the bank wants you spending on its card, not someone else's. Miles are how it wins you."),
    dict(floor=3, id="million", card=("1,000,000+", "NEW DELTA AMEX CARDS A YEAR · 4 YEARS RUNNING"),
         text="It works. Delta has signed up more than a million new card members a year, four years in a row.",
         say="It works. Delta has signed up more than a million new card members a year, four years in a row."),
    dict(floor=3, id="ten", card=("$10 BILLION", "DELTA'S TARGET FROM AMEX, A YEAR"),
         text="And Delta expects the Amex payments to reach $10 billion a year within a few years.",
         say="And Delta expects the Amex payments to reach ten billion dollars a year within a few years."),
    dict(floor=3, id="everyone", cut=True, text="And the shops paying those fees build them into their prices. Everyone pays for the miles. Only some people collect them."),
    # 4 · YOU: what it means for your wallet
    dict(floor=4, id="you", air=2, text="So what does this mean for you?"),
    dict(floor=4, id="uk", card=("0.3%", "UK CAP ON CREDIT CARD FEES"),
         text="If you're in Britain, the fee banks can charge shops on a credit card is capped at 0.3 percent.",
         say="If you're in Britain, the fee banks can charge shops on a credit card is capped at nought point three percent."),
    dict(floor=4, id="thinner", text="That's why British cards give far fewer miles than American ones. The money to pay for them isn't there."),
    dict(floor=4, id="interest", text="So in Britain, the banks earn more from interest and fees. A rewards card only pays you if you clear it in full, every month."),
    dict(floor=4, id="devalue", text="Wherever you are, remember who controls the currency. When an airline raises the miles a seat costs, everything you've saved is worth less, overnight."),
    dict(floor=4, id="spendit", cut=True, text="Miles are not savings. Earn them, then spend them."),
    # 5 · WHAT IF
    dict(floor=5, id="imagine", air=3, cut=True, text="So imagine one more step."),
    dict(floor=5, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=5, id="scene", text="An airline whose miles are worth more than its flights, decides the flying is the cost of running the currency. Seats priced to keep you collecting, not to make a profit."),
    dict(floor=5, id="question", air=1, text="At what point is it a bank that happens to fly?"),
    # 6 · THE CLOSE: mirrored
    dict(floor=6, id="then", air=2, cut=True, text="Last year, American Express paid Delta $8.2 billion.",
         say="Last year, American Express paid Delta eight point two billion dollars."),
    dict(floor=6, id="close", cut=True, text="The planes carry the passengers. The miles carry the airline."),
]

FLOORS = ["THE PRICE", "THE MACHINE", "THE PROOF", "THE MONEY", "YOU", "WHAT IF", "THE CLOSE"]

SOURCES = [
    "Delta Air Lines, December quarter and full year 2025 results (13 Jan 2026): American Express remuneration $8.2B "
    "in 2025, up 11%; pre-tax income $6.2B (GAAP); more than 1M card acquisitions for the fourth consecutive year; "
    "expected to grow to $10B (Delta investor relations; SEC 8-K)",
    "United Airlines MileagePlus financing, June 2020: MileagePlus valued at about $21.9B (12x 2019 EBITDA of about "
    "$1.8B); $6.8B raised against it (United investor presentation, 15 Jun 2020; SEC 8-K)",
    "United's market value of about $10.5B against the programme's ~$20B (The Hustle, 5 Oct 2020); MileagePlus sold "
    "about $5.3B of miles in 2019, about 71% to third parties such as card companies (Skift, 15 Jun 2020)",
    "American Airlines, March 2021: $10B financing secured by AAdvantage; third-party appraisal $19.5B-$31.5B "
    "(Davis Polk; SEC filing)",
    "Average US credit card interchange about 2%; UK and EU cap on consumer credit card interchange 0.3% "
    "(EU Interchange Fee Regulation 2015, retained in UK law)",
    "The what-if is labelled as imagined, not a forecast",
]
