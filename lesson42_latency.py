import time
import statistics


def process_order(order_id):
    price = 25000 + (order_id % 100)
    quantity = (order_id % 10) + 1
    return price * quantity


def main():
    total_orders = 10000
    latencies_ns = []

    for order_id in range(1, total_orders + 1):
        start = time.perf_counter_ns()

        process_order(order_id)

        end = time.perf_counter_ns()
        latencies_ns.append(end - start)

    sorted_latencies = sorted(latencies_ns)

    def percentile(values, percent):
        index = int((percent / 100) * len(values))
        index = min(index, len(values) - 1)
        return values[index]

    print("Orders measured:", total_orders)
    print(
        f"Average latency: "
        f"{statistics.mean(latencies_ns) / 1000:.3f} microseconds"
    )
    print(
        f"p50 latency: "
        f"{percentile(sorted_latencies, 50) / 1000:.3f} microseconds"
    )
    print(
        f"p95 latency: "
        f"{percentile(sorted_latencies, 95) / 1000:.3f} microseconds"
    )
    print(
        f"p99 latency: "
        f"{percentile(sorted_latencies, 99) / 1000:.3f} microseconds"
    )


if __name__ == "__main__":
    main()