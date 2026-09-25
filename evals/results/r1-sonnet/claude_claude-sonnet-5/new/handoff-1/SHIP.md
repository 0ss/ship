# Ship
- [x] pro plan price 12 -> 15 — "pro plan price goes 12 -> 15" — proof: `python3 -m unittest` test_price_pro ok (price("pro")==15)
- [x] invites expire after 14 days, add expires_at on the invite — "make it 14 days not 7" — proof: test_invite_expires_after_14_days ok (Invite.expires_at = created_at + 14d)
- ~~team plan to 45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] display_name blanks out Arabic names, needs fixing — "display_name blanks out Arabic names, needs fixing" — proof: test_arabic_name ok (was ascii-encoding then discarding non-ascii bytes; now slices/titles the str directly)
