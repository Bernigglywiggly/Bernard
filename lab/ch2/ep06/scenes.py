"""HOW THEY PROFIT · EP06 · THE COMPANY THAT NEVER TOUCHES YOUR MONEY (Visa): the storyboard (ch2/kit.py) in the
ledger look, keyed to the script's line ids and the narrator's words. No logos anywhere: Visa is a brass node.

CRAFT.md applied: a different shape from EP05 (a map and a route, where EP05 cut up a banknote). The persistent object
is the MESSAGE, a small brass packet: it crosses the Atlantic in the cold open, runs the four-party route in chapters
1-2 and 6, and makes the same crossing again at the close so the film loops. Money (coins) only ever moves between
the two banks, underneath the Visa node, which is the whole argument in one picture.

The map is real (Natural Earth 1:110m land, public domain; Lisbon 38.72N 9.14W, Columbus, Ohio 39.96N 83.00W); the
payment on it is an illustration and says so on screen.

  0 ONE SECOND              the Atlantic: the tap in Lisbon, the message out to Ohio and back; $17T; never held it
  1 FOUR PARTIES            the route: cafe, cafe's bank, Visa, card's bank; "not a financial institution"; the risk
  2 THE FEE IT DOESN'T KEEP interchange: coins from bank to bank under the Visa node; why set a fee you don't keep
  3 THREE METERS            $17.5B; 257.5B messages, 700M a day; $20.0B; the border, $14.2B; the four lines as bars
  4 THE MONEY IT HANDS BACK $15.8B; $55.8B less incentives = $40.0B; about 24 cents per $100
  5 HALF                    $16.0B costs; $20.1B; 50 cents of each dollar; what a bank needs and Visa doesn't; $22.8B
  6 THE RULEBOOK            the fee turns red; $2.5B; regulators; the verdict; the shop's bank; the crossing again
"""
import json
import math
import os

import engine  # noqa: F401  (paths)
import skia  # noqa: E402

from engine import tl  # noqa: E402
from ch2 import look as L  # noqa: E402
from ch2 import ledger  # noqa: E402
from ch2.kit import (Board, Beat, CX, PAPER, BRASS, RED, MUTED, INK, number, statement, floor_card,  # noqa: E402
                     node, typed, serif, source, shop, bank, server, card, bars, ticks, quote, ease, seg, lerp)

K8 = "VISA, FISCAL FOURTH QUARTER AND FULL-YEAR 2025 RESULTS (8-K, 28 OCT 2025)"
K10 = "VISA FORM 10-K, FISCAL 2025 (SEC EDGAR)"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- the map (the North Atlantic, equirectangular)
LON0, LON1, LAT0, LAT1 = -104.0, 14.0, 22.0, 58.0
MX0, MY0, MW, MH = 150.0, 130.0, 1620.0, 690.0
LISBON, OHIO = (-9.14, 38.72), (-83.00, 39.96)
_LAND = []


def xy(lon, lat):
    return MX0 + (lon - LON0) / (LON1 - LON0) * MW, MY0 + (LAT1 - lat) / (LAT1 - LAT0) * MH


def land():
    if not _LAND:
        d = json.load(open(os.path.join(HERE, "data", "ne_110m_land.geojson")))
        p = skia.Path()
        for f in d["features"]:
            for ring in f["geometry"]["coordinates"]:
                if max(x for x, _ in ring) < LON0 - 5 or min(x for x, _ in ring) > LON1 + 5:
                    continue
                if max(y for _, y in ring) < LAT0 - 5 or min(y for _, y in ring) > LAT1 + 5:
                    continue
                p.moveTo(*xy(*ring[0]))
                for pt in ring[1:]:
                    p.lineTo(*xy(*pt))
                p.close()
        _LAND.append(p)
    return _LAND[0]


