import asyncio
from chronosmatch_engine import OrderBook


async def producer(queue):
    orders = [
        (1, "S", 25000, 5),
        (2, "B", 25000, 3),
        (3, "B", 24900, 2),
        (4, "S", 24900, 1),
    ]

    for order in orders:
        await queue.put(order)
        print(f"Produced order #{order[0]}")

        # Simulate a short delay between incoming orders.
        await asyncio.sleep(0.1)

    # Signal that no more orders will arrive.
    await queue.put(None)


async def consumer(queue, order_book):
    while True:
        order = await queue.get()

        try:
            if order is None:
                print("No more orders to process.")
                return

            order_id, side, price, quantity = order

            trades = order_book.add_order(
                order_id, side, price, quantity
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

    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(
        consumer(queue, order_book)
    )

    await producer_task
    await queue.join()
    await consumer_task

    print("\nAll orders processed.")
    print("Remaining buys:", order_book.buys)
    print("Remaining sells:", order_book.sells)


if __name__ == "__main__":
    asyncio.run(main())