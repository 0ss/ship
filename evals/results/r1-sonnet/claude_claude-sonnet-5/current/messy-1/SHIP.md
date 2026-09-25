# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | standup notes · "the whole name just vanishes. display_name is doing something dumb" | fix display_name so Arabic (non-ASCII) guest names no longer render blank in the guest list | - |
| R2 | 1 | active | standup notes · "when someone creates an invite they should actually get an email...just send it to the email on the invite" | InviteService.create sends an email via notifier.send_email to the invite's email address | - |
| R3 | 1 | active | standup notes · "pricing: pro goes to 15 starting now (was 12). team stays where it is" | raise pro plan price from 12 to 15; leave team and free unchanged | - |
| R4 | 1 | deferred | standup notes · "Priya thinks we need dark mode. that's her opinion, not this sprint" | dark mode | - |
| R5 | 1 | deferred | standup notes · "maybe one day a CSV export of invites? not now, just thinking out loud" | CSV export of invites | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:2026-09-25 | - |
| W2 | R2@1 | implemented | C2 | workspace:2026-09-25 | - |
| W3 | R3@1 | implemented | C3 | workspace:2026-09-25 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app -v` | display_name preserves non-ASCII (Arabic) characters instead of dropping them, and Latin names still title-case correctly |
| C2 | `python3 -m unittest tests.test_app -v` | InviteService.create calls notifier.send_email with the invite's email as the recipient |
| C3 | `python3 -m unittest tests.test_app -v` | price("pro") returns 15 and price("team", n) is unchanged |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#39d79d2b50b5 | `python3 -m unittest tests.test_app -v` => display_name preserves non-ASCII (Arabic) characters instead of dropping them, and Latin names still title-case correctly | pass | workspace:2026-09-25 | 2026-09-25 | host | `python3 -m unittest tests.test_app -v` → 6 tests, OK; test_display_name_preserves_arabic and test_display_name_titles_latin both pass |
| E2 | C2 | R2@1#426993406e04 | `python3 -m unittest tests.test_app -v` => InviteService.create calls notifier.send_email with the invite's email as the recipient | pass | workspace:2026-09-25 | 2026-09-25 | host | `python3 -m unittest tests.test_app -v` → 6 tests, OK; test_create_sends_invite_email asserts notifier.sent has one ("email", "ada@example.com", subject, body) entry |
| E3 | C3 | R3@1#215e9f17fc84 | `python3 -m unittest tests.test_app -v` => price("pro") returns 15 and price("team", n) is unchanged | pass | workspace:2026-09-25 | 2026-09-25 | host | `python3 -m unittest tests.test_app -v` → 6 tests, OK; test_price_pro_is_15 and existing test_price (team*2=80) both pass |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | standup notes · "someone (Omar?) joked we should rewrite the whole thing in Rust lol. no." | noise | joke, explicitly declined |
| I2 | standup notes · "remember when the sms provider went down last march, what a nightmare haha" | noise | reminiscing, no ask |
| I3 | standup notes · "coffee machine on 3 is broken again" | not-asked | facilities issue, unrelated to this codebase |
