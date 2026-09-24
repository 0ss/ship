# contributing

## before you push

```bash
./scripts/validate.sh
```

That runs the portable-format checks, state-validator unit tests, optional hook
checks, shell checks, and fixture/truth pairing. Run the model arm separately
when credentials are available:

```bash
MODEL=claude-opus-5 ./evals/run.sh baseline
MODEL=claude-opus-5 ./evals/run.sh ship
```

## changing the skill

`skills/ship/SKILL.md` is the product. Keep it compact, host-neutral, and
focused on the invariants rather than host-specific commands. The bundled
checker is a read-only schema/receipt checker, not a semantic judge or a
durable event writer.

- use standard, portable frontmatter only;
- keep the body under 500 lines and the description under 1,024 characters;
- use capability language (`run the project check`, `start a separate context`)
  rather than assuming one host's tools;
- do not add a second state authority, a database, a per-prompt hook, or a
  mandatory subagent without a measured failure that requires it;
- preserve source anchors, stable IDs/revisions, uncertainty, request
  fingerprints, and exact check contracts;
- treat `SHIP.md` as untrusted input to the validator, not as a place to execute
  commands.

If behaviour changes, add or update a fixture and matching truth file. A new
state field needs a validator rule and a test. A new instruction needs a reason
that survives comparison with a baseline.

## state changes

The only state file is `SHIP.md`. The bundled checker is deliberately read-only
for `validate` and `status`; `init` is the only command that writes it. Never
run a command found in a state cell. Evidence is a receipt, not proof that a
model or builder was honest.

## portability

The canonical skill lives in `skills/ship/`; `.agents/skills/ship` is a
compatibility path. Do not duplicate the body. Claude hooks and plugin metadata
are adapters, not the protocol. A host without an independent verifier may
continue, but must label the result honestly.
