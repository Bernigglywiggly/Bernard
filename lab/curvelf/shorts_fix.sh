#!/bin/zsh
# 8 Oct night: the five Shorts the second critic held back (quote cards flickering at the frame edge, a label under the headline).
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python
A=lf01_escape/LF01_FLOW_v7.mp4; B=lf02_price/LF02_FLOW_v6.mp4; C=lf03_held/LF03_FLOW_v4.mp4
export FLOW_VERT=1
s() { $P flow.py "$@" > flow_short_$3.log 2>&1 & }
s lf02_price short jevons paradox_00 paradox_06 $B "Cheaper AI means a bigger bill" "The Price of Thinking"
s lf01_escape short escape open_00 open_07 $A "An AI test escaped and hacked a real company" "The AI That Escaped"
s lf01_escape short talk board_02 board_07 $A "The AI agents built a secret message board" "The AI That Escaped"
wait
s lf01_escape short cheat why_00 why_08 $A "Why the AI cheated" "The AI That Escaped"
s lf03_held short knew knew_00 knew_06 $C "It knew the rules. Sometimes it attacked anyway." "Too Dangerous to Release"
wait
for f in lf02_price/shorts/short_jevons lf01_escape/shorts/short_escape lf01_escape/shorts/short_talk lf01_escape/shorts/short_cheat lf03_held/shorts/short_knew; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f.mp4)"; done
echo SHORTSFIX DONE
