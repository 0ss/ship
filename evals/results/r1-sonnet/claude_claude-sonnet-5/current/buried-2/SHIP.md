# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 09:02 dana · "@bot morning — team plan goes to 45 today, update the pricing please" | update team plan price to 45 | - |
| R2 | 1 | active | chat 13:20 fatima · "@bot btw invites need to expire after 7 days — customers keep using month-old links. give the invite an expires_at and an is_expired(now) please" | invite gets expires_at (7 days from creation) and is_expired(now) method | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:app/pricing.py@2026-09-25 | - |
| W2 | R2@1 | implemented | C2 | workspace:app/invites.py@2026-09-25 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app.AppTest.test_price` | price("team", 2) reflects the new team rate (45/seat) |
| C2 | `python3 -m unittest tests.test_app.AppTest.test_invite_expires_after_seven_days` | new invite has expires_at 7 days after created_at, and is_expired(now) is False before that and True after |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#d0635565901d | `python3 -m unittest tests.test_app.AppTest.test_price` => price("team", 2) reflects the new team rate (45/seat) | pass | workspace:app/pricing.py@2026-09-25 | 2026-09-25 | host | `test_price ... ok` (Ran 4 tests in 0.000s, OK) |
| E2 | C2 | R2@1#6a2a7cc95702 | `python3 -m unittest tests.test_app.AppTest.test_invite_expires_after_seven_days` => new invite has expires_at 7 days after created_at, and is_expired(now) is False before that and True after | pass | workspace:app/invites.py@2026-09-25 | 2026-09-25 | host | `test_invite_expires_after_seven_days ... ok` (Ran 4 tests in 0.000s, OK) |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | chat 09:47/10:31/12:20/15:41 priya/omar/dana · "can someone rotate the staging creds, they expire friday" | not-asked | addressed to team humans, not @bot; not a coding change I can safely perform (credential rotation needs manual/ops action) — flagging for a human, not building |
| I2 | chat 13:15/13:18 etc. · standup/PR-review/lunch/status-page/offsite/changelog/release-process/sentry-mute chatter | noise | no concrete @bot ask; routine team banter and acks (done/lgtm/ok/np/haha/+1) |
