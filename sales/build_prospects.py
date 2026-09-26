"""Build prospects.json from the FSA open-data mirror (food-hygiene-uk/data) files.

Selection is hand-curated by FHRSID (independents only; chains, franchises,
concessions and institutional canteens left out). Everything else (name, address,
rating, dates) comes straight from the FSA files.
"""
import json

BASE = "/tmp/claude-0/-home-user-Bernard/1ae07d89-33ea-566a-ad7d-a2b7cf4c658b/scratchpad"
MIRROR = "https://raw.githubusercontent.com/food-hygiene-uk/data/main/public/files/open-data-files/FHRS{}en-GB.json"
first_seen = json.load(open(f"{BASE}/data/first_seen.json"))

# town -> (FSA authority code, [(FHRSID, cuisine), ...])
PICKS = {
    "Stone": ("292", [
        (1195858, "Fish & chips (inferred from name)"),
        (1195891, "Fish & chips (inferred from name)"),
        (1196110, "Fish & chips (inferred from name)"),
        (1196193, "Pizza & kebab (from name)"),
        (1195735, "Kebab (from name)"),
        (1195816, "Chinese (inferred from name)"),
        (1382329, "Chicken (inferred from name)"),
        (1195941, "Fast food (type not stated)"),
        (1195502, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1195618, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1195483, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1195685, "Pizza (from name)"),
        (1195796, "Indian restaurant (from name)"),
        (1195940, "Italian / pasta (from name)"),
        (1748271, "Japanese-style bento (inferred from name)"),
        (1338807, "Unknown (FSA type: restaurant/cafe)"),
        (1195552, "Unknown (FSA type: restaurant/cafe)"),
        (1889467, "Restaurant, bar & grill (from name)"),
        (1195498, "Unknown (FSA type: restaurant/cafe)"),
        (1195901, "Bar & kitchen (from name)"),
        (1195354, "Coffee shop (from name)"),
        (1196000, "Tea shop (from name)"),
        (1195166, "Tea room (from name)"),
        (1936488, "Bakery (from name)"),
        (1557000, "Sandwiches / rolls (inferred from name)"),
    ]),
    "Newcastle-under-Lyme": ("290", [
        (1137166, "Fish & chips (from name)"),
        (1724991, "Kebab (from name)"),
        (1828058, "Kebab (from name)"),
        (1772347, "Kebab (from name)"),
        (1759579, "Kebab / Turkish (the 2015 FSA list had 'MARMARIS KEBABS' here)"),
        (1937678, "Pizza & shawarma (from name)"),
        (85714, "Pizza (inferred from name)"),
        (1822945, "Pizza (from name)"),
        (1870542, "Pizza & peri-peri (from name)"),
        (1685082, "Chinese (from name)"),
        (81344, "Chinese (from name)"),
        (1877918, "Chinese (from name)"),
        (1004870, "Chinese (inferred from name)"),
        (1353828, "Chinese (inferred from name)"),
        (1724989, "Indian (inferred from name)"),
        (1055531, "Indian / tandoori (inferred from name)"),
        (1898760, "Grill (inferred from name)"),
        (1987198, "Smash burgers (inferred from name)"),
        (1893677, "Chicken (inferred from name)"),
        (85327, "Staffordshire oatcakes (from name)"),
        (1050314, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1722943, "Unknown (FSA type: takeaway/sandwich shop)"),
        (83640, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1845664, "Fast food (type not stated)"),
        (1776097, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1749342, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1832506, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1722944, "Unknown (FSA type: takeaway/sandwich shop)"),
        (701262, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1889228, "Cafe (from name)"),
        (1578883, "Cafe (from name)"),
        (1799173, "Cafe & eatery (from name)"),
    ]),
    "Tamworth": ("295", [
        (1620292, "Fish & chips (inferred from name)"),
        (1799468, "Fish & chips (inferred from name)"),
        (1901935, "Pan-Asian (from name)"),
        (1557638, "Chinese / Cantonese (from name)"),
        (1435377, "Chinese (from name)"),
        (1589615, "Chinese (inferred from name)"),
        (1589630, "Indian + sushi (two trading names at one address)"),
        (1904493, "Indian (inferred from name)"),
        (1785915, "Pizza (from name)"),
        (1923797, "Burgers (inferred from name)"),
        (1538176, "Burgers & desserts (from name)"),
        (1878614, "Fried chicken (from name)"),
        (1957914, "Milkshakes / desserts (inferred from name)"),
        (1589550, "Unknown, possibly Turkish (Ephesus is a Turkish place name)"),
        (1738218, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1692952, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1775392, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1416191, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1971681, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1937050, "Indian / tandoori (from name)"),
        (1923798, "Chinese (from name)"),
        (1676090, "Grill (from name)"),
        (1664140, "Chinese (inferred from name)"),
        (1416200, "Fish & chips (from name)"),
        (1688068, "Unknown (FSA type: takeaway/sandwich shop)"),
        (1948937, "Peri-peri chicken (inferred from name)"),
        (1908321, "Cafe / coffee (inferred from name)"),
        (1899172, "Sandwiches (from name)"),
    ]),
}

