# Ship
schema: 1

## Requirements
| id | revision | disposition | source | request | question |
|---|---:|---|---|---|---|
| R1 | 1 | active | chat 0:00 · "creating an invite should email" | creating an invite calls notifier.send_email to the invite's email | - |
| R2 | 1 | active | chat 0:00 · "pro plan is 15 now" | pricing.PLANS["pro"] = 15 (was 12) | - |
| R3 | 1 | active | chat 0:00 · "Arabic names blank" | display_name handles Unicode properly (Arabic names no longer blank) | - |
| R4 | 1 | active | chat 0:00 · "expire after 7 days" | Invite has expires_at field and is_expired(now) method | - |

## Work
| id | covers | progress | check | code | blocked_by |
|---|---|---|---|---|---|
| W1 | R2@1 | planned | C1 | - | - |
| W2 | R3@1 | planned | C2 | - | - |
| W3 | R4@1 | planned | C3 | - | - |
| W4 | R1@1 | planned | C4 | - | - |

## Checks
| id | command | done_when |
|---|---|---|
| C1 | `python -c "from app.pricing import PLANS; assert PLANS['pro'] == 15"` | pro plan price is 15 |
| C2 | `python -c "from app.display import display_name; assert display_name('محمد') == 'محمد'.title()"` | Arabic names preserved in display_name |
| C3 | `npm test 2>&1 \| grep -E "is_expired|expires_at"` | Invite has expires_at and is_expired method |
| C4 | `npm test 2>&1 \| grep -E "send_email"` | creating invite calls notifier.send_email |

## Evidence
| id | check | intent | contract | result | code | ran | by | receipt |
|---|---|---|---|---|---|---|---|---|

## History
| id | kind | from | to | source | note |
|---|---|---|---|---|---|

## Ignored
| id | source | kind | note |
|---|---|---|---|
