# Ship
- [x] update pro pricing to 15 per seat; keep free at zero — proof: `python3 -m unittest -v` (5 tests passed)
- [x] update team pricing to 45 per seat — proof: `python3 -m unittest -v` (5 tests passed)
- [x] send invite email via `notifier.send_email` on creation — proof: notifier assertions passed
- [x] send invite SMS via `notifier.send_sms` on creation — proof: notifier assertions passed
- [x] preserve Arabic display names without breaking Latin title-casing — proof: Arabic and Latin display tests passed
- [x] set invite expiry exactly 7 days after creation and add `invite.is_expired(now)` — proof: expiry boundary tests passed
- [x] use the fake notifier in tests; do not integrate a provider — proof: tests use `RecordingNotifier`, all passed
- [x] add `InviteService.export_csv()` with only name and phone columns, one row per invite — proof: CSV output test passed
- [x] keep implementation in Python — proof: `python3 -m compileall -q app tests` passed
