# Ship
- [x] Enforce at most 5 invites per user per minute — repaired `RateLimiter` to track independent sliding-window timestamps per user; proof: `python3 -m unittest -v` → 7 tests, all OK, including sixth-request blocking, user isolation, window expiry, and rejected-attempt accounting.
