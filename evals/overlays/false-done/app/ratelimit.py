import time


class RateLimited(Exception):
    pass


class RateLimiter:
    """Allow at most `limit` invites per user per `window` seconds."""

    def __init__(self, limit=5, window=60, clock=time.monotonic):
        self.limit = limit
        self.window = window
        self.clock = clock
        self.count = 0
        self.started = clock()

    def allow(self, user_id):
        self.count += 1
        return self.count <= self.limit
