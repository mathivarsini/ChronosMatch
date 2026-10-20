import heapq
import itertools


class HeapOrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.sequence = itertools.count()

    def add_order(self, order_id, side, price, quantity):
        seq = next(self.sequence)

        if side == "B":
            # Negative price: highest buy price comes first.
            heapq.heappush(
                self.buy_orders,
                (-price, seq, order_id, quantity)
            )
        elif side == "S":
            # Lowest sell price comes first.
            heapq.heappush(
                self.sell_orders,
                (price, seq, order_id, quantity)
            )
        else:
            raise ValueError("Side must be B or S")

    def best_buy(self):
        if not self.buy_orders:
            return None
        return self.buy_orders[0]

    def best_sell(self):
        if not self.sell_orders:
            return None
        return self.sell_orders[0]


book = HeapOrderBook()

book.add_order(101, "B", 25000, 5)
book.add_order(102, "B", 25200, 3)
book.add_order(103, "B", 25200, 4)

book.add_order(201, "S", 25300, 2)
book.add_order(202, "S", 25050, 6)

buy = book.best_buy()
sell = book.best_sell()

print("Best buy:", (-buy[0], buy[2], buy[3]))
print("Best sell:", (sell[0], sell[2], sell[3]))