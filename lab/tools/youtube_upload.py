"""YouTube uploads for The Curve (and the other channels) through the YouTube Data API v3, so Claude can upload and
schedule from a cloud session. Plain `requests`, no Google libraries.

One-time setup (UPLOADING.md has every click): a Google Cloud project with the YouTube Data API v3 switched on, an
OAuth client of type "TVs and Limited Input devices", and its id and secret saved in the cloud environment's settings
as YT_CLIENT_ID and YT_CLIENT_SECRET (never in the chat or the repo). Sign-in is a short code typed at
google.com/device on a phone, so nothing has to run on a computer.

Google's rule for projects it hasn't audited: every video uploaded through them is locked as private for good, with no
appeal, whatever privacy is asked for. So `upload` refuses to send anything until the project has passed Google's audit
(set YT_AUDITED=1 in the environment once it has), unless --test is given for a throwaway private test.

    python3 lab/tools/youtube_upload.py signin           # prints a code: enter it at google.com/device
    python3 lab/tools/youtube_upload.py whoami           # which channel the sign-in can upload to
    python3 lab/tools/youtube_upload.py upload FILE --title "..." --description-file d.txt --tags ai,explained \
        [--publish-at 2026-10-05T17:00:00Z] [--thumbnail t.jpg] [--playlist PLxxxx] [--category 27] [--dry-run]
    python3 lab/tools/youtube_upload.py plan uploads.json [--dry-run]   # many at once (format below)

uploads.json: a list of {"file", "title", "description" or "description_file", "tags": [...], "publish_at",
"thumbnail", "playlist", "category", "made_for_kids": false, "synthetic": true}. Paths are relative to the JSON file.
Each finished upload is recorded in uploads.done.json beside it, so a re-run skips what's already up.
"""
import argparse
import datetime
import json
import mimetypes
import os
import stat
import sys
import time

import requests

SCOPE = "https://www.googleapis.com/auth/youtube"            # the device flow's upload-capable scope
DEVICE_URL = "https://oauth2.googleapis.com/device/code"
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
TOKEN_FILE = os.environ.get("YT_TOKEN_FILE", os.path.expanduser("~/.config/thecurve/youtube.json"))
CHUNK = 8 * 1024 * 1024                                       # a multiple of 256 KiB, as resumable uploads require


class Fail(SystemExit):
    pass


def client():
    cid, secret = os.environ.get("YT_CLIENT_ID", ""), os.environ.get("YT_CLIENT_SECRET", "")
    if not cid or not secret:
        raise Fail("YT_CLIENT_ID and YT_CLIENT_SECRET aren't set in this environment. Add them in the cloud environment's "
                   "settings (see UPLOADING.md), then start a new session.")
    return cid, secret


# ---------------------------------------------------------------- sign-in (device flow) and tokens
def save_token(tok):
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(tok, f)
    os.chmod(TOKEN_FILE, stat.S_IRUSR | stat.S_IWUSR)


