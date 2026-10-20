import cProfile
import pstats
import mmap

from chronosmatch_ring_buffer import RingBuffer, ORDER_SIZE

CAPACITY = 1024
TOTAL_ORDERS = 100_000
BUFFER_SIZE = CAPACITY * ORDER_SIZE


def process_orders():
    with open("lesson16_buffer.bin", "w+b") as file:
        file.write(b"\x00" * BUFFER_SIZE)
        file.flush()

        with mmap.mmap(file.fileno(), BUFFER_SIZE) as memory:
            ring = RingBuffer(memory, CAPACITY)

            for i in range(TOTAL_ORDERS):
                order = (i, 250.0, 5, b"B")

                if not ring.write(order):
                    ring.read()
                    ring.write(order)

                ring.read()


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    process_orders()

    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats("cumtime")
    stats.print_stats(15)