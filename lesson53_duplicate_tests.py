import unittest
from lesson48_heap_matching import HeapMatchingEngine


class TestDuplicateOrderIDs(unittest.TestCase):

    def test_duplicate_id_is_rejected(self):
        engine = HeapMatchingEngine()

        engine.add_order(101, "B", 25000, 5)

        with self.assertRaisesRegex(ValueError, "Duplicate order ID"):
            engine.add_order(101, "S", 25000, 5)

        self.assertEqual(len(engine.buys), 1)
        self.assertEqual(len(engine.sells), 0)

    def test_matched_id_cannot_be_reused(self):
        engine = HeapMatchingEngine()

        engine.add_order(101, "S", 25000, 2)
        engine.add_order(102, "B", 25000, 2)

        with self.assertRaisesRegex(ValueError, "Duplicate order ID"):
            engine.add_order(101, "B", 25000, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)