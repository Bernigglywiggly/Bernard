"""THE MARGIN · EP03 · THE $65 MEMBERSHIP: the storyboard (ch2/kit.py) in the ledger look, keyed to the script's line ids
and the narrator's words. No logos: the warehouse, the card and the food are plain line drawings.

  I THE PRICE    $1.50 since 1985; the $4.99 chicken; $9.2 billion profit; the card in your wallet
  II THE MACHINE pay to get in: $65 · £42; Price Club 1976; 14% · 15%; fewer than 4,000 products; pallets; near cost
  III THE PROOF  the FY2026 receipt: fees $5.9B, operating profit $11.7B, half; $297B of goods at ~2¢ a dollar;
                 84.1M members, 92.3% renew; the bait: $30-40M a year, a $450M plant, 157M chickens
  IV THE MONEY   the sunk fee; $1.25 a week; the $130 upgrade; 42.3M; $60 → $65; still 92%
  V YOU          the upgrade's line: $3,250 (£2,100); bulk spoils; unit prices; go with a list
  VI WHAT IF     a shop at cost, a door that costs more; customer or subscriber?
  VII THE CLOSE  $1.50 again; the hot dog gets you in, the card keeps you coming back
"""
import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402
from ch2 import ledger  # noqa: E402
from ch2.kit import (Board, Beat, CX, CY, W, H, PAPER, BRASS, RED, MUTED, INK, number, statement, floor_card, stamp,  # noqa: E402
                     receipt, split, node, arrow, typed, serif, source, coins, person, card, warehouse, hotdog, cup, chicken,
                     bars, ticks, quote, icon_row, ease, seg, lerp)

TRAILS, GLINTS = [], []
FY = "COSTCO, FISCAL 2026 RESULTS (24 SEP 2026)"
CALL = "COSTCO Q4 FISCAL 2026 EARNINGS CALL"


def door(c, b):
    warehouse(c, CX, 600, 330, b.k(b.t0, 0.6))
    k = b.k(b.w("door", "pay") - 0.2, 0.5)
    if k > 0:
        card(c, CX, 520, 200 * k + 1, 1.0, BRASS, "MEMBER")
    typed(c, b, "YOU PAY TO GET IN", CX, 760, b.w("door", "pay") - 0.1, 28, BRASS)


