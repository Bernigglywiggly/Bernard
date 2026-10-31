#!/bin/bash
# Short 14 (How SpaceX Will Catch a Falling Starship): SpaceX's own video of the first Super Heavy tower catch
# ("Starship's Fifth Flight Test", youtube.com/watch?v=hI9HQfCAw64, 128-150 s; SOURCES.txt in the footage folder).
# Each clip is a BAND 1080x760: crop 1535x1080 from x 150 (the tower and the arms sit at x ~800), scaled 0.70x.
# 23.976 fps in; RIFE slows each cut x1.5 and lands it on 30 fps so it lasts at least its scene.
# Shot boundaries in catch_128-150.mp4 (scene detection): 8.17-10.47 s booster settling into the arms at sunset;
# 16.85-19.81 s caught, wrapped in steam.
set -e
F=~/Bernard/lab/curve_v2/footage/spacex_flight5
R=~/tools/rife-ncnn-vulkan-20221029-macos
OUT=~/Bernard/lab/motion/public/shorts
W=/private/tmp/claude-501/s14clips
mk() {  # name first_frame n_frames slow
  local n=$1 a=$2 cnt=$3 slow=$4
  rm -rf $W/$n && mkdir -p $W/$n/in $W/$n/out
  ffmpeg -loglevel error -y -i $F/catch_128-150.mp4 -vf "select='between(n\,$a\,$((a+cnt-1)))',crop=1535:1080:150:0,scale=1080:760:flags=lanczos" -vsync 0 -start_number 1 $W/$n/in/%04d.png
  local nin=$(ls $W/$n/in | wc -l | tr -d ' ')
  local nf=$(python3 -c "print(round($nin*$slow*30/23.976))")
  $R/rife-ncnn-vulkan -i $W/$n/in -o $W/$n/out -m $R/rife-v4.6 -n $nf -f %04d.png > /dev/null 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i $W/$n/out/%04d.png -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/$n.mp4
  echo "$n: $nin in -> $nf frames ($(python3 -c "print(round($nf/30,2))") s)"
}
mk s14_catch 198 52 1.5    # frame 0 + x1: 8.26-10.43 s, the booster drops into the arms (2.2 s of source)
mk s14_steam 406 68 1.6    # x1 end + x2: 16.93-19.77 s, caught, steam (2.8 s of source)
# loop: the catch clip's first second, reversed, so the last frame is frame 0
ffmpeg -loglevel error -y -i $OUT/s14_catch.mp4 -vf "trim=end_frame=30,reverse,setpts=PTS-STARTPTS" -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/s14_loop.mp4
echo "s14_loop: 30 frames"
