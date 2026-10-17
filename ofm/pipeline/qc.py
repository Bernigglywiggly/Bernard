#!/usr/bin/env python3
"""Identity QC: face-embedding similarity vs the master set + a fixed-details checklist + contact sheet.

  python qc.py --char test_ava out/test_ava/shoots/test_shots [more files/dirs] [--threshold 0.40]
               [--approve-to out/test_ava/approved]

How the score works (CPU only, no torch):
  * OpenCV YuNet finds the face + 5 landmarks; OpenCV SFace (ArcFace-style recogniser, OpenCV Zoo)
    turns the aligned face into a 128-d embedding.
  * Each candidate is compared (cosine) with the CENTROID of the reference embeddings
    (refs = characters/<char>_refs.json, else out/<char>/master/*). Also reported: the lowest
    cosine to any single ref.
  * OpenCV's published same-person threshold for SFace cosine is 0.363. Default gate here is
    0.40 (a bit stricter). Calibrate on your own set: real consistent outputs of one character
    usually land well above 0.5; a different face usually lands below 0.3.
  * Embeddings cannot see moles, freckles, tattoos or eye colour reliably -> CHECKLIST.md lists
    the bible's fixed details per image for a human / vision pass. Both gates must pass.
Outputs next to the inputs' first folder: qc.json, qc.csv, contact_sheet.jpg, CHECKLIST.md
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import urllib.request
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import prompts as P
from ws import CACHE, OUT

HERE = Path(__file__).resolve().parent
MODELS = {
    "det": ("face_detection_yunet_2023mar.onnx",
            "https://huggingface.co/opencv/face_detection_yunet/resolve/main/face_detection_yunet_2023mar.onnx"),
    "rec": ("face_recognition_sface_2021dec.onnx",
            "https://huggingface.co/opencv/face_recognition_sface/resolve/main/face_recognition_sface_2021dec.onnx"),
}
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")


def model_path(key: str) -> str:
    name, url = MODELS[key]
    p = CACHE / "models" / name
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        print(f"[qc] fetching {name} (OpenCV Zoo, one-off)")
        urllib.request.urlretrieve(url, p)
    return str(p)


class FaceID:
    def __init__(self):
        self.det = cv2.FaceDetectorYN.create(model_path("det"), "", (320, 320), 0.8, 0.3, 5000)
        self.rec = cv2.FaceRecognizerSF.create(model_path("rec"), "")

    def embed(self, path: Path):
        img = cv2.imread(str(path))
        if img is None:
            return None, 0, "unreadable"
        h, w = img.shape[:2]
        scale = 1.0
        if max(h, w) > 1600:                      # detector is faster + steadier on ~1.6k images
            scale = 1600 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))
            h, w = img.shape[:2]
        self.det.setInputSize((w, h))
        _, faces = self.det.detect(img)
        if faces is None or len(faces) == 0:
            return None, 0, "no face"
        face = max(faces, key=lambda f: f[2] * f[3])
        aligned = self.rec.alignCrop(img, face)
        feat = self.rec.feature(aligned).flatten().astype(np.float32)
        feat /= np.linalg.norm(feat) + 1e-9
        return feat, len(faces), f"face {int(face[2])}x{int(face[3])}px conf {face[14]:.2f}"


def gather(items: list[str]) -> list[Path]:
    out = []
    for it in items:
        p = Path(it)
        if p.is_dir():
            out += sorted(q for q in p.iterdir() if q.suffix.lower() in IMG_EXT and not q.name.startswith("contact"))
        elif p.suffix.lower() in IMG_EXT:
            out.append(p)
    return out


def ref_paths(char: str, explicit: list[str] | None) -> list[Path]:
    if explicit:
        return gather(explicit)
    f = HERE / "characters" / f"{char}_refs.json"
    if f.exists():
        refs = json.loads(f.read_text()).get("refs") or []
        if refs:
            return [Path(r) for r in refs]
    master = OUT / char / "master"
    return gather([str(master)]) if master.exists() else []


def contact_sheet(rows: list[dict], dest: Path, thumb: int = 360):
    cols = min(4, max(1, len(rows)))
    nrows = (len(rows) + cols - 1) // cols
    W, H = cols * thumb, nrows * (thumb + 56)
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    except OSError:
        font = small = ImageFont.load_default()
    for i, r in enumerate(rows):
        x, y = (i % cols) * thumb, (i // cols) * (thumb + 56)
        try:
            im = Image.open(r["file"]).convert("RGB")
            im.thumbnail((thumb, thumb))
            sheet.paste(im, (x + (thumb - im.width) // 2, y + (thumb - im.height) // 2))
        except Exception:
            pass
        col = (60, 200, 90) if r["verdict"] == "PASS" else (230, 70, 60)
        score = "n/a" if r["score"] is None else f"{r['score']:.3f}"
        d.rectangle([x, y + thumb, x + thumb - 1, y + thumb + 55], fill=(36, 36, 36))
        d.text((x + 8, y + thumb + 4), f"{r['verdict']}  id {score}", fill=col, font=font)
        d.text((x + 8, y + thumb + 30), Path(r["file"]).name[:44], fill=(200, 200, 200), font=small)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest, quality=90)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--char", required=True)
    ap.add_argument("--refs", nargs="*", help="reference images (default: locked refs or master set)")
    ap.add_argument("--threshold", type=float, default=0.40)
    ap.add_argument("--approve-to", default=None, help="copy PASS images here (feeds the LoRA dataset)")
    ap.add_argument("--out", default=None, help="folder for qc outputs (default: first input folder)")
    a = ap.parse_args()

    bible = P.load_bible(a.char)
    cands = gather(a.inputs)
    refs = ref_paths(a.char, a.refs)
    if not cands:
        raise SystemExit("[qc] no candidate images found")
    if not refs:
        raise SystemExit("[qc] no reference images: run character.py master first (or pass --refs)")
    fid = FaceID()
    ref_feats = []
    for r in refs:
        f, n, info = fid.embed(r)
        print(f"[qc] ref {r.name}: {info}")
        if f is not None:
            ref_feats.append(f)
    if not ref_feats:
        raise SystemExit("[qc] no face found in any reference image")
    centroid = np.mean(ref_feats, axis=0)
    centroid /= np.linalg.norm(centroid)

    ref_set = {str(Path(r).resolve()) for r in refs}
    rows = []
    for c in cands:
        f, nfaces, info = fid.embed(c)
        if f is None:
            score, worst, verdict = None, None, "FAIL"
        else:
            score = float(np.dot(f, centroid))
            worst = float(min(np.dot(f, rf) for rf in ref_feats))
            verdict = "PASS" if score >= a.threshold else "FAIL"
        is_ref = str(c.resolve()) in ref_set
        rows.append({"file": str(c), "score": score, "min_vs_single_ref": worst, "faces": nfaces,
                     "verdict": verdict, "is_ref": is_ref, "info": info})
        print(f"[qc] {verdict:4}  {'n/a' if score is None else f'{score:.3f}'}  {c.name}  ({info}"
              f"{', REF itself' if is_ref else ''}{', MULTIPLE FACES' if nfaces > 1 else ''})")

    outdir = Path(a.out) if a.out else (Path(a.inputs[0]) if Path(a.inputs[0]).is_dir() else Path(a.inputs[0]).parent)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "qc.json").write_text(json.dumps({"threshold": a.threshold, "refs": [str(r) for r in refs],
                                                "rows": rows}, indent=1))
    with (outdir / "qc.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    contact_sheet(rows, outdir / "contact_sheet.jpg")
    checklist = ["# Fixed-details checklist (human / vision pass)", "",
                 f"Character: {a.char}. An image ships only if the identity score PASSES and every box is ticked.", ""]
    items = P.marks_checklist(bible)
    for r in rows:
        sc = "n/a" if r["score"] is None else f"{r['score']:.3f}"
        checklist.append(f"## {Path(r['file']).name}  (identity {sc}, {r['verdict']})")
        checklist += [f"- [ ] {it}" for it in items]
        checklist.append("")
    (outdir / "CHECKLIST.md").write_text("\n".join(checklist))
    n_pass = sum(r["verdict"] == "PASS" for r in rows)
    print(f"[qc] {n_pass}/{len(rows)} pass at {a.threshold}. Sheet: {outdir/'contact_sheet.jpg'}  "
          f"Checklist: {outdir/'CHECKLIST.md'}")
    if a.approve_to:
        dest = Path(a.approve_to); dest.mkdir(parents=True, exist_ok=True)
        for r in rows:
            if r["verdict"] == "PASS":
                shutil.copy2(r["file"], dest / Path(r["file"]).name)
        print(f"[qc] copied passes to {dest} (still tick CHECKLIST.md before using them)")


if __name__ == "__main__":
    main()
