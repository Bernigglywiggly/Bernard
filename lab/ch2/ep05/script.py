"""HOW THEY PROFIT · EP05 · WHERE YOUR $100 GOES (PayPal), v0 draft (5 Oct 2026, before scenes and voice).

New structure (CRAFT.md §1: no fixed seven chapters). The film follows ONE $100 payment from the tap on the yellow
button to PayPal's last cent of profit. The $100 is the persistent object on screen: a single banknote/receipt that
gets cut into pieces as each party takes its share, so every chapter is a transformation of the same object.

The hidden mechanism: PayPal keeps about $1.85 of every $100 that moves through it (2025 average). A little over half
of that goes straight out again to card networks, banks and losses, leaving about 86 cents, and about 34 cents ends
as operating profit. On top sits about $1.3B of interest earned on money people leave in their balances. And there
are two PayPals: the branded button (good margins, struggling) and unbranded processing (huge, thin, being trimmed).

Every number is in FACTS.md with its source; lines marked TO VERIFY there must be checked before voicing.
Voice: Higgsfield Seed Audio "Sterling" (engine/voice_hf.py), calm, professor's pace (CRAFT.md §2: no staccato runs,
one number per sentence). About 7 minutes.

Fields as in the other HTP scripts: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · ONE HUNDRED DOLLARS: the cold open
    dict(floor=0, id="tap", text="Somewhere right now, someone is about to spend a hundred dollars by tapping a yellow button."),
    dict(floor=0, id="trail", card=("$100", "ONE PAYMENT, FOLLOWED TO THE END"),
         text="We're going to follow that hundred dollars all the way through PayPal, to see how much of it the company keeps and where the rest goes."),
    dict(floor=0, id="scale", cut=True, card=("$1.79 TRILLION", "PAID THROUGH PAYPAL · 2025"),
         text="Last year, $1.79 trillion moved through PayPal this way.",
         say="Last year, one point seven nine trillion dollars moved through PayPal this way."),
    dict(floor=0, id="small", air=1, text="What it keeps from each payment is tiny, and the way it adds up tells you how the company really works."),
    # 1 · THE TOLL: what the shop pays
    dict(floor=1, id="toll", card=("3.49% + 49¢", "PAYPAL CHECKOUT · US STANDARD RATE"),
         text="If the shop is a small business on PayPal's standard US rate, the button costs it 3.49 percent of the sale, plus 49 cents.",
         say="If the shop is a small business on PayPal's standard American rate, the button costs it three point four nine percent of the sale, plus forty-nine cents."),
    dict(floor=1, id="fee", card=("$3.98", "THE FEE ON A $100 SALE"),
         text="On our hundred dollars, that comes to $3.98, taken before the shop sees the money.",
         say="On our hundred dollars, that comes to three dollars and ninety-eight cents, taken before the shop sees the money."),
    dict(floor=1, id="why", air=1,
         text="Shops pay it because the button sells. PayPal's own annual report says the point is that fewer shoppers abandon their basket when they don't have to type a card number or an address."),
    # 2 · THE AVERAGE: why PayPal keeps far less than $3.98
    dict(floor=2, id="avg", cut=True, card=("$1.85", "PAYPAL'S REVENUE PER $100 PAID · 2025 AVERAGE"),
         text="Across the whole company, though, the average is much lower. For every hundred dollars that moved through PayPal last year, it earned about $1.85.",
         say="Across the whole company, though, the average is much lower. For every hundred dollars that moved through PayPal last year, it earned about one dollar and eighty-five cents."),
    dict(floor=2, id="who", text="The gap comes from who is paying. Large merchants negotiate their rates down, and a big share of the volume isn't the yellow button at all."),
    dict(floor=2, id="braintree",
         text="It's Braintree, PayPal's card processing business, which handles payments behind other companies' own checkout pages."),
    dict(floor=2, id="psp", card=("9.3 BILLION", "PAYMENTS PROCESSED UNBRANDED · 2025"),
         text="About 9.3 billion of last year's payments were this kind of processing, where the shopper never sees the PayPal name.",
         say="About nine point three billion of last year's payments were this kind of processing, where the shopper never sees the PayPal name."),
    dict(floor=2, id="third", air=1, text="That's more than a third of every payment PayPal handled."),
    # 3 · WHO ELSE GETS PAID: the $100 is cut up
    dict(floor=3, id="networks", cut=True, card=("89¢", "PER $100 · PAID ON TO CARD NETWORKS AND BANKS"),
         text="From that average, PayPal pays the card networks and banks that actually move the money: about 89 cents of every hundred dollars.",
         say="From that average, PayPal pays the card networks and banks that actually move the money, about eighty-nine cents of every hundred dollars."),
    dict(floor=3, id="losses", card=("10¢", "PER $100 · LOST TO FRAUD AND UNPAID LOANS"),
         text="About 10 more cents is lost to fraud, to sellers who never deliver, and to loans that aren't repaid.",
         say="About ten more cents is lost to fraud, to sellers who never deliver, and to loans that aren't repaid."),
    dict(floor=3, id="left", card=("86¢", "PER $100 · LEFT AFTER THE PAYMENT ITSELF IS PAID FOR"),
         text="That leaves about 86 cents, so a little over half of what PayPal charges goes straight back out to the rest of the payment system.",
         say="That leaves about eighty-six cents, so a little over half of what PayPal charges goes straight back out to the rest of the payment system."),
    # 4 · THIRTY-FOUR CENTS: what's left at the end
    dict(floor=4, id="costs", text="Out of what's left, PayPal still pays its engineers, its customer service, its marketing and its offices."),
    dict(floor=4, id="profit", card=("34¢", "PER $100 · PAYPAL'S OPERATING PROFIT · 2025"),
         text="At the end of the line, its operating profit came to about 34 cents for every hundred dollars.",
         say="At the end of the line, its operating profit came to about thirty-four cents for every hundred dollars."),
    dict(floor=4, id="total", card=("$6.1 BILLION", "PAYPAL'S OPERATING INCOME · 2025"),
         text="That sounds small, but across that much money it added up to $6.1 billion of operating profit last year.",
         say="That sounds small, but across that much money it added up to six point one billion dollars of operating profit last year."),
    # 5 · MONEY THAT SITS STILL: interest on balances
    dict(floor=5, id="still", cut=True, air=1, text="There is one more source of income, and it asks almost nothing of PayPal."),
    dict(floor=5, id="balance",
         text="When people leave money in their PayPal or Venmo balance, PayPal holds it, and the assets underneath those balances earn interest."),
    dict(floor=5, id="interest", card=("ABOUT $1.3 BILLION", "INTEREST ON CUSTOMER BALANCES · 2025"),
         text="Last year that interest came to about $1.3 billion.",
         say="Last year that interest came to about one point three billion dollars."),
    dict(floor=5, id="yours", air=1, text="In an ordinary balance, the interest on your idle money goes to PayPal, and none of it comes to you."),
    # 6 · TWO PAYPALS
    dict(floor=6, id="two", cut=True, text="Put those pieces together and there are really two PayPals."),
    dict(floor=6, id="button", text="One is the yellow button, which shoppers choose by name, and where the margins are good."),
    dict(floor=6, id="pipes", text="The other is the processing behind other companies' checkouts, where the volume is enormous and the margins are thin."),
    dict(floor=6, id="shed",
         text="In 2025 PayPal deliberately turned some of that thin business away. Its annual report says Braintree's volume grew while its number of transactions fell, because of a shift to what it calls profitable growth."),
    # 7 · THE BUTTON'S PROBLEM, and the verdict
    dict(floor=7, id="game", cut=True, text="That makes the button the part that matters most, and it's where PayPal admits it's struggling."),
    dict(floor=7, id="quote", card=("“PARTICULARLY IN BRANDED CHECKOUT”", "PAYPAL'S RESULTS STATEMENT · 3 FEB 2026"),
         text="When it reported these results in February, the company wrote that its execution had not been where it needs to be, particularly in branded checkout."),
    dict(floor=7, id="ceo", text="On the same day, it named a new chief executive, Enrique Lores."),
    dict(floor=7, id="phone", text="On a phone, the yellow button now sits beside other one-tap ways to pay, and all of them are competing for the same moment."),
    dict(floor=7, id="verdict", air=1,
         text="Here's how I'd read it. Plenty of companies can move money, so the valuable thing PayPal owns is the moment a shopper trusts its button enough to press it without typing anything."),
    dict(floor=7, id="card", card=("2.99% + 49¢", "A STANDARD CARD PAYMENT THROUGH PAYPAL · US"),
         text="If you sell online, compare the two prices. A standard card payment through PayPal costs a shop 2.99 percent plus 49 cents, so the extra half a percent is what you pay for the shoppers the button brings.",
         say="If you sell online, compare the two prices. A standard card payment through PayPal costs a shop two point nine nine percent plus forty-nine cents, so the extra half a percent is what you pay for the shoppers the button brings."),
    dict(floor=7, id="close", text="And if you keep money sitting in a balance, someone is earning interest on it. It's worth checking that the someone is you."),
]

FLOORS = ["ONE HUNDRED DOLLARS", "THE TOLL", "THE AVERAGE", "WHO ELSE GETS PAID", "THIRTY-FOUR CENTS",
          "MONEY THAT SITS STILL", "TWO PAYPALS", "THE BUTTON'S PROBLEM"]

SOURCES = [
    "PayPal Holdings, Form 10-K for 2025 (SEC EDGAR): net revenues $33,172M (transaction revenues $29,798M; revenues "
    "from other value added services $3,374M); transaction expense rate 0.89% of TPV; transaction and credit loss rate "
    "0.10%; branded checkout 'reduce[s] cart abandonment'; Braintree TPV grew while its transactions fell, 'our "
    "strategic shift as we focus on profitable growth'",
    "PayPal fourth quarter and full year 2025 results (8-K, Exhibit 99.1, 3 Feb 2026): TPV $1.79T; transaction margin "
    "dollars $15.5B ($14.2B excluding interest on customer balances); GAAP operating income $6.1B; 439M active "
    "accounts; 25.4B payment transactions, 16.1B excluding PSP; 'our execution has not been where it needs to be, "
    "particularly in branded checkout'; Enrique Lores appointed President and CEO",
    "PayPal US business fees page (checked 5 Oct 2026): PayPal Checkout 3.49% + fixed fee; standard credit and debit "
    "card payments 2.99% + fixed fee; USD fixed fee $0.49",
    "Per-$100 figures are worked out from the totals above: revenue $33.2B / TPV $1.79T = $1.85; 89¢ and 10¢ from the "
    "two rates; 86¢ left; operating income $6.1B / $1.79T = 34¢; interest on balances about $1.3B = $15.5B - $14.2B",
]
