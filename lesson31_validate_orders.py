import mmap
import struct

ORDER_FORMAT = "<qqqc"
ORDER_SIZE = struct.calcsize(ORDER_FORMAT)


def validate_order(order):
    if len(order) != 4:
        raise ValueError("Order must contain 4 fields")

    order_id, price_units, quantity, side = order

    if not isinstance(order_id, int) or isinstance(order_id, bool):
        raise ValueError("Order ID must be an integer")
    if not 1 <= order_id <= 2**63 - 1:
        raise ValueError("Order ID is out of range")

    if not isinstance(price_units, int) or isinstance(price_units, bool):
        raise ValueError("Price must be an integer number of paise")
    if not 1 <= price_units <= 2**63 - 1:
        raise ValueError("Price must be positive and in range")

    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise ValueError("Quantity must be an integer")
    if not 1 <= quantity <= 2**63 - 1:
        raise ValueError("Quantity must be positive and in range")

    if side not in (b"B", b"S"):
        raise ValueError("Side must be b'B' or b'S'")


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
        # Validate before changing buffer state.
        validate_order(order)

        if self.count == self.capacity:
            return False

        offset = self.write_pointer * ORDER_SIZE
        struct.pack_into(ORDER_FORMAT, self.memory, offset, *order)

        self.write_pointer = (self.write_pointer + 1) % self.capacity
        self.count += 1
        return True

    def read(self):
        if self.count == 0:
            return None

        offset = self.read_pointer * ORDER_SIZE
        order = struct.unpack_from(ORDER_FORMAT, self.memory, offset)

        self.read_pointer = (self.read_pointer + 1) % self.capacity
        self.count -= 1
        return order


def main():
    size = 2 * ORDER_SIZE

    with open("lesson31_buffer.bin", "w+b") as file:
        file.truncate(size)

        with mmap.mmap(file.fileno(), size) as memory:
            ring = RingBuffer(memory, 2)

            assert ring.write((1001, 25050, 5, b"B"))
            assert ring.write((1002, 25100, 3, b"S"))

            invalid_orders = [
                (0, 25050, 5, b"B"),
                (1003, 0, 5, b"B"),
                (1004, 25050, -1, b"S"),
                (1005, 25050, 5, b"X"),
            ]

            for order in invalid_orders:
                try:
                    ring.write(order)
                except ValueError as error:
                    print(f"Rejected {order}: {error}")
                else:
                    raise AssertionError(f"Invalid order accepted: {order}")

            assert ring.count == 2
            assert ring.read() == (1001, 25050, 5, b"B")
            assert ring.read() == (1002, 25100, 3, b"S")
            assert ring.read() is None

            print("\nAll validation tests passed!")


if __name__ == "__main__":
    main()