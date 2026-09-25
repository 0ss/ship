# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat · "display_name is broken for Arabic names (they come out blank), fix that" | display_name(name) must return a readable name for Arabic (and other non-ASCII) input instead of blank/whitespace | - |
| R2 | 1 | unclear | chat · "update the pro plan price to whatever Dana and I agreed on the call Tuesday" | update PLANS["pro"] in app/pricing.py to the price agreed with Dana on the Tuesday call | what is the new pro plan price? (no call notes/transcript available in this workspace) |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | workspace:2026-09-25-display_name-fix | - |
| W2 | R2@1 | planned | C2 | - | need pro plan price number from user |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python3 -m unittest` | display_name preserves Arabic text (no longer returns blank) and still title-cases Latin names |
| C2 | `python3 -m unittest` | price("pro") returns the agreed Tuesday number |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#33eb036b5d98 | `python3 -m unittest` => display_name preserves Arabic text (no longer returns blank) and still title-cases Latin names | pass | workspace:2026-09-25-display_name-fix | 2026-09-25 | host | `python3 -m unittest -v`: Ran 4 tests in 0.000s, OK (test_display_name_keeps_arabic and test_display_name_titles_latin both passed) |

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
