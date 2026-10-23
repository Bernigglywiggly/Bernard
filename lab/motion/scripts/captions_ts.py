"""Whisper JSON (scripts/transcribe.mjs) -> a TypeScript captions module for Remotion. Respellings fix names and
house spellings token by token. Usage:
  python3 scripts/captions_ts.py vo.json src/curve_v2/voS4Captions.ts VO_S4_CAPTIONS --fix "H2X=H2-X" "Robot=robot"
A fix matches a token's text with its leading space removed; the leading space is kept."""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument("json"); ap.add_argument("ts"); ap.add_argument("name")
ap.add_argument("--fix", nargs="*", default=[])
a = ap.parse_args()
fixes = dict(f.split("=", 1) for f in a.fix)
raw = json.load(open(a.json))
caps = []
for c in raw:  # merge glued tokens (" H" "2" "X") into words first, so fixes see whole words
    if caps and not c["text"].startswith(" ") and c["text"] != "":
        caps[-1]["text"] += c["text"]
        caps[-1]["endMs"] = c["endMs"]
    else:
        caps.append(dict(c))
for c in caps:
    lead = " " if c["text"].startswith(" ") else ""
    core = c["text"].strip()
    for k, v in fixes.items():
        if core == k or core.rstrip(".,!?;") == k:
            core = v + core[len(core.rstrip(".,!?;")):] if core != k else v
    c["text"] = lead + core
src = os.path.relpath(a.json, os.path.dirname(os.path.abspath(a.ts)))
with open(a.ts, "w") as f:
    f.write(f"// Generated from {os.path.basename(a.json)} by scripts/captions_ts.py; fixes: {', '.join(a.fix) or 'none'}.\n")
    f.write('import type { Caption } from "@remotion/captions";\n\n')
    f.write(f"export const {a.name}: Caption[] = {json.dumps(caps)};\n")
print("".join(c["text"] for c in caps))
