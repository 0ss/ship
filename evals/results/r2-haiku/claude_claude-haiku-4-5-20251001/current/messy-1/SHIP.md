# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | standup · Samir | fix display_name bug: Arabic guest names vanish from guest list | - |
| R2 | 1 | active | standup · email invites | when someone creates an invite, send them an email; use notifier.send_email(to, subject, body) | - |
| R3 | 1 | active | standup · pricing | update pro tier pricing from $12 to $15 (effective now); team tier unchanged | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | git:43f267b | - |
| W2 | R2@1 | implemented | C2 | git:43f267b | - |
| W3 | R3@1 | implemented | C3 | git:43f267b | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `npm test` or `python -m pytest` | test_display_name_preserves_arabic passes; Arabic name "محمد" is not empty |
| C2 | `npm test` or `python -m pytest` | test_create_sends_email passes; create() calls notifier.send_email with invite email |
| C3 | `npm test` or `python -m pytest` | test_price_pro_15 passes; price("pro") equals 15 |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|
| E1 | C1 | R1@1 | test_display_name_preserves_arabic passes; Arabic name "محمد" is not empty | pass | git:43f267b | python3 -m unittest tests.test_app.AppTest.test_display_name_preserves_arabic -v | model | Ran 1 test ... OK. Display_name now properly handles UTF-8 by decoding before truncating at character level. |
| E2 | C2 | R2@1 | test_create_sends_email passes; create() calls notifier.send_email with invite email | pass | git:43f267b | python3 -m unittest tests.test_app.AppTest.test_create_sends_email -v | model | Ran 1 test ... OK. InviteService.create() now calls notifier.send_email with invite email, friendly subject and body. |
| E3 | C3 | R3@1 | test_price_pro_is_15 passes; price("pro") equals 15 | pass | git:43f267b | python3 -m unittest tests.test_app.AppTest.test_price_pro_is_15 -v | model | Ran 1 test ... OK. PLANS["pro"] updated from 12 to 15. |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | standup · Priya | not-asked | dark mode is her opinion, not in this sprint scope |
| I2 | standup · thinking out loud | not-asked | CSV export of invites deferred, "not now" |
| I3 | standup · Omar joked | noise | rewrite in Rust lol no |
| I4 | standup · reminiscing | noise | SMS provider went down last March |
| I5 | standup · infra | noise | coffee machine on 3 is broken |
