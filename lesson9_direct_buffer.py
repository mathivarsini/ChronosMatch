import mmap
import struct

ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)
CAPACITY = 3
BUFFER_SIZE = CAPACITY * ORDER_SIZE


class RingBuffer:
    def __init__(self, memory, capacity):
        self.memory = memory
        self.capacity = capacity
        self.write_pointer = 0
        self.read_pointer = 0
        self.count = 0

    def write(self, order):
        if self.count >= self.capacity:
            return False

        offset = self.write_pointer * ORDER_SIZE

        # Pack directly into mapped memory
        struct.pack_into(
            ORDER_FORMAT,
            self.memory,
            offset,
            *order
        )

        self.write_pointer = (
            self.write_pointer + 1
        ) % self.capacity

        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_pointer * ORDER_SIZE

        # Read directly from mapped memory
        order = struct.unpack_from(
            ORDER_FORMAT,
            self.memory,
            offset
        )

        self.read_pointer = (
            self.read_pointer + 1
        ) % self.capacity

        self.count -= 1
        return order


with open("lesson9_buffer.bin", "w+b") as file:
    file.write(b"\x00" * BUFFER_SIZE)
    file.flush()

    with mmap.mmap(file.fileno(), BUFFER_SIZE) as memory:
        ring = RingBuffer(memory, CAPACITY)

        ring.write((201, 250.0, 10, b"B"))
        ring.write((202, 251.0, 5, b"S"))

        print("First order:", ring.read())
        print("Second order:", ring.read())
        print("Empty buffer:", ring.read())

        assert ring.count == 0
        print("All checks passed!")