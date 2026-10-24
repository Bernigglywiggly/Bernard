"""HOW THEY PROFIT · EP04 · THE CLOUD BEHIND THE CART: the storyboard (ch2/kit.py) in the ledger look, keyed to the script's
line ids and the narrator's words. No logos: the shop, the parcels, the search page and the servers are line drawings.

  I THE PRICE    $716.9B of sales; the boxes; 57% of the profit from one business; it rents out computers
  II THE MACHINE five businesses: the shop $265B; the marketplace 61% · 15% · $172B; adverts $68.6B; subscriptions
                 $49.6B; AWS, the computers behind the apps
  III THE PROOF  2006; years of silence; $265M in Q1 2015; the 2025 segments: 7¢, under 3¢, 35¢; 18% of sales, 57% of
                 profit; adverts counted inside the shop; $131.8B of building; Jassy; ~$200B planned
  IV THE MONEY   where a dollar goes; 45¢ by one estimate; the busiest shop; the loop; the computers rented to everyone
  V YOU          Sponsored; the first result; scroll, check, compare; count every fee; the segment table; the parcel
  VI WHAT IF     an assistant that shops for you: who pays to be chosen, and who does it work for?
  VII THE CLOSE  $717B again; you see the boxes, the profit is in the cloud
"""
import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402
from ch2 import ledger  # noqa: E402
from ch2.kit import (Board, Beat, CX, CY, W, H, PAPER, BRASS, RED, MUTED, INK, number, statement, floor_card, stamp,  # noqa: E402
                     split, node, arrow, typed, serif, source, coins, person, card, warehouse, shop, server, parcel,
                     bars, ticks, quote, icon_row, ease, seg, lerp)

FY = "AMAZON, FULL-YEAR 2025 RESULTS (FORM 8-K, FEB 2026)"
CALL = "AMAZON Q4 2025 EARNINGS CALL (FEB 2026)"


def racks(c, b, n=3, x=CX, y=430, s=150, at=None, gap=230):
    t0 = b.t0 if at is None else at
    for i in range(n):
        k = b.k(t0 + 0.15 * i, 0.5)
        if k > 0:
            server(c, x + (i - (n - 1) / 2) * gap, y, s, k, PAPER, b.k(t0 + 0.4 + 0.15 * i, 1.2))


def advert_box(c, x, y, s, a=1.0):
    """An advert: a framed panel marked AD, for icon rows."""
    c.drawRect(skia.Rect.MakeXYWH(x - s, y - 0.6 * s, 2 * s, 1.2 * s), L.stroke(PAPER, 2.2, a))
    L.text(c, "AD", x, y + 0.2 * s, L.font(L.MONO_M, int(0.55 * s)), L.fill(BRASS, a), "center", track=0.1)


def boxes(c, b):
    warehouse(c, 520, 600, 220, b.k(b.w("boxes", "warehouses") - 0.3, 0.5))
    for i in range(3):
        parcel(c, 1160 + i * 190, 560 - (i % 2) * 40, 80, b.k(b.w("boxes", "boxes") - 0.3 + 0.15 * i, 0.5))
    typed(c, b, "THE WEBSITE · THE WAREHOUSES · THE VANS · THE BOXES", CX, 760, b.t0 + 0.4, 24, BRASS)


def rents(c, b):
    racks(c, b, 3, CX, 420, 150)
    typed(c, b, "IT RENTS OUT COMPUTERS", CX, 720, b.w("rents", "rents") - 0.2, 32, BRASS)


def search(c, b, line, sponsored_at, n_ads=2, y0=250):
    """A search page: the box with a query typed in, then result rows; the first n_ads carry a Sponsored tag."""
    x0, w = 420, 1080
    k = b.k(b.t0, 0.4)
    if k <= 0:
        return
    c.drawRoundRect(skia.Rect.MakeXYWH(x0, y0, w, 70), 35, 35, L.stroke(PAPER, 2.2, k))
    typed(c, b, "DESK LAMP", x0 + 50, y0 + 46, b.t0 + 0.3, 26, PAPER, "left", 0.08)
    for i in range(4):
        y = y0 + 120 + i * 110
        ki = b.k(b.t0 + 0.6 + 0.2 * i, 0.4)
        if ki <= 0:
            continue
        c.drawRect(skia.Rect.MakeXYWH(x0, y, 120, 86), L.stroke(MUTED, 1.6, ki))
        c.drawLine(x0 + 150, y + 26, x0 + 700, y + 26, L.stroke(PAPER, 3, 0.8 * ki))
        c.drawLine(x0 + 150, y + 60, x0 + 480, y + 60, L.stroke(MUTED, 2, 0.7 * ki))
        if i < n_ads:
            kt = b.k(sponsored_at + 0.25 * i, 0.3)
            if kt > 0:
                r = skia.Rect.MakeXYWH(x0 + w - 260, y + 18, 230, 46)
                c.drawRoundRect(r, 6, 6, L.stroke(BRASS, 2, kt))
                L.text(c, "SPONSORED", x0 + w - 145, y + 50, L.font(L.MONO_M, 22), L.fill(BRASS, kt), "center", track=0.12)


