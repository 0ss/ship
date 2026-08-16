<div align="center">

# 🚢 ship

**Be as messy as you actually are.**

Paste the transcript. Send the voice note. Ramble across fifteen messages.
Ship turns it into a requirements ledger, builds it, and proves it worked.

*One word. One file. One skill.*

</div>

---

## 😖 The problem

Every agentic framework assumes you arrive organised.

You don't. You have a 40-minute meeting transcript, a WhatsApp thread where one
idea is split across five messages, a voice note with no punctuation, and a
thing you changed your mind about twice.

So you clean it up first. You write the tickets. You file the issues. You run
the planner, then the implementer, then the reviewer. Five skills, five
approval gates, and you're the one holding it all together.

**Ship deletes that job.**

```diff
- /clarify → /to-spec → /to-tickets → /to-issues → /implement → /code-review
+ just talk
```

## 🚀 Install

```bash
/plugin marketplace add 0ss/ship
/plugin install ship@ship
```

Then, once per repo:

```
/ship
```

That's the last time you type anything. Ship creates `requirements.md`, and
from then on the file's existence turns the skill on by itself — every session,
forever. Delete the file to turn it off.

## 💬 What it actually looks like

```
you   [pastes 800 words of meeting notes]
ship  +R1 +R2 +R3 +R4 · R2 unclear, I'll ask at the end. keep going.

you   oh also the export is broken
ship  +R5

you   [pastes a screenshot transcript]
ship  +R6 +R7 · R3 superseded — you said weekly, this says daily. taking daily.

you   no wait weekly was right
ship  R3 back to weekly.

you   ok go
ship  one question — R2 "make it cleaner": remove the sidebar? (y/n/other)

you   y
ship  building R1–R7...

      ✅ 6 shipped, evidence on each
      ⚠️  R4 partial — the email path needs an SMTP key you haven't set
      🔍 found an ask I'd missed in your meeting notes: "…and obviously it
         needs to email them". added as R8, building it now.

      done? or keep going.
```

You typed four things. Two of them were "ok go" and "y".

## 🧠 How it works

Every message you send runs the same four steps:

```
1. read requirements.md from disk
2. sort what you said → ask / context / decided / noise
3. merge each ask into the ledger
4. print one line so you can see it landed
```

Then the work happens in three passes, none of which you name:

| pass | question | source of truth |
|---|---|---|
| **absorb** | what did you ask for? | your messages |
| **build** | does it exist? | the codebase |
| **prove** | is that true? | your original material, re-read |

**Prove runs in a fresh subagent.** A verifier that watched itself write the
code confirms its own inventory instead of checking it. So proving gets a
clean head — and because it re-reads your *original* mess rather than the
ledger, it catches asks the ledger missed.

## 📒 The ledger

One file, `requirements.md`, in your repo root. Human-readable, git-friendly,
the entire state of the system.

```markdown
| #  | requirement                        | source          | covers | state   |
|----|------------------------------------|-----------------|--------|---------|
| R1 | hard stop before diligence spend   | voice-1 02:14   | T3     | shipped |
| R2 | sortable table columns             | wa sat 21:03    | —      | unclear |

## superseded
- R1 "stop before spend" → "warn, then stop" → "hard stop" (sun 11:02)

## not asked for
- caching layer — my idea, nobody asked
```

Row IDs are permanent. Evidence links to them, so R7 stays R7 forever.

## ⚖️ Conflicts resolve themselves

| what happened | what ship does |
|---|---|
| you contradict yourself | most recent wins, old version kept under `superseded` |
| you contradict your contradiction | that's just newer. wins. |
| you contradict **already-shipped code** | row reopens, code gets fixed next build |
| you repeat yourself | merges into the existing row, no duplicate |
| one ask spread over five messages | assembles into one row |
| genuinely ambiguous | banked, asked **once**, at the pause |

**No question ever interrupts you mid-flow.** If you're sending fifteen
messages, a question after message three wrecks the dump. Questions wait until
you stop.

## ✅ Three guarantees

1. **Nothing you say is lost.** Every sentence becomes a row or is explicitly
   marked noise. Never silently dropped.
2. **Nothing is called done without evidence.** A row is `shipped` only with a
   re-runnable check attached. No evidence means not shipped, and the prove
   pass catches it.
3. **Only you close it.** Ship reopens rows freely. It never decides you're
   finished.

Each is measurable, and each has fixtures in [`evals/`](evals/).

## 📊 Benchmark

The headline metric is **turns to done** — how many times the human has to
intervene. Every other framework optimises output quality; this one optimises
how little you have to do, so that's what it must be judged on.

Five hand-labelled fixtures ship with the repo: a meeting transcript with a
double reversal, a fifteen-message chat thread, an unpunctuated voice note, a
pure ramble whose correct output is an *empty* ledger, and a reversal that
arrives after the code already exists.

Measured today:

| | always-loaded descriptions | idle context cost |
|---|---|---|
| **ship** | **1** | **~133 tokens** |
| ship, in a repo with no ledger | 1 | ~133 tokens, hook silent |

Recall, precision and turns-to-done are **not yet published** — the fixtures
and rubrics are in [`evals/`](evals/README.md), the numbers aren't, because no
run has happened yet. They'll land with model, date and raw ledgers attached.

No invented numbers. That's the deal.

## 🪶 Why it's cheap

Frameworks in this space are criticised for cost, not correctness — plugin
hooks injecting on every prompt have been measured filling
[15–20% of the context window before you speak](https://github.com/anthropics/claude-code/issues/35713).

Ship spends **one** always-loaded description and **one line** per prompt, and
that line only appears in repos that have a ledger. The skill body itself loads
only when there's work to do. In every other repo on your machine, ship costs
nothing.

## 🤔 Why not just use a planning framework?

Different stage of the pipeline.

Planning-first frameworks start from an idea you already hold and sharpen it
through questioning. That's genuinely good, and if you arrive with a clean idea
you should use one.

Ship starts one step earlier — from material you already produced and cannot
face organising. It has no opinion about your idea. It just refuses to lose any
part of it.

They compose fine. Ship gets you a ledger; nothing stops you planning from it.

## 📁 What's in here

```
skills/ship/SKILL.md      the whole skill, ~170 lines
hooks/                    two-line injector, silent without a ledger
evals/fixtures/           five hand-labelled messy inputs
evals/truth/              what a careful human would extract
evals/context-cost.sh     measure any plugin's idle cost, including this one
```

## ❓ FAQ

**Do I type `/ship` every session?**
No. Once per repo, ever. After that the ledger turns it on.

**Can I break it by talking out of order?**
No. There is no order. Rows have states; your messages move them.

**What if I dump while it's building?**
Absorbed as usual. It finishes the ticket in hand, then picks up the change.

**What if my context dies mid-run?**
The ledger is on disk with evidence per ticket. Next session resumes exactly
where it stopped — anything without evidence gets rebuilt, anything with it is
trusted.

**Does it work on a repo that already exists?**
Yes. It reads the code a ticket touches before planning it.

**What if I'm just thinking out loud?**
Nothing gets built. That's [fixture 04](evals/fixtures/04-no-asks.md), and
producing tickets from it counts as a failure.

## 📄 License

MIT
