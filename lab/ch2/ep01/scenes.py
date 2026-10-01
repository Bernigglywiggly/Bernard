"""THE MARGIN · EP01 · BANKS WITH WINGS: the storyboard (ch2/kit.py), keyed to the script's line ids and the narrator's
words, drawn in the ledger look (ch2/ledger.py). Figures carry their source line; the what-if is labelled.

  I THE PRICE    $8.2 billion; not an airline, a card company; bigger than Delta's profit; banks with wings
  II THE MACHINE a mile costs almost nothing; the airline makes it, prices it, runs the shop; 1981; the flow:
                 miles to the bank, cash back, miles to you; empty seats; breakage
  III THE PROOF  June 2020; not its planes, its miles; the United receipt; SkyMiles $26B; AAdvantage; who buys miles
  IV THE MONEY   the card fee to the bank; ~2%; a million cards a year; $10B; ~1% of the US economy; the quote; $650
  V YOU          0.3% in Britain; clear it every month; who controls the currency; Sept 2023; 1.2 cents; spend them
  VI WHAT IF     a bank that happens to fly
  VII THE CLOSE  $8.2 billion again; the planes carry the passengers, the miles carry the airline
"""
import math

import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402
from ch2.kit import (Board, Beat, CX, CY, W, H, PAPER, BRASS, RED, MUTED, INK, number, statement, floor_card, stamp,  # noqa: E402
                     receipt, split, node, arrow, typed, serif, source, plane, card, bank, coins, person, ease, seg, lerp)

TRAILS, GLINTS = [], []


def bars(c, b, rows, at, x0=300, y0=360, w=1300, h=90, gap=150, vmax=None):
    """Horizontal bars to compare amounts: rows = [(label, value, display, colour, time or None)]."""
    vmax = vmax or max(r[1] for r in rows)
    for i, (lab, v, disp, colr, ti) in enumerate(rows):
        t = ti if ti is not None else at + 0.6 * i
        k = b.k(t, 0.7)
        y = y0 + i * gap
        if k > 0:
            c.drawRect(skia.Rect.MakeXYWH(x0, y, w * v / vmax * k, h), L.fill(colr, 0.9))
        typed(c, b, lab, x0, y - 18, t, 22, MUTED, "left", 0.1)
        serif(c, b, disp, x0 + w * v / vmax * k + 24, y + 64, t + 0.4, 54, colr, "left", rise=0)


def ticks(c, b, items, at, x=560, y=360, gap=110, size=44):
    """A list that ticks off: items = [(text, time or None)]."""
    for i, (txt, ti) in enumerate(items):
        t = ti if ti is not None else at + 0.5 * i
        k = b.k(t, 0.4)
        if k > 0:
            yy = y + i * gap
            c.drawLine(x - 70, yy - 14, x - 52, yy + 2, L.stroke(BRASS, 3, k))
            c.drawLine(x - 52, yy + 2, x - 20, yy - 34, L.stroke(BRASS, 3, k))
        serif(c, b, txt, x, y + i * gap, t, size, PAPER, "left")


def route(c, b, at):
    """Two cities joined by a dashed arc, a plane flying it: Austin to Raleigh."""
    k = b.k(at, 0.8)
    if k <= 0:
        return
    (x0, y0), (x1, y1) = (520, 330), (1400, 330)
    pts = [(lerp(x0, x1, u), y0 - 160 * math.sin(math.pi * u)) for u in [i / 40 * k for i in range(41)]]
    p = L.stroke(BRASS, 2.0, 0.9)
    p.setPathEffect(skia.DashPathEffect.Make([12, 9], 0))
    path = skia.Path()
    path.moveTo(*pts[0])
    for q in pts[1:]:
        path.lineTo(*q)
    c.drawPath(path, p)
    for x, y, name in ((x0, y0, "AUSTIN"), (x1, y1, "RALEIGH")):
        c.drawCircle(x, y, 9, L.fill(PAPER, b.k(at, 0.3)))
        typed(c, b, name, x, y + 50, at + 0.2, 24, PAPER)
    if k >= 1:
        u = min(1.0, (b.t - at - 0.8) / 2.5)
        plane(c, lerp(x0, x1, u), y0 - 160 * math.sin(math.pi * u), 40, 1.0, PAPER)


