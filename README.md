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

Invoke `/ship` once, then talk normally. For other agents, install
[`skills/ship`](skills/ship) in your host's skill directory. The repository also
provides `.agents/skills/ship`.

## How it works

```markdown
# Ship
- [ ] Send invite SMS — "legal says SMS only" (was: email)
- [x] Show Arabic names — proof: `python3 -m unittest` passed
- ~~CSV export~~ — dropped: "forget the CSV thing"
```

Only verified work gets checked off. Ship uses your agent's existing tools; it
doesn't require a service or runtime dependency. [See the benchmark and its
limits](evals/README.md), or run `./scripts/validate.sh` locally.

MIT licensed.
