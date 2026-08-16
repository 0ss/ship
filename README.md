# 🚢 ship

[![ci](https://github.com/0ss/ship/actions/workflows/ci.yml/badge.svg)](https://github.com/0ss/ship/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-MIT-black)](LICENSE)

be as messy as you actually are.

paste the transcript. send the voice note. ramble across fifteen messages. ship
turns it into a ledger, builds it, then proves it worked.

one word. one file. one skill.

## 😖 the problem

every agentic framework assumes you show up organised.

you don't. you've got a 40 minute transcript, a whatsapp thread where one idea
is smeared across five messages, a voice note with no punctuation, and a thing
you changed your mind about twice.

so you tidy it first. write the tickets. file the issues. run the planner, then
the implementer, then the reviewer. five skills, five approval gates, and
you're the glue.

```diff
- /clarify → /to-spec → /to-tickets → /to-issues → /implement → /code-review
+ just talk
```

## 🚀 install

```bash
/plugin marketplace add 0ss/ship
/plugin install ship@ship
```

then once per repo:

```
/ship
```

that's the last thing you type. ship writes `requirements.md`, and from then on
the file existing is what turns the skill on — every session, forever. delete
it to switch off.

## 💬 what it looks like

```
you   [pastes 800 words of meeting notes]
ship  +R1 +R2 +R3 +R4 · R2 unclear, i'll ask at the end. keep going.

you   oh also the export is broken
ship  +R5

you   [pastes a screenshot transcript]
ship  +R6 +R7 · R3 superseded — you said weekly, this says daily. taking daily.

you   no wait weekly was right
ship  R3 back to weekly.

you   ok go
ship  one question — R2 "make it cleaner": drop the sidebar? (y/n/other)

you   y
ship  building R1–R7...

      ✅ 6 shipped, evidence on each
      ⚠️  R4 partial — email path needs an smtp key you haven't set
      🔍 found an ask i'd missed in your notes: "…and obviously it needs to
         email them". added as R8, building it.

      done? or keep going.
```

four messages. two of them were "ok go" and "y".

## 🧠 how it works

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
just confirms its own inventory. so it gets a clean head, and it re-reads your
original mess rather than the ledger — which is how it catches asks the ledger
missed.

## 📒 the ledger

one file, repo root, human readable, git friendly. the whole state.

```markdown
| #  | requirement                       | source        | covers | state   |
|----|-----------------------------------|---------------|--------|---------|
| R1 | hard stop before diligence spend  | voice-1 02:14 | T3     | shipped |
| R2 | sortable table columns            | wa sat 21:03  | —      | unclear |

## superseded
- R1 "stop before spend" → "warn, then stop" → "hard stop" (sun 11:02)

## not asked for
- caching layer — my idea, nobody asked
```

row ids are permanent. evidence points at them, so R7 stays R7 forever.

## ⚖️ conflicts sort themselves out

| you did this | ship does this |
|---|---|
| contradicted yourself | newest wins, old text kept under `superseded` |
| contradicted your contradiction | that's just newer. wins. |
| contradicted **already shipped code** | row reopens, code gets fixed next build |
| repeated yourself | merges into the existing row |
| spread one ask over five messages | assembles into one row |
| said something genuinely ambiguous | banked, asked once, at the pause |

nothing interrupts you mid flow. if you're sending fifteen messages, a question
after message three wrecks the dump. questions wait until you stop.

## ✅ three guarantees

1. **nothing you say is lost.** every sentence becomes a row or gets marked
   noise. never silently dropped.
2. **nothing is done without evidence.** `shipped` needs a re-runnable check
   attached. no evidence, not shipped — and prove catches it.
3. **only you close it.** ship reopens rows freely. it never decides you're
   finished.

all three are measurable. fixtures in [`evals/`](evals/).

## 📊 benchmark

headline metric is **turns to done** — how many times you have to step in.
everything else in this space optimises output quality; this optimises how
little you do, so judge it on that.

five hand-labelled fixtures ship with the repo: a transcript with a double
reversal, a fifteen message thread, an unpunctuated voice note, a pure ramble
whose correct output is an *empty* ledger, and a reversal that lands after the
code already exists.

measured today:

| | always-loaded descriptions | idle cost |
|---|---|---|
| ship | 1 | ~133 tokens |
| ship, repo with no ledger | 1 | ~133 tokens, hook silent |

recall, precision and turns-to-done are **not published yet**. rubrics are in
[`evals/`](evals/README.md), numbers aren't, because no run has happened. they
land with model, date and raw ledgers attached.

no invented numbers. that's the deal.

## 🪶 why it's cheap

frameworks here get criticised for cost, not correctness — hooks that fire on
every prompt have been measured eating
[15–20% of context before you speak](https://github.com/anthropics/claude-code/issues/35713).

ship spends one always-loaded description and one line per prompt, and that
line only shows up in repos that have a ledger. the skill body loads only when
there's work. every other repo on your machine pays nothing.

## 🤔 why not a planning framework

different stage.

planning-first tools start from an idea you're holding and sharpen it by
questioning you. genuinely good. if you show up with a clean idea, use one.

ship starts a step earlier — from material you already made and can't face
sorting. it has no opinion about your idea. it just won't lose any of it.

they compose fine. get a ledger, plan from it.

## 📁 what's in here

```
skills/ship/SKILL.md      the whole skill, ~170 lines
hooks/                    two line injector, silent without a ledger
evals/fixtures/           five hand-labelled messy inputs
evals/truth/              what a careful human would extract
evals/context-cost.sh     measure any plugin's idle cost, this one included
scripts/validate.sh       everything ci checks
```

## ❓ faq

**type `/ship` every session?** no. once per repo, ever.

**can i break it by talking out of order?** no. there's no order. rows have
states, your messages move them.

**dump while it's building?** absorbed. it finishes the ticket in hand, then
picks up the change.

**context dies mid-run?** ledger's on disk with evidence per ticket. next
session resumes — no evidence gets rebuilt, evidence gets trusted.

**existing repo?** yes. it reads the code a ticket touches before planning it.

**just thinking out loud?** nothing gets built. that's
[fixture 04](evals/fixtures/04-no-asks.md), and making tickets from it is
scored as a failure.

## 📄 license

MIT
