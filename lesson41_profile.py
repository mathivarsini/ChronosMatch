import cProfile
import pstats
import time


def process_orders(total_orders):
    total = 0

    for order_id in range(1, total_orders + 1):
        price = 25000 + (order_id % 100)
        quantity = (order_id % 10) + 1
        total += price * quantity

    return total


def main():
    total_orders = 500_000

    start = time.perf_counter()
    result = process_orders(total_orders)
    elapsed = time.perf_counter() - start

    print("Orders processed:", total_orders)
    print("Result checksum:", result)
    print(f"Elapsed time: {elapsed:.6f} seconds")
    print(f"Throughput: {total_orders / elapsed:,.0f} operations/sec")

    print("\n--- Profiling results ---")
    profiler = cProfile.Profile()
    profiler.enable()
    process_orders(total_orders)
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(10)


if __name__ == "__main__":
    main()