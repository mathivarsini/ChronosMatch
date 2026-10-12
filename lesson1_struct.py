import struct

order_format = "<qdqc"

order_id = 1002
price = 275.0
quantity = 5
side = b"S"

packed_order = struct.pack(
    order_format,
    order_id,
    price,
    quantity,
    side
)

print("Packed order:", packed_order)
print("Size in bytes:", len(packed_order))

unpacked_order = struct.unpack(
    order_format,
    packed_order
)

print("Unpacked order:", unpacked_order)