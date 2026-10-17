#!/bin/zsh
# Everything, in order, in one queue: the three Curve films, the Ponzi film, then the nine Shorts, then levels.
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python; S=music/serious
FLOW_MUSIC="$(ls $S/lf01_a/*.mp3 | tail -1),$(ls $S/lf01_b/*.mp3 | tail -1)" ./render_flow.sh lf01_escape LF01_FLOW_v6 6 2>&1 | tail -3
FLOW_MUSIC="$(ls $S/lf03_a/*.mp3 | tail -1),$(ls $S/lf03_b/*.mp3 | tail -1)" ./render_flow.sh lf03_held LF03_FLOW_v3 6 2>&1 | tail -3
./render_flow.sh lf02_price LF02_FLOW_v5 6 2>&1 | tail -1
FLOW_MUSIC="$(ls $S/mc02_a/*.mp3 | tail -1),$(ls $S/mc02_b/*.mp3 | tail -1)" ./render_flow.sh mc02_ponzi MC02_PONZI_v2 6 2>&1 | tail -3
[ -f lf01_escape/LF01_FLOW_v6.mp4 ] && rm -f lf01_escape/LF01_FLOW_v5*.mp4 lf01_escape/RESOLVE_TEST_v1.mp4 lf01_escape/RAIL_TEST_v2_serious_music.mp4
[ -f lf03_held/LF03_FLOW_v3.mp4 ] && rm -f lf03_held/LF03_FLOW_v2*.mp4
[ -f lf02_price/LF02_FLOW_v5.mp4 ] && rm -f lf02_price/LF02_FLOW_v4*.mp4
[ -f mc02_ponzi/MC02_PONZI_v2.mp4 ] && rm -f mc02_ponzi/MC02_PONZI_v1*.mp4
./shorts_all.sh > /dev/null 2>&1
$P remux_shorts.py
f=mc02_ponzi/MC02_PONZI_v2.mp4; echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f | cut -c1-6)s $(ffmpeg -hide_banner -nostats -i $f -af ebur128=peak=true -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2 | tr -s ' ' | tr '\n' ' ')"
