# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | closed | chat 09:02 · "update the pricing" | team plan goes to 45, update pricing from 40 to 45 | - |
| R2 | 1 | closed | chat 13:20 · "@bot invites expire" | invites need to expire after 7 days; add expires_at and is_expired(now) | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | git:8d4c96d | - |
| W2 | R2@1 | implemented | C2 | git:8d4c96d | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python -m pytest tests/test_app.py -k price` | team plan price is 45, test passes |
| C2 | `python -m pytest tests/test_app.py -k invite` | invites have expires_at, is_expired(now) method works, test passes |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#pricing | `python -m pytest tests/test_app.py -k price` => team plan price is 45, test passes | pass | git:8d4c96d | 2026-09-25 | model | test_price (tests.test_app.AppTest.test_price) ... ok |
| E2 | C2 | R2@1#expires | `python -m pytest tests/test_app.py -k invite` => invites have expires_at, is_expired(now) method works, test passes | pass | git:8d4c96d | 2026-09-25 | model | test_create_stores_invite passed; manual expiration tests: invite not expired at creation, at 6 days, expired at 7 and 10 days |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | close | R1@1 | R1@1 | implementation | pricing.py PLANS["team"] 40→45, test updated |
| H2 | close | R2@1 | R2@1 | implementation | Invite.expires_at added, is_expired(now) method added, 7-day expiration in create() |

## Ignored
| id | source | kind | note |
|---|---|---|---|
| I1 | chat · repeated msgs | noise | multiple "flaky test", "sentry alert", "did anyone", "brb", "lgtm", social chat |
| I2 | chat · chat 09:17/09:53 | not-asked | "does anyone know why node 18 is pinned" - question asked but no actionable ask to fix |
| I3 | chat · chat 11:15/11:16 | not-asked | "sentry is noisy, muting timeout alert" - reported action, no ask |
