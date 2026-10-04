"""HOW THEY PROFIT · EP05 · WHERE YOUR $100 GOES (PayPal): the storyboard (ch2/kit.py) in the ledger look, keyed to the
script's line ids and the narrator's words. No logos: the button is a plain brass pill marked PAY.

CRAFT.md applied: one persistent object (the $100 note) that is cut up chapter by chapter; the foreground becomes the
transition (the $1.85 sliver of the note zooms up to become the next bar, the 86¢ piece becomes the next split);
the note returns at the close so the film loops back to its opening tap.

  0 ONE HUNDRED DOLLARS  the button; the note; $1.79T; tiny, and how it adds up
  1 THE TOLL             3.49% + 49¢; the receipt: $3.98 off, $96.02 to the shop; why shops pay
  2 THE AVERAGE          the $1.85 sliver of the note; who pays less; Braintree behind other checkouts; 9.3B; a third
  3 WHO ELSE GETS PAID   the sliver becomes a bar: 89¢ networks and banks, 10¢ losses, 86¢ left
  4 THIRTY-FOUR CENTS    the 86¢ piece: costs, then 34¢ profit; $6.1B
  5 MONEY THAT SITS STILL  the balance; about $1.3B of interest; not yours
  6 TWO PAYPALS          the button and the pipes; Braintree's "profitable growth"
  7 THE BUTTON'S PROBLEM the February quote; Enrique Lores; one-tap rivals; the verdict; 2.99% vs 3.49%; the note again
"""
import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402
from ch2 import ledger  # noqa: E402
from ch2.kit import (Board, Beat, CX, PAPER, BRASS, RED, MUTED, INK, number, statement, floor_card,  # noqa: E402
                     node, arrow, typed, serif, source, coins, person, card, shop, bank, server,
                     bars, ticks, quote, receipt, ease, seg, lerp)

K10 = "PAYPAL FORM 10-K, 2025 (SEC EDGAR)"
FY = "PAYPAL, FOURTH QUARTER AND FULL YEAR 2025 RESULTS (8-K, 3 FEB 2026)"
FEES = "PAYPAL US BUSINESS FEES PAGE (CHECKED 5 OCT 2026)"

NOTE = (260, 330, 1400, 300)        # the $100 note: x0, y0, w, h (the film's persistent object)
SLIVER = 1.85 / 100                 # PayPal's average revenue per $100 (FACTS.md)


# ---------------------------------------------------------------- the persistent objects
def button(c, x, y, w, a=1.0, pressed=0.0):
    """The checkout button: a brass pill marked PAY (no logo), pressed down by `pressed` (0..1)."""
    if a <= 0:
        return
    h = w * 0.22
    dy = 6 * pressed
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2 + dy, w, h), h / 2, h / 2)
    c.drawRRect(r, L.fill(BRASS, 0.95 * a))
    L.text(c, "PAY", x, y + h * 0.18 + dy, L.font(L.SERIF_B, int(h * 0.5)), L.fill(INK, a), "center", track=0.12)


def note(c, b, a=1.0, cut=0.0, cut_label="", glow=0.0, x0=None, y0=None, w=None, h=None):
    """The $100 note. `cut` is the fraction marked off at its right-hand end (brass), labelled `cut_label`."""
    nx, ny, nw, nh = NOTE
    x0, y0, w, h = x0 or nx, y0 or ny, w or nw, h or nh
    if a <= 0:
        return
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), L.fill("#121A27", 0.95 * a))
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), L.stroke(PAPER, 2.2, a))
    c.drawRect(skia.Rect.MakeXYWH(x0 + 14, y0 + 14, w - 28, h - 28), L.stroke(BRASS, 1.2, 0.55 * a))
    L.text(c, "$100", x0 + 60, y0 + h * 0.62, L.font(L.SERIF_B, int(h * 0.42)), L.fill(PAPER, a), "left")
    L.text(c, "ONE PAYMENT", x0 + w - 60, y0 + 70, L.font(L.MONO_M, 22), L.fill(MUTED, a), "right", track=0.18)
    if cut > 0:
        cw = max(6.0, w * cut)
        c.drawRect(skia.Rect.MakeXYWH(x0 + w - cw, y0, cw, h), L.fill(BRASS, (0.55 + 0.45 * glow) * a))
        if cut_label:
            L.text(c, cut_label, x0 + w - cw / 2, y0 + h + 60, L.font(L.SERIF_B, 54), L.fill(BRASS, a), "center")
            c.drawLine(x0 + w - cw / 2, y0 + h + 4, x0 + w - cw / 2, y0 + h + 18, L.stroke(BRASS, 2, a))


