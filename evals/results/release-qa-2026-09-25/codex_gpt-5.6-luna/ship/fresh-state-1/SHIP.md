# Ship
- [x] Fix Arabic `display_name` — "fix Arabic display_name" — proof: `python3 -m unittest -v`, `test_display_name_preserves_arabic` passed
- [x] Raise pro from 12 to 15 — "raise pro from 12 to 15" — proof: `python3 -m unittest -v`, `test_price` passed with `price("pro") == 15`
- [x] Make invites expire after 14 days with `expires_at` — "make invites expire after 14 days with expires_at" — proof: `python3 -m unittest -v`, invite expiry test passed
- [x] Update team price to 45 — "Dana confirmed the team price is 45" — proof: `python3 -m unittest -v`, `test_price` passed with `price("team", 2) == 90`
