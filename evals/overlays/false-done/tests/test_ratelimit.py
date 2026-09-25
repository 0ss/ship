import unittest

from app.ratelimit import RateLimiter


class RateLimiterTest(unittest.TestCase):
    def test_sixth_invite_is_blocked(self):
        limiter = RateLimiter(limit=5, window=60, clock=lambda: 0)
        results = [limiter.allow("u1") for _ in range(6)]
        self.assertEqual(results, [True] * 5 + [False])


if __name__ == "__main__":
    unittest.main()
