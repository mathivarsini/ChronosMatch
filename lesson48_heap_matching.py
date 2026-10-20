import heapq
import itertools


class HeapMatchingEngine:
    def __init__(self):
        self.buys = []
        self.sells = []
        self.sequence = itertools.count()

    def add_order(self, order_id, side, price, quantity):
        # Validate order ID
        if not isinstance(order_id, int) or isinstance(order_id, bool):
            raise ValueError("Order ID must be an integer")

        if not 1 <= order_id <= 2**63 - 1:
            raise ValueError("Order ID is out of range")

        # Validate side
        if side not in ("B", "S"):
            raise ValueError("Side must be B or S")

        # Validate price
        if not isinstance(price, int) or isinstance(price, bool):
            raise ValueError("Price must be an integer in paise")

        if not 1 <= price <= 2**63 - 1:
            raise ValueError("Price must be positive and in range")

        # Validate quantity
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be an integer")

        if not 1 <= quantity <= 2**63 - 1:
            raise ValueError("Quantity must be positive and in range")

        seq = next(self.sequence)

        if side == "B":
            heapq.heappush(
                self.buys,
                (-price, seq, order_id, quantity)
            )
        else:
            heapq.heappush(
                self.sells,
                (price, seq, order_id, quantity)
            )

        return self.match()

    def match(self):
        trades = []

        while self.buys and self.sells:
            buy = self.buys[0]
            sell = self.sells[0]

            buy_price = -buy[0]
            sell_price = sell[0]

            if buy_price < sell_price:
                break

            quantity = min(buy[3], sell[3])
            trade_price = sell_price

            trades.append({
                "buy_id": buy[2],
                "sell_id": sell[2],
                "price": trade_price,
                "quantity": quantity,
            })

            heapq.heappop(self.buys)
            heapq.heappop(self.sells)

            remaining_buy = buy[3] - quantity
            remaining_sell = sell[3] - quantity

            if remaining_buy > 0:
                heapq.heappush(
                    self.buys,
                    (buy[0], buy[1], buy[2], remaining_buy)
                )

            if remaining_sell > 0:
                heapq.heappush(
                    self.sells,
                    (sell[0], sell[1], sell[2], remaining_sell)
                )

        return trades


def main():
    engine = HeapMatchingEngine()

    print("Sell order:", engine.add_order(201, "S", 25000, 10))
    print("Buy order:", engine.add_order(101, "B", 25000, 4))
    print("Buy order:", engine.add_order(102, "B", 25000, 8))

    print("\nRemaining buy orders:")
    for order in sorted(engine.buys):
        print("ID:", order[2], "Remaining:", order[3])

    print("\nRemaining sell orders:")
    for order in sorted(engine.sells):
        print("ID:", order[2], "Remaining:", order[3])


if __name__ == "__main__":
    main()