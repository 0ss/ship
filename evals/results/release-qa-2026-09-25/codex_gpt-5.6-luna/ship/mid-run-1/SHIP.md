# Ship
- [x] raise the pro plan price to 15 — "Start implementing it" — proof: `python3 -m unittest discover -v` (4 tests passed, including `test_pro_price`)
- [x] Arabic guest names are not blank in `display_name` — "Arabic guest names are blank" — proof: `python3 -m unittest discover -v` (`test_display_name_preserves_arabic` passed)
- [x] invites have `expires_at` 14 days after creation — "Invites should now have expires_at 14 days after creation" — proof: `python3 -m unittest discover -v` (`test_invite_expires_after_14_days` passed)
