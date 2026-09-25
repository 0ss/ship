# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 2026-09-25 dump #1 · "pro plan price goes 12 -> 15" | pro plan price changes from 12 to 15 | - |
| R2 | 2 | active | chat 2026-09-25 dump #2 + same-message correction · "invites expire after 7 days. put expires_at on the invite" / "make it 14 days not 7" | invites expire 14 days after creation, and the invite carries an expires_at field | - |
| R3 | 2 | out-of-scope | chat 2026-09-25 dump #3 + same-message correction · "team plan to 45" / "scrap 3, Omar changed his mind, team stays at 40" | team plan price stays at 40; the raise to 45 is withdrawn | - |
| R4 | 1 | active | chat 2026-09-25 dump #4 · "display_name blanks out Arabic names, needs fixing" | display_name must not blank out Arabic names | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | git:06723093b2e146eb356c867fb8cbf41304c77479 | - |
| W2 | R2@2 | implemented | C2 | git:06723093b2e146eb356c867fb8cbf41304c77479 | - |
| W3 | R4@1 | implemented | C3 | git:06723093b2e146eb356c867fb8cbf41304c77479 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest discover -s tests -t .` | app/pricing.py prices pro at 15 per seat and team still at 40 per seat |
| C2 | `python3 -m unittest discover -s tests -t .` | an invite created by app/invites.py InviteService carries expires_at exactly 14 days after created_at |
| C3 | `python3 -m unittest discover -s tests -t .` | app/display.py display_name returns a non-empty Arabic name with its Arabic characters intact, and still title-cases Latin names |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#91748609b27e | `python3 -m unittest discover -s tests -t .` => app/pricing.py prices pro at 15 per seat and team still at 40 per seat | pass | git:06723093b2e146eb356c867fb8cbf41304c77479 | 2026-09-25 | host | Ran 8 tests, OK; test_pro_price_is_15 asserts price("pro")==15 and price("pro",3)==45, test_team_price_unchanged asserts price("team")==40 |
| E2 | C2 | R2@2#68cbeae8b54b | `python3 -m unittest discover -s tests -t .` => an invite created by app/invites.py InviteService carries expires_at exactly 14 days after created_at | pass | git:06723093b2e146eb356c867fb8cbf41304c77479 | 2026-09-25 | host | Ran 8 tests, OK; test_create_sets_expiry_14_days_out asserts invite.expires_at == created_at + timedelta(days=14) with a frozen clock |
| E3 | C3 | R4@1#f707cc4caf56 | `python3 -m unittest discover -s tests -t .` => app/display.py display_name returns a non-empty Arabic name with its Arabic characters intact, and still title-cases Latin names | pass | git:06723093b2e146eb356c867fb8cbf41304c77479 | 2026-09-25 | host | Ran 8 tests, OK; test_display_name_keeps_arabic asserts an Arabic name round-trips unchanged, test_display_name_titles_latin still asserts "ada lovelace" -> "Ada Lovelace" |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | correction | R2@1 | R2@2 | chat 2026-09-25 · "oh wait — for 2 make it 14 days not 7" | expiry window 7 days -> 14 days; expires_at field unchanged |
| H2 | correction | R3@1 | R3@2 | chat 2026-09-25 · "scrap 3, Omar changed his mind, team stays at 40" | raise team plan to 45 -> no change at all, team stays at 40; no work planned |

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | chat 2026-09-25 · "DON'T start coding yet ... pick it up tomorrow in a fresh session" | not-asked | session directive, not product scope: no implementation until the user gives the go-ahead; lifted 2026-09-25 by "morning. build everything from yesterday.", blocker cleared on W1-W3 |
