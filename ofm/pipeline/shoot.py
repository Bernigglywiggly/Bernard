#!/usr/bin/env python3
"""Shot list (YAML/JSON) -> identity-locked photos.

  python shoot.py --char test_ava shots/test_shots.yaml [--mode refs|lora|lora-edit] [--variants 1] [--dry-run]

Modes
  refs       (default) multi-reference edit: master refs + scene prompt -> new photo.
             Model default bytedance/seedream-v5.0-flash/edit ($0.027, up to 10 refs, refs free).
             Premium: --model google/nano-banana-2.1/edit (~$0.07 at 2k with 4 refs).
  lora       text-to-image with the trained character LoRA: wavespeed-ai/z-image/turbo-lora ($0.01).
  lora-edit  LoRA + reference image: wavespeed-ai/qwen-image/edit-2511-lora ($0.025, up to 3 refs).

Shot fields: id, scene, outfit, pose, lighting, camera, mood, look (phone|35mm|studio), aspect.
Outputs: out/<char>/shoots/<list>/<id>_v<n>.jpg + manifest.json (prompt + model + seed per image).
Then run qc.py on that folder.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

import prompts as P
from character import load_refs
from ws import OUT, WaveSpeed, add_common_args

MODE_MODEL = {"refs": "bytedance/seedream-v5.0-flash/edit",
              "lora": "wavespeed-ai/z-image/turbo-lora",
              "lora-edit": "wavespeed-ai/qwen-image/edit-2511-lora"}


def load_shots(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text()) if path.suffix in (".yaml", ".yml") else json.loads(path.read_text())
    shots = data["shots"] if isinstance(data, dict) else data
    for s in shots:
        P.lint(json.dumps(s), where=f"shot {s.get('id')}")
    return shots


def scene_text(s: dict) -> str:
    keys = ["scene", "outfit", "pose", "lighting", "camera", "mood"]
    return ". ".join(f"{k.capitalize()}: {s[k]}" for k in keys if s.get(k))


def build_prompt(bible: dict, s: dict, mode: str, n_refs: int, trigger: str | None) -> str:
    look = s.get("look", "phone")
    ident = P.identity_text(bible, full_body=True)
    if mode == "lora":
        return (f"{trigger}, photo of {trigger} woman, {ident}. {scene_text(s)}. {P.realism_text(look)}")
    lock = P.identity_lock_clause(n_refs)
    return (f"{lock} New candid photo of her in a different place. {scene_text(s)}. "
            f"Her fixed details: {ident}. Signature style: {bible.get('signature_style', '')}. "
            f"{P.realism_text(look)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shotlist")
    ap.add_argument("--char", required=True)
    ap.add_argument("--mode", choices=list(MODE_MODEL), default="refs")
    ap.add_argument("--model", default=None, help="override the model for this mode")
    ap.add_argument("--max-refs", type=int, default=4, help="refs sent per image (front + 3/4s + full body)")
    ap.add_argument("--variants", type=int, default=1)
    ap.add_argument("--only", default="", help="comma list of shot ids")
    ap.add_argument("--resolution", default="2k")
    ap.add_argument("--lora-scale", type=float, default=0.9)
    add_common_args(ap)
    a = ap.parse_args()

    bible = P.load_bible(a.char)
    refs = load_refs(a.char)
    model = a.model or MODE_MODEL[a.mode]
    ref_imgs = (refs.get("refs") or ([refs["anchor"]] if refs.get("anchor") else []))[: a.max_refs]
    if not ref_imgs and a.mode != "lora":
        if not a.dry_run:
            raise SystemExit(f"no refs locked for {a.char}: run character.py master, qc.py, then character.py pick")
        ref_imgs = ["<front.jpg>", "<34l.jpg>", "<34r.jpg>", "<fullbody.jpg>"][: a.max_refs]
    loras, trigger = None, None
    if a.mode in ("lora", "lora-edit"):
        lora = refs.get("lora") or {}
        trigger = lora.get("trigger_word") or bible["lora"]["trigger_word"]
        path = lora.get("url") or bible["lora"].get("path")
        if not path:
            if not a.dry_run:
                raise SystemExit("no trained LoRA yet: character.py dataset + train first")
            path = "<trained-lora.safetensors URL>"
        loras = [{"path": path, "scale": a.lora_scale}]

    shots_path = Path(a.shotlist)
    shots = load_shots(shots_path)
    if a.only:
        keep = set(a.only.split(","))
        shots = [s for s in shots if s["id"] in keep]
    outdir = OUT / a.char / "shoots" / shots_path.stem
    manifest_f = outdir / "manifest.json"
    manifest = json.loads(manifest_f.read_text()) if manifest_f.exists() else {}

    ws = WaveSpeed(dry_run=a.dry_run, run_cap=a.run_cap, month_cap=a.month_cap, job=f"shoot:{a.char}")
    try:
        for s in shots:
            prompt = build_prompt(bible, s, a.mode, len(ref_imgs), trigger)
            for v in range(a.variants):
                imgs = [] if a.mode == "lora" else ref_imgs[: (3 if a.mode == "lora-edit" else a.max_refs)]
                payload = P.image_payload(model, prompt, imgs, aspect=s.get("aspect", "4:5"),
                                          resolution=a.resolution, loras=loras)
                name = f"{s['id']}_v{v}"
                res = ws.run(model, payload, dest=outdir / name, note=f"shot {s['id']}")
                if not a.dry_run:
                    manifest[name] = {"model": model, "mode": a.mode, "prompt": prompt, "refs": imgs,
                                      "files": [str(p) for p in res["files"]], "task_id": res.get("task_id"),
                                      "est_usd": res["est"]}
                    outdir.mkdir(parents=True, exist_ok=True)
                    manifest_f.write_text(json.dumps(manifest, indent=1))
        if not a.dry_run:
            print(f"[shoot] done -> {outdir}. Next: python qc.py --char {a.char} {outdir}")
    finally:
        ws.close()


if __name__ == "__main__":
    main()
