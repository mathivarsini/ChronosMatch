import mmap
import struct
import os
order_format = "<qdqc"
order_size = struct.calcsize(order_format)

filename = "order_buffer.bin"


with open(filename, "w+b") as file:
    file.write(b"\x00" * order_size)
    file.flush()

    with mmap.mmap(file.fileno(), order_size) as buffer:

        order = (1001, 250.0, 10, b"B")


        packed_order = struct.pack(order_format, *order)


        buffer.seek(0)
        buffer.write(packed_order)


        buffer.seek(0)
        read_bytes = buffer.read(order_size)


        result = struct.unpack(order_format, read_bytes)

        print("Order size:", order_size, "bytes")
        print("Read order:", result)

print("Memory-mapped file test completed.")