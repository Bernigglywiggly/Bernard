# WaveSpeed models for a consistent AI persona (read Mon 12 Oct 2026)

Prices come from each model's wavespeed.ai page on 12 Oct 2026. Every page says "documentation prices may be
outdated; the final task charge prevails", so `ws.py` adds a 10% margin and logs the real balance before/after each run.
**Consistency and realism columns are my expectations from vendor claims and general model reputation. None has been
tested on our character yet.** The first paid run (README, step 3) replaces them with measured qc scores.

## 1. API in one table

| Thing | Value |
|---|---|
| Auth | `Authorization: Bearer $WAVESPEED_API_KEY` (key from wavespeed.ai/accesskey) |
| Submit | `POST https://api.wavespeed.ai/api/v3/{model_id}` with JSON. Returns `data.id`, `data.status="created"` |
| Poll | `GET https://api.wavespeed.ai/api/v3/predictions/{id}/result`, at least 2 s apart. Stop on `completed` (read `data.outputs`, a list of URLs) or `failed / cancelled / timeout / deleted` |
| Sync mode | `"enable_sync_mode": true` on some models, 110 s budget. If it returns `status: processing, code 5004`, poll. **Never resubmit** (double charge). Not used by our code |
| Upload | `POST /api/v3/media/upload/binary` (multipart field `file`) → `data.download_url`. Or the 2-step `POST /api/v3/media/uploads` ticket + `PUT`. Max 200 MB. **Uploads kept 7 days** |
| Balance | `GET /api/v3/balance` → `data.balance` (USD). Any key can read it |
| Usage | `POST /api/v3/user/usage_stats` (owner/admin/billing keys only), per model and per day |
| Rate limits | Bronze (new account) 5 predictions/min, 2 concurrent. Silver after any top-up under $1,000: 500/min |
| Trained LoRAs | Kept about 7 days on WaveSpeed. Keep the local copy and re-host it (private Hugging Face repo) |

## 2. Content policy (applies to every model on WaveSpeed)

| Rule (WaveSpeed Acceptable Use Policy) | Our position |
|---|---|
| No nudity, sexual acts or sexually explicit material, real or fictional | SFW only. `prompts.py` refuses nude/explicit/lingerie terms before any call |
| No sexualised minors, incl. AI-generated | Bible age must be 25 to 30. Youthful-coded words refused (teen, schoolgirl, petite-young...) |
| Consent needed for any real face or voice uploaded; no deceptive synthetic media of real people; no impersonation | Invented face only. Celebrity / lookalike / "resembling" terms refused. No real photo is ever uploaded |
| Users 18+; breaches → warnings, rate limits, suspension, termination | Owner's account; keep it clean |
| Provider rules on top: Google (Nano Banana, Veo) safety guidelines; OpenAI (GPT-image) usage policy; Sora 2 rejects input images with human faces | Sora 2 excluded (also deprecated by OpenAI on 24 Sep 2026; WaveSpeed flags it "unstable") |

Each model also has an `enable_safety_checker` toggle. We leave it on where the field is documented.

## 3. Identity-locked image generation (reference images in, new scene out)

| Rank | Model ID | Refs | Consistency (prior) | Realism (prior) | Cost / image | Speed | Notes |
|---|---|---|---|---|---|---|---|
| 1 | `bytedance/seedream-v5.0-flash/edit` | up to 10, free | High | High | **$0.027** flat (1k to 2k) | fast | **Default.** Cheapest per image with 10 refs; no 4:5 confirmed, we use 3:4 |
| 2 | `google/nano-banana-2.1/edit` | up to 14 | High | High | $0.04 1k, $0.06 2k, $0.135 4k, +$0.002/ref | ~20-40 s | **Premium / fixer.** Strong at "keep everything, change only X". Supports 4:5 and 9:16 |
| 3 | `bytedance/seedream-v5.0-pro/edit` | up to 10, +$0.003 each | High | High | $0.045 1k, $0.09 2k | ~26-32 s | Use if flash drifts on small marks |
| 4 | `google/nano-banana-pro/edit` | up to 14 | High | High | $0.14 (1k/2k), $0.24 4k | ~76 s | Hero shots only |
| 5 | `kwaivgi/kling-image-o1` | up to 10 | Vendor claims "stable identity" | Medium-high | $0.028 | ~27 s | Cheap second opinion |
| 6 | `openai/gpt-image-2/edit` | up to 16 | Medium-high | Medium (glossy at low quality) | $0.02 low to $0.23 high (1k); +$0.012/extra ref | ~53 s | OpenAI moderation is the strictest on people |
| 7 | `wavespeed-ai/qwen-image/edit-2511` | up to 3 | Medium | Medium | $0.02 to $0.03 | ~9 s | Fast, few refs |
| - | FLUX Kontext max multi (`wavespeed-ai/flux-kontext-max/multi`) | multi | Medium (2025 generation) | Medium | ~$0.08 | | Superseded by the rows above |