def cut_bar(c, b, parts, total, at, x0=190, y0=400, w=1540, h=200, grow_from=None, title="", src=""):
    """A bar for `total`, cut into parts = [(label, value, fill, ink, time)]; with grow_from=(x, y, w, h) the bar
    first grows out of that rectangle (the foreground becoming the next scene)."""
    k = b.k(at, 0.8, "io")
    if grow_from:
        gx, gy, gw, gh = grow_from
        bx, by, bw, bh = lerp(gx, x0, k), lerp(gy, y0, k), lerp(gw, w, k), lerp(gh, h, k)
    else:
        bx, by, bw, bh = x0, y0, w * k, h
    c.drawRect(skia.Rect.MakeXYWH(bx, by, bw, bh), L.fill(BRASS, 0.25 + 0.2 * (1 - k)))
    c.drawRect(skia.Rect.MakeXYWH(bx, by, bw, bh), L.stroke(PAPER, 1.6, 0.8))
    if title:
        serif(c, b, title, x0, y0 - 90, at + 0.3, 50, PAPER, "left", L.SERIF)
    if k < 0.999:
        return
    x = x0
    for (lab, v, fill, ink, ti) in parts:
        kk = b.k(ti, 0.6)
        ww = w * v / total
        if kk > 0:
            c.drawRect(skia.Rect.MakeXYWH(x, y0, ww * kk, h), L.fill(fill))
            c.drawRect(skia.Rect.MakeXYWH(x, y0, ww * kk, h), L.stroke(PAPER, 1.5, 0.7))
            ka = b.k(ti + 0.3, 0.4)
            if ww < 220:                                    # too thin to hold its label: a callout under the bar
                c.drawLine(x + ww / 2, y0 + h + 6, x + ww / 2, y0 + h + 34, L.stroke(fill, 2, ka))
                L.text(c, lab, x + ww / 2, y0 + h + 78, L.font(L.SERIF_M, 36), L.fill(fill, ka), "center")
            else:
                f = L.font(L.SERIF_M, 40)
                while f.getSize() > 18 and f.measureText(lab) > ww - 50:
                    f = L.font(L.SERIF_M, f.getSize() - 2)
                L.text(c, lab, x + 26, y0 + h / 2 + 14, f, L.fill(ink, ka), "left")
        x += ww
    if src:
        source(c, b, src, at + 1.0)


def phone(c, b, x, y, at):
    """A phone at checkout: several one-tap ways to pay stacked, the brass one among them."""
    k = b.k(at, 0.5)
    if k <= 0:
        return
    w, h = 360, 680
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 48, 48)
    c.drawRRect(r, L.fill("#0F1622", 0.95 * k))
    c.drawRRect(r, L.stroke(PAPER, 2.2, k))
    typed(c, b, "CHECKOUT", x, y - h / 2 + 80, at + 0.2, 22, MUTED)
    for i in range(4):
        ki = b.k(at + 0.4 + 0.2 * i, 0.4)
        if ki <= 0:
            continue
        yy = y - 120 + i * 110
        rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 130, yy - 34, 260, 68), 34, 34)
        if i == 1:
            c.drawRRect(rr, L.fill(BRASS, 0.95 * ki))
            L.text(c, "PAY", x, yy + 12, L.font(L.SERIF_B, 32), L.fill(INK, ki), "center", track=0.12)
        else:
            c.drawRRect(rr, L.stroke(PAPER, 2, 0.8 * ki))
            L.text(c, "ONE TAP", x, yy + 10, L.font(L.MONO_M, 22), L.fill(PAPER, 0.8 * ki), "center", track=0.12)


