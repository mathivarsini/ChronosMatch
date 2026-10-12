import mmap
import time

from chronosmatch_ring_buffer import RingBuffer, ORDER_SIZE

CAPACITY = 1024
TOTAL_ORDERS = 100_000

BUFFER_SIZE = CAPACITY * ORDER_SIZE


def benchmark():
    with open("benchmark_buffer.bin", "w+b") as file:
        file.write(b"\x00" * BUFFER_SIZE)
        file.flush()

        with mmap.mmap(file.fileno(), BUFFER_SIZE) as memory:
            ring = RingBuffer(memory, CAPACITY)

            # Measure writing orders
            start = time.perf_counter()

            for i in range(TOTAL_ORDERS):
                order = (i, 250.0, 5, b"B")

                # Keep writing if the buffer is full
                while not ring.write(order):
                    ring.read()

            write_elapsed = time.perf_counter() - start

            # Measure reading any orders still in the buffer
            start = time.perf_counter()

            read_count = 0
            while ring.count > 0:
                ring.read()
                read_count += 1

            read_elapsed = time.perf_counter() - start

            print("ChronosMatch Ring Buffer Benchmark")
            print("----------------------------------")
            print(f"Orders submitted: {TOTAL_ORDERS}")
            print(f"Write phase time: {write_elapsed:.6f} seconds")
            print(
                f"Write-phase throughput: "
                f"{TOTAL_ORDERS / write_elapsed:,.0f} orders/second"
            )
            print(f"Final orders read: {read_count}")
            print(f"Read phase time: {read_elapsed:.6f} seconds")

            if read_elapsed > 0:
                print(
                    f"Read throughput: "
                    f"{read_count / read_elapsed:,.0f} orders/second"
                )


if __name__ == "__main__":
    benchmark()