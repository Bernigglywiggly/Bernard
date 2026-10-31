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

# A take the voice model would only read in two halves (vo_XXa + vo_XXb) is joined into vo_XX.wav, half a second apart.
import glob  # noqa: E402

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402

for a in sorted(glob.glob(os.path.join(HERE, "src", "vo_[0-9][0-9]a.wav"))):
    b, out = a[:-5] + "b.wav", a[:-5] + ".wav"
    if os.path.exists(b) and not os.path.exists(out):
        ya, sr = sf.read(a, dtype="float32", always_2d=True)
        yb, _ = sf.read(b, dtype="float32", always_2d=True)
        sf.write(out, np.concatenate([ya, np.zeros((int(0.5 * sr), ya.shape[1]), np.float32), yb]), sr)
        print(out, "joined")
