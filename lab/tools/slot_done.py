#!/usr/bin/env python3
"""Is a Short for this publish slot already uploaded? The guard every scheduled build runs first, so two accounts (or a
re-run) never build or upload the same slot twice. Checks every channel/uploads_*.json manifest against its
uploads_*.done.json (file -> video id). Prints "DONE <file> <video id>" or "OPEN".
Usage: python3 lab/tools/slot_done.py 2026-11-01T17:00:00Z
"""
import glob
import json
import os
import sys

slot = sys.argv[1]
channel = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "channel")
for manifest in sorted(glob.glob(os.path.join(channel, "uploads_*.json"))):
    if manifest.endswith(".done.json"):
        continue
    done_path = manifest[: -len(".json")] + ".done.json"
    if not os.path.exists(done_path):
        continue
    entries = json.load(open(manifest, encoding="utf-8"))
    entries = entries if isinstance(entries, list) else entries.get("items", [])
    done = json.load(open(done_path, encoding="utf-8"))
    for e in entries:
        if e.get("publish_at") == slot and e.get("file") in done:
            print("DONE", e["file"], done[e["file"]])
            sys.exit(0)
print("OPEN")
