# Ship
- [ ] Enforce max 5 invites per user per minute — "the requirement was max 5 invites per user per minute"; current implementation uses one global counter, ignores `user_id` and `window`, and is not wired into `InviteService`.
