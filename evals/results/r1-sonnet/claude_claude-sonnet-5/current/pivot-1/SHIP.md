# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 2 | active | chat · "wait actually no emails at all, legal says SMS only. notifier.send_sms to the invite's phone instead" | on InviteService.create, call notifier.send_sms to the invite's phone (SMS only, no email) | - |
| R2 | 2 | active | chat · "finance just pinged, we DO need the csv export after all. just name and phone columns" | InviteService.export_csv() returns CSV text with only name and phone columns | - |
| R3 | 2 | active | chat · "oh and make expiry 30 days, 7 is way too short" | Invite gets expires_at = created_at + 30 days | - |
| R4 | 1 | active | chat · "also Arabic names are broken on the guest list, they come out blank" | display_name must not blank out non-ASCII names (e.g. Arabic); it should preserve them, only truncating by length | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@2 | implemented | C1 | workspace:invites@2026-09-25 | - |
| W2 | R2@2 | implemented | C2 | workspace:invites@2026-09-25 | - |
| W3 | R3@2 | implemented | C3 | workspace:invites@2026-09-25 | - |
| W4 | R4@1 | implemented | C4 | workspace:invites@2026-09-25 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app -v` | creating an invite calls notifier.send_sms once with the invite's phone number |
| C2 | `python3 -m unittest tests.test_app -v` | export_csv returns CSV text with header ["name","phone"] and one name/phone row per invite, no other columns |
| C3 | `python3 -m unittest tests.test_app -v` | invite.expires_at equals invite.created_at + 30 days |
| C4 | `python3 -m unittest tests.test_app -v` | display_name("أحمد") returns "أحمد" unchanged, not blank |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#ce1363006804 | `python3 -m unittest tests.test_app -v` => creating an invite calls notifier.send_email once with the invite's email address | pass | workspace:invites@2026-09-25 | 2026-09-25 | assistant | superseded by R1 revision 2 (email -> SMS); test removed |
| E2 | C3 | R3@1#88c927e17243 | `python3 -m unittest tests.test_app -v` => invite.expires_at equals invite.created_at + 7 days | pass | workspace:invites@2026-09-25 | 2026-09-25 | assistant | superseded by R3 revision 2 (7 -> 30 days) |
| E3 | C1 | R1@2#ef63870e9283 | `python3 -m unittest tests.test_app -v` => creating an invite calls notifier.send_sms once with the invite's phone number | pass | workspace:invites@2026-09-25 | 2026-09-25 | assistant | test_create_sends_sms_to_invitee ... ok (5 tests, OK) |
| E4 | C4 | R4@1#91df0b386018 | `python3 -m unittest tests.test_app -v` => display_name("أحمد") returns "أحمد" unchanged, not blank | pass | workspace:invites@2026-09-25 | 2026-09-25 | assistant | test_display_name_preserves_arabic ... ok (6 tests, OK) |
| E5 | C3 | R3@2#fe664de847ae | `python3 -m unittest tests.test_app -v` => invite.expires_at equals invite.created_at + 30 days | pass | workspace:invites@2026-09-25 | 2026-09-25 | assistant | test_invite_expires_after_thirty_days ... ok (6 tests, OK) |
| E6 | C2 | R2@2#9dc8d9c9d7c2 | `python3 -m unittest tests.test_app -v` => export_csv returns CSV text with header ["name","phone"] and one name/phone row per invite, no other columns | pass | workspace:invites@2026-09-25 | 2026-09-25 | assistant | test_export_csv_has_name_and_phone_only ... ok (7 tests, OK) |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | correction | R1@1 | R1@2 | chat · "wait actually no emails at all, legal says SMS only" | switched from notifier.send_email(email) to notifier.send_sms(phone); legal requires SMS only |
| H2 | close | R2@1 | R2@1 | chat · "forget the CSV thing, we don't need it" | user canceled the CSV export requirement; export_csv() and its test removed from the codebase |
| H3 | correction | R3@1 | R3@2 | chat · "oh and make expiry 30 days, 7 is way too short" | INVITE_LIFETIME changed from timedelta(days=7) to timedelta(days=30) |
| H4 | correction | R2@1 | R2@2 | chat · "finance just pinged, we DO need the csv export after all. just name and phone columns" | reopened: export_csv() reinstated with scope narrowed to name + phone columns only (original had 5 columns) |

## Ignored
| id | source | kind | note |
|---|---|---|---|