AREA_NOTE = {
    "Stone": "Stone town centre / ST15",
    "Newcastle-under-Lyme": "Newcastle-under-Lyme town centre (ST5 1 / ST5 2)",
    "Tamworth": "Tamworth",
}


NOTES = {
    1382329: "a takeaway called RED ROOSTERS is also on Borough Road, Newcastle, so this may be a small local group",
    1893677: "a takeaway called Red Roosters is also at 13 High Street, Stone, so this may be a small local group",
    1971681: "same address as 'Ana's Kebab-Tamworth' (FSA 5, Nov 2025), so probably a change of business",
    1904493: "new FHRSID in Jan 2026 (often a new owner); a 'Papadom 4 U' traded here in the c.2015 FSA list",
    1901935: "this unit was 'Shapla Indian Takeaway' in the c.2015 FSA list",
    1195618: "also listed here in the c.2015 FSA list, so 'awaiting inspection' probably means a re-registration",
    1195483: "also listed here in the c.2015 FSA list (as 'Sunny Hill Takeaway'), so probably a re-registration",
}


def address(e):
    parts = [e.get(k) for k in ("AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4", "PostCode")]
    return ", ".join(p for p in parts if p)


out = []
for town, (code, picks) in PICKS.items():
    data = json.load(open(f"{BASE}/data/FHRS{code}en-GB.json"))["FHRSEstablishment"]
    extract = data["Header"]["ExtractDate"]
    by_id = {e["FHRSID"]: e for e in data["EstablishmentCollection"]}
    for fid, cuisine in picks:
        e = by_id[fid]
        rating, rdate = e["RatingValue"], (e.get("RatingDate") or "")[:10]
        sig = []
        if rating == "AwaitingInspection":
            sig.append("FSA: awaiting first inspection (new or recently changed business)")
        else:
            sig.append(f"FSA hygiene rating {rating} (inspected {rdate})")
            if rating in ("0", "1", "2"):
                sig.append("low hygiene rating, so pitch reviews with care")
        fs = first_seen.get(str(fid))
        if fs:
            note = f"first appeared in FSA open data {fs} (independent-food-business-pulse tracker)"
            if fid < 1850000:
                note += "; older FHRSID, so possibly a re-listing rather than a brand-new business"
            else:
                note += ", likely a new business or new owner"
            sig.append(note)
        if fid in NOTES:
            sig.append(NOTES[fid])
        sig.append(f"FSA type: {e['BusinessType']}; FSA extract {extract}")
        sig.append(f"FHRSID {fid}; FSA page https://ratings.food.gov.uk/business/{fid} (built from the confirmed URL format)")
        sig.append("Google/Tripadvisor rating, delivery apps and own website NOT checked (no web search left)")
        if rating == "AwaitingInspection" or rdate >= "2025-01-01":
            conf = "high"
        else:
            conf = "medium"
        out.append({
            "town": town,
            "name": e["BusinessName"],
            "address": address(e),
            "cuisine": cuisine,
            "signals": "; ".join(sig),
            "source_url": MIRROR.format(code),
            "confidence": conf,
        })

json.dump(out, open(f"{BASE}/prospects.json", "w"), indent=2, ensure_ascii=False)
from collections import Counter
print(Counter(p["town"] for p in out))
