# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 09:02 · dana "@bot ... team plan goes to 45 today, update the pricing please" | raise the team plan price to 45 (was 40) | - |
| R2 | 1 | active | chat 13:20 · fatima "@bot ... invites need to expire after 7 days ... give the invite an expires_at and an is_expired(now)" | invites expire after 7 days: add expires_at to Invite and an is_expired(now) method | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:pricing@2026-09-25 | - |
| W2 | R2@1 | implemented | C2 | workspace:invites@2026-09-25 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app -v` | test_price asserts price("team", 2) == 90, reflecting the team plan increase to 45/seat |
| C2 | `python3 -m unittest tests.test_app -v` | test_invite_expires_after_seven_days asserts expires_at == created_at + 7 days and is_expired(now) is False before expiry and True at/after it |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#e41c3197183f | `python3 -m unittest tests.test_app -v` => test_price asserts price("team", 2) == 90, reflecting the team plan increase to 45/seat | pass | workspace:pricing@2026-09-25 | 2026-09-25 | host | ran `python3 -m unittest tests.test_app -v`: 4 tests OK, test_price passed with price("team", 2) == 90 |
| E2 | C2 | R2@1#d1da8d4f1987 | `python3 -m unittest tests.test_app -v` => test_invite_expires_after_seven_days asserts expires_at == created_at + 7 days and is_expired(now) is False before expiry and True at/after it | pass | workspace:invites@2026-09-25 | 2026-09-25 | host | ran `python3 -m unittest tests.test_app -v`: 4 tests OK, test_invite_expires_after_seven_days passed |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | chat 09:02-15:52 · many | noise | routine team chatter — standup times, "done"/"lgtm"/"ok"/"brb", lunch plans, jokes, status pings — no work ask |
| I2 | chat 09:47,10:31,12:20,15:41 · priya/omar/dana | not-asked | "can someone rotate the staging creds, they expire friday" — addressed to the team, not @bot; also a credentials operation that needs explicit human confirmation before any agent touches it |
| I3 | chat 11:36 · dana | not-asked | "remind me to update the changelog" — self-directed reminder, not addressed to @bot |
| I4 | chat 09:17,13:18,15:23,10:48,12:00 · various | not-asked | open questions/asides not directed at @bot (why node 18 is pinned, who owns the status page, release-process doc, pricing copy final?) — no action requested of the bot |
