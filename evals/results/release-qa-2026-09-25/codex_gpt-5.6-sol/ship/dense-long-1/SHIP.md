# Ship
- [x] pro costs 15 per seat — proof: `python3 -m unittest -v`, `test_price` passed
- [x] team costs 45 per seat — proof: `python3 -m unittest -v`, `test_price` passed
- [x] free remains zero — proof: `python3 -m unittest -v`, `test_price` passed
- [x] invite creation emails `invite.email` using `notifier.send_email` — proof: `python3 -m unittest -v`, `test_create_stores_invite` passed
- [x] invite creation texts `invite.phone` using `notifier.send_sms` independently of email — proof: `python3 -m unittest -v`, `test_create_stores_invite` passed
- [x] `display_name` preserves Arabic names without breaking Latin title-casing — proof: `python3 -m unittest -v`, Arabic and Latin display-name tests passed
- [x] invites expire exactly seven days after creation and expose `invite.is_expired(now)` — proof: `python3 -m unittest -v`, expiry boundary test passed
- [x] `InviteService.export_csv()` returns CSV containing only `name` and `phone`, one row per invite — proof: `python3 -m unittest -v`, CSV content/escaping test passed
