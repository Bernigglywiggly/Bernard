#!/bin/zsh
# Render a whole one-camera Curve film: parts in parallel, join, mix.   ./render_flow.sh lf01_escape OUTNAME [workers]
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python; F=$1; OUT=$2; N=${3:-6}
TOTAL=$($P -c "import json;print(int(json.load(open('$F/flow/lines.json'))['total'])+1)")
STEP=60; rm -f $F/flow/seg_*.mp4 $F/flow/list.txt
starts=($(seq 0 $STEP $TOTAL))
for a in $starts; do
  while (( $(jobs -r | wc -l) >= N )); do sleep 2; done
  $P flow.py $F seg $a $((a+STEP)) > $F/flow/seg_$a.log 2>&1 &
done; wait
for a in $starts; do printf "file 'seg_%04d.mp4'\n" $a >> $F/flow/list.txt; done
ffmpeg -v error -y -f concat -safe 0 -i $F/flow/list.txt -c copy $F/flow/picture.mp4 && $P mix_flow.py $F $F/flow/picture.mp4 $F/$OUT.mp4 && \
ffmpeg -v error -y -i $F/$OUT.mp4 -vf scale=1280:720 -c:v libx264 -crf 24 -c:a copy $F/${OUT}_phone.mp4 && ls -la $F/$OUT*.mp4
