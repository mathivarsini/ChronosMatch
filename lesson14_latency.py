import mmap
import time

from chronosmatch_ring_buffer import RingBuffer, ORDER_SIZE

CAPACITY = 1024
TOTAL_ORDERS = 100_000
BUFFER_SIZE = CAPACITY * ORDER_SIZE


def main():
    latencies_ns = []

    with open("lesson14_buffer.bin", "w+b") as file:
        file.write(b"\x00" * BUFFER_SIZE)
        file.flush()

        with mmap.mmap(file.fileno(), BUFFER_SIZE) as memory:
            ring = RingBuffer(memory, CAPACITY)

            for i in range(TOTAL_ORDERS):
                order = (i, 250.0, 5, b"B")

                # Make space if the buffer is full.
                if ring.count == CAPACITY:
                    ring.read()

                # Measure one write operation.
                start = time.perf_counter_ns()
                success = ring.write(order)
                end = time.perf_counter_ns()

                if not success:
                    raise RuntimeError("Unexpected full buffer")

                latencies_ns.append(end - start)

                # Read one order to keep the buffer from filling.
                if ring.count == CAPACITY:
                    ring.read()

    latencies_us = sorted(
        latency / 1000 for latency in latencies_ns
    )

    average_us = sum(latencies_us) / len(latencies_us)
    p50_us = latencies_us[len(latencies_us) // 2]
    p99_us = latencies_us[int(len(latencies_us) * 0.99)]

    print("ChronosMatch Latency Benchmark")
    print("------------------------------")
    print(f"Orders measured: {len(latencies_us):,}")
    print(f"Average latency: {average_us:.3f} microseconds")
    print(f"Median latency (p50): {p50_us:.3f} microseconds")
    print(f"99th percentile (p99): {p99_us:.3f} microseconds")


if __name__ == "__main__":
    main()