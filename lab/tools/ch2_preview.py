"""python3 tools/ch2_preview.py ch2/ep01 0 45 out.mp4 (from lab/). A silent motion preview of a Channel 2 film on its estimated timeline (no voice exists yet): frames t0..t1 with captions."""
import os, subprocess, sys
os.environ["EP_BUILD"] = "build_est"
ep_dir = os.path.abspath(sys.argv[1]); t0, t1, out = float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
sys.path.insert(0, ep_dir); sys.path.insert(0, os.path.join(ep_dir, "..", ".."))
import engine
from engine import tl
import ch2.ledger as ledger
from script import FLOORS
ledger.FLOORS[:] = FLOORS
tl.load(ep_dir, "")
import scenes
W, H, FPS = 1920, 1080, 24
enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i in range(int(t0 * FPS), int(t1 * FPS)):
    t = i / FPS
    enc.stdin.write(ledger.compose(scenes, t, lambda c, tt: ledger.CAPTIONS.draw(c, tt)).tobytes())
enc.stdin.close(); enc.wait()
print(out, round(os.path.getsize(out) / 1e6, 1), "MB")