def arc(u):
    """A point u (0..1) along the crossing from Lisbon to Ohio, bowed north the way a great circle looks on this map."""
    (x0, y0), (x1, y1) = xy(*LISBON), xy(*OHIO)
    return lerp(x0, x1, u), lerp(y0, y1, u) - 190 * math.sin(math.pi * u)


def packet(c, x, y, a=1.0, s=1.0):
    """The message: a small brass packet with a pale centre (the film's persistent object)."""
    if a <= 0:
        return
    c.drawRect(skia.Rect.MakeXYWH(x - 15 * s, y - 10 * s, 30 * s, 20 * s), L.fill(BRASS, a))
    c.drawRect(skia.Rect.MakeXYWH(x - 8 * s, y - 3 * s, 16 * s, 6 * s), L.fill(INK, 0.85 * a))


def pin(c, b, lonlat, label, sub, at, side=1):
    k = b.k(at, 0.4)
    if k <= 0:
        return
    x, y = xy(*lonlat)
    pulse = (b.t - at) % 2.4 / 2.4                                  # never quite still: a slow ring off each place
    c.drawCircle(x, y, 10 + 46 * pulse, L.stroke(BRASS, 2, 0.5 * (1 - pulse) * k))
    c.drawCircle(x, y, 9, L.fill(BRASS, k))
    typed(c, b, label, x + 26 * side, y - 22, at + 0.15, 26, PAPER, "left" if side > 0 else "right", 0.14)
    typed(c, b, sub, x + 26 * side, y + 14, at + 0.4, 18, MUTED, "left" if side > 0 else "right", 0.1, L.MONO)


def atlantic(c, b, a=1.0):
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(MX0, MY0, MW, MH))
    for lon in range(-100, 20, 20):                                 # graticule
        x, _ = xy(lon, 0)
        c.drawLine(x, MY0, x, MY0 + MH, L.stroke(MUTED, 1, 0.16 * a))
    for lat in range(30, 60, 10):
        _, y = xy(0, lat)
        c.drawLine(MX0, y, MX0 + MW, y, L.stroke(MUTED, 1, 0.16 * a))
    c.drawPath(land(), L.fill("#16202F", 0.95 * a))
    c.drawPath(land(), L.stroke(MUTED, 1.4, 0.55 * a))
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(MX0, MY0, MW, MH), L.stroke(PAPER, 1.4, 0.35 * a))


def route_line(c, k, a=1.0):
    """The crossing drawn up to fraction k."""
    if k <= 0:
        return
    p = skia.Path()
    p.moveTo(*arc(0))
    for i in range(1, 61):
        if i / 60 > k:
            break
        p.lineTo(*arc(i / 60))
    c.drawPath(p, L.stroke(BRASS, 2.4, 0.85 * a))


def crossing(c, b, t_out, t_back, d=1.5):
    """The message out to Ohio and back; returns (out, back) progress."""
    out, back = ease(seg(b.t, t_out, t_out + d), "io"), ease(seg(b.t, t_back, t_back + d), "io")
    route_line(c, out)
    if 0 < out and back <= 0:
        packet(c, *arc(out), 1.0, 1.0 + 0.5 * math.sin(math.pi * out))
    elif back > 0:
        packet(c, *arc(1 - back), 1.0, 1.0 + 0.5 * math.sin(math.pi * back))
    return out, back


def opening(c, b):
    atlantic(c, b)
    pin(c, b, LISBON, "A CAFÉ · LISBON", "38.72°N  9.14°W", b.t0 + 0.1, side=1)
    t_out, t_back = b.w("ocean", "left") - 0.3, b.w("ocean", "come") - 0.5
    out, back = crossing(c, b, t_out, t_back)
    if out >= 1:
        pin(c, b, OHIO, "A BANK · OHIO", "39.96°N  83.00°W", t_out + 1.5, side=1)
    typed(c, b, "APPROVED", xy(*LISBON)[0] - 30, xy(*LISBON)[1] + 70, b.w("tap", "approved") - 0.2, 34, BRASS, "right", 0.2)
    typed(c, b, "ABOUT ONE SECOND", xy(*LISBON)[0] - 30, xy(*LISBON)[1] + 112, b.w("tap", "second") - 0.2, 20, MUTED, "right", 0.14, L.MONO)
    typed(c, b, "ILLUSTRATION: ONE CARD PAYMENT ACROSS A BORDER", MX0 + 20, MY0 + MH - 22, b.t0 + 0.8, 18, MUTED, "left", 0.1, L.MONO, 70)


