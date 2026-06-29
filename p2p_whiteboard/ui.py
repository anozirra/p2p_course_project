import tkinter as tk

from p2p_whiteboard.state import BoardState


class BoardUI:

    def __init__(self, board: BoardState):
        self.board = board
        self._last_draw_point: tuple[int, int] | None = None
        self._last_erase_point: tuple[int, int] | None = None

        self.window = tk.Tk()
        self.window.title("P2P Whiteboard")

        self.toolbar = tk.Frame(self.window)
        self.toolbar.pack(fill=tk.X)

        self.clear_button = tk.Button(
            self.toolbar,
            text="Clear",
            command=self.apply_clear,
        )
        self.clear_button.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(
            self.window,
            width=self.board.width,
            height=self.board.height,
            bg="white",
        )
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_draw)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_draw_stop)

        self.canvas.bind("<Button-3>", self.on_erase)
        self.canvas.bind("<B3-Motion>", self.on_erase)
        self.canvas.bind("<ButtonRelease-3>", self.on_erase_stop)

    def run(self) -> None:
        self.window.mainloop()

    def on_draw(self, event) -> None:
        current_point = (event.x, event.y)

        for x, y in self.points_between(self._last_draw_point, current_point):
            self.apply_set_pixel(x, y)

        self._last_draw_point = current_point

    def on_erase(self, event) -> None:
        current_point = (event.x, event.y)

        for x, y in self.points_between(self._last_erase_point, current_point):
            self.apply_remove_pixel(x, y)

        self._last_erase_point = current_point

    def on_draw_stop(self, event) -> None:
        self._last_draw_point = None

    def on_erase_stop(self, event) -> None:
        self._last_erase_point = None

    def apply_set_pixel(self, x: int, y: int) -> bool:
        changed = self.board.set_pixel(x, y)
        if changed:
            self.draw_pixel(x, y)
        return changed

    def apply_remove_pixel(self, x: int, y: int) -> bool:
        changed = self.board.remove_pixel(x, y)
        if changed:
            self.erase_pixel(x, y)
        return changed

    def apply_clear(self) -> None:
        self.board.clear()
        self.canvas.delete("all")

    def redraw(self) -> None:
        self.canvas.delete("all")
        for x, y in self.board.get_pixels():
            self.draw_pixel(x, y)

    def draw_pixel(self, x: int, y: int) -> None:
        self.canvas.create_rectangle(
            x,
            y,
            x + 1,
            y + 1,
            fill="black",
            outline="black",
        )

    def erase_pixel(self, x: int, y: int) -> None:
        '''Erase one pixel on the canvas.'''
        self.canvas.create_rectangle(
            x,
            y,
            x + 1,
            y + 1,
            fill="white",
            outline="white",
        )

    def points_between(
        self,
        start: tuple[int, int] | None,
        end: tuple[int, int],
    ) -> list[tuple[int, int]]:
        '''Return pixels between two mouse positions so dragging has no gaps.'''
        if start is None:
            return [end]

        start_x, start_y = start
        end_x, end_y = end
        dx = end_x - start_x
        dy = end_y - start_y
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return [end]

        points = []
        for step in range(steps + 1):
            x = round(start_x + dx * step / steps)
            y = round(start_y + dy * step / steps)
            point = (x, y)
            if not points or points[-1] != point:
                points.append(point)

        return points