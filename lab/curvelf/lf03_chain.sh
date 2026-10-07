#!/bin/zsh
cd ~/Bernard/lab/curvelf; P=~/youtube/.venv/bin/python
$P flow.py lf03_held lay 2>&1 | tail -1
while pgrep -f "chain_render.sh|shorts_chain.sh" >/dev/null; do sleep 10; done
./render_flow.sh lf03_held LF03_FLOW_v1 6 2>&1 | tail -2
M=lf03_held/LF03_FLOW_v1.mp4; export FLOW_VERT=1
$P flow.py lf03_held short held open_00 open_05 $M "OpenAI lined up its next model, then cancelled the launch" "Too Dangerous to Release" > /tmp/s7.log 2>&1 &
$P flow.py lf03_held short test test_00 test_10 $M "What GPT-6 did in the UK's simulated test" "Too Dangerous to Release" > /tmp/s8.log 2>&1 &
$P flow.py lf03_held short knew knew_00 knew_06 $M "It knew the rules. Sometimes it attacked anyway." "Too Dangerous to Release" > /tmp/s9.log 2>&1 &
wait; tail -n 1 /tmp/s[7-9].log; ls -la lf03_held/*.mp4 lf03_held/shorts