def pallets(c, b):
    for i in range(10):
        x, y = 320 + (i % 5) * 300, 330 + (i // 5) * 230
        k = b.k(b.t0 + 0.1 * i, 0.4)
        if k <= 0:
            continue
        c.drawRect(skia.Rect.MakeXYWH(x - 100, y + 60, 200, 14), L.stroke(MUTED, 1.6, k))
        for j in range(3):
            c.drawLine(x - 90 + j * 90, y + 74, x - 90 + j * 90, y + 84, L.stroke(MUTED, 1.6, k))
        for r in range(2):
            for q in range(3):
                c.drawRect(skia.Rect.MakeXYWH(x - 96 + q * 64, y - 60 + r * 60, 62, 58), L.stroke(PAPER, 1.4, 0.85 * k))
    typed(c, b, "NO DECORATION · NO ADVERTS IN THE AISLES · NO WASTED SPACE", CX, 820, b.w("pallets", "decoration,") - 0.3, 22, BRASS)


def bait(c, b):
    hotdog(c, 620, 430, 130, b.k(b.t0, 0.5))
    cup(c, 860, 430, 70, b.k(b.t0 + 0.2, 0.5))
    chicken(c, 1300, 450, 130, b.k(b.t0 + 0.3, 0.5))
    stamp(c, b, "BAIT", CX, 700, b.w("bait", "bait.") - 0.3, RED, 64)
    typed(c, b, "AND COSTCO PAYS FOR IT", CX, 830, b.w("bait", "pays") - 0.3, 26, PAPER)


BOARD = Board([
    # I · THE PRICE
    Beat("hotdog", lambda c, b: (hotdog(c, 760, 380, 150, b.k(b.t0, 0.5)), cup(c, 1100, 380, 80, b.k(b.t0 + 0.2, 0.5)),
                                 serif(c, b, "$1.50", CX, 640, b.w("hotdog", "fifty.") - 0.4, 150),
                                 typed(c, b, "A HOT DOG AND A DRINK · THE SAME PRICE SINCE 1985", CX, 730, b.w("hotdog", "same") - 0.3, 26),
                                 source(c, b, "NPR, 3 JUN 2024"))),
    Beat("chicken", lambda c, b: (chicken(c, CX, 360, 160, b.k(b.t0, 0.5)),
                                  serif(c, b, "$4.99", CX, 640, b.w("chicken", "ninety-nine.") - 0.4, 150),
                                  typed(c, b, "TENS OF MILLIONS OF DOLLARS A YEAR TO KEEP IT THERE", CX, 730, b.w("chicken", "tens") - 0.3, 26),
                                  source(c, b, "COSTCO'S FINANCE CHIEF, SEATTLE TIMES, 2015"))),
    Beat("profit", lambda c, b: number(c, b, "$9.2 billion", "COSTCO'S PROFIT · YEAR TO AUGUST 2026", src=FY)),
    Beat("how", lambda c, b: statement(c, b, ["How does a shop with prices like that", ("make so much money?", b.w("how", "money?") - 0.4)],
                                       size=72, face=L.SERIF_I)),
    Beat("card", lambda c, b: (card(c, CX, 420, 440 * b.k(b.w("card", "card") - 0.3, 0.6, "o") + 1, 1.0, BRASS, "MEMBER"),
                               serif(c, b, "The card in your wallet.", CX, 720, b.w("card", "card") - 0.1, 70, PAPER))),
    # II · THE MACHINE
    Beat("door", lambda c, b: floor_card(c, b, "II", "The Machine", "CHARGE FOR THE DOOR. SELL AT COST.")),
    Beat(("door", "pay"), door),
    Beat("fee", lambda c, b: (number(c, b, "$65 · £42", "A YEAR · BASIC MEMBERSHIP · US · UK",
                                     src="COSTCO (US, FROM 1 SEP 2024); MONEYSAVINGEXPERT (UK, 2026)"))),
    Beat("buys", lambda c, b: statement(c, b, ["No goods. No credit.", ("Only the right to walk in and buy.", b.w("buys", "only") - 0.3)], size=72)),
    Beat("promise", lambda c, b: statement(c, b, ["In return: low prices.", ("And it holds itself to that.", b.w("promise", "holds") - 0.3)], size=72)),
    Beat("price", lambda c, b: (number(c, b, "1976", "SOL PRICE OPENS PRICE CLUB · SAN DIEGO", y=400),
                                typed(c, b, "A WAREHOUSE THAT CHARGED SMALL BUSINESSES A FEE TO SHOP", CX, 620, b.w("price", "charged") - 0.3, 24, PAPER),
                                source(c, b, "COSTCO; ENCYCLOPAEDIA BRITANNICA"))),
    Beat("sinegal", lambda c, b: (ticks(c, b, [("1983: Jim Sinegal and Jeffrey Brotman found Costco.", b.t0 + 0.2),
                                               ("1993: Costco and Price Club merge.", b.w("sinegal", "later,") - 0.3)], b.t0, x=360, y=420, size=50))),
    Beat("caps", lambda c, b: (number(c, b, "14% · 15%", "MOST IT MARKS UP · BRANDS · ITS OWN KIRKLAND SIGNATURE",
                                      src="AS WIDELY REPORTED (YAHOO FINANCE; ACQUIRED)"),
                               stamp(c, b, "THE RULE", 1500, 260, b.w("caps", "rule,") - 0.2, BRASS, 40))),
    Beat("fewer", lambda c, b: (number(c, b, "< 4,000", "PRODUCTS IN A WAREHOUSE · BOUGHT IN ENORMOUS QUANTITIES", src="COSTCO FORM 10-K"),
                                typed(c, b, "SO SUPPLIERS CUT THEIR PRICES", CX, 700, b.w("fewer", "suppliers") - 0.3, 26, PAPER))),
    Beat("pallets", pallets),
    Beat("thin", lambda c, b: statement(c, b, ["So the shelves run", ("close to cost.", b.w("thin", "cost.") - 0.4)], size=96)),
    Beat("pure", lambda c, b: (card(c, CX, 400, 360, b.k(b.t0, 0.5), BRASS, "MEMBER"),
                               typed(c, b, "COSTS ALMOST NOTHING TO COLLECT", CX, 640, b.w("pure", "costs") - 0.3, 26, PAPER),
                               serif(c, b, "Almost pure profit.", CX, 740, b.w("pure", "pure") - 0.3, 72, BRASS, face=L.SERIF_I))),
    # III · THE PROOF
    Beat("year", lambda c, b: floor_card(c, b, "III", "The Proof", "HOW MUCH OF THE BUSINESS IS THE FEE")),
    Beat("fees", lambda c, b: (receipt(c, b, 660, 110, 600, "COSTCO · YEAR TO AUG 2026", "THE ACCOUNTS",
                                       [("", ""), ("MEMBERSHIP FEES", "$5.9B"), ("OPERATING PROFIT", "$11.7B"), ("", ""), ("THE FEE'S SHARE", "~50%")],
                                       times=[None, b.w("fees", "five") - 0.2, b.w("opinc", "eleven") - 0.3, None, b.w("half", "half") - 0.3],
                                       circle=4),
                               source(c, b, FY + ": MEMBERSHIP FEES $5,907M; OPERATING INCOME $11,685M")), until="half"),
    Beat("goods", lambda c, b: (number(c, b, "$297 billion", "OF GOODS SOLD · THE OTHER HALF OF THE PROFIT", src=FY), )),
    Beat("cents", lambda c, b: (number(c, b, "~2¢", "OF PROFIT ON EVERY DOLLAR · BEFORE THE FEES", src="($11,685M − $5,907M) ÷ $297,247M ≈ 1.9%"),
                                coins(c, CX, 820, 1, 1.0, 26))),
    Beat("design", lambda c, b: statement(c, b, ["Not a weakness. The design.", ("Sell at almost no profit.", b.w("design", "sell") - 0.3),
                                                 ("Charge for the door.", b.w("design", "charge") - 0.3)], size=66, cols=[PAPER, PAPER, BRASS])),
    Beat("members", lambda c, b: (number(c, b, "84.1 million", "PAID MEMBERS · 150.4 MILLION CARDHOLDERS · AUG 2026", src=CALL))),
    Beat("renew", lambda c, b: number(c, b, "92.3%", "RENEW EVERY YEAR · US AND CANADA", src=CALL)),
    Beat("bait", bait),
    Beat("galanti", lambda c, b: (number(c, b, "$30–40 million", "A YEAR OF MARGIN · TO HOLD THE CHICKEN AT $4.99", size=140,
                                         src="RICHARD GALANTI, COSTCO CFO (SEATTLE TIMES, 2015)"))),
    Beat("plant", lambda c, b: (number(c, b, "$450 million", "ITS OWN CHICKEN PLANT · NEBRASKA · 2019", src="LINCOLN PREMIUM POULTRY"))),
    Beat("sold", lambda c, b: (number(c, b, "157 million", "ROTISSERIE CHICKENS SOLD · FISCAL 2025", src="COSTCO, AS REPORTED BY TASTING TABLE"),
                               typed(c, b, "EACH ONE A REASON TO KEEP THE CARD", CX, 700, b.w("sold", "reason") - 0.3, 26, BRASS))),
    # IV · THE MONEY
    Beat("why", lambda c, b: floor_card(c, b, "IV", "The Money", "WHY PEOPLE PAY TO SHOP")),
    Beat("sunk", lambda c, b: statement(c, b, ["A fee you've already paid", ("changes how you shop.", b.w("sunk", "changes") - 0.3),
                                               ("You come back. You buy more.", b.w("sunk", "come") - 0.3)], size=66, cols=[PAPER, PAPER, BRASS])),
    Beat("week", lambda c, b: (number(c, b, "$1.25", "A WEEK · A BASIC MEMBERSHIP", y=380),
                               typed(c, b, "LESS THAN THE HOT DOG", CX, 600, b.w("week", "less") - 0.3, 30, BRASS),
                               hotdog(c, CX, 720, 90, b.k(b.w("week", "hot") - 0.3, 0.5)))),
    Beat("exec", lambda c, b: (number(c, b, "$130", "EXECUTIVE · 2% BACK ON MOST PURCHASES · UP TO $1,250 A YEAR", src="COSTCO"))),
    Beat("execs", lambda c, b: (number(c, b, "42.3 million", "EXECUTIVE MEMBERS · HALF OF ALL PAID MEMBERS", src=CALL),
                                typed(c, b, "PAYING DOUBLE TO BE REWARDED FOR SPENDING MORE", CX, 690, b.w("execs", "double") - 0.3, 24, PAPER))),
    Beat("rise", lambda c, b: (number(c, b, "$60 → $65", "THE FIRST FEE RISE IN SEVEN YEARS · SEPT 2024", src="AXIOS, 31 AUG 2024"),
                               typed(c, b, "EXECUTIVE: $120 → $130", CX, 690, b.w("rise", "hundred") - 0.3, 26, PAPER))),
    Beat("stayed", lambda c, b: (number(c, b, "> 92%", "STILL RENEWING · TWO YEARS LATER · US AND CANADA", src=CALL))),
    Beat("never", lambda c, b: statement(c, b, ["The fee was never the reason people came.", ("The prices were.", b.w("never", "prices") - 0.3),
                                                ("And the fee pays for the prices.", b.w("never", "paid") - 0.5)], size=58,
                                         cols=[PAPER, PAPER, BRASS])),
    # V · YOU
    Beat("you", lambda c, b: floor_card(c, b, "V", "You", "IS IT WORTH IT FOR YOU?")),
    Beat("basic", lambda c, b: statement(c, b, ["The card pays off only if Costco", ("saves you more than the fee.", b.w("basic", "saves") - 0.3),
                                                ("What you buy, not the chicken.", b.w("basic", "depends") - 0.3)], size=60, cols=[PAPER, PAPER, BRASS])),
    Beat("upgrade", lambda c, b: (number(c, b, "$3,250", "A YEAR · WHERE THE $130 UPGRADE PAYS FOR ITSELF · US", src="$65 EXTRA ÷ 2% = $3,250"),
                                  typed(c, b, "ABOUT $63 A WEEK", CX, 690, b.w("upgrade", "week.") - 0.6, 28, PAPER))),
    Beat("uk", lambda c, b: number(c, b, "£2,100", "A YEAR · THE SAME LINE IN BRITAIN", src="MONEYSAVINGEXPERT, 2026")),
    Beat("spoil", lambda c, b: statement(c, b, ["Bulk only saves money", ("if you use it before it spoils.", b.w("spoil", "use") - 0.3)], size=70)),
    Beat("unit", lambda c, b: (serif(c, b, "Check the unit price.", CX, 420, b.t0 + 0.2, 80, BRASS),
                               typed(c, b, "ON THE SHELF LABEL · NOT THE PRICE OF THE PACK", CX, 520, b.w("unit", "shelf") - 0.3, 26, PAPER),
                               typed(c, b, "BIG ISN'T ALWAYS CHEAPER", CX, 600, b.w("unit", "big") - 0.3, 26, MUTED))),
    Beat("list", lambda c, b: (warehouse(c, 520, 560, 220, b.k(b.t0, 0.5)), hotdog(c, 1400, 500, 110, b.k(b.t0 + 0.3, 0.5)),
                               typed(c, b, "THE DOOR", 520, 640, b.w("list", "door.") - 0.3, 24, PAPER),
                               typed(c, b, "THE HOT DOG", 1400, 640, b.w("list", "hot") - 0.3, 24, PAPER),
                               arrow(c, b, [(760, 480), (960, 380), (1100, 380), (1270, 480)], b.w("list", "between") - 0.3,
                                     "WHERE THE BASKET FILLS UP", BRASS, "coin"))),
    Beat("go", lambda c, b: statement(c, b, ["Go with a list.", ("The fee only pays if the list does.", b.w("go", "fee") - 0.3)], size=78)),
    # VI · WHAT IF
    Beat("imagine", lambda c, b: floor_card(c, b, "VI", "What If", "IMAGINE ONE MORE STEP")),
    Beat("whatif", lambda c, b: statement(c, b, ["Not a forecast.", ("A what-if.", b.w("whatif", "what-if.") - 0.4)], size=88)),
    Beat("scene", lambda c, b: (warehouse(c, CX, 520, 300, b.k(b.t0, 0.5)),
                                stamp(c, b, "0% MARKUP", 600, 300, b.w("scene", "markup") - 0.3, BRASS, 40),
                                card(c, 1420, 400, 200, b.k(b.w("scene", "door,") - 0.3, 0.5), BRASS, "MEMBER"),
                                typed(c, b, "THE DOOR COSTS MORE EACH YEAR", CX, 720, b.w("scene", "more") - 0.3, 26, BRASS))),
    Beat("subs", lambda c, b: ticks(c, b, [("Your phone.", b.t0 + 0.1), ("Your films. Your music.", b.w("subs", "films,") - 0.3),
                                           ("Even your printer's ink.", b.w("subs", "printer's") - 0.3),
                                           ("A fee to keep access.", b.w("subs", "fee") - 0.3)], b.t0, x=560, y=330, size=54)),
    Beat("question", lambda c, b: statement(c, b, ["At what point are you not a customer,", ("but a subscriber?", b.w("question", "subscriber?") - 0.4)],
                                            size=78, face=L.SERIF_I)),
    # VII · THE CLOSE
    Beat("then", lambda c, b: (hotdog(c, 760, 380, 150, 1.0 * b.k(b.t0, 0.5)), cup(c, 1100, 380, 80, b.k(b.t0 + 0.2, 0.5)),
                               serif(c, b, "$1.50", CX, 640, b.t0 + 0.4, 150))),
    Beat("close", lambda c, b: (statement(c, b, [("The hot dog gets you in.", b.t0 + 0.1),
                                                 ("The card keeps you coming back.", b.w("close", "card") - 0.3)], size=76),
                                typed(c, b, ledger.BRAND, CX, 860, tl.le("close") + 0.6, 30, BRASS, track=0.3))),
], tail=4.0)


def frame(c, t):
    BOARD.frame(c, t)


def end_time():
    return BOARD.end()
