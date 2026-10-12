import mmap
import struct

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
CAPACITY = 3
BUFFER_SIZE = CAPACITY * ORDER_SIZE

with open("lesson5_buffer.bin", "w+b") as file:
    file.write(b"\x00" * BUFFER_SIZE)
    file.flush()

    with mmap.mmap(file.fileno(), BUFFER_SIZE) as buffer:
        write_pointer = 0
        read_pointer = 0
        count = 0

        def write_order(order):
            global write_pointer, count

            if count == CAPACITY:
                print("Buffer full:", order[0])
                return

            buffer.seek(write_pointer * ORDER_SIZE)
            buffer.write(struct.pack(ORDER_FORMAT, *order))

            print("Written:", order[0])
            write_pointer = (write_pointer + 1) % CAPACITY
            count += 1

        def read_order():
            global read_pointer, count

            if count == 0:
                print("Buffer empty")
                return

            buffer.seek(read_pointer * ORDER_SIZE)
            data = buffer.read(ORDER_SIZE)
            order = struct.unpack(ORDER_FORMAT, data)

            print("Read:", order[0])
            read_pointer = (read_pointer + 1) % CAPACITY
            count -= 1

        # Fill all three slots
        write_order((101, 250.0, 2, b"B"))
        write_order((102, 251.0, 3, b"S"))
        write_order((103, 252.0, 4, b"B"))

        # Free two slots
        read_order()
        read_order()

        # Write two more orders; the pointer wraps around
        write_order((104, 253.0, 5, b"S"))
        write_order((105, 254.0, 6, b"B"))

        print("Final count:", count)