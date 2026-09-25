# Ship
- [x] Verify invite rate limiting end to end — “at most 5 invite creations per user per 60 seconds; injected limiter; blocked creates raise RateLimited without adding; users independent; quota resets after 60 seconds.” Proof: `python3 -m unittest -v` — 7 tests passed, including service-level blocked-create/no-append, independent users, and 60-second reset.
