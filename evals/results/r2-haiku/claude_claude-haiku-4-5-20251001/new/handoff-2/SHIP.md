# Ship

- [x] pro plan price goes 12 -> 15 — proof: `price('pro')` returns 15
- [x] invites expire after 14 days, put expires_at on the invite — proof: expires_at = created_at + 14 days
- ~~team plan to 45~~ — Omar changed his mind, stays at 40
- [x] display_name blanks out Arabic names, needs fixing — proof: display_name("محمد علي") = "محمد علي"
