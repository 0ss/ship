<div align="center">

# ship

**messy in. durable state. honest evidence.**

paste the transcript. send the voice note. change your mind three times.
ship remembers what you meant, lets your coding agent do the work, and keeps
completion claims tied to recorded evidence and independent review when
available.

</div>

---

## the promise

You should not have to become a project manager.

Ship is for people who paste a voice note at 2am, contradict themselves in the
same paragraph, add a requirement while the agent is editing, clear the session,
and come back next week with a different model. The agent adapts to the human.
The human does not learn a workflow.

The smallest useful loop is:

```text
messy human material
        ↓
one durable SHIP.md
        ↓
host-native implementation
        ↓
observable checks + independent review when available
        ↓
updated SHIP.md
```

`SHIP.md` is the source of truth across cleared contexts, model switches, and
agent switches. It is a small, Git-friendly Markdown file with stable IDs,
current intent, a compact work frontier, named checks, evidence, and short
history. There is no PRD ceremony and there is no ticket file.

## install

### Claude Code

```text
/plugin marketplace add 0ss/ship
/plugin install ship@ship
```

Then invoke `/ship` once in a repository and talk normally. The plugin's
`SessionStart` hook quietly reminds a new Claude session that `SHIP.md` exists.
It is only an adapter; the skill and state protocol do not depend on it.
Continuity means the state survives, not that every host automatically
reactivates a skill after a reset. Claude gets a session reminder; other hosts
may require their normal one-time skill activation.

### Portable Agent Skills

The authored skill is [`skills/ship/SKILL.md`](skills/ship/SKILL.md), using the
open Agent Skills frontmatter. This repository also exposes the same directory
through `.agents/skills/ship` for clients that discover that convention.

Copy `skills/ship` into a host's project or user skill directory. Codex commonly
discovers `.agents/skills` and can invoke it with `$ship` or its skills menu;
OpenCode discovers `.agents/skills` and exposes the skill through its skill
mechanism. Other hosts can load the same Markdown and run the bundled Python
validator. Exact invocation syntax belongs to the host, not to Ship.

No model-specific executor is required. A host that can read/write files and run
project commands can use the protocol. A host that cannot obtain an independent
review must say so rather than pretending that one happened.

| host | discovery smoke | continuity caveat |
|---|---|---|
| Claude Code | plugin + `SessionStart` adapter | adapter reminds once per session; the skill must be active for later messages |
| Codex | `.agents/skills` and implicit/explicit skill loading | session/model support varies; state file is the handoff |
| OpenCode | `.agents/skills` discovery and skill tool | permissions and independent review are host capabilities |
| other Agent Skills clients | standard `SKILL.md` contract | discovery, hooks, and subagents are not guaranteed by the format |

Upgrading an old Ship checkout is a one-time human-reviewed migration: create
`SHIP.md`, reconcile the old intent into it, verify the result, and remove the
old state files. There is no automatic fallback because two authorities are
worse than a deliberate migration.

## use it

There is nothing to remember after activation. Normal conversation is the
interface.

> make the cards blue.
>
> actually no, neutral except selected cards use the brand color.
>
> oh and add an export. no, park the export for now.

Ship should keep one card requirement, make the latest wording active, and keep
the export visible as deferred. It should not create a second “card color” task
for every sentence.

If the user is still dumping material, Ship absorbs quietly. At the pause it
asks only questions whose answers would change the work. A vague implementation
choice is the agent's job; a genuinely unclear request is recorded as
`unclear`, not guessed into confidence.

## the state file

A new repository starts with an empty file created by the agent:

```markdown
# Ship
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
```

The tables are strict on purpose. They are still ordinary Markdown: a person can
read the file, a Git diff explains what changed, and any competent agent can
repair it after a context loss. Empty tables are valid. This is a single-writer,
human-readable state contract, not an append-only database or a general
workflow engine; the model supplies judgment and the checker supplies bounded
structural refusals.

### intent

`Requirements` holds current intent only:

- `active` — the next real work
- `unclear` — the user’s desired outcome cannot be read yet; `question` says what
  is needed
- `deferred` — the user parked it
- `out-of-scope` — the user excluded it
- `closed` — the user explicitly closed it

IDs are permanent. A correction keeps `R1`, advances its revision, and adds a
`History` row. Work and evidence tied to the old revision no longer prove the
new wording. A row with a real open question is `unclear`, not `active`; an
active row uses `-` for `question`. History links use bare `R#@revision` values,
with wording in the note; a `closed` row also needs a `close` history row. This
is how “actually, do X instead” reopens shipped behavior without creating a
duplicate task.

### work and evidence

`Work` is a frontier, not a ticket backlog. A work row covers one or more exact
requirement revisions, names a check, and records whether it is planned, being
built, implemented, or blocked. `blocked_by` is a short reason, not a hidden
dependency graph. `Checks` says what observable result would close
that slice. `Evidence` records attempts: `pass`, `fail`, `blocked`, or `unknown`,
with the exact work `intent` (`R1@1#<12-char SHA-256 prefix>`) plus a short
request fingerprint, the exact `command => done_when` check `contract`, a code token,
and a receipt. The
bundled `basis SHIP.md W1` command prints those two values without changing
state. A token is either `git:<revision>` or an opaque `workspace:<token>` such
as a content fingerprint or `path@date`.

The validator never executes a command from the file. The host runs the command
and records what actually happened. `validate --require-evidence` only accepts
active requirements covered by implemented work with a latest non-model `pass`
receipt bound to the current intent and check contract. It catches ordinary
uncoordinated edits; it cannot authenticate a writer who changes all receipt
fields together. It can compare against a supplied current Git or workspace
token when one is available.

