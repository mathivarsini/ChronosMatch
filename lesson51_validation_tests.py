import unittest
from lesson48_heap_matching import HeapMatchingEngine


class TestOrderValidation(unittest.TestCase):

    def setUp(self):
        self.engine = HeapMatchingEngine()

    def test_reject_invalid_side(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, "X", 25000, 5)

    def test_reject_zero_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, "B", 0, 5)

    def test_reject_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, "B", 25000, -5)

    def test_reject_float_price(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(1, "B", 25000.5, 5)

    def test_reject_invalid_order_id(self):
        with self.assertRaises(ValueError):
            self.engine.add_order(0, "B", 25000, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)