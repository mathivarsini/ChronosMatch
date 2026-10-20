import time

# Each order is: (order_id, price, quantity)

buy_orders = [
    (1, 25000, 5),
    (2, 25200, 3),
    (3, 25100, 4),
]

sell_orders = [
    (4, 25300, 2),
    (5, 25050, 6),
    (6, 25150, 3),
]

start = time.perf_counter()

best_buy = max(buy_orders, key=lambda order: order[1])
best_sell = min(sell_orders, key=lambda order: order[1])

elapsed = time.perf_counter() - start

print("Best buy order:", best_buy)
print("Best sell order:", best_sell)
print(f"Lookup time: {elapsed * 1_000_000:.2f} microseconds")