def quote(c, b, text_lines, who, at):
    for i, ln in enumerate(text_lines):
        serif(c, b, ln, CX, CY - 40 + i * 84, at + 0.3 * i, 62, PAPER, face=L.SERIF_I)
    L.text(c, "“", CX - 720, CY - 60, L.font(L.SERIF_B, 220), L.fill(BRASS, 0.5 * b.k(at, 0.5)), "left")
    typed(c, b, who, CX, CY + 40 + len(text_lines) * 84, at + 0.6, 22, BRASS)


def seats(c, b, at, filled=0.45):
    """A cabin seat map seen from above, most of it empty."""
    import numpy as np
    rng = np.random.default_rng(3)
    full = rng.random((6, 26)) < filled
    for col_ in range(26):
        for row in range(6):
            x = 300 + col_ * 50 + (30 if col_ > 12 else 0)
            y = 300 + row * 58 + (40 if row > 2 else 0)
            k = b.k(at + 0.015 * (col_ + row), 0.3)
            if k <= 0:
                continue
            r = skia.Rect.MakeXYWH(x, y, 36, 42)
            if full[row, col_]:
                c.drawRoundRect(r, 6, 6, L.fill(MUTED, 0.6 * k))
            else:
                c.drawRoundRect(r, 6, 6, L.stroke(BRASS, 1.6, 0.9 * k))


