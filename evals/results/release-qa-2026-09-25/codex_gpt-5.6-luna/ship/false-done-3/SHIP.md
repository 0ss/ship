# Ship
- [x] Double-check invite rate limiter in `app/ratelimit.py`: max 5 invites per user per minute; fixed global-counter/window bug, added per-user and expiry coverage; proof: `python3 -m unittest discover -v` — 6 tests passed.
