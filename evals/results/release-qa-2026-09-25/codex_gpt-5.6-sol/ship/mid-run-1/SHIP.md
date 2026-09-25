# Ship
- [x] Raise the Pro plan price to 15 — "Raise the pro plan price to 15. Start implementing it." Proof: `python3 -m unittest -v` passed 4 tests, including `test_pro_price` asserting 15.
- [x] Arabic guest names are not blank in `display_name` — "Arabic guest names are blank in display_name; fix that too." Proof: `python3 -m unittest -v` passed 6 tests, including `test_display_name_preserves_arabic`.
- [x] Invites have `expires_at` 14 days after creation — "Invites should now have expires_at 14 days after creation." Proof: `python3 -m unittest -v` passed 6 tests, including `test_invite_expires_fourteen_days_after_creation`.