# ---------------------------------------------------------------- the route (four parties on one line)
RY = 410
STOPS = [(330, "The café", "WHERE THE CARD IS TAPPED"), (790, "The café's bank", "COLLECTS CARD PAYMENTS"),
         (1210, "The network", "CARRIES THE MESSAGE"), (1620, "The card's bank", "ISSUED THE CARD")]
NW, NH = 330, 150


def stop(c, b, i, at, hot=False, a=1.0):
    x, title, sub = STOPS[i]
    k = b.k(at, 0.45) * a
    if k <= 0:
        return
    node(c, b, x, RY, NW, NH, title, sub, at)
    if hot:                                                         # the network is the brass one
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - NW / 2, RY - NH / 2, NW, NH), 6, 6)
        c.drawRRect(r, L.stroke(BRASS, 3.2, 0.95 * k))


def wire(c, b, i, at):
    """The wire from stop i to stop i+1, with the message riding it."""
    k = b.k(at, 0.5)
    if k <= 0:
        return
    x0, x1 = STOPS[i][0] + NW / 2, STOPS[i + 1][0] - NW / 2
    c.drawLine(x0, RY, lerp(x0, x1, k), RY, L.stroke(PAPER, 2.2, 0.8))
    if k >= 1:
        u = ((b.t - at) * 0.55 + i * 0.33) % 1.0
        packet(c, lerp(x0, x1, u), RY, 0.95, 0.8)


def route(c, b, times, wires=True):
    for i, t in enumerate(times):
        if t is None:
            continue
        stop(c, b, i, t, hot=(i == 2))
        if wires and i < 3 and times[i + 1] is not None:
            wire(c, b, i, max(t, times[i + 1]) + 0.3)


def interchange(c, b, at, col=BRASS, label="INTERCHANGE"):
    """Coins from the café's bank to the card's bank, passing UNDER the network without stopping there."""
    k = b.k(at, 0.9)
    if k <= 0:
        return
    xa, xb, y0, dip = STOPS[1][0], STOPS[3][0], RY + NH / 2 + 6, 190
    p = skia.Path()
    n = 48
    for j in range(n + 1):
        u = j / n * k
        x, y = lerp(xa, xb, u), y0 + dip * math.sin(math.pi * u)
        (p.moveTo if j == 0 else p.lineTo)(x, y)
    c.drawPath(p, L.stroke(col, 2.6, 0.9))
    if k >= 1:
        for j in range(4):
            u = ((b.t - at) * 0.3 + j / 4) % 1.0
            L.coin(c, lerp(xa, xb, u), y0 + dip * math.sin(math.pi * u), 14, 0.95)
        typed(c, b, label, (xa + xb) / 2, y0 + dip + 56, at + 0.9, 30, col, "center", 0.2)


def parties(c, b):
    t = [b.t0 + 0.1, tl.ls("shopbank") - 0.1, tl.ls("yourbank") + 1.6, tl.ls("yourbank") - 0.1]
    route(c, b, t)
    typed(c, b, "ONE CARD PAYMENT · FOUR PARTIES", CX, 190, b.t0 + 0.3, 26, BRASS, "center", 0.2)


