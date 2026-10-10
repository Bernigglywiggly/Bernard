#!/bin/zsh
# 8 Oct, final critic: score pieces steadied (holes cut, sags levelled); the three scored films re-mixed, Shorts sound re-cut.
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python; S=music/serious
FLOW_LIMIT=0.56 FLOW_MUSIC="$(ls $S/lf01_a/*.mp3 | tail -1),$(ls $S/lf01_b/*.mp3 | tail -1)" $P mix_flow.py lf01_escape lf01_escape/flow/picture.mp4 lf01_escape/LF01_FLOW_v6.mp4 | tail -3
FLOW_MUSIC="$(ls $S/lf03_a/*.mp3 | tail -1),$(ls $S/lf03_b/*.mp3 | tail -1)" $P mix_flow.py lf03_held lf03_held/flow/picture.mp4 lf03_held/LF03_FLOW_v3.mp4 | tail -3
FLOW_MUSIC="$(ls $S/mc02_a/*.mp3 | tail -1),$(ls $S/mc02_b/*.mp3 | tail -1)" $P mix_flow.py mc02_ponzi mc02_ponzi/flow/picture.mp4 mc02_ponzi/MC02_PONZI_v3.mp4 | tail -3
$P - <<'PY'
import soundfile as sf, numpy as np, subprocess
for F,f in (("lf01_escape","LF01_FLOW_v6.mp4"),("lf03_held","LF03_FLOW_v3.mp4"),("mc02_ponzi","MC02_PONZI_v3.mp4")):
    y,sr=sf.read(f"{F}/flow/garage.wav"); y=y.mean(1); h=sr//2
    r=20*np.log10(np.array([np.sqrt((y[i:i+h]**2).mean()) for i in range(3*sr,len(y)-14*sr,h)])+1e-9)
    med=np.median(r); low=[(3+i/2) for i in np.where(r<med-15)[0]]
    m=np.array([r[i:i+60].mean() for i in range(0,len(r)-60,60)])
    pk=subprocess.run(f"ffmpeg -hide_banner -nostats -i {F}/{f} -af ebur128=peak=true -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2 | tr -s ' ' | tr '\\n' ' '",shell=True,capture_output=True,text=True).stdout
    print(F,"stem median %.0f dB; half-seconds 15 dB under: %d %s; 30 s means min %.0f max %.0f |"%(med,len(low),[round(x) for x in low[:12]],m.min(),m.max()),pk)
PY
$P remux_shorts.py 2>&1 | grep "lf0"
