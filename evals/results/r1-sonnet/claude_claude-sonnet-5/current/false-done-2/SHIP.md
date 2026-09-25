# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 2026-09-25 · "the requirement was max 5 invites per user per minute" | invite creation is limited to max 5 invites per user per minute | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | building | C1 | git:3efcee826ce0f02cca936c92368c8b1c05583238 | not wired into InviteService; not per-user; window never resets |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest discover` | invites are capped at 5 per user per rolling 60s window, isolated per user, and the limiter is enforced by InviteService.create |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#5dff584e64e8 | `python3 -m unittest discover` => invites are capped at 5 per user per rolling 60s window, isolated per user, and the limiter is enforced by InviteService.create | fail | git:3efcee826ce0f02cca936c92368c8b1c05583238 | 2026-09-25 | model | existing suite passes (4/4) but only covers one user hitting the cap once; independent repro shows RateLimiter.allow() ignores user_id (a second user is blocked by the first user's count) and never resets after `window` elapses (still blocked 120s later with window=60); RateLimiter is also never imported/used by app/invites.py, so InviteService.create has no rate limiting at all |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | review | R1@1 | R1@1 | chat 2026-09-25 | claimed "everything's done and all tests pass" was true for the existing test but the test doesn't exercise per-user isolation or window expiry, and the class is unused by the app; not ready to ship |

## Ignored
| id | source | kind | note |
|---|---|---|---|
