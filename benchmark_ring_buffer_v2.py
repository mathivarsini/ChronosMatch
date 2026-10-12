import mmap
import time

from chronosmatch_ring_buffer import RingBuffer, ORDER_SIZE

CAPACITY = 1024
BATCHES = 100
TOTAL_ORDERS = CAPACITY * BATCHES

BUFFER_SIZE = CAPACITY * ORDER_SIZE


def benchmark():
    with open("benchmark_buffer_v2.bin", "w+b") as file:
        file.write(b"\x00" * BUFFER_SIZE)
        file.flush()

        with mmap.mmap(file.fileno(), BUFFER_SIZE) as memory:
            ring = RingBuffer(memory, CAPACITY)

            start = time.perf_counter()

            for batch in range(BATCHES):
              for i in range(CAPACITY):
                 order_id = batch * CAPACITY + i
                 order = (order_id, 250.0, 5, b"B")

                 if not ring.write(order):
                    raise RuntimeError("Unexpected full buffer")

              for _ in range(CAPACITY):
                ring.read()

            write_elapsed = time.perf_counter() - start

            # Benchmark reading
            start = time.perf_counter()
            read_count = 0

            while ring.count > 0:
                ring.read()
                read_count += 1

            read_elapsed = time.perf_counter() - start

            print("ChronosMatch Benchmark v2")
            print("-------------------------")
            print(f"Orders written: {TOTAL_ORDERS:,}")
            print(f"Orders read: {read_count:,}")
            print(f"Write time: {write_elapsed:.6f} seconds")
            print(f"Read time: {read_elapsed:.6f} seconds")

            print(
                f"Write throughput: "
                f"{TOTAL_ORDERS / write_elapsed:,.0f} orders/second"
            )

            print(
                f"Read throughput: "
                f"{read_count / read_elapsed:,.0f} orders/second"
            )

            assert read_count == TOTAL_ORDERS
            assert ring.count == 0

            print("Benchmark completed successfully!")


if __name__ == "__main__":
    benchmark()