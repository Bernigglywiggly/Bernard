#!/bin/zsh
# Ponzi third cut (critic fixes), and the three Curve films re-mixed so no score piece is entered from its quiet opening.
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python; S=music/serious
FLOW_MUSIC="$(ls $S/mc02_a/*.mp3 | tail -1),$(ls $S/mc02_b/*.mp3 | tail -1)" ./render_flow.sh mc02_ponzi MC02_PONZI_v3 6 2>&1 | tail -3
[ -f mc02_ponzi/MC02_PONZI_v3.mp4 ] && rm -f mc02_ponzi/MC02_PONZI_v2*.mp4
FLOW_LIMIT=0.56 FLOW_MUSIC="$(ls $S/lf01_a/*.mp3 | tail -1),$(ls $S/lf01_b/*.mp3 | tail -1)" $P mix_flow.py lf01_escape lf01_escape/flow/picture.mp4 lf01_escape/LF01_FLOW_v6.mp4 | tail -3
FLOW_MUSIC="$(ls $S/lf03_a/*.mp3 | tail -1),$(ls $S/lf03_b/*.mp3 | tail -1)" $P mix_flow.py lf03_held lf03_held/flow/picture.mp4 lf03_held/LF03_FLOW_v3.mp4 | tail -3
$P remux_shorts.py 2>&1 | grep "lf0"
f=mc02_ponzi/MC02_PONZI_v3.mp4; echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f | cut -c1-6)s $(ffmpeg -hide_banner -nostats -i $f -af ebur128=peak=true -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2 | tr -s ' ' | tr '\n' ' ')"
