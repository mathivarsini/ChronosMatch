import mmap
import time

from chronosmatch_ring_buffer import RingBuffer, ORDER_SIZE

CAPACITY = 1024
TOTAL_ORDERS = 100_000


def main():
    size = CAPACITY * ORDER_SIZE

    with open("lesson24_buffer.bin", "w+b") as file:
        file.truncate(size)

        with mmap.mmap(file.fileno(), size) as memory:
            ring = RingBuffer(memory, CAPACITY)
            start = time.perf_counter()

            for i in range(1, TOTAL_ORDERS + 1):
                order = (i, 250.0, 5, b"B")

                if not ring.write(order):
                    ring.read()
                    if not ring.write(order):
                        raise RuntimeError("Could not write order")

            while ring.count > 0:
                ring.read()

            elapsed = time.perf_counter() - start
            throughput = TOTAL_ORDERS / elapsed

            print("ChronosMatch Week 1 Benchmark")
            print("-----------------------------")
            print(f"Orders processed: {TOTAL_ORDERS:,}")
            print(f"Elapsed time: {elapsed:.6f} seconds")
            print(f"Throughput: {throughput:,.0f} orders/second")
            print(f"Remaining orders: {ring.count}")


if __name__ == "__main__":
    main()