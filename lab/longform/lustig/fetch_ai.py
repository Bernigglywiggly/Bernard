"""Download finished generations: python3 fetch_ai.py '<jobs_wait JSON>' -> src/ai/<id>.png|mp4, URLs kept in
assets_ai.json (so a fresh checkout can re-fetch everything without re-generating). Failed jobs are dropped from
src/jobs.json so they get resubmitted."""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
jp, ap = os.path.join(HERE, "src", "jobs.json"), os.path.join(HERE, "assets_ai.json")
jobs = json.load(open(jp))
rev = {v: k for k, v in jobs.items()}
urls = json.load(open(ap)) if os.path.exists(ap) else {}
os.makedirs(os.path.join(HERE, "src", "ai"), exist_ok=True)
for x in json.loads(sys.argv[1])["jobs"]:
    k = rev.get(x["job_id"])
    if not k:
        continue
    if x["status"] == "completed":
        ext = os.path.splitext(x["result_url"])[1]
        dest = os.path.join(HERE, "src", "ai", k + ext)
        if not os.path.exists(dest):
            open(dest, "wb").write(urllib.request.urlopen(x["result_url"], timeout=180).read())
        urls[k] = x["result_url"]
        print("got", k)
    elif x["status"] in ("failed", "nsfw", "canceled", "cancelled"):
        jobs.pop(k, None)
        print("FAILED", k, x["status"])
json.dump(jobs, open(jp, "w"), indent=1)
json.dump(dict(sorted(urls.items())), open(ap, "w"), indent=1)
