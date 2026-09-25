# Ship
- [x] pro plan price goes 12 -> 15 — proof: `app/pricing.py` PLANS["pro"]=15, test_pro_price passes
- [x] invites expire after 14 days — put expires_at on the invite ("for 2 make it 14 days not 7") — proof: Invite.expires_at = created_at + 14d, test_invite_expires_in_14_days passes
- ~~team plan to 45~~ — dropped: "scrap 3, Omar changed his mind, team stays at 40"
- [x] display_name blanks out Arabic names, needs fixing — proof: fixed ascii-encode/decode bug in `app/display.py`, test_arabic_name ("محمد أحمد") passes; `python3 -m unittest -v` 6 ok
