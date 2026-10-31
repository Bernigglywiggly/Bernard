"""Whisper JSON (scripts/transcribe.mjs) -> a TypeScript captions module for Remotion. Respellings fix names and
house spellings token by token. Usage:
  python3 scripts/captions_ts.py vo.json src/curve_v2/voS4Captions.ts VO_S4_CAPTIONS --fix "H2X=H2-X" "Robot=robot"
A fix matches a token's text with its leading space removed; the leading space is kept."""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument("json"); ap.add_argument("ts"); ap.add_argument("name")
ap.add_argument("--fix", nargs="*", default=[])
ap.add_argument("--script", help="the narration text (or a .py with LINES): caption words come from the script, timings from whisper")
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
if a.script:
    import difflib, re, runpy
    if a.script.endswith(".py"):
        lines = runpy.run_path(a.script)["LINES"]
        text = " ".join(l.get("cap", l["text"]) for l in lines)
    else:
        text = a.script
    breaks = set()
    sw = []
    for tok in text.split():
        if tok == "/":
            breaks.add(len(sw))
            continue
        sw.append(tok)
    # a new line in the script is a break too
    if a.script.endswith(".py"):
        n = 0
        for l in lines:
            breaks.add(n)
            n += len([t for t in l.get("cap", l["text"]).split() if t != "/"])
    norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower().replace("-", " ").replace("%", "percent"))
    NUM = {"fifty": "50", "seventy": "70", "nine": "9", "fortythree": "43", "four": "4", "eight": "8", "two": "2", "six": "6"}
    def key(w):
        n = norm(w)
        return NUM.get(n, n)
    wk = [key(c["text"]) for c in caps]
    sk = [key(w) for w in sw]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=wk, b=sk, autojunk=False).get_opcodes():
        if op == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                out.append({**caps[i], "text": " " + sw[j]})
        elif j2 > j1:
            # script words without a 1:1 match share the whisper span they replace (or a sliver after the last word)
            if i2 > i1:
                t0, t1 = caps[i1]["startMs"], caps[i2 - 1]["endMs"]
            else:
                t0 = out[-1]["endMs"] if out else 0
                t1 = t0 + 120 * (j2 - j1)
            n = j2 - j1
            for k, j in enumerate(range(j1, j2)):
                a0 = t0 + (t1 - t0) * k / n
                a1 = t0 + (t1 - t0) * (k + 1) / n
                out.append({"text": " " + sw[j], "startMs": int(a0), "endMs": int(a1), "timestampMs": int(a0), "confidence": 0.5})
    # mark forced page breaks: the first word of each manual page gets a leading pilcrow
    for j, c in enumerate(out):
        if j in breaks and j > 0:
            c["text"] = " ¶" + c["text"].lstrip()
    out[0]["text"] = out[0]["text"].lstrip()
    caps = out
src = os.path.relpath(a.json, os.path.dirname(os.path.abspath(a.ts)))
with open(a.ts, "w") as f:
    f.write(f"// Generated from {os.path.basename(a.json)} by scripts/captions_ts.py; fixes: {', '.join(a.fix) or 'none'}.\n")
    f.write('import type { Caption } from "@remotion/captions";\n\n')
    f.write(f"export const {a.name}: Caption[] = {json.dumps(caps)};\n")
print("".join(c["text"] for c in caps))
