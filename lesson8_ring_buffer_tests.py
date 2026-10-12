import mmap
import struct

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)


class RingBuffer:
    def __init__(self, memory, capacity):
        self.memory = memory
        self.capacity = capacity
        self.write_pointer = 0
        self.read_pointer = 0
        self.count = 0

    def write(self, order):
        if self.count >= self.capacity:
            return False

        offset = self.write_pointer * ORDER_SIZE
        self.memory.seek(offset)
        self.memory.write(struct.pack(ORDER_FORMAT, *order))

        self.write_pointer = (self.write_pointer + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_pointer * ORDER_SIZE
        self.memory.seek(offset)
        data = self.memory.read(ORDER_SIZE)

        order = struct.unpack(ORDER_FORMAT, data)

        self.read_pointer = (self.read_pointer + 1) % self.capacity
        self.count -= 1
        return order


def run_tests():
    capacity = 3
    buffer_size = capacity * ORDER_SIZE

    with open("lesson8_test.bin", "w+b") as file:
        file.write(b"\x00" * buffer_size)
        file.flush()

        with mmap.mmap(file.fileno(), buffer_size) as memory:
            ring = RingBuffer(memory, capacity)

            # Test 1: Empty buffer
            assert ring.read() is None
            print("PASS: Empty-buffer test")

            # Test 2: Fill the buffer
            assert ring.write((101, 250.0, 2, b"B"))
            assert ring.write((102, 251.0, 3, b"S"))
            assert ring.write((103, 252.0, 4, b"B"))
            print("PASS: Write test")

            # Test 3: Reject a fourth order
            assert not ring.write((104, 253.0, 5, b"S"))
            print("PASS: Full-buffer test")

            # Test 4: FIFO reading
            assert ring.read()[0] == 101
            assert ring.read()[0] == 102
            print("PASS: FIFO test")

            # Test 5: Wraparound
            assert ring.write((104, 253.0, 5, b"S"))
            assert ring.write((105, 254.0, 6, b"B"))
            print("PASS: Wraparound write test")

            # Remaining orders must still be FIFO
            assert ring.read()[0] == 103
            assert ring.read()[0] == 104
            assert ring.read()[0] == 105
            assert ring.read() is None
            print("PASS: Final FIFO and empty-buffer tests")

            assert ring.count == 0
            print("PASS: Final count is zero")

    print("\nAll tests passed!")


if __name__ == "__main__":
    run_tests()