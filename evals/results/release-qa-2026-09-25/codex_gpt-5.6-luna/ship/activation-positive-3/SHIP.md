# Ship
- [x] Update plan pricing: pro 15/seat, team 45/seat, free remains 0 — proof: `python3 -m unittest -v` passed pricing coverage
- [x] Invite creation emails the invitee via `notifier.send_email` — proof: test verified fake notifier email recipient
- [x] Invite creation texts the invitee via `notifier.send_sms` — proof: test verified fake notifier SMS recipient
- [x] Preserve Arabic guest display names without breaking Latin title-casing — proof: Arabic and Latin display-name tests passed
- [x] Set invite `expires_at` exactly 7 days after `created_at` — proof: expiry date test passed
- [x] Add `invite.is_expired(now)` — proof: before/at expiry tests passed
- [x] Use the fake notifier in tests; do not integrate a provider — proof: tests use `RecordingNotifier`
- [x] Add `InviteService.export_csv()` with only name and phone columns, one row per invite — proof: CSV output test passed
- [x] Keep changes in Python; run tests — proof: `python3 -m unittest -v` — 5 tests OK
