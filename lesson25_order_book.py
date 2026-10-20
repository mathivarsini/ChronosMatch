buy_orders = []
sell_orders = []


def add_buy_order(order_id, price, quantity):
    buy_orders.append({
        "id": order_id,
        "price": price,
        "quantity": quantity
    })

    # Highest buy price first
    buy_orders.sort(key=lambda order: -order["price"])


def add_sell_order(order_id, price, quantity):
    sell_orders.append({
        "id": order_id,
        "price": price,
        "quantity": quantity
    })

    # Lowest sell price first
    sell_orders.sort(key=lambda order: order["price"])


add_buy_order(1, 102, 5)
add_buy_order(2, 105, 3)
add_buy_order(3, 102, 2)

add_sell_order(4, 108, 4)
add_sell_order(5, 103, 6)
add_sell_order(6, 103, 1)

print("BUY ORDERS")
for order in buy_orders:
    print(order)

print("\nSELL ORDERS")
for order in sell_orders:
    print(order)