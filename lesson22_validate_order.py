import mmap
import struct

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)

CAPACITY = 1024
TOTAL_ORDERS = 100_000


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

        struct.pack_into(
            ORDER_FORMAT, self.memory, offset,
            order[0], order[1], order[2], order[3]
        )

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


def main():
    buffer_size = CAPACITY * ORDER_SIZE

    with open("lesson22_buffer.bin", "w+b") as file:
        file.truncate(buffer_size)

        with mmap.mmap(file.fileno(), buffer_size) as memory:
            ring = RingBuffer(memory, CAPACITY)

            for i in range(1, TOTAL_ORDERS + 1):
                side = b"B" if i % 2 == 1 else b"S"
                expected = (i, float(250 + i % 100), i % 10 + 1, side)

                # Drain the oldest order if the buffer is full.
                if not ring.write(expected):
                    actual = ring.read()
                    if actual is None:
                        raise AssertionError("Unexpected empty buffer")

                    expected_oldest_id = i - CAPACITY
                    assert actual[0] == expected_oldest_id, (
                        f"FIFO error: expected ID {expected_oldest_id}, "
                        f"got {actual[0]}"
                    )

                    assert ring.write(expected), "Write failed after draining"

            # Check all remaining orders in FIFO order.
            first_remaining_id = TOTAL_ORDERS - ring.count + 1

            while ring.count > 0:
                actual = ring.read()
                expected_id = first_remaining_id
                expected = (
                    expected_id,
                    float(250 + expected_id % 100),
                    expected_id % 10 + 1,
                    b"B" if expected_id % 2 == 1 else b"S",
                )

                assert actual == expected, (
                    f"Data mismatch: expected {expected}, got {actual}"
                )
                first_remaining_id += 1

            print(f"Orders validated: {TOTAL_ORDERS:,}")
            print("FIFO order: PASS")
            print("Price, quantity and side: PASS")
            print("Buffer empty at end: PASS")
            print("Lesson 22 completed successfully!")


if __name__ == "__main__":
    main()