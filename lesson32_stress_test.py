import mmap
import struct

ORDER_FORMAT = "<qqqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)

CAPACITY = 128
TOTAL_ORDERS = 10_000


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
        if self.count >= self.capacity:
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


def make_order(order_id):
    price_units = 25_000 + (order_id % 100)
    quantity = order_id % 10 + 1
    side = b"B" if order_id % 2 else b"S"

    return (order_id, price_units, quantity, side)


def main():
    size = CAPACITY * ORDER_SIZE

    with open("lesson32_buffer.bin", "w+b") as file:
        file.truncate(size)

        with mmap.mmap(file.fileno(), size) as memory:
            ring = RingBuffer(memory, CAPACITY)

            written = 0
            read_count = 0

            for order_id in range(1, TOTAL_ORDERS + 1):
                order = make_order(order_id)

                # If full, read and verify the oldest order.
                if not ring.write(order):
                    expected = make_order(read_count + 1)
                    actual = ring.read()

                    assert actual == expected, (
                        f"Mismatch: expected {expected}, got {actual}"
                    )
                    read_count += 1

                    assert ring.write(order)

                written += 1

            # Verify all orders still in the buffer.
            while ring.count:
                expected = make_order(read_count + 1)
                actual = ring.read()

                assert actual == expected, (
                    f"Mismatch: expected {expected}, got {actual}"
                )
                read_count += 1

            assert written == TOTAL_ORDERS
            assert read_count == TOTAL_ORDERS
            assert ring.count == 0

            print(f"Orders written: {written:,}")
            print(f"Orders verified: {read_count:,}")
            print(f"Buffer capacity: {CAPACITY}")
            print("FIFO and wraparound: PASS")
            print("All Lesson 32 tests passed!")


if __name__ == "__main__":
    main()