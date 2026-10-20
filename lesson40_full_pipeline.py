import asyncio
import mmap
import struct
import tempfile

from chronosmatch_engine import OrderBook

ORDER_FORMAT = "<qqqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
CAPACITY = 10


class RingBuffer:
    def __init__(self, memory, capacity):
        self.memory = memory
        self.capacity = capacity
        self.write_pos = 0
        self.read_pos = 0
        self.count = 0

    def write(self, order):
        if self.count == self.capacity:
            return False

        offset = self.write_pos * ORDER_SIZE
        struct.pack_into(ORDER_FORMAT, self.memory, offset, *order)

        self.write_pos = (self.write_pos + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_pos * ORDER_SIZE
        order = struct.unpack_from(ORDER_FORMAT, self.memory, offset)

        self.read_pos = (self.read_pos + 1) % self.capacity
        self.count -= 1
        return order


async def producer(ring_buffer, queue):
    orders = [
        (1, 25000, 5, b"S"),
        (2, 25000, 3, b"B"),
        (3, 24900, 2, b"B"),
        (4, 24900, 1, b"S"),
    ]

    for order in orders:
        accepted = ring_buffer.write(order)

        if not accepted:
            raise RuntimeError("Ring buffer is full")

        print(f"Queued order #{order[0]} in ring buffer")

        # Move available orders to the asynchronous queue.
        while True:
            item = ring_buffer.read()

            if item is None:
                break

            await queue.put(item)

        await asyncio.sleep(0.05)

    await queue.put(None)


async def consumer(queue, order_book):
    while True:
        order = await queue.get()

        try:
            if order is None:
                print("No more orders.")
                return

            order_id, price, quantity, side = order

            trades = order_book.add_order(
                order_id,
                side.decode("ascii"),
                price,
                quantity,
            )

            print(f"Processed order #{order_id}")

            for trade in trades:
                print(
                    f"TRADE: Buy #{trade['buy_id']} | "
                    f"Sell #{trade['sell_id']} | "
                    f"Price: {trade['price']} | "
                    f"Quantity: {trade['quantity']}"
                )
        finally:
            queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=2)
    order_book = OrderBook()

    with tempfile.TemporaryFile() as file:
        file.truncate(CAPACITY * ORDER_SIZE)

        with mmap.mmap(
            file.fileno(), CAPACITY * ORDER_SIZE
        ) as memory:
            ring_buffer = RingBuffer(memory, CAPACITY)

            producer_task = asyncio.create_task(
                producer(ring_buffer, queue)
            )
            consumer_task = asyncio.create_task(
                consumer(queue, order_book)
            )

            await producer_task
            await queue.join()
            await consumer_task

    print("\nPipeline complete.")
    print("Remaining buys:", order_book.buys)
    print("Remaining sells:", order_book.sells)


if __name__ == "__main__":
    asyncio.run(main())