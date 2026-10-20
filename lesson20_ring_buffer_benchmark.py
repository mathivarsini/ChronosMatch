import mmap
import struct
import time

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
        if self.count == self.capacity:
            return False

        offset = self.write_pointer * ORDER_SIZE

        struct.pack_into(
            ORDER_FORMAT,
            self.memory,
            offset,
            order[0],
            order[1],
            order[2],
            order[3],
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

    with open("lesson20_buffer.bin", "w+b") as file:
        file.write(b"\x00" * buffer_size)
        file.flush()

        with mmap.mmap(file.fileno(), buffer_size) as memory:
            ring = RingBuffer(memory, CAPACITY)

            start = time.perf_counter()

            for i in range(TOTAL_ORDERS):
                order = (i + 1, 250.0, 5, b"B")

                while not ring.write(order):
                    ring.read()

            while ring.count > 0:
                ring.read()

            elapsed = time.perf_counter() - start
            throughput = TOTAL_ORDERS / elapsed

            print(f"Orders processed: {TOTAL_ORDERS:,}")
            print(f"Elapsed time: {elapsed:.6f} seconds")
            print(f"Throughput: {throughput:,.0f} orders/second")
            print("Benchmark completed successfully!")


if __name__ == "__main__":
    main()