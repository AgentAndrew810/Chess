import random
from objects.board import Board
from objects.move import Move


class Engine:
    def __init__(self) -> None:
        return

    def search(self, board: Board) -> Move:
        return random.choice(board.get_moves())
