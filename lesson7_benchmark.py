import mmap
import struct
import time

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)

TOTAL_ORDERS = 100_000
BUFFER_SIZE = TOTAL_ORDERS * ORDER_SIZE

with open("lesson7_benchmark.bin", "w+b") as file:
    file.write(b"\x00" * BUFFER_SIZE)
    file.flush()

    with mmap.mmap(file.fileno(), BUFFER_SIZE) as buffer:
        # Benchmark writing binary orders
        start = time.perf_counter()

        for i in range(TOTAL_ORDERS):
            order = (i + 1, 250.0, 10, b"B")
            data = struct.pack(ORDER_FORMAT, *order)

            buffer.seek(i * ORDER_SIZE)
            buffer.write(data)

        write_time = time.perf_counter() - start

        # Benchmark reading and unpacking the orders
        start = time.perf_counter()

        for i in range(TOTAL_ORDERS):
            buffer.seek(i * ORDER_SIZE)
            data = buffer.read(ORDER_SIZE)
            order = struct.unpack(ORDER_FORMAT, data)

        read_time = time.perf_counter() - start

        print("Total orders:", TOTAL_ORDERS)
        print("Order size:", ORDER_SIZE, "bytes")
        print(f"Write time: {write_time:.4f} seconds")
        print(f"Read time:  {read_time:.4f} seconds")

        if write_time > 0:
            print(
                f"Write throughput: "
                f"{TOTAL_ORDERS / write_time:,.0f} orders/second"
            )

        if read_time > 0:
            print(
                f"Read throughput: "
                f"{TOTAL_ORDERS / read_time:,.0f} orders/second"
            )