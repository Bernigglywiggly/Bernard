"""CHANNEL 2 · EP02 · THE LANDLORD IN THE GOLDEN ARCHES, v1 (1 Oct 2026): The Margin, film 2 (channel/channel2/BIBLE.md).

The hidden mechanism: McDonald's is paid by the restaurants, not by you. About 95% of its restaurants are run by
franchisees, who pay McDonald's a royalty and, for most, rent on a building McDonald's owns or leases. Rent is a share
of sales, with a minimum, so McDonald's is paid first, whether or not the restaurant makes a profit. In 2025 it took
$10.4B in rent, more than its whole net income ($8.6B), and more than all the food its own restaurants sold ($9.7B).

Voice: Curve Elder A (EL_VOICE=elder), calm and unhurried, never George. About 8-9 minutes at the engine's pace.
No jokes; straight in; every figure on screen with its source.

Fields as in The Curve's scripts: id, text (caption), say (spoken form), card (big number, small line), air, cut, floor.
"""

LINES = [
    # 0 · THE PRICE: the cold open
    dict(floor=0, id="rent", card=("$10.4 BILLION", "RENT COLLECTED BY McDONALD'S · 2025"),
         text="Last year, McDonald's collected $10.4 billion in rent.",
         say="Last year, McDonald's collected ten point four billion dollars in rent."),
    dict(floor=0, id="notyou", text="Not from you. From the people who run its restaurants."),
    dict(floor=0, id="profit", cut=True, card=("$8.6 BILLION", "McDONALD'S NET INCOME · 2025"),
         text="That rent was more than McDonald's made in profit all year: $8.6 billion.",
         say="That rent was more than McDonald's made in profit all year: eight point six billion dollars."),
    dict(floor=0, id="think", air=1, text="Most people think McDonald's is a burger company."),
    dict(floor=0, id="landlord", cut=True, text="The accounts describe something else. A landlord. And the burgers are how the rent gets paid."),
    # 1 · THE MACHINE: who pays whom
    dict(floor=1, id="count", air=1, card=("45,356", "McDONALD'S RESTAURANTS · END OF 2025"),
         text="There are about 45,000 McDonald's restaurants in the world.",
         say="There are about forty-five thousand McDonald's restaurants in the world."),
    dict(floor=1, id="franchised", card=("95%", "RUN BY FRANCHISEES, NOT BY McDONALD'S"),
         text="About 95 percent of them aren't run by McDonald's at all. They're run by franchisees: local business owners.",
         say="About ninety-five percent of them aren't run by McDonald's at all. They're run by franchisees: local business owners."),
    dict(floor=1, id="pays", text="The franchisee pays for the kitchen, the staff, the food and the electricity."),
    dict(floor=1, id="owns", card=("56% · 80%", "LAND · BUILDINGS OWNED BY McDONALD'S"),
         text="McDonald's keeps something else. In the markets it runs directly, it owns the land under more than half its restaurants, and about four in five of the buildings.",
         say="McDonald's keeps something else. In the markets it runs directly, it owns the land under more than half its restaurants, and about four in five of the buildings."),
    dict(floor=1, id="lease", text="Where it doesn't own the site, it usually leases it itself, and rents it on to the franchisee."),
    dict(floor=1, id="twice", card=("RENT + ROYALTY", "WHAT A FRANCHISEE PAYS McDONALD'S"),
         text="So most franchisees pay McDonald's twice. A royalty, for the name and the system. And rent, for the building."),
    dict(floor=1, id="keys", card=("$500,000", "OF THEIR OWN MONEY, NOT BORROWED · US FRANCHISEE"),
         text="To get the keys in America, a franchisee pays a $45,000 fee up front, and must have at least half a million dollars of their own money. Not borrowed.",
         say="To get the keys in America, a franchisee pays a forty-five thousand dollar fee up front, and must have at least half a million dollars of their own money. Not borrowed."),
    dict(floor=1, id="fitout", text="They pay for the kitchen equipment, the seating, the signs and the screens. McDonald's keeps the ground and the walls."),
    dict(floor=1, id="share", text="And the rent isn't a fixed amount. It's a share of sales, with a minimum."),
    dict(floor=1, id="every", text="Every burger, every coffee, every portion of fries: part of the money is rent."),
    dict(floor=1, id="first", cut=True, text="When sales rise, the rent rises. When food or wages cost more, that comes out of the franchisee's margin. Not the rent."),
    # 2 · THE PROOF: how it began, and what the filings show
    dict(floor=2, id="rescue", air=2, text="This wasn't an accident. It was a rescue."),
    dict(floor=2, id="kroc", card=("1.9%", "RAY KROC'S CUT OF EACH RESTAURANT'S SALES · 1950s"),
         text="In the 1950s, Ray Kroc, the salesman who turned McDonald's into a chain, took 1.9 percent of each restaurant's sales.",
         say="In the nineteen-fifties, Ray Kroc, the salesman who turned McDonald's into a chain, took one point nine percent of each restaurant's sales."),
    dict(floor=2, id="brothers", text="And half a percent of that went to the McDonald brothers, who had invented the system. It wasn't enough to build a company on.",
         say="And half a percent of that went to the McDonald brothers, who had invented the system. It wasn't enough to build a company on."),
    dict(floor=2, id="sonneborn", card=("1956", "FRANCHISE REALTY CORPORATION"),
         text="Then a finance man called Harry Sonneborn had an idea. Get the land first. Build the restaurant. Then rent it to the franchisee, at a markup.",
         say="Then a finance man called Harry Sonneborn had an idea. Get the land first. Build the restaurant. Then rent it to the franchisee, at a markup."),
    dict(floor=2, id="quote", text="He later put it bluntly: \"We are not technically in the food business. We are in the real estate business.\""),
    dict(floor=2, id="quote2", cut=True, text="\"The only reason we sell fifteen-cent hamburgers is because they are the greatest producer of revenue, from which our tenants can pay us our rent.\""),
    dict(floor=2, id="seventy", air=2, text="Seventy years later, the filings show how far that idea went."),
    dict(floor=2, id="paid", card=("$16.5 BILLION", "PAID TO McDONALD'S BY FRANCHISEES · 2025"),
         text="In 2025, franchisees paid McDonald's $16.5 billion. $10.4 billion of it was rent. About $6 billion was royalties.",
         say="In twenty twenty-five, franchisees paid McDonald's sixteen and a half billion dollars. Ten point four billion of it was rent. About six billion was royalties."),
    dict(floor=2, id="own", card=("$9.7 BILLION", "FOOD SOLD BY McDONALD'S OWN RESTAURANTS · 2025"),
         text="Its own restaurants, the ones it runs itself, sold $9.7 billion of food.",
         say="Its own restaurants, the ones it runs itself, sold nine point seven billion dollars of food."),
    dict(floor=2, id="more", cut=True, text="So McDonald's took in more from rent than from every meal it served itself."),
    dict(floor=2, id="margin", card=("~90%", "OF McDONALD'S RESTAURANT MARGIN CAME FROM FRANCHISEES · 2025"),
         text="And the rent side is where the profit is. Franchised restaurants produced about 90 percent of all the margin McDonald's restaurants earned.",
         say="And the rent side is where the profit is. Franchised restaurants produced about ninety percent of all the margin McDonald's restaurants earned."),
    dict(floor=2, id="dividend", card=("49 YEARS", "OF DIVIDEND RISES IN A ROW · SINCE 1976"),
         text="Rent is steady money. It's why McDonald's has been able to raise the dividend it pays its shareholders every year for 49 years.",
         say="Rent is steady money. It's why McDonald's has been able to raise the dividend it pays its shareholders every year for forty-nine years."),
    # 3 · THE MONEY: one meal, split
    dict(floor=3, id="where", air=2, text="So where does your money go?"),
    dict(floor=3, id="spent", card=("$139.4 BILLION", "SPENT AT McDONALD'S WORLDWIDE · 2025"),
         text="In 2025, people spent $139 billion at McDonald's restaurants around the world.",
         say="In twenty twenty-five, people spent a hundred and thirty-nine billion dollars at McDonald's restaurants around the world."),
    dict(floor=3, id="stays", text="Most of that stays with the franchisees, to pay for the food, the staff and the bills."),
    dict(floor=3, id="us", card=("13,700+", "McDONALD'S RESTAURANTS IN THE US · 2024"),
         text="In America alone there are more than 13,700 of them. About 95 percent are run by franchisees, and most of those are McDonald's tenants.",
         say="In America alone there are more than thirteen thousand seven hundred of them. About ninety-five percent are run by franchisees, and most of those are McDonald's tenants."),
    dict(floor=3, id="ten", card=("~$1.28 OF EVERY $10", "SPENT AT A FRANCHISED McDONALD'S GOES TO McDONALD'S"),
         text="But on average, of every ten dollars spent at a franchised McDonald's, about a dollar thirty goes to McDonald's itself.",
         say="But on average, of every ten dollars spent at a franchised McDonald's, about a dollar thirty goes to McDonald's itself."),
    dict(floor=3, id="eighty", text="About eighty cents of that is rent."),
    dict(floor=3, id="royalty", card=("4% → 5%", "US ROYALTY FOR NEW RESTAURANTS · FROM 2024"),
         text="And the share is growing. Since 2024, new restaurants in America pay a royalty of 5 percent of sales, up from 4: the first rise in nearly thirty years.",
         say="And the share is growing. Since twenty twenty-four, new restaurants in America pay a royalty of five percent of sales, up from four: the first rise in nearly thirty years."),
    dict(floor=3, id="term", card=("20 YEARS", "A TYPICAL McDONALD'S FRANCHISE AGREEMENT"),
         text="A franchise agreement usually runs for twenty years. Twenty years of rent, agreed in advance."),
    dict(floor=3, id="risk", text="Now look at it from the franchisee's side. They carry the wages, the food, the energy bills, and the risk."),
    dict(floor=3, id="flop", text="If a new menu flops, or a price war eats their margin, they take the hit. The rent still arrives."),
    dict(floor=3, id="before", cut=True, text="Because the money is tied to sales, not profit, McDonald's is paid before anyone knows whether the restaurant made money."),
    # 4 · YOU: what it means for your wallet
    dict(floor=4, id="you", air=2, text="So what does this mean for you?"),
    dict(floor=4, id="prices", card=("$5.29", "AVERAGE US BIG MAC · 2024, UP FROM $4.39 IN 2019"),
         text="When menu prices rise, the franchisee sets them. In 2024, McDonald's said the average Big Mac in America cost $5.29, up from $4.39 in 2019.",
         say="When menu prices rise, the franchisee sets them. In twenty twenty-four, McDonald's said the average Big Mac in America cost five dollars twenty-nine, up from four thirty-nine in twenty nineteen."),
    dict(floor=4, id="either", text="But a higher price means higher sales, and higher sales mean higher rent. The landlord wins either way."),
    dict(floor=4, id="deals", text="It also explains the deals and the app offers. More visits mean more sales, and more sales mean more rent, even when the deal itself barely pays."),
    dict(floor=4, id="lesson", text="The lesson isn't really about burgers. It's about owning the thing everyone else has to use."),
    dict(floor=4, id="franchise", text="If you ever think of buying a franchise, any franchise, read the lease before the menu. Find out who owns the building, and how much of every sale leaves before you're paid."),
    dict(floor=4, id="invest", text="If you invest, look past the product. Ask what the company actually charges for."),
    dict(floor=4, id="often", cut=True, text="Plenty of businesses that look like they sell one thing make their money from another."),
    # 5 · WHAT IF
    dict(floor=5, id="imagine", air=3, cut=True, text="So imagine one more step."),
    dict(floor=5, id="whatif", air=2, text="Not a forecast. A what-if."),
    dict(floor=5, id="street", text="Picture a whole high street run this way. The bakery, the gym, the coffee shop, each paying a share of every sale to the same landlord, who sets the rules and never has to cook."),
    dict(floor=5, id="already", text="Shopping centres already charge some tenants a share of their takings. Apps take a cut of every order. The idea is spreading."),
    dict(floor=5, id="question", air=1, text="At what point does the street work for the landlord?"),
    # 6 · THE CLOSE: mirrored
    dict(floor=6, id="then", air=2, cut=True, text="Last year, McDonald's collected $10.4 billion in rent.",
         say="Last year, McDonald's collected ten point four billion dollars in rent."),
    dict(floor=6, id="close", cut=True, text="The burgers bring in the customers. The customers pay the rent."),
]

