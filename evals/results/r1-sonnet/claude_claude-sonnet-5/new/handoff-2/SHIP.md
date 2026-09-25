# Ship
- [x] pro plan price goes 12 -> 15 — proof: `python3 -m unittest` test_pro_price ok (price("pro",2)==30)
- [x] invites expire after 14 days — put `expires_at` on the invite (was 7 days, corrected to 14) — proof: test_invite_expires_after_14_days ok
- ~~team plan to 45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] display_name blanks out Arabic names, needs fixing — proof: test_display_name_keeps_arabic ok, display_name("محمد أحمد") == "محمد أحمد"
