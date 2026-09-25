# Ship
- [x] Set pro pricing to 15 per seat and team pricing to 45 per seat; keep free at zero — proof: `python3 -m unittest -v` (5 tests OK)
- [x] Send invite creation email and SMS through the fake notifier — proof: `test_create_stores_invite` verifies email and SMS destinations; 5 tests OK
- [x] Preserve Arabic display names without breaking Latin title-casing — proof: `test_display_name_titles_latin`; 5 tests OK
- [x] Set `expires_at` exactly 7 days after `created_at` and add `invite.is_expired(now)` — proof: `test_invite_expiry`; 5 tests OK
- [x] Add `InviteService.export_csv()` with only name and phone columns, one row per invite — proof: `test_export_csv`; 5 tests OK
- [x] Keep the changes as small Python edits and run the tests — proof: `python3 -m unittest -v` reported 5 tests, all OK
