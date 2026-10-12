import mmap
import struct

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)


class RingBuffer:
    def __init__(self, memory, capacity):
        self.memory = memory
        self.capacity = capacity
        self.write_pointer = 0
        self.read_pointer = 0
        self.count = 0

    def write(self, order):
        if self.count == self.capacity:
            print("Buffer full! Order rejected:", order[0])
            return False

        data = struct.pack(ORDER_FORMAT, *order)
        offset = self.write_pointer * ORDER_SIZE

        self.memory.seek(offset)
        self.memory.write(data)

        self.write_pointer = (
            self.write_pointer + 1
        ) % self.capacity

        self.count += 1
        print("Written:", order[0])
        return True

    def read(self):
        if self.count == 0:
            print("Buffer empty!")
            return None

        offset = self.read_pointer * ORDER_SIZE

        self.memory.seek(offset)
        data = self.memory.read(ORDER_SIZE)
        order = struct.unpack(ORDER_FORMAT, data)

        self.read_pointer = (
            self.read_pointer + 1
        ) % self.capacity

        self.count -= 1
        print("Read:", order[0])
        return order


CAPACITY = 3
BUFFER_SIZE = CAPACITY * ORDER_SIZE

with open("lesson6_buffer.bin", "w+b") as file:
    file.write(b"\x00" * BUFFER_SIZE)
    file.flush()

    with mmap.mmap(file.fileno(), BUFFER_SIZE) as memory:
        ring = RingBuffer(memory, CAPACITY)

        print("--- Writing orders ---")
        ring.write((101, 250.0, 2, b"B"))
        ring.write((102, 251.0, 3, b"S"))
        ring.write((103, 252.0, 4, b"B"))

        print("\n--- Testing full buffer ---")
        ring.write((104, 253.0, 5, b"S"))

        print("\n--- Reading an order ---")
        ring.read()

        print("\n--- Reusing a slot ---")
        ring.write((104, 253.0, 5, b"S"))

        print("\nOrders remaining:", ring.count)