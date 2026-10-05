"""Measure HTP EP05 stillness (motion_report's metric) over the first 120 s at 10 fps, drift on vs off."""
import os, sys
os.environ["EP_BUILD"] = "build_est"
sys.path.insert(0, "/home/user/Bernard/lab")
import numpy as np, skia
import engine
from engine import tl
from ch2 import kit, ledger
ep = "/home/user/Bernard/lab/ch2/ep05"
tl.load(ep, "HOW THEY PROFIT · WHERE YOUR $100 GOES")
sys.path.insert(0, ep)
import scenes
def lum(img):
    a = img.resize(320, 180).toarray()[..., :3].astype(np.float32)
    return 0.114 * a[..., 0] + 0.587 * a[..., 1] + 0.299 * a[..., 2]
for push in (0.035,):
    kit.DRIFT["push"] = push
    prev, d = None, []
    for i in range(0, 1200):
        y = lum(ledger.compose(scenes, i / 10))
        if prev is not None: d.append(np.abs(y - prev).mean())
        prev = y
    d = np.array(d)
    print(f"push {push}: frozen {100*np.mean(d<0.05):.0f}%  near-still {100*np.mean(d<0.15):.0f}%  median {np.median(d):.3f}")
