import time
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

    def search(self, board: Board):
        current_time = time.time()

        eval, move = self.minimax(board, 3)
        if eval > 0:
            print(f"White is up {round(eval/100, 2)} pieces!")
        else:
            print(f"Black is up {round(-eval/100, 2)} pieces!")

        print(f"Computer Move Time: {round(time.time()-current_time, 3)}\n")

        return move

    def minimax(self, board: Board, depth: int) -> tuple[int, Move | None]:
        if depth == 0:
            return self.evaluate(board), None

        if board.white_to_move:
            max_eval = -INFINITY
            max_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)
                eval = self.minimax(child, depth - 1)[0]

                if eval >= max_eval:
                    max_eval = eval
                    max_move = move

            return max_eval, max_move

        else:
            min_eval = INFINITY
            min_move = None

            for move in board.get_legal_moves():
                child = board.make_move(move)
                eval = self.minimax(child, depth - 1)[0]

                if eval <= min_eval:
                    min_eval = eval
                    min_move = move

            return min_eval, min_move

    def evaluate(self, board: Board) -> int:
        score = 0

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
