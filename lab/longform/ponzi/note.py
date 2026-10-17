"""Record finished Higgsfield jobs in assets_ai.json: python3 note.py <id> <stamp>[.<ext>] ... (id = still or clip id).
The job id comes from src/jobs.json; the URL is the account's public CloudFront path."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_31VfeicI6k9Gk6DeOoM2TRmu1f3/"
jobs = json.load(open(os.path.join(HERE, "src", "jobs.json")))
p = os.path.join(HERE, "assets_ai.json")
a = json.load(open(p))
args = sys.argv[1:]
for sid, stamp in zip(args[::2], args[1::2]):
    ext = ".mp4" if sid.startswith("k_") else ".png"
    a[sid] = f"{BASE}hf_{stamp}_{jobs[sid]}{ext}"
json.dump(dict(sorted(a.items())), open(p, "w"), indent=1)
print(len(a), "assets")
