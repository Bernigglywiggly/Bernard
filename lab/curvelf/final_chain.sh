#!/bin/zsh
# After lf03_chain.sh: film 2 again (long number phrases set crisp, limiter in the mix) and its three Shorts from the new file.
cd ~/Bernard/lab/curvelf; P=~/youtube/.venv/bin/python
while pgrep -f "chain_render.sh|shorts_chain.sh|lf03_chain.sh" >/dev/null; do sleep 10; done
./render_flow.sh lf02_price LF02_FLOW_v3 6 2>&1 | tail -1
B=lf02_price/LF02_FLOW_v3.mp4; [ -f $B ] && rm -f lf02_price/LF02_FLOW_v2*.mp4
export FLOW_VERT=1
$P flow.py lf02_price short war open_00 open_05 $B "Two AI labs cut prices in one afternoon" "The Price of Thinking" > /tmp/s4.log 2>&1 &
$P flow.py lf02_price short bigmac bigmac_00 bigmac_07 $B "What AI really costs, in Big Macs" "The Price of Thinking" > /tmp/s5.log 2>&1 &
$P flow.py lf02_price short jevons paradox_00 paradox_06 $B "Cheaper AI means a bigger bill" "The Price of Thinking" > /tmp/s6.log 2>&1 &
wait; ls -la lf0*/LF0*_FLOW_v*.mp4 lf0*/shorts/*.mp4
