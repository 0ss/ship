# Ship
- [x] creating an invite should email the invitee (notifier.send_email, to the invite's email) — proof: email ('email', 'test@example.com', "You're invited!", 'Hi Test User, join us!') sent on create
- [x] pro plan is 15 now, not 12 — proof: price("pro") returns 15
- [x] Arabic names come out blank in display_name, fix — proof: display_name("محمد علي") returns 'محمد علي'
- [x] invites expire after 7 days: expires_at on the invite plus an is_expired(now) method — proof: invite.expires_at = created_at + 7 days, is_expired(after_expiry) returns True
