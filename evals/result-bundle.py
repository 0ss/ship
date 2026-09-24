#!/usr/bin/env python3
"""Export and verify the compact, dated model-smoke result bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

CASES = (
    ("ship", "04-no-asks"),
    ("ship", "02-whatsapp-thread"),
    ("ship", "05-contradicts-shipped"),
    ("ship", "08-repeated-corrections"),
    ("ship", "07-injection"),
    ("baseline", "08-repeated-corrections"),
)
FILES = ("SHIP.md", "validation.txt", "status.txt", "evidence.txt", "reply.txt", "legacy-files.txt")
BUNDLE_DATE = "2026-09-24"
BUNDLE_MODEL = "claude-opus-5"
BUNDLE_COMMAND = "MODEL=claude-opus-5 ./evals/run.sh <arm> <fixture>"
BUNDLE_NOTE = (
    "Single-trial smoke artifacts. Evidence mode may fail for planned or blocked work; "
    "this is expected and recorded separately from structural validation."
)
SOURCE_FILES = ("evals/run.sh", "skills/ship/scripts/ship-state.py")


def digest(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def source_hashes() -> dict[str, str]:
    return {
        filename: hashlib.sha256(Path(filename).read_bytes()).hexdigest()
        for filename in SOURCE_FILES
    }


def read_exit(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("exit="):
            return line.split("=", 1)[1]
    return None


def export_bundle(runs: Path, output: Path, date: str, model: str) -> None:
    output = output.resolve()
    if output == Path("/") or len(output.parts) < 3:
        raise ValueError(f"refusing unsafe output path: {output}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    cases: dict[str, object] = {}
    for arm, name in CASES:
        source = runs / arm / name
        if not source.is_dir():
            raise FileNotFoundError(f"missing run directory: {source}")
        destination = output / f"{arm}-{name}"
        destination.mkdir()
        files: dict[str, object] = {}
        for filename in FILES:
            source_file = source / filename
            if not source_file.is_file():
                raise FileNotFoundError(f"missing result artifact: {source_file}")
            destination_file = destination / filename
            shutil.copyfile(source_file, destination_file)
            files[filename] = digest(destination_file)
        cases[destination.name] = {
            "files": files,
            "validation_exit": read_exit(destination / "validation.txt"),
            "evidence_mode_exit": read_exit(destination / "evidence.txt"),
        }

    manifest = {
        "date": date,
        "model": model,
        "contract": {"schema": 1, "plugin": "0.4.0"},
        "command": BUNDLE_COMMAND,
        "note": BUNDLE_NOTE,
        "sources": source_hashes(),
        "cases": cases,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def verify_bundle(output: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = output / "manifest.json"
    if not manifest_path.is_file():
        return [f"missing {manifest_path}"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cannot read manifest: {exc}"]
    cases = manifest.get("cases")
    if not isinstance(cases, dict) or not cases:
        return ["manifest has no cases"]
    expected_case_names = {f"{arm}-{name}" for arm, name in CASES}
    if set(cases) != expected_case_names:
        return [f"manifest case set differs: expected {sorted(expected_case_names)}"]
    if manifest.get("contract") != {"schema": 1, "plugin": "0.4.0"}:
        return ["manifest contract metadata differs"]
    expected_metadata = {
        "date": BUNDLE_DATE,
        "model": BUNDLE_MODEL,
        "command": BUNDLE_COMMAND,
        "note": BUNDLE_NOTE,
    }
    for key, expected in expected_metadata.items():
        if manifest.get(key) != expected:
            return [f"manifest {key} metadata differs"]
    try:
        if manifest.get("sources") != source_hashes():
            return ["bundle source hashes differ; regenerate the dated bundle"]
    except OSError as exc:
        return [f"cannot hash bundle sources: {exc}"]

    expected_dirs = set(cases)
    actual_dirs = {path.name for path in output.iterdir() if path.is_dir()}
    if expected_dirs != actual_dirs:
        errors.append(f"case directories differ: expected {sorted(expected_dirs)}, got {sorted(actual_dirs)}")
    for name, expected in sorted(cases.items()):
        case_dir = output / name
        if not case_dir.is_dir():
            continue
        expected_files = expected.get("files", {}) if isinstance(expected, dict) else {}
        if set(expected_files) != set(FILES):
            errors.append(f"{name}: required artifact set differs")
        try:
            actual_validation_exit = read_exit(case_dir / "validation.txt")
            actual_evidence_exit = read_exit(case_dir / "evidence.txt")
        except OSError as exc:
            errors.append(f"{name}: cannot read exit metadata ({exc})")
        else:
            if expected.get("validation_exit") != actual_validation_exit:
                errors.append(f"{name}: validation exit metadata differs")
            if expected.get("evidence_mode_exit") != actual_evidence_exit:
                errors.append(f"{name}: evidence-mode exit metadata differs")
        actual_files = {
            str(path.relative_to(case_dir))
            for path in case_dir.rglob("*")
            if path.is_file()
        }
        if set(expected_files) != actual_files:
            errors.append(f"{name}: file set differs")
        for filename, metadata in expected_files.items():
            path = case_dir / filename
            if not path.is_file():
                continue
            try:
                actual = digest(path)
            except OSError as exc:
                errors.append(f"{name}/{filename}: cannot read ({exc})")
                continue
            if actual != metadata:
                errors.append(f"{name}/{filename}: hash or byte count differs")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    export = subparsers.add_parser("export")
    export.add_argument("--runs", type=Path, default=Path("evals/runs"))
    export.add_argument("--out", type=Path, required=True)
    export.add_argument("--date", default=BUNDLE_DATE)
    export.add_argument("--model", default=BUNDLE_MODEL)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--bundle", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        if args.command == "export":
            export_bundle(args.runs, args.out, args.date, args.model)
            print(f"exported {args.out}")
            return 0
        errors = verify_bundle(args.bundle)
    except (OSError, ValueError) as exc:
        print(f"result-bundle: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"result-bundle: {error}", file=sys.stderr)
        return 1
    print(f"verified {args.bundle}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
