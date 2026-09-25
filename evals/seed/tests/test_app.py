import unittest
from datetime import datetime

from app.display import display_name
from app.invites import InviteService
from app.notify import RecordingNotifier
from app.pricing import price


class AppTest(unittest.TestCase):
    def test_create_stores_invite(self):
        svc = InviteService(RecordingNotifier(), clock=lambda: datetime(2026, 1, 1))
        invite = svc.create("ada lovelace", "ada@example.com", "+15550001")
        self.assertEqual(svc.invites, [invite])

    def test_display_name_titles_latin(self):
        self.assertEqual(display_name("ada lovelace"), "Ada Lovelace")

    def test_price(self):
        self.assertEqual(price("team", 2), 80)


if __name__ == "__main__":
    unittest.main()
