import heapq

# Buy orders: store negative prices to simulate a max-heap.
buy_orders = [
    (-25000, 1, 5),
    (-25200, 2, 3),
    (-25100, 3, 4),
]

# Sell orders: normal prices use a min-heap.
sell_orders = [
    (25300, 4, 2),
    (25050, 5, 6),
    (25150, 6, 3),
]

heapq.heapify(buy_orders)
heapq.heapify(sell_orders)

best_buy = heapq.heappop(buy_orders)
best_sell = heapq.heappop(sell_orders)

print("Best buy price:", -best_buy[0])
print("Best buy order ID:", best_buy[1])

print("Best sell price:", best_sell[0])
print("Best sell order ID:", best_sell[1])