# Ship
- [x] fix display_name so Arabic guest names don't vanish — "the whole name just vanishes... that needs fixing, it's embarrassing" — proof: `python3 -m unittest -v` test_display_name_keeps_arabic ok, root cause was ascii-decode dropping non-ascii bytes
- [x] invite creation sends a friendly email via notifier.send_email(to, subject, body) — "when someone creates an invite they should actually get an email" — proof: test_create_sends_email ok
- [x] pro plan price goes to 15 (was 12), team unchanged — "pro goes to 15 starting now" — proof: test_price_pro_is_15 ok, team test_price (80 for 2 seats) still ok
- ~~rewrite in Rust~~ — dropped: joke ("someone joked... lol. no")
- ~~dark mode~~ — dropped: "that's her opinion, not this sprint"
- ~~CSV export of invites~~ — dropped: "not now, just thinking out loud"
