# Ship
- [ ] invite rate limiter in app/ratelimit.py enforces max 5 invites per user per minute — BROKEN: counter is global (not per-user) and never resets after the window (proof: `limiter.allow('u1')`x5 then `limiter.allow('u2')` → False; after clock+61s, u1 still blocked). Existing test only covers single user within one window, doesn't catch either bug. Needs fix, not shippable as-is.
