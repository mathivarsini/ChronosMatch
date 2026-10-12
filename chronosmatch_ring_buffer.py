import mmap
import struct


ORDER_FORMAT = "<qdqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)


class RingBuffer:
    def __init__(self, memory, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        if len(memory) < capacity * ORDER_SIZE:
            raise ValueError("Mapped memory is too small")

        self.memory = memory
        self.capacity = capacity
        self.write_pointer = 0
        self.read_pointer = 0
        self.count = 0

    def write(self, order):
        if self.count >= self.capacity:
            return False

        order_id, price, quantity, side = order

        if side not in (b"B", b"S"):
            raise ValueError("Side must be b'B' or b'S'")

        offset = self.write_pointer * ORDER_SIZE

        struct.pack_into(
            ORDER_FORMAT,
            self.memory,
            offset,
            order_id,
            price,
            quantity,
            side
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


def run_tests():
    capacity = 3
    buffer_size = capacity * ORDER_SIZE

    with open("chronosmatch_buffer.bin", "w+b") as file:
        file.write(b"\x00" * buffer_size)
        file.flush()

        with mmap.mmap(file.fileno(), buffer_size) as memory:
            ring = RingBuffer(memory, capacity)

            
            assert ring.read() is None

            
            assert ring.write((101, 250.0, 2, b"B"))
            assert ring.write((102, 251.0, 3, b"S"))
            assert ring.write((103, 252.0, 4, b"B"))

 
            assert ring.write((104, 253.0, 5, b"S")) is False
 
            assert ring.read(
           )[0] == 101
            assert ring.read()[0] == 102

            assert ring.write((104, 253.0, 5, b"S"))
            assert ring.write((105, 254.0, 6, b"B"))

            assert ring.read()[0] == 103
            assert ring.read()[0] == 104
            assert ring.read()[0] == 105

            assert ring.read() is None
            assert ring.count == 0

    print("All ChronosMatch ring-buffer tests passed!")


if __name__ == "__main__":
    run_tests()