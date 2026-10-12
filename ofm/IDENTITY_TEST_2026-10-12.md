# Identity-lock test, persona A1 (12 Oct 2026, overnight)

Reference: `concepts/A1.png` (Higgsfield soul_2 text-only). Sheets: `concepts/a1_set/A1_CONSISTENCY_v1.jpg`, `A1_CONSISTENCY_v2_refedit.jpg` (gitignored).

| Route | Cost each | Same face? | Age held (~40)? | Follows new scene? | Verdict |
|---|---|---|---|---|---|
| Higgsfield soul_2 + 1 image ref | 0.12 credits | **No**: 5 different faces | **No**: drifts to mid-20s | **No**: copies the reference pose and outfit | Style reference only. Never use for identity |
| Nano Banana 2.1 edit, 1 ref, 1k | 1.5 credits (on WaveSpeed ~$0.07) | **Yes** | **Yes**: laugh lines kept | **Yes**: sofa/gaming, London street, bed | **Works.** Use for the identity set |

## What this changes
- Identity set (20-30 images) = reference-edit model from the approved A1 image, not text-only or soul_2.
- In the WaveSpeed pipeline: test Seedream 5.0 Flash Edit ($0.027) against Nano Banana 2.1 Edit (~$0.07) on the same 3 scenes. Keep whichever holds the face; cost difference is ~£2/month at 60 photos.
- Every prompt states the age and "fine laugh lines, natural skin texture": generators pull faces younger.
- After 15-25 approved images: train the LoRA (~$2.50) and compare.
- Higgsfield credits left ~9.6 (used ~6.5 tonight). Further generation should run on WaveSpeed once `ofm/.env` exists.
