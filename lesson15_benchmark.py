import mmap
import time

from chronosmatch_ring_buffer import RingBuffer, ORDER_SIZE

CAPACITY = 1024
ORDERS_PER_ROUND = 20_000
ROUNDS = 3
BUFFER_SIZE = CAPACITY * ORDER_SIZE


def percentile(values, percent):
    ordered = sorted(values)
    index = int((percent / 100) * len(ordered))
    index = min(index, len(ordered) - 1)
    return ordered[index]


def main():
    with open("lesson15_buffer.bin", "w+b") as file:
        file.write(b"\x00" * BUFFER_SIZE)
        file.flush()

        with mmap.mmap(file.fileno(), BUFFER_SIZE) as memory:
            ring = RingBuffer(memory, CAPACITY)

            for round_number in range(1, ROUNDS + 1):
                latencies = []
                start_round = time.perf_counter()

                for i in range(ORDERS_PER_ROUND):
                    order = (i, 250.0, 5, b"B")

                    start = time.perf_counter_ns()
                    success = ring.write(order)
                    end = time.perf_counter_ns()

                    if not success:
                        raise RuntimeError("Buffer unexpectedly full")

                    latencies.append((end - start) / 1000)

                    # Drain outside the timed write operation.
                    ring.read()

                elapsed = time.perf_counter() - start_round
                throughput = ORDERS_PER_ROUND / elapsed

                print(f"\nRound {round_number}")
                print(f"Orders: {ORDERS_PER_ROUND:,}")
                print(f"Average write latency: "
                      f"{sum(latencies) / len(latencies):.3f} us")
                print(f"P50 write latency: "
                      f"{percentile(latencies, 50):.3f} us")
                print(f"P99 write latency: "
                      f"{percentile(latencies, 99):.3f} us")
                print(f"Combined write/read throughput: "
                      f"{throughput:,.0f} orders/second")

            assert ring.count == 0
            print("\nAll benchmark rounds completed.")


if __name__ == "__main__":
    main()