def tap(c, b):
    k = b.k(b.t0, 0.5)
    press = ease(seg(b.t, b.w("tap", "tapping") - 0.1, b.w("tap", "tapping") + 0.15)) * (
        1 - ease(seg(b.t, b.w("tap", "tapping") + 0.3, b.w("tap", "tapping") + 0.6)))
    button(c, CX, 420, 520, k, press)
    person(c, CX - 420, 470, 130, b.k(b.t0 + 0.2, 0.5))
    typed(c, b, "$100", CX, 640, b.w("tap", "hundred") - 0.3, 40, PAPER)


def trail(c, b):
    note(c, b, b.k(b.t0, 0.6))
    typed(c, b, "ONE PAYMENT, FOLLOWED TO THE END", CX, 740, b.w("trail", "follow") - 0.2, 28, BRASS)


def receipt_fee(c, b):
    receipt(c, b, 620, 210, 680, "A SALE OF $100 · PAYPAL CHECKOUT", "What the shop gets",
            [("SALE", "$100.00"), ("FEE · 3.49% + $0.49", "−$3.98"), ("THE SHOP RECEIVES", "$96.02")],
            times=[b.t0 + 0.4, b.w("fee", "comes") - 0.2, b.w("fee", "before") - 0.2], circle=1)
    source(c, b, FEES, b.t0 + 1.0)


def avg_sliver(c, b):
    t = b.w("avg", "hundred") - 0.3
    note(c, b, 1.0, cut=SLIVER * b.k(t, 0.6), cut_label="$1.85", glow=b.k(b.w("avg", "earned") - 0.2, 0.4))
    typed(c, b, "PAYPAL'S REVENUE PER $100 PAID · 2025 AVERAGE", CX, 820, b.t0 + 0.3, 24, BRASS)
    source(c, b, "$33.2B ÷ $1.79T · " + K10, b.t0 + 1.2)


def behind(c, b):
    person(c, 300, 470, 120, b.k(b.t0, 0.4))
    node(c, b, 800, 470, 500, 140, "Another company's page", "ITS OWN NAME ON THE CHECKOUT", b.t0 + 0.3)
    node(c, b, 1340, 470, 380, 140, "Braintree", "PAYPAL'S CARD PROCESSING", b.w("braintree", "braintree,") - 0.2)
    bank(c, 1720, 470, 70, b.k(b.w("braintree", "handles") - 0.2, 0.4))
    arrow(c, b, [(380, 470), (440, 470), (490, 470), (535, 470)], b.t0 + 0.5, "", PAPER, "coin")
    arrow(c, b, [(1060, 470), (1090, 470), (1120, 470), (1140, 470)], b.w("braintree", "braintree,"), "", BRASS, "coin")
    arrow(c, b, [(1540, 470), (1580, 470), (1610, 470), (1635, 470)], b.w("braintree", "handles"), "", BRASS, "coin")


def money_cut(c, b):
    """The $1.85 sliver of the note grows into a bar and is cut into who else gets paid."""
    nx, ny, nw, nh = NOTE
    sw = nw * SLIVER
    parts = [("Card networks and banks · 89¢", 0.89, "#3A4560", PAPER, b.w("networks", "networks") - 0.2),
             ("Losses · 10¢", 0.10, RED, PAPER, b.w("losses", "fraud,") - 0.2),
             ("Left · 86¢", 0.86, BRASS, INK, b.w("left", "leaves") - 0.2)]
    cut_bar(c, b, parts, 1.85, b.t0 + 0.1, grow_from=(nx + nw - sw, ny, sw, nh), title="The $1.85, cut up",
            src="TRANSACTION EXPENSE RATE 0.89% · TRANSACTION AND CREDIT LOSS RATE 0.10% · " + K10)


def profit_cut(c, b):
    left = (190 + 1540 * (0.99 / 1.85), 400, 1540 * (0.86 / 1.85), 200)       # the 86¢ piece, where money_cut left it
    parts = [("Staff, tech, marketing, offices", 0.52, "#3A4560", PAPER, b.t0 + 0.6),
             ("Profit · 34¢", 0.34, BRASS, INK, b.w("profit", "thirty-four") - 0.3)]
    cut_bar(c, b, parts, 0.86, b.t0 + 0.1, grow_from=left, title="The 86¢",
            src="$6.1B OPERATING INCOME ÷ $1.79T · " + FY)


