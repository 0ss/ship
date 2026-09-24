# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | closed | fixture-01 | screener hard-stops before diligence spend, no override | - |
| R3 | 1 | closed | fixture-01 | CSV export of the whole filtered set | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | git:setup1 | - |
| W2 | R3@1 | implemented | C2 | git:setup1 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `test-r1` | old hard-stop behavior passes |
| C2 | `test-r3` | old export behavior passes |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#d39cfc70a7d9 | `test-r1` => old hard-stop behavior passes | pass | git:setup1 | setup | host | exit 0 |
| E2 | C2 | R3@1#bd308fe814a2 | `test-r3` => old export behavior passes | pass | git:setup1 | setup | host | exit 0 |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | close | R1@1 | R1@1 | fixture-01 | user closed the previously verified requirement |
| H2 | close | R3@1 | R3@1 | fixture-01 | user closed the previously verified requirement |

## Ignored
| id | source | kind | note |
|---|---|---|---|
