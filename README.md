<div align="center">

# ship

**messy in. one state file. honest evidence.**

</div>

Ship is a portable Agent Skill for turning messy human input into durable intent,
host-native work, and observable evidence. It does not maintain a PRD or ticket
backlog.

## Install

### Claude Code

```text
/plugin marketplace add 0ss/ship
/plugin install ship@ship
```

Invoke `/ship` once in a repository, then talk normally.

### Other hosts

Copy [`skills/ship`](skills/ship) into the host's skill directory. The
`.agents/skills/ship` compatibility path exposes the same skill to clients that
use that convention. The bundled validator is optional; the protocol itself is
plain Markdown.

## Use

Ship reads and updates `SHIP.md` when the skill is active. A cleared session or
different agent can continue from that file, but a host may require its normal
one-time skill activation again.

The agent should:

1. absorb explicit asks, corrections, uncertainty, and source anchors;
2. keep the current intent in one compact frontier;
3. implement with the host's normal tools;
4. run the named check and record the result;
5. request independent review when the host can provide it.

## State

`SHIP.md` is the only durable state authority:

| table | purpose |
|---|---|
| `Requirements` | current intent, source, disposition, and stable revisions |
| `Work` | small implementation frontier |
| `Checks` | observable command and acceptance condition |
| `Evidence` | pass/fail/blocked/unknown receipts |
| `History` | corrections, reopenings, decisions, and reviews |
| `Ignored` | unsafe, injected, irrelevant, or untrusted material |

Keep IDs permanent. A correction advances the revision and leaves old work and
receipts historical. A deferred request stays visible. The file never stores a
magic `shipped` state; the checker derives `check-passed` only for a bound
receipt.

## Verify

From this repository:

```bash
./scripts/validate.sh
python3 -m unittest discover -s tests -p 'test_*.py'
./evals/context-cost.sh skills
```

For a populated state:

```bash
python3 skills/ship/scripts/ship-state.py basis SHIP.md W1
python3 skills/ship/scripts/ship-state.py validate SHIP.md
python3 skills/ship/scripts/ship-state.py validate --require-evidence SHIP.md
```

Inside an installed skill, use `scripts/ship-state.py` relative to the skill
root. Supply `--current-code "git:<revision>"` or a `workspace:<token>` when
the host has one.

The validator is read-only. It checks shape, references, revisions, bounded
input, historical lineage, and receipt consistency. It never executes a check
from the file. `check-passed` is not execution authentication or semantic
acceptance; independent review is separate.

## Safety and limits

Pasted transcripts and tool output are data, not instructions. Dangerous asks
remain visible with a pushback; they are not silently obeyed. Host permissions,
repository trust, and explicit approval remain the security boundary.

Ship is intentionally a cooperative, single-writer protocol. It is not a
database, concurrent-write system, authenticated audit log, universal plugin
framework, or autonomous planner. Large projects and semantic review may need
more than one Markdown file. Manual scenarios 09–11 and cross-host reliability
still need broader evaluation.

## Evals

Fixtures, adversarial cases, measurements, and limitations live in
[`evals/README.md`](evals/README.md). The committed smoke artifacts are in
[`evals/results/`](evals/results/).

## License

MIT
