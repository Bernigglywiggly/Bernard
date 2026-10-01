"""THE MARGIN · EP02 · THE LANDLORD IN THE GOLDEN ARCHES: the storyboard (ch2/kit.py) in the ledger look, keyed to the
script's line ids and the narrator's words. No logos: restaurants are drawn as plain roadside buildings.

  I THE PRICE    $10.4 billion in rent; not from you; more than the profit; a landlord
  II THE MACHINE 45,356 restaurants, 95% franchised; who pays for what; the land and the buildings; rent + royalty;
                 $500,000 of their own money; a share of every sale
  III THE PROOF  the 1.9% and the half percent; Sonneborn's idea; his words; the 2025 receipt; 90% of the margin; 49 years
  IV THE MONEY   $139.4 billion; of every $10, $1.28; 4% to 5%; 20 years; the franchisee's side; paid first
  V YOU          $5.29; the landlord wins either way; read the lease before the menu
  VI WHAT IF     a high street that pays one landlord
  VII THE CLOSE  $10.4 billion again; the burgers bring the customers, the customers pay the rent
"""
import math

import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402
from ch2.kit import (Board, Beat, CX, CY, W, H, PAPER, BRASS, RED, MUTED, INK, number, statement, floor_card, stamp,  # noqa: E402
                     receipt, split, node, arrow, typed, serif, source, coins, person, shop, land, bars, ticks, quote,
                     icon_row, ease, seg, lerp)

TRAILS, GLINTS = [], []
TEN_K = "MCDONALD'S FORM 10-K FOR 2025"


def grid_of_shops(c, b, at, n=95, franch_at=None):
    """A hundred small restaurants; from franch_at, 95 of them turn to brass (run by franchisees)."""
    for i in range(100):
        x, y = 330 + (i % 20) * 64, 250 + (i // 20) * 76
        k = b.k(at + 0.01 * i, 0.3)
        if k <= 0:
            continue
        franch = franch_at is not None and i < n and b.t >= franch_at + 0.01 * i
        col = BRASS if franch else PAPER
        c.drawRect(skia.Rect.MakeXYWH(x, y, 40, 28), L.stroke(col, 1.6, k))
        c.drawLine(x - 4, y, x + 44, y, L.stroke(col, 1.6, k))


def lease_flow(c, b):
    """Owns the land / leases it, and rents it on: landlord -> franchisee, rent and royalty back."""
    land(c, 560, 470, 230, b.k(b.t0, 0.5))
    typed(c, b, "THE LAND · 56% OWNED", 560, 560, b.t0 + 0.3, 22, BRASS)
    shop(c, 560, 410, 130, b.k(b.w("owns", "buildings.") - 0.4, 0.5))
    typed(c, b, "THE BUILDINGS · 80%", 560, 610, b.w("owns", "buildings.") - 0.2, 22, PAPER)
    t_lease = b.w("lease", "leases")
    node(c, b, 1400, 450, 380, 140, "Franchisee", "RUNS THE RESTAURANT", t_lease - 0.2)
    arrow(c, b, [(820, 380), (980, 300), (1180, 300), (1290, 380)], b.w("lease", "rents") - 0.3, "RENTS IT ON", PAPER, None)
    source(c, b, TEN_K + ": OWNED ABOUT 56% OF THE LAND AND 80% OF THE BUILDINGS")


def twice(c, b):
    node(c, b, 560, 420, 380, 140, "Franchisee", "", b.t0 + 0.1)
    node(c, b, 1380, 420, 380, 140, "McDonald's", "", b.t0 + 0.3)
    arrow(c, b, [(760, 380), (900, 290), (1060, 290), (1190, 380)], b.w("twice", "royalty,") - 0.3, "ROYALTY · THE NAME", BRASS, "coin")
    arrow(c, b, [(760, 470), (900, 560), (1060, 560), (1190, 470)], b.w("twice", "rent,") - 0.3, "RENT · THE BUILDING", BRASS, "coin", 44)


def fitout(c, b):
    icon_row(c, b, [(lambda c_, x, y, s, a: c_.drawRect(skia.Rect.MakeXYWH(x - s * 0.6, y - s * 0.5, s * 1.2, s), L.stroke(PAPER, 2.2, a)),
                     "KITCHEN", b.w("fitout", "kitchen") - 0.3),
                    (lambda c_, x, y, s, a: [c_.drawRect(skia.Rect.MakeXYWH(x - s * 0.5 + j * s * 0.38, y - s * 0.2, s * 0.28, s * 0.5),
                                                         L.stroke(PAPER, 2.2, a)) for j in range(3)], "SEATING", b.w("fitout", "seating,") - 0.3),
                    (lambda c_, x, y, s, a: c_.drawRect(skia.Rect.MakeXYWH(x - s * 0.7, y - s * 0.35, s * 1.4, s * 0.6), L.stroke(PAPER, 2.2, a)),
                     "SIGNS & SCREENS", b.w("fitout", "screens.") - 0.6)], b.t0, y=330, size=90)
    serif(c, b, "The franchisee pays for the inside.", CX, 640, b.t0 + 0.3, 50, PAPER)
    serif(c, b, "McDonald's keeps the ground and the walls.", CX, 720, b.w("fitout", "keeps") - 0.3, 50, BRASS)


def till(c, b):
    """Every sale: items ring up and a slice of each drops into a rent jar."""
    items = [("BURGER", "every burger,"), ("COFFEE", "coffee,"), ("FRIES", "fries:")]
    for i, (lab, wd_) in enumerate(items):
        t = b.w("every", wd_.split()[-1]) - 0.3
        k = b.k(t, 0.4)
        x = 520 + i * 300
        if k > 0:
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 110, 330, 220, 120), 10, 10, L.stroke(PAPER, 2.0, k))
            L.text(c, lab, x, 400, L.font(L.MONO_M, 26), L.fill(PAPER, k), "center", track=0.1)
            kd = b.k(t + 0.4, 0.6)
            if kd > 0:
                L.coin(c, lerp(x, 1500, kd), lerp(470, 560, kd) - 120 * math.sin(math.pi * kd), 14, 1.0)
    c.drawRoundRect(skia.Rect.MakeXYWH(1420, 500, 160, 200), 14, 14, L.stroke(BRASS, 2.4, b.k(b.t0, 0.5)))
    typed(c, b, "RENT", 1500, 740, b.t0 + 0.3, 26, BRASS)
    typed(c, b, "PART OF EVERY SALE IS RENT", CX, 820, b.w("every", "rent.") - 0.5, 26, PAPER)


