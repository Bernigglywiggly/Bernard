# Automation and scale: toward 50 channels by 1 Feb 2027

Written 3 Oct 2026 (cloud account). The user: "setup everything needed api, mcp, connectors to be able fully automate
creation, analysis, critique, upload and review ... by febuary rule changes i want 50 channels live ... at that scale,
due to volume, revenue share doesnt acc have to be that much due to multiplication factor".

## The limits that shape the plan (checked 3 Oct 2026)
1. **Factory networks get terminated, not just demonetised.** In January 2026 YouTube terminated 16 channels (4.7 billion
   views, about $10M a year) that uploaded hundreds of near-identical AI videos in bulk
   ([OutlierKit](https://outlierkit.com/resources/youtube-ai-slop-crackdown-2026/)). YouTube still welcomes AI-assisted
   storytelling; the line is mass-produced, low-effort content with no human creative input. Channels under one owner
   are linked, so one network-level strike can take several down. **So every channel needs its own format, research
   angle, look, voice and music, a human-approved upload, and no near-duplicate videos** (see `channel/CHANNELS.md`).
2. **Phone verification: one number verifies two channels a year**
   ([YouTube Help](https://support.google.com/youtube/answer/171664?hl=en)). Custom thumbnails and videos over 15 minutes
   need it, so 50 channels need about 25 numbers, or a slower roll-out.
3. **Uploads by API:** since June 2026 uploads have their own quota, 100 a day per Google Cloud project
   ([OutlierKit](https://outlierkit.com/resources/youtube-api-quota/)), so quota is not the limit; Google's audit is.
   Until the project is audited, every API upload is locked as private (see `UPLOADING.md`).
4. **Monetisation is per channel:** 1,000 subscribers + 4,000 watch hours (or 10M Shorts views in 90 days) before 1 Feb
   2027, double after. Spreading the same output over 50 young channels makes each one less likely to get there; the
   watch-hour push should go to the strongest few first.
5. **Cost per film (Higgsfield, measured):** GPT Image 2.5 still 1 credit, Kling 3.0 Pro 5 s clip 7.5, Seed Audio about
   6 per chapter take. A 12-minute Curve film is about 120 credits (LF03: 11 takes, 32 stills, 2 clips); the Lustig
   documentary was about 320. Rendering is about 45 minutes a film on a 4-CPU cloud session.
   50 channels x 2 long films a week = 100 films = about 12,000 credits and 75 render-hours a week.

## Recommended route to 50 (multiplication with the least risk)
| Phase | When | Channels | What |
|---|---|---|---|
| 1. Prove | Oct | 5 | The Curve, Money crimes, What if, Maps & power, The Margin at full quality: 2-3 long films a week each, Shorts daily. Gate: click-through >= 4%, average view duration >= 40%. |
| 2. Translate the winners | Nov | +15-25 | Each proven film in Spanish, Portuguese, Hindi, German, French (and more): a Seed Audio or ElevenLabs voice per language, translated captions and on-screen text. Safest: YouTube's multi-language audio tracks on the same video (one channel, more audiences). More channels: a localised channel per language, which multiplies channels but risks looking like copies across channels. |
| 3. New formats | Dec-Jan | +15-20 | New formats from the trend desk and the bench in `channel/CHANNELS.md` (AI for small business, How it's built, crime psychology, ...), each with its own look, voice and music. Cut any channel that misses the gate after six weeks. |
Roughly 8-10 formats x 5-6 languages = 50 channels, on a production cost of about 10 originals a week plus
translations (a translated film reuses every picture, so it costs a voice and captions, not 120 credits).

## The pipeline: every stage, its tool, and what's missing
| Stage | Tool | Status |
|---|---|---|
| Ideas | Trend desk routine (daily 05:49 UTC, cloud account); vidIQ outliers, keywords and trending | Live |
| Research and script | Claude + web search; sources kept in each script's docstring | Live |
| Critique before render | Claude fact-check pass; vidIQ `score_title`, `score_thumbnail`; Higgsfield `virality_predictor` | Tools connected; not yet a routine |
| Voice | Higgsfield Seed Audio presets (any language); ElevenLabs | Seed Audio live; ElevenLabs needs `ELEVENLABS_API_KEY` |
| Pictures and motion | Higgsfield (GPT Image, Kling, Veo), `lab/curvelf`, `lab/longform`, Remotion (`lab/motion`) | Live |
| Music and sound | Synthesised beds (`lab/music/beds.py`), Kevin MacLeod jazz with credits, `lab/sfx` | Live |
| Render and QC | Cloud sessions; contact sheets, loudness checks, Claude review | Live; one film at a time per session |
| Upload: YouTube | A: Zapier's YouTube app (already Google-verified: public uploads at once; one Zapier task per upload). B: `lab/tools/youtube_upload.py` with your own Google Cloud project (needs `YT_CLIENT_ID`, `YT_CLIENT_SECRET` and the audit) | Zapier connected, no YouTube account linked yet; B not set up |
| Upload: Shorts on TikTok, Instagram, Facebook | Metricool connector (in the directory, not installed); Higgsfield's TikTok publishing | Not set up |
| Analytics and review | vidIQ (channel analytics, comments, earnings); YouTube Analytics API (same sign-in as B); a weekly review routine | vidIQ connected with no channel linked |
| Optimise | vidIQ `update_video`, `update_video_thumbnail`; YouTube Test & Compare | Needs channels linked |

## What only you can do (in this order)
1. **Channels:** create each channel as a Brand Account under your Google account, verify it by phone (two channels per
   number a year), and link one AdSense account to all of them when they qualify.
2. **Zapier:** in Zapier, connect YouTube (one connection per channel). Then I can upload from a session with the
   title, description, thumbnail, playlist and the AI label. Zapier's free plan has 100 tasks a month; volume needs a
   paid plan.
3. **vidIQ:** connect each channel (vidIQ currently has no YouTube channel linked), so analytics and review can run.
4. **Metricool:** claude.ai > Settings > Connectors > "Metricool Social Media Management", with each brand's TikTok,
   Instagram and Facebook linked (steps in `UPLOADING.md`, route A).
5. **Own API (cheaper at volume):** Google Cloud project + OAuth client (steps in `UPLOADING.md`, route B). Put the two
   values in the cloud environment's settings (the environment menu in the session title bar > Edit) as `YT_CLIENT_ID`
   and `YT_CLIENT_SECRET`, then apply for the audit. Never paste keys into the chat or the repo (the repo is public).
6. **Optional:** `ELEVENLABS_API_KEY` in the same settings, for ElevenLabs voices.
7. **Budget:** about 120 credits per original long film, about 6-10 per translated one; plan the Higgsfield top-ups.

## What gets automated once those exist
- `channel/registry.json`: one entry per channel (format, language, voice, look, music, upload slots, gates).
- Routines (each fires a fresh session): daily production per channel from its queue; a daily upload slot per channel
  (Zapier or the API), held for your approval at first; Shorts to Metricool; a weekly review per channel (vidIQ +
  YouTube Analytics) that rewrites its next topics and flags channels to cut or double.
- Uploads stay human-approved until a channel has a track record: the inauthentic-content line is "no human creative
  input", and an approval step is the cheapest insurance.
