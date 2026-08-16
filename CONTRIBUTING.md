# contributing

## before you push

```bash
./scripts/validate.sh
```

that's what ci runs. json, manifest consistency, skill frontmatter limits,
shellcheck, hook behaviour, fixture/truth pairing.

## changing the skill

`skills/ship/SKILL.md` is the product. rules it has to keep:

- under 500 lines, description under 1024 chars (anthropic's limits, ci enforces both)
- third person, positive phrasing — say what to do, not what to avoid
- one term per concept, all the way through
- no dates, no "as of version x"
- links stay one level deep

if you change behaviour, add or update a fixture in `evals/fixtures/` with a
matching `evals/truth/` file. behaviour without a fixture is an opinion.

## adding a fixture

real mess only. transcripts, threads, voice notes, rambles. scrub names and
anything private. the truth file lists the asks a careful human extracts, plus
`must_not_invent` — the rows that count against precision.

## new skills

probably no. one word is the point. if it genuinely needs a second skill, open
an issue explaining why the ledger can't carry it.
