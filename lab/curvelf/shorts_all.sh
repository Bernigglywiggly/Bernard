#!/bin/zsh
# All nine Shorts, three at a time, from the current film files.
cd "$(dirname "$0")"; P=~/youtube/.venv/bin/python
A=lf01_escape/LF01_FLOW_v7.mp4; B=lf02_price/LF02_FLOW_v6.mp4; C=lf03_held/LF03_FLOW_v4.mp4
export FLOW_VERT=1
s() { $P flow.py "$@" > flow_short_$3.log 2>&1 & }
s lf01_escape short escape open_00 open_07 $A "An AI test escaped and hacked a real company" "The AI That Escaped"
s lf01_escape short talk board_02 board_07 $A "The AI agents built a secret message board" "The AI That Escaped"
s lf01_escape short cheat why_00 why_08 $A "Why the AI cheated" "The AI That Escaped"
wait
s lf02_price short war open_00 open_05 $B "Two AI labs cut prices in one afternoon" "The Price of Thinking"
s lf02_price short bigmac bigmac_00 bigmac_07 $B "What AI really costs, in Big Macs" "The Price of Thinking"
s lf02_price short jevons paradox_00 paradox_06 $B "Cheaper AI means a bigger bill" "The Price of Thinking"
wait
s lf03_held short held open_00 open_05 $C "OpenAI lined up its next model, then cancelled the launch" "Too Dangerous to Release"
s lf03_held short test test_00 test_07 $C "What GPT-6 did in the UK's simulated test" "Too Dangerous to Release"
s lf03_held short knew knew_00 knew_06 $C "It knew the rules. Sometimes it attacked anyway." "Too Dangerous to Release"
wait
tail -qn 1 flow_short_*.log
