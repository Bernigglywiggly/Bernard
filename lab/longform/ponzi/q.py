"""Queue helper for the stills: `q.py next N` prints the next N requests not yet submitted (src/jobs.json);
`q.py add 11=<job id> 15=<job id> ...` records submitted jobs by request index."""
import json
import os
import sys

import ai_assets as a

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "src", "jobs.json")
jobs = json.load(open(p)) if os.path.exists(p) else {}
if sys.argv[1] == "next":
    todo = [r for r in a.stills_batch(0, size=len(a.STILLS)) if a.STILLS[r["index"]][0] not in jobs]
    print(json.dumps(todo[:int(sys.argv[2])], ensure_ascii=False))
else:
    for kv in sys.argv[2:]:
        i, jid = kv.split("=")
        jobs[a.STILLS[int(i)][0]] = jid
    json.dump(jobs, open(p, "w"), indent=1)
    print(len(jobs), "submitted of", len(a.STILLS))
