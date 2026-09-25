# Ship
- [x] On invite creation send email only to `invite.email` with `notifier.send_email`; remove SMS — proof: `python3 -m unittest -v` (4 tests passed, including `test_create_sends_email_only_to_invitee`); invite flow contains no `send_sms` call (was: SMS only; originally: email)
