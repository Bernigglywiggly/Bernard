# Uploading on autopilot: what's set up, and the steps only you can do

Written 3 Oct 2026. Two routes, and they work together:

| | Route A: Metricool (start today) | Route B: YouTube's own API (start today, live in a few weeks) |
|---|---|---|
| What Claude can do | Schedule shorts and short films to YouTube, TikTok, Instagram and Facebook in one go, and read the analytics back | Upload straight to YouTube with everything set: title, description, tags, thumbnail, playlist, schedule, the AI-content label |
| What it needs from you | A free Metricool account with your channels linked, and the Metricool connector switched on in Claude | A Google Cloud project (about 10 minutes), two values saved in the environment's settings, and Google's audit |
| The catch | The free plan caps scheduled posts (about 20); Metricool fetches each video from a public web link, so files have to be online first | Until Google audits the project, every API upload is **locked as private for good**, with no appeal. The uploader refuses to upload until you say the audit has passed |
| Best for | The daily Shorts on four platforms | The long films (they're too big for the repo's links anyway) |

A plain "API key" can only read public data (search, view counts). Uploading always needs a sign-in (OAuth), which is
what Route B sets up.

---

## Route A: Metricool, about 15 minutes, on your phone
1. Go to **metricool.com**, sign up (free), and make a brand called **The Curve**.
2. In that brand, connect: **YouTube** (the channel's Google account), **TikTok**, **Instagram** (it has to be a
   professional account, Creator or Business, linked to a Facebook Page), and the **Facebook Page**.
3. In **claude.ai → Settings → Connectors**, find **Metricool Social Media Management** and press Connect. Sign in to
   Metricool when asked, and switch it on in the chat or session you're using.
4. Tell Claude: "schedule this week's shorts". Claude picks the best times from your Metricool data and books them.

Notes:
- Metricool takes each video from a public link. The repo is public, so shorts and short films (each under 100 MB) can
  go up there and Claude passes their links. The long films (about 250 MB) are too big for that, so they go through
  Route B, or you upload them in YouTube Studio yourself.
- The house/garage versions of the films are on the other Claude account's machine, so that account's session is the
  one that puts them online.
- Metricool may not have the "AI-generated" switches. Tick YouTube's "altered or synthetic content" in Studio and
  TikTok's "AI-generated content" in the app if a post needs it.

---

## Route B: the YouTube Data API, about 10 minutes, then Google's audit
Do this on a computer if you can (the Google Cloud console is awkward on a phone). Use the Google account that owns
the channel.

1. **Make a project.** Open **console.cloud.google.com** → the project picker at the top → **New project** → name it
   `The Curve uploader` → **Create**, then make sure it's selected.
2. **Switch on the API.** Menu → **APIs & Services → Library** → search **YouTube Data API v3** → **Enable**.
3. **Set up sign-in.** Menu → **Google Auth Platform** (it may be called **OAuth consent screen**) → **Get started**:
   - App name `The Curve uploader`, support email: yours → **Next**.
   - Audience: **External** → **Next** → contact email: yours → agree → **Create**.
   - **Audience** → **Test users** → **Add users** → your Google account's email → **Save**.
   - **Data access** → **Add or remove scopes** → tick or paste `https://www.googleapis.com/auth/youtube` → **Update** → **Save**.
4. **Make the client.** **Clients** → **Create client** → Application type **TVs and Limited Input devices** → name it
   `Claude uploader` → **Create**. Copy the **Client ID** and the **Client secret** straight away: Google may show the
   secret only once.
5. **Save them for Claude** (never paste them in the chat): in the Claude Code session, open the cloud environment menu
   in the title bar → **Edit** → environment variables, and add
   ```
   YT_CLIENT_ID=<the client ID>
   YT_CLIENT_SECRET=<the client secret>
   ```
   Save, then start a new session.
6. **Ask for the audit.** Fill in Google's **YouTube API Services – Audit and Quota Extension Form**
   (support.google.com/youtube/contact/yt_api_form). Prepared answers are below. Google replies by email; it can take
   days to weeks, and it may ask for a short screen recording of the tool working.
7. **When the audit passes:** add `YT_AUDITED=1` to the same environment variables and start a new session.
8. **Sign in (each new session, about 20 seconds):** tell Claude "sign me in to YouTube". Claude shows a code; open
   **google.com/device** on your phone, enter it, pick the channel's account and allow it. While the project is in
   "Testing" the sign-in lasts 7 days; pressing **Publish app** on the Audience page stops that (Google then shows an
   "unverified app" warning on the sign-in page, which is expected for a private tool: **Advanced → Go to…**).

What Claude runs (`lab/tools/youtube_upload.py`):
```
python3 lab/tools/youtube_upload.py signin
python3 lab/tools/youtube_upload.py whoami
python3 lab/tools/youtube_upload.py plan uploads.json --dry-run   # checks every file, title and date first
python3 lab/tools/youtube_upload.py plan uploads.json             # uploads, schedules, sets thumbnails and playlists
```
Every upload goes up private or scheduled (`publishAt`), is marked not made for kids, has YouTube's altered or
synthetic content label set (the AI narrator), and is logged in `uploads.done.json` so nothing goes up twice. Custom
thumbnails need the channel verified by phone once (YouTube Settings → Channel → Feature eligibility).

### Prepared answers for the audit form
- **What does your API client do?** "A private tool that uploads my own channel's videos. It is used only by me, the
  channel owner, from my own computer, to upload and schedule videos I made, with their titles, descriptions,
  thumbnails and playlists. It does not access other users' data, does not download or store YouTube content, and
  has no public users."
- **Who uses it?** "Only me (one Google account, the channel owner)."
- **Which API methods?** "videos.insert, thumbnails.set, playlistItems.insert, channels.list (mine=true)."
- **Does it display YouTube data to users?** "No."
- **Does it store YouTube data?** "Only the IDs of videos I uploaded, so the same file is never uploaded twice."
- **Quota needed:** "The default is enough (a few uploads a day)."
- **Link to the client:** the code is in a public GitHub repository (`lab/tools/youtube_upload.py`); give its link if
  the form asks for one.

---

## Already done for you
- `lab/tools/youtube_upload.py`: sign-in by phone code, resumable uploads that survive a dropped connection, scheduling,
  thumbnails, playlists, the AI-content label, checks on titles (100 characters), descriptions (5,000 bytes) and tags
  (500 characters), and a lock that stops real uploads until the audit has passed. Tested with a dry run here.
- Titles, descriptions with sources, tags and pinned comments for every film: `lab/engine/kit.py` and
  `lab/engine/brand.py` (the cloud account's branch has the newer long-form copy in each film's `POST.md`).
- The status board with an upload tracker: **The Curve HQ** (link in `HANDOFF.md`).
