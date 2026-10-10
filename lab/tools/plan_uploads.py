"""The upload plan: every film and Short in the launch running order (channel/LAUNCH.md, the go-live page), with its file,
title, description, tags, thumbnail, playlist and publish time, written to channel/uploads.json for
tools/youtube_upload.py (`plan`, or the Zapier route: `zapier-init`, then `put`).

    python3 lab/tools/plan_uploads.py          # writes channel/uploads.json and checks every file
Times in SLOTS are UK clock times; British Summer Time (UTC+1) runs to 25 Oct 2026, so 17:00 UK is 16:00Z.
"""
import datetime
import importlib.util
import json
import os
import re
import sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(LAB)
OUT = os.path.join(ROOT, "channel", "uploads.json")
sys.path.insert(0, os.path.join(LAB, "music", "jazz"))

CHANNEL_TAGS = {"curve": ["ai", "the curve", "explained", "economics", "technology"],
                "crimes": ["true crime", "fraud", "scam", "con artist", "documentary"],
                "profit": ["business", "business model", "economics", "explained"]}
PLAYLIST = {"curve": "Every film", "crimes": "Every case", "profit": "Every company"}

# (date, UK time, channel, kind, source) in running order; kind: film | season | short | htp_short | ep_short | ai_short
SLOTS = [
    ("2026-10-05", "13:00", "crimes", "ai_short", "shorts/lustig"),
    ("2026-10-05", "13:00", "curve", "short", "curvelf/lf01_escape:escape"),
    ("2026-10-05", "17:00", "curve", "film", "curvelf/lf01_escape"),
    ("2026-10-06", "13:00", "curve", "short", "curvelf/lf01_escape:board"),
    ("2026-10-06", "13:00", "crimes", "short", "longform/lustig:capone"),
    ("2026-10-06", "17:00", "crimes", "film", "longform/lustig"),
    ("2026-10-07", "13:00", "curve", "short", "curvelf/lf02_price:war"),
    ("2026-10-07", "13:00", "crimes", "short", "longform/lustig:bribe"),
    ("2026-10-07", "17:00", "curve", "film", "curvelf/lf02_price"),
    ("2026-10-08", "13:00", "curve", "short", "curvelf/lf01_escape:cheat"),
    ("2026-10-08", "13:00", "crimes", "short", "longform/lustig:escape"),
    ("2026-10-09", "13:00", "curve", "short", "curvelf/lf02_price:bigmac"),
    ("2026-10-09", "13:00", "crimes", "short", "longform/lustig:certificate"),
    ("2026-10-09", "13:00", "profit", "htp_short", "ch2/ep01:part1"),
    ("2026-10-09", "17:00", "curve", "film", "curvelf/lf03_held"),
    ("2026-10-09", "17:00", "profit", "film", "ch2/ep01"),
    ("2026-10-10", "13:00", "curve", "short", "curvelf/lf02_price:jevons"),
    ("2026-10-10", "13:00", "crimes", "short", "longform/lustig:box"),
    ("2026-10-10", "13:00", "profit", "htp_short", "ch2/ep01:part2"),
    ("2026-10-11", "13:00", "curve", "short", "curvelf/lf03_held:held"),
    ("2026-10-11", "13:00", "crimes", "short", "longform/lustig:rules"),
    ("2026-10-11", "13:00", "profit", "htp_short", "ch2/ep01:part3"),
    ("2026-10-11", "17:00", "curve", "season", "season1:1"),
    ("2026-10-12", "13:00", "curve", "short", "curvelf/lf03_held:test"),
    ("2026-10-12", "13:00", "crimes", "short", "longform/ponzi:line"),
    ("2026-10-12", "13:00", "profit", "htp_short", "ch2/ep01:part4"),
    ("2026-10-13", "13:00", "curve", "short", "curvelf/lf03_held:knew"),
    ("2026-10-13", "13:00", "crimes", "short", "longform/ponzi:machine"),
    ("2026-10-13", "13:00", "profit", "htp_short", "ch2/ep01:part5"),
    ("2026-10-13", "17:00", "crimes", "film", "longform/ponzi"),
    ("2026-10-13", "17:00", "profit", "film", "ch2/ep02"),
    ("2026-10-13", "20:00", "profit", "htp_short", "ch2/ep02:part1"),
    ("2026-10-14", "13:00", "curve", "ep_short", "ep09:toddler"),
    ("2026-10-14", "13:00", "crimes", "short", "longform/ponzi:run"),
    ("2026-10-14", "13:00", "profit", "htp_short", "ch2/ep02:part2"),
    ("2026-10-14", "17:00", "curve", "season", "season1:2"),
    ("2026-10-15", "13:00", "curve", "ep_short", "ep10:dinosaur"),
    ("2026-10-15", "13:00", "crimes", "short", "longform/ponzi:today"),
    ("2026-10-15", "13:00", "profit", "htp_short", "ch2/ep02:part3"),
    ("2026-10-16", "13:00", "curve", "ep_short", "ep11:birthday"),
    ("2026-10-16", "13:00", "crimes", "short", "longform/ponzi:zarossi"),
    ("2026-10-16", "13:00", "profit", "htp_short", "ch2/ep02:part4"),
    ("2026-10-16", "17:00", "profit", "film", "ch2/ep03"),
    ("2026-10-16", "20:00", "profit", "htp_short", "ch2/ep03:part1"),
    ("2026-10-17", "13:00", "curve", "ep_short", "ep12:paper"),
    ("2026-10-17", "13:00", "crimes", "short", "longform/ponzi:barron"),
    ("2026-10-17", "13:00", "profit", "htp_short", "ch2/ep02:part5"),
    ("2026-10-17", "20:00", "profit", "htp_short", "ch2/ep03:part2"),
    ("2026-10-18", "13:00", "curve", "ep_short", "ep05:japan"),
    ("2026-10-18", "13:00", "crimes", "short", "longform/ponzi:end"),
    ("2026-10-18", "13:00", "profit", "htp_short", "ch2/ep03:part3"),
    # week 3 so far: How They Profit only (the other channels need new films: see HANDOFF.md, credits)
    ("2026-10-19", "13:00", "profit", "htp_short", "ch2/ep03:part4"),
    ("2026-10-20", "13:00", "profit", "htp_short", "ch2/ep03:part5"),
    ("2026-10-20", "17:00", "profit", "film", "ch2/ep04"),
    ("2026-10-20", "20:00", "profit", "htp_short", "ch2/ep04:part1"),
    ("2026-10-21", "13:00", "profit", "htp_short", "ch2/ep04:part2"),
    ("2026-10-22", "13:00", "profit", "htp_short", "ch2/ep04:part3"),
    ("2026-10-23", "13:00", "profit", "htp_short", "ch2/ep04:part4"),
    ("2026-10-24", "13:00", "profit", "htp_short", "ch2/ep04:part5"),
]
HTP_FILMS = {"ep01": "Banks With Wings", "ep02": "The Landlord in the Golden Arches", "ep03": "The $65 Membership",
             "ep04": "The Cloud Behind the Cart"}


