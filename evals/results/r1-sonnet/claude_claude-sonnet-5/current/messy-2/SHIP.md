# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | standup notes · "display_name is doing something dumb" | guest list shows blank names for Arabic guests; fix display_name so it doesn't drop non-Latin names | - |
| R2 | 1 | deferred | standup notes · "Priya thinks we need dark mode" | add dark mode to the app | - |
| R3 | 1 | active | standup notes · "when someone creates an invite they should actually get an email" | InviteService.create sends an email via notifier.send_email(to, subject, body) to the invite's email, friendly subject/body | - |
| R4 | 1 | active | standup notes · "pricing: pro goes to 15 starting now (was 12). team stays where it is" | raise pro plan price to 15 (was 12); leave team plan unchanged | - |
| R5 | 1 | deferred | standup notes · "maybe one day a CSV export of invites? not now, just thinking out loud" | CSV export of invites | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:standup@2026-09-25 | - |
| W2 | R3@1 | implemented | C2 | workspace:standup@2026-09-25 | - |
| W3 | R4@1 | implemented | C3 | workspace:standup@2026-09-25 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app.AppTest.test_display_name_preserves_arabic` | display_name returns the Arabic guest name intact instead of an empty string |
| C2 | `python3 -m unittest tests.test_app.AppTest.test_create_sends_invite_email` | creating an invite calls notifier.send_email exactly once with the invite's email and a non-empty subject/body |
| C3 | `python3 -m unittest tests.test_app.AppTest.test_price_pro_is_15` | price("pro", 1) returns 15 while team price stays 40 |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#d22e77fd3c15 | `python3 -m unittest tests.test_app.AppTest.test_display_name_preserves_arabic` => display_name returns the Arabic guest name intact instead of an empty string | pass | workspace:standup@2026-09-25 | 2026-09-25 | host | `python3 -m unittest tests.test_app.AppTest.test_display_name_preserves_arabic` -> ok, Ran 1 test, OK |
| E2 | C2 | R3@1#185f89b8f50e | `python3 -m unittest tests.test_app.AppTest.test_create_sends_invite_email` => creating an invite calls notifier.send_email exactly once with the invite's email and a non-empty subject/body | pass | workspace:standup@2026-09-25 | 2026-09-25 | host | `python3 -m unittest tests.test_app.AppTest.test_create_sends_invite_email` -> ok, Ran 1 test, OK |
| E3 | C3 | R4@1#7b7f54ec936b | `python3 -m unittest tests.test_app.AppTest.test_price_pro_is_15` => price("pro", 1) returns 15 while team price stays 40 | pass | workspace:standup@2026-09-25 | 2026-09-25 | host | `python3 -m unittest tests.test_app.AppTest.test_price_pro_is_15` -> ok, Ran 1 test, OK |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | standup notes · "someone (Omar?) joked we should rewrite the whole thing in Rust lol. no." | noise | joke, explicitly declined by the room |
| I2 | standup notes · "remember when the sms provider went down last march, what a nightmare haha" | noise | reminiscing, not a request |
| I3 | standup notes · "coffee machine on 3 is broken again" | noise | unrelated to the codebase |
