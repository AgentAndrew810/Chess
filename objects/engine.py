from objects.board import Board
from objects.move import Move
from constants import PIECE_VALUES, PIECE_TABLES, INFINITY


class Engine:
    def __init__(self) -> None:
        self.WHITE_PIECE_TABLES = PIECE_TABLES
        self.BLACK_PIECE_TABLES = {}

        # reverse the order of the outer list in each table for black
        for piece, table in PIECE_TABLES.items():
            reversed_table = table[::-1]
            self.BLACK_PIECE_TABLES[piece.lower()] = reversed_table

    def search(self, board: Board) -> Move | None:
        eval, move = self.minimax(board, 3, -INFINITY, INFINITY)

        if eval > 0:
            print(f"White is up {round(eval/100, 2)} pieces!")
        else:
            print(f"Black is up {round(-eval/100, 2)} pieces!")

        return move

    def minimax(
        self, board: Board, depth: int, alpha: int, beta: int
    ) -> tuple[int, Move | None]:
        if depth == 0:
            return self.evaluate(board), None

        if board.white_to_move:
            max_eval = -INFINITY
            best_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)
                eval = self.minimax(child, depth - 1, alpha, beta)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if alpha >= beta:
                    break

            return max_eval, best_move

        else:
            min_eval = INFINITY
            best_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)
                eval = self.minimax(child, depth - 1, alpha, beta)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move

    def evaluate(self, board: Board) -> int:
        score = 0

        # add or remove 50 points for being able to castle
        if board.w_castle_k or board.w_castle_q:
            score += 50

        if board.b_castle_k or board.b_castle_q:
            score -= 50

        for rank in range(8):
            for file in range(8):
                piece = board.board[rank][file]

                # skip blank squares
                if not piece:
                    continue

                if piece.isupper():
                    score += PIECE_VALUES[piece]
                    score += self.WHITE_PIECE_TABLES[piece][rank][file]
                else:
                    score -= PIECE_VALUES[piece.upper()]
                    score -= self.BLACK_PIECE_TABLES[piece][rank][file]

        return score

        # for rank in range(8):
        #     for file in range(8):
        #         piece = board.board[rank][file]

        #         # skip blank squares
        #         if not piece:
        #             continue

        #         # get 1 if white, else -1
        #         plus_minus = 1 if piece.isupper() else -1
        #         piece = piece.upper()

        #         # add or subtract the value of the piece
        #         score += plus_minus * PIECE_VALUES[piece]

        #         if piece.isupper():
        #             score += PIECE_TABLES[piece][rank][file]

        #         else:
        #             score -= PIECE_TABLES[piece][rank][file]

        #         # add points based on position on board
        #         if piece == "P":
        #             if plus_minus == 1:
        #                 score += PAWN_TABLE_WHITE[rank][file]
        #             else:
        #                 score -= PAWN_TABLE_BLACK[rank][file]

        #         elif piece == "N":
        #             score += plus_minus * KNIGHTS_TABLE[rank][file]

        #         elif piece == "B":
        #             score += plus_minus * BISHOPS_TABLE[rank][file]

        #         elif piece == "R":
        #             score += plus_minus * ROOKS_TABLE[rank][file]

        #         elif piece == "Q":
        #             score += plus_minus * QUEEN_TABLE[rank][file]

        #         elif piece == "K":
        #             if plus_minus == 1:
        #                 score += KING_TABLE_WHITE[rank][file]
        #             else:
        #                 score -= KING_TABLE_BLACK[rank][file]

        # return score
