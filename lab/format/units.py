"""Analogies, as many as it takes (the user, 28 Sep 2026): every big number gets something people can picture, and the
out-of-the-ordinary ones are the house style. What a missile costs in Big Macs; a million dollars a day since the
Romans invaded Britain; dollar bills laid end to end three quarters of the way to the Sun. George says them straight:
the humour is in the comparison, never in the phrasing. Every value here is sourced and dated; round to two figures
and say "about".

    python3 units.py usd 725e9                 # a big amount: Big Macs, per person, a million a day since..., notes
    python3 units.py usd 96.2e9 --days 91      # ...plus per second / per day
    python3 units.py gbp 1.5e6                 # a UK amount: average houses, years of the median salary
    python3 units.py item patriot              # what a thing costs, in Big Macs and in other things
    python3 units.py sources
"""
import argparse
from math import floor, log10

# ---------------------------------------------------------------- prices (US dollars), each with its source
BIG_MAC = 6.22                     # The Economist, Big Mac index, July 2026: US average (Jan 2026 $6.12, Jul 2025 $6.01)
ITEMS = {
    "big_mac": (6.22, "a Big Mac", "The Economist, Big Mac index, July 2026 (US average)"),
    "patriot": (4.2e6, "a Patriot interceptor (PAC-3 MSE)", "US Army FY2025 budget: about $4.2M each (FY2027 request: about $5.3M)"),
    "tomahawk": (2.0e6, "a Tomahawk cruise missile", "US Navy Block V production lots: about $2M each (CSIS)"),
    "javelin": (216717, "a Javelin anti-tank missile", "US Army FY2021: $216,717 per missile, launcher not included"),
    "shahed": (35e3, "a Shahed drone", "CSIS estimate: $20,000-$50,000 each (midpoint used; say 'tens of thousands')"),
    "unitree_g1": (16e3, "a Unitree G1 humanoid robot", "Unitree launch price, May 2024: $16,000 (The Robot Report)"),
}
# ---------------------------------------------------------------- the UK in pounds
UK_HOUSE = (272611, "HM Land Registry / ONS UK House Price Index, July 2026: average UK house £272,611")
UK_SALARY = (39039, "ONS Annual Survey of Hours and Earnings, April 2025: median full-time pay £39,039 a year")
# ---------------------------------------------------------------- people, paper, distance, history
PEOPLE = (8.30e9, "UN World Population Prospects 2024: 8.30 billion people on 1 July 2026")
NOTE_MM = (0.10922, 156.1, "US Bureau of Engraving and Printing: a dollar note is 0.0043 in (0.109 mm) thick, 6.14 in (156 mm) long")
UP = [("Everest", 8849.0), ("the International Space Station", 400e3), ("the Moon", 384400e3)]
ALONG = [("London to Edinburgh", 534e3), ("London to New York", 5570e3), ("London to Tokyo", 9560e3), ("round the Earth", 40075e3),
         ("the Moon", 384400e3), ("the Sun", 149.6e9)]
HISTORY = [(-2560, "the Great Pyramid was built"), (-753, "Rome was founded"), (43, "the Romans invaded Britain"),
           (122, "Hadrian's Wall went up"), (1066, "the Battle of Hastings"), (1215, "Magna Carta"),
           (1605, "the Gunpowder Plot"), (1666, "the Great Fire of London"), (1776, "American independence"),
           (1848, "the California gold rush"), (1912, "the Titanic sank"), (1969, "the Moon landing")]
NOW = 2026.7
# ---------------------------------------------------------------- energy, kept for physics stories
KCAL = 4184.0
ENERGY = {"big_mac": (580 * KCAL, "Big Macs", "McDonald's US: 580 kcal (UK: 509 kcal)"),
          "tank_round": (0.5 * 10 * 1555 ** 2, "tank rounds", "120 mm M829A3: 10 kg at 1,555 m/s, about 12.1 MJ"),
          "cup_of_tea": (0.25 * 4184 * 85, "cups of tea (boiling the water)", "physics: 250 ml from 15 to 100 C, about 89 kJ")}


