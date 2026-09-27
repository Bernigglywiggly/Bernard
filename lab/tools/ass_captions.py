"""Captions as an ASS subtitle file from an episode's lines.json, for burning into videos made outside our
renderer (Blender, Higgsfield plates): Inter Tight, white, a soft dark box, bottom centre.

    python3 tools/ass_captions.py lab/ep03s/build/lines.json out.ass [--until 34.8]
"""
import json
import sys


def ts(t):
    h, r = divmod(max(0.0, t), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def main(src, dst, until=None):
    L = json.load(open(src))["lines"]
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Tight Medium,50,&H00FFFFFF,&H00FFFFFF,&H8C0E0C0B,&H8C0E0C0B,0,0,0,0,100,100,0,0,3,16,0,2,240,240,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    out = [head]
    for i, ln in enumerate(L):
        if until is not None and ln["start"] > until - 0.6:     # no flash of a line that only just starts
            break
        end = ln["end"] + 0.25 if until is None else min(ln["end"] + 0.25, until)
        if i + 1 < len(L):
            end = min(end, L[i + 1]["start"] - 0.06)      # never two lines on screen at once
        text = ln["text"].replace("\n", " ")
        out.append(f"Dialogue: 0,{ts(ln['start'] - 0.05)},{ts(end)},Cap,,0,0,0,,{text}\n")
    open(dst, "w").write("".join(out))
    print("wrote", dst)


if __name__ == "__main__":
    until = float(sys.argv[sys.argv.index("--until") + 1]) if "--until" in sys.argv else None
    main(sys.argv[1], sys.argv[2], until)
