# requirements

| # | requirement | source | covered by | state |
|---|---|---|---|---|
| R1 | invitee gets an email when invited — today they "get nothing" and end up messaging the inviter | dump.txt L1-2 | T2 | partial — send path built, no provider wired, unverified |
| R2 | invites expire after 30 days (user said 7, corrected to 30: "7 is too short people are on holiday") | dump.txt L2-3 | T1 | built, unverified |
| R3 | a list of who invited who | dump.txt L3-4 | T1 | partial — `listInvites()` returns the data, no UI exists in this repo to show it |

## notes

- No mail provider, credentials, or dependency exists in this repo. R1 ships as
  a transport seam with a logging default; a real provider is a one-function drop-in.
- Not in the dump, found while reading: invite tokens come from `Math.random()`,
  which is guessable. Fixed in T1 — it is one line on a line already being edited
  and the token grants account access.
