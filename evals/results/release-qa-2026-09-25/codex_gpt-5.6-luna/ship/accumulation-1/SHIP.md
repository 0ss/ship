# Ship
- [x] Raise pro pricing from 12 to 15; keep team at 40 — proof: `python3 -m unittest -v`, pricing assertions passed.
- [x] Preserve Arabic names in `display_name` instead of returning blank text — proof: `python3 -m unittest -v`, Arabic regression test passed.
- [x] Send invite SMS messages using `notifier.send_sms` to the invite phone — proof: `python3 -m unittest -v`, 4 tests passed; create test verifies phone recipient.
- [x] Add `export_csv` with only invite `name` and `phone` columns — proof: `python3 -m unittest -v`, CSV shape test passed.
- [x] Make invites expire after 14 days with `expires_at` — proof: `python3 -m unittest -v`, creation and 14-day expiry-boundary tests passed.
