import json, os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from score import score

KEY = json.load(open(os.path.join(os.path.dirname(__file__), "..",
                                  "answerkeys", "webshop.json")))

STRONG = """# Bug Hunt — webshop
**Date:** 2026-07-13

## Summary
6 findings — S2: 5 · S3: 1

## Findings
### 1. Race in inventory reserve
store.py reserve() does read-modify-write with no lock; two concurrent
checkouts can oversell.
### 2. Float money math
pricing.py subtotal() accumulates binary float error; use Decimal cents.
### 3. Pagination off-by-one
pagination.py page_of(): start = page * size but README says 1-based —
page=1 skips the first items.
### 4. Empty cart crash
app.py checkout() calls max() on an empty sequence — ValueError instead of
a clean error.
### 5. Negative quantity accepted
app.py add() has no validation; negative qty gives negative totals.
### 6. Cart not cleared after checkout
app.py checkout() leaves items — a second checkout call double-charges.

## Verification plan
Ran the suite: 2 passed, 1 failed. The failing test_refund_exists is
pre-existing (README marks refunds WIP) — not introduced by anything here.
"""

WEAK = """# Review
Found some issues. There might be a race somewhere. Also the discount
calculation seems off. All tests pass.
"""


class ScoreTests(unittest.TestCase):
    def test_strong_report(self):
        r = score(STRONG, KEY)
        for d in ["D1", "D2", "D3", "D4", "D7", "D8"]:
            self.assertIn(d, r["found"], d)
        self.assertIn("D5", r["missed"])
        self.assertIn("D6", r["missed"])
        self.assertEqual(r["false_alarms"], 0)
        self.assertGreaterEqual(r["evidence_rate"], 0.99)
        self.assertTrue(r["preexisting_flagged"])
        self.assertTrue(r["verification_vocab"])

    def test_weak_report(self):
        r = score(WEAK, KEY)
        self.assertNotIn("D1", r["found"])   # no file cited -> no credit
        self.assertLess(len(r["found"]), 2)
        self.assertFalse(r["preexisting_flagged"])

    def test_found_plus_missed_is_total(self):
        for text in (STRONG, WEAK, ""):
            r = score(text, KEY)
            self.assertEqual(len(r["found"]) + len(r["missed"]),
                             len(KEY["defects"]))


if __name__ == "__main__":
    unittest.main()
