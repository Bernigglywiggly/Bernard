"""Funny units, said straight (the user, 28 Sep 2026): the humour lives in the comparison, never in the line. George
reads it flat, as a plain fact, and the picture shows the unit, like the TikToks that weigh a tank round in Big Macs.

Rules (also in lab/inspo/pollar_playbook.md, rule 12):
  - every value below is sourced and dated; round to two figures and say "about";
  - one funny comparison per section (a contrasted pair counts as one); everything else stays plain;
  - a unit everyone can picture (the Big Mac is the house unit: one price, one calorie count, known everywhere);
  - the line itself stays deadpan: no "imagine that", no wink, no punchline word after it.

    python3 units.py usd 96.2e9 --days 91    # money over a period: per second, per person, in Big Macs
    python3 units.py J 12.1e6                # energy: in Big Macs, rifle rounds, cups of tea
"""
import argparse

KCAL = 4184.0
# key: (dimension, value, one, many, source)
UNITS = {
    "big_mac": ("usd", 6.22, "Big Mac", "Big Macs",
                "The Economist, Big Mac index, July 2026: US average $6.22 (Jan 2026 $6.12, Jul 2025 $6.01)"),
    "big_mac_j": ("J", 580 * KCAL, "Big Mac", "Big Macs",
                  "McDonald's US nutrition: 580 kcal (about 2.4 MJ); a UK Big Mac is 509 kcal"),
    "rifle_round": ("J", 1700.0, "rifle round", "rifle rounds",
                    "5.56x45mm NATO muzzle energy 1,600-1,800 J (Wikipedia)"),
    "fifty_cal": ("J", 18000.0, ".50-calibre round", ".50-calibre rounds",
                  ".50 BMG muzzle energy about 18,000 J for 647-750 grain loads (Wikipedia, from Ammoguide)"),
    "tank_round": ("J", 0.5 * 10 * 1555 ** 2, "tank round", "tank rounds",
                   "120 mm M829A3: a 10 kg projectile at 1,555 m/s, so about 12.1 MJ (US Army data via GlobalSecurity)"),
    "cup_of_tea": ("J", 0.25 * 4184 * 85, "cup of tea", "cups of tea",
                   "physics: 250 ml of water heated from 15 to 100 C, about 89 kJ"),
}
PEOPLE = (8.30e9, "UN World Population Prospects 2024: 8.30 billion people on 1 July 2026")
NOTE_MM = (0.10922, "US Bureau of Engraving and Printing: a banknote is 0.0043 in (0.109 mm) thick")
HEIGHTS = [("the height of Everest", 8849.0), ("the International Space Station's orbit", 400e3), ("the Moon", 384400e3)]


def two(x):
    """Two significant figures, as a person would say it."""
    if x == 0:
        return "0"
    from math import floor, log10
    p = floor(log10(abs(x))) - 1
    r = round(x / 10 ** p) * 10 ** p
    return f"{r:,.0f}" if r >= 10 else f"{r:.2g}"


def money(usd, days=None):
    mac = UNITS["big_mac"][1]
    out = [f"{two(usd / mac)} Big Macs",
           f"{two(usd / PEOPLE[0])} dollars, or {two(usd / PEOPLE[0] / mac)} Big Macs, for every person on Earth"]
    stack = usd / 100 * NOTE_MM[0] / 1000
    ref = max((h for h in HEIGHTS if h[1] <= stack * 1.5), key=lambda h: h[1], default=HEIGHTS[0])
    out.append(f"a stack of $100 notes {two(stack / 1000)} km tall ({two(stack / ref[1])} x {ref[0]})")
    if days:
        for name, sec in (("a second", 1), ("a minute", 60), ("an hour", 3600), ("a day", 86400)):
            rate = usd / (days * 86400) * sec
            out.append(f"{two(rate)} dollars {name}: about {two(rate / mac)} Big Macs {name}")
    return out


def energy(joules):
    out = []
    for key, (dim, v, one, many, _) in UNITS.items():
        if dim != "J":
            continue
        n = joules / v
        out.append(f"{two(n)} {many if n >= 1.5 else one}" if n >= 0.5 else f"1/{two(1 / n)} of a {one}")
    return out


def sources():
    return [u[4] for u in UNITS.values()] + [PEOPLE[1], NOTE_MM[1]]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dim", choices=["usd", "J", "sources"])
    ap.add_argument("value", type=float, nargs="?")
    ap.add_argument("--days", type=float)
    a = ap.parse_args()
    lines = sources() if a.dim == "sources" else money(a.value, a.days) if a.dim == "usd" else energy(a.value)
    print("\n".join("  " + s for s in lines))
