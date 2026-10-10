import json, sys, os
sys.path.insert(0, "lab/tools"); import youtube_upload as yu
plan = json.load(open("channel/uploads.json")); base = "channel"
done = json.load(open("channel/uploads.done.json")) if os.path.exists("channel/uploads.done.json") else {}
CONN = {"curve": "02f9e902-69d2-8a12-af4b-b4f4cd146eeb", "crimes": "02ce9a67-dbe7-8998-8da5-26da5fc35e26", "profit": "02d0de21-a222-85ea-aea9-5b0920dd34b0"}
for i in map(int, sys.argv[1:]):
    e = yu.entry_from(plan[i], base)
    key = os.path.relpath(e["file"], base)
    if key in done: print(i, "DONE", done[key]); continue
    print(json.dumps({"i": i, "conn": CONN[e["channel"]], "len": str(os.path.getsize(e["file"])), "body": json.dumps(yu.body_for(e))}))
