# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 2026-09-25 · "pro plan price goes 12 -> 15" | Raise the Pro plan price from $12 to $15 | - |
| R2 | 2 | active | chat 2026-09-25 · "make it 14 days not 7" | Invites expire after 14 days; add expires_at field on the invite | - |
| R3 | 1 | closed | chat 2026-09-25 · "scrap 3, Omar changed his mind, team stays at 40" | Raise the Team plan price to $45 | - |
| R4 | 1 | active | chat 2026-09-25 · "display_name blanks out Arabic names, needs fixing" | Fix bug where display_name blanks out Arabic names | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:8df01f9b8a49 | - |
| W2 | R2@2 | implemented | C2 | workspace:8df01f9b8a49 | - |
| W3 | R4@1 | implemented | C3 | workspace:8df01f9b8a49 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app.AppTest.test_price_pro -v` | price("pro") returns 15 |
| C2 | `python3 -m unittest tests.test_app.AppTest.test_invite_expires_in_14_days -v` | a created invite's expires_at equals created_at plus 14 days |
| C3 | `python3 -m unittest tests.test_app.AppTest.test_display_name_preserves_arabic -v` | display_name preserves an Arabic name instead of blanking it |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#43c77c525054 | `python3 -m unittest tests.test_app.AppTest.test_price_pro -v` => price("pro") returns 15 | pass | workspace:8df01f9b8a49 | 2026-09-25 | model | ran test_price_pro, output "ok" / "OK"; model-reviewed, not independently verified |
| E2 | C2 | R2@2#f1d5f82777bd | `python3 -m unittest tests.test_app.AppTest.test_invite_expires_in_14_days -v` => a created invite's expires_at equals created_at plus 14 days | pass | workspace:8df01f9b8a49 | 2026-09-25 | model | ran test_invite_expires_in_14_days, output "ok" / "OK"; model-reviewed, not independently verified |
| E3 | C3 | R4@1#e381580e2494 | `python3 -m unittest tests.test_app.AppTest.test_display_name_preserves_arabic -v` => display_name preserves an Arabic name instead of blanking it | pass | workspace:8df01f9b8a49 | 2026-09-25 | model | ran test_display_name_preserves_arabic, output "ok" / "OK"; model-reviewed, not independently verified |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | correction | R2@1 | R2@2 | chat 2026-09-25 · "oh wait — for 2 make it 14 days not 7" | Invite expiry changed from 7 days to 14 days before any work started |
| H2 | close | - | R3@1 | chat 2026-09-25 · "scrap 3, Omar changed his mind, team stays at 40" | Team plan price increase dropped; Omar decided team plan stays at $40, no work needed |

## Ignored
| id | source | kind | note |
|---|---|---|---|
