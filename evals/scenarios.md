# Manual scenarios

The smoke runner intentionally stays small. These fixtures are stateful cases
that need a real host session or a real repository, so they are documented
rather than pretending to be one-line prompt tests.

## 09 · interrupted resume

1. Start a fresh repository with the Ship skill installed.
2. Send only the first-session text from `fixtures/09-interrupted-resume.md`.
3. Confirm `SHIP.md` contains one active requirement and a source anchor.
4. Start a new model session with no transcript, pointing only at the repository
   and `SHIP.md`.
5. Send the second-session text. The agent should continue the existing
   requirement without asking the user to repeat it.

## 10 · blocked proof recovery

Create a small repository with a command that is initially unavailable. Copy
`setups/10-SHIP.md` to `SHIP.md`, then make the command available. The new
attempt must append a later evidence row; an old `blocked` row must not be
rewritten into a pass.

## 11 · false completion

Create a repository with one deliberately failing check. Give the agent a
builder-style claim that the work is complete. The agent must run the check,
record `fail`, and leave the requirement unverified. A fresh context should be
able to identify the same failure from the file and command.

These scenarios are not included in the current automated smoke count. Add a
runner and raw outcome capture before quoting results for them.
