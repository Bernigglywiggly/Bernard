"""The pilot's jungle bed, arranged to the voice: calm half-time under the cold open, the full break
from 'Here's the part nobody explains properly', drums out for the drop, an atmospheric break for the
gold rush, full again for 'Right now', and a coda. Bars follow build/lines.json.

    python3 music_build.py      # ../out/music/pilot_bed.wav + stems
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


def bar_at(t):
    return int(math.floor(t / BAR + 1e-6))


def main():
    b_curve = bar_at(L[4]["start"] - 0.5)            # full drums a bar-ish before 'Here's the part...'
    b_drop = bar_at(L[11]["start"] - 0.4)
    b_break = bar_at(L[12]["start"] - 0.8)
    b_full2 = bar_at(L[17]["start"] - 0.45)
    b_coda = bar_at(L[20]["start"] - 0.55)
    b_end = int(math.ceil(M["total"] / BAR)) + 1
    arr = [("intro", 2), ("build", b_curve - 2), ("full", b_drop - b_curve), ("drop", b_break - b_drop),
           ("break", b_full2 - b_break), ("full", b_coda - b_full2), ("coda", b_end - b_coda)]
    print(arr, sum(n for _, n in arr) * BAR)
    json.dump(dict(arr=arr, bar=BAR), open(os.path.join(HERE, "build", "music_arr.json"), "w"))
    jungle.render(arr, "pilot_bed", flavour="liquid", rhodes_on=True, reese_on=False)


if __name__ == "__main__":
    main()
