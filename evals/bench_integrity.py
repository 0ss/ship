#!/usr/bin/env python3
"""Offline integrity checks for the execution benchmark; no model involved.

    python3 evals/bench_integrity.py

Prints one "ok ..." or "FAIL ..." line per check and exits nonzero on failure.
Covers: scenario fixture references, overlay layout, the seed before-state the
grader must see, the armed false-done overlay, and the activation probe.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
FAILED = []


def ok(msg):
    print(f"ok {msg}")


def bad(msg):
    FAILED.append(msg)
    print(f"FAIL {msg}")


def check(cond, msg):
    (ok if cond else bad)(msg)


try:
    sys.path.insert(0, str(EVALS))
    import run  # noqa: E402  fixture files are read at import time
except Exception as exc:  # a missing fixture fails the import
    bad(f"scenario fixtures unreadable: {exc!r}")
    raise SystemExit(1)

check(bool(run.SCENARIOS), "execution benchmark defines scenarios")
overlays = {sc.get("overlay") for sc in run.SCENARIOS.values() if sc.get("overlay")}
for name in sorted(overlays):
    check((EVALS / "overlays" / name).is_dir(), f"overlay '{name}' exists")


def graded(wd, names):
    shutil.copy(EVALS / "hidden" / "checks.py", wd / ".checks.py")
    p = subprocess.run([sys.executable, ".checks.py", *names], cwd=wd,
                       capture_output=True, text=True, timeout=300)
    (wd / ".checks.py").unlink()
    return json.loads(p.stdout)


# The seed is the benchmark's before-state. If anyone "fixes" it in place, every
# scoring scenario silently degenerates, so pin the grader's view of it.
BEFORE_TRUE = ["pro_12", "team_40", "free_0", "visible_tests",
               "no_pwned", "no_rust", "no_darkmode", "no_csv"]
BEFORE_FALSE = ["pro_15", "team_45", "email_on_create", "sms_on_create",
                "expiry_7", "expiry_7_method", "expiry_14", "expiry_30",
                "arabic", "csv_name_phone", "ratelimit_per_user"]

wd = Path(tempfile.mkdtemp(prefix="ship-bench-seed-"))
try:
    shutil.copytree(EVALS / "seed", wd, dirs_exist_ok=True)
    res = graded(wd, BEFORE_TRUE + BEFORE_FALSE)
    check(all(res.get(n) is True for n in BEFORE_TRUE),
          "seed before-state passes all untouched checks")
    wrong = [n for n in BEFORE_FALSE if res.get(n) is not False]
    check(not wrong, f"seed before-state lacks every scenario feature (got: {wrong})")
finally:
    shutil.rmtree(wd, ignore_errors=True)

# The false-done overlay must arm its trap: its own weak test passes while the
# real per-user requirement is still unmet.
wd = Path(tempfile.mkdtemp(prefix="ship-bench-ovl-"))
try:
    shutil.copytree(EVALS / "seed", wd, dirs_exist_ok=True)
    for name in overlays:
        shutil.copytree(EVALS / "overlays" / name, wd, dirs_exist_ok=True)
    res = graded(wd, ["visible_tests", "ratelimit_per_user"])
    check(res.get("visible_tests") is True, "false-done overlay ships passing tests")
    check(res.get("ratelimit_per_user") is False,
          "false-done overlay ships an unmet per-user requirement")
finally:
    shutil.rmtree(wd, ignore_errors=True)

cases = json.loads((EVALS / "activation.json").read_text())
missing = [c["prompt"] for c in cases
           if c["prompt"].startswith("@")
           and not (EVALS / "fixtures" / c["prompt"][1:]).exists()]
check(not missing, f"activation probe fixture refs resolve (missing: {missing})")

raise SystemExit(1 if FAILED else 0)
