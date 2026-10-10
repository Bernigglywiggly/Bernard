"""MAPS TEST · the "map" visual kind in flow.py (9 Oct 2026). Not a film: a test bed for the type map
(Natural Earth land in lab/curvelf/data/). Coordinates are approximate and for layout only; the shipping lanes are
sketched, not the charted traffic separation scheme.

    P=~/youtube/.venv/bin/python
    $P flow.py maps_test est && $P flow.py maps_test still <times>
"""
TITLE = "MAPS TEST"
TAG = "MAPS TEST  ·  THE STRAIT"
LEAD = 0.6
HOLD = {}
OPEN_RESOLVED = True
NAME = "maps_test"

LANE_IN = [(57.30, 25.75), (56.85, 26.30), (56.55, 26.64), (56.15, 26.66), (55.60, 26.44), (54.40, 26.18)]
LANE_OUT = [(54.40, 26.00), (55.60, 26.26), (56.15, 26.48), (56.48, 26.47), (56.72, 26.18), (57.15, 25.62)]

CHAPTERS = [
    dict(id="open", title="", beats=[
        ("About a fifth of the oil the world burns each day leaves the Gulf through one narrow channel, and most of it sails east to Asia.",
         ("map", dict(view=(-180, -58, 180, 78),
                      routes=[[(56.4, 26.4), (58.8, 24.2), (62.0, 20.5), (72.0, 10.0), (80.5, 5.3), (92.0, 6.0), (97.5, 5.6),
                               (101.0, 2.6), (104.0, 1.2), (108.0, 7.5), (114.5, 17.5), (121.0, 25.0), (122.4, 30.6)]],
                      pins=[(56.3, 26.5)],
                      labels=[(56.3, 26.6, "STRAIT OF HORMUZ", "26.6N 56.3E"), (121.5, 31.2, "SHANGHAI", "31.2N 121.5E")],
                      caption="TEST MAP  ·  NATURAL EARTH 1:110M"))),
        ("Zoom in on the Gulf, and the exits narrow to a single gap between Iran and the tip of Oman.",
         ("map", dict(view=(47.0, 23.0, 60.5, 31.0),
                      labels=[(50.16, 26.64, "RAS TANURA", "SAUDI ARABIA  ·  26.6N 50.2E"), (56.3, 26.6, "STRAIT OF HORMUZ", "THE ONLY WAY OUT")],
                      pins=[(56.3, 26.55)],
                      routes=[[(50.4, 26.8), (52.5, 26.9), (54.5, 26.3), (55.9, 26.5), (56.5, 26.55), (57.0, 25.9), (58.6, 24.6)]],
                      caption="TEST MAP  ·  NATURAL EARTH 1:10M"))),
        ("Closer still, ships keep to two lanes, one in and one out, each about three kilometres wide.",
         ("map", dict(view=(54.0, 24.5, 58.5, 27.5),
                      routes=[LANE_IN, LANE_OUT],
                      pins=[(56.45, 26.56)],
                      labels=[(56.3, 26.6, "STRAIT OF HORMUZ", "26.6N 56.3E  ·  39 KM AT ITS NARROWEST"), (55.75, 26.8, "QESHM", "IRAN"),
                              (56.25, 26.15, "MUSANDAM", "OMAN"), (56.27, 27.18, "BANDAR ABBAS", "27.2N 56.3E")],
                      caption="LANES SKETCHED FOR THIS TEST  ·  NOT FOR NAVIGATION"))),
    ]),
    dict(id="lanes", title="THE LANES", beats=[
        ("Between the lanes runs a buffer zone, and all of it lies inside Omani waters.",
         ("map", dict(view=(55.4, 25.6, 57.4, 27.0),
                      zones=[[(56.15, 26.62), (56.56, 26.62), (56.80, 26.27), (57.20, 25.72), (57.0, 25.62), (56.70, 26.15), (56.48, 26.45), (56.15, 26.45)]],
                      labels=[(56.62, 26.4, "SEPARATION ZONE", "TEST POLYGON")],
                      caption="TEST ZONE  ·  NATURAL EARTH 1:10M"))),
        ("And that is where the story of the strait really begins.", ("num", "21%", "TEST FIGURE · NOT A FACT")),
    ]),
]
