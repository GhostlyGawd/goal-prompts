"""The scaffold's one product test — the pinning test for AC-1."""
import unittest

from src.product import health


class TestSmoke(unittest.TestCase):
    def test_ac_1_health(self):
        self.assertEqual(health(), "ok")


if __name__ == "__main__":
    unittest.main()
