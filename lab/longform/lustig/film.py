"""MONEY CRIMES · long-form 01: "The Man Who Sold the Eiffel Tower" (Victor Lustig). 16:9, about 15 minutes.

The picture to the narration's timings (build/words.json from vo.py): GPT Image 2.5 stills and Kling 3.0 clips (src/ai,
see ai_assets.py; labelled AI RECONSTRUCTION on screen), public-domain photographs from Wikimedia Commons (src/arch,
credited on screen and in arch/credits.json), and drawn graphics (maps from Natural Earth, documents, counters).

    python3 ../doc.py lustig frames 12 50 300    # QC stills
    python3 ../doc.py lustig render              # the film -> out/
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "lustig"
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
    return g(CARDS[cid], "card", x=0.5, kicker=f"CHAPTER {NUM[k]}", title=title, bg=A(bg) if bg[0] != "/" else bg)


CERT_W, CERT_H = 1532, 1358
CERT_NAME, CERT_JOB = (0.27, 0.30, 2.1), (0.36, 0.63, 2.1)


def cert_box(cam, x0, y0, x1, y1):
    """A rectangle on the certificate (picture pixels) to screen pixels under a still camera (as doc.draw_cover)."""
    cx, cy, z = cam
    sc = max(1920 / CERT_W, 1080 / CERT_H) * z
    ww, wh = 1920 / sc, 1080 / sc
    px = min(max(cx * CERT_W, ww / 2), CERT_W - ww / 2) - ww / 2
    py = min(max(cy * CERT_H, wh / 2), CERT_H - wh / 2) - wh / 2
    return ((x0 - px) * sc, (y0 - py) * sc, (x1 - x0) * sc, (y1 - y0) * sc)


PARIS, VIENNA, HOSTINNE, DRESDEN = (2.35, 48.86), (16.37, 48.21), (15.72, 50.54), (13.74, 51.05)
EUROPE = [(14.42, 50.08, "PRAGUE"), (16.37, 48.21, "VIENNA"), (13.74, 51.05, "DRESDEN"), (13.40, 52.52, "BERLIN"),
          (11.58, 48.14, "MUNICH"), (19.04, 47.50, "BUDAPEST"), (4.35, 50.85, "BRUSSELS"), (8.68, 50.11, "FRANKFURT")]
LEHAVRE, NYC, SPRINGFIELD, CHICAGO = (0.11, 49.49), (-74.0, 40.71), (-93.29, 37.21), (-87.63, 41.88)

SHOTS = [
    # ---- cold open
    clip(0.0, "o01"),
    still(3.9, "o02", ((0.32, 0.55, 1.05), (0.28, 0.58, 1.3)), x=0.4),
    g(9.9, "letter", stamp_t=0.45),
    arch(12.2, "crillon_1915.jpg", cam=((0.5, 0.55, 1.0), (0.5, 0.5, 1.12)), credit="HÔTEL DE CRILLON, c. 1915 · LIBRARY OF CONGRESS"),
    clip(19.7, "o03", x=0.5),
    still(25.6, "o04", ((0.55, 0.5, 1.0), (0.58, 0.52, 1.18))),
    still(30.9, "o05", ((0.4, 0.5, 1.1), (0.6, 0.5, 1.1))),
    still(33.2, "o06", ((0.5, 0.62, 1.0), (0.5, 0.45, 1.16)), x=0.4),
    g(38.5, "letter"),
    still(40.6, "o07", ((0.6, 0.5, 1.15), (0.45, 0.5, 1.0))),
    arch(46.7, "lustig_1935.jpg", mode="print", rot=-2.0, credit="VICTOR LUSTIG, 1935 · PUBLIC DOMAIN"),
    still(49.6, "t05", ((0.5, 0.5, 1.0), (0.45, 0.45, 1.12))),
    still(w("sell", 50), "t06", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.25))),
    arch(w("con", 52), "capone_1929.jpg", mode="print", rot=1.5, credit="AL CAPONE, 1929 · PUBLIC DOMAIN"),
    still(w("flood", 56), "m01", ((0.45, 0.5, 1.1), (0.55, 0.5, 1.1))),
    still(w("climb", 59), "e02", ((0.5, 0.35, 1.15), (0.5, 0.6, 1.15))),
    g(63.7, "title", x=0.6, bg=A("o08"), kicker="MONEY CRIMES", lines=["THE MAN WHO SOLD", "THE EIFFEL TOWER"],
      sub="THE TRUE STORY OF VICTOR LUSTIG"),
    # ---- 1 a boy from Bohemia
    card("boy", 0, "A Boy from Bohemia", "b01"),
    g(72.85, "map", x=0.5, v0=(10.0, 49.0, 38.0), v1=(15.2, 50.2, 15.0), move=6.0, towns=EUROPE[:6],
      pins=[(*HOSTINNE, "HOSTINNÉ", 3.0, "BOHEMIA · 4 JANUARY 1890")]),
    still(83.2, "b01", ((0.5, 0.5, 1.0), (0.55, 0.45, 1.12)), x=0.5),
    still(86.7, "b02", ((0.5, 0.5, 1.12), (0.5, 0.5, 1.0))),
    still(90.3, "b03", ((0.6, 0.5, 1.0), (0.62, 0.45, 1.15))),
    still(94.6, "b04", ((0.5, 0.6, 1.1), (0.5, 0.45, 1.0))),
    still(99.8, "b05", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.12))),
    arch(108.7, "sorbonne.jpg", grade=None, cam=((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)),
         credit="LA SORBONNE, c. 1900 · P.-J.-V. DARGAUD · PUBLIC DOMAIN"),
    clip(114.6, "b06", x=0.4),
    still(119.7, "b07", ((0.45, 0.45, 1.05), (0.4, 0.42, 1.2))),
    still(125.4, "b08", ((0.5, 0.45, 1.0), (0.5, 0.42, 1.15))),
    still(129.7, "b09", ((0.5, 0.5, 1.1), (0.5, 0.5, 1.0))),
    still(133.4, "o04", ((0.62, 0.48, 1.35), (0.64, 0.5, 1.6))),
    clip(136.7, "b11", x=0.4),
    still(141.5, "b10", ((0.5, 0.5, 1.0), (0.55, 0.48, 1.14))),
    still(148.9, "b11", ((0.5, 0.5, 1.3), (0.5, 0.5, 1.0))),
    still(151.8, "r05", ((0.4, 0.5, 1.12), (0.6, 0.5, 1.12)), x=0.4),
    still(155.7, "b12", ((0.5, 0.5, 1.0), (0.5, 0.52, 1.15))),
    # ---- 2 the money box
    card("box", 1, "The Money Box", "x01"),
    still(162.61, "x01", ((0.5, 0.55, 1.0), (0.5, 0.5, 1.14)), x=0.5),
    clip(170.7, "x02"),
    g(173.2, "boxdiagram", x=0.4, t_clock=4.0, t_out=8.0),
    g(183.9, "boxdiagram", reveal=True, head="HOW IT REALLY WORKED"),
    still(191.7, "x03", ((0.5, 0.5, 1.0), (0.52, 0.45, 1.14)), x=0.4),
    still(197.1, "x04", ((0.45, 0.5, 1.1), (0.55, 0.5, 1.1))),
    still(200.8, "x01", ((0.5, 0.3, 1.35), (0.5, 0.32, 1.55))),
    still(207.0, "x05", ((0.5, 0.5, 1.0), (0.5, 0.55, 1.14))),
    still(210.8, "x06", ((0.5, 0.5, 1.12), (0.5, 0.5, 1.0))),
    g(216.3, "plate", bg=A("x06")),
    still(221.8, "x07", ((0.4, 0.5, 1.1), (0.55, 0.5, 1.1)), x=0.4),
    still(228.6, "x08", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.15))),
    still(237.0, "x09", ((0.5, 0.5, 1.0), (0.5, 0.45, 1.12)), x=0.4),
    g(241.6, "map", x=0.5, v0=(-96.0, 38.5, 44.0), v1=(-93.0, 37.4, 14.0), move=3.0,
      pins=[(*SPRINGFIELD, "SPRINGFIELD, MISSOURI", 1.2, "MAY 1922 · 'ROBERT DUVAL' · $10,000")],
      borders="ne_50m_admin_1_states_provinces_lakes", caption="REMEMBER THIS TOWN"),
    # ---- 3 the tower nobody wanted
    card("tower", 2, "The Tower Nobody Wanted", "o06"),
    clip(252.34, "t01", x=0.5),
    still(257.5, "t02", ((0.5, 0.45, 1.0), (0.5, 0.35, 1.25))),
    arch(262.3, "eiffel_1889.jpg", mode="print", rot=-1.5, credit="THE TOWER AT NIGHT, 1889 · PUBLIC DOMAIN"),
    arch(265.5, "expo_1889.jpg", cam=((0.5, 0.5, 1.12), (0.5, 0.5, 1.0)), credit="EXPOSITION UNIVERSELLE, 1889 · PUBLIC DOMAIN", x=0.4),
    g(271.9, "timeline", span=(1885, 1930), marks=[(1889, "BUILT", 0.2), (1909, "PERMIT\nRUNS OUT", 1.4)]),
    g(276.0, "plate", bg=A("t06"), grade="bw"),
    still(279.1, "o06", ((0.5, 0.25, 1.6), (0.5, 0.2, 1.85))),
    still(284.0, "t03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.2))),
    still(286.0, "t04", ((0.45, 0.5, 1.1), (0.55, 0.45, 1.1))),
    still(290.0, "t02", ((0.35, 0.6, 1.3), (0.6, 0.6, 1.3))),
    clip(294.2, "t05", x=0.4),
    still(302.7, "t06", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.2))),
    # ---- 4 the sale
    card("sale", 3, "The Sale", "s03"),
    still(311.7, "s01", ((0.5, 0.5, 1.0), (0.5, 0.55, 1.14)), x=0.5),
    g(315.2, "letter", english="DEPUTY DIRECTOR-GENERAL · MINISTRY OF POSTS AND TELEGRAPHS", en_t=3.6),
    still(325.1, "s02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.15))),
    clip(331.6, "s03", x=0.4),
    still(336.0, "s04", ((0.4, 0.5, 1.1), (0.6, 0.5, 1.1))),
    still(339.6, "s05", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14))),
    g(347.9, "plate", bg=A("o05"), x=0.4),
    clip(364.7, "s06", x=0.4),
    still(368.6, "s07", ((0.35, 0.5, 1.15), (0.6, 0.5, 1.2))),
    still(376.6, "s08", ((0.5, 0.5, 1.0), (0.5, 0.45, 1.14)), x=0.4),
    still(383.7, "s09", ((0.6, 0.5, 1.1), (0.4, 0.5, 1.1))),
    still(391.4, "s10", ((0.5, 0.5, 1.0), (0.45, 0.45, 1.16))),
    still(401.7, "o07", ((0.5, 0.5, 1.0), (0.6, 0.5, 1.2)), x=0.4),
    clip(405.8, "s11", x=0.4),
    still(412.0, "s11", ((0.35, 0.45, 1.3), (0.35, 0.45, 1.45))),
    still(419.8, "s12", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.15))),
    still(421.9, "s13", ((0.5, 0.5, 1.12), (0.5, 0.5, 1.0)), x=0.4),
    still(431.4, "s08", ((0.5, 0.4, 1.3), (0.5, 0.4, 1.45))),
    still(435.9, "s12", ((0.5, 0.5, 1.15), (0.5, 0.5, 1.35))),
    clip(w("Austria", 441) - 1.6, "s14", x=0.4),
    # ---- 5 he came back
    card("back", 4, "He Came Back", "s14"),
    g(450.4, "map", x=0.5, v0=(9.0, 48.8, 24.0), routes=[(PARIS, VIENNA, 0.4, 2.2)], towns=[EUROPE[i] for i in (0, 3, 4, 6, 7)],
      pins=[(*PARIS, "PARIS", 0.1), (*VIENNA, "VIENNA", 2.0)]),
    still(454.0, "r01", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.4),
    still(459.3, "r02", ((0.5, 0.5, 1.12), (0.5, 0.5, 1.0))),
    g(467.7, "map", x=0.4, v0=(9.0, 48.8, 24.0), routes=[(VIENNA, PARIS, 0.3, 2.0)], towns=[EUROPE[i] for i in (0, 3, 4, 6, 7)],
      pins=[(*VIENNA, "VIENNA", 0.0), (*PARIS, "PARIS", 1.8, "A MONTH LATER")]),
    still(471.6, "s02", ((0.5, 0.5, 1.2), (0.5, 0.5, 1.0)), x=0.4),
    still(479.1, "r03", ((0.5, 0.5, 1.0), (0.5, 0.45, 1.14))),
    clip(484.4, "r04", x=0.3),
    g(489.0, "map", x=0.4, v0=(-36.0, 44.0, 95.0), routes=[(LEHAVRE, NYC, 0.3, 3.0)],
      pins=[(*PARIS, "FRANCE", 0.0), (*NYC, "NEW YORK", 2.8, None, "left")]),
    # ---- 6 the man who conned Capone
    card("capone", 5, "The Man Who Conned Capone", "c01"),
    arch(496.99, "capone_1929.jpg", mode="print", rot=-1.5, x=0.5, credit="AL CAPONE, 1929 · PUBLIC DOMAIN"),
    still(503.6, "c01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14))),
    still(510.0, "c01", ((0.72, 0.5, 1.35), (0.72, 0.5, 1.5))),
    clip(515.1, "c02", x=0.4),
    still(519.6, "c03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.1))),
    still(523.9, "c03", ((0.6, 0.45, 1.3), (0.6, 0.45, 1.45))),
    still(531.1, "c04", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.15))),
    still(536.0, "c04", ((0.45, 0.6, 1.3), (0.5, 0.6, 1.45))),
    clip(542.3, "c05", x=0.4),
    still(550.5, "o04", ((0.5, 0.5, 1.0), (0.52, 0.5, 1.15))),
    arch(555.0, "capone_1929.jpg", mode="print", rot=2.0, credit="AL CAPONE, 1929 · PUBLIC DOMAIN"),
    # ---- 7 Lustig money
    card("money", 6, "Lustig Money", "m01"),
    still(565.0, "m01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14)), x=0.5),
    clip(570.5, "m02"),
    g(576.5, "map", x=0.4, v0=(-97.0, 39.0, 40.0), borders="ne_50m_admin_1_states_provinces_lakes",
      pins=[(-99.8, 41.5, "NEBRASKA", 0.5)]),
    still(584.6, "m03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.2)), x=0.4),
    g(589.8, "map", x=0.4, v0=(-90.0, 38.5, 40.0), borders="ne_50m_admin_1_states_provinces_lakes",
      routes=[(NYC, CHICAGO, 0.2, 1.4), (NYC, (-90.2, 38.6), 0.6, 1.9), (NYC, (-80.0, 40.44), 0.4, 1.0),
              (NYC, (-71.06, 42.36), 0.8, 1.4), (NYC, (-90.07, 29.95), 1.0, 2.6), (NYC, (-84.39, 33.75), 1.3, 2.6),
              (NYC, (-94.58, 39.1), 1.5, 3.0), (NYC, (-77.04, 38.9), 0.5, 1.2)],
      pins=[(*NYC, "NEW YORK", 0.0)]),
    (arch(596.0, "breadline.jpg", mode="print", rot=1.2, fit=0.88, credit="NEW YORK BREADLINE, 1932 · NATIONAL ARCHIVES", x=0.4)
     if os.path.exists(R("breadline.jpg")) else still(596.0, "m05", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.12)), x=0.4)),
    arch(601.5, "lustig_note.jpg", mode="print", fit=0.5, rot=-3.0, credit="A 'LUSTIG' $10 NOTE · U.S. GOVERNMENT, PUBLIC DOMAIN"),
    still(610.3, "m04", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12))),
    arch(613.7, "wanted_1935.jpg", mode="print", rot=1.2, credit="WANTED NOTICE, 1935 · PUBLIC DOMAIN"),
    still(618.75, "l01", ((0.3, 0.5, 1.3), (0.3, 0.5, 1.35))),
    # ---- 8 the locker
    card("locker", 7, "The Locker", "l04"),
    still(623.09, "l01", ((0.4, 0.5, 1.1), (0.55, 0.5, 1.1)), x=0.5),
    clip(629.6, "l02"),
    (arch(638.0, "lustig_mugshot.jpg", cam=((0.5, 0.5, 1.0), (0.5, 0.45, 1.1)), credit="VICTOR LUSTIG · U.S. GOVERNMENT, PUBLIC DOMAIN")
     if os.path.exists(R("lustig_mugshot.jpg")) else
     arch(638.0, "lustig_boi_1931.jpg", mode="print", rot=1.5, credit="VICTOR LUSTIG, 1931 · U.S. DEPARTMENT OF JUSTICE, PUBLIC DOMAIN")),
    still(645.4, "l03", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.2))),
    still(648.7, "l04", ((0.4, 0.5, 1.1), (0.6, 0.5, 1.1))),
    clip(652.3, "l05"),
    still(659.4, "l06", ((0.5, 0.6, 1.0), (0.5, 0.45, 1.14)), x=0.4),
    still(670.0, "l07", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.15))),
    # ---- 9 the escape
    card("escape", 8, "The Escape", "e02"),
    still(682.48, "e01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14)), x=0.5),
    clip(688.0, "e02"),
    still(695.2, "e03", ((0.5, 0.7, 1.15), (0.5, 0.4, 1.15))),
    g(704.6, "plate", bg=A("e03")),
    g(708.4, "map", v0=(-77.5, 40.6, 12.0), borders="ne_50m_admin_1_states_provinces_lakes",
      routes=[(NYC, (-80.0, 40.44), 0.1, 1.2)], pins=[(*NYC, "NEW YORK", 0.0), (-80.0, 40.44, "PITTSBURGH", 1.1, "27 DAYS LATER", "left")]),
    still(711.2, "e04", ((0.5, 0.5, 1.0), (0.5, 0.45, 1.14))),
    g(717.9, "plate", bg=A("e04")),
    arch(727.1, "alcatraz_1930s.jpg", cam=((0.4, 0.5, 1.1), (0.6, 0.5, 1.1)), credit="ALCATRAZ, 1930s · U.S. NAVY, PUBLIC DOMAIN", x=0.5),
    # ---- 10 the Rock
    card("rock", 9, "The Rock", "k01"),
    still(737.82, "k01", ((0.5, 0.5, 1.0), (0.55, 0.5, 1.14)), x=0.5),
    g(745.6, "timeline", span=(1930, 1950), marks=[(1935, "SENTENCED", 0.2), (1947, "DIES", 1.0)]),
    still(749.4, "k02", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14)), x=0.4),
    arch(756.5, "lustig_boi_1931.jpg", mode="print", rot=-1.0, credit="VICTOR LUSTIG · U.S. GOVERNMENT, PUBLIC DOMAIN"),
    g(761.6, "map", x=0.4, v0=(-95.0, 38.0, 36.0), v1=(-93.3, 37.4, 12.0), move=2.5, borders="ne_50m_admin_1_states_provinces_lakes",
      pins=[(*SPRINGFIELD, "SPRINGFIELD, MISSOURI", 0.6)]),
    *([arch(775.6, "death_cert.png", mode="print", fit=0.94, rot=-0.6, credit="DEATH CERTIFICATE, 1947 · PUBLIC DOMAIN"),
       arch(781.9, "death_cert.png", cam=(CERT_NAME, CERT_NAME), quiet=True),
       arch(w("occupation", 785) - 0.25, "death_cert.png", cam=(CERT_JOB, CERT_JOB), quiet=True)]
      if os.path.exists(R("death_cert.png")) else
      [g(775.6, "record", head="CERTIFICATE OF DEATH · MISSOURI · 1947",
         fields=[("NAME OF DECEASED", "Robert V. Miller", 0.4), ("DATE OF DEATH", "March 11, 1947", 1.2),
                 ("PLACE OF DEATH", "Federal prison hospital, Springfield", 1.9),
                 ("USUAL OCCUPATION", "Apprentice salesman & counterfeiter", 2.6)],
         hi=[(0, w("Robert", 780) - 775.6), (3, w("apprentice", 785) - 775.6)],
         note="TRANSCRIBED FROM HIS DEATH CERTIFICATE")]),
    arch(w("greatest", 789) - 0.2, "lustig_1935.jpg", mode="print", rot=1.0, x=0.5, credit="VICTOR LUSTIG, 1935 · PUBLIC DOMAIN"),
    # ---- 11 the con man's commandments
    card("rules", 10, "The Con Man's Commandments", "n01"),
    still(795.99, "n01", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.5),
    g(806.3, "plate", bg=A("n01"), x=0.4),
    still(821.8, "n02", ((0.5, 0.5, 1.0), (0.5, 0.45, 1.14)), x=0.4),
    g(827.6, "plate", bg=A("s03"), x=0.4),
    g(843.3, "phone", x=0.4, bg=A("n04"), msgs=[
        (w("bank", 846) - 1.6 - 843.3, "Bank Security", "Unusual activity on your account.\nMove your savings to a safe\naccount now. Tell no one."),
        (w("investment", 852) - 843.3, "VIP Investments", "Insiders only: 40% a month,\nguaranteed. Closes tonight."),
        (w("official", 855) - 843.3, "Customs Office", "Your parcel is held. Pay the\n£2.99 release fee to receive it.")]),
    still(859.3, "n04", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.14))),
    clip(863.2, "n05", x=0.4),
    still(871.8, "n06", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.12)), x=0.4),
    g(CH["end_voice"] + 0.4, "endcard", x=0.8, bg=A("o06"), line="MONEY CRIMES", sub="TRUE STORIES OF THE PERFECT CON"),
]

L = lambda t0, t1, s, sub=None, **k: dict(kind="label", t0=t0, t1=t1, text=s, sub=sub, **k)
N = lambda t0, t1, title, sub, **k: dict(kind="name", t0=t0, t1=t1, title=title, sub=sub, **k)
STAMP = lambda t0, t1, s, **k: dict(kind="stamp", t0=t0, t1=t1, text=s, **k)
COUNT = lambda t0, t1, v, **k: dict(kind="counter", t0=t0, t1=t1, value=v, **k)

OVERLAYS = [
    L(1.0, 6.0, "PARIS · 1925"),
    STAMP(39.0, 40.5, "FAUX", x=1300, y=700, rot=-10, size=150),
    N(47.0, 49.5, "VICTOR LUSTIG", "1890 – 1947", x=1440, y=900, size=58),
    STAMP(w("sell", 50) + 0.3, w("con", 52), "SOLD", x=1300, y=640, rot=-8, size=170),
    # chapter 1
    L(94.9, 99.6, "DRESDEN"),
    dict(kind="lines", t0=99.8, t1=108.6, x=1240, y=300, gap=84, size=58, font="serif",
         items=[(w("German", 99), "Deutsch"), (w("French", 99), "Français"), (w("English", 99), "English"),
                (w("Italian", 99), "Italiano"), (w("Hungarian", 99), "Magyar")]),
    L(109.0, 114.4, "PARIS · 1909", "LA SORBONNE"),
    L(137.0, 141.0, "THE ATLANTIC"),
    # chapter 2
    L(163.0, 170.5, "THE 'RUMANIAN BOX'"),
    dict(kind="quote", t0=216.5, t1=221.6, text="“Officer, my illegal\nmoney machine is broken.”", size=74, y=470,
         sub="SAID NO VICTIM, EVER"),
    L(222.0, 228.4, "TEXAS → CHICAGO"),
    STAMP(235.35, 236.95, "COUNTERFEIT", x=960, y=600, rot=-7, size=150),
    L(237.3, 241.4, "SPRINGFIELD, MISSOURI · 1922"),
    # chapter 3
    L(252.6, 257.3, "PARIS · 1925"),
    L(265.8, 271.7, "THE WORLD'S FAIR · 1889"),
    L(279.4, 283.8, "A RADIO MAST · FROM 1903"),
    dict(kind="quote", t0=276.2, t1=279.0, text="« inutile et monstrueuse »", size=84, y=520,
         sub="'USELESS AND MONSTROUS' · THE ARTISTS' PROTEST, 1887"),
    COUNT(302.9, 308.3, 7000, sub="TONNES OF IRON", post="", size=190),
    # chapter 4
    L(331.8, 335.8, "HÔTEL DE CRILLON · 1925"),
    STAMP(344.6, 347.8, "STRICTLY CONFIDENTIAL", x=960, y=560, rot=-5, size=110),
    dict(kind="lines", t0=348.0, t1=364.5, x=960, y=360, gap=120, size=70, font="serif", align="center",
         items=[(348.1, "THE SECRET EXPLAINED EVERYTHING"), (w("why", 351), "Why a hotel, not a ministry?"),
                (w("Why", 358), "Why nobody could check."), (w("Why", 361), "Why it had to be fast.")], hi=0),
    N(377.0, 383.4, "ANDRÉ POISSON", "SCRAP-METAL DEALER"),
    dict(kind="lines", t0=395.0, t1=401.5, x=1180, y=380, gap=100, size=56, font="mono",
         items=[(w("secrecy", 395), "WHY THE SECRECY?"), (w("rush", 396), "WHY THE RUSH?"), (w("really", 398), "WHO IS HE?")]),
    STAMP(w("bribe", 419), 421.8, "A BRIBE", x=960, y=600, rot=-6, size=170),
    COUNT(w("70", 437) - 0.2, 442.2, 70000, sub="FRANCS", size=180),
    L(w("Austria", 441), w("Austria", 441) + 3.6, "PARIS → AUSTRIA"),
    # chapter 5
    L(454.3, 459.0, "VIENNA"),
    STAMP(461.5, 467.5, "NO COMPLAINT", x=1350, y=360, rot=-7, size=110),
    # chapter 6
    N(497.3, 503.2, "AL CAPONE", "CHICAGO", x=1420, y=900),
    L(497.3, 503.2, "THE STORY GOES"),
    COUNT(w("Capone", 503) + 0.8, 509.8, 50000, pre="$", size=180),
    L(519.9, 523.7, "TWO MONTHS LATER"),
    COUNT(w("tide", 538) - 2.2, 542.1, 5000, pre="$", sub="'TO TIDE HIM OVER'", size=180),
    STAMP(556.5, 561.6, "UNVERIFIED", x=1300, y=760, rot=-8, size=130),
    # chapter 7
    dict(kind="lines", t0=577.0, t1=584.4, x=1180, y=380, gap=120, size=56, font="serif",
         items=[(577.6, "William Watts — pharmacist"), (580.6, "Tom Shaw — chemist")]),
    L(596.3, 601.3, "THE GREAT DEPRESSION"),
    L(601.8, 610.1, "“LUSTIG MONEY”", "A COUNTERFEIT $10 NOTE"),
    L(610.6, 613.5, "U.S. SECRET SERVICE"),
    # chapter 8
    N(623.5, 629.3, "BILLY MAY", "HIS MISTRESS"),
    L(638.3, 645.2, "NEW YORK · 10 MAY 1935", "ARRESTED"),
    L(648.9, 652.1, "TIMES SQUARE SUBWAY"),
    COUNT(w("Inside", 652) + 0.6, 659.2, 51000, pre="$", sub="IN COUNTERFEIT NOTES", size=170),
    L(659.7, 666.8, "FEDERAL HOUSE OF DETENTION", "MANHATTAN"),
    STAMP(667.1, 669.9, "ESCAPE-PROOF", x=960, y=640, rot=-6, size=150),
    L(670.3, 679.0, "1 SEPTEMBER 1935"),
    # chapter 9
    COUNT(704.8, 708.3, 27, sub="DAYS ON THE RUN", size=230, count=1.2),
    dict(kind="lines", t0=718.0, t1=727.0, x=960, y=420, gap=150, size=96, font="cap", align="center",
         items=[(718.2, "9 DECEMBER 1935"), (w("15", 717) - 0.1, "15 YEARS"), (w("5", 720) - 0.1, "+ 5 FOR THE ESCAPE")], hi=0),
    L(w("Alcatraz", 733) - 0.2, 734.5, "ALCATRAZ", "SAN FRANCISCO BAY"),
    # chapter 10
    L(749.7, 756.3, "SPRINGFIELD, MISSOURI", "MARCH 1947"),
    N(756.8, 761.4, "VICTOR LUSTIG", "DIED 11 MARCH 1947", x=1440, y=900, size=58),
    dict(kind="lines", t0=763.0, t1=775.4, x=200, y=800, gap=70, size=44, font="mono",
         items=[(765.0, "1922 — 'ROBERT DUVAL' WALKS OUT WITH $10,000"), (770.5, "1947 — VICTOR LUSTIG DIES HERE")]),
    *([dict(kind="box", t0=w("Robert", 780), t1=w("occupation", 785) - 0.25, rect=cert_box(CERT_NAME, 266, 388, 560, 434), color=0xFFC8321F),
       dict(kind="box", t0=w("apprentice", 785.6), t1=w("greatest", 789) - 0.2, rect=cert_box(CERT_JOB, 310, 816, 784, 886), color=0xFFC8321F),
       dict(kind="credit", t0=782.0, t1=w("greatest", 789) - 0.2, text="DEATH CERTIFICATE, 1947 · PUBLIC DOMAIN")]
      if os.path.exists(R("death_cert.png")) else []),
    # chapter 11
    L(796.3, 806.0, "THE TEN COMMANDMENTS FOR CON MEN"),
    dict(kind="lines", t0=806.4, t1=821.7, x=300, y=250, gap=96, size=58, font="serif", tick=True,
         items=[(w("patient", 806) - 0.2, "Be a patient listener."), (w("bored", 808) - 0.3, "Never look bored."),
                (w("politics", 810) - 1.5, "Let them reveal their politics. Then agree."),
                (w("boast", 814) - 0.2, "Never boast."), (w("importance", 815) - 0.4, "Let your importance be quietly obvious."),
                (w("untidy", 819) - 0.3, "Never be untidy."), (w("drunk", 820) - 0.3, "Never get drunk.")]),
    dict(kind="lines", t0=827.8, t1=843.1, x=420, y=300, gap=110, size=64, font="serif", tick=True,
         items=[(w("official", 830) - 0.3, "An official title."), (w("secret", 832) - 0.2, "A secret nobody else could know."),
                (w("deadline", 835) - 0.2, "A deadline."), (w("reason", 836) - 0.2, "A reason not to check."),
                (w("victim", 838) - 0.2, "A victim who wanted it.")]),
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

SFX = [(0.0, "swell", -8), (9.95, "paper", -10), (10.35, "thock", -4), (63.7, "sub_drop", -6)]
for c in CH["chapters"][1:]:
    SFX.append((c["card"], "whoosh", -12))
for o in OVERLAYS:                                   # a thud for every stamp, a rattle of coins for every counter
    if o["kind"] == "stamp":
        SFX.append((o["t0"], "thock", -4))
    elif o["kind"] == "counter":
        SFX.append((o["t0"] + 0.1, "tick_run", -14))
        SFX.append((o["t0"] + o.get("count", 1.4), "coin", -12))
for sh in SHOTS:                                     # paper for documents and archive prints, air for maps
    if sh.get("quiet"):
        continue
    if sh["kind"] == "arch" or (sh["kind"] == "gfx" and sh["fn"] in ("letter", "timeline", "record")):
        SFX.append((sh["t"] + 0.05, "paper", -14))
    elif sh["kind"] == "gfx" and sh["fn"] == "map":
        SFX.append((sh["t"] + 0.05, "whoosh", -16))

MUSIC = []                      # music.py fills build/music.json
_mj = os.path.join(BUILD, "music.json")
if os.path.exists(_mj):
    MUSIC = [tuple(x) for x in json.load(open(_mj))]

SEGMENTS = [c["card"] for c in CH["chapters"][1:]]
