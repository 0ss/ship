# Ship
- [x] creating an invite should email the invitee via notifier.send_email, to invite's email — proof: ran InviteService.create, notifier.sent == [('email', 'ada@example.com', ...)]
- [x] pro plan is 15 now, not 12 — proof: price('pro', 1) == 15
- [x] Arabic names come out blank in display_name, fix — proof: display_name('محمد العلي') == 'محمد العلي' (was blank via ascii-only encode)
- [x] invites expire after 7 days: expires_at on the invite plus an is_expired(now) method — proof: is_expired at +6d False, +7d True; `python3 -m unittest discover -s tests` 3 ok
