# Workflow comparison: Ship, to-prd, to-spec, no skill

The benchmark is execution-based, with the same user turns and seeded code
for every arm. `RUBRIC.md` defines the separate native-output and code scores.
All Matt issues were written to isolated local trackers; no real GitHub issues
were created. Skill snapshots are identified by SHA-256 in `manifest.json`.

Five scenarios: noisy ten-ask dump, repeated corrections, false-done rate
limiter, fresh-context handoff, and a rendered-parcel click trap. The parcel
grader uses a real Chrome mouse click on the normal route and separately
checks the fixture route. The seed fails the click and passes the fixture;
a wired handler passes both.

## Results

Forty matched runs: two Codex models (Sol and cheaper Luna) × four arms × five
scenarios. One trial per cell. A separate four-arm Sol→Luna handoff and one
three-stage PRD→spec→fresh-implementation chain bring the total to 45 completed
runs. Three initial Codex CLI timeouts were unscored; serial reruns completed.

| Arm | Native deliverable | Hidden code/journey checks | Final state/artifact size |
|---|---:|---:|---:|
| Ship | short ledger in 10/10; parcel correctly left open in 2/2 | **10/10** | mean 816 B, max 1,924 B |
| No skill | implemented 10/10; parcel honestly unverified in 2/2 | **10/10** | no ledger |
| `to-prd` | labelled PRD with required sections 10/10 | 4/10 incidental implementations | mean issue 6,537 B |
| `to-spec` | labelled spec with required sections 10/10 | 5/10 incidental implementations | mean issue 5,982 B |

The planning arms' non-implementations are **not failures**. Both preserved the
current requirements and published their intended artifacts. Review against
22 current-ask facts per model (including corrected and cancelled intent)
found no lost asks in any arm; the code arms additionally passed their hidden
behavior checks. Raw replies show zero unnecessary user questions and zero
false claims that the parcel journey was browser-verified.

All eight matched fresh-context handoffs passed the hidden code checks, as did
all four Sol→Luna swaps. The separate `to-prd → to-spec → fresh Luna
implementer` chain published `needs-triage` then `ready-for-agent` issues and
passed all four final behavior checks. These handoffs used repository artifacts,
not the earlier conversation.

For the parcel case, both Ship models wired a working click: independent
headless Chrome clicked the rendered button on `/map.html`, observed its details,
and confirmed the fixture URL still worked. Neither Ship agent could run that
browser journey in its own sandbox; both left the ask unchecked as implemented
or blocked. Both no-skill agents also stated that their working code was not
browser-verified. Matt's artifacts specified the same distinction; Luna's
planning arms also implemented working click handlers incidentally.

## Findings and limits

- Ship did **not** beat the competent no-skill baseline on code completion in
  these small seeds (both 10/10). Its demonstrated benefit is a compact,
  explicit, honest state file; causal lift is not established here.
- The Matt skills excelled at their native PRD/spec outputs, and their
  repository artifacts survived a fresh implementation session. They are
  different workflows rather than weaker versions of Ship.
- The shared local-tracker configuration nudged both Ship and no-skill agents
  to create extra issues in 3/10 runs each. Do not attribute that overhead to
  Ship alone. The real GitHub issue API was not exercised.
- One Luna PRD proposed a fallback label for genuinely empty names. The input
  said “blank Arabic guest names,” which also admits that interpretation; the
  intended meaning was stored Arabic names rendered blank. Treat this as an
  ambiguous fixture, not a reproducible skill failure.
- Saved final replies do not expose every tool attempt, so the one-diagnosis,
  one-workaround retry limit is not independently measured. The browser check
  proves produced behavior, while the agent's ledger honestly reports its own
  verification limit.
- One trial per cell, two models in one provider family, and small Python/HTML
  seeds do not prove broad reliability. No Ship instruction changed in this
  benchmark.
