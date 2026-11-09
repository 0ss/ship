import unittest
from datetime import datetime, timedelta

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


class PricingTest(unittest.TestCase):
    def test_pro_plan_is_15(self):
        self.assertEqual(price("pro"), 15)

    def test_team_stays_40_and_free_stays_0(self):
        self.assertEqual(price("team"), 40)
        self.assertEqual(price("free"), 0)


class ExpiryTest(unittest.TestCase):
    T0 = datetime(2026, 1, 1, 12, 0, 0)

    def service(self):
        return InviteService(RecordingNotifier(), clock=lambda: self.T0)

    def test_invite_expires_exactly_14_days_after_creation(self):
        invite = self.service().create("Ada Lovelace", "ada@example.com", "+15550001")
        self.assertEqual(invite.created_at, self.T0)
        self.assertEqual(invite.expires_at, self.T0 + timedelta(days=14))

    def test_is_expired_flips_only_after_expiry(self):
        invite = self.service().create("Ada", "ada@example.com", "+15550001")
        self.assertFalse(invite.is_expired(self.T0 + timedelta(days=13, hours=23, minutes=59)))
        self.assertTrue(invite.is_expired(self.T0 + timedelta(days=14)))
        self.assertTrue(invite.is_expired(self.T0 + timedelta(days=14, seconds=1)))

    def test_is_expired_defaults_to_now(self):
        stale = InviteService(RecordingNotifier(),
                              clock=lambda: datetime.utcnow() - timedelta(days=15))
        self.assertTrue(stale.create("Ada", "a@example.com", "+15550001").is_expired())
        fresh = InviteService(RecordingNotifier())  # real clock: expires in 14 days
        self.assertFalse(fresh.create("Ada", "a@example.com", "+15550001").is_expired())


class DisplayTest(unittest.TestCase):
    def test_arabic_names_survive(self):
        self.assertEqual(display_name("محمد عبدالله"), "محمد عبدالله")

    def test_long_arabic_name_shortens_at_word_boundary(self):
        long_name = "عبدالرحمن بن عبدالعزيز بن محمد آل سعود"
        short = display_name(long_name)
        self.assertLessEqual(len(short), 24)
        self.assertTrue(short.endswith("…"))
        kept = short.rstrip("…")
        self.assertTrue(long_name.startswith(kept))
        self.assertIn(long_name[len(kept):len(kept) + 1], (" ", ""))

    def test_long_latin_name_shortens_and_titles(self):
        short = display_name("ada lovelace smith jonesson")
        self.assertEqual(short, "Ada Lovelace Smith…")


if __name__ == "__main__":
    unittest.main()
