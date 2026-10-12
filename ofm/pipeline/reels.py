#!/usr/bin/env python3
"""Approved stills -> 9:16 Reels (5-8 s) via image-to-video, + caption, audio placeholder, frame sheet.

  python reels.py --char test_ava out/test_ava/approved/cafe_window_v0.jpg --motion turn [--duration 5]
                  [--model kwaivgi/kling-v2.6-std/image-to-video] [--caption "sunday reset"] [--dry-run]

Best results: shoot the source still at 9:16 (aspect: "9:16" in the shot list). Kling and MiniMax H3
follow the input image's aspect ratio; a 4:5 still is centre-cropped (or --fit blur-pad) to 1080x1920.

Models (price from wavespeed.ai pages, 12 Oct 2026):
  kwaivgi/kling-v2.6-std/image-to-video   $0.21 / 5 s, $0.42 / 10 s   (default: best price for human motion)
  kwaivgi/kling-v3.0-std/image-to-video   $0.084/s (5 s = $0.42)       (hero clips)
  wavespeed-ai/minimax-h3/image-to-video  $0.04/s 480p .. $0.08/s 768p (cheapest; check face drift)
  alibaba/wan-3.0/image-to-video          $0.10/s 720p, 2-30 s
  bytedance/seedance-2.0/image-to-video   $0.24/s 720p                  (premium)
  google/veo3.1-fast/image-to-video       $0.10/s no audio
Audio: no music is baked in. A silent track is added; pick a trending sound inside Instagram/TikTok
(their licensed library) when posting. That keeps rights clean and lets the platform credit the sound.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import prompts as P
from ws import OUT, WaveSpeed, add_common_args

MOTIONS = {
    "hair": "a gentle breeze moves her hair, she blinks naturally and gives a small relaxed smile, "
            "subtle handheld camera sway",
    "turn": "she starts looking away, then turns her head to look into the camera and smiles softly, "
            "slow natural movement, handheld phone camera",
    "walk": "she walks towards the camera at a relaxed pace with a natural gait, background passes by, "
            "camera walks backwards in front of her, handheld",
    "laugh": "she laughs naturally at something off-camera, shoulders move, glances down then back at the "
             "camera, candid",
    "sip": "she lifts the cup, takes a small sip, lowers it and smiles at the camera, natural pace",
}
KEEP = ("Keep her face, age, eye colour, any skin marks and hair (colour, streaks, parting) exactly as in the image. "
        "Realistic human motion, "
        "natural skin, no morphing, no face change, no extra fingers, stable background.")
NEG = "morphing face, identity change, distorted hands, extra fingers, warped jewellery, flicker, cartoon, CGI"


def video_payload(model: str, image: str, prompt: str, duration: int) -> dict:
    P.lint(prompt)
    if model.startswith("kwaivgi/kling-v2.6"):
        return {"image": image, "prompt": prompt, "negative_prompt": NEG, "duration": 5 if duration <= 5 else 10}
    if model.startswith("kwaivgi/kling-v3"):
        return {"image": image, "prompt": prompt, "negative_prompt": NEG, "duration": duration,
                "cfg_scale": 0.5, "sound": False}
    if model.startswith("wavespeed-ai/minimax-h3"):
        return {"image": image, "prompt": prompt, "resolution": "768p", "duration": duration}
    if model.startswith("alibaba/wan-3.0"):
        return {"image": image, "prompt": prompt, "resolution": "720p", "aspect_ratio": "9:16",
                "duration": duration, "generate_audio": False}
    if model.startswith("bytedance/seedance"):
        return {"image": image, "prompt": prompt, "aspect_ratio": "9:16", "resolution": "720p",
                "duration": duration, "generate_audio": False}
    if model.startswith("google/veo3.1"):
        return {"image": image, "prompt": prompt, "aspect_ratio": "9:16", "duration": min(duration, 8),
                "resolution": "1080p", "generate_audio": False, "negative_prompt": NEG}
    raise SystemExit(f"no video payload builder for {model}")


def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def duration_of(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def finish(raw: Path, dest: Path, caption: str | None, fit: str) -> Path:
    """Fit to 1080x1920, optional caption in the safe zone, silent stereo track."""
    if fit == "crop":
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    else:  # blurred copy behind a centred fit
        vf = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];"
              "[b]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    if caption:
        P.lint(caption, where="caption")
        txt = caption.replace("\\", "").replace("'", "’").replace(":", "\\:")
        vf += (f",drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial Bold.ttf:text='{txt}':"
               "fontsize=58:fontcolor=white:borderw=3:bordercolor=black@0.6:x=(w-text_w)/2:y=h*0.68")
    ff("-i", str(raw), "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
       "-vf", vf + ",fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
       "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(dest))
    return dest


def frame_sheet(videos: list[Path], dest: Path, h: int = 480):
    rows = []
    for v in videos:
        d = duration_of(v)
        frames = []
        for i, t in enumerate([0.05, d / 2, max(0.0, d - 0.1)]):
            fp = dest.parent / f".{v.stem}_f{i}.jpg"
            ff("-ss", f"{t:.2f}", "-i", str(v), "-frames:v", "1", "-q:v", "3", str(fp))
            im = Image.open(fp).convert("RGB")
            im = im.resize((int(im.width * h / im.height), h))
            frames.append(im); fp.unlink()
        rows.append((v.name, frames))
    W = max(sum(f.width for f in fr) + 8 * 4 for _, fr in rows)
    sheet = Image.new("RGB", (W, len(rows) * (h + 40)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for r, (name, frames) in enumerate(rows):
        x, y = 8, r * (h + 40)
        d.text((8, y + 10), f"{name}   first / mid / last", fill=(220, 220, 220), font=font)
        for im in frames:
            sheet.paste(im, (x, y + 36)); x += im.width + 8
    sheet.save(dest, quality=88)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stills", nargs="+")
    ap.add_argument("--char", required=True)
    ap.add_argument("--motion", default="turn", help=f"preset ({', '.join(MOTIONS)}) or free text")
    ap.add_argument("--model", default="kwaivgi/kling-v2.6-std/image-to-video")
    ap.add_argument("--duration", type=int, default=5)
    ap.add_argument("--caption", default=None)
    ap.add_argument("--fit", choices=["crop", "blur-pad"], default="crop")
    add_common_args(ap)
    a = ap.parse_args()
    P.load_bible(a.char)  # bible lint + age check
    motion = MOTIONS.get(a.motion, a.motion)
    prompt = f"{motion}. {KEEP}"
    outdir = OUT / a.char / "reels"
    ws = WaveSpeed(dry_run=a.dry_run, run_cap=a.run_cap, month_cap=a.month_cap, job=f"reels:{a.char}")
    finished = []
    try:
        for s in a.stills:
            sp = Path(s)
            payload = video_payload(a.model, str(sp), prompt, a.duration)
            name = f"{sp.stem}_{a.motion if a.motion in MOTIONS else 'custom'}"
            res = ws.run(a.model, payload, dest=outdir / f"{name}_raw", note=f"reel {name}")
            if a.dry_run:
                continue
            raw = res["files"][0]
            final = finish(raw, outdir / f"{name}_916.mp4", a.caption, a.fit)
            (outdir / f"{name}_AUDIO.txt").write_text(
                "Silent track baked in. When posting: add a trending sound from the platform's own library.\n")
            (outdir / f"{name}.json").write_text(json.dumps({"model": a.model, "prompt": prompt, "still": str(sp),
                                                             "task_id": res.get("task_id"), "est": res["est"]}, indent=1))
            finished.append(final)
            print(f"[reels] {final}")
        if finished:
            frame_sheet(finished, outdir / "reels_sheet.jpg")
            print(f"[reels] frame sheet: {outdir/'reels_sheet.jpg'}  (check face drift between first/mid/last)")
    finally:
        ws.close()


if __name__ == "__main__":
    main()
