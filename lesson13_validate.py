TOTAL_ORDERS = 102_400
TARGET_THROUGHPUT = 100_000

# Replace these example values with your actual benchmark results.
elapsed_seconds = 0.8
orders_processed = 102_400

if elapsed_seconds <= 0:
    raise ValueError("Elapsed time must be positive")

if orders_processed != TOTAL_ORDERS:
    print("WARNING: The processed order count is incorrect.")
else:
    print("Order count verified.")

throughput = orders_processed / elapsed_seconds

print(f"Orders processed: {orders_processed:,}")
print(f"Elapsed time: {elapsed_seconds:.4f} seconds")
print(f"Throughput: {throughput:,.0f} orders/second")
print(f"Target: {TARGET_THROUGHPUT:,} orders/second")

if throughput >= TARGET_THROUGHPUT:
    print("Throughput target met in this measurement.")
else:
    print("Throughput target not met in this measurement.")