## 4. LoRA route (strongest consistency once trained): **yes, WaveSpeed offers it**

| Step | Model ID | Cost | Time | Notes |
|---|---|---|---|---|
| Train (recommended) | `wavespeed-ai/z-image-lora-trainer` | **$1.25 per 1,000 steps** (2,000 steps = $2.50) | ~12 min at 1k steps | ZIP of images + optional .txt captions. Trigger word is NOT auto-added when captions exist (our `dataset` adds it) |
| Infer | `wavespeed-ai/z-image/turbo-lora` | **$0.01 / image** | ~6 s | Up to 3 LoRAs, `loras: [{"path": url, "scale": 0.9}]`, size up to 1536 px |
| Infer with a pose/composition image | `wavespeed-ai/z-image-turbo/image-to-image-lora` | ~$0.01 (page not read) | | LoRA identity + your layout |
| Alt train | `wavespeed-ai/qwen-image-2512-lora-trainer` | $1 per 1,000 steps | ~20 min | Infer on `wavespeed-ai/qwen-image/text-to-image-2512-lora` (price not read) |
| Alt train | `wavespeed-ai/flux-dev-lora-trainer` (+ `-turbo` $1.25) | from $1 | ~7 min | Infer on `wavespeed-ai/flux-dev-lora` / `flux-krea-dev-lora` (older base) |
| LoRA + reference edit | `wavespeed-ai/qwen-image/edit-2511-lora` | $0.025 | ~9 s | Up to 3 refs + LoRAs (scale 0 to 2). Whether a text-to-image LoRA transfers to this edit model: untested |
| Video LoRA | `wavespeed-ai/wan-2.2-image-lora-trainer` ($3+) → `wavespeed-ai/wan-2.2/i2v-720p-lora` | | | Only if Reels show face drift |

When to switch: when 15 to 25 qc-approved images exist, train once ($2.50 to $5 with one retry), then run the same
shot list both ways and compare qc scores + the checklist. Keep whichever wins. A LoRA makes images 2.7x cheaper
($0.01 vs $0.027) and fixes marks/tattoo placement better in theory, but Z-Image's base realism must be checked.

## 5. Image-to-video for 9:16 Reels

| Rank | Model ID | Cost | Per 5 s | Speed | Notes |
|---|---|---|---|---|---|
| 1 | `kwaivgi/kling-v2.6-std/image-to-video` | $0.21 / 5 s, $0.42 / 10 s | **$0.21** | ~80 s | **Default.** Kling is the reference for human motion; follows input aspect ratio (feed 9:16 stills) |
| 2 | `kwaivgi/kling-v3.0-std/image-to-video` | $0.084/s (sound x1.5) | $0.42 | ~68 s | Hero clips; 3 to 15 s |
| 3 | `wavespeed-ai/minimax-h3/image-to-video` | $0.04/s 480p, $0.06 540p, $0.08 768p, $0.16 1080p | $0.20 to $0.40 | ~82 s | Open-weights H3 hosted by WaveSpeed; follows input aspect; LoRA variant exists |
| 4 | `alibaba/wan-3.0/image-to-video` | $0.05/s 480p, $0.10/s 720p, $0.20/s 1080p | $0.50 (720p) | ~312 s | 2 to 30 s; slow |
| 5 | `google/veo3.1-fast/image-to-video` | $0.10/s no audio, $0.15/s audio | $0.50 | ~109 s | Up to 8 s; Google safety rules |
| 6 | `bytedance/seedance-2.0/image-to-video` | $0.12/s 480p, $0.24/s 720p, $0.60/s 1080p | $1.20 (720p) | ~152 s | 9:16 explicit; premium |
| 7 | `kwaivgi/kling-v3-turbo-std/image-to-video` | $0.112/s | $0.56 | ~105 s | 720p only; no reason to pick over v3.0 std |
| x | `openai/sora-2/image-to-video` | $0.10/s | | | Excluded: rejects faces in input images; deprecated |

Hailuo 2.3: listed on WaveSpeed's site map but I could not read its page or price. Not needed.

## 6. Upscale / skin detail

| Model ID | Cost | Notes |
|---|---|---|
| `wavespeed-ai/seedvr2/image` | $0.01 base (2k/4k/8k; larger may cost more) | Restoration upscaler; **default** final pass |
| `wavespeed-ai/image-upscaler` | $0.01 | Plain upscale |
| `clarity-ai/crystal-upscaler` | $0.05 up to 4 MP, $0.20 up to 16 MP | `creativity` -10..10; keep at 0 or below on faces or it invents a new face |
| `wavespeed-ai/ultimate-image-upscaler` | $0.06 | High-fidelity option |
Instagram shows 1080 px wide, so a 2k output needs no upscale for feed posts. Upscale only for Fanvue/print.

