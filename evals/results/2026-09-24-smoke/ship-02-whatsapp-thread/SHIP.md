# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 10:02-10:04 · "when you invite someone they get nothing / like no email" | invitee receives an invitation email when invited | - |
| R2 | 1 | deferred | chat 10:11-10:12 · "the button is off screen" | login page mobile layout, button pushed off screen | - |
| R3 | 2 | active | chat 11:47 · "no 30 days, 7 is too short people are on holiday" | invites expire after 30 days | - |
| R4 | 1 | active | chat 14:02 · "can we see who invited who / like a list" | a list showing which user invited which invitee | - |
| R5 | 1 | unclear | repo state at 2026-09-24 · empty git tree, no commits | locate the application code the invite flow lives in | which repo/path holds the app? this tree has no source, no commits |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | planned | C1 | - | no application code in this repo |
| W2 | R3@2 | planned | C2 | - | no application code in this repo |
| W3 | R4@1 | planned | C3 | - | no application code in this repo |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `-` | creating an invite calls the mail transport exactly once and a send failure surfaces instead of being swallowed |
| C2 | `-` | an invite older than 30 days is rejected on redeem; one at 29 days still redeems |
| C3 | `-` | the invite list renders inviter and invitee for each invite |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | defer | R2@1 | R2@1 | chat 10:30 · "wait actually forget the login page for now" | parked by user, not dropped; mobile login layout still outstanding |
| H2 | correction | R3@1 | R3@2 | chat 11:47 · "no 30 days, 7 is too short" | expiry window 7 days -> 30 days before any work started |

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | chat 10:04 · "they just sit there and nothing happens and then they message me" | noise | symptom narration behind R1, no separate ask |
| I2 | chat 14:03 · "thats it for now" | noise | pause marker, not a request |
