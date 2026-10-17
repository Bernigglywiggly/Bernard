"""MONEY CRIMES · long-form 02: "The Original Ponzi Scheme" (Charles Ponzi). 16:9, about 13.5 minutes.

The picture to the narration's timings (build/words.json from vo.py): GPT Image 2.5 stills and Kling 3.0 clips (src/ai,
see ai_assets.py; labelled AI RECONSTRUCTION on screen, and never Ponzi's face), public-domain photographs from
Wikimedia Commons and the Library of Congress (src/arch, credited on screen), and drawn graphics (maps, documents,
counters).

    python3 ../doc.py ponzi frames 12 50 300    # QC stills
    python3 ../doc.py ponzi render              # the film -> out/
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "ponzi"
SRC, BUILD = os.path.join(HERE, "src"), os.path.join(HERE, "build")
VOICE, WORDS = os.path.join(BUILD, "voice.wav"), os.path.join(BUILD, "words.json")
CH = json.load(open(os.path.join(BUILD, "chapters.json")))
END = CH["total"]
CARDS = {c["id"]: c["card"] for c in CH["chapters"]}
_W = json.load(open(WORDS))


def w(word, after=0.0):
    """When word is first said after `after` seconds (so the cuts follow the read, not hand-typed numbers)."""
    for x in _W:
        if x[1] >= after - 0.01 and x[0].strip(".,?!;:\"'").lower() == word.lower():
            return x[1]
    raise KeyError((word, after))


A = lambda n: os.path.join(SRC, "ai", n + ".png")
R = lambda n: os.path.join(SRC, "arch", n)
PUSH = ((0.5, 0.5, 1.0), (0.5, 0.5, 1.1))
PULL = ((0.5, 0.5, 1.12), (0.5, 0.5, 1.0))


def still(t, n, cam=PUSH, x=0.0, grade=None):
    return dict(t=t, kind="still", src=A(n), cam=cam, x=x, grade=grade, ai=True)


def clip(t, n, x=0.0):
    return dict(t=t, kind="clip", src=os.path.join(SRC, "ai", "k_" + n + ".mp4"), still=A(n), x=x, ai=True)


def arch(t, f, x=0.0, **kw):
    return dict(t=t, kind="arch", src=R(f), x=x, **kw)


def g(t, fn, x=0.0, **opt):
    return dict(t=t, kind="gfx", fn=fn, x=x, opt=opt)


NUM = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN"]


def card(cid, k, title, bg):
    return g(CARDS[cid], "card", x=0.5, kicker=f"CHAPTER {NUM[k]}", title=title, bg=A(bg))


BOSTON, MONTREAL, ATLANTA = (-71.06, 42.36), (-73.57, 45.50), (-84.39, 33.75)
LUGO, ROME, MADRID = (11.91, 44.42), (12.50, 41.90), (-3.70, 40.42)
JACKSONVILLE, NEW_ORLEANS = (-81.66, 30.33), (-90.07, 29.95)
ITALY = [(12.50, 41.90, "ROME"), (11.25, 43.77, "FLORENCE"), (9.19, 45.46, "MILAN"), (11.34, 44.49, "BOLOGNA"),
         (12.33, 45.44, "VENICE"), (14.27, 40.85, "NAPLES")]
STATES = "ne_50m_admin_1_states_provinces_lakes"
PORTRAIT = "CHARLES PONZI, 1920 · PUBLIC DOMAIN"
LOC = "CHARLES PONZI, 1920 · BAIN NEWS SERVICE, LIBRARY OF CONGRESS"
POLICE = "CHARLES PONZI · POLICE PHOTOGRAPH · PUBLIC DOMAIN"

SHOTS = [
    # ---- cold open
    clip(0.0, "o01"),
    still(5.0, "o01", ((0.5, 0.5, 1.08), (0.62, 0.55, 1.3))),
    still(11.1, "o02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14)), x=0.4),
    still(17.1, "o05", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.15))),
    still(22.0, "o03", ((0.45, 0.5, 1.1), (0.55, 0.45, 1.1)), x=0.4),
    g(27.8, "plate", bg=A("o06")),
    clip(30.6, "o04", x=0.4),
    still(35.6, "o04", ((0.5, 0.5, 1.1), (0.45, 0.5, 1.28))),
    still(43.3, "o05", ((0.6, 0.5, 1.25), (0.62, 0.5, 1.45))),
    arch(47.1, "ponzi_1920.jpg", mode="print", rot=-2.0, credit=PORTRAIT),
    arch(51.9, "dont_be_ponzied.jpg", mode="print", fit=0.92, rot=1.5,
         credit="'DON'T BE PONZIED' · BANK ADVERTISEMENT, 1920s · PUBLIC DOMAIN"),
    g(57.1, "title", x=0.6, bg=A("o06"), kicker="MONEY CRIMES", lines=["THE ORIGINAL", "PONZI SCHEME"],
      sub="THE TRUE STORY OF CHARLES PONZI"),
    # ---- 1 two dollars and fifty cents
    card("arrive", 0, "Two Dollars and Fifty Cents", "a02"),
    g(66.95, "map", x=0.5, v0=(12.0, 43.2, 16.0), v1=(11.9, 44.2, 8.0), move=6.0, towns=ITALY,
      pins=[(*LUGO, "LUGO", 1.5, "3 MARCH 1882")]),
    still(78.6, "a01", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.4),
    still(84.9, "a01", ((0.35, 0.55, 1.25), (0.3, 0.5, 1.4))),
    clip(89.0, "a02", x=0.4),
    still(94.0, "a03", ((0.5, 0.5, 1.0), (0.5, 0.55, 1.15))),
    still(96.7, "a04", ((0.5, 0.5, 1.0), (0.52, 0.5, 1.18))),
    g(100.0, "plate", bg=A("a04"), x=0.4),
    still(109.2, "a05", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.12)), x=0.4),
    still(w("slept", 110) - 0.2, "a06", ((0.5, 0.5, 1.12), (0.5, 0.55, 1.0))),
    still(115.3, "a07", ((0.5, 0.5, 1.0), (0.6, 0.5, 1.15))),
    still(122.3, "a05", ((0.3, 0.5, 1.3), (0.35, 0.5, 1.45))),
    # ---- 2 robbing Peter
    card("montreal", 1, "Robbing Peter", "m01"),
    g(131.0, "map", x=0.5, v0=(-73.0, 43.6, 14.0), borders=STATES, routes=[(BOSTON, MONTREAL, 0.4, 1.8)],
      pins=[(*BOSTON, "BOSTON", 0.2), (*MONTREAL, "MONTREAL", 1.6, "1907")]),
    still(136.0, "m01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14)), x=0.4),
    still(141.5, "m01", ((0.6, 0.45, 1.25), (0.62, 0.45, 1.4))),
    still(147.3, "m02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12))),
    g(156.6, "plate", bg=A("m02"), x=0.4),
    still(165.4, "m03", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14))),
    still(168.6, "m04", ((0.5, 0.5, 1.1), (0.45, 0.5, 1.1))),
    still(174.7, "m05", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.2)), x=0.4),
    still(181.8, "m06", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.16))),
    still(187.2, "m07", ((0.4, 0.5, 1.1), (0.6, 0.5, 1.1)), x=0.4),
    g(196.0, "map", x=0.4, v0=(-80.0, 38.0, 24.0), borders=STATES, pins=[(*ATLANTA, "ATLANTA", 0.4, "FEDERAL PRISON")]),
    still(199.9, "m08", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.4),
    still(206.2, "m08", ((0.72, 0.62, 1.4), (0.72, 0.62, 1.6))),
    still(212.9, "m06", ((0.5, 0.5, 1.2), (0.5, 0.5, 1.0))),
    arch(215.0, "ponzi_1920.jpg", cam=((0.5, 0.3, 1.0), (0.5, 0.25, 1.25)), credit=PORTRAIT),
    # ---- 3 the coupon
    card("coupon", 2, "The Coupon", "c01"),
    still(225.26, "o06", ((0.5, 0.5, 1.0), (0.45, 0.5, 1.12)), x=0.5),
    still(232.5, "c01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12))),
    still(236.9, "c01", ((0.62, 0.62, 1.4), (0.64, 0.62, 1.65))),
    g(239.4, "record", head="INTERNATIONAL REPLY COUPON",
      fields=[("WHAT IT IS", "A pre-paid reply, for a letter abroad", 0.5),
              ("WHERE YOU BUY IT", "A post office, in one country", w("buy", 240) - 239.4),
              ("WHAT IT'S WORTH", "Stamps, in another", w("swap", 245) - 239.4),
              ("ITS PRICE", "Fixed by treaty, before the war", w("fixed", 250) - 239.4)],
      note="HOW THE COUPON WORKED"),
    g(258.2, "map", x=0.4, v0=(-30.0, 42.0, 110.0), routes=[(MADRID, BOSTON, 4.8, 7.4), (ROME, BOSTON, 5.4, 8.0)],
      pins=[(*MADRID, "SPAIN", 4.6), (*ROME, "ITALY", 5.2), (*BOSTON, "BOSTON", 7.4)]),
    still(272.6, "c02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14)), x=0.4),
    still(278.0, "c03", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14))),
    g(281.4, "plate", bg=A("c03")),
    still(285.0, "c04", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    still(292.0, "c04", ((0.5, 0.6, 1.3), (0.5, 0.45, 1.5))),
    still(301.8, "c03", ((0.3, 0.5, 1.3), (0.3, 0.5, 1.42))),
    # ---- 4 fifty percent in forty-five days
    card("promise", 3, "Fifty Percent in Forty-Five Days", "p01"),
    clip(307.78, "p01", x=0.5),
    still(312.8, "p01", ((0.5, 0.5, 1.05), (0.6, 0.5, 1.2))),
    g(315.8, "record", head="SECURITIES EXCHANGE COMPANY",
      fields=[("YOU HAND OVER", "$1,000", 0.5), ("IN 45 DAYS", "$1,500", w("45", 316) - 315.8),
              ("IN 90 DAYS", "$2,000", w("90", 322) - 315.8)],
      note="AN ILLUSTRATION OF THE PROMISE"),
    still(326.1, "p02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    still(333.6, "o05", ((0.4, 0.5, 1.15), (0.55, 0.5, 1.15))),
    still(342.3, "p01", ((0.3, 0.55, 1.35), (0.35, 0.55, 1.5))),
    g(345.2, "plate", bg=A("p01"), x=0.4),
    still(361.0, "p02", ((0.5, 0.5, 1.15), (0.6, 0.5, 1.3))),
    still(367.8, "p03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    still(372.9, "p04", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.12))),
    still(376.2, "p04", ((0.4, 0.6, 1.3), (0.42, 0.6, 1.45))),
    # ---- 5 the king of School Street
    card("king", 4, "The King of School Street", "k01"),
    arch(385.37, "ponzi_1920_loc.jpg", mode="print", rot=-1.5, x=0.5, credit=LOC),
    still(391.6, "k01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12))),
    still(w("limousine", 392) - 0.4, "k02", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.12))),
    still(w("canes", 393) - 0.4, "k03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.2))),
    still(401.6, "k04", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.4),
    still(405.2, "k05", ((0.5, 0.5, 1.0), (0.5, 0.45, 1.14))),
    still(418.0, "p03", ((0.5, 0.5, 1.25), (0.5, 0.5, 1.05))),
    still(423.1, "p04", ((0.6, 0.5, 1.1), (0.4, 0.5, 1.1))),
    # ---- 6 the question
    card("post", 5, "The Question", "n01"),
    clip(431.7, "n01", x=0.5),
    g(436.7, "plate", bg=A("n01")),
    still(441.2, "o01", ((0.4, 0.5, 1.2), (0.6, 0.5, 1.2))),
    still(443.2, "n02", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.4),
    still(452.9, "n03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12))),
    g(460.0, "plate", bg=A("n03"), x=0.4),
    still(471.1, "c03", ((0.5, 0.5, 1.1), (0.55, 0.45, 1.25))),
    # ---- 7 the run
    card("run", 6, "The Run", "r01"),
    clip(482.66, "r01", x=0.5),
    still(487.7, "r01", ((0.5, 0.5, 1.08), (0.6, 0.5, 1.25))),
    still(493.0, "r02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12))),
    g(497.4, "plate", bg=A("r02")),
    clip(502.1, "o04", x=0.4),
    still(507.1, "o04", ((0.3, 0.5, 1.3), (0.35, 0.5, 1.45))),
    still(510.8, "r03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    still(516.9, "r03", ((0.45, 0.4, 1.3), (0.45, 0.4, 1.45))),
    still(520.2, "n03", ((0.5, 0.5, 1.3), (0.5, 0.5, 1.1))),
    # ---- 8 hopelessly insolvent
    card("fall", 7, "Hopelessly Insolvent", "f01"),
    still(527.48, "f01", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.5),
    still(536.1, "n02", ((0.6, 0.5, 1.25), (0.62, 0.5, 1.4))),
    g(540.0, "plate", bg=A("n01")),
    still(550.5, "f02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    still(553.3, "m03", ((0.5, 0.5, 1.2), (0.5, 0.5, 1.05))),
    still(w("forged", 555) - 0.3, "m05", ((0.6, 0.55, 1.3), (0.6, 0.55, 1.45))),
    arch(564.6, "ponzi_5247.jpg", mode="print", fit=0.62, rot=1.2, credit=POLICE),
    still(569.0, "f03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    still(574.1, "f04", ((0.5, 0.5, 1.0), (0.5, 0.45, 1.14))),
    g(578.7, "plate", bg=A("n01"), x=0.4),
    # ---- 9 the bill
    card("bill", 8, "The Bill", "b01"),
    still(585.27, "b01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.5),
    g(588.9, "plate", bg=A("b01")),
    still(595.6, "f03", ((0.5, 0.5, 1.2), (0.5, 0.5, 1.0))),
    g(600.2, "plate", bg=A("b01"), x=0.4),
    still(605.4, "b02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14))),
    g(612.2, "timeline", x=0.4, span=(1919, 1935),
      marks=[(1920, "FEDERAL · 5 YEARS", 0.3), (1922, "SUPREME COURT", w("Supreme", 616) - 612.2),
             (1925, "STATE · 7–9 YEARS", w("Seven", 621) - 612.2)]),
    # ---- 10 he tried again
    card("again", 9, "He Tried Again", "g01"),
    still(627.39, "g01", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.5),
    g(632.5, "map", x=0.4, v0=(-83.0, 30.5, 18.0), borders=STATES, pins=[(*JACKSONVILLE, "FLORIDA", 0.4, "1925")]),
    still(639.5, "g02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14))),
    g(642.7, "plate", bg=A("g02")),
    still(648.0, "g03", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.12)), x=0.4),
    g(655.8, "map", x=0.4, v0=(-88.0, 30.5, 22.0), borders=STATES, pins=[(*NEW_ORLEANS, "NEW ORLEANS", 0.6, "ARRESTED")]),
    still(663.5, "g04", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    still(671.5, "g04", ((0.65, 0.5, 1.3), (0.62, 0.5, 1.45))),
    still(676.4, "g04", ((0.3, 0.6, 1.35), (0.3, 0.6, 1.5))),
    # ---- 11 cheap at the price
    card("end", 10, "Cheap at the Price", "e02"),
    still(683.9, "e01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.5),
    still(688.8, "e01", ((0.62, 0.55, 1.3), (0.62, 0.55, 1.45))),
    still(696.1, "e02", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.16)), x=0.4),
    still(704.2, "e02", ((0.7, 0.55, 1.35), (0.72, 0.55, 1.55))),
    still(708.0, "e03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14))),
    arch(713.2, "ponzi_1920.jpg", mode="print", rot=1.0, credit=PORTRAIT),
    g(717.5, "plate", bg=A("o06"), x=0.4),
    g(727.8, "plate", bg=A("o05"), x=0.4),
    g(746.3, "plate", bg=A("e05"), x=0.4),
    still(765.2, "e04", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    g(768.2, "phone", x=0.4, bg=A("e04"), msgs=[
        (0.3, "Crypto Club", "Guaranteed 2% a day.\nWithdraw any time."),
        (w("trading", 765) - 768.2, "AI Trading Bot", "Our bot made 41% last month.\nSpots close tonight."),
        (w("foreign", 765) - 768.2, "FX Signals VIP", "Double your money in 90 days.\nAsk me how.")]),
    still(773.7, "e05", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    g(783.6, "plate", bg=A("o06")),
    g(CH["end_voice"] + 0.4, "endcard", x=0.8, bg=A("o06"), line="MONEY CRIMES", sub="TRUE STORIES OF THE PERFECT CON"),
]

L = lambda t0, t1, s, sub=None, **k: dict(kind="label", t0=t0, t1=t1, text=s, sub=sub, **k)
N = lambda t0, t1, title, sub, **k: dict(kind="name", t0=t0, t1=t1, title=title, sub=sub, **k)
STAMP = lambda t0, t1, s, **k: dict(kind="stamp", t0=t0, t1=t1, text=s, **k)
COUNT = lambda t0, t1, v, **k: dict(kind="counter", t0=t0, t1=t1, value=v, **k)
Q = lambda t0, t1, s, sub=None, **k: dict(kind="quote", t0=t0, t1=t1, text=s, sub=sub, **k)

OVERLAYS = [
    L(1.0, 6.0, "BOSTON · JULY 1920"),
    Q(28.0, 30.4, "“Where is the money\ncoming from?”", size=84, y=470),
    N(47.4, 51.6, "CHARLES PONZI", "1882 – 1949", x=1440, y=900, size=58),
    # chapter 1
    L(89.2, 93.8, "BOSTON · NOVEMBER 1903"),
    COUNT(96.9, 99.8, 2.50, pre="$", fmt="{:,.2f}", sub="ALL HE HAD", size=190),
    Q(100.3, 108.9, "“I landed in this country with $2.50 in cash\nand $1 million in hopes, and those\nhopes never left me.”",
      sub="CHARLES PONZI", size=64, y=400),
    # chapter 2
    L(136.2, 141.3, "MONTREAL · 1907", "LUIGI ZAROSSI'S BANK"),
    COUNT(w("6%", 141) - 0.1, 147.1, 6, post="%", sub="INTEREST · TWICE THE GOING RATE", size=200),
    dict(kind="lines", t0=156.8, t1=165.2, x=960, y=380, gap=120, size=64, font="serif", align="center",
         items=[(156.8, "New customers' deposits"), (w("paid", 157) - 0.2, "paid the old customers' interest"),
                (w("Robbing", 160) - 0.1, "Robbing Peter to pay Paul.")], hi=2),
    COUNT(w("$423.58", 175) - 0.1, 181.6, 423.58, pre="$", fmt="{:,.2f}", sub="A FORGED CHEQUE", size=180),
    L(182.0, 187.0, "QUEBEC", "PENITENTIARY"),
    N(200.1, 206.0, "CHARLES W. MORSE", "WALL STREET SPECULATOR"),
    # chapter 3
    L(225.5, 232.3, "BOSTON · 1919"),
    COUNT(w("400%", 281) - 0.1, 284.8, 400, post="%", sub="THE PROFIT HE CLAIMED", size=210),
    STAMP(w("spend", 286) - 0.2, 289.0, "YOU CAN'T SPEND STAMPS", x=960, y=640, rot=-6, size=110),
    # chapter 4
    COUNT(w("18", 326) - 0.1, 329.7, 18, sub="INVESTORS, THE FIRST MONTH", size=210),
    COUNT(w("$1,800", 330) - 0.1, 333.4, 1800, pre="$", sub="BETWEEN THEM", size=200),
    STAMP(w("paid", 337) - 0.1, 342.1, "PAID IN FULL", x=1300, y=640, rot=-8, size=130),
    dict(kind="lines", t0=345.4, t1=360.8, x=960, y=330, gap=110, size=58, font="serif", align="center",
         items=[(345.4, "The next investors' money"), (w("knew", 351) - 0.2, "pays the first investors,"),
                (w("told", 353) - 0.2, "who tell their friends,"), (w("whole", 358) - 0.2, "who become the next investors.")],
         hi=3),
    COUNT(w("$420,000", 368) - 0.1, 372.7, 420000, pre="$", sub="TAKEN IN BY MAY 1920", size=170),
    COUNT(w("million", 373) - 1.0, 376.0, 2500000, pre="$", sub="BY JUNE", size=170),
    COUNT(w("quarter", 377) - 0.3, 382.0, 250000, pre="$", sub="A DAY, BY JULY · BY SOME ACCOUNTS", size=170),
    # chapter 5
    N(385.6, 391.4, "CHARLES PONZI", "FIVE FOOT TWO", x=1440, y=900, size=58),
    L(391.8, 395.0, "LEXINGTON, MASSACHUSETTS"),
    L(405.4, 417.8, "HANOVER TRUST COMPANY", "BOSTON"),
    # chapter 6
    Q(437.0, 441.0, "“DOUBLES THE MONEY\nWITHIN THREE MONTHS”", sub="THE BOSTON POST · 24 JULY 1920", size=80, y=420),
    N(443.5, 448.4, "RICHARD GROZIER", "ACTING PUBLISHER, THE BOSTON POST"),
    N(453.1, 459.8, "CLARENCE BARRON", "FINANCIAL JOURNALIST"),
    COUNT(w("160", 460) - 0.1, 468.2, 160000000, sub="COUPONS NEEDED", size=170, y=470),
    COUNT(w("27,000", 468) - 0.1, 471.0, 27000, sub="COUPONS IN CIRCULATION", size=170, y=470, color=0xFFC8321F),
    # chapter 7
    L(482.9, 487.5, "SCHOOL STREET · 26 JULY 1920"),
    COUNT(w("two", 497) - 0.2, 502.0, 2000000, pre="$", sub="PAID OUT IN THREE DAYS", size=170),
    # chapter 8
    N(530.1, 535.9, "WILLIAM McMASTERS", "PONZI'S PUBLICITY AGENT"),
    L(540.2, 545.0, "THE BOSTON POST · 2 AUGUST 1920"),
    STAMP(w("hopelessly", 545) - 0.1, 550.3, "HOPELESSLY INSOLVENT", x=960, y=560, rot=-6, size=120),
    L(553.5, 558.0, "11 AUGUST 1920"),
    L(569.2, 573.9, "HANOVER TRUST", "SEIZED"),
    L(578.9, 585.0, "PULITZER PRIZE · 1921", "THE BOSTON POST"),
    # chapter 9
    dict(kind="lines", t0=589.1, t1=595.4, x=960, y=420, gap=130, size=78, font="serif", align="center",
         items=[(589.1, "Tens of thousands of investors"), (w("between", 590) - 0.2, "$10–15 million · in 1920 money")],
         hi=1),
    COUNT(w("five", 596) - 0.2, 600.0, 6, sub="BANKS FAILED", size=210),
    COUNT(600.4, 605.2, 30, pre="UNDER ", post="¢", sub="BACK ON EACH DOLLAR · YEARS LATER", size=190, count=1.0),
    # chapter 10
    COUNT(w("Two", 644) - 0.1, 647.8, 200, post="%", sub="IN 60 DAYS · THE NEW PROMISE", size=210),
    L(663.7, 671.3, "1934 · DEPORTED TO ITALY"),
    # chapter 11
    L(684.1, 688.6, "RIO DE JANEIRO"),
    L(696.3, 703.9, "18 JANUARY 1949"),
    COUNT(w("$75", 708) - 0.1, 713.0, 75, pre="$", sub="HIS ESTATE", size=210),
    Q(717.7, 723.7, "“Even if they never got anything for it,\nit was cheap at that price.”", sub="CHARLES PONZI", size=68,
      y=440),
    Q(723.9, 727.6, "“It was easily worth fifteen million bucks\nto watch me put the thing over.”", sub="CHARLES PONZI",
      size=68, y=440),
    dict(kind="lines", t0=728.0, t1=746.1, x=330, y=300, gap=110, size=60, font="serif", tick=True,
         items=[(w("return", 730) - 0.2, "A return too good to refuse."),
                (w("story", 733) - 0.2, "A story too complicated to check."),
                (w("first", 736) - 0.2, "The first investors paid: now they're salesmen."),
                (w("money", 741) - 0.2, "Money that only flows while new money arrives.")]),
    N(746.5, 756.3, "BERNIE MADOFF", "CONFESSED, DECEMBER 2008", x=1420, y=900),
    COUNT(w("$65", 756) - 0.1, 762.4, 65, pre="$", post=" BILLION", sub="ON PAPER", size=170),
    Q(785.8, CH["end_voice"] + 0.3, "Where is the money coming from?", size=80, y=520),
]


def _ai_tags():
    """The reconstruction tag, small, on every AI shot (with a moment's grace after a dissolve)."""
    out = []
    for i, s in enumerate(SHOTS):
        if s.get("ai"):
            t1 = SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else END
            out.append(dict(kind="ai", t0=s["t"] + 0.2, t1=t1, fd=0.2))
        if s["kind"] == "arch" and s.get("credit"):
            t1 = SHOTS[i + 1]["t"] if i + 1 < len(SHOTS) else END
            out.append(dict(kind="credit", t0=s["t"] + 0.3, t1=t1, text=s["credit"], fd=0.25))
    return out


OVERLAYS += _ai_tags()

SFX = [(0.0, "swell", -8), (57.1, "sub_drop", -6)]
for c in CH["chapters"][1:]:
    SFX.append((c["card"], "whoosh", -12))
for o in OVERLAYS:                                   # a thud for every stamp, a rattle of coins for every counter
    if o["kind"] == "stamp":
        SFX.append((o["t0"], "thock", -4))
    elif o["kind"] == "counter":
        SFX.append((o["t0"] + 0.1, "tick_run", -14))
        SFX.append((o["t0"] + o.get("count", 1.4), "coin", -12))
for sh in SHOTS:                                     # paper for documents and archive prints, air for maps
    if sh["kind"] == "arch" or (sh["kind"] == "gfx" and sh["fn"] in ("timeline", "record")):
        SFX.append((sh["t"] + 0.05, "paper", -14))
    elif sh["kind"] == "gfx" and sh["fn"] == "map":
        SFX.append((sh["t"] + 0.05, "whoosh", -16))

MUSIC = []                      # music.py fills build/music.json
_mj = os.path.join(BUILD, "music.json")
if os.path.exists(_mj):
    MUSIC = [tuple(x) for x in json.load(open(_mj))]

SEGMENTS = [c["card"] for c in CH["chapters"][1:]]
