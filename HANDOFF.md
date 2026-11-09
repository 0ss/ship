# Handoff: Ship redesign (in progress, nothing committed)

## Goal
Redesign `ship` into the smallest model-agnostic layer for: messy human intent → completed work → observable proof. Benchmark current vs new, ablate everything, delete what doesn't earn its place, leave repo working, commit. Full original brief: ask the user (long prompt: "obligation → frontier → proof", minimalism rule, 12 eval classes, required final report sections: Primitive / Architecture / Deleted / Benchmark / Failures found / Why this design won / Limitations / Repository).

User git rules (~/.claude/CLAUDE.md): no AI attribution in commits; short casual lowercase commit messages.

## Where things are
- Current Ship (baseline to beat): `skills/ship/SKILL.md` (193 lines, 10K chars, 6-table SHIP.md), `skills/ship/scripts/ship-state.py` (826-line validator), `hooks/` (Claude SessionStart reminder), `tests/test_ship_state.py`, `scripts/validate.sh`, old evals (`evals/run.sh`, `old-fixtures/`, `truth/`, `setups/`, `result-bundle.py`, `context-cost.sh`, `trigger-cases.json`, `scenarios.md`, `results/2026-09-24-smoke*`). Uncommitted user WIP exists in `skills/ship/SKILL.md` + `evals/README.md`; untracked `SHIP.md` (dogfood ledger) and `docs/` (user research note) — don't delete those two without asking.
- **New eval harness** (untracked, keep): `evals/run.py`, `evals/seed/` (tiny Python invite app), `evals/overlays/false-done/`, `evals/fixtures/` (new scenarios; old ones moved to `evals/old-fixtures/`), `evals/hidden/checks.py` (hidden acceptance checks; agents never see it), `evals/activation.py` + `evals/activation.json` (routing test, not run yet).
- **Arms** (plugin roots): `evals/arms/current` (snapshot of current skill+hook), `evals/arms/new` (candidate, 32 lines / 2.5K chars), `evals/arms/rule-only` (871 chars ablation), `evals/arms/nostate` (no SHIP.md ablation).
- Round-1 results: `evals/results/r1-sonnet/` (`summary.txt`, per-run `result.json`, `SHIP.md`, `diff.txt`).

## Harness
```
python3 evals/run.py --host claude:claude-sonnet-5 --arm new=evals/arms/new --arm current=evals/arms/current --arm baseline= \
  --scenario all --trials 2 --jobs 8 --out <dir>
python3 evals/run.py --host x --arm x= --out <dir> --summary   # re-summarize
```
Hosts: `claude:MODEL`, `codex:gpt-5.6-sol`, `opencode:opencode-go/{glm-5.3,kimi-k2.6,grok-4.7}`. Gemini CLI unusable (account ineligible); opencode deepseek region-blocked.
Scenarios: messy, buried, pivot (6-turn correction/cancel/re-add), handoff (capture, clear, resume), interrupted (killed at 75s, fresh resume), false-done, blocker, injection. Metrics: complete, recall, false obligations, false completion (judge: claims done ∧ checks fail), unnecessary questions (Haiku judge), recovery, state bytes, time.
Gotchas:
- Claude runs use `--setting-sources project,local`, `--plugin-dir`, `acceptEdits` + scoped `--allowedTools`. `--dangerously-skip-permissions` for nested agents is blocked by the auto-mode classifier — don't use it.
- Claude auto-memory must be off (`--settings {"autoMemoryEnabled": false}`, already in run.py): in round 1 the no-skill baseline passed handoff only because of Claude's private memory. Round-1 handoff/interrupted numbers were taken with memory ON — rerun them.
- Activation prefix: `/ship ` on Claude, "Use the ship skill." elsewhere (first turn of each session only).
- zsh doesn't word-split `$VAR` args; write arms out explicitly.

## Round 1 (Sonnet 5, 8 scenarios × 2)
| arm | complete | asks | min | state bytes |
|---|---|---|---|---|
| baseline | 88% | 8 | 1.3 | 0 |
| current | 81% | 16 | 3.4 | 2770 |
| new | 100% | 3 | 1.6 | 547 |

Failures seen:
- false-done: baseline and current both *found* the per-user/window bug, then asked permission or "sent it back" instead of fixing. new fixed it 2/2.
- current interrupted#2: killed at 75s before its heavy ledger existed → fresh session had nothing, asked user "what were we working on". new writes state first.
- current asks far more (commit offers, confirmations); new's 3 asks = 2 commit offers + 1 legit scope question.
- new records jokes/non-asks as struck "dropped" lines (noise). Candidate fix: "strike only asks the user cancelled".
- Validator unreachable from inside a plugin sandbox (agent noted it, wrote ledger by hand) — friction evidence against the script.

## Was running when handed off (results in a scratchpad dir that may vanish — rerun if missing)
- Haiku 4.5, all 3 arms × all scenarios × 2 (memory off).
- Sonnet handoff+interrupted × 3 trials, all arms (memory off).
- Codex gpt-5.6-sol + OpenCode glm-5.3, new arm, handoff (adapter smoke — adapters for codex/opencode untested until this finishes).

## Remaining plan
1. Rerun the two above into `evals/results/`. Check codex/opencode adapters parse replies/session ids correctly.
2. Cross-model: new vs current on codex + ≥1 opencode family.
3. Ablations (rule-only, nostate, + drop ask-policy, drop prove step) on the scenarios they affect; delete any part whose removal doesn't hurt.
4. Activation: `python3 evals/activation.py evals/arms/new 3` vs `evals/arms/current` (Claude only).
5. Test SessionStart hook value: resume without `/ship` re-activation, with/without hook. Keep hook only if it measurably helps.
6. Install winner into `skills/ship/SKILL.md`; delete validator, tests, old evals, bundle tooling, hook (unless step 5 says keep); fix `scripts/validate.sh`, CI, README, evals/README (write real numbers), CHANGELOG, bump version in both manifests. Keep `.agents/skills/ship` symlink.
7. `./scripts/validate.sh` green, commit (user rules above), final report in the brief's format.
