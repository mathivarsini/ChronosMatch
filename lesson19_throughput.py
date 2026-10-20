orders = 200_000

pack_time = 0.051961
pack_into_time = 0.027743

pack_throughput = orders / pack_time
pack_into_throughput = orders / pack_into_time

print(f"struct.pack(): {pack_throughput:,.0f} orders/second")
print(f"struct.pack_into(): {pack_into_throughput:,.0f} orders/second")

improvement = (pack_into_throughput / pack_throughput - 1) * 100

print(f"Throughput improvement: {improvement:.2f}%")