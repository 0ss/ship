# Execution benchmark

`run.py` gives each arm a fresh copy of a tiny invite service from `seed/`,
plays real user turns through a coding-agent CLI, and runs `hidden/checks.py`
against the result. The agent never sees the hidden checks. A separate small
model judges final replies for user questions and completion claims. An arm is
a plugin root under `arms/`; `current` snapshots pre-redesign Ship, `new` is the
32-line draft, and the other arms remove specific mechanisms. The released
skill adds two small clarifications to that draft about noise and needless
permission questions.

| scenario | pressure |
|---|---|
| messy | multiple asks mixed with jokes and irrelevant scope |
| buried | two requests inside a long chat export |
| pivot | correction, cancellation, new ask, and re-add over several turns |
| handoff | fresh session works from durable state |
| interrupted | kill mid-work and resume in a fresh session |
| false-done | passing visible tests conceal an unmet per-user requirement |
| blocker | only the user knows the agreed price; other work can proceed |
| injection | hostile instructions embedded in source material |

Checks include completion of each expected behavior, forbidden scope changes,
visible tests, unnecessary user interventions, false completion claims, state
size, and recovery. `activation.json` adds positive and near-miss routing
prompts. `bench_integrity.py` verifies the seed remains a real before-state
and the false-done trap remains armed.

## Final release QA (2026-09-25)

`results/release-qa-2026-09-25/` contains a 15-scenario matched Codex matrix
(Sol and Luna, Ship and baseline), a model swap and repeat trials, raw turn
replies, ledgers, and `adjudications.json`. The long noisy dump has 109 lines
with its CSV request at line 66. The end-to-end rate-limit variant tests
service integration; the original false-done check covers only the limiter
object. Two reply-judge labels were corrected against raw text.

Claude Haiku's long-dump attempt timed out without a reply; its unscored
artifact is under `infrastructure/`. OpenCode Go returned a provider quota
error. Neither host supplies cross-family evidence in this run.

## Run

```bash
./scripts/validate.sh
python3 evals/run.py --host claude:claude-sonnet-5 \
  --arm new=evals/arms/new --arm current=evals/arms/current \
  --arm baseline= --scenario all --trials 2 --jobs 2 \
  --out evals/results/local
python3 evals/run.py --summary --out evals/results/local
python3 evals/activation.py evals/arms/new 1
```

`--host` also accepts `codex:MODEL` and `opencode:MODEL`. For reset tests,
`--resume-without-activation` omits explicit skill invocation after the first
session. On Claude, auto-memory is disabled in the execution runner so recovery
must come from the repository. A local CLI and credentials are required; keep
`--jobs` small to avoid saturating the host. Individual `result.json` files
contain the hidden-check result and per-turn replies; `SHIP.md` and `diff.txt`
capture the final state and changed-file summary. Incomplete jobs can be
resumed with the same command and output directory.

## Measurements

Initial Sonnet 5 comparison: 8 scenarios × 2 trials per arm. **These first
runs left Claude's private auto-memory enabled**, so handoff and interruption
results are not clean tests of the state file. See `results/r1-sonnet/`.

| arm | completed | unnecessary questions | mean state | mean time |
|---|---:|---:|---:|---:|
| no skill | 14/16 | 8 | 0 B | 1.3 min |
| pre-redesign Ship | 13/16 | 16 | 2,770 B | 3.4 min |
| redesign | 16/16 | 3 | 547 B | 1.6 min |

None of those runs changed forbidden scope or made a false completion claim.
The old skill and no-skill baseline both identified the false-done bug but
stopped to ask rather than fix it; the redesign fixed it twice. The old skill
lost one interrupted run before it wrote a state file. The new skill sometimes
recorded jokes as struck asks, adding noise. A separate Haiku run found a real
redesign failure: an `is_expired(now)` method was put on the service, not the
invite, and the model incorrectly claimed both buried asks were done despite
passing its own tests.

Additional **partial** observations: the new arm completed 15/16 Haiku runs;
the old arm completed 3/8 runs that finished before the batch was stopped. With
Claude auto-memory disabled, the new arm completed 5/5 finished Sonnet
handoff/interruption runs. Codex completed a handoff smoke and two new-arm
cases (handoff and false-done). An overloaded Sonnet ablation batch gave the
new arm 4/5 and the no-ask-policy arm 2/4 on different subsets. The rule-only,
no-state, proof-step, SessionStart hook, and activation comparisons did not
finish; they cannot support a causal claim. OpenCode returned a provider 429
quota error, not a skill failure. See each `result.json` for the actual checks;
do not compare unmatched subsets as a head-to-head rate.

## Limits

The hidden grader tests a compact app, not arbitrary tasks. Its forbidden-scope
checks cover specific actions, not every invented obligation. The reply judge
can misclassify phrasing, and a passing test cannot prove every product outcome.
Result samples are small; activation, ablation, and cross-host reliability need
more clean trials. The optional hook and validator were removed because they
had no demonstrated benefit in these execution results, not because a powered
ablation proved they never help. Inspect failures and the actual artifacts
rather than treating a summary percentage as a guarantee.