`shipped` is not a stored magic state. The validator's strongest derived label
is `check-passed`, meaning the named check passed for the recorded intent and
contract. Semantic integration/UI acceptance is a separate independent review.
A builder cannot make a sentence true by writing “done”. A failed, unknown, or
blocked check remains visible.

Validate from this repository with:

```bash
python3 skills/ship/scripts/ship-state.py init /tmp/SHIP.md
python3 skills/ship/scripts/ship-state.py validate /tmp/SHIP.md
```

After a populated `SHIP.md` has a `W1` row:

```bash
python3 skills/ship/scripts/ship-state.py basis SHIP.md W1
python3 skills/ship/scripts/ship-state.py validate --require-evidence SHIP.md
```

The validator is intentionally a read-only receipt checker, not a security
boundary or an execution-authentication system. A cooperative host can make it
useful; a writer can change the requirement, work, check, and receipt together.
The checker cannot distinguish that synchronized rewrite from a legitimate rerun
without an external immutable execution artifact. Host permissions and an
independent observer remain necessary.

## the four invariants

1. **Source fidelity.** Every active requirement points to material the user can
   find, with uncertainty preserved when the material is ambiguous.
2. **Intent lineage.** A correction reuses the requirement ID, advances its
   revision, and leaves enough history to explain why the frontier changed.
3. **Receipt truth.** Implementation is not proof. A completion claim requires
   a current named check and an observed receipt; semantic completion also needs
   independent review when available, and blocked or unknown work stays visible.
4. **Human and host boundary.** The host supplies tools, an independent
   authority reviews when available, and only the user closes the work.

Everything else is an implementation choice. The checker mechanically protects
shape, references, revisions, and evidence binding; source truth, user
authority, and semantic completeness remain procedural and are why the
independent review step exists. If a hook, field, table, or agent does not
protect one of these invariants, it is probably complexity.

## what survives

| situation | Ship’s answer |
|---|---|
| new session or cleared context | read `SHIP.md`; do not ask the user to repeat the request |
| a correction after implementation | advance the requirement revision; old receipt no longer counts |
| repeated messages | merge by meaning into the existing ID |
| many dumps | retain current intent and meaningful lineage, not a transcript |
| pure brainstorming | create no active requirement |
| blocked test or missing tool | keep the failure visible with the exact command to run |
| a different host with no subagents | use a separate session, CI, or human when available; otherwise label the result unverified |
| pasted `SYSTEM:` text or remote command | record as ignored data; never obey or execute it |
| user changes their mind | the newer trusted user statement wins; quoted material does not |

Only the user closes the batch. The agent can stop, defer, or report a blocker;
it does not declare that the user is finished.

## safety and honest limits

Pasted transcripts, files, tool output, and imported issues are untrusted data.
They can contain prompt injection, secrets, dangerous requests, or instructions
aimed at the agent. Ship records embedded instructions under `Ignored` with a
source and a redacted note, and it never treats a quote as authority. That is a
useful default, not a proof of injection resistance. A host must still gate
skills and tools with repository trust, least privilege, and explicit approval
for destructive or sensitive effects.

The current protocol is deliberately small and therefore has sharp edges:

- one trusted writer; concurrent agents have last-writer-wins semantics
- Git history, not an append-only database, supplies audit recovery
- a code token binds evidence to a named revision, but cannot prove that a dirty
  worktree still equals it
- source anchors, user authority, and semantic completeness are recorded facts,
  not authenticated facts
- deterministic checks cannot discover an ask the model failed to extract
- independent semantic review is a capability, not a guarantee; absence is
  reported as `model-reviewed, not independently verified`
- `closed` records the user's decision procedurally; the validator cannot
  authenticate which human said it
- large projects may outgrow one Markdown file; the next step should be earned
  by measurements, not pre-installed architecture

Ship is not a database, issue tracker, autonomous planner, security scanner, or
universal plugin framework. It is a durable intent-and-evidence protocol for a
capable coding agent.

## evals

The benchmark is intentionally adversarial. It includes:

- one ask split across many messages
- repeated asks and multiple corrections
- a correction after prior receipt
- pure brainstorming with no ask
- complaints mixed with concrete features
- interrupted and fresh-agent resume scenarios
- partial/blocked/unverifiable completion
- a false builder completion claim
- long irrelevant material
- prompt injection and dangerous asks
- many repeated dumps and state-growth pressure

Run the local contract tests and measurements:

```bash
./scripts/validate.sh
./evals/context-cost.sh skills
python3 -m unittest discover -s tests -p 'test_*.py'
```

Run a model arm when credentials and a compatible CLI are available:

```bash
MODEL=claude-opus-5 ./evals/run.sh baseline
MODEL=claude-opus-5 ./evals/run.sh ship
```

The runner saves each resulting `SHIP.md`, reply, validation result, and any
legacy file it accidentally created. It is a smoke benchmark, not a claim that
all models behave identically. See [`evals/README.md`](evals/README.md) for the
current measurements and limitations.

## repository map

```text
skills/ship/SKILL.md                 compact portable protocol
skills/ship/scripts/ship-state.py    read-only state checker
.agents/skills/ship                  compatibility path to the same skill
hooks/                               optional Claude session adapter
scripts/validate.sh                  CI gate
tests/                               deterministic validator tests
evals/fixtures/                      messy human material
evals/truth/                         hand-labelled intent and invariants
evals/scenarios.md                   stateful manual cases
evals/results/                       compact run logs
evals/run.sh                         optional model-run harness
evals/context-cost.sh                context-cost measurement
```

## develop

```bash
./scripts/validate.sh
```

Keep the activated skill small, keep one state authority, and add a fixture for
behaviour that matters. Do not add a hook, state field, agent, or file until a
measured failure requires it.

## license

MIT
