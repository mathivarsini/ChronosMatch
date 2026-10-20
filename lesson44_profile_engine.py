import cProfile
import pstats
from chronosmatch_engine import OrderBook


def run_engine():
    book = OrderBook()
    trade_count = 0

    for pair in range(1, 5001):
        # Add a sell order
        book.add_order(
            2 * pair - 1, "S", 25000, 1
        )

        # Add a matching buy order
        trades = book.add_order(
            2 * pair, "B", 25000, 1
        )

        trade_count += len(trades)

    print("Completed trades:", trade_count)


profiler = cProfile.Profile()
profiler.enable()

run_engine()

profiler.disable()

print("\n=== Profiling Results ===")

stats = pstats.Stats(profiler)
stats.strip_dirs()
stats.sort_stats("cumtime")
stats.print_stats(15)