def balance(c, b):
    card(c, CX - 260, 430, 380, b.k(b.t0, 0.5), PAPER, "BALANCE")
    coins(c, CX + 300, 520, 14, b.k(b.w("balance", "holds") - 0.2, 0.5), 20, 7)
    typed(c, b, "MONEY LEFT SITTING IN BALANCES", CX, 700, b.w("balance", "leave") - 0.2, 26, PAPER)
    typed(c, b, "THE ASSETS UNDERNEATH EARN INTEREST", CX, 760, b.w("balance", "interest.") - 0.4, 26, BRASS)


def two(c, b):
    button(c, CX - 380, 430, 380, b.k(b.t0 + 0.1, 0.5))
    for i in range(3):
        server(c, CX + 300 + (i - 1) * 140, 430, 70, b.k(b.t0 + 0.4 + 0.1 * i, 0.5), PAPER, 0.8)
    typed(c, b, "THE BUTTON", CX - 380, 620, b.t0 + 0.6, 28, BRASS)
    typed(c, b, "THE PIPES", CX + 300, 620, b.t0 + 0.8, 28, PAPER)


def fees_compare(c, b):
    bars(c, b, [("A STANDARD CARD PAYMENT THROUGH PAYPAL · US", 2.99, "2.99% + 49¢", MUTED, b.w("card", "standard") - 0.3),
                ("PAYPAL CHECKOUT · THE BUTTON · US", 3.49, "3.49% + 49¢", BRASS, b.w("card", "extra") - 0.4)],
         b.t0, x0=300, y0=380, w=1000, gap=200, vmax=4.0)
    source(c, b, FEES, b.t0 + 1.0)


def close(c, b):
    note(c, b, b.k(b.t0, 0.6), y0=260)
    statement(c, b, [("Someone is earning interest on idle money.", b.t0 + 0.2),
                     ("Check that the someone is you.", b.w("close", "checking") - 0.3)], y=700, size=56, cols=[PAPER, BRASS])
    typed(c, b, ledger.BRAND, CX, 900, tl.le("close") + 0.6, 30, BRASS, track=0.3)