def two(x):
    """Two significant figures, as a person would say it."""
    if x == 0:
        return "0"
    p = floor(log10(abs(x))) - 1
    r = round(x / 10 ** p) * 10 ** p
    return f"{r:,.0f}" if r >= 10 else f"{r:.2g}"


def since(days, per_day):
    """'Spend $X a day since <event>' when the start year lands near something famous."""
    years = days / 365.25
    start = NOW - years
    near = min(HISTORY, key=lambda h: abs(h[0] - start))
    if abs(near[0] - start) <= max(8, 0.03 * years):
        year = f"AD {near[0]}" if 0 < near[0] < 1000 else str(near[0]) if near[0] > 0 else f"{-near[0]} BC"
        return f"${two(per_day)} a day, every day since {near[1]} ({year}), and you'd only just have spent it"
    return f"${two(per_day)} a day for {two(years)} years"


def usd(amount, days=None):
    out = [f"{two(amount / BIG_MAC)} Big Macs",
           f"${two(amount / PEOPLE[0])} for every person on Earth ({two(amount / PEOPLE[0] / BIG_MAC)} Big Macs each)"]
    for k, (v, name, _) in ITEMS.items():
        if k != "big_mac" and amount / v >= 2:
            out.append(f"{two(amount / v)} x {name}")
    for per_day in (1e3, 1e6, 1e9):
        if 30 <= amount / per_day <= 2e6:
            out.append(since(amount / per_day, per_day))
    stack = amount / 100 * NOTE_MM[0] / 1000
    tall = max((u for u in UP if u[1] <= stack * 1.3), key=lambda u: u[1], default=UP[0])
    out.append(f"$100 notes stacked {two(stack / 1000)} km high: {two(stack / tall[1])} x {tall[0]}")
    length = amount * NOTE_MM[1] / 1000
    far = max((a for a in ALONG if a[1] <= length * 1.3), key=lambda a: a[1], default=ALONG[0])
    out.append(f"$1 notes end to end: {two(length / 1000)} km, {two(length / far[1])} x {far[0]}")
    if days:
        for name, sec in (("a second", 1), ("a minute", 60), ("a day", 86400)):
            rate = amount / (days * 86400) * sec
            out.append(f"${two(rate)} {name}: about {two(rate / BIG_MAC)} Big Macs {name}")
    return out


def gbp(amount):
    return [f"{two(amount / UK_HOUSE[0])} average UK houses", f"{two(amount / UK_SALARY[0])} years of the median UK full-time salary"]


def item(key):
    v, name, _ = ITEMS[key]
    out = [f"{name}: ${two(v)} = about {two(v / BIG_MAC)} Big Macs"]
    for k, (w, other, _) in ITEMS.items():
        if k not in (key, "big_mac") and v / w >= 2:
            out.append(f"= about {two(v / w)} x {other}")
    return out


def energy(joules):
    return [f"{two(joules / v)} {name}" for v, name, _ in ENERGY.values()]


def sources():
    return [s for _, _, s in ITEMS.values()] + [UK_HOUSE[1], UK_SALARY[1], PEOPLE[1], NOTE_MM[2]] + [s for _, _, s in ENERGY.values()]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["usd", "gbp", "item", "J", "sources"])
    ap.add_argument("value", nargs="?")
    ap.add_argument("--days", type=float)
    a = ap.parse_args()
    if a.kind == "sources":
        lines = sources()
    elif a.kind == "item":
        lines = item(a.value)
    elif a.kind == "gbp":
        lines = gbp(float(a.value))
    elif a.kind == "J":
        lines = energy(float(a.value))
    else:
        lines = usd(float(a.value), a.days)
    print("\n".join("  " + s for s in lines))
