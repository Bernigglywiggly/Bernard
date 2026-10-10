#!/bin/zsh
# 8 Oct evening: every final-critic fix in one pass. Four films re-rendered (crisp figures, held card, readable AI label,
# Ponzi's ending with pictures, steadier score), then the nine Shorts (headline below the app's top bar, three trimmed under 60 s).
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python; S=music/serious
m() { echo "$(ls $S/$1_a/*.mp3 | tail -1),$(ls $S/$1_b/*.mp3 | tail -1)" }
FLOW_MUSIC="$(m lf03)" ./render_flow.sh lf03_held LF03_FLOW_v4 6 2>&1 | tail -2
FLOW_MUSIC="$(m mc02)" ./render_flow.sh mc02_ponzi MC02_PONZI_v4 6 2>&1 | tail -2
FLOW_LIMIT=0.56 FLOW_MUSIC="$(m lf01)" ./render_flow.sh lf01_escape LF01_FLOW_v7 6 2>&1 | tail -2
./render_flow.sh lf02_price LF02_FLOW_v6 6 2>&1 | tail -2
for pair in lf03_held/LF03_FLOW_v4:lf03_held/LF03_FLOW_v3 mc02_ponzi/MC02_PONZI_v4:mc02_ponzi/MC02_PONZI_v3 lf01_escape/LF01_FLOW_v7:lf01_escape/LF01_FLOW_v6 lf02_price/LF02_FLOW_v6:lf02_price/LF02_FLOW_v5; do
  [ -s ${pair%%:*}.mp4 ] && rm -f ${pair##*:}.mp4 ${pair##*:}_phone.mp4
done
rm -f lf01_escape/flow/short_*_pic_orig.mp4
./shorts_all.sh 2>&1 | tail -9
$P remux_shorts.py 2>&1 | grep "lf0"
for f in lf01_escape/LF01_FLOW_v7 lf02_price/LF02_FLOW_v6 lf03_held/LF03_FLOW_v4 mc02_ponzi/MC02_PONZI_v4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f.mp4 | cut -c1-6)s $(ffmpeg -hide_banner -nostats -i $f.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2 | tr -s ' ' | tr '\n' ' ')"; done
for f in */shorts/*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
echo FIXALL DONE
