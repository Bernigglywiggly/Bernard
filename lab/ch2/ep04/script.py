"""HOW THEY PROFIT · EP04 · THE CLOUD BEHIND THE CART, v1 (4 Oct 2026): film 4 (channel/channel2/BIBLE.md).

The hidden mechanism: the shop everyone sees runs on thin margins; most of Amazon's profit comes from renting out
computers. In 2025 AWS was 18% of Amazon's $716.9B of sales and 57% of its $80.0B operating profit ($45.6B on
$128.7B of sales). The two shop segments, which already include the advertising and the sellers' fees, made $34.3B
on $588.2B. Around the shop sit the businesses that charge sellers: a 15% commission in most categories, delivery
fees, and $68.6B of advertising.

Voice: Higgsfield Seed Audio "Sterling" (engine/voice_hf.py), calm and unhurried. About 8 minutes at the engine's pace.
No jokes; straight in; every figure on screen with its source. No logos: the shop, the boxes and the servers are plain
line drawings.

Fields as in The Curve's scripts: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · THE PRICE: the cold open
    dict(floor=0, id="sales", card=("$716.9 BILLION", "AMAZON'S NET SALES · 2025"),
         text="Last year, Amazon's sales came to $717 billion.",
         say="Last year, Amazon's sales came to seven hundred and seventeen billion dollars."),
    dict(floor=0, id="boxes", text="Most of that was shopping: the website, the warehouses, the vans, the boxes at your door."),
    dict(floor=0, id="most", cut=True, card=("57%", "OF AMAZON'S OPERATING PROFIT · 2025 · FROM ONE BUSINESS"),
         text="But 57 percent of its profit came from a business most shoppers never see.",
         say="But fifty-seven percent of its profit came from a business most shoppers never see."),
    dict(floor=0, id="rents", air=1, text="It doesn't sell anything you can hold. It rents out computers."),
    dict(floor=0, id="front", cut=True, text="The shop is what you see. Most of the profit is somewhere else."),
    # 1 · THE MACHINE: five businesses behind one website
    dict(floor=1, id="five", air=1, text="Amazon is really five businesses behind one website."),
    dict(floor=1, id="shop", card=("$265 BILLION", "AMAZON'S OWN ONLINE SALES · 2025"),
         text="The first is the shop you know. Amazon buys goods, stores them and sells them to you: $265 billion of them last year.",
         say="The first is the shop you know. Amazon buys goods, stores them and sells them to you: two hundred and sixty-five billion dollars of them last year."),
    dict(floor=1, id="market", card=("61%", "OF ITEMS SOLD ON AMAZON · FROM OTHER SELLERS · Q4 2025"),
         text="The second is a marketplace. About six in ten things sold on Amazon come from other sellers, not from Amazon itself.",
         say="The second is a marketplace. About six in ten things sold on Amazon come from other sellers, not from Amazon itself."),
    dict(floor=1, id="commission", card=("15%", "AMAZON'S COMMISSION ON EACH SALE · MOST CATEGORIES"),
         text="They pay Amazon to be there: a commission on every sale, 15 percent in most categories. And if Amazon stores and ships their goods, a fee for that too.",
         say="They pay Amazon to be there: a commission on every sale, fifteen percent in most categories. And if Amazon stores and ships their goods, a fee for that too."),
    dict(floor=1, id="sellers", card=("$172 BILLION", "PAID BY OTHER SELLERS FOR AMAZON'S SERVICES · 2025"),
         text="Last year those sellers paid Amazon $172 billion.",
         say="Last year those sellers paid Amazon a hundred and seventy-two billion dollars."),
    dict(floor=1, id="ads", text="The third business is advertising. Search for almost anything, and the first results you see are often adverts, paid for by sellers and brands."),
    dict(floor=1, id="adsum", card=("$68.6 BILLION", "AMAZON'S ADVERTISING SALES · 2025"),
         text="In 2025, they paid Amazon $68.6 billion to be seen.",
         say="In twenty twenty-five, they paid Amazon sixty-eight point six billion dollars to be seen."),
    dict(floor=1, id="prime", card=("$49.6 BILLION", "SUBSCRIPTIONS, PRIME INCLUDED · 2025"),
         text="The fourth is subscriptions, Prime among them: almost $50 billion more.",
         say="The fourth is subscriptions, Prime among them: almost fifty billion dollars more."),
    dict(floor=1, id="cloud", text="And the fifth isn't a shop at all. Amazon Web Services rents computing power to other companies: servers, storage, and the machines behind countless apps and websites."),
    dict(floor=1, id="anyone", cut=True, text="Start-ups, banks, governments. If you've used an app today, there's a good chance some of it ran on Amazon's computers."),
    # 2 · THE PROOF: how it began, and what the accounts show
    dict(floor=2, id="began", air=2, text="It began as a way to rent out the kind of computing Amazon had built to run its own shop."),
    dict(floor=2, id="launch", card=("2006", "AMAZON WEB SERVICES OPENS TO THE PUBLIC"),
         text="In 2006, it started selling storage and computing time to anyone, by the hour.",
         say="In two thousand and six, it started selling storage and computing time to anyone, by the hour."),
    dict(floor=2, id="silent", text="For years, Amazon didn't say how much money that made. It was hidden inside the shop's numbers."),
    dict(floor=2, id="reveal", card=("$265 MILLION", "AWS OPERATING PROFIT · FIRST QUARTER 2015"),
         text="In April 2015, Amazon showed the figures for the first time. The side business was already making a profit: $265 million in three months.",
         say="In April twenty fifteen, Amazon showed the figures for the first time. The side business was already making a profit: two hundred and sixty-five million dollars in three months."),
    dict(floor=2, id="ten", air=1, text="Ten years later, here's what the 2025 accounts show.",
         say="Ten years later, here's what the twenty twenty-five accounts show."),
    dict(floor=2, id="north", card=("$29.6 BILLION", "OPERATING PROFIT · NORTH AMERICA · ON $426 BILLION OF SALES"),
         text="Amazon's shops in North America sold $426 billion and made $29.6 billion of operating profit. About seven cents in every dollar.",
         say="Amazon's shops in North America sold four hundred and twenty-six billion dollars and made twenty-nine point six billion of operating profit. About seven cents in every dollar."),
    dict(floor=2, id="world", card=("$4.7 BILLION", "OPERATING PROFIT · REST OF THE WORLD · ON $162 BILLION"),
         text="In the rest of the world: $162 billion of sales, $4.7 billion of profit. Under three cents a dollar.",
         say="In the rest of the world: a hundred and sixty-two billion dollars of sales, four point seven billion of profit. Under three cents a dollar."),
    dict(floor=2, id="include", text="And those shop numbers already include the sellers' fees and the advertising."),
    dict(floor=2, id="aws", card=("$45.6 BILLION", "AWS OPERATING PROFIT · ON $128.7 BILLION OF SALES · 2025"),
         text="Now the cloud. AWS sold $128.7 billion of computing, and made $45.6 billion. Thirty-five cents in every dollar.",
         say="Now the cloud. A W S sold a hundred and twenty-eight point seven billion dollars of computing, and made forty-five point six billion. Thirty-five cents in every dollar."),
    dict(floor=2, id="share", cut=True, card=("18% · 57%", "AWS'S SHARE OF AMAZON'S SALES · AND OF ITS PROFIT"),
         text="Eighteen percent of Amazon's sales. Fifty-seven percent of its profit."),
    dict(floor=2, id="hidden", text="Amazon doesn't say how much profit its advertising makes. It counts it inside the shop."),
    dict(floor=2, id="van", text="But an advert needs no warehouse, no van and no driver."),
    dict(floor=2, id="bet", air=1, card=("$131.8 BILLION", "AMAZON'S CAPITAL SPENDING · 2025 · UP FROM $83.0 BILLION"),
         text="And Amazon is betting on the cloud. In 2025 it spent $131.8 billion on buildings and equipment, up from $83 billion the year before.",
         say="And Amazon is betting on the cloud. In twenty twenty-five it spent a hundred and thirty-one point eight billion dollars on buildings and equipment, up from eighty-three billion the year before."),
    dict(floor=2, id="jassy", text="Its chief executive, Andy Jassy, said the spending was predominantly in AWS, because demand was very high.",
         say="Its chief executive, Andy Jassy, said the spending was predominantly in A W S, because demand was very high."),
    dict(floor=2, id="plan", cut=True, card=("~$200 BILLION", "AMAZON'S PLANNED CAPITAL SPENDING · 2026"),
         text="For 2026, Amazon has said it plans to spend about $200 billion.",
         say="For twenty twenty-six, Amazon has said it plans to spend about two hundred billion dollars."),
    # 3 · THE MONEY: the seller's side
    dict(floor=3, id="where", air=2, text="So where does your money go when you buy from a seller on Amazon?"),
    dict(floor=3, id="split", text="Part goes to the seller. Part goes to Amazon, as the commission. Part pays for the warehouse and the delivery."),
    dict(floor=3, id="adcost", text="And part may already have gone on the advert that put the product in front of you."),
    dict(floor=3, id="toll", card=("45¢", "OF EACH $1 A SELLER TAKES, PAID BACK TO AMAZON · ONE ESTIMATE, 2023"),
         text="By one estimate, from a group that campaigns against Amazon's power, sellers now pay Amazon about 45 cents of every dollar they take, in commissions, delivery fees and advertising.",
         say="By one estimate, from a group that campaigns against Amazon's power, sellers now pay Amazon about forty-five cents of every dollar they take, in commissions, delivery fees and advertising."),
    dict(floor=3, id="choose", text="Sellers don't have to use the warehouses or buy the adverts. But on the busiest shop in the world, it's hard to be found without them."),
    dict(floor=3, id="somewhere", text="And every fee has to come from somewhere: the seller's margin, or the price."),
    dict(floor=3, id="flywheel", text="The shop brings the customers. The customers bring the sellers. The sellers pay for the adverts."),
    dict(floor=3, id="engine", cut=True, text="And the computers that run all of it are rented out to everyone else, at thirty-five cents of profit in the dollar."),
    # 4 · YOU
    dict(floor=4, id="you", air=2, cut=True, text="So what does this mean for you?"),
    dict(floor=4, id="sponsored", text="When you search on Amazon, look for the word Sponsored. Those results paid to be there."),
    dict(floor=4, id="top", text="The first result isn't always the best one. Sometimes it's just the one that paid."),
    dict(floor=4, id="compare", text="Scroll past the adverts, check who the seller is, and compare the price with the same thing elsewhere."),
    dict(floor=4, id="sell", text="If you sell on Amazon, count every fee before you set a price: the commission, the storage, the delivery, the adverts, the returns."),
    dict(floor=4, id="invest", text="And if you invest, read the segment table, not the headline sales. It shows where a company really earns its money."),
    dict(floor=4, id="parcel", cut=True, text="The parcel at your door is the part you see. The profit is in the parts you don't."),
    # 5 · WHAT IF
    dict(floor=5, id="imagine", air=3, cut=True, text="So imagine one more step."),
    dict(floor=5, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=5, id="agent", text="Picture shopping done for you by an AI assistant. You ask for a lamp, and it simply picks one."),
    dict(floor=5, id="paid", text="Today, sellers pay to be at the top of the page. Who will pay to be the assistant's choice?"),
    dict(floor=5, id="same", text="And if one company runs the shop, sells the adverts, and rents out the computers the assistant runs on..."),
    dict(floor=5, id="question", air=1, text="Who is the assistant really working for?"),
    # 6 · THE CLOSE: mirrored
    dict(floor=6, id="then", air=2, cut=True, text="Last year, Amazon's sales came to $717 billion.",
         say="Last year, Amazon's sales came to seven hundred and seventeen billion dollars."),
    dict(floor=6, id="close", cut=True, text="You see the boxes. The profit is in the cloud."),
]

FLOORS = ["THE PRICE", "THE MACHINE", "THE PROOF", "THE MONEY", "YOU", "WHAT IF", "THE CLOSE"]

SOURCES = [
    "Amazon.com, Inc., fourth quarter and full year 2025 results (Form 8-K, Exhibit 99.1, Feb 2026): net sales $716.9B "
    "(2024: $638.0B); operating income $80.0B; net income $77.7B; segments: North America sales $426.3B, operating "
    "income $29.6B; International sales $161.9B, operating income $4.7B; AWS sales $128.7B, operating income $45.6B; "
    "net sales by group: online stores $265.3B, third-party seller services $172.3B, advertising services $68.6B, "
    "subscription services $49.6B, physical stores $22.6B (SEC EDGAR)",
    "AWS's shares: $128.7B / $716.9B = 18% of sales; $45.6B / $80.0B = 57% of operating income; operating margin "
    "$45.6B / $128.7B = 35%; North America 6.9%; International 2.9%",
    "Third-party sellers' share of paid units: 61% in Q4 2025 (Amazon supplemental data, as reported by seller-analytics "
    "publications)",
    "Referral fees of 15% in most categories (Amazon Seller Central fee schedule); Fulfillment by Amazon fees per item",
    "AWS public launch: Amazon S3 (14 Mar 2006) and EC2 (25 Aug 2006) (AWS press releases)",
    "Amazon first quarter 2015 results (23 Apr 2015): AWS segment broken out for the first time, sales $1.57B, "
    "operating income $265M (Amazon; AWSInsider, 23 Apr 2015)",
    "Capital expenditures (purchases of property and equipment) $131.8B in 2025, $83.0B in 2024 (Form 8-K, Feb 2026); "
    "Andy Jassy on the Q4 2025 call: 'predominantly in AWS, because we have very high demand'; about $200B of capital "
    "spending planned for 2026 (Amazon Q4 2025 call; CNBC, Yahoo Finance, Feb 2026)",
    "Institute for Local Self-Reliance, 'Amazon's Monopoly Tollbooth in 2023' (Dec 2023): Amazon's fees took an "
    "average of 45% of independent sellers' revenue (commissions, fulfillment fees, advertising); ILSR campaigns "
    "against Amazon's market power",
    "The what-if is labelled as imagined, not a forecast",
]
