#!/bin/bash
# Short 4 footage: crops tall from Unitree's 1080p50 film, RIFE slow motion, 30 fps, 1080x1920.
set -e
S=~/Bernard/lab/curve_v2/footage/unitree_2026-10-21/h2x_official_1080p50.mp4
R=~/tools/rife-ncnn-vulkan-20221029-macos
OUT=~/Bernard/lab/motion/public/shorts
W=/private/tmp/claude-501/s4clips
mkdir -p $OUT $W
clip() {  # name start dur x0 x1 frames_out
  if [ -n "$ONLY" ] && [[ " $ONLY " != *" $1 "* ]]; then return; fi
  local n=$1 a=$2 d=$3 x0=$4 x1=$5 nf=$6
  rm -rf $W/$n && mkdir -p $W/$n/in $W/$n/out
  local N=$(python3 -c "print(round($d*50))")
  ffmpeg -loglevel error -y -ss $a -t $d -i $S -vf "crop=608:1080:'$x0+($x1-$x0)*n/$N':0" -start_number 1 $W/$n/in/%04d.png
  if [ "$nf" = "fps" ]; then
    ffmpeg -loglevel error -y -framerate 50 -i $W/$n/in/%04d.png -vf "fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5" -c:v libx264 -crf 14 -pix_fmt yuv420p $OUT/$n.mp4
  else
    $R/rife-ncnn-vulkan -i $W/$n/in -o $W/$n/out -m $R/rife-v4.6 -n $nf -f %04d.png > /dev/null 2>&1
    ffmpeg -loglevel error -y -framerate 30 -i $W/$n/out/%04d.png -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.5" -c:v libx264 -crf 14 -pix_fmt yuv420p $OUT/$n.mp4
  fi
  echo "$n: $(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 $OUT/$n.mp4) frames"
}
clip s4_hook   2.46 0.46 600 700 92     # upside down over the car to the landing, ~6.7x slower
clip s4_kick   19.20 1.40 420 560 80    # high kick into the spinning kick, ~1.9x slower
clip s4_balance 23.00 2.20 640 680 122  # one-leg kicks under the "8 hours" label, ~1.8x slower
clip s4_knife  35.40 2.00 780 780 fps   # the knife "security demonstration", real speed
ffmpeg -loglevel error -y -i $OUT/s4_hook.mp4 -frames:v 1 $OUT/s4_frame0.png
ffmpeg -loglevel error -y -i $OUT/s4_hook.mp4 -vf reverse -c:v libx264 -crf 14 -pix_fmt yuv420p $OUT/s4_hook_rev.mp4
# Unitree's own on-screen labels, real pixels, for the receipts
ffmpeg -loglevel error -y -ss 0.5 -i $S -frames:v 1 -vf "crop=820:76:0:992,scale=1640:-1:flags=lanczos" $OUT/s4_label_speed.png
ffmpeg -loglevel error -y -ss 24.0 -i $S -frames:v 1 -vf "crop=760:110:1160:30,scale=1520:-1:flags=lanczos" $OUT/s4_label_8h.png
ffmpeg -loglevel error -y -ss 33.5 -i $S -frames:v 1 -vf "crop=600:76:0:992,scale=1200:-1:flags=lanczos" $OUT/s4_label_demo.png
ls -la $OUT | grep s4_
