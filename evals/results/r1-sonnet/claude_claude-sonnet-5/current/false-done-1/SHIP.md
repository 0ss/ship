# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | /ship:ship 2026-09-25 · "the requirement was max 5 invites per user per minute" | invite rate limiter must allow at most 5 invites per user per 60s window | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | blocked | C1 | workspace:app/ratelimit.py@2026-09-25 | not per-user, no window reset, not wired into InviteService |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest discover` plus manual per-user/window trace of app/ratelimit.py | two distinct user_ids each get their own 5-per-60s allowance, count resets after window elapses, and RateLimiter is invoked from the invite creation path |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#pending | `python3 -m unittest discover` plus manual trace => two distinct user_ids each get their own 5-per-60s allowance, count resets after window elapses, and RateLimiter is invoked from the invite creation path | fail | workspace:app/ratelimit.py@2026-09-25 | 2026-09-25 | salahalboijan@gmail.com | `python3 -m unittest discover` -> 4/4 pass (only regression coverage: single user, frozen clock). Manual read of app/ratelimit.py: `allow(self, user_id)` never uses `user_id` — `self.count` is one counter shared across ALL users, so two different users combined only get 5 invites total, not 5 each. `window` is stored but never read in `allow()`, so count never resets — after 5 invites ever occur, every later call returns False forever, even after the 60s window passes. Also grepped repo: RateLimiter is not imported or called anywhere in app/invites.py or elsewhere, so it is not enforced on invite creation at all. |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | review | R1@1 | R1@1 | independent code read 2026-09-25 | claim "everything's done and all tests pass" verified as true but insufficient: passing test only covers one user with a frozen clock, missing per-user isolation, window expiry, and wiring into InviteService |

## Ignored
| id | source | kind | note |
|---|---|---|---|
