#!/bin/bash
# Short 10 (How SpaceX Really Makes Money): vertical cuts from SpaceX's own 4K "Starship's Fifth Flight Test"
# (hI9HQfCAw64, section 128-152 s = f5_catch4k.mp4, 23.976 fps), RIFE to 30 fps. Local times are shot boundaries
# from scene detection: descent close-up 3.80-8.17, booster held in the tower 16.85-19.81.
set -e
SRC=~/Bernard/lab/curve_v2/footage/spacex_2026-10-28/f5_catch4k.mp4
R=~/tools/rife-ncnn-vulkan-20221029-macos
OUT=~/Bernard/lab/motion/public/shorts
W=/private/tmp/claude-501/s10clips
mk() {  # name start dur crop(w:h:x:y) slow
  local n=$1 ss=$2 t=$3 crop=$4 slow=$5
  rm -rf $W/$n && mkdir -p $W/$n/in $W/$n/out
  ffmpeg -loglevel error -y -ss $ss -t $t -i $SRC -vf "crop=$crop,scale=1080:1920:flags=lanczos" -start_number 1 $W/$n/in/%04d.png
  local nin=$(ls $W/$n/in | wc -l | tr -d ' ')
  local nf=$(python3 -c "print(round($nin/23.976*30*$slow))")
  $R/rife-ncnn-vulkan -i $W/$n/in -o $W/$n/out -m $R/rife-v4.6 -n $nf -f %04d.png > /dev/null 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i $W/$n/out/%04d.png -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/$n.mp4
  echo "$n: $nin in -> $nf frames ($(python3 -c "print(round($nf/30,2))") s)"
}
mk s10_catch   16.95 2.8 1215:2160:1273:0 1.25   # frame 0 and the loop: the booster held in the chopsticks at sunset
mk s10_descent 4.0   4.0 1215:2160:1503:0 1.0    # x3 "rockets... lost money": the booster burning down to the tower
# loop: the catch's first second, reversed, so the last frame is frame 0
ffmpeg -loglevel error -y -i $OUT/s10_catch.mp4 -vf "trim=end_frame=30,reverse,setpts=PTS-STARTPTS" -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/s10_loop.mp4
echo "s10_loop: 30 frames"
