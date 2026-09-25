# Ship

- [x] Fix Arabic guest names showing blank — "the whole name just vanishes. display_name is doing something dumb" — proof: `python3 -m unittest` 6 ok, incl. test_display_name_preserves_arabic
- [x] Send email when invite created — "there's notifier.send_email(to, subject, body) already, just send it to the email on the invite" — proof: test_email_sent_on_invite_create passes
- [x] Pro pricing from 12 to 15 — "pro goes to 15 starting now" — proof: test_pro_price_is_15 passes
