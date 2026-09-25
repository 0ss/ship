# Ship
- [x] invite create sends SMS via notifier.send_sms to invite.phone — "legal says SMS only" (was: email) — proof: notifier.sent == [('sms', '+15550001', ...)]
- [x] InviteService.export_csv() — name and phone columns only, finance needs it — proof: ran export_csv() with 2 invites, got 'name,phone\r\nada lovelace,+15550001\r\nbob,+15550002\r\n'
- [x] invites expire after 30 days (was 7, "7 is way too short") — expires_at field on Invite — proof: created 2026-01-01, invite.expires_at == 2026-01-31
- [x] Arabic names on guest list come out blank — proof: `python3 -m unittest` 4/4 ok incl. new test_display_name_arabic_name asserting display_name("فاطمة الزهراء") == "فاطمة الزهراء"
