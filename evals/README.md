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
