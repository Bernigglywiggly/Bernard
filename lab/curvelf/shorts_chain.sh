#!/bin/zsh
cd ~/Bernard/lab/curvelf; P=~/youtube/.venv/bin/python
while pgrep -f "chain_render.sh" >/dev/null; do sleep 10; done
A=lf01_escape/LF01_FLOW_v4.mp4; [ -f $A ] || A=lf01_escape/LF01_FLOW_v3.mp4
B=lf02_price/LF02_FLOW_v2.mp4; [ -f $B ] || B=lf02_price/LF02_FLOW_v1.mp4
export FLOW_VERT=1
$P flow.py lf01_escape short escape open_00 open_08 $A "An AI test escaped and hacked a real company" "The AI That Escaped" > /tmp/s1.log 2>&1 &
$P flow.py lf01_escape short talk board_02 board_07 $A "The AI agents built a secret message board" "The AI That Escaped" > /tmp/s2.log 2>&1 &
$P flow.py lf01_escape short cheat why_00 why_09 $A "Why the AI cheated" "The AI That Escaped" > /tmp/s3.log 2>&1 &
$P flow.py lf02_price short war open_00 open_05 $B "Two AI labs cut prices in one afternoon" "The Price of Thinking" > /tmp/s4.log 2>&1 &
$P flow.py lf02_price short bigmac bigmac_00 bigmac_07 $B "What AI really costs, in Big Macs" "The Price of Thinking" > /tmp/s5.log 2>&1 &
$P flow.py lf02_price short jevons paradox_00 paradox_06 $B "Cheaper AI means a bigger bill" "The Price of Thinking" > /tmp/s6.log 2>&1 &
wait; tail -n 2 /tmp/s[1-6].log; ls -la lf01_escape/shorts lf02_price/shorts
