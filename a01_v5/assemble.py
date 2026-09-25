"""Brand finishing + the cut (ffmpeg).

Every shot gets the same finishing pass whatever world it came from: bloom keyed on brightness
(so amber blooms amber), vignette, film grain, the HUD with a running timecode, and a short amber
flash + chromatic kick whenever the world changes or a hit lands. W4 SIGNAL shots are first
crushed to a 3-colour ordered dither (ground, phosphor, amber) so the amber line survives there.

    python3 assemble.py              # finish all shots, cut hook + outro, mix voice + sound design
    python3 assemble.py S05 S07      # re-finish just these, then re-cut
"""
import os
import subprocess
import sys

from shots import AUDIO, BUILD, FONTS, FPS, OUTRO, SHOTS, TEX, frames

W, H = 1920, 1080
MONO = os.path.join(FONTS, "PlexMono-600.ttf")


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def timecode(t0, f0, col="0xECEDEF"):
    """drawtext: running hook timecode + frame counter, next to the mini drift line."""
    T = f"({t0:.3f}+t)"
    tc = (rf"%{{eif\:floor({T}/60)\:d\:2}}\:%{{eif\:mod(floor({T})\,60)\:d\:2}}."
          rf"%{{eif\:mod(floor({T}*100)\,100)\:d\:2}}")
    return (f"drawtext=fontfile='{MONO}':fontsize=19:fontcolor={col}@0.6:x=352:y=1003:text='{tc}',"
            f"drawtext=fontfile='{MONO}':fontsize=19:fontcolor={col}@0.4:x=474:y=1003:"
            rf"text='F %{{eif\:n+{f0}\:d\:4}}'")


def hit_expr(times, dur=0.13):
    return "+".join(rf"between(t\,{h:.3f}\,{h + dur:.3f})" for h in times)


def finish(s, prev_world=None):
    src = os.path.join(BUILD, "frames", s["id"])
    os.makedirs(os.path.join(BUILD, "shots"), exist_ok=True)
    out = os.path.join(BUILD, "shots", s["id"] + ".mp4")
    n, dur = frames(s), frames(s) / FPS
    ins = ["-framerate", str(FPS / s.get("step", 1)), "-pattern_type", "glob", "-i", os.path.join(src, "*.png"),
           "-loop", "1", "-i", os.path.join(TEX, f"HUD_{s['id']}.png")]
    if s.get("post") == "signal":
        ins += ["-i", os.path.join(TEX, "signal_palette.png")]
        fc = [f"[0:v]fps={FPS},scale=480:270:flags=area[s];[s][2:v]paletteuse=dither=bayer:bayer_scale=2,"
              f"scale={W}:{H}:flags=neighbor,format=gbrp[b0]"]
    else:
        fc = [f"[0:v]fps={FPS},scale={W}:{H}:flags=lanczos,format=gbrp[b0]"]
    hits = list(s.get("hits", []))
    if prev_world is not None and s["world"] != prev_world:
        hits = [0.0] + hits                      # every world change enters on an amber flash
    kick = f",rgbashift=rh=-7:bh=7:enable='{hit_expr(hits)}'" if hits else ""
    fc.append(f"[b0]null{kick}[base]")
    # bloom keyed on brightness, so each colour blooms as itself
    fc.append(f"[base]split=3[a][c][m];[m]format=gray,lut=y='if(gt(val,118),(val-118)*255/92,0)',format=gbrp[mk];"
              f"[c][mk]blend=all_mode=multiply,scale=480:270,gblur=sigma=7,scale={W}:{H}[g];"
              f"[a][g]blend=all_mode=screen:all_opacity={s.get('bloom', 0.6)},vignette=angle=0.5[f]")
    hud = "[1:v]format=rgba"
    if "hud_fade" in s:
        a, b = s["hud_fade"]
        hud += f",fade=t=out:st={a}:d={b - a}:alpha=1"
    fc.append(hud + "[hud];[f][hud]overlay=0:0:shortest=1[h0]")
    last = "h0"
    for i, ov in enumerate(s.get("overlays", [])):
        img, t0, t1 = ov[:3]
        idx = ins.count("-i")
        ins += ["-loop", "1", "-i", os.path.join(TEX, img)]
        if s is OUTRO:
            fc.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0}:d=1.6:alpha=1[o{i}];[{last}][o{i}]overlay=0:0:shortest=1[h{i + 1}]")
        else:
            fc.append(f"[{last}][{idx}:v]overlay=0:0:shortest=1:enable='between(t,{t0},{t1})'[h{i + 1}]")
        last = f"h{i + 1}"
    tail = "format=yuv444p"
    if hits:
        tail += f",eq=brightness=0.07:saturation=1.3:enable='{hit_expr(hits, 0.085)}'"
    if s is not OUTRO:
        tail += "," + timecode(s["t0"], round(s["t0"] * FPS), "0x0B0B0C" if s.get("hud") == "ink" else "0xECEDEF")
    if "fade_in" in s:
        tail += f",fade=t=in:st=0:d={s['fade_in']},fade=t=out:st={dur - s['fade_out']:.3f}:d={s['fade_out']}"
    grain = 11 if s is OUTRO else 9
    fc.append(f"[{last}]{tail},noise=c0s={grain}:c0f=t+u,format=yuv420p[v]")
    ff(*ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-frames:v", str(n), "-r", str(FPS),
       "-c:v", "libx264", "-crf", "14", "-preset", "medium", out)
    return out


def cut():
    shots_dir = os.path.join(BUILD, "shots")
    lst = os.path.join(shots_dir, "list.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{s['id']}.mp4'\n" for s in SHOTS)
    sfx = os.path.join(BUILD, "audio", "hook_sfx.wav")
    hook = os.path.join(BUILD, "A01_v5_hook_proof.mp4")
    ff("-f", "concat", "-safe", "0", "-i", lst, "-i", AUDIO, "-i", sfx, "-filter_complex",
       "[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0[vo];[vo][2:a]amix=inputs=2:normalize=0:duration=first,"
       "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest",
       "-movflags", "+faststart", hook)
    outro = os.path.join(BUILD, "A01_v5_outro_template.mp4")
    if os.path.exists(os.path.join(shots_dir, OUTRO["id"] + ".mp4")):
        ff("-i", os.path.join(shots_dir, OUTRO["id"] + ".mp4"), "-i", os.path.join(BUILD, "audio", "outro_music.wav"),
           "-af", "loudnorm=I=-16:TP=-1.5,aresample=48000", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
           "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", outro)
    return hook, outro


if __name__ == "__main__":
    only = set(sys.argv[1:])
    prev = None
    for s in SHOTS + [OUTRO]:
        if os.path.isdir(os.path.join(BUILD, "frames", s["id"])) and (not only or s["id"] in only):
            print("finish", finish(s, None if s is OUTRO else prev))
        prev = s["world"]
    print("cut", *cut())
