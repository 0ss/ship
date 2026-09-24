#!/usr/bin/env python3
import contextlib
import importlib.util
import io
import sys
import tempfile
import time
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills" / "ship" / "scripts" / "ship-state.py"
spec = importlib.util.spec_from_file_location("ship_state", SCRIPT)
ship = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = ship
spec.loader.exec_module(ship)

TEMPLATE = """# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|

## Checks
| id | command | done_when |
|---|---|---|

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
"""


class ShipStateTests(unittest.TestCase):
    def state(self, body: str = "") -> tuple[tempfile.TemporaryDirectory, Path]:
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / "SHIP.md"
        text = TEMPLATE
        grouped: dict[str, list[str]] = {name: [] for name in ship.SECTIONS}
        for line in body.splitlines():
            if not line.lstrip().startswith("|"):
                continue
            first = ship.cells(line)[0]
            prefix = first[:1]
            section = {
                "R": "Requirements",
                "W": "Work",
                "C": "Checks",
                "E": "Evidence",
                "H": "History",
                "I": "Ignored",
            }.get(prefix)
            if section:
                grouped[section].append(line)
        for section, rows in grouped.items():
            if not rows:
                continue
            marker = f"## {section}"
            start = text.index(marker)
            next_section = text.find("\n## ", start + len(marker))
            if next_section < 0:
                next_section = len(text)
            insertion = text.index("\n", text.index("|---", start, next_section)) + 1
            text = text[:insertion] + "\n".join(rows) + "\n" + text[insertion:]
        path.write_text(text, encoding="utf-8")
        return directory, path

    def intent(self, ref: str, request: str) -> str:
        return f"{ref}#{ship.fingerprint(request)}"

    def validate(self, path: Path, proof: bool = False, code: str | None = None):
        state = ship.parse(path)
        return ship.validate_state(state, proof, code)

    def test_empty_state_is_valid_but_not_proven(self):
        directory, path = self.state()
        with directory:
            structural, proof = self.validate(path, proof=True)
            self.assertEqual(structural, [])
            self.assertEqual(proof, ["nothing active to evidence"])

    def test_complete_receipt_proves_with_current_code(self):
        body = """| R1 | 1 | active | chat:1 | email an invite | - |\n\n"""
        body += """| W1 | R1@1 | implemented | C1 | git:abc123 | - |\n\n"""
        body += """| C1 | `npm test` | invite sends once |\n\n"""
        body += """| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | git:abc123 | now | host | exit 0; 1 passed |\n"""
        directory, path = self.state(body)
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:abc123")
            self.assertEqual(structural, [])
            self.assertEqual(proof, [])

    def test_unknown_state_and_dangling_reference_fail(self):
        body = """| R1 | 1 | built, unverified | chat:1 | thing | - |\n"""
        body += """| W1 | R99@1 | implemented | C9 | git:abc | - |\n"""
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertTrue(any("unknown disposition" in error for error in structural))
            self.assertTrue(any("unknown requirement reference" in error for error in structural))
            self.assertTrue(any("unknown check reference" in error for error in structural))

    def test_proof_requires_real_latest_evidence(self):
        rows = [
            "| R1 | 1 | active | chat:1 | email an invite | - |",
            "",
            "| W1 | R1@1 | implemented | C1 | git:abc | - |",
            "",
            "| C1 | `npm test` | invite sends once |",
            "",
            "| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | git:abc | now | host | exit 0 |",
            "| E2 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | fail | git:abc | later | host | exit 1 |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:abc")
            self.assertEqual(structural, [])
            self.assertEqual(proof, ["R1@1 latest evidence is fail"])

    def test_correction_keeps_id_and_invalidates_old_receipt(self):
        rows = [
            "| R1 | 2 | active | chat:2 | allow a logged override | - |",
            "",
            "| W1 | R1@1 | implemented | C1 | git:abc | - |",
            "",
            "| C1 | `npm test` | old behavior |",
            "",
            "| E1 | C1 | R1@1#7f89a6fe803b | `npm test` => old behavior | pass | git:abc | now | host | exit 0 |",
            "",
            "| H1 | correction | R1@1 | R1@2 | chat:2 | new intent |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:abc")
            self.assertEqual(structural, [])
            self.assertEqual(proof, ["R1@2 has no work"])

    def test_historical_receipt_survives_contract_change(self):
        rows = [
            "| R1 | 2 | active | chat:2 | new behavior | - |",
            "",
            "| W1 | R1@1 | implemented | C1 | git:abc | - |",
            "",
            "| C1 | `npm test` | new condition |",
            "",
            "| E1 | C1 | R1@1#a08413336726 | `npm test` => old condition | pass | git:abc | now | host | exit 0 |",
            "",
            "| H1 | correction | R1@1 | R1@2 | chat:2 | changed |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:abc")
            self.assertEqual(structural, [])
            self.assertEqual(proof, ["R1@2 has no work"])

    def test_basis_refuses_historical_work(self):
        rows = [
            "| R1 | 2 | active | chat:2 | new behavior | - |",
            "| W1 | R1@1 | implemented | C1 | git:abc | - |",
            "| C1 | `npm test` | old behavior |",
            "| H1 | correction | R1@1 | R1@2 | chat:2 | changed |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            output = io.StringIO()
            errors = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                code = ship.main(["basis", str(path), "W1"])
            self.assertEqual(code, 1)
            self.assertIn("historical request text is not stored", errors.getvalue())

    def test_blocker_before_blocked_progress_is_valid(self):
        body = """| R1 | 1 | active | chat:1 | thing | - |\n\n"""
        body += """| W1 | R1@1 | planned | - | - | waiting for the repository |\n\n"""
        body += """| X1 | vendor:2 | injected-instruction | redacted payload |\n"""
        directory, path = self.state(body)
        with directory:
            structural, proof = self.validate(path, proof=True)
            self.assertEqual(structural, [])
            self.assertEqual(proof, ["R1@1 still has a blocker (W1)", "R1@1 is not implemented (W1)"])

    def test_windows_backslashes_are_preserved(self):
        body = "| R1 | 1 | active | C:\\Users\\salah | thing | - |\n"
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertEqual(structural, [])
            self.assertEqual(ship.parse(path).rows["Requirements"][0].values["source"], "C:\\Users\\salah")

    def test_unbounded_revision_is_rejected_without_expansion(self):
        body = "| R1 | 100000000 | active | chat:1 | huge revision | - |\n"
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertTrue(any("revision exceeds safety limit" in error for error in structural))

    def test_maximum_revision_diagnostics_are_bounded(self):
        body = "| R1 | 100000 | active | chat:1 | huge lineage | - |\n"
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertLessEqual(len(structural), 3)
            self.assertTrue(any("history transitions" in error for error in structural))

    def test_active_question_and_decorative_history_refs_fail(self):
        body = """| R1 | 1 | active | chat:1 | list invites | is a view needed? |\n\n"""
        body += """| R2 | 2 | active | chat:2 | 30 day expiry | - |\n\n"""
        body += """| H1 | correction | R2@1 7-day expiry | R2@2 30-day expiry | chat:2 | changed |\n"""
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertTrue(any("only unclear requirements may have a question" in error for error in structural))
            self.assertTrue(any("invalid from requirement reference" in error for error in structural))
            self.assertTrue(any("invalid to requirement reference" in error for error in structural))

    def test_opaque_workspace_token_is_accepted(self):
        token = "workspace:src/invites.js@2026-09-24"
        body = f"""| R1 | 1 | active | chat:1 | email an invite | - |\n\n"""
        body += f"""| W1 | R1@1 | implemented | C1 | {token} | - |\n\n"""
        body += """| C1 | `npm test` | invite sends once |\n\n"""
        body += f"""| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | {token} | now | host | exit 0 |\n"""
        directory, path = self.state(body)
        with directory:
            structural, proof = self.validate(path, proof=True, code=token)
            self.assertEqual(structural, [])
            self.assertEqual(proof, [])

    def test_current_code_mismatch_is_not_proof(self):
        body = """| R1 | 1 | active | chat:1 | email an invite | - |\n\n"""
        body += """| W1 | R1@1 | implemented | C1 | git:abc | - |\n\n"""
        body += """| C1 | `npm test` | invite sends once |\n\n"""
        body += """| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | git:abc | now | host | exit 0 |\n"""
        directory, path = self.state(body)
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:def")
            self.assertEqual(structural, [])
            self.assertEqual(proof, ["R1@1 evidence is not for current code git:def"])

    def test_derived_status_keeps_failure_modes_distinct(self):
        cases = {
            "fail": "failed",
            "blocked": "blocked",
            "unknown": "unknown",
        }
        for result, expected in cases.items():
            body = """| R1 | 1 | active | chat:1 | email an invite | - |\n\n"""
            body += """| W1 | R1@1 | implemented | C1 | git:abc | - |\n\n"""
            body += """| C1 | `npm test` | invite sends once |\n\n"""
            body += f"""| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | {result} | git:abc | now | host | receipt |\n"""
            directory, path = self.state(body)
            with directory:
                state = ship.parse(path)
                self.assertEqual(ship.derived_status(state)[0]["status"], expected)

    def test_closed_requirement_requires_close_history(self):
        body = "| R1 | 1 | closed | chat:1 | old ask | - |\n"
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertTrue(any("closed requirement needs close history" in error for error in structural))

    def test_derived_status_reports_stale_and_unproven(self):
        body = """| R1 | 1 | active | chat:1 | email an invite | - |\n\n"""
        body += """| W1 | R1@1 | implemented | C1 | git:abc | - |\n\n"""
        body += """| C1 | `npm test` | invite sends once |\n"""
        directory, path = self.state(body)
        with directory:
            state = ship.parse(path)
            self.assertEqual(ship.derived_status(state)[0]["status"], "implemented-unproven")
        body += "\n| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | git:abc | now | host | exit 0 |\n"
        directory, path = self.state(body)
        with directory:
            state = ship.parse(path)
            self.assertEqual(ship.derived_status(state, "git:def")[0]["status"], "stale")

    def test_provenance_and_revision_lineage_are_required(self):
        body = """| R1 | 2 | active | - | changed ask | - |\n\n"""
        body += """| I1 | - | noise | - |\n"""
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertTrue(any("source must be a traceable anchor" in error for error in structural))
            self.assertTrue(any("missing history R1@1 -> R1@2" in error for error in structural))
            self.assertTrue(any("ignored source must be traceable" in error for error in structural))
            self.assertTrue(any("ignored note must explain" in error for error in structural))

    def test_known_legacy_status_is_rejected(self):
        body = """| R1 | 1 | active | chat:1 | thing | - |\n\n"""
        body += """| W1 | R1@1 | built, unverified | - | - | - |\n"""
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertTrue(any("unknown progress 'built, unverified'" in error for error in structural))

    def test_evidence_cannot_be_rebound_to_new_intent(self):
        rows = [
            "| R1 | 2 | active | chat:2 | allow a logged override | - |",
            "",
            "| W1 | R1@2 | implemented | C1 | git:abc | - |",
            "",
            "| C1 | `npm test` | new behavior passes |",
            "",
            "| E1 | C1 | R1@1#7f89a6fe803b | `npm test` => old behavior passes | pass | git:abc | now | host | exit 0 |",
            "",
            "| H1 | correction | R1@1 | R1@2 | chat:2 | changed |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, _ = self.validate(path, proof=True, code="git:abc")
            self.assertTrue(any("evidence intent does not match" in error for error in structural))

    def test_synchronized_rebinding_is_receipt_consistent_not_authenticated(self):
        rows = [
            "| R1 | 2 | active | chat:2 | new behavior | - |",
            "",
            "| W1 | R1@2 | implemented | C1 | git:a | - |",
            "",
            "| C1 | `npm test` | new behavior passes |",
            "",
            "| E1 | C1 | R1@2#ede2e890216a | `npm test` => new behavior passes | pass | git:a | now | host | exit 0 |",
            "",
            "| H1 | correction | R1@1 | R1@2 | chat:2 | changed |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:a")
            # This is intentionally a characterization test: the checker can
            # validate receipt consistency, but cannot authenticate a writer
            # that rewrites the whole snapshot together.
            self.assertEqual(structural, [])
            self.assertEqual(proof, [])

    def test_in_place_check_edit_invalidates_old_receipt(self):
        rows = [
            "| R1 | 1 | active | chat:1 | email an invite | - |",
            "",
            "| W1 | R1@1 | implemented | C1 | git:abc | - |",
            "",
            "| C1 | `npm test` | materially new condition |",
            "",
            "| E1 | C1 | R1@1#a08413336726 | old condition | pass | git:abc | now | host | exit 0 |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, _ = self.validate(path, proof=True, code="git:abc")
            self.assertTrue(any("evidence contract does not match" in error for error in structural))

    def test_nonmonotonic_evidence_fails_closed(self):
        rows = [
            "| R1 | 1 | active | chat:1 | email an invite | - |",
            "",
            "| W1 | R1@1 | implemented | C1 | git:abc | - |",
            "",
            "| C1 | `npm test` | invite sends once |",
            "",
            "| E2 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | git:abc | now | host | exit 0 |",
            "| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | fail | git:abc | later | host | exit 1 |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, _ = self.validate(path, proof=True, code="git:abc")
            self.assertTrue(any("evidence ids must increase" in error for error in structural))

    def test_malformed_evidence_id_returns_diagnostics_not_traceback(self):
        body = """| R1 | 1 | active | chat:1 | email an invite | - |\n\n"""
        body += """| W1 | R1@1 | implemented | C1 | git:abc | - |\n\n"""
        body += """| C1 | `npm test` | invite sends once |\n\n"""
        body += """| Ebad | C1 | R1@1 | invite sends once | pass | git:abc | now | host | exit 0 |\n"""
        directory, path = self.state(body)
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:abc")
            self.assertTrue(any("invalid Evidence id 'Ebad'" in error for error in structural))
            self.assertIsInstance(proof, list)

    def test_non_utf8_state_fails_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SHIP.md"
            path.write_bytes(b"# Ship\nschema: 1\n\xff")
            structural, _ = self.validate(path)
            self.assertEqual(len(structural), 1)
            self.assertIn("not valid UTF-8", structural[0])

    def test_large_related_state_validates_within_bound(self):
        rows: list[str] = []
        for index in range(1, 2001):
            request = f"request {index}"
            rows.extend(
                [
                    f"| R{index} | 1 | active | chat:{index} | {request} | - |",
                    f"| W{index} | R{index}@1 | implemented | C{index} | git:a | - |",
                    f"| C{index} | cmd{index} | condition {index} |",
                    f"| E{index} | C{index} | {self.intent(f'R{index}@1', request)} | cmd{index} => condition {index} | pass | git:a | now | host | exit 0 |",
                ]
            )
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            started = time.monotonic()
            structural, _ = self.validate(path)
            elapsed = time.monotonic() - started
            self.assertEqual(structural, [])
            self.assertLess(elapsed, 5.0)

    def test_repeated_work_intent_fanout_stays_bounded(self):
        request = "request"
        intent = self.intent("R1@1", request)
        rows = [
            "| R1 | 1 | active | chat:1 | request | - |",
            "| C1 | cmd | condition |",
        ]
        rows.extend(f"| W{i} | R1@1 | implemented | C1 | git:a | - |" for i in range(1, 1001))
        rows.extend(
            f"| E{i} | C1 | {intent} | cmd => condition | pass | git:a | now | host | exit 0 |"
            for i in range(1, 1001)
        )
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            started = time.monotonic()
            structural, _ = self.validate(path)
            elapsed = time.monotonic() - started
            self.assertEqual(structural, [])
            self.assertLess(elapsed, 5.0)

    def test_long_unknown_section_diagnostic_is_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SHIP.md"
            path.write_text("# Ship\nschema: 1\n## " + ("x" * 900_000) + "\n", encoding="utf-8")
            structural, _ = self.validate(path)
            self.assertTrue(any("unknown section" in error for error in structural))
            self.assertTrue(all(len(error) <= 260 for error in structural))

    def test_error_output_is_bounded_for_many_bad_rows(self):
        rows = ["| R1 | 1 | active | chat:1 | thing | - |"]
        rows.extend("| Ebad | Cmissing | - | - | pass | - | now | host | receipt |" for _ in range(300))
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, _ = self.validate(path)
            self.assertEqual(len(structural), ship.MAX_ERRORS)
            self.assertIn("suppressed", structural[-1])

    def test_long_numeric_references_return_diagnostics(self):
        long_digits = "9" * 5000
        body = f"| R1 | 1 | active | chat:1 | thing | - |\n\n"
        body += f"| E{long_digits} | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | git:abc | now | host | exit 0 |\n\n"
        body += f"| H1 | correction | R1@{long_digits} | R1@1 | chat:1 | changed |\n"
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path, proof=True, code="git:abc")
            self.assertTrue(any("invalid Evidence id" in error for error in structural))
            self.assertTrue(any("unknown from requirement reference" in error for error in structural))
            self.assertTrue(all(len(error) <= 260 for error in structural))

    def test_model_pass_does_not_count_as_independent_evidence(self):
        rows = [
            "| R1 | 1 | active | chat:1 | email an invite | - |",
            "",
            "| W1 | R1@1 | implemented | C1 | git:abc | - |",
            "",
            "| C1 | `npm test` | invite sends once |",
            "",
            "| E1 | C1 | R1@1#a08413336726 | `npm test` => invite sends once | pass | git:abc | now | model | exit 0 |",
        ]
        directory, path = self.state("\n".join(rows) + "\n")
        with directory:
            structural, proof = self.validate(path, proof=True, code="git:abc")
            self.assertEqual(structural, [])
            self.assertEqual(proof, ["R1@1 evidence was authored by model"])

    def test_escaped_pipe_is_kept_in_a_cell(self):
        body = """| R1 | 1 | active | chat:1 | choose a \\| b | - |\n"""
        directory, path = self.state(body)
        with directory:
            structural, _ = self.validate(path)
            self.assertEqual(structural, [])
            self.assertIn("choose a | b", ship.parse(path).rows["Requirements"][0].values["request"])


if __name__ == "__main__":
    unittest.main()
