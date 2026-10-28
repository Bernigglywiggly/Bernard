#!/bin/bash
# Short 11 (Touchscreen MacBook): vertical cuts from Apple's own film of the 28 Oct 2026 launch, converted to 30 fps with
# RIFE. ⏳ Pre-built by account B on Wed 28 Oct before the launch: the 17:40 run sets SRC (Apple's 4K film, downloaded with
# yt-dlp --download-sections into lab/curve_v2/footage/apple_2026-10-28/, URL in SOURCES.txt there) and the mk lines below
# from scene detection, then sets HOOK_CLIP, LOOP_CLIP and FIX_CLIP in CurveV2Short11.tsx. Each clip must last at least
# as long as its scene (raise the slow factor); 5 s or less of Apple's footage per shot.
set -e
SRC=~/Bernard/lab/curve_v2/footage/apple_2026-10-28/apple_film_4k.mp4   # ⏳
R=~/tools/rife-ncnn-vulkan-20221029-macos
OUT=~/Bernard/lab/motion/public/shorts
W=/private/tmp/claude-501/s11clips
FPS_IN=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$SRC")   # e.g. 24000/1001
mk() {  # name start dur crop(w:h:x:y) slow
  local n=$1 ss=$2 t=$3 crop=$4 slow=$5
  rm -rf $W/$n && mkdir -p $W/$n/in $W/$n/out
  ffmpeg -loglevel error -y -ss $ss -t $t -i "$SRC" -vf "crop=$crop,scale=1080:1920:flags=lanczos" -start_number 1 $W/$n/in/%04d.png
  local nin=$(ls $W/$n/in | wc -l | tr -d ' ')
  local nf=$(python3 -c "from fractions import Fraction as F; print(round($nin / float(F('$FPS_IN')) * 30 * $slow))")
  $R/rife-ncnn-vulkan -i $W/$n/in -o $W/$n/out -m $R/rife-v4.6 -n $nf -f %04d.png > /dev/null 2>&1
  ffmpeg -loglevel error -y -framerate 30 -i $W/$n/out/%04d.png -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/$n.mp4
  echo "$n: $nin in -> $nf frames ($(python3 -c "print(round($nf/30,2))") s)"
}
# ⏳ from scene detection on SRC (ffmpeg -i "$SRC" -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep pts_time):
# mk s11_touch <start> <dur> 1215:2160:<x>:0 <slow>   # frame 0 and the loop: a finger on the MacBook Pro's screen (scene x1, ~3.4 s)
# mk s11_fix   <start> <dur> 1215:2160:<x>:0 <slow>   # x5: Apple's touch features, e.g. a menu opening round a fingertip (~4.3 s)
# loop: the hook's first second, reversed, so the last frame is frame 0
# ffmpeg -loglevel error -y -i $OUT/s11_touch.mp4 -vf "trim=end_frame=30,reverse,setpts=PTS-STARTPTS" -c:v libx264 -crf 15 -pix_fmt yuv420p $OUT/s11_loop.mp4
