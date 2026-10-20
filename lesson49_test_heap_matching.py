import unittest
from lesson48_heap_matching import HeapMatchingEngine


class TestHeapMatchingEngine(unittest.TestCase):

    def test_full_fill(self):
        engine = HeapMatchingEngine()

        engine.add_order(1, "S", 25000, 5)
        trades = engine.add_order(2, "B", 25000, 5)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["quantity"], 5)
        self.assertEqual(len(engine.sells), 0)
        self.assertEqual(len(engine.buys), 0)

    def test_partial_fill(self):
        engine = HeapMatchingEngine()

        engine.add_order(1, "S", 25000, 10)
        trades = engine.add_order(2, "B", 25000, 4)

        self.assertEqual(trades[0]["quantity"], 4)
        self.assertEqual(engine.sells[0][3], 6)

    def test_unmatched_orders(self):
        engine = HeapMatchingEngine()

        engine.add_order(1, "S", 26000, 5)
        trades = engine.add_order(2, "B", 25000, 5)

        self.assertEqual(trades, [])
        self.assertEqual(len(engine.buys), 1)
        self.assertEqual(len(engine.sells), 1)

    def test_price_priority(self):
        engine = HeapMatchingEngine()

        engine.add_order(1, "S", 25000, 5)
        trades = engine.add_order(2, "B", 26000, 5)

        self.assertEqual(trades[0]["price"], 25000)

    def test_time_priority(self):
        engine = HeapMatchingEngine()

        engine.add_order(1, "S", 25000, 3)
        engine.add_order(2, "S", 25000, 4)

        trades = engine.add_order(3, "B", 25000, 3)

        self.assertEqual(trades[0]["sell_id"], 1)

        # The second sell order should remain.
        self.assertEqual(engine.sells[0][2], 2)
        self.assertEqual(engine.sells[0][3], 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)