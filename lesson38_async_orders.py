import asyncio


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
        await asyncio.sleep(0.1)

    # Tell the consumer that no more orders are coming.
    await queue.put(None)


async def consumer(queue):
    while True:
        order = await queue.get()

        try:
            if order is None:
                print("Consumer: no more orders.")
                return

            order_id, side, price, quantity = order

            print(
                f"Consumed order #{order_id}: "
                f"{side}, price={price}, quantity={quantity}"
            )
        finally:
            queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=2)

    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    await queue.join()
    await consumer_task

    print("All orders processed.")


if __name__ == "__main__":
    asyncio.run(main())