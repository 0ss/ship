# Ship
- [x] Send SMS to invite.phone when invite is created using notifier.send_sms — "legal says SMS only" — proof: test_create_sends_sms passes
- [x] CSV export name and phone columns only — "finance just pinged, we DO need the csv export after all" — proof: test_export_csv passes
- [x] Add expires_at to invites, expires after 30 days — "7 is way too short" — proof: test_create_sets_expires_at passes
- [x] Arabic names show in full on guest list — proof: test_arabic_name passes
