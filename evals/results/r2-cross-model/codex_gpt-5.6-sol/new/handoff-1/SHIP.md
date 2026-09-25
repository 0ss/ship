# Ship
- [x] Pro plan price goes from $12 to $15 — proof: `python3 -m unittest -v` 5 ok, incl. `test_price`
- [x] Invites expire after 14 days using an `expires_at` field — proof: `python3 -m unittest -v` 5 ok, incl. `test_invite_expires_after_14_days`
- ~~Team plan price goes from $40 to $45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] Fix `display_name` blanking out Arabic names — proof: `python3 -m unittest -v` 5 ok, incl. `test_display_name_preserves_arabic`
