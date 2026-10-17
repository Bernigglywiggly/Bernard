import json, subprocess, sys
plan = json.load(open("channel/uploads.json"))
for ln in open(sys.argv[1]):
    if not ln.strip(): continue
    i, url = ln.split(None, 1)
    f = "channel/" + plan[int(i)]["file"]
    r = subprocess.run([sys.executable, "lab/tools/youtube_upload.py", "put", url.strip(), f, "--manifest", "channel/uploads.json"], capture_output=True, text=True)
    print(i, (r.stdout.strip().splitlines() or ["?"])[-1], r.stderr[-300:], flush=True)
