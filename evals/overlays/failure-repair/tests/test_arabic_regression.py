import unittest

from app.display import display_name


class ArabicRegression(unittest.TestCase):
    def test_arabic_name(self):
        self.assertEqual(display_name("محمد عبدالله"), "محمد عبدالله")
