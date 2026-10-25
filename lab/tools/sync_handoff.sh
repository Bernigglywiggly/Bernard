#!/bin/bash
# Copy ~/Bernard/HANDOFF.md to every place a new session looks for it (the owner's rule: they must never disagree).
# Usage: bash lab/tools/sync_handoff.sh
set -e
SRC=~/Bernard/HANDOFF.md
for dst in ~/RESUME_HERE_2026-10-05.md ~/youtube/CURRENT_STATE.md ~/CLAUDE_HANDOFF_BUNDLE/HANDOFF.md ~/Downloads/CLAUDE_HANDOFF/HANDOFF.md \
  ~/Downloads/GoldenPlate_Vault/00_RESUME_HERE.md ~/Downloads/GoldenPlate_Vault/00_START_HERE.md \
  ~/Downloads/GoldenPlate_Vault/00_CURRENT_STATE.md ~/Downloads/GoldenPlate_Vault/CURRENT_STATE.md; do
  mkdir -p "$(dirname "$dst")"
  cp "$SRC" "$dst"
done
md5 -q "$SRC" ~/RESUME_HERE_2026-10-05.md ~/youtube/CURRENT_STATE.md ~/CLAUDE_HANDOFF_BUNDLE/HANDOFF.md ~/Downloads/CLAUDE_HANDOFF/HANDOFF.md \
  ~/Downloads/GoldenPlate_Vault/00_RESUME_HERE.md ~/Downloads/GoldenPlate_Vault/00_START_HERE.md ~/Downloads/GoldenPlate_Vault/00_CURRENT_STATE.md \
  ~/Downloads/GoldenPlate_Vault/CURRENT_STATE.md | sort -u | wc -l | awk '{print ($1 == 1) ? "handoff synced: 9 copies identical" : "MISMATCH"}'
