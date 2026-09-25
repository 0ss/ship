# Ship

- [x] Change Pro plan price from 12 to 15 — “pro plan price goes 12 -> 15” — proof: `python3 -m unittest -v`, 4 tests passed including `price("pro") == 15`
- [x] Make invites expire after 14 days and add `expires_at` to the invite — “make it 14 days not 7” — proof: `python3 -m unittest -v`, expiry asserted as 2026-01-15 for a 2026-01-01 invite
- ~~Change Team plan price to 45~~ — dropped: “scrap 3, Omar changed his mind, team stays at 40”
- [x] Fix `display_name` blanking out Arabic names — “display_name blanks out Arabic names, needs fixing” — proof: `python3 -m unittest -v`, Arabic preservation test passed
