PRICE_SCALE = 100


def price_to_units(price):
    # Convert a price with two decimal places to integer units.
    return round(price * PRICE_SCALE)


def units_to_price(units):
    return units / PRICE_SCALE


buy_price = price_to_units(250.50)
sell_price = price_to_units(250.25)

print("Buy price in units:", buy_price)
print("Sell price in units:", sell_price)

if buy_price >= sell_price:
    print("Trade is possible!")
else:
    print("Trade is not possible.")

print("Buy price:", units_to_price(buy_price))
print("Sell price:", units_to_price(sell_price))