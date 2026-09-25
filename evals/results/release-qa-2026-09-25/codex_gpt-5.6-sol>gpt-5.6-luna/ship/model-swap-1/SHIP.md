# Ship

- [x] Pro plan price goes from 12 to 15 — "pro plan price goes 12 -> 15" — proof: `python3 -m unittest -v`, 5 tests passed including `test_price`
- [x] Invites expire after 14 days; add `expires_at` to the invite — "make it 14 days not 7" — proof: `python3 -m unittest -v`, `test_invite_expires_after_fourteen_days` passed
- ~~Team plan price goes from 40 to 45~~ — dropped: "Omar changed his mind, team stays at 40"
- [x] Fix `display_name` blanking out Arabic names — "display_name blanks out Arabic names, needs fixing" — proof: `python3 -m unittest -v`, `test_display_name_preserves_arabic` passed
