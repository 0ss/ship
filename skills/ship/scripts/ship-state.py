#!/usr/bin/env python3
"""Validate and inspect Ship's small, single-file state contract.

This tool is deliberately read-only for validate/status/basis. It never executes
a check named in SHIP.md and never changes the state file. `init` is the only
mutating command and refuses to overwrite an existing file.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "1"
MAX_FILE_BYTES = 1_000_000
MAX_ROWS = 20_000
MAX_ERRORS = 200
MAX_REVISION = 100_000
SECTIONS = {
    "Requirements": ["id", "revision", "disposition", "source", "request", "question"],
    "Work": ["id", "covers", "progress", "check", "code", "blocked_by"],
    "Checks": ["id", "command", "done_when"],
    "Evidence": ["id", "check", "intent", "contract", "result", "code", "ran", "by", "receipt"],
    "History": ["id", "kind", "from", "to", "source", "note"],
    "Ignored": ["id", "source", "kind", "note"],
}
DISPOSITIONS = {"active", "unclear", "deferred", "out-of-scope", "closed"}
PROGRESS = {"planned", "building", "implemented", "blocked"}
RESULTS = {"pass", "fail", "blocked", "unknown"}
BY = {"host", "human", "ci", "verifier", "model"}
HISTORY_KINDS = {"correction", "reopen", "defer", "close", "decision", "review"}
IGNORED_KINDS = {"embedded-instruction", "injected-instruction", "noise", "not-asked", "unsafe"}
ID_PATTERNS = {
    "Requirements": re.compile(r"R[1-9][0-9]*\Z"),
    "Work": re.compile(r"W[1-9][0-9]*\Z"),
    "Checks": re.compile(r"C[1-9][0-9]*\Z"),
    "Evidence": re.compile(r"E[1-9][0-9]*\Z"),
    "History": re.compile(r"H[1-9][0-9]*\Z"),
    "Ignored": re.compile(r"[IX][1-9][0-9]*\Z"),
}
REF = re.compile(r"R([1-9][0-9]*)@([1-9][0-9]*)\Z")
INTENT = re.compile(r"(R[1-9][0-9]*@[1-9][0-9]*)#([0-9a-f]{12})\Z")
CHECK = re.compile(r"C[1-9][0-9]*\Z")
CODE = re.compile(r"(?:git|workspace):[A-Za-z0-9._/@:+-]+\Z")
SEPARATOR = re.compile(r":?-{3,}:?\Z")


@dataclass
class Row:
    section: str
    values: dict[str, str]
    line: int


@dataclass
class State:
    path: Path
    rows: dict[str, list[Row]]
    errors: list[str]


def bounded_errors(errors: list[str], label: str = "validation errors") -> list[str]:
    normalized = [error if len(error) <= 240 else error[:237] + "..." for error in errors]
    if len(normalized) <= MAX_ERRORS:
        return normalized
    omitted = len(normalized) - MAX_ERRORS + 1
    return normalized[: MAX_ERRORS - 1] + [f"additional {omitted} {label} suppressed"]


def cells(line: str) -> list[str]:
    """Split a Markdown table row, honouring backslash-escaped pipes."""
    text = line.strip()
    if not (text.startswith("|") and text.endswith("|")):
        raise ValueError("table row must start and end with |")
    result: list[str] = []
    current: list[str] = []
    escaped = False
    for char in text[1:-1]:
        if escaped:
            if char == "|":
                current.append("|")
            else:
                current.extend(("\\", char))
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    result.append("".join(current).strip())
    return result


def is_separator(value: str) -> bool:
    return bool(SEPARATOR.fullmatch(value.strip()))


def parse(path: Path) -> State:
    errors: list[str] = []
    rows: dict[str, list[Row]] = {name: [] for name in SECTIONS}
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return State(path, rows, [f"state file exceeds safety limit {MAX_FILE_BYTES} bytes"])
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeError:
        return State(path, rows, [f"state file is not valid UTF-8: {path}"])
    except OSError as exc:
        return State(path, rows, [f"cannot read {path}: {exc}"])

    if not lines or lines[0].strip() != "# Ship":
        errors.append("line 1: file must start with '# Ship'")

    schema_seen = False
    seen_sections: set[str] = set()
    row_count = 0
    row_limit_reported = False
    index = 1
    while index < len(lines):
        line_no = index + 1
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("schema:"):
            if schema_seen:
                errors.append(f"line {line_no}: duplicate schema line")
            schema_seen = True
            if line.strip() != f"schema: {SCHEMA}":
                errors.append(f"line {line_no}: schema must be {SCHEMA}")
            index += 1
            continue
        if not line.startswith("## "):
            errors.append(f"line {line_no}: unexpected top-level content")
            index += 1
            continue

        section = line[3:].strip()
        if section not in SECTIONS:
            errors.append(f"line {line_no}: unknown section '{section}'")
            index += 1
            continue
        if section in seen_sections:
            errors.append(f"line {line_no}: duplicate section '{section}'")
        seen_sections.add(section)
        index += 1
        while index < len(lines) and not lines[index].strip():
            index += 1
        if index >= len(lines):
            errors.append(f"line {line_no}: section '{section}' has no table")
            continue
        header_line = index + 1
        try:
            header = cells(lines[index])
        except ValueError as exc:
            errors.append(f"line {header_line}: {exc}")
            index += 1
            continue
        expected = SECTIONS[section]
        if header != expected:
            errors.append(
                f"line {header_line}: {section} columns must be {' | '.join(expected)}"
            )
        index += 1
        if index >= len(lines):
            errors.append(f"line {header_line}: section '{section}' has no separator")
            continue
        separator_line = index + 1
        try:
            separator = cells(lines[index])
        except ValueError as exc:
            errors.append(f"line {separator_line}: {exc}")
            index += 1
            continue
        if len(separator) != len(expected) or not all(is_separator(v) for v in separator):
            errors.append(f"line {separator_line}: malformed table separator")
        index += 1

        while index < len(lines) and not lines[index].startswith("## "):
            row_line = index + 1
            if not lines[index].strip():
                index += 1
                continue
            if not lines[index].lstrip().startswith("|"):
                errors.append(f"line {row_line}: expected a table row in {section}")
                index += 1
                continue
            try:
                values = cells(lines[index])
            except ValueError as exc:
                errors.append(f"line {row_line}: {exc}")
                index += 1
                continue
            if len(values) != len(expected):
                errors.append(f"line {row_line}: expected {len(expected)} columns")
                index += 1
                continue
            if row_count >= MAX_ROWS:
                if not row_limit_reported:
                    errors.append(f"row limit {MAX_ROWS} exceeded; remaining rows ignored")
                    row_limit_reported = True
                index += 1
                continue
            row_count += 1
            rows[section].append(Row(section, dict(zip(expected, values)), row_line))
            index += 1

    if not schema_seen:
        errors.append("missing 'schema: 1'")
    for section in SECTIONS:
        if section not in seen_sections and not any(section in error for error in errors):
            errors.append(f"missing required section '{section}'")
    return State(path, rows, bounded_errors(errors))


def dash(value: str) -> bool:
    return value.strip() in {"", "-"}


def numeric_id(value: str, prefix: str) -> int | None:
    match = re.fullmatch(rf"{prefix}([1-9][0-9]*)", value)
    if not match or len(match.group(1)) > 8:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def revision_number(value: str) -> int | None:
    if len(value) > 8:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def revision_input(value: str) -> int | None:
    if not re.fullmatch(r"[1-9][0-9]*", value):
        return None
    return MAX_REVISION + 1 if len(value) > 8 else int(value)


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def expected_intent(
    state: State, work: Row, requirements: dict[str, Row] | None = None
) -> str:
    if requirements is None:
        requirements = {row.values["id"]: row for row in state.rows["Requirements"]}
    parts: list[str] = []
    for ref in (part.strip() for part in work.values["covers"].split(",")):
        base = ref.split("@", 1)[0]
        requirement = requirements.get(base)
        if requirement is not None:
            parts.append(f"{ref}#{fingerprint(requirement.values['request'])}")
    return ",".join(parts)


def intent_refs(value: str) -> tuple[str, ...] | None:
    refs: list[str] = []
    for part in value.split(","):
        match = INTENT.fullmatch(part.strip())
        if not match:
            return None
        refs.append(match.group(1))
    return tuple(refs)


def intent_matches(
    state: State,
    value: str,
    work: Row,
    requirements: dict[str, Row] | None = None,
) -> bool:
    if requirements is None:
        requirements = {row.values["id"]: row for row in state.rows["Requirements"]}
    expected_refs = [part.strip() for part in work.values["covers"].split(",") if part.strip()]
    parsed: list[tuple[str, str]] = []
    for part in value.split(","):
        match = INTENT.fullmatch(part.strip())
        if not match:
            return False
        parsed.append((match.group(1), match.group(2)))
    if [ref for ref, _ in parsed] != expected_refs:
        return False
    for ref, request_hash in parsed:
        base = ref.split("@", 1)[0]
        requirement = requirements.get(base)
        if requirement is None:
            return False
        current = revision_number(requirement.values["revision"])
        revision = revision_number(ref.split("@", 1)[1])
        if current is None or revision is None:
            return False
        if revision > current:
            return False
        # Prior revisions are retained as historical receipts. Their old text
        # is intentionally not re-hashed against the current request; they can
        # never satisfy proof for the current revision.
        if revision == current and request_hash != fingerprint(requirement.values["request"]):
            return False
    return True


def add(errors: list[str], row: Row, message: str) -> None:
    if len(message) > 240:
        message = message[:237] + "..."
    errors.append(f"line {row.line}: {message}")


def validate_state(
    state: State,
    require_evidence: bool = False,
    current_code: str | None = None,
) -> tuple[list[str], list[str]]:
    """Return structural errors and proof-mode errors."""
    errors = list(state.errors)
    proof_errors: list[str] = []

    def check_row(row: Row, allowed: set[str], field: str) -> None:
        if row.values[field] not in allowed:
            add(errors, row, f"unknown {field} '{row.values[field]}'")

    maps: dict[str, dict[str, Row]] = {}
    for section in SECTIONS:
        section_map: dict[str, Row] = {}
        for row in state.rows[section]:
            key = row.values["id"]
            if not ID_PATTERNS[section].fullmatch(key) or numeric_id(key, key[:1]) is None:
                add(errors, row, f"invalid {section} id '{key}'")
            if key in section_map:
                add(errors, row, f"duplicate id '{key}'")
            else:
                section_map[key] = row
        maps[section] = section_map

    requirements = maps["Requirements"]
    work = maps["Work"]
    checks = maps["Checks"]
    evidence = maps["Evidence"]
    current_refs = {
        f"{row.values['id']}@{row.values['revision']}"
        for row in state.rows["Requirements"]
    }
    work_refs: dict[tuple[str, tuple[str, ...]], Row] = {}
    work_group_current: dict[tuple[str, tuple[str, ...]], bool] = {}
    work_group_codes: dict[tuple[str, tuple[str, ...]], set[str]] = {}
    work_check_ids: set[str] = set()
    work_by_ref: dict[str, list[Row]] = {}
    for item in state.rows["Work"]:
        item_refs = tuple(
            part.strip() for part in item.values["covers"].split(",") if part.strip()
        )
        key = (item.values["check"], item_refs)
        work_check_ids.add(item.values["check"])
        work_refs.setdefault(key, item)
        work_group_codes.setdefault(key, set()).add(item.values["code"])
        work_group_current[key] = work_group_current.get(key, False) or any(
            ref in current_refs for ref in item_refs
        )
        for ref in item_refs:
            work_by_ref.setdefault(ref, []).append(item)
    latest_index = latest_evidence_index(state)

    def known_ref(value: str) -> bool:
        match = REF.fullmatch(value)
        if not match:
            return False
        requirement = requirements.get(f"R{match.group(1)}")
        if requirement is None:
            return False
        current = revision_number(requirement.values["revision"])
        revision = revision_number(match.group(2))
        if current is None or revision is None:
            return False
        return 1 <= revision <= min(current, MAX_REVISION)

    for row in state.rows["Requirements"]:
        revision = revision_input(row.values["revision"])
        if revision is None:
            add(errors, row, "revision must be a positive integer")
        elif revision > MAX_REVISION:
            add(errors, row, f"revision exceeds safety limit {MAX_REVISION}")
        check_row(row, DISPOSITIONS, "disposition")
        if dash(row.values["source"]):
            add(errors, row, "source must be a traceable anchor")
        if dash(row.values["request"]):
            add(errors, row, "request must not be empty")
        if row.values["disposition"] == "unclear":
            if dash(row.values["question"]):
                add(errors, row, "unclear requirement needs a question")
        elif not dash(row.values["question"]):
            add(errors, row, "only unclear requirements may have a question")

    def refs(value: str) -> list[str]:
        return [part.strip() for part in value.split(",") if part.strip()]

    def check_contract(check: Row) -> str:
        return f"{check.values['command']} => {check.values['done_when']}"

    for row in state.rows["Work"]:
        covered = refs(row.values["covers"])
        if not covered:
            add(errors, row, "covers must name at least one requirement revision")
        for ref in covered:
            if not known_ref(ref):
                add(errors, row, f"unknown requirement reference '{ref}'")
        check_row(row, PROGRESS, "progress")
        if not dash(row.values["code"]) and not CODE.fullmatch(row.values["code"]):
            add(errors, row, "code must be git:<revision> or workspace:<token>")
        if row.values["progress"] == "implemented":
            if dash(row.values["check"]):
                add(errors, row, "implemented work needs a check")
            if dash(row.values["code"]):
                add(errors, row, "implemented work needs a code token")
        if row.values["progress"] == "blocked" and dash(row.values["blocked_by"]):
            add(errors, row, "blocked work needs blocked_by")
        if not dash(row.values["check"]) and not CHECK.fullmatch(row.values["check"]):
            add(errors, row, f"invalid check reference '{row.values['check']}'")

    for row in state.rows["Checks"]:
        if dash(row.values["command"]):
            add(errors, row, "check command must not be empty")
        if dash(row.values["done_when"]):
            add(errors, row, "done_when must be one observable condition")

    last_evidence_id = 0
    for row in state.rows["Evidence"]:
        check_id = row.values["check"]
        if not CHECK.fullmatch(check_id) or check_id not in checks:
            add(errors, row, f"unknown check reference '{check_id}'")
        check_row(row, RESULTS, "result")
        check_row(row, BY, "by")
        if dash(row.values["intent"]):
            add(errors, row, "evidence intent must name the covered requirement revision")
        if dash(row.values["contract"]):
            add(errors, row, "evidence contract must name the checked condition")
        if not dash(row.values["code"]) and not CODE.fullmatch(row.values["code"]):
            add(errors, row, "evidence code must be git:<revision> or workspace:<token>")
        if row.values["result"] in {"pass", "fail"}:
            if dash(row.values["code"]):
                add(errors, row, f"{row.values['result']} evidence needs a code token")
            if dash(row.values["ran"]):
                add(errors, row, f"{row.values['result']} evidence needs ran")
        if dash(row.values["receipt"]):
            add(errors, row, "receipt must explain the result")
        if row.values["result"] == "blocked" and not row.values["receipt"].lower().startswith("blocked:"):
            add(errors, row, "blocked evidence receipt must start with 'blocked:'")
        evidence_id = numeric_id(row.values["id"], "E")
        if evidence_id is not None:
            if evidence_id <= last_evidence_id:
                add(errors, row, "evidence ids must increase in file order")
            last_evidence_id = evidence_id

    for row in state.rows["History"]:
        check_row(row, HISTORY_KINDS, "kind")
        if dash(row.values["source"]):
            add(errors, row, "history source must be traceable")
        if dash(row.values["note"]):
            add(errors, row, "history note must explain the transition")
        for field in ("from", "to"):
            value = row.values[field]
            if not dash(value) and not REF.fullmatch(value):
                add(errors, row, f"invalid {field} requirement reference '{value}'")
            elif not dash(value) and not known_ref(value):
                add(errors, row, f"unknown {field} requirement reference '{value}'")
        if row.values["kind"] in {"correction", "reopen"}:
            before = row.values["from"]
            after = row.values["to"]
            before_match = REF.fullmatch(before)
            after_match = REF.fullmatch(after)
            if not before_match or not after_match or before_match.group(1) != after_match.group(1):
                add(errors, row, "correction must link two revisions of one requirement")
            elif f"R{before_match.group(1)}" not in requirements:
                add(errors, row, "correction references an unknown requirement")
            else:
                before_revision = revision_number(before_match.group(2))
                after_revision = revision_number(after_match.group(2))
                if before_revision is None or after_revision is None:
                    add(errors, row, "correction revision is too large")
                elif after_revision <= before_revision:
                    add(errors, row, "correction must move to a newer revision")
        if row.values["kind"] == "close":
            target = row.values["to"]
            if not known_ref(target):
                add(errors, row, "close history must target a known requirement revision")

    for row in state.rows["Ignored"]:
        check_row(row, IGNORED_KINDS, "kind")
        if dash(row.values["source"]):
            add(errors, row, "ignored source must be traceable")
        if dash(row.values["note"]):
            add(errors, row, "ignored note must explain what was ignored")

    # Referential checks that need the parsed maps.
    for row in state.rows["Work"]:
        if not dash(row.values["check"]) and row.values["check"] not in checks:
            add(errors, row, f"unknown check reference '{row.values['check']}'")

    for row in state.rows["Evidence"]:
        check_id = row.values["check"]
        if check_id not in checks:
            continue
        if check_id not in work_check_ids:
            add(errors, row, "evidence has no corresponding work item")
            continue
        parsed_refs = intent_refs(row.values["intent"])
        key = (check_id, parsed_refs) if parsed_refs is not None else None
        representative = work_refs.get(key) if key is not None else None
        if key is None or representative is None or not intent_matches(
            state, row.values["intent"], representative, requirements
        ):
            add(errors, row, "evidence intent does not match the work it covers")
            continue
        if work_group_current[key]:
            # A current receipt is bound to the current acceptance contract.
            # Historical work may retain an old contract so corrections do not
            # force evidence retirement; it can never satisfy current proof.
            if row.values["contract"] != check_contract(checks[check_id]):
                add(errors, row, "evidence contract does not match the current check")
        if row.values["result"] == "pass" and row.values["code"] not in work_group_codes[key]:
            add(errors, row, "pass evidence code does not match its work")

    # Every revision after 1 needs an explicit lineage entry. Index links once
    # so a large history table does not make lineage validation quadratic.
    history_links = {
        (row.values["kind"], row.values["from"], row.values["to"])
        for row in state.rows["History"]
    }
    close_targets = {
        row.values["to"] for row in state.rows["History"] if row.values["kind"] == "close"
    }
    for row in state.rows["Requirements"]:
        revision = revision_number(row.values["revision"])
        if revision is None:
            continue
        base = row.values["id"]
        if revision > MAX_REVISION:
            continue
        missing: list[str] = []
        for previous in range(1, revision):
            expected_from = f"{base}@{previous}"
            expected_to = f"{base}@{previous + 1}"
            if not any(
                (kind, expected_from, expected_to) in history_links
                for kind in ("correction", "reopen")
            ):
                missing.append(f"{expected_from} -> {expected_to}")
                if len(missing) > 20:
                    break
        if missing:
            if len(missing) > 20 or revision > 1000:
                add(errors, row, f"revision {revision} is missing {len(missing)}+ history transitions")
            else:
                for transition in missing:
                    add(errors, row, f"revision {revision} missing history {transition}")
        if row.values["disposition"] == "closed":
            target = f"{row.values['id']}@{row.values['revision']}"
            if target not in close_targets:
                add(errors, row, f"closed requirement needs close history for {target}")

    if require_evidence:
        active = [r for r in state.rows["Requirements"] if r.values["disposition"] == "active"]
        if not active:
            proof_errors.append("nothing active to evidence")
        for req in active:
            ref = f"{req.values['id']}@{req.values['revision']}"
            current_work = work_by_ref.get(ref, [])
            if not current_work:
                proof_errors.append(f"{ref} has no work")
            for item in current_work:
                if not dash(item.values["blocked_by"]):
                    proof_errors.append(f"{ref} still has a blocker ({item.values['id']})")
                if item.values["progress"] != "implemented":
                    proof_errors.append(f"{ref} is not implemented ({item.values['id']})")
                    continue
                if dash(item.values["check"]):
                    proof_errors.append(f"{ref} has no check")
                    continue
                latest = latest_evidence(state, item.values["check"], latest_index)
                if latest is None:
                    proof_errors.append(f"{ref} has no evidence")
                    continue
                if latest.values["result"] != "pass":
                    proof_errors.append(f"{ref} latest evidence is {latest.values['result']}")
                if latest.values["result"] == "pass" and latest.values["by"] == "model":
                    proof_errors.append(f"{ref} evidence was authored by model")
                if latest.values["code"] != item.values["code"]:
                    proof_errors.append(f"{ref} evidence code does not match work")
                if not intent_matches(state, latest.values["intent"], item, requirements):
                    proof_errors.append(f"{ref} evidence intent does not match work")
                check = checks.get(item.values["check"])
                if check is None or latest.values["contract"] != f"{check.values['command']} => {check.values['done_when']}":
                    proof_errors.append(f"{ref} evidence contract does not match check")
                if current_code and latest.values["code"] != current_code:
                    proof_errors.append(f"{ref} evidence is not for current code {current_code}")

    return bounded_errors(errors), bounded_errors(proof_errors, "evidence-mode errors")


def latest_evidence_index(state: State) -> dict[str, Row]:
    latest: dict[str, Row] = {}
    numbers: dict[str, int] = {}
    for row in state.rows["Evidence"]:
        number = numeric_id(row.values["id"], "E")
        if number is None:
            continue
        check_id = row.values["check"]
        if number > numbers.get(check_id, -1):
            latest[check_id] = row
            numbers[check_id] = number
    return latest


def latest_evidence(
    state: State,
    check_id: str,
    index: dict[str, Row] | None = None,
) -> Row | None:
    if index is not None:
        return index.get(check_id)
    return latest_evidence_index(state).get(check_id)


def evidence_status(
    state: State,
    item: Row,
    current_code: str | None,
    latest_index: dict[str, Row] | None = None,
    requirements: dict[str, Row] | None = None,
    checks: dict[str, Row] | None = None,
) -> str:
    if item.values["progress"] != "implemented":
        return "in-progress" if item.values["progress"] == "building" else "open"
    if dash(item.values["check"]):
        return "implemented-unproven"
    if requirements is None:
        requirements = {row.values["id"]: row for row in state.rows["Requirements"]}
    if latest_index is None:
        latest_index = latest_evidence_index(state)
    latest = latest_evidence(state, item.values["check"], latest_index)
    if latest is None:
        return "implemented-unproven"
    if latest.values["result"] == "fail":
        return "failed"
    if latest.values["result"] == "blocked":
        return "blocked"
    if latest.values["result"] == "unknown":
        return "unknown"
    if latest.values["by"] == "model":
        return "implemented-unproven"
    if latest.values["code"] != item.values["code"]:
        return "stale"
    if current_code and latest.values["code"] != current_code:
        return "stale"
    if checks is None:
        checks = {row.values["id"]: row for row in state.rows["Checks"]}
    check = checks.get(item.values["check"])
    if check is None or not intent_matches(state, latest.values["intent"], item, requirements):
        return "stale"
    if latest.values["contract"] != f"{check.values['command']} => {check.values['done_when']}":
        return "stale"
    return "check-passed"


def derived_status(state: State, current_code: str | None = None) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    requirements = {row.values["id"]: row for row in state.rows["Requirements"]}
    checks = {row.values["id"]: row for row in state.rows["Checks"]}
    work_by_ref: dict[str, list[Row]] = {}
    for work in state.rows["Work"]:
        for ref in (part.strip() for part in work.values["covers"].split(",")):
            if ref:
                work_by_ref.setdefault(ref, []).append(work)
    latest_index = latest_evidence_index(state)
    for req in state.rows["Requirements"]:
        ref = f"{req.values['id']}@{req.values['revision']}"
        disposition = req.values["disposition"]
        status = disposition
        if disposition == "active":
            works = work_by_ref.get(ref, [])
            if not works:
                status = "open"
            elif any(w.values["progress"] == "blocked" or not dash(w.values["blocked_by"]) for w in works):
                status = "blocked"
            elif any(w.values["progress"] == "building" for w in works):
                status = "in-progress"
            elif any(w.values["progress"] != "implemented" for w in works):
                status = "open"
            else:
                statuses = [
                    evidence_status(state, item, current_code, latest_index, requirements, checks)
                    for item in works
                ]
                priority = ["blocked", "failed", "stale", "unknown", "implemented-unproven", "in-progress", "open"]
                status = next((candidate for candidate in priority if candidate in statuses), "check-passed")
                if all(candidate == "check-passed" for candidate in statuses):
                    status = "check-passed"
        result.append({"id": ref, "disposition": disposition, "status": status, "request": req.values["request"]})
    return result


def summary(state: State, current_code: str | None = None) -> dict[str, object]:
    statuses = derived_status(state, current_code)
    counts: dict[str, int] = {}
    dispositions: dict[str, int] = {}
    for item in statuses:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
        dispositions[item["disposition"]] = dispositions.get(item["disposition"], 0) + 1
    return {
        "file": str(state.path),
        "bytes": state.path.stat().st_size,
        "counts": counts,
        "dispositions": dispositions,
        "requirements": statuses,
    }


def print_errors(errors: list[str]) -> None:
    for error in errors:
        print(error, file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "validate", "status", "basis"))
    parser.add_argument("path", nargs="?", default="SHIP.md")
    parser.add_argument("work_id", nargs="?")
    parser.add_argument("--require-evidence", dest="require_evidence", action="store_true")
    parser.add_argument("--current-code")
    parser.add_argument("--short", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    path = Path(args.path)

    if args.command == "init":
        if path.exists() or path.is_symlink():
            print(f"{path} already exists", file=sys.stderr)
            return 1
        path.write_text(
            """# Ship\nschema: 1\n\n## Requirements\n| id | revision | disposition | source | request | question |\n|---|---:|---|---|---|---|\n\n## Work\n| id | covers | progress | check | code | blocked_by |\n|---|---|---|---|---|---|\n\n## Checks\n| id | command | done_when |\n|---|---|---|\n\n## Evidence\n| id | check | intent | contract | result | code | ran | by | receipt |\n|---|---|---|---|---|---|---|---|---|\n\n## History\n| id | kind | from | to | source | note |\n|---|---|---|---|---|---|\n\n## Ignored\n| id | source | kind | note |\n|---|---|---|---|\n""",
            encoding="utf-8",
        )
        return 0

    if args.command == "basis":
        if not args.work_id:
            print("basis requires a work id", file=sys.stderr)
            return 1
        state = parse(path)
        structural, _ = validate_state(state)
        if structural:
            print_errors(structural)
            return 1
        work = next((row for row in state.rows["Work"] if row.values["id"] == args.work_id), None)
        if work is None:
            print(f"unknown work id '{args.work_id}'", file=sys.stderr)
            return 1
        current_refs = {
            f"{row.values['id']}@{row.values['revision']}"
            for row in state.rows["Requirements"]
        }
        covered_refs = {
            part.strip() for part in work.values["covers"].split(",") if part.strip()
        }
        if not covered_refs.issubset(current_refs):
            print("basis requires current work; historical request text is not stored", file=sys.stderr)
            return 1
        check = next((row for row in state.rows["Checks"] if row.values["id"] == work.values["check"]), None)
        if check is None:
            print(f"work '{args.work_id}' has no check", file=sys.stderr)
            return 1
        print(f"intent={expected_intent(state, work)}")
        print(f"contract={check.values['command']} => {check.values['done_when']}")
        return 0

    state = parse(path)
    structural, proof = validate_state(state, args.require_evidence, args.current_code)
    if structural or proof:
        print_errors(structural)
        print_errors(proof)
        return 1

    data = summary(state, args.current_code)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    elif args.short:
        dispositions = data["dispositions"]
        counts = data["counts"]
        print(
            "active={} unclear={} deferred={} out-of-scope={} closed={} blocked={} failed={} unknown={} stale={} check-passed={} bytes={}".format(
                dispositions.get("active", 0),
                dispositions.get("unclear", 0),
                dispositions.get("deferred", 0),
                dispositions.get("out-of-scope", 0),
                dispositions.get("closed", 0),
                counts.get("blocked", 0),
                counts.get("failed", 0),
                counts.get("unknown", 0),
                counts.get("stale", 0),
                counts.get("check-passed", 0),
                data["bytes"],
            )
        )
    else:
        for item in data["requirements"]:
            print(f"{item['id']} · {item['status']} · {item['request']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
