import unittest
from lesson48_heap_matching import HeapMatchingEngine


class TestOrderBookState(unittest.TestCase):

    def test_invalid_order_does_not_change_book(self):
        engine = HeapMatchingEngine()

        # Add a valid, unmatched buy order.
        engine.add_order(101, "B", 25000, 5)

        # Save the current state.
        buys_before = engine.buys.copy()
        sells_before = engine.sells.copy()

        # An invalid order should raise ValueError.
        with self.assertRaises(ValueError):
            engine.add_order(102, "X", 25000, 3)

        # The order book must remain unchanged.
        self.assertEqual(engine.buys, buys_before)
        self.assertEqual(engine.sells, sells_before)

    def test_invalid_price_does_not_change_book(self):
        engine = HeapMatchingEngine()

        engine.add_order(101, "S", 26000, 4)

        sells_before = engine.sells.copy()

        with self.assertRaises(ValueError):
            engine.add_order(102, "B", -100, 2)

        self.assertEqual(engine.sells, sells_before)
        self.assertEqual(engine.buys, [])

    def test_invalid_quantity_does_not_change_book(self):
        engine = HeapMatchingEngine()

        engine.add_order(101, "B", 25000, 5)

        buys_before = engine.buys.copy()

        with self.assertRaises(ValueError):
            engine.add_order(102, "B", 25000, 0)

        self.assertEqual(engine.buys, buys_before)


if __name__ == "__main__":
    unittest.main(verbosity=2)