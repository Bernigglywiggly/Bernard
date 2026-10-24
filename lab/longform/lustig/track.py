"""Record generation job ids by request index (python3 track.py '<json of jobs>'): index < 100 is STILLS[index], >= 100
is the clip list. Prints what still needs submitting."""
import json
import os
import sys

import ai_assets as a

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "jobs.json")
j = json.load(open(p)) if os.path.exists(p) else {}
clips = list(a.CLIPS)
for x in json.loads(sys.argv[1]) if len(sys.argv) > 1 else []:
    if x.get("job_id"):
        k = a.STILLS[x["index"]][0] if x["index"] < 100 else clips[x["index"] - 100]
        j[k] = x["job_id"]
json.dump(j, open(p, "w"), indent=1)
todo_s = [i for i, s in enumerate(a.STILLS) if s[0] not in j]
todo_c = [100 + i for i, c in enumerate(clips) if c not in j]
print(len(j), "recorded; stills to submit:", todo_s, "clips to submit:", todo_c)
