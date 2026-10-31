"""MONEY CRIMES · long-form 03: "The Salad Oil Swindle" (Tino De Angelis, 1963), v0 draft (5 Oct 2026). Narrated by
Imogen, as films 01 and 02.

NOT YET VERIFIED: every figure rests on secondary sources (see FACTS.md). Before voicing, a checker verifies each claim
against Norman C. Miller's The Great Salad Oil Swindle (1965), contemporary reports and Buffett's partnership letters;
lines marked TO VERIFY in FACTS.md change with what the record says. Where sources differ the script takes the cautious
line ("more than 150 million dollars" covers both the $175M and $180M counts; "more than a third" for the share price).

Structure (CRAFT.md §1, unlike films 01-02's life story): the film is built like the tanks. It opens on the top layer,
the inspection everyone saw, then goes down a layer per chapter (the oil, the paper, the crash, the guarantor) and ends
on what the inspector was standing on. The point of view is in the close: every check was real and every one was
pointed where it was told to look. Narration: professor's pace, one number per sentence, no staccato runs (CRAFT §2).
"""
CHAPTERS = [
    dict(id="open", title="The top of the tank", paras=[
        "Bayonne, New Jersey, in the early 1960s. An inspector climbs a ladder on the side of a storage tank the size of a house, "
        "opens the hatch at the top, and lowers a sampling tube into the dark.",
        "What comes back up is vegetable oil, thick and golden, exactly what the paperwork says should be there. He "
        "writes it down, signs the form, and walks over to the next tank.",
        "Those signatures were worth a great deal of money. Banks lent against them, brokers traded on them, and one of "
        "the most trusted names in American finance stood behind them.",
        "Most of what the inspector was standing on, though, was water. By the time anyone looked properly, more than "
        "150 million dollars had been lent against oil that did not exist.",
        "This is the story of how one company borrowed against an ocean of salad oil, why every check on it passed, and "
        "why a young investor in Omaha named Warren Buffett looked at the wreckage and saw an opportunity.",
    ]),
    dict(id="king", title="The salad oil king", paras=[
        "The man behind the tanks was Anthony De Angelis, known to everyone as Tino. His company, Allied Crude Vegetable "
        "Oil Refining, bought, stored and sold edible oils on a very large scale.",
        "Oil is a comfortable thing for a lender to hold as security. It sits in a tank, it has a market price, and if a "
        "loan goes bad it can be sold quickly.",
        "So the arrangement looked sound. Allied's oil went into storage, an independent warehouse company counted it "
        "and issued receipts, and those receipts went to the lenders as collateral.",
        "The warehouse company was a subsidiary of American Express, called American Express Warehousing. A "
        "receipt with that name on it was treated almost like cash.",
    ]),
    dict(id="trick", title="Oil floats", paras=[
        "The trick began with something every cook knows. Oil floats on water.",
        "Allied's tanks held a little oil and a great deal of water underneath it. A sample drawn from the top came up "
        "as pure oil, and the top was where the samples were drawn.",
        "Some tanks, according to later accounts, had hidden compartments inside them, so a measuring rod dropped "
        "through the hatch found oil in one small section while the rest of the tank held water.",
        "The tanks were also connected by pipes. Oil could be pumped from one tank to the next ahead of the inspectors, "
        "so the same oil was counted more than once.",
        "Later still, the receipts themselves were forged, and at that point the oil was hardly needed at all.",
        "There was one more weakness, and it mattered most. The custodians who looked after the oil on behalf of the "
        "lenders were Allied's own people, men who answered to De Angelis.",
    ]),
    dict(id="paper", title="Paper oil", paras=[
        "Receipts became loans, and the loans paid for more receipts. By the usual account, Allied claimed about 900,000 "
        "tons of oil as collateral.",
        "The tanks held perhaps 60,000 tons, and not all of that was oil.",
        "It was later reported that at one point Allied's claimed stocks were as large as the government's own count "
        "of all the soybean and cottonseed oil in the United States.",
        "No one added that up while the money was flowing. Each lender saw its own receipts, and each receipt looked "
        "fine on its own.",
        "In the end, 51 banks and firms had lent against them.",
    ]),
    dict(id="fall", title="November 1963", paras=[
        "By 1963 De Angelis was also betting heavily on the price of soybean and cottonseed oil, buying futures contracts through Wall "
        "Street brokers in the belief that prices would keep rising.",
        "Then the price fell. Allied could not meet its brokers' demands for cash, and in November the whole structure "
        "gave way in a matter of days.",
        "Allied filed for bankruptcy on the 19th of November, 1963.",
        "Three days later, President Kennedy was shot in Dallas, and the country's attention went somewhere else entirely.",
        "Underneath the headlines, a Wall Street brokerage, Ira Haupt and Company, had collapsed. It had financed De "
        "Angelis's trading, and the receipts it held were worthless.",
        "To protect Haupt's ordinary customers, the New York Stock Exchange stepped in with up to 12 million dollars of its members' money, and Haupt's banks agreed to wait for theirs.",
    ]),
    dict(id="checked", title="Who checked?", paras=[
        "When investigators finally opened the tanks and looked all the way down, they found water.",
        "American Express Warehousing faced about 210 million dollars of claims.",
        "It had about 130,000 dollars of assets to meet them.",
        "The parent company's whole business, from charge cards to travellers' cheques, depended on people trusting its "
        "name. American Express eventually settled the claims for about 60 million dollars.",
        "Its share price fell by more than a third.",
        "De Angelis pleaded guilty, and in 1965 he was sentenced to 20 years in prison. He was released in 1972.",
    ]),
    dict(id="buyer", title="The buyer", paras=[
        "In Omaha, a young investment manager named Warren Buffett read the same news and came to a different "
        "conclusion.",
        "His reasoning, as he and his biographers later told it, was that the scandal had damaged the company's balance "
        "sheet without touching its customers. People were still paying with American Express cards and cheques.",
        "He put a large part of his partnership's money into American Express shares while they were cheap, and it "
        "became one of the best investments of his early career.",
    ]),
    dict(id="close", title="Underneath", paras=[
        "Every safeguard in this story was real. The inspectors inspected, the receipts were signed, and the lenders "
        "kept careful files.",
        "Each check answered the question it was asked, and every one of those questions was about the top of the tank.",
        "That's the part I'd keep. When someone shows you proof, it's worth asking who decided where you would look.",
        "As for the oil, what little there was had been floating on the water all along.",
    ]),
]