FLOORS = ["THE PRICE", "THE MACHINE", "THE PROOF", "THE MONEY", "YOU", "WHAT IF", "THE CLOSE"]

SOURCES = [
    "McDonald's Corporation, Form 10-K for 2025 (filed Feb 2026): franchised revenues $16,548M (rents $10,442M, "
    "royalties $6,018M); company-operated sales $9,690M; franchised margins $13,930M, about 90% of restaurant margin "
    "dollars; net income $8,563M; 45,356 restaurants, about 95% franchised; the company owned about 56% of the land "
    "and 80% of the buildings for its restaurants; rent and royalties based on a percent of sales with minimum rent "
    "payments; franchise arrangements generally 20 years (SEC EDGAR)",
    "McDonald's fourth quarter and full year 2025 results (11 Feb 2026): systemwide sales $139.4B",
    "Per $10 maths: franchised sales = systemwide sales minus company-operated sales (about $129.7B); rents are about "
    "8.0% of that and royalties about 4.6%, together about 12.8%. An average across all franchised restaurants",
    "Ray Kroc's 1.9% service fee (0.5% to the McDonald brothers), Harry Sonneborn and Franchise Realty Corporation "
    "(1956), and Sonneborn's quote: John F. Love, McDonald's: Behind the Arches (Bantam, 1986)",
    "US franchisee requirements: $45,000 initial fee and at least $500,000 of non-borrowed personal resources; the "
    "franchisee pays for equipment, seating, signs and technology (McDonald's US business and franchising FAQ)",
    "49 consecutive annual dividend increases since 1976 (McDonald's dividend release, 22 Oct 2025)",
    "US royalty for new restaurants raised from 4% to 5% from 1 Jan 2024, the first rise in nearly three decades "
    "(CNN, 22 Sep 2023; McDonald's supplemental information on franchisor updates)",
    "Average US Big Mac $5.29 in 2024 against $4.39 in 2019; franchisees set their own prices (McDonald's USA "
    "president Joe Erlinger's open letter, 29 May 2024; CNN, CNBC)",
    "More than 13,700 US restaurants, 95% franchisee-operated (Erlinger's open letter, 29 May 2024)",
    "The what-if is labelled as imagined, not a forecast",
]
