# media/: finished files saved for the account switch (5 Oct 2026)

Build folders are gitignored and the cloud container is temporary, so the finished videos that still need uploading
live here. They are the only copies (their voice tracks were in build folders).

- `2026-10-05_youtube/`: the 29 videos not yet uploaded (`channel/uploads.json` minus `channel/uploads.done.json`),
  by channel, each with an `UPLOAD_SHEET.md` (titles, descriptions, tags, schedule, pinned comment) and `manifest.json`
  (index -> original path). Files over 90 MB are split into `.partNN` pieces (GitHub's 100 MB limit). Rebuild them:

      cd media/2026-10-05_youtube && for f in $(ls */*.part00 | sed 's/.part00$//'); do cat "$f".part* > "$f"; done

  To upload with the pipeline instead of by hand, put each file back at its `original` path (manifest.json) and run the
  Zapier resumable upload as in HANDOFF.md (needs the Zapier plan upgraded).
- The walk-in Reels are not here: they rebuild for free from `sales/reels/make_reels.py` (see HANDOFF.md).

Delete this folder in a commit before merging the PR to keep main small.
