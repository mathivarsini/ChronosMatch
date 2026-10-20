import unittest
from chronosmatch_engine import OrderBook


class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook()

    def test_full_match(self):
        self.book.add_order(1, "S", 100, 5)
        trades = self.book.add_order(2, "B", 100, 5)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["quantity"], 5)

    def test_partial_match(self):
        self.book.add_order(1, "S", 100, 10)
        trades = self.book.add_order(2, "B", 100, 4)

        self.assertEqual(trades[0]["quantity"], 4)
        self.assertEqual(self.book.sells[0]["quantity"], 6)

    def test_invalid_order(self):
        with self.assertRaises(ValueError):
            self.book.add_order(1, "X", 100, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)