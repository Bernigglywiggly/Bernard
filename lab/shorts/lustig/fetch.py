"""Download this short's AI assets (narration, stills, clips) from Higgsfield's CDN, listed in assets.json, so make.py can
rebuild it on any machine; the bed is re-made with beds.caper (see make.py)."""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
for rel, url in json.load(open(os.path.join(HERE, "assets.json"))).items():
    p = os.path.join(HERE, rel)
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        urllib.request.urlretrieve(url, p)
        print(rel)
