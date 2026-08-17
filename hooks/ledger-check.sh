#!/usr/bin/env bash
# Prints a one-line reminder when a ship ledger exists in the working directory.
# Silent otherwise, so repos that do not use ship pay zero context cost.
set -uo pipefail

ledger="requirements.md"
[ -f "$ledger" ] || exit 0

# States live in the last column of the ledger table: | R1 | ... | open |
count() {
  grep -cE "\|[[:space:]]*$1[[:space:]]*\|[[:space:]]*$" "$ledger" 2>/dev/null || true
}

open=$(count open)
unclear=$(count unclear)
built=$(count built)
shipped=$(count shipped)

echo "ship: ledger active, ${open:-0} open, ${unclear:-0} unclear, ${built:-0} built, ${shipped:-0} shipped. Absorb this message into requirements.md before responding, then continue the work."
exit 0
