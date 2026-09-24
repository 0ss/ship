#!/usr/bin/env bash
# Everything CI checks, runnable locally: ./scripts/validate.sh
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
root=$(pwd)

fail=0
ok() { printf '  \033[32mok\033[0m   %s\n' "$1"; }
bad() { printf '  \033[31mFAIL\033[0m %s\n' "$1"; fail=1; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

head_ "json"
for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json hooks/hooks.json evals/truth/*.json evals/trigger-cases.json; do
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" 2>/dev/null; then
    ok "$f"
  else
    bad "$f is not valid json"
  fi
done

head_ "plugin manifest"
pname=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['name'])")
mnames=$(python3 -c "import json;print(' '.join(p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']))")
[[ " $mnames " == *" $pname "* ]] && ok "plugin.json name '$pname' is listed" || bad "plugin.json name '$pname' missing from marketplace.json"
pver=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json')).get('version',''))")
mver=$(python3 -c "import json;print(json.load(open('.claude-plugin/marketplace.json'))['plugins'][0].get('version',''))")
[ "$pver" = "$mver" ] && ok "version $pver matches in both manifests" || bad "version mismatch: plugin=$pver marketplace=$mver"
[ -f hooks/hooks.json ] && ok "optional Claude hook adapter is present" || bad "hooks/hooks.json missing"
hookdecl=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json')).get('hooks',''))")
[ -z "$hookdecl" ] && ok "manifest leaves auto-discovered hooks alone" || bad "manifest must not redeclare hooks"

head_ "portable skill"
skill=skills/ship/SKILL.md
[ -f "$skill" ] && ok "canonical skill exists" || bad "canonical skill missing"
[ -L .agents/skills/ship ] && [ "$(readlink .agents/skills/ship)" = "../../skills/ship" ] \
  && ok ".agents compatibility path points to canonical skill" \
  || bad ".agents/skills/ship must link to ../../skills/ship"
if python3 - "$skill" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
if not text.startswith("---\n"):
    raise SystemExit("missing YAML frontmatter")
end = text.find("\n---\n", 4)
if end < 0:
    raise SystemExit("unterminated frontmatter")
front = text[4:end]
fields = {}
for line in front.splitlines():
    if not line or line.startswith(" "):
        continue
    key, sep, value = line.partition(":")
    if not sep:
        raise SystemExit(f"malformed frontmatter line: {line}")
    fields[key] = value.strip()
allowed = {"name", "description", "license", "compatibility", "metadata"}
if set(fields) - allowed:
    raise SystemExit(f"non-standard frontmatter fields: {set(fields) - allowed}")
if fields.get("name") != "ship":
    raise SystemExit("name must be ship")
if not re.fullmatch(r"[a-z0-9-]{1,64}", fields.get("name", "")):
    raise SystemExit("name is not kebab-case")
if not 1 <= len(fields.get("description", "")) <= 1024:
    raise SystemExit("description must be 1-1024 characters")
if len(text[end + 5:].splitlines()) >= 500:
    raise SystemExit("skill body must stay under 500 lines")
PY
then ok "frontmatter is portable and within limits"
else bad "portable skill format"
fi
[ -x skills/ship/scripts/ship-state.py ] && ok "state validator is executable" || bad "state validator is not executable"
python3 -m py_compile skills/ship/scripts/ship-state.py && ok "state validator compiles" || bad "state validator does not compile"
! grep -qE 'requirements\.md|tickets\.md' "$skill" && ok "skill names no legacy state files" || bad "skill still references legacy state files"

head_ "state tests"
if python3 -m unittest discover -s tests -p 'test_*.py' >/tmp/ship-tests.out 2>&1; then
  ok "validator unit tests"
else
  cat /tmp/ship-tests.out
  bad "validator unit tests"
fi

head_ "shell"
if command -v shellcheck >/dev/null 2>&1; then
  for s in hooks/*.sh evals/*.sh scripts/*.sh; do
    shellcheck -S warning "$s" >/dev/null 2>&1 && ok "$s" || { shellcheck -S warning "$s"; bad "$s"; }
  done
else
  printf '  skip shellcheck (not installed)\n'
fi
for s in hooks/*.sh evals/*.sh scripts/*.sh; do
  [ -x "$s" ] && ok "$s is executable" || bad "$s is not executable"
done

head_ "hook behaviour"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
out=$(cd "$tmp" && CLAUDE_PLUGIN_ROOT="$root" bash "$root/hooks/ledger-check.sh")
[ -z "$out" ] && ok "silent without SHIP.md" || bad "spoke without SHIP.md: $out"
python3 skills/ship/scripts/ship-state.py init "$tmp/SHIP.md"
out=$(cd "$tmp" && CLAUDE_PLUGIN_ROOT="$root" bash "$root/hooks/ledger-check.sh")
[[ "$out" == *"Ship state active"* ]] && ok "reports existing valid state" || bad "did not report valid state: $out"
printf 'not a ship state\n' > "$tmp/SHIP.md"
out=$(cd "$tmp" && CLAUDE_PLUGIN_ROOT="$root" bash "$root/hooks/ledger-check.sh")
[[ "$out" == *"invalid"* ]] && ok "warns about invalid state" || bad "did not warn about invalid state: $out"

head_ "evals"
for fx in evals/fixtures/*.md; do
  t="evals/truth/$(basename "${fx%.md}").json"
  [ -f "$t" ] && ok "$(basename "$fx") has ground truth" || bad "$(basename "$fx") has no truth file"
done
[ -f evals/setups/05-SHIP.md ] && ok "contradiction setup exists" || bad "contradiction setup missing"
for setup in evals/setups/*.md; do
  python3 skills/ship/scripts/ship-state.py validate "$setup" >/dev/null 2>&1 \
    && ok "$(basename "$setup") is a valid state fixture" \
    || bad "$(basename "$setup") is not a valid state fixture"
done
basis=$(python3 skills/ship/scripts/ship-state.py basis evals/setups/05-SHIP.md W1 2>/dev/null || true)
[[ "$basis" == intent=R1@1#* && "$basis" == *'contract='* ]] \
  && ok "basis command reports intent and contract" \
  || bad "basis command did not report a bound intent and contract"
python3 -m py_compile evals/result-bundle.py 2>/dev/null && ok "result bundle helper compiles" || bad "result bundle helper does not compile"
if python3 evals/result-bundle.py verify --bundle evals/results/2026-09-24-smoke >/dev/null 2>&1; then
  ok "result bundle hashes match"
else
  bad "result bundle hashes do not match"
fi
filter_out=$(mktemp)
if ./evals/run.sh ship definitely-not-a-fixture >"$filter_out" 2>&1; then
  bad "unknown eval filter was accepted"
else
  filter_code=$?
  [ "$filter_code" -eq 2 ] && ok "unknown eval filter fails clearly" || bad "unknown eval filter returned $filter_code"
fi
rm -f "$filter_out"

echo
[ "$fail" -eq 0 ] && { printf '\033[32mall checks passed\033[0m\n'; exit 0; } || { printf '\033[31mvalidation failed\033[0m\n'; exit 1; }
