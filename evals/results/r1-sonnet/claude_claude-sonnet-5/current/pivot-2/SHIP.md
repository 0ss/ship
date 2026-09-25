# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 2 | active | chat · /ship:ship follow-up "wait actually no emails at all, legal says SMS only. notifier.send_sms to the invite's phone instead." | invite creation sends an SMS via notifier.send_sms to the invite's phone; legal requires SMS only, no emails | - |
| R2 | 2 | active | chat · follow-up "ugh ok finance just pinged, we DO need the csv export after all. just name and phone columns, nothing else" | add a CSV export of all invites with name and phone columns only, InviteService.export_csv() returning the csv text | - |
| R3 | 2 | active | chat · follow-up "oh and make expiry 30 days, 7 is way too short" | invites should expire after 30 days, put an expires_at on the invite | - |
| R4 | 1 | active | chat · "also Arabic names are broken on the guest list, they come out blank" | fix display_name so non-Latin names (e.g. Arabic) render instead of coming out blank | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:invites@2026-09-25-rev1 | - |
| W2 | R2@1 | implemented | C2 | workspace:invites@2026-09-25-rev1 | - |
| W3 | R3@1 | implemented | C3 | workspace:invites@2026-09-25-rev1 | - |
| W4 | R1@2 | implemented | C4 | workspace:invites@2026-09-25-rev2 | - |
| W5 | R4@1 | implemented | C5 | workspace:invites@2026-09-25-rev3 | - |
| W6 | R3@2 | implemented | C6 | workspace:invites@2026-09-25-rev4 | - |
| W7 | R2@2 | implemented | C7 | workspace:invites@2026-09-25-rev5 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app.AppTest.test_create_sends_email_to_invitee` | InviteService.create calls notifier.send_email once, addressed to the invite's email |
| C2 | `python3 -m unittest tests.test_app.AppTest.test_export_csv_includes_all_invites` | export_csv() returns CSV text with a header row plus one row per created invite |
| C3 | `python3 -m unittest tests.test_app.AppTest.test_create_sets_expires_at_seven_days_out` | created invite's expires_at equals created_at + 7 days |
| C4 | `python3 -m unittest tests.test_app.AppTest.test_create_sends_sms_to_invitee` | InviteService.create calls notifier.send_sms once, addressed to the invite's phone |
| C5 | `python3 -m unittest tests.test_app.AppTest.test_display_name_keeps_arabic` | display_name("فاطمة الزهراء") returns the Arabic name unchanged, not blank |
| C6 | `python3 -m unittest tests.test_app.AppTest.test_create_sets_expires_at_thirty_days_out` | created invite's expires_at equals created_at + 30 days |
| C7 | `python3 -m unittest tests.test_app.AppTest.test_export_csv_has_name_and_phone_only` | export_csv() returns CSV text with a header row of exactly name,phone plus one name,phone row per created invite |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#2b81154394ff | `python3 -m unittest tests.test_app.AppTest.test_create_sends_email_to_invitee` => InviteService.create calls notifier.send_email once, addressed to the invite's email | pass | workspace:invites@2026-09-25-rev1 | 2026-09-25 | agent | superseded by R1@2/E4 (email replaced with SMS); ran full suite `python3 -m unittest -v` at the time: 6 tests OK |
| E2 | C2 | R2@1#3bcc29839f07 | `python3 -m unittest tests.test_app.AppTest.test_export_csv_includes_all_invites` => export_csv() returns CSV text with a header row plus one row per created invite | pass | workspace:invites@2026-09-25-rev1 | 2026-09-25 | agent | requirement closed by user, export_csv() and its test removed from codebase; historical record only |
| E3 | C3 | R3@1#232afba3e160 | `python3 -m unittest tests.test_app.AppTest.test_create_sets_expires_at_seven_days_out` => created invite's expires_at equals created_at + 7 days | pass | workspace:invites@2026-09-25-rev2 | 2026-09-25 | agent | ran full suite `python3 -m unittest -v`: 5 tests OK, incl. test_create_sets_expires_at_seven_days_out |
| E4 | C4 | R1@2#55a4022c4613 | `python3 -m unittest tests.test_app.AppTest.test_create_sends_sms_to_invitee` => InviteService.create calls notifier.send_sms once, addressed to the invite's phone | pass | workspace:invites@2026-09-25-rev2 | 2026-09-25 | agent | ran full suite `python3 -m unittest -v`: 5 tests OK, incl. test_create_sends_sms_to_invitee |
| E5 | C5 | R4@1#f518d3cbf40b | `python3 -m unittest tests.test_app.AppTest.test_display_name_keeps_arabic` => display_name("فاطمة الزهراء") returns the Arabic name unchanged, not blank | pass | workspace:invites@2026-09-25-rev3 | 2026-09-25 | agent | ran full suite `python3 -m unittest -v`: 6 tests OK, incl. test_display_name_keeps_arabic |
| E6 | C6 | R3@2#69f4738c378c | `python3 -m unittest tests.test_app.AppTest.test_create_sets_expires_at_thirty_days_out` => created invite's expires_at equals created_at + 30 days | pass | workspace:invites@2026-09-25-rev4 | 2026-09-25 | agent | ran full suite `python3 -m unittest -v`: 6 tests OK, incl. test_create_sets_expires_at_thirty_days_out; supersedes E3 (R3@1, 7 days) |
| E7 | C7 | R2@2#8d547d637a3e | `python3 -m unittest tests.test_app.AppTest.test_export_csv_has_name_and_phone_only` => export_csv() returns CSV text with a header row of exactly name,phone plus one name,phone row per created invite | pass | workspace:invites@2026-09-25-rev5 | 2026-09-25 | agent | ran full suite `python3 -m unittest -v`: 7 tests OK, incl. test_export_csv_has_name_and_phone_only |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | correction | R1@1 | R1@2 | chat · follow-up "wait actually no emails at all, legal says SMS only." | email notification replaced with SMS per legal requirement; notifier.send_email call removed, notifier.send_sms(invite.phone, ...) added |
| H2 | close | R2@1 | R2@1 | chat · follow-up "forget the CSV thing, we don't need it." | CSV export cancelled by user; InviteService.export_csv() and its test deleted from codebase |
| H3 | correction | R3@1 | R3@2 | chat · follow-up "oh and make expiry 30 days, 7 is way too short" | expiry window changed from 7 to 30 days; INVITE_LIFETIME updated to timedelta(days=30) |
| H4 | reopen | R2@1 | R2@2 | chat · follow-up "ugh ok finance just pinged, we DO need the csv export after all. just name and phone columns, nothing else" | closure reversed by user; export_csv() reintroduced with narrower scope (name, phone only — no email/created_at/expires_at columns this time) |

## Ignored
| id | source | kind | note |
|---|---|---|---|
