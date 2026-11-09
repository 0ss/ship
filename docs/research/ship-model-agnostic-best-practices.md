# Ship as a model-agnostic continuity protocol for general users

## Bottom line

Keep Ship as a plain Agent Skill, but treat the skill file as the *procedure* and `SHIP.md` as the *portable continuity record*. Skill standards define packaging and discovery metadata; they do not define a durable task-state or handoff protocol. Therefore Ship's continuity guarantee must be explicit in its own workflow, grounded in repository files rather than any model's session memory, and tested across hosts with fresh contexts.

## Findings and recommendations

### Portable format and discovery

- **Standard requirement:** A skill is a directory with `SKILL.md`, YAML frontmatter, and required `name` and `description`. Name constraints include lowercase letters/numbers/hyphens, a 64-character maximum, and a match with the containing directory. The Markdown body is otherwise unrestricted. [Agent Skills specification](https://agentskills.io/specification)
- **Standard recommendation:** Use progressive disclosure: catalog metadata first, instructions at activation, and supporting resources only as needed; keep the main file under 500 lines and the instructions under about 5,000 tokens. The spec does not require a particular skill installation path. [Specification: progressive disclosure](https://agentskills.io/specification#progressive-disclosure)
- **Host facts:** OpenCode and Codex both discover `.agents/skills/<name>/SKILL.md`; OpenCode also scans `.claude/skills` and `.opencode/skills`. Claude Code uses its own project/personal/plugin locations. Implicit invocation depends on skill descriptions in Codex and Claude Code; OpenCode exposes descriptions in its skill catalog. Explicit invocation mechanisms differ by host. [OpenCode V2 skills](https://opencode.ai/v2/docs/skills), [Codex skills](https://developers.openai.com/codex/skills/), [Claude Code skills](https://code.claude.com/docs/en/skills)
- **Recommendation:** Keep one canonical, host-neutral `SKILL.md` with only standard frontmatter and Markdown instructions; publish/copy it into each host's discovery path. Keep Python as an optional capability with an explicit fallback, and do not make host-specific tool names, slash commands, frontmatter extensions, or memory features part of the protocol.
- **Recommendation:** Tune `description` for both true triggers and near-miss exclusions. Test the metadata alone in new sessions; a correctly written body cannot help when a host never loads it. [Agent Skills: optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)

The user-provided [skills-best-practices guide](https://github.com/mgechev/skills-best-practices) is a useful secondary checklist for short metadata, direct procedural steps, relative resource paths, and evaluation. These are authoring recommendations, not additional Agent Skills format requirements; defer format claims to the [specification](https://agentskills.io/specification).

### State that survives contexts, resets, and delegates

- **Host facts:** Claude Code documents that each session starts with a fresh context; its auto-memory is stored on the local machine and the main conversation's auto-memory is not loaded into ordinary subagents. OpenCode provides session continuation and automatic compaction/summary agents. Such host facilities are useful but have different scopes and behavior. [Claude Code memory](https://code.claude.com/docs/en/memory), [OpenCode V2 CLI](https://opencode.ai/v2/docs/cli), [OpenCode V2 agents](https://opencode.ai/v2/docs/agents)
- **Protocol recommendation:** Make the checked-in state file authoritative across all hosts, models, new sessions, and agents. At each activation and after delegated work: reread state from disk; verify its shape; reconcile new user input against recorded intent; update state before yielding; then report the next action. A context summary or final chat answer is not a substitute for the state file.
- **Protocol recommendation:** State should expose a compact, explicit frontier: stable requirement IDs/revisions and source anchors; current work and its blocker/owner; named checks and acceptance conditions; observed evidence with provenance; correction/decision history; and the exact next action or question. Mark unknown and blocked states directly—never infer success from an agent's prose.
- **Protocol recommendation:** Handoff packets should be self-contained and point to the state file, exact bounded assignment, relevant source/input paths, output artifact, acceptance/check, and current revision. Require a returning agent to report changed paths, work performed, check command and actual result, unresolved issues, and state edits. The coordinator rereads the artifacts and validates before accepting the handoff.

These are Ship protocol recommendations, **not requirements of the Agent Skills specification**. The spec packages reusable instructions; it makes no guarantee that a host reloads a skill on a fresh session or carries conversational context forward. [Agent Skills specification](https://agentskills.io/specification), [Claude Code session memory](https://code.claude.com/docs/en/memory)

### Multi-agent coordination

- **Host facts:** Claude subagents run in separate contexts and are intended to return summaries; Codex supports bounded parallel subagents and warns that each has additional model/tool cost; OpenCode distinguishes primary agents and subagents. These are host-specific orchestration features, not portable skill primitives. [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://developers.openai.com/codex/subagents), [OpenCode V2 agents](https://opencode.ai/v2/docs/agents)
- **Recommendation:** Keep coordination host-neutral: make one coordinator the sole writer of canonical `SHIP.md`; assign agents non-overlapping work/artifacts or read-only review; pass the same state snapshot/revision and a bounded task; then reconcile returned evidence centrally. Where available, enforce the single-writer boundary with path-scoped permissions. Avoid simultaneous writes to the state ledger. Parallelize independent investigations, not dependent edits or shared state transitions.
- **Recommendation:** Delegation is optional. If no subagent capability is available, the main agent follows the same bounded work/check/handoff contract itself. Never claim independent review when the same context/model merely reread its own work.

### Evaluation evidence and user-facing reports

- **Evaluation recommendations from the standard's guide:** Use realistic prompts, edge cases, clean contexts, with-skill versus baseline/previous-version comparisons, observable assertions, concrete evidence for passes, human review for subjective qualities, execution traces, and iteration. Trigger testing should include positive and near-miss prompts and repeated trials because model behavior varies. [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills), [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- **Ship-specific recommendation:** For each supported host/model, exercise intake, correction/reopen, interruption and fresh-session resume, delegated handoff, blocked-check recovery, false completion, and unavailable-skill/validator paths. Start each run in a clean repository/context; preserve prompt, model/host/version, tool trace, state before/after, command output, token/time cost, and failed as well as successful trials. Grade requirement recall and invention against hand-labeled truth; separately validate ledger structure, revision/evidence bindings, actual check result, and recovery from only the durable file. Use repeated trials before making reliability claims; report the measured sample and known gaps.
- **User-facing reporting:** The Agent Skills sources recommend concise, structured instructions and concrete output templates, but do not mandate a user-facing report format. Apply the ADHD-friendly output guidance as an inclusive default for general users, without assuming a diagnosis or making clinical claims: lead with outcome/status, show only the next action and any blocker/decision, keep evidence and uncertainty explicit, and group necessary questions together. Prefer a short scannable report (`Done` / `Next` / `Blocked` / `Evidence`) over a transcript recap. [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices), [Claude skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Repository fit

This checkout has no existing `docs/` or research-note convention. Its current evaluation convention is `evals/README.md`, which already distinguishes structural validation from model behavior, preserves fresh-resume and handoff scenarios, and cautions that current smoke runs are not cross-host reliability evidence. The recommended destination `docs/research/ship-model-agnostic-best-practices.md` follows the requested fallback. [Local evaluation methodology](../../evals/README.md)

## Source list

- [User-provided practical guide](https://github.com/mgechev/skills-best-practices)
- [Agent Skills format specification](https://agentskills.io/specification)
- [Adding Agent Skills support (discovery/activation lifecycle)](https://agentskills.io/client-implementation/adding-skills-support)
- [Skill evaluation guide](https://agentskills.io/skill-creation/evaluating-skills)
- [Skill description optimization guide](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Skill authoring best practices](https://agentskills.io/skill-creation/best-practices)
- [Claude Code skills](https://code.claude.com/docs/en/skills), [subagents](https://code.claude.com/docs/en/sub-agents), [memory](https://code.claude.com/docs/en/memory)
- [Codex skills](https://developers.openai.com/codex/skills/), [subagents](https://developers.openai.com/codex/subagents)
- [OpenCode V2 skills](https://opencode.ai/v2/docs/skills), [agents](https://opencode.ai/v2/docs/agents), [CLI/session controls](https://opencode.ai/v2/docs/cli)
