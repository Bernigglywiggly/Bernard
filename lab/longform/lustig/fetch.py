"""Fetch the film's generated media on a fresh checkout: the AI stills and clips (assets_ai.json) into src/ai and the
narration takes (assets_vo.json) into src/. The archive photographs are in the repo (src/arch, public domain).

    python3 fetch.py
"""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
for manifest, folder in (("assets_ai.json", os.path.join("src", "ai")), ("assets_vo.json", None)):
    for k, url in json.load(open(os.path.join(HERE, manifest))).items():
        dest = os.path.join(HERE, folder, k + os.path.splitext(url)[1]) if folder else os.path.join(HERE, k)
        if not os.path.exists(dest):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "wb").write(urllib.request.urlopen(url, timeout=300).read())
            print(dest)
