import time
from statistics import mean
from lesson48_heap_matching import HeapMatchingEngine

PAIRS = 2500
PRICE = 25000
QUANTITY = 1

engine = HeapMatchingEngine()
latencies = []
trade_count = 0

for pair in range(1, PAIRS + 1):

    # Measure sell-order processing latency
    start = time.perf_counter_ns()

    engine.add_order(
        2 * pair - 1, "S", PRICE, QUANTITY
    )

    end = time.perf_counter_ns()
    latencies.append((end - start) / 1000)

    # Measure buy-order processing latency
    start = time.perf_counter_ns()

    trades = engine.add_order(
        2 * pair, "B", PRICE, QUANTITY
    )

    end = time.perf_counter_ns()
    latencies.append((end - start) / 1000)

    trade_count += len(trades)

# Sort the measurements
latencies.sort()

def percentile(values, percent):
    index = int((percent / 100) * len(values))
    index = min(index, len(values) - 1)
    return values[index]

print("=== ChronosMatch Latency Benchmark ===")
print("Total orders:", len(latencies))
print("Completed trades:", trade_count)
print(f"Average latency: {mean(latencies):.3f} microseconds")
print(f"P50 latency: {percentile(latencies, 50):.3f} microseconds")
print(f"P95 latency: {percentile(latencies, 95):.3f} microseconds")
print(f"P99 latency: {percentile(latencies, 99):.3f} microseconds")