# P2P Whiteboard

Decentralized whiteboard for P2P project.

## Run

Create and activate a virtual environment, then run: `python run_peer.py`

Left click or drag to draw black pixels.

Right click or drag to erase.

Use `Clear` to clear the board.

## UI / State Interfaces

`BoardState` stores the board data:

```python
class BoardState:
    ''' Stores the current black pixels on the whiteboard. '''

    def is_inside(self, x: int, y: int) -> bool:
        ''' Return True if the grid coordinate is inside the board. '''

    def set_pixel(self, x: int, y: int) -> bool:
        ''' Turn one grid pixel black. '''

    def remove_pixel(self, x: int, y: int) -> bool:
        ''' Turn one grid pixel white again. '''

    def has_pixel(self, x: int, y: int) -> bool:
        ''' Return True if the grid pixel is currently black.'''

    def clear(self) -> bool:
        ''' Remove all black pixels. '''

    def get_pixels(self) -> set[tuple[int, int]]:
        ''' Return a copy of all black pixels. '''
```



`BoardUI` updates both state and display:

```python
class BoardUI:
    '''Tkinter UI for a local pixel whiteboard.'''

    def run(self) -> None:
        '''Start the Tkinter event loop.'''

    def on_draw(self, event) -> None:
        '''Handle local left-click drawing.'''

    def on_erase(self, event) -> None:
        '''Handle local right-click erasing.'''

    def on_draw_stop(self, event) -> None:
        '''Stop the current draw action.'''

    def on_erase_stop(self, event) -> None:
        '''Stop the current erase action.'''

    def apply_set_pixel(self, x: int, y: int) -> bool:
        '''Set one pixel in BoardState and draw it on the canvas.'''

    def apply_remove_pixel(self, x: int, y: int) -> bool:
        '''Remove one pixel from BoardState and erase it on the canvas.'''

    def apply_clear(self) -> None:
        '''Clear BoardState and the canvas.'''
        
    def redraw(self) -> None:
        '''Redraw the canvas from the current BoardState.'''

    def draw_pixel(self, x: int, y: int) -> None:
        '''Draw one black pixel on the canvas.'''

    def erase_pixel(self, x: int, y: int) -> None:
        '''Erase one pixel on the canvas.'''

    def points_between(
        self,
        start: tuple[int, int] | None,
        end: tuple[int, int],
    ) -> list[tuple[int, int]]:
        '''Return pixels between two mouse positions so dragging has no gaps.'''
```

The Chord/network layer should exchange pixel coordinates and call the
`BoardUI` apply methods when remote updates arrive.
