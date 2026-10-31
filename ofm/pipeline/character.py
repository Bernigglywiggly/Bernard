#!/usr/bin/env python3
"""Character bible -> master reference set -> (optional) character LoRA.

  python character.py master  --char test_ava [--anchors 1] [--views front,34l,34r,profile,fullbody] [--dry-run]
  python character.py pick    --char test_ava out/test_ava/master/front.jpg ...   # lock the chosen refs
  python character.py dataset --char test_ava --src out/test_ava/approved          # zip 15-25 refs + captions
  python character.py train   --char test_ava --trainer z-image --steps 2000 [--dry-run]

Flow
  1. anchor: text-to-image portrait(s) from the bible's fixed traits (cheap, ~$0.03 each).
     With --anchors >1 it stops so a human picks the face (then `pick`).
  2. views: identity-locked edits of the anchor into front / 3-4 left / 3-4 right / profile /
     full body, neutral expression, plain background. These are the MASTER SET.
  3. qc.py scores every view against the anchor; keep only passes.
  4. Once 15-25 approved images exist (master set + best shoot outputs), `dataset` + `train`
     make a LoRA on WaveSpeed's Z-Image trainer ($1.25 per 1,000 steps). Use it only if a
     side-by-side qc run shows it beats reference-editing (see MODELS.md).
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import prompts as P
from ws import OUT, WaveSpeed, add_common_args

HERE = Path(__file__).resolve().parent

VIEWS = {
    "front": "front-facing head-and-shoulders portrait, looking straight into the camera, neutral relaxed "
             "expression, mouth closed",
    "34l": "head-and-shoulders portrait, head turned three-quarters to her left, eyes to camera, neutral expression",
    "34r": "head-and-shoulders portrait, head turned three-quarters to her right, eyes to camera, neutral expression",
    "profile": "head-and-shoulders portrait in exact left side profile, neutral expression",
    "fullbody": "full-body photo standing straight, front view, arms relaxed at her sides with the inside of "
                "her right wrist visible, fitted plain heather-grey t-shirt, mid-blue straight jeans, white "
                "sneakers",
}
BACKDROP = "plain light-grey seamless studio background, even soft light, no props, no jewellery"


def refs_file(char: str) -> Path:
    return HERE / "characters" / f"{char}_refs.json"


def load_refs(char: str) -> dict:
    f = refs_file(char)
    return json.loads(f.read_text()) if f.exists() else {}


def save_refs(char: str, data: dict):
    refs_file(char).write_text(json.dumps(data, indent=2))
    print(f"[character] wrote {refs_file(char)}")


def cmd_master(a):
    bible = P.load_bible(a.char)
    ws = WaveSpeed(dry_run=a.dry_run, run_cap=a.run_cap, month_cap=a.month_cap, job=f"master:{a.char}")
    outdir = OUT / a.char / "master"
    refs = load_refs(a.char)
    anchor = refs.get("anchor")
    try:
        if not anchor or a.new_anchor:
            base = (f"Photo of an invented person: {P.identity_text(bible)}. {VIEWS['front']}. {BACKDROP}. "
                    f"{P.realism_text('studio')}")
            got = []
            for i in range(a.anchors):
                payload = P.image_payload(a.anchor_model, base, None, aspect="3:4", resolution="2k")
                res = ws.run(a.anchor_model, payload, dest=outdir / f"anchor_{i:02d}", note="anchor")
                got += [str(p) for p in res["files"]]
            if a.dry_run:
                anchor = "<anchor_00.jpg>"
            elif a.anchors > 1:
                print(f"[character] {len(got)} anchors in {outdir}. Look at them, then run:\n"
                      f"  python character.py pick --char {a.char} <best anchor>")
                return
            else:
                anchor = got[0]
                refs.update({"anchor": anchor, "refs": [anchor]})
                if not a.dry_run:
                    save_refs(a.char, refs)

        views = [v for v in a.views.split(",") if v]
        for v in views:
            full = v == "fullbody"
            prompt = (f"{P.identity_lock_clause(1)} New photo of her: {VIEWS[v]}. {BACKDROP}. "
                      f"Identity details to preserve: {P.identity_text(bible, full_body=full)}. "
                      f"{P.realism_text('studio')}")
            payload = P.image_payload(a.edit_model, prompt, [anchor], aspect="9:16" if full else "3:4",
                                      resolution="2k")
            ws.run(a.edit_model, payload, dest=outdir / v, note=f"view {v}")
        if not a.dry_run:
            print(f"[character] master views in {outdir}. Next: python qc.py --char {a.char} {outdir}")
    finally:
        ws.close()


def cmd_pick(a):
    files = [str(Path(f).resolve()) for f in a.files]
    for f in files:
        if not Path(f).exists():
            raise SystemExit(f"missing {f}")
    refs = load_refs(a.char)
    refs["anchor"] = files[0]
    refs["refs"] = files
    save_refs(a.char, refs)


def cmd_dataset(a):
    bible = P.load_bible(a.char)
    trig = bible["lora"]["trigger_word"]
    src = Path(a.src)
    imgs = sorted([p for p in src.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")])
    if not a.min <= len(imgs) <= a.max:
        raise SystemExit(f"need {a.min}-{a.max} approved images in {src}, found {len(imgs)}")
    zpath = OUT / a.char / f"{a.char}_lora_dataset.zip"
    zpath.parent.mkdir(parents=True, exist_ok=True)
    caption = (f"{trig}, a {bible['age']}-year-old woman with {bible['hair']['colour']} hair and "
               f"{bible['face']['eyes']} eyes")
    with zipfile.ZipFile(zpath, "w") as z:
        for i, p in enumerate(imgs):
            z.write(p, f"{i:03d}{p.suffix.lower()}")
            z.writestr(f"{i:03d}.txt", caption)   # trigger word is NOT auto-added when captions exist
    print(f"[character] dataset {zpath} ({len(imgs)} images, trigger '{trig}')")


TRAINERS = {
    "z-image": "wavespeed-ai/z-image-lora-trainer",          # -> wavespeed-ai/z-image/turbo-lora ($0.01/img)
    "qwen-2512": "wavespeed-ai/qwen-image-2512-lora-trainer",  # -> qwen-image/text-to-image-2512-lora
    "flux-dev": "wavespeed-ai/flux-dev-lora-trainer",
}
LR = {"z-image": 0.0001, "qwen-2512": 0.0004, "flux-dev": 0.0004}


def cmd_train(a):
    bible = P.load_bible(a.char)
    zpath = OUT / a.char / f"{a.char}_lora_dataset.zip"
    if not zpath.exists() and not a.dry_run:
        raise SystemExit(f"build the dataset first: python character.py dataset --char {a.char} --src ...")
    model = TRAINERS[a.trainer]
    payload = {"data": str(zpath), "trigger_word": bible["lora"]["trigger_word"], "steps": a.steps,
               "learning_rate": LR[a.trainer], "lora_rank": a.rank}
    ws = WaveSpeed(dry_run=a.dry_run, run_cap=a.run_cap, month_cap=a.month_cap, job=f"train:{a.char}")
    try:
        res = ws.run(model, payload, dest=OUT / a.char / "lora" / f"{a.char}_{a.trainer}", timeout_s=7200,
                     note=f"lora {a.trainer} {a.steps} steps")
        if not a.dry_run:
            refs = load_refs(a.char)
            # WaveSpeed keeps the trained file ~7 days: we keep the URL AND a local copy.
            refs["lora"] = {"trainer": a.trainer, "url": res["outputs"][0] if res["outputs"] else None,
                            "local": [str(p) for p in res["files"]], "trigger_word": payload["trigger_word"]}
            save_refs(a.char, refs)
            print("[character] LoRA URL expires in ~7 days: re-host the local .safetensors (e.g. a private "
                  "Hugging Face repo) and put that URL in characters/<name>_refs.json -> lora.url")
    finally:
        ws.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("master"); m.add_argument("--char", required=True)
    m.add_argument("--anchors", type=int, default=1, help="candidate anchor faces to generate (pick one if >1)")
    m.add_argument("--new-anchor", action="store_true")
    m.add_argument("--views", default=",".join(VIEWS))
    m.add_argument("--anchor-model", default="bytedance/seedream-v5.0-flash")
    m.add_argument("--edit-model", default="bytedance/seedream-v5.0-flash/edit")
    add_common_args(m)
    p = sub.add_parser("pick"); p.add_argument("--char", required=True); p.add_argument("files", nargs="+")
    d = sub.add_parser("dataset"); d.add_argument("--char", required=True); d.add_argument("--src", required=True)
    d.add_argument("--min", type=int, default=15); d.add_argument("--max", type=int, default=25)
    t = sub.add_parser("train"); t.add_argument("--char", required=True)
    t.add_argument("--trainer", choices=list(TRAINERS), default="z-image")
    t.add_argument("--steps", type=int, default=2000); t.add_argument("--rank", type=int, default=16)
    add_common_args(t)
    a = ap.parse_args()
    {"master": cmd_master, "pick": cmd_pick, "dataset": cmd_dataset, "train": cmd_train}[a.cmd](a)


if __name__ == "__main__":
    main()
