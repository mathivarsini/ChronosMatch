import time
from lesson48_heap_matching import HeapMatchingEngine

PAIRS = 5000
PRICE = 25000
QUANTITY = 1

engine = HeapMatchingEngine()
trade_count = 0

total_orders = PAIRS * 2

start = time.perf_counter()

for pair in range(1, PAIRS + 1):
    engine.add_order(
        2 * pair - 1, "S", PRICE, QUANTITY
    )

    trades = engine.add_order(
        2 * pair, "B", PRICE, QUANTITY
    )

    trade_count += len(trades)

elapsed = time.perf_counter() - start

throughput = total_orders / elapsed if elapsed > 0 else 0

print("=== Validated Engine Benchmark ===")
print("Total orders:", total_orders)
print("Completed trades:", trade_count)
print(f"Elapsed time: {elapsed:.6f} seconds")
print(f"Throughput: {throughput:,.0f} orders/second")
print("Remaining buy orders:", len(engine.buys))
print("Remaining sell orders:", len(engine.sells))