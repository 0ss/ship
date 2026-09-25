# Ship
- [x] Pricing is free 0, pro 15 per seat, and team 45 per seat — proof: `python3 -m unittest -v`, pricing assertions passed
- [x] Invite creation emails the invitee via `notifier.send_email` — proof: `test_create_stores_invite` passed with recorded email destination
- [x] Invite creation independently texts the invitee via `notifier.send_sms` — proof: `test_create_stores_invite` passed with recorded SMS destination
- [x] Guest display names preserve Arabic and retain Latin title-casing — proof: Arabic and Latin display-name tests passed
- [x] Invites expire exactly seven days after creation and expose `invite.is_expired(now)` — proof: boundary assertions passed in `test_create_stores_invite`
- [x] `InviteService.export_csv()` returns name and phone columns only, one row per invite — proof: `test_export_csv_has_only_name_and_phone` passed
- [x] Run the test suite — proof: `python3 -m unittest -v` ran 5 tests, all passed
