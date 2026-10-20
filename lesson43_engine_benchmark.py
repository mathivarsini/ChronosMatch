import time
from chronosmatch_engine import OrderBook

PAIRS = 5000
PRICE = 25000  # ₹250.00 represented in paise
QUANTITY = 1

book = OrderBook()
trade_count = 0

total_orders = PAIRS * 2

start = time.perf_counter()

for pair in range(1, PAIRS + 1):
    # Add a sell order
    book.add_order(
        2 * pair - 1, "S", PRICE, QUANTITY
    )

    # Add a matching buy order
    trades = book.add_order(
        2 * pair, "B", PRICE, QUANTITY
    )

    trade_count += len(trades)

end = time.perf_counter()

elapsed = end - start
throughput = total_orders / elapsed if elapsed > 0 else 0

print("=== ChronosMatch Engine Benchmark ===")
print(f"Total orders: {total_orders}")
print(f"Completed trades: {trade_count}")
print(f"Elapsed time: {elapsed:.6f} seconds")
print(f"Throughput: {throughput:,.0f} orders/second")