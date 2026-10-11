#!/usr/bin/env python3
"""Outlier finder without vidIQ credits (uses yt-dlp, no API key).

For each query: YouTube search (filtered by upload window, optionally sorted by views), then for every
channel in the results the median views of its last N uploads, then ratio = video views / channel median.
That is the same idea as vidIQ's "outlier score" (views vs the channel's typical video).

  python3 lab/tools/radar_outliers.py "how visa makes money" "ponzi scheme" --window year --sort views
  python3 lab/tools/radar_outliers.py --file queries.txt --window month --out out.tsv

Windows: hour, today, week, month, year, all. Sort: relevance (default) or views.
Caches channel medians in lab/tools/cache_radar/ for 7 days. Prints a TSV sorted by ratio.
Caveats: search results are YouTube's (personalisation-free but US-ish); medians use the last N uploads
of the channel's /videos tab (long-form only), so Shorts-heavy channels look different; views are
lifetime, so a 3-day-old video's ratio is understated. Judge ratio >= 3 as an outlier, >= 10 as a breakout.
"""
import argparse, base64, json, statistics, subprocess, sys, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache_radar"
DATE = {"hour": 1, "today": 2, "week": 3, "month": 4, "year": 5, "all": 0}
SORT = {"relevance": 0, "date": 2, "views": 3}


def sp(sort, date):
    f = bytearray()
    if date:
        f += bytes([8, date])
    f += bytes([16, 1])  # type = video
    b = bytearray()
    if sort:
        b += bytes([8, sort])
    b += bytes([18, len(f)]) + f
    return base64.b64encode(bytes(b)).decode()


def ytdlp_json(url, n):
    r = subprocess.run(["yt-dlp", "--no-warnings", "--flat-playlist", "-J", "--playlist-end", str(n), url],
                       capture_output=True, text=True, timeout=180)
    if r.returncode or not r.stdout.strip():
        return {}
    return json.loads(r.stdout)


def search(q, window, sort, n):
    url = ("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
           + "&sp=" + urllib.parse.quote(sp(SORT[sort], DATE[window])))
    d = ytdlp_json(url, n)
    return [e for e in d.get("entries", []) if e.get("id") and e.get("view_count") is not None]


def channel_median(cid, n=30):
    CACHE.mkdir(exist_ok=True)
    f = CACHE / f"{cid}.json"
    if f.exists() and time.time() - f.stat().st_mtime < 7 * 86400:
        return json.loads(f.read_text())
    d = ytdlp_json(f"https://www.youtube.com/channel/{cid}/videos", n)
    views = [e["view_count"] for e in d.get("entries", []) if e.get("view_count") is not None]
    out = {"median": statistics.median(views) if views else None, "n": len(views),
           "subs": d.get("channel_follower_count"), "name": d.get("channel")}
    f.write_text(json.dumps(out))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--window", default="year", choices=DATE)
    ap.add_argument("--sort", default="relevance", choices=SORT)
    ap.add_argument("--n", type=int, default=20, help="search results per query")
    ap.add_argument("--minviews", type=int, default=20000)
    ap.add_argument("--mindur", type=int, default=240, help="seconds; 0 keeps Shorts")
    ap.add_argument("--out")
    a = ap.parse_args()
    qs = list(a.queries)
    if a.file:
        qs += [l.strip() for l in open(a.file) if l.strip() and not l.startswith("#")]
    with ThreadPoolExecutor(6) as ex:
        results = list(ex.map(lambda q: (q, search(q, a.window, a.sort, a.n)), qs))
    vids = {}
    for q, es in results:
        for e in es:
            if e["view_count"] >= a.minviews and (e.get("duration") or 0) >= a.mindur and e.get("channel_id"):
                vids.setdefault(e["id"], (q, e))
    cids = sorted({e["channel_id"] for _, e in vids.values()})
    with ThreadPoolExecutor(8) as ex:
        meds = dict(zip(cids, ex.map(channel_median, cids)))
    rows = []
    for vid, (q, e) in vids.items():
        m = meds.get(e["channel_id"]) or {}
        med = m.get("median")
        ratio = e["view_count"] / med if med else None
        rows.append((ratio or 0, e["view_count"], med, m.get("subs"), e.get("duration"), e.get("channel"),
                     e.get("title"), f"https://youtu.be/{vid}", q))
    rows.sort(key=lambda r: -r[0])
    lines = ["ratio\tviews\tch_median\tsubs\tdur_s\tchannel\ttitle\turl\tquery"]
    for r in rows:
        lines.append("\t".join("" if v is None else (f"{v:.1f}" if isinstance(v, float) else str(v)) for v in r))
    txt = "\n".join(lines)
    if a.out:
        Path(a.out).write_text(txt + "\n")
    print(txt)


if __name__ == "__main__":
    sys.exit(main())
