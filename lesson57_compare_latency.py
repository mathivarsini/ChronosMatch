import time
from statistics import mean
from lesson48_heap_matching import HeapMatchingEngine

ORDERS = 5000
PRICE = 25000
QUANTITY = 1


def measure_latency(engine, order_id, side, price, quantity):
    start = time.perf_counter_ns()

    trades = engine.add_order(
        order_id, side, price, quantity
    )

    end = time.perf_counter_ns()

    latency_us = (end - start) / 1000
    return latency_us, len(trades)



no_match_engine = HeapMatchingEngine()
no_match_latencies = []

for i in range(1, ORDERS + 1):
    latency, _ = measure_latency(
        no_match_engine,
        i,
        "B",
        20000,
        QUANTITY
    )
    no_match_latencies.append(latency)



match_engine = HeapMatchingEngine()
match_latencies = []
trade_count = 0

for i in range(1, ORDERS + 1):
    match_engine.add_order(
        2 * i - 1,
        "S",
        PRICE,
        QUANTITY
    )

    latency, trades = measure_latency(
        match_engine,
        2 * i,
        "B",
        PRICE,
        QUANTITY
    )

    match_latencies.append(latency)
    trade_count += trades


print("=== ChronosMatch Latency Comparison ===")

print("\nScenario 1: No matching")
print("Orders measured:", len(no_match_latencies))
print(
    f"Average latency: "
    f"{mean(no_match_latencies):.3f} microseconds"
)

print("\nScenario 2: Matching trades")
print("Buy orders measured:", len(match_latencies))
print("Completed trades:", trade_count)
print(
    f"Average latency: "
    f"{mean(match_latencies):.3f} microseconds"
)