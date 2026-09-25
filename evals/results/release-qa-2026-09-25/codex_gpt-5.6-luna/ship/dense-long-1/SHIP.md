# Ship
- [x] Set pro pricing to 15 per seat and team pricing to 45 per seat; keep free at zero. Proof: `python3 -m unittest -v` passed pricing assertions.
- [x] Preserve Arabic names in `display_name` without breaking Latin title-casing. Proof: test suite passed Arabic and Latin display-name assertions.
- [x] On invite creation, send email via `notifier.send_email` and SMS via `notifier.send_sms` to the invitee's phone; use the fake notifier in tests. Proof: test suite passed `RecordingNotifier` assertions.
- [x] Set invite `expires_at` exactly 7 days after `created_at` and add `invite.is_expired(now)`. Proof: test suite passed boundary expiry assertions.
- [x] Add `InviteService.export_csv()` with only name and phone columns, one row per invite. Proof: test suite passed exact CSV output assertion.
- [ ] Keep changes as small Python edits; do not migrate languages or add unrelated features.
