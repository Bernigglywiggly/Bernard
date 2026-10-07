#!/bin/zsh
cd ~/Bernard/lab/curvelf
while pgrep -f "render_flow.sh lf02_price LF02_FLOW_v1" >/dev/null; do sleep 10; done
./render_flow.sh lf01_escape LF01_FLOW_v4 6 2>&1 | tail -2
./render_flow.sh lf02_price LF02_FLOW_v2 6 2>&1 | tail -2
rm -f lf01_escape/LF01_FLOW_v3*.mp4 lf02_price/LF02_FLOW_v1*.mp4
ls -la lf01_escape/LF01_FLOW_v4.mp4 lf02_price/LF02_FLOW_v2.mp4
