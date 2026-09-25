# Ship
- [x] team plan price goes to 45 — dana: "team plan goes to 45 today, update the pricing please" — proof: `python3 -m unittest -v` test_price passes (team,2 -> 90)
- [x] invite expires after 7 days: add expires_at + is_expired(now) — fatima: "invites need to expire after 7 days ... give the invite an expires_at and an is_expired(now)" — proof: `python3 -m unittest -v` test_invite_expires_after_7_days passes (4/4 tests ok)
