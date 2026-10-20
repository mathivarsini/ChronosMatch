import mmap
import struct
import time

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)

CAPACITY = 1024
TOTAL_ORDERS = 1_000_000


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
        order = struct.unpack_from(
            ORDER_FORMAT, self.memory, offset
        )

        self.read_pointer = (self.read_pointer + 1) % self.capacity
        self.count -= 1
        return order


def main():
    buffer_size = CAPACITY * ORDER_SIZE

    with open("lesson21_buffer.bin", "w+b") as file:
        file.truncate(buffer_size)

        with mmap.mmap(file.fileno(), buffer_size) as memory:
            ring = RingBuffer(memory, CAPACITY)
            start = time.perf_counter()
            processed = 0

            for i in range(TOTAL_ORDERS):
                order = (i + 1, 250.0, 5, b"B")

                if not ring.write(order):
                    ring.read()
                    if not ring.write(order):
                        raise RuntimeError("Buffer write failed")

                processed += 1

            while ring.count > 0:
                ring.read()

            elapsed = time.perf_counter() - start
            throughput = processed / elapsed

            print(f"Orders submitted: {processed:,}")
            print(f"Elapsed time: {elapsed:.4f} seconds")
            print(f"Throughput: {throughput:,.0f} orders/second")
            print(f"Orders remaining: {ring.count}")

            if ring.count == 0:
                print("Stress test completed successfully!")


if __name__ == "__main__":
    main()