BOARD = Board([
    # I · THE PRICE
    Beat("rent", lambda c, b: number(c, b, "$10.4 billion", "IN RENT · COLLECTED BY McDONALD'S · 2025", src=TEN_K)),
    Beat("notyou", lambda c, b: statement(c, b, [("Not from you.", b.t0 + 0.1), ("From the people who run its restaurants.", b.w("notyou", "people") - 0.3)],
                                          size=68)),
    Beat("profit", lambda c, b: (bars(c, b, [("RENT COLLECTED", 10.4, "$10.4B", BRASS, b.t0 + 0.2),
                                             ("McDONALD'S NET INCOME", 8.6, "$8.6B", PAPER, b.w("profit", "profit") - 0.3)], b.t0),
                                 source(c, b, TEN_K + ": RENTS $10,442M; NET INCOME $8,563M"))),
    Beat("think", lambda c, b: statement(c, b, ["Most people think", ("it's a burger company.", b.w("think", "burger") - 0.3)], size=80)),
    Beat("landlord", lambda c, b: (serif(c, b, "A landlord.", CX, 420, b.w("landlord", "landlord.") - 0.3, 130, BRASS, face=L.SERIF_I),
                                   typed(c, b, "THE BURGERS ARE HOW THE RENT GETS PAID", CX, 560, b.w("landlord", "burgers") - 0.3, 26, PAPER))),
    # II · THE MACHINE
    Beat("count", lambda c, b: floor_card(c, b, "II", "The Machine", "WHO PAYS WHOM")),
    Beat(("count", "forty-five"), lambda c, b: number(c, b, "45,356", "McDONALD'S RESTAURANTS · END OF 2025", src=TEN_K)),
    Beat("franchised", lambda c, b: (grid_of_shops(c, b, b.t0, 95, b.w("franchised", "ninety-five") - 0.2),
                                     typed(c, b, "95% RUN BY FRANCHISEES: LOCAL BUSINESS OWNERS", CX, 720, b.w("franchised", "franchisees:") - 0.4, 26, BRASS))),
    Beat("pays", lambda c, b: (shop(c, CX - 120, 560, 200, b.k(b.t0, 0.5)),
                               icon_row(c, b, [(lambda c_, x, y, s, a: None, "THE KITCHEN", b.w("pays", "kitchen,") - 0.3),
                                               (lambda c_, x, y, s, a: None, "THE STAFF", b.w("pays", "staff,") - 0.3),
                                               (lambda c_, x, y, s, a: None, "THE FOOD", b.w("pays", "food") - 0.3),
                                               (lambda c_, x, y, s, a: None, "THE ELECTRICITY", b.w("pays", "electricity.") - 0.4)],
                                        b.t0, y=600, size=60),
                               typed(c, b, "THE FRANCHISEE PAYS FOR", CX, 200, b.t0 + 0.2, 26, PAPER))),
    Beat("owns", lease_flow, until="lease"),
    Beat("twice", twice),
    Beat("keys", lambda c, b: (number(c, b, "$500,000", "OF THEIR OWN MONEY · NOT BORROWED", y=420,
                                      src="McDONALD'S US FRANCHISING FAQ"),
                               stamp(c, b, "$45,000 FEE", 1460, 260, b.w("keys", "fee") - 0.3, BRASS, 38))),
    Beat("fitout", fitout),
    Beat("share", lambda c, b: statement(c, b, ["The rent isn't a fixed amount.", ("It's a share of sales.", b.w("share", "share") - 0.3),
                                                ("With a minimum.", b.w("share", "minimum.") - 0.4)], size=66, cols=[PAPER, BRASS, MUTED])),
    Beat("every", till),
    Beat("first", lambda c, b: (
        bars(c, b, [("WHEN SALES RISE", 1.0, "RENT RISES", BRASS, b.t0 + 0.2),
                    ("WHEN FOOD OR WAGES COST MORE", 1.0, "THE FRANCHISEE PAYS", PAPER, b.w("first", "food") - 0.3)], b.t0, w=700),
        stamp(c, b, "NOT THE RENT", 1500, 760, b.w("first", "rent.", 1) - 0.4, RED, 42))),
    # III · THE PROOF
    Beat("rescue", lambda c, b: floor_card(c, b, "III", "The Proof", "HOW A BURGER CHAIN BECAME A LANDLORD")),
    Beat("kroc", lambda c, b: number(c, b, "1.9%", "RAY KROC'S CUT OF EACH RESTAURANT'S SALES · 1950s",
                                     src="JOHN F. LOVE, McDONALD'S: BEHIND THE ARCHES (1986)")),
    Beat("brothers", lambda c, b: (split(c, b, "Of that 1.9%:", [("THE McDONALD BROTHERS · 0.5%", 0.5, "#2A3442", PAPER),
                                                                 ("KROC'S COMPANY · 1.4%", 1.4, BRASS, INK)],
                                         total=1.9, y0=420, h=160),
                                   typed(c, b, "NOT ENOUGH TO BUILD A COMPANY ON", CX, 700, b.w("brothers", "enough") - 0.3, 26, PAPER))),
    Beat("sonneborn", lambda c, b: (
        typed(c, b, "HARRY SONNEBORN · 1956 · FRANCHISE REALTY CORPORATION", CX, 200, b.t0 + 0.2, 22, BRASS),
        ticks(c, b, [("Get the land first.", b.w("sonneborn", "land") - 0.3), ("Build the restaurant.", b.w("sonneborn", "build") - 0.3),
                     ("Rent it to the franchisee, at a markup.", b.w("sonneborn", "rent") - 0.3)], b.t0, x=520, y=360, size=54))),
    Beat(("quote", "we"), lambda c, b: quote(c, b, ["We are not technically in the food business.", "We are in the real estate business."],
                                             "HARRY SONNEBORN · AS QUOTED IN BEHIND THE ARCHES", b.t0 + 0.1, 54)),
    Beat("quote2", lambda c, b: quote(c, b, ["The only reason we sell fifteen-cent hamburgers", "is because they are the greatest producer",
                                             "of revenue, from which our tenants", "can pay us our rent."],
                                      "HARRY SONNEBORN", b.t0 + 0.1, 46)),
    Beat("seventy", lambda c, b: statement(c, b, ["Seventy years later,", ("the filings show how far it went.", b.w("seventy", "filings") - 0.3)],
                                           size=72)),
    Beat("paid", lambda c, b: receipt(c, b, 660, 110, 600, "McDONALD'S · 2025", "PAID BY FRANCHISEES",
                                      [("", ""), ("RENT", "$10.4B"), ("ROYALTIES", "$6.0B"), ("", ""), ("TOTAL", "$16.5B")],
                                      times=[None, b.w("paid", "rent.") - 0.3, b.w("paid", "royalties.") - 0.4, None,
                                             b.w("paid", "sixteen") - 0.2], circle=1), until="paid"),
    Beat("own", lambda c, b: (bars(c, b, [("RENT FROM FRANCHISEES", 10.4, "$10.4B", BRASS, b.t0 + 0.1),
                                          ("FOOD SOLD BY ITS OWN RESTAURANTS", 9.7, "$9.7B", PAPER, b.w("own", "sold") - 0.3)], b.t0),
                              source(c, b, TEN_K + ": COMPANY-OPERATED SALES $9,690M")), until="more"),
    Beat("margin", lambda c, b: number(c, b, "~90%", "OF ALL RESTAURANT MARGIN CAME FROM FRANCHISEES · 2025",
                                       src=TEN_K + ": FRANCHISED MARGINS $13,930M")),
    Beat("dividend", lambda c, b: number(c, b, "49 years", "OF DIVIDEND RISES IN A ROW · SINCE 1976",
                                         src="McDONALD'S DIVIDEND RELEASE, 22 OCT 2025")),
    # IV · THE MONEY
    Beat("where", lambda c, b: floor_card(c, b, "IV", "The Money", "ONE MEAL, SPLIT")),
    Beat("spent", lambda c, b: number(c, b, "$139.4 billion", "SPENT AT McDONALD'S WORLDWIDE · 2025",
                                      src="McDONALD'S FULL-YEAR 2025 RESULTS (11 FEB 2026)")),
    Beat("stays", lambda c, b: statement(c, b, ["Most of it stays with the franchisees:", ("food, staff and bills.", b.w("stays", "food,") - 0.3)],
                                         size=66)),
    Beat("us", lambda c, b: (grid_of_shops(c, b, b.t0, 95, b.t0 + 0.8),
                             typed(c, b, "13,700+ IN AMERICA · MOST OF THEM McDONALD'S TENANTS", CX, 720, b.t0 + 0.5, 26, BRASS))),
    Beat("ten", lambda c, b: split(c, b, "Of every $10 spent at a franchised McDonald's",
                                   [("THE RESTAURANT KEEPS", 8.72, "#2A3442", PAPER), ("RENT", 0.80, BRASS, INK), ("ROYALTY", 0.46, "#8A6F3C", PAPER)],
                                   callouts=[("≈ $1.28 GOES TO McDONALD'S", CX, 760, b.w("ten", "thirty") - 0.3)],
                                   src="10-K 2025 AND 2025 RESULTS · AN AVERAGE ACROSS FRANCHISED SALES"), until="eighty"),
    Beat("royalty", lambda c, b: number(c, b, "4% → 5%", "US ROYALTY FOR NEW RESTAURANTS · FROM 2024",
                                        src="CNN, 22 SEP 2023; McDONALD'S FRANCHISOR UPDATES")),
    Beat("term", lambda c, b: number(c, b, "20 years", "OF RENT, AGREED IN ADVANCE · A TYPICAL FRANCHISE", src=TEN_K)),
    Beat("risk", lambda c, b: icon_row(c, b, [(lambda c_, x, y, s, a: person(c_, x, y, s, a), "THE WAGES", b.w("risk", "wages,") - 0.3),
                                              (lambda c_, x, y, s, a: L.coin(c_, x, y, s * 0.4, a), "THE FOOD", b.w("risk", "food,") - 0.3),
                                              (lambda c_, x, y, s, a: c_.drawCircle(x, y, s * 0.4, L.stroke(PAPER, 2.2, a)), "THE ENERGY", b.w("risk", "energy") - 0.3),
                                              (lambda c_, x, y, s, a: stamp(c_, b, "RISK", x, y, b.w("risk", "risk.") - 0.3, RED, 40), "THE RISK",
                                               b.w("risk", "risk.") - 0.3)], b.t0, y=420, size=110)),
    Beat("flop", lambda c, b: (statement(c, b, ["A menu flops. A price war.", ("The franchisee takes the hit.", b.w("flop", "hit.") - 0.4)], size=62),
                               stamp(c, b, "RENT STILL ARRIVES", CX, 760, b.w("flop", "arrives.") - 0.5, BRASS, 40))),
    Beat("before", lambda c, b: statement(c, b, ["Tied to sales, not profit.", ("Paid before anyone knows", b.w("before", "paid") - 0.3),
                                                 ("if the restaurant made money.", b.w("before", "whether") - 0.3)], size=64, cols=[PAPER, BRASS, BRASS])),
    # V · YOU
    Beat("you", lambda c, b: floor_card(c, b, "V", "You", "WHAT IT MEANS FOR YOUR WALLET")),
    Beat("prices", lambda c, b: (number(c, b, "$5.29", "AVERAGE US BIG MAC · 2024 · UP FROM $4.39 IN 2019",
                                        src="McDONALD'S USA OPEN LETTER, 29 MAY 2024"),
                                 typed(c, b, "THE FRANCHISEE SETS THE PRICE", CX, 230, b.t0 + 0.3, 24, MUTED))),
    Beat("either", lambda c, b: (statement(c, b, ["Higher prices, higher sales,", ("higher rent.", b.w("either", "rent.") - 0.4)], size=72),
                                 stamp(c, b, "LANDLORD WINS", 1480, 760, b.w("either", "wins") - 0.3, BRASS, 40))),
    Beat("deals", lambda c, b: statement(c, b, ["Deals and app offers:", ("more visits, more sales, more rent.", b.w("deals", "visits") - 0.3)],
                                         size=60)),
    Beat("lesson", lambda c, b: statement(c, b, ["Own the thing", ("everyone else has to use.", b.w("lesson", "everyone") - 0.3)], size=84,
                                          face=L.SERIF_I)),
    Beat("franchise", lambda c, b: (serif(c, b, "Read the lease before the menu.", CX, 380, b.t0 + 0.3, 72, BRASS),
                                    ticks(c, b, [("Who owns the building?", b.w("franchise", "owns") - 0.3),
                                                 ("What share of every sale leaves first?", b.w("franchise", "leaves") - 0.4)], b.t0, x=500, y=540, size=46))),
    Beat("invest", lambda c, b: statement(c, b, ["Look past the product.", ("Ask what it charges for.", b.w("invest", "charges") - 0.3)], size=80)),
    Beat("often", lambda c, b: statement(c, b, ["They look like they sell one thing.", ("They make money from another.", b.w("often", "money") - 0.3)],
                                         size=66)),
    # VI · WHAT IF
    Beat("imagine", lambda c, b: floor_card(c, b, "VI", "What If", "IMAGINE ONE MORE STEP")),
    Beat("whatif", lambda c, b: statement(c, b, ["Not a forecast.", ("A what-if.", b.w("whatif", "what-if.") - 0.4)], size=88)),
    Beat("street", lambda c, b: (
        [shop(c, 330 + i * 330, 560, 80, b.k(b.t0 + 0.2 * i, 0.5)) for i in range(5)],
        [typed(c, b, nm, 330 + i * 330, 640, b.w("street", w_) - 0.3, 20, PAPER) for i, (nm, w_) in
         enumerate((("BAKERY", "bakery,"), ("GYM", "gym,"), ("COFFEE", "coffee"), ("SHOP", "shop,"), ("SHOP", "shop,")))],
        [arrow(c, b, [(330 + i * 330, 470), (330 + i * 330, 300), (CX, 300), (CX, 230)], b.w("street", "share") - 0.3 + 0.1 * i, "", BRASS, "coin")
         for i in range(5)],
        typed(c, b, "ONE LANDLORD", CX, 200, b.w("street", "landlord,") - 0.3, 26, BRASS))),
    Beat("already", lambda c, b: ticks(c, b, [("Shopping centres: a share of the takings.", b.t0 + 0.1),
                                              ("Apps: a cut of every order.", b.w("already", "apps") - 0.3)], b.t0, x=420, y=420, size=52)),
    Beat("question", lambda c, b: statement(c, b, ["At what point does the street", ("work for the landlord?", b.w("question", "work") - 0.3)],
                                            size=80, face=L.SERIF_I)),
    # VII · THE CLOSE
    Beat("then", lambda c, b: number(c, b, "$10.4 billion", "IN RENT · 2025")),
    Beat("close", lambda c, b: (statement(c, b, [("The burgers bring in the customers.", b.t0 + 0.1),
                                                 ("The customers pay the rent.", b.w("close", "customers", 1) - 0.3)], size=70),
                                typed(c, b, "THE MARGIN", CX, 860, tl.le("close") + 0.6, 30, BRASS, track=0.3))),
], tail=4.0)


def frame(c, t):
    BOARD.frame(c, t)


def end_time():
    return BOARD.end()
