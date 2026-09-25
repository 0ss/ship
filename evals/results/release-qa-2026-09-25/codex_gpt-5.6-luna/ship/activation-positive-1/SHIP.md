# Ship
- [x] Update pricing: pro 15/seat, team 45/seat, free remains 0 — "make pro 15... team 45... leave free at zero" — proof: `python3 -m unittest -v`, 5 passed
- [x] Invite creation emails invitee via `notifier.send_email` — "email the invitee's email address" — proof: notification test passed
- [x] Invite creation texts invitee via `notifier.send_sms` — "text the invitee's phone" — proof: notification test passed
- [x] Preserve Arabic names in `display_name` without breaking Latin title-casing — "Arabic names on the guest list are blank" — proof: display-name tests passed
- [x] Set `expires_at` exactly 7 days after `created_at` and add `invite.is_expired(now)` — "invites need an expires_at..." — proof: expiry assertions passed
- [x] Add `InviteService.export_csv()` with only name and phone columns, one row per invite — "InvoiceService isn't the right place" — proof: CSV test passed
- [x] Keep changes in Python and use the fake notifier in tests — "small Python edits... fake notifier" — proof: implementation uses existing `RecordingNotifier`
- [x] Run tests — "please run the tests" — proof: `python3 -m unittest -v`, 5 passed
