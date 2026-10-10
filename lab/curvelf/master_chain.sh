#!/bin/zsh
# All three films with the chapter rail; the serious score on films 1 and 3, the garage bed on film 2; then the nine Shorts.
cd "$(dirname "$0")"
S=music/serious
FLOW_MUSIC="$(ls $S/lf01_a/*.mp3 | tail -1),$(ls $S/lf01_b/*.mp3 | tail -1)" ./render_flow.sh lf01_escape LF01_FLOW_v6 6 2>&1 | tail -4
FLOW_MUSIC="$(ls $S/lf03_a/*.mp3 | tail -1),$(ls $S/lf03_b/*.mp3 | tail -1)" ./render_flow.sh lf03_held LF03_FLOW_v3 6 2>&1 | tail -4
./render_flow.sh lf02_price LF02_FLOW_v5 6 2>&1 | tail -2
[ -f lf01_escape/LF01_FLOW_v6.mp4 ] && rm -f lf01_escape/LF01_FLOW_v5*.mp4 lf01_escape/RAIL_TEST_v1.mp4
[ -f lf03_held/LF03_FLOW_v3.mp4 ] && rm -f lf03_held/LF03_FLOW_v2*.mp4
[ -f lf02_price/LF02_FLOW_v5.mp4 ] && rm -f lf02_price/LF02_FLOW_v4*.mp4
./shorts_all.sh
for f in lf0*/LF0*_FLOW_v?.mp4 lf0*/shorts/*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f | cut -c1-6)s $(ffmpeg -hide_banner -nostats -i $f -af ebur128=peak=true -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2 | tr -s ' ' | tr '\n' ' ')"; done
