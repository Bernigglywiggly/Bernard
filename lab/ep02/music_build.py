"""EP02 bed (same arrangement logic as EP01), arranged by floor: a ride-and-pads intro under GROUND, a half-time pulse under MECHANISM and
YOU, drums out for the IDEA, silence into the drop, the full liquid break once we land in IMAGINE, drums out
again for the two questions, and a coda for SURFACE. Bars follow build/lines.json (170 BPM).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "music"))
import jungle  # noqa: E402

M = json.load(open(os.path.join(HERE, "build", "lines.json")))
L = M["lines"]
BAR = jungle.BAR


def bar(t):
    return int(math.floor(t / BAR + 1e-6))


def first(f):
    return next(x for x in L if x["floor"] == f)


def main():
    drop_i = next(i for i, x in enumerate(L) if x.get("drop"))
    land = L[drop_i - 1]["end"] + 1.0 + 3.24
    q_i = next(i for i, x in enumerate(L) if x.get("quiet"))
    b1 = bar(first(1)["start"] - 0.9)
    b3 = bar(first(3)["start"] - 0.9)
    b4 = bar(L[drop_i - 1]["start"] - 0.9)
    b_land = bar(land) + 1
    b_q = bar(L[q_i]["start"] - 0.4)
    b5 = bar(first(5)["start"] - 0.9)
    b_end = int(math.ceil(M["total"] / BAR)) + 1
    arr = [("intro", b1), ("build", b3 - b1), ("break", b4 - b3), ("drop", b_land - b4),
           ("full", b_q - b_land), ("drop", b5 - b_q), ("coda", b_end - b5)]
    arr = [(s, n) for s, n in arr if n > 0]
    print(arr, round(sum(n for _, n in arr) * BAR, 1), "s")
    json.dump(dict(arr=arr), open(os.path.join(HERE, "build", "music_arr.json"), "w"))
    jungle.render(arr, "ep02_bed", flavour="liquid", rhodes_on=True, reese_on=False)


if __name__ == "__main__":
    main()
