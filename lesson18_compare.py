import struct
import time

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
TOTAL_ORDERS = 200_000

order_id = 1001
price = 250.0
quantity = 5
side = b"B"


def benchmark_pack():
    buffer = bytearray(ORDER_SIZE)

    start = time.perf_counter()

    for _ in range(TOTAL_ORDERS):
        record = struct.pack(
            ORDER_FORMAT,
            order_id,
            price,
            quantity,
            side
        )
        buffer[:] = record

    return time.perf_counter() - start


def benchmark_pack_into():
    buffer = bytearray(ORDER_SIZE)

    start = time.perf_counter()

    for _ in range(TOTAL_ORDERS):
        struct.pack_into(
            ORDER_FORMAT,
            buffer,
            0,
            order_id,
            price,
            quantity,
            side
        )

    return time.perf_counter() - start


if __name__ == "__main__":
    # Warm up both implementations
    benchmark_pack()
    benchmark_pack_into()

    pack_time = benchmark_pack()
    pack_into_time = benchmark_pack_into()

    print(f"Orders per test: {TOTAL_ORDERS:,}")
    print(f"struct.pack time:      {pack_time:.6f} seconds")
    print(f"struct.pack_into time: {pack_into_time:.6f} seconds")

    if pack_into_time < pack_time:
        print("pack_into was faster in this run.")
    elif pack_into_time > pack_time:
        print("pack was faster in this run.")
    else:
        print("Both took the same measured time.")