def the_fee(c, b):
    route(c, b, [b.t0 - 5] * 4)
    interchange(c, b, b.t0 + 0.3)
    typed(c, b, "SETS THE DEFAULT RATES", STOPS[2][0], RY - NH / 2 - 34, b.w("sets", "writes") - 0.3, 22, BRASS, "center", 0.14)
    typed(c, b, "COLLECTS NONE OF IT", STOPS[2][0], RY - NH / 2 - 70, b.w("sets", "without") - 0.3, 22, PAPER, "center", 0.14)
    source(c, b, K10 + ": \"IRFS ARE PAID BY ACQUIRERS TO ISSUERS. WE ESTABLISH DEFAULT IRFS\"", b.t0 + 1.2)


def the_weak_point(c, b):
    route(c, b, [b.t0 - 5] * 4)
    interchange(c, b, b.t0 + 0.2, RED, "THE FEE IT SETS AND NEVER COLLECTS")


# ---------------------------------------------------------------- the money
def meters(c, b):
    floor_card(c, b, "III", "Three Meters", "WHAT VISA CHARGES THE BANKS")


def border(c, b):
    """The third meter: the crossing again, small, with the border it trips marked mid-ocean."""
    atlantic(c, b, 0.8)
    route_line(c, b.k(b.t0 + 0.1, 1.0))
    u = ((b.t - b.t0) * 0.28) % 1.0
    packet(c, *arc(u), 1.0, 1.0)
    bx, by = arc(0.5)
    kb = b.k(b.w("border", "different") - 0.3, 0.5)
    c.drawLine(bx, by - 150, bx, by - 150 + 300 * kb, L.stroke(RED, 2.4, 0.9 * kb))
    typed(c, b, "A BORDER CROSSED", bx + 20, by + 120, b.w("border", "different") - 0.1, 22, RED, "left", 0.14)
    serif(c, b, "$14.2 billion", CX, 760, b.w("border", "crossings") - 0.3, 110, PAPER)
    typed(c, b, "INTERNATIONAL TRANSACTION REVENUE · FISCAL 2025", CX, 820, b.w("border", "crossings") + 0.2, 24, BRASS)


def four_lines(c, b):
    bars(c, b, [("SERVICE", 17.5, "$17.5B", MUTED, b.t0 + 0.1), ("DATA PROCESSING", 20.0, "$20.0B", BRASS, b.t0 + 0.4),
                ("INTERNATIONAL", 14.2, "$14.2B", MUTED, b.t0 + 0.7), ("OTHER", 4.1, "$4.1B", PAPER, b.w("other", "fourth") - 0.2)],
         b.t0, x0=300, y0=250, w=1050, h=70, gap=135, vmax=22)
    source(c, b, K8, b.t0 + 1.2)


def handed_back(c, b):
    """$55.8B charged, $15.8B handed back, $40.0B kept: one bar, the incentives peeling off the end."""
    x0, y0, w, h = 240, 380, 1440, 170
    k = b.k(b.t0 + 0.1, 0.7)
    ki = b.k(b.w("net", "remained") - 0.6, 0.8)
    wi = w * 15.8 / 55.8
    drop = 215 * ki                                                  # the incentives fall clear of the bar
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, (w - wi) * k, h), L.fill(BRASS, 0.3))
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, (w - wi) * k, h), L.stroke(PAPER, 1.6, 0.8))
    typed(c, b, "CHARGED TO BANKS AND PARTNERS · $55.8 BILLION", x0, y0 - 28, b.t0 + 0.3, 24, MUTED, "left", 0.12)
    if k > 0:
        kw = min(1.0, max(0.0, (k * w - (w - wi)) / wi))
        c.drawRect(skia.Rect.MakeXYWH(x0 + w - wi, y0 + drop, wi * kw, h), L.fill(MUTED, 0.5))
        c.drawRect(skia.Rect.MakeXYWH(x0 + w - wi, y0 + drop, wi * kw, h), L.stroke(PAPER, 1.4, 0.7))
        serif(c, b, "$15.8B", x0 + w - wi / 2, y0 + drop + 108, b.t0 + 0.8, 64, PAPER, rise=0)
        typed(c, b, "HANDED BACK AS INCENTIVES", x0 + w - wi / 2, y0 + drop + h + 40, b.t0 + 1.0, 22, MUTED)
    if ki > 0:
        wk = w - wi
        c.drawRect(skia.Rect.MakeXYWH(x0, y0, wk, h), L.fill(BRASS, 0.9 * ki))
        serif(c, b, "$40.0 billion", x0 + 40, y0 + 112, b.w("net", "remained") - 0.2, 96, INK, "left", rise=0)
        typed(c, b, "VISA'S NET REVENUE · FISCAL 2025", x0, y0 + h + 44, b.w("net", "remained") + 0.2, 24, BRASS, "left", 0.12)
    source(c, b, K8, b.t0 + 1.2)


