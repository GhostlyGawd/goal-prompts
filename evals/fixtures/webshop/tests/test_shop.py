import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pricing
from app import Cart


class Happy(unittest.TestCase):
    def test_subtotal(self):
        self.assertAlmostEqual(pricing.subtotal({"apple": 2}), 0.80, places=2)

    def test_checkout_reserves_and_totals(self):
        c = Cart()
        c.add("apple", 1)
        order = c.checkout()
        self.assertIn("total", order)

    def test_refund_exists(self):
        self.assertTrue(hasattr(Cart, "refund"))


if __name__ == "__main__":
    unittest.main()
