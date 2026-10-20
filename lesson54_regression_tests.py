import unittest
from lesson48_heap_matching import HeapMatchingEngine


class TestChronosMatchRegression(unittest.TestCase):

    def setUp(self):
        self.engine = HeapMatchingEngine()

    def test_valid_order_is_accepted(self):
        trades = self.engine.add_order(1, "B", 25000, 5)

        self.assertEqual(trades, [])
        self.assertEqual(len(self.engine.buys), 1)

    def test_invalid_side_is_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, "X", 25000, 5)

        self.assertEqual(self.engine.buys, [])
        self.assertEqual(self.engine.sells, [])

    def test_duplicate_id_is_rejected(self):
        self.engine.add_order(1, "B", 25000, 5)

        with self.assertRaises(ValueError):
            self.engine.add_order(1, "S", 25000, 5)

        self.assertEqual(len(self.engine.buys), 1)
        self.assertEqual(self.engine.sells, [])

    def test_partial_fill(self):
        self.engine.add_order(1, "S", 25000, 10)
        trades = self.engine.add_order(2, "B", 25000, 4)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["quantity"], 4)
        self.assertEqual(self.engine.sells[0][3], 6)

    def test_best_sell_price_is_matched_first(self):
        self.engine.add_order(1, "S", 26000, 3)
        self.engine.add_order(2, "S", 25000, 3)

        trades = self.engine.add_order(3, "B", 26000, 3)

        self.assertEqual(trades[0]["sell_id"], 2)
        self.assertEqual(trades[0]["price"], 25000)

    def test_earlier_same_price_order_is_matched_first(self):
        self.engine.add_order(1, "S", 25000, 2)
        self.engine.add_order(2, "S", 25000, 4)

        trades = self.engine.add_order(3, "B", 25000, 2)

        self.assertEqual(trades[0]["sell_id"], 1)
        self.assertEqual(self.engine.sells[0][2], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)