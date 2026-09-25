# Ship
- [x] Arabic `display_name` renders correctly — proof: `python3 -m unittest -v` passes Arabic preservation and character-safe truncation tests (6 tests OK)
- [x] Pro plan price is 15 — proof: `python3 -m unittest -v` passes `test_pro_price` (6 tests OK)
- [x] Invites expire after 14 days and expose `expires_at` — proof: `python3 -m unittest -v` checks exact `created_at + timedelta(days=14)` (6 tests OK)
- [x] Team plan price is 45 — "Dana confirmed the team price is 45"; proof: `python3 -m unittest -v` passes `test_team_price`, including 2 seats = 90 (6 tests OK)
