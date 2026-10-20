import unittest


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
                key=lambda x: (-x["price"], x["sequence"])
            )
        else:
            self.sells.append(order)
            self.sells.sort(
                key=lambda x: (x["price"], x["sequence"])
            )

        return self.match()

    def match(self):
        trades = []

        while self.buys and self.sells:
            buy = self.buys[0]
            sell = self.sells[0]

            if buy["price"] < sell["price"]:
                break

            quantity = min(
                buy["quantity"], sell["quantity"]
            )

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


class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook()

    def test_full_match(self):
        self.book.add_order(1, "S", 100, 5)
        trades = self.book.add_order(2, "B", 100, 5)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["quantity"], 5)
        self.assertEqual(len(self.book.buys), 0)
        self.assertEqual(len(self.book.sells), 0)

    def test_partial_match(self):
        self.book.add_order(1, "S", 100, 10)
        trades = self.book.add_order(2, "B", 100, 4)

        self.assertEqual(trades[0]["quantity"], 4)
        self.assertEqual(self.book.sells[0]["quantity"], 6)

    def test_no_match(self):
        self.book.add_order(1, "S", 110, 5)
        trades = self.book.add_order(2, "B", 100, 5)

        self.assertEqual(len(trades), 0)
        self.assertEqual(len(self.book.buys), 1)
        self.assertEqual(len(self.book.sells), 1)

    def test_price_priority(self):
        self.book.add_order(1, "S", 105, 2)
        self.book.add_order(2, "S", 100, 2)

        trades = self.book.add_order(3, "B", 110, 2)

        self.assertEqual(trades[0]["sell_id"], 2)
        self.assertEqual(trades[0]["price"], 100)

    def test_time_priority(self):
        self.book.add_order(1, "S", 100, 2)
        self.book.add_order(2, "S", 100, 2)

        trades = self.book.add_order(3, "B", 100, 2)

        self.assertEqual(trades[0]["sell_id"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)