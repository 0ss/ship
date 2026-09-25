# Ship
- [x] send SMS when invite created — `notifier.send_sms` to invite's phone (legal says SMS only) — proof: test_create_sends_sms passes
- [x] CSV export of invites — name and phone columns only — proof: test_export_csv passes
- [x] invites expire after 30 days — add `expires_at` field on invite — proof: test_invite_expires_after_30_days passes
- [x] Arabic names show in full — proof: test_arabic_name passes
