# Ship

- [x] Pro plan price goes from 12 to 15 — "pro plan price goes 12 -> 15" — proof: `python3 -m unittest -v`, 4 tests OK, including Pro=15 and Team=40
- [x] Invites expire after 14 days; add `expires_at` to the invite — "make it 14 days not 7" — proof: `python3 -m unittest -v`, 4 tests OK, including exact 14-day expiry
- ~~Team plan price goes from 40 to 45~~ — dropped: "scrap 3, Omar changed his mind, team stays at 40"
- [x] Fix `display_name` blanking out Arabic names — "display_name blanks out Arabic names, needs fixing" — proof: `python3 -m unittest -v`, 4 tests OK, including Arabic name preservation