BOARD = Board([
    # 0 · ONE HUNDRED DOLLARS
    Beat("tap", tap),
    Beat("trail", trail),
    Beat("scale", lambda c, b: number(c, b, "$1.79 trillion", "PAID THROUGH PAYPAL · 2025", src=FY)),
    Beat("small", lambda c, b: statement(c, b, ["What it keeps from each payment is tiny.",
                                                ("The way it adds up is the whole story.", b.w("small", "way") - 0.3)],
                                         size=64, cols=[PAPER, BRASS])),
    # 1 · THE TOLL
    Beat("toll", lambda c, b: (shop(c, CX, 300, 110, b.k(b.t0, 0.5)),
                               number(c, b, "3.49% + 49¢", "PAYPAL CHECKOUT · US STANDARD RATE", y=600, size=140,
                                      at=b.w("toll", "costs") - 0.4, src=FEES))),
    Beat("fee", receipt_fee),
    Beat("why", lambda c, b: (statement(c, b, ["Shops pay because the button sells.",
                                               ("Fewer shoppers abandon their basket.", b.w("why", "fewer") - 0.3)],
                                        size=62, cols=[PAPER, BRASS]),
                              source(c, b, "PAYPAL FORM 10-K, 2025: \"REDUCE CART ABANDONMENT\"", b.t0 + 1.0))),
    # 2 · THE AVERAGE
    Beat("avg", avg_sliver),
    Beat("who", lambda c, b: ticks(c, b, [("Large merchants negotiate lower rates.", b.w("who", "large") - 0.3),
                                          ("Much of the volume isn't the button at all.", b.w("who", "share") - 0.3)],
                                   b.t0, x=380, y=380, size=52)),
    Beat("braintree", behind),
    Beat("psp", lambda c, b: number(c, b, "9.3 billion", "PAYMENTS PROCESSED WITHOUT THE PAYPAL NAME · 2025",
                                    src="25.4B PAYMENTS − 16.1B EXCLUDING PSP · " + FY)),
    Beat("third", lambda c, b: bars(c, b, [("UNBRANDED PROCESSING", 9.3, "9.3 billion", BRASS, b.t0 + 0.2),
                                           ("EVERYTHING ELSE", 16.1, "16.1 billion", MUTED, b.t0 + 0.6)],
                                    b.t0, x0=300, y0=380, w=1000, gap=200, vmax=18)),
    # 3 · WHO ELSE GETS PAID: one continuous beat while the bar is cut
    Beat("networks", money_cut, until="left"),
    # 4 · THIRTY-FOUR CENTS
    Beat("costs", lambda c, b: ticks(c, b, [("Engineers.", b.w("costs", "engineers,") - 0.3),
                                            ("Customer service.", b.w("costs", "customer") - 0.3),
                                            ("Marketing.", b.w("costs", "marketing") - 0.3),
                                            ("Offices.", b.w("costs", "offices.") - 0.3)], b.t0, x=640, y=320, gap=100, size=54)),
    Beat("profit", profit_cut),
    Beat("total", lambda c, b: number(c, b, "$6.1 billion", "PAYPAL'S OPERATING INCOME · 2025", src=FY)),
    # 5 · MONEY THAT SITS STILL
    Beat("still", lambda c, b: floor_card(c, b, "+", "Money That Sits Still", "ONE MORE SOURCE OF INCOME")),
    Beat("balance", balance),
    Beat("interest", lambda c, b: number(c, b, "~$1.3 billion", "INTEREST ON CUSTOMER BALANCES · 2025",
                                         src="$15.5B − $14.2B: TRANSACTION MARGIN WITH AND WITHOUT IT · " + FY)),
    Beat("yours", lambda c, b: statement(c, b, ["In an ordinary balance,",
                                                ("the interest goes to PayPal.", b.w("yours", "paypal,") - 0.3),
                                                ("None of it comes to you.", b.w("yours", "none") - 0.3)],
                                         size=66, cols=[PAPER, PAPER, BRASS])),
    # 6 · TWO PAYPALS
    Beat("two", two, until="pipes"),
    Beat("shed", lambda c, b: (typed(c, b, "BRAINTREE · 2025", CX, 250, b.t0 + 0.2, 26, PAPER),
                               quote(c, b, ["Our strategic shift", "as we focus on profitable growth."], K10,
                                     b.w("shed", "shift") - 0.3))),
    # 7 · THE BUTTON'S PROBLEM
    Beat("game", lambda c, b: (button(c, CX, 330, 420, b.k(b.t0, 0.5)),
                               statement(c, b, ["The part that matters most", ("is where PayPal is struggling.",
                                                                               b.w("game", "struggling.") - 0.4)],
                                         y=580, size=60, cols=[PAPER, BRASS]))),
    Beat("quote", lambda c, b: quote(c, b, ["Our execution has not been where it needs to be,",
                                            "particularly in branded checkout."], FY, b.w("quote", "execution") - 0.3,
                                     size=54)),
    Beat("ceo", lambda c, b: (typed(c, b, "3 FEBRUARY 2026", CX, 300, b.t0 + 0.2, 26, BRASS),
                              serif(c, b, "A new chief executive: Enrique Lores.", CX, 480, b.w("ceo", "enrique") - 0.4, 64))),
    Beat("phone", lambda c, b: (phone(c, b, CX - 300, 470, b.t0 + 0.1),
                                typed(c, b, "EVERY BUTTON WANTS", CX + 360, 440, b.w("phone", "competing") - 0.3, 30, PAPER),
                                typed(c, b, "THE SAME MOMENT", CX + 360, 500, b.w("phone", "moment.") - 0.4, 30, BRASS))),
    Beat("verdict", lambda c, b: statement(c, b, ["Plenty of companies can move money.",
                                                  ("PayPal's valuable thing is a moment:", b.w("verdict", "valuable") - 0.3),
                                                  ("a shopper trusting the button enough to press it.",
                                                   b.w("verdict", "trusts") - 0.3)],
                                           size=56, cols=[PAPER, PAPER, BRASS], face=L.SERIF_I)),
    Beat("card", fees_compare),
    Beat("close", close),
], tail=4.0)


def frame(c, t):
    BOARD.frame(c, t)


def end_time():
    return BOARD.end()