def tickets_grid(c, b, at, fade_at, n=48):
    """Miles as tickets; from fade_at some go to dashed outlines (expired) and some dim (forgotten)."""
    import numpy as np
    rng = np.random.default_rng(7)
    fate = rng.random(n)
    for i in range(n):
        x, y = 360 + (i % 12) * 100, 300 + (i // 12) * 100
        k = b.k(at + 0.02 * i, 0.3)
        if k <= 0:
            continue
        kf = b.k(fade_at + 0.03 * i, 0.6)
        if fate[i] < 0.25 and kf > 0:
            c.save(); c.translate(x, y); c.rotate(45)
            p = L.stroke(PAPER, 1.4, 0.5 * k)
            p.setPathEffect(skia.DashPathEffect.Make([5, 4], 0))
            c.drawRect(skia.Rect.MakeXYWH(-16, -16, 32, 32), p)
            c.restore()
        else:
            L.ticket(c, x, y, 16, k * (1 - 0.6 * kf if fate[i] < 0.45 else 1.0))


def wings(c, b, at):
    k = b.k(at, 0.7)
    if k <= 0:
        return
    bank(c, CX, 380, 150, k)
    for sgn in (-1, 1):
        p = skia.Path()
        x0 = CX + sgn * 175
        p.moveTo(x0, 330)
        p.lineTo(x0 + sgn * 330 * k, 260)
        p.lineTo(x0 + sgn * 360 * k, 290)
        p.lineTo(x0, 400)
        c.drawPath(p, L.stroke(BRASS, 2.4, k))
        for j in range(1, 4):
            c.drawLine(x0 + sgn * 80 * j * k, 330 - 17 * j, x0 + sgn * 88 * j * k, 400 - 27 * j, L.stroke(BRASS, 1.2, 0.6 * k))
    serif(c, b, "Banks with wings.", CX, 700, at + 0.5, 84, PAPER, face=L.SERIF_I)


def flow(c, b):
    """The machine: Delta makes miles, sells them to the bank for cash, the bank hands them to you."""
    t_sell, t_bulk = b.w("sell", "sells"), b.w("sell", "banks.")
    t_hand, t_coffee = b.w("cards", "hand"), b.w("cards", "coffee,")
    t_cash, t_years = b.w("cash", "cash"), b.w("cash", "years")
    node(c, b, 520, 360, 420, 150, "Delta", "MAKES THE MILES", b.t0 + 0.1)
    node(c, b, 1400, 360, 420, 150, "The bank", "BUYS THEM IN BULK", t_sell - 0.2)
    arrow(c, b, [(730, 410), (870, 490), (1050, 490), (1190, 410)], t_bulk - 0.3, "MILES", MUTED, "ticket", 40)
    node(c, b, 960, 760, 420, 150, "You", "EARN THEM ON EVERYTHING", t_hand - 0.2)
    arrow(c, b, [(1400, 435), (1400, 630), (1300, 760), (1170, 760)], t_hand, "", MUTED, "ticket")
    typed(c, b, "A FEW PER COFFEE, PER BILL", 1370, 600, t_coffee - 0.2, 20, PAPER, "right", 0.08)
    arrow(c, b, [(1190, 310), (1050, 230), (870, 230), (730, 310)], t_cash - 0.3, "CASH TODAY", BRASS, "coin")
    typed(c, b, "FOR SEATS CLAIMED YEARS FROM NOW", CX, 160, t_years - 0.3, 22, BRASS)


BOARD = Board([
    # I · THE PRICE
    Beat("paid", lambda c, b: number(c, b, "$8.2 billion", "PAID TO DELTA AIR LINES · 2025",
                                     src="DELTA AIR LINES, FULL-YEAR 2025 RESULTS (13 JAN 2026)")),
    Beat("notflights", lambda c, b: (
        statement(c, b, [("Not an airline.", b.w("notflights", "airline.") - 0.3),
                         ("Not a single seat.", b.w("notflights", "seat.") - 0.4),
                         ("A credit card company.", b.w("notflights", "credit") - 0.2)], size=70),
        card(c, 1560, 760, 260, b.k(b.w("notflights", "credit"), 0.5), PAPER, "AMEX"))),
    Beat("profit", lambda c, b: (
        bars(c, b, [("PAID BY AMERICAN EXPRESS", 8.2, "$8.2B", BRASS, b.t0 + 0.2),
                    ("DELTA'S PROFIT BEFORE TAX", 6.2, "$6.2B", PAPER, b.w("profit", "profit") - 0.3)], b.t0),
        source(c, b, "DELTA AIR LINES, FULL-YEAR 2025 RESULTS: $8.2B FROM AMEX; $6.2B PRE-TAX INCOME (GAAP)"))),
    Beat("banks", lambda c, b: statement(c, b, ["Stop thinking of airlines", ("as airlines.", b.w("banks", "airlines", 1) - 0.4)],
                                         size=78, cols=[PAPER, PAPER])),
    Beat("wings", lambda c, b: wings(c, b, b.t0 + 0.2)),
    # II · THE MACHINE
    Beat("print", lambda c, b: floor_card(c, b, "II", "The Machine", "HOW A MILE IS MADE")),
    Beat(("print", "mile."), lambda c, b: (L.ticket(c, CX, 380, 90 * b.k(b.t0, 0.5, "o") + 1, 1.0),
                                           serif(c, b, "One mile.", CX, 620, b.t0 + 0.3, 84),
                                           typed(c, b, "COSTS THE AIRLINE ALMOST NOTHING TO MAKE", CX, 700, b.t0 + 0.6, 24))),
    Beat("currency", lambda c, b: (
        serif(c, b, "A currency.", 560, 250, b.t0 + 0.1, 72, BRASS, "left"),
        ticks(c, b, [("It creates it.", b.w("currency", "creates") - 0.2), ("It sets its value.", b.w("currency", "value,") - 0.3),
                     ("It runs the only shop that takes it.", b.w("currency", "shop") - 0.3)], b.t0, y=400))),
    Beat("origin", lambda c, b: number(c, b, "1981", "AMERICAN AIRLINES LAUNCHES AADVANTAGE",
                                       src="AMERICAN AIRLINES: AADVANTAGE LAUNCHED 1 MAY 1981")),
    Beat("copied", lambda c, b: (
        [plane(c, 420 + (i % 6) * 216, 330 + (i // 6) * 150, 70, b.k(b.t0 + 0.08 * i, 0.4)) for i in range(12)],
        typed(c, b, "EVERY BIG AIRLINE HAD ONE", CX, 690, b.t0 + 0.8, 26, PAPER),
        typed(c, b, "THEN: WHO ELSE WANTS TO BUY MILES?", CX, 750, b.w("copied", "buy") - 0.5, 26, BRASS))),
    Beat("sell", flow, until="cash"),
    Beat("empty", lambda c, b: (seats(c, b, b.t0 + 0.1),
                                typed(c, b, "SEATS THAT WOULD HAVE FLOWN EMPTY ANYWAY", CX, 780, b.t0 + 0.5, 26, BRASS))),
    Beat("never", lambda c, b: (tickets_grid(c, b, b.t0 + 0.1, b.w("never", "expire.") - 0.4),
                                typed(c, b, "SOME EXPIRE · SOME ARE FORGOTTEN", CX, 760, b.w("never", "expire.") - 0.2, 26, PAPER),
                                typed(c, b, "THE MONEY IS KEPT", CX, 820, b.w("never", "kept.") - 0.4, 26, BRASS))),
    Beat("breakage", lambda c, b: (serif(c, b, "breakage", CX, 420, b.w("breakage", "breakage.") - 0.3, 130, BRASS, face=L.SERIF_I),
                                   typed(c, b, "(N.) MILES SOLD AND NEVER USED: A SALE WITH NOTHING TO DELIVER", CX, 540,
                                         b.w("breakage", "every") - 0.3, 24, PAPER))),
    # III · THE PROOF
    Beat("2020", lambda c, b: floor_card(c, b, "III", "The Proof", "WHAT THE MILES ARE WORTH")),
    Beat("grounded", lambda c, b: (
        [plane(c, 560 + i * 400, 400, 140, b.k(b.t0 + 0.15 * i, 0.5), MUTED) for i in range(3)],
        typed(c, b, "JUNE 2020 · THE PLANES ARE GROUNDED", CX, 220, b.t0 + 0.1, 26, PAPER),
        typed(c, b, "UNITED NEEDS TO BORROW BILLIONS", CX, 640, b.w("grounded", "borrow") - 0.3, 26, BRASS),
        typed(c, b, "AGAINST SOMETHING LENDERS TRUST", CX, 700, b.w("grounded", "trust.") - 0.5, 26, PAPER))),
    Beat("planes", lambda c, b: statement(c, b, [("Not its planes.", b.t0 + 0.1), ("Not its airports.", b.w("planes", "airports.") - 0.4),
                                                 ("Its miles.", b.w("planes", "miles.") - 0.3)], size=80)),
    Beat("trust", lambda c, b: (card(c, 620, 450, 340, b.k(b.t0, 0.5)), coins(c, 1250, 560, int(30 * b.k(b.t0 + 0.4, 3.0)), 1.0, 20),
                                typed(c, b, "PEOPLE KEEP SPENDING ON THEIR CARDS", CX, 720, b.t0 + 0.6, 26, PAPER),
                                typed(c, b, "FLYING OR NOT", CX, 780, b.w("trust", "fly.") - 0.5, 26, BRASS))),
    Beat("valued", lambda c, b: (
        receipt(c, b, 1060, 120, 560, "UNITED AIRLINES · JUNE 2020", "MILEAGEPLUS",
                [("", ""), ("VALUED FOR THE LOAN", "$21.9B"), ("BORROWED AGAINST IT", "$6.8B"), ("", ""),
                 ("ALL OF UNITED", "$10.5B"), ("ON THE STOCK MARKET", "")],
                times=[None, b.w("valued", "valued") - 0.2, b.w("valued", "borrowed") - 0.2, None,
                       b.w("market", "whole") - 0.3, b.w("market", "market") - 0.3], circle=1),
        serif(c, b, "The miles were worth", 190, 470, b.w("worth", "miles") - 0.3, 70, PAPER, "left"),
        serif(c, b, "twice the airline.", 190, 560, b.w("worth", "twice") - 0.3, 70, BRASS, "left", L.SERIF_I),
        source(c, b, "UNITED INVESTOR PRESENTATION AND 8-K, 15 JUN 2020; THE HUSTLE, 5 OCT 2020")), until="worth"),
    Beat("delta2020", lambda c, b: (number(c, b, "$26 billion", "SKYMILES, VALUED FOR THE LOAN · SEPT 2020",
                                           src="DELTA 8-K, SEPT 2020; REUTERS"),
                                    stamp(c, b, "$9B BORROWED", 1480, 300, b.w("delta2020", "borrowed"), BRASS, 40))),
    Beat("american", lambda c, b: (number(c, b, "$19.5–31.5 billion", "AADVANTAGE, APPRAISED · MARCH 2021", size=130,
                                          src="AMERICAN AIRLINES, MARCH 2021 FINANCING (DAVIS POLK; SEC FILING)"),
                                   stamp(c, b, "$10B BORROWED", 1480, 290, b.w("american", "borrowed"), BRASS, 40))),
    Beat("sold", lambda c, b: (number(c, b, "$5.3 billion", "MILES UNITED SOLD IN 2019", y=330, size=130),
                               split(c, b, "", [("PARTNERS · MOSTLY CARD COMPANIES · 71%", 71, BRASS, INK), ("FLYERS · 29%", 29, "#2A3442", PAPER)],
                                     at=b.w("third", "seventy") - 0.3, y0=560, h=130, total=100.0,
                                     src="SKIFT, 15 JUN 2020; UNITED INVESTOR PRESENTATION")), until="third"),
    # IV · THE MONEY
    Beat("whybank", lambda c, b: floor_card(c, b, "IV", "The Money", "WHY A BANK PAYS FOR MILES")),
    Beat("swipe", lambda c, b: (
        card(c, 460, 430, 300, b.k(b.t0, 0.5)), node(c, b, 960, 430, 300, 130, "The shop", "PAYS A FEE", b.w("swipe", "shop") - 0.3),
        node(c, b, 1480, 430, 300, 130, "Your bank", "GETS PART OF IT", b.w("swipe", "bank") - 0.3),
        arrow(c, b, [(1110, 430), (1220, 380), (1250, 380), (1330, 430)], b.w("swipe", "part") - 0.3, "", BRASS, "coin"))),
    Beat("two", lambda c, b: number(c, b, "~2%", "OF EVERYTHING YOU BUY · AVERAGE US CARD FEE",
                                    src="AVERAGE US CREDIT CARD INTERCHANGE, ABOUT 2%")),
    Beat("spend", lambda c, b: (card(c, 700, 440, 320, 1.0 * b.k(b.t0, 0.5), BRASS, "ITS CARD"),
                                card(c, 1220, 440, 320, 0.4 * b.k(b.t0 + 0.2, 0.5), MUTED, "ANOTHER"),
                                [L.ticket(c, lerp(1500, 760, ease(seg(b.t, b.w("spend", "miles") - 0.3 + 0.2 * j, b.w("spend", "miles") + 0.6 + 0.2 * j))),
                                          260 + 30 * j, 12, b.k(b.w("spend", "miles") - 0.3, 0.2)) for j in range(4)],
                                typed(c, b, "MILES ARE HOW IT WINS YOU", CX, 700, b.w("spend", "wins") - 0.3, 28, BRASS))),
    Beat("million", lambda c, b: number(c, b, "1,000,000+", "NEW DELTA AMEX CARDS A YEAR · FOUR YEARS RUNNING",
                                        src="DELTA AIR LINES, FULL-YEAR 2025 RESULTS")),
    Beat("ten", lambda c, b: number(c, b, "$10 billion", "A YEAR · DELTA'S TARGET FROM AMEX", src="DELTA AIR LINES, 2025 RESULTS")),
    Beat("gdp", lambda c, b: number(c, b, "~1%", "OF THE WHOLE US ECONOMY · SPENT ON DELTA AMEX CARDS",
                                    src="ED BASTIAN, DELTA CEO (FAST COMPANY, 2023)")),
    Beat("tenth", lambda c, b: (statement(c, b, [("A tenth of all American Express card spending.", b.t0 + 0.1),
                                                 ("More than a tenth of Delta's revenue.", b.w("tenth", "delta", 1) - 0.3)], size=56,
                                                cols=[PAPER, BRASS]),
                                source(c, b, "FORTUNE, 3 APR 2026"))),
    Beat("routes", lambda c, b: (route(c, b, b.t0 + 0.2),
                                 typed(c, b, "NEW DELTA FLIGHTS · 2025", CX, 600, b.t0 + 0.6, 24, MUTED))),
    Beat(("routes", "these"), lambda c, b: quote(c, b, ["These are places we acquire", "a lot of cards."],
                                                  "ED BASTIAN, DELTA CEO, ON NEW FLIGHTS FROM AUSTIN AND RALEIGH · OCT 2025", b.t0 + 0.15)),
    Beat("fees", lambda c, b: number(c, b, "$650", "A YEAR · THE TOP DELTA AMEX CARD'S FEE", src="AMERICAN EXPRESS")),
    Beat("everyone", lambda c, b: (
        [person(c, 420 + i * 180, 420, 90, 1.0, PAPER if i % 3 else BRASS) for i in range(7)],
        typed(c, b, "THE FEES ARE IN THE PRICES", CX, 230, b.t0 + 0.2, 26, PAPER),
        serif(c, b, "Everyone pays for the miles.", CX, 640, b.w("everyone", "everyone") - 0.3, 62),
        serif(c, b, "Only some people collect them.", CX, 730, b.w("everyone", "only") - 0.3, 62, BRASS))),
    # V · YOU
    Beat("you", lambda c, b: floor_card(c, b, "V", "You", "WHAT IT MEANS FOR YOUR WALLET")),
    Beat("uk", lambda c, b: number(c, b, "0.3%", "THE UK CAP ON CREDIT CARD FEES",
                                   src="EU INTERCHANGE FEE REGULATION 2015, RETAINED IN UK LAW")),
    Beat("thinner", lambda c, b: (bars(c, b, [("UNITED STATES · TYPICAL CARD FEE", 2.0, "~2%", BRASS, b.t0 + 0.2),
                                              ("BRITAIN · CAPPED", 0.3, "0.3%", PAPER, b.t0 + 0.6)], b.t0),
                                  typed(c, b, "FEWER MILES ON BRITISH CARDS", CX, 760, b.w("thinner", "fewer") - 0.3, 26, BRASS))),
    Beat("interest", lambda c, b: statement(c, b, [("Clear it in full.", b.w("interest", "clear") - 0.3),
                                                   ("Every month.", b.w("interest", "every") - 0.3)], size=88)),
    Beat("devalue", lambda c, b: (serif(c, b, "Who controls the currency?", CX, 380, b.t0 + 0.2, 72),
                                  typed(c, b, "THE AIRLINE SETS WHAT A SEAT COSTS IN MILES", CX, 480, b.w("devalue", "raises") - 0.3, 24),
                                  stamp(c, b, "WORTH LESS OVERNIGHT", CX, 640, b.w("devalue", "overnight.") - 0.3, RED, 46))),
    Beat("rules", lambda c, b: (number(c, b, "Sept 2023", "DELTA MAKES ELITE STATUS FAR HARDER TO EARN",
                                       src="CNBC, 28 SEP 2023; SKIFT, 18 OCT 2023"),
                                stamp(c, b, "SOFTENED · OCT 2023", 1460, 280, b.w("rules", "softened") - 0.2, BRASS, 34))),
    Beat("novote", lambda c, b: statement(c, b, [("The rules still changed.", b.t0 + 0.1), ("The members had no vote.", b.w("novote", "members") - 0.3)],
                                          size=76)),
    Beat("cent", lambda c, b: (number(c, b, "1.2¢", "WHAT A DELTA OR UNITED MILE IS WORTH", src="NERDWALLET, 2026 VALUATIONS"),
                               typed(c, b, "50,000 MILES ≈ $600", CX, 690, b.w("cent", "fifty") - 0.3, 34, PAPER))),
    Beat("spendit", lambda c, b: statement(c, b, [("Miles are not savings.", b.t0 + 0.1), ("Earn them, then spend them.", b.w("spendit", "earn") - 0.3)],
                                           size=84)),
    # VI · WHAT IF
    Beat("imagine", lambda c, b: floor_card(c, b, "VI", "What If", "IMAGINE ONE MORE STEP")),
    Beat("whatif", lambda c, b: statement(c, b, ["Not a forecast.", ("A what-if.", b.w("whatif", "what-if.") - 0.4)], size=88)),
    Beat("scene", lambda c, b: (bank(c, CX, 420, 170, b.k(b.t0, 0.6)),
                                [plane(c, CX + 330 * math.cos(b.t * 0.6 + j * 2.09), 380 + 140 * math.sin(b.t * 0.6 + j * 2.09),
                                       55, b.k(b.t0 + 0.4, 0.6), BRASS) for j in range(3)],
                                typed(c, b, "THE FLYING: THE COST OF RUNNING THE CURRENCY", CX, 720, b.w("scene", "flying") - 0.3, 24, PAPER))),
    Beat("already", lambda c, b: ticks(c, b, [("It prints the currency.", b.w("already", "prints") - 0.3),
                                              ("It sets its value.", b.w("already", "value,") - 0.3),
                                              ("It decides what it buys.", b.w("already", "decides") - 0.3)], b.t0, y=380, size=60)),
    Beat("question", lambda c, b: statement(c, b, ["At what point is it a bank", ("that happens to fly?", b.w("question", "happens") - 0.3)],
                                            size=84, face=L.SERIF_I)),
    # VII · THE CLOSE
    Beat("then", lambda c, b: number(c, b, "$8.2 billion", "AMERICAN EXPRESS → DELTA · 2025")),
    Beat("close", lambda c, b: (statement(c, b, [("The planes carry the passengers.", b.t0 + 0.1),
                                                 ("The miles carry the airline.", b.w("close", "miles") - 0.3)], size=72),
                                typed(c, b, "THE MARGIN", CX, 860, tl.le("close") + 0.6, 30, BRASS, track=0.3))),
], tail=4.0)


def frame(c, t):
    BOARD.frame(c, t)


def end_time():
    return BOARD.end()