def signin():
    cid, secret = client()
    r = requests.post(DEVICE_URL, data={"client_id": cid, "scope": SCOPE}, timeout=30)
    d = r.json()
    if r.status_code != 200:
        raise Fail(f"Google refused the sign-in request: {d.get('error')} {d.get('error_description', '')}".strip())
    print(f"On your phone, open {d['verification_url']} and enter the code:  {d['user_code']}", flush=True)
    print(f"(the code works for {d['expires_in'] // 60} minutes; this waits for you)", flush=True)
    wait, deadline = d.get("interval", 5), time.time() + d["expires_in"]
    while time.time() < deadline:
        time.sleep(wait)
        t = requests.post(TOKEN_URL, data={"client_id": cid, "client_secret": secret, "device_code": d["device_code"],
                                           "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}, timeout=30).json()
        err = t.get("error")
        if err == "authorization_pending":
            continue
        if err == "slow_down":
            wait += 5
            continue
        if err:
            raise Fail(f"Sign-in stopped: {err} {t.get('error_description', '')}".strip())
        t["obtained_at"] = time.time()
        save_token(t)
        print("Signed in. The sign-in is kept on this machine only (not in the repo).")
        return whoami()
    raise Fail("The code expired before it was entered. Run signin again.")


def access_token():
    if not os.path.exists(TOKEN_FILE):
        raise Fail("Not signed in on this machine yet: run `signin` first.")
    tok = json.load(open(TOKEN_FILE))
    if time.time() < tok.get("obtained_at", 0) + tok.get("expires_in", 0) - 120:
        return tok["access_token"]
    cid, secret = client()
    t = requests.post(TOKEN_URL, data={"client_id": cid, "client_secret": secret, "refresh_token": tok["refresh_token"],
                                       "grant_type": "refresh_token"}, timeout=30).json()
    if "access_token" not in t:
        raise Fail(f"The saved sign-in no longer works ({t.get('error')}): run `signin` again.")
    tok.update(access_token=t["access_token"], expires_in=t.get("expires_in", 3600), obtained_at=time.time())
    save_token(tok)
    return tok["access_token"]


def auth():
    return {"Authorization": "Bearer " + access_token()}


def whoami():
    r = requests.get(f"{API}/channels", params={"part": "snippet,status", "mine": "true"}, headers=auth(), timeout=30)
    r.raise_for_status()
    items = r.json().get("items", [])
    if not items:
        raise Fail("This Google account has no YouTube channel yet: create the channel first, then sign in again.")
    for ch in items:
        print(f"Channel: {ch['snippet']['title']}  (id {ch['id']})")
    return items


# ---------------------------------------------------------------- one upload
def body_for(e):
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": bool(e.get("made_for_kids", False)),
              "containsSyntheticMedia": bool(e.get("synthetic", True)), "embeddable": True, "license": "youtube"}
    if e.get("publish_at"):
        when = datetime.datetime.fromisoformat(e["publish_at"].replace("Z", "+00:00"))
        if when.tzinfo is None:
            raise Fail(f"publish_at needs a time zone, e.g. 2026-10-05T17:00:00Z: {e['publish_at']!r}")
        if when <= datetime.datetime.now(datetime.timezone.utc):
            raise Fail(f"publish_at is in the past: {e['publish_at']}")
        status["publishAt"] = when.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    elif e.get("public"):
        status["privacyStatus"] = "public"
    title = e["title"].strip()
    if not 0 < len(title) <= 100:
        raise Fail(f"YouTube titles are 1-100 characters; this one is {len(title)}: {title!r}")
    desc = e.get("description", "")
    if len(desc.encode()) > 5000:
        raise Fail(f"YouTube descriptions are at most 5,000 bytes; {title!r} has {len(desc.encode())}")
    tags = [t.strip() for t in e.get("tags", []) if t.strip()]
    if len(",".join(tags)) > 500:
        raise Fail(f"Tags for {title!r} add up to more than 500 characters")
    return {"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": str(e.get("category", 27)),
                        "defaultLanguage": "en", "defaultAudioLanguage": "en"},
            "status": status}


def upload_file(path, body):
    size = os.path.getsize(path)
    kind = mimetypes.guess_type(path)[0] or "video/mp4"
    r = requests.post(f"{UPLOAD}/videos", params={"uploadType": "resumable", "part": "snippet,status"},
                      headers={**auth(), "Content-Type": "application/json; charset=UTF-8",
                               "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": kind},
                      data=json.dumps(body), timeout=60)
    if r.status_code != 200:
        raise Fail(f"YouTube refused the upload: {r.status_code} {r.text[:400]}")
    session, sent, tries = r.headers["Location"], 0, 0
    with open(path, "rb") as f:
        while sent < size:
            f.seek(sent)
            chunk = f.read(CHUNK)
            end = sent + len(chunk) - 1
            try:
                p = requests.put(session, headers={**auth(), "Content-Length": str(len(chunk)),
                                                   "Content-Range": f"bytes {sent}-{end}/{size}"}, data=chunk, timeout=300)
            except requests.RequestException:
                p = None
            if p is not None and p.status_code in (200, 201):
                return p.json()
            if p is not None and p.status_code == 308:
                rng = p.headers.get("Range")
                sent = int(rng.split("-")[1]) + 1 if rng else 0
                tries = 0
                print(f"  {sent * 100 // size}%", flush=True)
                continue
            tries += 1                                        # a dropped connection or a 5xx: ask where it got to
            if tries > 6 or (p is not None and p.status_code < 500):
                raise Fail(f"Upload failed: {p.status_code if p is not None else 'no response'} "
                           f"{p.text[:400] if p is not None else ''}")
            time.sleep(min(60, 2 ** tries))
            q = requests.put(session, headers={**auth(), "Content-Range": f"bytes */{size}"}, timeout=60)
            if q.status_code in (200, 201):
                return q.json()
            rng = q.headers.get("Range")
            sent = int(rng.split("-")[1]) + 1 if rng else 0
    raise Fail("Upload ended without YouTube confirming the video")


def set_thumbnail(video_id, path):
    with open(path, "rb") as f:
        r = requests.post(f"{UPLOAD}/thumbnails/set", params={"videoId": video_id},
                          headers={**auth(), "Content-Type": mimetypes.guess_type(path)[0] or "image/jpeg"}, data=f.read(),
                          timeout=120)
    if r.status_code != 200:
        print(f"  thumbnail not set ({r.status_code}): custom thumbnails need the channel verified by phone once "
              f"(YouTube Settings > Channel > Feature eligibility). {r.text[:200]}")
        return False
    return True


