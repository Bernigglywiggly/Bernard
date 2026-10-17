"""CHANNEL 2 · EP03 · THE $65 MEMBERSHIP, v1 (1 Oct 2026): The Margin, film 3 (channel/channel2/BIBLE.md).

The hidden mechanism: Costco sells its goods at close to cost and makes its profit at the door. In the year to
August 2026, membership fees were $5.9B, about half of its $11.7B operating income; take the fees away and $297B of
goods earned about two cents of operating profit per dollar. The cheap things ($1.50 hot dog, $4.99 chicken) are
bait it pays for; the fee, renewed by more than nine in ten members, is the business.

Voice: Curve Elder A (EL_VOICE=elder), calm and unhurried, never George. About 8 minutes at the engine's pace.
No jokes; straight in; every figure on screen with its source.

Fields as in The Curve's scripts: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · THE PRICE: the cold open
    dict(floor=0, id="hotdog", card=("$1.50", "COSTCO HOT DOG AND DRINK · SINCE 1985"),
         text="At Costco, a hot dog and a drink cost $1.50. The same price since 1985.",
         say="At Costco, a hot dog and a drink cost a dollar fifty. The same price since nineteen eighty-five."),
    dict(floor=0, id="chicken", card=("$4.99", "COSTCO ROTISSERIE CHICKEN · SINCE 2009"),
         text="A whole roast chicken costs $4.99. Costco has said it gives up tens of millions of dollars a year to keep it there.",
         say="A whole roast chicken costs four ninety-nine. Costco has said it gives up tens of millions of dollars a year to keep it there."),
    dict(floor=0, id="profit", cut=True, card=("$9.2 BILLION", "COSTCO'S NET INCOME · YEAR TO AUG 2026"),
         text="And yet last year, Costco made a profit of $9.2 billion.",
         say="And yet last year, Costco made a profit of nine point two billion dollars."),
    dict(floor=0, id="how", air=1, text="How does a shop with prices like that make so much money?"),
    dict(floor=0, id="card", cut=True, text="Because the shopping isn't really what it sells. The card in your wallet is."),
    # 1 · THE MACHINE: charge for the door, sell at cost
    dict(floor=1, id="door", air=1, text="To shop at Costco, you pay to get in."),
    dict(floor=1, id="fee", card=("$65 · £42", "A YEAR'S BASIC MEMBERSHIP · US · UK"),
         text="In America, a basic membership is $65 a year. In Britain, £42.",
         say="In America, a basic membership is sixty-five dollars a year. In Britain, forty-two pounds."),
    dict(floor=1, id="buys", text="The fee buys you no goods and no credit. Only the right to walk in and buy."),
    dict(floor=1, id="promise", text="In return, Costco promises low prices. And it holds itself to that."),
    dict(floor=1, id="price", card=("1976", "PRICE CLUB, SAN DIEGO: THE FIRST WAREHOUSE CLUB"),
         text="The idea goes back to 1976, when Sol Price opened Price Club in San Diego: a warehouse that charged small businesses a fee to shop.",
         say="The idea goes back to nineteen seventy-six, when Sol Price opened Price Club in San Diego: a warehouse that charged small businesses a fee to shop."),
    dict(floor=1, id="sinegal", text="Jim Sinegal, who had learned the trade working for Sol Price, co-founded Costco in 1983 with Jeffrey Brotman. Ten years later, Costco and Price Club merged.",
         say="Jim Sinegal, who had learned the trade working for Sol Price, co-founded Costco in nineteen eighty-three with Jeffrey Brotman. Ten years later, Costco and Price Club merged."),
    dict(floor=1, id="caps", card=("14% · 15%", "COSTCO'S REPORTED MARKUP LIMITS · BRANDS · KIRKLAND"),
         text="Its founders set a rule, widely reported ever since: no branded item marked up more than 14 percent over cost. Its own brand, Kirkland Signature, no more than 15.",
         say="Its founders set a rule, widely reported ever since: no branded item marked up more than fourteen percent over cost. Its own brand, Kirkland Signature, no more than fifteen."),
    dict(floor=1, id="fewer", card=("< 4,000", "PRODUCTS IN A TYPICAL COSTCO WAREHOUSE"),
         text="It keeps the range small: fewer than four thousand products in a warehouse, bought in enormous quantities, so suppliers cut their prices.",
         say="It keeps the range small: fewer than four thousand products in a warehouse, bought in enormous quantities, so suppliers cut their prices."),
    dict(floor=1, id="pallets", text="The goods sit on pallets, in the boxes they arrived in. No decoration, no adverts in the aisles, no wasted space."),
    dict(floor=1, id="thin", text="So the shelves run close to cost."),
    dict(floor=1, id="pure", cut=True, text="And the membership fee? It costs Costco almost nothing to collect. It's almost pure profit."),
    # 2 · THE PROOF: the numbers
    dict(floor=2, id="year", air=2, text="The accounts show how much of the business that fee really is."),
    dict(floor=2, id="fees", card=("$5.9 BILLION", "MEMBERSHIP FEES · YEAR TO AUG 2026"),
         text="In the year to August 2026, Costco collected $5.9 billion in membership fees.",
         say="In the year to August twenty twenty-six, Costco collected five point nine billion dollars in membership fees."),
    dict(floor=2, id="opinc", card=("$11.7 BILLION", "COSTCO'S OPERATING INCOME · YEAR TO AUG 2026"),
         text="Its operating profit, everything the business earned before interest and tax, was $11.7 billion.",
         say="Its operating profit, everything the business earned before interest and tax, was eleven point seven billion dollars."),
    dict(floor=2, id="half", cut=True, text="So about half of Costco's operating profit came from the fee alone."),
    dict(floor=2, id="goods", card=("$297 BILLION", "GOODS COSTCO SOLD · YEAR TO AUG 2026"),
         text="And the other half? That came from selling $297 billion of goods.",
         say="And the other half? That came from selling two hundred and ninety-seven billion dollars of goods."),
    dict(floor=2, id="cents", card=("~2¢", "OPERATING PROFIT PER $1 OF GOODS, BEFORE FEES"),
         text="Take the fees away, and the shops made about two cents of profit on every dollar you spent.",
         say="Take the fees away, and the shops made about two cents of profit on every dollar you spent."),
    dict(floor=2, id="design", text="That's not a weakness. It's the design. Sell at almost no profit, and charge for the door."),
    dict(floor=2, id="members", card=("84.1 MILLION", "PAID COSTCO MEMBERS · AUG 2026"),
         text="And people keep paying. Costco now has 84 million paid members, and 150 million cardholders.",
         say="And people keep paying. Costco now has eighty-four million paid members, and a hundred and fifty million cardholders."),
    dict(floor=2, id="renew", card=("92.3%", "MEMBERS WHO RENEW EACH YEAR · US AND CANADA"),
         text="In America and Canada, more than 92 percent of members renew every year.",
         say="In America and Canada, more than ninety-two percent of members renew every year."),
    dict(floor=2, id="bait", air=1, text="The cheap things are bait. And Costco pays for the bait itself."),
    dict(floor=2, id="galanti", text="In 2015, its finance chief said Costco was willing to give up $30 to $40 million a year of margin to hold the chicken at $4.99.",
         say="In twenty fifteen, its finance chief said Costco was willing to give up thirty to forty million dollars a year of margin to hold the chicken at four ninety-nine."),
    dict(floor=2, id="plant", card=("$450 MILLION", "COSTCO'S OWN CHICKEN PLANT · NEBRASKA · 2019"),
         text="Then it built its own $450 million chicken plant in Nebraska, to keep that price where it is.",
         say="Then it built its own four hundred and fifty million dollar chicken plant in Nebraska, to keep that price where it is."),
    dict(floor=2, id="sold", card=("157 MILLION", "ROTISSERIE CHICKENS SOLD · 2025"),
         text="In 2025 it sold 157 million of those chickens. Each one a reason to come back, and to keep the card.",
         say="In twenty twenty-five it sold a hundred and fifty-seven million of those chickens. Each one a reason to come back, and to keep the card."),
    # 3 · THE MONEY: why people pay to shop
    dict(floor=3, id="why", air=2, text="So why would anyone pay to go shopping?"),
    dict(floor=3, id="sunk", text="Because a fee you've already paid changes how you shop. You want your money's worth. So you come back, and you buy more each time."),
    dict(floor=3, id="week", card=("$1.25", "A BASIC MEMBERSHIP, PER WEEK"),
         text="Spread over a year, a basic membership costs about $1.25 a week. Less than the hot dog.",
         say="Spread over a year, a basic membership costs about a dollar twenty-five a week. Less than the hot dog."),
    dict(floor=3, id="exec", card=("$130", "EXECUTIVE MEMBERSHIP · 2% BACK, UP TO $1,250"),
         text="Then there's the upgrade. For $130, an Executive member gets 2 percent back on most purchases, up to $1,250 a year.",
         say="Then there's the upgrade. For a hundred and thirty dollars, an Executive member gets two percent back on most purchases, up to twelve hundred and fifty dollars a year."),
    dict(floor=3, id="execs", card=("42.3 MILLION", "EXECUTIVE MEMBERS · AUG 2026"),
         text="Half of Costco's paid members now have it: 42 million people, paying double the fee to be rewarded for spending more.",
         say="Half of Costco's paid members now have it: forty-two million people, paying double the fee to be rewarded for spending more."),
    dict(floor=3, id="rise", card=("$60 → $65", "THE FIRST FEE RISE IN SEVEN YEARS · SEPT 2024"),
         text="In September 2024, Costco raised the fee for the first time in seven years: from $60 to $65, and from $120 to $130.",
         say="In September twenty twenty-four, Costco raised the fee for the first time in seven years: from sixty dollars to sixty-five, and from a hundred and twenty to a hundred and thirty."),
    dict(floor=3, id="stayed", text="Two years later, renewals in America and Canada are still above 92 percent.",
         say="Two years later, renewals in America and Canada are still above ninety-two percent."),
    dict(floor=3, id="never", cut=True, text="When a fee goes up and almost no one leaves, the fee was never the reason people came. The prices were. And the prices are paid for by the fee."),
    # 4 · YOU: is it worth it for you?
    dict(floor=4, id="you", air=2, text="So is it worth it for you?"),
    dict(floor=4, id="basic", text="The basic card pays off only if Costco saves you more than the fee. That depends on what you buy, not on how cheap the chicken is."),
    dict(floor=4, id="upgrade", card=("$3,250", "YEARLY SPEND WHERE THE UPGRADE PAYS FOR ITSELF · US"),
         text="The upgrade has a simple test. The extra $65 only comes back if you spend more than $3,250 a year there. About $63 a week.",
         say="The upgrade has a simple test. The extra sixty-five dollars only comes back if you spend more than three thousand two hundred and fifty dollars a year there. About sixty-three dollars a week."),
    dict(floor=4, id="uk", card=("£2,100", "THE SAME LINE IN BRITAIN"),
         text="In Britain, the line is about £2,100 a year.",
         say="In Britain, the line is about two thousand one hundred pounds a year."),
    dict(floor=4, id="spoil", text="Bulk only saves money if you use it before it spoils. A bargain you throw away costs more than the small pack."),
    dict(floor=4, id="unit", text="Check the unit price on the shelf label, not the price of the pack. Big isn't always cheaper."),
    dict(floor=4, id="list", text="And remember why the cheap things are there: to get you through the door. Everything between the door and the hot dog is where the basket fills up."),
    dict(floor=4, id="go", cut=True, text="Go with a list. The fee only pays if the list does."),
    # 5 · WHAT IF
    dict(floor=5, id="imagine", air=3, cut=True, text="So imagine one more step."),
    dict(floor=5, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=5, id="scene", text="A shop that sells everything at exactly what it paid. No markup at all. It earns only from the door, and the door costs more each year."),
    dict(floor=5, id="subs", text="Your phone, your films, your music, even your printer's ink: more and more of what you buy is a fee to keep access."),
    dict(floor=5, id="question", air=1, text="At what point are you not a customer, but a subscriber?"),
    # 6 · THE CLOSE: mirrored
    dict(floor=6, id="then", air=2, cut=True, text="At Costco, a hot dog and a drink still cost $1.50.",
         say="At Costco, a hot dog and a drink still cost a dollar fifty."),
    dict(floor=6, id="close", cut=True, text="The hot dog gets you in. The card keeps you coming back."),
]

FLOORS = ["THE PRICE", "THE MACHINE", "THE PROOF", "THE MONEY", "YOU", "WHAT IF", "THE CLOSE"]

SOURCES = [
    "Costco Wholesale, fourth quarter and fiscal 2026 results (24 Sep 2026), 52 weeks to 30 Aug 2026: net sales "
    "$297,247M; membership fees $5,907M; operating income $11,685M; net income $9,226M (investor.costco.com)",
    "Costco Q4 fiscal 2026 earnings call (Sep 2026): 84.1M paid members, 150.4M cardholders, 42.3M paid Executive "
    "members; renewal rate 92.3% US and Canada, 89.8% worldwide (Motley Fool and GuruFocus transcripts)",
    "Two cents per dollar: (operating income minus membership fees) / net sales = ($11,685M - $5,907M) / $297,247M, "
    "about 1.9%; membership fees treated as having almost no direct cost",
    "Markup limits of 14% (brands) and 15% (Kirkland Signature) set by the founders, as widely reported (Yahoo Finance, "
    "Acquired); fewer than 4,000 active SKUs per warehouse (Costco Form 10-K)",
    "$1.50 hot dog and drink since 1985 (NPR, 3 Jun 2024); $4.99 rotisserie chicken since 2009; CFO Richard Galanti "
    "on giving up $30-40M a year of gross margin to hold the price (Seattle Times, 2015); $450M Lincoln Premium Poultry "
    "plant, Fremont, Nebraska, opened 2019; 157.4M rotisserie chickens sold in fiscal 2025 (Tasting Table)",
    "US fees $65 Gold Star and $130 Executive from 1 Sep 2024, up from $60 and $120, the first rise since 2017; "
    "Executive reward 2% up to $1,250 a year (Axios, 31 Aug 2024; Costco)",
    "UK fees £42 standard and £84 Executive, 2% back capped at £500; the upgrade pays above about £2,100 a year of "
    "spend (MoneySavingExpert, 2026)",
    "Upgrade break-even (US): the extra $65 / 2% = $3,250 a year, about $63 a week",
    "Price Club opened by Sol Price in San Diego in 1976; Costco co-founded by Jim Sinegal and Jeffrey Brotman in 1983; "
    "Costco and Price Club merged in 1993 (Costco; Encyclopaedia Britannica)",
    "The what-if is labelled as imagined, not a forecast",
]
