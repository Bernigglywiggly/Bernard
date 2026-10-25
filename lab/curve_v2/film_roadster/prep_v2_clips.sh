#!/bin/bash
# Roadster film v2 (critic round 1: fewer repeated clips): two fresh cuts from Tesla's 4K "The Ramp" (7p5LxFdc-Qg
# 0:18-0:25, 3840x2160 23.976 fps): the flight on its jets and the landing into smoke, cropped wider than S1's
# punched-in drop.mp4, RIFE to 30 fps at 2x slower (no duplicate frames). ONLY="name ..." makes just those.
set -e
SRC=~/Bernard/lab/curve_v2/footage/tesla_2026-10-15/ramp_4k.webm
R=~/tools/rife-ncnn-vulkan-20221029-macos
OUT=~/Bernard/lab/motion/public/film
W=/private/tmp/claude-501/filmclips_v2
mk() {  # name start dur crop(w:h:x:y) slow
  local n=$1 ss=$2 t=$3 crop=$4 slow=$5
  if [ -n "$ONLY" ] && [[ " $ONLY " != *" $n "* ]]; then return; fi
  rm -rf $W/$n && mkdir -p $W/$n/in $W/$n/out
  ffmpeg -loglevel error -y -ss $ss -t $t -i $SRC -vf "crop=$crop,scale=1920:1080:flags=lanczos" -start_number 1 $W/$n/in/%04d.png
  local nin=$(ls $W/$n/in | wc -l | tr -d ' ')
  local nf=$(python3 -c "print(round($nin/23.976*30*$slow))")
  $R/rife-ncnn-vulkan -i $W/$n/in -o $W/$n/out -m $R/rife-v4.6 -n $nf -f %04d.png > /dev/null 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i $W/$n/out/%04d.png -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/$n.mp4
  echo "$n: $nin in -> $nf frames ($(python3 -c "print(round($nf/30,2))") s)"
}
mk ramp4k_flight  1.0 2.9 3200:1800:300:120 2    # S4 "one launch per fill": the car on its jets, mid-air
mk ramp4k_landing 4.4 2.6 3000:1688:180:300 2    # S4 payoff: it settles into its own smoke
# b2 "whether this car counts as an aircraft": Tesla's head-on lift over the lineup (r5vsHHPVhJg 0:06-0:11, unused in
# v1), RIFE 1.3x slower so it fills the 6.5 s bridge without duplicate frames
SRC=~/Bernard/lab/curve_v2/footage/tesla_2026-10-15/film/kick_headon.mp4
mk kick_headon_slow 0 5.2 3840:2160:0:0 1.3