def utc(day, hhmm):
    t = datetime.datetime.fromisoformat(f"{day}T{hhmm}:00")
    off = 1 if t < datetime.datetime(2026, 10, 25, 1) else 0          # BST until the last Sunday of October
    return (t - datetime.timedelta(hours=off)).strftime("%Y-%m-%dT%H:%M:%SZ")


def section(post, head):
    return post.split(f"## {head}\n", 1)[1].split("\n## ", 1)[0].strip()


def hashtags(text):
    return [t.replace("_", " ") for t in re.findall(r"#(\w+)", text)]


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rel(p):
    return os.path.relpath(p, os.path.dirname(OUT))


def film(src, ch):
    d = os.path.join(LAB, src)
    slug = os.path.basename(d)
    post = open(os.path.join(d, "POST.md")).read()
    desc = section(post, "Description")
    return dict(file=rel(os.path.join(d, "out", f"{slug}_1080p.mp4")), title=section(post, "Title").split("**")[1],
                description=desc, tags=CHANNEL_TAGS[ch] + hashtags(desc), thumbnail=rel(os.path.join(d, "out", "thumb_a.jpg")),
                pinned=section(post, "Pinned comment"))


def season(src, ch):
    n = src.split(":")[1]
    os.environ["SEASON"] = n
    b = os.path.join(LAB, f"season{n}" if n != "1" else "season1", "build")
    b = b if os.path.isdir(b) else os.path.join(LAB, "season1", "build")
    sys.path.insert(0, os.path.join(LAB, "pack"))
    import build as pk
    cfg = pk.SEASON_PAGES[n]
    meta = json.load(open(os.path.join(b, f"season{n}.json")))
    desc = pk.season_description(open(os.path.join(b, "description.txt")).read())
    return dict(file=rel(os.path.join(b, f"the_curve_season{n}.mp4")),
                title=cfg["titles"][0].format(mins=int(meta["duration"] // 60)), description=desc,
                tags=CHANNEL_TAGS[ch] + ["documentary", "ai explained"], thumbnail=rel(os.path.join(b, "thumb_a.jpg")),
                pinned=cfg["pinned"])


def film_short(src, ch):
    where, key = src.split(":")
    d = os.path.join(LAB, where)
    sp = module(os.path.join(d, "shorts.py"), "shorts_" + os.path.basename(d)).SHORTS[key]
    credit = ""
    if sp.get("music"):
        import library as jazz
        credit = "\n\n" + jazz.credit_line(sp["music"])
    return dict(file=rel(os.path.join(d, "out", f"short_{key}_9x16.mp4")), title=sp["title"],
                description=f"{sp['caption']} Full story: {sp['film']} (linked).{credit}",
                tags=CHANNEL_TAGS[ch] + ["shorts"] + hashtags(sp["caption"]), pinned=sp["pinned"])


def kit_short(d, key, film_name, ch):
    k = {x["name"]: x for x in json.load(open(os.path.join(d, "kit.json")))}[key]
    tail = f" Full film: {film_name} (linked)." if film_name else ""
    return dict(file=rel(os.path.join(d, k["file"])), title=k["hook"], description=k["post"] + tail,
                tags=CHANNEL_TAGS[ch] + ["shorts"] + hashtags(k["post"]),
                pinned=f"{k['tag'].split(' · ')[-1].title()}. Full film: {film_name}, on the channel." if film_name else "")


def ai_short(src, ch):
    d = os.path.join(LAB, src)
    sys.path.insert(0, os.path.join(LAB, "pack"))
    import build as pk
    pc = pk.post_copy(os.path.join(d, "POST.md"))
    master = [f for f in sorted(os.listdir(os.path.join(d, "out"))) if f.endswith("_9x16.mp4")][0]
    return dict(file=rel(os.path.join(d, "out", master)), title=pc["title"], description=pc["description"],
                tags=CHANNEL_TAGS[ch] + ["shorts"], pinned=pc["pinned"])


def entry(day, hhmm, ch, kind, src):
    if kind == "film":
        e = film(src, ch)
    elif kind == "season":
        e = season(src, ch)
    elif kind == "short":
        e = film_short(src, ch)
    elif kind == "htp_short":
        ep, key = src.split(":")
        e = kit_short(os.path.join(LAB, ep, "build", "shorts"), key, HTP_FILMS[ep.split("/")[1]], ch)
    elif kind == "ep_short":
        ep, key = src.split(":")
        e = kit_short(os.path.join(LAB, ep, "build", "shorts"), key, "", ch)
    else:
        e = ai_short(src, ch)
    tags, seen = [], set()
    for t in e["tags"]:
        if t.lower() not in seen:
            seen.add(t.lower()); tags.append(t)
    e.update(channel=ch, slot=f"{day} {hhmm} UK", publish_at=utc(day, hhmm), tags=tags, playlist_name=PLAYLIST[ch],
             category=27, made_for_kids=False, synthetic=True, kind=kind, source=src)
    return e


def main():
    plan, missing = [], []
    for s in SLOTS:
        try:
            e = entry(*s)
        except (FileNotFoundError, KeyError) as err:
            missing.append(f"{s[0]} {s[2]} {s[4]}: {err}")
            continue
        for k in ("file", "thumbnail"):
            if e.get(k) and not os.path.exists(os.path.join(os.path.dirname(OUT), e[k])):
                missing.append(f"{e['slot']} {e['channel']}: no {k} {e[k]}")
        plan.append(e)
    json.dump(plan, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"{len(plan)} uploads -> {OUT}")
    for m in missing:
        print("  missing:", m)


if __name__ == "__main__":
    main()
