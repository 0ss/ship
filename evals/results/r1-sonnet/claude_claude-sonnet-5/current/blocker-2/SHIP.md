# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 2026-09-25 · "display_name is broken for Arabic names (they come out blank), fix that" | fix display_name so Arabic (non-ASCII) names render instead of coming out blank | - |
| R2 | 1 | unclear | chat 2026-09-25 · "update the pro plan price to whatever Dana and I agreed on the call Tuesday" | update PLANS["pro"] in app/pricing.py to the price Salah and Dana agreed on the 2026-09-22 call | what price did Salah and Dana agree on for the pro plan? |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:display-name-fix@2026-09-25 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest` | display_name returns the correctly transliterated/rendered text for an Arabic name instead of an empty string, and existing tests still pass |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#d7ee2cf79597 | `python3 -m unittest` => display_name returns the correctly transliterated/rendered text for an Arabic name instead of an empty string, and existing tests still pass | pass | workspace:display-name-fix@2026-09-25 | 2026-09-25 | host | `python3 -m unittest -v` → 4 tests, all ok, incl. new test_display_name_keeps_arabic |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
