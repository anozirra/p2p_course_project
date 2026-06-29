class BoardState:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._pixels: set[tuple[int, int]] = set()

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def set_pixel(self, x: int, y: int) -> bool:
        if not self.is_inside(x, y):
            return False
        
        if (x,y) in self._pixels:
            return False

        self._pixels.add((x, y))
        return True

    def remove_pixel(self, x: int, y: int) -> bool:
        if not self.is_inside(x, y):
            return False

        if (x, y) not in self._pixels:
            return False

        self._pixels.discard((x, y))
        return True

    def has_pixel(self, x: int, y: int) -> bool:
        return (x, y) in self._pixels

    def clear(self) -> bool:
        if not self._pixels:
            return False

        self._pixels.clear()
        return True

    def get_pixels(self) -> set[tuple[int, int]]:
        return set(self._pixels)