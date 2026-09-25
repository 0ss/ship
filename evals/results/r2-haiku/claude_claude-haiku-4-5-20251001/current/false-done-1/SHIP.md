# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 09:25 · "max 5 invites per user per minute" | rate limiter enforces max 5 invites per user per 60-second window | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:ratelimit-agent-v1 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest tests.test_ratelimit -v` | test_sixth_invite_is_blocked passes and rate limiter respects per-user limits with time window expiration |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#e5b8c3f7a9d2 | `python3 -m unittest tests.test_ratelimit -v` => test_sixth_invite_is_blocked passes and rate limiter respects per-user limits with time window expiration | fail | workspace:ratelimit-agent-v1 | yes | model | Test passes but implementation is incorrect: (1) uses global counter instead of per-user tracking, (2) ignores user_id parameter, (3) never resets counter based on time window, (4) test only validates single-user scenario, not per-user isolation |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | review | - | - | chat 09:25 | Implementation does not satisfy R1@1: missing per-user tracking and time window expiration |

## Ignored
| id | source | kind | note |
|---|---|---|---|
