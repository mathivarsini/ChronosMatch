class OrderBook:
    def __init__(self):
        self.buys = []
        self.sells = []
        self.sequence = 0

    def add_order(self, order_id, side, price, quantity):
        if order_id <= 0 or price <= 0 or quantity <= 0:
            raise ValueError("Order ID, price, and quantity must be positive")

        if side not in ("B", "S"):
            raise ValueError("Side must be B or S")

        self.sequence += 1

        order = {
            "id": order_id,
            "price": price,
            "quantity": quantity,
            "sequence": self.sequence,
        }

        if side == "B":
            self.buys.append(order)
            self.buys.sort(
                key=lambda item: (-item["price"], item["sequence"])
            )
        else:
            self.sells.append(order)
            self.sells.sort(
                key=lambda item: (item["price"], item["sequence"])
            )

        return self.match()

    def match(self):
        trades = []

        while self.buys and self.sells:
            buy = self.buys[0]
            sell = self.sells[0]

            if buy["price"] < sell["price"]:
                break

            quantity = min(buy["quantity"], sell["quantity"])

            trades.append({
                "buy_id": buy["id"],
                "sell_id": sell["id"],
                "price": sell["price"],
                "quantity": quantity,
            })

            buy["quantity"] -= quantity
            sell["quantity"] -= quantity

            if buy["quantity"] == 0:
                self.buys.pop(0)

            if sell["quantity"] == 0:
                self.sells.pop(0)

        return trades