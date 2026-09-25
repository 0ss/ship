# Ship
- [x] pro plan price 12 -> 15 — proof: `python3 -m unittest -v` test_pro_price ok, app/pricing.py PLANS["pro"]=15
- [x] invites expire after 14 days — put expires_at on the invite (was: 7 days) — proof: test_invite_expires_after_14_days ok, Invite.expires_at = created_at + 14d
- ~~team plan to 45~~ — dropped: "Omar changed his mind, team stays at 40" — confirmed unchanged, test_team_price_unchanged ok
- [x] display_name blanks out Arabic names, needs fixing — proof: test_display_name_keeps_arabic ok ("فاطمة الزهراء" round-trips); bug was byte-slicing then ascii-decoding, which silently dropped non-ASCII text
