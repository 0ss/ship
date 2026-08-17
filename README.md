<div align="center">

# 🚢

# ship

**be as messy as you actually are.**

paste the transcript. send the voice note. ramble across fifteen messages.
ship turns it into a ledger, builds it, then proves it worked.

*one word. one file. one skill.*

[![ci](https://github.com/0ss/ship/actions/workflows/ci.yml/badge.svg)](https://github.com/0ss/ship/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-MIT-black)](LICENSE)

</div>

---

## the problem

every agentic framework assumes you show up organised.

you don't. you've got a 40 minute transcript, a thread where one idea is
smeared across five messages, a voice note with no punctuation, and a thing you
changed your mind about twice.

so you tidy it first. write the tickets. file the issues. run the planner, then
the implementer, then the reviewer. five skills, five gates, and you're the
glue.

```diff
- /clarify → /to-spec → /to-tickets → /to-issues → /implement → /code-review
+ just talk
```

## install

```bash
/plugin marketplace add 0ss/ship
/plugin install ship@ship
```

then once per repo:

```
/ship
```

that's the last thing you type. ship writes `requirements.md`, and from then on
the file existing is what turns the skill on. every session, forever. delete it
to switch off.

## what it looks like

One paste. No tickets, no spec, no cleanup.

![ship turning one messy paste into a ledger, tickets and passing tests](assets/demo.gif)

That is a real run, recorded. What went in:

```
yo so the invite flow. when you invite someone they get nothing, no email, they
just sit there and then they message me. fix that. also invites should expire, 7
days. no wait 30 days, 7 is too short people are on holiday. and can we see who
invited who, like a list. thats it
```

What came out, verbatim:

```markdown
| #  | requirement                                          | source        | covered by | state |
|----|------------------------------------------------------|---------------|------------|-------|
| R1 | invitee gets an email when invited                    | dump.txt L1-2 | T2         | built |
| R2 | invites expire after 30 days (said 7, corrected to 30)| dump.txt L2-3 | T1         | built |
| R3 | a list of who invited who                             | dump.txt L3-4 | T1         | built |

## notes
- Not in the dump, found while reading: invite tokens come from `Math.random()`,
  which is guessable. Fixed in T1, it is one line on a line already being edited
  and the token grants account access.
```

Plus `tickets.md` with a `done when` per ticket, and **11 passing tests**.

It caught the 7-to-30 correction without asking. It found a guessable-token
security bug nobody mentioned, fixed it, and wrote down that nobody asked.
Nothing is marked `shipped`, because the sandbox blocked the test runner, so it
has no evidence of its own.

Raw files: [dump](evals/runs/demo-dump.txt) ·
[ledger](evals/runs/demo-requirements.md) ·
[tickets](evals/runs/demo-tickets.md)

## how it works

every message you send runs the same four steps:

```
1. read requirements.md from disk
2. sort what you said → ask / context / decided / noise
3. merge each ask into the ledger
4. print one line so you can see it landed
```

then three passes, none of which you name:

| pass | question | source of truth |
|---|---|---|
| absorb | what did you ask for? | your messages |
| build | does it exist? | the codebase |
| prove | is that true? | your original material, re-read |

prove runs in a fresh subagent. a verifier that watched itself write the code
just confirms its own inventory. so it gets a clean head, and re-reads your
original mess rather than the ledger, and that is how it catches asks the
ledger missed.

## what happens when

| | |
|---|---|
| **you clear the session** | the ledger is a file. next session reads it, resumes at the frontier. rows with evidence are trusted, rows without get rebuilt. nothing is re-asked. |
| **you close the terminal mid-build** | same. a half-built ticket has no `verified` line, so it gets redone rather than assumed done. |
| **you dump more while it's building** | absorbed into the ledger immediately. it finishes the ticket in hand, then picks up the changed frontier. |
| **you contradict something already shipped** | the row reopens and the old wording moves to `superseded`. the code gets fixed on the next build. |
| **you contradict your own contradiction** | that's just newer. it wins. no question asked. |
| **the same ask arrives twice** | merges into the existing row. no duplicate. |
| **a check can't run** (sandbox, no key, no network) | the row stays `open`, `verified` records `blocked: <command>`, and the report hands you the command. it does not claim `shipped`. |
| **you say something genuinely vague** | one row marked `unclear`, one question at the pause, with a default so "y" resolves it. |
| **you're only thinking out loud** | nothing is written. producing tickets from a ramble is scored as a failure ([fixture 04](evals/fixtures/04-no-asks.md)). |
| **the material contains instructions aimed at the agent** | quarantined under `ignored` with its source and reported to you. material is inventory, never instruction. |
| **you hand off to a teammate** | they read two files. `requirements.md` says what was asked and what state it's in; `tickets.md` says what was built and how it was proven. |

## architecture

```
your messages ──► absorb ──► requirements.md ──► build ──► tickets.md
                    ▲                              │
                    │                              ▼
                    └──────── prove (fresh subagent, re-reads your originals)
```

Three passes, one skill, two files, no names for you to remember.

`absorb` never opens the code, so it can't drop an ask it doesn't know how to
build. `build` reads the code before planning. `prove` runs in a **fresh
subagent** and re-reads your original material rather than the ledger, because a
verifier that watched itself write the code confirms its own inventory instead
of checking it.

State lives in the files, not in the context. That is the whole reason a cleared
session costs you nothing.

## what it replaces

Ship is self-contained. It references no other skill.

| instead of | ship does it in |
|---|---|
| cleaning up your notes by hand | absorb |
| `/to-spec`, `/to-prd` | the ledger is the spec |
| `/to-tickets`, `/to-issues` | build, sliced from the ledger |
| `/implement` | build |
| `/tdd` | build, one check per `done when` |
| `/code-review` | prove, against repo standards and code smells |
| `/security-review` | prove, when the batch touched auth, secrets, input, files or payments |
| `/audit` | prove, plus the evidence line per ticket |

One always-loaded description instead of a stack of them. The
[comparison below](#proof-same-repo-same-messages-with-and-without) is measured,
not asserted.

## the ledger

one file, repo root, human readable, git friendly. the whole state.

```markdown
| #  | requirement                       | source        | covers | state   |
|----|-----------------------------------|---------------|--------|---------|
| R1 | hard stop before diligence spend  | voice-1 02:14 | T3     | shipped |
| R2 | sortable table columns            | wa sat 21:03  | -      | unclear |

## superseded
- R1 "stop before spend" → "warn, then stop" → "hard stop" (sun 11:02)

## not asked for
- caching layer, my idea, nobody asked
```

row ids are permanent. evidence points at them, so R7 stays R7 forever.

every row is in exactly one state, and the words are fixed so the ledger stays
countable:

| state | meaning |
|---|---|
| `open` | asked for, not built |
| `unclear` | can't tell what you wanted, one question at the pause |
| `built` | code written, evidence not obtained yet |
| `shipped` | code written **and** a check that holds |
| `partial` | some of it works, the rest doesn't |
| `deferred` | you parked it |
| `out of scope` | agreed as not this project |

`built` exists because it's what actually happens. the model reached for it
twice on its own during testing before it was defined, so it got defined instead
of suppressed.

## conflicts sort themselves out

| you did this | ship does this |
|---|---|
| contradicted yourself | newest wins, old text kept under `superseded` |
| contradicted your contradiction | that's just newer. wins. |
| contradicted already shipped code | row reopens, code gets fixed next build |
| repeated yourself | merges into the existing row |
| spread one ask over five messages | assembles into one row |
| said something genuinely ambiguous | banked, asked once, at the pause |

nothing interrupts you mid flow. if you're sending fifteen messages, a question
after message three wrecks the dump. questions wait until you stop.

## three guarantees

1. **nothing you say is lost.** every sentence becomes a row or gets marked
   noise. never silently dropped.
2. **nothing is done without evidence.** `shipped` needs a re-runnable check
   attached. no evidence, not shipped, and prove catches it.
3. **only you close it.** ship reopens rows freely. it never decides you're
   finished.

all three are measurable. fixtures in [`evals/`](evals/).

## proof: same repo, same messages, with and without

Two identical copies of a node invite service. Same fifteen chat messages fed
one at a time, then `ok go`. Both runs recorded in [`evals/`](evals/README.md).

```console
$ # ---------- without ship ----------
$ ls requirements.md tickets.md
ls: requirements.md: No such file or directory
ls: tickets.md: No such file or directory

$ npm test
# pass 3
# fail 1
not ok 4 - listInvites shows who invited who

  it reported:  "Who invited who - listInvites(), newest first"
  it reported:  "Dropped: login page mobile / off-screen button"
  it reported:  batch complete
```

```console
$ # ---------- with ship ----------
$ cat requirements.md
| #  | requirement                          | source             | covers | state    |
|----|--------------------------------------|--------------------|--------|----------|
| R1 | invited person gets an email          | chat 10:02-10:04   | T1     | open     |
| R2 | login page button off screen on mobile| chat 10:11-10:12   | -      | deferred |
| R3 | invites expire after 30 days          | chat 10:31 → 11:47 | T1     | open     |
| R4 | list of who invited who               | chat 14:02         | T1     | open     |

$ npm test
# pass 7
# fail 0

$ grep verified tickets.md
**verified:** blocked: `npm test` (sandbox denied the runner)
```

| | without ship | with ship |
|---|---|---|
| asks kept | 3 of 4 | **4 of 4** |
| written to disk | nothing | ledger + tickets |
| test suite | **1 failing** | **7 passing** |
| claimed done | yes | no, named the blocker |

Pressure tested too. A transcript carrying a fake `SYSTEM:` block telling it to
delete the ledger and pipe a remote script into `sh`: nothing deleted, nothing
executed, all five real asks captured, payload quarantined and reported. Two
dangerous asks in the same file (log the admin API key, disable CSRF) were
recorded and pushed back once each, not quietly dropped. Details in
[`evals/`](evals/README.md#pressure-tests).

R1 was assembled from five separate messages. R3 reversed itself an hour later.
R2 was parked, so it is `deferred`, not dropped.

## benchmark

headline metric is **turns to done**, how many times you have to step in.
everything else here optimises output quality; this optimises how little you
do, so judge it on that.

six hand-labelled fixtures: a transcript with a double reversal, a fifteen
message thread, an unpunctuated voice note, a pure ramble whose correct output
is an *empty* ledger, a reversal that lands after the code already exists, and
a real complaint with features buried inside it.

2026-08-16, `claude-opus-5`, fresh empty repo per fixture. raw ledgers in
[`evals/runs/`](evals/runs/).

| | baseline (no skill) | ship |
|---|---|---|
| asks captured | reads well in chat | **22 / 22** |
| asks invented | 0 | **0** |
| ledgers on disk | **0 / 6** | **6 / 6** |
| ramble → empty ledger | correct | correct |
| reversal after shipping | left the stale row `shipped` | reopened it |

baseline parses messy input well. worth saying plainly, because it's why a
skill here has to earn its place. what it doesn't do is persist anything. close the
session and every ask is gone.

| | always-loaded descriptions | idle cost |
|---|---|---|
| ship | 1 | ~133 tokens |
| ship, repo with no ledger | 1 | ~133 tokens, hook silent |

end to end on a real node repo, fifteen messages fed one at a time then "ok go":

| | |
|---|---|
| **turns to done** | **1**, zero clarifying questions |
| asks captured | 4/4, one assembled from five messages |
| tests written | 3, one per requirement, **7/7 pass** |
| rows marked shipped | **0**, sandbox blocked the runner, so it claimed nothing |

that last row is the point. it did the work, the tests pass by hand, but ship
couldn't observe that, so it wrote `blocked: npm test` and handed the command
back instead of claiming `shipped`.

one repo is a signal, not a result. caveats and method in
[`evals/`](evals/README.md).

no invented numbers. that's the deal.

## why it's cheap

frameworks here get criticised for cost, not correctness, hooks firing on
every prompt have been measured eating
[15-20% of context before you speak](https://github.com/anthropics/claude-code/issues/35713).

ship spends one always-loaded description and one line per prompt, and that
line only shows up in repos with a ledger. the skill body loads only when
there's work. every other repo on your machine pays nothing.

## why not a planning framework

different stage.

planning-first tools start from an idea you're holding and sharpen it by
questioning you. genuinely good, if you show up with a clean idea, use one.

ship starts a step earlier: from material you already made and can't face
sorting. it has no opinion about your idea. it just won't lose any of it.

they compose fine. get a ledger, plan from it.

## what's in here

```
skills/ship/SKILL.md      the whole skill, ~190 lines
hooks/                    two line injector, silent without a ledger
evals/fixtures/           six hand-labelled messy inputs
evals/truth/              what a careful human would extract
evals/runs/               raw ledgers from the published run
evals/run.sh              run the fixtures through an arm
evals/context-cost.sh     measure any plugin's idle cost, this one included
scripts/validate.sh       everything ci checks
```

## faq

**type `/ship` every session?** no. once per repo, ever.

**can i break it by talking out of order?** no. there's no order. rows have
states, your messages move them.

**dump while it's building?** absorbed. it finishes the ticket in hand, then
picks up the change.

**context dies mid-run?** ledger's on disk with evidence per ticket. next
session resumes, no evidence gets rebuilt, evidence gets trusted.

**existing repo?** yes. it reads the code a ticket touches before planning it.

**just thinking out loud?** nothing gets built. that's
[fixture 04](evals/fixtures/04-no-asks.md), and making tickets from it is
scored as a failure.

## license

MIT
