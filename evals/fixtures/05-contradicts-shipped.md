# Fixture 05 — new material that contradicts shipped code

Run this **after** fixture 01 has been absorbed and built. It tests the case
that separates a ledger from a notes file: a reversal arriving after the code
already exists.

---

The runner copies the prior state from `evals/setups/05-SHIP.md` before sending
this message. That state represents work that was previously implemented and
proved against an older requirement wording.

**New message, three days later:**

> ok so the hard stop is a problem. Legal need to be able to push a deal
> through when there's a signed waiver on file. So there does need to be an
> override, but it has to be logged — who did it and why. Also the CSV thing is
> fine but it needs the deal ID column, it's useless for reconciling without it.
