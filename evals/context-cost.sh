#!/usr/bin/env bash
# Measure the recurring catalog cost, activated procedure size, and optional
# Claude session reminder for a skill directory.
#
#   ./evals/context-cost.sh skills
#   ./evals/context-cost.sh ~/.agents/skills
#
# Character counts are exact UTF-8 character counts; the token estimate is the
# deliberately rough chars/4 heuristic, not a provider tokenizer.
set -uo pipefail

[ $# -ge 1 ] || { echo "usage: $0 <skills-dir> [skills-dir...]" >&2; exit 1; }
repo=$(pwd)
validator="$repo/skills/ship/scripts/ship-state.py"
hook="$repo/hooks/ledger-check.sh"

total_chars=0
total_skills=0
printf '%-28s %8s %8s\n' 'skill' 'catalog' 'body'
printf '%-28s %8s %8s\n' '----' '------' '----'

for dir in "$@"; do
  [ -d "$dir" ] || { echo "not a directory: $dir" >&2; continue; }
  while IFS= read -r skill; do
    grep -qE '^disable-model-invocation:[[:space:]]*true' "$skill" && continue
    desc=$(awk '/^description:/{sub(/^description:[[:space:]]*/,""); print; exit}' "$skill")
    [ -n "$desc" ] || continue
    name=$(awk '/^name:/{sub(/^name:[[:space:]]*/,""); print; exit}' "$skill")
    body=$(awk 'BEGIN{front=0} /^---[[:space:]]*$/{front++; next} front>=2{print}' "$skill")
    printf '%-28s %8d %8d\n' "${name:-$(basename "$(dirname "$skill")")}" "${#desc}" "${#body}"
    total_chars=$((total_chars + ${#desc}))
    total_skills=$((total_skills + 1))
  done < <(find -L "$dir" -name SKILL.md -type f | sort)
done

printf '%-28s %8s %8s\n' '------' '------' '------'
printf '%-28s %8d (~%d tokens)\n' "catalog total ($total_skills)" "$total_chars" "$((total_chars / 4))"

if [ -x "$hook" ] && [ -x "$validator" ]; then
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  python3 "$validator" init "$tmp/SHIP.md" >/dev/null
  reminder=$(cd "$tmp" && CLAUDE_PLUGIN_ROOT="$repo" bash "$hook" 2>/dev/null || true)
  printf 'optional Claude SessionStart reminder: %d chars (~%d tokens)\n' "${#reminder}" "$(( ${#reminder} / 4 ))"
fi