def add_to_playlist(video_id, playlist):
    r = requests.post(f"{API}/playlistItems", params={"part": "snippet"}, headers=auth(), timeout=60,
                      json={"snippet": {"playlistId": playlist, "resourceId": {"kind": "youtube#video", "videoId": video_id}}})
    if r.status_code != 200:
        print(f"  not added to playlist {playlist} ({r.status_code}): {r.text[:200]}")


def entry_from(e, base):
    e = dict(e)
    e["file"] = os.path.join(base, e["file"])
    if e.get("description_file"):
        e["description"] = open(os.path.join(base, e["description_file"]), encoding="utf-8").read().strip()
    if e.get("thumbnail"):
        e["thumbnail"] = os.path.join(base, e["thumbnail"])
    if not os.path.exists(e["file"]):
        raise Fail(f"Missing video file: {e['file']}")
    if e.get("thumbnail") and not os.path.exists(e["thumbnail"]):
        raise Fail(f"Missing thumbnail: {e['thumbnail']}")
    return e


def guard(test):
    if os.environ.get("YT_AUDITED") == "1" or test:
        return
    raise Fail("Not uploading: until Google audits this API project, every upload is locked as private for good. "
               "Set YT_AUDITED=1 in the environment once the audit has passed, or pass --test for a private test upload.")


def do_upload(e, dry, test):
    body = body_for(e)
    mb = os.path.getsize(e["file"]) / 1e6
    when = body["status"].get("publishAt", body["status"]["privacyStatus"])
    print(f"{e['title']}  [{mb:.1f} MB, {when}, synthetic={body['status']['containsSyntheticMedia']}]", flush=True)
    if dry:
        return None
    guard(test)
    v = upload_file(e["file"], body)
    vid = v["id"]
    print(f"  uploaded: https://youtu.be/{vid}", flush=True)
    if e.get("thumbnail"):
        set_thumbnail(vid, e["thumbnail"])
    if e.get("playlist"):
        add_to_playlist(vid, e["playlist"])
    return vid


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("signin")
    sub.add_parser("whoami")
    u = sub.add_parser("upload")
    u.add_argument("file")
    u.add_argument("--title", required=True)
    u.add_argument("--description-file")
    u.add_argument("--description", default="")
    u.add_argument("--tags", default="")
    u.add_argument("--publish-at")
    u.add_argument("--public", action="store_true", help="publish straight away (default: private, or scheduled)")
    u.add_argument("--thumbnail")
    u.add_argument("--playlist")
    u.add_argument("--category", default=27, type=int, help="27 = Education, 28 = Science & Technology")
    u.add_argument("--made-for-kids", action="store_true")
    u.add_argument("--not-synthetic", action="store_true", help="only if no AI voice or AI pictures are used")
    u.add_argument("--dry-run", action="store_true")
    u.add_argument("--test", action="store_true", help="allow a private test upload before the audit")
    p = sub.add_parser("plan")
    p.add_argument("manifest")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--test", action="store_true")
    a = ap.parse_args()
    try:
        if a.cmd == "signin":
            signin()
        elif a.cmd == "whoami":
            whoami()
        elif a.cmd == "upload":
            e = {"file": a.file, "title": a.title, "tags": a.tags.split(",") if a.tags else [], "publish_at": a.publish_at,
                 "public": a.public, "thumbnail": a.thumbnail, "playlist": a.playlist, "category": a.category,
                 "made_for_kids": a.made_for_kids, "synthetic": not a.not_synthetic,
                 "description": open(a.description_file, encoding="utf-8").read().strip() if a.description_file else a.description}
            do_upload(entry_from(e, "."), a.dry_run, a.test)
        elif a.cmd == "plan":
            base = os.path.dirname(os.path.abspath(a.manifest))
            done_path = os.path.splitext(a.manifest)[0] + ".done.json"
            done = json.load(open(done_path)) if os.path.exists(done_path) else {}
            entries = [entry_from(e, base) for e in json.load(open(a.manifest))]    # check every file before uploading any
            for e in entries:
                key = os.path.relpath(e["file"], base)
                if key in done:
                    print(f"{e['title']}: already up (https://youtu.be/{done[key]})")
                    continue
                vid = do_upload(e, a.dry_run, a.test)
                if vid:
                    done[key] = vid
                    json.dump(done, open(done_path, "w"), indent=1)
    except requests.HTTPError as err:
        raise Fail(f"YouTube said: {err.response.status_code} {err.response.text[:400]}")


if __name__ == "__main__":
    main()
