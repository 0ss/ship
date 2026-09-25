# Ship
- [x] team plan price goes to 45 — "@bot morning — team plan goes to 45 today, update the pricing please" (dana) — proof: `python3 -m unittest -v` test_price passes with price("team",2)==90
- [x] invite needs expires_at + is_expired(now), 7 day expiry — "@bot btw invites need to expire after 7 days — customers keep using month-old links. give the invite an expires_at and an is_expired(now) please" (fatima) — proof: `python3 -m unittest -v` 5 ok, incl. test_invite_not_expired_before_seven_days and test_invite_expired_after_seven_days
