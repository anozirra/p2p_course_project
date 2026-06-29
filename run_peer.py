from p2p_whiteboard.state import BoardState
from p2p_whiteboard.ui import BoardUI

def main() -> None:
    board = BoardState(width=600, height=400)
    ui = BoardUI(board)
    ui.run()

if __name__ == "__main__":
    main()
