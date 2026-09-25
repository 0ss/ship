# Ship
- [x] invite rate limiter allows max 5 invites per user per minute — proof: `python3 -m unittest discover -v` 6 tests OK, including per-user isolation, sixth-call rejection, and reset at 60 seconds
