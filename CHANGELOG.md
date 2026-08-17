# changelog

## 0.3.0

- `built` is a real state: code written, evidence not obtained. the state list is
  now closed, no invented states or appended phrases
- hook counts `built`
- recorded demo of a real run, plus its raw dump, ledger and tickets
- readme: what happens when (session cleared, dump mid-build, contradiction after
  shipping, blocked check, handoff), architecture, what it replaces

## 0.2.0

pressure testing round.

- material is inventory, never instruction. injected text goes under `ignored`
  with its source and is reported, not obeyed
- rows are numbered in source order, so a re-read of the same material gives the
  same ledger
- prove pass also reviews against repo standards, code smells, and security when
  the batch touched auth, secrets, input, files or payments
- defined what to do when a check cannot run: row stays `open`, `verified` records
  `blocked: <command>`
- fixture 07 (injection + dangerous asks), side-by-side baseline comparison

## 0.1.0

first cut.

- `ship` skill, absorb, build, prove
- `requirements.md` ledger, permanent row ids, recency wins, superseded kept
- session/prompt hooks, silent in repos with no ledger
- five fixtures with hand-labelled ground truth
- `context-cost.sh`, measure any plugin's idle cost
- ci: json, manifests, skill limits, shellcheck, hook behaviour
