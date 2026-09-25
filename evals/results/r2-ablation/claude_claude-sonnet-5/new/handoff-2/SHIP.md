# Ship
- [x] pro plan price goes 12 -> 15 — proof: `python3 -m unittest` test_price_pro_is_15 ok, PLANS["pro"]=15
- [x] invites expire after 14 days (was 7) — put expires_at on the invite — proof: test_invite_expires_after_14_days ok, Invite.expires_at = created_at + 14d
- ~~team plan to 45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] display_name blanks out Arabic names, needs fixing — proof: test_display_name_keeps_arabic ok, "فاطمة الزهراء" round-trips (bug was utf-8-encode→ascii-decode stripping non-ascii bytes)
