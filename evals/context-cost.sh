#!/usr/bin/env bash
# Measures the idle context cost of a skill collection: the bytes every skill's
# description spends in the system prompt on every turn, before you say anything.
#
#   ./evals/context-cost.sh ../ship/skills
#   ./evals/context-cost.sh ~/.claude/plugins/cache/superpowers/*/skills
#
# Token counts are chars/4, the standard rough estimate. Compare like with like.
set -uo pipefail

[ $# -ge 1 ] || { echo "usage: $0 <skills-dir> [skills-dir...]" >&2; exit 1; }

total_chars=0
total_skills=0

for dir in "$@"; do
  [ -d "$dir" ] || { echo "not a directory: $dir" >&2; continue; }

  while IFS= read -r skill; do
    # Model-invoked skills spend context; user-invoked ones do not.
    grep -qE '^disable-model-invocation:[[:space:]]*true' "$skill" && continue

    desc=$(awk '/^description:/{sub(/^description:[[:space:]]*/,""); print; exit}' "$skill")
    [ -n "$desc" ] || continue

    name=$(awk '/^name:/{sub(/^name:[[:space:]]*/,""); print; exit}' "$skill")
    printf '%6d  %s\n' "${#desc}" "${name:-$(basename "$(dirname "$skill")")}"

    total_chars=$((total_chars + ${#desc}))
    total_skills=$((total_skills + 1))
  done < <(find "$dir" -name SKILL.md -type f | sort)
done

echo "------"
printf '%6d  chars across %d always-loaded descriptions (~%d tokens)\n' \
  "$total_chars" "$total_skills" "$((total_chars / 4))"
