import mmap
import struct

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
CAPACITY = 4
BUFFER_SIZE = CAPACITY * ORDER_SIZE

with open("lesson4_buffer.bin", "w+b") as file:
    file.write(b"\x00" * BUFFER_SIZE)
    file.flush()

    with mmap.mmap(file.fileno(), BUFFER_SIZE) as buffer:
        write_pointer = 0
        read_pointer = 0
        count = 0

        def write_order(order):
            global write_pointer, count

            if count == CAPACITY:
                print("Buffer is full! Order rejected.")
                return

            data = struct.pack(ORDER_FORMAT, *order)
            buffer.seek(write_pointer * ORDER_SIZE)
            buffer.write(data)

            write_pointer = (write_pointer + 1) % CAPACITY
            count += 1
            print("Order added:", order[0])

        def read_order():
            global read_pointer, count

            if count == 0:
                print("Buffer is empty! Nothing to read.")
                return

            buffer.seek(read_pointer * ORDER_SIZE)
            data = buffer.read(ORDER_SIZE)
            order = struct.unpack(ORDER_FORMAT, data)

            read_pointer = (read_pointer + 1) % CAPACITY
            count -= 1
            print("Order read:", order[0])

        print("--- Filling the buffer ---")
        write_order((1001, 250.0, 10, b"B"))
        write_order((1002, 251.0, 5, b"S"))
        write_order((1003, 252.0, 8, b"B"))
        write_order((1004, 253.0, 3, b"S"))

        print("\n--- Testing full condition ---")
        write_order((1005, 254.0, 2, b"B"))

        print("\n--- Reading all orders ---")
        read_order()
        read_order()
        read_order()
        read_order()

        print("\n--- Testing empty condition ---")
        read_order()

        print("\nFinal order count:", count)