## 7. Recommended stack + monthly cost (backlog of 60 photos + 20 Reels)

```
bible ─▶ anchor (Seedream 5 flash t2i) ─▶ 5 master views (Seedream 5 flash edit) ─▶ qc.py ─▶ pick refs
   └─▶ shoot.py (Seedream flash edit, 4 refs; Nano Banana 2.1 to fix misses) ─▶ qc.py + checklist ─▶ approved
          └─▶ (after 15-25 approved) Z-Image LoRA, A/B vs refs ─▶ keep the winner
                 └─▶ reels.py (Kling 2.6 std, 5 s, 9:16 stills) ─▶ frame sheet ─▶ post with in-app trending audio
```

| Line | Volume (with rejects) | Unit | Month cost |
|---|---|---|---|
| Master set (one-off) | 4 anchor candidates + 5 views x 2 tries = 14 | $0.027 | $0.38 |
| Photos, default model | 60 keepers at ~40% reject, 2 variants → ~150 gens | $0.027 | $4.05 |
| Fixes on Nano Banana 2.1 (2k, 4 refs) | ~30 | $0.068 | $2.04 |
| 9:16 source stills for Reels | 20 keepers → ~30 gens | $0.027 | $0.81 |
| Reels, Kling 2.6 std 5 s | 20 keepers, ~1.5 tries → 30 | $0.21 | $6.30 |
| Hero Reels upgrade, Kling 3.0 std 6 s (5 of the 20) | ~8 | $0.504 | $4.03 |
| LoRA training, once + one retry | 2 x 2,000 steps | $2.50 | $5.00 |
| Upscale (Fanvue/print only) | 20 | $0.01 | $0.20 |
| **Total** | | | **about $23 (≈ £17) per month** |

- That is under a quarter of the $100 budget. The spare $75 is for tests, or for 4x the volume.
- After a winning LoRA, photos drop to $0.01 each: 150 gens = $1.50.
- Cost is not the bottleneck. His approval time is: about 60 to 90 seconds per image to tick the checklist.
- Against THE GOAL: this pipeline makes no money by itself. It removes the content bottleneck in
  `FANVUE_PLAN_8OCT.md` (40 images + 12 clips per batch) for about £17/month, which is below the Higgsfield line
  (£30 to £45) it could replace. Its value depends entirely on posting every day.

## Sources (read 12 Oct 2026)
- API: wavespeed.ai/docs, /docs/submit-task, /docs/get-result, /docs/upload-files-api, /docs/sync-mode,
  /docs/api-authentication, /docs/check-balance, /docs/check-usage; github.com/WaveSpeedAI/wavespeed-python
- Models: wavespeed.ai/models, /models/bytedance/seedream-v5.0-pro/edit, /models/bytedance/seedream-v5.0-flash/edit,
  /models/google/nano-banana-2.1/edit, /models/google/nano-banana-pro/edit, /models/openai/gpt-image-2/edit,
  /models/kwaivgi/kling-image-o1, /models/wavespeed-ai/qwen-image/edit-2511, /models/wavespeed-ai/qwen-image/edit-2511-lora,
  /collections/training-tools, /collections/lora-generation, /models/wavespeed-ai/z-image-lora-trainer,
  /models/wavespeed-ai/z-image/turbo-lora, /models/wavespeed-ai/qwen-image-2512-lora-trainer,
  /models/wavespeed-ai/flux-dev-lora-trainer, /models/wavespeed-ai/wan-2.2-image-lora-trainer, /collections/kling,
  /models/kwaivgi/kling-v2.6-std/image-to-video, /models/kwaivgi/kling-v3.0-std/image-to-video,
  /models/kwaivgi/kling-v3-turbo-std/image-to-video, /models/wavespeed-ai/minimax-h3/image-to-video,
  /models/alibaba/wan-3.0/image-to-video, /models/bytedance/seedance-2.0/image-to-video,
  /models/google/veo3.1-fast/image-to-video, /models/openai/sora-2/image-to-video, /models/wavespeed-ai/seedvr2/image,
  /models/wavespeed-ai/image-upscaler, /models/clarity-ai/crystal-upscaler
- Policy: wavespeed.ai/static/acceptable-use; OpenAI video generation guide (developers.openai.com/docs/guides/video-generation)
- Not read: seedream-v5.0-flash text-to-image page (fields assumed same as edit), z-image-turbo/image-to-image-lora,
  qwen-image/text-to-image-2512-lora prices, Hailuo 2.3. The first paid run confirms or corrects these.
