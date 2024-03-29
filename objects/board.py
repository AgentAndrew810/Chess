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
            if self.make_move(move).can_attack_king():
                continue

            if move.castling_type:
                # create a board with the opponent to move
                new_board = self.make_move(Move(0, 0, 0, 0))

                # if the opponent can attack the king, skip move
                # since you can't castle in check
                if new_board.can_attack_king():
                    continue

                # create a board with the king doing the first move
                if move.castling_type == "K":
                    new_board = self.make_move(Move(7, 4, 7, 5))
                elif move.castling_type == "Q":
                    new_board = self.make_move(Move(7, 4, 7, 2))
                elif move.castling_type == "k":
                    new_board = self.make_move(Move(0, 4, 0, 6))
                else:
                    new_board = self.make_move(Move(0, 4, 0, 2))

                # if the opponent can attack the king, skip move
                # since you can't move through a check in castling
                if new_board.can_attack_king():
                    continue

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
        board.last_move = move
        board.white_to_move = not self.white_to_move
        board.white_king = self.white_king
        board.black_king = self.black_king

        # set default castle rights
        board.w_castle_k = self.w_castle_k
        board.w_castle_q = self.w_castle_q
        board.b_castle_k = self.b_castle_k
        board.b_castle_q = self.b_castle_q

        castling = move.castling_type
        if castling:
            if castling == "K":
                board.board[7][5] = "R"
                board.board[7][7] = ""
            elif castling == "Q":
                board.board[7][3] = "R"
                board.board[7][0] = ""
            elif castling == "k":
                board.board[0][5] = "r"
                board.board[0][7] = ""
            elif castling == "q":
                board.board[0][3] = "r"
                board.board[0][0] = ""

        # update king location and castle rights if king moved
        if piece == "K":
            board.white_king = move.new_pos
            board.w_castle_k = False
            board.w_castle_q = False
        elif piece == "k":
            board.black_king = move.new_pos
            board.b_castle_k = False
            board.b_castle_q = False

        # update castle rights if rooks moved
        elif piece == "R":
            if move.old_pos == (7, 7):
                board.w_castle_k = False
            elif move.old_pos == (7, 0):
                board.w_castle_q = False

        elif piece == "r":
            if move.old_pos == (0, 7):
                board.b_castle_k = False
            elif move.old_pos == (0, 0):
                board.b_castle_q = False

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

                elif piece.upper() == "B":  # bishop
                    moves.extend(self.get_piece_moves(rank, file, D_OFFSETS, True))

                elif piece.upper() == "R":  # rook
                    moves.extend(self.get_piece_moves(rank, file, C_OFFSETS, True))

                elif piece.upper() == "Q":  # queen
                    moves.extend(
                        self.get_piece_moves(rank, file, C_OFFSETS + D_OFFSETS, True)
                    )

                elif piece.upper() == "K":  # king
                    moves.extend(
                        self.get_piece_moves(rank, file, C_OFFSETS + D_OFFSETS, False)
                    )

                    # castling
                    if piece == "K" and (rank, file) == (7, 4):
                        if self.w_castle_k:
                            if (
                                not self.board[7][5]
                                and not self.board[7][6]
                                and self.board[7][7] == "R"
                            ):
                                moves.append(Move(rank, file, rank, file + 2, "K"))

                        if self.w_castle_q:
                            if (
                                not self.board[7][3]
                                and not self.board[7][2]
                                and not self.board[7][1]
                                and self.board[7][0] == "R"
                            ):
                                moves.append(Move(rank, file, rank, file - 2, "Q"))

                    elif piece == "k" and (rank, file) == (0, 4):
                        if self.b_castle_k:
                            if (
                                not self.board[0][5]
                                and not self.board[0][6]
                                and self.board[0][7] == "r"
                            ):
                                moves.append(Move(rank, file, rank, file + 2, "k"))

                        if self.b_castle_q:
                            if (
                                not self.board[0][3]
                                and not self.board[0][2]
                                and not self.board[0][1]
                                and self.board[0][0] == "r"
                            ):
                                moves.append(Move(rank, file, rank, file - 2, "q"))

        return moves

    def get_piece_moves(
        self, rank: int, file: int, offsets: list[tuple[int, int]], sliding: bool
    ) -> list[Move]:
        moves = []

        for offset in offsets:
            # set the initial position to adding the offset
            new_rank, new_file = rank + offset[0], file + offset[1]

            # if the piece can slide, continue adding the move while it can
            while self.can_move(new_rank, new_file, True):
                moves.append(Move(rank, file, new_rank, new_file))

                # if you hit a piece, or not a sliding piece, exit loop
                if self.board[new_rank][new_file] or not sliding:
                    break

                # add new offset
                new_rank, new_file = new_rank + offset[0], new_file + offset[1]

        return moves
