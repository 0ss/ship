# Ship
- [x] On invite creation send an email to the invitee with `notifier.send_email` — final correction restored email-only behavior; proof: `python3 -m unittest` (4 tests passed), including email assertion
- ~~On invite creation send an SMS to the invitee's phone with `notifier.send_sms`~~ — cancelled by final correction: email only
