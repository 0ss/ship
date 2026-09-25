# Ship
- [x] pro plan price 12 -> 15 — proof: `python3 -m unittest -v` test_pro_price ok
- [x] invites expire after 14 days — added `expires_at` on the invite — proof: test_invite_expires_after_14_days ok
- ~~team plan to 45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] display_name blanks out Arabic names, needs fixing — proof: test_arabic_name ok (was stripping non-ascii bytes)
