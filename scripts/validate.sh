#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import json
from pathlib import Path

plugin = json.loads(Path('.claude-plugin/plugin.json').read_text())
marketplace = json.loads(Path('.claude-plugin/marketplace.json').read_text())
assert plugin['name'] == 'ship'
assert any(p['name'] == 'ship' and p['version'] == plugin['version'] for p in marketplace['plugins'])
assert Path('.agents/skills/ship').is_symlink()
assert Path('.agents/skills/ship').readlink() == Path('../../skills/ship')

skill = Path('skills/ship/SKILL.md').read_text()
assert skill.startswith('---\n') and '\n---\n' in skill[4:]
front = skill.split('---\n', 2)[1]
assert 'name: ship\n' in front and 'description: ' in front
assert len(skill.splitlines()) < 500
print('ok plugin, portable skill, and compatibility link')
PY

python3 -m py_compile evals/run.py evals/activation.py evals/bench_integrity.py evals/hidden/checks.py
python3 evals/bench_integrity.py
echo 'all checks passed'
