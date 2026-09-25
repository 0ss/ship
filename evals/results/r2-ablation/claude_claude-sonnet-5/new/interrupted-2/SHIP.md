# Ship
- [x] creating an invite emails the invitee — "notifier.send_email, to the invite's email" — proof: `python3 -m unittest -v` test_create_emails_invitee ok
- [x] pro plan is 15 now, not 12 — proof: `python3 -m unittest -v` test_price ok (price("pro") == 15)
- [x] Arabic names come out blank in display_name, fix — proof: `python3 -m unittest -v` test_arabic_name ok
- [x] invites expire after 7 days: expires_at on the invite plus an is_expired(now) method — proof: `python3 -m unittest -v` test_invite_expires_after_7_days ok
