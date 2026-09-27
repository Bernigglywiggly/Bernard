#!/bin/bash
# Assemble the Blender version at 24 fps: the 12 fps renders get motion-interpolated in-betweens for the calm shots;
# the fast shots (the gold burst, the shovel and the push into its grip) and every cut use real rendered in-betweens
# (blender/cold_open.py --inbetweens), since interpolation smears particles and blends across cuts.
# Then 1080p, captions, and the shared mix.
set -e
cd "$(dirname "$0")"
DUR=$(python3 -c "import json; print(json.load(open('build/events.json'))['dur'])")
python3 ../tools/ass_captions.py build/lines.json build/captions.ass --until "$DUR"
rm -rf build/d24 && mkdir -p build/d24
ffmpeg -v error -y -framerate 12 -i build/blender/frame_%04d.png \
  -vf "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" -start_number 0 build/d24/%04d.png
cp build/blender24/*.png build/d24/
ffmpeg -v error -y -framerate 24 -i build/d24/%04d.png \
  -vf "scale=1920:1080:flags=lanczos,subtitles=build/captions.ass:fontsdir=../../a01_v6/fonts" \
  -c:v libx264 -preset slow -crf 20 -maxrate 6M -bufsize 12M -pix_fmt yuv420p build/style_D_blender_silent.mp4
ffmpeg -v error -y -i build/style_D_blender_silent.mp4 -i build/open_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest \
  -movflags +faststart build/style_D_blender.mp4
ls -la build/style_D_blender.mp4
