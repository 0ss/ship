# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 2026-09-25 · "pro plan price goes 12 -> 15" | raise pro plan price from 12 to 15 | - |
| R2 | 2 | active | chat 2026-09-25 · "invites expire after 7 days. put expires_at on the invite" then "for 2 make it 14 days not 7" | invites expire after 14 days; add expires_at field on the invite | - |
| R3 | 2 | closed | chat 2026-09-25 · "team plan to 45" then "scrap 3, Omar changed his mind, team stays at 40" | (retracted) raise team plan price from 40 to 45 | - |
| R4 | 1 | active | chat 2026-09-25 · "display_name blanks out Arabic names, needs fixing" | fix display_name so it no longer blanks out Arabic names | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | git:af102ae | - |
| W2 | R2@2 | implemented | C2 | git:af102ae | - |
| W3 | R4@1 | implemented | C3 | git:af102ae | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_app -v` | `PLANS["pro"]` is 15 and `price("pro", 1)` returns 15 |
| C2 | `python3 -m unittest tests.test_app -v` | creating an invite sets `expires_at` to `created_at` + 14 days |
| C3 | `python3 -m unittest tests.test_app -v` | `display_name` preserves Arabic input (e.g. a name like "محمد") instead of returning blank/empty text |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#90f594a5e5d6 | `python3 -m unittest tests.test_app -v` => `PLANS["pro"]` is 15 and `price("pro", 1)` returns 15 | pass | git:af102ae | 2026-09-25 | host | `test_pro_price_is_15 ... ok`, full suite `Ran 6 tests in 0.000s OK` |
| E2 | C2 | R2@2#a5c25b3f0455 | `python3 -m unittest tests.test_app -v` => creating an invite sets `expires_at` to `created_at` + 14 days | pass | git:af102ae | 2026-09-25 | host | `test_create_sets_expires_at_14_days_out ... ok`, full suite `Ran 6 tests in 0.000s OK` |
| E3 | C3 | R4@1#1943dfa4851c | `python3 -m unittest tests.test_app -v` => `display_name` preserves Arabic input (e.g. a name like "محمد") instead of returning blank/empty text | pass | git:af102ae | 2026-09-25 | host | `test_display_name_preserves_arabic ... ok`, full suite `Ran 6 tests in 0.000s OK` |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | correction | R2@1 | R2@2 | chat 2026-09-25 · "oh wait — for 2 make it 14 days not 7" | invite expiry window corrected from 7 days to 14 days |
| H2 | correction | R3@1 | R3@2 | chat 2026-09-25 · "scrap 3, Omar changed his mind, team stays at 40" | team plan price bump to 45 abandoned; team plan remains 40, no code change needed |
| H3 | close | R3@2 | R3@2 | chat 2026-09-25 · "scrap 3, Omar changed his mind, team stays at 40" | requirement closed, no work needed |

## Ignored
| id | source | kind | note |
|---|---|---|---|
