# changelog

## 0.4.0

- replaced the competing `requirements.md` + `tickets.md` design with one
  `SHIP.md` contract for intent, work frontier, checks, evidence, history, and
  ignored material
- added stable requirement revisions so corrections reopen work without duplicate
  requirements or stale evidence
- added a read-only Python state validator and unit tests for malformed states,
  dangling references, blocked/failed checks, stale revisions, rebinding, and
  false completion claims
- added receipt binding for ordinary stale edits with a request fingerprint and
  exact check contract; added the read-only `basis` helper and monotonic
  evidence ordering
- explicitly scoped the checker to receipt consistency, not execution
  authentication
- made independent verification capability-based: separate context, CI, or human
  when available; honest `unverified` fallback otherwise
- removed the per-prompt hook; kept one optional Claude `SessionStart` adapter
- exposed the skill through `.agents/skills` for portable Agent Skills clients
- added adversarial repeated-dump, resume, blocked-proof, false-completion,
  irrelevant-material, and state-growth fixtures
- rewrote installation, architecture, limitations, and benchmark documentation

## 0.3.0

- added a real `built` state after pressure testing found completion-state drift
- added blocked-check handling and the first injection fixture
- recorded a demo run and expanded the benchmark

## 0.2.0

- added contradiction handling, source traceability, and a fresh verifier
- introduced the first absorb/build/prove benchmark fixtures

## 0.1.0

- first public cut
