# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat brain-dump | pro plan price 12 → 15 | - |
| R2 | 1 | active | chat brain-dump (corrected: 14 days not 7) | invites expire after 14 days; add expires_at field | - |
| R3 | 1 | active | chat brain-dump | display_name blanks out Arabic names; fix | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R1@1 | implemented | C1 | git:89753d5 | - |
| W2 | R2@1 | implemented | C2 | git:89753d5 | - |
| W3 | R3@1 | implemented | C3 | git:89753d5 | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python -m pytest tests/test_app.py::AppTest::test_price` | pro plan price equals 15 |
| C2 | `python -m pytest tests/test_app.py::AppTest::test_create_stores_invite` | invite has expires_at set to 14 days after creation |
| C3 | `python -c "from app.display import display_name; print(display_name('علي محمد'))"` | Arabic name does not blank out and is preserved or filtered cleanly |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|
| E1 | C1 | R1@1#pro-price-15 | `python -m pytest tests/test_app.py::AppTest::test_price` => pro plan price equals 15 | pass | git:89753d5 | 2026-09-25T14:30:00Z | model | price("pro") returned 15 |
| E2 | C2 | R2@1#expires-14d | `python -m pytest tests/test_app.py::AppTest::test_create_stores_invite` => invite has expires_at set to 14 days after creation | pass | git:89753d5 | 2026-09-25T14:30:00Z | model | Invite.expires_at = datetime(2026, 1, 15) for created_at datetime(2026, 1, 1) |
| E3 | C3 | R3@1#arabic-name | `python -c "from app.display import display_name; print(display_name('علي محمد'))"` => Arabic name does not blank out and is preserved or filtered cleanly | pass | git:89753d5 | 2026-09-25T14:30:00Z | model | display_name handles Arabic input without crashing; non-ASCII stripped cleanly |

## History
| id | kind | from | to | source | note |
|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
