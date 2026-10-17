# Launch: three channels, every platform, week 1 (5-11 Oct 2026)

The user (3 Oct, night): set the YouTube channels up with every asset and detail, schedule a week of posts that can be
tweaked, review performance and adjust; three channels at a high standard first, ten live by the end of October, all
of them on every social platform with content made for each.

## The three
| Channel | What | Ready now | Kit |
|---|---|---|---|
| **The Curve** | The hidden mechanism behind AI headlines | LF01, LF02, LF03, Season One and Two; 9 Shorts + EP Shorts | `channel/the-curve/brand/` |
| **Money Crimes** | The greatest cons, frauds and heists | Film 01 (Lustig, 14:56), film 02 (Ponzi, 13:27); 14 Shorts | `channel/money-crimes/brand/` |
| **How They Profit** (was The Margin) | How big companies really make money | Films 01 (Delta's miles, 7:40), 02 (McDonald's, 8:01), 03 (Costco) made 4 Oct; 5 Shorts each | `channel/channel2/brand/` |
Each `brand/` folder has the profile picture, YouTube banner, watermark, X and Facebook covers and `SETUP.md` (names,
handles, descriptions, bios for every platform, keywords, upload defaults, playlists).

## Set-up, once (about an hour; only you can do this)
1. **YouTube:** in the Google account you'll use, YouTube > profile > Settings > "Add or manage your channels" > Create a
   channel, once per channel (each becomes a Brand Account you own). Upload the avatar and banner, paste the
   description and keywords from `SETUP.md`, set the upload defaults.
2. **Verify each channel** (youtube.com/verify): one phone number covers two channels a year, so this needs two numbers
   for three channels. Verification unlocks custom thumbnails and videos over 15 minutes.
3. **TikTok, Instagram (switch to a Creator account), Facebook Page, X** for each channel: same name, handle, picture
   and bio from `SETUP.md`. Link the Instagram account to its Facebook Page (needed for scheduling).
4. **Connect for automation** (any order): Zapier > YouTube (each channel; this is how Claude uploads, see the Zapier
   route in `UPLOADING.md`); vidIQ > each channel; Metricool connector in claude.ai, if you want me to schedule across
   TikTok/Instagram/Facebook. Until then the free schedulers do it:
   YouTube Studio (schedule on upload), TikTok's desktop scheduler (up to 10 days ahead), Meta Business Suite
   (Instagram + Facebook).

## The first two weeks (5-18 Oct; times UK)
Go-live page (set-up steps, every channel's art and copy, the running order with links):
https://claude.ai/artifact/SGW5GGULhWhdNZxaBtMNSm. The machine-readable plan is `channel/uploads.json`, written by
`python3 lab/tools/plan_uploads.py` (its SLOTS list is the running order; edit it there and re-run).
- Films at 17:00 UK (noon New York), Shorts at 13:00, a second Short at 20:00 while two How They Profit films' parts
  overlap. British Summer Time ends 25 Oct; the plan converts every slot to UTC.
- **The Curve:** LF01 Mon 5, LF02 Wed 7, LF03 Fri 9, Season One Sun 11, Season Two Wed 14 (the EPs go out only inside the
  seasons, so no near-duplicates); a Short a day: the nine LF Shorts, then standalone EP Shorts (toddler, dinosaur,
  birthday, paper, japan).
- **Money Crimes:** Lustig Tue 6, Ponzi Tue 13; a Short a day: the Eiffel teaser, the six Lustig cuts, the seven Ponzi
  cuts (zarossi, barron and end added 4 Oct).
- **How They Profit:** Banks With Wings Fri 9, The Landlord in the Golden Arches Tue 13, The $65 Membership Fri 16; each
  film's five parts on consecutive days.
Every upload goes up scheduled (private with a publish time), not made for kids, altered or synthetic content: Yes, with
its title, description, tags, thumbnail and playlist. Nothing is locked: anything can be moved in YouTube Studio
before its slot, and if set-up slips the whole block moves together (change the dates in SLOTS).

## Review (what we watch, and what changes it)
- **48 hours after each long film:** click-through rate (aim 4%+; below 3% means swap the title or thumbnail; the three
  thumbnails go in YouTube's Test & Compare) and average view duration (aim 40%+; below 30% means a slower or longer
  opening to fix in the next film).
- **Shorts:** "viewed vs swiped away" (aim 70%+) and average percentage viewed. The top Short each week gets a sequel;
  the weakest format gets dropped.
- **Sunday 11 Oct:** a written review per channel (vidIQ once connected, otherwise screenshots of YouTube Studio's
  Analytics tab) and the week-2 plan: what to double, what to cut, which channel gets the next films.

## To ten channels by 31 October
Week 2-3: What if (3D science, the highest-virality format) and Maps & power (geopolitics on a 3D globe). Week 3-4: the
best two channels in Spanish and Portuguese (same films, new voice, captions and on-screen text), and one new format
from the trend desk. Each new channel goes live only with a week of posts ready, its own look and voice, and the same
review rules. See `AUTOMATION.md` for the limits (phone verification, upload approvals) that pace this.
