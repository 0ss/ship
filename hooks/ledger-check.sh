#!/usr/bin/env bash
# Optional Claude adapter: remind a new session about existing Ship state.
# The portable protocol does not depend on this hook.
set -uo pipefail

state="SHIP.md"
[ -f "$state" ] || exit 0

root="${CLAUDE_PLUGIN_ROOT:-.}"
validator="$root/skills/ship/scripts/ship-state.py"
if ! command -v python3 >/dev/null 2>&1 || [ ! -f "$validator" ]; then
  echo "Ship state exists in SHIP.md. Read it before acting."
  exit 0
fi

if ! python3 "$validator" validate "$state" >/dev/null 2>&1; then
  echo "Ship state exists in SHIP.md but is invalid. Read and repair it before acting."
  exit 0
fi

summary=$(python3 "$validator" status --short "$state" 2>/dev/null || true)
echo "Ship state active (${summary:-read SHIP.md}). Read and update SHIP.md before responding."
