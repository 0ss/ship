# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 2 | active | chat day1 09:12 · "only the selected card gets the brand color" | normal cards stay neutral, selected card uses the brand color | - |
| R2 | 1 | deferred | chat day2 10:03 · "park it until next month" | CSV export of the filtered list | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@2 | blocked | - | - | no app source in repo, only scripts/ship-state.py |

## Checks
| id | command | done_when |
|---|---|---|

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|
| H1 | correction | R1@1 | R1@2 | chat day1 09:12 | was "make the cards blue, selected ones brighter", now "cards neutral, brand color only on the selected card" |
| H2 | defer | R2@1 | R2@1 | chat day2 10:03 | export parked until next month, not dropped |
| H3 | decision | R1@2 | R1@2 | chat day3 16:20 | restated same ask, keep R1 and do not open a second requirement |

## Ignored
| id | source | kind | note |
|---|---|---|---|
