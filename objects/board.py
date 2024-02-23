from __future__ import annotations
from objects.move import Move
from constants import K_OFFSETS, C_OFFSETS, D_OFFSETS


class Board:
    def __init__(self, board: list[list[str]], white_to_move: bool) -> None:
        self.board = board
        self.white_to_move = white_to_move

    @classmethod
    def from_fen(cls, FEN: str) -> Board:
        board = [["" for _ in range(8)] for _ in range(8)]
        rank = 0
        file = 0

        for char in FEN:
            if char == "/":
                rank += 1
                file = 0
            elif char.isdigit():
                file += int(char)
            elif char == ".":
                file += 1
            else:
                board[rank][file] = char
                file += 1

        return Board(board, True)

    def make_move(self, move: Move) -> Board:
        # copy the board
        new_board = [rank.copy() for rank in self.board]

        # move the piece
        new_board[move.new_rank][move.new_file] = new_board[move.old_rank][
            move.old_file
        ]
        new_board[move.old_rank][move.old_file] = ""

        # update additional information
        white_to_move = not self.white_to_move
        return Board(new_board, white_to_move)

    def can_move(self, rank: int, file: int, can_attack: bool) -> bool:
        # if the position is not on the board
        if 0 <= rank <= 7 and 0 <= file <= 7:
            piece = self.board[rank][file]

            # if there is no piece return True
            if not piece:
                return True

            # if the piece is allowed to attack
            if can_attack:
                # return false if the piece on the square is of the same color
                return self.white_to_move != piece.isupper()
            else:
                # otherwise piece cannot move there
                return False

        # if the position is off the board, the piece cannot move there
        return False

    def get_moves(self) -> list[Move]:
        moves = []

        for rank in range(8):
            for file in range(8):
                # get the piece
                piece = self.board[rank][file]

                # if there isn't a piece
                if not piece:
                    continue

                # if the piece's colour is not the player to move
                if self.white_to_move != piece.isupper():
                    continue

                if piece.upper() == "P":  # pawn
                    first_rank = 6 if self.white_to_move else 1
                    offset = -1 if self.white_to_move else 1

                    # if on board and no piece is on square, move one square up
                    if self.can_move(rank + offset, file, False):
                        moves.append(Move(rank, file, rank + offset, file))

                        # if also on the first rank and no piece is on square, move two squares up
                        if rank == first_rank:
                            if self.can_move(rank + offset * 2, file, False):
                                moves.append(Move(rank, file, rank + offset * 2, file))

                elif piece.upper() == "N":  # knight
                    moves.extend(self.get_piece_moves(rank, file, K_OFFSETS, False))

                elif piece.upper() == "K":  # king
                    moves.extend(
                        self.get_piece_moves(rank, file, C_OFFSETS + D_OFFSETS, False)
                    )

                elif piece.upper() == "B":  # bishop
                    moves.extend(self.get_piece_moves(rank, file, D_OFFSETS, True))

                elif piece.upper() == "R":  # rook
                    moves.extend(self.get_piece_moves(rank, file, C_OFFSETS, True))

                elif piece.upper() == "Q":  # queen
                    moves.extend(
                        self.get_piece_moves(rank, file, C_OFFSETS + D_OFFSETS, True)
                    )

        return moves

    def get_piece_moves(
        self, rank: int, file: int, offsets: list[tuple[int, int]], sliding: bool
    ) -> list[Move]:
        moves = []

        for offset in offsets:
            # set the initial position to adding the offset
            new_rank, new_file = rank + offset[0], file + offset[1]

            if sliding:
                # if the piece can slide, continue adding the move while it can
                while self.can_move(new_rank, new_file, True):
                    moves.append(Move(rank, file, new_rank, new_file))

                    # if you hit a piece exit loop
                    if self.board[new_rank][new_file]:
                        break

                    # add new offset
                    new_rank, new_file = new_rank + offset[0], new_file + offset[1]
            else:
                # add the normal move
                if self.can_move(new_rank, new_file, True):
                    moves.append(Move(rank, file, new_rank, new_file))

        return moves