def sliver(c, b):
    """$100 moved; Visa's 24 cents is too thin to see at scale, so the end of the strip is magnified."""
    x0, y0, w, h = 240, 300, 1440, 110
    k = b.k(b.t0 + 0.1, 0.6)
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w * k, h), L.fill("#121A27", 0.95))
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w * k, h), L.stroke(PAPER, 2, 0.85))
    serif(c, b, "$100 moved", x0 + 40, y0 + 76, b.t0 + 0.4, 60, PAPER, "left", rise=0)
    ks = b.k(b.w("cents", "kept") - 0.6, 0.6)
    if ks > 0:
        c.drawRect(skia.Rect.MakeXYWH(x0 + w - 4, y0, 4, h), L.fill(BRASS, ks))          # 0.24% of 1440 px = 3.5 px
        c.drawLine(x0 + w - 2, y0 + h + 6, x0 + w - 2, y0 + h + 70, L.stroke(BRASS, 2, ks))
        serif(c, b, "about 24¢", x0 + w, y0 + h + 190, b.w("cents", "kept") - 0.3, 130, BRASS, "right")
        typed(c, b, "VISA'S NET REVENUE PER $100 MOVED ON ITS NETWORK", x0 + w, y0 + h + 250, b.w("cents", "kept") + 0.2, 24, PAPER, "right", 0.12)
    source(c, b, "$40.0B NET REVENUE ÷ $17T PAYMENTS AND CASH VOLUME · " + K8 + " · " + K10, b.t0 + 1.2)


def half(c, b):
    x0, y0, w, h = 240, 360, 1440, 190
    k = b.k(b.t0 + 0.1, 0.6)
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w * k, h), L.stroke(PAPER, 2, 0.85))
    typed(c, b, "ONE DOLLAR OF NET REVENUE", x0, y0 - 28, b.t0 + 0.3, 24, MUTED, "left", 0.12)
    kp = b.k(b.w("half", "50") - 0.5, 0.8)
    if kp > 0:
        c.drawRect(skia.Rect.MakeXYWH(x0, y0, w * 0.5 * kp, h), L.fill(BRASS, 0.92))
        serif(c, b, "50¢ profit", x0 + 40, y0 + 124, b.w("half", "50") - 0.2, 100, INK, "left", rise=0)
        typed(c, b, "COSTS, TAX AND EVERYTHING ELSE", x0 + w * 0.75, y0 + h / 2 + 8, b.w("half", "50") + 0.3, 22, MUTED)
    source(c, b, "$20.1B NET INCOME ÷ $40.0B NET REVENUE · " + K8, b.t0 + 1.2)


