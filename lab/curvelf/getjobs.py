"""Download finished Higgsfield results for a film from compact lines "<job_id> <hf_YYYYMMDD_HHMMSS> [ext]" on stdin
(the stamp is the prefix of the result file name): python3 getjobs.py <film> < lines."""
import json
import subprocess
import sys

B = "https://d8j0ntlcm91z4.cloudfront.net/user_31VfeicI6k9Gk6DeOoM2TRmu1f3/"
jobs = []
for ln in sys.stdin:
    p = ln.split()
    if len(p) >= 2:
        jobs.append(dict(job_id=p[0], status="completed", result_url=f"{B}{p[1]}_{p[0]}.{p[2] if len(p) > 2 else 'png'}"))
r = subprocess.run([sys.executable, "assets.py", sys.argv[1], "fetch", json.dumps(dict(jobs=jobs))], capture_output=True, text=True)
d = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {}
print(r.stderr[-400:], "unsubmitted:", d.get("unsubmitted"), "pending:", d.get("pending"))
