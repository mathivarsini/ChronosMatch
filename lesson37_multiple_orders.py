from chronosmatch_ring_buffer import RingBuffer
from chronosmatch_engine import OrderBook

import mmap
import struct
import tempfile

ORDER_FORMAT = "<qqqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
CAPACITY = 3


def process_orders(buffer, order_book):
    processed = 0

    while True:
        order = buffer.read()

        if order is None:
            break

        order_id, price, quantity, side = order

        print(f"Processing order #{order_id}")

        trades = order_book.add_order(
            order_id,
            side.decode("ascii"),
            price,
            quantity,
        )

        for trade in trades:
            print(
                f"TRADE: Buy #{trade['buy_id']}, "
                f"Sell #{trade['sell_id']}, "
                f"Price {trade['price']}, "
                f"Quantity {trade['quantity']}"
            )

        processed += 1

    return processed


def main():
    with tempfile.TemporaryFile() as file:
        file.truncate(CAPACITY * ORDER_SIZE)

        with mmap.mmap(
            file.fileno(), CAPACITY * ORDER_SIZE
        ) as memory:

            buffer = RingBuffer(memory, CAPACITY)
            order_book = OrderBook()

            orders = [
                (1, 25000, 5, b"S"),
                (2, 25000, 3, b"B"),
                (3, 24900, 2, b"B"),
            ]

            print("Adding orders to the ring buffer:")

            for order in orders:
                success = buffer.write(order)
                print(f"Order #{order[0]} accepted: {success}")

            # The buffer has capacity 3, so a fourth order
            # should be rejected while it is full.
            extra_order = (4, 25000, 1, b"S")
            print(
                "Fourth order accepted:",
                buffer.write(extra_order),
            )

            print("\nProcessing orders in FIFO order:")
            processed = process_orders(buffer, order_book)

            print(f"\nTotal orders processed: {processed}")
            print("Remaining buy orders:", order_book.buys)
            print("Remaining sell orders:", order_book.sells)


if __name__ == "__main__":
    main()