def per_dollar(c, b, cents, label, at):
    typed(c, b, f"≈ {cents} IN EVERY $1", CX, 760, at, 30, BRASS)


def no_van(c, b):
    advert_box(c, CX, 360, 120, b.k(b.t0, 0.5))
    for i, (word, txt) in enumerate((("warehouse,", "NO WAREHOUSE"), ("van", "NO VAN"), ("driver.", "NO DRIVER"))):
        typed(c, b, txt, 560 + i * 400, 640, b.w("van", word) - 0.25, 30, PAPER if i < 2 else BRASS)


def dollar_flow(c, b):
    node(c, b, 360, 470, 340, 140, "Your $1", "AT A SELLER ON AMAZON", b.t0 + 0.1)
    targets = [("The seller", "WHAT'S LEFT", 240, b.w("split", "seller.")),
               ("Commission", "TO AMAZON", 420, b.w("split", "commission.")),
               ("Warehouse", "AND DELIVERY", 600, b.w("split", "warehouse")),
               ("The advert", "MAYBE ALREADY PAID", 780, b.w("adcost", "advert"))]
    for name, sub, y, t in targets:
        node(c, b, 1470, y, 380, 130, name, sub, t - 0.2)
        arrow(c, b, [(540, 470), (900, 470), (1000, y), (1270, y)], t - 0.4, "", BRASS if name != "The seller" else PAPER,
              "coin")


def loop(c, b):
    pts = [(CX, 300), (CX + 340, 620), (CX - 340, 620)]
    names = [("The shop", "BRINGS CUSTOMERS", b.w("flywheel", "shop") - 0.2),
             ("Customers", "BRING SELLERS", b.w("flywheel", "customers", 1) - 0.2),
             ("Sellers", "PAY FOR ADVERTS", b.w("flywheel", "sellers", 1) - 0.2)]
    for (x, y), (name, sub, t) in zip(pts, names):
        node(c, b, x, y, 330, 120, name, sub, t)
    arrow(c, b, [(CX + 160, 330), (CX + 330, 380), (CX + 370, 480), (CX + 350, 560)], names[1][2] + 0.2, "", BRASS, "coin")
    arrow(c, b, [(CX + 170, 650), (CX + 60, 700), (CX - 60, 700), (CX - 170, 650)], names[2][2] + 0.2, "", BRASS, "coin")
    arrow(c, b, [(CX - 350, 560), (CX - 370, 480), (CX - 330, 380), (CX - 160, 330)], names[2][2] + 1.0, "", BRASS, "coin")


def assistant(c, b):
    person(c, 520, 470, 150, b.k(b.t0, 0.5))
    k = b.k(b.w("agent", "ask") - 0.3, 0.4)
    if k > 0:
        r = skia.Rect.MakeXYWH(640, 300, 420, 100)
        c.drawRoundRect(r, 18, 18, L.stroke(PAPER, 2, k))
        L.text(c, "I need a lamp.", 850, 362, L.font(L.SERIF_M, 40), L.fill(PAPER, k), "center")
    k2 = b.k(b.w("agent", "picks") - 0.3, 0.4)
    if k2 > 0:
        r = skia.Rect.MakeXYWH(1020, 470, 520, 120)
        c.drawRoundRect(r, 18, 18, L.stroke(BRASS, 2, k2))
        typed(c, b, "1 LAMP · CHOSEN FOR YOU", 1280, 542, b.w("agent", "picks") - 0.1, 26, BRASS)


