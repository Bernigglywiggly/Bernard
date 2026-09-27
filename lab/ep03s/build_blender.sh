#!/bin/bash
# Assemble the Blender version: 12 fps frames -> smoothed to 30 fps -> 1080p -> captions -> the shared mix.
set -e
cd "$(dirname "$0")"
DUR=$(python3 -c "import json; print(json.load(open('build/events.json'))['dur'])")
python3 ../tools/ass_captions.py build/lines.json build/captions.ass --until "$DUR"
ffmpeg -v error -y -framerate 12 -i build/blender/frame_%04d.png \
  -vf "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=1920:1080:flags=lanczos,subtitles=build/captions.ass:fontsdir=../../a01_v6/fonts" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p build/style_D_blender_silent.mp4
ffmpeg -v error -y -i build/style_D_blender_silent.mp4 -i build/open_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest \
  -movflags +faststart build/style_D_blender.mp4
ls -la build/style_D_blender.mp4
