# 🚢 Ship

**A model-agnostic way for messy people to get things done — out of the box.**

Drop a brain dump, a chat thread, or a changing list of asks. Ship keeps the
current work in a small `SHIP.md` checklist, handles corrections and cancellations,
and keeps going until each ask has observable proof. A fresh session or another
model can pick up where the last one stopped.

## Install

Claude Code:

```text
/plugin marketplace add 0ss/ship
/plugin install ship@ship
```

For other agents, copy [`skills/ship`](skills/ship) into your agent's skill
directory (for example, `.agents/skills/ship` in your project).

## Use it

In your project, send the agent:

```text
/ship Here's the messy version: invite guests by email, fix Arabic names on
the guest list, and export a CSV. Oh wait—legal says SMS only, not email.
Finish it and run the checks.
```

Keep talking normally: `Forget the CSV export. Make invites expire after 14 days.`
Ship updates the same checklist and works on the latest asks. In a new chat or
with another model, say: `Read SHIP.md and finish what's still open.`

The file in your project will look like:

```markdown
# Ship
- [ ] Send invite SMS — "legal says SMS only" (was: email) — implemented: notifier wired; next: verify delivery
- [x] Show Arabic names — verified: opened guest list → Arabic record → full name displayed
- ~~CSV export~~ — dropped: "forget the CSV thing"
- [ ] Expire invites after 14 days
```

For non-Claude agents, use the same prompt without `/ship`: `Use the ship skill.
Here's the messy version: ...` Ship uses your agent's existing tools; only
verified user journeys get checked off. No service or runtime dependency.

[Benchmark and limits](evals/README.md) · Verify this repo: `./scripts/validate.sh`

MIT licensed.
