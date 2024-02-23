import random
from objects.board import Board
from objects.move import Move
from constants import PIECE_VALUES


class Engine:
    def __init__(self) -> None:
        return

    def search(self, board: Board) -> Move:
        return random.choice(board.get_moves())

    def evaluate(self, board: Board) -> int:
        score = 0

        for rank in range(8):
            for file in range(8):
                piece = board.board[rank][file]

                # if the piece is white add the value, otherwise subtract the value
                if piece.upper() in PIECE_VALUES:
                    if piece.isupper():
                        score += PIECE_VALUES[piece.upper()]
                    else:
                        score -= PIECE_VALUES[piece.upper()]

        return score
