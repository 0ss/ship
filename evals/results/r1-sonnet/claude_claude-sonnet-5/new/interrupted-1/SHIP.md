# Ship
- [x] creating an invite should email the invitee — proof: `python3 -m unittest -v` test_create_emails_invitee ok
- [x] pro plan is 15 now, not 12 — proof: test_pro_price ok (price("pro",2)==30)
- [x] Arabic names come out blank in display_name, fix — proof: test_display_name_keeps_arabic ok ("محمد علي" preserved)
- [x] invites expire after 7 days: expires_at on the invite plus an is_expired(now) method — proof: test_invite_expires_after_7_days ok
