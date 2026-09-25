#!/usr/bin/env python3
"""Does the host pick Ship on its own? Claude only (stream-json shows Skill calls).

    python3 evals/activation.py ARM_ROOT [trials]
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
sys.path.insert(0, str(EVALS))
from run import CLAUDE, FIX  # noqa: E402

SAMPLE = "# Ship\n- [ ] invites expire after 7 days — \"expire after 7 days\"\n- [x] pro plan is 15 — proof: `python3 -m unittest` 3 ok\n"


def trial(arm, case):
    wd = Path(tempfile.mkdtemp(prefix="ship-act-"))
    shutil.copytree(EVALS / "seed", wd, dirs_exist_ok=True)
    if case.get("ship_md"):
        (wd / "SHIP.md").write_text(SAMPLE)
    prompt = case["prompt"]
    if prompt.startswith("@"):
        prompt = (FIX / prompt[1:]).read_text()
    cmd = [CLAUDE, "-p", "--model", sys.argv[3] if len(sys.argv) > 3 else "claude-sonnet-5",
            "--setting-sources", "project,local", "--plugin-dir", str(Path(arm).resolve()), "--max-turns", "3",
           "--output-format", "stream-json", "--verbose", "--allowedTools", "Read", "Glob", "Grep", "Skill",
           "--", prompt]
    try:
        out = subprocess.run(cmd, cwd=wd, capture_output=True, text=True, timeout=300).stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    shutil.rmtree(wd, ignore_errors=True)
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = ev.get("message")
        if not isinstance(message, dict):
            continue
        for block in message.get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill" \
                    and "ship" in json.dumps(block.get("input", {})):
                return True
    return False


if __name__ == "__main__":
    arm, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1
    cases = json.loads((EVALS / "activation.json").read_text())
    tp = fp = pos = neg = 0
    from concurrent.futures import ThreadPoolExecutor
    jobs = [c for c in cases for _ in range(n)]
    with ThreadPoolExecutor(6) as ex:
        hits = list(ex.map(lambda c: trial(arm, c), jobs))
    for c, hit in zip(jobs, hits):
        print(f"{'want' if c['want'] else 'skip'} {'HIT ' if hit else 'miss'} {c['prompt'][:70]!r}")
        pos += c["want"]; neg += not c["want"]; tp += hit and c["want"]; fp += hit and not c["want"]
    print(f"activation recall {tp}/{pos}, false activations {fp}/{neg}")
