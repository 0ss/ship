# Ship
- [x] invite creation sends SMS via notifier.send_sms to invite.phone — "legal says SMS only" (was: email) — proof: ran create(), notifier.sent == [('sms', '+15550001', ...)]
- [x] InviteService.export_csv() with name and phone columns only — "finance just pinged, we DO need the csv export after all" (was: dropped, then re-added, columns narrowed to name+phone) — proof: header 'name,phone', rows match created invites
- [x] invites expire after 30 days (was 7, "7 is way too short") — expires_at on the invite — proof: created_at=2026-01-01 → expires_at=2026-01-31 (asserted in script)
- [x] Arabic names show on guest list instead of blank — proof: display_name('محمد العلي') == 'محمد العلي' (was '' before fix); existing Latin test still passes
