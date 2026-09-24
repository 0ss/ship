# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat:tuesday | export the filtered list as CSV | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:empty | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `npm test -- export` | the export contains every filtered row |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#05884f97127f | `npm test -- export` => the export contains every filtered row | blocked | workspace:empty | - | host | blocked: `npm test -- export` (runner unavailable) |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
