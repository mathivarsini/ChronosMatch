buy_orders = []
sell_orders = []
trades = []
next_sequence = 0


def add_order(order_id, side, price, quantity):
    global next_sequence

    if price <= 0 or quantity <= 0:
        raise ValueError("Price and quantity must be positive")

    if side not in ("B", "S"):
        raise ValueError("Side must be B or S")

    next_sequence += 1

    order = {
        "id": order_id,
        "price": price,
        "quantity": quantity,
        "sequence": next_sequence,
    }

    if side == "B":
        buy_orders.append(order)
        buy_orders.sort(
            key=lambda item: (-item["price"], item["sequence"])
        )
    else:
        sell_orders.append(order)
        sell_orders.sort(
            key=lambda item: (item["price"], item["sequence"])
        )

    match_orders()


def match_orders():
    while buy_orders and sell_orders:
        buyer = buy_orders[0]
        seller = sell_orders[0]

        if buyer["price"] < seller["price"]:
            break

        quantity = min(buyer["quantity"], seller["quantity"])

        trades.append({
            "buy_order_id": buyer["id"],
            "sell_order_id": seller["id"],
            "price": seller["price"],
            "quantity": quantity,
        })

        buyer["quantity"] -= quantity
        seller["quantity"] -= quantity

        if buyer["quantity"] == 0:
            buy_orders.pop(0)

        if seller["quantity"] == 0:
            sell_orders.pop(0)


add_order(1, "B", 105, 4)
add_order(2, "B", 103, 5)
add_order(3, "S", 101, 2)
add_order(4, "S", 102, 3)

print("TRADES")
for trade in trades:
    print(trade)

print("\nREMAINING BUY ORDERS")
for order in buy_orders:
    print(order)

print("\nREMAINING SELL ORDERS")
for order in sell_orders:
    print(order)