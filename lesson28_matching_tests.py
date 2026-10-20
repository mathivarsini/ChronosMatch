def run_matching(buy_orders, sell_orders):
    # Best buy: highest price, earliest order first at equal prices.
    buy_orders.sort(key=lambda o: (-o["price"], o["sequence"]))

    # Best sell: lowest price, earliest order first at equal prices.
    sell_orders.sort(key=lambda o: (o["price"], o["sequence"]))

    trades = []

    while buy_orders and sell_orders:
        buyer = buy_orders[0]
        seller = sell_orders[0]

        if buyer["price"] < seller["price"]:
            break

        quantity = min(buyer["quantity"], seller["quantity"])

        trades.append({
            "buy_id": buyer["id"],
            "sell_id": seller["id"],
            "price": seller["price"],
            "quantity": quantity,
        })

        buyer["quantity"] -= quantity
        seller["quantity"] -= quantity

        if buyer["quantity"] == 0:
            buy_orders.pop(0)

        if seller["quantity"] == 0:
            sell_orders.pop(0)

    return trades


def order(order_id, price, quantity, sequence):
    return {
        "id": order_id,
        "price": price,
        "quantity": quantity,
        "sequence": sequence,
    }


def test_full_match():
    buys = [order(1, 105, 5, 1)]
    sells = [order(2, 103, 5, 2)]

    trades = run_matching(buys, sells)

    assert len(trades) == 1
    assert trades[0]["quantity"] == 5
    assert len(buys) == 0
    assert len(sells) == 0


def test_partial_fill():
    buys = [order(1, 105, 10, 1)]
    sells = [order(2, 103, 6, 2)]

    trades = run_matching(buys, sells)

    assert trades[0]["quantity"] == 6
    assert buys[0]["quantity"] == 4
    assert len(sells) == 0


def test_no_match():
    buys = [order(1, 100, 5, 1)]
    sells = [order(2, 105, 5, 2)]

    trades = run_matching(buys, sells)

    assert len(trades) == 0
    assert buys[0]["quantity"] == 5
    assert sells[0]["quantity"] == 5


if __name__ == "__main__":
    test_full_match()
    print("PASS: Full match")

    test_partial_fill()
    print("PASS: Partial fill")

    test_no_match()
    print("PASS: No match")

    print("All Lesson 28 tests passed!")