#!/usr/bin/env bash
# Run selected messy-input fixtures through an arm and save the durable state.
#
#   MODEL=claude-opus-5 ./evals/run.sh baseline
#   MODEL=claude-opus-5 ./evals/run.sh ship
#
# Every arm gets a fresh temporary Git repository. The ship arm receives the
# standard skill and a copy of its state validator; the baseline arm does not.
# This is a smoke benchmark, not a claim of model-independent behavior.
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

arm="${1:-}"
case "$arm" in
  baseline|ship) ;;
  *) echo "usage: $0 baseline|ship [fixture-filter]" >&2; exit 1 ;;
esac
filter="${2:-}"

model="${MODEL:-claude-opus-5}"
out="evals/runs/$arm"
skill="skills/ship/SKILL.md"
validator="skills/ship/scripts/ship-state.py"
failures=0
matched=0
mkdir -p "$out"

sys=()
if [ "$arm" = ship ]; then
  sys=(--append-system-prompt "$(cat "$skill")")
fi

prepare() {
  local wd="$1"
  git -C "$wd" init -q
  if [ "$arm" = ship ]; then
    mkdir -p "$wd/scripts"
    cp "$validator" "$wd/scripts/ship-state.py"
    chmod +x "$wd/scripts/ship-state.py"
  fi
}

run() { # run <workdir> <prompt> [session-id]
  local wd="$1" prompt="$2" sid="${3:-}"
  local args=(-p --model "$model" --permission-mode acceptEdits
    --allowedTools "Bash(python3 *)" "Bash(node *)" "Bash(npm *)" "Bash(git *)")
  [ -n "$sid" ] && args+=(--session-id "$sid")
  (cd "$wd" && claude "${args[@]}" ${sys[@]+"${sys[@]}"} "$prompt") 2>&1
}

resume() { # resume <workdir> <session-id> <prompt>
  (cd "$1" && claude -p --model "$model" --permission-mode acceptEdits \
    --allowedTools "Bash(python3 *)" "Bash(node *)" "Bash(npm *)" "Bash(git *)" \
    -r "$2" ${sys[@]+"${sys[@]}"} "$3") 2>&1
}

selected() {
  if [ -z "$filter" ] || [[ "$1" == *"$filter"* ]]; then
    matched=1
    return 0
  fi
  return 1
}

collect() { # collect <workdir> <name> <reply>
  local wd="$1" name="$2"
  rm -rf "${out:?}/$name"
  mkdir -p "$out/$name"
  if [ -f "$wd/SHIP.md" ]; then
    cp "$wd/SHIP.md" "$out/$name/SHIP.md"
    local validation_ok=1
    if ! python3 "$validator" validate "$wd/SHIP.md" >"$out/$name/validation.txt" 2>&1; then
      failures=$((failures + 1))
      validation_ok=0
    fi
    if python3 "$validator" status --short "$wd/SHIP.md" >"$out/$name/status.txt" 2>&1; then
      printf 'exit=0\n' >>"$out/$name/status.txt"
    else
      printf 'exit=1\n' >>"$out/$name/status.txt"
      [ "$validation_ok" -eq 1 ] && failures=$((failures + 1))
    fi
    if python3 "$validator" validate --require-evidence "$wd/SHIP.md" >"$out/$name/evidence.txt" 2>&1; then
      printf 'exit=0\n' >>"$out/$name/evidence.txt"
    else
      printf 'exit=1\n' >>"$out/$name/evidence.txt"
    fi
  else
    printf '(no SHIP.md produced)\n' > "$out/$name/SHIP.md"
    printf '(no state file)\n' > "$out/$name/validation.txt"
    printf 'exit=1\n(no state file)\n' > "$out/$name/status.txt"
    printf 'exit=1\n(no state file)\n' > "$out/$name/evidence.txt"
  fi
  : > "$out/$name/legacy-files.txt"
  for legacy in requirements.md tickets.md; do
    [ -e "$wd/$legacy" ] && printf '%s\n' "$legacy" >> "$out/$name/legacy-files.txt"
  done
  printf '%s\n' "$3" > "$out/$name/reply.txt"
  printf '  saved %s\n' "$out/$name"
}

single_fixtures=(
  01-meeting-transcript
  03-voice-note
  04-no-asks
  06-complaint-plus-features
  07-injection
  08-repeated-corrections
  12-irrelevant-material
  13-many-dumps
)

for fixture in "${single_fixtures[@]}"; do
  selected "$fixture" || continue
  printf '%s · %s\n' "$arm" "$fixture"
  wd=$(mktemp -d)
  prepare "$wd"
  if ! reply=$(run "$wd" "$(cat "evals/fixtures/$fixture.md")"); then
    failures=$((failures + 1))
    reply="[runner] model command failed"
  fi
  collect "$wd" "$fixture" "$reply"
  rm -rf "$wd"
done

if selected "02-whatsapp-thread"; then
  printf '%s · 02-whatsapp-thread (15 turns)\n' "$arm"
  wd=$(mktemp -d)
  prepare "$wd"
  sid=$(python3 -c 'import uuid; print(uuid.uuid4())')
  first=1
  reply=""
  while IFS= read -r line; do
    msg=$(sed -E 's/^[0-9]+\. `[0-9:]+` //' <<<"$line")
    [ -n "$msg" ] || continue
    if [ "$first" = 1 ]; then
      if ! reply=$(run "$wd" "$msg" "$sid"); then
        failures=$((failures + 1))
        reply="[runner] model command failed"
      fi
      first=0
    else
      if ! reply=$(resume "$wd" "$sid" "$msg"); then
        failures=$((failures + 1))
        reply="[runner] model resume failed"
      fi
    fi
    printf '.'
  done < <(grep -E '^[0-9]+\. `' "evals/fixtures/02-whatsapp-thread.md")
  printf '\n'
  collect "$wd" "02-whatsapp-thread" "$reply"
  rm -rf "$wd"
fi

if selected "05-contradicts-shipped"; then
  printf '%s · 05-contradicts-shipped\n' "$arm"
  wd=$(mktemp -d)
  prepare "$wd"
  cp evals/setups/05-SHIP.md "$wd/SHIP.md"
  if ! reply=$(run "$wd" 'ok so the hard stop is a problem. Legal need to be able to push a deal through when there is a signed waiver on file. So there does need to be an override, but it has to be logged, who did it and why. Also the CSV thing is fine but it needs the deal ID column, it is useless for reconciling without it.'); then
    failures=$((failures + 1))
    reply="[runner] model command failed"
  fi
  collect "$wd" "05-contradicts-shipped" "$reply"
  rm -rf "$wd"
fi

if [ "$matched" -eq 0 ]; then
  printf 'no fixture matched filter: %s\n' "$filter" >&2
  exit 2
fi
printf '\ndone · %s\n' "$out"
[ "$failures" -eq 0 ] || exit 1
