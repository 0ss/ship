#!/usr/bin/env bash
# Everything CI checks, runnable locally: ./scripts/validate.sh
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

fail=0
ok()   { printf '  \033[32mok\033[0m   %s\n' "$1"; }
bad()  { printf '  \033[31mFAIL\033[0m %s\n' "$1"; fail=1; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

head_ "json"
for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json hooks/hooks.json evals/truth/*.json; do
  if python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" 2>/dev/null; then
    ok "$f"
  else
    bad "$f is not valid json"
  fi
done

head_ "plugin manifest"
pname=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['name'])")
mnames=$(python3 -c "import json;print(' '.join(p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']))")
[[ " $mnames " == *" $pname "* ]] && ok "plugin.json name '$pname' is listed in marketplace.json" \
  || bad "plugin.json name '$pname' missing from marketplace.json ($mnames)"

pver=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json')).get('version',''))")
mver=$(python3 -c "import json;print(json.load(open('.claude-plugin/marketplace.json'))['plugins'][0].get('version',''))")
[ "$pver" = "$mver" ] && ok "version $pver matches in both manifests" \
  || bad "version mismatch: plugin.json=$pver marketplace.json=$mver"

# hooks/hooks.json is auto-discovered. Declaring it in the manifest as well
# duplicate-loads it and the whole plugin fails to load.
hookdecl=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json')).get('hooks',''))")
[ -f hooks/hooks.json ] && ok "hooks/hooks.json present for auto-discovery" || bad "hooks/hooks.json missing"
[ -z "$hookdecl" ] && ok "manifest does not redeclare the auto-discovered hooks file" \
  || bad "plugin.json declares hooks='$hookdecl', auto-discovery already loads hooks/hooks.json, this breaks plugin load"

head_ "skills"
# Limits are Anthropic's: name <=64 chars kebab-case with no reserved words,
# description <=1024 chars, body under 500 lines.
while IFS= read -r skill; do
  dir=$(basename "$(dirname "$skill")")
  name=$(awk '/^name:/{sub(/^name:[[:space:]]*/,"");print;exit}' "$skill")
  desc=$(awk '/^description:/{sub(/^description:[[:space:]]*/,"");print;exit}' "$skill")
  lines=$(wc -l < "$skill")

  [ "$name" = "$dir" ] && ok "$dir · name matches directory" || bad "$dir · name '$name' != directory '$dir'"
  [[ "$name" =~ ^[a-z0-9-]{1,64}$ ]] && ok "$dir · name is kebab-case, ${#name}/64 chars" || bad "$dir · name must be lowercase/digits/hyphens, max 64"
  [[ "$name" == *anthropic* || "$name" == *claude* ]] && bad "$dir · name uses a reserved word" || ok "$dir · no reserved words"
  [ -n "$desc" ] && ok "$dir · description present" || bad "$dir · description is empty"
  [ "${#desc}" -le 1024 ] && ok "$dir · description ${#desc}/1024 chars" || bad "$dir · description ${#desc} chars, limit is 1024"
  [ "$lines" -lt 500 ] && ok "$dir · $lines lines, under the 500 limit" || bad "$dir · $lines lines, limit is 500"

  # References must stay one level deep, or Claude reads them partially.
  while IFS= read -r ref; do
    [ -f "$(dirname "$skill")/$ref" ] && ok "$dir · link resolves: $ref" || bad "$dir · broken link: $ref"
  done < <(grep -oE '\]\([a-zA-Z0-9_-]+\.md\)' "$skill" | tr -d '](.)' | sed 's/$/.md/' | sort -u)
done < <(find skills -name SKILL.md | sort)

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
out=$(cd "$tmp" && bash "$OLDPWD/hooks/ledger-check.sh")
[ -z "$out" ] && ok "silent with no ledger (zero context cost)" || bad "spoke with no ledger: $out"

printf '| # | r | s | c | state |\n|---|---|---|---|---|\n| R1 | a | b | T1 | shipped |\n| R2 | c | d | - | open |\n| R3 | e | f | - | unclear |\n' > "$tmp/requirements.md"
out=$(cd "$tmp" && bash "$OLDPWD/hooks/ledger-check.sh")
[[ "$out" == *"1 open"* && "$out" == *"1 unclear"* && "$out" == *"1 shipped"* ]] \
  && ok "counts correctly with a ledger" || bad "wrong counts: $out"

head_ "evals"
for fx in evals/fixtures/*.md; do
  t="evals/truth/$(basename "${fx%.md}").json"
  [ -f "$t" ] && ok "$(basename "$fx") has ground truth" || bad "$(basename "$fx") has no truth/ file"
done

echo
[ "$fail" -eq 0 ] && { printf '\033[32mall checks passed\033[0m\n'; exit 0; } || { printf '\033[31mvalidation failed\033[0m\n'; exit 1; }
