"""Wikimedia Commons search for public-domain archival pictures (2 Oct). Prints candidates with their licence, so only
public-domain files go into a film; `get` downloads one at a sensible size and records its credit in arch/credits.json.

    python3 tools/commons.py search "Victor Lustig" [n]
    python3 tools/commons.py get "File:Victor Lustig.jpg" lustig/arch/lustig_mugshot.jpg
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "BernardStudio/1.0 (https://github.com/bernigglywiggly/bernard; documentary research)"
API = "https://commons.wikimedia.org/w/api.php"


def call(**q):
    q.update(format="json")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers={"User-Agent": UA})
    for i in range(8):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(15 * (i + 1))
    raise SystemExit("Commons kept saying 429")


def info(titles, width=2400):
    d = call(action="query", titles="|".join(titles), prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=width)
    out = []
    for p in d.get("query", {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        g = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", ""))[:90]
        out.append(dict(title=p["title"], w=ii.get("width"), h=ii.get("height"), url=ii.get("thumburl") or ii.get("url"),
                        licence=g("LicenseShortName"), artist=g("Artist"), date=g("DateTimeOriginal"), desc=g("ImageDescription")))
    return out


def search(q, n=12):
    d = call(action="query", list="search", srsearch=q, srnamespace=6, srlimit=n)
    titles = [x["title"] for x in d["query"]["search"]]
    return info(titles) if titles else []


def get(title, dest, width=2400):
    meta = info([title], width)[0]
    if "public domain" not in meta["licence"].lower() and "pd" not in meta["licence"].lower() and "cc0" not in meta["licence"].lower():
        raise SystemExit(f"not public domain: {meta['licence']}")
    req = urllib.request.Request(meta["url"], headers={"User-Agent": UA})
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    for i in range(8):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                open(dest, "wb").write(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(15 * (i + 1))
    else:
        raise SystemExit(f"{title}: the download kept saying 429")
    cp = os.path.join(os.path.dirname(os.path.abspath(dest)), "credits.json")
    cr = json.load(open(cp)) if os.path.exists(cp) else {}
    cr[os.path.basename(dest)] = dict(title=title, licence=meta["licence"], artist=meta["artist"], date=meta["date"],
                                      source="https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")))
    json.dump(cr, open(cp, "w"), indent=1, ensure_ascii=False)
    print(dest, meta["w"], "x", meta["h"], meta["licence"])


if __name__ == "__main__":
    if sys.argv[1] == "search":
        for x in search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 12):
            print(f"{x['title'][:70]:70s} {x['w']}x{x['h']} | {x['licence'][:22]} | {x['date'][:20]} | {x['desc'][:60]}")
    else:
        get(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 2400)
