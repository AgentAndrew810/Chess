from __future__ import annotations
from objects.move import Move


class Board:
    def __init__(self, board: list[str]) -> None:
        self.board = board
        self.white_to_move = True

    @classmethod
    def from_fen(cls, fen: str) -> Board:
        board = [""] * 64
        index = 0

        for char in fen:
            if char.isdigit():
                index += int(char)
            elif char == "/":
                continue
            else:
                board[index] = char
                index += 1

        return Board(board)

    def get_moves(self) -> list[Move]:
        return []
