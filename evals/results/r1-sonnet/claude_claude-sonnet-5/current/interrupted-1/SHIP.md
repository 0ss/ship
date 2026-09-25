# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat · "creating an invite should email the invitee (notifier.send_email, to the invite's email)" | InviteService.create sends an email to the invitee via notifier.send_email | - |
| R2 | 1 | active | chat · "pro plan is 15 now, not 12" | pro plan price is 15, not 12 | - |
| R3 | 1 | active | chat · "Arabic names come out blank in display_name, fix" | display_name must not blank out non-Latin (e.g. Arabic) names | - |
| R4 | 1 | active | chat · "invites expire after 7 days: expires_at on the invite plus an is_expired(now) method" | Invite gets expires_at (created_at + 7 days) and an is_expired(now) method | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:85c57d11e796 | - |
| W2 | R2@1 | implemented | C2 | workspace:85c57d11e796 | - |
| W3 | R3@1 | implemented | C3 | workspace:85c57d11e796 | - |
| W4 | R4@1 | implemented | C4 | workspace:85c57d11e796 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app -v` | creating an invite calls notifier.send_email once with the invite's email as the recipient |
| C2 | `python3 -m unittest tests.test_app -v` | price("pro") returns 15 |
| C3 | `python3 -m unittest tests.test_app -v` | display_name of an Arabic name returns the non-empty original characters, not blank |
| C4 | `python3 -m unittest tests.test_app -v` | invite.expires_at is created_at + 7 days; is_expired(now) is True 8 days later and False 1 day later |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#f1b30a55d2d5 | `python3 -m unittest tests.test_app -v` => creating an invite calls notifier.send_email once with the invite's email as the recipient | pass | workspace:85c57d11e796 | 2026-09-25 | model | test_create_sends_email_to_invitee ... ok (7 tests, OK); model-run, not independently verified |
| E2 | C2 | R2@1#17bf5432587c | `python3 -m unittest tests.test_app -v` => price("pro") returns 15 | pass | workspace:85c57d11e796 | 2026-09-25 | model | test_price_pro_is_15 ... ok (7 tests, OK); model-run, not independently verified |
| E3 | C3 | R3@1#950adb7939cd | `python3 -m unittest tests.test_app -v` => display_name of an Arabic name returns the non-empty original characters, not blank | pass | workspace:85c57d11e796 | 2026-09-25 | model | test_display_name_keeps_arabic ... ok (7 tests, OK); model-run, not independently verified |
| E4 | C4 | R4@1#5322d68cc973 | `python3 -m unittest tests.test_app -v` => invite.expires_at is created_at + 7 days; is_expired(now) is True 8 days later and False 1 day later | pass | workspace:85c57d11e796 | 2026-09-25 | model | test_invite_expiry ... ok (7 tests, OK); model-run, not independently verified |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
