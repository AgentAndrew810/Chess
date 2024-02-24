from __future__ import annotations
from objects.move import Move
from constants import K_OFFSETS, C_OFFSETS, D_OFFSETS


class Board:
    def __init__(self, board: list[list[str]], starter_options: bool) -> None:
        self.board = board

        if starter_options:
            # set additional options
            self.white_to_move = True
            self.last_move = None
            self.w_castle_k = True
            self.w_castle_q = True
            self.b_castle_k = True
            self.b_castle_q = True

            for rank in range(8):
                for file in range(8):
                    piece = self.board[rank][file]

                    if piece == "K":
                        self.white_king = (rank, file)
                    elif piece == "k":
                        self.black_king = (rank, file)

    def can_attack_king(self) -> bool:
        king_pos = self.black_king if self.white_to_move else self.white_king

        # if has a move attacking king, return true
        for move in self.get_moves():
            if move.new_pos == king_pos:
                return True

        return False

    def get_legal_moves(self) -> list[Move]:
        moves = []

        for move in self.get_moves():
            new_board = self.make_move(move)

            if not new_board.can_attack_king():
                moves.append(move)

        return moves

    def make_move(self, move: Move) -> Board:
        # create and copy board
        board = Board([rank.copy() for rank in self.board], False)
        piece = board.board[move.old_rank][move.old_file]

        # check if promotion
        last_rank = 0 if self.white_to_move else 7
        if move.new_rank == last_rank:
            if piece == "p":
                piece = "q"
            elif piece == "P":
                piece = "Q"

        # move the piece
        board.board[move.new_rank][move.new_file] = piece
        board.board[move.old_rank][move.old_file] = ""

        # update additional information
        board.white_to_move = not self.white_to_move
        board.last_move = move
        board.white_king = self.white_king
        board.black_king = self.black_king

        # update king location if it moved
        if piece == "K":
            board.white_king = move.new_pos
        elif piece == "k":
            board.black_king = move.new_pos

        return board

    def can_move(
        self, rank: int, file: int, can_attack: bool, must_attack: bool = False
    ) -> bool:
        # check if the position is not on the board
        if not (0 <= rank <= 7 and 0 <= file <= 7):
            return False  # position is off the board

        piece = self.board[rank][file]

        # if there is no piece there
        if not piece:
            # return false if must_attack, otherwise true
            return not must_attack

        if can_attack or must_attack:
            # return true if the piece on the square is a different colour
            return self.white_to_move != piece.isupper()

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

                    # diagonal attack left
                    if self.can_move(rank + offset, file - 1, True, True):
                        moves.append(Move(rank, file, rank + offset, file - 1))

                    # diagonal attack right
                    if self.can_move(rank + offset, file + 1, True, True):
                        moves.append(Move(rank, file, rank + offset, file + 1))

                    # move one square up
                    if self.can_move(rank + offset, file, False):
                        moves.append(Move(rank, file, rank + offset, file))

                        # if on first rank, move two squares up
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
