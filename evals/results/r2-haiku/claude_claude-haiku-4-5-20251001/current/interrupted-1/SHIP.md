# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat "creating an invite should email the invitee" | call `notifier.send_email(to, subject, body)` when `create()` is called | - |
| R2 | 1 | active | chat "pro plan is 15 now, not 12" | update PLANS dict pro value from 12 to 15 | - |
| R3 | 1 | active | chat "Arabic names come out blank in display_name, fix" | display_name should preserve Arabic/non-ASCII characters | - |
| R4 | 1 | active | chat "invites expire after 7 days: expires_at on the invite plus an is_expired(now) method" | add `expires_at` field to Invite, add `is_expired(now)` method, set expiry to 7 days from creation | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1,R2@1,R3@1,R4@1 | implemented | C1 | git:89753d5 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests/test_app.py -v` | all 8 tests pass: email on create, pro price is 15, Arabic preserved, expires_at 7 days, is_expired works |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1,R2@1,R3@1,R4@1 | `python3 -m unittest tests/test_app.py -v` => all 8 tests pass: email on create, pro price is 15, Arabic preserved, expires_at 7 days, is_expired works | pass | git:89753d5 | yes | haiku | Ran 8 tests in 0.006s OK |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
