#!/bin/zsh
# The Ponzi film (Money Crimes 02) in the new look: real photographs, the rail, its own score. Waits for the Curve run.
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python; S=music/serious
while pgrep -f "[m]aster_chain.sh" >/dev/null; do sleep 10; done
$P flow.py mc02_ponzi lay 2>&1 | tail -1
FLOW_MUSIC="$(ls $S/mc02_a/*.mp3 | tail -1),$(ls $S/mc02_b/*.mp3 | tail -1)" ./render_flow.sh mc02_ponzi MC02_PONZI_v2 6 2>&1 | tail -4
f=mc02_ponzi/MC02_PONZI_v2.mp4; echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f | cut -c1-6)s $(ffmpeg -hide_banner -nostats -i $f -af ebur128=peak=true -f null - 2>&1 | grep -E 'I:|Peak:' | tail -2 | tr -s ' ' | tr '\n' ' ')"
