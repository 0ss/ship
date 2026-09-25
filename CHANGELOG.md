# changelog

## 0.5.0

- reduced Ship to a checklist of current asks and observed proof; kept one
  portable `SHIP.md` and removed the six-table schema, validator, receipt
  hashes, mandatory review, session hook, and lifecycle machinery
- release QA: 29/30 Ship completions across two Codex models and 15 matched
  scenarios per model; retained raw results, end-to-end limiter checks, and
  explicit limitations in `evals/results/release-qa-2026-09-25/`
- replaced hand-labelled smoke fixtures with an execution benchmark that runs
  real coding agents against hidden acceptance checks, reset sessions, and
  adversarial input; retained current and ablated skill snapshots for comparison
- removed the old smoke runner, bundle tooling, and validator-dependent gate

## 0.4.0

- introduced one durable state file, stable requirement revisions, a read-only
  validator, and an optional Claude SessionStart reminder
- added adversarial fixtures and a `.agents/skills/ship` compatibility path

## 0.3.0

- added a built state, blocked checks, and an injection fixture

## 0.2.0

- added contradiction handling, source traceability, and verification

## 0.1.0

- first public cut