BOARD = Board([
    # I · THE PRICE
    Beat("sales", lambda c, b: number(c, b, "$716.9 billion", "AMAZON'S NET SALES · 2025", src=FY)),
    Beat("boxes", boxes),
    Beat("most", lambda c, b: number(c, b, "57%", "OF AMAZON'S OPERATING PROFIT · 2025 · FROM ONE BUSINESS", src=FY)),
    Beat("rents", rents),
    Beat("front", lambda c, b: statement(c, b, ["The shop is what you see.",
                                               ("Most of the profit is somewhere else.", b.w("front", "most") - 0.3)], size=74)),
    # II · THE MACHINE
    Beat("five", lambda c, b: floor_card(c, b, "II", "The Machine", "FIVE BUSINESSES BEHIND ONE WEBSITE")),
    Beat("shop", lambda c, b: (shop(c, CX, 330, 130, b.k(b.t0, 0.5)),
                               number(c, b, "$265 billion", "1 · THE SHOP · AMAZON'S OWN ONLINE SALES · 2025", y=600, size=130,
                                      at=b.w("shop", "billion") - 0.6, src=FY))),
    Beat("market", lambda c, b: number(c, b, "61%", "2 · THE MARKETPLACE · ITEMS SOLD BY OTHER SELLERS · Q4 2025",
                                       src="AMAZON SUPPLEMENTAL DATA, Q4 2025, AS REPORTED")),
    Beat("commission", lambda c, b: (number(c, b, "15%", "AMAZON'S COMMISSION ON EACH SALE · MOST CATEGORIES",
                                            src="AMAZON SELLER CENTRAL FEE SCHEDULE"),
                                     typed(c, b, "+ A FEE TO STORE AND SHIP", CX, 700, b.w("commission", "stores") - 0.3, 28, PAPER))),
    Beat("sellers", lambda c, b: number(c, b, "$172 billion", "PAID BY OTHER SELLERS FOR AMAZON'S SERVICES · 2025", src=FY)),
    Beat("ads", lambda c, b: (search(c, b, "ads", b.w("ads", "adverts,") - 0.3),
                              typed(c, b, "3 · ADVERTISING", 420, 210, b.t0 + 0.2, 24, BRASS, "left"))),
    Beat("adsum", lambda c, b: number(c, b, "$68.6 billion", "PAID TO BE SEEN · AMAZON'S ADVERTISING SALES · 2025", src=FY)),
    Beat("prime", lambda c, b: number(c, b, "$49.6 billion", "4 · SUBSCRIPTIONS, PRIME INCLUDED · 2025", src=FY)),
    Beat("cloud", lambda c, b: (racks(c, b, 4, CX, 400, 140, gap=210),
                                typed(c, b, "5 · AMAZON WEB SERVICES", CX, 680, b.w("cloud", "amazon") - 0.2, 30, BRASS),
                                typed(c, b, "SERVERS · STORAGE · COMPUTING POWER, RENTED BY THE HOUR", CX, 740,
                                      b.w("cloud", "servers,") - 0.2, 22, PAPER))),
    Beat("anyone", lambda c, b: ticks(c, b, [("Start-ups.", b.t0 + 0.1), ("Banks.", b.w("anyone", "banks,") - 0.3),
                                             ("Governments.", b.w("anyone", "governments.") - 0.3),
                                             ("The apps on your phone.", b.w("anyone", "app") - 0.3)], b.t0, x=640, y=300, size=56)),
    # III · THE PROOF
    Beat("began", lambda c, b: floor_card(c, b, "III", "The Proof", "WHAT THE ACCOUNTS SHOW")),
    Beat("launch", lambda c, b: (number(c, b, "2006", "AMAZON WEB SERVICES OPENS TO THE PUBLIC", y=400,
                                        src="AWS: S3 (14 MAR 2006), EC2 (25 AUG 2006)"),
                                 typed(c, b, "STORAGE AND COMPUTING, BY THE HOUR", CX, 620, b.w("launch", "storage") - 0.3, 26, PAPER))),
    Beat("silent", lambda c, b: statement(c, b, ["For years, Amazon didn't say how much it made.",
                                                 ("It was hidden inside the shop's numbers.", b.w("silent", "hidden") - 0.3)],
                                          size=60)),
    Beat("reveal", lambda c, b: (typed(c, b, "APRIL 2015 · THE CLOUD'S FIGURES, SHOWN FOR THE FIRST TIME", CX, 250, b.t0 + 0.2, 26, PAPER),
                                 number(c, b, "$265 million", "AWS OPERATING PROFIT · FIRST QUARTER 2015",
                                        at=b.w("reveal", "making") - 0.4, src="AMAZON, FIRST QUARTER 2015 RESULTS (23 APR 2015)"))),
    Beat("ten", lambda c, b: statement(c, b, ["Ten years later:", ("the 2025 accounts.", b.w("ten", "accounts") - 0.4)], size=84)),
    Beat("north", lambda c, b: (typed(c, b, "THE SHOPS · NORTH AMERICA", CX, 230, b.t0 + 0.2, 26, PAPER),
                                number(c, b, "$29.6 billion", "OPERATING PROFIT · NORTH AMERICA · ON $426 BILLION OF SALES", y=420,
                                       at=b.t0 + 0.4, src=FY),
                                per_dollar(c, b, "7¢", "", b.w("north", "cents") - 0.5))),
    Beat("world", lambda c, b: (typed(c, b, "THE SHOPS · THE REST OF THE WORLD", CX, 230, b.t0 + 0.2, 26, PAPER),
                                number(c, b, "$4.7 billion", "OPERATING PROFIT · REST OF THE WORLD · ON $162 BILLION OF SALES", y=420,
                                       at=b.t0 + 0.4, src=FY),
                                typed(c, b, "UNDER 3¢ IN EVERY $1", CX, 760, b.w("world", "under") - 0.3, 30, BRASS))),
    Beat("include", lambda c, b: statement(c, b, ["Those shop numbers already include",
                                                  ("the sellers' fees and the advertising.", b.w("include", "sellers'") - 0.3)],
                                           size=64)),
    Beat("aws", lambda c, b: (typed(c, b, "THE CLOUD · AMAZON WEB SERVICES", CX, 230, b.t0 + 0.2, 26, BRASS),
                              racks(c, b, 5, CX, 140, 50, gap=90),
                              number(c, b, "$45.6 billion", "AWS OPERATING PROFIT · ON $128.7 BILLION OF SALES · 2025", y=420,
                                     at=b.w("aws", "made") - 0.4, src=FY),
                              per_dollar(c, b, "35¢", "", b.w("aws", "cents") - 0.5))),
    Beat("share", lambda c, b: (bars(c, b, [("AWS · SHARE OF AMAZON'S SALES", 18, "18%", MUTED, b.t0 + 0.2),
                                            ("AWS · SHARE OF AMAZON'S OPERATING PROFIT", 57, "57%", BRASS, b.w("share", "profit.") - 0.6)],
                                      b.t0, x0=300, y0=380, w=1150, gap=200, vmax=60),
                                source(c, b, "$128.7B ÷ $716.9B · $45.6B ÷ $80.0B (" + FY + ")"))),
    Beat("hidden", lambda c, b: statement(c, b, ["Amazon doesn't say how much profit its advertising makes.",
                                                 ("It counts it inside the shop.", b.w("hidden", "counts") - 0.3)], size=56)),
    Beat("van", no_van),
    Beat("bet", lambda c, b: (racks(c, b, 5, CX, 360, 110, gap=170),
                              number(c, b, "$131.8 billion", "SPENT ON BUILDINGS AND EQUIPMENT · 2025 · UP FROM $83.0 BILLION", y=640,
                                     size=120, at=b.w("bet", "spent") - 0.4, src=FY))),
    Beat("jassy", lambda c, b: (typed(c, b, "ANDY JASSY · AMAZON'S CHIEF EXECUTIVE", CX, 250, b.t0 + 0.2, 26, PAPER),
                                quote(c, b, ["Predominantly in AWS,", "because we have very high demand."],
                                      CALL, b.w("jassy", "predominantly") - 0.3))),
    Beat("plan", lambda c, b: number(c, b, "~$200 billion", "AMAZON'S PLANNED CAPITAL SPENDING · 2026", src=CALL)),
    # IV · THE MONEY
    Beat("where", lambda c, b: floor_card(c, b, "IV", "The Money", "WHERE YOUR MONEY GOES")),
    Beat("split", dollar_flow, until="adcost"),
    Beat("toll", lambda c, b: (number(c, b, "45¢", "OF EACH $1 A SELLER TAKES, PAID TO AMAZON · ONE ESTIMATE, 2023", y=420,
                                      at=b.w("toll", "cents") - 0.6,
                                      src="INSTITUTE FOR LOCAL SELF-RELIANCE, DEC 2023 (CAMPAIGNS AGAINST AMAZON'S POWER)"),
                               coins(c, CX, 680, 9, b.k(b.w("toll", "commissions,") - 0.3, 0.5), 20, 9))),
    Beat("choose", lambda c, b: statement(c, b, ["Sellers don't have to use the warehouses or buy the adverts.",
                                                 ("But on the busiest shop in the world,", b.w("choose", "busiest") - 0.3),
                                                 ("it's hard to be found without them.", b.w("choose", "hard") - 0.3)],
                                          size=52, cols=[PAPER, PAPER, BRASS])),
    Beat("somewhere", lambda c, b: statement(c, b, ["Every fee comes from somewhere:",
                                                    ("the seller's margin,", b.w("somewhere", "seller's") - 0.3),
                                                    ("or the price.", b.w("somewhere", "price.") - 0.3)], size=70,
                                             cols=[PAPER, PAPER, BRASS])),
    Beat("flywheel", loop),
    Beat("engine", lambda c, b: (racks(c, b, 4, CX, 380, 140, gap=210),
                                 typed(c, b, "RENTED OUT TO EVERYONE ELSE", CX, 660, b.w("engine", "rented") - 0.3, 30, PAPER),
                                 typed(c, b, "35¢ OF PROFIT IN THE DOLLAR", CX, 730, b.w("engine", "profit") - 0.6, 30, BRASS))),
    # V · YOU
    Beat("you", lambda c, b: floor_card(c, b, "V", "You", "WHAT THIS MEANS FOR YOU")),
    Beat("sponsored", lambda c, b: (search(c, b, "sponsored", b.w("sponsored", "sponsored.") - 0.3),
                                    typed(c, b, "THOSE RESULTS PAID TO BE THERE", 420, 210, b.w("sponsored", "paid") - 0.3, 24, BRASS,
                                          "left"))),
    Beat("top", lambda c, b: statement(c, b, ["The first result isn't always the best one.",
                                              ("Sometimes it's just the one that paid.", b.w("top", "sometimes") - 0.3)], size=64)),
    Beat("compare", lambda c, b: ticks(c, b, [("Scroll past the adverts.", b.t0 + 0.1),
                                              ("Check who the seller is.", b.w("compare", "check") - 0.3),
                                              ("Compare the price elsewhere.", b.w("compare", "compare") - 0.3)],
                                       b.t0, x=560, y=340, size=58)),
    Beat("sell", lambda c, b: (typed(c, b, "IF YOU SELL: COUNT EVERY FEE", 500, 230, b.t0 + 0.2, 26, BRASS, "left"),
                               ticks(c, b, [("The commission.", b.w("sell", "commission,") - 0.3),
                                            ("The storage.", b.w("sell", "storage,") - 0.3),
                                            ("The delivery.", b.w("sell", "delivery,") - 0.3),
                                            ("The adverts.", b.w("sell", "adverts,") - 0.3),
                                            ("The returns.", b.w("sell", "returns.") - 0.3)], b.t0, x=560, y=320, gap=92, size=50))),
    Beat("invest", lambda c, b: statement(c, b, ["Read the segment table,",
                                                 ("not the headline sales.", b.w("invest", "headline") - 0.3)], size=80)),
    Beat("parcel", lambda c, b: (parcel(c, CX, 320, 120, b.k(b.t0, 0.5)),
                                 statement(c, b, ["The parcel is the part you see.",
                                                  ("The profit is in the parts you don't.", b.w("parcel", "profit") - 0.3)],
                                           y=560, size=64))),
    # VI · WHAT IF
    Beat("imagine", lambda c, b: floor_card(c, b, "VI", "What If", "IMAGINE ONE MORE STEP")),
    Beat("whatif", lambda c, b: statement(c, b, ["Not a forecast.", ("A what-if.", b.w("whatif", "what-if.") - 0.4)], size=88)),
    Beat("agent", assistant),
    Beat("paid", lambda c, b: statement(c, b, ["Today, sellers pay to be at the top of the page.",
                                               ("Who will pay to be the assistant's choice?", b.w("paid", "who") - 0.3)], size=58)),
    Beat("same", lambda c, b: icon_row(c, b, [(lambda c_, x, y, s, a: shop(c_, x, y, s, a), "THE SHOP", b.w("same", "shop,") - 0.3),
                                              (advert_box, "THE ADVERTS", b.w("same", "adverts,") - 0.3),
                                              (lambda c_, x, y, s, a: server(c_, x, y, s * 0.9, a), "THE COMPUTERS",
                                               b.w("same", "computers") - 0.3)], b.t0, y=420, size=110)),
    Beat("question", lambda c, b: statement(c, b, ["Who is the assistant", ("really working for?", b.w("question", "really") - 0.3)],
                                            size=84, face=L.SERIF_I)),
    # VII · THE CLOSE
    Beat("then", lambda c, b: number(c, b, "$716.9 billion", "AMAZON'S SALES · 2025")),
    Beat("close", lambda c, b: (statement(c, b, [("You see the boxes.", b.t0 + 0.1),
                                                 ("The profit is in the cloud.", b.w("close", "profit") - 0.3)], size=80),
                                typed(c, b, ledger.BRAND, CX, 860, tl.le("close") + 0.6, 30, BRASS, track=0.3))),
], tail=4.0)


def frame(c, t):
    BOARD.frame(c, t)


def end_time():
    return BOARD.end()
