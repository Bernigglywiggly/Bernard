"""Prompt layers shared by character.py / shoot.py / reels.py, plus the safety lint.

Three layers, always in this order:
  1. IDENTITY  - built from the character bible (fixed traits; never varies per shot)
  2. SCENE     - from the shot list (scene, outfit, pose, lighting, camera, mood)
  3. REALISM   - phone/35mm look + "avoid" clauses for AI tells
Edit models on WaveSpeed take no negative_prompt field, so the AI-tell negatives are
written into the prompt as plain "Avoid: ..." text (works on Seedream / Nano Banana / GPT-image).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- safety lint
# SFW only, clearly adult, invented face only. Any hit = hard refusal before spending.
BANNED = [
    # youthful-coded / age-bait
    r"\bteen\w*", r"\bschool ?girl", r"\bschool uniform", r"\bunderage", r"\bminor\b", r"\bloli",
    r"\bchild\w*", r"\bkid\b", r"\bkids\b", r"barely legal", r"just turned", r"\b1[0-9][ -]?(year|yr)s?[ -]?old",
    r"petite[ -]young", r"young[ -]looking", r"\byouthful", r"\bbaby[ -]?face", r"\bjailbait",
    # explicit / nudity
    r"\bnude\b", r"\bnudity", r"\bnaked", r"\btopless", r"\bbottomless", r"\bnipple", r"\bgenital",
    r"\bexplicit", r"\bsex\b", r"\bsexual", r"\bporn", r"\berotic", r"\blingerie", r"see[ -]through",
    r"\bthong\b", r"\bfetish", r"\bnsfw",
    # real-person likeness
    r"\bcelebrit", r"\blook[ -]?alike", r"\bresembl", r"\bdoppelg", r"\bfamous (actress|model|singer|person)",
    r"\bdeepfake", r"\bin the likeness of",
]
_BANNED_RE = [re.compile(p, re.I) for p in BANNED]


def lint(text: str, where: str = "prompt") -> None:
    hits = sorted({m.group(0) for r in _BANNED_RE for m in [r.search(text)] if m})
    if hits:
        raise SystemExit(f"[safety] refused {where}: banned term(s) {hits}. "
                         "SFW only, clearly adult (25-45), invented person only.")


# ---------------------------------------------------------------- character bible

def load_bible(name: str) -> dict:
    p = HERE / "characters" / f"{name}.json"
    bible = json.loads(p.read_text())
    age = int(bible.get("age", 0))
    if not 25 <= age <= 45:
        raise SystemExit(f"[safety] bible age must be 25-45 (got {age}).")
    lint(json.dumps(bible), where=f"bible {p.name}")
    return bible


def identity_text(b: dict, full_body: bool = False) -> str:
    f, h, m = b["face"], b["hair"], b["marks"]
    parts = [
        f"{b['age']}-year-old adult woman, {b['ethnicity_look']}",
        f"face {f['shape']}, {f['eyes']} eyes, {f['brows']}, {f['nose']}, {f['lips']}, {f['skin']}",
        f"{h['colour']} hair, {h['length']}, {h['style']}",
    ]
    parts += [mk["description"] + " " + mk["placement"] for mk in m]
    if full_body:
        parts.append(f"{b['body']['height']}, {b['body']['build']}")
    return "; ".join(parts)


def marks_checklist(b: dict) -> list[str]:
    items = [f"Eye colour: {b['face']['eyes']}", f"Hair: {b['hair']['colour']}, {b['hair']['length']}"]
    items += [f"{mk['name']}: {mk['description']} {mk['placement']}" for mk in b["marks"]]
    items.append(f"Build: {b['body']['build']}")
    items.append(f"Reads clearly as an adult woman of about {b['age']} (no youthful look; reject if she reads under {int(b['age']) - 5})")
    items.append("Hands: five fingers each, no fused/extra fingers; jewellery not warped; no garbled text")
    return items


# ---------------------------------------------------------------- realism layer
REALISM = {
    "phone": ("candid smartphone photo, shot on a recent iPhone main camera, natural available light, "
              "slight lens distortion at the edges, mild noise in shadows, realistic white balance"),
    "35mm": ("35mm film photograph, Portra 400 colour, fine natural grain, soft highlight roll-off, "
             "slightly imperfect focus, real location"),
    "studio": ("professional editorial photo, 85mm lens, softbox key light, plain seamless background, "
               "true-to-life colour, no retouching"),
}
SKIN = ("natural skin texture with visible pores, fine peach fuzz, slight under-eye texture, "
        "tiny natural asymmetries, real hair flyaways")
AVOID = ("Avoid: plastic or airbrushed skin, waxy sheen, over-symmetrical face, beauty-filter look, "
         "extra or fused fingers, warped jewellery, garbled or fake text, duplicated limbs, "
         "HDR glow, oversaturated colours, CGI or 3D-render look, watermark")


def realism_text(look: str = "phone") -> str:
    return f"{REALISM.get(look, REALISM['phone'])}. {SKIN}. {AVOID}."


def identity_lock_clause(n_refs: int) -> str:
    return (f"Keep the exact same woman as in the reference image{'s' if n_refs > 1 else ''}: identical face "
            "shape, eye colour, brows, nose, lips, skin tone, freckles, moles and tattoo positions, and the "
            "same hair colour. Do not beautify or change her identity. Only change what is described below.")


# ---------------------------------------------------------------- payload builders
# Field names per model family, from each wavespeed.ai model page (12 Oct 2026).

def image_payload(model: str, prompt: str, images: list[str] | None, aspect: str = "4:5",
                  resolution: str = "2k", seed: int | None = None, loras: list[dict] | None = None,
                  size: str | None = None) -> dict:
    lint(prompt)
    images = images or []
    if model.startswith("bytedance/seedream"):
        # Seedream: images max 10, aspect_ratio, resolution 1k/1.5k/2k, jpeg|png
        p = {"prompt": prompt, "aspect_ratio": aspect if aspect != "4:5" else "3:4",
             "resolution": resolution if resolution in ("1k", "1.5k", "2k") else "2k",
             "output_format": "jpeg", "enable_safety_checker": True}
        if images:
            p["images"] = images[:10]
    elif model.startswith("google/nano-banana"):
        p = {"prompt": prompt, "aspect_ratio": aspect, "resolution": resolution, "output_format": "jpeg"}
        if images:
            p["images"] = images[:14]
    elif model.startswith("openai/gpt-image"):
        p = {"prompt": prompt, "images": images[:16], "aspect_ratio": aspect,
             "resolution": resolution, "quality": "medium", "output_format": "jpeg"}
    elif model == "kwaivgi/kling-image-o1":
        p = {"prompt": prompt, "images": images[:10], "aspect_ratio": aspect,
             "resolution": "2k" if resolution != "1k" else "1k", "num_images": 1}
    elif model.startswith("wavespeed-ai/qwen-image/edit"):
        p = {"prompt": prompt, "images": images[:3], "size": size or "1024*1280", "output_format": "jpeg"}
        if loras:
            p["loras"] = loras[:3]
    elif model.startswith("wavespeed-ai/z-image") or model.startswith("wavespeed-ai/qwen-image/text-to-image"):
        p = {"prompt": prompt, "size": size or "1088*1360", "output_format": "jpeg",
             "loras": loras or [], "enable_safety_checker": True}
        if images:  # image-to-image-lora variant
            p["image"] = images[0]
    else:
        raise SystemExit(f"no payload builder for {model}")
    if seed is not None and not model.startswith(("google/", "openai/", "bytedance/")):
        p["seed"] = seed
    return p
