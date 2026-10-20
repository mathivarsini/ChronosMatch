from chronosmatch_ring_buffer import RingBuffer
from chronosmatch_engine import OrderBook

import mmap
import struct
import tempfile

ORDER_FORMAT = "<qqqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
CAPACITY = 10


def process_orders(buffer, order_book):
    """Read queued orders and send them to the matching engine."""
    while True:
        order = buffer.read()

        if order is None:
            break

        order_id, price, quantity, side = order

        # Convert the binary side into the engine's expected format.
        side = side.decode("ascii")

        trades = order_book.add_order(
            order_id, side, price, quantity
        )

        for trade in trades:
            print(
                f"Trade: Buy #{trade['buy_id']} | "
                f"Sell #{trade['sell_id']} | "
                f"Price: {trade['price']} | "
                f"Quantity: {trade['quantity']}"
            )


def main():
    with tempfile.TemporaryFile() as file:
        file.truncate(CAPACITY * ORDER_SIZE)

        with mmap.mmap(
            file.fileno(), CAPACITY * ORDER_SIZE
        ) as memory:

            buffer = RingBuffer(memory, CAPACITY)
            order_book = OrderBook()

            # Queue a sell order and a matching buy order.
            buffer.write((1, 25000, 5, b"S"))
            buffer.write((2, 25000, 3, b"B"))

            print("Processing queued orders...")
            process_orders(buffer, order_book)

            print("Remaining buy orders:", order_book.buys)
            print("Remaining sell orders:", order_book.sells)


if __name__ == "__main__":
    main()