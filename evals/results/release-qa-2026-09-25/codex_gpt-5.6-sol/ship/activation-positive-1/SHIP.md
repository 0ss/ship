# Ship
- [x] Set per-seat prices to free 0, pro 15, team 45 — proof: `python3 -m unittest discover -v`, `test_price` passed
- [x] Invite creation emails the invitee via `notifier.send_email` — proof: `test_create_stores_invite` passed with `RecordingNotifier`
- [x] Invite creation independently texts the invitee via `notifier.send_sms` — proof: `test_create_stores_invite` passed with `RecordingNotifier`
- [x] Preserve Arabic names in `display_name` without breaking Latin title-casing — proof: Arabic and Latin display-name tests passed
- [x] Set `expires_at` exactly seven days after `created_at` — proof: creation test passed with exact timedelta assertion
- [x] Add `invite.is_expired(now)` — proof: boundary test passed immediately before and at expiration
- [x] Add `InviteService.export_csv()` with only name and phone columns and one row per invite — proof: CSV test passed, including comma escaping
