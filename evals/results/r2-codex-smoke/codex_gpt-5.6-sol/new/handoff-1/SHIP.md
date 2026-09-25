# Ship
- [x] pro plan price goes 12 -> 15 — proof: `python3 -m unittest -v` 4 ok, including `test_price`
- [x] invites expire after 14 days; put `expires_at` on the invite — proof: `python3 -m unittest -v` 4 ok, including exact `expires_at` assertion
- ~~team plan price to 45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] fix `display_name` blanking out Arabic names — proof: `python3 -m unittest -v` 4 ok, including `test_display_name_preserves_arabic`
