import mmap
import struct


ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)

CAPACITY = 4
BUFFER_SIZE = CAPACITY * ORDER_SIZE


with open("ring_buffer.bin", "w+b") as file:
    file.write(b"\x00" * BUFFER_SIZE)
    file.flush()

    with mmap.mmap(file.fileno(), BUFFER_SIZE) as buffer:
        write_pointer = 0
        read_pointer = 0
        count = 0

        def write_order(order):
            global write_pointer, count

            if count == CAPACITY:
                print("Buffer is full!")
                return

            packed = struct.pack(ORDER_FORMAT, *order)
            offset = write_pointer * ORDER_SIZE

            buffer.seek(offset)
            buffer.write(packed)

            write_pointer = (write_pointer + 1) % CAPACITY
            count += 1
            print("Written:", order)

        def read_order():
            global read_pointer, count

            if count == 0:
                print("Buffer is empty!")
                return

            offset = read_pointer * ORDER_SIZE
            buffer.seek(offset)
            data = buffer.read(ORDER_SIZE)

            order = struct.unpack(ORDER_FORMAT, data)

            read_pointer = (read_pointer + 1) % CAPACITY
            count -= 1
            print("Read:", order)

        
        write_order((1001, 250.0, 10, b"B"))
        write_order((1002, 275.0, 5, b"S"))
        write_order((1003, 260.0, 8, b"B"))

        read_order()
        read_order()


        write_order((1004, 280.0, 3, b"S"))

        print("Orders remaining:", count)