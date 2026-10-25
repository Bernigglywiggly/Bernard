#!/bin/bash
# One heavy job at a time on this Mac, across every Claude account (TEAM.md §3.4): Remotion full renders, Blender
# animations, RIFE. Waits while another account's job holds the lock; clears a lock whose process has died.
# Usage (run it in the background): ACCOUNT=B bash lab/tools/heavy.sh npx remotion render Film-Roadster out.mp4
L=/tmp/bernard_heavy.lock
while ! mkdir "$L" 2>/dev/null; do
  pid=$(cut -d' ' -f1 "$L/who" 2>/dev/null)
  if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then rm -rf "$L"; continue; fi
  echo "waiting: $(cat "$L/who" 2>/dev/null)" >&2
  sleep 30
done
echo "$$ $(date +%H:%M) ${ACCOUNT:-?}: $*" > "$L/who"
trap 'rm -rf "$L"' EXIT INT TERM
"$@"
