# Ship
- [x] Final-scope audit: all current asks pass, with no invite email and no 7-day expiry — proof: `python3 -m unittest -v` passed all 8 tests; targeted `rg` scan found neither `send_email` nor 7-day expiry in invite implementation/tests; compile and diff checks passed
- [x] Raise the pro price from 12 to 15 while team remains 40 — proof: `python3 -m unittest -v`, pro and team price tests passed; direct output was `pro=15, team=40`
- [x] Arabic names render in `display_name` instead of blank — proof: latest `python3 -m unittest -v`, `test_display_name_preserves_arabic` passed
- [x] Send invite SMS using `notifier.send_sms` to the invite phone — proof: latest `python3 -m unittest -v`, `test_create_sends_invite_sms_to_phone` passed
- [x] Restore `export_csv` with only invite name and phone columns — proof: `python3 -m unittest -v`, `test_export_csv_contains_only_name_and_phone_columns` passed with comma-containing and Arabic names (restored after earlier drop)
- [x] Make invites expire after 14 days using `expires_at` — proof: `python3 -m unittest -v`, `test_create_sets_expiry_fourteen_days_after_creation` passed; search confirmed no stale 7-day implementation or test remains
