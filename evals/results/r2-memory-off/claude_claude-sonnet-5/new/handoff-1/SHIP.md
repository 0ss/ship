# Ship
- [x] pro plan price 12 -> 15 — proof: `python3 -m unittest -v` test_price_pro ok (PLANS["pro"]=15)
- [x] invites expire after 14 days — proof: `python3 -m unittest -v` test_invite_expires_in_14_days ok (`expires_at` = created_at + 14d)
- ~~team plan to 45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] `display_name` blanks out Arabic names, needs fixing — proof: `python3 -m unittest -v` test_display_name_keeps_arabic_name ok ("محمد علي" no longer stripped)
