import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calc import subtotal_cents


class T(unittest.TestCase):
    def test_total(self):
        self.assertEqual(subtotal_cents({"apple": 2, "pear": 1}), 190)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            subtotal_cents({})

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            subtotal_cents({"apple": -1})

    def test_rejects_unknown(self):
        with self.assertRaises(KeyError):
            subtotal_cents({"kiwi": 1})


if __name__ == "__main__":
    unittest.main()
