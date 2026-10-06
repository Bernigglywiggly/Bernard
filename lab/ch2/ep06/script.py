"""HOW THEY PROFIT · EP06 · THE COMPANY THAT NEVER TOUCHES YOUR MONEY (Visa), v0 draft (6 Oct 2026, before scenes and voice).

Structure (CRAFT.md §1: a different shape from EP05's "follow one $100"): ONE CARD TAP, traced on a map. The film
opens in the middle of the tap (a cafe in Lisbon, a card from a bank in Ohio: an ILLUSTRATION, labelled on screen),
then walks the message hop by hop: shop, the shop's bank, Visa, the cardholder's bank, and back. The persistent object
is the message itself, a small packet that travels the route; money only ever moves between the two banks.

The hidden mechanism: Visa lends nothing and holds nothing. It sets the fee the banks pay each other (interchange)
and doesn't collect it; it charges the banks for membership, for each message and for crossing a border, gives
$15.8B of that back as incentives, and still turns half of its net revenue into profit. The verdict: the product is
the rulebook, and the rulebook is also what it keeps being sued over.

Every number is in FACTS.md with its source. Fiscal 2025 (year to 30 Sep 2025). VISA REPORTS FISCAL 2026 IN LATE
OCTOBER 2026: if this is voiced after that, swap every figure for the new year first.
Voice: Higgsfield Seed Audio "Sterling" (engine/voice_hf.py), calm, professor's pace. About 7 minutes.

Fields as in the other HTP scripts: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · ONE SECOND: the cold open, mid-tap
    dict(floor=0, id="tap", text="A card touches a reader in a café in Lisbon, and about a second later the reader says approved."),
    dict(floor=0, id="ocean",
         text="In that second a message has left the café, crossed the Atlantic to a bank in Ohio, and come back with an answer."),
    dict(floor=0, id="scale", cut=True, card=("$17 TRILLION", "PAYMENTS AND CASH VOLUME ON VISA · FISCAL 2025"),
         text="Last year, $17 trillion of payments and cash moved across Visa's network like this.",
         say="Last year, seventeen trillion dollars of payments and cash moved across Visa's network like this."),
    dict(floor=0, id="never", air=1,
         text="The company in the middle of that route never held any of the money, and that turns out to be the reason it is so profitable."),
    # 1 · FOUR PARTIES: who is actually in the tap
    dict(floor=1, id="four", text="Four parties take part in a card payment, and it helps to meet them in the order the message does."),
    dict(floor=1, id="shopbank", text="The café has a bank that collects card payments on its behalf, and the message goes there first."),
    dict(floor=1, id="yourbank",
         text="At the far end is the bank that issued the card, which is the one that knows whether there is money or credit behind it."),
    dict(floor=1, id="quote", card=("“VISA IS NOT A FINANCIAL INSTITUTION”", "VISA ANNUAL REPORT · FISCAL 2025"),
         text="Visa sits between those two banks, and its own annual report is plain about what it is. It says that Visa is not a financial institution."),
    dict(floor=1, id="risk", air=1,
         text="It doesn't issue the card and it doesn't lend the money, so when a cardholder never pays the bill, the loss belongs to the bank."),
    # 2 · THE FEE IT DOESN'T KEEP: interchange
    dict(floor=2, id="fee", cut=True, text="When the café is paid, its bank hands a fee across to the bank that issued the card."),
    dict(floor=2, id="interchange", card=("INTERCHANGE", "PAID BY THE SHOP'S BANK TO THE CARDHOLDER'S BANK"),
         text="The fee is called interchange, and for most shops it is a large part of what accepting a card costs."),
    dict(floor=2, id="sets", text="Visa writes the default rates for interchange, and then the money passes from one bank to the other without Visa collecting it."),
    dict(floor=2, id="whyset", air=1,
         text="That looks generous until you see what the fee is for. It pays banks to put Visa's name on their cards, and every card they issue sends more messages down Visa's wires. In a minute, what Visa charges for those messages."),
    # 3 · THREE METERS: what Visa does charge
    dict(floor=3, id="meters", cut=True, text="Visa's own income comes from the banks, and it is counted on three meters."),
    dict(floor=3, id="service", card=("$17.5 BILLION", "SERVICE REVENUE · FISCAL 2025"),
         text="The first is a charge for being on the network at all, which rises with the amount spent on a bank's cards. Last year it brought in $17.5 billion.",
         say="The first is a charge for being on the network at all, which rises with the amount spent on a bank's cards. Last year it brought in seventeen and a half billion dollars."),
    dict(floor=3, id="count", card=("257.5 BILLION", "TRANSACTIONS PROCESSED BY VISA · FISCAL 2025"),
         text="The second meter counts messages, and last year Visa processed 257.5 billion transactions.",
         say="The second meter counts messages, and last year Visa processed two hundred and fifty-seven and a half billion transactions."),
    dict(floor=3, id="daily", text="That works out at roughly 700 million messages every day.",
         say="That works out at roughly seven hundred million messages every day."),
    dict(floor=3, id="processing", card=("$20.0 BILLION", "DATA PROCESSING REVENUE · FISCAL 2025"),
         text="Charging for each message earned $20 billion, which makes it the largest meter.",
         say="Charging for each message earned twenty billion dollars, which makes it the largest meter."),
    dict(floor=3, id="border", card=("$14.2 BILLION", "INTERNATIONAL TRANSACTION REVENUE · FISCAL 2025"),
         text="The third meter only runs when the card and the shop are in different countries, as they are in our café. Those crossings earned $14.2 billion.",
         say="The third meter only runs when the card and the shop are in different countries, as they are in our café. Those crossings earned fourteen point two billion dollars."),
    dict(floor=3, id="other", air=1, text="A smaller fourth line, for licences and extra services, added about four billion more."),
    # 4 · THE MONEY IT HANDS BACK: incentives, and the net
    dict(floor=4, id="back", cut=True, text="Before any of this is counted as revenue, Visa gives a large part of it back."),
    dict(floor=4, id="incentives", card=("$15.8 BILLION", "CLIENT INCENTIVES · FISCAL 2025"),
         text="Last year it paid $15.8 billion in incentives to banks and other partners, which is the price of keeping their cards on Visa and off a rival network.",
         say="Last year it paid fifteen point eight billion dollars in incentives to banks and other partners, which is the price of keeping their cards on Visa and off a rival network."),
    dict(floor=4, id="net", card=("$40.0 BILLION", "VISA'S NET REVENUE · FISCAL 2025"),
         text="What remained was $40 billion of net revenue.",
         say="What remained was forty billion dollars of net revenue."),
    dict(floor=4, id="cents", card=("ABOUT 24¢", "VISA'S NET REVENUE PER $100 MOVED"),
         text="Set against the money that moved, it is a very thin slice. For every hundred dollars that crossed the network, Visa kept about 24 cents.",
         say="Set against the money that moved, it is a very thin slice. For every hundred dollars that crossed the network, Visa kept about twenty-four cents."),
    # 5 · HALF: why so much of it is profit
    dict(floor=5, id="thin", cut=True, text="A slice that thin should belong to a low-margin business, and Visa is close to the opposite."),
    dict(floor=5, id="costs", card=("$16.0 BILLION", "OPERATING EXPENSES · FISCAL 2025"),
         text="Running the whole company cost $16 billion last year, and that includes a large sum set aside for lawsuits, which we will come back to.",
         say="Running the whole company cost sixteen billion dollars last year, and that includes a large sum set aside for lawsuits, which we will come back to."),
    dict(floor=5, id="profit", card=("$20.1 BILLION", "VISA'S NET INCOME · FISCAL 2025"),
         text="After tax, the profit was $20.1 billion.",
         say="After tax, the profit was twenty point one billion dollars."),
    dict(floor=5, id="half", card=("50¢", "PROFIT FROM EACH DOLLAR OF NET REVENUE"),
         text="That means about 50 cents of every dollar Visa took in ended the year as profit.",
         say="That means about fifty cents of every dollar Visa took in ended the year as profit."),
    dict(floor=5, id="why", air=1,
         text="The explanation is in what Visa leaves to others. A bank needs branches, loan books and reserves for the customers who don't pay, while Visa needs data centres and a rulebook, and sending one more message costs it almost nothing."),
    dict(floor=5, id="returned", card=("$22.8 BILLION", "RETURNED TO SHAREHOLDERS · FISCAL 2025"),
         text="With little to spend the money on, it sent $22.8 billion back to shareholders through buybacks and dividends.",
         say="With little to spend the money on, it sent twenty-two point eight billion dollars back to shareholders through buybacks and dividends."),
    # 6 · THE RULEBOOK: the weak point, and the verdict
    dict(floor=6, id="weak", cut=True, text="The weak point of this arrangement is the same fee Visa sets and never collects."),
    dict(floor=6, id="sued", text="Shops have been taking Visa to court over interchange for years."),
    dict(floor=6, id="suits", card=("$2.5 BILLION", "SET ASIDE FOR LITIGATION · FISCAL 2025"),
         text="Last year the company set aside $2.5 billion for that litigation and other legal matters.",
         say="Last year the company set aside two and a half billion dollars for that litigation and other legal matters."),
    dict(floor=6, id="regulators",
         text="Its annual report also warns that regulators and central banks in a number of countries are reviewing those fees and the rules around them."),
    dict(floor=6, id="verdict", air=1,
         text="Here's how I'd read it. Visa's real product is the rulebook that lets a café in Lisbon trust a bank in Ohio it has never heard of, and the wires are only how the rules get delivered."),
    dict(floor=6, id="shop",
         text="If you run a shop, most of what a card payment costs you goes to banks, so the rate your own bank quotes you is the part worth negotiating."),
    dict(floor=6, id="close",
         text="And the next time a reader says approved, the money will have moved between two banks, on terms written by a company that was never holding it."),
]

FLOORS = ["ONE SECOND", "FOUR PARTIES", "THE FEE IT DOESN'T KEEP", "THREE METERS", "THE MONEY IT HANDS BACK", "HALF",
          "THE RULEBOOK"]

SOURCES = [
    "Visa Inc., Fiscal Fourth Quarter and Full-Year 2025 Results (8-K, Exhibit 99.1, 28 Oct 2025): net revenue $40.0B "
    "(+11%); GAAP net income $20.1B; service revenue $17.5B; data processing revenue $20.0B; international transaction "
    "revenue $14.2B; other revenue $4.1B; client incentives $15.8B; GAAP operating expenses $16.0B, including a $2.5B "
    "litigation provision 'associated with the interchange multidistrict litigation (MDL) case and other legal matters'; "
    "257.5 billion transactions processed by Visa; share repurchases and dividends $22.8B",
    "Visa Inc., Form 10-K for fiscal 2025 (SEC EDGAR): 'total payments and cash volume was $17 trillion'; 'Visa is not "
    "a financial institution. We do not issue cards, extend credit or set rates and fees for account holders of Visa "
    "products nor do we earn revenue from or bear credit risk with respect to any of these activities'; 'Generally, "
    "IRFs are paid by acquirers to issuers. We establish default IRFs'; interchange fees 'continue to be subject to "
    "increased government regulation globally, and regulatory authorities and central banks in a number of "
    "jurisdictions have reviewed or are reviewing these fees, rules and practices'",
    "Worked out from the totals above: $40.0B / $17T = about 24 cents per $100; $20.1B / $40.0B = 50%; 257.5 billion / "
    "365 = about 705 million transactions a day; the four revenue lines total $55.8B, less $15.8B of incentives = $40.0B",
    "The Lisbon café and the Ohio bank are an illustration of a cross-border payment, not a real transaction",
]
