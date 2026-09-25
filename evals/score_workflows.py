#!/usr/bin/env python3
"""Summarize objective outcomes; inspect raw artifacts for semantic recall."""
import argparse
import json
from pathlib import Path

HEADINGS = ("## Problem Statement", "## Solution", "## User Stories",
            "## Implementation Decisions", "## Testing Decisions", "## Out of Scope", "## Further Notes")


def passed(value):
    return value.get("passed") is True if isinstance(value, dict) else value is True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    args = parser.parse_args()
    rows = {}
    for path in args.results.rglob("result.json"):
        result = json.loads(path.read_text())
        model, arm, scenario = (result[key] for key in ("model", "arm", "scenario"))
        final = result["log"][-1]
        checks = result["checks"]
        code_ok = all(passed(value) for value in checks.values())
        issue = final["issues"]
        label = "needs-triage" if arm == "to-prd" else "ready-for-agent"
        native_issue = len(issue) == 1 and all(
            f"Label: {label}" in body and all(h in body for h in HEADINGS)
            for body in issue.values())
        state = final["state"] or ""
        rows.setdefault((model, arm), []).append((scenario, code_ok, native_issue,
                                                   len(state.encode())))
    for (model, arm), results in sorted(rows.items()):
        print(f"{model:17} {arm:8} runs={len(results):2} "
              f"code={sum(r[1] for r in results)}/{len(results)} "
              f"issues={sum(r[2] for r in results) if arm in ('to-prd','to-spec') else '-'} "
              f"mean/max state={sum(r[3] for r in results)//len(results)}/{max(r[3] for r in results)}")
        for scenario, code_ok, issue_ok, _ in results:
            suffix = f" issue={issue_ok}" if arm in ("to-prd", "to-spec") else ""
            print(f"  {scenario:12} code={code_ok}{suffix}")


if __name__ == "__main__":
    main()
