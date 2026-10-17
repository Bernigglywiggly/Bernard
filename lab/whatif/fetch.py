"""A fresh checkout: download a What if film's keyframes and clips from the URLs in its jobs.json, then rebuild its
sound. Afterwards `cd lab/motion && npx remotion render WhatIf-<Film> out/whatif_<film>.mp4`.

    python3 whatif/fetch.py blackhole
"""
import json
import os
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
film = sys.argv[1]
d = os.path.join(os.path.dirname(HERE), "motion", "public", "whatif", film)
for rel, url in json.load(open(os.path.join(d, "jobs.json")))["urls"].items():
    dest = os.path.join(d, rel)
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(urllib.request.urlopen(url, timeout=300).read())
        print("got", rel)
subprocess.run([sys.executable, os.path.join(HERE, f"sound_{film}.py")], check=True)
