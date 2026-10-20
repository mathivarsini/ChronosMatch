import mmap
import struct

ORDER_FORMAT = "<qqqc"
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

        order_id, price_units, quantity, side = order

        if side not in (b"B", b"S"):
            raise ValueError("Side must be b'B' or b'S'")

        if price_units <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive")

        offset = self.write_pointer * ORDER_SIZE

        struct.pack_into(
            ORDER_FORMAT,
            self.memory,
            offset,
            order_id,
            price_units,
            quantity,
            side,
        )

        self.write_pointer = (self.write_pointer + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_pointer * ORDER_SIZE
        order = struct.unpack_from(
            ORDER_FORMAT, self.memory, offset
        )

        self.read_pointer = (self.read_pointer + 1) % self.capacity
        self.count -= 1
        return order


def main():
    capacity = 3
    size = capacity * ORDER_SIZE

    with open("lesson30_buffer.bin", "w+b") as file:
        file.truncate(size)

        with mmap.mmap(file.fileno(), size) as memory:
            ring = RingBuffer(memory, capacity)

            # ₹250.50 = 25,050 paise
            order = (1001, 25050, 5, b"B")

            assert ring.write(order)
            actual = ring.read()

            assert actual == order

            order_id, price_units, quantity, side = actual

            print("Order ID:", order_id)
            print(f"Price: ₹{price_units / 100:.2f}")
            print("Quantity:", quantity)
            print("Side:", side.decode())
            print("Binary record size:", ORDER_SIZE, "bytes")
            print("All tests passed!")


if __name__ == "__main__":
    main()