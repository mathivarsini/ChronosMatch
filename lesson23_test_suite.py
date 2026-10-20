import mmap
import struct

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)


class RingBuffer:
    def __init__(self, memory, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        if len(memory) < capacity * ORDER_SIZE:
            raise ValueError("Mapped memory is too small")

        self.memory = memory
        self.capacity = capacity
        self.write_pointer = 0
        self.read_pointer = 0
        self.count = 0

    def write(self, order):
        if self.count == self.capacity:
            return False

        offset = self.write_pointer * ORDER_SIZE
        struct.pack_into(ORDER_FORMAT, self.memory, offset, *order)

        self.write_pointer = (self.write_pointer + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_pointer * ORDER_SIZE
        order = struct.unpack_from(ORDER_FORMAT, self.memory, offset)

        self.read_pointer = (self.read_pointer + 1) % self.capacity
        self.count -= 1
        return order


def test_empty_buffer():
    with create_buffer(3) as ring:
        assert ring.read() is None


def test_full_buffer():
    with create_buffer(2) as ring:
        assert ring.write((1, 100.0, 2, b"B"))
        assert ring.write((2, 101.0, 3, b"S"))
        assert not ring.write((3, 102.0, 4, b"B"))


def test_fifo():
    with create_buffer(3) as ring:
        first = (1, 100.0, 2, b"B")
        second = (2, 101.0, 3, b"S")

        ring.write(first)
        ring.write(second)

        assert ring.read() == first
        assert ring.read() == second


def test_wraparound():
    with create_buffer(2) as ring:
        ring.write((1, 100.0, 1, b"B"))
        ring.write((2, 101.0, 1, b"S"))
        assert ring.read()[0] == 1

        assert ring.write((3, 102.0, 1, b"B"))
        assert ring.read()[0] == 2
        assert ring.read()[0] == 3


class create_buffer:
    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        self.file = open("lesson23_buffer.bin", "w+b")
        size = self.capacity * ORDER_SIZE
        self.file.truncate(size)
        self.memory = mmap.mmap(self.file.fileno(), size)
        self.ring = RingBuffer(self.memory, self.capacity)
        return self.ring

    def __exit__(self, exc_type, exc_value, traceback):
        self.memory.close()
        self.file.close()
        return False


if __name__ == "__main__":
    tests = [
        test_empty_buffer,
        test_full_buffer,
        test_fifo,
        test_wraparound,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("All Lesson 23 tests passed!")