def why(c, b):
    """What a bank has to carry, and what the network carries."""
    lx, rx = CX - 420, CX + 420
    bank(c, lx, 250, 90, b.k(b.t0 + 0.1, 0.5))
    typed(c, b, "A BANK NEEDS", lx, 370, b.t0 + 0.3, 26, MUTED)
    for i, (txt, wd) in enumerate([("Branches", "branches,"), ("Loan books", "loan"), ("Reserves for bad debts", "reserves")]):
        serif(c, b, txt, lx, 450 + i * 84, b.w("why", wd) - 0.3, 52, PAPER)
    for j in range(2):
        server(c, rx - 70 + j * 140, 250, 76, b.k(b.w("why", "visa") - 0.3 + 0.1 * j, 0.5), BRASS, 0.9)
    typed(c, b, "THE NETWORK NEEDS", rx, 370, b.w("why", "visa") - 0.2, 26, BRASS)
    for i, (txt, wd) in enumerate([("Data centres", "data"), ("A rulebook", "rulebook,")]):
        serif(c, b, txt, rx, 450 + i * 84, b.w("why", wd) - 0.3, 52, BRASS)
    c.drawLine(CX, 220, CX, 220 + 460 * b.k(b.t0 + 0.2, 0.7), L.stroke(MUTED, 1.4, 0.5))


def closing(c, b):
    atlantic(c, b)
    pin(c, b, LISBON, "A CAFÉ · LISBON", "", b.t0 + 0.1, side=1)
    pin(c, b, OHIO, "A BANK · OHIO", "", b.t0 + 0.3, side=1)
    crossing(c, b, b.t0 + 0.5, b.w("close", "banks,") - 0.4, d=1.8)
    typed(c, b, "APPROVED", xy(*LISBON)[0] - 30, xy(*LISBON)[1] + 70, b.w("close", "approved,") - 0.2, 34, BRASS, "right", 0.2)
    typed(c, b, ledger.BRAND, CX, MY0 + MH + 60, tl.le("close") + 0.6, 30, BRASS, track=0.3)


