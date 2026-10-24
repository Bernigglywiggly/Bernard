#!/bin/bash
# Roadster film: Tesla's 4K 23.976 fps clips -> 1920x1080 30 fps with RIFE (no duplicate frames), optional slow motion.
set -e
SRC=~/Bernard/lab/curve_v2/footage/tesla_2026-10-15
R=~/tools/rife-ncnn-vulkan-20221029-macos
OUT=~/Bernard/lab/motion/public/film
W=/private/tmp/claude-501/filmclips
mkdir -p $OUT $W
mk() {  # name src slow
  local n=$1 s=$2 slow=$3
  if [ -n "$ONLY" ] && [[ " $ONLY " != *" $n "* ]]; then return; fi
  rm -rf $W/$n && mkdir -p $W/$n/in $W/$n/out
  ffmpeg -loglevel error -y -i $s -vf "scale=1920:1080:flags=lanczos" -start_number 1 $W/$n/in/%04d.png
  local nin=$(ls $W/$n/in | wc -l | tr -d ' ')
  local nf=$(python3 -c "print(round($nin/23.976*30*$slow))")
  $R/rife-ncnn-vulkan -i $W/$n/in -o $W/$n/out -m $R/rife-v4.6 -n $nf -f %04d.png > /dev/null 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i $W/$n/out/%04d.png -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/$n.mp4
  echo "$n: $nin in -> $nf frames ($(python3 -c "print(round($nf/30,2))") s)"
}
mk kick_side_slow     $SRC/film/kick_side.mp4        3    # inverted over the Semi, rolls upright, lands
mk kick_close_slow    $SRC/film/kick_close.mp4       2.5  # close roll over the Semi, jets, smoke landing
mk kick_headon        $SRC/film/kick_headon.mp4      1    # head-on approach and lift over the lineup
mk kick_under_slow    $SRC/film/kick_under.mp4       3    # low angle, underside while inverted
mk ramp_overhead_slow $SRC/film/ramp_overhead.mp4    2.5  # overhead drone: mid-air roll with jets
mk ramp_aerial_wide   $SRC/film/ramp_aerial_wide.mp4 1    # wide aerial of the whole run
mk ramp_climb_wide    $SRC/film/ramp_climb_wide.mp4  1    # climbing the curl (car small: punch in)
mk ramp_leave_top     $SRC/film/ramp_leave_top.mp4   2    # leaves the top, jets, smoke landing
mk zero60_slow        $SRC/film/zero60.mp4           8    # the 0.81 s launch, 8x slower
cp $SRC/hang_slow8_punch.mp4 $OUT/hang_slow8.mp4      # already 1080p30: the hang, 8x slower, punched in
cp $SRC/drop_punch.mp4 $OUT/drop.mp4                  # already 1080p30: the drop, punched in
ls -la $OUT
