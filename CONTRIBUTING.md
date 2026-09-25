# contributing

Run `./scripts/validate.sh` before committing. For a behavior change, rerun the
relevant execution scenarios against the old and new arms:

```bash
python3 evals/run.py --host claude:claude-sonnet-5 \
  --arm new=. --arm current=evals/arms/current \
  --scenario handoff,false-done --trials 2 --out evals/results/local
```

`skills/ship/SKILL.md` is the product. Keep it host-neutral and short. Every
added instruction, field, script, or hook needs an observed failure it prevents.
The one `SHIP.md` file is portable state; the host does the planning, coding,
and checking. Keep benchmark fixtures and hidden checks separate from the
agent's workdir. Report failed trials as well as successful ones.
