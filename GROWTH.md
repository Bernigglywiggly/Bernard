# GROWTH: the loop every film goes through (set up 11 Oct 2026, owner: "self-analyse as we progress")

Three stages. Each one writes something down, so the studio learns between sessions.

| Stage | When | What happens | Written to |
|---|---|---|---|
| 1. Pick | Before scripting | Score the idea on the radar: Demand, Gap, Timing, Fit, Effort (/25). Only make ideas scoring 17+, or calendar events we can pre-build | `lab/research/RADAR_<date>.md` (weekly, how-to in `RADAR_HOWTO.md`) |
| 2. Make | Script to upload | CRAFT.md gates (facts file, independent fact-check, lint, stills, critic) plus CRAFT §9 attention rules; 3 thumbnails from `lab/tools/thumbs_v2.py`; Test & Compare on every long film | the film's folder |
| 3. Measure | 48 h and 7 d after publishing, then weekly | Pull analytics (below), compare each video with its channel's median, read the retention curve, write one lesson per film into CRAFT "Learned", feed winners back into the radar | `lab/research/REVIEW_<date>.md`, CRAFT.md |

## The numbers that matter (in this order)
1. **Stayed to watch / swipe-away** (Shorts) and **average view percentage** (long films): did the content hold?
2. **Impressions click-through rate**: did the packaging earn the click? (judge only with Test & Compare running)
3. **Where the retention curve drops**: the exact second and what was on screen; that is the next fix.
4. **Subscribers per 1,000 views** and **returning viewers**: is a channel forming?
Raw views come last: they mostly follow 1-3.

## How to pull analytics (works through the Zapier YouTube connection, read-only)
Zapier tool `execute_zapier_read_action`, selected_api `YouTubeV4CLIAPI`, action `_zap_raw_request`, tool_name
`youtube_make_api_get_request`, params `{"method":"GET","url":"https://youtubeanalytics.googleapis.com/v2/reports",
"querystring":{...},"fail_on_errors":false}` with the channel's `connection_id`:
The Curve `02f9e902-69d2-8a12-af4b-b4f4cd146eeb` · Money Crimes `02ce9a67-dbe7-8998-8da5-26da5fc35e26` ·
How They Profit `02d0de21-a222-85ea-aea9-5b0920dd34b0` · Curva Explica `020e1621-8ed2-8623-aa3a-11cd759b5c3e`.
- Per video: `ids=channel==MINE`, `startDate`, `endDate`, `metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained`, `dimensions=video`, `sort=-views`, `maxResults=50`.
- Retention curve: `metrics=audienceWatchRatio,relativeRetentionPerformance`, `dimensions=elapsedVideoTimeRatio`, `filters=video==<ID>`.
- Traffic sources: `metrics=views`, `dimensions=insightTrafficSourceType`, `filters=video==<ID>`.
- CTR/impressions are NOT in this API: read them in YouTube Studio (owner) or note "not available".
Video ids: `channel/uploads_newlook.done.json`.

## Baseline (11 Oct 2026, The Curve, 1 Sep to 10 Oct)
Top video 46 views (39% average viewed); 4 videos with any views. Every channel is at the very start: the first
lessons will come from retention curves, not view counts.

## Honest frame
YouTube income needs 1,000 subscribers + 4,000 watch hours per channel (see ALIGNMENT_8OCT.md). This loop is how we
get there faster; it does not change that the £2,000/month goal runs mainly through the sales routes.
