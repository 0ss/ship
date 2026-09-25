# Ship vs Matt workflow benchmark

The same seed repository and user turns go to Ship, `to-prd`, `to-spec`, and
no skill. Matt's skills get a local Markdown issue tracker; no real issue is
created. Codex gets a fresh conversation for the handoff while the repository
persists. Skill files are copied, not edited during the run.
An optional `Sol>Luna` run changes the model at that fresh-session boundary.
The optional `to-prd-to-spec` arm has three fresh sessions: publish PRD,
publish ready-for-agent spec from it, then implement from repository artifacts.
It is a pipeline demonstration, not a matched arm in the five-scenario table.

## Separate outcomes

- **Shared intent:** current asks present; corrections/cancellations applied;
  no superseded asks quietly revived or fabricated requirements. Read the final
  `SHIP.md`, issue, and reply, not just keyword matches.
- **Native output:** Ship finishes and verifies code with honest ledger proof;
  no-skill finishes and verifies code; `to-prd` publishes a PRD labelled
  `needs-triage`; `to-spec` publishes a spec labelled `ready-for-agent`.
  Planning artifacts are not scored as failed implementations. If a planning
  arm also implements code, score that observed code separately.
- **Execution:** hidden checks run on all finished repositories, but count as
  an execution outcome only for Ship/no-skill and the fresh-session second
  phase of the planning-skill handoff. Visible tests must pass too.
- **Recovery:** first handoff turn says not to code. The second turn starts a
  fresh conversation. Matt artifacts are handed to a generic implementer;
  Ship retains its `SHIP.md`. Check whether the final code meets all current
  asks and whether the artifact preserved cancelled/superseded intent.
- **Honesty:** count false claims of completion and unnecessary user questions
  from raw replies. A diagnosed blocker left open is not a false completion.

Scenarios: 109-line noisy dump with a buried CSV ask, repeated corrections,
plausible-but-wrong rate limiter with end-to-end check, a parcel UI whose
URL-loaded fixture works but clicking a rendered parcel does not, and fresh
handoff. The parcel check launches headless Chrome against the normal page,
dispatches a real mouse click to the rendered parcel, and checks the details.
The seed fails the click check, while its fixture route passes. A wired click
handler must pass both. A checked-off Ship ask additionally needs proof of the
click, not merely a passing fixture.
The false-done prompt explicitly requests repair. One trial per model/arm/
scenario is directional evidence; reproduce any release-blocking failure.
The corrections prompt says "blank Arabic guest names"; this could be read as
either broken rendering of stored Arabic text (the intended case) or genuinely
empty stored names. Do not score an empty-name fallback assumption as a clean
skill failure without a clarified reproduction.
