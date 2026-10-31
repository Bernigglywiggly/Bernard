#!/bin/bash
# Short 13 (How Do Jets Land on Aircraft Carriers?): U.S. Navy footage of the F-35C's first landing on the John F.
# Kennedy (CVN 79), 13 Oct 2026 (public domain; SOURCES.txt in the footage folder). Each clip is a full-width
# cinematic BAND 1080x468: crop 1920x832 from y 124, which drops the uploader's corner logos (flag top-left, YouTube
# mark bottom-right) with no upscaling. RIFE slows each cut so it lasts at least as long as its scene (29.97 fps in).
# Shot boundaries (scene detection): trap_head one shot 3.00-15.15 s; trap_side side landing 0.33-8.21 s, stern
# approach 8.21-11.28 s.
set -e
F=~/Bernard/lab/curve_v2/footage/navy_cvn79_2026-10-13
R=~/tools/rife-ncnn-vulkan-20221029-macos
OUT=~/Bernard/lab/motion/public/shorts
W=/private/tmp/claude-501/s13clips
mk() {  # name src first_frame n_frames slow
  local n=$1 src=$2 a=$3 cnt=$4 slow=$5
  rm -rf $W/$n && mkdir -p $W/$n/in $W/$n/out
  ffmpeg -loglevel error -y -i $F/$src -vf "select='between(n\,$a\,$((a+cnt-1)))',crop=1920:832:0:124,scale=1080:468:flags=lanczos" -vsync 0 -start_number 1 $W/$n/in/%04d.png
  local nin=$(ls $W/$n/in | wc -l | tr -d ' ')
  local nf=$(python3 -c "print(round($nin*$slow))")
  $R/rife-ncnn-vulkan -i $W/$n/in -o $W/$n/out -m $R/rife-v4.6 -n $nf -f %04d.png > /dev/null 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i $W/$n/out/%04d.png -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/$n.mp4
  echo "$n: $nin in -> $nf frames ($(python3 -c "print(round($nf/30,2))") s)"
}
mk s13_head  trap_head.mp4 150 82 1.5    # frame 0 + x1: head-on, touchdown to nearly stopped, the wire pulled out at the left
mk s13_side  trap_side.mp4 135 60 1.5    # x1 end: side angle, the wire under the jet
mk s13_stern trap_side.mp4 246 92 1.45   # x2: over the wake, across the ramp
# loop: the head-on clip's first second, reversed, so the last frame is frame 0
ffmpeg -loglevel error -y -i $OUT/s13_head.mp4 -vf "trim=end_frame=30,reverse,setpts=PTS-STARTPTS" -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/s13_loop.mp4
echo "s13_loop: 30 frames"
