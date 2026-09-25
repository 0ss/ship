# Ship
- [x] fix display_name so Arabic guest names don't vanish — "the whole name just vanishes... that needs fixing, it's embarrassing" — proof: `python3 -m unittest -v` 6 ok, incl. test_display_name_arabic (was dropping all non-ASCII bytes)
- [x] send a real email on invite create via notifier.send_email(to, subject, body) — "they should actually get an email... just send it to the email on the invite" — proof: test_create_sends_email passes, notifier.sent has ("email", invite.email, subject, body)
- [x] pro plan price 12 -> 15, team unchanged — "pro goes to 15 starting now (was 12). team stays where it is" — proof: test_price_pro (15) and test_price (team*2=80) both pass
