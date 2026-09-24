# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 2 | active | chat 2026-09-24 · "there does need to be an override, but it has to be logged, who did it and why" | screener still hard-stops before diligence spend, but Legal can override when a signed waiver is on file; every override writes an audit record with the acting user and the stated reason | - |
| R3 | 2 | active | chat 2026-09-24 · "it needs the deal ID column, it is useless for reconciling without it" | CSV export of the whole filtered set, including a deal ID column | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | git:setup1 | - |
| W2 | R3@1 | implemented | C2 | git:setup1 | - |
| W3 | R1@2 | blocked | C3 | - | screener/hard-stop code is not in this repo |
| W4 | R3@2 | blocked | C4 | - | CSV export code is not in this repo |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `test-r1` | old hard-stop behavior passes |
| C2 | `test-r3` | old export behavior passes |
| C3 | `test-r1-override` | without a waiver the stop still blocks; with a waiver on file an override succeeds and writes one audit record carrying the acting user and the reason; a missing reason is rejected |
| C4 | `test-r3-dealid` | exported CSV header includes deal ID and every row carries its deal's ID for the whole filtered set |

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
| H3 | reopen | R1@1 | R1@2 | chat 2026-09-24 | was "hard-stops before diligence spend, no override"; now the stop stays but a signed waiver on file lets Legal override, and each override is logged with actor and reason. W1/E1 stay bound to R1@1 and do not prove R1@2 |
| H4 | reopen | R3@1 | R3@2 | chat 2026-09-24 | was "CSV export of the whole filtered set"; now the export must also include a deal ID column for reconciliation. W2/E2 stay bound to R3@1 |

## Ignored
| id | source | kind | note |
|---|---|---|---|
