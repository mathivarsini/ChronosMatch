import mmap
import struct
import tempfile
import unittest

ORDER_FORMAT = "<qqqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
CAPACITY = 3


class RingBuffer:
    def __init__(self, memory, capacity):
        self.memory = memory
        self.capacity = capacity
        self.write_pos = 0
        self.read_pos = 0
        self.count = 0

    def write(self, order):
        order_id, price, quantity, side = order

        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if side not in (b"B", b"S"):
            raise ValueError("Side must be B or S")

        if self.count == self.capacity:
            return False

        offset = self.write_pos * ORDER_SIZE
        struct.pack_into(ORDER_FORMAT, self.memory, offset, *order)

        self.write_pos = (self.write_pos + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_pos * ORDER_SIZE
        order = struct.unpack_from(
            ORDER_FORMAT, self.memory, offset
        )

        self.read_pos = (self.read_pos + 1) % self.capacity
        self.count -= 1
        return order


class TestRingBuffer(unittest.TestCase):
    def setUp(self):
        self.file = tempfile.TemporaryFile()
        self.file.truncate(CAPACITY * ORDER_SIZE)

        self.memory = mmap.mmap(
            self.file.fileno(), CAPACITY * ORDER_SIZE
        )
        self.buffer = RingBuffer(self.memory, CAPACITY)

    def tearDown(self):
        self.memory.close()
        self.file.close()

    def make_order(self, order_id):
        return (order_id, 25000, 5, b"B")

    def test_empty_buffer(self):
        self.assertIsNone(self.buffer.read())

    def test_full_buffer(self):
        for order_id in range(1, CAPACITY + 1):
            self.assertTrue(
                self.buffer.write(self.make_order(order_id))
            )

        self.assertFalse(
            self.buffer.write(self.make_order(4))
        )

    def test_fifo_order(self):
        self.buffer.write(self.make_order(1))
        self.buffer.write(self.make_order(2))

        self.assertEqual(self.buffer.read()[0], 1)
        self.assertEqual(self.buffer.read()[0], 2)

    def test_wraparound(self):
        for order_id in range(1, 4):
            self.buffer.write(self.make_order(order_id))

        self.assertEqual(self.buffer.read()[0], 1)
        self.assertTrue(self.buffer.write(self.make_order(4)))

        self.assertEqual(self.buffer.read()[0], 2)
        self.assertEqual(self.buffer.read()[0], 3)
        self.assertEqual(self.buffer.read()[0], 4)

    def test_invalid_order(self):
        invalid_order = (1, 25000, 5, b"X")

        with self.assertRaises(ValueError):
            self.buffer.write(invalid_order)

        self.assertEqual(self.buffer.count, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)