BOARD = Board([
    # 0 · ONE SECOND
    Beat(-0.6, opening, until="ocean"),          # frame 0 is the finished map with the café on it (CRAFT §3)
    Beat("scale", lambda c, b: number(c, b, "$17 trillion", "PAYMENTS AND CASH VOLUME ON VISA'S NETWORK · FISCAL 2025", src=K10)),
    Beat("never", lambda c, b: statement(c, b, ["The company in the middle of that route",
                                                ("never held any of the money.", b.w("never", "never") - 0.3)],
                                         size=68, cols=[PAPER, BRASS])),
    # 1 · FOUR PARTIES
    Beat("four", parties, until="yourbank"),
    Beat("quote", lambda c, b: quote(c, b, ["Visa is not a financial institution.",
                                            "We do not issue cards, extend credit", "or set rates and fees for account holders."],
                                     K10, b.w("quote", "plain") - 0.3, size=54)),
    Beat("risk", lambda c, b: (bank(c, CX, 250, 100, b.k(b.t0, 0.5)),
                               statement(c, b, ["When a cardholder never pays the bill,",
                                                ("the loss belongs to the bank.", b.w("risk", "loss") - 0.3)],
                                         y=520, size=62, cols=[PAPER, BRASS]))),
    # 2 · THE FEE IT DOESN'T KEEP
    Beat("fee", the_fee, until="sets"),
    Beat("whyset", lambda c, b: statement(c, b, ["The fee pays banks to issue Visa's cards.",
                                                 ("Every card sends more messages", b.w("whyset", "every") - 0.3),
                                                 ("down Visa's wires.", b.w("whyset", "wires.") - 0.5)],
                                          size=62, cols=[PAPER, PAPER, BRASS])),
    # 3 · THREE METERS
    Beat("meters", meters),
    Beat("service", lambda c, b: number(c, b, "$17.5 billion", "METER ONE · SERVICE REVENUE · FISCAL 2025",
                                        at=b.w("service", "brought") - 0.4, src=K8)),
    Beat("count", lambda c, b: number(c, b, "257.5 billion", "TRANSACTIONS PROCESSED BY VISA · FISCAL 2025",
                                      at=b.w("count", "processed") - 0.4, src=K8)),
    Beat("daily", lambda c, b: (number(c, b, "≈ 700 million", "MESSAGES EVERY DAY", src="257.5 BILLION ÷ 365 · " + K8),
                                [packet(c, 200 + ((b.t * 420 + j * 173) % 1520), 760 + 22 * (j % 3), 0.8, 0.7) for j in range(9)])),
    Beat("processing", lambda c, b: number(c, b, "$20.0 billion", "METER TWO · DATA PROCESSING REVENUE · FISCAL 2025",
                                           at=b.w("processing", "earned") - 0.4, src=K8)),
    Beat("border", border),
    Beat("other", four_lines),
    # 4 · THE MONEY IT HANDS BACK
    Beat("back", lambda c, b: statement(c, b, ["Before any of this counts as revenue,",
                                               ("Visa gives a large part of it back.", b.w("back", "gives") - 0.3)],
                                        size=64, cols=[PAPER, BRASS])),
    Beat("incentives", lambda c, b: number(c, b, "$15.8 billion", "INCENTIVES PAID TO BANKS AND PARTNERS · FISCAL 2025",
                                           at=b.w("incentives", "paid") - 0.4, src=K8)),
    Beat("net", handed_back),
    Beat("cents", sliver),
    # 5 · HALF
    Beat("thin", lambda c, b: statement(c, b, ["A slice that thin sounds like a low-margin business.",
                                               ("Visa is close to the opposite.", b.w("thin", "opposite.") - 0.6)],
                                        size=60, cols=[PAPER, BRASS])),
    Beat("costs", lambda c, b: number(c, b, "$16.0 billion", "OPERATING EXPENSES · FISCAL 2025 · INCLUDES A LITIGATION PROVISION",
                                      at=b.w("costs", "cost") - 0.4, src=K8)),
    Beat("profit", lambda c, b: number(c, b, "$20.1 billion", "VISA'S NET INCOME · FISCAL 2025", src=K8)),
    Beat("half", half),
    Beat("why", why),
    Beat("returned", lambda c, b: number(c, b, "$22.8 billion", "BUYBACKS AND DIVIDENDS · FISCAL 2025",
                                         at=b.w("returned", "sent") - 0.4, src=K8)),
    # 6 · THE RULEBOOK
    Beat("weak", the_weak_point, until="sued"),
    Beat("suits", lambda c, b: number(c, b, "$2.5 billion", "SET ASIDE FOR THE INTERCHANGE LITIGATION AND OTHER LEGAL MATTERS · FISCAL 2025",
                                      at=b.w("suits", "set") - 0.4, src=K8, col=RED)),
    Beat("regulators", lambda c, b: quote(c, b, ["Regulatory authorities and central banks",
                                                 "in a number of jurisdictions", "have reviewed or are reviewing these fees."],
                                          K10, b.t0 + 0.2, size=54)),
    Beat("verdict", lambda c, b: statement(c, b, ["Visa's real product is the rulebook",
                                                  ("that lets a café in Lisbon trust a bank in Ohio.", b.w("verdict", "lets") - 0.3),
                                                  ("The wires only deliver it.", b.w("verdict", "wires") - 0.3)],
                                           size=58, cols=[PAPER, PAPER, BRASS], face=L.SERIF_I)),
    Beat("shop", lambda c, b: (shop(c, CX - 520, 300, 100, b.k(b.t0, 0.5)), bank(c, CX + 520, 300, 100, b.k(b.t0 + 0.3, 0.5)),
                               statement(c, b, ["Most of a card payment's cost goes to banks.",
                                                ("The rate your own bank quotes is the part to negotiate.", b.w("shop", "rate") - 0.3)],
                                         y=580, size=54, cols=[PAPER, BRASS]))),
    Beat("close", closing),
], tail=4.0)


def frame(c, t):
    BOARD.frame(c, t)


def end_time():
    return BOARD.end()
