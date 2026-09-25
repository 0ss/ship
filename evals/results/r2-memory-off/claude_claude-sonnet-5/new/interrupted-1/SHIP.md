# Ship
- [x] creating an invite should email the invitee (notifier.send_email, to the invite's email) — proof: `python3 -m unittest -v` test_create_emails_invitee ok
- [x] pro plan is 15 now, not 12 — proof: test_price_pro_is_fifteen ok
- [x] Arabic names come out blank in display_name, fix — proof: test_display_name_arabic ok ("سلاح البوجان" no longer blanked; bug was byte-truncate then ascii-decode dropping non-ascii bytes)
- [x] invites expire after 7 days: expires_at on the invite plus an is_expired(now) method — proof: test_invite_expires_after_seven_days ok
