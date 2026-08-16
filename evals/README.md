# 📊 Benchmark

Skills are not automatically useful. [SkillsBench](https://arxiv.org/pdf/2602.12670)
found that skills sometimes *degrade* agent performance, and that chaining
several skills does not reliably beat using one. So this repo ships its
evidence, not its opinion.

Anthropic's own guidance is to
[write evaluations before writing the skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#build-evaluations-first).
These fixtures were written first.

## Contents

- [What is measured](#what-is-measured)
- [Fixtures](#fixtures)
- [Running it](#running-it)
- [Results](#results)
- [Scope](#scope)

## What is measured

| metric | question | how |
|---|---|---|
| **turns to done** | how many times does the human have to intervene? | count user messages that are not new material — clarifications, re-prompts, corrections of the agent |
| **recall** | asks captured ÷ asks present | against `truth/*.json` |
| **precision** | rows that correspond to a real ask | invented requirements are the failure |
| **recency** | does the last word win? | reversals in fixtures 01, 02, 05 |
| **restraint** | does thinking-aloud produce zero rows? | fixture 04 |
| **stability** | same fixture twice, same ledger? | diff two runs |
| **accretion** | 15 separate messages = 1 paste? | fixture 02, both deliveries |
| **evidence rate** | `shipped` rows carrying a re-runnable check | read `tickets.md` |
| **idle context cost** | bytes spent before the human says anything | `./context-cost.sh` |

**Turns to done is the headline.** Every other framework optimises output
quality. This one optimises how little the human has to do, so that is the
number it must be judged on.

## Fixtures

| fixture | shape | tests |
|---|---|---|
| [01](fixtures/01-meeting-transcript.md) | 34-min meeting transcript | asks buried in discussion, a reversal reversed, one genuinely unclear ask |
| [02](fixtures/02-whatsapp-thread.md) | 15 one-line chat messages | accretion, one ask split across five messages, ID stability |
| [03](fixtures/03-voice-note.md) | unpunctuated voice note | false starts, trailing ask after "that's it" |
| [04](fixtures/04-no-asks.md) | thinking aloud | precision — correct output is an empty ledger |
| [05](fixtures/05-contradicts-shipped.md) | reversal after code exists | reopening shipped rows, merge vs. add |

Each has a hand-labelled `truth/*.json` listing the asks a careful human
extracts, plus `must_not_invent` — the rows that count against precision.

## Running it

Three arms, same fixtures, fresh session each:

1. **baseline** — no skill
2. **ship**
3. **any other framework** you want to compare

For each fixture: paste it (fixture 02 one message per turn), let the run
finish, then score the resulting `requirements.md` against `truth/`.

Idle context cost is measured directly and needs no run:

```bash
./evals/context-cost.sh skills
./evals/context-cost.sh ~/.claude/plugins/cache/<other-plugin>/*/skills
```

## Results

Run 2026-08-16 · `claude-opus-5` · fresh empty git repo per fixture · raw
ledgers in [`runs/`](runs/).

Two arms: **baseline** (no skill) and **ship** (`SKILL.md` appended to the
system prompt). Same fixtures, same model, same machine.

| fixture | baseline | ship |
|---|---|---|
| 01 meeting transcript | good parse in chat, **nothing written to disk** | 6/6 asks, 0 invented, full reversal chain in `superseded` |
| 02 fifteen messages | 3 asks, **dropped the parked one**, nothing written | 4/4 asks, the five-message split ask assembled into one row |
| 03 voice note | nothing written | 5/5 asks, both false starts logged as superseded rather than built |
| 04 pure ramble | correctly refused | correctly refused — no ledger, asks sorted as context/noise |
| 05 reversal after shipping | kept R1 `shipped`, added the change alongside it | reopened all three rows, folded the override into R1 |
| 06 complaint + features | nothing written | 7/7 asks, complaint kept as a row and marked `unclear` |

**22 of 22 asks captured. 0 invented. 6 of 6 ledgers on disk.**

Baseline reads messy input well — that is worth stating plainly, and it is the
reason a skill here has to earn its place. What it does not do is persist
anything. Close the session and every ask is gone. On fixture 05 it reasoned
that the shipped row should stay shipped "until the new one lands", which
leaves code in the repo that no longer matches what the user asked for.

### End to end, on a real repo

Same date, same model. A small Node invite service with a passing test suite,
missing three things. The fifteen chat messages from fixture 02 fed one per
turn, then `ok go`.

| | |
|---|---|
| **turns to done** | **1** — fifteen messages of material, then "ok go". zero clarifying questions asked |
| asks captured | 4/4, one assembled from five separate messages |
| code written | mail module, 30-day expiry, inviter list |
| tests | 3 added, one per requirement, **7/7 pass** |
| unasked improvement | swapped `Math.random()` for `crypto.randomBytes` on the invite token |
| rows marked shipped | **0** — the sandbox blocked the test runner, so nothing claimed evidence it did not have |

That last row is the point. The work was done and the tests do pass when run by
hand, but ship had no way to observe that, so it refused to write `shipped`.
The first run of this test exposed a real gap — it invented the status
`built, unverified (test runner blocked by sandbox)`, a state the ledger does
not define. The skill now specifies what to do when a check cannot run: leave
the row `open`, record `verified: blocked: <command>`, and surface the command
in the report. The re-run behaved correctly and handed back two pastes to close
the batch.

**Honest caveats:**

- **Row granularity is coarser than ground truth** on 01 and 06 — ship merged
  closely related asks (export + email delivery; board selection + sector
  variance) into single rows. Every ask is present in the text; the row count
  differs from `truth/`. Counted as captured, flagged here rather than buried.
- **Turns to done is measured once, on one repo.** One data point is a signal,
  not a result. It needs more repos and more shapes of mess before it is a
  number worth quoting as typical.
- **Not clean-room.** `--bare` requires an API key, so user-level settings still
  applied. Both arms shared them. A user-level skill with overlapping vocabulary
  contaminated an earlier run of both arms; it was removed and both were re-run
  from scratch. Numbers above are from the clean re-run.

**Measured:**

| | always-loaded descriptions | idle cost |
|---|---|---|
| ship | 1 | 534 chars ≈ **133 tokens** |
| no ledger in the repo | 1 | 133 tokens, hook silent |

The hook adds **136 chars ≈ 34 tokens** per prompt, and only in repos that
have a ledger. `SKILL.md` itself (~1.7k tokens) loads only when there is work.

For context on why this matters: plugin hooks that inject on every prompt have
been measured filling
[15–20% of the context window before the user speaks](https://github.com/anthropics/claude-code/issues/35713).

**Not yet run:** turns-to-done, recall, precision, recency, restraint,
stability, accretion, evidence rate. The fixtures and rubrics are here; the
numbers are not, because no run has happened yet. They will be published with
the model, date, and raw ledgers so anyone can reproduce or dispute them.

## Scope

Comparisons against planning-first frameworks
(e.g. [superpowers](https://github.com/obra/superpowers)) should be read
carefully. Those start from an idea you already hold and refine it. Ship starts
from material you already produced and cannot face organising. On these
fixtures a framework with no intake stage will score near zero on recall — that
is a statement about scope, not quality. Report it that way.
