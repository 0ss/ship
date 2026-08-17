#!/usr/bin/env bash
# Runs the fixtures through one arm and saves whatever each run produced.
#
#   ./evals/run.sh baseline     # no skill
#   ./evals/run.sh ship         # SKILL.md appended to the system prompt
#
# Each run happens in a fresh empty git repo, so no project CLAUDE.md or
# existing code leaks in. The only difference between arms is the skill.
#
# NOT clean-room: user-level hooks and settings still apply, because --bare
# requires ANTHROPIC_API_KEY and most users are on OAuth. Both arms inherit the
# same environment, so the comparison holds, but absolute numbers are only
# comparable within one machine. Set ANTHROPIC_API_KEY and add --bare for a
# clean-room run. Output lands in evals/runs/<arm>/.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

arm="${1:-}"
[ "$arm" = baseline ] || [ "$arm" = ship ] || { echo "usage: $0 baseline|ship" >&2; exit 1; }

model="${MODEL:-claude-opus-5}"
out="evals/runs/$arm"
mkdir -p "$out"

sys=()
[ "$arm" = ship ] && sys=(--append-system-prompt "$(cat skills/ship/SKILL.md)")

run() { # run <workdir> <prompt> [session-id]
  local wd="$1" prompt="$2" sid="${3:-}"
  local args=(-p --model "$model" --permission-mode acceptEdits)
  [ -n "$sid" ] && args+=(--session-id "$sid")
  (cd "$wd" && claude "${args[@]}" ${sys[@]+"${sys[@]}"} "$prompt") 2>&1
}

resume() { # resume <workdir> <session-id> <prompt>
  (cd "$1" && claude -p --model "$model" --permission-mode acceptEdits \
    -r "$2" ${sys[@]+"${sys[@]}"} "$3") 2>&1
}

collect() { # collect <workdir> <name> <transcript>
  local wd="$1" name="$2"
  mkdir -p "$out/$name"
  cp "$wd/requirements.md" "$out/$name/requirements.md" 2>/dev/null || \
    echo "(no requirements.md produced)" > "$out/$name/requirements.md"
  cp "$wd/tickets.md" "$out/$name/tickets.md" 2>/dev/null || true
  printf '%s\n' "$3" > "$out/$name/reply.txt"
  echo "  saved $out/$name"
}

# --- single-paste fixtures -------------------------------------------------
for f in 01-meeting-transcript 03-voice-note 04-no-asks 06-complaint-plus-features; do
  echo "$arm · $f"
  wd=$(mktemp -d); git -C "$wd" init -q
  reply=$(run "$wd" "$(cat "evals/fixtures/$f.md")")
  collect "$wd" "$f" "$reply"
  rm -rf "$wd"
done

# --- accretion: 15 separate turns in one session ---------------------------
echo "$arm · 02-whatsapp-thread (15 turns)"
wd=$(mktemp -d); git -C "$wd" init -q
sid=$(uuidgen | tr 'A-Z' 'a-z')
first=1; reply=""
while IFS= read -r line; do
  msg=$(sed -E 's/^[0-9]+\. `[0-9:]+` //' <<<"$line")
  [ -n "$msg" ] || continue
  if [ "$first" = 1 ]; then reply=$(run "$wd" "$msg" "$sid"); first=0
  else reply=$(resume "$wd" "$sid" "$msg"); fi
  printf '.'
done < <(grep -E '^[0-9]+\. `' "evals/fixtures/02-whatsapp-thread.md")
echo
collect "$wd" "02-whatsapp-thread" "$reply"
rm -rf "$wd"

# --- reversal arriving after code shipped ----------------------------------
echo "$arm · 05-contradicts-shipped"
wd=$(mktemp -d); git -C "$wd" init -q
cat > "$wd/requirements.md" <<'EOF'
# Requirements

| # | requirement | source | covers | state |
|---|---|---|---|---|
| R1 | screener hard-stops before diligence spend, no override | meeting | T1 | shipped |
| R2 | deals table sortable by date and amount | meeting | T2 | shipped |
| R3 | CSV export of the whole filtered set | meeting | T3 | shipped |
EOF
reply=$(run "$wd" "ok so the hard stop is a problem. Legal need to be able to push a deal through when there's a signed waiver on file. So there does need to be an override, but it has to be logged, who did it and why. Also the CSV thing is fine but it needs the deal ID column, it's useless for reconciling without it.")
collect "$wd" "05-contradicts-shipped" "$reply"
rm -rf "$wd"

echo
echo "done · $out"
