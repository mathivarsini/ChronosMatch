buy_orders = []
sell_orders = []
trades = []


def add_buy_order(order_id, price, quantity):
    buy_orders.append({
        "id": order_id,
        "price": price,
        "quantity": quantity
    })
    buy_orders.sort(key=lambda order: -order["price"])


def add_sell_order(order_id, price, quantity):
    sell_orders.append({
        "id": order_id,
        "price": price,
        "quantity": quantity
    })
    sell_orders.sort(key=lambda order: order["price"])


def match_orders():
    while buy_orders and sell_orders:
        buyer = buy_orders[0]
        seller = sell_orders[0]

        # No trade is possible if the buyer's price
        # is lower than the seller's price.
        if buyer["price"] < seller["price"]:
            break

        trade_quantity = min(
            buyer["quantity"],
            seller["quantity"]
        )

        trades.append({
            "buy_order_id": buyer["id"],
            "sell_order_id": seller["id"],
            "price": seller["price"],
            "quantity": trade_quantity
        })

        buyer["quantity"] -= trade_quantity
        seller["quantity"] -= trade_quantity

        if buyer["quantity"] == 0:
            buy_orders.pop(0)

        if seller["quantity"] == 0:
            sell_orders.pop(0)


add_buy_order(1, 105, 10)
add_sell_order(2, 103, 6)

match_orders()

print("EXECUTED TRADES")
for trade in trades:
    print(trade)

print("\nREMAINING BUY ORDERS")
for order in buy_orders:
    print(order)

print("\nREMAINING SELL ORDERS")
for order in sell_orders:
    print(order)