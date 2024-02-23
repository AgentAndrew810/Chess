from __future__ import annotations
from objects.move import Move
from constants import KNIGHT_OFFSETS, STRAIGHT_OFFSETS, DIAGONAL_OFFSETS


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

    def on_board(self, pos: int) -> bool:
        if pos >= 0 and pos <= 63:
            return True
        else:
            return False

    def piece_on_square(self, pos: int, inclue_enemy: bool = False) -> bool:
        piece = self.board[pos]
        # if there is a piece on that square
        if piece:
            # if including enemy pieces, then return true
            if inclue_enemy:
                return True
            else:
                # otherwise, only return true if the piece is the player to move's piece
                if self.white_to_move == piece.isupper():
                    return True

        return False

    def get_moves(self) -> list[Move]:
        moves = []

        for pos in range(64):
            # get the piece rank and file
            piece = self.board[pos]
            rank = pos // 8
            file = pos % 8

            # if there isn't a piece
            if not piece:
                continue

            # if the piece's colour is not the player to move
            elif self.white_to_move != piece.isupper():
                continue

            if piece.upper() == "P":
                first_rank = 6 if self.white_to_move else 1
                direction = -8 if self.white_to_move else 8

                # if on board and no piece is on square, move one square up
                if self.on_board(pos + direction):
                    if not self.piece_on_square(pos + direction, True):
                        moves.append(Move(pos, pos + direction))

                        # if also on the first rank and no piece is on square, move two squares up
                        if rank == first_rank:
                            if not self.piece_on_square(pos + direction * 2, True):
                                moves.append(Move(pos, pos + direction * 2))

            elif piece.upper() == "N":
                for direction in KNIGHT_OFFSETS:
                    # get the new rank and file based on the direction
                    new_rank, new_file = rank + direction[0], file + direction[1]
                    new_pos = new_rank * 8 + new_file

                    if 0 <= new_rank <= 7 and 0 <= new_file <= 7:
                        if not self.piece_on_square(new_pos):
                            moves.append(Move(pos, new_pos))

            elif piece.upper() == "K":
                moves.extend(
                    self.get_piece_moves(
                        pos, STRAIGHT_OFFSETS + DIAGONAL_OFFSETS, False
                    )
                )

            elif piece.upper() == "B":
                moves.extend(self.get_piece_moves(pos, DIAGONAL_OFFSETS, True))

            elif piece.upper() == "R":
                moves.extend(self.get_piece_moves(pos, STRAIGHT_OFFSETS, True))

            elif piece.upper() == "Q":
                moves.extend(
                    self.get_piece_moves(pos, STRAIGHT_OFFSETS + DIAGONAL_OFFSETS, True)
                )

        return moves

    def get_piece_moves(
        self, pos: int, offsets: list[int], sliding: bool
    ) -> list[Move]:
        moves = []

        for offset in offsets:
            # set the initial position to adding the move
            new_pos = pos + offset

            if sliding:
                # if the piece can slide continue adding the move while it can
                while self.on_board(new_pos) and not self.piece_on_square(new_pos):
                    moves.append(Move(pos, new_pos))

                    # if you hit a piece exit loop
                    if self.piece_on_square(new_pos, True):
                        break

                    # add new offset
                    new_pos += offset
            else:
                # add the normal move
                if self.on_board(new_pos) and not self.piece_on_square(new_pos):
                    moves.append(Move(pos, new_pos))

        return moves
